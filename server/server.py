"""
Chat Server Implementation
Handles server setup and client connections
"""

import socket
import threading
import sys
from server.client_handler import ClientHandler
from common.constants import DEFAULT_SERVER_HOST, DEFAULT_PORT, SYSTEM_MESSAGE


class ChatServer:
    """Chat server that handles multiple client connections"""

    def __init__(self, host=DEFAULT_SERVER_HOST, port=DEFAULT_PORT):
        """Initialize the server with host and port"""
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False

        # Active clients dictionary and lock for thread-safe access
        self.active_clients = {}
        self.clients_lock = threading.Lock()
        self.client_threads = {}

    def start(self):
        """Start the server and listen for connections"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            print(f"[INFO] Server started on {self.host}:{self.port}")

            self.accept_connections()

        except Exception as e:
            print(f"[ERROR] Server error: {e}")
            self.stop()

    def accept_connections(self):
        """Accept incoming client connections"""
        try:
            while self.running:
                try:
                    # Set a timeout to allow checking if server is still running
                    self.server_socket.settimeout(1.0)
                    client_socket, addr = self.server_socket.accept()
                    self.server_socket.settimeout(None)  # Reset timeout

                    # Create a client handler for this connection
                    handler = ClientHandler(
                        client_socket,
                        addr,
                        self.active_clients,
                        self.clients_lock,
                        self.broadcast_message,
                    )

                    # Start the handler in a new thread
                    thread = threading.Thread(target=handler.handle)
                    thread.daemon = True
                    self.client_threads[client_socket] = thread
                    thread.start()
                except socket.timeout:
                    # This is expected due to the timeout we set
                    continue
                except Exception as e:
                    if self.running:
                        print(f"[ERROR] Error accepting connection: {e}")

        except KeyboardInterrupt:
            print("[INFO] Server shutting down...")
        except Exception as e:
            if self.running:
                print(f"[ERROR] Error in accept loop: {e}")
        finally:
            self.stop()

    def broadcast_message(self, message, exclude=None):
        """Send message to all clients except the sender"""
        print(f"[INFO] Current clients: {self.active_clients}")
        with self.clients_lock:
            dead_clients = []
            for client_socket, (username, _) in self.active_clients.items():
                try:
                    if client_socket != exclude:
                        client_socket.send(message.encode("utf-8"))
                except:
                    # Mark this client for removal
                    dead_clients.append(client_socket)

            # Remove any dead clients
            for client in dead_clients:
                if client in self.active_clients:
                    username = self.active_clients[client][0]
                    addr = self.active_clients[client][1]
                    self.client_threads[client].join()
                    # Remove from active clients
                    del self.active_clients[client]
                    print(
                        f"[INFO] Removed dead client: {username} ({addr[0]}:{addr[1]})"
                    )

    def stop(self):
        """Stop the server and close all connections"""
        self.running = False

        # Close all client connections
        with self.clients_lock:
            for sock in list(self.active_clients.keys()):
                try:
                    sock.close()
                except:
                    pass

        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass

        print("[INFO] Server closed.")


def start_server(host=DEFAULT_SERVER_HOST, port=DEFAULT_PORT):
    """Start the chat server with the specified host and port"""
    server = ChatServer(host, port)

    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    start_server()
