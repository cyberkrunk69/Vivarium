import asyncio
import websockets

async def handle_connection(websocket, path):
    # Handle WebSocket connection
    pass

async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())