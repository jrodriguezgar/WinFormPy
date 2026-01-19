"""
Studio Application Template
===========================

A tabbed application with IDE style.
Features a dark theme with activity bar, sidebar, and tabs.

USAGE
-----
    python templates/studio_template.py
    
    or:  uv run python templates/studio_template.py

FEATURES
--------
- Activity Bar (left icon bar)
- Sidebar panel (Explorer, Search, etc.)
- Tabbed document area
- Status bar
- Studio dark theme colors
- Welcome tab on startup
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from winformpy import (
    Form, Panel, Button, Label, TextBox, RichTextBox, TabControl, TabPage,
    TreeView, ListBox, AnchorStyles, RichTextBoxStreamType
)


# Studio Color Palette
class StudioColors:
    """Studio dark theme colors."""
    # Activity Bar
    ACTIVITY_BAR_BG = '#333333'
    ACTIVITY_BAR_ICON = '#858585'
    ACTIVITY_BAR_ICON_ACTIVE = '#FFFFFF'
    ACTIVITY_BAR_INDICATOR = '#007ACC'
    
    # Sidebar
    SIDEBAR_BG = '#252526'
    SIDEBAR_HEADER = '#BBBBBB'
    SIDEBAR_TEXT = '#CCCCCC'
    SIDEBAR_HOVER = '#2A2D2E'
    SIDEBAR_SELECTED = '#094771'
    
    # Editor
    EDITOR_BG = '#1E1E1E'
    EDITOR_TEXT = '#D4D4D4'
    EDITOR_LINE_NUMBER = '#858585'
    EDITOR_SELECTION = '#264F78'
    EDITOR_CURSOR = '#AEAFAD'
    
    # Tabs
    TAB_ACTIVE_BG = '#1E1E1E'
    TAB_INACTIVE_BG = '#2D2D2D'
    TAB_BORDER = '#252526'
    TAB_TEXT_ACTIVE = '#FFFFFF'
    TAB_TEXT_INACTIVE = '#969696'
    
    # Title Bar
    TITLE_BAR_BG = '#3C3C3C'
    TITLE_BAR_TEXT = '#CCCCCC'
    
    # Status Bar
    STATUS_BAR_BG = '#007ACC'
    STATUS_BAR_TEXT = '#FFFFFF'
    STATUS_BAR_NO_FOLDER = '#68217A'
    
    # Panel
    PANEL_BG = '#1E1E1E'
    PANEL_BORDER = '#474747'
    
    # Accent
    ACCENT = '#007ACC'
    ERROR = '#F14C4C'
    WARNING = '#CCA700'
    SUCCESS = '#89D185'


class DocumentTab:
    """Represents a document tab in the editor area."""
    
    def __init__(self, tab_control, title="Untitled", content="", is_modified=False):
        self.tab_control = tab_control
        self.title = title
        self.is_modified = is_modified
        self._content = content
        
        # Create tab page
        self.tab_page = TabPage(tab_control, {
            'Text': self._get_tab_title(),
            'BackColor': StudioColors.EDITOR_BG
        })
        
        # Create editor area
        self._create_editor()
    
    def _get_tab_title(self):
        """Get tab title with modified indicator."""
        if self.is_modified:
            return f"● {self.title}"
        return self.title
    
    def _create_editor(self):
        """Create the editor text area."""
        # Editor container with line numbers
        self.editor_container = Panel(self.tab_page, {
            'Dock': 'Fill',
            'BackColor': StudioColors.EDITOR_BG
        })
        
        # Line numbers panel
        self.line_numbers = Panel(self.editor_container, {
            'Width': 50,
            'Dock': 'Left',
            'BackColor': StudioColors.EDITOR_BG
        })
        
        # Text editor (using RichTextBox for enhanced editing)
        self.editor = RichTextBox(self.editor_container, {
            'Dock': 'Fill',
            'BackColor': StudioColors.EDITOR_BG,
            'ForeColor': StudioColors.EDITOR_TEXT,
            'Text': self._content,
            'WordWrap': False,
            'Font': ('Consolas', 11)
        })
        
        # Handle text changes (use *args to handle variable argument calls)
        self.editor.TextChanged = lambda *args: self._on_text_changed()
    
    def _on_text_changed(self):
        """Handle text changes."""
        if not self.is_modified:
            self.is_modified = True
            self.tab_page.Text = self._get_tab_title()
    
    @property
    def Content(self):
        return self.editor.Text
    
    @Content.setter
    def Content(self, value):
        self.editor.Text = value
    
    @property
    def Rtf(self):
        """Gets the content in RTF format."""
        return self.editor.Rtf
    
    @Rtf.setter
    def Rtf(self, value):
        """Sets the content from RTF format."""
        self.editor.Rtf = value
    
    def save(self):
        """Mark the document as saved."""
        self.is_modified = False
        self.tab_page.Text = self._get_tab_title()
    
    def load_file(self, path, file_type=None):
        """
        Load content from a file using RichTextBox.LoadFile.
        
        Args:
            path: Path to the file to load.
            file_type: RichTextBoxStreamType or None for auto-detect.
        """
        self.editor.LoadFile(path, file_type)
        self.title = os.path.basename(path)
        self.tab_page.Text = self._get_tab_title()
        self.is_modified = False
    
    def save_file(self, path, file_type=None):
        """
        Save content to a file using RichTextBox.SaveFile.
        
        Args:
            path: Path to save the file.
            file_type: RichTextBoxStreamType or None for auto-detect.
        """
        self.editor.SaveFile(path, file_type)
        self.title = os.path.basename(path)
        self.tab_page.Text = self._get_tab_title()
        self.is_modified = False
class StudioApp:
    """Main Studio Application with IDE style."""
    
    def __init__(self):
        self.documents = []
        self.current_document = None
        self.sidebar_visible = True
        self.active_activity = 'explorer'
        
        # Create main form
        self.form = Form({
            'Text': 'Studio - WinFormPy',
            'Width': 1280,
            'Height': 800,
            'StartPosition': 'CenterScreen',
            'BackColor': StudioColors.EDITOR_BG
        })
        
        # CRITICAL: Apply geometry BEFORE creating children
        # This ensures child controls get correct dimensions for Dock calculations
        self.form.ApplyLayout()
        
        # Create UI components
        self._create_title_bar()
        self._create_status_bar()
        self._create_main_container()
        
        # Open welcome tab
        self._open_welcome_tab()
    
    def _create_title_bar(self):
        """Create the title bar."""
        self.title_bar = Panel(self.form, {
            'Width': 1280,
            'Height': 30,
            'Dock': 'Top',
            'BackColor': StudioColors.TITLE_BAR_BG
        })
        
        # App icon/menu
        self.btn_menu = Button(self.title_bar, {
            'Text': '☰',
            'Left': 5,
            'Top': 2,
            'Width': 30,
            'Height': 26,
            'AutoSize': False,
            'BackColor': StudioColors.TITLE_BAR_BG,
            'ForeColor': StudioColors.TITLE_BAR_TEXT,
            'FlatStyle': 'Flat'
        })
        
        # Title
        self.lbl_title = Label(self.title_bar, {
            'Text': 'Studio - WinFormPy',
            'Left': 45,
            'Top': 7,
            'Width': 400,
            'Height': 20,
            'AutoSize': False,
            'ForeColor': StudioColors.TITLE_BAR_TEXT,
            'BackColor': StudioColors.TITLE_BAR_BG
        })
    
    def _create_status_bar(self):
        """Create the status bar."""
        self.status_bar = Panel(self.form, {
            'Width': 1280,
            'Height': 22,
            'Dock': 'Bottom',
            'BackColor': StudioColors.STATUS_BAR_BG
        })
        
        # Branch indicator
        self.lbl_branch = Label(self.status_bar, {
            'Text': '⎇ main',
            'Left': 10,
            'Top': 3,
            'Width': 80,
            'Height': 16,
            'AutoSize': False,
            'ForeColor': StudioColors.STATUS_BAR_TEXT,
            'BackColor': StudioColors.STATUS_BAR_BG
        })
        
        # Errors/Warnings
        self.lbl_problems = Label(self.status_bar, {
            'Text': '⚠ 0  ✕ 0',
            'Left': 100,
            'Top': 3,
            'Width': 80,
            'Height': 16,
            'AutoSize': False,
            'ForeColor': StudioColors.STATUS_BAR_TEXT,
            'BackColor': StudioColors.STATUS_BAR_BG
        })
        
        # Line/Column indicator (right side)
        self.lbl_position = Label(self.status_bar, {
            'Text': 'Ln 1, Col 1',
            'Left': 1100,
            'Top': 3,
            'Width': 80,
            'Height': 16,
            'Anchor': AnchorStyles.Top | AnchorStyles.Right,
            'AutoSize': False,
            'ForeColor': StudioColors.STATUS_BAR_TEXT,
            'BackColor': StudioColors.STATUS_BAR_BG
        })
        
        # Encoding
        self.lbl_encoding = Label(self.status_bar, {
            'Text': 'UTF-8',
            'Left': 1000,
            'Top': 3,
            'Width': 50,
            'Height': 16,
            'Anchor': AnchorStyles.Top | AnchorStyles.Right,
            'AutoSize': False,
            'ForeColor': StudioColors.STATUS_BAR_TEXT,
            'BackColor': StudioColors.STATUS_BAR_BG
        })
    
    def _create_main_container(self):
        """Create the main container with activity bar, sidebar, and editor."""
        self.main_container = Panel(self.form, {
            'Width': 1280,
            'Height': 800,
            'Dock': 'Fill',
            'BackColor': StudioColors.EDITOR_BG
        })
        
        # Activity Bar (left icon bar)
        self._create_activity_bar()
        
        # Sidebar
        self._create_sidebar()
        
        # Editor area
        self._create_editor_area()
    
    def _create_activity_bar(self):
        """Create the activity bar with icons."""
        self.activity_bar = Panel(self.main_container, {
            'Width': 48,
            'Height': 800,
            'Dock': 'Left',
            'BackColor': StudioColors.ACTIVITY_BAR_BG
        })
        
        # Activity buttons
        activities = [
            ('📁', 'explorer', 'Explorer'),
            ('🔍', 'search', 'Search'),
            ('⎇', 'source', 'Source Control'),
            ('🐛', 'debug', 'Run and Debug'),
            ('🧩', 'extensions', 'Extensions'),
        ]
        
        self.activity_buttons = {}
        for i, (icon, key, tooltip) in enumerate(activities):
            btn = Button(self.activity_bar, {
                'Text': icon,
                'Left': 0,
                'Top': i * 48,
                'Width': 48,
                'Height': 48,
                'AutoSize': False,
                'BackColor': StudioColors.ACTIVITY_BAR_BG,
                'ForeColor': StudioColors.ACTIVITY_BAR_ICON if key != 'explorer' else StudioColors.ACTIVITY_BAR_ICON_ACTIVE,
                'FlatStyle': 'Flat'
            })
            btn.Click = lambda s, e, k=key: self._on_activity_click(k)
            self.activity_buttons[key] = btn
        
        # Settings at bottom
        btn_settings = Button(self.activity_bar, {
            'Text': '⚙',
            'Left': 0,
            'Top': 700,
            'Width': 48,
            'Height': 48,
            'Anchor': AnchorStyles.Bottom | AnchorStyles.Left,
            'AutoSize': False,
            'BackColor': StudioColors.ACTIVITY_BAR_BG,
            'ForeColor': StudioColors.ACTIVITY_BAR_ICON,
            'FlatStyle': 'Flat'
        })
    
    def _create_sidebar(self):
        """Create the sidebar panel."""
        self.sidebar = Panel(self.main_container, {
            'Width': 250,
            'Height': 800,
            'Dock': 'Left',
            'BackColor': StudioColors.SIDEBAR_BG
        })
        
        # Sidebar header
        self.sidebar_header = Label(self.sidebar, {
            'Text': 'EXPLORER',
            'Left': 20,
            'Top': 10,
            'Width': 200,
            'Height': 20,
            'AutoSize': False,
            'ForeColor': StudioColors.SIDEBAR_HEADER,
            'BackColor': StudioColors.SIDEBAR_BG
        })
        
        # Open folder section
        self.open_folder_panel = Panel(self.sidebar, {
            'Left': 0,
            'Top': 40,
            'Width': 250,
            'Height': 100,
            'BackColor': StudioColors.SIDEBAR_BG
        })
        
        lbl_no_folder = Label(self.open_folder_panel, {
            'Text': 'You have not yet opened a folder.',
            'Left': 20,
            'Top': 20,
            'Width': 210,
            'Height': 40,
            'AutoSize': False,
            'ForeColor': StudioColors.SIDEBAR_TEXT,
            'BackColor': StudioColors.SIDEBAR_BG
        })
        
        btn_open_folder = Button(self.open_folder_panel, {
            'Text': 'Open Folder',
            'Left': 20,
            'Top': 60,
            'Width': 120,
            'Height': 28,
            'AutoSize': False,
            'BackColor': StudioColors.ACCENT,
            'ForeColor': '#FFFFFF'
        })
        btn_open_folder.Click = lambda s, e: self._on_open_folder()
        
        # Recent files section
        self.recent_panel = Panel(self.sidebar, {
            'Left': 0,
            'Top': 150,
            'Width': 250,
            'Height': 200,
            'BackColor': StudioColors.SIDEBAR_BG
        })
        
        lbl_recent = Label(self.recent_panel, {
            'Text': 'RECENT',
            'Left': 20,
            'Top': 0,
            'Width': 200,
            'Height': 20,
            'AutoSize': False,
            'ForeColor': StudioColors.SIDEBAR_HEADER,
            'BackColor': StudioColors.SIDEBAR_BG
        })
    
    def _create_editor_area(self):
        """Create the editor area with tabs."""
        self.editor_area = Panel(self.main_container, {
            'Dock': 'Fill',
            'BackColor': StudioColors.EDITOR_BG
        })
        
        # Tab control
        self.tab_control = TabControl(self.editor_area, {
            'Dock': 'Fill',
            'BackColor': StudioColors.TAB_INACTIVE_BG
        })
        
        self.tab_control.SelectedIndexChanged = self._on_tab_changed
    
    def _on_activity_click(self, activity_key):
        """Handle activity bar click."""
        # Update button colors
        for key, btn in self.activity_buttons.items():
            if key == activity_key:
                btn.ForeColor = StudioColors.ACTIVITY_BAR_ICON_ACTIVE
            else:
                btn.ForeColor = StudioColors.ACTIVITY_BAR_ICON
        
        # Update sidebar header
        titles = {
            'explorer': 'EXPLORER',
            'search': 'SEARCH',
            'source': 'SOURCE CONTROL',
            'debug': 'RUN AND DEBUG',
            'extensions': 'EXTENSIONS'
        }
        self.sidebar_header.Text = titles.get(activity_key, 'EXPLORER')
        self.active_activity = activity_key
        
        # Toggle sidebar visibility if clicking same activity
        if activity_key == self.active_activity and self.sidebar_visible:
            pass  # Could toggle sidebar here
    
    def _on_open_folder(self):
        """Handle open folder button click."""
        # In a real app, show folder dialog
        self.new_document("folder_opened.py", "# Folder opened\n")
    
    def _open_welcome_tab(self):
        """Open the welcome tab."""
        welcome_content = """

