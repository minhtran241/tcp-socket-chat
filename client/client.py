"""
Main Chat Client Implementation
Combines network communication with UI components
"""

import socket
import threading
import queue
import darkdetect
import tkinter as tk

from client.gui.login import LoginGUI
from client.gui.chat import ChatGUI
from client.theme import get_theme, WINDOW_SIZE
from common.constants import DEFAULT_HOST, DEFAULT_PORT


class ChatClient:
    """Chat client that connects to a server and manages communication and UI"""

    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
        """Initialize the client with host and port"""
        self.host = host
        self.port = port
        self.socket = None
        self.username = ""
        self.connected = False
        self.running = True
        self.receive_thread = None
        self.theme = darkdetect.theme().lower()
        self.colors = get_theme(self.theme)

        # Message queue for thread-safe communication
        self.message_queue = queue.Queue()

        # Create the UI components
        self.root = tk.Tk()
        self.root.title("TCP Socket Chat Client")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(False, False)

        # Apply theme to root window
        self.root.configure(bg=self.colors["bg_main"])

        # Initialize UI components - do this after setting initial theme
        self.login_ui = LoginGUI(self.root, self, self.theme)
        self.chat_ui = ChatGUI(self.root, self)

    def start(self) -> None:
        """Start the client application"""
        self.setup_login_ui()
        self.root.mainloop()

    def setup_login_ui(self) -> None:
        """Initialize and display the login UI"""
        # Ensure login UI has latest theme colors
        self.login_ui.colors = self.colors
        self.login_ui.theme = self.theme
        self.login_ui.setup_login_frame()

    def update_theme(self, theme: str) -> None:
        """Update the theme of the application"""
        if theme != self.theme:
            self.theme = theme
            self.colors = get_theme(self.theme)

            # Update root window
            self.root.configure(bg=self.colors["bg_main"])
            # Set the foreground color of the root window
            self.root.option_add("*foreground", self.colors["fg_main"])

            # Propagate theme to UI components
            self.login_ui.colors = self.colors
            self.login_ui.theme = self.theme
            self.chat_ui.colors = self.colors

            # Update active UI if needed
            if hasattr(self, "chat_ui") and self.chat_ui.chat_frame:
                self.chat_ui.setup_chat_frame()
            elif hasattr(self, "login_ui") and self.login_ui.login_frame:
                self.login_ui.setup_login_frame()

    def setup_chat_ui(self) -> None:
        """Initialize and display the chat UI"""
        # Ensure chat UI has latest theme colors
        self.chat_ui.colors = self.colors
        self.chat_ui.setup_chat_frame()

    def connect_to_server(self, username: str) -> bool:
        """Connect to the chat server"""
        self.username = username

        # Ensure we're properly disconnected first
        self.disconnect()

        try:
            # Create new socket and connect
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))

            # Send username to server
            self.socket.send(self.username.encode("utf-8"))

            # Start receiving thread
            self.running = True
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()

            self.connected = True
            return True

        except Exception as e:
            self.message_queue.put(f"[Error] Could not connect to server: {str(e)}")
            return False

    def receive_messages(self) -> None:
        """Receive messages from server and put them in queue"""
        while self.running:
            try:
                # Set a timeout to allow checking if we're still running
                self.socket.settimeout(0.5)
                data = self.socket.recv(1024).decode("utf-8")
                if not data:
                    break

                # Put message in queue for UI thread to handle
                self.message_queue.put(data)

            except socket.timeout:
                # This is expected due to the timeout we set
                continue
            except Exception as e:
                if self.running:
                    self.message_queue.put(f"[Error] Connection lost: {str(e)}")
                    self.running = False
                break

        # If we're still supposed to be running but we exited the loop, server disconnected
        if self.running:
            self.message_queue.put("[Info] Server disconnected.")
            self.chat_ui.handle_server_disconnect()

    def send_message(self, message: str) -> bool:
        """Send message to server"""
        if not self.connected or not self.socket:
            return False

        try:
            self.socket.send(message.encode("utf-8"))
            return True
        except Exception as e:
            self.message_queue.put(f"[Error] Could not send message: {str(e)}")
            return False

    def disconnect(self) -> None:
        """Disconnect from the server"""
        # Set running to False to stop the receive thread
        self.running = False

        # Close socket if it exists
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None

        self.connected = False

        # Wait for the receive thread to finish if it's running
        if self.receive_thread and self.receive_thread.is_alive():
            try:
                self.receive_thread.join(timeout=1.0)
            except:
                pass
            self.receive_thread = None

    def on_closing(self) -> None:
        """Handle window close event"""
        import tkinter.messagebox as messagebox

        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # Stop any update timers in the chat UI
            if hasattr(self.chat_ui, "update_timer") and self.chat_ui.update_timer:
                self.root.after_cancel(self.chat_ui.update_timer)
                self.chat_ui.update_timer = None

            self.disconnect()
            self.root.destroy()


def start_client(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    """Start the chat client with the specified host and port"""
    client = ChatClient(host, port)
    client.start()


if __name__ == "__main__":
    start_client()
