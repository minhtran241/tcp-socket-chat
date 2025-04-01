"""
Chat Client Theming
Defines theme colors and styles for the chat application
"""

# Theme color definitions
THEME_COLORS = {
    "light": {
        "bg_main": "#f5f5f5",       # Main background - light gray
        "bg_input": "#ffffff",       # Input area - white
        "status_bar": "#e0e0e0",     # Status bar background
        "status_text": "#616161",    # Status bar text
        
        # Message backgrounds
        "regular_message_bg": "#fafafa",    # Off-white
        "regular_message_fg": "#212121",    # Near black
        "system_message_bg": "#f3e5f5",     # Light purple
        "system_message_fg": "#4a148c",     # Dark purple
        "error_message_bg": "#ffebee",      # Light red
        "error_message_fg": "#c62828",      # Dark red
        "dm_to_me_bg": "#ffebee",           # Light red
        "dm_to_me_fg": "#c62828",           # Dark red
        "dm_from_me_bg": "#e3f2fd",         # Light blue
        "dm_from_me_fg": "#0d47a1",         # Dark blue
        "my_message_bg": "#e8f5e9",         # Light green
        "my_message_fg": "#1b5e20",         # Dark green
        "timestamp": "#666666",             # Gray for timestamps
        "hyperlink": "#0000FF",             # Blue for hyperlinks
    },
    
    "dark": {
        "bg_main": "#212121",       # Main background - dark gray
        "bg_input": "#2c2c2c",       # Input area - lighter dark
        "status_bar": "#333333",     # Status bar background
        "status_text": "#bbbbbb",    # Status bar text
        
        # Message backgrounds
        "regular_message_bg": "#2c2c2c",    # Dark gray
        "regular_message_fg": "#e0e0e0",    # Light gray
        "system_message_bg": "#4a148c",     # Deep purple
        "system_message_fg": "#e1bee7",     # Light purple
        "error_message_bg": "#b71c1c",      # Dark red
        "error_message_fg": "#ffcdd2",      # Light red
        "dm_to_me_bg": "#b71c1c",           # Dark red
        "dm_to_me_fg": "#ffcdd2",           # Light red
        "dm_from_me_bg": "#0d47a1",         # Dark blue
        "dm_from_me_fg": "#bbdefb",         # Light blue
        "my_message_bg": "#1b5e20",         # Dark green
        "my_message_fg": "#c8e6c9",         # Light green
        "timestamp": "#9e9e9e",             # Gray for timestamps
        "hyperlink": "#64b5f6",             # Light blue for hyperlinks
    }
}

def get_theme(theme_name="light"):
    """Get the theme colors for the specified theme name"""
    return THEME_COLORS.get(theme_name, THEME_COLORS["light"])

# UI constants
WINDOW_SIZE = "800x500"  # Default window size for the client
FONT_REGULAR = ("Arial", 12)
FONT_BOLD = ("Arial", 12, "bold")
FONT_ITALIC = ("Arial", 12, "italic")
FONT_BOLD_ITALIC = ("Arial", 12, "bold italic")
FONT_TIMESTAMP = ("Arial", 10)

# Colors
COLOR_MY_MESSAGE = "#e6ffe6"  # Light green
COLOR_DM_TO_ME = "#ffe6e6"  # Light red
COLOR_DM_FROM_ME = "#e6e6ff"  # Light blue
COLOR_URL = "blue"

# Message style configuration
MESSAGE_STYLES = {
    "my_message": {
        "background": "#e8f5e9",  # Light green
        "foreground": "#1b5e20",  # Dark green
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
        "background": "#e3f2fd",  # Light blue
        "foreground": "#0d47a1",  # Dark blue
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
    "timestamp": {
        "font": FONT_TIMESTAMP,
        "foreground": "#666666"
    },
    "hyperlink": {
        "foreground": "#0000FF",  # Blue for hyperlinks
        "underline": True
    }
}
