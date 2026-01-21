"""
Email Panel - Embeddable email client component.

This module provides an embeddable email panel that can be integrated
into any WinFormPy application.

Architecture:
    EmailBackend (low-level ops)
        ↓ used by
    EmailManager (business logic)
        ↓ used by
    EmailPanel (this module) / EmailForm (email_ui.py)
"""

import sys
import os

# Add parent path for imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..', '..', '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy.winformpy import (
    Panel, Label, Button, TextBox, RichTextBox, ListBox, TreeView,
    ToolStrip, ToolStripButton, ToolStripSeparator,
    DockStyle, AnchorStyles, BorderStyle, Font, FontStyle,
    ScrollBars, ControlBase
)

# Use try/except for imports to support both direct execution and package import
try:
    from .email_manager import (
        EmailManager, EmailEventType, EmailEvent, EmailFilter,
        SortField, SortOrder
    )
    from .email_backend import (
        EmailMessage, EmailFolder, EmailAccount, EmailAddress,
        EmailFlags, FolderType
    )
except ImportError:
    from email_manager import (
        EmailManager, EmailEventType, EmailEvent, EmailFilter,
        SortField, SortOrder
    )
    from email_backend import (
        EmailMessage, EmailFolder, EmailAccount, EmailAddress,
        EmailFlags, FolderType
    )


