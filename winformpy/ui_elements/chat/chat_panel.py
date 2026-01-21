import sys
import os

# Add project root to path for imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..', '..', '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy.winformpy import (
    Panel, Label, Button, TextBox,
    DockStyle, AnchorStyles, Color, 
    Font, FlatStyle, Clipboard
)
from winformpy.ui_elements.chat.chat_manager import ChatManager
import tkinter as tk

class ChatBubble(Panel):
    """A single chat message bubble."""
    
    def __init__(self, parent, message, width=400, colors=None):
        """
        Initialize a chat bubble.
        
        Args:
            parent: Parent panel (usually ChatPanel)
            message: ChatMessage object
            width: Width of the bubble container
            colors: Optional dict with 'user_bubble', 'assistant_bubble' colors
        """
        super().__init__(parent, {
            'Width': width,
            'Height': 60,
            'BackColor': parent.BackColor
        })
        
        self.message = message
        self._container_width = width
        
        # Get colors from parent ChatPanel or use defaults
        if colors is None:
            colors = {}
        user_bubble_bg = colors.get('user_bubble', "#DCF8C6")
        assistant_bubble_bg = colors.get('assistant_bubble', "#F0F0F0")
        user_text_color = colors.get('user_text', "#000000")
        assistant_text_color = colors.get('assistant_text', "#000000")
        
        # Colors - User messages on right, Assistant on left
        if message.is_user:
            bubble_bg = user_bubble_bg
            text_color = user_text_color
        else:
            bubble_bg = assistant_bubble_bg
            text_color = assistant_text_color
        
        # Calculate bubble dimensions - max 75% of container width
        bubble_width = int(width * 0.75)
        
        # Position for user (right) or assistant (left)
        if message.is_user:
            bubble_left = width - bubble_width - 10
        else:
            bubble_left = 10
        
        # Create the bubble panel with correct position
        self.bubble = Panel(self, {
            'BackColor': bubble_bg,
            'Left': bubble_left,
            'Top': 5,
            'Width': bubble_width,
            'Height': 40
        })
        
        # Text label inside bubble
        self.lbl_text = Label(self.bubble, {
            'Text': message.text,
            'Font': Font("Segoe UI", 10),
            'ForeColor': text_color,
            'Left': 10,
            'Top': 8,
            'Width': bubble_width - 20,
            'AutoSize': True
        })

        # Configure text wrapping and calculate height
        req_height = 30  # Default height
        # Note: Direct tkinter - WinFormPy Label doesn't have wraplength property yet
        if hasattr(self.lbl_text, '_tk_widget') and self.lbl_text._tk_widget:
            self.lbl_text._tk_widget.config(wraplength=bubble_width - 25, justify='left')
            self.lbl_text.Refresh()
            req_height = self.lbl_text._tk_widget.winfo_reqheight()
        
        # Update bubble and container heights
        self.bubble.Height = req_height + 20
        self.Height = self.bubble.Height + 10
        
        # Store bubble position for later updates
        self._bubble_left = bubble_left
        self._bubble_width = bubble_width
    
    def _place_control(self, width=None, height=None):
        """Override to ensure bubble stays positioned correctly after FlowLayout places us."""
        super()._place_control(width, height)
        
        # Re-position the bubble after parent places us using WinFormPy properties
        if hasattr(self, '_bubble_left') and hasattr(self, 'bubble') and self.bubble:
            self.bubble.Left = self._bubble_left
            self.bubble.Top = 5
            self.bubble.Width = self._bubble_width


