"""
Chat Client Theming
Defines theme colors and styles for the chat application with modern design
"""

# Theme color definitions
THEME_COLORS = {
    "light": {
        "bg_main": "#f7f9fb",       # Main background - very light blue-gray
        "bg_input": "#ffffff",       # Input area - white
        "primary": "#3f51b5",        # Primary color - indigo
        "primary_fg": "#ffffff",     # Primary text color - white
        "secondary": "#e8eaf6",      # Secondary color - light indigo for other messages
        "secondary_fg": "#303030",   # Secondary text color - dark gray
        "online_status": "#4caf50",  # Green for online status
        "disconnect_button_bg": "#f44336",  # Red for disconnect button
        "disconnect_button_fg": "#ffffff",  # White text for disconnect button
        # Message type colors - enhanced
        "warning": "#ff9800",      # Orange for warnings
        "info": "#03a9f4",         # Light blue for information
        "success": "#4caf50",      # Green for success
        "debug": "#9c27b0",        # Purple for debug
        "message_accent": "#e0e0e0", # Light gray for message accents
    },
    
    "dark": {
        "bg_main": "#121212",       # Main background - very dark gray
        "bg_input": "#1e1e1e",      # Input area - lighter dark
        "primary": "#5c6bc0",       # Primary color - indigo with higher value for dark mode
        "primary_fg": "#ffffff",    # Primary text color - white
        "secondary": "#2a2a2a",     # Secondary color - dark gray for other messages
        "secondary_fg": "#e0e0e0",  # Secondary text color - light gray
        "online_status": "#4caf50", # Green for online status
        "disconnect_button_bg": "#f44336",  # Red for disconnect button	
        "disconnect_button_fg": "#ffffff",  # White text for disconnect button
        # Message type colors - enhanced for dark mode
        "warning": "#ff9800",      # Orange for warnings
        "info": "#03a9f4",         # Light blue for information
        "success": "#4caf50",      # Green for success
        "debug": "#9c27b0",        # Purple for debug
        "message_accent": "#3a3a3a", # Dark gray for message accents
    }
}

def get_theme(theme_name="light"):
    """Get the theme colors for the specified theme name"""
    return THEME_COLORS.get(theme_name, THEME_COLORS["light"])

# UI constants
WINDOW_SIZE = "900x650"  # Slightly larger default window size
FONT_HEADING = ("Avenir", 18, "bold")
FONT_SUBHEADING = ("Avenir", 14)
FONT_REGULAR = ("Avenir", 12)
FONT_BOLD = ("Avenir", 12, "bold")
FONT_ITALIC = ("Avenir", 12, "italic")
FONT_BOLD_ITALIC = ("Avenir", 12, "bold italic")
FONT_TIMESTAMP = ("Avenir", 9)

# Message style configuration
MESSAGE_STYLES = {
    "my_message": {
        "background": "#e8f0fe",  # Light blue
        "foreground": "#1a237e",  # Dark blue
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "relief": "flat",
        "borderwidth": 0,
        "font": FONT_BOLD
    },
    "dm_to_me": {
        "background": "#ffebee",  # Light red
        "foreground": "#c62828",  # Dark red
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "relief": "flat",
        "borderwidth": 0,
        "font": FONT_BOLD_ITALIC
    },
    "dm_from_me": {
        "background": "#e8f5e9",  # Light green
        "foreground": "#1b5e20",  # Dark green
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "relief": "flat",
        "borderwidth": 0,
        "font": FONT_BOLD_ITALIC
    },
    "regular": {
        "background": "#f5f5f5",  # Light gray
        "foreground": "#212121",  # Near black
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "borderwidth": 0,
        "font": FONT_BOLD
    },
    "error_message": {
        "background": "#ffebee",  # Light red
        "foreground": "#c62828",  # Dark red
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "borderwidth": 0,
        "font": FONT_ITALIC
    },
    # Enhanced message types
    "warning_message": {
        "background": "#fff3e0",  # Light orange
        "foreground": "#e65100",  # Dark orange
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "borderwidth": 0,
        "font": FONT_BOLD
    },
    "info_message": {
        "background": "#e1f5fe",  # Very light blue
        "foreground": "#01579b",  # Dark blue
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "borderwidth": 0,
        "font": FONT_REGULAR
    },
    "success_message": {
        "background": "#e8f5e9",  # Light green
        "foreground": "#1b5e20",  # Dark green
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "borderwidth": 0,
        "font": FONT_BOLD
    },
    "debug_message": {
        "background": "#f3e5f5",  # Light purple
        "foreground": "#4a148c",  # Dark purple
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "borderwidth": 0,
        "font": FONT_ITALIC
    },
    "announcement": {
        "background": "#bbdefb",  # Light blue
        "foreground": "#0d47a1",  # Dark blue
        "lmargin1": 10,
        "lmargin2": 10,
        "rmargin": 10,
        "relief": "flat",
        "borderwidth": 0,
        "font": FONT_BOLD
    },
    "timestamp": {
        "font": FONT_TIMESTAMP,
        "foreground": "#757575"
    },
}