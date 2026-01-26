"""
Document Viewer Example - WinFormPy

This example demonstrates the Document Viewer UI element for previewing
various document formats including PDF, Word, images, and text files.

Features demonstrated:
- Loading different document types
- Page navigation
- Zoom controls
- Text extraction
- Document information
- Multiple viewer modes (panel, form, dialog)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from winformpy import (
    Form, Panel, Label, Button, ListBox, TextBox, TabControl, TabPage,
    OpenFileDialog, MessageBox, DockStyle, Font, FontStyle, Application
)

# Import document viewer components
from winformpy.ui_elements.document_viewer import (
    DocumentViewerPanel, DocumentViewerForm, DocumentViewerDialog,
    PDFBackend, WordBackend, ImageBackend
)


class DocumentViewerExampleForm(Form):
    """
    Main form demonstrating Document Viewer functionality.
    """
    
    def __init__(self):
        super().__init__()
        self.Text = "Document Viewer Example"
        self.Width = 1200
        self.Height = 800
        self.StartPosition = "CenterScreen"
        
        # Sample documents list
        self.sample_documents = []
        
        # Apply layout
        self.ApplyLayout()
        
        self._init_header()
        self._init_tabs()
        self._init_footer()
    
    def _init_header(self):
        """Initialize header."""
        header = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 80,
            'BackColor': '#2c3e50'
        })
        
        Label(header, {
            'Text': 'Document Viewer UI Element Demo',
            'Font': Font('Segoe UI', 16, FontStyle.Bold),
            'ForeColor': 'white',
            'BackColor': '#2c3e50',
            'Left': 20,
            'Top': 15,
            'AutoSize': True
        })
        
        Label(header, {
            'Text': 'Preview PDF, Word, images, and text files with built-in viewer',
            'Font': Font('Segoe UI', 10),
            'ForeColor': '#bdc3c7',
            'BackColor': '#2c3e50',
            'Left': 20,
            'Top': 50,
            'AutoSize': True
        })
    
    def _init_tabs(self):
        """Initialize tab control."""
        tabs = TabControl(self, {
            'Dock': DockStyle.Fill
        })
        
        # Tab 1: Embedded Panel
        self._create_embedded_panel_tab(tabs)
        
        # Tab 2: Standalone Form
        self._create_standalone_form_tab(tabs)
        
        # Tab 3: Modal Dialog
        self._create_modal_dialog_tab(tabs)
        
        # Tab 4: Features Demo
        self._create_features_tab(tabs)
    
    def _create_embedded_panel_tab(self, parent):
        """Create embedded panel demonstration tab."""
        tab = TabPage(parent, {
            'Text': 'Embedded Panel',
            'BackColor': 'white'
        })
        
        # Left side: Controls
        left_panel = Panel(tab, {
            'Dock': DockStyle.Left,
            'Width': 250,
            'BackColor': '#ecf0f1'
        })
        
        Label(left_panel, {
            'Text': 'Document Viewer Panel',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'ForeColor': '#2c3e50',
            'BackColor': '#ecf0f1',
            'Left': 10,
            'Top': 10,
            'AutoSize': True
        })
        
        Label(left_panel, {
            'Text': 'Load a document to preview:',
            'ForeColor': '#2c3e50',
            'BackColor': '#ecf0f1',
            'Left': 10,
            'Top': 45,
            'Width': 230
        })
        
        # Quick load buttons
        y = 75
        
        btn_open_pdf = Button(left_panel, {
            'Text': 'Open PDF...',
            'Left': 10,
            'Top': y,
            'Width': 230,
            'Height': 35
        })
        btn_open_pdf.Click = lambda s, e: self._open_document_for_panel('PDF')
        
        y += 45
        btn_open_word = Button(left_panel, {
            'Text': 'Open Word...',
            'Left': 10,
            'Top': y,
            'Width': 230,
            'Height': 35
        })
        btn_open_word.Click = lambda s, e: self._open_document_for_panel('Word')
        
        y += 45
        btn_open_image = Button(left_panel, {
            'Text': 'Open Image...',
            'Left': 10,
            'Top': y,
            'Width': 230,
            'Height': 35
        })
        btn_open_image.Click = lambda s, e: self._open_document_for_panel('Image')
        
        y += 45
        btn_open_text = Button(left_panel, {
            'Text': 'Open Text File...',
            'Left': 10,
            'Top': y,
            'Width': 230,
            'Height': 35
        })
        btn_open_text.Click = lambda s, e: self._open_document_for_panel('Text')
        
        y += 60
        Label(left_panel, {
            'Text': 'Document Info:',
            'Font': Font('Segoe UI', 9, FontStyle.Bold),
            'ForeColor': '#2c3e50',
            'BackColor': '#ecf0f1',
            'Left': 10,
            'Top': y,
            'AutoSize': True
        })
        
        y += 25
        self.lbl_doc_info = Label(left_panel, {
            'Text': 'No document loaded',
            'ForeColor': '#34495e',
            'BackColor': '#ecf0f1',
            'Left': 10,
            'Top': y,
            'Width': 230,
            'Height': 100
        })
        
        y += 110
        btn_extract = Button(left_panel, {
            'Text': 'Extract Page Text',
            'Left': 10,
            'Top': y,
            'Width': 230,
            'Height': 35
        })
        btn_extract.Click = lambda s, e: self._extract_text_from_panel()
        
        # Right side: Document viewer panel
        self.viewer_panel = DocumentViewerPanel(tab, {
            'Dock': DockStyle.Fill
        })
        
        # Connect events
        self.viewer_panel.DocumentLoaded = self._on_panel_document_loaded
        self.viewer_panel.PageChanged = self._on_panel_page_changed
    
    def _create_standalone_form_tab(self, parent):
        """Create standalone form demonstration tab."""
        tab = TabPage(parent, {
            'Text': 'Standalone Form',
            'BackColor': '#f8f9fa'
        })
        
        Label(tab, {
            'Text': 'Standalone Document Viewer Form',
            'Font': Font('Segoe UI', 12, FontStyle.Bold),
            'Left': 20,
            'Top': 20,
            'AutoSize': True
        })
        
        Label(tab, {
            'Text': 'Opens a complete document viewer in a separate window\n'
                   'with menu bar, toolbar, and full functionality.',
            'Left': 20,
            'Top': 55,
            'Width': 500,
            'Height': 50
        })
        
        btn_open_viewer = Button(tab, {
            'Text': 'Open Document Viewer Form',
            'Left': 20,
            'Top': 120,
            'Width': 250,
            'Height': 40,
            'Font': Font('Segoe UI', 10, FontStyle.Bold)
        })
        btn_open_viewer.Click = lambda s, e: self._open_standalone_viewer()
        
        # Features list
        Label(tab, {
            'Text': 'Features:',
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'Left': 20,
            'Top': 180,
            'AutoSize': True
        })
        
        features = [
            "✓ File menu (Open, Close, Exit)",
            "✓ View menu (Zoom controls)",
            "✓ Tools menu (Extract text, Document info)",
            "✓ Keyboard shortcuts (Ctrl+O, Ctrl+Plus, Ctrl+Minus)",
            "✓ Status bar with current page info",
            "✓ Full navigation controls"
        ]
        
        y = 210
        for feature in features:
            Label(tab, {
                'Text': feature,
                'Left': 30,
                'Top': y,
                'AutoSize': True
            })
            y += 25
    
    def _create_modal_dialog_tab(self, parent):
        """Create modal dialog demonstration tab."""
        tab = TabPage(parent, {
            'Text': 'Modal Dialog',
            'BackColor': 'white'
        })
        
        Label(tab, {
            'Text': 'Document Viewer as Modal Dialog',
            'Font': Font('Segoe UI', 12, FontStyle.Bold),
            'Left': 20,
            'Top': 20,
            'AutoSize': True
        })
        
        Label(tab, {
            'Text': 'Shows a document in a modal dialog window.\n'
                   'Useful for quick document preview in workflows.',
            'Left': 20,
            'Top': 55,
            'Width': 500,
            'Height': 50
        })
        
        btn_show_dialog = Button(tab, {
            'Text': 'Open Document in Dialog',
            'Left': 20,
            'Top': 120,
            'Width': 250,
            'Height': 40,
            'Font': Font('Segoe UI', 10, FontStyle.Bold)
        })
        btn_show_dialog.Click = lambda s, e: self._show_modal_dialog()
        
        # Use case examples
        Label(tab, {
            'Text': 'Use Cases:',
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'Left': 20,
            'Top': 180,
            'AutoSize': True
        })
        
        use_cases = [
            "• Preview attachments in email client",
            "• View reports before printing",
            "• Quick document verification",
            "• Invoice/receipt preview",
            "• Contract review workflow"
        ]
        
        y = 210
        for case in use_cases:
            Label(tab, {
                'Text': case,
                'Left': 30,
                'Top': y,
                'AutoSize': True
            })
            y += 25
    
    def _create_features_tab(self, parent):
        """Create features demonstration tab."""
        tab = TabPage(parent, {
            'Text': 'Features & API',
            'BackColor': '#f8f9fa'
        })
        
        Label(tab, {
            'Text': 'Document Viewer Features',
            'Font': Font('Segoe UI', 12, FontStyle.Bold),
            'Left': 20,
            'Top': 20,
            'AutoSize': True
        })
        
        # Supported formats
        Label(tab, {
            'Text': 'Supported Formats:',
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'Left': 20,
            'Top': 60,
            'AutoSize': True
        })
        
        formats_text = """
