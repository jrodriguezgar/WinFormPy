# 💬 Chat UI Module

A Messenger-style chat interface component with modern features.

> ⚠️ **Architecture-agnostic**: This component delegates message sending to an **external backend** (`ChatBackend`). You provide the integration with your AI service, WebSocket server, or chat API.

> **📦 Component Structure**: This module provides:
> - `ChatPanel` - Embeddable panel for any Form/Panel
> - `ChatUI` - Standalone form that **uses ChatPanel internally** (access via `.chat_panel` property)

## Quick Demo

Run the demos to see the component in action:

```bash
# Interactive demo with response handlers and features
python winformpy/ui_elements/chat/chat_panel.py

# Minimal standalone form (for integration in your app)
python winformpy/ui_elements/chat/chat_ui.py
```

## 📖 Overview

This module provides a complete chat UI solution with Messenger-like features:

### Core Features
- ✅ Message bubbles with rounded corners
- ✅ User messages aligned right (green)
- ✅ Assistant messages aligned left (gray)
- ✅ Scrollable message area
- ✅ Input area with send button
- ✅ Full state management
- ✅ **Pluggable backend** for external chat services

### Messenger-Style Features
- 👤 **Avatars** - Circular avatars with user initials
- ⏰ **Timestamps** - HH:MM display on each message
- ✓✓ **Read Status** - Sent (✓) and Read (✓✓ blue) indicators
- 💬 **Typing Indicator** - Animated "typing..." animation
- 🔍 **Search** - Search within conversation
- 😊 **Emoji Picker** - Quick-access emoji bar
- 📋 **Context Menu** - Right-click to Copy, Reply, Delete
- ⚙️ **Settings** - Toggle avatars, timestamps, read status
- 📤 **Export** - Save conversation to text file

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│  ChatUI (Complete Form)                             │
│  - Header with avatar, title, online status         │
│  - Search bar (collapsible)                         │
│  - Emoji quick-access bar                           │
│  - Footer with status, count, timestamp             │
│  - Uses ChatPanel internally                        │
├─────────────────────────────────────────────────────┤
│  ChatPanel (Embeddable Panel)                       │
│  - Messages area with scrolling                     │
│  - Rounded chat bubbles with avatars                │
│  - Typing indicator animation                       │
│  - Context menu support                             │
├─────────────────────────────────────────────────────┤
│  ChatManager (Service Layer)                        │
│  - Message history                                  │
│  - State management (ChatState enum)                │
│  - Read/unread tracking                             │
│  - Delegates to optional backend                    │
├─────────────────────────────────────────────────────┤
│  ⚠️ EXTERNAL (not part of this project)             │
│  ChatBackend (ChatBackend implementation)       │
│  - API calls to chat services                       │
│  - WebSocket connections                            │
│  - AI/LLM integrations                              │
└─────────────────────────────────────────────────────┘
```

**⚠️ IMPORTANT**: The Chat Backend is **NOT part of this project**. It must be provided externally.

---

## 📋 Chat Backend Contract (External)

The external backend must implement `ChatBackend` for connecting to chat services:

```python
from winformpy.ui_elements.chat import ChatBackend

class MyChatBackend(ChatBackend):
    """Required interface for the Chat Backend (external)."""
    
    # === Required Method ===
    
    def send_message(self, text: str, context: list = None) -> str | None:
        """
        Send a message and receive a response.
        
        Args:
            text: User's message text
            context: Previous messages for conversation context
            
        Returns:
            str: Response text, or None if async
        """
        pass
    
    # === Optional Methods ===
    
    def connect(self) -> bool:
        """Connect to the chat service. Returns True if successful."""
        return True
    
    def disconnect(self) -> None:
        """Disconnect from the chat service."""
        pass
    
    def get_history(self, limit: int = None) -> list:
        """Retrieve message history from external storage."""
        return []
    
    def save_history(self, messages: list) -> bool:
        """Save message history to external storage."""
        return True
