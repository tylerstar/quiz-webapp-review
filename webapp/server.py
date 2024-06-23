import asyncio
import async_timeout
import logging
import uvicorn

from fastapi import FastAPI, WebSocket, WebSocketDisconnect


logger = logging.getLogger('uvicorn.error')


def singleton(cls):
    """
    Decorator to implement the singleton pattern. This decorator ensures a class has only one instance
    across the application.

    Args:
        cls (class): Class to apply singleton pattern.

    Returns:
        function: Function to get the single instance of the class.
    """
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


# Create a manager to manage the websocket connections
@singleton
class ConnectionManager:
    """
    Manages WebSocket connections for the FastAPI application, allowing for message broadcasting and
    connection handling with a timeout feature.
    """
    def __init__(self):
        self.active_connections = dict()
        
        # Close the connection if client become inactive for more than 1 hour
        self.timeout = 3600

    async def connect(self, websocket: WebSocket):
        """Register a new WebSocket connection."""
        self.active_connections[websocket] = None

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        del self.active_connections[websocket]

    async def broadcast(self, message: str):
        """Send a message to all connected WebSockets."""
        for connection in self.active_connections:
            await connection.send_text(message)
            
    def set_client_timeout(self, timeout: int):
        """Set the timeout for all client connections."""
        self.timeout = timeout


app = FastAPI()


# Attach the manager to the app for global access
app.manager = ConnectionManager()


# Logic to process all messages from different clients
@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    """
    WebSocket endpoint for handling incoming connections and messages.

    Args:
        websocket (WebSocket): WebSocket connection object.
        username (str): Username of the client connecting.
    """
    await websocket.accept()
    await app.manager.connect(websocket)
    
    try:
        while True:
            try:
                async with async_timeout.timeout(app.manager.timeout):
                    data = await websocket.receive_text()

                broadcast_message = f"{username}: {data}"
                await app.manager.broadcast(broadcast_message)
            except asyncio.TimeoutError:
                logger.info(f"Timeout: No data received from "
                            f"{username} in {app.manager.timeout} seconds.")
                break 
    except WebSocketDisconnect:
        logger.info(f"{username} left the chat")
    except Exception as e:
        logger.exception(f"Fatal error occurred while processing the message: {e}")
    finally:
        logger.info(f"Disconnecting {username}")
        app.manager.disconnect(websocket)


def start_server(host: str, port: int, timeout: int):
    """
    Start the FastAPI application with a specified timeout for WebSocket connections.

    Args:
        host (str): Host address for the server.
        port (int): Port number for the server.
        timeout (int): Timeout in seconds for the WebSocket server.
    """
    app.manager.set_client_timeout(timeout)
    uvicorn.run(app, host=host, port=port)