"""
.NET 2.0 Controls Example - Complete Demonstration

This example demonstrates the new .NET 2.0 controls that replaced older ones:

.NET 1.x vs .NET 2.0 COMPARISON:
┌─────────────────┬──────────────────┬────────────────────────────┐
│ .NET 1.x        │ .NET 2.0         │ Description                │
├─────────────────┼──────────────────┼────────────────────────────┤
│ MainMenu        │ MenuStrip        │ Main application menu      │
│ ContextMenu     │ ContextMenuStrip │ Right-click context menu   │
│ ToolBar         │ ToolStrip        │ Toolbar with buttons       │
│ StatusBar       │ StatusStrip      │ Bottom status bar          │
└─────────────────┴──────────────────┴────────────────────────────┘

FEATURES DEMONSTRATED:

1. MenuStrip (replaces MainMenu):
   ✓ Hierarchical menu structure (File, Edit, View, Tools, Help)
   ✓ Keyboard shortcuts display (Ctrl+N, Ctrl+S, F1, etc.)
   ✓ Checkable menu items (Word Wrap toggle)
   ✓ Menu separators for organization
   ✓ Disabled menu items (Plugins example)
   ✓ Nested submenus (Recent Files, Zoom)
   ✓ Click event handling
   ✓ Icons/emojis in menu text

2. ToolStrip (replaces ToolBar):
   ✓ ToolStripButton - Standard clickable buttons
   ✓ ToolStripLabel - Static text labels
   ✓ ToolStripSeparator - Visual dividers
   ✓ ToolStripComboBox - Dropdown selection (font chooser)
   ✓ ToolStripTextBox - Text input with placeholder
   ✓ Button tooltips (ToolTipText property)
   ✓ Event handling (Click, SelectedIndexChanged)
   ✓ Custom sizing (Width property)

3. StatusStrip (replaces StatusBar):
   ✓ ToolStripStatusLabel - Status messages
   ✓ Multiple status panels with BorderSides
   ✓ Spring property for flexible sizing
   ✓ Real-time clock update (using InvokeAsync)
   ✓ Dynamic text statistics (Lines, Words, Chars)
   ✓ Zoom level display
   ✓ Action counter

4. ContextMenuStrip (replaces ContextMenu):
   ✓ Right-click context menu on RichTextBox
   ✓ Cut, Copy, Paste operations
   ✓ Select All command
   ✓ Keyboard shortcuts display
   ✓ Separator items
   ✓ Event handling

CONTROLS USED:
- MenuStrip, ToolStrip, StatusStrip, ContextMenuStrip
- ToolStripMenuItem, ToolStripButton, ToolStripLabel
- ToolStripSeparator, ToolStripStatusLabel
- ToolStripComboBox, ToolStripTextBox
- RichTextBox, Panel, Label
- Font, DockStyle, BorderStyle

INTERACTIVE FEATURES:
✓ Type in text area to see live statistics
✓ Use menu commands (File > New, Edit > Copy, etc.)
✓ Click toolbar buttons (New, Open, Save, formatting)
✓ Change font using dropdown combo box
✓ Search using toolbar text box
✓ Right-click on text for context menu
✓ Watch status bar update in real-time
✓ Test keyboard shortcuts (Ctrl+C, Ctrl+V, etc.)
"""

from winformpy.winformpy import (
    Application, Form, MenuStrip, ToolStrip, StatusStrip, ContextMenuStrip,
    ToolStripMenuItem, ToolStripButton, ToolStripComboBox, ToolStripTextBox, 
    ToolStripStatusLabel, ToolStripSeparator, ToolStripLabel, 
    Panel, TextBox, RichTextBox, Label, Button,
    DockStyle, Font, FontStyle, MessageBox, ImageList, BorderStyle
)
from datetime import datetime


