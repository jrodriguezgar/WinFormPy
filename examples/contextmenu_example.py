"""
ContextMenuStrip Example - WinFormPy

This example demonstrates ContextMenuStrip functionality:
- Creating context menus
- Attaching to different controls
- Menu items with icons
- Submenus
- Separators
- Enabled/disabled items
- Checked items
- Dynamic menu updates
- Menu item events
"""

from winformpy import (
    Application, Form, Label, Button, TextBox, Panel, ListBox,
    ContextMenuStrip, ToolStripMenuItem, ToolStripSeparator,
    MessageBox, DockStyle, Font, FontStyle
)


class ContextMenuForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "ContextMenuStrip Demo"
        self.Width = 1100
        self.Height = 750
        self.StartPosition = "CenterScreen"
        
        # Apply layout before adding controls
        self.ApplyLayout()
        
        self._init_header()
        self._init_text_area()
        self._init_listbox_area()
        self._init_panel_area()
        self._init_button_area()
        self._init_footer()
        
        # Create context menus
        self._create_text_context_menu()
        self._create_listbox_context_menu()
        self._create_panel_context_menu()
        self._create_button_context_menu()
    
    def _init_header(self):
        """Initialize header panel"""
        header = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 80,
            'BackColor': '#2c3e50'
        })
        
        title = Label(header, {
            'Text': 'ContextMenuStrip Examples',
            'Font': Font('Segoe UI', 16, FontStyle.Bold),
            'ForeColor': 'white',
            'BackColor': '#2c3e50',
            'Left': 20,
            'Top': 15,
            'AutoSize': True
        })
        
        subtitle = Label(header, {
            'Text': 'Right-click on different areas to see context menus',
            'Font': Font('Segoe UI', 10),
            'ForeColor': '#bdc3c7',
            'BackColor': '#2c3e50',
            'Left': 20,
            'Top': 50,
            'AutoSize': True
        })
    
    def _init_text_area(self):
        """Initialize text editing area"""
        panel = Panel(self, {
            'Left': 20,
            'Top': 100,
            'Width': 520,
            'Height': 270,
            'BackColor': 'white',
            'BorderStyle': 'FixedSingle'
        })
        
        # Title
        Label(panel, {
            'Text': 'TextBox with Edit Context Menu',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 10,
            'Top': 10,
            'AutoSize': True
        })
        
        # TextBox
        self.txt_editor = TextBox(panel, {
            'Multiline': True,
            'Left': 10,
            'Top': 40,
            'Width': 500,
            'Height': 220,
            'ScrollBars': 'Vertical',
            'Text': 'Right-click here to see edit options:\n\n'
                   '- Cut\n'
                   '- Copy\n'
                   '- Paste\n'
                   '- Select All\n'
                   '- Clear\n\n'
                   'Try selecting some text first!'
        })
    
    def _init_listbox_area(self):
        """Initialize listbox area"""
        panel = Panel(self, {
            'Left': 560,
            'Top': 100,
            'Width': 520,
            'Height': 270,
            'BackColor': '#f8f9fa',
            'BorderStyle': 'FixedSingle'
        })
        
        # Title
        Label(panel, {
            'Text': 'ListBox with Item Management Menu',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 10,
            'Top': 10,
            'AutoSize': True
        })
        
        # ListBox
        self.listbox = ListBox(panel, {
            'Left': 10,
            'Top': 40,
            'Width': 500,
            'Height': 220
        })
        
        # Add sample items
        for i in range(1, 11):
            self.listbox.Items.append(f'Item {i}')
    
    def _init_panel_area(self):
        """Initialize panel with context menu"""
        panel = Panel(self, {
            'Left': 20,
            'Top': 390,
            'Width': 520,
            'Height': 270,
            'BackColor': 'white',
            'BorderStyle': 'FixedSingle'
        })
        
        # Title
        Label(panel, {
            'Text': 'Panel with Appearance Menu',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 10,
            'Top': 10,
            'AutoSize': True
        })
        
        # Colored panel
        self.colored_panel = Panel(panel, {
            'Left': 10,
            'Top': 40,
            'Width': 500,
            'Height': 220,
            'BackColor': '#3498db',
            'BorderStyle': 'FixedSingle'
        })
        
        self.colored_panel_label = Label(self.colored_panel, {
            'Text': 'Right-click to change colors\nand appearance',
            'Font': Font('Segoe UI', 12),
            'ForeColor': 'white',
            'BackColor': '#3498db',
            'Left': 140,
            'Top': 90,
            'Width': 250,
            'Height': 50,
            'TextAlign': 'MiddleCenter'
        })
    
    def _init_button_area(self):
        """Initialize button area"""
        panel = Panel(self, {
            'Left': 560,
            'Top': 390,
            'Width': 520,
            'Height': 270,
            'BackColor': '#f8f9fa',
            'BorderStyle': 'FixedSingle'
        })
        
        # Title
        Label(panel, {
            'Text': 'Buttons with Action Menus',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 10,
            'Top': 10,
            'AutoSize': True
        })
        
        # Buttons
        y = 60
        for i in range(1, 4):
            btn = Button(panel, {
                'Text': f'Button {i}\n(Right-click for options)',
                'Left': 10,
                'Top': y,
                'Width': 500,
                'Height': 50
            })
            y += 65
    
    def _init_footer(self):
        """Initialize footer panel"""
        footer = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': 50,
            'BackColor': '#ecf0f1'
        })
        
        btn_close = Button(footer, {
            'Text': 'Close',
            'Left': 960,
            'Top': 10,
            'Width': 100,
            'Height': 30
        })
        btn_close.Click = lambda s, e: self.Close()
    
    def _create_text_context_menu(self):
        """Create context menu for TextBox"""
        menu = ContextMenuStrip()
        
        # Cut
        item_cut = ToolStripMenuItem()
        item_cut.Text = 'Cut'
        item_cut.ShortcutKeys = 'Ctrl+X'
        item_cut.Click = lambda s, e: self._text_cut()
        menu.Items.append(item_cut)
        
        # Copy
        item_copy = ToolStripMenuItem()
        item_copy.Text = 'Copy'
        item_copy.ShortcutKeys = 'Ctrl+C'
        item_copy.Click = lambda s, e: self._text_copy()
        menu.Items.append(item_copy)
        
        # Paste
        item_paste = ToolStripMenuItem()
        item_paste.Text = 'Paste'
        item_paste.ShortcutKeys = 'Ctrl+V'
        item_paste.Click = lambda s, e: self._text_paste()
        menu.Items.append(item_paste)
        
        # Separator
        menu.Items.append(ToolStripSeparator())
        
        # Select All
        item_select = ToolStripMenuItem()
        item_select.Text = 'Select All'
        item_select.ShortcutKeys = 'Ctrl+A'
        item_select.Click = lambda s, e: self._text_select_all()
        menu.Items.append(item_select)
        
        # Separator
        menu.Items.append(ToolStripSeparator())
        
        # Clear
        item_clear = ToolStripMenuItem()
        item_clear.Text = 'Clear'
        item_clear.Click = lambda s, e: self._text_clear()
        menu.Items.append(item_clear)
        
        # Attach to TextBox
        self.txt_editor.ContextMenuStrip = menu
    
    def _create_listbox_context_menu(self):
        """Create context menu for ListBox"""
        menu = ContextMenuStrip()
        
        # Add Item
        item_add = ToolStripMenuItem()
        item_add.Text = 'Add Item...'
        item_add.Click = lambda s, e: self._listbox_add()
        menu.Items.append(item_add)
        
        # Remove Item
        item_remove = ToolStripMenuItem()
        item_remove.Text = 'Remove Selected'
        item_remove.Click = lambda s, e: self._listbox_remove()
        menu.Items.append(item_remove)
        
        # Separator
        menu.Items.append(ToolStripSeparator())
        
        # Edit Item
        item_edit = ToolStripMenuItem()
        item_edit.Text = 'Edit Item...'
        item_edit.Click = lambda s, e: self._listbox_edit()
        menu.Items.append(item_edit)
        
        # Separator
        menu.Items.append(ToolStripSeparator())
        
        # Clear All
        item_clear = ToolStripMenuItem()
        item_clear.Text = 'Clear All'
        item_clear.Click = lambda s, e: self._listbox_clear()
        menu.Items.append(item_clear)
        
        # Separator
        menu.Items.append(ToolStripSeparator())
        
        # Sort submenu
        item_sort = ToolStripMenuItem()
        item_sort.Text = 'Sort'
        
        item_sort_asc = ToolStripMenuItem()
        item_sort_asc.Text = 'Ascending'
        item_sort_asc.Click = lambda s, e: self._listbox_sort(True)
        item_sort.DropDownItems.Add(item_sort_asc)
        
        item_sort_desc = ToolStripMenuItem()
        item_sort_desc.Text = 'Descending'
        item_sort_desc.Click = lambda s, e: self._listbox_sort(False)
        item_sort.DropDownItems.Add(item_sort_desc)
        
        menu.Items.append(item_sort)
        
        # Attach to ListBox
        self.listbox.ContextMenuStrip = menu
    
    def _create_panel_context_menu(self):
        """Create context menu for Panel"""
        menu = ContextMenuStrip()
        
        # Colors submenu
        item_colors = ToolStripMenuItem()
        item_colors.Text = 'Background Color'
        
        colors = [
            ('Blue', '#3498db'),
            ('Green', '#2ecc71'),
            ('Red', '#e74c3c'),
            ('Purple', '#9b59b6'),
            ('Orange', '#e67e22'),
            ('Gray', '#95a5a6')
        ]
        
        for name, color in colors:
            item = ToolStripMenuItem()
            item.Text = name
            item.Click = lambda s, e, c=color: self._panel_change_color(c)
            item_colors.DropDownItems.Add(item)
        
        menu.Items.append(item_colors)
        
        # Separator
        menu.Items.append(ToolStripSeparator())
        
        # Border Style submenu
        item_border = ToolStripMenuItem()
        item_border.Text = 'Border Style'
        
        borders = ['None', 'FixedSingle', 'Fixed3D']
        for border in borders:
            item = ToolStripMenuItem()
            item.Text = border
            item.Click = lambda s, e, b=border: self._panel_change_border(b)
            item_border.DropDownItems.Add(item)
        
        menu.Items.append(item_border)
        
        # Separator
        menu.Items.append(ToolStripSeparator())
        
        # Reset
        item_reset = ToolStripMenuItem()
        item_reset.Text = 'Reset to Default'
        item_reset.Click = lambda s, e: self._panel_reset()
        menu.Items.append(item_reset)
        
        # Attach to Panel and Label
        self.colored_panel.ContextMenuStrip = menu
        self.colored_panel_label.ContextMenuStrip = menu
    
    def _create_button_context_menu(self):
        """Create context menu for Buttons"""
        menu = ContextMenuStrip()
        
        # Show Info
        item_info = ToolStripMenuItem()
        item_info.Text = 'Show Button Info'
        item_info.Click = lambda s, e: self._button_info()
        menu.Items.append(item_info)
        
        # Separator
        menu.Items.append(ToolStripSeparator())
        
        # Enable/Disable (with checkbox)
        self.item_button_enabled = ToolStripMenuItem()
        self.item_button_enabled.Text = 'Enabled'
        self.item_button_enabled.Checked = True
        self.item_button_enabled.CheckOnClick = True
        self.item_button_enabled.Click = lambda s, e: self._button_toggle_enabled()
        menu.Items.append(self.item_button_enabled)
        
        # Visible (with checkbox)
        self.item_button_visible = ToolStripMenuItem()
        self.item_button_visible.Text = 'Visible'
        self.item_button_visible.Checked = True
        self.item_button_visible.CheckOnClick = True
        menu.Items.append(self.item_button_visible)
        
        # Attach to all buttons
        for control in self.Controls:
            if hasattr(control, 'Controls'):
                for child in control.Controls:
                    if child.__class__.__name__ == 'Button' and 'Right-click' in str(child.Text):
                        child.ContextMenuStrip = menu
    
    # TextBox menu handlers
    def _text_cut(self):
        """Cut text"""
        if hasattr(self.txt_editor, 'Cut'):
            self.txt_editor.Cut()
        else:
            MessageBox.Show('Cut operation', 'Action', 'OK', 'Information')
    
    def _text_copy(self):
        """Copy text"""
        if hasattr(self.txt_editor, 'Copy'):
            self.txt_editor.Copy()
        else:
            MessageBox.Show('Copy operation', 'Action', 'OK', 'Information')
    
    def _text_paste(self):
        """Paste text"""
        if hasattr(self.txt_editor, 'Paste'):
            self.txt_editor.Paste()
        else:
            MessageBox.Show('Paste operation', 'Action', 'OK', 'Information')
    
    def _text_select_all(self):
        """Select all text"""
        if hasattr(self.txt_editor, 'SelectAll'):
            self.txt_editor.SelectAll()
        else:
            MessageBox.Show('Select All operation', 'Action', 'OK', 'Information')
    
    def _text_clear(self):
        """Clear text"""
        self.txt_editor.Text = ''
    
    # ListBox menu handlers
    def _listbox_add(self):
        """Add item to listbox"""
        # Simple input dialog simulation
        new_item = f'New Item {self.listbox.Items.Count + 1}'
        self.listbox.Items.append(new_item)
        MessageBox.Show(f'Added: {new_item}', 'Item Added', 'OK', 'Information')
    
    def _listbox_remove(self):
        """Remove selected item"""
        if self.listbox.SelectedIndex >= 0:
            item = self.listbox.SelectedItem
            self.listbox.Items.Remove(item)
            MessageBox.Show(f'Removed: {item}', 'Item Removed', 'OK', 'Information')
        else:
            MessageBox.Show('No item selected', 'Warning', 'OK', 'Warning')
    
    def _listbox_edit(self):
        """Edit selected item"""
        if self.listbox.SelectedIndex >= 0:
            MessageBox.Show('Edit dialog would open here', 'Edit Item', 'OK', 'Information')
        else:
            MessageBox.Show('No item selected', 'Warning', 'OK', 'Warning')
    
    def _listbox_clear(self):
        """Clear all items"""
        count = self.listbox.Items.Count
        self.listbox.Items.Clear()
        MessageBox.Show(f'Cleared {count} items', 'Cleared', 'OK', 'Information')
    
    def _listbox_sort(self, ascending):
        """Sort listbox items"""
        items = list(self.listbox.Items)
        items.sort(reverse=not ascending)
        self.listbox.Items.Clear()
        for item in items:
            self.listbox.Items.append(item)
        
        direction = 'ascending' if ascending else 'descending'
        MessageBox.Show(f'Items sorted {direction}', 'Sorted', 'OK', 'Information')
    
    # Panel menu handlers
    def _panel_change_color(self, color):
        """Change panel color"""
        self.colored_panel.BackColor = color
        self.colored_panel_label.BackColor = color
    
    def _panel_change_border(self, border):
        """Change panel border"""
        self.colored_panel.BorderStyle = border
    
    def _panel_reset(self):
        """Reset panel to default"""
        self.colored_panel.BackColor = '#3498db'
        self.colored_panel_label.BackColor = '#3498db'
        self.colored_panel.BorderStyle = 'FixedSingle'
    
    # Button menu handlers
    def _button_info(self):
        """Show button info"""
        MessageBox.Show(
            'Button Information:\n\n'
            'This is a demonstration button with\n'
            'a context menu attached.',
            'Button Info',
            'OK',
            'Information'
        )
    
    def _button_toggle_enabled(self):
        """Toggle button enabled state"""
        # This would toggle the button that was right-clicked
        pass


def main():
    form = ContextMenuForm()
    Application.Run(form)


if __name__ == '__main__':
    main()



