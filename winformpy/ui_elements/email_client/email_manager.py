"""
Email Manager - Business logic layer for email operations.

This module provides the business logic for email handling:
- Account management
- Message organization and threading
- Event handling and notifications
- State management

Architecture:
    EmailPrimitives (low-level ops)
        ↓ used by
    EmailManager (this module)
        ↓ used by
    EmailPanel/EmailForm (UI)
"""

from enum import Enum, auto
from typing import List, Optional, Dict, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
import threading
import queue

# Use try/except for imports to support both direct execution and package import
try:
    from .email_primitives import (
        EmailPrimitives, EmailMessage, EmailFolder, EmailAccount,
        EmailAddress, EmailAttachment, EmailFlags, EmailPriority,
        FolderType
    )
except ImportError:
    from email_primitives import (
        EmailPrimitives, EmailMessage, EmailFolder, EmailAccount,
        EmailAddress, EmailAttachment, EmailFlags, EmailPriority,
        FolderType
    )


# =============================================================================
# Enums
# =============================================================================

class EmailEventType(Enum):
    """Types of email events."""
    CONNECTED = auto()
    DISCONNECTED = auto()
    NEW_MESSAGE = auto()
    MESSAGE_DELETED = auto()
    MESSAGE_MOVED = auto()
    MESSAGE_FLAGS_CHANGED = auto()
    FOLDER_CHANGED = auto()
    SENDING_MESSAGE = auto()
    MESSAGE_SENT = auto()
    SEND_FAILED = auto()
    SYNC_STARTED = auto()
    SYNC_COMPLETED = auto()
    ERROR = auto()


class SortField(Enum):
    """Fields to sort messages by."""
    DATE = "date"
    FROM = "from"
    SUBJECT = "subject"
    SIZE = "size"
    ATTACHMENTS = "attachments"


class SortOrder(Enum):
    """Sort order."""
    ASCENDING = "asc"
    DESCENDING = "desc"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class EmailEvent:
    """Represents an email event."""
    event_type: EmailEventType
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    message: str = ""


@dataclass
class MessageThread:
    """Represents a conversation thread."""
    thread_id: str
    subject: str
    participants: List[EmailAddress]
    messages: List[EmailMessage]
    last_date: datetime
    unread_count: int = 0
    
    @property
    def message_count(self) -> int:
        return len(self.messages)
    
    @property
    def latest_message(self) -> Optional[EmailMessage]:
        return self.messages[-1] if self.messages else None


@dataclass
class EmailFilter:
    """Filter criteria for messages."""
    folder: str = None
    search_text: str = None
    from_address: str = None
    to_address: str = None
    subject: str = None
    has_attachments: bool = None
    is_unread: bool = None
    is_starred: bool = None
    date_from: datetime = None
    date_to: datetime = None
    priority: EmailPriority = None


# =============================================================================
# Email Manager
# =============================================================================