```

---

## 📦 Components

| Component | Type | Description |
|-----------|------|-------------|
| `ChatUI` | Form | Complete Messenger-style chat window |
| `ChatPanel` | Panel | Embeddable chat panel with full features |
| `ChatManager` | Service | Manages message history and state |
| `ChatBackend` | ABC | Abstract base class for external backends |
| `ChatMessage` | Model | Represents a single message with metadata |
| `ChatState` | Enum | Conversation state values |

---

## 🚀 Quick Start

### Using ChatUI (Complete Form)

```python
from winformpy import Application
from winformpy.ui_elements.chat import ChatUI

# Create Messenger-style chat window
chat = ChatUI(
    title="My Assistant",
    width=650, 
    height=800,
    user_name="You",
    assistant_name="Bot"
)

# Set custom response handler
def my_handler(user_message):
    return f"You said: {user_message}"

chat.set_response_handler(my_handler)

# Add welcome message
chat.send_message("Hello! 👋 How can I help you?")

Application.Run(chat)
```

### Using ChatPanel (Embeddable)

```python
from winformpy import Form, Application
from winformpy.ui_elements.chat import ChatPanel

form = Form({'Text': 'My Chat App', 'Width': 550, 'Height': 700})
form.ApplyLayout()

chat = ChatPanel(form)
chat.manager.receive_message("Welcome! How can I help you?")

Application.Run(form)
```

### Customizing with Sub-Properties

ChatPanel supports sub-properties for configuring internal elements:

```python
from winformpy import Form, Application, DockStyle, Font
from winformpy.ui_elements.chat import ChatPanel

form = Form({'Text': 'Custom Chat', 'Width': 550, 'Height': 700})
form.ApplyLayout()

# Configure internal elements with sub-properties
chat = ChatPanel(form, props={
    'Dock': DockStyle.Fill,
    
    # Configure input area at the bottom
    'InputArea': {
        'Height': 80,
        'BackColor': '#E8E8E8'
    },
    
    # Configure send button
    'SendButton': {
        'Text': 'Send',
        'BackColor': '#107C10',
        'ForeColor': '#FFFFFF',
        'Width': 70
    },
    
    # Configure message area background
    'MessageArea': {
        'BackColor': '#F5F5F5'
    },
    
    # Configure user message bubbles
    'UserBubble': {
        'BackColor': '#A8D8A8',  # Lighter green
        'ForeColor': '#000000'
    },
    
    # Configure assistant message bubbles
    'AssistantBubble': {
        'BackColor': '#E0E0E0',
        'ForeColor': '#333333'
    }
})

Application.Run(form)
```

#### Available Sub-Properties

| Sub-Property | Keys | Description |
|--------------|------|-------------|
| `InputArea` | `Height`, `BackColor` | Input container at bottom |
| `SendButton` | `Text`, `BackColor`, `ForeColor`, `Width`, `Font` | Send button |
| `MessageArea` | `BackColor` | Scrollable messages container |
| `UserBubble` | `BackColor`, `ForeColor` | User message bubbles |
| `AssistantBubble` | `BackColor`, `ForeColor` | Assistant message bubbles |

### Run Demo

```bash
# ChatUI demo (complete window)
python -m winformpy.ui_elements.chat.chat_ui

# ChatPanel demo (panel only)
python -m winformpy.ui_elements.chat.chat_panel
```

---

## 🔌 Using External Backends

### Example: OpenAI Backend (External Implementation)

```python
from winformpy import Application
from winformpy.ui_elements.chat import ChatUI, ChatBackend, ChatManager

# External backend implementation (NOT part of WinFormPy)
class OpenAIChatBackend(ChatBackend):
    """Example backend using OpenAI API."""
    
    def __init__(self, api_key, model="gpt-4"):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def send_message(self, text, context=None):
        messages = []
        if context:
            for msg in context:
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })
        messages.append({"role": "user", "content": text})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content

# Create backend instance
backend = OpenAIChatBackend(api_key="your-api-key")

