"""
Chat UI Implementation
Handles the chat interface for the chat client with enhanced visual styling
"""
import os
import tkinter as tk
if os.name == "posix":
    from tkmacosx import Button
else:
    # For Windows and Linux, use the standard tkinter Button
    from tkinter import Button
from tkinter import scrolledtext, Frame, Label, messagebox, Canvas
import queue
import datetime
import webbrowser

from client.utils import process_emoji_shortcodes, extract_urls
from client.tkHyperlinkManager import HyperlinkManager
from common.constants import (
    DM_FROM,
    DM_TO,
    ERROR_MESSAGE,
    WARNING_MESSAGE,
    INFO_MESSAGE,
    SUCCESS_MESSAGE,
    DEBUG_MESSAGE,
    ANNOUNCEMENT
)
from client.theme import FONT_BOLD, FONT_REGULAR, MESSAGE_STYLES


class ChatGUI:
    """Chat interface for the chat client"""

    def __init__(self, root, client):
        """Initialize the chat UI with root window and client reference"""
        self.root = root
        self.client = client
        self.colors = self.client.colors
        self.chat_frame = None
        self.chat_display = None
        self.hyperlink_manager = None
        self.message_entry = None
        self.update_timer = None
        self.status_label = None

    def setup_chat_frame(self):
        """Create main chat interface with proper color constants for message types"""
        if self.chat_frame:
            self.chat_frame.destroy()

        self.chat_frame = Frame(self.root, bg=self.colors["bg_main"])
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        # Set window title with username
        self.root.title(
            f"TCP Socket Chat App - {self.client.username} ({self.client.host}:{self.client.port})"
        )

        # Add header with user info and disconnect button
        header_frame = Frame(self.chat_frame, bg=self.colors["bg_main"], padx=10, pady=8)
        header_frame.pack(fill=tk.X)
        
        # Add avatar placeholder (circle)
        avatar_size = 30
        avatar_canvas = Canvas(
            header_frame, 
            width=avatar_size, 
            height=avatar_size, 
            bg=self.colors["bg_main"], 
            highlightthickness=0
        )
        avatar_canvas.pack(side=tk.LEFT, padx=(0, 10))
        
        # Draw avatar square
        avatar_canvas.create_rectangle(
            0, 0, avatar_size, avatar_size,
            fill=self.colors["primary"],
            outline=self.colors["primary"],
        )
        avatar_canvas.create_text(
            avatar_size/2, avatar_size/2,
            text=self.client.username[0].upper(),
            fill=self.colors["primary_fg"],
            font=FONT_BOLD
        )
        
        # Green dot for online status
        online_status = Label(
            header_frame, 
            text="●", 
            bg=self.colors["bg_main"], 
            fg=self.colors["online_status"],
            font=FONT_BOLD
        )
        online_status.pack(side=tk.LEFT)
        
        user_label = Label(
            header_frame, 
            text=f"Logged in as: {self.client.username}",
            bg=self.colors["bg_main"],
            font=FONT_BOLD,
        )
        user_label.pack(side=tk.LEFT)

        # Disconnect button with default styling
        self.disconnect_button = Button(
            header_frame, 
            text="Disconnect", 
            command=self.disconnect_from_server,
            font=FONT_BOLD,
            padx=10,
            pady=2,
            cursor="hand2",
            background=self.colors["disconnect_button_bg"],
            foreground=self.colors["disconnect_button_fg"],
        )
        self.disconnect_button.pack(side=tk.RIGHT)

        # Chat area with messages display
        chat_area = Frame(self.chat_frame, bg=self.colors["bg_main"], highlightbackground=self.colors["primary"])
        chat_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Messages display with rounded corners and border
        self.chat_display = scrolledtext.ScrolledText(
            chat_area, 
            wrap=tk.WORD, 
            font=FONT_REGULAR,
            bg=self.colors["bg_input"],
            bd=1,
            relief=tk.SOLID,
            padx=8,
            pady=8,
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)

        # Initialize hyperlink manager
        self.hyperlink_manager = HyperlinkManager(self.chat_display)

        # Configure tags for different message types using imported constants
        for tag_name, style in MESSAGE_STYLES.items():
            self.chat_display.tag_configure(tag_name, **style)

        # Message input area with improved styling
        input_frame = Frame(self.chat_frame, bg=self.colors["bg_main"], pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.message_entry = scrolledtext.ScrolledText(
            input_frame, 
            wrap=tk.WORD, 
            height=3, 
            font=FONT_REGULAR,
            bg=self.colors["bg_input"],
            bd=1,
            relief=tk.SOLID,
            padx=8,
            pady=8
        )
        self.message_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)
        self.message_entry.focus()

        # Bind key events for emoji processing as you type
        self.message_entry.bind("<KeyRelease>", self.process_emoji_as_you_type)

        # Send button with default styling
        self.send_button = Button(
            input_frame, 
            text="Send", 
            command=self.send_message,
            font=FONT_BOLD,
            padx=15,
            pady=5,
            cursor="hand2",
            background=self.colors["primary"],
            foreground=self.colors["primary_fg"],
        )
        self.send_button.pack(side=tk.RIGHT, padx=5)

        # Bind Enter key to send message (Shift+Enter for new line)
        self.message_entry.bind("<Return>", self.handle_return_key)
        
        # Add a status bar
        self.status_frame = Frame(self.chat_frame, bg=self.colors["primary"], height=20)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = Label(
            self.status_frame, 
            text=f"Connected to {self.client.host}:{self.client.port}", 
            bg=self.colors["primary"], 
            fg=self.colors["primary_fg"],
            anchor="w",
            padx=10
        )
        self.status_label.pack(side=tk.LEFT)

        # Add connection indicator
        self.connection_indicator = Label(
            self.status_frame,
            text="●",
            bg=self.colors["primary"],
            fg=self.colors["online_status"],
            padx=10
        )
        self.connection_indicator.pack(side=tk.RIGHT)
        
        # Start message processing
        self.start_message_processing()

    def disconnect_from_server(self):
        """Disconnect from the server and return to login screen"""
        self.client.disconnect()

        # Stop the message processing timer
        if self.update_timer:
            self.root.after_cancel(self.update_timer)
            self.update_timer = None

        # Clear any existing data
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        if self.message_entry:
            self.message_entry.delete("1.0", tk.END)
        
        # Destroy the chat frame completely
        if self.chat_frame:
            self.chat_frame.destroy()
            self.chat_frame = None
            self.chat_display = None
            self.message_entry = None
            self.status_label = None

        # Return to login screen
        self.client.setup_login_ui()

    def start_message_processing(self):
        """Start processing messages from the queue"""
        # Cancel any existing timer
        if self.update_timer:
            self.root.after_cancel(self.update_timer)

        # Start a new timer
        self.update_timer = self.root.after(100, self.process_messages)

    def process_messages(self):
        """Process messages from the queue and update UI"""
        try:
            while not self.client.message_queue.empty():
                message = self.client.message_queue.get_nowait()
                self.display_message(message)
        except queue.Empty:
            pass

        if self.client.running:
            self.update_timer = self.root.after(100, self.process_messages)

    def display_message(self, message):
        """Add a message to the chat display with proper styling for URLs and message types"""
        if not self.chat_display:
            return

        self.chat_display.config(state=tk.NORMAL)

        # Determine message type for formatting
        if message.startswith(f"@{self.client.username}: "):
            msg_tag = "my_message"
        elif message.startswith(DM_FROM):
            msg_tag = "dm_to_me"
        elif message.startswith(DM_TO):
            msg_tag = "dm_from_me"
        elif message.startswith(ERROR_MESSAGE):
            msg_tag = "error_message"
        elif message.startswith(WARNING_MESSAGE):
            msg_tag = "warning_message"  
        elif message.startswith(INFO_MESSAGE):
            msg_tag = "info_message"
        elif message.startswith(SUCCESS_MESSAGE):
            msg_tag = "success_message"
        elif message.startswith(DEBUG_MESSAGE):
            msg_tag = "debug_message"
        elif message.startswith(ANNOUNCEMENT):
            msg_tag = "announcement"
        else:
            msg_tag = "regular"

        # Add timestamp
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Insert message prefix ([DM from/to] or [System] or [Error] or username)
        message_prefix = message.split(": ", 1)[0]
        self.chat_display.insert(tk.END, f"{message_prefix}", msg_tag)
        self.chat_display.insert(tk.END, "\t")
        
        # Get message content after prefix
        message = message.split(": ", 1)[1] if ": " in message else message
        
        # Extract URLs from the message
        urls = extract_urls(message)
        
        if urls:
            # Insert message with clickable URLs
            current_pos = 0
            for url_start, url_end, url in urls:
                # Insert text before URL
                if url_start > current_pos:
                    self.chat_display.insert(tk.END, message[current_pos:url_start])
                
                # Insert the URL with hyperlink tags and the url tag
                url_text = message[url_start:url_end]
                hyperlink_tags = self.hyperlink_manager.add(lambda u=url: webbrowser.open(u))
                self.chat_display.insert(tk.END, url_text, hyperlink_tags)
                
                current_pos = url_end
            
            # Insert any remaining text after the last URL
            if current_pos < len(message):
                self.chat_display.insert(tk.END, message[current_pos:])
        else:
            # No URLs, insert the whole message
            self.chat_display.insert(tk.END, message)

        # Add a newline at the end
        self.chat_display.insert(tk.END, "\n")
        
        # Scroll to bottom
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def process_emoji_as_you_type(self, event):
        """Process emoji shortcodes as the user types"""
        if not self.message_entry:
            return

        current_text = self.message_entry.get("1.0", tk.END)

        # Don't process if no potential shortcodes
        if ":" not in current_text:
            return

        # Process text with emojis
        processed_text = process_emoji_shortcodes(current_text)

        # Only update if there was a change
        if processed_text != current_text:
            cursor_pos = self.message_entry.index(tk.INSERT)
            self.message_entry.delete("1.0", tk.END)
            self.message_entry.insert("1.0", processed_text)

            # Try to keep cursor position
            try:
                self.message_entry.mark_set(tk.INSERT, cursor_pos)
            except:
                pass

    def send_message(self):
        """Send message to server"""
        if not self.message_entry:
            return

        message = self.message_entry.get("1.0", tk.END).strip()
        if not message:
            return

        # Process emoji shortcodes
        message = process_emoji_shortcodes(message)

        # Send via client
        if self.client.send_message(message):
            self.message_entry.delete("1.0", tk.END)
            
            # Update status temporarily to show message sent
            self.status_label.config(text="Message sent!")
            self.root.after(2000, lambda: self.status_label.config(
                text=f"Connected to {self.client.host}:{self.client.port}")
            )

    def handle_return_key(self, event):
        """Handle Return key press in message entry field"""
        # If Shift+Enter is pressed, allow newline
        if event.state & 0x1:  # Shift is pressed
            return

        # Otherwise send the message
        self.send_message()
        return "break"  # Prevent default behavior

    def handle_server_disconnect(self):
        """Handle server disconnect event"""
        # Stop the message processing timer
        if self.update_timer:
            self.root.after_cancel(self.update_timer)
            self.update_timer = None

        # Show disconnect message and return to login screen
        if self.root.winfo_exists():
            messagebox.showwarning(
                "Disconnected", "You have been disconnected from the server."
            )
            # Setup login UI again
            self.client.setup_login_ui()