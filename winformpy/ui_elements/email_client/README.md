# Email Client UI Element

A complete email client component for WinFormPy applications with a three-layer architecture.

> ⚠️ **Architecture-agnostic**: This component delegates email operations to an **external backend** (`EmailBackend`). You provide the IMAP/SMTP, Gmail API, or custom email service implementation.

> **📦 Component Structure**: This module provides:
> - `EmailPanel` - Embeddable panel for any Form/Panel
> - `EmailForm` - Standalone form that **uses EmailPanel internally**

## Quick Demo

Run the built-in demos to see the component in action:

```bash
# Embeddable panel demo (with mock data)
python winformpy/ui_elements/email_client/email_panel.py

# Standalone form demo
python winformpy/ui_elements/email_client/email_ui.py
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        UI Layer                                  │
│    EmailPanel (embeddable) / EmailForm (standalone)             │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────────────────┐  │
│  │ FolderTree  │  │ MessageList │  │     ReadingPane        │  │
│  │             │  │             │  │  (preview/compose)     │  │
│  └─────────────┘  └─────────────┘  └────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Manager Layer                                │
│                    EmailManager                                  │
│                                                                  │
│  • Account management          • Message threading              │
│  • Message caching             • Search and filtering           │
│  • Event handling              • Background sync                │
│  • Compose/Reply/Forward       • State management               │
└──────────────────────────┬──────────────────────────────────────┘
                           │ delegates
┌──────────────────────────▼──────────────────────────────────────┐
│                   Primitives Layer                               │
│                   EmailBackend (Base Class)                   │
│                                                                  │
│  • Abstract interface for email operations                      │
│  • Default stub implementations                                 │
│  • Override methods for actual backends                         │
└──────────────────────────┬──────────────────────────────────────┘
                           │ implemented by
┌──────────────────────────▼──────────────────────────────────────┐
│  ⚠️ EXTERNAL (not part of this project)                         │
│  Concrete Backend Implementation                                 │
│                                                                  │
│  • IMAPBackend (using imaplib/imapclient)                       │
│  • GmailAPIBackend (using Google API)                           │
│  • GraphAPIBackend (using Microsoft Graph)                      │
│  • Any custom email service implementation                      │
└─────────────────────────────────────────────────────────────────┘
```

**⚠️ IMPORTANT**: The concrete backend implementation is **NOT part of this project**. 
It must be provided externally by the application.

## 📋 EmailBackend Contract (External)

The external backend must subclass `EmailBackend` and implement the required methods:

```python
from winformpy.ui_elements.email_client import EmailBackend, EmailAccount

class MyEmailBackend(EmailBackend):
    """Required interface for the Email Backend (external)."""
    
    # === Connection Methods ===
    
    def connect(self) -> bool:
        """Connect to email server. Returns True if successful."""
        pass
    
    def disconnect(self) -> None:
        """Disconnect from email server."""
        pass
    
    # === Folder Methods ===
    
    def get_folders(self) -> list:
        """Get list of EmailFolder objects."""
        pass
    
    def get_message_count(self, folder: str) -> tuple:
        """Returns (total_count, unread_count)."""
        pass
    
    # === Message Methods ===
    
    def get_message_list(self, folder: str, start: int, limit: int) -> list:
        """Get list of EmailMessage objects (headers only)."""
        pass
    
    def get_message(self, uid: int, folder: str) -> EmailMessage | None:
        """Get full message including body and attachments."""
        pass
    
    def send_message(self, message: EmailMessage) -> bool:
        """Send an email. Returns True if successful."""
        pass
    
    # ... other methods as needed
```

## Files

| File | Description |
|------|-------------|
| `email_primitives.py` | Base class for email backends (IMAP/SMTP abstraction) |
| `email_manager.py` | Business logic, state management, events |
| `email_panel.py` | Embeddable email panel component |
| `email_ui.py` | Standalone email client form |
| `__init__.py` | Package exports |

## Quick Start

### Standalone Email Client

```python
from winformpy.ui_elements.email_client import EmailForm, EmailAccount

# Create the form
form = EmailForm()

# Configure account (optional - can also use Settings dialog)
account = EmailAccount(
    email="user@example.com",
    display_name="John Doe",
    incoming_server="imap.example.com",
    incoming_port=993,
    outgoing_server="smtp.example.com",
    outgoing_port=587,
    incoming_username="user@example.com",
    incoming_password="password"
)
form.ConfigureAccount(account)

# Connect and show
form.Connect()
form.Show()
```

### Embedded Panel

```python
from winformpy.winformpy import Form, DockStyle
from winformpy.ui_elements.email_client import EmailPanel, EmailManager

# Create form
form = Form({'Text': 'My App', 'Width': 1200, 'Height': 800})
form.ApplyLayout()

# Create manager and panel
manager = EmailManager()
email_panel = EmailPanel(form, manager, {'Dock': DockStyle.Fill})

form.Show()
```

