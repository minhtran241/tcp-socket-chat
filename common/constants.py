"""
Common constants shared between client and server
"""

# Default network settings
DEFAULT_HOST = "localhost"  # Default host for client
DEFAULT_SERVER_HOST = "0.0.0.0"  # Listen on all interfaces for server
DEFAULT_PORT = 12345  # Default port for both client and server

# Message prefixes
SYSTEM_MESSAGE = "[System]"
ERROR_MESSAGE = "[Error]"
WARNING_MESSAGE = "[Warning]"
INFO_MESSAGE = "[Info]"
SUCCESS_MESSAGE = "[Success]"
DEBUG_MESSAGE = "[Debug]"
ANNOUNCEMENT = "[Announcement]"

# Direct message prefixes
DM_PREFIX = "@"
DM_FROM = "[DM from"
DM_TO = "[DM to"