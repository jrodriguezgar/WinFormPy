"""
Email Primitives - Low-level email operations abstraction.

This module provides the primitive operations for email handling as an
abstract interface that must be implemented by an external backend.

Architecture:
    ┌─────────────────────────────────────────────────────┐
    │  EmailPanel / EmailForm (Visual Layer)              │
    └─────────────────────┬───────────────────────────────┘
                          │ uses
    ┌─────────────────────▼───────────────────────────────┐
    │  EmailManager (Business Logic)                      │
    │    → Manages state, caching, events                 │
    │    → Delegates operations to primitives             │
    └─────────────────────┬───────────────────────────────┘
                          │ delegates
    ┌─────────────────────▼───────────────────────────────┐
    │  EmailBackend (Interface/Base Class)             │
    │    → Abstract interface for email operations        │
    │    → Provides default stub implementations          │
    └─────────────────────┬───────────────────────────────┘
                          │ implemented by
    ┌─────────────────────▼───────────────────────────────┐
    │  ⚠️ EXTERNAL (not part of this project)             │
    │  Concrete Backend Implementation                    │
    │    → IMAPBackend, GmailAPIBackend, etc.             │
    │    → Uses imaplib, imapclient, google-api, etc.     │
    └─────────────────────────────────────────────────────┘

⚠️ IMPORTANT: The concrete backend implementation is NOT part of this project.
It must be provided externally by the application.

Example backend implementation:
    class IMAPBackend(EmailBackend):
        def connect(self) -> bool:
            import imaplib
            self._imap = imaplib.IMAP4_SSL(
                self._account.incoming_server,
                self._account.incoming_port
            )
            self._imap.login(
                self._account.incoming_username,
                self._account.incoming_password
            )
            self._connected = True
            return True
        
        def get_message_list(self, folder="INBOX", start=0, limit=50):
            self._imap.select(folder)
            # ... implementation
"""

import os
import re
from datetime import datetime
from enum import Enum, Flag, auto
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass, field


# =============================================================================
# Enums
# =============================================================================

class EmailProtocol(Enum):
    """Email protocol types."""
    IMAP = "imap"
    IMAP_SSL = "imaps"
    POP3 = "pop3"
    POP3_SSL = "pop3s"
    SMTP = "smtp"
    SMTP_SSL = "smtps"
    SMTP_TLS = "smtp_tls"


class EmailPriority(Enum):
    """Email priority levels."""
    Low = 5
    Normal = 3
    High = 1


class EmailFlags(Flag):
    """Email message flags (IMAP standard)."""
    NONE = 0
    SEEN = auto()      # Read
    ANSWERED = auto()  # Replied
    FLAGGED = auto()   # Starred/Important
    DELETED = auto()   # Marked for deletion
    DRAFT = auto()     # Draft message
    RECENT = auto()    # Recently arrived


class FolderType(Enum):
    """Standard email folder types."""
    INBOX = "INBOX"
    SENT = "Sent"
    DRAFTS = "Drafts"
    TRASH = "Trash"
    SPAM = "Spam"
    ARCHIVE = "Archive"
    CUSTOM = "Custom"


class AttachmentType(Enum):
    """Attachment content types."""
    IMAGE = "image"
    DOCUMENT = "document"
    ARCHIVE = "archive"
    AUDIO = "audio"
    VIDEO = "video"
    OTHER = "other"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class EmailAddress:
    """Represents an email address with optional display name."""
    address: str
    display_name: str = ""
    
    def __str__(self):
        if self.display_name:
            return f'"{self.display_name}" <{self.address}>'
        return self.address
    
    @staticmethod
    def parse(address_string: str) -> 'EmailAddress':
        """Parse an email address string like 'Name <email@domain.com>'."""
        match = re.match(r'"?([^"<]*)"?\s*<?([^>]+)>?', address_string.strip())
        if match:
            name = match.group(1).strip()
            addr = match.group(2).strip()
            return EmailAddress(addr, name)
        return EmailAddress(address_string.strip())


