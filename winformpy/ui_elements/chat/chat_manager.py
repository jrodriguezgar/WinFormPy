"""
Module: chat_manager.py
Description: Service layer for chat message management.
Manages message history and state, with optional delegation to external backend.
The backend can implement send/receive operations for external chat services.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Optional, Callable, Any, Dict


class ChatState(Enum):
    """Represents the current state of the chat."""
    Idle = 0          # No activity
    UserTyping = 1    # User is typing
    Sending = 2       # Message being sent
    WaitingResponse = 3  # Waiting for assistant response
    AssistantTyping = 4  # Assistant is generating response


class ChatMessage:
    """Represents a single chat message."""
    
    def __init__(self, text, is_user, timestamp=None):
        self.text = text
        self.is_user = is_user
        self.timestamp = timestamp or datetime.now()
        self.is_read = False
        self.id = id(self)


# =============================================================================
# Chat Backend Contract (External)
# =============================================================================

class ChatBackend(ABC):
    """
    Abstract base class for chat backend implementations.
    
    Subclass this to create backends that connect to external chat services
    (APIs, WebSockets, AI services, etc.)
    
    ⚠️ IMPORTANT: The concrete implementation is NOT part of this project.
    It must be provided externally by the application.
    
    Example:
        class OpenAIChatBackend(ChatBackend):
            def __init__(self, api_key):
                self.client = OpenAI(api_key=api_key)
            
            def send_message(self, text, context=None):
                response = self.client.chat.completions.create(...)
                return response.choices[0].message.content
    """
    
    @abstractmethod
    def send_message(self, text: str, context: Optional[List[Dict[str, Any]]] = None) -> Optional[str]:
        """
        Send a message and optionally receive a response.
        
        Args:
            text: The message text to send
            context: Optional conversation context (list of previous messages)
            
        Returns:
            str: Response text from the backend, or None if async
            
        Raises:
            Exception: If sending fails
        """
        pass
    
    def connect(self) -> bool:
        """
        Connect to the chat service (optional).
        
        Returns:
            bool: True if connection successful
        """
        return True
    
    def disconnect(self) -> None:
        """Disconnect from the chat service (optional)."""
        pass
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve message history from backend (optional).
        
        Args:
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of message dictionaries
        """
        return []
    
    def save_history(self, messages: List['ChatMessage']) -> bool:
        """
        Save message history to backend (optional).
        
        Args:
            messages: List of ChatMessage objects to save
            
        Returns:
            bool: True if save successful
        """
        return True


