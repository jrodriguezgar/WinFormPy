"""
Windows 11 File Explorer Style Template
========================================

A tabbed application styled like the 
Windows 11 File Explorer with Fluent Design.

USAGE
-----
    python templates/explorer_template.py
    
    or:  uv run python templates/explorer_template.py

FEATURES
--------
- Modern Windows 11 Fluent Design
- Navigation pane with Quick Access and folders
- Command bar with modern icons
- Address bar with breadcrumbs
- Tabbed content area
- Details pane (optional)
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from winformpy import (
    Form, Panel, Button, Label, TextBox, TabControl, TabPage,
    ListBox, AnchorStyles, DockStyle, FlowLayoutPanel, FlowDirection
)


# Windows 11 Fluent Design Color Palette
class Win11Colors:
    """Windows 11 Fluent Design colors."""
    # Background
    BG_PRIMARY = '#FFFFFF'
    BG_SECONDARY = '#F3F3F3'
    BG_TERTIARY = '#FAFAFA'
    BG_MICA = '#F9F9F9'
    
    # Navigation Pane
    NAV_BG = '#F3F3F3'
    NAV_HOVER = '#E5E5E5'
    NAV_SELECTED = '#CCE4F7'
    NAV_TEXT = '#1A1A1A'
    NAV_ICON = '#1A1A1A'
    
    # Command Bar
    COMMAND_BG = '#FFFFFF'
    COMMAND_HOVER = '#E5E5E5'
    COMMAND_ICON = '#1A1A1A'
    COMMAND_DISABLED = '#A0A0A0'
    
    # Tabs
    TAB_BG = '#FFFFFF'
    TAB_ACTIVE = '#FFFFFF'
    TAB_INACTIVE = '#F3F3F3'
    TAB_HOVER = '#E5E5E5'
    TAB_TEXT = '#1A1A1A'
    TAB_BORDER = '#E5E5E5'
    
    # Address Bar
    ADDRESS_BG = '#FFFFFF'
    ADDRESS_BORDER = '#E5E5E5'
    ADDRESS_TEXT = '#1A1A1A'
    ADDRESS_ICON = '#666666'
    
    # Content Area
    CONTENT_BG = '#FFFFFF'
    CONTENT_HEADER = '#1A1A1A'
    CONTENT_TEXT = '#3B3B3B'
    CONTENT_HOVER = '#F5F5F5'
    CONTENT_SELECTED = '#CCE4F7'
    CONTENT_BORDER = '#E5E5E5'
    
    # Accent
    ACCENT = '#0078D4'
    ACCENT_HOVER = '#1084D9'
    ACCENT_LIGHT = '#CCE4F7'
    
    # Status
    STATUS_BG = '#F3F3F3'
    STATUS_TEXT = '#666666'
    
    # Shadows and effects
    SHADOW = '#0000001A'
    BORDER_RADIUS = 4


class FileItem:
    """Represents a file or folder item."""
    
    def __init__(self, name, item_type="file", size="", modified="", icon="📄"):
        self.name = name
        self.type = item_type
        self.size = size
        self.modified = modified
        self.icon = icon
        self.is_folder = item_type == "folder"


class ExplorerTab:
    """Represents a file explorer tab."""
    
    def __init__(self, tab_control, path="This PC", on_navigate=None):
        self.tab_control = tab_control
        self.path = path
        self.history = [path]
        self.history_index = 0
        self.on_navigate = on_navigate
        self.selected_items = []
        
        # Create tab page
        self.tab_page = TabPage(tab_control, {
            'Text': self._get_folder_name(path),
            'BackColor': Win11Colors.CONTENT_BG
        })
        
        # Create components
        self._create_address_bar()
        self._create_content_area()
        
        # Load initial content
        self._load_content(path)
    
    def _get_folder_name(self, path):
        """Get display name for a path."""
        if path == "This PC":
            return "This PC"
        return os.path.basename(path) or path
    
    def _create_address_bar(self):
        """Create the address bar with breadcrumbs."""
        self.address_bar = Panel(self.tab_page, {
            'Height': 40,
            'Dock': 'Top',
            'BackColor': Win11Colors.CONTENT_BG
        })
        
        # Back button
        self.btn_back = Button(self.address_bar, {
            'Text': '←',
            'Left': 8,
            'Top': 6,
            'Width': 32,
            'Height': 28,
            'BackColor': Win11Colors.CONTENT_BG,
            'ForeColor': Win11Colors.ADDRESS_ICON,
            'FlatStyle': 'Flat'
        })
        self.btn_back.Click = lambda s, e: self.go_back()
        
        # Forward button
        self.btn_forward = Button(self.address_bar, {
            'Text': '→',
            'Left': 42,
            'Top': 6,
            'Width': 32,
            'Height': 28,
            'BackColor': Win11Colors.CONTENT_BG,
            'ForeColor': Win11Colors.ADDRESS_ICON,
            'FlatStyle': 'Flat'
        })
        self.btn_forward.Click = lambda s, e: self.go_forward()
        
        # Up button
        self.btn_up = Button(self.address_bar, {
            'Text': '↑',
            'Left': 76,
            'Top': 6,
            'Width': 32,
            'Height': 28,
            'BackColor': Win11Colors.CONTENT_BG,
            'ForeColor': Win11Colors.ADDRESS_ICON,
            'FlatStyle': 'Flat'
        })
        self.btn_up.Click = lambda s, e: self.go_up()
        
        # Refresh button
        self.btn_refresh = Button(self.address_bar, {
            'Text': '↻',
            'Left': 110,
            'Top': 6,
            'Width': 32,
            'Height': 28,
            'BackColor': Win11Colors.CONTENT_BG,
            'ForeColor': Win11Colors.ADDRESS_ICON,
            'FlatStyle': 'Flat'
        })
        self.btn_refresh.Click = lambda s, e: self.refresh()
        
        # Address text box - Anchored Left/Right to stretch
        self.txt_address = TextBox(self.address_bar, {
            'Left': 150,
            'Top': 8,
            'Width': 600,
            'Height': 26,
            'Text': self.path,
            'BackColor': Win11Colors.ADDRESS_BG,
            'ForeColor': Win11Colors.ADDRESS_TEXT,
            'Anchor': AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right
        })
        self.txt_address.KeyPress = self._on_address_keypress
        
        # Search box - Anchored Right to stay on the side
        self.txt_search = TextBox(self.address_bar, {
            'Left': 770,
            'Top': 8,
            'Width': 200,
            'Height': 26,
            'Text': '🔍 Search',
            'BackColor': Win11Colors.ADDRESS_BG,
            'ForeColor': Win11Colors.ADDRESS_ICON,
            'Anchor': AnchorStyles.Top | AnchorStyles.Right
        })
    
    def _create_content_area(self):
        """Create the content area with file list."""
        self.content_area = Panel(self.tab_page, {
            'Dock': 'Fill',
            'BackColor': Win11Colors.CONTENT_BG
        })
        
        # Column headers
        self.header_panel = Panel(self.content_area, {
            'Height': 30,
            'Dock': 'Top',
            'BackColor': Win11Colors.CONTENT_BG
        })
        
        headers = [
            ('Name', 0, 400),
            ('Date modified', 410, 150),
            ('Type', 570, 100),
            ('Size', 680, 80)
        ]
        
        for text, left, width in headers:
            lbl = Label(self.header_panel, {
                'Text': text,
                'Left': left,
                'Top': 5,
                'Width': width,
                'Height': 20,
                'ForeColor': Win11Colors.CONTENT_TEXT,
                'BackColor': Win11Colors.CONTENT_BG
            })
        
        # Separator line
        self.separator = Panel(self.content_area, {
            'Height': 1,
            'Dock': 'Top',
            'BackColor': Win11Colors.CONTENT_BORDER
        })
        
        # File list
        self.file_list = ListBox(self.content_area, {
            'Dock': 'Fill',
            'BackColor': Win11Colors.CONTENT_BG,
            'ForeColor': Win11Colors.CONTENT_TEXT
        })
    
    def _on_address_keypress(self, sender, e):
        """Handle Enter in address bar."""
        if hasattr(e, 'KeyChar') and e.KeyChar == '\r':
            self.navigate(self.txt_address.Text)
    
    def _load_content(self, path):
        """Load folder content."""
        self.file_list.Items.Clear()
        
        if path == "This PC":
            # Show drives
            items = [
                "📁 Desktop",
                "📁 Documents",
                "📁 Downloads",
                "📁 Pictures",
                "📁 Music",
                "📁 Videos",
                "──────────────",
                "💿 Local Disk (C:)",
                "💿 Data (D:)",
            ]
        else:
            # Show sample files
            items = [
                "📁 Folder 1                    Today            File folder",
                "📁 Folder 2                    Yesterday        File folder",
                "📄 document.docx               Today            Word Doc        24 KB",
                "📊 spreadsheet.xlsx            Yesterday        Excel           156 KB",
                "🖼 image.png                   Last week        PNG Image       2.4 MB",
                "📝 notes.txt                   Today            Text File       4 KB",
            ]
        
        for item in items:
            self.file_list.Items.Add(item)
    
    def navigate(self, path):
        """Navigate to a path."""
        self.path = path
        self.txt_address.Text = path
        self.tab_page.Text = self._get_folder_name(path)
        
        # Update history
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        self.history.append(path)
        self.history_index = len(self.history) - 1
        
        self._load_content(path)
    
    def go_back(self):
        """Navigate back in history."""
        if self.history_index > 0:
            self.history_index -= 1
            path = self.history[self.history_index]
            self.path = path
            self.txt_address.Text = path
            self.tab_page.Text = self._get_folder_name(path)
            self._load_content(path)
    
    def go_forward(self):
        """Navigate forward in history."""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            path = self.history[self.history_index]
            self.path = path
            self.txt_address.Text = path
            self.tab_page.Text = self._get_folder_name(path)
            self._load_content(path)
    
    def go_up(self):
        """Navigate to parent folder."""
        if self.path != "This PC":
            parent = os.path.dirname(self.path)
            if parent:
                self.navigate(parent)
            else:
                self.navigate("This PC")
    
    def refresh(self):
        """Refresh current content."""
        self._load_content(self.path)


class ExplorerApp:
    """Main Application with Windows 11 File Explorer style."""
    
    def __init__(self):
        self.tabs = []
        self.current_tab = None
        
        # Create main form
        self.form = Form({
            'Text': 'File Explorer',
            'Width': 1200,
            'Height': 750,
            'StartPosition': 'CenterScreen',
            'BackColor': Win11Colors.BG_MICA
        })
        
        # CRITICAL: Apply geometry BEFORE creating children
        # This ensures child controls get correct dimensions for Dock calculations
        self.form.ApplyLayout()
        
        # Create UI components
        self._create_command_bar()
        self._create_status_bar()
        self._create_main_container()
        
        # Open initial tab
        self.new_tab("This PC")
    
    def _create_command_bar(self):
        """Create the command bar toolbar."""
        self.command_bar = Panel(self.form, {
            'Height': 48,
            'Dock': 'Top',
            'BackColor': Win11Colors.COMMAND_BG
        })
        
        # Command buttons - Manual layout is fine for toolbars with fixed items
        commands = [
            ('✂', 'Cut'),
            ('📋', 'Copy'),
            ('📄', 'Paste'),
            ('✏', 'Rename'),
            ('🗑', 'Delete'),
            ('│', None),  # Separator
            ('📁', 'New Folder'),
            ('│', None),
            ('↕', 'Sort'),
            ('👁', 'View'),
            ('│', None),
            ('⋯', 'More'),
        ]
        
        x = 10
        for icon, tooltip in commands:
            if tooltip is None:
                # Separator
                sep = Label(self.command_bar, {
                    'Text': '│',
                    'Left': x,
                    'Top': 10,
                    'Width': 10,
                    'Height': 28,
                    'ForeColor': Win11Colors.CONTENT_BORDER,
                    'BackColor': Win11Colors.COMMAND_BG
                })
                x += 15
            else:
                btn = Button(self.command_bar, {
                    'Text': icon,
                    'Left': x,
                    'Top': 8,
                    'Width': 40,
                    'Height': 32,
                    'BackColor': Win11Colors.COMMAND_BG,
                    'ForeColor': Win11Colors.COMMAND_ICON,
                    'FlatStyle': 'Flat'
                })
                x += 45
        
        # New tab button (right side) - Position from right edge, anchor right
        self.btn_new_tab = Button(self.command_bar, {
            'Text': '+',
            'Width': 40,
            'Height': 32,
            'Left': 1150,
            'Top': 8,
            'BackColor': Win11Colors.COMMAND_BG,
            'ForeColor': Win11Colors.COMMAND_ICON,
            'FlatStyle': 'Flat',
            'Anchor': AnchorStyles.Top | AnchorStyles.Right
        })
        self.btn_new_tab.Click = lambda s, e: self.new_tab()
    
    def _create_status_bar(self):
        """Create the status bar."""
        self.status_bar = Panel(self.form, {
            'Height': 26,
            'Dock': 'Bottom',
            'BackColor': Win11Colors.STATUS_BG
        })
        
        # Item count
        self.lbl_items = Label(self.status_bar, {
            'Text': '6 items',
            'Left': 10,
            'Top': 5,
            'Width': 100,
            'Height': 18,
            'ForeColor': Win11Colors.STATUS_TEXT,
            'BackColor': Win11Colors.STATUS_BG
        })
        
        # Selected count
        self.lbl_selected = Label(self.status_bar, {
            'Text': '',
            'Left': 120,
            'Top': 5,
            'Width': 150,
            'Height': 18,
            'ForeColor': Win11Colors.STATUS_TEXT,
            'BackColor': Win11Colors.STATUS_BG
        })
        
        # View buttons (right side) - Anchor Right so they stay on the edge
        self.btn_details = Button(self.status_bar, {
            'Text': '☰',
            'Left': 1100,
            'Top': 2,
            'Width': 30,
            'Height': 22,
            'BackColor': Win11Colors.STATUS_BG,
            'ForeColor': Win11Colors.STATUS_TEXT,
            'FlatStyle': 'Flat',
            'Anchor': AnchorStyles.Top | AnchorStyles.Right
        })
        
        self.btn_icons = Button(self.status_bar, {
            'Text': '▦',
            'Left': 1135,
            'Top': 2,
            'Width': 30,
            'Height': 22,
            'BackColor': Win11Colors.STATUS_BG,
            'ForeColor': Win11Colors.STATUS_TEXT,
            'FlatStyle': 'Flat',
            'Anchor': AnchorStyles.Top | AnchorStyles.Right
        })
    
    def _create_main_container(self):
        """Create main container with navigation pane and content."""
        self.main_container = Panel(self.form, {
            'Dock': 'Fill',
            'BackColor': Win11Colors.BG_MICA
        })
        
        # IMPORTANT: Create Nav Pane (Dock Left) BEFORE Tab Area (Dock Fill)
        # so the Fill control respects the Left space
        self._create_nav_pane()
        
        # Tab area fills remaining space
        self._create_tab_area()
    
    def _create_nav_pane(self):
        """Create the navigation pane."""
        self.nav_pane = Panel(self.main_container, {
            'Width': 220,
            'Dock': 'Left',
            'BackColor': Win11Colors.NAV_BG
        })
        
        # Quick Access section
        sections = [
            ('📌 Quick access', [
                '  📁 Desktop',
                '  📥 Downloads',
                '  📄 Documents',
                '  🖼 Pictures',
            ]),
            ('💻 This PC', [
                '  💿 Local Disk (C:)',
                '  💿 Data (D:)',
            ]),
            ('🌐 Network', []),
        ]
        
        y = 10
        for section_title, items in sections:
            # Section header
            lbl_section = Label(self.nav_pane, {
                'Text': section_title,
                'Left': 10,
                'Top': y,
                'Width': 200,
                'Height': 24,
                'ForeColor': Win11Colors.NAV_TEXT,
                'BackColor': Win11Colors.NAV_BG
            })
            y += 28
            
            # Section items
            for item in items:
                btn_item = Button(self.nav_pane, {
                    'Text': item,
                    'Left': 5,
                    'Top': y,
                    'Width': 210,
                    'Height': 28,
                    'BackColor': Win11Colors.NAV_BG,
                    'ForeColor': Win11Colors.NAV_TEXT,
                    'FlatStyle': 'Flat',
                    'TextAlign': 'MiddleLeft'
                })
                
                # Navigate on click
                folder_name = item.strip().split(' ', 1)[-1]
                btn_item.Click = lambda s, e, fn=folder_name: self._navigate_to_folder(fn)
                y += 28
            
            y += 10
    
    def _navigate_to_folder(self, folder_name):
        """Navigate current tab to a folder."""
        if self.current_tab:
            if folder_name in ['Desktop', 'Downloads', 'Documents', 'Pictures']:
                path = os.path.expanduser(f"~/{folder_name}")
            elif 'Local Disk' in folder_name or '(:)' in folder_name:
                path = folder_name[-3:-1] + '\\'
            else:
                path = folder_name
            self.current_tab.navigate(path)
    
    def _create_tab_area(self):
        """Create the tabbed content area."""
        self.tab_area = Panel(self.main_container, {
            'Dock': 'Fill',
            'BackColor': Win11Colors.TAB_BG
        })
        
        # Tab control
        self.tab_control = TabControl(self.tab_area, {
            'Dock': 'Fill',
            'BackColor': Win11Colors.TAB_BG
        })
        
        self.tab_control.SelectedIndexChanged = self._on_tab_changed
    
    def new_tab(self, path="This PC"):
        """Create a new explorer tab."""
        tab = ExplorerTab(self.tab_control, path=path)
        self.tabs.append(tab)
        
        # Select the new tab
        self.tab_control.SelectedIndex = len(self.tabs) - 1
        self.current_tab = tab
        self._update_title()
        
        return tab
    
    def close_tab(self, tab):
        """Close a tab."""
        if tab in self.tabs:
            index = self.tabs.index(tab)
            self.tabs.remove(tab)
            
            if self.tabs:
                new_index = min(index, len(self.tabs) - 1)
                self.tab_control.SelectedIndex = new_index
                self.current_tab = self.tabs[new_index]
            else:
                # Open a new tab if all closed
                self.new_tab()
            
            self._update_title()
    
    def _on_tab_changed(self, sender, e):
        """Handle tab change."""
        index = self.tab_control.SelectedIndex
        if 0 <= index < len(self.tabs):
            self.current_tab = self.tabs[index]
            self._update_title()
    
    def _update_title(self):
        """Update window title."""
        if self.current_tab:
            self.form.Text = f'{self.current_tab.path} - File Explorer'
        else:
            self.form.Text = 'File Explorer'
    
    def run(self):
        """Run the application."""
        self.form.ShowDialog()


def main():
    """Application entry point."""
    app = ExplorerApp()
    app.run()


if __name__ == "__main__":
    main()