## Components

### EmailBackend (Base Class for External Backends)

⚠️ **This is an abstraction layer.** Override methods to connect to actual email services.

```python
from winformpy.ui_elements.email_client import EmailBackend, EmailAccount

class IMAPBackend(EmailBackend):
    """
    Example IMAP backend implementation (EXTERNAL - not part of WinFormPy).
    Uses Python's imaplib for actual email operations.
    """
    
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
    
    def disconnect(self) -> None:
        if self._imap:
            self._imap.logout()
        self._connected = False
    
    def get_folders(self):
        status, folders = self._imap.list()
        # Parse and return EmailFolder objects
        ...
    
    def get_message_list(self, folder="INBOX", start=0, limit=50):
        self._imap.select(folder)
        status, data = self._imap.search(None, 'ALL')
        # Parse and return EmailMessage objects
        ...
    
    def send_message(self, message):
        import smtplib
        from email.mime.text import MIMEText
        
        smtp = smtplib.SMTP(
            self._account.outgoing_server,
            self._account.outgoing_port
        )
        smtp.starttls()
        smtp.login(
            self._account.outgoing_username,
            self._account.outgoing_password
        )
        # Send message
        smtp.send_message(msg)
        smtp.quit()
        return True

# Usage with EmailManager
account = EmailAccount(email="user@example.com", ...)
backend = IMAPBackend(account)
manager = EmailManager(primitives=backend)
```

### Gmail API Backend Example (External)

```python
from winformpy.ui_elements.email_client import EmailBackend

class GmailAPIBackend(EmailBackend):
    """
    Example Gmail API backend (EXTERNAL - not part of WinFormPy).
    Uses Google API client for Gmail operations.
    """
    
    def __init__(self, credentials_path):
        super().__init__()
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        
        creds = Credentials.from_authorized_user_file(credentials_path)
        self.service = build('gmail', 'v1', credentials=creds)
    
    def connect(self) -> bool:
        # OAuth already handled in __init__
        self._connected = True
        return True
    
    def get_message_list(self, folder="INBOX", start=0, limit=50):
        results = self.service.users().messages().list(
            userId='me', 
            labelIds=[folder],
            maxResults=limit
        ).execute()
        # Convert to EmailMessage objects
        ...
```

### EmailManager

Business logic layer with event handling.

```python
from winformpy.ui_elements.email_client import (
    EmailManager, EmailEventType, EmailFilter
)

manager = EmailManager()

# Event handling
def on_new_message(event):
    msg = event.data.get('message')
    print(f"New message from {msg.from_address}")

manager.on_event(EmailEventType.NEW_MESSAGE, on_new_message)

# Filtering
filter_ = EmailFilter(
    is_unread=True,
    has_attachments=True
)
messages = manager.get_messages(filter_=filter_)

# Compose
msg = manager.create_message(
    to=["recipient@example.com"],
    subject="Hello",
    body="This is a test email."
)
manager.send_message(msg)
```

### EmailPanel

Embeddable component with full functionality.

```python
panel = EmailPanel(form, manager)

# Events
panel.OnMessageSelected = lambda s, msg: print(f"Selected: {msg.subject}")
panel.OnCompose = lambda s, e: show_custom_compose_dialog()

# Actions
panel.SelectFolder("INBOX")
panel.ComposeNew()
panel.Reply(reply_all=True)
panel.Forward()
panel.Delete()
panel.Refresh()
```

### EmailForm

Complete standalone email client.

```python
form = EmailForm()

# Access manager
form.Manager.configure_account(account)
form.Manager.on_event(EmailEventType.ERROR, handle_error)

# Access panel
form.EmailPanel.OnCompose = custom_compose

# Control
form.Connect()
form.Disconnect()
form.Show()
```

## Data Classes

### EmailMessage

Represents an email message with all metadata.

```python
from winformpy.ui_elements.email_client import (
    EmailMessage, EmailAddress, EmailFlags, EmailPriority
)

msg = EmailMessage(
    subject="Meeting Tomorrow",
    from_address=EmailAddress("sender@example.com", "John Sender"),
    to_addresses=[EmailAddress("me@example.com")],
    body_text="Let's meet at 10am.",
    priority=EmailPriority.High,
    flags=EmailFlags.SEEN | EmailFlags.FLAGGED
)

# Properties
print(msg.is_read)         # True (SEEN flag)
print(msg.is_starred)      # True (FLAGGED)
print(msg.has_attachments) # False
print(msg.preview)         # "Let's meet at 10am."
print(msg.date_formatted)  # "Jan 15"
```

### EmailAccount

Account configuration.

