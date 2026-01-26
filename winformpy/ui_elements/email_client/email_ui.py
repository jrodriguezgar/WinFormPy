"""
Email UI - Complete email client form.

This module provides a standalone email client form that uses
EmailPanel for the main interface.

Architecture:
    EmailBackend (low-level ops)
        ↓ used by
    EmailManager (business logic)
        ↓ used by
    EmailPanel (embeddable) / EmailForm (this module)
"""

import sys
import os

# Add parent path for imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..', '..', '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy.winformpy import (
    Form, Panel, Label, Button, TextBox, MenuStrip, ToolStripMenuItem,
    StatusStrip, ToolStripStatusLabel, DockStyle, FormBorderStyle, Font, FontStyle,
    MessageBox
)

# Use try/except for imports to support both direct execution and package import
try:
    from .email_manager import EmailManager, EmailEventType
    from .email_panel import EmailPanel
    from .email_backend import EmailAccount, EmailMessage
except ImportError:
    from email_manager import EmailManager, EmailEventType
    from email_panel import EmailPanel
    from email_backend import EmailAccount, EmailMessage


class EmailForm(Form):
    """
    Complete email client form.
    
    Provides a full-featured email application with:
    - Menu bar with File, Edit, View, Message, Tools, Help menus
    - Email panel with folders, message list, and reading pane
    - Status bar with connection status and message count
    
    Usage:
        manager = EmailManager()
        manager.configure_account(account)
        
        form = EmailForm(manager)
        form.Show()
    """
    
    def __init__(self, manager: EmailManager = None, props: dict = None):
        """
        Initialize the email form.
        
        Args:
            manager: EmailManager instance. If None, creates a new one.
            props: Additional form properties
        """
        defaults = {
            'Text': 'Email Client',
            'Width': 1200,
            'Height': 800
        }
        if props:
            defaults.update(props)
        
        super().__init__(defaults)
        
        self._manager = manager or EmailManager()
        
        self.ApplyLayout()
        
        self._setup_menu()
        self._setup_ui()
        self._setup_statusbar()
        self._setup_events()
    
    # =========================================================================
    # Properties
    # =========================================================================
    
    @property
    def Manager(self) -> EmailManager:
        """Get the email manager."""
        return self._manager
    
    @property
    def EmailPanel(self) -> EmailPanel:
        """Get the email panel."""
        return self._email_panel
    
    # =========================================================================
    # UI Setup
    # =========================================================================
    
    def _setup_menu(self):
        """Set up the menu bar."""
        self._menu = MenuStrip(self, {
            'Dock': DockStyle.Top
        })
        
        # File menu
        file_menu = ToolStripMenuItem(self._menu, {'Text': 'File'})
        
        new_msg = ToolStripMenuItem(file_menu, {'Text': 'New Message'})
        new_msg.Click = lambda s, e: self._email_panel.ComposeNew()
        
        ToolStripMenuItem(file_menu, {'Text': '-'})  # Separator
        
        check_mail = ToolStripMenuItem(file_menu, {'Text': 'Check for New Messages'})
        check_mail.Click = lambda s, e: self._manager.sync_now()
        
        ToolStripMenuItem(file_menu, {'Text': '-'})
        
        account_settings = ToolStripMenuItem(file_menu, {'Text': 'Account Settings...'})
        account_settings.Click = lambda s, e: self._show_account_settings()
        
        ToolStripMenuItem(file_menu, {'Text': '-'})
        
        exit_item = ToolStripMenuItem(file_menu, {'Text': 'Exit'})
        exit_item.Click = lambda s, e: self.Close()
        
        # Edit menu
        edit_menu = ToolStripMenuItem(self._menu, {'Text': 'Edit'})
        
        undo = ToolStripMenuItem(edit_menu, {'Text': 'Undo'})
        redo = ToolStripMenuItem(edit_menu, {'Text': 'Redo'})
        ToolStripMenuItem(edit_menu, {'Text': '-'})
        cut = ToolStripMenuItem(edit_menu, {'Text': 'Cut'})
        copy = ToolStripMenuItem(edit_menu, {'Text': 'Copy'})
        paste = ToolStripMenuItem(edit_menu, {'Text': 'Paste'})
        ToolStripMenuItem(edit_menu, {'Text': '-'})
        select_all = ToolStripMenuItem(edit_menu, {'Text': 'Select All'})
        ToolStripMenuItem(edit_menu, {'Text': '-'})
        find = ToolStripMenuItem(edit_menu, {'Text': 'Find...'})
        
        # View menu
        view_menu = ToolStripMenuItem(self._menu, {'Text': 'View'})
        
        folders = ToolStripMenuItem(view_menu, {'Text': 'Folder Pane'})
        reading = ToolStripMenuItem(view_menu, {'Text': 'Reading Pane'})
        ToolStripMenuItem(view_menu, {'Text': '-'})
        sort_by = ToolStripMenuItem(view_menu, {'Text': 'Sort By'})
        
        sort_date = ToolStripMenuItem(sort_by, {'Text': 'Date'})
        sort_from = ToolStripMenuItem(sort_by, {'Text': 'From'})
        sort_subject = ToolStripMenuItem(sort_by, {'Text': 'Subject'})
        
        ToolStripMenuItem(view_menu, {'Text': '-'})
        refresh = ToolStripMenuItem(view_menu, {'Text': 'Refresh'})
        refresh.Click = lambda s, e: self._manager.sync_now()
        
        # Message menu
        message_menu = ToolStripMenuItem(self._menu, {'Text': 'Message'})
        
        new_msg2 = ToolStripMenuItem(message_menu, {'Text': 'New Message'})
        new_msg2.Click = lambda s, e: self._email_panel.ComposeNew()
        
        ToolStripMenuItem(message_menu, {'Text': '-'})
        
        reply = ToolStripMenuItem(message_menu, {'Text': 'Reply'})
        reply.Click = lambda s, e: self._email_panel.Reply()
        
        reply_all = ToolStripMenuItem(message_menu, {'Text': 'Reply All'})
        reply_all.Click = lambda s, e: self._email_panel.Reply(reply_all=True)
        
        forward = ToolStripMenuItem(message_menu, {'Text': 'Forward'})
        forward.Click = lambda s, e: self._email_panel.Forward()
        
        ToolStripMenuItem(message_menu, {'Text': '-'})
        
        mark_read = ToolStripMenuItem(message_menu, {'Text': 'Mark as Read'})
        mark_unread = ToolStripMenuItem(message_menu, {'Text': 'Mark as Unread'})
        mark_starred = ToolStripMenuItem(message_menu, {'Text': 'Toggle Star'})
        
        ToolStripMenuItem(message_menu, {'Text': '-'})
        
        move_to = ToolStripMenuItem(message_menu, {'Text': 'Move To'})
        delete = ToolStripMenuItem(message_menu, {'Text': 'Delete'})
        delete.Click = lambda s, e: self._email_panel.Delete()
        
        # Tools menu
        tools_menu = ToolStripMenuItem(self._menu, {'Text': 'Tools'})
        
        filters = ToolStripMenuItem(tools_menu, {'Text': 'Message Filters...'})
        ToolStripMenuItem(tools_menu, {'Text': '-'})
        options = ToolStripMenuItem(tools_menu, {'Text': 'Options...'})
        
        # Help menu
        help_menu = ToolStripMenuItem(self._menu, {'Text': 'Help'})
        
        help_contents = ToolStripMenuItem(help_menu, {'Text': 'Help Contents'})
        ToolStripMenuItem(help_menu, {'Text': '-'})
        about = ToolStripMenuItem(help_menu, {'Text': 'About Email Client'})
        about.Click = lambda s, e: self._show_about()
    
    def _setup_ui(self):
        """Set up the main UI."""
        # Email panel fills the form
        self._email_panel = EmailPanel(self, self._manager, {
            'Dock': DockStyle.Fill
        })
    
    def _setup_statusbar(self):
        """Set up the status bar."""
        self._statusbar = StatusStrip(self, {
            'Dock': DockStyle.Bottom
        })
        
        self._status_label = ToolStripStatusLabel('Ready')
        self._statusbar.Items.Add(self._status_label)
        
        self._message_count_label = ToolStripStatusLabel('0 messages')
        self._statusbar.Items.Add(self._message_count_label)
    
    def _setup_events(self):
        """Set up event handlers."""
        self._manager.on_event(EmailEventType.CONNECTED, self._on_connected)
        self._manager.on_event(EmailEventType.DISCONNECTED, self._on_disconnected)
        self._manager.on_event(EmailEventType.NEW_MESSAGE, self._on_new_message)
        self._manager.on_event(EmailEventType.SYNC_STARTED, self._on_sync_started)
        self._manager.on_event(EmailEventType.SYNC_COMPLETED, self._on_sync_completed)
        self._manager.on_event(EmailEventType.ERROR, self._on_error)
    
    # =========================================================================
    # Event Handlers
    # =========================================================================
    
    def _on_connected(self, event):
        """Handle connected event."""
        self._status_label.Text = "Connected"
        self.Text = f"Email Client - {self._manager.account.email if self._manager.account else ''}"
    
    def _on_disconnected(self, event):
        """Handle disconnected event."""
        self._status_label.Text = "Disconnected"
    
    def _on_new_message(self, event):
        """Handle new message event."""
        msg = event.data.get('message')
        if msg:
            self._status_label.Text = f"New message from {msg.from_address}"
    
    def _on_sync_started(self, event):
        """Handle sync started event."""
        self._status_label.Text = "Checking for new messages..."
    
    def _on_sync_completed(self, event):
        """Handle sync completed event."""
        self._status_label.Text = "Ready"
        
        # Update message count
        inbox = self._manager.get_inbox()
        if inbox:
            self._message_count_label.Text = f"{inbox.message_count} messages ({inbox.unread_count} unread)"
    
    def _on_error(self, event):
        """Handle error event."""
        error = event.data.get('error', 'Unknown error')
        self._status_label.Text = f"Error: {error}"
    
    # =========================================================================
    # Dialogs
    # =========================================================================
    
    def _show_account_settings(self):
        """Show account settings dialog."""
        settings_form = Form({
            'Text': 'Account Settings',
            'Width': 500,
            'Height': 400,
            'FormBorderStyle': FormBorderStyle.FixedDialog
        })
        settings_form.ApplyLayout()
        
        # Email
        Label(settings_form, {
            'Text': 'Email Address:',
            'Left': 20,
            'Top': 20,
            'Width': 120
        })
        email_box = TextBox(settings_form, {
            'Left': 150,
            'Top': 20,
            'Width': 300
        })
        
        # Display Name
        Label(settings_form, {
            'Text': 'Display Name:',
            'Left': 20,
            'Top': 50,
            'Width': 120
        })
        name_box = TextBox(settings_form, {
            'Left': 150,
            'Top': 50,
            'Width': 300
        })
        
        # Incoming Server
        Label(settings_form, {
            'Text': 'Incoming Server:',
            'Left': 20,
            'Top': 100,
            'Width': 120
        })
        incoming_box = TextBox(settings_form, {
            'Left': 150,
            'Top': 100,
            'Width': 200
        })
        
        Label(settings_form, {
            'Text': 'Port:',
            'Left': 360,
            'Top': 100,
            'Width': 40
        })
        incoming_port = TextBox(settings_form, {
            'Text': '993',
            'Left': 400,
            'Top': 100,
            'Width': 50
        })
        
        # Outgoing Server
        Label(settings_form, {
            'Text': 'Outgoing Server:',
            'Left': 20,
            'Top': 130,
            'Width': 120
        })
        outgoing_box = TextBox(settings_form, {
            'Left': 150,
            'Top': 130,
            'Width': 200
        })
        
        Label(settings_form, {
            'Text': 'Port:',
            'Left': 360,
            'Top': 130,
            'Width': 40
        })
        outgoing_port = TextBox(settings_form, {
            'Text': '587',
            'Left': 400,
            'Top': 130,
            'Width': 50
        })
        
        # Username
        Label(settings_form, {
            'Text': 'Username:',
            'Left': 20,
            'Top': 180,
            'Width': 120
        })
        username_box = TextBox(settings_form, {
            'Left': 150,
            'Top': 180,
            'Width': 300
        })
        
        # Password
        Label(settings_form, {
            'Text': 'Password:',
            'Left': 20,
            'Top': 210,
            'Width': 120
        })
        password_box = TextBox(settings_form, {
            'Left': 150,
            'Top': 210,
            'Width': 300,
            'UseSystemPasswordChar': True
        })
        
        # Buttons
        def on_save(s, e):
            account = EmailAccount(
                email=email_box.Text,
                display_name=name_box.Text,
                incoming_server=incoming_box.Text,
                incoming_port=int(incoming_port.Text or 993),
                outgoing_server=outgoing_box.Text,
                outgoing_port=int(outgoing_port.Text or 587),
                incoming_username=username_box.Text,
                incoming_password=password_box.Text
            )
            self._manager.configure_account(account)
            settings_form.Close()
        
        save_btn = Button(settings_form, {
            'Text': 'Save',
            'Left': 290,
            'Top': 320,
            'Width': 80
        })
        save_btn.Click = on_save
        
        cancel_btn = Button(settings_form, {
            'Text': 'Cancel',
            'Left': 380,
            'Top': 320,
            'Width': 80
        })
        cancel_btn.Click = lambda s, e: settings_form.Close()
        
        # Load current settings if available
        if self._manager.account:
            acc = self._manager.account
            email_box.Text = acc.email
            name_box.Text = acc.display_name
            incoming_box.Text = acc.incoming_server
            incoming_port.Text = str(acc.incoming_port)
            outgoing_box.Text = acc.outgoing_server
            outgoing_port.Text = str(acc.outgoing_port)
            username_box.Text = acc.incoming_username
        
        settings_form.ShowDialog()
    
    def _show_about(self):
        """Show about dialog."""
        MessageBox.Show(
            "Email Client\n\n"
            "A simple email client built with WinFormPy.\n\n"
            "This is a demonstration of the email_client UI element\n"
            "using the primitives → manager → UI architecture.",
            "About Email Client"
        )
    
    # =========================================================================
    # Public Methods
    # =========================================================================
    
    def Connect(self) -> bool:
        """
        Connect to the email server.
        
        Returns:
            bool: True if connection successful
        """
        return self._manager.connect()
    
    def Disconnect(self):
        """Disconnect from the email server."""
        self._manager.disconnect()
    
    def ConfigureAccount(self, account: EmailAccount):
        """
        Configure the email account.
        
        Args:
            account: EmailAccount configuration
        """
        self._manager.configure_account(account)


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    form = EmailForm(EmailManager())
    Application.Run(form)