@dataclass
class EmailAttachment:
    """Represents an email attachment."""
    filename: str
    content_type: str
    size: int
    data: bytes = field(default=b"", repr=False)
    content_id: str = ""  # For inline attachments
    
    @property
    def attachment_type(self) -> AttachmentType:
        """Determine the type based on content_type."""
        ct = self.content_type.lower()
        if ct.startswith("image/"):
            return AttachmentType.IMAGE
        elif ct.startswith("audio/"):
            return AttachmentType.AUDIO
        elif ct.startswith("video/"):
            return AttachmentType.VIDEO
        elif ct in ["application/zip", "application/x-rar", "application/x-7z"]:
            return AttachmentType.ARCHIVE
        elif ct in ["application/pdf", "application/msword", 
                    "application/vnd.openxmlformats-officedocument"]:
            return AttachmentType.DOCUMENT
        return AttachmentType.OTHER
    
    @property
    def size_formatted(self) -> str:
        """Return human-readable size."""
        if self.size < 1024:
            return f"{self.size} B"
        elif self.size < 1024 * 1024:
            return f"{self.size / 1024:.1f} KB"
        else:
            return f"{self.size / (1024 * 1024):.1f} MB"


@dataclass
class EmailMessage:
    """Represents an email message."""
    # Identifiers
    message_id: str = ""
    uid: int = 0
    
    # Headers
    subject: str = ""
    from_address: Optional[EmailAddress] = None
    to_addresses: List[EmailAddress] = field(default_factory=list)
    cc_addresses: List[EmailAddress] = field(default_factory=list)
    bcc_addresses: List[EmailAddress] = field(default_factory=list)
    reply_to: Optional[EmailAddress] = None
    
    # Dates
    date: Optional[datetime] = None
    received_date: Optional[datetime] = None
    
    # Content
    body_text: str = ""
    body_html: str = ""
    
    # Attachments
    attachments: List[EmailAttachment] = field(default_factory=list)
    
    # Flags and metadata
    flags: EmailFlags = EmailFlags.NONE
    priority: EmailPriority = EmailPriority.Normal
    folder: str = "INBOX"
    
    # Threading
    in_reply_to: str = ""
    references: List[str] = field(default_factory=list)
    thread_id: str = ""
    
    @property
    def is_read(self) -> bool:
        return EmailFlags.SEEN in self.flags
    
    @property
    def is_starred(self) -> bool:
        return EmailFlags.FLAGGED in self.flags
    
    @property
    def is_draft(self) -> bool:
        return EmailFlags.DRAFT in self.flags
    
    @property
    def has_attachments(self) -> bool:
        return len(self.attachments) > 0
    
    @property
    def preview(self) -> str:
        """Get a preview of the message body (first 100 chars)."""
        text = self.body_text or self.body_html
        # Remove HTML tags if present
        text = re.sub(r'<[^>]+>', '', text)
        text = ' '.join(text.split())[:100]
        return text + "..." if len(text) >= 100 else text
    
    @property
    def date_formatted(self) -> str:
        """Format date for display."""
        if not self.date:
            return ""
        now = datetime.now()
        if self.date.date() == now.date():
            return self.date.strftime("%H:%M")
        elif self.date.year == now.year:
            return self.date.strftime("%b %d")
        return self.date.strftime("%b %d, %Y")


@dataclass
class EmailFolder:
    """Represents an email folder/mailbox."""
    name: str
    path: str
    folder_type: FolderType = FolderType.CUSTOM
    message_count: int = 0
    unread_count: int = 0
    has_children: bool = False
    children: List['EmailFolder'] = field(default_factory=list)
    
    @property
    def display_name(self) -> str:
        """Get display name with unread count."""
        if self.unread_count > 0:
            return f"{self.name} ({self.unread_count})"
        return self.name


@dataclass
class EmailAccount:
    """Represents an email account configuration."""
    # Account info
    email: str
    display_name: str = ""
    
    # Incoming server (IMAP/POP3)
    incoming_server: str = ""
    incoming_port: int = 993
    incoming_protocol: EmailProtocol = EmailProtocol.IMAP_SSL
    incoming_username: str = ""
    incoming_password: str = ""
    
    # Outgoing server (SMTP)
    outgoing_server: str = ""
    outgoing_port: int = 587
    outgoing_protocol: EmailProtocol = EmailProtocol.SMTP_TLS
    outgoing_username: str = ""
    outgoing_password: str = ""
    
    # Settings
    use_same_credentials: bool = True
    check_interval_minutes: int = 5
    leave_on_server: bool = True
    
    def __post_init__(self):
        if not self.incoming_username:
            self.incoming_username = self.email
        if not self.outgoing_username and self.use_same_credentials:
            self.outgoing_username = self.incoming_username
        if not self.outgoing_password and self.use_same_credentials:
            self.outgoing_password = self.incoming_password


# =============================================================================
# Primitive Operations - Base Class for External Backend
# =============================================================================

