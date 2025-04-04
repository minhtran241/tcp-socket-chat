"""
Chat Client Theming
Defines theme colors and styles for the chat application
"""

# Theme color definitions
THEME_COLORS = {
    "light": {
        "bg_main": "#f5f5f5",       # Main background - light gray
        "bg_input": "#ffffff",       # Input area - white
        "primary": "#2196F3",      # Primary color - blue
        "primary_fg": "#ffffff",  # Primary text color - white
        "secondary": "#f5f5f5",  # Secondary color - light gray
        "secondary_fg": "#212121",  # Secondary text color - near black
        "online_status": "#4caf50",  # Green for online status
        "disconnect_button_bg": "#f44336",  # Red for disconnect button
        "disconnect_button_fg": "#ffffff",  # White text for disconnect button
        # New color definitions for message types
        "warning": "#ff9800",      # Orange for warnings
        "info": "#03a9f4",         # Light blue for information
        "success": "#4caf50",      # Green for success
        "debug": "#9c27b0",        # Purple for debug
    },
    
    "dark": {
        "bg_main": "#212121",       # Main background - dark gray
        "bg_input": "#2c2c2c",       # Input area - lighter dark
        "primary": "#2196F3",      # Primary color - blue
        "primary_fg": "#ffffff",  # Primary text color - white
        "secondary": "#2c2c2c",  # Secondary color - dark gray
        "secondary_fg": "#e0e0e0",  # Secondary text color - light gray
        "online_status": "#4caf50",  # Green for online status
        "disconnect_button_bg": "#f44336",  # Red for disconnect button	
        "disconnect_button_fg": "#ffffff",  # White text for disconnect button
        # New color definitions for message types
        "warning": "#ff9800",      # Orange for warnings
        "info": "#03a9f4",         # Light blue for information
        "success": "#4caf50",      # Green for success
        "debug": "#9c27b0",        # Purple for debug
    }
}

def get_theme(theme_name="light"):
    """Get the theme colors for the specified theme name"""
    return THEME_COLORS.get(theme_name, THEME_COLORS["light"])

# UI constants
WINDOW_SIZE = "800x600"  # Default window size for the client
FONT_HEADING = ("Avenir", 16, "bold")
FONT_SUBHEADING = ("Avenir", 14)
FONT_REGULAR = ("Avenir", 12)
FONT_BOLD = ("Avenir", 12, "bold")
FONT_ITALIC = ("Avenir", 12, "italic")
FONT_BOLD_ITALIC = ("Avenir", 12, "bold italic")
FONT_TIMESTAMP = ("Avenir", 10)

# Colors
COLOR_MY_MESSAGE = "#e6ffe6"  # Light green
COLOR_DM_TO_ME = "#ffe6e6"  # Light red
COLOR_DM_FROM_ME = "#e6e6ff"  # Light blue
COLOR_URL = "blue"

# Message style configuration
MESSAGE_STYLES = {
    "my_message": {
        "background": "#e3f2fd",  # Light blue
        "foreground": "#0d47a1",  # Dark blue
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "relief": "groove",
        "borderwidth": 1,
        "font": FONT_BOLD
    },
    "dm_to_me": {
        "background": "#ffebee",  # Light red
        "foreground": "#c62828",  # Dark red
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "relief": "groove",
        "borderwidth": 1,
        "font": FONT_BOLD_ITALIC
    },
    "dm_from_me": {
        "background": "#e8f5e9",  # Light green
        "foreground": "#1b5e20",  # Dark green
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "relief": "groove",
        "borderwidth": 1,
        "font": FONT_BOLD_ITALIC
    },
    "regular": {
        "background": "#fafafa",  # Off-white
        "foreground": "#212121",  # Near black
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "borderwidth": 1,
        "font": FONT_BOLD
    },
    "system_message": {
        "background": "#f3e5f5",  # Light purple
        "foreground": "#4a148c",  # Dark purple
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "borderwidth": 1,
        "font": FONT_BOLD
    },
    "error_message": {
        "background": "#ffebee",  # Light red
        "foreground": "#c62828",  # Dark red
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "borderwidth": 1,
        "font": FONT_ITALIC
    },
    # New message types
    "warning_message": {
        "background": "#fff3e0",  # Light orange
        "foreground": "#e65100",  # Dark orange
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "borderwidth": 1,
        "font": FONT_BOLD
    },
    "info_message": {
        "background": "#e1f5fe",  # Very light blue
        "foreground": "#01579b",  # Dark blue
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "borderwidth": 1,
        "font": FONT_REGULAR
    },
    "success_message": {
        "background": "#e8f5e9",  # Light green
        "foreground": "#1b5e20",  # Dark green
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "borderwidth": 1,
        "font": FONT_BOLD
    },
    "debug_message": {
        "background": "#f3e5f5",  # Light purple
        "foreground": "#4a148c",  # Dark purple
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "borderwidth": 1,
        "font": FONT_ITALIC
    },
    "announcement": {
        "background": "#bbdefb",  # Light blue
        "foreground": "#0d47a1",  # Dark blue
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "relief": "ridge",
        "borderwidth": 2,
        "font": FONT_BOLD
    },
    "timestamp": {
        "font": FONT_TIMESTAMP,
        "foreground": "#666666"
    },
}