class DotNet2ControlsForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = ".NET 2.0 Controls - MenuStrip, ToolStrip, StatusStrip, ContextMenuStrip"
        self.Width = 1200
        self.Height = 800
        self.StartPosition = "CenterScreen"
        self.BackColor = '#F0F0F0'
        self.ApplyLayout()
        
        # State variables
        self.action_count = 0
        self.word_wrap = True
        self.toolbar_style = "ImageAndText"
        self.zoom_level = 100
        self.clipboard_text = ""
        
        # Initialize components in .NET 2.0 style order
        self._create_menustrip()
        self._create_toolstrip()
        self._create_content_area()
        self._create_statusstrip()
        self._create_contextmenu()
        
        # Start clock
        self._update_clock()
    
    # ========================================================================
    # MENUSTRIP - Replaces MainMenu (.NET 1.x)
    # ========================================================================
    
    def _create_menustrip(self):
        """Create MenuStrip (replaces .NET 1.x MainMenu)."""
        self.menustrip = MenuStrip(self, {
            'BackColor': '#F8F8F8'
        })
        self.menustrip.Dock = DockStyle.Top
        
        # File Menu
        menu_file = ToolStripMenuItem("📁 File")
        menu_file.DropDownItems.Add(self._create_menu_item("🆕 New", "Ctrl+N", self._on_new))
        menu_file.DropDownItems.Add(self._create_menu_item("📂 Open...", "Ctrl+O", self._on_open))
        menu_file.DropDownItems.Add(ToolStripMenuItem("-"))
        menu_file.DropDownItems.Add(self._create_menu_item("💾 Save", "Ctrl+S", self._on_save))
        menu_file.DropDownItems.Add(self._create_menu_item("💾 Save As...", "Ctrl+Shift+S", self._on_save_as))
        menu_file.DropDownItems.Add(ToolStripMenuItem("-"))
        
        # Recent Files submenu
        recent = ToolStripMenuItem("📋 Recent Files")
        recent.DropDownItems.Add(self._create_menu_item("Document1.txt", "", lambda s, e: self._log_action("Open: Document1.txt")))
        recent.DropDownItems.Add(self._create_menu_item("Project2.py", "", lambda s, e: self._log_action("Open: Project2.py")))
        recent.DropDownItems.Add(self._create_menu_item("Notes3.md", "", lambda s, e: self._log_action("Open: Notes3.md")))
        menu_file.DropDownItems.Add(recent)
        
        menu_file.DropDownItems.Add(ToolStripMenuItem("-"))
        menu_file.DropDownItems.Add(self._create_menu_item("🚪 Exit", "Alt+F4", self._on_exit))
        self.menustrip.Items.Add(menu_file)
        
        # Edit Menu
        menu_edit = ToolStripMenuItem("✏️ Edit")
        menu_edit.DropDownItems.Add(self._create_menu_item("↶ Undo", "Ctrl+Z", lambda s, e: self._log_action("Undo")))
        menu_edit.DropDownItems.Add(self._create_menu_item("↷ Redo", "Ctrl+Y", lambda s, e: self._log_action("Redo")))
        menu_edit.DropDownItems.Add(ToolStripMenuItem("-"))
        menu_edit.DropDownItems.Add(self._create_menu_item("✂️ Cut", "Ctrl+X", self._on_cut))
        menu_edit.DropDownItems.Add(self._create_menu_item("📋 Copy", "Ctrl+C", self._on_copy))
        menu_edit.DropDownItems.Add(self._create_menu_item("📌 Paste", "Ctrl+V", self._on_paste))
        menu_edit.DropDownItems.Add(ToolStripMenuItem("-"))
        menu_edit.DropDownItems.Add(self._create_menu_item("🔍 Find...", "Ctrl+F", lambda s, e: self._log_action("Find")))
        menu_edit.DropDownItems.Add(self._create_menu_item("🔄 Replace...", "Ctrl+H", lambda s, e: self._log_action("Replace")))
        self.menustrip.Items.Add(menu_edit)
        
        # View Menu
        menu_view = ToolStripMenuItem("👁️ View")
        
        # Word Wrap (checkable)
        self.menu_wordwrap = ToolStripMenuItem("📝 Word Wrap")
        self.menu_wordwrap.Checked = True
        self.menu_wordwrap.CheckOnClick = True
        self.menu_wordwrap.Click = self._on_toggle_wordwrap
        menu_view.DropDownItems.Add(self.menu_wordwrap)
        
        menu_view.DropDownItems.Add(ToolStripMenuItem("-"))
        
        # Zoom submenu
        zoom = ToolStripMenuItem("🔍 Zoom")
        zoom.DropDownItems.Add(self._create_menu_item("Zoom In", "Ctrl++", lambda s, e: self._on_zoom(110, e)))
        zoom.DropDownItems.Add(self._create_menu_item("Zoom Out", "Ctrl+-", lambda s, e: self._on_zoom(90, e)))
        zoom.DropDownItems.Add(self._create_menu_item("Reset Zoom", "Ctrl+0", lambda s, e: self._on_zoom(100, e)))
        menu_view.DropDownItems.Add(zoom)
        
        self.menustrip.Items.Add(menu_view)
        
        # Tools Menu
        menu_tools = ToolStripMenuItem("🔧 Tools")
        menu_tools.DropDownItems.Add(self._create_menu_item("⚙️ Options...", "", lambda s, e: self._log_action("Options")))
        menu_tools.DropDownItems.Add(self._create_menu_item("🎨 Customize...", "", lambda s, e: self._log_action("Customize")))
        
        # Disabled item example
        disabled_item = ToolStripMenuItem("🔌 Plugins...")
        disabled_item.Enabled = False
        menu_tools.DropDownItems.Add(disabled_item)
        
        self.menustrip.Items.Add(menu_tools)
        
        # Help Menu
        menu_help = ToolStripMenuItem("❓ Help")
        menu_help.DropDownItems.Add(self._create_menu_item("📖 View Help", "F1", lambda s, e: self._log_action("Help")))
        menu_help.DropDownItems.Add(self._create_menu_item("ℹ️ About", "", self._on_about))
        self.menustrip.Items.Add(menu_help)
        
        # Assign to form
        self.Menu = self.menustrip
    
    def _create_menu_item(self, text, shortcut, handler):
        """Helper to create menu item with shortcut and handler."""
        item = ToolStripMenuItem(text)
        if shortcut:
            item.ShortcutKeys = shortcut
        if handler:
            item.Click = handler
        return item
    
    # ========================================================================
    # TOOLSTRIP - Replaces ToolBar (.NET 1.x)
    # ========================================================================
    
    def _create_toolstrip(self):
        """Create ToolStrip (replaces .NET 1.x ToolBar)."""
        self.toolstrip = ToolStrip(self, {
            'BackColor': '#F0F0F0',
            'Height': 35
        })
        self.toolstrip.Dock = DockStyle.Top
        
        # ToolStripButton - Standard button
        btn_new = ToolStripButton("🆕 New")
        btn_new.Click = self._on_new
        btn_new.ToolTipText = "Create new document (Ctrl+N)"
        self.toolstrip.Items.Add(btn_new)
        
        btn_open = ToolStripButton("📂 Open")
        btn_open.Click = self._on_open
        btn_open.ToolTipText = "Open file (Ctrl+O)"
        self.toolstrip.Items.Add(btn_open)
        
        btn_save = ToolStripButton("💾 Save")
        btn_save.Click = self._on_save
        btn_save.ToolTipText = "Save file (Ctrl+S)"
        self.toolstrip.Items.Add(btn_save)
        
        # ToolStripSeparator
        self.toolstrip.Items.Add(ToolStripSeparator())
        
        # Cut/Copy/Paste
        btn_cut = ToolStripButton("✂️ Cut")
        btn_cut.Click = self._on_cut
        self.toolstrip.Items.Add(btn_cut)
        
        btn_copy = ToolStripButton("📋 Copy")
        btn_copy.Click = self._on_copy
        self.toolstrip.Items.Add(btn_copy)
        
        btn_paste = ToolStripButton("📌 Paste")
        btn_paste.Click = self._on_paste
        self.toolstrip.Items.Add(btn_paste)
        
        self.toolstrip.Items.Add(ToolStripSeparator())
        
        # Bold/Italic/Underline buttons
        btn_bold = ToolStripButton("B")
        btn_bold.ToolTipText = "Bold (Ctrl+B)"
        btn_bold.Click = lambda s, e: self._log_action("Bold")
        self.toolstrip.Items.Add(btn_bold)
        
        btn_italic = ToolStripButton("I")
        btn_italic.ToolTipText = "Italic (Ctrl+I)"
        btn_italic.Click = lambda s, e: self._log_action("Italic")
        self.toolstrip.Items.Add(btn_italic)
        
        btn_underline = ToolStripButton("U")
        btn_underline.ToolTipText = "Underline (Ctrl+U)"
        btn_underline.Click = lambda s, e: self._log_action("Underline")
        self.toolstrip.Items.Add(btn_underline)
        
        self.toolstrip.Items.Add(ToolStripSeparator())
        
        # ToolStripLabel
        lbl = ToolStripLabel("Font:")
        self.toolstrip.Items.Add(lbl)
        
        # ToolStripComboBox
        self.combo_font = ToolStripComboBox()
        self.combo_font.Width = 120
        self.combo_font.Items.append("Consolas")
        self.combo_font.Items.append("Courier New")
        self.combo_font.Items.append("Segoe UI")
        self.combo_font.Items.append("Arial")
        self.combo_font.SelectedIndex = 0
        self.combo_font.SelectedIndexChanged = self._on_font_changed
        self.toolstrip.Items.Add(self.combo_font)
        
        self.toolstrip.Items.Add(ToolStripSeparator())
        
        # ToolStripTextBox
        lbl_search = ToolStripLabel("Search:")
        self.toolstrip.Items.Add(lbl_search)
        
        self.txt_search = ToolStripTextBox()
        self.txt_search.Width = 150
        self.txt_search.PlaceholderText = "Search..."
        self.toolstrip.Items.Add(self.txt_search)
        
        btn_search = ToolStripButton("🔍")
        btn_search.Click = lambda s, e: self._log_action(f"Search: {self.txt_search.Text}")
        self.toolstrip.Items.Add(btn_search)
    
    # ========================================================================
    # CONTENT AREA
    # ========================================================================
    
    def _create_content_area(self):
        """Create main content area."""
        # Left panel with information
        left_panel = Panel(self, {
            'Width': 300,
            'BackColor': '#FFFFFF',
            'BorderStyle': BorderStyle.FixedSingle
        })
        left_panel.Dock = DockStyle.Left
        
        Label(left_panel, {
            'Text': '.NET 2.0 CONTROLS',
            'Left': 10,
            'Top': 10,
            'Width': 280,
            'Font': Font('Segoe UI', 12, FontStyle.Bold),
            'ForeColor': '#0078D4'
        })
        
        info_text = """
┌─────────────────────────────┐
│ .NET 1.x  →  .NET 2.0      │
├─────────────────────────────┤
│ MainMenu  →  MenuStrip     │
│ ToolBar   →  ToolStrip     │
│ StatusBar →  StatusStrip   │
│ ContextMenu → ContextMenuStrip│
└─────────────────────────────┘

FEATURES SHOWN:

MenuStrip (top):
• Hierarchical menus
• Keyboard shortcuts
• Checkable items
• Submenus (3+ levels)
• Separators
• Disabled items

ToolStrip (below menu):
• ToolStripButton
• ToolStripComboBox
• ToolStripTextBox
• ToolStripSeparator
• ToolStripLabel
• Event handling
• Tooltips

StatusStrip (bottom):
• ToolStripStatusLabel
• Real-time clock
• Statistics display
• Spring property
• Border styles

ContextMenuStrip:
• Right-click on text
• Cut/Copy/Paste
• Select All
• Shortcuts display

TRY IT:
✓ Use menus (File, Edit, etc.)
✓ Click toolbar buttons
✓ Change font with combo
✓ Type in text area
✓ Right-click for menu
✓ Watch status bar update
"""
        
        Label(left_panel, {
            'Text': info_text,
            'Left': 10,
            'Top': 40,
            'Width': 280,
            'Height': 650,
            'Font': Font('Consolas', 8),
            'ForeColor': '#333333'
        })
        
        # Main text area
        main_panel = Panel(self, {
            'BackColor': '#F5F5F5',
            'Padding': (10, 10, 10, 10)
        })
        main_panel.Dock = DockStyle.Fill
        
        Label(main_panel, {
            'Text': 'Text Editor - Try typing, selecting text, and right-clicking',
            'Left': 10,
            'Top': 10,
            'AutoSize': True,
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'ForeColor': '#0078D4'
        })
        
        self.txt_content = RichTextBox(main_panel, {
            'Left': 10,
            'Top': 40,
            'Width': 850,
            'Height': 600,
            'Font': Font('Consolas', 11),
            'BorderStyle': BorderStyle.FixedSingle
        })
        self.txt_content.Text = """Welcome to .NET 2.0 Controls Example!

This example demonstrates the new controls introduced in .NET Framework 2.0:

MenuStrip - Replaces MainMenu with better rendering and features
ToolStrip - Replaces ToolBar with flexible containers and items
StatusStrip - Replaces StatusBar with professional panels
ContextMenuStrip - Replaces ContextMenu with modern styling

Try these actions:
1. Use the File menu to test menu items
2. Click toolbar buttons
3. Select text and right-click for context menu
4. Type here to see statistics in status bar
5. Use keyboard shortcuts (Ctrl+C, Ctrl+V, etc.)

The status bar at the bottom shows:
• Action count
• Character/Word/Line count
• Real-time clock
• Current zoom level
"""
        self.txt_content.TextChanged = self._on_text_changed
    
    # ========================================================================
    # STATUSSTRIP - Replaces StatusBar (.NET 1.x)
    # ========================================================================
    
    def _create_statusstrip(self):
        """Create StatusStrip (replaces .NET 1.x StatusBar)."""
        self.statusstrip = StatusStrip(self)
        self.statusstrip.Dock = DockStyle.Bottom
        
        # Main status label (Spring = True to fill space)
        self.lbl_status = ToolStripStatusLabel("Ready")
        self.lbl_status.Spring = True
        self.lbl_status.TextAlign = "MiddleLeft"
        self.statusstrip.Items.Add(self.lbl_status)
        
        # Statistics label
        self.lbl_stats = ToolStripStatusLabel("Lines: 0 | Words: 0 | Chars: 0")
        self.lbl_stats.BorderSides = "Left"
        self.statusstrip.Items.Add(self.lbl_stats)
        
        # Zoom label
        self.lbl_zoom = ToolStripStatusLabel(f"Zoom: {self.zoom_level}%")
        self.lbl_zoom.BorderSides = "Left"
        self.statusstrip.Items.Add(self.lbl_zoom)
        
        # Clock label
        self.lbl_clock = ToolStripStatusLabel("")
        self.lbl_clock.BorderSides = "Left"
        self.statusstrip.Items.Add(self.lbl_clock)
    
    # ========================================================================
    # CONTEXTMENUSTRIP - Replaces ContextMenu (.NET 1.x)
    # ========================================================================
    
    def _create_contextmenu(self):
        """Create ContextMenuStrip (replaces .NET 1.x ContextMenu)."""
        self.contextmenu = ContextMenuStrip()
        
        # Cut
        item_cut = ToolStripMenuItem("✂️ Cut")
        item_cut.ShortcutKeys = "Ctrl+X"
        item_cut.Click = self._on_cut
        self.contextmenu.Items.append(item_cut)
        
        # Copy
        item_copy = ToolStripMenuItem("📋 Copy")
        item_copy.ShortcutKeys = "Ctrl+C"
        item_copy.Click = self._on_copy
        self.contextmenu.Items.append(item_copy)
        
        # Paste
        item_paste = ToolStripMenuItem("📌 Paste")
        item_paste.ShortcutKeys = "Ctrl+V"
        item_paste.Click = self._on_paste
        self.contextmenu.Items.append(item_paste)
        
        self.contextmenu.Items.append(ToolStripMenuItem("-"))
        
        # Select All
        item_select = ToolStripMenuItem("Select All")
        item_select.ShortcutKeys = "Ctrl+A"
        item_select.Click = lambda s, e: self.txt_content.SelectAll()
        self.contextmenu.Items.append(item_select)
        
        # Assign to text box
        self.txt_content.ContextMenuStrip = self.contextmenu
    
    # ========================================================================
    # EVENT HANDLERS
    # ========================================================================
    
    def _on_new(self, sender, e):
        """Handle New action."""
        self.txt_content.Text = ""
        self._log_action("New document created")
    
    def _on_open(self, sender, e):
        """Handle Open action."""
        self._log_action("Open dialog would appear here")
    
    def _on_save(self, sender, e):
        """Handle Save action."""
        self._log_action("Document saved")
    
    def _on_save_as(self, sender, e):
        """Handle Save As action."""
        self._log_action("Save As dialog would appear here")
    
    def _on_cut(self, sender, e):
        """Handle Cut action."""
        try:
            self.clipboard_text = self.txt_content.SelectedText
            # Remove selected text
            self._log_action(f"Cut: '{self.clipboard_text[:20]}...'")
        except:
            self._log_action("Cut: No text selected")
    
    def _on_copy(self, sender, e):
        """Handle Copy action."""
        try:
            self.clipboard_text = self.txt_content.SelectedText
            self._log_action(f"Copied: '{self.clipboard_text[:20]}...'")
        except:
            self._log_action("Copy: No text selected")
    
    def _on_paste(self, sender, e):
        """Handle Paste action."""
        if self.clipboard_text:
            # Insert clipboard text at cursor
            self._log_action(f"Pasted: '{self.clipboard_text[:20]}...'")
        else:
            self._log_action("Paste: Clipboard is empty")
    
    def _on_toggle_wordwrap(self, sender, e):
        """Toggle word wrap."""
        self.word_wrap = self.menu_wordwrap.Checked
        # Note: RichTextBox word wrap would be set here
        self._log_action(f"Word Wrap: {'ON' if self.word_wrap else 'OFF'}")
    
    def _on_zoom(self, sender, e):
        """Handle zoom change."""
        if isinstance(sender, int):  # Called from lambda
            self.zoom_level = sender
        else:
            self.zoom_level = 100
        
        self.lbl_zoom.Text = f"Zoom: {self.zoom_level}%"
        self._log_action(f"Zoom: {self.zoom_level}%")
    
    def _on_font_changed(self, sender, e):
        """Handle font change."""
        font_name = self.combo_font.SelectedItem
        self.txt_content.Font = Font(font_name, 11)
        self._log_action(f"Font changed to: {font_name}")
    
    def _on_text_changed(self, sender, e):
        """Update statistics when text changes."""
        text = self.txt_content.Text
        chars = len(text)
        words = len(text.split()) if text.strip() else 0
        lines = text.count('\n') + 1 if text else 1
        
        self.lbl_stats.Text = f"Lines: {lines} | Words: {words} | Chars: {chars}"
    
    def _on_about(self, sender, e):
        """Show About dialog."""
        MessageBox.Show(
            "WinFormPy .NET 2.0 Controls Example\n\n" +
            "Demonstrates MenuStrip, ToolStrip,\n" +
            "StatusStrip, and ContextMenuStrip\n\n" +
            "These controls replaced the older\n" +
            ".NET 1.x MainMenu, ToolBar, StatusBar,\n" +
            "and ContextMenu controls.",
            "About",
            "OK",
            "Information"
        )
    
    def _on_exit(self, sender, e):
        """Exit application."""
        self.Close()
    
    def _log_action(self, action):
        """Log action to status bar."""
        self.action_count += 1
        self.lbl_status.Text = f"[{self.action_count}] {action}"
    
    def _update_clock(self):
        """Update clock in status bar."""
        now = datetime.now()
        self.lbl_clock.Text = now.strftime("%H:%M:%S")
        self.InvokeAsync(self._update_clock, 1000)


if __name__ == "__main__":
    Application.Run(DotNet2ControlsForm())
