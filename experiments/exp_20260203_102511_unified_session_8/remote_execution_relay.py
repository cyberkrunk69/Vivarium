#!/usr/bin/env python3
"""
Remote Execution Relay - Runs on swarm server
Routes commands to user machines and responses back to users
"""

import asyncio
import websockets
import json
import uuid
import time
import hmac
import hashlib
import logging
from typing import Dict, Set, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class RemoteMachine:
    machine_id: str
    session_token: str
    websocket: websockets.WebSocketServerProtocol
    hostname: str
    platform: str
    user: str
    connected_at: datetime
    last_seen: datetime

@dataclass
class PendingCommand:
    command_id: str
    user_session: str
    machine_id: str
    command: str
    args: list
    created_at: datetime
    timeout: datetime

class RemoteExecutionRelay:
    def __init__(self, port: int = 8765):
        self.port = port
        self.machines: Dict[str, RemoteMachine] = {}
        self.user_sessions: Dict[str, websockets.WebSocketServerProtocol] = {}
        self.pending_commands: Dict[str, PendingCommand] = {}
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Security
        self.secret = "claude-swarm-2026"
        self.max_command_timeout = timedelta(minutes=5)
        
        # Start cleanup task
        asyncio.create_task(self._cleanup_task())
    
    def _verify_auth_token(self, machine_id: str, timestamp: float, session_token: str, auth_token: str) -> bool:
        """Verify HMAC authentication token"""
        # Check timestamp is recent (within 5 minutes)
        if abs(time.time() - timestamp) > 300:
            return False
        
        expected_message = f"{machine_id}:{timestamp}:{session_token}"
        expected_token = hmac.new(self.secret.encode(), expected_message.encode(), hashlib.sha256).hexdigest()
        
        return hmac.compare_digest(expected_token, auth_token)
    
    async def _cleanup_task(self):
        """Periodically clean up expired commands and dead connections"""
        while True:
            await asyncio.sleep(30)  # Run every 30 seconds
            
            now = datetime.now()
            
            # Clean expired commands
            expired = [cmd_id for cmd_id, cmd in self.pending_commands.items() 
                      if now > cmd.timeout]
            
            for cmd_id in expired:
                cmd = self.pending_commands.pop(cmd_id)
                self.logger.warning(f"Command {cmd_id} timed out")
                
                # Notify user session if still connected
                if cmd.user_session in self.user_sessions:
                    await self._send_to_user(cmd.user_session, {
                        "type": "command_result",
                        "command_id": cmd_id,
                        "success": False,
                        "result": "Command timed out",
                        "machine_id": cmd.machine_id
                    })
    
    async def handle_connection(self, websocket, path):
        """Handle new WebSocket connection"""
        self.logger.info(f"New connection from {websocket.remote_address}")
        
        if path == "/remote_exec":
            await self._handle_machine_connection(websocket)
        elif path == "/user_session":
            await self._handle_user_connection(websocket)
        else:
            await websocket.close(1000, "Unknown endpoint")
    
    async def _handle_machine_connection(self, websocket):
        """Handle connection from remote execution client"""
        machine_id = None
        
        try:
            # Wait for registration
            registration_msg = await asyncio.wait_for(websocket.recv(), timeout=30)
            registration = json.loads(registration_msg)
            
            if registration.get("type") != "register":
                await websocket.close(1000, "Expected registration message")
                return
            
            # Verify authentication
            machine_id = registration.get("machine_id")
            timestamp = registration.get("timestamp")
            session_token = registration.get("session_token")
            auth_token = registration.get("auth_token")
            
            if not self._verify_auth_token(machine_id, timestamp, session_token, auth_token):
                await websocket.close(1000, "Authentication failed")
                return
            
            # Register machine
            machine = RemoteMachine(
                machine_id=machine_id,
                session_token=session_token,
                websocket=websocket,
                hostname=registration.get("hostname", "unknown"),
                platform=registration.get("platform", "unknown"),
                user=registration.get("user", "unknown"),
                connected_at=datetime.now(),
                last_seen=datetime.now()
            )
            
            self.machines[machine_id] = machine
            self.logger.info(f"Registered machine {machine_id} ({machine.hostname})")
            
            # Send confirmation
            await websocket.send(json.dumps({
                "type": "registered",
                "machine_id": machine_id
            }))
            
            # Listen for responses
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self._handle_machine_message(machine_id, data)
                except json.JSONDecodeError:
                    self.logger.error(f"Invalid JSON from machine {machine_id}")
                except Exception as e:
                    self.logger.error(f"Error handling machine message: {e}")
                    
        except asyncio.TimeoutError:
            self.logger.warning("Machine registration timeout")
        except websockets.exceptions.ConnectionClosed:
            self.logger.info(f"Machine {machine_id} disconnected")
        except Exception as e:
            self.logger.error(f"Error in machine connection: {e}")
        finally:
            # Clean up
            if machine_id and machine_id in self.machines:
                del self.machines[machine_id]
                self.logger.info(f"Machine {machine_id} removed")
    
    async def _handle_user_connection(self, websocket):
        """Handle connection from user session (Claude interface)"""
        session_id = str(uuid.uuid4())
        self.user_sessions[session_id] = websocket
        
        self.logger.info(f"User session {session_id} connected")
        
        try:
            # Send machine list
            await self._send_machine_list(session_id)
            
            # Listen for commands
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self._handle_user_message(session_id, data)
                except json.JSONDecodeError:
                    self.logger.error(f"Invalid JSON from user {session_id}")
                except Exception as e:
                    self.logger.error(f"Error handling user message: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            self.logger.info(f"User session {session_id} disconnected")
        except Exception as e:
            self.logger.error(f"Error in user connection: {e}")
        finally:
            # Clean up
            if session_id in self.user_sessions:
                del self.user_sessions[session_id]
    
    async def _handle_machine_message(self, machine_id: str, data: Dict[str, Any]):
        """Handle message from remote machine"""
        msg_type = data.get("type")
        
        if msg_type == "result":
            # Command result from machine
            command_id = data.get("command_id")
            success = data.get("success", False)
            result = data.get("result", "")
            
            if command_id in self.pending_commands:
                cmd = self.pending_commands.pop(command_id)
                
                # Send result back to user session
                if cmd.user_session in self.user_sessions:
                    await self._send_to_user(cmd.user_session, {
                        "type": "command_result",
                        "command_id": command_id,
                        "success": success,
                        "result": result,
                        "machine_id": machine_id
                    })
            
            # Update last seen
            if machine_id in self.machines:
                self.machines[machine_id].last_seen = datetime.now()
    
    async def _handle_user_message(self, session_id: str, data: Dict[str, Any]):
        """Handle message from user session"""
        msg_type = data.get("type")
        
        if msg_type == "execute_command":
            # Execute command on remote machine
            target_machine = data.get("machine_id")
            command = data.get("command", "")
            args = data.get("args", [])
            
            if target_machine not in self.machines:
                await self._send_to_user(session_id, {
                    "type": "error",
                    "message": f"Machine {target_machine} not connected"
                })
                return
            
            # Create command
            command_id = str(uuid.uuid4())
            pending_cmd = PendingCommand(
                command_id=command_id,
                user_session=session_id,
                machine_id=target_machine,
                command=command,
                args=args,
                created_at=datetime.now(),
                timeout=datetime.now() + self.max_command_timeout
            )
            
            self.pending_commands[command_id] = pending_cmd
            
            # Send to machine
            machine = self.machines[target_machine]
            try:
                await machine.websocket.send(json.dumps({
                    "type": "execute",
                    "command_id": command_id,
                    "command": command,
                    "args": args
                }))
                
                # Confirm command sent
                await self._send_to_user(session_id, {
                    "type": "command_sent",
                    "command_id": command_id,
                    "machine_id": target_machine
                })
                
            except Exception as e:
                # Failed to send to machine
                del self.pending_commands[command_id]
                await self._send_to_user(session_id, {
                    "type": "error", 
                    "message": f"Failed to send command to machine: {e}"
                })
        
        elif msg_type == "list_machines":
            await self._send_machine_list(session_id)
    
    async def _send_to_user(self, session_id: str, data: Dict[str, Any]):
        """Send message to user session"""
        if session_id in self.user_sessions:
            try:
                await self.user_sessions[session_id].send(json.dumps(data))
            except Exception as e:
                self.logger.error(f"Failed to send to user {session_id}: {e}")
    
    async def _send_machine_list(self, session_id: str):
        """Send list of connected machines to user"""
        machine_list = []
        for machine_id, machine in self.machines.items():
            machine_list.append({
                "machine_id": machine_id,
                "hostname": machine.hostname,
                "platform": machine.platform,
                "user": machine.user,
                "connected_at": machine.connected_at.isoformat(),
                "last_seen": machine.last_seen.isoformat()
            })
        
        await self._send_to_user(session_id, {
            "type": "machine_list",
            "machines": machine_list
        })
    
    # Public API for orchestrator integration
    async def execute_remote_command(self, machine_id: str, command: str, args: list = None) -> Dict[str, Any]:
        """Execute command on remote machine (for orchestrator use)"""
        if args is None:
            args = []
        
        if machine_id not in self.machines:
            return {
                "success": False,
                "error": f"Machine {machine_id} not connected"
            }
        
        # Create command
        command_id = str(uuid.uuid4())
        result_event = asyncio.Event()
        result_data = {}
        
        # Store result handler
        async def result_handler(data):
            result_data.update(data)
            result_event.set()
        
        # Send command
        machine = self.machines[machine_id]
        try:
            await machine.websocket.send(json.dumps({
                "type": "execute",
                "command_id": command_id, 
                "command": command,
                "args": args
            }))
            
            # Wait for result (with timeout)
            try:
                await asyncio.wait_for(result_event.wait(), timeout=60)
                return result_data
            except asyncio.TimeoutError:
                return {
                    "success": False,
                    "error": "Command timeout"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to send command: {e}"
            }
    
    def get_connected_machines(self) -> Dict[str, Dict[str, Any]]:
        """Get list of connected machines"""
        return {
            machine_id: {
                "hostname": machine.hostname,
                "platform": machine.platform,
                "user": machine.user,
                "connected_at": machine.connected_at.isoformat(),
                "last_seen": machine.last_seen.isoformat()
            }
            for machine_id, machine in self.machines.items()
        }

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Remote Execution Relay Server")
    parser.add_argument("--port", type=int, default=8765, help="Server port")
    parser.add_argument("--host", default="0.0.0.0", help="Bind host")
    
    args = parser.parse_args()
    
    relay = RemoteExecutionRelay(args.port)
    
    print(f"Starting remote execution relay on {args.host}:{args.port}")
    print("Endpoints:")
    print(f"  - ws://{args.host}:{args.port}/remote_exec (for client machines)")
    print(f"  - ws://{args.host}:{args.port}/user_session (for user interfaces)")
    
    async with websockets.serve(relay.handle_connection, args.host, args.port):
        try:
            await asyncio.Future()  # Run forever
        except KeyboardInterrupt:
            print("\nShutting down...")

if __name__ == "__main__":
    asyncio.run(main())