class ChatPanel(Panel):
    """A chat panel component with message bubbles and input area."""
    
    # Default colors
    COLORS = {
        'background': '#FFFFFF',
        'input_bg': '#F5F5F5',
        'button_bg': '#0078D4',
        'button_fg': '#FFFFFF',
        'user_bubble': '#DCF8C6',
        'assistant_bubble': '#F0F0F0'
    }
    
    def __init__(self, master_form, props=None, manager=None):
        """
        Initialize the ChatPanel.
        
        Args:
            master_form: Parent form or container
            props: Optional dictionary of properties. Supports sub-properties:
                - 'InputArea': {'Height': 60, 'BackColor': '#F5F5F5', ...}
                - 'SendButton': {'Text': '➤', 'BackColor': '#0078D4', 'Width': 60, ...}
                - 'MessageArea': {'BackColor': '#FFFFFF', ...}
                - 'UserBubble': {'BackColor': '#DCF8C6', 'ForeColor': '#000', ...}
                - 'AssistantBubble': {'BackColor': '#F0F0F0', 'ForeColor': '#000', ...}
            manager: Optional ChatManager instance. If None, a new one is created.
                    Pass a manager with a backend configured for external chat services.
                    
        Example:
            chat = ChatPanel(form, props={
                'Dock': DockStyle.Fill,
                'InputArea': {'Height': 80, 'BackColor': '#E0E0E0'},
                'SendButton': {'BackColor': '#107C10', 'Text': 'Send'},
                'UserBubble': {'BackColor': '#A8D8A8'}
            }, manager=my_manager)
        """
        # Extract sub-properties before passing to parent
        self._input_area_props = props.pop('InputArea', {}) if props else {}
        self._send_button_props = props.pop('SendButton', {}) if props else {}
        self._message_area_props = props.pop('MessageArea', {}) if props else {}
        self._user_bubble_props = props.pop('UserBubble', {}) if props else {}
        self._assistant_bubble_props = props.pop('AssistantBubble', {}) if props else {}
        
        default_props = {
            'Dock': DockStyle.Fill,
            'BackColor': '#FFFFFF'
        }
        if props:
            default_props.update(props)
            
        super().__init__(master_form, default_props)
        
        # Create instance copy of COLORS and apply sub-properties
        self.COLORS = self.COLORS.copy()
        if 'BackColor' in self._input_area_props:
            self.COLORS['input_bg'] = self._input_area_props['BackColor']
        if 'BackColor' in self._send_button_props:
            self.COLORS['button_bg'] = self._send_button_props['BackColor']
        if 'ForeColor' in self._send_button_props:
            self.COLORS['button_fg'] = self._send_button_props['ForeColor']
        if 'BackColor' in self._message_area_props:
            self.COLORS['background'] = self._message_area_props['BackColor']
        if 'BackColor' in self._user_bubble_props:
            self.COLORS['user_bubble'] = self._user_bubble_props['BackColor']
        if 'BackColor' in self._assistant_bubble_props:
            self.COLORS['assistant_bubble'] = self._assistant_bubble_props['BackColor']
        
        # Use provided manager or create a new one
        self.manager = manager if manager is not None else ChatManager()
        self.manager.on_message_received = self.add_message_bubble
        
        # Store responses for simulated conversation (fallback when no backend)
        self._response_index = 0
        self._simulated_responses = [
            "That's a great question! WinFormPy is designed to make GUI development intuitive.",
            "You can create buttons, panels, text boxes, and many more controls easily.",
            "For layout, I recommend using Dock and Anchor properties. Remember to call ApplyLayout() on your Form first!",
            "Here's a tip: Use `DockStyle.Fill` for controls that should expand to fill available space.",
            "If you need help with a specific control, just ask! I'm here to help. 😊",
            "WinFormPy wraps Tkinter with a Windows Forms-style API, making it familiar for .NET developers.",
            "Feel free to explore the examples in the 'examples/' folder for more inspiration!",
        ]
        
        # Build UI - Order matters for Dock!
        # 1. Input area at bottom (create first, dock bottom)
        self._create_input_area()
        
        # 2. Messages area fills remaining space
        self._create_messages_area()
        
    def _create_input_area(self):
        """Create the input area at the bottom."""
        # Apply InputArea sub-properties
        input_height = self._input_area_props.get('Height', 60)
        input_bg = self._input_area_props.get('BackColor', self.COLORS['input_bg'])
        
        self.input_container = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': input_height,
            'BackColor': input_bg
        })
        
        # Apply SendButton sub-properties
        btn_text = self._send_button_props.get('Text', '➤')
        btn_width = self._send_button_props.get('Width', 60)
        btn_bg = self._send_button_props.get('BackColor', self.COLORS['button_bg'])
        btn_fg = self._send_button_props.get('ForeColor', self.COLORS['button_fg'])
        btn_font = self._send_button_props.get('Font', Font("Segoe UI", 14))
        
        # Send Button (dock right first)
        self.btn_send = Button(self.input_container, {
            'Text': btn_text,
            'Dock': DockStyle.Right,
            'Width': btn_width,
            'FlatStyle': FlatStyle.Flat,
            'BackColor': btn_bg,
            'ForeColor': btn_fg,
            'Font': btn_font
        })
        self.btn_send.Click = self._on_send_click
        
        # Input Text Box (fills remaining space)
        self.txt_input = TextBox(self.input_container, {
            'Dock': DockStyle.Fill,
            'Multiline': True,
            'Font': Font("Segoe UI", 11),
            'BackColor': '#FFFFFF'
        })
        
        # Bind Enter key for sending using WinFormPy BindKey
        self.txt_input.BindKey('Return', self._on_enter_pressed)
    
    def _create_messages_area(self):
        """Create the scrollable messages area using tkinter Canvas."""
        # Apply MessageArea sub-properties
        msg_bg = self._message_area_props.get('BackColor', self.COLORS['background'])
        
        # Create a container panel that will hold the canvas
        self.messages_container = Panel(self, {
            'Dock': DockStyle.Fill,
            'BackColor': msg_bg
        })
        
        # Get the tkinter widget from the panel for custom canvas creation
        container_widget = self.messages_container.GetTkWidget()
        
        if container_widget:
            # Create Canvas for scrolling
            self._canvas = tk.Canvas(container_widget, bg='#FFFFFF', highlightthickness=0)
            self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Scrollbar (initially hidden - auto-hide behavior)
            self._scrollbar = tk.Scrollbar(container_widget, orient=tk.VERTICAL, command=self._canvas.yview)
            # Don't pack initially - will be shown when needed
            self._scrollbar_visible = False
            
            self._canvas.configure(yscrollcommand=self._on_scroll_update)
            
            # Inner frame for messages
            self._messages_frame = tk.Frame(self._canvas, bg='#FFFFFF')
            self._canvas_window = self._canvas.create_window((0, 0), window=self._messages_frame, anchor='nw')
            
            # Bind events
            self._messages_frame.bind('<Configure>', self._on_frame_configure)
            self._canvas.bind('<Configure>', self._on_canvas_configure)
            
            # Mouse wheel scrolling
            self._canvas.bind('<MouseWheel>', self._on_mousewheel)
            self._messages_frame.bind('<MouseWheel>', self._on_mousewheel)
        
        # Track current Y position for stacking messages
        self._next_message_y = 5
    
    def _on_scroll_update(self, first, last):
        """Handle scroll updates and auto-hide scrollbar."""
        if self._scrollbar:
            self._scrollbar.set(first, last)
            self._update_scrollbar_visibility()
    
    def _update_scrollbar_visibility(self):
        """Show/hide scrollbar based on whether it's needed."""
        if not self._scrollbar:
            return
        
        first, last = self._scrollbar.get()
        needed = not (float(first) <= 0.0 and float(last) >= 1.0)
        
        if needed and not self._scrollbar_visible:
            self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self._scrollbar_visible = True
        elif not needed and self._scrollbar_visible:
            self._scrollbar.pack_forget()
            self._scrollbar_visible = False
        
    def _on_frame_configure(self, event):
        """Update scroll region when frame content changes."""
        self._canvas.configure(scrollregion=self._canvas.bbox('all'))
        self._update_scrollbar_visibility()
    
    def _on_canvas_configure(self, event):
        """Update frame width when canvas is resized."""
        self._canvas.itemconfig(self._canvas_window, width=event.width)
        self._update_scrollbar_visibility()
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling - only scroll if scrollbar is needed."""
        if self._scrollbar_visible:
            self._canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        
    def _on_send_click(self, sender, e):
        """Handle send button click."""
        text = self.txt_input.Text.strip()
        if text:
            # Send user message (backend will be invoked if configured)
            msg = self.manager.send_message(text)
            self.add_message_bubble(msg)
            self.txt_input.Text = ""
            
            # Only simulate response if no backend is configured
            if not self.manager.has_backend:
                self.after(800, lambda: self._send_simulated_response())

    def _on_enter_pressed(self, event):
        """Handle Enter key in text box."""
        # Check if Shift is pressed (allow Shift+Enter for new line)
        if event.state & 0x0001:  # Shift pressed
            return  # Allow new line
        
        self._on_send_click(None, None)
        return "break"  # Prevent newline insertion

    def _send_simulated_response(self):
        """Send a simulated response from the assistant (fallback when no backend)."""
        # Simple OK response for demo
        self.manager.receive_message("OK")

    def _create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=15, **kwargs):
        """Draw a rounded rectangle on a canvas."""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
            x1 + radius, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    def add_message_bubble(self, message, show_timestamp=True, show_status=True, show_avatar=True):
        """Add a message bubble to the chat area with Messenger-like features."""
        if not hasattr(self, '_messages_frame') or not self._messages_frame:
            return
        
        # Calculate width based on canvas size
        canvas_width = self._canvas.winfo_width()
        if canvas_width < 100:
            canvas_width = 500  # Default width
        
        bubble_container_width = canvas_width - 20
        
        # Get colors from COLORS (may be customized via sub-properties)
        user_bubble_bg = self.COLORS.get('user_bubble', '#DCF8C6')
        assistant_bubble_bg = self.COLORS.get('assistant_bubble', '#F0F0F0')
        
        # Apply bubble-specific sub-properties
        user_fg = self._user_bubble_props.get('ForeColor', '#000000')
        assistant_fg = self._assistant_bubble_props.get('ForeColor', '#000000')
        
        # Colors for user vs assistant
        if message.is_user:
            bubble_bg = user_bubble_bg
            text_fg = user_fg
            avatar_bg = "#128C7E"  # Dark green
            avatar_text = "U"
        else:
            bubble_bg = assistant_bubble_bg
            text_fg = assistant_fg
            avatar_bg = "#0078D4"  # Blue
            avatar_text = "A"
        
        # Calculate bubble dimensions
        bubble_width = int(bubble_container_width * 0.70)
        
        # Create a temporary label to measure text height
        temp_label = tk.Label(self._messages_frame, text=message.text, 
                              font=('Segoe UI', 10), wraplength=bubble_width - 50)
        temp_label.update_idletasks()
        text_height = temp_label.winfo_reqheight()
        text_width = min(temp_label.winfo_reqwidth(), bubble_width - 50)
        temp_label.destroy()
        
        # Bubble dimensions with padding
        padding = 12
        timestamp_height = 15 if show_timestamp else 0
        actual_bubble_width = text_width + padding * 2 + 20
        actual_bubble_height = text_height + padding * 2 + timestamp_height
        
        # Avatar size
        avatar_size = 32 if show_avatar else 0
        
        # Container frame height
        container_height = max(actual_bubble_height, avatar_size) + 10
        
        # Container frame
        bubble_frame = tk.Frame(self._messages_frame, bg='#FFFFFF', height=container_height)
        bubble_frame.pack(fill=tk.X, padx=5, pady=3)
        bubble_frame.pack_propagate(False)
        
        # Create avatar if enabled
        if show_avatar:
            avatar_canvas = tk.Canvas(bubble_frame, bg='#FFFFFF', highlightthickness=0,
                                       width=avatar_size, height=avatar_size)
            # Draw circular avatar
            avatar_canvas.create_oval(2, 2, avatar_size-2, avatar_size-2, 
                                       fill=avatar_bg, outline=avatar_bg)
            avatar_canvas.create_text(avatar_size//2, avatar_size//2, 
                                       text=avatar_text, fill='white',
                                       font=('Segoe UI', 11, 'bold'))
        
        # Create canvas for rounded bubble
        bubble_canvas = tk.Canvas(bubble_frame, bg='#FFFFFF', highlightthickness=0,
                                   width=actual_bubble_width, height=actual_bubble_height)
        
        # Position based on sender
        if message.is_user:
            bubble_canvas.pack(side=tk.RIGHT, padx=5, pady=2)
            if show_avatar:
                avatar_canvas.pack(side=tk.RIGHT, padx=2, pady=2)
        else:
            if show_avatar:
                avatar_canvas.pack(side=tk.LEFT, padx=2, pady=2)
            bubble_canvas.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Draw rounded rectangle
        self._create_rounded_rectangle(bubble_canvas, 2, 2, 
                                        actual_bubble_width - 2, actual_bubble_height - 2,
                                        radius=12, fill=bubble_bg, outline=bubble_bg)
        
        # Add text on canvas
        text_x = padding + 5
        text_y = (actual_bubble_height - timestamp_height) // 2
        bubble_canvas.create_text(text_x, text_y, text=message.text, anchor='w',
                                   font=('Segoe UI', 10), fill='#000000',
                                   width=bubble_width - 50)
        
        # Add timestamp
        if show_timestamp:
            time_str = message.timestamp.strftime("%H:%M")
            time_x = actual_bubble_width - 10
            time_y = actual_bubble_height - 8
            bubble_canvas.create_text(time_x, time_y, text=time_str, anchor='e',
                                       font=('Segoe UI', 8), fill='#888888')
        
        # Add read status for user messages
        if show_status and message.is_user:
            status_x = actual_bubble_width - 35
            status_y = actual_bubble_height - 8
            if message.is_read:
                status_text = "✓✓"  # Read
                status_color = "#34B7F1"  # Blue checkmarks
            else:
                status_text = "✓"  # Sent
                status_color = "#888888"
            bubble_canvas.create_text(status_x, status_y, text=status_text, anchor='e',
                                       font=('Segoe UI', 8), fill=status_color)
        
        # Store reference to bubble for context menu
        bubble_canvas.message = message
        bubble_canvas.bubble_frame = bubble_frame
        
        # Bind events
        bubble_frame.bind('<MouseWheel>', self._on_mousewheel)
        bubble_canvas.bind('<MouseWheel>', self._on_mousewheel)
        bubble_canvas.bind('<Button-3>', lambda e: self._show_context_menu(e, message, bubble_frame))
        bubble_canvas.bind('<Double-Button-1>', lambda e: self._on_bubble_double_click(message))
        
        # Update and scroll to bottom
        self._messages_frame.update_idletasks()
        self._scroll_to_bottom()
        
        return bubble_frame
    
    def _show_context_menu(self, event, message, bubble_frame):
        """Show context menu for message bubble."""
        menu = tk.Menu(self._messages_frame, tearoff=0)
        menu.add_command(label="📋 Copy", command=lambda: self._copy_message(message))
        menu.add_command(label="↩️ Reply", command=lambda: self._reply_to_message(message))
        menu.add_separator()
        menu.add_command(label="🗑️ Delete", command=lambda: self._delete_message(message, bubble_frame))
        menu.tk_popup(event.x_root, event.y_root)
    
    def _copy_message(self, message):
        """Copy message text to clipboard using WinFormPy Clipboard class."""
        Clipboard.SetText(message.text)
    
    def _reply_to_message(self, message):
        """Set reply context for the message."""
        self._reply_to = message
        # Show reply preview in input area
        preview_text = message.text[:50] + "..." if len(message.text) > 50 else message.text
        self.txt_input.Text = f"↩️ {preview_text}\n"
        if hasattr(self.txt_input, '_tk_widget') and self.txt_input._tk_widget:
            self.txt_input._tk_widget.focus_set()
    
    def _delete_message(self, message, bubble_frame):
        """Delete a message from the chat."""
        # Remove from manager
        if message in self.manager.messages:
            self.manager.messages.remove(message)
        # Remove visual
        bubble_frame.destroy()
        self._messages_frame.update_idletasks()
    
    def _on_bubble_double_click(self, message):
        """Handle double-click on bubble (toggle read status for demo)."""
        message.is_read = not message.is_read
        # Could refresh the bubble here
    
    def show_typing_indicator(self, name="Assistant"):
        """Show typing indicator."""
        if hasattr(self, '_typing_indicator') and self._typing_indicator:
            return  # Already showing
        
        self._typing_indicator = tk.Frame(self._messages_frame, bg='#FFFFFF')
        self._typing_indicator.pack(fill=tk.X, padx=5, pady=3)
        
        # Create typing dots animation
        dots_canvas = tk.Canvas(self._typing_indicator, bg='#FFFFFF', 
                                 highlightthickness=0, width=60, height=30)
        dots_canvas.pack(side=tk.LEFT, padx=10)
        
        # Draw typing bubble
        self._create_rounded_rectangle(dots_canvas, 2, 2, 58, 28, 
                                        radius=10, fill='#F0F0F0', outline='#F0F0F0')
        
        # Create animated dots
        self._typing_dots = []
        for i in range(3):
            dot = dots_canvas.create_oval(12 + i*15, 12, 20 + i*15, 20, 
                                           fill='#888888', outline='#888888')
            self._typing_dots.append(dot)
        
        self._dots_canvas = dots_canvas
        self._animate_typing_dots(0)
        
        self._messages_frame.update_idletasks()
        self._scroll_to_bottom()
    
    def _animate_typing_dots(self, step):
        """Animate typing dots."""
        if not hasattr(self, '_typing_indicator') or not self._typing_indicator:
            return
        
        colors = ['#888888', '#AAAAAA', '#CCCCCC']
        for i, dot in enumerate(self._typing_dots):
            color_idx = (step + i) % 3
            self._dots_canvas.itemconfig(dot, fill=colors[color_idx])
        
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._tk_widget.after(300, lambda: self._animate_typing_dots((step + 1) % 3))
    
    def hide_typing_indicator(self):
        """Hide typing indicator."""
        if hasattr(self, '_typing_indicator') and self._typing_indicator:
            self._typing_indicator.destroy()
            self._typing_indicator = None
            self._typing_dots = None
            self._dots_canvas = None
    
    def _scroll_to_bottom(self):
        """Scroll the messages area to show the latest message."""
        if hasattr(self, '_canvas') and self._canvas:
            self._canvas.update_idletasks()
            self._canvas.yview_moveto(1.0)
        
    def after(self, ms, func):
        """Schedule a function to run after ms milliseconds."""
        # Note: Direct tkinter access - Timer not yet implemented in WinFormPy
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._tk_widget.after(ms, func)


# =============================================================================
# Demo Application
# =============================================================================
if __name__ == "__main__":
    from winformpy.winformpy import Form
    
    print("=" * 50)
    print("ChatPanel Demo - Simulated Conversation")
    print("=" * 50)
    
    # Create main form
    app = Form({
        'Text': "ChatPanel Demo - WinFormPy",
        'Width': 550,
        'Height': 650,
        'StartPosition': 'CenterScreen',
        'BackColor': '#FFFFFF'
    })
    
    # CRITICAL: Apply layout before adding child controls
    app.ApplyLayout()
    
    # Create chat panel
    chat_panel = ChatPanel(app)
    
    # Simulate a conversation with delays
    def show_conversation():
        # Initial greeting
        chat_panel.manager.receive_message(
            "Welcome to WinFormPy Chat! 👋\n\n"
            "I'm a demo assistant. Type a message and press Enter or click Send."
        )
        
        # Schedule more demo messages
        def add_user_msg():
            msg = chat_panel.manager.send_message("How do I create a button?")
            chat_panel.add_message_bubble(msg)
        
        def add_bot_msg():
            chat_panel.manager.receive_message(
                "Creating a button is easy! Here's an example:\n\n"
                "btn = Button(form, {\n"
                "    'Text': 'Click Me',\n"
                "    'Left': 10,\n"
                "    'Top': 10\n"
                "})\n"
                "btn.Click = my_handler"
            )
        
        def add_user_msg2():
            msg = chat_panel.manager.send_message("What about layout?")
            chat_panel.add_message_bubble(msg)
        
        def add_bot_msg2():
            chat_panel.manager.receive_message(
                "For layout, use Dock and Anchor:\n\n"
                "• Dock.Fill - fills available space\n"
                "• Dock.Top/Bottom/Left/Right\n"
                "• Anchor for relative positioning\n\n"
                "Remember: Call form.ApplyLayout() first!"
            )
        
        # Schedule the conversation
        chat_panel.after(1500, add_user_msg)
        chat_panel.after(2500, add_bot_msg)
        chat_panel.after(5000, add_user_msg2)
        chat_panel.after(6000, add_bot_msg2)
    
    # Start the demo conversation
    show_conversation()
    
    print("\nDemo Features:")
    print("  • Type messages and press Enter to send")
    print("  • User messages appear on the right (green)")
    print("  • Assistant messages appear on the left (gray)")
    print("  • Simulated responses after each message")
    print("\nStarting chat window...")
    
    app.ShowDialog()