class EmailPanel(Panel):
    """
    Embeddable email panel component.
    
    Provides a complete email interface including:
    - Folder tree view
    - Message list
    - Message preview/reading pane
    - Compose functionality
    
    Can be embedded in any WinFormPy Form or Panel.
    
    Usage:
        manager = EmailManager()
        manager.configure_account(account)
        
        panel = EmailPanel(parent_form, manager)
        panel.Dock = DockStyle.Fill
    """
    
    def __init__(self, master, manager: EmailManager = None, props: dict = None):
        """
        Initialize the email panel.
        
        Args:
            master: Parent control
            manager: EmailManager instance. If None, creates a new one.
            props: Additional properties
        """
        super().__init__(master, props)
        
        self._manager = manager or EmailManager()
        self._selected_message: EmailMessage = None
        self._messages: list = []
        
        # Event handlers
        self._on_message_selected = None
        self._on_compose = None
        self._on_reply = None
        self._on_forward = None
        
        self._setup_ui()
        self._setup_events()
        self._load_folders()
    
    # =========================================================================
    # Properties
    # =========================================================================
    
    @property
    def Manager(self) -> EmailManager:
        """Get the email manager."""
        return self._manager
    
    @Manager.setter
    def Manager(self, value: EmailManager):
        """Set the email manager."""
        self._manager = value
        self._load_folders()
    
    @property
    def SelectedMessage(self) -> EmailMessage:
        """Get the currently selected message."""
        return self._selected_message
    
    @property
    def OnMessageSelected(self):
        """Event handler for message selection."""
        return self._on_message_selected
    
    @OnMessageSelected.setter
    def OnMessageSelected(self, handler):
        """Set message selection handler."""
        self._on_message_selected = handler
    
    @property
    def OnCompose(self):
        """Event handler for compose action."""
        return self._on_compose
    
    @OnCompose.setter
    def OnCompose(self, handler):
        """Set compose handler."""
        self._on_compose = handler
    
    # =========================================================================
    # UI Setup
    # =========================================================================
    
    def _setup_ui(self):
        """Set up the user interface."""
        # Toolbar
        self._toolbar = ToolStrip(self, {
            'Dock': DockStyle.Top
        })
        
        # Toolbar buttons
        self._btn_compose = ToolStripButton(self._toolbar, {
            'Text': '✉ New',
            'ToolTipText': 'Compose new email'
        })
        self._btn_compose.Click = self._on_compose_click
        
        self._toolbar.Items.Add(ToolStripSeparator())
        
        self._btn_reply = ToolStripButton(self._toolbar, {
            'Text': '↩ Reply',
            'ToolTipText': 'Reply to sender'
        })
        self._btn_reply.Click = self._on_reply_click
        
        self._btn_reply_all = ToolStripButton(self._toolbar, {
            'Text': '↩↩ Reply All',
            'ToolTipText': 'Reply to all'
        })
        self._btn_reply_all.Click = self._on_reply_all_click
        
        self._btn_forward = ToolStripButton(self._toolbar, {
            'Text': '→ Forward',
            'ToolTipText': 'Forward message'
        })
        self._btn_forward.Click = self._on_forward_click
        
        self._toolbar.Items.Add(ToolStripSeparator())
        
        self._btn_delete = ToolStripButton(self._toolbar, {
            'Text': '🗑 Delete',
            'ToolTipText': 'Delete message'
        })
        self._btn_delete.Click = self._on_delete_click
        
        self._btn_archive = ToolStripButton(self._toolbar, {
            'Text': '📁 Archive',
            'ToolTipText': 'Archive message'
        })
        self._btn_archive.Click = self._on_archive_click
        
        self._toolbar.Items.Add(ToolStripSeparator())
        
        self._btn_refresh = ToolStripButton(self._toolbar, {
            'Text': '🔄 Refresh',
            'ToolTipText': 'Refresh messages'
        })
        self._btn_refresh.Click = self._on_refresh_click
        
        # Left panel - Folder tree
        self._folder_panel = Panel(self, {
            'Dock': DockStyle.Left,
            'Width': 200,
            'BackColor': '#F5F5F5'
        })
        
        self._folder_label = Label(self._folder_panel, {
            'Text': 'Folders',
            'Dock': DockStyle.Top,
            'Height': 30,
            'Font': Font('Segoe UI', 10, FontStyle.Bold)
        })
        
        self._folder_tree = TreeView(self._folder_panel, {
            'Dock': DockStyle.Fill
        })
        self._folder_tree.AfterSelect = self._on_folder_selected
        
        # Main content area
        self._content_panel = Panel(self, {
            'Dock': DockStyle.Fill
        })
        
        # Message list panel (top)
        self._message_list_panel = Panel(self._content_panel, {
            'Dock': DockStyle.Top,
            'Height': 250
        })
        
        # Search bar
        self._search_panel = Panel(self._message_list_panel, {
            'Dock': DockStyle.Top,
            'Height': 35
        })
        
        self._search_box = TextBox(self._search_panel, {
            'Left': 5,
            'Top': 5,
            'Width': 250,
            'Height': 25,
            'PlaceholderText': '🔍 Search messages...'
        })
        self._search_box.TextChanged = self._on_search_changed
        
        # Message list
        self._message_list = ListBox(self._message_list_panel, {
            'Dock': DockStyle.Fill
        })
        self._message_list.SelectedIndexChanged = self._on_message_list_selected
        
        # Reading pane (bottom)
        self._reading_pane = Panel(self._content_panel, {
            'Dock': DockStyle.Fill,
            'BackColor': '#FFFFFF'
        })
        
        # Message header
        self._header_panel = Panel(self._reading_pane, {
            'Dock': DockStyle.Top,
            'Height': 80,
            'BackColor': '#F8F8F8'
        })
        
        self._subject_label = Label(self._header_panel, {
            'Text': '',
            'Left': 10,
            'Top': 5,
            'Width': 600,
            'Height': 25,
            'Font': Font('Segoe UI', 12, FontStyle.Bold)
        })
        
        self._from_label = Label(self._header_panel, {
            'Text': '',
            'Left': 10,
            'Top': 30,
            'Width': 600,
            'Height': 20,
            'Font': Font('Segoe UI', 9)
        })
        
        self._date_label = Label(self._header_panel, {
            'Text': '',
            'Left': 10,
            'Top': 50,
            'Width': 600,
            'Height': 20,
            'ForeColor': '#666666',
            'Font': Font('Segoe UI', 8)
        })
        
        # Message body
        self._body_text = RichTextBox(self._reading_pane, {
            'Dock': DockStyle.Fill,
            'ReadOnly': True,
            'Font': Font('Segoe UI', 10)
        })
        
        self._update_button_states()
    
    def _setup_events(self):
        """Set up event handlers from manager."""
        self._manager.on_event(EmailEventType.NEW_MESSAGE, self._on_new_message)
        self._manager.on_event(EmailEventType.MESSAGE_DELETED, self._on_message_deleted)
        self._manager.on_event(EmailEventType.FOLDER_CHANGED, self._on_folder_changed)
        self._manager.on_event(EmailEventType.SYNC_COMPLETED, self._on_sync_completed)
    
    # =========================================================================
    # Data Loading
    # =========================================================================
    
    def _load_folders(self):
        """Load folder tree."""
        self._folder_tree.BeginUpdate()
        self._folder_tree.Nodes.Clear()
        
        folders = self._manager.refresh_folders()
        
        # Add folder icons based on type
        folder_icons = {
            FolderType.INBOX: '📥',
            FolderType.SENT: '📤',
            FolderType.DRAFTS: '📝',
            FolderType.TRASH: '🗑',
            FolderType.SPAM: '⚠️',
            FolderType.ARCHIVE: '📁',
            FolderType.CUSTOM: '📂'
        }
        
        for folder in folders:
            icon = folder_icons.get(folder.folder_type, '📂')
            display = f"{icon} {folder.display_name}"
            node = self._folder_tree.Nodes.Add(display)
            node.Tag = folder.path
        
        self._folder_tree.EndUpdate()
        
        # Select inbox by default
        if self._folder_tree.Nodes.Count > 0:
            self._folder_tree.SelectedNode = self._folder_tree.Nodes[0]
    
    def _load_messages(self):
        """Load messages for current folder."""
        self._message_list.BeginUpdate()
        self._message_list.Items.Clear()
        
        self._messages = self._manager.get_messages()
        
        for msg in self._messages:
            # Format: [Unread indicator] From - Subject (Date)
            unread = "●" if not msg.is_read else " "
            star = "★" if msg.is_starred else " "
            attach = "📎" if msg.has_attachments else " "
            
            from_name = msg.from_address.display_name if msg.from_address else ""
            if not from_name and msg.from_address:
                from_name = msg.from_address.address
            
            display = f"{unread}{star}{attach} {from_name[:20]} - {msg.subject[:40]} ({msg.date_formatted})"
            self._message_list.Items.Add(display)
        
        self._message_list.EndUpdate()
        self._update_button_states()
    
    def _show_message(self, message: EmailMessage):
        """Display a message in the reading pane."""
        self._selected_message = message
        
        if message:
            # Get full message if needed
            if not message.body_text and not message.body_html:
                message = self._manager.get_message(message.uid)
            
            self._subject_label.Text = message.subject
            
            from_text = str(message.from_address) if message.from_address else "Unknown"
            self._from_label.Text = f"From: {from_text}"
            
            to_text = ", ".join(str(a) for a in message.to_addresses)
            self._date_label.Text = f"To: {to_text} • {message.date_formatted}"
            
            # Show body (prefer plain text for RichTextBox)
            body = message.body_text or message.body_html
            self._body_text.Text = body
            
            # Mark as read
            if not message.is_read:
                self._manager.mark_as_read(message.uid)
        else:
            self._subject_label.Text = ""
            self._from_label.Text = ""
            self._date_label.Text = ""
            self._body_text.Text = ""
        
        self._update_button_states()
    
    def _update_button_states(self):
        """Update toolbar button enabled states."""
        has_selection = self._selected_message is not None
        
        self._btn_reply.Enabled = has_selection
        self._btn_reply_all.Enabled = has_selection
        self._btn_forward.Enabled = has_selection
        self._btn_delete.Enabled = has_selection
        self._btn_archive.Enabled = has_selection
    
    # =========================================================================
    # Event Handlers - Toolbar
    # =========================================================================
    
    def _on_compose_click(self, sender, e):
        """Handle compose button click."""
        if self._on_compose:
            self._on_compose(self, None)
        else:
            self._show_compose_dialog()
    
    def _on_reply_click(self, sender, e):
        """Handle reply button click."""
        if self._selected_message:
            reply = self._manager.create_reply(self._selected_message)
            if self._on_reply:
                self._on_reply(self, reply)
            else:
                self._show_compose_dialog(reply)
    
    def _on_reply_all_click(self, sender, e):
        """Handle reply all button click."""
        if self._selected_message:
            reply = self._manager.create_reply(self._selected_message, reply_all=True)
            if self._on_reply:
                self._on_reply(self, reply)
            else:
                self._show_compose_dialog(reply)
    
    def _on_forward_click(self, sender, e):
        """Handle forward button click."""
        if self._selected_message:
            forward = self._manager.create_forward(self._selected_message)
            if self._on_forward:
                self._on_forward(self, forward)
            else:
                self._show_compose_dialog(forward)
    
    def _on_delete_click(self, sender, e):
        """Handle delete button click."""
        if self._selected_message:
            self._manager.move_to_trash(self._selected_message.uid)
            self._load_messages()
    
    def _on_archive_click(self, sender, e):
        """Handle archive button click."""
        if self._selected_message:
            self._manager.move_to_archive(self._selected_message.uid)
            self._load_messages()
    
    def _on_refresh_click(self, sender, e):
        """Handle refresh button click."""
        self._manager.sync_now()
    
    # =========================================================================
    # Event Handlers - Navigation
    # =========================================================================
    
    def _on_folder_selected(self, sender, e):
        """Handle folder selection."""
        node = self._folder_tree.SelectedNode
        if node and node.Tag:
            self._manager.select_folder(node.Tag)
            self._load_messages()
    
    def _on_message_list_selected(self, sender, e):
        """Handle message list selection."""
        index = self._message_list.SelectedIndex
        if 0 <= index < len(self._messages):
            self._show_message(self._messages[index])
            
            if self._on_message_selected:
                self._on_message_selected(self, self._messages[index])
    
    def _on_search_changed(self, sender, e):
        """Handle search text changed."""
        query = self._search_box.Text.strip()
        
        if query:
            self._messages = self._manager.search(query)
        else:
            self._messages = self._manager.get_messages()
        
        # Refresh list
        self._message_list.BeginUpdate()
        self._message_list.Items.Clear()
        
        for msg in self._messages:
            unread = "●" if not msg.is_read else " "
            star = "★" if msg.is_starred else " "
            attach = "📎" if msg.has_attachments else " "
            
            from_name = msg.from_address.display_name if msg.from_address else ""
            if not from_name and msg.from_address:
                from_name = msg.from_address.address
            
            display = f"{unread}{star}{attach} {from_name[:20]} - {msg.subject[:40]} ({msg.date_formatted})"
            self._message_list.Items.Add(display)
        
        self._message_list.EndUpdate()
    
    # =========================================================================
    # Event Handlers - Manager Events
    # =========================================================================
    
    def _on_new_message(self, event: EmailEvent):
        """Handle new message event."""
        # Refresh if in inbox
        if self._manager.current_folder == "INBOX":
            self._load_messages()
    
    def _on_message_deleted(self, event: EmailEvent):
        """Handle message deleted event."""
        self._load_messages()
        self._show_message(None)
    
    def _on_folder_changed(self, event: EmailEvent):
        """Handle folder changed event."""
        self._load_messages()
    
    def _on_sync_completed(self, event: EmailEvent):
        """Handle sync completed event."""
        self._load_folders()
        self._load_messages()
    
    # =========================================================================
    # Compose Dialog
    # =========================================================================
    
    def _show_compose_dialog(self, message: EmailMessage = None):
        """
        Show compose dialog.
        
        Args:
            message: Pre-filled message for reply/forward
        """
        # This would show a compose dialog
        # For now, just create a simple compose form
        from winformpy.winformpy import Form, MessageBox
        
        compose_form = Form({
            'Text': 'Compose Email',
            'Width': 600,
            'Height': 500
        })
        compose_form.ApplyLayout()
        
        # To field
        Label(compose_form, {
            'Text': 'To:',
            'Left': 10,
            'Top': 10,
            'Width': 50
        })
        to_box = TextBox(compose_form, {
            'Left': 70,
            'Top': 10,
            'Width': 500
        })
        if message and message.to_addresses:
            to_box.Text = ", ".join(str(a) for a in message.to_addresses)
        
        # Subject field
        Label(compose_form, {
            'Text': 'Subject:',
            'Left': 10,
            'Top': 40,
            'Width': 50
        })
        subject_box = TextBox(compose_form, {
            'Left': 70,
            'Top': 40,
            'Width': 500
        })
        if message:
            subject_box.Text = message.subject
        
        # Body
        body_box = RichTextBox(compose_form, {
            'Left': 10,
            'Top': 70,
            'Width': 560,
            'Height': 340
        })
        if message:
            body_box.Text = message.body_text
        
        # Send button
        def on_send(s, e):
            new_msg = self._manager.create_message(
                to=[to_box.Text],
                subject=subject_box.Text,
                body=body_box.Text
            )
            if self._manager.send_message(new_msg):
                MessageBox.Show("Email sent successfully!", "Success")
                compose_form.Close()
            else:
                MessageBox.Show("Failed to send email.", "Error")
        
        send_btn = Button(compose_form, {
            'Text': 'Send',
            'Left': 400,
            'Top': 420,
            'Width': 80
        })
        send_btn.Click = on_send
        
        # Cancel button
        cancel_btn = Button(compose_form, {
            'Text': 'Cancel',
            'Left': 490,
            'Top': 420,
            'Width': 80
        })
        cancel_btn.Click = lambda s, e: compose_form.Close()
        
        compose_form.Show()
    
    # =========================================================================
    # Public Methods
    # =========================================================================
    
    def Refresh(self):
        """Refresh the email panel."""
        self._manager.sync_now()
    
    def SelectFolder(self, folder_path: str):
        """
        Select a folder.
        
        Args:
            folder_path: Folder path to select
        """
        self._manager.select_folder(folder_path)
        self._load_messages()
    
    def ComposeNew(self):
        """Open compose dialog for new message."""
        self._show_compose_dialog()
    
    def Reply(self, reply_all: bool = False):
        """
        Reply to selected message.
        
        Args:
            reply_all: If True, reply to all recipients
        """
        if self._selected_message:
            reply = self._manager.create_reply(self._selected_message, reply_all)
            self._show_compose_dialog(reply)
    
    def Forward(self):
        """Forward selected message."""
        if self._selected_message:
            forward = self._manager.create_forward(self._selected_message)
            self._show_compose_dialog(forward)
    
    def Delete(self, permanent: bool = False):
        """
        Delete selected message.
        
        Args:
            permanent: If True, permanently delete
        """
        if self._selected_message:
            if permanent:
                self._manager.delete_message(self._selected_message.uid, permanent=True)
            else:
                self._manager.move_to_trash(self._selected_message.uid)
            self._load_messages()


# =============================================================================
# Main Entry Point
# =============================================================================

def main():
    """Run the email panel demo."""
    from winformpy.winformpy import Form, Application
    
    # Create form
    form = Form({
        'Text': 'Email Panel Demo',
        'Width': 1200,
        'Height': 800
    })
    form.ApplyLayout()
    
    # Create manager
    manager = EmailManager()
    
    # Create email panel
    panel = EmailPanel(form, manager, {
        'Dock': DockStyle.Fill
    })
    
    # Show form
    Application.Run(form)


if __name__ == "__main__":
    main()
