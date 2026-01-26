"""
WordProcessorPanel - A complete word processor component for WinFormPy.

Provides a rich text editor with formatting toolbar, find/replace dialog,
and standard word processing features.

Features:
    - Rich text editing with RichTextBox
    - Formatting toolbar (Bold, Italic, Underline, Colors, Fonts)
    - Find and Replace functionality
    - File operations (New, Open, Save, Save As)
    - Undo/Redo support
    - Word count and status bar

Architecture:
    ┌─────────────────────────────────────────┐
    │           WordProcessorPanel            │
    ├─────────────────────────────────────────┤
    │ ┌─────────────────────────────────────┐ │
    │ │         Formatting Toolbar          │ │
    │ │ [B][I][U] | Font | Size | Colors    │ │
    │ └─────────────────────────────────────┘ │
    │ ┌─────────────────────────────────────┐ │
    │ │                                     │ │
    │ │           RichTextBox               │ │
    │ │         (Editor Area)               │ │
    │ │                                     │ │
    │ └─────────────────────────────────────┘ │
    │ ┌─────────────────────────────────────┐ │
    │ │ Status Bar: Word Count | Line | Col │ │
    │ └─────────────────────────────────────┘ │
    └─────────────────────────────────────────┘
"""

import sys
import os
from typing import Optional, Callable
from datetime import datetime

# Add project root to path for imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..', '..', '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy.winformpy import (
    Panel, Label, Button, TextBox, RichTextBox, ComboBox,
    DockStyle, AnchorStyles, Color,
    Font, FontStyle, Form,
    RichTextBoxStreamType, RichTextBoxFinds
)


