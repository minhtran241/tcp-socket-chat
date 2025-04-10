import argparse
from server.server import start_server
from client.client import start_client
from common.constants import DEFAULT_HOST, DEFAULT_SERVER_HOST, DEFAULT_PORT


def main() -> None:
    parser = argparse.ArgumentParser(description="TCP Socket Chat Application CLI")
    parser.add_argument(
        "mode", choices=["server", "client"], help="Run as server or client"
    )
    parser.add_argument(
        "--host", default=None, help="Specify host (default: server/client default)"
    )
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT, help="Specify port (default: 5000)"
    )

    args = parser.parse_args()
    host = (
        args.host
        if args.host
        else (DEFAULT_SERVER_HOST if args.mode == "server" else DEFAULT_HOST)
    )

    if args.mode == "server":
        start_server(host, args.port)
    else:
        start_client(host, args.port)


if __name__ == "__main__":
    main()
