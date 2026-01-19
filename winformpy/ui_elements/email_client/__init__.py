"""
Email Client - WinFormPy UI Element

A complete email client component with three-layer architecture:

- **Primitives Layer** (`email_primitives.py`): Low-level email operations
  (IMAP/SMTP abstraction, email parsing)
  
- **Manager Layer** (`email_manager.py`): Business logic and state management
  (account handling, message organization, events)
  
- **UI Layer** (`email_panel.py`, `email_ui.py`): Visual components
  (embeddable panel and standalone form)

Usage:
    from winformpy.ui_elements.email_client import (
        EmailForm, EmailPanel, EmailManager, EmailAccount
    )
    
    # Standalone form
    form = EmailForm()
    form.Show()
    
    # Or embed in existing form
    manager = EmailManager()
    panel = EmailPanel(parent, manager)
    panel.Dock = DockStyle.Fill
"""

from .email_primitives import (
    EmailPrimitives,
    EmailProtocol,
    EmailPriority,
    EmailFlags,
    FolderType,
    AttachmentType,
    EmailAddress,
    EmailAttachment,
    EmailMessage,
    EmailFolder,
    EmailAccount
)

from .email_manager import (
    EmailManager,
    EmailEventType,
    EmailEvent,
    SortField,
    SortOrder,
    MessageThread,
    EmailFilter
)

from .email_panel import EmailPanel
from .email_ui import EmailForm

__all__ = [
    # Primitives
    'EmailPrimitives',
    'EmailProtocol',
    'EmailPriority',
    'EmailFlags',
    'FolderType',
    'AttachmentType',
    'EmailAddress',
    'EmailAttachment',
    'EmailMessage',
    'EmailFolder',
    'EmailAccount',
    
    # Manager
    'EmailManager',
    'EmailEventType',
    'EmailEvent',
    'SortField',
    'SortOrder',
    'MessageThread',
    'EmailFilter',
    
    # UI
    'EmailPanel',
    'EmailForm'
]
