# Websocket Chat Application

This repository contains the code for a simple Websocket chat application using Python. The application consists of a server and a client that can communicate over websockets.

## Files

- `main.py`: The entry point for the application. It contains the CLI commands to start the server or client.
- `server.py`: Contains the server logic using FastAPI and manages WebSocket connections.
- `client.py`: Implements the WebSocket client that can connect to the server and exchange messages.
- `requirements.txt`: Lists all the Python dependencies required to run the application.

## Requirements

- Python 3.10
- Dependencies are listed in the `requirements.txt` file. Install them using:
  ```bash
  pip install -r requirements.txt
  
## Usage

To start the server, run the following command:
```bash
python main.py server --host 127.0.0.1 --port 8000
```

To start a client and connect to the server, use:
```bash
python main.py client --host 127.0.0.1 --port 8000 --username <YourUsername>
```
Replace <YourUsername> with your desired username.

## Example Commands

Start the server on localhost and default port 8000:
```bash
python main.py server --host 127.0.0.1 --port 8000
```

Connect a client named 'ClientA' to the server:
```bash
python main.py client --username ClientA
```

## Note
Make sure to run the server before attempting to connect any clients. Both the server and client commands must be run in separate terminal instances.
