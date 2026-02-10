import asyncio
import websockets

class Client:
    def __init__(self):
        self.session_token = None
        self.websocket = None

    async def connect_to_lan_server(self):
        # Connect to LAN Server
        self.websocket = await websockets.connect('ws://localhost:8765')
        self.session_token = await self.websocket.recv()

        # Handle file operations
        while True:
            try:
                # Send file operation to LAN Server
                await self.websocket.send('file_operation')
            except websockets.ConnectionClosed:
                # Handle disconnection
                break

async def main():
    client = Client()
    await client.connect_to_lan_server()

asyncio.run(main())