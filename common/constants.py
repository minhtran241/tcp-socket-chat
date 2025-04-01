"""
Common constants shared between client and server
"""

# Default network settings
DEFAULT_HOST = "localhost"  # Default host for client
DEFAULT_SERVER_HOST = "0.0.0.0"  # Listen on all interfaces for server
DEFAULT_PORT = 12345  # Default port for both client and server

# Message types
SYSTEM_MESSAGE = "[System]"
DM_FROM = "[DM from"
DM_TO = "[DM to"
ERROR_MESSAGE = "[ERROR]"

# Direct message prefix
DM_PREFIX = "@"