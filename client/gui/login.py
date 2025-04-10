"""
Login UI Implementation
Handles the login interface for the chat client with a compact design
"""

import os
import darkdetect
import tkinter as tk

if os.name == "posix":
    from tkmacosx import Button
else:
    # For Windows and Linux, use the standard tkinter Button
    # NOTE Linux may have issues on Xorg desktop environments
    from tkinter import Button
from tkinter import Frame, Label, messagebox, Entry, StringVar, Radiobutton

from client.theme import FONT_BOLD, FONT_REGULAR, FONT_HEADING, FONT_SUBHEADING


class LoginGUI:
    """Login interface for the chat client"""

    def __init__(
        self, root: tk.Tk, client: any, theme: str = darkdetect.theme().lower()
    ) -> None:
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
        self.theme_var = None  # Will hold the StringVar for theme selection

    def setup_login_frame(self) -> None:
        """Create a compact login frame with username input and connect button"""
        # Clear any existing frames
        if self.login_frame:
            self.login_frame.destroy()

        # Update colors from client
        self.colors = self.client.colors
        self.theme = self.client.theme

        # Create a smaller centered frame rather than filling the window
        self.login_frame = Frame(
            self.root, bg=self.colors["bg_main"], bd=1, relief=tk.SOLID
        )
        # Position the frame in the center with fixed width
        self.login_frame.place(
            relx=0.5, rely=0.5, anchor=tk.CENTER, width=380, height=250
        )

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
            anchor="e",
        ).grid(row=0, column=0, sticky="e", pady=2)

        self.username_entry = Entry(
            form_frame,
            bg=self.colors["bg_input"],
            fg=self.colors["fg_input"],
            insertbackground=self.colors["fg_input"],
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
            anchor="e",
        ).grid(row=1, column=0, sticky="e", pady=2)

        self.port_entry = Entry(
            form_frame,
            font=FONT_REGULAR,
            bd=1,
            relief=tk.GROOVE,
            width=15,
            bg=self.colors["bg_input"],
            fg=self.colors["fg_input"],
            # cursor color
            insertbackground=self.colors["fg_input"],
        )
        self.port_entry.insert(0, str(self.client.port))
        self.port_entry.grid(row=1, column=1, sticky="ew", pady=2, ipady=3)

        # Theme row
        Label(
            form_frame,
            text="Theme:",
            bg=self.colors["bg_main"],
            font=FONT_BOLD,
            width=8,
            anchor="e",
        ).grid(row=2, column=0, sticky="e", pady=2)

        # Theme radio buttons instead of dropdown
        self.theme_var = StringVar(form_frame)
        self.theme_var.set(self.theme)  # Set to current theme

        # Create a frame for radio buttons
        theme_frame = Frame(form_frame, bg=self.colors["bg_main"])
        theme_frame.grid(row=2, column=1, sticky="ew", pady=2)

        # Light theme radio button
        light_radio = Radiobutton(
            theme_frame,
            text="Light",
            variable=self.theme_var,
            value="light",
            command=self._on_theme_change,
            bg=self.colors["bg_main"],
            fg=self.colors["fg_main"],
            font=FONT_REGULAR,
            selectcolor=self.colors["bg_input"],
        )
        light_radio.pack(side=tk.LEFT, padx=(0, 10))

        # Dark theme radio button
        dark_radio = Radiobutton(
            theme_frame,
            text="Dark",
            variable=self.theme_var,
            value="dark",
            command=self._on_theme_change,
            bg=self.colors["bg_main"],
            fg=self.colors["fg_main"],
            font=FONT_REGULAR,
            selectcolor=self.colors["bg_input"],
        )
        dark_radio.pack(side=tk.LEFT)

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

    def _on_theme_change(self, *args) -> None:
        """Handle theme change from radio buttons"""
        selected_theme = self.theme_var.get()
        if selected_theme != self.theme:
            # Update client theme
            self.client.update_theme(selected_theme)
            # Update local theme
            self.theme = selected_theme
            self.colors = self.client.colors
            # Refresh UI with new theme
            self.setup_login_frame()

    def connect_to_server(self) -> None:
        """Connect to the chat server with the entered username and apply theme"""
        username = self.username_entry.get().strip()

        if not username:
            messagebox.showerror("Error", "Username cannot be empty")
            return

        try:
            port = int(self.port_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Port must be a number")
            return

        # Get selected theme
        selected_theme = self.theme_var.get()

        # Update client with port and theme
        self.client.port = port
        self.client.update_theme(selected_theme)

        # Try to connect using the client
        if self.client.connect_to_server(username):
            # Switch from login frame to chat frame
            self.login_frame.destroy()
            self.login_frame = None
            self.client.setup_chat_ui()
        else:
            messagebox.showerror("Connection Error", "Could not connect to server")
