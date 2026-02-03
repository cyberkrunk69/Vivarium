#!/usr/bin/env python3
"""
Remote Execution Relay
Runs on swarm server to relay commands to user machines.
"""

import asyncio
import websockets
import json
import logging
import uuid
import hmac
import hashlib
from datetime import datetime, timedelta
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RemoteExecutionRelay:
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.connected_clients = {}  # machine_id -> client_info
        self.pending_commands = {}   # request_id -> command_info
        self.client_websockets = {}  # websocket -> machine_id
        
        # Command timeout
        self.command_timeout = 30  # seconds
    
    async def start_server(self):
        """Start the WebSocket server"""
        logger.info(f"Starting remote execution relay on {self.host}:{self.port}")
        
        async def handle_client(websocket, path):
            await self.handle_client_connection(websocket, path)
        
        start_server = websockets.serve(handle_client, self.host, self.port)
        await start_server
        logger.info(f"Remote execution relay running on ws://{self.host}:{self.port}")
    
    async def handle_client_connection(self, websocket, path):
        """Handle new client connections"""
        try:
            machine_id = None
            
            async for message in websocket:
                try:
                    data = json.loads(message)
                    
                    if data.get("type") == "register":
                        machine_id = await self._handle_registration(websocket, data)
                        if machine_id:
                            self.client_websockets[websocket] = machine_id
                    else:
                        await self._handle_client_message(websocket, data)
                        
                except json.JSONDecodeError:
                    logger.error("Invalid JSON from client")
                except Exception as e:
                    logger.error(f"Client message error: {e}")
        
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client disconnected: {machine_id}")
        except Exception as e:
            logger.error(f"Client connection error: {e}")
        finally:
            await self._cleanup_client(websocket)
    
    async def _handle_registration(self, websocket, data):
        """Handle client registration"""
        machine_id = data.get("machine_id")
        auth_token = data.get("auth_token")
        platform = data.get("platform")
        hostname = data.get("hostname")
        capabilities = data.get("capabilities", [])
        
        if not machine_id or not auth_token:
            await self._send_to_client(websocket, {
                "type": "error",
                "message": "Missing machine_id or auth_token"
            })
            return None
        
        # Store client info
        client_info = {
            "websocket": websocket,
            "machine_id": machine_id,
            "auth_token": auth_token,
            "platform": platform,
            "hostname": hostname,
            "capabilities": capabilities,
            "connected_at": datetime.now(),
            "last_seen": datetime.now()
        }
        
        self.connected_clients[machine_id] = client_info
        
        await self._send_to_client(websocket, {
            "type": "registered",
            "machine_id": machine_id
        })
        
        logger.info(f"Registered client: {hostname} ({platform}) - {machine_id}")
        return machine_id
    
    async def _handle_client_message(self, websocket, data):
        """Handle messages from registered clients"""
        msg_type = data.get("type")
        
        if msg_type == "command_result":
            await self._handle_command_result(data)
        elif msg_type == "pong":
            await self._handle_pong(websocket, data)
        else:
            logger.warning(f"Unknown client message type: {msg_type}")
    
    async def _handle_command_result(self, data):
        """Handle command execution results"""
        request_id = data.get("request_id")
        
        if request_id in self.pending_commands:
            command_info = self.pending_commands[request_id]
            
            # Store result
            command_info["result"] = data
            command_info["completed_at"] = datetime.now()
            
            # Notify any waiting coroutines
            if "result_future" in command_info:
                command_info["result_future"].set_result(data)
            
            logger.info(f"Command {request_id} completed: {data.get('success')}")
        else:
            logger.warning(f"Received result for unknown command: {request_id}")
    
    async def _handle_pong(self, websocket, data):
        """Handle pong response"""
        machine_id = self.client_websockets.get(websocket)
        if machine_id and machine_id in self.connected_clients:
            self.connected_clients[machine_id]["last_seen"] = datetime.now()
    
    async def _cleanup_client(self, websocket):
        """Clean up disconnected client"""
        machine_id = self.client_websockets.pop(websocket, None)
        if machine_id and machine_id in self.connected_clients:
            del self.connected_clients[machine_id]
            logger.info(f"Cleaned up client: {machine_id}")
    
    async def _send_to_client(self, websocket, data):
        """Send data to specific client"""
        try:
            await websocket.send(json.dumps(data))
        except Exception as e:
            logger.error(f"Failed to send to client: {e}")
    
    def _generate_command_signature(self, command_data, auth_token):
        """Generate HMAC signature for command"""
        return hmac.new(
            auth_token.encode(),
            json.dumps(command_data, sort_keys=True).encode(),
            hashlib.sha256
        ).hexdigest()
    
    async def execute_remote_command(self, machine_id, command, args=None, timeout=None):
        """Execute command on remote machine"""
        if machine_id not in self.connected_clients:
            raise ValueError(f"Machine {machine_id} not connected")
        
        client_info = self.connected_clients[machine_id]
        websocket = client_info["websocket"]
        auth_token = client_info["auth_token"]
        
        if command not in client_info["capabilities"]:
            raise ValueError(f"Machine {machine_id} does not support command '{command}'")
        
        request_id = str(uuid.uuid4())
        command_data = {
            "command": command,
            "args": args or [],
            "request_id": request_id
        }
        
        signature = self._generate_command_signature(command_data, auth_token)
        
        message = {
            "type": "command",
            "request_id": request_id,
            "command": command,
            "args": args or [],
            "signature": signature
        }
        
        # Store pending command
        result_future = asyncio.Future()
        self.pending_commands[request_id] = {
            "machine_id": machine_id,
            "command": command,
            "args": args,
            "sent_at": datetime.now(),
            "result_future": result_future
        }
        
        try:
            await self._send_to_client(websocket, message)
            
            # Wait for result with timeout
            timeout = timeout or self.command_timeout
            result = await asyncio.wait_for(result_future, timeout=timeout)
            
            return result
            
        except asyncio.TimeoutError:
            raise TimeoutError(f"Command {request_id} timed out after {timeout}s")
        finally:
            # Clean up pending command
            self.pending_commands.pop(request_id, None)
    
    def get_connected_machines(self):
        """Get list of connected machines"""
        machines = []
        for machine_id, client_info in self.connected_clients.items():
            machines.append({
                "machine_id": machine_id,
                "platform": client_info["platform"],
                "hostname": client_info["hostname"],
                "capabilities": client_info["capabilities"],
                "connected_at": client_info["connected_at"].isoformat(),
                "last_seen": client_info["last_seen"].isoformat()
            })
        return machines
    
    def find_machine_by_hostname(self, hostname):
        """Find machine by hostname"""
        for machine_id, client_info in self.connected_clients.items():
            if client_info["hostname"].lower() == hostname.lower():
                return machine_id
        return None
    
    async def ping_machine(self, machine_id):
        """Ping a specific machine"""
        if machine_id not in self.connected_clients:
            return False
        
        client_info = self.connected_clients[machine_id]
        websocket = client_info["websocket"]
        
        try:
            await self._send_to_client(websocket, {
                "type": "ping",
                "request_id": str(uuid.uuid4())
            })
            return True
        except:
            return False

