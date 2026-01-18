import sys
import os
import tkinter as tk
from datetime import datetime

# Add project root to path for direct execution
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..', '..', '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy import Form, Application, Panel, Label, Button, TextBox, DockStyle, FlatStyle, Font, AnchorStyles
from winformpy.ui_elements.chat.chat_panel import ChatPanel


class ChatUI(Form):
    """
    A complete Messenger-style chat UI form with modern features.
    
    Features:
    - Header with title, search, and action buttons
    - Chat panel with avatars, timestamps, read status
    - Typing indicator animation
    - Context menu (right-click): Copy, Reply, Delete
    - Emoji picker
    - Search in conversation
    - Export and clear chat
    - User/Assistant name customization
    
    Properties:
        Title (str): The title displayed in the header.
        chat_panel (ChatPanel): Access to the underlying chat panel.
        UserName (str): Name for user messages.
        AssistantName (str): Name for assistant messages.
        
    Events:
        on_message_sent: Callback when user sends a message.
        on_clear_chat: Callback when chat is cleared.
    """
    
    # Common emojis for quick access
    QUICK_EMOJIS = ['😊', '👍', '❤️', '😂', '🎉', '👋', '🔥', '✨', '💡', '⭐']
    
    def __init__(self, title="WinFormPy Assistant", width=600, height=750, 
                 user_name="You", assistant_name="Assistant"):
        """
        Initialize the ChatUI form.
        
        Args:
            title: Window and header title.
            width: Form width in pixels.
            height: Form height in pixels.
            user_name: Display name for user messages.
            assistant_name: Display name for assistant messages.
        """
        super().__init__({
            'Text': title,
            'Width': width,
            'Height': height,
            'StartPosition': 'CenterScreen',
            'BackColor': '#FFFFFF'
        })
        
        # Configuration
        self.UserName = user_name
        self.AssistantName = assistant_name
        self._show_avatars = True
        self._show_timestamps = True
        self._show_status = True
        
        # Event callbacks
        self.on_message_sent = None
        self.on_clear_chat = None
        self._custom_response_handler = None
        
        # Search state
        self._search_visible = False
        self._search_results = []
        self._search_index = 0
        
        # CRITICAL: Apply layout before adding child controls
        self.ApplyLayout()
        
        # Build UI components
        self._create_header(title)
        self._create_search_bar()
        self._create_footer()
        self._create_emoji_bar()
        self._create_chat_panel()
        
        # Wire up custom message handling
        self._original_send_handler = self.chat_panel._on_send_click
        self.chat_panel._on_send_click = self._handle_send
    
    def _create_header(self, title):
        """Create the header panel with title and actions."""
        self.header = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 55,
            'BackColor': '#0078D4'
        })
        
        # Avatar/Status indicator
        if hasattr(self, '_root') and self._root:
            self._header_canvas = tk.Canvas(self.header._tk_widget, bg='#0078D4', 
                                            highlightthickness=0, width=40, height=40)
            self._header_canvas.place(x=10, y=7)
            # Draw online indicator
            self._header_canvas.create_oval(5, 5, 35, 35, fill='#00CC66', outline='#00AA55', width=2)
            self._header_canvas.create_text(20, 20, text="💬", font=('Segoe UI Emoji', 14))
        
        # Title label
        self.lbl_title = Label(self.header, {
            'Text': f"  {title}",
            'Font': Font("Segoe UI", 13, "Bold"),
            'ForeColor': '#FFFFFF',
            'BackColor': '#0078D4',
            'Left': 55,
            'Top': 8,
            'Width': 250,
            'Height': 25
        })
        
        # Subtitle (online status)
        self.lbl_subtitle = Label(self.header, {
            'Text': '  Online',
            'Font': Font("Segoe UI", 9),
            'ForeColor': '#B0D4F1',
            'BackColor': '#0078D4',
            'Left': 55,
            'Top': 30,
            'Width': 200,
            'Height': 18
        })
        
        # Search button
        self.btn_search = Button(self.header, {
            'Text': '🔍',
            'Width': 40,
            'Height': 35,
            'Top': 10,
            'FlatStyle': FlatStyle.Flat,
            'BackColor': '#0078D4',
            'ForeColor': '#FFFFFF',
            'Font': Font("Segoe UI Emoji", 12)
        })
        self.btn_search.Click = self._toggle_search
        
        # Clear button
        self.btn_clear = Button(self.header, {
            'Text': '🗑️',
            'Width': 40,
            'Height': 35,
            'Top': 10,
            'FlatStyle': FlatStyle.Flat,
            'BackColor': '#0078D4',
            'ForeColor': '#FFFFFF',
            'Font': Font("Segoe UI Emoji", 12)
        })
        self.btn_clear.Click = self._on_clear_click
        
        # Settings button
        self.btn_settings = Button(self.header, {
            'Text': '⚙️',
            'Width': 40,
            'Height': 35,
            'Top': 10,
            'FlatStyle': FlatStyle.Flat,
            'BackColor': '#0078D4',
            'ForeColor': '#FFFFFF',
            'Font': Font("Segoe UI Emoji", 12)
        })
        self.btn_settings.Click = self._on_settings_click
        
        # Position buttons on right side
        self._position_header_buttons()
        
        # Bind resize to reposition buttons
        self.Resize = self._on_form_resize
    
    def _create_search_bar(self):
        """Create collapsible search bar."""
        self.search_panel = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 0,  # Hidden by default
            'BackColor': '#E8E8E8'
        })
        
        self.txt_search = TextBox(self.search_panel, {
            'Left': 10,
            'Top': 8,
            'Width': 400,
            'Height': 28,
            'Font': Font("Segoe UI", 10)
        })
        
        self.btn_search_prev = Button(self.search_panel, {
            'Text': '▲',
            'Width': 35,
            'Height': 28,
            'Top': 8,
            'FlatStyle': FlatStyle.Flat
        })
        self.btn_search_prev.Click = lambda s, e: self._search_prev()
        
        self.btn_search_next = Button(self.search_panel, {
            'Text': '▼',
            'Width': 35,
            'Height': 28,
            'Top': 8,
            'FlatStyle': FlatStyle.Flat
        })
        self.btn_search_next.Click = lambda s, e: self._search_next()
        
        self.lbl_search_results = Label(self.search_panel, {
            'Text': '0/0',
            'Font': Font("Segoe UI", 9),
            'Top': 12,
            'Width': 60,
            'Height': 20
        })
        
        # Bind Enter key for search
        if hasattr(self.txt_search, '_tk_widget') and self.txt_search._tk_widget:
            self.txt_search._tk_widget.bind('<Return>', lambda e: self._do_search())
    
    def _create_emoji_bar(self):
        """Create emoji quick-access bar above input."""
        self.emoji_panel = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': 0,  # Hidden by default
            'BackColor': '#F8F8F8'
        })
        
        self._emoji_buttons = []
        for i, emoji in enumerate(self.QUICK_EMOJIS):
            btn = Button(self.emoji_panel, {
                'Text': emoji,
                'Left': 10 + i * 45,
                'Top': 5,
                'Width': 40,
                'Height': 35,
                'FlatStyle': FlatStyle.Flat,
                'BackColor': '#F8F8F8',
                'Font': Font("Segoe UI Emoji", 14)
            })
            btn.Click = lambda s, e, em=emoji: self._insert_emoji(em)
            self._emoji_buttons.append(btn)
    
    def _create_footer(self):
        """Create a footer with status information."""
        self.footer = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': 30,
            'BackColor': '#F0F0F0'
        })
        
        # Emoji toggle button
        self.btn_emoji = Button(self.footer, {
            'Text': '😊',
            'Left': 5,
            'Top': 2,
            'Width': 30,
            'Height': 26,
            'FlatStyle': FlatStyle.Flat,
            'BackColor': '#F0F0F0',
            'Font': Font("Segoe UI Emoji", 12)
        })
        self.btn_emoji.Click = self._toggle_emoji_bar
        
        self.lbl_status = Label(self.footer, {
            'Text': '  Ready',
            'Font': Font("Segoe UI", 9),
            'ForeColor': '#666666',
            'Left': 45,
            'Top': 6,
            'Width': 300,
            'Height': 20
        })
        
        self.lbl_msg_count = Label(self.footer, {
            'Text': 'Messages: 0',
            'Font': Font("Segoe UI", 9),
            'ForeColor': '#666666',
            'Top': 6,
            'Width': 100,
            'Height': 20
        })
        
        # Timestamp
        self.lbl_time = Label(self.footer, {
            'Text': datetime.now().strftime("%H:%M"),
            'Font': Font("Segoe UI", 9),
            'ForeColor': '#999999',
            'Top': 6,
            'Width': 50,
            'Height': 20
        })
        
        self._position_footer_labels()
        
        # Update time every minute
        self._update_time()
    
    def _update_time(self):
        """Update footer time display."""
        self.lbl_time.Text = datetime.now().strftime("%H:%M")
        if hasattr(self, '_root') and self._root:
            self._root.after(60000, self._update_time)
    
    def _position_header_buttons(self):
        """Position header buttons on the right side."""
        form_width = self.Width
        self.btn_settings.Left = form_width - 55
        self.btn_clear.Left = form_width - 100
        self.btn_search.Left = form_width - 145
        
        # Position search bar elements
        if hasattr(self, 'txt_search'):
            self.txt_search.Width = form_width - 180
            self.btn_search_prev.Left = form_width - 155
            self.btn_search_next.Left = form_width - 115
            self.lbl_search_results.Left = form_width - 75
    
    def _position_footer_labels(self):
        """Position footer labels."""
        self.lbl_msg_count.Left = self.Width - 200
        self.lbl_time.Left = self.Width - 70
    
    def _create_chat_panel(self):
        """Create the main chat panel."""
        self.chat_panel = ChatPanel(self, {
            'Dock': DockStyle.Fill,
            'BackColor': '#FFFFFF'
        })
    
    def _on_form_resize(self, sender=None, e=None):
        """Handle form resize to reposition elements."""
        self._position_header_buttons()
        self._position_footer_labels()
    
    def _toggle_search(self, sender=None, e=None):
        """Toggle search bar visibility."""
        self._search_visible = not self._search_visible
        self.search_panel.Height = 45 if self._search_visible else 0
        if self._search_visible and hasattr(self.txt_search, '_tk_widget'):
            self.txt_search._tk_widget.focus_set()
    
    def _toggle_emoji_bar(self, sender=None, e=None):
        """Toggle emoji bar visibility."""
        current_height = self.emoji_panel.Height
        self.emoji_panel.Height = 45 if current_height == 0 else 0
    
    def _insert_emoji(self, emoji):
        """Insert emoji into input box."""
        current_text = self.chat_panel.txt_input.Text
        self.chat_panel.txt_input.Text = current_text + emoji
        if hasattr(self.chat_panel.txt_input, '_tk_widget'):
            self.chat_panel.txt_input._tk_widget.focus_set()
    
    def _do_search(self):
        """Perform search in messages."""
        query = self.txt_search.Text.strip().lower()
        if not query:
            return
        
        self._search_results = []
        for i, msg in enumerate(self.chat_panel.manager.messages):
            if query in msg.text.lower():
                self._search_results.append(i)
        
        self._search_index = 0
        self._update_search_display()
    
    def _search_prev(self):
        """Go to previous search result."""
        if self._search_results:
            self._search_index = (self._search_index - 1) % len(self._search_results)
            self._update_search_display()
    
    def _search_next(self):
        """Go to next search result."""
        if self._search_results:
            self._search_index = (self._search_index + 1) % len(self._search_results)
            self._update_search_display()
    
    def _update_search_display(self):
        """Update search results display."""
        if self._search_results:
            self.lbl_search_results.Text = f"{self._search_index + 1}/{len(self._search_results)}"
            # Could highlight the message here
        else:
            self.lbl_search_results.Text = "0/0"
    
    def _handle_send(self, sender, e):
        """Handle send button click with custom logic."""
        text = self.chat_panel.txt_input.Text.strip()
        if text:
            # Update status
            self.lbl_status.Text = '  Sending...'
            
            # Send user message
            msg = self.chat_panel.manager.send_message(text)
            self.chat_panel.add_message_bubble(msg, 
                                                show_timestamp=self._show_timestamps,
                                                show_status=self._show_status,
                                                show_avatar=self._show_avatars)
            self.chat_panel.txt_input.Text = ""
            
            # Update message count
            msg_count = len(self.chat_panel.manager.messages)
            self.lbl_msg_count.Text = f'Messages: {msg_count}'
            
            # Fire event
            if self.on_message_sent:
                self.on_message_sent(text)
            
            # Show typing indicator
            self.chat_panel.show_typing_indicator(self.AssistantName)
            self.lbl_status.Text = f'  {self.AssistantName} is typing...'
            
            # Use custom handler or default
            if self._custom_response_handler:
                self.after(500, lambda: self._get_custom_response(text))
            else:
                self.after(1500, lambda: self._send_default_response())
    
    def _get_custom_response(self, user_message):
        """Get response from custom handler."""
        try:
            self.chat_panel.hide_typing_indicator()
            response = self._custom_response_handler(user_message)
            if response:
                msg = self.chat_panel.manager.receive_message(response)
                self.chat_panel.add_message_bubble(msg,
                                                    show_timestamp=self._show_timestamps,
                                                    show_status=self._show_status,
                                                    show_avatar=self._show_avatars)
                msg_count = len(self.chat_panel.manager.messages)
                self.lbl_msg_count.Text = f'Messages: {msg_count}'
                # Mark previous user message as read
                self._mark_last_user_message_read()
            self.lbl_status.Text = '  Ready'
        except Exception as ex:
            self.chat_panel.hide_typing_indicator()
            self.lbl_status.Text = f'  Error: {str(ex)}'
    
    def _send_default_response(self):
        """Send default OK response."""
        self.chat_panel.hide_typing_indicator()
        msg = self.chat_panel.manager.receive_message("OK")
        self.chat_panel.add_message_bubble(msg,
                                            show_timestamp=self._show_timestamps,
                                            show_status=self._show_status,
                                            show_avatar=self._show_avatars)
        msg_count = len(self.chat_panel.manager.messages)
        self.lbl_msg_count.Text = f'Messages: {msg_count}'
        self._mark_last_user_message_read()
        self.lbl_status.Text = '  Ready'
    
    def _mark_last_user_message_read(self):
        """Mark the last user message as read."""
        for msg in reversed(self.chat_panel.manager.messages):
            if msg.is_user:
                msg.is_read = True
                break
    
    def _on_clear_click(self, sender, e):
        """Handle clear button click."""
        self.clear_chat()
    
    def _on_settings_click(self, sender, e):
        """Show settings dialog."""
        self._show_settings_menu(sender)
    
    def _show_settings_menu(self, sender):
        """Show settings popup menu."""
        if hasattr(self, '_root') and self._root:
            menu = tk.Menu(self._root, tearoff=0)
            
            # Toggle options
            menu.add_checkbutton(label="Show Avatars", 
                                  command=lambda: self._toggle_setting('avatars'))
            menu.add_checkbutton(label="Show Timestamps", 
                                  command=lambda: self._toggle_setting('timestamps'))
            menu.add_checkbutton(label="Show Read Status", 
                                  command=lambda: self._toggle_setting('status'))
            menu.add_separator()
            menu.add_command(label="Export Chat...", command=self._export_chat_dialog)
            menu.add_separator()
            menu.add_command(label="About", command=self._show_about)
            
            # Position near the button
            x = self.btn_settings.Left + self._root.winfo_x()
            y = self.btn_settings.Top + self.header.Height + self._root.winfo_y() + 30
            menu.tk_popup(x, y)
    
    def _toggle_setting(self, setting):
        """Toggle a display setting."""
        if setting == 'avatars':
            self._show_avatars = not self._show_avatars
        elif setting == 'timestamps':
            self._show_timestamps = not self._show_timestamps
        elif setting == 'status':
            self._show_status = not self._show_status
        self.lbl_status.Text = f'  {setting.title()} toggled'
    
    def _export_chat_dialog(self):
        """Export chat to file."""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.export_history())
                self.lbl_status.Text = f'  Exported to {os.path.basename(filename)}'
        except Exception as ex:
            self.lbl_status.Text = f'  Export failed: {str(ex)}'
    
    def _show_about(self):
        """Show about dialog."""
        if hasattr(self, '_root') and self._root:
            from tkinter import messagebox
            messagebox.showinfo(
                "About ChatUI",
                "WinFormPy ChatUI\n\n"
                "A Messenger-style chat interface component.\n\n"
                "Features:\n"
                "• Message bubbles with avatars\n"
                "• Timestamps and read status\n"
                "• Typing indicator\n"
                "• Emoji picker\n"
                "• Search in conversation\n"
                "• Context menu (right-click)\n"
                "• Export chat history"
            )
    
    def after(self, ms, func):
        """Schedule a function to run after ms milliseconds."""
        if hasattr(self, '_root') and self._root:
            self._root.after(ms, func)
    
    # ===== Public API =====
    
    def set_response_handler(self, handler):
        """
        Set a custom response handler for processing user messages.
        
        Args:
            handler: A callable that takes a message string and returns a response string.
                    Example: lambda msg: f"You said: {msg}"
        """
        self._custom_response_handler = handler
    
    def send_message(self, text, is_user=False):
        """
        Programmatically send a message to the chat.
        
        Args:
            text: The message text.
            is_user: If True, display as user message (right side).
                    If False, display as assistant message (left side).
        """
        if is_user:
            msg = self.chat_panel.manager.send_message(text)
        else:
            msg = self.chat_panel.manager.receive_message(text)
        
        if msg:
            self.chat_panel.add_message_bubble(msg,
                                                show_timestamp=self._show_timestamps,
                                                show_status=self._show_status,
                                                show_avatar=self._show_avatars)
        
        msg_count = len(self.chat_panel.manager.messages)
        self.lbl_msg_count.Text = f'Messages: {msg_count}'
    
    def show_typing(self, name=None):
        """Show typing indicator."""
        self.chat_panel.show_typing_indicator(name or self.AssistantName)
        self.lbl_status.Text = f'  {name or self.AssistantName} is typing...'
    
    def hide_typing(self):
        """Hide typing indicator."""
        self.chat_panel.hide_typing_indicator()
        self.lbl_status.Text = '  Ready'
    
    def clear_chat(self):
        """Clear all messages from the chat."""
        # Clear manager history
        self.chat_panel.manager.clear_history()
        
        # Clear visual messages
        if hasattr(self.chat_panel, '_messages_frame') and self.chat_panel._messages_frame:
            for widget in self.chat_panel._messages_frame.winfo_children():
                widget.destroy()
        
        # Update UI
        self.lbl_msg_count.Text = 'Messages: 0'
        self.lbl_status.Text = '  Chat cleared'
        
        # Fire event
        if self.on_clear_chat:
            self.on_clear_chat()
    
    def get_history(self):
        """
        Get the chat message history.
        
        Returns:
            List of ChatMessage objects.
        """
        return self.chat_panel.manager.messages.copy()
    
    def export_history(self):
        """
        Export chat history as formatted text.
        
        Returns:
            str: Formatted chat history.
        """
        lines = []
        lines.append(f"Chat Export - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 50)
        for msg in self.chat_panel.manager.messages:
            sender = self.UserName if msg.is_user else self.AssistantName
            timestamp = msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            status = " ✓✓" if msg.is_read and msg.is_user else ""
            lines.append(f"[{timestamp}] {sender}{status}:")
            lines.append(f"  {msg.text}")
            lines.append("")
        return "\n".join(lines)
    
    @property
    def Title(self):
        """Get the header title."""
        return self.lbl_title.Text.strip()
    
    @Title.setter
    def Title(self, value):
        """Set the header title."""
        self.lbl_title.Text = f"  {value}"
        self.Text = value
    
    def set_online_status(self, is_online, status_text=None):
        """Set the online status indicator."""
        if is_online:
            self.lbl_subtitle.Text = f"  {status_text or 'Online'}"
            self.lbl_subtitle.ForeColor = '#B0D4F1'
        else:
            self.lbl_subtitle.Text = f"  {status_text or 'Offline'}"
            self.lbl_subtitle.ForeColor = '#FF9999'


# Backward compatibility alias
ChatForm = ChatUI


# =============================================================================
# Demo Application
# =============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("ChatUI Demo - Messenger-Style Chat Interface")
    print("=" * 60)
    
    # Create chat UI
    chat = ChatUI(
        title="WinFormPy Messenger", 
        width=650, 
        height=800,
        user_name="You",
        assistant_name="WinFormPy Bot"
    )
    
    # Set custom response handler
    def smart_handler(message):
        msg_lower = message.lower()
        if 'hello' in msg_lower or 'hi' in msg_lower:
            return "Hello! 👋 How can I help you today?"
        elif 'help' in msg_lower:
            return ("I can help you with:\n"
                    "• 🔍 Search - Click the magnifying glass\n"
                    "• 😊 Emojis - Click the emoji button\n"
                    "• ⚙️ Settings - Toggle display options\n"
                    "• Right-click a message to copy/reply/delete")
        elif 'emoji' in msg_lower:
            return "Try the emoji bar! Click 😊 in the footer. 🎉✨🔥"
        elif 'time' in msg_lower:
            return f"The current time is {datetime.now().strftime('%H:%M:%S')} ⏰"
        else:
            return f"You said: '{message}'\n\nTry saying 'help' for more info!"
    
    chat.set_response_handler(smart_handler)
    
    # Add welcome message
    chat.send_message(
        "Welcome to WinFormPy Messenger! 🎉\n\n"
        "This demo showcases Messenger-style features:\n\n"
        "✓ Avatars and timestamps\n"
        "✓ Read status (✓✓)\n"
        "✓ Typing indicator\n"
        "✓ Emoji quick-access bar\n"
        "✓ Search in conversation (🔍)\n"
        "✓ Right-click context menu\n"
        "✓ Settings menu (⚙️)\n\n"
        "Try typing 'help' to learn more!"
    )
    
    print("\nDemo Features:")
    print("  • Avatars with initials (U/A)")
    print("  • Timestamps on each message")
    print("  • Read status checkmarks (✓✓)")
    print("  • Typing indicator animation")
    print("  • Emoji picker (click 😊)")
    print("  • Search bar (click 🔍)")
    print("  • Right-click for context menu")
    print("  • Settings menu (click ⚙️)")
    print("  • Export chat to file")
    print("\nStarting Messenger-style chat...")
    
    Application.Run(chat)