class EmailManager:
    """
    Email Manager - Business logic layer.
    
    Handles:
    - Account and connection management
    - Message caching and organization
    - Event handling and callbacks
    - Background synchronization
    - Message threading
    """
    
    def __init__(self, primitives: EmailPrimitives = None):
        """
        Initialize the email manager.
        
        Args:
            primitives: EmailPrimitives instance for low-level operations.
                       If None, a default instance will be created.
        """
        self._primitives = primitives or EmailPrimitives()
        
        # State
        self._account: Optional[EmailAccount] = None
        self._folders: List[EmailFolder] = []
        self._current_folder: str = "INBOX"
        self._messages: Dict[int, EmailMessage] = {}  # UID -> Message
        self._threads: Dict[str, MessageThread] = {}  # ThreadID -> Thread
        
        # Sorting
        self._sort_field = SortField.DATE
        self._sort_order = SortOrder.DESCENDING
        
        # Event handling
        self._event_handlers: Dict[EmailEventType, List[Callable]] = {}
        self._event_queue = queue.Queue()
        
        # Background sync
        self._sync_thread: Optional[threading.Thread] = None
        self._sync_running = False
        self._sync_interval = 60  # seconds
    
    # =========================================================================
    # Properties
    # =========================================================================
    
    @property
    def primitives(self) -> EmailPrimitives:
        """Get the primitives layer."""
        return self._primitives
    
    @primitives.setter
    def primitives(self, value: EmailPrimitives):
        """Set the primitives layer."""
        self._primitives = value
    
    @property
    def is_connected(self) -> bool:
        """Check if connected to server."""
        return self._primitives.is_connected
    
    @property
    def account(self) -> Optional[EmailAccount]:
        """Get current account."""
        return self._account
    
    @property
    def current_folder(self) -> str:
        """Get current folder path."""
        return self._current_folder
    
    @property
    def folders(self) -> List[EmailFolder]:
        """Get list of folders."""
        return self._folders
    
    @property
    def sort_field(self) -> SortField:
        """Get current sort field."""
        return self._sort_field
    
    @sort_field.setter
    def sort_field(self, value: SortField):
        """Set sort field."""
        self._sort_field = value
    
    @property
    def sort_order(self) -> SortOrder:
        """Get current sort order."""
        return self._sort_order
    
    @sort_order.setter
    def sort_order(self, value: SortOrder):
        """Set sort order."""
        self._sort_order = value
    
    # =========================================================================
    # Account Management
    # =========================================================================
    
    def configure_account(self, account: EmailAccount) -> None:
        """
        Configure the email account.
        
        Args:
            account: EmailAccount configuration
        """
        self._account = account
        self._primitives = EmailPrimitives(account)
    
    def connect(self) -> bool:
        """
        Connect to the email server.
        
        Returns:
            bool: True if connection successful
        """
        try:
            result = self._primitives.connect()
            if result:
                self._fire_event(EmailEventType.CONNECTED)
                self.refresh_folders()
            return result
        except Exception as e:
            self._fire_event(EmailEventType.ERROR, {"error": str(e)})
            return False
    
    def disconnect(self) -> None:
        """Disconnect from the email server."""
        self.stop_sync()
        self._primitives.disconnect()
        self._fire_event(EmailEventType.DISCONNECTED)
    
    # =========================================================================
    # Folder Operations
    # =========================================================================
    
    def refresh_folders(self) -> List[EmailFolder]:
        """
        Refresh the folder list from server.
        
        Returns:
            List of EmailFolder objects
        """
        self._folders = self._primitives.get_folders()
        
        # Update message counts
        for folder in self._folders:
            total, unread = self._primitives.get_message_count(folder.path)
            folder.message_count = total
            folder.unread_count = unread
        
        return self._folders
    
    def select_folder(self, folder_path: str) -> bool:
        """
        Select a folder to view.
        
        Args:
            folder_path: Path of folder to select
            
        Returns:
            bool: True if successful
        """
        self._current_folder = folder_path
        self._fire_event(EmailEventType.FOLDER_CHANGED, {"folder": folder_path})
        return True
    
    def get_folder(self, folder_path: str) -> Optional[EmailFolder]:
        """
        Get a specific folder by path.
        
        Args:
            folder_path: Folder path
            
        Returns:
            EmailFolder or None
        """
        for folder in self._folders:
            if folder.path == folder_path:
                return folder
        return None
    
    def get_inbox(self) -> Optional[EmailFolder]:
        """Get the inbox folder."""
        return self.get_folder("INBOX")
    
    def create_folder(self, name: str, parent: str = None) -> Optional[EmailFolder]:
        """
        Create a new folder.
        
        Args:
            name: Folder name
            parent: Parent folder path
            
        Returns:
            Created folder or None
        """
        folder = self._primitives.create_folder(name, parent)
        if folder:
            self._folders.append(folder)
        return folder
    
    # =========================================================================
    # Message Operations
    # =========================================================================
    
    def get_messages(self, folder: str = None, filter_: EmailFilter = None,
                     start: int = 0, limit: int = 50) -> List[EmailMessage]:
        """
        Get messages from a folder with optional filtering.
        
        Args:
            folder: Folder path (uses current folder if None)
            filter_: Optional filter criteria
            start: Starting index
            limit: Maximum messages to return
            
        Returns:
            List of EmailMessage objects
        """
        folder = folder or self._current_folder
        messages = self._primitives.get_message_list(folder, start, limit)
        
        # Cache messages
        for msg in messages:
            self._messages[msg.uid] = msg
        
        # Apply filter if provided
        if filter_:
            messages = self._apply_filter(messages, filter_)
        
        # Sort messages
        messages = self._sort_messages(messages)
        
        return messages
    
    def get_message(self, uid: int, folder: str = None) -> Optional[EmailMessage]:
        """
        Get a specific message with full content.
        
        Args:
            uid: Message UID
            folder: Folder path
            
        Returns:
            EmailMessage or None
        """
        folder = folder or self._current_folder
        
        # Check cache first
        if uid in self._messages:
            cached = self._messages[uid]
            if cached.body_text or cached.body_html:
                return cached
        
        # Fetch from server
        message = self._primitives.get_message(uid, folder)
        if message:
            self._messages[uid] = message
        return message
    
    def mark_as_read(self, uid: int, folder: str = None) -> bool:
        """Mark a message as read."""
        folder = folder or self._current_folder
        result = self._primitives.mark_as_read(uid, folder)
        if result and uid in self._messages:
            self._messages[uid].flags |= EmailFlags.SEEN
            self._fire_event(EmailEventType.MESSAGE_FLAGS_CHANGED, {"uid": uid})
        return result
    
    def mark_as_unread(self, uid: int, folder: str = None) -> bool:
        """Mark a message as unread."""
        folder = folder or self._current_folder
        result = self._primitives.mark_as_unread(uid, folder)
        if result and uid in self._messages:
            self._messages[uid].flags &= ~EmailFlags.SEEN
            self._fire_event(EmailEventType.MESSAGE_FLAGS_CHANGED, {"uid": uid})
        return result
    
    def toggle_star(self, uid: int, folder: str = None) -> bool:
        """Toggle the starred status of a message."""
        folder = folder or self._current_folder
        result = self._primitives.toggle_star(uid, folder)
        if result and uid in self._messages:
            msg = self._messages[uid]
            if EmailFlags.FLAGGED in msg.flags:
                msg.flags &= ~EmailFlags.FLAGGED
            else:
                msg.flags |= EmailFlags.FLAGGED
            self._fire_event(EmailEventType.MESSAGE_FLAGS_CHANGED, {"uid": uid})
        return result
    
    def delete_message(self, uid: int, folder: str = None, 
                       permanent: bool = False) -> bool:
        """
        Delete a message.
        
        Args:
            uid: Message UID
            folder: Folder path
            permanent: If True, permanently delete
            
        Returns:
            bool: True if successful
        """
        folder = folder or self._current_folder
        result = self._primitives.delete_message(uid, folder, permanent)
        if result:
            if uid in self._messages:
                del self._messages[uid]
            self._fire_event(EmailEventType.MESSAGE_DELETED, {"uid": uid})
        return result
    
    def move_message(self, uid: int, to_folder: str, 
                     from_folder: str = None) -> bool:
        """
        Move a message to another folder.
        
        Args:
            uid: Message UID
            to_folder: Destination folder
            from_folder: Source folder (uses current if None)
            
        Returns:
            bool: True if successful
        """
        from_folder = from_folder or self._current_folder
        result = self._primitives.move_message(uid, from_folder, to_folder)
        if result:
            if uid in self._messages:
                self._messages[uid].folder = to_folder
            self._fire_event(EmailEventType.MESSAGE_MOVED, {
                "uid": uid, 
                "from": from_folder, 
                "to": to_folder
            })
        return result
    
    def move_to_trash(self, uid: int, folder: str = None) -> bool:
        """Move a message to trash."""
        return self.move_message(uid, "Trash", folder)
    
    def move_to_archive(self, uid: int, folder: str = None) -> bool:
        """Move a message to archive."""
        return self.move_message(uid, "Archive", folder)
    
    # =========================================================================
    # Compose and Send
    # =========================================================================
    
    def create_message(self, to: List[str] = None, subject: str = "",
                       body: str = "") -> EmailMessage:
        """
        Create a new message.
        
        Args:
            to: List of recipient addresses
            subject: Message subject
            body: Message body
            
        Returns:
            New EmailMessage
        """
        msg = EmailMessage()
        msg.subject = subject
        msg.body_text = body
        msg.to_addresses = [EmailAddress.parse(addr) for addr in (to or [])]
        
        if self._account:
            msg.from_address = EmailAddress(
                self._account.email,
                self._account.display_name
            )
        
        return msg
    
    def create_reply(self, original: EmailMessage, 
                     reply_all: bool = False) -> EmailMessage:
        """
        Create a reply to a message.
        
        Args:
            original: Message to reply to
            reply_all: If True, reply to all recipients
            
        Returns:
            New EmailMessage configured as reply
        """
        msg = EmailMessage()
        
        # Set recipients
        reply_to = original.reply_to or original.from_address
        msg.to_addresses = [reply_to] if reply_to else []
        
        if reply_all:
            # Add other recipients
            for addr in original.to_addresses:
                if self._account and addr.address != self._account.email:
                    if addr not in msg.to_addresses:
                        msg.to_addresses.append(addr)
            msg.cc_addresses = list(original.cc_addresses)
        
        # Set subject
        if not original.subject.lower().startswith("re:"):
            msg.subject = f"Re: {original.subject}"
        else:
            msg.subject = original.subject
        
        # Set threading headers
        msg.in_reply_to = original.message_id
        msg.references = original.references + [original.message_id]
        
        # Set from
        if self._account:
            msg.from_address = EmailAddress(
                self._account.email,
                self._account.display_name
            )
        
        return msg
    
    def create_forward(self, original: EmailMessage) -> EmailMessage:
        """
        Create a forward of a message.
        
        Args:
            original: Message to forward
            
        Returns:
            New EmailMessage configured as forward
        """
        msg = EmailMessage()
        
        # Set subject
        if not original.subject.lower().startswith("fwd:"):
            msg.subject = f"Fwd: {original.subject}"
        else:
            msg.subject = original.subject
        
        # Build forward body
        header = f"\n\n---------- Forwarded message ----------\n"
        header += f"From: {original.from_address}\n"
        header += f"Date: {original.date_formatted}\n"
        header += f"Subject: {original.subject}\n"
        if original.to_addresses:
            header += f"To: {', '.join(str(a) for a in original.to_addresses)}\n"
        header += "\n"
        
        msg.body_text = header + original.body_text
        if original.body_html:
            msg.body_html = header.replace("\n", "<br>") + original.body_html
        
        # Copy attachments
        msg.attachments = list(original.attachments)
        
        # Set from
        if self._account:
            msg.from_address = EmailAddress(
                self._account.email,
                self._account.display_name
            )
        
        return msg
    
    def send_message(self, message: EmailMessage) -> bool:
        """
        Send an email message.
        
        Args:
            message: Message to send
            
        Returns:
            bool: True if sent successfully
        """
        self._fire_event(EmailEventType.SENDING_MESSAGE, {"message": message})
        
        try:
            result = self._primitives.send_message(message)
            if result:
                self._fire_event(EmailEventType.MESSAGE_SENT, {"message": message})
            else:
                self._fire_event(EmailEventType.SEND_FAILED, {"message": message})
            return result
        except Exception as e:
            self._fire_event(EmailEventType.SEND_FAILED, {
                "message": message,
                "error": str(e)
            })
            return False
    
    def save_draft(self, message: EmailMessage) -> int:
        """
        Save a message as draft.
        
        Args:
            message: Message to save
            
        Returns:
            int: UID of saved draft, or 0 on failure
        """
        return self._primitives.save_draft(message)
    
    # =========================================================================
    # Threading
    # =========================================================================
    
    def get_threads(self, folder: str = None) -> List[MessageThread]:
        """
        Get messages grouped by conversation thread.
        
        Args:
            folder: Folder path
            
        Returns:
            List of MessageThread objects
        """
        folder = folder or self._current_folder
        messages = self.get_messages(folder, limit=200)
        
        # Group by thread
        threads: Dict[str, List[EmailMessage]] = {}
        
        for msg in messages:
            # Use subject for basic threading
            thread_key = msg.thread_id or self._get_thread_key(msg.subject)
            
            if thread_key not in threads:
                threads[thread_key] = []
            threads[thread_key].append(msg)
        
        # Convert to MessageThread objects
        result = []
        for thread_id, msgs in threads.items():
            msgs.sort(key=lambda m: m.date or datetime.min)
            
            # Get all unique participants
            participants = set()
            for m in msgs:
                if m.from_address:
                    participants.add(m.from_address)
            
            thread = MessageThread(
                thread_id=thread_id,
                subject=msgs[0].subject,
                participants=list(participants),
                messages=msgs,
                last_date=msgs[-1].date or datetime.now(),
                unread_count=sum(1 for m in msgs if not m.is_read)
            )
            result.append(thread)
        
        # Sort by last date
        result.sort(key=lambda t: t.last_date, reverse=True)
        return result
    
    def _get_thread_key(self, subject: str) -> str:
        """Get a normalized thread key from subject."""
        # Remove Re:, Fwd:, etc.
        subject = subject.lower()
        for prefix in ["re:", "fwd:", "fw:", "re :", "fwd :"]:
            while subject.startswith(prefix):
                subject = subject[len(prefix):].strip()
        return subject
    
    # =========================================================================
    # Search
    # =========================================================================
    
    def search(self, query: str, folder: str = None) -> List[EmailMessage]:
        """
        Search for messages.
        
        Args:
            query: Search query
            folder: Folder to search (searches all if None)
            
        Returns:
            List of matching messages
        """
        # Build search criteria
        criteria = {"body": query}  # Simple text search
        
        folder = folder or self._current_folder
        uids = self._primitives.search_messages(criteria, folder)
        
        # Fetch messages
        messages = []
        for uid in uids:
            msg = self.get_message(uid, folder)
            if msg:
                messages.append(msg)
        
        return messages
    
    # =========================================================================
    # Background Sync
    # =========================================================================
    
    def start_sync(self, interval: int = 60) -> None:
        """
        Start background synchronization.
        
        Args:
            interval: Sync interval in seconds
        """
        if self._sync_running:
            return
        
        self._sync_interval = interval
        self._sync_running = True
        self._sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
        self._sync_thread.start()
    
    def stop_sync(self) -> None:
        """Stop background synchronization."""
        self._sync_running = False
        if self._sync_thread:
            self._sync_thread = None
    
    def sync_now(self) -> None:
        """Perform immediate synchronization."""
        self._fire_event(EmailEventType.SYNC_STARTED)
        
        try:
            self.refresh_folders()
            # Refresh current folder messages
            self.get_messages(self._current_folder, limit=50)
            
            self._fire_event(EmailEventType.SYNC_COMPLETED)
        except Exception as e:
            self._fire_event(EmailEventType.ERROR, {"error": str(e)})
    
    def _sync_loop(self) -> None:
        """Background sync loop."""
        import time
        
        while self._sync_running:
            try:
                # Use IDLE if available, otherwise poll
                new_uids = self._primitives.idle(timeout=self._sync_interval)
                
                for uid in new_uids:
                    msg = self.get_message(uid)
                    if msg:
                        self._fire_event(EmailEventType.NEW_MESSAGE, {"message": msg})
            except Exception:
                # Connection might be lost, try to reconnect
                time.sleep(self._sync_interval)
    
    # =========================================================================
    # Event Handling
    # =========================================================================
    
    def on_event(self, event_type: EmailEventType, 
                 handler: Callable[[EmailEvent], None]) -> None:
        """
        Register an event handler.
        
        Args:
            event_type: Type of event to handle
            handler: Callback function
        """
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        self._event_handlers[event_type].append(handler)
    
    def off_event(self, event_type: EmailEventType,
                  handler: Callable[[EmailEvent], None]) -> None:
        """
        Remove an event handler.
        
        Args:
            event_type: Type of event
            handler: Callback to remove
        """
        if event_type in self._event_handlers:
            if handler in self._event_handlers[event_type]:
                self._event_handlers[event_type].remove(handler)
    
    def _fire_event(self, event_type: EmailEventType, 
                    data: Dict[str, Any] = None) -> None:
        """Fire an event to all registered handlers."""
        event = EmailEvent(event_type, data or {})
        
        if event_type in self._event_handlers:
            for handler in self._event_handlers[event_type]:
                try:
                    handler(event)
                except Exception:
                    pass  # Don't let handler errors break the flow
    
    # =========================================================================
    # Helper Methods
    # =========================================================================
    
    def _apply_filter(self, messages: List[EmailMessage], 
                      filter_: EmailFilter) -> List[EmailMessage]:
        """Apply filter to message list."""
        result = messages
        
        if filter_.search_text:
            text = filter_.search_text.lower()
            result = [m for m in result if 
                     text in m.subject.lower() or 
                     text in m.body_text.lower() or
                     text in str(m.from_address).lower()]
        
        if filter_.is_unread is not None:
            result = [m for m in result if m.is_read != filter_.is_unread]
        
        if filter_.is_starred is not None:
            result = [m for m in result if m.is_starred == filter_.is_starred]
        
        if filter_.has_attachments is not None:
            result = [m for m in result if 
                     m.has_attachments == filter_.has_attachments]
        
        if filter_.date_from:
            result = [m for m in result if 
                     m.date and m.date >= filter_.date_from]
        
        if filter_.date_to:
            result = [m for m in result if 
                     m.date and m.date <= filter_.date_to]
        
        return result
    
    def _sort_messages(self, messages: List[EmailMessage]) -> List[EmailMessage]:
        """Sort messages according to current sort settings."""
        reverse = self._sort_order == SortOrder.DESCENDING
        
        if self._sort_field == SortField.DATE:
            key = lambda m: m.date or datetime.min
        elif self._sort_field == SortField.FROM:
            key = lambda m: str(m.from_address).lower()
        elif self._sort_field == SortField.SUBJECT:
            key = lambda m: m.subject.lower()
        elif self._sort_field == SortField.ATTACHMENTS:
            key = lambda m: len(m.attachments)
        else:
            key = lambda m: m.date or datetime.min
        
        return sorted(messages, key=key, reverse=reverse)
