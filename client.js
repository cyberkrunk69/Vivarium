const websocket = new WebSocket('ws://localhost:8765');

// Handle file editing and send commands to WebSocket server
websocket.onmessage = (event) => {
    // Handle message from server
};

// Send command to server
websocket.send('edit_file');