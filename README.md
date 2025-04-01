# TCP Socket Chat Application

A lightweight, multi-threaded chat application built with TCP sockets that enables real-time group communication.

## Overview

This application implements a server-client architecture for group chat functionality. The server acts as a message reflector, relaying messages between connected clients, while each client provides a user interface for sending and receiving messages. The system supports dynamic joining and leaving of participants without disrupting ongoing conversations.

## Core Features

-   **Multi-threaded Server**: Handles concurrent client connections with dedicated threads
-   **Interactive User Interface**: Separate areas for message composition and conversation display
-   **Real-time Communication**: Messages propagate instantly to all connected users
-   **Username Identification**: All messages include sender identification
-   **Connection Management**: Graceful handling of client connections and disconnections
-   **Dynamic Participation**: Users can join or leave at any time without disrupting the chat

## Requirements

-   Python 3.13+
-   uv package manager (for managing Python packages)
-   Required packages:
    -   tkinter (for GUI implementation)
    -   socket (standard library)
    -   threading (standard library)

## Installation

1. Install the `uv` package manager [here](https://docs.astral.sh/uv/getting-started/installation/)
2. Install python 3.13+ using `uv` [here](https://docs.astral.sh/uv/guides/install-python/)
3. Install the required packages:

    ```bash
    uv pip install -r pyproject.toml
    ```

## Usage

### Running the Server/Client

```bash
uv run main.py server --host <host> --port <port>
uv run main.py client --host <host> --port <port>
```

Parameters:

-   `--host`: IP address to bind the server to (default: 0.0.0.0)
-   `--port`: Port number to listen on (default: 12345)

## Testing in a Network Environment

To test the application across different machines:

1. Start the server on a remote machine (e.g., on a university server):

    ```bash
    uv run main.py server --port 12345
    ```

2. Set up an SSH tunnel from your local machine for secure access:

    ```bash
    ssh -N -L 12345:localhost:12345 yourusername@remote-server.edu &
    ```

3. Connect clients from different machines to the server:
    ```bash
    uv run main.py client --port 12345
    ```

## Architecture

### Server

-   Listens for incoming client connections
-   Creates a new thread for each connected client
-   Maintains a list of active connections
-   Broadcasts messages from one client to all other clients

### Client

-   Connects to the server using TCP sockets
-   Provides a UI with separate input and chat display areas
-   Uses multi-threading to handle message receiving and UI updates concurrently
-   Displays username with each message for identification

## Contributors

-   [Minh Tran](https://github.com/minhtran241)
-   [Elijah Morgan](https://github.com/ElijahLeeMorgan)