class EmailBackend:
    """
    Base class for email operations - to be implemented by external backend.
    
    This class provides default stub implementations for all email operations.
    Subclass and override methods to connect to actual email services.
    
    ⚠️ IMPORTANT: This is an abstraction layer. The actual implementation
    that connects to IMAP/SMTP servers is NOT part of this project and must
    be provided externally.
    
    Required backend implementations:
    - IMAP backend: For reading emails (imaplib, imapclient, etc.)
    - SMTP backend: For sending emails (smtplib, etc.)
    - Or API-based: Gmail API, Microsoft Graph, etc.
    
    Example:
        class MyIMAPBackend(EmailBackend):
            def connect(self) -> bool:
                import imaplib
                self._imap = imaplib.IMAP4_SSL(...)
                self._connected = True
                return True
            
            def get_message_list(self, folder="INBOX", start=0, limit=50):
                # Actual IMAP implementation
                pass
        
        # Usage
        backend = MyIMAPBackend(account)
        manager = EmailManager(primitives=backend)
    """
    
    def __init__(self, account: EmailAccount = None):
        """
        Initialize with optional account configuration.
        
        Args:
            account: EmailAccount configuration. Required for most operations.
        """
        self._account = account
        self._connected = False
        self._imap_connection = None
        self._smtp_connection = None
    
    @property
    def is_connected(self) -> bool:
        """Check if connected to server."""
        return self._connected
    
    # =========================================================================
    # Connection Methods
    # =========================================================================
    
    def connect(self) -> bool:
        """
        Connect to the email server.
        
        Returns:
            bool: True if connection successful
            
        Raises:
            ConnectionError: If connection fails
        """
        if not self._account:
            raise ValueError("No account configured")
        
        # Placeholder - actual implementation would use imaplib/smtplib
        self._connected = True
        return True
    
    def disconnect(self) -> None:
        """Disconnect from the email server."""
        self._connected = False
        self._imap_connection = None
        self._smtp_connection = None
    
    def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticate with the server.
        
        Args:
            username: Account username
            password: Account password
            
        Returns:
            bool: True if authentication successful
        """
        # Placeholder
        return True
    
    # =========================================================================
    # Folder Operations
    # =========================================================================
    
    def get_folders(self) -> List[EmailFolder]:
        """
        Get list of all folders.
        
        Returns:
            List of EmailFolder objects
        """
        # Return standard folders as placeholder
        return [
            EmailFolder("Inbox", "INBOX", FolderType.INBOX),
            EmailFolder("Sent", "Sent", FolderType.SENT),
            EmailFolder("Drafts", "Drafts", FolderType.DRAFTS),
            EmailFolder("Trash", "Trash", FolderType.TRASH),
            EmailFolder("Spam", "Spam", FolderType.SPAM),
        ]
    
    def create_folder(self, name: str, parent: str = None) -> EmailFolder:
        """
        Create a new folder.
        
        Args:
            name: Folder name
            parent: Parent folder path (optional)
            
        Returns:
            Created EmailFolder
        """
        path = f"{parent}/{name}" if parent else name
        return EmailFolder(name, path, FolderType.CUSTOM)
    
    def delete_folder(self, folder_path: str) -> bool:
        """
        Delete a folder.
        
        Args:
            folder_path: Path of folder to delete
            
        Returns:
            bool: True if successful
        """
        return True
    
    def rename_folder(self, old_path: str, new_name: str) -> bool:
        """
        Rename a folder.
        
        Args:
            old_path: Current folder path
            new_name: New folder name
            
        Returns:
            bool: True if successful
        """
        return True
    
    # =========================================================================
    # Message Retrieval
    # =========================================================================
    
    def get_message_count(self, folder: str = "INBOX") -> Tuple[int, int]:
        """
        Get message count for a folder.
        
        Args:
            folder: Folder path
            
        Returns:
            Tuple of (total_count, unread_count)
        """
        return (0, 0)
    
    def get_message_list(self, folder: str = "INBOX", 
                         start: int = 0, limit: int = 50) -> List[EmailMessage]:
        """
        Get list of messages (headers only).
        
        Args:
            folder: Folder path
            start: Starting index
            limit: Maximum messages to return
            
        Returns:
            List of EmailMessage with headers only
        """
        return []
    
    def get_message(self, uid: int, folder: str = "INBOX") -> Optional[EmailMessage]:
        """
        Get full message including body and attachments.
        
        Args:
            uid: Message UID
            folder: Folder path
            
        Returns:
            EmailMessage or None if not found
        """
        return None
    
    def search_messages(self, criteria: Dict[str, Any], 
                       folder: str = "INBOX") -> List[int]:
        """
        Search for messages matching criteria.
        
        Args:
            criteria: Search criteria dict:
                - subject: Subject contains
                - from: From address contains
                - to: To address contains
                - body: Body contains
                - since: Date since
                - before: Date before
                - flagged: Is starred
                - unseen: Is unread
            folder: Folder to search
            
        Returns:
            List of matching message UIDs
        """
        return []
    
    # =========================================================================
    # Message Operations
    # =========================================================================
    
    def move_message(self, uid: int, from_folder: str, to_folder: str) -> bool:
        """
        Move a message to another folder.
        
        Args:
            uid: Message UID
            from_folder: Source folder
            to_folder: Destination folder
            
        Returns:
            bool: True if successful
        """
        return True
    
    def copy_message(self, uid: int, from_folder: str, to_folder: str) -> bool:
        """
        Copy a message to another folder.
        
        Args:
            uid: Message UID
            from_folder: Source folder
            to_folder: Destination folder
            
        Returns:
            bool: True if successful
        """
        return True
    
    def delete_message(self, uid: int, folder: str = "INBOX", 
                       permanent: bool = False) -> bool:
        """
        Delete a message.
        
        Args:
            uid: Message UID
            folder: Folder containing message
            permanent: If True, permanently delete. If False, move to Trash.
            
        Returns:
            bool: True if successful
        """
        return True
    
    def set_flags(self, uid: int, flags: EmailFlags, folder: str = "INBOX") -> bool:
        """
        Set message flags.
        
        Args:
            uid: Message UID
            flags: Flags to set
            folder: Folder containing message
            
        Returns:
            bool: True if successful
        """
        return True
    
    def remove_flags(self, uid: int, flags: EmailFlags, folder: str = "INBOX") -> bool:
        """
        Remove message flags.
        
        Args:
            uid: Message UID
            flags: Flags to remove
            folder: Folder containing message
            
        Returns:
            bool: True if successful
        """
        return True
    
    def mark_as_read(self, uid: int, folder: str = "INBOX") -> bool:
        """Mark a message as read."""
        return self.set_flags(uid, EmailFlags.SEEN, folder)
    
    def mark_as_unread(self, uid: int, folder: str = "INBOX") -> bool:
        """Mark a message as unread."""
        return self.remove_flags(uid, EmailFlags.SEEN, folder)
    
    def toggle_star(self, uid: int, folder: str = "INBOX") -> bool:
        """Toggle the starred/flagged status of a message."""
        return True
    
    # =========================================================================
    # Sending Messages
    # =========================================================================
    
    def send_message(self, message: EmailMessage) -> bool:
        """
        Send an email message.
        
        Args:
            message: EmailMessage to send
            
        Returns:
            bool: True if sent successfully
        """
        if not message.from_address:
            if self._account:
                message.from_address = EmailAddress(
                    self._account.email, 
                    self._account.display_name
                )
        return True
    
    def save_draft(self, message: EmailMessage) -> int:
        """
        Save a message as draft.
        
        Args:
            message: EmailMessage to save
            
        Returns:
            int: UID of saved draft
        """
        message.flags = EmailFlags.DRAFT
        return 0
    
    # =========================================================================
    # Attachment Operations
    # =========================================================================
    
    def get_attachment(self, message_uid: int, attachment_index: int,
                       folder: str = "INBOX") -> Optional[EmailAttachment]:
        """
        Download a specific attachment.
        
        Args:
            message_uid: Message UID
            attachment_index: Index of attachment
            folder: Folder containing message
            
        Returns:
            EmailAttachment with data, or None
        """
        return None
    
    def save_attachment(self, attachment: EmailAttachment, 
                        filepath: str) -> bool:
        """
        Save an attachment to disk.
        
        Args:
            attachment: Attachment to save
            filepath: Path to save to
            
        Returns:
            bool: True if saved successfully
        """
        try:
            with open(filepath, 'wb') as f:
                f.write(attachment.data)
            return True
        except Exception:
            return False
    
    # =========================================================================
    # Utility Methods
    # =========================================================================
    
    def idle(self, timeout: int = 30) -> List[int]:
        """
        Wait for new messages using IMAP IDLE.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            List of new message UIDs
        """
        return []
    
    def noop(self) -> bool:
        """
        Send NOOP to keep connection alive.
        
        Returns:
            bool: True if connection is still alive
        """
        return self._connected