class ChatManager:
    """
    Manages message history and conversation state.
    
    Optionally delegates send operations to an external backend.
    If no backend is provided, messages are stored locally only.
    
    Architecture:
        ┌─────────────────────────────────────────────────────┐
        │  ChatUI / ChatPanel (Visual Layer)                  │
        └─────────────────────┬───────────────────────────────┘
                              │ uses
        ┌─────────────────────▼───────────────────────────────┐
        │  ChatManager (Service Layer)                        │
        │    → Manages state and local history                │
        │    → Optionally delegates to backend                │
        └─────────────────────┬───────────────────────────────┘
                              │ delegates (optional)
        ┌─────────────────────▼───────────────────────────────┐
        │  ⚠️ EXTERNAL (not part of this project)             │
        │  ChatBackend (ChatBackend implementation)       │
        │    → Connects to external chat service              │
        │    → API, WebSocket, AI service, etc.               │
        └─────────────────────────────────────────────────────┘
    
    Properties:
        messages (list): List of ChatMessage objects (history)
        state (ChatState): Current state of the conversation
        is_typing (bool): Whether someone is currently typing
        unread_count (int): Number of unread messages
        backend: Optional external chat backend
    
    Events/Callbacks:
        on_message_received: Called when a new message is received
        on_state_changed: Called when the chat state changes
        on_error: Called when an error occurs
    """
    
    def __init__(self, backend: Optional[ChatBackend] = None):
        """
        Initialize the chat manager.
        
        Args:
            backend: Optional backend implementing ChatBackend.
                    If None, messages are stored locally only without
                    external service integration.
        """
        # Backend for external operations
        self._backend = backend
        
        # Message history
        self.messages = []
        
        # State management
        self._state = ChatState.Idle
        self._is_user_typing = False
        self._is_assistant_typing = False
        
        # Callbacks
        self.on_message_received = None  # Callback function(message)
        self.on_state_changed = None     # Callback function(old_state, new_state)
        self.on_error = None             # Callback function(error_message)
    
    @property
    def state(self):
        """Gets the current chat state."""
        return self._state
    
    @state.setter
    def state(self, value):
        """Sets the chat state and triggers callback."""
        if self._state != value:
            old_state = self._state
            self._state = value
            if self.on_state_changed:
                self.on_state_changed(old_state, value)
    
    @property
    def is_typing(self):
        """Returns True if user or assistant is typing."""
        return self._is_user_typing or self._is_assistant_typing
    
    @property
    def unread_count(self):
        """Gets the number of unread messages."""
        return sum(1 for msg in self.messages if not msg.is_read and not msg.is_user)
    
    @property
    def last_message(self):
        """Gets the most recent message, or None if no messages."""
        return self.messages[-1] if self.messages else None
    
    @property
    def message_count(self):
        """Gets the total number of messages."""
        return len(self.messages)
    
    @property
    def backend(self) -> Optional[ChatBackend]:
        """Gets the current backend."""
        return self._backend
    
    @backend.setter
    def backend(self, value: Optional[ChatBackend]):
        """Sets the backend for external chat operations."""
        self._backend = value
    
    @property
    def has_backend(self) -> bool:
        """Returns True if an external backend is configured."""
        return self._backend is not None

    def send_message(self, text, delegate_to_backend=True):
        """
        User sends a message.
        
        If a backend is configured and delegate_to_backend is True,
        the message will be sent to the external service.
        
        Args:
            text: The message text
            delegate_to_backend: Whether to send via backend (default True)
            
        Returns:
            ChatMessage: The created message
        """
        self.state = ChatState.Sending
        msg = ChatMessage(text, is_user=True)
        msg.is_read = True  # User's own messages are always read
        self.messages.append(msg)
        
        # Delegate to backend if configured
        if delegate_to_backend and self._backend:
            try:
                self.state = ChatState.WaitingResponse
                context = self._build_context()
                response = self._backend.send_message(text, context)
                if response:
                    # Backend returned a synchronous response
                    self.receive_message(response)
            except Exception as e:
                self.state = ChatState.Idle
                if self.on_error:
                    self.on_error(str(e))
        else:
            self.state = ChatState.WaitingResponse
        
        return msg
    
    def _build_context(self) -> List[Dict[str, Any]]:
        """
        Build conversation context for backend.
        
        Returns:
            List of message dictionaries with role and content
        """
        context = []
        for msg in self.messages:
            context.append({
                'role': 'user' if msg.is_user else 'assistant',
                'content': msg.text,
                'timestamp': msg.timestamp.isoformat()
            })
        return context

    def receive_message(self, text):
        """
        System/Assistant sends a message.
        
        Args:
            text: The message text
            
        Returns:
            ChatMessage: The created message
        """
        self._is_assistant_typing = False
        msg = ChatMessage(text, is_user=False)
        self.messages.append(msg)
        self.state = ChatState.Idle
        if self.on_message_received:
            self.on_message_received(msg)
        return msg
    
    def set_user_typing(self, is_typing):
        """Sets whether the user is currently typing."""
        self._is_user_typing = is_typing
        if is_typing:
            self.state = ChatState.UserTyping
        elif self.state == ChatState.UserTyping:
            self.state = ChatState.Idle
    
    def set_assistant_typing(self, is_typing):
        """Sets whether the assistant is currently typing/generating."""
        self._is_assistant_typing = is_typing
        if is_typing:
            self.state = ChatState.AssistantTyping
        elif self.state == ChatState.AssistantTyping:
            self.state = ChatState.Idle
    
    def mark_all_read(self):
        """Marks all messages as read."""
        for msg in self.messages:
            msg.is_read = True
    
    def mark_message_read(self, message):
        """Marks a specific message as read."""
        message.is_read = True
    
    def clear_history(self):
        """Clears all message history."""
        self.messages.clear()
        self.state = ChatState.Idle
    
    def get_history(self, limit=None):
        """
        Gets message history.
        
        Args:
            limit: Maximum number of messages to return (None for all)
            
        Returns:
            list: List of ChatMessage objects
        """
        if limit is None:
            return list(self.messages)
        return list(self.messages[-limit:])
    
    # =========================================================================
    # Backend Operations
    # =========================================================================
    
    def connect(self) -> bool:
        """
        Connect to the backend service.
        
        Returns:
            bool: True if connection successful, or True if no backend
        """
        if self._backend:
            try:
                return self._backend.connect()
            except Exception as e:
                if self.on_error:
                    self.on_error(f"Connection failed: {e}")
                return False
        return True
    
    def disconnect(self) -> None:
        """Disconnect from the backend service."""
        if self._backend:
            try:
                self._backend.disconnect()
            except Exception as e:
                if self.on_error:
                    self.on_error(f"Disconnect failed: {e}")
    
    def load_history(self, limit: Optional[int] = None) -> bool:
        """
        Load message history from backend.
        
        Args:
            limit: Maximum number of messages to load
            
        Returns:
            bool: True if load successful
        """
        if not self._backend:
            return False
        
        try:
            history = self._backend.get_history(limit)
            for msg_data in history:
                msg = ChatMessage(
                    text=msg_data.get('content', ''),
                    is_user=msg_data.get('role', 'user') == 'user',
                    timestamp=datetime.fromisoformat(msg_data['timestamp']) 
                        if 'timestamp' in msg_data else None
                )
                msg.is_read = msg_data.get('is_read', True)
                self.messages.append(msg)
            return True
        except Exception as e:
            if self.on_error:
                self.on_error(f"Load history failed: {e}")
            return False
    
    def save_history(self) -> bool:
        """
        Save message history to backend.
        
        Returns:
            bool: True if save successful
        """
        if not self._backend:
            return False
        
        try:
            return self._backend.save_history(self.messages)
        except Exception as e:
            if self.on_error:
                self.on_error(f"Save history failed: {e}")
            return False
