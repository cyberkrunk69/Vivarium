#!/usr/bin/env python3
"""
Remote Execution Client - Runs on user's machine
Connects to swarm server and executes commands locally
"""

import asyncio
import websockets
import json
import uuid
import subprocess
import platform
import hashlib
import hmac
import time
import logging
from pathlib import Path
from typing import Optional, Dict, Any

class RemoteExecutionClient:
    def __init__(self, server_host: str = "localhost", server_port: int = 8765):
        self.server_host = server_host
        self.server_port = server_port
        self.machine_id = self._get_machine_id()
        self.session_token = str(uuid.uuid4())
        self.websocket = None
        self.running = False
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Command whitelist for security
        self.allowed_commands = {
            "open": self._cmd_open,
            "list": self._cmd_list, 
            "status": self._cmd_status,
            "ping": self._cmd_ping,
            "browse": self._cmd_browse,
            "show": self._cmd_show,
            "find": self._cmd_find
        }
        
    def _get_machine_id(self) -> str:
        """Generate unique machine identifier"""
        import getmac
        mac = getmac.get_mac_address()
        if mac:
            return hashlib.sha256(f"{mac}-{platform.node()}".encode()).hexdigest()[:16]
        else:
            # Fallback to hostname + platform
            return hashlib.sha256(f"{platform.node()}-{platform.platform()}".encode()).hexdigest()[:16]
    
    def _generate_auth_token(self, timestamp: float, secret: str = "claude-swarm-2026") -> str:
        """Generate HMAC authentication token"""
        message = f"{self.machine_id}:{timestamp}:{self.session_token}"
        return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
    
    async def connect(self):
        """Connect to swarm server"""
        uri = f"ws://{self.server_host}:{self.server_port}/remote_exec"
        
        try:
            self.websocket = await websockets.connect(uri)
            self.logger.info(f"Connected to swarm server at {uri}")
            
            # Send registration message
            timestamp = time.time()
            auth_token = self._generate_auth_token(timestamp)
            
            registration = {
                "type": "register",
                "machine_id": self.machine_id,
                "session_token": self.session_token,
                "timestamp": timestamp,
                "auth_token": auth_token,
                "platform": platform.platform(),
                "hostname": platform.node(),
                "user": Path.home().name
            }
            
            await self.websocket.send(json.dumps(registration))
            self.logger.info(f"Registered machine {self.machine_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to connect: {e}")
            raise
    
    async def listen_for_commands(self):
        """Listen for commands from swarm server"""
        self.running = True
        
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    await self._handle_command(data)
                except json.JSONDecodeError:
                    self.logger.error(f"Invalid JSON received: {message}")
                except Exception as e:
                    self.logger.error(f"Error handling command: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            self.logger.info("Connection to server closed")
        except Exception as e:
            self.logger.error(f"Error in command loop: {e}")
        finally:
            self.running = False
    
    async def _handle_command(self, data: Dict[str, Any]):
        """Handle incoming command from server"""
        cmd_type = data.get("type")
        cmd_id = data.get("command_id", str(uuid.uuid4()))
        
        if cmd_type != "execute":
            return
            
        command = data.get("command", "")
        args = data.get("args", [])
        
        self.logger.info(f"Executing command: {command} {args}")
        
        # Validate command is allowed
        base_cmd = command.split()[0] if command else ""
        
        if base_cmd not in self.allowed_commands:
            await self._send_response(cmd_id, False, f"Command '{base_cmd}' not allowed")
            return
        
        try:
            # Execute the allowed command
            handler = self.allowed_commands[base_cmd]
            result = await handler(command, args)
            
            await self._send_response(cmd_id, True, result)
            
        except Exception as e:
            await self._send_response(cmd_id, False, f"Command failed: {e}")
    
    async def _send_response(self, command_id: str, success: bool, result: str):
        """Send command result back to server"""
        response = {
            "type": "result",
            "command_id": command_id,
            "machine_id": self.machine_id,
            "success": success,
            "result": result,
            "timestamp": time.time()
        }
        
        await self.websocket.send(json.dumps(response))
    
    # Command handlers
    async def _cmd_ping(self, command: str, args: list) -> str:
        """Ping command"""
        return f"pong from {self.machine_id} ({platform.node()})"
    
    async def _cmd_status(self, command: str, args: list) -> str:
        """System status command"""
        return f"Machine: {platform.node()}\nPlatform: {platform.platform()}\nUser: {Path.home().name}\nID: {self.machine_id}"
    
    async def _cmd_open(self, command: str, args: list) -> str:
        """Open file or application"""
        if len(args) == 0:
            target = "browser"  # Default
        else:
            target = " ".join(args)
        
        system = platform.system()
        
        try:
            if system == "Darwin":  # macOS
                if target in ["browser", "web"]:
                    subprocess.run(["open", "-a", "Safari"], check=True)
                    return "Opened Safari browser"
                elif target in ["finder", "files"]:
                    subprocess.run(["open", "."], check=True) 
                    return "Opened Finder"
                else:
                    subprocess.run(["open", target], check=True)
                    return f"Opened {target}"
                    
            elif system == "Windows":
                if target in ["browser", "web"]:
                    subprocess.run(["start", "msedge"], shell=True, check=True)
                    return "Opened Edge browser"
                elif target in ["explorer", "files"]:
                    subprocess.run(["explorer", "."], shell=True, check=True)
                    return "Opened File Explorer"
                else:
                    subprocess.run(["start", target], shell=True, check=True)
                    return f"Opened {target}"
                    
            elif system == "Linux":
                if target in ["browser", "web"]:
                    subprocess.run(["xdg-open", "http://google.com"], check=True)
                    return "Opened default browser"
                elif target in ["files", "folder"]:
                    subprocess.run(["xdg-open", "."], check=True)
                    return "Opened file manager"
                else:
                    subprocess.run(["xdg-open", target], check=True)
                    return f"Opened {target}"
                    
        except subprocess.CalledProcessError as e:
            return f"Failed to open {target}: {e}"
    
    async def _cmd_list(self, command: str, args: list) -> str:
        """List files in directory"""
        target_dir = args[0] if args else "."
        
        try:
            path = Path(target_dir)
            if not path.exists():
                return f"Directory {target_dir} does not exist"
            
            files = [item.name for item in path.iterdir()]
            return f"Files in {target_dir}:\n" + "\n".join(files[:20])  # Limit to 20 items
            
        except Exception as e:
            return f"Failed to list directory: {e}"
    
    async def _cmd_browse(self, command: str, args: list) -> str:
        """Browse to URL"""
        url = args[0] if args else "http://google.com"
        
        try:
            if platform.system() == "Darwin":
                subprocess.run(["open", url], check=True)
            elif platform.system() == "Windows":
                subprocess.run(["start", url], shell=True, check=True)
            else:
                subprocess.run(["xdg-open", url], check=True)
                
            return f"Opened {url} in browser"
            
        except Exception as e:
            return f"Failed to browse to {url}: {e}"
    
    async def _cmd_show(self, command: str, args: list) -> str:
        """Show file contents (limited)"""
        filename = args[0] if args else ""
        
        if not filename:
            return "No filename specified"
        
        try:
            path = Path(filename)
            if not path.exists():
                return f"File {filename} does not exist"
            
            if path.is_dir():
                return f"{filename} is a directory"
            
            # Limit file size
            if path.stat().st_size > 1024 * 10:  # 10KB limit
                return f"File {filename} too large to display"
            
            content = path.read_text(encoding='utf-8', errors='ignore')
            return f"Contents of {filename}:\n{content[:500]}..."  # First 500 chars
            
        except Exception as e:
            return f"Failed to read file: {e}"
    
    async def _cmd_find(self, command: str, args: list) -> str:
        """Find files by pattern"""
        pattern = args[0] if args else "*"
        
        try:
            matches = list(Path(".").glob(f"**/{pattern}"))[:20]  # Limit results
            if not matches:
                return f"No files found matching {pattern}"
            
            return f"Found files matching {pattern}:\n" + "\n".join(str(m) for m in matches)
            
        except Exception as e:
            return f"Failed to search: {e}"
    
    async def disconnect(self):
        """Disconnect from server"""
        self.running = False
        if self.websocket:
            await self.websocket.close()

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Remote Execution Client")
    parser.add_argument("--host", default="localhost", help="Swarm server host")
    parser.add_argument("--port", type=int, default=8765, help="Swarm server port")
    
    args = parser.parse_args()
    
    client = RemoteExecutionClient(args.host, args.port)
    
    try:
        await client.connect()
        print(f"Connected to swarm at {args.host}:{args.port}")
        print(f"Machine ID: {client.machine_id}")
        print("Listening for commands... (Ctrl+C to exit)")
        
        await client.listen_for_commands()
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())