```python
from winformpy.ui_elements.email_client import EmailAccount, EmailProtocol

account = EmailAccount(
    email="user@gmail.com",
    display_name="User Name",
    incoming_server="imap.gmail.com",
    incoming_port=993,
    incoming_protocol=EmailProtocol.IMAP_SSL,
    outgoing_server="smtp.gmail.com",
    outgoing_port=587,
    outgoing_protocol=EmailProtocol.SMTP_TLS,
    incoming_username="user@gmail.com",
    incoming_password="app_password"
)
```

### EmailFolder

Folder/mailbox representation.

```python
from winformpy.ui_elements.email_client import EmailFolder, FolderType

inbox = EmailFolder(
    name="Inbox",
    path="INBOX",
    folder_type=FolderType.INBOX,
    message_count=150,
    unread_count=5
)

print(inbox.display_name)  # "Inbox (5)"
```

## Event Types

| Event | Description | Data |
|-------|-------------|------|
| `CONNECTED` | Connected to server | - |
| `DISCONNECTED` | Disconnected from server | - |
| `NEW_MESSAGE` | New message received | `message`: EmailMessage |
| `MESSAGE_DELETED` | Message deleted | `uid`: int |
| `MESSAGE_MOVED` | Message moved | `uid`, `from`, `to` |
| `MESSAGE_FLAGS_CHANGED` | Flags updated | `uid`: int |
| `FOLDER_CHANGED` | Folder selected | `folder`: str |
| `SENDING_MESSAGE` | Sending started | `message`: EmailMessage |
| `MESSAGE_SENT` | Message sent | `message`: EmailMessage |
| `SEND_FAILED` | Send failed | `message`, `error` |
| `SYNC_STARTED` | Sync started | - |
| `SYNC_COMPLETED` | Sync completed | - |
| `ERROR` | Error occurred | `error`: str |

## Features

### Message Threading

```python
# Get messages grouped by conversation
threads = manager.get_threads()

for thread in threads:
    print(f"{thread.subject} ({thread.message_count} messages)")
    print(f"  Participants: {', '.join(str(p) for p in thread.participants)}")
    print(f"  Unread: {thread.unread_count}")
```

### Background Sync

```python
# Start background synchronization
manager.start_sync(interval=60)  # Check every 60 seconds

# Stop sync
manager.stop_sync()

# Manual sync
manager.sync_now()
```

### Search

```python
# Simple text search
results = manager.search("meeting tomorrow")

# Filtered search
filter_ = EmailFilter(
    search_text="project",
    is_unread=True,
    date_from=datetime(2024, 1, 1)
)
results = manager.get_messages(filter_=filter_)
```

## Keyboard Shortcuts (in EmailForm)

| Key | Action |
|-----|--------|
| Ctrl+N | New message |
| Ctrl+R | Reply |
| Ctrl+Shift+R | Reply all |
| Ctrl+F | Forward |
| Delete | Delete message |
| F5 | Refresh |

## Extending

### Using Custom Backend with EmailManager

```python
from winformpy.ui_elements.email_client import (
    EmailManager, EmailPanel, EmailBackend, EmailAccount
)
from winformpy import Form, Application, DockStyle

# Your custom backend (external implementation)
class MyIMAPBackend(EmailBackend):
    # ... implement required methods
    pass

# Create account and backend
account = EmailAccount(
    email="user@example.com",
    incoming_server="imap.example.com",
    incoming_port=993,
    incoming_username="user@example.com",
    incoming_password="password"
)

backend = MyIMAPBackend(account)

# Create manager with custom backend
manager = EmailManager(primitives=backend)

# Create UI
form = Form({'Text': 'My Email Client', 'Width': 1200, 'Height': 800})
form.ApplyLayout()

email_panel = EmailPanel(form, manager, {'Dock': DockStyle.Fill})

# Connect and run
manager.connect()
Application.Run(form)
```

### Changing Backend at Runtime

```python
# Switch to a different backend
new_backend = GmailAPIBackend(credentials_path)
manager.primitives = new_backend
manager.connect()
```

### Custom UI

```python
class MyEmailPanel(EmailPanel):
    """Custom email panel with additional features."""
    
    def _setup_ui(self):
        super()._setup_ui()
        
        # Add custom toolbar button
        self._btn_label = ToolStripButton(self._toolbar, {
            'Text': '🏷️ Label',
            'ToolTipText': 'Add label'
        })
        self._btn_label.Click = self._on_label_click
    
    def _on_label_click(self, sender, e):
        # Custom label functionality
        pass
```

## Requirements

- WinFormPy core library
- Python 3.8+

For actual email functionality (not included in base implementation):
- `imaplib` / `imapclient` for IMAP
- `smtplib` for SMTP
- `email` module for parsing (standard library)