# Create manager with backend
manager = ChatManager(backend=backend)

# Use with ChatPanel
form = Form({'Text': 'AI Chat', 'Width': 600, 'Height': 700})
form.ApplyLayout()
chat = ChatPanel(form, manager=manager)

Application.Run(form)
```

### Example: WebSocket Backend (External Implementation)

```python
from winformpy.ui_elements.chat import ChatBackend
import websocket
import json

class WebSocketChatBackend(ChatBackend):
    """Example backend using WebSocket connection."""
    
    def __init__(self, url):
        self.url = url
        self.ws = None
    
    def connect(self) -> bool:
        self.ws = websocket.create_connection(self.url)
        return True
    
    def disconnect(self):
        if self.ws:
            self.ws.close()
    
    def send_message(self, text, context=None):
        self.ws.send(json.dumps({"message": text}))
        result = self.ws.recv()
        return json.loads(result).get("response")
```

### Example: Local Storage Backend

```python
from winformpy.ui_elements.chat import ChatBackend
import json
import os

class FileStorageChatBackend(ChatBackend):
    """Backend that persists chat history to file."""
    
    def __init__(self, filepath):
        self.filepath = filepath
    
    def send_message(self, text, context=None):
        # No external service, just return None
        return None
    
    def get_history(self, limit=None):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                history = json.load(f)
                return history[-limit:] if limit else history
        return []
    
    def save_history(self, messages):
        history = [
            {"role": "user" if m.is_user else "assistant", 
             "content": m.text,
             "timestamp": m.timestamp.isoformat()}
            for m in messages
        ]
        with open(self.filepath, 'w') as f:
            json.dump(history, f)
        return True
```

---

## 📊 ChatUI API

### Constructor

```python
ChatUI(
    title="WinFormPy Assistant",  # Header and window title
    width=600,                     # Window width
    height=750,                    # Window height
    user_name="You",               # Display name for user messages
    assistant_name="Assistant"     # Display name for assistant messages
)
```

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `Title` | str | Header title (get/set) |
| `UserName` | str | Name displayed for user messages |
| `AssistantName` | str | Name displayed for assistant messages |
| `chat_panel` | ChatPanel | Access to underlying chat panel |
| `on_message_sent` | callable | Callback when user sends message |
| `on_clear_chat` | callable | Callback when chat is cleared |

### Methods

| Method | Parameters | Description |
|--------|------------|-------------|
| `set_response_handler(handler)` | `handler: callable` | Set custom response function |
| `send_message(text, is_user)` | `text: str, is_user: bool` | Send message programmatically |
| `show_typing(name)` | `name: str` | Show typing indicator |
| `hide_typing()` | — | Hide typing indicator |
| `clear_chat()` | — | Clear all messages |
| `get_history()` | — | Get list of ChatMessage objects |
| `export_history()` | — | Export as formatted text |
| `set_online_status(is_online, text)` | `is_online: bool, text: str` | Update online status indicator |

### Response Handler

```python
def my_handler(user_message: str) -> str:
    """
    Custom response handler.
    
    Args:
        user_message: The message sent by the user
        
    Returns:
        The response text to display
    """
    # Example: Smart responses
    if 'hello' in user_message.lower():
        return "Hello! 👋 How can I help?"
    return f"You said: {user_message}"

