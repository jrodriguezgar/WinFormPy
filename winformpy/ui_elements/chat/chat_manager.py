from datetime import datetime
from enum import Enum


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


class ChatManager:
    """
    Manages message history and conversation state.
    
    Properties:
        messages (list): List of ChatMessage objects (history)
        state (ChatState): Current state of the conversation
        is_typing (bool): Whether someone is currently typing
        unread_count (int): Number of unread messages
    
    Events/Callbacks:
        on_message_received: Called when a new message is received
        on_state_changed: Called when the chat state changes
    """
    
    def __init__(self):
        # Message history
        self.messages = []
        
        # State management
        self._state = ChatState.Idle
        self._is_user_typing = False
        self._is_assistant_typing = False
        
        # Callbacks
        self.on_message_received = None  # Callback function(message)
        self.on_state_changed = None     # Callback function(old_state, new_state)
    
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

    def send_message(self, text):
        """
        User sends a message.
        
        Args:
            text: The message text
            
        Returns:
            ChatMessage: The created message
        """
        self.state = ChatState.Sending
        msg = ChatMessage(text, is_user=True)
        msg.is_read = True  # User's own messages are always read
        self.messages.append(msg)
        self.state = ChatState.WaitingResponse
        return msg

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
