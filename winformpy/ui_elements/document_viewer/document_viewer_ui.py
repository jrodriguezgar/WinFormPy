"""
Document Viewer UI - Standalone forms and dialogs

This module provides ready-to-use forms for document viewing.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from winformpy.winformpy import (
    Form, Panel, Label, Button, TextBox, MenuStrip, ToolStripMenuItem,
    OpenFileDialog, SaveFileDialog, MessageBox, PrintDialog, PageSetupDialog,
    DockStyle, Font, FontStyle, DialogResult
)

# Handle imports for both module and direct execution
try:
    from .document_backend import DocumentBackend, PDFBackend, WordBackend
    from .document_viewer_panel import DocumentViewerPanel
except ImportError:
    from document_backend import DocumentBackend, PDFBackend, WordBackend
    from document_viewer_panel import DocumentViewerPanel


class DocumentViewerForm(Form):
    """
    Standalone document viewer form with menu bar and full functionality.
    
    Features:
    - File menu (Open, Close, Exit)
    - View menu (Zoom, Navigation)
    - Tools menu (Extract text, Document info)
    - Full document navigation
    - Multiple document format support
    
    Example:
        viewer = DocumentViewerForm()
        viewer.Show()
        
        # Or open a specific file
        viewer = DocumentViewerForm()
        viewer.open_document('report.pdf')
        viewer.Show()
    """
    
    def __init__(self, title: str = "Document Viewer", width: int = 1024, height: int = 768):
        super().__init__()
        
        self.Text = title
        self.Width = width
        self.Height = height
        self.StartPosition = "CenterScreen"
        
        # Apply layout
        self.ApplyLayout()
        
        self._init_menu()
        self._init_viewer_panel()
        self._init_status_bar()
    
    def _init_menu(self):
        """Initialize menu bar."""
        menu = MenuStrip(self)
        
        # File menu
        file_menu = ToolStripMenuItem()
        file_menu.Text = "File"
        
        open_item = ToolStripMenuItem()
        open_item.Text = "Open..."
        open_item.ShortcutKeys = "Ctrl+O"
        open_item.Click = lambda s, e: self._open_file()
        file_menu.DropDownItems.Add(open_item)
        
        close_item = ToolStripMenuItem()
        close_item.Text = "Close Document"
        close_item.Click = lambda s, e: self._close_document()
        file_menu.DropDownItems.Add(close_item)
        
        file_menu.DropDownItems.Add(ToolStripMenuItem())  # Separator
        
        page_setup_item = ToolStripMenuItem()
        page_setup_item.Text = "Page Setup..."
        page_setup_item.Click = lambda s, e: self._show_page_setup()
        file_menu.DropDownItems.Add(page_setup_item)
        
        print_item = ToolStripMenuItem()
        print_item.Text = "Print..."
        print_item.ShortcutKeys = "Ctrl+P"
        print_item.Click = lambda s, e: self._show_print_dialog()
        file_menu.DropDownItems.Add(print_item)
        
        file_menu.DropDownItems.Add(ToolStripMenuItem())  # Separator
        
        exit_item = ToolStripMenuItem()
        exit_item.Text = "Exit"
        exit_item.Click = lambda s, e: self.Close()
        file_menu.DropDownItems.Add(exit_item)
        
        menu.Items.Add(file_menu)
        
        # View menu
        view_menu = ToolStripMenuItem()
        view_menu.Text = "View"
        
        zoom_in_item = ToolStripMenuItem()
        zoom_in_item.Text = "Zoom In"
        zoom_in_item.ShortcutKeys = "Ctrl+Plus"
        zoom_in_item.Click = lambda s, e: self.viewer_panel.zoom_in()
        view_menu.DropDownItems.Add(zoom_in_item)
        
        zoom_out_item = ToolStripMenuItem()
        zoom_out_item.Text = "Zoom Out"
        zoom_out_item.ShortcutKeys = "Ctrl+Minus"
        zoom_out_item.Click = lambda s, e: self.viewer_panel.zoom_out()
        view_menu.DropDownItems.Add(zoom_out_item)
        
        fit_width_item = ToolStripMenuItem()
        fit_width_item.Text = "Fit to Width"
        fit_width_item.Click = lambda s, e: self.viewer_panel.fit_to_width()
        view_menu.DropDownItems.Add(fit_width_item)
        
        menu.Items.Add(view_menu)
        
        # Tools menu
        tools_menu = ToolStripMenuItem()
        tools_menu.Text = "Tools"
        
        extract_text_item = ToolStripMenuItem()
        extract_text_item.Text = "Extract Current Page Text"
        extract_text_item.Click = lambda s, e: self._extract_text()
        tools_menu.DropDownItems.Add(extract_text_item)
        
        doc_info_item = ToolStripMenuItem()
        doc_info_item.Text = "Document Information"
        doc_info_item.Click = lambda s, e: self._show_doc_info()
        tools_menu.DropDownItems.Add(doc_info_item)
        
        menu.Items.Add(tools_menu)
        
        self.MainMenuStrip = menu
    
    def _init_viewer_panel(self):
        """Initialize document viewer panel with full toolbar."""
        self.viewer_panel = DocumentViewerPanel(self, {
            'Dock': DockStyle.Fill
        })
        
        # Panel already has its own toolbar with all buttons
        # All button groups are enabled by default
        
        # Connect events
        self.viewer_panel.PageChanged = self._on_page_changed
        self.viewer_panel.DocumentLoaded = self._on_document_loaded
    
    def _init_status_bar(self):
        """Initialize status bar."""
        self.status_bar = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': 25,
            'BackColor': '#34495e'
        })
        
        self.lbl_status = Label(self.status_bar, {
            'Text': 'Ready',
            'ForeColor': 'white',
            'Left': 10,
            'Top': 5,
            'AutoSize': True
        })
    
    def _open_file(self):
        """Open file dialog and load document."""
        dialog = OpenFileDialog()
        dialog.Filter = (
            "All Documents|*.pdf;*.docx;*.doc;*.txt;*.md;*.jpg;*.png|"
            "PDF Files|*.pdf|"
            "Word Documents|*.docx;*.doc|"
            "Text Files|*.txt;*.md;*.log|"
            "Images|*.jpg;*.jpeg;*.png;*.gif;*.bmp|"
            "All Files|*.*"
        )
        dialog.Title = "Open Document"
        
        if dialog.ShowDialog() == 'OK':
            self.open_document(dialog.FileName)
    
    def open_document(self, file_path: str) -> bool:
        """
        Open a document file.
        
        Args:
            file_path: Path to the document
            
        Returns:
            True if loaded successfully
        """
        success = self.viewer_panel.load_document(file_path)
        
        if success:
            self.Text = f"Document Viewer - {os.path.basename(file_path)}"
            self.lbl_status.Text = f"Loaded: {file_path}"
        else:
            MessageBox.Show(
                f"Failed to load document: {file_path}\n\n"
                "Make sure required libraries are installed:\n"
                "- PyMuPDF (pip install PyMuPDF) for PDF\n"
                "- python-docx (pip install python-docx) for Word",
                "Error Loading Document",
                "OK",
                "Error"
            )
            self.lbl_status.Text = "Failed to load document"
        
        return success
    
    def _close_document(self):
        """Close current document."""
        self.viewer_panel.close_document()
        self.Text = "Document Viewer"
        self.lbl_status.Text = "Document closed"
    
    def _extract_text(self):
        """Extract text from current page."""
        text = self.viewer_panel.get_current_page_text()
        
        if text:
            # Show in a dialog
            TextDisplayDialog(self, "Page Text", text).ShowDialog()
        else:
            MessageBox.Show("No text available on current page", "Extract Text", "OK", "Information")
    
    def _show_doc_info(self):
        """Show document information."""
        info = self.viewer_panel.get_document_info()
        
        if info:
            msg = f"File: {info.get('file_path', 'N/A')}\n"
            msg += f"Format: {info.get('format', 'Unknown')}\n"
            msg += f"Pages: {info.get('page_count', 0)}"
            
            MessageBox.Show(msg, "Document Information", "OK", "Information")
        else:
            MessageBox.Show("No document loaded", "Document Information", "OK", "Information")
    
    def _on_page_changed(self, sender, e):
        """Handle page change event."""
        page = e.get('page', 0)
        self.lbl_status.Text = f"Page {page + 1}"
    
    def _on_document_loaded(self, sender, e):
        """Handle document loaded event."""
        file_path = e.get('file_path', '')
        self.lbl_status.Text = f"Loaded: {os.path.basename(file_path)}"
    
    def _show_page_setup(self):
        """Show page setup dialog."""
        dialog = PageSetupDialog()
        
        result = dialog.ShowDialog()
        
        if result == 'OK':
            # Show current settings
            msg = "Page Setup:\n\n"
            msg += f"Paper Size: {dialog.PaperSize}\n"
            msg += f"Orientation: {dialog.Landscape and 'Landscape' or 'Portrait'}\n"
            msg += f"Margins: L={dialog.MarginLeft}, R={dialog.MarginRight}, "
            msg += f"T={dialog.MarginTop}, B={dialog.MarginBottom}"
            
            MessageBox.Show(msg, "Page Setup Applied", "OK", "Information")
    
    def _show_print_dialog(self):
        """Show print dialog."""
        if not self.viewer_panel.backend or not self.viewer_panel.backend.document_loaded:
            MessageBox.Show(
                "No document loaded. Please open a document first.",
                "Print",
                "OK",
                "Warning"
            )
            return
        
        dialog = PrintDialog()
        
        # Set document name
        if self.viewer_panel.backend.file_path:
            dialog.DocumentName = os.path.basename(self.viewer_panel.backend.file_path)
        
        result = dialog.ShowDialog()
        
        if result == 'OK':
            # Show print settings that would be used
            msg = "Print Settings:\n\n"
            msg += f"Document: {dialog.DocumentName}\n"
            msg += f"Printer: {dialog.PrinterName}\n"
            msg += f"Copies: {dialog.Copies}\n"
            msg += f"Page Range: {dialog.PrintRange}\n"
            
            if dialog.PrintRange == 'Selection' or dialog.PrintRange == 'Pages':
                msg += f"From Page: {dialog.FromPage}\n"
                msg += f"To Page: {dialog.ToPage}\n"
            
            msg += f"Collate: {dialog.Collate}\n"
            
            MessageBox.Show(
                msg + "\nNote: Actual printing functionality requires printer integration.",
                "Print Configuration",
                "OK",
                "Information"
            )


class DocumentViewerDialog(Form):
    """
    Modal dialog for viewing a document.
    
    Use this when you need to show a document in a modal window.
    
    Example:
        dialog = DocumentViewerDialog(parent_form, 'report.pdf')
        result = dialog.ShowDialog()
    """
    
    def __init__(self, parent=None, file_path: str = None, title: str = "View Document"):
        super().__init__()
        
        self.Text = title
        self.Width = 900
        self.Height = 700
        self.StartPosition = "CenterParent"
        
        # Apply layout
        self.ApplyLayout()
        
        self._init_viewer_panel()
        self._init_buttons()
        
        # Load document if provided
        if file_path:
            self.viewer_panel.load_document(file_path)
            self.Text = f"{title} - {os.path.basename(file_path)}"
    
    def _init_viewer_panel(self):
        """Initialize viewer panel."""
        self.viewer_panel = DocumentViewerPanel(self, {
            'Dock': DockStyle.Fill
        })
    
    def _init_buttons(self):
        """Initialize button panel."""
        button_panel = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': 50,
            'BackColor': '#ecf0f1'
        })
        
        btn_close = Button(button_panel, {
            'Text': 'Close',
            'Left': 780,
            'Top': 10,
            'Width': 100,
            'Height': 30
        })
        btn_close.Click = lambda s, e: self.Close()


class TextDisplayDialog(Form):
    """Simple dialog to display extracted text."""
    
    def __init__(self, parent, title: str, text: str):
        super().__init__()
        
        self.Text = title
        self.Width = 700
        self.Height = 500
        self.StartPosition = "CenterParent"
        
        self.ApplyLayout()
        
        # Text area
        txt = TextBox(self, {
            'Multiline': True,
            'ReadOnly': True,
            'ScrollBars': 'Both',
            'Dock': DockStyle.Fill,
            'Font': Font('Consolas', 10),
            'Text': text
        })
        
        # Button panel
        button_panel = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': 50,
            'BackColor': '#ecf0f1'
        })
        
        btn_copy = Button(button_panel, {
            'Text': 'Copy to Clipboard',
            'Left': 20,
            'Top': 10,
            'Width': 150,
            'Height': 30
        })
        btn_copy.Click = lambda s, e: self._copy_to_clipboard(text)
        
        btn_close = Button(button_panel, {
            'Text': 'Close',
            'Left': 570,
            'Top': 10,
            'Width': 100,
            'Height': 30
        })
        btn_close.Click = lambda s, e: self.Close()
    
    def _copy_to_clipboard(self, text):
        """Copy text to clipboard."""
        try:
            from winformpy.winformpy import Clipboard
            Clipboard.SetText(text)
            MessageBox.Show("Text copied to clipboard", "Success", "OK", "Information")
        except Exception as e:
            MessageBox.Show(f"Failed to copy: {e}", "Error", "OK", "Error")


# Example usage
if __name__ == "__main__":
    from winformpy.winformpy import Application
    
    # Simple standalone viewer
    viewer = DocumentViewerForm()
    viewer.Show()
    Application.Run(viewer)