chat.set_response_handler(my_handler)
```

---

## 📊 ChatPanel API

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `manager` | ChatManager | Message manager instance |

### Methods

| Method | Parameters | Description |
|--------|------------|-------------|
| `add_message_bubble(message, ...)` | See below | Add bubble with Messenger features |
| `show_typing_indicator(name)` | `name: str` | Show animated typing indicator |
| `hide_typing_indicator()` | — | Remove typing indicator |
| `after(ms, func)` | `ms: int, func: callable` | Schedule delayed execution |

### add_message_bubble() Parameters

```python
def add_message_bubble(
    message,                # ChatMessage object
    show_timestamp=True,    # Display HH:MM timestamp
    show_status=True,       # Display ✓/✓✓ read status
    show_avatar=True        # Display circular avatar
)
```

### Context Menu (Right-Click)

| Action | Description |
|--------|-------------|
| Copy | Copy message text to clipboard (uses `Clipboard.SetText()`) |
| Reply | Reply to this message (adds quote) |
| Delete | Remove message from chat |

> **Note**: The Copy action uses the WinFormPy `Clipboard` class. See the main README for more information about clipboard operations.

### Typing Indicator

```python
# Show typing indicator
chat_panel.show_typing_indicator("Assistant")

# Simulated typing delay
def after_typing():
    chat_panel.hide_typing_indicator()
    # Add response...

chat_panel.after(1500, after_typing)
```

---

## 📊 ChatManager API

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `messages` | list | List of all ChatMessage objects |
| `state` | ChatState | Current conversation state |
| `is_typing` | bool | True if user or assistant is typing |
| `unread_count` | int | Number of unread messages |
| `last_message` | ChatMessage | Most recent message |
| `message_count` | int | Total number of messages |

### Methods

| Method | Parameters | Description |
|--------|------------|-------------|
| `send_message(text)` | `text: str` | User sends a message |
| `receive_message(text)` | `text: str` | Assistant sends a message |
| `set_user_typing(is_typing)` | `is_typing: bool` | Set user typing indicator |
| `set_assistant_typing(is_typing)` | `is_typing: bool` | Set assistant typing indicator |
| `mark_all_read()` | — | Mark all messages as read |
| `clear_history()` | — | Clear all message history |
| `get_history(limit)` | `limit: int` | Get history with optional limit |

### Callbacks

| Callback | Signature | Description |
|----------|-----------|-------------|
| `on_message_received` | `(message)` | Called when message is received |
| `on_state_changed` | `(old_state, new_state)` | Called when state changes |

---

## 🔧 ChatState Enum

```python
class ChatState(Enum):
    Idle = 0            # No activity
    UserTyping = 1      # User is typing
    Sending = 2         # Message being sent
    WaitingResponse = 3 # Waiting for response
    AssistantTyping = 4 # Assistant generating response
```

---

## 💡 Examples

### Smart Bot with Features

```python
from winformpy import Application
from winformpy.ui_elements.chat import ChatUI
from datetime import datetime

chat = ChatUI(
    title="Smart Bot",
    user_name="You",
    assistant_name="SmartBot"
)

def smart_handler(msg):
    msg_lower = msg.lower()
    if 'hello' in msg_lower or 'hi' in msg_lower:
        return "Hello! 👋 How can I help?"
    elif 'time' in msg_lower:
        return f"The current time is {datetime.now().strftime('%H:%M:%S')} ⏰"
    elif 'emoji' in msg_lower:
        return "Try the emoji bar! Click 😊 🎉✨🔥"
    else:
        return f"You said: {msg}"

chat.set_response_handler(smart_handler)
chat.send_message("Welcome! Say 'hello', 'time', or 'emoji' 🤖")

Application.Run(chat)
```

### Manual Typing Indicator

```python
from winformpy.ui_elements.chat import ChatUI

chat = ChatUI(title="Manual Demo")

# Show typing manually
chat.show_typing("Bot")

# After some async operation...
def after_api_call(response):
    chat.hide_typing()
    chat.send_message(response)
```

### With State Handling

```python
from winformpy.ui_elements.chat import ChatUI, ChatState

chat = ChatUI()

def on_state_changed(old_state, new_state):
    if new_state == ChatState.AssistantTyping:
        print("Assistant is thinking...")
    elif new_state == ChatState.Idle:
        print("Ready for input")

chat.chat_panel.manager.on_state_changed = on_state_changed

