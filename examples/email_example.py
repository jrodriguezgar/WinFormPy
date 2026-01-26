"""
Email Client Demo - Complete email interface

This example demonstrates:
- Email folder navigation
- Message list display
- Email composition
- Read/Unread management
- Search functionality
"""

import sys
import os

# Add project root to path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy.winformpy import Application
from winformpy.ui_elements.email_client.email_ui import EmailForm
from winformpy.ui_elements.email_client.email_manager import EmailManager


def main():
    """Run email client demo."""
    print("=" * 60)
    print("  EMAIL CLIENT DEMO")
    print("=" * 60)
    print("\nFeatures:")
    print("  • Three-panel layout (Folders, Messages, Content)")
    print("  • Email composition window")
    print("  • Read/Unread status management")
    print("  • Folder navigation (Inbox, Sent, Drafts, Trash)")
    print("  • Search functionality")
    print("  • Message preview and full view")
    print()
    print("Starting email client...")
    
    # Create manager and form
    manager = EmailManager()
    form = EmailForm(manager, {'Text': 'WinFormPy Email Client - Demo'})
    
    Application.Run(form)


if __name__ == "__main__":
    main()
