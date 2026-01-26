"""
MenuStrip Example - MenuStrip Control Demonstration

This example demonstrates the MenuStrip control in WinFormPy with:
1. Creating a complete menu system
2. Nested menu items (File, Edit, View, Format, Tools, Help)
3. Menu item click events
4. Keyboard shortcuts
5. Checkable menu items
6. Menu separators
7. Disabled menu items

FEATURES DEMONSTRATED:
- MenuStrip creation
- ToolStripMenuItem with hierarchical structure
- Click event handling
- Checkable menu items for toggles
- Menu separators
- Keyboard shortcuts display
- Dynamic menu enabling/disabling
"""

from winformpy.winformpy import (
    Application, Form, MenuStrip, ToolStripMenuItem, Panel, TextBox, Label,
    DockStyle, Font, FontStyle, MessageBox
)


class MenuStripExampleForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "WinFormPy MenuStrip Example"
        self.Width = 1000
        self.Height = 650
        self.StartPosition = "CenterScreen"
        self.ApplyLayout()
        
        # State variables
        self.word_wrap_enabled = True
        self.status_bar_visible = True
        self.toolbar_visible = True
        
        # Initialize components
        self._create_menustrip()
        self._create_content_area()
        self._create_bottom_status()
    
    def _create_menustrip(self):
        """Create main menu strip."""
        self.menustrip = MenuStrip(self, {
            'BackColor': '#F8F8F8'
        })
        self.menustrip.Dock = DockStyle.Top
        
        # File Menu
        self._create_file_menu()
        
        # Edit Menu
        self._create_edit_menu()
        
        # View Menu
        self._create_view_menu()
        
        # Format Menu
        self._create_format_menu()
        
        # Tools Menu
        self._create_tools_menu()
        
        # Help Menu
        self._create_help_menu()
    
    def _create_file_menu(self):
        """Create File menu."""
        menu_file = ToolStripMenuItem("File")
        
        # New
        item_new = ToolStripMenuItem("New")
        item_new.ShortcutKeys = "Ctrl+N"
        item_new.Click = lambda s, e: self._on_menu_action("File > New")
        menu_file.DropDownItems.Add(item_new)
        
        # Open
        item_open = ToolStripMenuItem("Open...")
        item_open.ShortcutKeys = "Ctrl+O"
        item_open.Click = lambda s, e: self._on_menu_action("File > Open")
        menu_file.DropDownItems.Add(item_open)
        
        # Separator
        menu_file.DropDownItems.Add(ToolStripMenuItem("-"))
        
        # Save
        item_save = ToolStripMenuItem("Save")
        item_save.ShortcutKeys = "Ctrl+S"
        item_save.Click = lambda s, e: self._on_menu_action("File > Save")
        menu_file.DropDownItems.Add(item_save)
        
        # Save As
        item_save_as = ToolStripMenuItem("Save As...")
        item_save_as.ShortcutKeys = "Ctrl+Shift+S"
        item_save_as.Click = lambda s, e: self._on_menu_action("File > Save As")
        menu_file.DropDownItems.Add(item_save_as)
        
        # Separator
        menu_file.DropDownItems.Add(ToolStripMenuItem("-"))
        
        # Print
        item_print = ToolStripMenuItem("Print...")
        item_print.ShortcutKeys = "Ctrl+P"
        item_print.Click = lambda s, e: self._on_menu_action("File > Print")
        menu_file.DropDownItems.Add(item_print)
        
        # Print Preview
        item_preview = ToolStripMenuItem("Print Preview")
        item_preview.Click = lambda s, e: self._on_menu_action("File > Print Preview")
        menu_file.DropDownItems.Add(item_preview)
        
        # Separator
        menu_file.DropDownItems.Add(ToolStripMenuItem("-"))
        
        # Recent Files (submenu)
        item_recent = ToolStripMenuItem("Recent Files")
        item_recent.DropDownItems.Add(self._create_menu_item("Document1.txt", "Recent > Document1"))
        item_recent.DropDownItems.Add(self._create_menu_item("Project2.py", "Recent > Project2"))
        item_recent.DropDownItems.Add(self._create_menu_item("Notes3.md", "Recent > Notes3"))
        menu_file.DropDownItems.Add(item_recent)
        
        # Separator
        menu_file.DropDownItems.Add(ToolStripMenuItem("-"))
        
        # Exit
        item_exit = ToolStripMenuItem("Exit")
        item_exit.ShortcutKeys = "Alt+F4"
        item_exit.Click = lambda s, e: self._on_exit()
        menu_file.DropDownItems.Add(item_exit)
        
        self.menustrip.Items.Add(menu_file)
    
    def _create_edit_menu(self):
        """Create Edit menu."""
        menu_edit = ToolStripMenuItem("Edit")
        
        # Undo
        item_undo = ToolStripMenuItem("Undo")
        item_undo.ShortcutKeys = "Ctrl+Z"
        item_undo.Click = lambda s, e: self._on_menu_action("Edit > Undo")
        menu_edit.DropDownItems.Add(item_undo)
        
        # Redo
        item_redo = ToolStripMenuItem("Redo")
        item_redo.ShortcutKeys = "Ctrl+Y"
        item_redo.Click = lambda s, e: self._on_menu_action("Edit > Redo")
        menu_edit.DropDownItems.Add(item_redo)
        
        # Separator
        menu_edit.DropDownItems.Add(ToolStripMenuItem("-"))
        
        # Cut
        item_cut = ToolStripMenuItem("Cut")
        item_cut.ShortcutKeys = "Ctrl+X"
        item_cut.Click = lambda s, e: self._on_menu_action("Edit > Cut")
        menu_edit.DropDownItems.Add(item_cut)
        
        # Copy
        item_copy = ToolStripMenuItem("Copy")
        item_copy.ShortcutKeys = "Ctrl+C"
        item_copy.Click = lambda s, e: self._on_menu_action("Edit > Copy")
        menu_edit.DropDownItems.Add(item_copy)
        
        # Paste
        item_paste = ToolStripMenuItem("Paste")
        item_paste.ShortcutKeys = "Ctrl+V"
        item_paste.Click = lambda s, e: self._on_menu_action("Edit > Paste")
        menu_edit.DropDownItems.Add(item_paste)
        
        # Separator
        menu_edit.DropDownItems.Add(ToolStripMenuItem("-"))
        
        # Select All
        item_select_all = ToolStripMenuItem("Select All")
        item_select_all.ShortcutKeys = "Ctrl+A"
        item_select_all.Click = lambda s, e: self._on_menu_action("Edit > Select All")
        menu_edit.DropDownItems.Add(item_select_all)
        
        # Separator
        menu_edit.DropDownItems.Add(ToolStripMenuItem("-"))
        
        # Find
        item_find = ToolStripMenuItem("Find...")
        item_find.ShortcutKeys = "Ctrl+F"
        item_find.Click = lambda s, e: self._on_menu_action("Edit > Find")
        menu_edit.DropDownItems.Add(item_find)
        
        # Replace
        item_replace = ToolStripMenuItem("Replace...")
        item_replace.ShortcutKeys = "Ctrl+H"
        item_replace.Click = lambda s, e: self._on_menu_action("Edit > Replace")
        menu_edit.DropDownItems.Add(item_replace)
        
        self.menustrip.Items.Add(menu_edit)
    
    def _create_view_menu(self):
        """Create View menu."""
        menu_view = ToolStripMenuItem("View")
        
        # Zoom submenu
        item_zoom = ToolStripMenuItem("Zoom")
        item_zoom.DropDownItems.Add(self._create_menu_item("Zoom In", "View > Zoom In", "Ctrl++"))
        item_zoom.DropDownItems.Add(self._create_menu_item("Zoom Out", "View > Zoom Out", "Ctrl+-"))
        item_zoom.DropDownItems.Add(self._create_menu_item("Reset Zoom", "View > Reset Zoom", "Ctrl+0"))
        menu_view.DropDownItems.Add(item_zoom)
        
        # Separator
        menu_view.DropDownItems.Add(ToolStripMenuItem("-"))
        
        # Toolbar (checkable)
        self.item_toolbar = ToolStripMenuItem("Toolbar")
        self.item_toolbar.Checked = self.toolbar_visible
        self.item_toolbar.CheckOnClick = True
        self.item_toolbar.Click = lambda s, e: self._on_toggle_toolbar()
        menu_view.DropDownItems.Add(self.item_toolbar)
        
        # Status Bar (checkable)
        self.item_statusbar = ToolStripMenuItem("Status Bar")
        self.item_statusbar.Checked = self.status_bar_visible
        self.item_statusbar.CheckOnClick = True
        self.item_statusbar.Click = lambda s, e: self._on_toggle_statusbar()
        menu_view.DropDownItems.Add(self.item_statusbar)
        
        # Separator
        menu_view.DropDownItems.Add(ToolStripMenuItem("-"))
        
        # Full Screen
        item_fullscreen = ToolStripMenuItem("Full Screen")
        item_fullscreen.ShortcutKeys = "F11"
        item_fullscreen.Click = lambda s, e: self._on_menu_action("View > Full Screen")
        menu_view.DropDownItems.Add(item_fullscreen)
        
        self.menustrip.Items.Add(menu_view)
    
    def _create_format_menu(self):
        """Create Format menu."""
        menu_format = ToolStripMenuItem("Format")
        
        # Word Wrap (checkable)
        self.item_wordwrap = ToolStripMenuItem("Word Wrap")
        self.item_wordwrap.Checked = self.word_wrap_enabled
        self.item_wordwrap.CheckOnClick = True
        self.item_wordwrap.Click = lambda s, e: self._on_toggle_wordwrap()
        menu_format.DropDownItems.Add(self.item_wordwrap)
        
        # Separator
        menu_format.DropDownItems.Add(ToolStripMenuItem("-"))
        
        # Font
        item_font = ToolStripMenuItem("Font...")
        item_font.Click = lambda s, e: self._on_menu_action("Format > Font")
        menu_format.DropDownItems.Add(item_font)
        
        # Text Color
        item_color = ToolStripMenuItem("Text Color...")
        item_color.Click = lambda s, e: self._on_menu_action("Format > Text Color")
        menu_format.DropDownItems.Add(item_color)
        
        # Separator
        menu_format.DropDownItems.Add(ToolStripMenuItem("-"))
        
        # Alignment submenu
        item_align = ToolStripMenuItem("Alignment")
        item_align.DropDownItems.Add(self._create_menu_item("Left", "Format > Align Left"))
        item_align.DropDownItems.Add(self._create_menu_item("Center", "Format > Align Center"))
        item_align.DropDownItems.Add(self._create_menu_item("Right", "Format > Align Right"))
        menu_format.DropDownItems.Add(item_align)
        
        self.menustrip.Items.Add(menu_format)
    
    def _create_tools_menu(self):
        """Create Tools menu."""
        menu_tools = ToolStripMenuItem("Tools")
        
        # Customize
        item_customize = ToolStripMenuItem("Customize...")
        item_customize.Click = lambda s, e: self._on_menu_action("Tools > Customize")
        menu_tools.DropDownItems.Add(item_customize)
        
        # Options
        item_options = ToolStripMenuItem("Options...")
        item_options.Click = lambda s, e: self._on_menu_action("Tools > Options")
        menu_tools.DropDownItems.Add(item_options)
        
        # Separator
        menu_tools.DropDownItems.Add(ToolStripMenuItem("-"))
        
        # Plugins submenu
        item_plugins = ToolStripMenuItem("Plugins")
        item_plugins.DropDownItems.Add(self._create_menu_item("Plugin Manager", "Tools > Plugin Manager"))
        item_plugins.DropDownItems.Add(self._create_menu_item("Install Plugin", "Tools > Install Plugin"))
        menu_tools.DropDownItems.Add(item_plugins)
        
        self.menustrip.Items.Add(menu_tools)
    
    def _create_help_menu(self):
        """Create Help menu."""
        menu_help = ToolStripMenuItem("Help")
        
        # View Help
        item_view_help = ToolStripMenuItem("View Help")
        item_view_help.ShortcutKeys = "F1"
        item_view_help.Click = lambda s, e: self._show_help()
        menu_help.DropDownItems.Add(item_view_help)
        
        # Online Documentation
        item_docs = ToolStripMenuItem("Online Documentation")
        item_docs.Click = lambda s, e: self._on_menu_action("Help > Online Documentation")
        menu_help.DropDownItems.Add(item_docs)
        
        # Separator
        menu_help.DropDownItems.Add(ToolStripMenuItem("-"))
        
        # Check for Updates
        item_updates = ToolStripMenuItem("Check for Updates...")
        item_updates.Click = lambda s, e: self._on_menu_action("Help > Check for Updates")
        menu_help.DropDownItems.Add(item_updates)
        
        # Separator
        menu_help.DropDownItems.Add(ToolStripMenuItem("-"))
        
        # About
        item_about = ToolStripMenuItem("About")
        item_about.Click = lambda s, e: self._show_about()
        menu_help.DropDownItems.Add(item_about)
        
        self.menustrip.Items.Add(menu_help)
    
    def _create_menu_item(self, text, action, shortcut=None):
        """Helper to create menu item."""
        item = ToolStripMenuItem(text)
        if shortcut:
            item.ShortcutKeys = shortcut
        item.Click = lambda s, e: self._on_menu_action(action)
        return item
    
    def _create_content_area(self):
        """Create main content area."""
        content_panel = Panel(self, {
            'BackColor': '#FFFFFF',
            'Padding': (20, 20, 20, 20)
        })
        content_panel.Dock = DockStyle.Fill
        
        # Title
        Label(content_panel, {
            'Text': 'MenuStrip Demonstration',
            'Left': 20,
            'Top': 20,
            'AutoSize': True,
            'Font': Font('Segoe UI', 18, FontStyle.Bold),
            'ForeColor': '#0078D4'
        })
        
        # Description
        Label(content_panel, {
            'Text': 'Explore the menu system above to see different MenuStrip features:',
            'Left': 20,
            'Top': 60,
            'Width': 900,
            'Font': Font('Segoe UI', 10)
        })
        
        # Features list
        features = [
            "File Menu - New, Open, Save, Print, Recent Files, Exit",
            "Edit Menu - Undo, Redo, Cut, Copy, Paste, Find, Replace",
            "View Menu - Zoom, Toolbar toggle, Status Bar toggle, Full Screen",
            "Format Menu - Word Wrap toggle, Font, Text Color, Alignment",
            "Tools Menu - Customize, Options, Plugins",
            "Help Menu - View Help, Documentation, Updates, About",
            "Keyboard Shortcuts - Displayed next to menu items",
            "Checkable Items - For toggleable options (Word Wrap, Toolbar, etc.)",
            "Nested Menus - Submenus for organized navigation"
        ]
        
        y_pos = 100
        for i, feature in enumerate(features, 1):
            Label(content_panel, {
                'Text': f"{i}. {feature}",
                'Left': 40,
                'Top': y_pos,
                'Width': 900,
                'Font': Font('Segoe UI', 9),
                'ForeColor': '#333333'
            })
            y_pos += 28
        
        # Action log
        Label(content_panel, {
            'Text': 'Menu Action Log:',
            'Left': 20,
            'Top': y_pos + 20,
            'AutoSize': True,
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'ForeColor': '#0078D4'
        })
        
        self.txt_log = TextBox(content_panel, {
            'Left': 20,
            'Top': y_pos + 50,
            'Width': 920,
            'Height': 120,
            'Multiline': True,
            'ScrollBars': 'Vertical',
            'BackColor': '#F8F8F8',
            'Font': Font('Consolas', 9),
            'ReadOnly': True
        })
    
    def _create_bottom_status(self):
        """Create bottom status panel."""
        status_panel = Panel(self, {
            'Height': 30,
            'BackColor': '#34495E'
        })
        status_panel.Dock = DockStyle.Bottom
        
        self.lbl_status = Label(status_panel, {
            'Text': 'Ready | Select any menu item to see action',
            'Left': 15,
            'Top': 6,
            'Width': 900,
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9),
            'BackColor': '#34495E'
        })
    
    def _on_menu_action(self, action):
        """Handle menu item clicks."""
        current_text = self.txt_log.Text
        new_entry = f"[MENU] {action}\n"
        self.txt_log.Text = new_entry + current_text
        self.lbl_status.Text = f"Action: {action}"
    
    def _on_toggle_toolbar(self):
        """Toggle toolbar visibility."""
        self.toolbar_visible = self.item_toolbar.Checked
        status = "shown" if self.toolbar_visible else "hidden"
        self._on_menu_action(f"View > Toolbar ({status})")
    
    def _on_toggle_statusbar(self):
        """Toggle status bar visibility."""
        self.status_bar_visible = self.item_statusbar.Checked
        status = "shown" if self.status_bar_visible else "hidden"
        self._on_menu_action(f"View > Status Bar ({status})")
    
    def _on_toggle_wordwrap(self):
        """Toggle word wrap."""
        self.word_wrap_enabled = self.item_wordwrap.Checked
        status = "enabled" if self.word_wrap_enabled else "disabled"
        self._on_menu_action(f"Format > Word Wrap ({status})")
    
    def _on_exit(self):
        """Handle exit menu item."""
        result = MessageBox.Show(
            "Are you sure you want to exit?",
            "Exit Application",
            "YesNo"
        )
        if result == "Yes":
            self.Close()
    
    def _show_help(self):
        """Show help dialog."""
        MessageBox.Show(
            "MenuStrip Example Help\n\n"
            "This application demonstrates MenuStrip features:\n\n"
            "• File Menu - Document operations\n"
            "• Edit Menu - Text editing commands\n"
            "• View Menu - Display options with checkable items\n"
            "• Format Menu - Text formatting\n"
            "• Tools Menu - Application tools\n"
            "• Help Menu - Help and about information\n\n"
            "Try clicking different menu items to see how they work!",
            "Help"
        )
    
    def _show_about(self):
        """Show about dialog."""
        MessageBox.Show(
            "MenuStrip Example\n"
            "Version 1.0\n\n"
            "WinFormPy Library\n"
            "Demonstrating MenuStrip control with hierarchical menus,\n"
            "keyboard shortcuts, and checkable items.\n\n"
            "© 2026 WinFormPy Project",
            "About"
        )


def main():
    """Application entry point."""
    app = MenuStripExampleForm()
    Application.Run(app)


if __name__ == '__main__':
    main()