• PDF - Full support with PyMuPDF (pip install PyMuPDF)
• Word - .docx, .doc with python-docx (pip install python-docx)
• Images - JPG, PNG, GIF, BMP (built-in)
• Text - TXT, MD, LOG, code files (built-in)
        """
        
        Label(tab, {
            'Text': formats_text.strip(),
            'Left': 30,
            'Top': 90,
            'Width': 500,
            'Height': 100
        })
        
        # API Examples
        Label(tab, {
            'Text': 'Code Examples:',
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'Left': 20,
            'Top': 210,
            'AutoSize': True
        })
        
        code_example = """
# Basic usage
panel = DocumentViewerPanel(parent_form)
panel.Dock = DockStyle.Fill
panel.load_document('report.pdf')

# Navigation
panel.next_page()
panel.previous_page()
panel.go_to_page(5)

# Zoom
panel.zoom_in()
panel.set_zoom(150)

# Extract text
text = panel.get_current_page_text()
        """
        
        TextBox(tab, {
            'Multiline': True,
            'ReadOnly': True,
            'Left': 20,
            'Top': 240,
            'Width': 550,
            'Height': 280,
            'Font': Font('Consolas', 9),
            'Text': code_example.strip(),
            'ScrollBars': 'Vertical'
        })
        
        # Installation instructions
        Label(tab, {
            'Text': 'Installation:',
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'Left': 600,
            'Top': 60,
            'AutoSize': True
        })
        
        install_text = """
