#!/usr/bin/env python3
"""
Remote Execution Client
Runs on user's machine to receive and execute commands from the swarm.
"""

import asyncio
import websockets
import json
import subprocess
import platform
import uuid
import hashlib
import hmac
import os
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RemoteExecutionClient:
    def __init__(self, server_host="localhost", server_port=8765, auth_token=None):
        self.server_host = server_host
        self.server_port = server_port
        self.auth_token = auth_token or self._generate_machine_token()
        self.machine_id = self._get_machine_id()
        self.websocket = None
        self.running = False
        
        # Command whitelist for security
        self.allowed_commands = {
            'open': self._handle_open_command,
            'ls': self._handle_ls_command,
            'pwd': self._handle_pwd_command,
            'echo': self._handle_echo_command,
            'browser': self._handle_browser_command,
            'file': self._handle_file_command,
            'app': self._handle_app_command,
        }
    
    def _get_machine_id(self):
        """Generate unique machine identifier"""
        import uuid
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                       for elements in range(0,2*6,2)][::-1])
        return f"{platform.system()}-{platform.node()}-{mac}"
    
    def _generate_machine_token(self):
        """Generate auth token based on machine characteristics"""
        machine_data = f"{platform.system()}{platform.node()}{uuid.getnode()}"
        return hashlib.sha256(machine_data.encode()).hexdigest()[:16]
    
    def _verify_command_signature(self, command_data, signature):
        """Verify command came from authorized server"""
        expected = hmac.new(
            self.auth_token.encode(), 
            json.dumps(command_data, sort_keys=True).encode(), 
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)
    
    async def connect(self):
        """Connect to the swarm server"""
        uri = f"ws://{self.server_host}:{self.server_port}/remote_exec"
        
        try:
            self.websocket = await websockets.connect(uri)
            logger.info(f"Connected to swarm server at {uri}")
            
            # Send registration
            await self.websocket.send(json.dumps({
                "type": "register",
                "machine_id": self.machine_id,
                "auth_token": self.auth_token,
                "platform": platform.system(),
                "hostname": platform.node(),
                "capabilities": list(self.allowed_commands.keys())
            }))
            
            self.running = True
            return True
            
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False
    
    async def listen(self):
        """Listen for commands from server"""
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    await self._handle_message(data)
                except json.JSONDecodeError:
                    logger.error("Invalid JSON received")
                except Exception as e:
                    logger.error(f"Message handling error: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info("Connection closed by server")
        except Exception as e:
            logger.error(f"Listen error: {e}")
        finally:
            self.running = False
    
    async def _handle_message(self, data):
        """Process incoming command messages"""
        msg_type = data.get("type")
        
        if msg_type == "command":
            await self._execute_command(data)
        elif msg_type == "ping":
            await self._send_response({"type": "pong", "request_id": data.get("request_id")})
        elif msg_type == "registered":
            logger.info(f"Successfully registered with server")
        else:
            logger.warning(f"Unknown message type: {msg_type}")
    
    async def _execute_command(self, command_data):
        """Execute a validated command"""
        request_id = command_data.get("request_id")
        command = command_data.get("command")
        args = command_data.get("args", [])
        signature = command_data.get("signature")
        
        # Verify command signature
        if not self._verify_command_signature({
            "command": command, 
            "args": args, 
            "request_id": request_id
        }, signature):
            await self._send_error(request_id, "Invalid command signature")
            return
        
        # Check if command is allowed
        if command not in self.allowed_commands:
            await self._send_error(request_id, f"Command '{command}' not allowed")
            return
        
        try:
            result = await self.allowed_commands[command](args)
            await self._send_response({
                "type": "command_result",
                "request_id": request_id,
                "success": True,
                "result": result
            })
        except Exception as e:
            await self._send_error(request_id, str(e))
    
    async def _handle_open_command(self, args):
        """Handle 'open' command - open files/URLs"""
        if not args:
            raise ValueError("No target specified for open command")
        
        target = args[0]
        
        if platform.system() == "Darwin":  # macOS
            subprocess.run(["open", target])
        elif platform.system() == "Windows":
            os.startfile(target)
        else:  # Linux
            subprocess.run(["xdg-open", target])
        
        return f"Opened: {target}"
    
    async def _handle_browser_command(self, args):
        """Handle browser-specific commands"""
        url = args[0] if args else "https://google.com"
        
        if platform.system() == "Darwin":
            subprocess.run(["open", "-a", "Safari", url])
        elif platform.system() == "Windows":
            subprocess.run(["start", url], shell=True)
        else:
            subprocess.run(["xdg-open", url])
        
        return f"Opened browser to: {url}"
    
    async def _handle_ls_command(self, args):
        """Handle directory listing"""
        path = args[0] if args else "."
        try:
            items = os.listdir(path)
            return {"path": path, "items": items}
        except PermissionError:
            raise ValueError(f"Permission denied: {path}")
    
    async def _handle_pwd_command(self, args):
        """Handle present working directory"""
        return {"pwd": os.getcwd()}
    
    async def _handle_echo_command(self, args):
        """Handle echo command"""
        return {"echo": " ".join(args)}
    
    async def _handle_file_command(self, args):
        """Handle file operations (read only for security)"""
        if not args:
            raise ValueError("No file specified")
        
        file_path = args[0]
        action = args[1] if len(args) > 1 else "info"
        
        if action == "info":
            path = Path(file_path)
            return {
                "exists": path.exists(),
                "is_file": path.is_file(),
                "is_dir": path.is_dir(),
                "size": path.stat().st_size if path.exists() else None
            }
        else:
            raise ValueError(f"File action '{action}' not allowed")
    
    async def _handle_app_command(self, args):
        """Handle application launching"""
        if not args:
            raise ValueError("No application specified")
        
        app_name = args[0]
        
        if platform.system() == "Darwin":
            subprocess.run(["open", "-a", app_name])
        elif platform.system() == "Windows":
            subprocess.run([app_name], shell=True)
        else:
            subprocess.run([app_name])
        
        return f"Launched application: {app_name}"
    
    async def _send_response(self, data):
        """Send response back to server"""
        if self.websocket:
            await self.websocket.send(json.dumps(data))
    
    async def _send_error(self, request_id, error_message):
        """Send error response"""
        await self._send_response({
            "type": "command_result",
            "request_id": request_id,
            "success": False,
            "error": error_message
        })
    
    async def disconnect(self):
        """Disconnect from server"""
        self.running = False
        if self.websocket:
            await self.websocket.close()

async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Remote Execution Client")
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--port", type=int, default=8765, help="Server port")
    parser.add_argument("--token", help="Auth token (auto-generated if not provided)")
    
    args = parser.parse_args()
    
    client = RemoteExecutionClient(args.host, args.port, args.token)
    
    print(f"Machine ID: {client.machine_id}")
    print(f"Auth Token: {client.auth_token}")
    print(f"Connecting to {args.host}:{args.port}...")
    
    if await client.connect():
        print("Connected! Listening for commands...")
        try:
            await client.listen()
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            await client.disconnect()
    else:
        print("Failed to connect to server")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())