class WordProcessorPanel(Panel):
    """
    A complete word processor panel with formatting tools and rich text editing.
    
    Features:
    - Formatting toolbar with bold, italic, underline buttons
    - Font family and size selection
    - Text and background color selection
    - Alignment options
    - Find and Replace
    - Word and character count
    - Modified state tracking
    
    Events:
    - DocumentChanged: Fired when the document content changes
    - DocumentSaved: Fired when the document is saved
    - DocumentOpened: Fired when a document is opened
    - SelectionChanged: Fired when the text selection changes
    """
    
    # Default toolbar button colors
    TOOLBAR_BG = '#F5F5F5'
    TOOLBAR_BUTTON_BG = '#FFFFFF'
    TOOLBAR_BUTTON_HOVER = '#E0E0E0'
    TOOLBAR_BUTTON_ACTIVE = '#B0C4DE'
    EDITOR_BG = '#FFFFFF'
    EDITOR_FG = '#000000'
    STATUS_BG = '#E8E8E8'
    STATUS_FG = '#333333'
    
    def __init__(self, master_form, props=None):
        """
        Initialize the WordProcessorPanel.
        
        Args:
            master_form: Parent form or container
            props: Optional dictionary with properties:
                - ShowToolbar: Show formatting toolbar (default True)
                - ShowStatusBar: Show status bar (default True)
                - ShowFindBar: Show find bar (default False)
                - DefaultFont: Default font family (default 'Segoe UI')
                - DefaultFontSize: Default font size (default 11)
                - EditorBackColor: Editor background color
                - EditorForeColor: Editor text color
                - ToolbarBackColor: Toolbar background color
                - ReadOnly: Make editor read-only (default False)
                
                Sub-properties for internal WinFormPy controls:
                - 'Toolbar': {'Height': 40, 'BackColor': '#F5F5F5', ...}
                - 'Editor': {'BackColor': '#FFF', 'ForeColor': '#000', 'Font': ..., ...}
                - 'StatusBar': {'Height': 25, 'BackColor': '#E8E8E8', 'ForeColor': '#333', ...}
                - 'FindBar': {'Height': 35, 'BackColor': '#FFF8DC', ...}
                - 'ToolbarButton': {'BackColor': '#FFF', 'Width': 32, 'Height': 28, ...}
        """
        # Extract sub-properties for internal controls
        self._toolbar_props = props.pop('Toolbar', {}) if props else {}
        self._editor_props = props.pop('Editor', {}) if props else {}
        self._statusbar_props = props.pop('StatusBar', {}) if props else {}
        self._findbar_props = props.pop('FindBar', {}) if props else {}
        self._toolbar_button_props = props.pop('ToolbarButton', {}) if props else {}
        
        defaults = {
            'Width': 800,
            'Height': 600,
            'BackColor': '#FFFFFF',
            'ShowToolbar': True,
            'ShowStatusBar': True,
            'ShowFindBar': False,
            'DefaultFont': 'Segoe UI',
            'DefaultFontSize': 11,
            'EditorBackColor': '#FFFFFF',
            'EditorForeColor': '#000000',
            'ToolbarBackColor': '#F5F5F5',
            'StatusBarBackColor': '#E8E8E8',
            'ReadOnly': False
        }
        
        if props:
            defaults.update(props)
        
        # Initialize Panel
        super().__init__(master_form, defaults)
        
        # Store configuration
        self._show_toolbar = defaults['ShowToolbar']
        self._show_status_bar = defaults['ShowStatusBar']
        self._show_find_bar = defaults['ShowFindBar']
        self._default_font = defaults['DefaultFont']
        self._default_font_size = defaults['DefaultFontSize']
        self._editor_back_color = self._editor_props.get('BackColor', defaults['EditorBackColor'])
        self._editor_fore_color = self._editor_props.get('ForeColor', defaults['EditorForeColor'])
        self._toolbar_back_color = self._toolbar_props.get('BackColor', defaults['ToolbarBackColor'])
        self._status_bar_back_color = self._statusbar_props.get('BackColor', defaults['StatusBarBackColor'])
        self._read_only = defaults['ReadOnly']
        
        # Document state
        self._file_path = None
        self._is_modified = False
        self._document_title = "Untitled"
        
        # Events
        self.DocumentChanged = lambda sender, e: None
        self.DocumentSaved = lambda sender, e: None
        self.DocumentOpened = lambda sender, e: None
        self.SelectionChanged = lambda sender, e: None
        self.ModifiedChanged = lambda sender, e: None
        
        # Font options
        self._font_families = [
            'Segoe UI', 'Arial', 'Calibri', 'Cambria', 'Comic Sans MS',
            'Consolas', 'Courier New', 'Georgia', 'Impact', 'Lucida Console',
            'Tahoma', 'Times New Roman', 'Trebuchet MS', 'Verdana'
        ]
        self._font_sizes = ['8', '9', '10', '11', '12', '14', '16', '18', 
                           '20', '24', '28', '32', '36', '48', '72']
        
        # Color presets
        self._color_presets = [
            '#000000', '#FFFFFF', '#FF0000', '#00FF00', '#0000FF',
            '#FFFF00', '#FF00FF', '#00FFFF', '#808080', '#800000',
            '#008000', '#000080', '#808000', '#800080', '#008080'
        ]
        
        # Build UI
        self._create_ui()
        
        # Apply layout to ensure Dock works correctly
        self.PerformLayout()
        
        # Bind events
        self._bind_events()
    
    def _create_ui(self):
        """Create the word processor UI components."""
        # Toolbar
        if self._show_toolbar:
            self._create_toolbar()
        
        # Find bar (initially hidden)
        self._create_find_bar()
        
        # Status bar
        if self._show_status_bar:
            self._create_status_bar()
        
        # Editor (RichTextBox)
        self._create_editor()
    
    def _create_toolbar(self):
        """Create the formatting toolbar."""
        # Apply Toolbar sub-properties
        toolbar_height = self._toolbar_props.get('Height', 40)
        toolbar_padding = self._toolbar_props.get('Padding', 4)
        
        self._toolbar = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': toolbar_height,
            'BackColor': self._toolbar_back_color,
            'Padding': toolbar_padding
        })
        
        x_pos = 8
        # Apply ToolbarButton sub-properties
        button_height = self._toolbar_button_props.get('Height', 28)
        button_width = self._toolbar_button_props.get('Width', 32)
        button_bg = self._toolbar_button_props.get('BackColor', self.TOOLBAR_BUTTON_BG)
        combo_height = 24
        
        # Bold button
        self._btn_bold = Button(self._toolbar, {
            'Text': 'B',
            'Left': x_pos,
            'Top': 6,
            'Width': button_width,
            'Height': button_height,
            'BackColor': button_bg,
            'Font': Font('Segoe UI', 10, FontStyle.Bold)
        })
        self._btn_bold.ToolTipText = 'Bold (Ctrl+B)'
        self._btn_bold.Click = lambda s, e: self._toggle_bold()
        x_pos += button_width + 2
        
        # Italic button
        self._btn_italic = Button(self._toolbar, {
            'Text': 'I',
            'Left': x_pos,
            'Top': 6,
            'Width': button_width,
            'Height': button_height,
            'BackColor': button_bg,
            'Font': Font('Segoe UI', 10, FontStyle.Italic)
        })
        self._btn_italic.ToolTipText = 'Italic (Ctrl+I)'
        self._btn_italic.Click = lambda s, e: self._toggle_italic()
        x_pos += button_width + 2
        
        # Underline button
        self._btn_underline = Button(self._toolbar, {
            'Text': 'U',
            'Left': x_pos,
            'Top': 6,
            'Width': button_width,
            'Height': button_height,
            'BackColor': button_bg
        })
        self._btn_underline.ToolTipText = 'Underline (Ctrl+U)'
        self._btn_underline.Click = lambda s, e: self._toggle_underline()
        x_pos += button_width + 2
        
        # Strikethrough button
        self._btn_strike = Button(self._toolbar, {
            'Text': 'S',
            'Left': x_pos,
            'Top': 6,
            'Width': button_width,
            'Height': button_height,
            'BackColor': button_bg
        })
        self._btn_strike.ToolTipText = 'Strikethrough'
        self._btn_strike.Click = lambda s, e: self._toggle_strikethrough()
        x_pos += button_width + 12
        
        # Separator
        sep1 = Label(self._toolbar, {
            'Text': '|',
            'Left': x_pos,
            'Top': 8,
            'Width': 10,
            'Height': 24,
            'ForeColor': '#999999',
            'BackColor': self._toolbar_back_color
        })
        x_pos += 14
        
        # Font family combo label
        font_label = Label(self._toolbar, {
            'Text': 'Font:',
            'Left': x_pos,
            'Top': 10,
            'Width': 32,
            'Height': 20,
            'ForeColor': '#333333',
            'BackColor': self._toolbar_back_color
        })
        x_pos += 35
        
        # Font family combo
        self._combo_font = ComboBox(self._toolbar, {
            'Left': x_pos,
            'Top': 8,
            'Width': 140,
            'Height': combo_height,
            'DropDownStyle': 'DropDownList'
        })
        self._combo_font.ToolTipText = 'Font Family'
        for family in self._font_families:
            self._combo_font.Items.Add(family)
        self._combo_font.SelectedIndex = 0
        self._combo_font.SelectedIndexChanged = lambda s, e: self._on_font_family_changed()
        x_pos += 145
        
        # Font size combo
        self._combo_size = ComboBox(self._toolbar, {
            'Left': x_pos,
            'Top': 8,
            'Width': 55,
            'Height': combo_height,
            'DropDownStyle': 'DropDownList'
        })
        self._combo_size.ToolTipText = 'Font Size'
        for size in self._font_sizes:
            self._combo_size.Items.Add(size)
        self._combo_size.SelectedIndex = self._font_sizes.index(str(self._default_font_size))
        self._combo_size.SelectedIndexChanged = lambda s, e: self._on_font_size_changed()
        x_pos += 60
        
        # Separator
        sep2 = Label(self._toolbar, {
            'Text': '|',
            'Left': x_pos,
            'Top': 8,
            'Width': 10,
            'Height': 24,
            'ForeColor': '#999999',
            'BackColor': self._toolbar_back_color
        })
        x_pos += 14
        
        # Text color button
        self._btn_text_color = Button(self._toolbar, {
            'Text': 'A',
            'Left': x_pos,
            'Top': 6,
            'Width': button_width,
            'Height': button_height,
            'BackColor': self.TOOLBAR_BUTTON_BG,
            'ForeColor': '#FF0000',
            'Font': Font('Segoe UI', 10, FontStyle.Bold)
        })
        self._btn_text_color.ToolTipText = 'Text Color'
        self._btn_text_color.Click = lambda s, e: self._show_color_picker('text')
        x_pos += button_width + 2
        
        # Background color button
        self._btn_bg_color = Button(self._toolbar, {
            'Text': '⬜',
            'Left': x_pos,
            'Top': 6,
            'Width': button_width,
            'Height': button_height,
            'BackColor': '#FFFF00'
        })
        self._btn_bg_color.ToolTipText = 'Highlight'
        self._btn_bg_color.Click = lambda s, e: self._show_color_picker('background')
        x_pos += button_width + 12
        
        # Separator
        sep3 = Label(self._toolbar, {
            'Text': '|',
            'Left': x_pos,
            'Top': 8,
            'Width': 10,
            'Height': 24,
            'ForeColor': '#999999',
            'BackColor': self._toolbar_back_color
        })
        x_pos += 14
        
        # Alignment buttons
        self._btn_align_left = Button(self._toolbar, {
            'Text': '≡',
            'Left': x_pos,
            'Top': 6,
            'Width': button_width,
            'Height': button_height,
            'BackColor': self.TOOLBAR_BUTTON_BG
        })
        self._btn_align_left.ToolTipText = 'Align Left'
        self._btn_align_left.Click = lambda s, e: self._set_alignment('left')
        x_pos += button_width + 2
        
        self._btn_align_center = Button(self._toolbar, {
            'Text': '≡',
            'Left': x_pos,
            'Top': 6,
            'Width': button_width,
            'Height': button_height,
            'BackColor': self.TOOLBAR_BUTTON_BG
        })
        self._btn_align_center.ToolTipText = 'Center'
        self._btn_align_center.Click = lambda s, e: self._set_alignment('center')
        x_pos += button_width + 2
        
        self._btn_align_right = Button(self._toolbar, {
            'Text': '≡',
            'Left': x_pos,
            'Top': 6,
            'Width': button_width,
            'Height': button_height,
            'BackColor': self.TOOLBAR_BUTTON_BG
        })
        self._btn_align_right.ToolTipText = 'Align Right'
        self._btn_align_right.Click = lambda s, e: self._set_alignment('right')
    
    def _create_find_bar(self):
        """Create the find/replace bar."""
        # Apply FindBar sub-properties
        findbar_height = self._findbar_props.get('Height', 35)
        findbar_bg = self._findbar_props.get('BackColor', '#FFF8DC')
        
        self._find_bar = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': findbar_height,
            'BackColor': findbar_bg,
            'Visible': self._show_find_bar
        })
        
        # Find label
        find_label = Label(self._find_bar, {
            'Text': 'Find:',
            'Left': 10,
            'Top': 8,
            'Width': 35,
            'Height': 20,
            'BackColor': findbar_bg
        })
        
        # Find textbox
        self._txt_find = TextBox(self._find_bar, {
            'Left': 50,
            'Top': 5,
            'Width': 200,
            'Height': 24
        })
        
        # Find buttons
        self._btn_find_prev = Button(self._find_bar, {
            'Text': '◄',
            'Left': 255,
            'Top': 4,
            'Width': 30,
            'Height': 26
        })
        self._btn_find_prev.ToolTipText = 'Previous'
        self._btn_find_prev.Click = lambda s, e: self._find_previous()
        
        self._btn_find_next = Button(self._find_bar, {
            'Text': '►',
            'Left': 288,
            'Top': 4,
            'Width': 30,
            'Height': 26
        })
        self._btn_find_next.ToolTipText = 'Next'
        self._btn_find_next.Click = lambda s, e: self._find_next()
        
        # Replace label
        replace_label = Label(self._find_bar, {
            'Text': 'Replace:',
            'Left': 330,
            'Top': 8,
            'Width': 55,
            'Height': 20,
            'BackColor': '#FFF8DC'
        })
        
        # Replace textbox
        self._txt_replace = TextBox(self._find_bar, {
            'Left': 390,
            'Top': 5,
            'Width': 150,
            'Height': 24
        })
        
        # Replace buttons
        self._btn_replace = Button(self._find_bar, {
            'Text': 'Replace',
            'Left': 545,
            'Top': 4,
            'Width': 60,
            'Height': 26
        })
        self._btn_replace.ToolTipText = 'Replace current'
        self._btn_replace.Click = lambda s, e: self._replace_current()
        
        self._btn_replace_all = Button(self._find_bar, {
            'Text': 'All',
            'Left': 608,
            'Top': 4,
            'Width': 40,
            'Height': 26
        })
        self._btn_replace_all.ToolTipText = 'Replace all'
        self._btn_replace_all.Click = lambda s, e: self._replace_all()
        
        # Close button
        self._btn_close_find = Button(self._find_bar, {
            'Text': '✕',
            'Left': 660,
            'Top': 4,
            'Width': 26,
            'Height': 26,
            'BackColor': '#FFF8DC'
        })
        self._btn_close_find.ToolTipText = 'Close'
        self._btn_close_find.Click = lambda s, e: self._hide_find_bar()
    
    def _create_status_bar(self):
        """Create the status bar."""
        # Apply StatusBar sub-properties
        statusbar_height = self._statusbar_props.get('Height', 24)
        statusbar_fg = self._statusbar_props.get('ForeColor', self.STATUS_FG)
        
        self._status_bar = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': statusbar_height,
            'BackColor': self._status_bar_back_color
        })
        
        # Word count
        self._lbl_word_count = Label(self._status_bar, {
            'Text': 'Words: 0',
            'Left': 10,
            'Top': 4,
            'Width': 100,
            'Height': 16,
            'ForeColor': statusbar_fg,
            'BackColor': self._status_bar_back_color
        })
        
        # Character count
        self._lbl_char_count = Label(self._status_bar, {
            'Text': 'Characters: 0',
            'Left': 120,
            'Top': 4,
            'Width': 120,
            'Height': 16,
            'ForeColor': statusbar_fg,
            'BackColor': self._status_bar_back_color
        })
        
        # Line count
        self._lbl_line_count = Label(self._status_bar, {
            'Text': 'Lines: 0',
            'Left': 250,
            'Top': 4,
            'Width': 80,
            'Height': 16,
            'ForeColor': statusbar_fg,
            'BackColor': self._status_bar_back_color
        })
        
        # Cursor position
        self._lbl_position = Label(self._status_bar, {
            'Text': 'Ln 1, Col 1',
            'Left': 340,
            'Top': 4,
            'Width': 100,
            'Height': 16,
            'ForeColor': self.STATUS_FG,
            'BackColor': self._status_bar_back_color
        })
        
        # Modified indicator
        self._lbl_modified = Label(self._status_bar, {
            'Text': '',
            'Left': 450,
            'Top': 4,
            'Width': 100,
            'Height': 16,
            'ForeColor': '#FF6600',
            'BackColor': self._status_bar_back_color
        })
    
    def _create_editor(self):
        """Create the RichTextBox editor."""
        # Apply Editor sub-properties
        editor_font = self._editor_props.get('Font', Font(self._default_font, self._default_font_size))
        editor_wordwrap = self._editor_props.get('WordWrap', True)
        editor_padding = self._editor_props.get('Padding', None)
        
        editor_props = {
            'Dock': DockStyle.Fill,
            'BackColor': self._editor_back_color,
            'ForeColor': self._editor_fore_color,
            'Font': editor_font,
            'WordWrap': editor_wordwrap,
            'ReadOnly': self._read_only,
            'ScrollBars': 'both'
        }
        if editor_padding is not None:
            editor_props['Padding'] = editor_padding
        
        self._editor = RichTextBox(self, editor_props)
    
    def _bind_events(self):
        """Bind editor events."""
        if hasattr(self._editor, 'TextChanged'):
            self._editor.TextChanged = self._on_text_changed
        
        if hasattr(self._editor, 'SelectionChanged'):
            self._editor.SelectionChanged = self._on_selection_changed
        
        # Keyboard shortcuts
        self._editor.BindKey('<Control-b>', lambda e: self._toggle_bold())
        self._editor.BindKey('<Control-i>', lambda e: self._toggle_italic())
        self._editor.BindKey('<Control-u>', lambda e: self._toggle_underline())
        self._editor.BindKey('<Control-f>', lambda e: self._show_find_bar())
        self._editor.BindKey('<Control-h>', lambda e: self._show_find_bar())
        self._editor.BindKey('<Control-s>', lambda e: self.Save())
        self._editor.BindKey('<Control-o>', lambda e: self.Open())
        self._editor.BindKey('<Control-n>', lambda e: self.New())
        self._editor.BindKey('<Escape>', lambda e: self._hide_find_bar())
    
    # =========================================================================
    # Event Handlers
    # =========================================================================
    
    def _on_text_changed(self, sender, e):
        """Handle text changes."""
        self._is_modified = True
        self._update_status_bar()
        self.DocumentChanged(self, e)
        self.ModifiedChanged(self, e)
    
    def _on_selection_changed(self, sender, e):
        """Handle selection changes."""
        self._update_cursor_position()
        self.SelectionChanged(self, e)
    
    # =========================================================================
    # Formatting Methods
    # =========================================================================
    
    def _toggle_bold(self):
        """Toggle bold formatting on selection."""
        self._editor.SelectionBold = not self._editor.SelectionBold
    
    def _toggle_italic(self):
        """Toggle italic formatting on selection."""
        self._editor.SelectionItalic = not self._editor.SelectionItalic
    
    def _toggle_underline(self):
        """Toggle underline formatting on selection."""
        self._editor.SelectionUnderline = not self._editor.SelectionUnderline
    
    def _toggle_strikethrough(self):
        """Toggle strikethrough formatting on selection."""
        self._editor.SelectionStrikethrough = not self._editor.SelectionStrikethrough
    
    def _on_font_family_changed(self):
        """Handle font family change."""
        if self._combo_font.SelectedIndex >= 0:
            # Save selection state
            sel_start = self._editor.SelectionStart
            sel_length = self._editor.SelectionLength
            
            # If no selection, select all to apply font to entire document
            if sel_length == 0:
                self._editor.SelectAll()
            
            family = self._font_families[self._combo_font.SelectedIndex]
            size = int(self._font_sizes[self._combo_size.SelectedIndex])
            new_font = Font(family, size)
            self._editor.SelectionFont = new_font
            
            # Force widget update to apply changes
            if hasattr(self._editor, '_tk_widget'):
                self._editor._tk_widget.update_idletasks()
            
            # Restore original selection and focus
            self._editor.SelectionStart = sel_start
            self._editor.SelectionLength = sel_length
            self._editor.Focus()
    
    def _on_font_size_changed(self):
        """Handle font size change."""
        if self._combo_size.SelectedIndex >= 0:
            # Save selection state
            sel_start = self._editor.SelectionStart
            sel_length = self._editor.SelectionLength
            
            # If no selection, select all to apply size to entire document
            if sel_length == 0:
                self._editor.SelectAll()
            
            family = self._font_families[self._combo_font.SelectedIndex]
            size = int(self._font_sizes[self._combo_size.SelectedIndex])
            new_font = Font(family, size)
            self._editor.SelectionFont = new_font
            
            # Force widget update to apply changes
            if hasattr(self._editor, '_tk_widget'):
                self._editor._tk_widget.update_idletasks()
            
            # Restore original selection and focus
            self._editor.SelectionStart = sel_start
            self._editor.SelectionLength = sel_length
            self._editor.Focus()
    
    def _show_color_picker(self, color_type):
        """Show color picker for text or background."""
        # For now, cycle through preset colors
        # A full implementation would show a color picker dialog
        current_color = getattr(self, f'_current_{color_type}_color_index', 0)
        current_color = (current_color + 1) % len(self._color_presets)
        setattr(self, f'_current_{color_type}_color_index', current_color)
        
        color = self._color_presets[current_color]
        if color_type == 'text':
            self._editor.SelectionColor = color
            self._btn_text_color.ForeColor = color
        else:
            self._editor.SelectionBackColor = color
            self._btn_bg_color.BackColor = color
    
    def _set_alignment(self, alignment):
        """Set text alignment."""
        self._editor.SelectionAlignment = alignment
    
    # =========================================================================
    # Find/Replace Methods
    # =========================================================================
    
    def _show_find_bar(self):
        """Show the find/replace bar."""
        self._find_bar.Visible = True
        self._show_find_bar = True
        self._txt_find.Focus()
    
    def _hide_find_bar(self):
        """Hide the find/replace bar."""
        self._find_bar.Visible = False
        self._show_find_bar = False
        self._editor.Focus()
    
    def _find_next(self):
        """Find next occurrence."""
        text = self._txt_find.Text
        if text:
            self._editor.Find(text, self._editor.SelectionStart + 1)
    
    def _find_previous(self):
        """Find previous occurrence."""
        text = self._txt_find.Text
        if text:
            self._editor.Find(text, 0, RichTextBoxFinds.Reverse)
    
    def _replace_current(self):
        """Replace current selection."""
        find_text = self._txt_find.Text
        replace_text = self._txt_replace.Text
        if find_text:
            self._editor.FindAndReplace(find_text, replace_text, replace_all=False)
    
    def _replace_all(self):
        """Replace all occurrences."""
        find_text = self._txt_find.Text
        replace_text = self._txt_replace.Text
        if find_text:
            count = self._editor.FindAndReplace(find_text, replace_text, replace_all=True)
            # Could show a message with count
    
    # =========================================================================
    # Status Bar Methods
    # =========================================================================
    
    def _update_status_bar(self):
        """Update status bar information."""
        if not self._show_status_bar:
            return
        
        text = self._editor.Text
        
        # Word count (split by whitespace)
        words = len(text.split()) if text.strip() else 0
        self._lbl_word_count.Text = f'Words: {words}'
        
        # Character count
        chars = len(text)
        self._lbl_char_count.Text = f'Characters: {chars}'
        
        # Line count
        lines = self._editor.LineCount
        self._lbl_line_count.Text = f'Lines: {lines}'
        
        # Modified indicator
        self._lbl_modified.Text = 'Modified' if self._is_modified else ''
    
    def _update_cursor_position(self):
        """Update cursor position in status bar."""
        if not self._show_status_bar:
            return
        
        try:
            # Get current position using WinFormPy API (not direct tkinter access)
            char_index = self._editor.SelectionStart
            line = self._editor.GetLineFromCharIndex(char_index) + 1  # 1-based
            line_start = self._editor.GetFirstCharIndexFromLine(line - 1)  # 0-based for method
            col = char_index - line_start + 1  # 1-based column
            self._lbl_position.Text = f'Ln {line}, Col {col}'
        except:
            pass
    
    # =========================================================================
    # Document Methods
    # =========================================================================
    
    def New(self):
        """Create a new document."""
        if self._is_modified:
            # Could prompt to save first
            pass
        
        self._editor.Clear()
        self._file_path = None
        self._document_title = "Untitled"
        self._is_modified = False
        self._update_status_bar()
    
    def Open(self, file_path=None, file_type=None):
        """
        Open a document.
        
        Args:
            file_path: Path to file. If None, shows file dialog.
            file_type: RichTextBoxStreamType indicating the format.
                       If None, auto-detects from file extension.
        """
        if file_path:
            try:
                self._editor.LoadFile(file_path, file_type)
                self._file_path = file_path
                self._document_title = os.path.basename(file_path)
                self._is_modified = False
                self._update_status_bar()
                self.DocumentOpened(self, None)
            except Exception as e:
                print(f"Error opening file: {e}")
    
    def Save(self):
        """Save the current document."""
        if self._file_path:
            self._save_to_file(self._file_path)
        else:
            # Would show save dialog
            pass
    
    def SaveAs(self, file_path, file_type=None):
        """
        Save the document to a new path.
        
        Args:
            file_path: Path to save to.
            file_type: RichTextBoxStreamType indicating the format.
                       If None, auto-detects from file extension.
        """
        self._save_to_file(file_path, file_type)
        self._file_path = file_path
        self._document_title = os.path.basename(file_path)
    
    def _save_to_file(self, file_path, file_type=None):
        """Save content to file."""
        try:
            self._editor.SaveFile(file_path, file_type)
            self._is_modified = False
            self._update_status_bar()
            self.DocumentSaved(self, None)
        except Exception as e:
            print(f"Error saving file: {e}")
    
    # =========================================================================
    # Properties
    # =========================================================================
    
    @property
    def Text(self):
        """Gets the document text (plain text without formatting)."""
        return self._editor.Text
    
    @Text.setter
    def Text(self, value):
        """Sets the document text."""
        self._editor.Text = value
        self._is_modified = True
        self._update_status_bar()
    
    @property
    def Rtf(self):
        """Gets the document text in RTF format."""
        return self._editor.Rtf
    
    @Rtf.setter
    def Rtf(self, value):
        """Sets the document from RTF format."""
        self._editor.Rtf = value
        self._is_modified = True
        self._update_status_bar()
    
    @property
    def SelectedText(self):
        """Gets the currently selected text."""
        return self._editor.SelectedText
    
    @SelectedText.setter
    def SelectedText(self, value):
        """Replaces the current selection with the specified text."""
        self._editor.SelectedText = value
    
    @property
    def SelectedRtf(self):
        """Gets the currently selected RTF text."""
        return self._editor.SelectedRtf
    
    @SelectedRtf.setter
    def SelectedRtf(self, value):
        """Replaces the current selection with RTF formatted text."""
        self._editor.SelectedRtf = value
    
    @property
    def FilePath(self):
        """Gets the current file path."""
        return self._file_path
    
    @property
    def DocumentTitle(self):
        """Gets the document title."""
        return self._document_title
    
    @property
    def IsModified(self):
        """Gets whether the document has been modified."""
        return self._is_modified
    
    @IsModified.setter
    def IsModified(self, value):
        """Sets the modified state."""
        self._is_modified = value
        self._update_status_bar()
        self.ModifiedChanged(self, None)
    
    @property
    def ReadOnly(self):
        """Gets whether the editor is read-only."""
        return self._read_only
    
    @ReadOnly.setter
    def ReadOnly(self, value):
        """Sets the read-only state."""
        self._read_only = value
        if hasattr(self, '_editor'):
            self._editor.ReadOnly = value
    
    @property
    def Editor(self):
        """Gets the RichTextBox editor control."""
        return self._editor
    
    @property
    def WordCount(self):
        """Gets the word count."""
        text = self._editor.Text
        return len(text.split()) if text.strip() else 0
    
    @property
    def CharacterCount(self):
        """Gets the character count."""
        return len(self._editor.Text)
    
    @property
    def LineCount(self):
        """Gets the line count."""
        return self._editor.LineCount
    
    # =========================================================================
    # Clipboard Methods (delegated to editor)
    # =========================================================================
    
    def Cut(self):
        """Cut selected text."""
        self._editor.Cut()
    
    def Copy(self):
        """Copy selected text."""
        self._editor.Copy()
    
    def Paste(self):
        """Paste from clipboard."""
        self._editor.Paste()
    
    def Undo(self):
        """Undo last action."""
        self._editor.Undo()
    
    def Redo(self):
        """Redo last undone action."""
        self._editor.Redo()
    
    def SelectAll(self):
        """Select all text."""
        self._editor.SelectAll()
    
    # =========================================================================
    # Write Methods (delegated to editor)
    # =========================================================================
    
    def Write(self, text, color=None):
        """Write text to the editor."""
        self._editor.Write(text, color)
        self._update_status_bar()
    
    def WriteLine(self, text='', color=None):
        """Write a line of text to the editor."""
        self._editor.WriteLine(text, color)
        self._update_status_bar()
    
    def AppendText(self, text, color=None):
        """Append text to the editor."""
        self._editor.AppendText(text, color)
        self._update_status_bar()
    
    def Clear(self):
        """Clear all text."""
        self._editor.Clear()
        self._update_status_bar()


