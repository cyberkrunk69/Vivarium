import asyncio
import websockets

async def handle_connection(websocket, path):
    # Handle WebSocket connection
    while True:
        try:
            # Receive message from client
            message = await websocket.recv()
            # Process message
            print(f"Received message: {message}")
            # Send response back to client
            await websocket.send(f"Received message: {message}")
        except websockets.ConnectionClosed:
            print("Connection closed")
            break

async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("Server started on port 8765")
        await asyncio.Future()  # run forever

asyncio.run(main())