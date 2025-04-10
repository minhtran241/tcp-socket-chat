"""
Login UI Implementation
Handles the login interface for the chat client with a compact design
"""

import os
import tkinter as tk
if os.name == "posix":
    from tkmacosx import Button
else:
    # For Windows and Linux, use the standard tkinter Button
    #NOTE Linux may have issues on Xorg desktop environments
    from tkinter import Button
from tkinter import Frame, Label, messagebox, Entry

from client.theme import FONT_BOLD, FONT_REGULAR, FONT_HEADING, FONT_SUBHEADING


class LoginGUI:
    """Login interface for the chat client"""

    def __init__(self, root:tk.Tk, client:"client.ChatClient", theme:str="light") -> None:
        """Initialize the login UI with root window and client reference"""
        self.root = root
        self.client = client
        self.theme = theme
        self.colors = self.client.colors
        self.login_frame = None
        self.username_entry = None
        self.host = self.client.host
        self.port_entry = self.client.port
        self.connect_button = None

    def setup_login_frame(self) -> None:
        """Create a compact login frame with username input and connect button"""
        # Clear any existing frames
        if self.login_frame:
            self.login_frame.destroy()

        # Create a smaller centered frame rather than filling the window
        self.login_frame = Frame(
            self.root, 
            bg=self.colors["bg_main"],
            bd=1,
            relief=tk.SOLID
        )
        # Position the frame in the center with fixed width
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=380, height=210)

        # Add app title
        title_label = Label(
            self.login_frame, 
            text="TCP Socket Chat App", 
            font=FONT_HEADING,
            fg=self.colors["primary"],
            bg=self.colors["bg_main"],
        )
        title_label.pack(pady=(10, 0))
        # Add subtitle
        subtitle_label = Label(
			self.login_frame,	
            text="Login to Chat",
            font=FONT_SUBHEADING,
            bg=self.colors["bg_main"],
		)
        subtitle_label.pack(pady=(0, 10))

        # Create a form layout with grid
        form_frame = Frame(self.login_frame, bg=self.colors["bg_main"])
        form_frame.pack(fill=tk.X, padx=20)
        
        # Username row
        Label(
            form_frame, 
            text="Username:", 
            bg=self.colors["bg_main"],
            font=FONT_BOLD,
            width=8,
            anchor="e"
        ).grid(row=0, column=0, sticky="e", pady=2)
        
        self.username_entry = Entry(
            form_frame, 
            font=FONT_REGULAR,
            bd=1,
            relief=tk.GROOVE,
            width=15,
        )
        self.username_entry.grid(row=0, column=1, sticky="ew", pady=2, ipady=3)
        self.username_entry.focus()
        
        # Port row
        Label(
            form_frame, 
            text="Port:", 
            bg=self.colors["bg_main"],
            font=FONT_BOLD,
            width=8,
            anchor="e"
        ).grid(row=1, column=0, sticky="e", pady=2)
        
        self.port_entry = Entry(
            form_frame, 
            font=FONT_REGULAR,
            bd=1,
            relief=tk.GROOVE,
            width=15
        )
        self.port_entry.insert(0, str(self.client.port))
        self.port_entry.grid(row=1, column=1, sticky="ew", pady=2, ipady=3)
        
        # Configure column to expand
        form_frame.columnconfigure(1, weight=1)
        
        # Connect button with default styling
        self.connect_button = Button(
            self.login_frame, 
            text="Connect",
            command=self.connect_to_server,
            font=FONT_BOLD,
            padx=10,
            pady=5,
            cursor="hand2",
            background=self.colors["primary"],
			foreground=self.colors["primary_fg"],
        )
        self.connect_button.pack(pady=15)
        
        # Bind Enter key to connect function
        self.username_entry.bind("<Return>", lambda event: self.connect_to_server())
        self.port_entry.bind("<Return>", lambda event: self.connect_to_server())

    def connect_to_server(self) -> None:
        """Connect to the chat server with the entered username"""
        username = self.username_entry.get().strip()

        if not username:
            messagebox.showerror("Error", "Username cannot be empty")
            return

        try:
            port = int(self.port_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Port must be a number")
            return

        # Update client host and port
        self.client.port = port

        # Try to connect using the client
        if self.client.connect_to_server(username):
            # Switch from login frame to chat frame
            self.login_frame.destroy()
            self.login_frame = None
            self.client.setup_chat_ui()
        else:
            messagebox.showerror("Connection Error", "Could not connect to server")