Application.Run(chat)
```

### Export Conversation

```python
# After conversation
history_text = chat.export_history()
print(history_text)
# Output:
# Chat Export - 2024-01-15 10:30:45
# ==================================================
# [2024-01-15 10:30:15] You ✓✓:
#   Hello there!
#
# [2024-01-15 10:30:16] Assistant:
#   Hi! How can I help?
```

### Toggle Display Options

```python
# Customize what's shown
chat._show_avatars = False       # Hide avatars
chat._show_timestamps = True     # Show timestamps
chat._show_status = True         # Show read receipts

# Or use settings menu (⚙️ button)
```

---

## 🖼️ Visual Layout

### ChatUI Structure (Messenger-Style)

```
┌─────────────────────────────────────────────────────┐
│  Header (Blue)                     [🔍][🗑️][⚙️]   │
│  💬 Title                                          │
│     Online                                          │
├─────────────────────────────────────────────────────┤
│  Search Bar (hidden by default)                     │
│  [______________search text__________] [▲][▼] 1/5  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  (A) ┌────────────────────────────┐                 │
│      │ Assistant message          │ 10:30          │
│      └────────────────────────────┘                 │
│                                                     │
│                 ┌────────────────────────────┐ (U) │
│           10:31 │ User message               │ ✓✓  │
│                 └────────────────────────────┘      │
│                                                     │
│  (A) ●●●                                            │
│      typing...                                      │
│                                                     │
├─────────────────────────────────────────────────────┤
│  Emoji bar (hidden by default)                      │
│  [😊][👍][❤️][😂][🎉][👋][🔥][✨][💡][⭐]           │
├─────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────┬─────┐  │
│  │ Type a message...                       │ ➤   │  │
│  └─────────────────────────────────────────┴─────┘  │
├─────────────────────────────────────────────────────┤
│ [😊] Ready                    Messages: 5    10:32 │
└─────────────────────────────────────────────────────┘
```

### Message Bubble Features

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  ┌───┐  ┌─────────────────────────────────────────┐  │
│  │ A │  │ This is the assistant's message         │  │
│  │   │  │ with multiple lines of text.            │  │
│  └───┘  │                                   10:30 │  │
│  Avatar └─────────────────────────────────────────┘  │
│                                                      │
│          ┌─────────────────────────────────────┐ ┌───┐
│          │ User message here                   │ │ U │
│          │                              10:31  │ │   │
│          │                                 ✓✓  │ └───┘
│          └─────────────────────────────────────┘     │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## 📁 Module Files

| File | Description |
|------|-------------|
| `__init__.py` | Module exports |
| `chat_manager.py` | ChatManager, ChatMessage, ChatState |
| `chat_panel.py` | ChatPanel embeddable component |
| `chat_ui.py` | ChatUI complete form |

---

## 🔗 Rich Text Compatibility

The `ChatPanel` uses WinFormPy's standard controls and can be extended to support rich text formatting in messages. For applications requiring rich text in chat messages:

### Current Implementation
- Messages are displayed as plain text in chat bubbles
- The input area uses a standard `TextBox` for message composition

### Integration with RichTextBox

For rich text chat applications, consider using `RichTextBox` for the input area:

```python
from winformpy import RichTextBox, RichTextBoxFinds

# In custom ChatPanel subclass
class RichChatPanel(ChatPanel):
    def _create_input_area(self):
        # Override to use RichTextBox for input
        self.txt_input = RichTextBox(self.input_container, {
            'Dock': DockStyle.Fill
        })
```

### Related Components

| Component | Description |
|-----------|-------------|
| `RichTextBox` | Rich text editing with formatting support |
| `WordProcessorPanel` | Full word processor with toolbar |
| `ConsolePanel` | Console-style output with colored text |

> **See Also**: For rich text editing capabilities, see `RichTextBox` with its `Write()`, `WriteLine()`, and formatting methods in the main WinFormPy documentation.

---

## 🔗 Related Documentation

- [Container Best Practices](../../../guides/README_Container_Best_Practice.md)
- [Dock & Anchor Guide](../../../guides/README_Dock_Anchor.md)