# =============================================================================
# Example Main
# =============================================================================

def main():
    """
    Example demonstrating WordProcessorPanel usage.
    
    Run with:
        python -m winformpy.ui_elements.word_processor.word_processor_panel
    """
    from winformpy.winformpy import Application
    
    # Create main form
    form = Form({
        'Text': 'Word Processor Panel Demo',
        'Width': 1024,
        'Height': 768,
        'StartPosition': 'CenterScreen',
        'BackColor': '#F0F0F0'
    })
    
    # CRITICAL: Apply layout before adding controls
    form.ApplyLayout()
    
    # Create word processor panel
    processor = WordProcessorPanel(form, {
        'Dock': DockStyle.Fill,
        'ShowToolbar': True,
        'ShowStatusBar': True,
        'ShowFindBar': False,
        'DefaultFont': 'Segoe UI',
        'DefaultFontSize': 11
    })
    
    # Add sample content demonstrating RichTextBox features
    processor.WriteLine("Welcome to WordProcessorPanel!", '#0078D4')
    processor.WriteLine()
    processor.WriteLine("This panel provides a complete word processor with:", '#333333')
    processor.WriteLine("  • Formatting toolbar (Bold, Italic, Underline)", '#666666')
    processor.WriteLine("  • Font family and size selection", '#666666')
    processor.WriteLine("  • Text and highlight colors", '#666666')
    processor.WriteLine("  • Text alignment (Left, Center, Right)", '#666666')
    processor.WriteLine("  • Find and Replace functionality", '#666666')
    processor.WriteLine("  • Status bar with word/character count", '#666666')
    processor.WriteLine()
    processor.WriteLine("Try the formatting buttons above!", '#008000')
    processor.WriteLine()
    processor.WriteLine("RTF Support:", '#0078D4')
    processor.WriteLine("  - Use File > Open to load .rtf files", '#666666')
    processor.WriteLine("  - Use File > Save As to save with formatting", '#666666')
    processor.WriteLine("  - Access raw RTF via the Rtf property", '#666666')
    processor.WriteLine()
    
    # Show document properties
    def show_properties(sender, e):
        from winformpy.winformpy import MessageBox
        props = (
            f"Document Properties:\n\n"
            f"Words: {processor.WordCount}\n"
            f"Characters: {processor.CharacterCount}\n"
            f"Lines: {processor.LineCount}\n"
            f"Modified: {processor.IsModified}\n"
            f"File: {processor.FilePath or '(Untitled)'}"
        )
        MessageBox.Show(props, "Document Info")
    
    # Add keyboard shortcut for properties
    processor.Editor.BindKey('<Control-i>', show_properties)
    processor.WriteLine("Press Ctrl+I to show document properties.", '#808080')
    
    # Run the application
    Application.Run(form)


if __name__ == "__main__":
    main()