# Integration with main orchestrator
class RemoteExecutionIntegration:
    """Integration layer for the main orchestrator"""
    
    def __init__(self, relay):
        self.relay = relay
    
    async def handle_user_command(self, user_session, command_text):
        """Handle user command that might need remote execution"""
        
        # Parse command for remote execution indicators
        if "open my browser" in command_text.lower():
            return await self._handle_browser_command(user_session)
        elif "open" in command_text.lower() and ("file" in command_text.lower() or "folder" in command_text.lower()):
            return await self._handle_file_command(user_session, command_text)
        elif "run" in command_text.lower() or "execute" in command_text.lower():
            return await self._handle_run_command(user_session, command_text)
        
        return None  # Not a remote execution command
    
    async def _handle_browser_command(self, user_session):
        """Handle browser opening command"""
        machine_id = self._get_user_machine(user_session)
        if not machine_id:
            return {"error": "Your machine is not connected"}
        
        try:
            result = await self.relay.execute_remote_command(machine_id, "browser")
            return {"success": True, "message": f"Browser opened on {machine_id}"}
        except Exception as e:
            return {"error": f"Failed to open browser: {e}"}
    
    async def _handle_file_command(self, user_session, command_text):
        """Handle file/folder opening command"""
        machine_id = self._get_user_machine(user_session)
        if not machine_id:
            return {"error": "Your machine is not connected"}
        
        # Extract file path from command (simple parsing)
        import re
        path_match = re.search(r'"([^"]+)"|\'([^\']+)\'|\s([^\s]+\.[^\s]+)', command_text)
        path = path_match.group(1) or path_match.group(2) or path_match.group(3) if path_match else ""
        
        try:
            result = await self.relay.execute_remote_command(machine_id, "open", [path])
            return {"success": True, "message": f"Opened {path} on {machine_id}"}
        except Exception as e:
            return {"error": f"Failed to open file: {e}"}
    
    async def _handle_run_command(self, user_session, command_text):
        """Handle general run command"""
        machine_id = self._get_user_machine(user_session)
        if not machine_id:
            return {"error": "Your machine is not connected"}
        
        # Extract application name (basic parsing)
        app_name = command_text.replace("run", "").replace("execute", "").strip()
        
        try:
            result = await self.relay.execute_remote_command(machine_id, "app", [app_name])
            return {"success": True, "message": f"Launched {app_name} on {machine_id}"}
        except Exception as e:
            return {"error": f"Failed to launch application: {e}"}
    
    def _get_user_machine(self, user_session):
        """Get machine ID for user session"""
        # This would integrate with your session management
        # For now, assume single machine per user
        machines = self.relay.get_connected_machines()
        return machines[0]["machine_id"] if machines else None

async def main():
    """Main server entry point"""
    relay = RemoteExecutionRelay()
    
    print("Starting Remote Execution Relay Server...")
    print("Clients can connect to ws://localhost:8765/remote_exec")
    
    await relay.start_server()
    
    # Keep server running
    try:
        await asyncio.Future()  # Run forever
    except KeyboardInterrupt:
        print("Shutting down...")

if __name__ == "__main__":
    asyncio.run(main())