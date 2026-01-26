"""
Document Viewer Panel - Reusable panel component for document preview

This module provides the main panel component for embedding document
viewing functionality into your forms.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from winformpy.winformpy import (
    Panel, Label, Button, PictureBox, TextBox, ComboBox, TrackBar,
    DockStyle, AnchorStyles, Font, FontStyle, PrinterSettings,
    PageSetupDialog, PrintDialog
)
from typing import Optional, Callable
import tkinter as tk
from io import BytesIO

# Handle imports for both module and direct execution
try:
    from .document_backend import (
        DocumentBackend, PDFBackend, WordBackend, ImageBackend, TextBackend
    )
except ImportError:
    from document_backend import (
        DocumentBackend, PDFBackend, WordBackend, ImageBackend, TextBackend
    )


class DocumentViewerPanel(Panel):
    """
    A reusable panel for viewing documents.
    
    Features:
    - PDF, Word, Image, and Text file support
    - Page navigation (previous/next, jump to page)
    - Zoom in/out
    - Fit to width/height
    - Text extraction view
    - Document information display
    
    Example:
        panel = DocumentViewerPanel(parent_form)
        panel.Dock = DockStyle.Fill
        panel.load_document('report.pdf')
        
        # Or with a specific backend
        backend = PDFBackend()
        panel = DocumentViewerPanel(parent_form, {'backend': backend})
        panel.load_document('document.pdf')
    """
    
    def __init__(self, parent, props: dict = None):
        super().__init__(parent, props)
        
        # Extract backend from props if provided
        self.backend = None
        if props and 'backend' in props:
            self.backend = props['backend']
        
        self.current_zoom = 100  # Percent
        self.fit_mode = None  # None, 'width', 'height', 'page'
        
        # Document settings storage - Using official PrinterSettings object
        self.PrinterSettings = PrinterSettings()
        
        # Page setup settings dictionary
        self.page_setup_settings = {
            'paper_size': 'Letter',
            'orientation': 'Portrait',
            'margin_left': 1.0,
            'margin_right': 1.0,
            'margin_top': 1.0,
            'margin_bottom': 1.0
        }
        
        self.print_settings = {
            'printer_name': 'Default Printer',
            'copies': 1,
            'print_range': 'All',
            'from_page': 1,
            'to_page': 1,
            'collate': True,
            'document_name': ''
        }
        
        # Toolbar visibility properties
        self._show_toolbar = True
        self._show_document_buttons = True
        self._show_navigation_buttons = True
        self._show_zoom_buttons = True
        self._show_view_buttons = True
        self._show_settings_panel = False  # Show/hide settings panel
        
        # Events
        self.PageChanged = None  # Callback when page changes
        self.DocumentLoaded = None  # Callback when document loads
        self.ZoomChanged = None  # Callback when zoom changes
        
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI components."""
        # Toolbar panel - Windows 11 style
        self.toolbar = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 45,
            'BackColor': '#f3f3f3'
        })
        
        # Document operations buttons group (starts at x=10)
        self._doc_buttons_x = 10
        
        self.btn_printer_setup = Button(self.toolbar, {
            'Text': '🖨 Printer',
            'Left': self._doc_buttons_x,
            'Top': 8,
            'Width': 85,
            'Height': 28,
            'BackColor': '#ffffff',
            'ForeColor': '#333333',
            'BorderWidth': 1
        })
        self.btn_printer_setup.Click = lambda s, e: self._show_printer_setup()
        
        self.btn_page_setup = Button(self.toolbar, {
            'Text': '📄 Page',
            'Left': self._doc_buttons_x + 92,
            'Top': 8,
            'Width': 75,
            'Height': 28,
            'BackColor': '#ffffff',
            'ForeColor': '#333333',
            'BorderWidth': 1
        })
        self.btn_page_setup.Click = lambda s, e: self._show_page_setup()
        
        self.btn_print = Button(self.toolbar, {
            'Text': '🖨 Print',
            'Left': self._doc_buttons_x + 174,
            'Top': 8,
            'Width': 75,
            'Height': 28,
            'BackColor': '#ffffff',
            'ForeColor': '#333333',
            'BorderWidth': 1
        })
        self.btn_print.Click = lambda s, e: self._show_print_dialog()
        
        # Separator after document buttons
        self._sep_doc = Label(self.toolbar, {
            'Text': '│',
            'ForeColor': '#cccccc',
            'Left': self._doc_buttons_x + 258,
            'Top': 10,
            'Width': 10,
            'Font': Font('Segoe UI', 11)
        })
        
        # Navigation buttons group (starts after separator)
        self._nav_buttons_x = self._doc_buttons_x + 275
        
        self.btn_first = Button(self.toolbar, {
            'Text': '⏮',
            'Left': self._nav_buttons_x,
            'Top': 8,
            'Width': 38,
            'Height': 28,
            'BackColor': '#ffffff',
            'ForeColor': '#333333',
            'BorderWidth': 1
        })
        self.btn_first.Click = lambda s, e: self.go_to_first_page()
        
        self.btn_prev = Button(self.toolbar, {
            'Text': '◀',
            'Left': self._nav_buttons_x + 42,
            'Top': 8,
            'Width': 38,
            'Height': 28,
            'BackColor': '#ffffff',
            'ForeColor': '#333333',
            'BorderWidth': 1
        })
        self.btn_prev.Click = lambda s, e: self.previous_page()
        
        # Page info label
        self.lbl_page = Label(self.toolbar, {
            'Text': 'Page: -',
            'ForeColor': '#555555',
            'Left': self._nav_buttons_x + 85,
            'Top': 13,
            'Width': 100,
            'TextAlign': 'MiddleCenter',
            'Font': Font('Segoe UI', 9)
        })
        
        self.btn_next = Button(self.toolbar, {
            'Text': '▶',
            'Left': self._nav_buttons_x + 190,
            'Top': 8,
            'Width': 38,
            'Height': 28,
            'BackColor': '#ffffff',
            'ForeColor': '#333333',
            'BorderWidth': 1
        })
        self.btn_next.Click = lambda s, e: self.next_page()
        
        self.btn_last = Button(self.toolbar, {
            'Text': '⏭',
            'Left': self._nav_buttons_x + 232,
            'Top': 8,
            'Width': 38,
            'Height': 28,
            'BackColor': '#ffffff',
            'ForeColor': '#333333',
            'BorderWidth': 1
        })
        self.btn_last.Click = lambda s, e: self.go_to_last_page()
        
        # Separator after navigation
        self._sep_nav = Label(self.toolbar, {
            'Text': '│',
            'ForeColor': '#cccccc',
            'Left': self._nav_buttons_x + 278,
            'Top': 10,
            'Width': 10,
            'Font': Font('Segoe UI', 11)
        })
        
        # Zoom buttons group
        self._zoom_buttons_x = self._nav_buttons_x + 295
        
        self.btn_zoom_out = Button(self.toolbar, {
            'Text': '🔍−',
            'Left': self._zoom_buttons_x,
            'Top': 8,
            'Width': 45,
            'Height': 28,
            'BackColor': '#ffffff',
            'ForeColor': '#333333',
            'BorderWidth': 1
        })
        self.btn_zoom_out.Click = lambda s, e: self.zoom_out()
        
        self.lbl_zoom = Label(self.toolbar, {
            'Text': '100%',
            'ForeColor': '#555555',
            'Left': self._zoom_buttons_x + 50,
            'Top': 13,
            'Width': 55,
            'TextAlign': 'MiddleCenter',
            'Font': Font('Segoe UI', 9)
        })
        
        self.btn_zoom_in = Button(self.toolbar, {
            'Text': '🔍+',
            'Left': self._zoom_buttons_x + 110,
            'Top': 8,
            'Width': 45,
            'Height': 28,
            'BackColor': '#ffffff',
            'ForeColor': '#333333',
            'BorderWidth': 1
        })
        self.btn_zoom_in.Click = lambda s, e: self.zoom_in()
        
        # Separator after zoom
        self._sep_zoom = Label(self.toolbar, {
            'Text': '│',
            'ForeColor': '#cccccc',
            'Left': self._zoom_buttons_x + 163,
            'Top': 10,
            'Width': 10,
            'Font': Font('Segoe UI', 11)
        })
        
        # View buttons group
        self._view_buttons_x = self._zoom_buttons_x + 180
        
        self.btn_fit_width = Button(self.toolbar, {
            'Text': '⬜ Fit',
            'Left': self._view_buttons_x,
            'Top': 8,
            'Width': 65,
            'Height': 28,
            'BackColor': '#ffffff',
            'ForeColor': '#333333',
            'BorderWidth': 1
        })
        self.btn_fit_width.Click = lambda s, e: self.fit_to_width()
        
        self.btn_extract_text = Button(self.toolbar, {
            'Text': '📝 Text',
            'Left': self._view_buttons_x + 72,
            'Top': 8,
            'Width': 65,
            'Height': 28,
            'BackColor': '#ffffff',
            'ForeColor': '#333333',
            'BorderWidth': 1
        })
        self.btn_extract_text.Click = lambda s, e: self._show_page_text()
        
        # Separator after view buttons
        self._sep_view = Label(self.toolbar, {
            'Text': '│',
            'ForeColor': '#cccccc',
            'Left': self._view_buttons_x + 145,
            'Top': 10,
            'Width': 10,
            'Font': Font('Segoe UI', 11)
        })
        
        # Settings toggle button
        self.btn_settings = Button(self.toolbar, {
            'Text': '⚙ Settings',
            'Left': self._view_buttons_x + 162,
            'Top': 8,
            'Width': 80,
            'Height': 28,
            'BackColor': '#ffffff',
            'ForeColor': '#333333',
            'BorderWidth': 1
        })
        self.btn_settings.Click = lambda s, e: self._toggle_settings_panel()
        
        # Settings panel (initially hidden)
        self.settings_panel = Panel(self, {
            'Dock': DockStyle.Right,
            'Width': 0,  # Hidden by default
            'BackColor': '#fafafa',
            'BorderStyle': 'FixedSingle'
        })
        
        # Settings panel content
        self._init_settings_panel()
        
        # Document display area
        self.display_panel = Panel(self, {
            'Dock': DockStyle.Fill,
            'BackColor': '#95a5a6',
            'AutoScroll': True
        })
        
        # PictureBox for document page
        self.picture_box = PictureBox(self.display_panel, {
            'Left': 10,
            'Top': 10,
            'Width': 600,
            'Height': 800,
            'BackColor': 'white',
            'BorderStyle': 'FixedSingle',
            'SizeMode': 'Zoom'
        })
        
        # Status bar
        self.status_bar = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': 28,
            'BackColor': '#f3f3f3',
            'BorderStyle': 'FixedSingle'
        })
        
        self.lbl_status = Label(self.status_bar, {
            'Text': 'No document loaded',
            'Left': 10,
            'Top': 6,
            'Width': 500,
            'AutoSize': False,
            'ForeColor': '#555555',
            'Font': Font('Segoe UI', 9)
        })
        
        # Initially disable navigation
        self._update_navigation_state()
        self._update_toolbar_visibility()
    
    def _init_settings_panel(self):
        """Initialize settings panel with Page Setup and Print settings display."""
        # Title
        title = Label(self.settings_panel, {
            'Text': 'Document Settings',
            'Left': 10,
            'Top': 10,
            'Width': 280,
            'Font': Font('Segoe UI', 10, FontStyle.Bold)
        })
        
        # Page Setup section
        lbl_page_setup = Label(self.settings_panel, {
            'Text': 'Page Setup:',
            'Left': 10,
            'Top': 40,
            'Width': 280,
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        
        self.txt_settings_display = TextBox(self.settings_panel, {
            'Left': 10,
            'Top': 65,
            'Width': 280,
            'Height': 250,
            'Multiline': True,
            'ReadOnly': True,
            'BackColor': 'white',
            'ScrollBars': 'Vertical'
        })
        
        # Refresh button
        btn_refresh = Button(self.settings_panel, {
            'Text': '🔄 Refresh Settings',
            'Left': 10,
            'Top': 325,
            'Width': 280,
            'Height': 30
        })
        btn_refresh.Click = lambda s, e: self._update_settings_display()
        
        # Close button
        btn_close = Button(self.settings_panel, {
            'Text': '✖ Close',
            'Left': 10,
            'Top': 365,
            'Width': 280,
            'Height': 30,
            'BackColor': '#e74c3c',
            'ForeColor': 'white'
        })
        btn_close.Click = lambda s, e: setattr(self, 'ShowSettingsPanel', False)
        
        self._update_settings_display()
    
    def _update_settings_display(self):
        """Update the settings display with current values."""
        if not hasattr(self, 'txt_settings_display'):
            return
        
        ps = self.PrinterSettings
        text = "═══ PRINTER SETTINGS ═══\n\n"
        text += f"Printer: {ps.PrinterName}\n"
        text += f"Paper Size: {ps.PaperSize}\n"
        text += f"Orientation: {'Landscape' if ps.Landscape else 'Portrait'}\n"
        text += f"Color: {'Color' if ps.Color else 'Grayscale'}\n"
        text += f"Duplex: {ps.Duplex}\n"
        text += f"Copies: {ps.Copies}\n"
        text += f"Print Range: {ps.PrintRange}\n"
        text += f"Valid: {'Yes' if ps.IsValid else 'No'}\n"
        text += f"Default: {'Yes' if ps.IsDefaultPrinter else 'No'}\n"
        
        text += "\n═══ PAGE SETUP ═══\n\n"
        text += f"Paper Size: {self.page_setup_settings['paper_size']}\n"
        text += f"Orientation: {self.page_setup_settings['orientation']}\n"
        text += f"Margins:\n"
        text += f"  Left:   {self.page_setup_settings['margin_left']} inches\n"
        text += f"  Right:  {self.page_setup_settings['margin_right']} inches\n"
        text += f"  Top:    {self.page_setup_settings['margin_top']} inches\n"
        text += f"  Bottom: {self.page_setup_settings['margin_bottom']} inches\n"
        text += "\n═══ PRINT SETTINGS ═══\n\n"
        text += f"Printer: {self.print_settings['printer_name']}\n"
        text += f"Document: {self.print_settings['document_name'] or 'Not set'}\n"
        text += f"Copies: {self.print_settings['copies']}\n"
        text += f"Range: {self.print_settings['print_range']}\n"
        
        if self.print_settings['print_range'] in ['Selection', 'Pages']:
            text += f"  From Page: {self.print_settings['from_page']}\n"
            text += f"  To Page: {self.print_settings['to_page']}\n"
        
        text += f"Collate: {'Yes' if self.print_settings['collate'] else 'No'}\n"
        
        self.txt_settings_display.Text = text
    
    @property
    def ShowSettingsPanel(self) -> bool:
        """Get/set settings panel visibility."""
        return self._show_settings_panel
    
    @ShowSettingsPanel.setter
    def ShowSettingsPanel(self, value: bool):
        """Set settings panel visibility."""
        self._show_settings_panel = value
        if hasattr(self, 'settings_panel'):
            if value:
                self.settings_panel.Width = 300
                self._update_settings_display()
            else:
                self.settings_panel.Width = 0
        
        # Update button appearance if it exists
        if hasattr(self, 'btn_settings'):
            if value:
                self.btn_settings.BackColor = '#e0e0e0'
            else:
                self.btn_settings.BackColor = '#ffffff'
    
    def get_page_setup_settings(self) -> dict:
                self.settings_panel.Width = 0
    
    def get_page_setup_settings(self) -> dict:
        """Get current page setup settings."""
        return self.page_setup_settings.copy()
    
    def get_print_settings(self) -> dict:
        """Get current print settings."""
        return self.print_settings.copy()
    
    def set_page_setup_settings(self, settings: dict):
        """
        Set page setup settings.
        
        Args:
            settings: Dictionary with keys: paper_size, orientation, 
                     margin_left, margin_right, margin_top, margin_bottom
        """
        self.page_setup_settings.update(settings)
        self._update_settings_display()
    
    def set_print_settings(self, settings: dict):
        """
        Set print settings.
        
        Args:
            settings: Dictionary with keys: printer_name, copies, print_range,
                     from_page, to_page, collate, document_name
        """
        self.print_settings.update(settings)
        self._update_settings_display()

    
    def load_document(self, file_path: str, backend: DocumentBackend = None) -> bool:
        """
        Load a document file.
        
        Args:
            file_path: Path to the document
            backend: Optional specific backend to use
            
        Returns:
            True if loaded successfully
        """
        # Auto-detect backend if not provided
        if backend is None:
            backend = self._detect_backend(file_path)
        
        if backend is None:
            self.lbl_status.Text = "Unsupported file format"
            return False
        
        self.backend = backend
        
        # Load document
        if not self.backend.load_document(file_path):
            self.lbl_status.Text = f"Failed to load: {file_path}"
            return False
        
        # Update UI
        self.current_zoom = 100
        self.backend.current_page = 0
        self._render_current_page()
        self._update_page_info()
        self._update_navigation_state()
        
        self.lbl_status.Text = f"Loaded: {os.path.basename(file_path)} ({self.backend.page_count} pages)"
        
        # Trigger event
        if self.DocumentLoaded:
            self.DocumentLoaded(self, {'file_path': file_path})
        
        return True
    
    def _detect_backend(self, file_path: str) -> Optional[DocumentBackend]:
        """Auto-detect appropriate backend based on file extension."""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            return PDFBackend()
        elif ext in ['.docx', '.doc']:
            return WordBackend()
        elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            return ImageBackend()
        elif ext in ['.txt', '.md', '.log', '.py', '.json', '.xml']:
            return TextBackend()
        
        return None
    
    def _render_current_page(self):
        """Render the current page and display it."""
        if not self.backend or not self.backend.document_loaded:
            return
        
        # Calculate target size based on zoom
        base_width = 600
        target_width = int(base_width * self.current_zoom / 100)
        
        # Render page
        img = self.backend.render_page(
            self.backend.current_page,
            width=target_width
        )
        
        # Convert PIL Image to PhotoImage and display
        self.picture_box.Image = img
        
        # Update picture box size
        self.picture_box.Width = img.width
        self.picture_box.Height = img.height
    
    def _update_page_info(self):
        """Update page information label."""
        if self.backend and self.backend.document_loaded:
            current = self.backend.current_page + 1
            total = self.backend.page_count
            self.lbl_page.Text = f"Page: {current} / {total}"
        else:
            self.lbl_page.Text = "Page: -"
    
    def _update_navigation_state(self):
        """Enable/disable navigation buttons based on state."""
        has_doc = self.backend and self.backend.document_loaded
        
        self.btn_first.Enabled = has_doc and self.backend.current_page > 0
        self.btn_prev.Enabled = has_doc and self.backend.current_page > 0
        self.btn_next.Enabled = has_doc and self.backend.current_page < self.backend.page_count - 1
        self.btn_last.Enabled = has_doc and self.backend.current_page < self.backend.page_count - 1
        
        self.btn_zoom_in.Enabled = has_doc
        self.btn_zoom_out.Enabled = has_doc
        self.btn_fit_width.Enabled = has_doc
    
    def next_page(self):
        """Go to next page."""
        if self.backend and self.backend.current_page < self.backend.page_count - 1:
            self.backend.current_page += 1
            self._render_current_page()
            self._update_page_info()
            self._update_navigation_state()
            
            if self.PageChanged:
                self.PageChanged(self, {'page': self.backend.current_page})
    
    def previous_page(self):
        """Go to previous page."""
        if self.backend and self.backend.current_page > 0:
            self.backend.current_page -= 1
            self._render_current_page()
            self._update_page_info()
            self._update_navigation_state()
            
            if self.PageChanged:
                self.PageChanged(self, {'page': self.backend.current_page})
    
    def go_to_first_page(self):
        """Go to first page."""
        if self.backend:
            self.backend.current_page = 0
            self._render_current_page()
            self._update_page_info()
            self._update_navigation_state()
            
            if self.PageChanged:
                self.PageChanged(self, {'page': 0})
    
    def go_to_last_page(self):
        """Go to last page."""
        if self.backend:
            self.backend.current_page = self.backend.page_count - 1
            self._render_current_page()
            self._update_page_info()
            self._update_navigation_state()
            
            if self.PageChanged:
                self.PageChanged(self, {'page': self.backend.current_page})
    
    def go_to_page(self, page_number: int):
        """Go to specific page (0-based)."""
        if self.backend and 0 <= page_number < self.backend.page_count:
            self.backend.current_page = page_number
            self._render_current_page()
            self._update_page_info()
            self._update_navigation_state()
            
            if self.PageChanged:
                self.PageChanged(self, {'page': page_number})
    
    def zoom_in(self):
        """Increase zoom level."""
        self.current_zoom = min(200, self.current_zoom + 25)
        self.lbl_zoom.Text = f"{self.current_zoom}%"
        self._render_current_page()
        
        if self.ZoomChanged:
            self.ZoomChanged(self, {'zoom': self.current_zoom})
    
    def zoom_out(self):
        """Decrease zoom level."""
        self.current_zoom = max(25, self.current_zoom - 25)
        self.lbl_zoom.Text = f"{self.current_zoom}%"
        self._render_current_page()
        
        if self.ZoomChanged:
            self.ZoomChanged(self, {'zoom': self.current_zoom})
    
    def set_zoom(self, zoom_percent: int):
        """Set specific zoom level."""
        self.current_zoom = max(25, min(200, zoom_percent))
        self.lbl_zoom.Text = f"{self.current_zoom}%"
        self._render_current_page()
        
        if self.ZoomChanged:
            self.ZoomChanged(self, {'zoom': self.current_zoom})
    
    def fit_to_width(self):
        """Fit document to panel width."""
        # This would calculate zoom based on panel width
        self.fit_mode = 'width'
        # For simplicity, set to 100%
        self.set_zoom(100)
    
    def get_current_page_text(self) -> str:
        """Get text content of current page."""
        if self.backend and self.backend.document_loaded:
            return self.backend.get_page_text(self.backend.current_page)
        return ""
    
    def get_document_info(self) -> dict:
        """Get document information."""
        if self.backend:
            return self.backend.get_document_info()
        return {}
    
    def close_document(self):
        """Close current document."""
        if self.backend:
            self.backend.close_document()
        
        self.picture_box.Image = None
        self.lbl_status.Text = "No document loaded"
        self._update_page_info()
        self._update_navigation_state()
    
    # Properties for controlling toolbar visibility
    
    @property
    def ShowToolbar(self) -> bool:
        """Get/set toolbar visibility."""
        return self._show_toolbar
    
    @ShowToolbar.setter
    def ShowToolbar(self, value: bool):
        """Set toolbar visibility."""
        self._show_toolbar = value
        self._update_toolbar_visibility()
    
    @property
    def ShowFileButtons(self) -> bool:
        """Get/set file buttons group visibility."""
        return self._show_file_buttons
    
    @ShowFileButtons.setter
    def ShowFileButtons(self, value: bool):
        """Set file buttons group visibility."""
        self._show_file_buttons = value
        self._update_toolbar_visibility()
    
    @property
    def ShowNavigationButtons(self) -> bool:
        """Get/set navigation buttons group visibility."""
        return self._show_navigation_buttons
    
    @ShowNavigationButtons.setter
    def ShowNavigationButtons(self, value: bool):
        """Set navigation buttons group visibility."""
        self._show_navigation_buttons = value
        self._update_toolbar_visibility()
    
    @property
    def ShowNavigationButtons(self) -> bool:
        """Get/set navigation buttons group visibility."""
        return self._show_navigation_buttons
    
    @ShowNavigationButtons.setter
    def ShowNavigationButtons(self, value: bool):
        """Set navigation buttons group visibility."""
        self._show_navigation_buttons = value
        self._update_toolbar_visibility()
    
    @property
    def ShowZoomButtons(self) -> bool:
        """Get/set zoom buttons group visibility."""
        return self._show_zoom_buttons
    
    @ShowZoomButtons.setter
    def ShowZoomButtons(self, value: bool):
        """Set zoom buttons group visibility."""
        self._show_zoom_buttons = value
        self._update_toolbar_visibility()
    
    @property
    def ShowViewButtons(self) -> bool:
        """Get/set view buttons group visibility."""
        return self._show_view_buttons
    
    @ShowViewButtons.setter
    def ShowViewButtons(self, value: bool):
        """Set view buttons group visibility."""
        self._show_view_buttons = value
        self._update_toolbar_visibility()
    
    def _update_toolbar_visibility(self):
        """Update visibility of toolbar and button groups."""
        # Hide/show entire toolbar
        if hasattr(self, 'toolbar'):
            if self._show_toolbar:
                self.toolbar.Height = 45
            else:
                self.toolbar.Height = 0
        
        # Document operation buttons group
        if hasattr(self, 'btn_printer_setup'):
            visible = self._show_toolbar and self._show_document_buttons
            self.btn_printer_setup.Visible = visible
            self.btn_page_setup.Visible = visible
            self.btn_print.Visible = visible
            self._sep_doc.Visible = visible
        
        # Navigation buttons group
        if hasattr(self, 'btn_first'):
            visible = self._show_toolbar and self._show_navigation_buttons
            self.btn_first.Visible = visible
            self.btn_prev.Visible = visible
            self.lbl_page.Visible = visible
            self.btn_next.Visible = visible
            self.btn_last.Visible = visible
            self._sep_nav.Visible = visible
        
        # Zoom buttons group
        if hasattr(self, 'btn_zoom_out'):
            visible = self._show_toolbar and self._show_zoom_buttons
            self.btn_zoom_out.Visible = visible
            self.lbl_zoom.Visible = visible
            self.btn_zoom_in.Visible = visible
            self._sep_zoom.Visible = visible
        
        # View buttons group
        if hasattr(self, 'btn_fit_width'):
            visible = self._show_toolbar and self._show_view_buttons
            self.btn_fit_width.Visible = visible
            self.btn_extract_text.Visible = visible
            self._sep_view.Visible = visible
            self.btn_settings.Visible = visible
    
    def _toggle_settings_panel(self):
        """Toggle settings panel visibility."""
        self.ShowSettingsPanel = not self.ShowSettingsPanel
        
        # Update button appearance
        if hasattr(self, 'btn_settings'):
            if self.ShowSettingsPanel:
                self.btn_settings.BackColor = '#e0e0e0'  # Pressed state
            else:
                self.btn_settings.BackColor = '#ffffff'  # Normal state
    
    def _show_page_text(self):
        """Show current page text in a dialog."""
        if not self.backend or not self.backend.document_loaded:
            return
        
        text = self.backend.get_page_text(self.backend.current_page)
        
        from winformpy.winformpy import MessageBox
        MessageBox.Show(
            text if text else "No text found on this page",
            f"Page {self.backend.current_page + 1} Text",
            "OK",
            "Information"
        )
    
    def _show_printer_setup(self):
        """Show printer setup dialog and save settings."""
        import tkinter as tk
        from tkinter import ttk
        from winformpy.winformpy import MessageBox
        
        # Create custom printer setup dialog
        dialog = tk.Toplevel()
        dialog.title("Printer Setup")
        dialog.geometry("500x450")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Result container
        result = {'status': 'Cancel'}
        
        # --- Printer Selection ---
        frame_printer = tk.LabelFrame(dialog, text="Printer", padx=10, pady=10)
        frame_printer.pack(fill='x', padx=10, pady=10)
        
        tk.Label(frame_printer, text="Name:").grid(row=0, column=0, sticky='w', pady=5)
        
        # Get installed printers from PrinterSettings
        printers = PrinterSettings.GetInstalledPrinters()
        cbo_printer = ttk.Combobox(frame_printer, values=printers, state="readonly", width=40)
        cbo_printer.set(self.PrinterSettings.PrinterName)
        cbo_printer.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        # --- Paper Settings ---
        frame_paper = tk.LabelFrame(dialog, text="Paper", padx=10, pady=10)
        frame_paper.pack(fill='x', padx=10, pady=10)
        
        tk.Label(frame_paper, text="Size:").grid(row=0, column=0, sticky='w', pady=5)
        paper_sizes = ["Letter", "A4", "A3", "Legal", "Tabloid"]
        cbo_paper = ttk.Combobox(frame_paper, values=paper_sizes, state="readonly", width=20)
        cbo_paper.set(self.PrinterSettings.PaperSize)
        cbo_paper.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        
        tk.Label(frame_paper, text="Orientation:").grid(row=1, column=0, sticky='w', pady=5)
        orientation_var = tk.StringVar(value="Landscape" if self.PrinterSettings.Landscape else "Portrait")
        tk.Radiobutton(frame_paper, text="Portrait", variable=orientation_var, value="Portrait").grid(row=1, column=1, sticky='w', padx=5)
        tk.Radiobutton(frame_paper, text="Landscape", variable=orientation_var, value="Landscape").grid(row=1, column=2, sticky='w', padx=5)
        
        # --- Print Quality ---
        frame_quality = tk.LabelFrame(dialog, text="Quality and Color", padx=10, pady=10)
        frame_quality.pack(fill='x', padx=10, pady=10)
        
        color_var = tk.BooleanVar(value=self.PrinterSettings.Color)
        tk.Checkbutton(frame_quality, text="Color (uncheck for Grayscale)", variable=color_var).grid(row=0, column=0, columnspan=2, sticky='w', pady=5)
        
        tk.Label(frame_quality, text="Duplex:").grid(row=1, column=0, sticky='w', pady=5)
        duplex_values = ["Simplex", "Horizontal", "Vertical"]
        cbo_duplex = ttk.Combobox(frame_quality, values=duplex_values, state="readonly", width=20)
        cbo_duplex.set(self.PrinterSettings.Duplex)
        cbo_duplex.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        # --- Buttons ---
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(fill='x', pady=10, padx=10)
        
        def on_ok():
            result['status'] = 'OK'
            
            # Update PrinterSettings object
            self.PrinterSettings.PrinterName = cbo_printer.get()
            self.PrinterSettings.PaperSize = cbo_paper.get()
            self.PrinterSettings.Landscape = (orientation_var.get() == "Landscape")
            self.PrinterSettings.Color = color_var.get()
            self.PrinterSettings.Duplex = cbo_duplex.get()
            
            # Update settings display if visible
            self._update_settings_display()
            dialog.destroy()
        
        def on_cancel():
            result['status'] = 'Cancel'
            dialog.destroy()
        
        tk.Button(btn_frame, text="OK", command=on_ok, width=10).pack(side='right', padx=5)
        tk.Button(btn_frame, text="Cancel", command=on_cancel, width=10).pack(side='right')
        
        # Wait for dialog
        dialog.wait_window()
        
        return result['status']
    
    def _show_page_setup(self):
        """Show page setup dialog and save settings."""
        from winformpy.winformpy import PageSetupDialog, MessageBox
        
        dialog = PageSetupDialog()
        
        # Load current settings
        dialog.PaperSize = self.page_setup_settings['paper_size']
        dialog.Landscape = self.page_setup_settings['orientation'] == 'Landscape'
        dialog.MarginLeft = self.page_setup_settings['margin_left']
        dialog.MarginRight = self.page_setup_settings['margin_right']
        dialog.MarginTop = self.page_setup_settings['margin_top']
        dialog.MarginBottom = self.page_setup_settings['margin_bottom']
        
        result = dialog.ShowDialog()
        
        if result == 'OK':
            # Save settings
            self.page_setup_settings['paper_size'] = dialog.PaperSize
            self.page_setup_settings['orientation'] = 'Landscape' if dialog.Landscape else 'Portrait'
            self.page_setup_settings['margin_left'] = dialog.MarginLeft
            self.page_setup_settings['margin_right'] = dialog.MarginRight
            self.page_setup_settings['margin_top'] = dialog.MarginTop
            self.page_setup_settings['margin_bottom'] = dialog.MarginBottom
            
            # Update settings display if visible
            self._update_settings_display()
            
            msg = "Page Setup:\n\n"
            msg += f"Paper Size: {dialog.PaperSize}\n"
            msg += f"Orientation: {self.page_setup_settings['orientation']}\n"
            msg += f"Margins: L={dialog.MarginLeft}, R={dialog.MarginRight}, "
            msg += f"T={dialog.MarginTop}, B={dialog.MarginBottom}"
            
            MessageBox.Show(msg, "Page Setup Applied", "OK", "Information")
    
    def _show_print_dialog(self):
        """Show print dialog and save settings."""
        from winformpy.winformpy import PrintDialog, MessageBox
        
        if not self.backend or not self.backend.document_loaded:
            MessageBox.Show(
                "No document loaded. Please open a document first.",
                "Print",
                "OK",
                "Warning"
            )
            return
        
        dialog = PrintDialog()
        
        # Set document name from backend
        if self.backend.file_path:
            dialog.DocumentName = os.path.basename(self.backend.file_path)
        else:
            dialog.DocumentName = self.print_settings['document_name']
        
        # Load current settings
        dialog.PrinterName = self.print_settings['printer_name']
        dialog.Copies = self.print_settings['copies']
        dialog.PrintRange = self.print_settings['print_range']
        dialog.FromPage = self.print_settings['from_page']
        dialog.ToPage = self.print_settings['to_page']
        dialog.Collate = self.print_settings['collate']
        
        result = dialog.ShowDialog()
        
        if result == 'OK':
            # Save settings
            self.print_settings['printer_name'] = dialog.PrinterName
            self.print_settings['document_name'] = dialog.DocumentName
            self.print_settings['copies'] = dialog.Copies
            self.print_settings['print_range'] = dialog.PrintRange
            self.print_settings['from_page'] = dialog.FromPage
            self.print_settings['to_page'] = dialog.ToPage
            self.print_settings['collate'] = dialog.Collate
            
            # Update settings display if visible
            self._update_settings_display()
            
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
                msg + "\nNote: Actual printing requires printer integration.",
                "Print Configuration",
                "OK",
                "Information"
            )


# Example usage when running this module directly
if __name__ == '__main__':
    from winformpy.winformpy import Form, Application, MessageBox, OpenFileDialog, Button, CheckBox
    
    class TestForm(Form):
        def __init__(self):
            super().__init__()
            self.Text = "Document Viewer Panel - Settings Example"
            self.Width = 1200
            self.Height = 700
            self.StartPosition = "CenterScreen"
            
            # Apply layout before adding controls
            self.ApplyLayout()
            
            # Create toolbar panel for open button and settings toggle
            toolbar = Panel(self, {
                'Dock': DockStyle.Top,
                'Height': 50,
                'BackColor': '#34495e'
            })
            
            # Open button
            btn_open = Button(toolbar, {
                'Text': '📂 Open Document',
                'Left': 10,
                'Top': 10,
                'Width': 150,
                'Height': 30,
                'BackColor': '#3498db',
                'ForeColor': 'white'
            })
            btn_open.Click = lambda s, e: self._open_document()
            
            # Create document viewer panel (with its own navigation/zoom toolbar)
            self.viewer_panel = DocumentViewerPanel(self, {'Dock': DockStyle.Fill})
            
            # Show instructions
            MessageBox.Show(
                "Document Viewer with Settings Panel\n\n"
                "1. Click 'Open Document' to load a file\n"
                "2. Click 'Settings' button in the viewer toolbar to show/hide settings\n"
                "3. Use Printer, Page Setup and Print buttons to configure\n"
                "4. Settings are saved and displayed in the right panel",
                "Document Viewer Panel",
                "OK",
                "Information"
            )
        
        def _open_document(self):
            """Open file dialog and load document."""
            dialog = OpenFileDialog()
            dialog.Filter = "All Supported|*.pdf;*.docx;*.doc;*.txt;*.md;*.jpg;*.png;*.gif;*.bmp|PDF Files|*.pdf|Word Documents|*.docx;*.doc|Images|*.jpg;*.png;*.gif;*.bmp|Text Files|*.txt;*.md|All Files|*.*"
            dialog.Title = "Open Document"
            
            if dialog.ShowDialog() == 'OK':
                try:
                    success = self.viewer_panel.load_document(dialog.FileName)
                    if not success:
                        MessageBox.Show(
                            "Failed to load document. Make sure you have the required libraries:\n\n"
                            "- pip install PyMuPDF (for PDFs)\n"
                            "- pip install python-docx (for Word documents)",
                            "Error",
                            "OK",
                            "Error"
                        )
                except Exception as ex:
                    MessageBox.Show(f"Error loading document: {str(ex)}", "Error", "OK", "Error")
    
    # Run the application
    form = TestForm()
    Application.Run(form)