Welcome to Studio!

This is a tabbed application built with WinFormPy,
featuring the iconic Visual Studio Code dark theme.

FEATURES:
─────────
• Activity Bar - Quick access to different views
• Sidebar - File explorer and search
• Tabbed Editor - Multiple documents in tabs
• Status Bar - Information and indicators
• Studio Dark Theme - Familiar, modern look

GETTING STARTED:
────────────────
1. Click "Open Folder" in the sidebar to open a project
2. Use the activity bar to switch between views
3. Create new documents with File > New
4. Enjoy the Studio experience in Python!

KEYBOARD SHORTCUTS:
──────────────────
• Ctrl+N     New File
• Ctrl+S     Save
• Ctrl+W     Close Tab
• Ctrl+Tab   Switch Tabs
• Ctrl+B     Toggle Sidebar
• Ctrl+`     Toggle Terminal

Built with WinFormPy - Python GUI the .NET way!
"""
        self.new_document("Welcome", welcome_content)
    
    def new_document(self, title="Untitled", content=""):
        """Create a new document tab."""
        doc = DocumentTab(self.tab_control, title=title, content=content)
        self.documents.append(doc)
        
        # Select the new tab
        self.tab_control.SelectedIndex = len(self.documents) - 1
        self.current_document = doc
        
        return doc
    
    def close_current_document(self):
        """Close the current document tab."""
        if self.current_document and len(self.documents) > 0:
            index = self.documents.index(self.current_document)
            self.documents.remove(self.current_document)
            
            if self.documents:
                new_index = min(index, len(self.documents) - 1)
                self.tab_control.SelectedIndex = new_index
                self.current_document = self.documents[new_index]
            else:
                self.current_document = None
    
    def _on_tab_changed(self, sender, e):
        """Handle tab selection change."""
        index = self.tab_control.SelectedIndex
        if 0 <= index < len(self.documents):
            self.current_document = self.documents[index]
            self._update_title()
    
    def _update_title(self):
        """Update the window title."""
        if self.current_document:
            self.form.Text = f'{self.current_document.title} - Studio'
            self.lbl_title.Text = f'{self.current_document.title} - Studio'
        else:
            self.form.Text = 'Studio - WinFormPy'
            self.lbl_title.Text = 'Studio - WinFormPy'
    
    def run(self):
        """Run the application."""
        self.form.ShowDialog()


def main():
    """Application entry point."""
    app = StudioApp()
    app.run()


if __name__ == "__main__":
    main()
