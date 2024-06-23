import asyncio
import aioconsole
import websockets


class Client:
    def __init__(self, host: str, port: int, username: str):
        """
        A Websocket client designed to connect to a specified server using Websocket protocol.
        This client handles establishing a connection to the server and allows interactive communication,
        enabling sending and receiving messages in real-time. The client is initialized with the server's
        host address, port number, and a username to identify the connection uniquely.

        Args:
            host (str): The host address of the server to which the client should connect.
            port (int): The port number on the server to be used for the connection.
            username (str): A unique username used to identify the client on the server.

        Attributes:
            host (str): Host address of the server.
            port (int): Port number on the server.
            username (str): Username of the client.
            uri (str): The complete URI used for the Websocket connection.
        """
        self.host = host
        self.port = port
        self.username = username
        self.uri = f"ws://{self.host}:{self.port}/ws/{self.username}"

    async def connect(self):
        """
        Establishes a WebSocket connection to the server and manages interactive communication tasks.
        Handles exceptions related to connection issues.
        """
        try:
            async with websockets.connect(self.uri) as websocket:
                print("Connected, start typing and chatting now")
                await self.create_interactive_tasks(websocket)
        except ConnectionRefusedError:
            print("Failed to connect to server, please check your network and ensure server is running")
        except Exception as e:
            print(f"Unexpected error while connecting to server: {e}")

    async def create_interactive_tasks(self, websocket):
        """
        Creates asynchronous tasks for sending and receiving messages and manages their lifecycle.

        Args:
            websocket: The WebSocket connection object used for communication.
        """
        sender = asyncio.create_task(self.sender(websocket))
        receiver = asyncio.create_task(self.receiver(websocket))
        done, pending = await asyncio.wait(
            [sender, receiver],
            return_when=asyncio.FIRST_COMPLETED
        )
        # If sender or receiver exits, close another task
        for task in pending:
            task.cancel()

    @classmethod
    async def sender(cls, websocket):
        """
        Continuously prompts the user for input and sends messages to the server.

        Args:
            websocket: The WebSocket connection object used for sending messages.
        """
        while True:
            # Don't use builtin input because it would block the event loop
            message = await aioconsole.ainput("")
            await websocket.send(message)

    @classmethod
    async def receiver(cls, websocket):
        """
        Continuously receives messages from the server and prints them to the console.

        Args:
            websocket: The WebSocket connection object used for receiving messages.
        """
        while True:
            try:
                response = await websocket.recv()
                print(response)
            except websockets.exceptions.ConnectionClosedError:
                print("Connection closed.")
                break


def start_client(host: str, port: int, username: str):
    """
    Initializes and starts a WebSocket client.

    Args:
        host (str): The host address of the server.
        port (int): The port number on the server.
        username (str): The username to identify the client.
    """
    client = Client(host, port, username)
    asyncio.run(client.connect())
