import click
from server import start_server
from client import start_client


@click.group()
def cli():
    pass


@cli.command()
@click.option("--host", default="127.0.0.1", help="Host to run the server on")
@click.option("--port", default=8000, type=int, help="Port to run the server on")
@click.option("--timeout", default=3600, type=int, help="Timeout for the websocket server")
def server(host: str, port: int, timeout: int):
    """
    Command to start the server

    Args:
        host: Host to run the server on
        port: Port to run the server on
        timeout: Timeout for the client
    """
    start_server(host, port, timeout)
    
    
@cli.command()
@click.option("--host", default="127.0.0.1", type=str, help="Server's host")
@click.option("--port", default=8000, type=int, help="Server's port")
@click.option("--username", required=True, help="Username for the client")
def client(host: str, port: int, username: str):
    """
    Command to start the client

    Args:
        host: Host of server
        port: Port of server
        username: client's username
    """
    start_client(host, port, username)


if __name__ == '__main__':
    cli()