pip install PyMuPDF
pip install python-docx
pip install Pillow
        """
        
        TextBox(tab, {
            'Multiline': True,
            'ReadOnly': True,
            'Left': 600,
            'Top': 90,
            'Width': 350,
            'Height': 80,
            'Font': Font('Consolas', 9),
            'Text': install_text.strip()
        })
    
    def _init_footer(self):
        """Initialize footer."""
        footer = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': 50,
            'BackColor': '#ecf0f1'
        })
        
        btn_close = Button(footer, {
            'Text': 'Close',
            'Left': 1070,
            'Top': 10,
            'Width': 100,
            'Height': 30
        })
        btn_close.Click = lambda s, e: self.Close()
    
    def _open_document_for_panel(self, doc_type):
        """Open document in embedded panel."""
        dialog = OpenFileDialog()
        
        if doc_type == 'PDF':
            dialog.Filter = "PDF Files|*.pdf"
        elif doc_type == 'Word':
            dialog.Filter = "Word Documents|*.docx;*.doc"
        elif doc_type == 'Image':
            dialog.Filter = "Images|*.jpg;*.jpeg;*.png;*.gif;*.bmp"
        elif doc_type == 'Text':
            dialog.Filter = "Text Files|*.txt;*.md;*.log;*.py;*.json"
        else:
            dialog.Filter = "All Files|*.*"
        
        if dialog.ShowDialog() == 'OK':
            success = self.viewer_panel.load_document(dialog.FileName)
            
            if not success:
                MessageBox.Show(
                    f"Failed to load document.\n\n"
                    f"Make sure required libraries are installed:\n"
                    f"- PyMuPDF for PDF: pip install PyMuPDF\n"
                    f"- python-docx for Word: pip install python-docx",
                    "Error",
                    "OK",
                    "Error"
                )
    
    def _on_panel_document_loaded(self, sender, e):
        """Handle document loaded event."""
        info = self.viewer_panel.get_document_info()
        
        info_text = f"File: {os.path.basename(info.get('file_path', ''))}\n"
        info_text += f"Format: {info.get('format', 'Unknown')}\n"
        info_text += f"Pages: {info.get('page_count', 0)}"
        
        self.lbl_doc_info.Text = info_text
    
    def _on_panel_page_changed(self, sender, e):
        """Handle page changed event."""
        page = e.get('page', 0)
        info = self.viewer_panel.get_document_info()
        total = info.get('page_count', 0)
        
        # Update info
        info_text = f"File: {os.path.basename(info.get('file_path', ''))}\n"
        info_text += f"Format: {info.get('format', 'Unknown')}\n"
        info_text += f"Page: {page + 1} / {total}"
        
        self.lbl_doc_info.Text = info_text
    
    def _extract_text_from_panel(self):
        """Extract text from current page."""
        text = self.viewer_panel.get_current_page_text()
        
        if text:
            # Show in message box (in real app, use a proper text viewer)
            MessageBox.Show(
                text[:500] + ("..." if len(text) > 500 else ""),
                "Page Text (Preview)",
                "OK",
                "Information"
            )
        else:
            MessageBox.Show("No text available", "Extract Text", "OK", "Information")
    
    def _open_standalone_viewer(self):
        """Open standalone viewer form."""
        viewer = DocumentViewerForm("Document Viewer - Standalone")
        viewer.Show()
    
    def _show_modal_dialog(self):
        """Show document in modal dialog."""
        dialog = OpenFileDialog()
        dialog.Filter = "All Documents|*.pdf;*.docx;*.doc;*.txt;*.jpg;*.png|All Files|*.*"
        
        if dialog.ShowDialog() == 'OK':
            doc_dialog = DocumentViewerDialog(self, dialog.FileName, "Document Preview")
            doc_dialog.ShowDialog()


def main():
    form = DocumentViewerExampleForm()
    Application.Run(form)


if __name__ == '__main__':
    main()
