#!/usr/bin/env python3
"""
WebSocket Server for Real-time LAN Session Updates
"""

import asyncio
import websockets
import json
import logging
from typing import Dict, Set
from datetime import datetime
import threading
from lan_session_manager import get_session_manager

logger = logging.getLogger(__name__)

class SessionWebSocketServer:
    """WebSocket server for real-time session updates"""

    def __init__(self, host="0.0.0.0", port=8765):
        self.host = host
        self.port = port
        self.clients: Dict[str, Set[websockets.WebSocketServerProtocol]] = {}
        self.session_manager = get_session_manager()
        self.server = None

    async def register_client(self, websocket, client_ip: str):
        """Register a new WebSocket client"""
        if client_ip not in self.clients:
            self.clients[client_ip] = set()

        self.clients[client_ip].add(websocket)

        # Register with session manager
        self.session_manager.register_websocket(client_ip, websocket)

        logger.info(f"WebSocket client registered: {client_ip}")

        # Send initial dashboard data
        try:
            dashboard_data = self.session_manager.get_user_dashboard_data(client_ip)
            await websocket.send(json.dumps({
                'event': 'dashboard_update',
                'data': dashboard_data,
                'timestamp': datetime.now().isoformat()
            }))
        except Exception as e:
            logger.error(f"Error sending initial data to {client_ip}: {e}")

    async def unregister_client(self, websocket, client_ip: str):
        """Unregister a WebSocket client"""
        if client_ip in self.clients:
            self.clients[client_ip].discard(websocket)
            if not self.clients[client_ip]:
                del self.clients[client_ip]

        # Unregister from session manager
        self.session_manager.unregister_websocket(client_ip, websocket)

        logger.info(f"WebSocket client unregistered: {client_ip}")

    async def broadcast_to_client(self, client_ip: str, message: dict):
        """Send message to all WebSocket connections for a specific client"""
        if client_ip not in self.clients:
            return

        message_str = json.dumps(message)
        disconnected = []

        for websocket in self.clients[client_ip].copy():
            try:
                await websocket.send(message_str)
            except websockets.exceptions.ConnectionClosed:
                disconnected.append(websocket)
            except Exception as e:
                logger.error(f"Error sending message to {client_ip}: {e}")
                disconnected.append(websocket)

        # Clean up disconnected clients
        for websocket in disconnected:
            await self.unregister_client(websocket, client_ip)

    async def broadcast_to_all(self, message: dict):
        """Send message to all connected clients"""
        for client_ip in list(self.clients.keys()):
            await self.broadcast_to_client(client_ip, message)

    async def handle_client(self, websocket, path):
        """Handle individual WebSocket client connection"""
        # Extract client IP from path: /ws/dashboard/{client_ip}
        try:
            path_parts = path.strip('/').split('/')
            if len(path_parts) >= 3 and path_parts[0] == 'ws' and path_parts[1] == 'dashboard':
                client_ip = path_parts[2]
            else:
                # Fallback to connection IP
                client_ip = websocket.remote_address[0]
        except Exception as e:
            logger.error(f"Error extracting client IP from path {path}: {e}")
            client_ip = websocket.remote_address[0]

        await self.register_client(websocket, client_ip)

        try:
            # Keep connection alive and handle incoming messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.handle_client_message(client_ip, data, websocket)
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON from {client_ip}: {message}")
                except Exception as e:
                    logger.error(f"Error handling message from {client_ip}: {e}")

        except websockets.exceptions.ConnectionClosed:
            logger.info(f"WebSocket connection closed for {client_ip}")
        except Exception as e:
            logger.error(f"WebSocket error for {client_ip}: {e}")
        finally:
            await self.unregister_client(websocket, client_ip)

    async def handle_client_message(self, client_ip: str, data: dict, websocket):
        """Handle incoming messages from WebSocket clients"""
        try:
            message_type = data.get('type')

            if message_type == 'ping':
                # Respond to ping with pong
                await websocket.send(json.dumps({
                    'type': 'pong',
                    'timestamp': datetime.now().isoformat()
                }))

            elif message_type == 'request_dashboard_update':
                # Send fresh dashboard data
                dashboard_data = self.session_manager.get_user_dashboard_data(client_ip)
                await websocket.send(json.dumps({
                    'event': 'dashboard_update',
                    'data': dashboard_data,
                    'timestamp': datetime.now().isoformat()
                }))

            elif message_type == 'submit_task':
                # Handle task submission
                task_description = data.get('description', 'User task')
                task_id = self.session_manager.submit_task(client_ip, task_description)

                await websocket.send(json.dumps({
                    'event': 'task_submitted',
                    'task_id': task_id,
                    'timestamp': datetime.now().isoformat()
                }))

            else:
                logger.warning(f"Unknown message type from {client_ip}: {message_type}")

        except Exception as e:
            logger.error(f"Error handling client message: {e}")

    def start_periodic_updates(self):
        """Start background task for periodic dashboard updates"""
        async def update_loop():
            while True:
                try:
                    # Send periodic updates to all connected clients
                    for client_ip in list(self.clients.keys()):
                        if self.clients[client_ip]:  # Has active connections
                            dashboard_data = self.session_manager.get_user_dashboard_data(client_ip)
                            await self.broadcast_to_client(client_ip, {
                                'event': 'periodic_update',
                                'data': dashboard_data,
                                'timestamp': datetime.now().isoformat()
                            })

                    await asyncio.sleep(30)  # Update every 30 seconds

                except Exception as e:
                    logger.error(f"Error in periodic update loop: {e}")
                    await asyncio.sleep(5)

        # Run in background
        asyncio.create_task(update_loop())

    async def start_server(self):
        """Start the WebSocket server"""
        logger.info(f"Starting WebSocket server on {self.host}:{self.port}")

        self.server = await websockets.serve(
            self.handle_client,
            self.host,
            self.port,
            ping_interval=30,
            ping_timeout=10
        )

        # Start periodic updates
        self.start_periodic_updates()

        logger.info("WebSocket server started successfully")
        return self.server

    async def stop_server(self):
        """Stop the WebSocket server"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            logger.info("WebSocket server stopped")

    def run_server(self):
        """Run the WebSocket server (blocking)"""
        async def main():
            await self.start_server()
            # Keep running forever
            await asyncio.Future()  # Run forever

        asyncio.run(main())

    def run_server_threaded(self):
        """Run the WebSocket server in a separate thread"""
        def run():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            async def start():
                await self.start_server()
                # Keep running
                await asyncio.Future()

            loop.run_until_complete(start())

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        return thread

# Global WebSocket server instance
websocket_server = SessionWebSocketServer()

def get_websocket_server():
    """Get global WebSocket server instance"""
    return websocket_server

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Run server
    server = SessionWebSocketServer()
    server.run_server()