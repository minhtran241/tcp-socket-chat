"""
Client Handler Module
Handles the communication with a single client
"""

import socket
import threading
from common.constants import SYSTEM_MESSAGE, DM_FROM, DM_TO, DM_PREFIX


class ClientHandler:
    """Handles communication with a single client"""

    def __init__(
        self, client_socket, addr, active_clients, clients_lock, broadcast_func
    ):
        """Initialize the client handler"""
        self.client_socket = client_socket
        self.addr = addr
        self.active_clients = active_clients
        self.clients_lock = clients_lock
        self.broadcast_message = broadcast_func
        self.username = None
        self.running = True

    def handle(self):
        """Main method to handle client connection"""
        try:
            # First message should be the username
            self.client_socket.settimeout(
                5.0
            )  # Set timeout for initial username reception
            username_message = self.client_socket.recv(1024).decode("utf-8")
            self.username = username_message.strip()

            # Reset timeout for normal operation
            self.client_socket.settimeout(None)

            # Check if username is already in use
            username_in_use = False
            with self.clients_lock:
                for _, (existing_username, _) in self.active_clients.items():
                    if existing_username.lower() == self.username.lower():
                        username_in_use = True
                        break

            if username_in_use:
                self.client_socket.send(
                    f"{SYSTEM_MESSAGE}: Username '{self.username}' is already in use. Please choose another.".encode(
                        "utf-8"
                    )
                )
                return

            # Store client info
            with self.clients_lock:
                self.active_clients[self.client_socket] = (self.username, self.addr)

            # Announce new user
            self.broadcast_message(
                # self.client_socket,
                f"{SYSTEM_MESSAGE}: @{self.username} has joined the chat.", exclude=self.client_socket
            )
            print(f"[INFO] {self.username} ({self.addr[0]}:{self.addr[1]}) connected.")

            # Send current user list to the new client
            self.send_welcome_message()

            # Handle messages from this client
            self.message_loop()

        except socket.timeout:
            print(
                f"[INFO] Client at {self.addr[0]}:{self.addr[1]} timed out during login"
            )
        except Exception as e:
            print(f"[ERROR] Exception during client handling: {e}")
        finally:
            # Client disconnected, clean up
            self.handle_disconnect()

    def send_welcome_message(self):
        """Send welcome message with current user list to the client"""
        with self.clients_lock:
            user_list = "Current users: " + ", ".join(
                [name for name, _ in self.active_clients.values()]
            )

        try:
            self.client_socket.send(
                f"{SYSTEM_MESSAGE}: Welcome, {self.username}! {user_list}".encode(
                    "utf-8"
                )
            )
        except:
            pass

    def message_loop(self):
        """Handle incoming messages from the client"""
        while self.running:
            try:
                # Set a timeout to allow checking if we're still running
                self.client_socket.settimeout(0.5)
                message = self.client_socket.recv(1024).decode("utf-8")

                if not message:
                    # Client disconnected
                    break

                # Process the message
                self.process_message(message)

            except socket.timeout:
                # This is expected due to the timeout we set
                continue
            except ConnectionResetError:
                # Client connection was reset
                break
            except Exception as e:
                print(f"[ERROR] Exception with {self.username}: {e}")
                break

        self.running = False

    def process_message(self, message):
        """Process a message from the client"""
        # Check for direct message
        if message.startswith(DM_PREFIX):
            # Extract target username and message
            parts = message[1:].split(" ", 1)
            if len(parts) > 1:
                target_username = parts[0]
                dm_message = parts[1]
                self.send_direct_message(target_username, dm_message)
            else:
                try:
                    self.client_socket.send(
                        f"{SYSTEM_MESSAGE}: Invalid DM format. Use '@username message'".encode(
                            "utf-8"
                        )
                    )
                except:
                    pass
        else:
            # Regular message - broadcast to all
            self.broadcast_message(f"@{self.username}: {message}")

    def send_direct_message(self, target_username, message):
        """Send a direct message to a specific user"""
        # Format the direct message
        formatted_message = f"{DM_FROM} {self.username}]: {message}"

        with self.clients_lock:
            # Find the target user
            for client_socket, (username, _) in self.active_clients.items():
                if username.lower() == target_username.lower():
                    try:
                        client_socket.send(formatted_message.encode("utf-8"))
                        # Also send confirmation to the sender
                        self.client_socket.send(
                            f"{DM_TO} {username}]: {message}".encode("utf-8")
                        )
                        return True
                    except:
                        # Connection might be closed or broken
                        return False

        # User not found
        try:
            self.client_socket.send(
                f"{SYSTEM_MESSAGE}: User '{target_username}' not found.".encode("utf-8")
            )
        except:
            pass
        return False

    def handle_disconnect(self):
        """Handle client disconnection"""
        self.running = False
        print(f"[INFO] {self.username} ({self.addr[0]}:{self.addr[1]}) disconnected.")

        with self.clients_lock:
            if self.client_socket in self.active_clients:
                print(
                    f"[INFO] Cleaning up {self.username} ({self.addr[0]}:{self.addr[1]})"
                )
                if self.username:
                    username = self.active_clients[self.client_socket][0]
                    addr = self.active_clients[self.client_socket][1]
                    del self.active_clients[self.client_socket]
                else:
                    # Unnamed client
                    del self.active_clients[self.client_socket]

        try:
            print(f"[INFO] Closing connection with @{self.username}...")
            self.client_socket.close()
            print(f"[INFO] Connection with @{self.username} closed.")
            self.broadcast_message(
                f"{SYSTEM_MESSAGE}: @{username} has left the chat.", exclude=self.client_socket
            )
            print(f"[INFO] @{username} ({addr[0]}:{addr[1]}) disconnected.")
        except:
            pass
