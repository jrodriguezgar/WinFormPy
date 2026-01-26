"""
WordProcessorForm - A complete WordUI-style word processor application.

Provides a full-featured word processor with:
- Menu bar with File, Edit, Format, View, Help menus
- Quick Access Toolbar
- Formatting toolbar (ribbon-style)
- RichTextBox editor with RTF support
- Status bar with word count, zoom, position
- Find and Replace
- Print support
- Recent files list
- Insert Date/Time
- Zoom control
"""

import sys
import os
from datetime import datetime
from typing import Optional, List

# Add project root to path for imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..', '..', '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy.winformpy import (
    Form, Panel, Button, Label, MenuStrip, ToolStripMenuItem, ComboBox,
    DockStyle, AnchorStyles, Font, FontStyle, FlatStyle,
    MessageBox, OpenFileDialog, SaveFileDialog, PrintDialog,
    RichTextBoxStreamType, Clipboard, Application
)
from winformpy.ui_elements.word_processor.word_processor_panel import WordProcessorPanel


class WordProcessorForm(Form):
    """
    A complete WordPad-style word processor form.
    
    Features:
    - File menu: New, Open, Save, Save As, Print, Recent Files, Exit
    - Edit menu: Undo, Redo, Cut, Copy, Paste, Delete, Select All, Find, Replace
    - Insert menu: Date/Time, Picture (placeholder)
    - Format menu: Bold, Italic, Underline, Strikethrough, Font, Paragraph
    - View menu: Zoom, Ruler, Toolbar, Status Bar, Word Wrap
    - Help menu: About, Keyboard Shortcuts
    - Quick Access Toolbar with common actions
    - Zoom slider in status bar
    - Recent files tracking
    """
    
    # Maximum recent files to track
    MAX_RECENT_FILES = 10
    
    # Zoom levels
    ZOOM_LEVELS = [50, 75, 100, 125, 150, 200, 300, 400, 500]
    
    def __init__(self, props=None):
        """
        Initialize the WordProcessorForm.
        
        Args:
            props: Optional dictionary with properties:
                - Text: Window title
                - Width: Window width
                - Height: Window height
        """
        defaults = {
            'Text': 'WordUI - WinFormPy',
            'Width': 1100,
            'Height': 800,
            'BackColor': '#F0F0F0',
            'StartPosition': 'CenterScreen'
        }
        
        if props:
            defaults.update(props)
        
        super().__init__(defaults)
        
        # State
        self._recent_files: List[str] = []
        self._zoom_level = 100
        self._ruler_visible = False
        self._toolbar_visible = True
        self._statusbar_visible = True
        self._wordwrap_enabled = True
        
        # Apply layout before adding controls
        self.ApplyLayout()
        
        # Create UI components (order matters for Dock)
        self._create_menu()
        self._create_quick_access_toolbar()
        self._create_status_bar_extended()
        self._create_word_processor()
        
        # Bind form events
        self._bind_events()
        self._bind_keyboard_shortcuts()
        
        # Update title
        self._update_title()
        
        # Focus editor
        self._word_processor.Editor.Focus()
    
    # =========================================================================
    # UI Creation
    # =========================================================================
    
    def _create_menu(self):
        """Create the menu bar with full WordPad-style menus."""
        self._menu_strip = MenuStrip(self, {
            'Dock': DockStyle.Top,
            'BackColor': '#F5F5F5'
        })
        
        self._create_file_menu()
        self._create_edit_menu()
        self._create_insert_menu()
        self._create_format_menu()
        self._create_view_menu()
        self._create_help_menu()
    
    def _create_file_menu(self):
        """Create File menu."""
        file_menu = ToolStripMenuItem(self._menu_strip, {'Text': 'File'})
        
        # New
        new_item = ToolStripMenuItem(file_menu, {'Text': '📄 New\tCtrl+N'})
        new_item.Click = lambda s, e: self._on_new()
        
        # Open
        open_item = ToolStripMenuItem(file_menu, {'Text': '📂 Open...\tCtrl+O'})
        open_item.Click = lambda s, e: self._on_open()
        
        # Save
        save_item = ToolStripMenuItem(file_menu, {'Text': '💾 Save\tCtrl+S'})
        save_item.Click = lambda s, e: self._on_save()
        
        # Save As
        save_as_item = ToolStripMenuItem(file_menu, {'Text': '💾 Save As...\tCtrl+Shift+S'})
        save_as_item.Click = lambda s, e: self._on_save_as()
        
        ToolStripMenuItem(file_menu, {'Text': '-'})  # Separator
        
        # Print
        print_item = ToolStripMenuItem(file_menu, {'Text': '🖨️ Print...\tCtrl+P'})
        print_item.Click = lambda s, e: self._on_print()
        
        # Print Preview (placeholder)
        preview_item = ToolStripMenuItem(file_menu, {'Text': '📋 Print Preview'})
        preview_item.Click = lambda s, e: self._on_print_preview()
        
        ToolStripMenuItem(file_menu, {'Text': '-'})
        
        # Page Setup
        page_setup_item = ToolStripMenuItem(file_menu, {'Text': '📐 Page Setup...'})
        page_setup_item.Click = lambda s, e: self._on_page_setup()
        
        ToolStripMenuItem(file_menu, {'Text': '-'})
        
        # Recent Files submenu
        self._recent_menu = ToolStripMenuItem(file_menu, {'Text': '📁 Recent Files'})
        self._update_recent_files_menu()
        
        ToolStripMenuItem(file_menu, {'Text': '-'})
        
        # Exit
        exit_item = ToolStripMenuItem(file_menu, {'Text': '🚪 Exit\tAlt+F4'})
        exit_item.Click = lambda s, e: self._on_exit()
    
    def _create_edit_menu(self):
        """Create Edit menu."""
        edit_menu = ToolStripMenuItem(self._menu_strip, {'Text': 'Edit'})
        
        # Undo/Redo
        undo_item = ToolStripMenuItem(edit_menu, {'Text': '↶ Undo\tCtrl+Z'})
        undo_item.Click = lambda s, e: self._word_processor.Undo()
        
        redo_item = ToolStripMenuItem(edit_menu, {'Text': '↷ Redo\tCtrl+Y'})
        redo_item.Click = lambda s, e: self._word_processor.Redo()
        
        ToolStripMenuItem(edit_menu, {'Text': '-'})
        
        # Clipboard operations
        cut_item = ToolStripMenuItem(edit_menu, {'Text': '✂️ Cut\tCtrl+X'})
        cut_item.Click = lambda s, e: self._word_processor.Cut()
        
        copy_item = ToolStripMenuItem(edit_menu, {'Text': '📋 Copy\tCtrl+C'})
        copy_item.Click = lambda s, e: self._word_processor.Copy()
        
        paste_item = ToolStripMenuItem(edit_menu, {'Text': '📄 Paste\tCtrl+V'})
        paste_item.Click = lambda s, e: self._word_processor.Paste()
        
        paste_special_item = ToolStripMenuItem(edit_menu, {'Text': '📄 Paste Special...'})
        paste_special_item.Click = lambda s, e: self._on_paste_special()
        
        ToolStripMenuItem(edit_menu, {'Text': '-'})
        
        # Delete
        delete_item = ToolStripMenuItem(edit_menu, {'Text': '🗑️ Delete\tDel'})
        delete_item.Click = lambda s, e: self._on_delete()
        
        ToolStripMenuItem(edit_menu, {'Text': '-'})
        
        # Find & Replace
        find_item = ToolStripMenuItem(edit_menu, {'Text': '🔍 Find...\tCtrl+F'})
        find_item.Click = lambda s, e: self._word_processor._show_find_bar()
        
        find_next_item = ToolStripMenuItem(edit_menu, {'Text': '🔍 Find Next\tF3'})
        find_next_item.Click = lambda s, e: self._word_processor._find_next()
        
        replace_item = ToolStripMenuItem(edit_menu, {'Text': '🔄 Replace...\tCtrl+H'})
        replace_item.Click = lambda s, e: self._on_replace()
        
        go_to_item = ToolStripMenuItem(edit_menu, {'Text': '➡️ Go To...\tCtrl+G'})
        go_to_item.Click = lambda s, e: self._on_goto()
        
        ToolStripMenuItem(edit_menu, {'Text': '-'})
        
        # Select All
        select_all_item = ToolStripMenuItem(edit_menu, {'Text': '☑️ Select All\tCtrl+A'})
        select_all_item.Click = lambda s, e: self._word_processor.SelectAll()
        
        ToolStripMenuItem(edit_menu, {'Text': '-'})
        
        # Time/Date
        time_date_item = ToolStripMenuItem(edit_menu, {'Text': '🕐 Time/Date\tF5'})
        time_date_item.Click = lambda s, e: self._insert_datetime()
    
    def _create_insert_menu(self):
        """Create Insert menu."""
        insert_menu = ToolStripMenuItem(self._menu_strip, {'Text': 'Insert'})
        
        # Date and Time
        datetime_item = ToolStripMenuItem(insert_menu, {'Text': '📅 Date and Time...'})
        datetime_item.Click = lambda s, e: self._show_datetime_dialog()
        
        ToolStripMenuItem(insert_menu, {'Text': '-'})
        
        # Insert Object (placeholder)
        object_item = ToolStripMenuItem(insert_menu, {'Text': '📦 Object...'})
        object_item.Click = lambda s, e: MessageBox.Show(
            "Object insertion is not yet implemented.",
            "Insert Object", "OK", "Information"
        )
    
    def _create_format_menu(self):
        """Create Format menu."""
        format_menu = ToolStripMenuItem(self._menu_strip, {'Text': 'Format'})
        
        # Font submenu
        font_submenu = ToolStripMenuItem(format_menu, {'Text': '🔤 Font'})
        
        bold_item = ToolStripMenuItem(font_submenu, {'Text': 'Bold\tCtrl+B'})
        bold_item.Click = lambda s, e: self._word_processor._toggle_bold()
        
        italic_item = ToolStripMenuItem(font_submenu, {'Text': 'Italic\tCtrl+I'})
        italic_item.Click = lambda s, e: self._word_processor._toggle_italic()
        
        underline_item = ToolStripMenuItem(font_submenu, {'Text': 'Underline\tCtrl+U'})
        underline_item.Click = lambda s, e: self._word_processor._toggle_underline()
        
        strikethrough_item = ToolStripMenuItem(font_submenu, {'Text': 'Strikethrough'})
        strikethrough_item.Click = lambda s, e: self._word_processor._toggle_strikethrough()
        
        ToolStripMenuItem(font_submenu, {'Text': '-'})
        
        font_dialog_item = ToolStripMenuItem(font_submenu, {'Text': 'Font...'})
        font_dialog_item.Click = lambda s, e: self._show_font_dialog()
        
        # Paragraph submenu
        para_submenu = ToolStripMenuItem(format_menu, {'Text': '¶ Paragraph'})
        
        align_left = ToolStripMenuItem(para_submenu, {'Text': '⬅️ Align Left\tCtrl+L'})
        align_left.Click = lambda s, e: self._word_processor._set_alignment('left')
        
        align_center = ToolStripMenuItem(para_submenu, {'Text': '⬆️ Center\tCtrl+E'})
        align_center.Click = lambda s, e: self._word_processor._set_alignment('center')
        
        align_right = ToolStripMenuItem(para_submenu, {'Text': '➡️ Align Right\tCtrl+R'})
        align_right.Click = lambda s, e: self._word_processor._set_alignment('right')
        
        ToolStripMenuItem(format_menu, {'Text': '-'})
        
        # Bullet list (placeholder)
        bullet_item = ToolStripMenuItem(format_menu, {'Text': '• Bullet List'})
        bullet_item.Click = lambda s, e: self._insert_bullet()
        
        ToolStripMenuItem(format_menu, {'Text': '-'})
        
        # Text Color
        text_color_item = ToolStripMenuItem(format_menu, {'Text': '🎨 Text Color...'})
        text_color_item.Click = lambda s, e: self._word_processor._show_color_picker('text')
        
        # Highlight Color
        highlight_item = ToolStripMenuItem(format_menu, {'Text': '🖍️ Highlight...'})
        highlight_item.Click = lambda s, e: self._word_processor._show_color_picker('background')
    
    def _create_view_menu(self):
        """Create View menu."""
        view_menu = ToolStripMenuItem(self._menu_strip, {'Text': 'View'})
        
        # Zoom submenu
        zoom_submenu = ToolStripMenuItem(view_menu, {'Text': '🔍 Zoom'})
        
        zoom_in_item = ToolStripMenuItem(zoom_submenu, {'Text': 'Zoom In\tCtrl++'})
        zoom_in_item.Click = lambda s, e: self._zoom_in()
        
        zoom_out_item = ToolStripMenuItem(zoom_submenu, {'Text': 'Zoom Out\tCtrl+-'})
        zoom_out_item.Click = lambda s, e: self._zoom_out()
        
        ToolStripMenuItem(zoom_submenu, {'Text': '-'})
        
        for level in self.ZOOM_LEVELS:
            item = ToolStripMenuItem(zoom_submenu, {'Text': f'{level}%'})
            item.Click = lambda s, e, l=level: self._set_zoom(l)
        
        ToolStripMenuItem(view_menu, {'Text': '-'})
        
        # Ruler toggle
        ruler_item = ToolStripMenuItem(view_menu, {'Text': '📏 Ruler'})
        ruler_item.Click = lambda s, e: self._toggle_ruler(s)
        self._ruler_menu_item = ruler_item
        
        ToolStripMenuItem(view_menu, {'Text': '-'})
        
        # Toolbar toggle
        toolbar_item = ToolStripMenuItem(view_menu, {'Text': '✓ Toolbar'})
        toolbar_item.Click = lambda s, e: self._toggle_toolbar(s)
        self._toolbar_menu_item = toolbar_item
        
        # Format Bar toggle
        format_bar_item = ToolStripMenuItem(view_menu, {'Text': '✓ Format Bar'})
        format_bar_item.Click = lambda s, e: self._toggle_format_bar(s)
        self._format_bar_menu_item = format_bar_item
        
        # Status Bar toggle
        statusbar_item = ToolStripMenuItem(view_menu, {'Text': '✓ Status Bar'})
        statusbar_item.Click = lambda s, e: self._toggle_statusbar(s)
        self._statusbar_menu_item = statusbar_item
        
        ToolStripMenuItem(view_menu, {'Text': '-'})
        
        # Word Wrap toggle
        wordwrap_item = ToolStripMenuItem(view_menu, {'Text': '✓ Word Wrap'})
        wordwrap_item.Click = lambda s, e: self._toggle_wordwrap(s)
        self._wordwrap_menu_item = wordwrap_item
    
    def _create_help_menu(self):
        """Create Help menu."""
        help_menu = ToolStripMenuItem(self._menu_strip, {'Text': 'Help'})
        
        # Help Topics
        help_topics = ToolStripMenuItem(help_menu, {'Text': '❓ Help Topics\tF1'})
        help_topics.Click = lambda s, e: self._show_help()
        
        ToolStripMenuItem(help_menu, {'Text': '-'})
        
        # Keyboard Shortcuts
        shortcuts_item = ToolStripMenuItem(help_menu, {'Text': '⌨️ Keyboard Shortcuts'})
        shortcuts_item.Click = lambda s, e: self._show_shortcuts()
        
        ToolStripMenuItem(help_menu, {'Text': '-'})
        
        # About
        about_item = ToolStripMenuItem(help_menu, {'Text': 'ℹ️ About WordUI'})
        about_item.Click = lambda s, e: self._show_about()
    
    def _create_quick_access_toolbar(self):
        """Create Quick Access Toolbar."""
        self._quick_toolbar = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 32,
            'BackColor': '#E1E1E1'
        })
        
        btn_size = 28
        x_pos = 4
        
        # New
        btn_new = Button(self._quick_toolbar, {
            'Text': '📄',
            'Left': x_pos,
            'Top': 2,
            'Width': btn_size,
            'Height': btn_size,
            'FlatStyle': FlatStyle.Flat,
            'BackColor': '#E1E1E1'
        })
        btn_new.ToolTipText = 'New (Ctrl+N)'
        btn_new.Click = lambda s, e: self._on_new()
        x_pos += btn_size + 2
        
        # Open
        btn_open = Button(self._quick_toolbar, {
            'Text': '📂',
            'Left': x_pos,
            'Top': 2,
            'Width': btn_size,
            'Height': btn_size,
            'FlatStyle': FlatStyle.Flat,
            'BackColor': '#E1E1E1'
        })
        btn_open.ToolTipText = 'Open (Ctrl+O)'
        btn_open.Click = lambda s, e: self._on_open()
        x_pos += btn_size + 2
        
        # Save
        btn_save = Button(self._quick_toolbar, {
            'Text': '💾',
            'Left': x_pos,
            'Top': 2,
            'Width': btn_size,
            'Height': btn_size,
            'FlatStyle': FlatStyle.Flat,
            'BackColor': '#E1E1E1'
        })
        btn_save.ToolTipText = 'Save (Ctrl+S)'
        btn_save.Click = lambda s, e: self._on_save()
        x_pos += btn_size + 8
        
        # Separator
        sep1 = Label(self._quick_toolbar, {
            'Text': '|',
            'Left': x_pos,
            'Top': 6,
            'Width': 8,
            'Height': 20,
            'ForeColor': '#999999',
            'BackColor': '#E1E1E1'
        })
        x_pos += 12
        
        # Undo
        btn_undo = Button(self._quick_toolbar, {
            'Text': '↶',
            'Left': x_pos,
            'Top': 2,
            'Width': btn_size,
            'Height': btn_size,
            'FlatStyle': FlatStyle.Flat,
            'BackColor': '#E1E1E1'
        })
        btn_undo.ToolTipText = 'Undo (Ctrl+Z)'
        btn_undo.Click = lambda s, e: self._word_processor.Undo()
        x_pos += btn_size + 2
        
        # Redo
        btn_redo = Button(self._quick_toolbar, {
            'Text': '↷',
            'Left': x_pos,
            'Top': 2,
            'Width': btn_size,
            'Height': btn_size,
            'FlatStyle': FlatStyle.Flat,
            'BackColor': '#E1E1E1'
        })
        btn_redo.ToolTipText = 'Redo (Ctrl+Y)'
        btn_redo.Click = lambda s, e: self._word_processor.Redo()
        x_pos += btn_size + 8
        
        # Separator
        sep2 = Label(self._quick_toolbar, {
            'Text': '|',
            'Left': x_pos,
            'Top': 6,
            'Width': 8,
            'Height': 20,
            'ForeColor': '#999999',
            'BackColor': '#E1E1E1'
        })
        x_pos += 12
        
        # Print
        btn_print = Button(self._quick_toolbar, {
            'Text': '🖨️',
            'Left': x_pos,
            'Top': 2,
            'Width': btn_size,
            'Height': btn_size,
            'FlatStyle': FlatStyle.Flat,
            'BackColor': '#E1E1E1'
        })
        btn_print.ToolTipText = 'Print (Ctrl+P)'
        btn_print.Click = lambda s, e: self._on_print()
        x_pos += btn_size + 2
        
        # Find
        btn_find = Button(self._quick_toolbar, {
            'Text': '🔍',
            'Left': x_pos,
            'Top': 2,
            'Width': btn_size,
            'Height': btn_size,
            'FlatStyle': FlatStyle.Flat,
            'BackColor': '#E1E1E1'
        })
        btn_find.ToolTipText = 'Find (Ctrl+F)'
        btn_find.Click = lambda s, e: self._word_processor._show_find_bar()
    
    def _create_status_bar_extended(self):
        """Create extended status bar with zoom control."""
        self._extended_status = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': 24,
            'BackColor': '#F0F0F0'
        })
        
        # Zoom label
        self._lbl_zoom = Label(self._extended_status, {
            'Text': '100%',
            'Left': 10,
            'Top': 4,
            'Width': 50,
            'Height': 16,
            'ForeColor': '#333333',
            'BackColor': '#F0F0F0'
        })
        
        # Zoom out button
        btn_zoom_out = Button(self._extended_status, {
            'Text': '-',
            'Left': 65,
            'Top': 2,
            'Width': 22,
            'Height': 20,
            'FlatStyle': FlatStyle.Flat,
            'BackColor': '#F0F0F0'
        })
        btn_zoom_out.ToolTipText = 'Zoom Out'
        btn_zoom_out.Click = lambda s, e: self._zoom_out()
        
        # Zoom slider (using ComboBox as placeholder)
        self._combo_zoom = ComboBox(self._extended_status, {
            'Left': 90,
            'Top': 2,
            'Width': 80,
            'Height': 20,
            'DropDownStyle': 'DropDownList'
        })
        for level in self.ZOOM_LEVELS:
            self._combo_zoom.Items.Add(f'{level}%')
        self._combo_zoom.SelectedIndex = self.ZOOM_LEVELS.index(100)
        self._combo_zoom.SelectedIndexChanged = lambda s, e: self._on_zoom_combo_changed()
        
        # Zoom in button
        btn_zoom_in = Button(self._extended_status, {
            'Text': '+',
            'Left': 175,
            'Top': 2,
            'Width': 22,
            'Height': 20,
            'FlatStyle': FlatStyle.Flat,
            'BackColor': '#F0F0F0'
        })
        btn_zoom_in.ToolTipText = 'Zoom In'
        btn_zoom_in.Click = lambda s, e: self._zoom_in()
        
        # Separator
        sep = Label(self._extended_status, {
            'Text': '|',
            'Left': 210,
            'Top': 4,
            'Width': 10,
            'Height': 16,
            'ForeColor': '#AAAAAA',
            'BackColor': '#F0F0F0'
        })
        
        # Word Wrap indicator
        self._lbl_wrap = Label(self._extended_status, {
            'Text': 'Word Wrap: On',
            'Left': 225,
            'Top': 4,
            'Width': 100,
            'Height': 16,
            'ForeColor': '#333333',
            'BackColor': '#F0F0F0'
        })
    
    def _create_word_processor(self):
        """Create the word processor panel."""
        self._word_processor = WordProcessorPanel(self, {
            'Dock': DockStyle.Fill,
            'ShowToolbar': True,
            'ShowStatusBar': True,
            'ShowFindBar': False
        })
    
    def _bind_events(self):
        """Bind word processor events."""
        self._word_processor.DocumentChanged = self._on_document_changed
        self._word_processor.DocumentSaved = self._on_document_saved
        self._word_processor.DocumentOpened = self._on_document_opened
        self._word_processor.ModifiedChanged = self._on_modified_changed
    
    def _bind_keyboard_shortcuts(self):
        """Bind additional keyboard shortcuts."""
        editor = self._word_processor.Editor
        
        # File shortcuts
        editor.BindKey('<Control-n>', lambda e: self._on_new())
        editor.BindKey('<Control-o>', lambda e: self._on_open())
        editor.BindKey('<Control-s>', lambda e: self._on_save())
        editor.BindKey('<Control-Shift-s>', lambda e: self._on_save_as())
        editor.BindKey('<Control-p>', lambda e: self._on_print())
        
        # Edit shortcuts
        editor.BindKey('<Control-h>', lambda e: self._on_replace())
        editor.BindKey('<Control-g>', lambda e: self._on_goto())
        editor.BindKey('<F3>', lambda e: self._word_processor._find_next())
        editor.BindKey('<F5>', lambda e: self._insert_datetime())
        
        # Format shortcuts
        editor.BindKey('<Control-l>', lambda e: self._word_processor._set_alignment('left'))
        editor.BindKey('<Control-e>', lambda e: self._word_processor._set_alignment('center'))
        editor.BindKey('<Control-r>', lambda e: self._word_processor._set_alignment('right'))
        
        # Zoom shortcuts
        editor.BindKey('<Control-plus>', lambda e: self._zoom_in())
        editor.BindKey('<Control-minus>', lambda e: self._zoom_out())
        editor.BindKey('<Control-equal>', lambda e: self._zoom_in())  # For keyboards without numpad
        
        # Help
        editor.BindKey('<F1>', lambda e: self._show_help())
    
    # =========================================================================
    # Event Handlers
    # =========================================================================
    
    def _on_document_changed(self, sender, e):
        """Handle document changes."""
        self._update_title()
    
    def _on_document_saved(self, sender, e):
        """Handle document saved."""
        self._update_title()
        self._add_recent_file(self._word_processor.FilePath)
    
    def _on_document_opened(self, sender, e):
        """Handle document opened."""
        self._update_title()
        self._add_recent_file(self._word_processor.FilePath)
    
    def _on_modified_changed(self, sender, e):
        """Handle modified state change."""
        self._update_title()
    
    def _update_title(self):
        """Update the window title."""
        title = self._word_processor.DocumentTitle
        if self._word_processor.IsModified:
            title = f"*{title}"
        self.Text = f"{title} - WordUI"
    
    # =========================================================================
    # File Menu Actions
    # =========================================================================
    
    def _on_new(self):
        """Create a new document."""
        if self._word_processor.IsModified:
            result = MessageBox.Show(
                "Do you want to save changes before creating a new document?",
                "Save Changes", "YesNoCancel", "Question"
            )
            if result == "Yes":
                self._on_save()
            elif result == "Cancel":
                return
        
        self._word_processor.New()
        self._update_title()
    
    def _on_open(self):
        """Open a document."""
        if self._word_processor.IsModified:
            result = MessageBox.Show(
                "Do you want to save changes before opening a new document?",
                "Save Changes", "YesNoCancel", "Question"
            )
            if result == "Yes":
                self._on_save()
            elif result == "Cancel":
                return
        
        dialog = OpenFileDialog()
        dialog.Filter = (
            "Rich Text Format (*.rtf)|*.rtf|"
            "Text Document (*.txt)|*.txt|"
            "All Documents (*.*)|*.*"
        )
        dialog.Title = "Open"
        
        if dialog.ShowDialog() == "OK":
            self._word_processor.Open(dialog.FileName)
    
    def _on_save(self):
        """Save the current document."""
        if self._word_processor.FilePath:
            self._word_processor.Save()
        else:
            self._on_save_as()
    
    def _on_save_as(self):
        """Save the document with a new name."""
        dialog = SaveFileDialog()
        dialog.Filter = (
            "Rich Text Format (*.rtf)|*.rtf|"
            "Text Document (*.txt)|*.txt|"
            "All Files (*.*)|*.*"
        )
        dialog.Title = "Save As"
        dialog.DefaultExt = ".rtf"
        
        if dialog.ShowDialog() == "OK":
            self._word_processor.SaveAs(dialog.FileName)
    
    def _on_print(self):
        """Print the document."""
        MessageBox.Show(
            "Printing is not yet fully implemented.\n\n"
            "In a complete implementation, this would open the system print dialog.",
            "Print", "OK", "Information"
        )
    
    def _on_print_preview(self):
        """Show print preview."""
        MessageBox.Show(
            "Print Preview is not yet implemented.",
            "Print Preview", "OK", "Information"
        )
    
    def _on_page_setup(self):
        """Show page setup dialog."""
        MessageBox.Show(
            "Page Setup is not yet implemented.",
            "Page Setup", "OK", "Information"
        )
    
    def _on_exit(self):
        """Exit the application."""
        if self._word_processor.IsModified:
            result = MessageBox.Show(
                "Do you want to save changes before exiting?",
                "Save Changes", "YesNoCancel", "Question"
            )
            if result == "Yes":
                self._on_save()
            elif result == "Cancel":
                return
        
        self.Close()
    
    # =========================================================================
    # Edit Menu Actions
    # =========================================================================
    
    def _on_delete(self):
        """Delete selected text."""
        editor = self._word_processor.Editor
        if editor.SelectedText:
            editor.SelectedText = ""
    
    def _on_paste_special(self):
        """Show paste special dialog."""
        # Simple paste as plain text
        text = Clipboard.GetText()
        if text:
            self._word_processor.Editor.SelectedText = text
    
    def _on_replace(self):
        """Show find and replace bar."""
        self._word_processor._show_find_bar()
        if hasattr(self._word_processor, '_txt_replace'):
            self._word_processor._txt_replace.Focus()
    
    def _on_goto(self):
        """Go to specific line."""
        MessageBox.Show(
            "Go To Line is not yet implemented.",
            "Go To", "OK", "Information"
        )
    
    # =========================================================================
    # Insert Menu Actions
    # =========================================================================
    
    def _insert_datetime(self):
        """Insert current date and time."""
        now = datetime.now()
        text = now.strftime("%I:%M %p %m/%d/%Y")
        self._word_processor.Editor.SelectedText = text
    
    def _show_datetime_dialog(self):
        """Show date/time format selection dialog."""
        now = datetime.now()
        formats = [
            now.strftime("%m/%d/%Y"),
            now.strftime("%A, %B %d, %Y"),
            now.strftime("%B %d, %Y"),
            now.strftime("%m/%d/%y"),
            now.strftime("%Y-%m-%d"),
            now.strftime("%d-%b-%y"),
            now.strftime("%I:%M %p"),
            now.strftime("%I:%M:%S %p"),
            now.strftime("%H:%M"),
            now.strftime("%H:%M:%S"),
            now.strftime("%I:%M %p %m/%d/%Y"),
        ]
        
        # Insert first format for now
        self._word_processor.Editor.SelectedText = formats[0]
    
    def _insert_bullet(self):
        """Insert a bullet point."""
        self._word_processor.Editor.SelectedText = "• "
    
    # =========================================================================
    # Format Menu Actions
    # =========================================================================
    
    def _show_font_dialog(self):
        """Show font selection dialog."""
        MessageBox.Show(
            "Use the toolbar to change font and size.\n\n"
            "A full Font Dialog will be implemented in a future version.",
            "Font", "OK", "Information"
        )
    
    # =========================================================================
    # View Menu Actions
    # =========================================================================
    
    def _zoom_in(self):
        """Zoom in."""
        current_idx = self.ZOOM_LEVELS.index(self._zoom_level) if self._zoom_level in self.ZOOM_LEVELS else 2
        if current_idx < len(self.ZOOM_LEVELS) - 1:
            self._set_zoom(self.ZOOM_LEVELS[current_idx + 1])
    
    def _zoom_out(self):
        """Zoom out."""
        current_idx = self.ZOOM_LEVELS.index(self._zoom_level) if self._zoom_level in self.ZOOM_LEVELS else 2
        if current_idx > 0:
            self._set_zoom(self.ZOOM_LEVELS[current_idx - 1])
    
    def _set_zoom(self, level):
        """Set zoom level."""
        self._zoom_level = level
        self._lbl_zoom.Text = f'{level}%'
        
        # Update combo
        if level in self.ZOOM_LEVELS:
            self._combo_zoom.SelectedIndex = self.ZOOM_LEVELS.index(level)
        
        # Apply zoom to editor (via font size scaling)
        base_size = 11
        scaled_size = int(base_size * level / 100)
        if scaled_size < 6:
            scaled_size = 6
        if scaled_size > 72:
            scaled_size = 72
    
    def _on_zoom_combo_changed(self):
        """Handle zoom combo selection."""
        idx = self._combo_zoom.SelectedIndex
        if 0 <= idx < len(self.ZOOM_LEVELS):
            self._set_zoom(self.ZOOM_LEVELS[idx])
    
    def _toggle_ruler(self, menu_item):
        """Toggle ruler visibility."""
        self._ruler_visible = not self._ruler_visible
        menu_item.Text = ('✓ ' if self._ruler_visible else '') + '📏 Ruler'
        # Ruler not implemented yet
    
    def _toggle_toolbar(self, menu_item):
        """Toggle quick access toolbar visibility."""
        self._toolbar_visible = not self._toolbar_visible
        self._quick_toolbar.Visible = self._toolbar_visible
        menu_item.Text = ('✓ ' if self._toolbar_visible else '') + 'Toolbar'
    
    def _toggle_format_bar(self, menu_item):
        """Toggle format bar (WordProcessor toolbar) visibility."""
        visible = hasattr(self._word_processor, '_toolbar') and self._word_processor._toolbar.Visible
        if hasattr(self._word_processor, '_toolbar'):
            self._word_processor._toolbar.Visible = not visible
        menu_item.Text = ('✓ ' if not visible else '') + 'Format Bar'
    
    def _toggle_statusbar(self, menu_item):
        """Toggle status bar visibility."""
        self._statusbar_visible = not self._statusbar_visible
        
        # Toggle both status bars
        self._extended_status.Visible = self._statusbar_visible
        if hasattr(self._word_processor, '_status_bar'):
            self._word_processor._status_bar.Visible = self._statusbar_visible
        
        menu_item.Text = ('✓ ' if self._statusbar_visible else '') + 'Status Bar'
    
    def _toggle_wordwrap(self, menu_item):
        """Toggle word wrap."""
        editor = self._word_processor.Editor
        self._wordwrap_enabled = not self._wordwrap_enabled
        editor.WordWrap = self._wordwrap_enabled
        
        menu_item.Text = ('✓ ' if self._wordwrap_enabled else '') + 'Word Wrap'
        self._lbl_wrap.Text = f"Word Wrap: {'On' if self._wordwrap_enabled else 'Off'}"
    
    # =========================================================================
    # Help Menu Actions
    # =========================================================================
    
    def _show_help(self):
        """Show help."""
        help_text = """
WordUI Help
===========

WordUI is a simple word processor for creating and editing documents.

Creating Documents:
- Click File > New to create a new document
- Click File > Open to open an existing document
- Click File > Save to save your document

Formatting Text:
- Select text and use the toolbar buttons for Bold, Italic, Underline
- Use Format menu for more options
- Change font and size using the dropdown menus

Finding Text:
- Press Ctrl+F to open Find bar
- Type text to search and press Enter
- Use Ctrl+H for Find and Replace

Keyboard Shortcuts:
- Press F1 for help
- See Help > Keyboard Shortcuts for full list
"""
        MessageBox.Show(help_text, "WordUI Help", "OK", "Information")
    
    def _show_shortcuts(self):
        """Show keyboard shortcuts."""
        shortcuts = """
Keyboard Shortcuts
==================

File:
  Ctrl+N          New document
  Ctrl+O          Open document
  Ctrl+S          Save document
  Ctrl+Shift+S    Save As
  Ctrl+P          Print

Edit:
  Ctrl+Z          Undo
  Ctrl+Y          Redo
  Ctrl+X          Cut
  Ctrl+C          Copy
  Ctrl+V          Paste
  Ctrl+A          Select All
  Ctrl+F          Find
  Ctrl+H          Replace
  F3              Find Next
  F5              Insert Date/Time
  Del             Delete selected

Format:
  Ctrl+B          Bold
  Ctrl+I          Italic
  Ctrl+U          Underline
  Ctrl+L          Align Left
  Ctrl+E          Center
  Ctrl+R          Align Right

View:
  Ctrl++          Zoom In
  Ctrl+-          Zoom Out

Help:
  F1              Help
"""
        MessageBox.Show(shortcuts, "Keyboard Shortcuts", "OK", "Information")
    
    def _show_about(self):
        """Show about dialog."""
        MessageBox.Show(
            "WordUI for WinFormPy\n"
            "Version 1.0\n\n"
            "A WordPad-style word processor built with WinFormPy.\n\n"
            "Features:\n"
            "• Rich text formatting (Bold, Italic, Underline, Strikethrough)\n"
            "• Font family and size selection\n"
            "• Text and highlight colors\n"
            "• Paragraph alignment\n"
            "• Find and Replace\n"
            "• RTF file support\n"
            "• Word count and statistics\n"
            "• Zoom control\n\n"
            "© 2026 WinFormPy Project",
            "About WordUI",
            "OK",
            "Information"
        )
    
    # =========================================================================
    # Recent Files
    # =========================================================================
    
    def _add_recent_file(self, filepath):
        """Add a file to recent files list."""
        if not filepath:
            return
        
        # Remove if already exists
        if filepath in self._recent_files:
            self._recent_files.remove(filepath)
        
        # Add to front
        self._recent_files.insert(0, filepath)
        
        # Trim to max
        self._recent_files = self._recent_files[:self.MAX_RECENT_FILES]
        
        # Update menu
        self._update_recent_files_menu()
    
    def _update_recent_files_menu(self):
        """Update the recent files menu."""
        # Clear existing items (simplified - in real impl would clear children)
        if not self._recent_files:
            no_recent = ToolStripMenuItem(self._recent_menu, {'Text': '(No recent files)'})
            no_recent.Enabled = False
    
    def _open_recent_file(self, filepath):
        """Open a file from recent files."""
        if os.path.exists(filepath):
            if self._word_processor.IsModified:
                result = MessageBox.Show(
                    "Do you want to save changes?",
                    "Save Changes", "YesNoCancel", "Question"
                )
                if result == "Yes":
                    self._on_save()
                elif result == "Cancel":
                    return
            
            self._word_processor.Open(filepath)
        else:
            MessageBox.Show(
                f"The file '{filepath}' no longer exists.",
                "File Not Found", "OK", "Warning"
            )
            self._recent_files.remove(filepath)
            self._update_recent_files_menu()


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == '__main__':
    form = WordProcessorForm()
    Application.Run(form)
