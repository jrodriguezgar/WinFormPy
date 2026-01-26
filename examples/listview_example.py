"""
ListView Example - Comprehensive ListView Control Demonstration

This example demonstrates the ListView control in WinFormPy with:
1. Different view modes (Details, List, LargeIcon, SmallIcon, Tile)
2. Column management and sorting
3. Item selection (single and multi-select)
4. Checkboxes
5. Context menu
6. Search and filter
7. Item editing

FEATURES DEMONSTRATED:
- View modes: Details, List, LargeIcon, SmallIcon
- Column headers with sorting
- FullRowSelect and GridLines
- Single and multi-select
- CheckBoxes for items
- Adding/removing items dynamically
- Item selection events
- Search functionality

NOTE: This example explicitly creates ImageLists for icons.
ListView supports:
- Automatic default icon creation when no ImageList is provided
- Configurable icon sizes (SmallIconSize, LargeIconSize)
- Configurable icon spacing (SmallIconSpacing, LargeIconSpacing)
"""

import sys
import os
# Add parent directory to path to import winformpy without installation
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from winformpy.winformpy import (
    Application, Form, ListView, ListViewItem, Panel, Button, Label,
    ComboBox, CheckBox, TextBox, DockStyle, Font, FontStyle,
    View, MessageBox, DialogResult, ContextMenuStrip, ToolStripMenuItem,
    ImageList
)
from winformpy.winformpy_extended import PhotoImage


class ListViewExampleForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "WinFormPy ListView Example"
        self.Width = 1100
        self.Height = 750
        self.StartPosition = "CenterScreen"
        self.ApplyLayout()
        
        # Initialize components
        self._create_imagelist()
        self._create_top_panel()
        self._create_control_panel()
        self._create_listview()
        self._create_bottom_panel()
        
        # Populate sample data
        self._populate_sample_data()
    
    def _create_top_panel(self):
        """Create top title panel."""
        top_panel = Panel(self, {
            'Height': 70,
            'BackColor': '#0078D4'
        })
        top_panel.Dock = DockStyle.Top
        
        Label(top_panel, {
            'Text': 'LISTVIEW CONTROL DEMONSTRATION',
            'Left': 20,
            'Top': 12,
            'AutoSize': True,
            'Font': Font('Segoe UI', 16, FontStyle.Bold),
            'ForeColor': '#FFFFFF',
            'BackColor': '#0078D4'
        })
        
        Label(top_panel, {
            'Text': 'Explore different view modes, selection, sorting, and filtering',
            'Left': 20,
            'Top': 42,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9),
            'ForeColor': '#E0E0E0',
            'BackColor': '#0078D4'
        })
    
    def _create_imagelist(self):
        """Create ImageLists for different icon sizes."""
        # Create small icon list (16x16) with a simple colored square
        self.small_imagelist = ImageList({'ImageSize': (16, 16)})
        small_icon = PhotoImage(width=16, height=16)
        # Create a blue square with a white center (simple person icon representation)
        for y in range(16):
            for x in range(16):
                if 2 <= x <= 13 and 2 <= y <= 13:
                    # Blue background
                    small_icon.put('#3498DB', (x, y))
                    # White circle for head (rows 4-7)
                    if 6 <= x <= 9 and 4 <= y <= 7:
                        small_icon.put('#FFFFFF', (x, y))
                    # White body (rows 8-12)
                    elif 5 <= x <= 10 and 8 <= y <= 12:
                        small_icon.put('#FFFFFF', (x, y))
        self.small_imagelist.Images.Add(small_icon, 0)  # Add with numeric key
        
        # Create large icon list (32x32) with a simple colored square
        self.large_imagelist = ImageList({'ImageSize': (32, 32)})
        large_icon = PhotoImage(width=32, height=32)
        # Create a blue square with a white center (simple person icon representation)
        for y in range(32):
            for x in range(32):
                if 4 <= x <= 27 and 4 <= y <= 27:
                    # Blue background
                    large_icon.put('#3498DB', (x, y))
                    # White circle for head (rows 8-14)
                    if 12 <= x <= 19 and 8 <= y <= 14:
                        large_icon.put('#FFFFFF', (x, y))
                    # White body (rows 15-24)
                    elif 10 <= x <= 21 and 15 <= y <= 24:
                        large_icon.put('#FFFFFF', (x, y))
        self.large_imagelist.Images.Add(large_icon, 0)  # Add with numeric key
    
    def _create_control_panel(self):
        """Create control panel with view options and settings."""
        control_panel = Panel(self, {
            'Height': 100,
            'BackColor': '#F5F5F5',
            'BorderStyle': 'FixedSingle'
        })
        control_panel.Dock = DockStyle.Top
        
        # View Mode Section
        Label(control_panel, {
            'Text': 'View Mode:',
            'Left': 20,
            'Top': 15,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9, FontStyle.Bold),
            'BackColor': '#F5F5F5'
        })
        
        self.combo_view = ComboBox(control_panel, {
            'Items': ['Details', 'List', 'LargeIcon', 'SmallIcon'],
            'Left': 20,
            'Top': 35,
            'Width': 140
        })
        self.combo_view.SelectedIndex = 0
        self.combo_view.SelectedIndexChanged = self._on_view_changed
        
        # Options Section
        Label(control_panel, {
            'Text': 'Options:',
            'Left': 180,
            'Top': 15,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9, FontStyle.Bold),
            'BackColor': '#F5F5F5'
        })
        
        self.chk_gridlines = CheckBox(control_panel, {
            'Text': 'Grid Lines',
            'Left': 180,
            'Top': 35,
            'Width': 110,
            'Checked': True,
            'BackColor': '#F5F5F5'
        })
        self.chk_gridlines.CheckedChanged = self._on_gridlines_changed
        
        self.chk_fullrow = CheckBox(control_panel, {
            'Text': 'Full Row Select',
            'Left': 180,
            'Top': 60,
            'Width': 120,
            'Checked': True,
            'BackColor': '#F5F5F5'
        })
        self.chk_fullrow.CheckedChanged = self._on_fullrow_changed
        
        self.chk_checkboxes = CheckBox(control_panel, {
            'Text': 'Show Checkboxes',
            'Left': 300,
            'Top': 35,
            'Width': 130,
            'Checked': False,
            'BackColor': '#F5F5F5'
        })
        self.chk_checkboxes.CheckedChanged = self._on_checkboxes_changed
        
        self.chk_multiselect = CheckBox(control_panel, {
            'Text': 'Multi-Select',
            'Left': 300,
            'Top': 60,
            'Width': 110,
            'Checked': True,
            'BackColor': '#F5F5F5'
        })
        self.chk_multiselect.CheckedChanged = self._on_multiselect_changed
        
        # Search Section
        Label(control_panel, {
            'Text': 'Search:',
            'Left': 440,
            'Top': 15,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9, FontStyle.Bold),
            'BackColor': '#F5F5F5'
        })
        
        self.txt_search = TextBox(control_panel, {
            'Left': 440,
            'Top': 35,
            'Width': 200
        })
        
        btn_search = Button(control_panel, {
            'Text': 'Search',
            'Left': 650,
            'Top': 33,
            'Width': 70,
            'Height': 26
        })
        btn_search.Click = self._on_search
        
        # Action Buttons
        btn_add = Button(control_panel, {
            'Text': '➕ Add Item',
            'Left': 740,
            'Top': 15,
            'Width': 100,
            'Height': 30,
            'BackColor': '#2ECC71',
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        btn_add.Click = self._on_add_item
        
        btn_remove = Button(control_panel, {
            'Text': '➖ Remove',
            'Left': 850,
            'Top': 15,
            'Width': 100,
            'Height': 30,
            'BackColor': '#E74C3C',
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        btn_remove.Click = self._on_remove_item
        
        btn_clear = Button(control_panel, {
            'Text': '🗑️ Clear All',
            'Left': 960,
            'Top': 15,
            'Width': 100,
            'Height': 30,
            'BackColor': '#95A5A6',
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        btn_clear.Click = self._on_clear_all
        
        btn_info = Button(control_panel, {
            'Text': 'ℹ️ Selection Info',
            'Left': 740,
            'Top': 55,
            'Width': 150,
            'Height': 30,
            'BackColor': '#3498DB',
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        btn_info.Click = self._on_show_selection_info
        
        btn_check_info = Button(control_panel, {
            'Text': '✓ Checked Info',
            'Left': 900,
            'Top': 55,
            'Width': 160,
            'Height': 30,
            'BackColor': '#9B59B6',
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        btn_check_info.Click = self._on_show_checked_info
    
    def _create_listview(self):
        """Create the main ListView control."""
        self.listview = ListView(self, {
            'View': View.Details,
            'FullRowSelect': True,
            'GridLines': True,
            'MultiSelect': True,
            'CheckBoxes': False,
            'BackColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9)
        })
        self.listview.Dock = DockStyle.Fill
        
        # Set ImageLists for icon views
        self.listview.SmallImageList = self.small_imagelist
        self.listview.LargeImageList = self.large_imagelist
        
        # Add columns
        self.listview.Columns.Add("ID", 60)
        self.listview.Columns.Add("Name", 200)
        self.listview.Columns.Add("Department", 150)
        self.listview.Columns.Add("Position", 180)
        self.listview.Columns.Add("Salary", 100)
        self.listview.Columns.Add("Status", 120)
        
        # Bind events
        self.listview.SelectedIndexChanged = self._on_selection_changed
        self.listview.ColumnClick = self._on_column_click
        self.listview.ItemActivate = self._on_item_activate
        
        # Create context menu
        self._create_context_menu()
    
    def _create_context_menu(self):
        """Create context menu for ListView."""
        context_menu = ContextMenuStrip()
        
        menu_edit = ToolStripMenuItem("Edit Item")
        menu_edit.Click = self._on_edit_item
        context_menu.Items.append(menu_edit)
        
        menu_delete = ToolStripMenuItem("Delete Item")
        menu_delete.Click = self._on_remove_item
        context_menu.Items.append(menu_delete)
        
        context_menu.Items.append(ToolStripMenuItem("-"))  # Separator
        
        menu_select_all = ToolStripMenuItem("Select All")
        menu_select_all.Click = self._on_select_all
        context_menu.Items.append(menu_select_all)
        
        self.listview.ContextMenuStrip = context_menu
    
    def _create_bottom_panel(self):
        """Create bottom status panel."""
        bottom_panel = Panel(self, {
            'Height': 40,
            'BackColor': '#34495E'
        })
        bottom_panel.Dock = DockStyle.Bottom
        
        self.lbl_status = Label(bottom_panel, {
            'Text': 'Ready | Total Items: 0 | Selected: 0',
            'Left': 15,
            'Top': 10,
            'Width': 1000,
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9),
            'BackColor': '#34495E'
        })
    
    def _populate_sample_data(self):
        """Populate ListView with sample employee data."""
        employees = [
            ("001", "John Smith", "Engineering", "Senior Developer", "$95,000", "Active"),
            ("002", "Sarah Johnson", "Marketing", "Marketing Manager", "$85,000", "Active"),
            ("003", "Michael Brown", "Sales", "Sales Representative", "$65,000", "Active"),
            ("004", "Emily Davis", "HR", "HR Specialist", "$60,000", "On Leave"),
            ("005", "David Wilson", "Engineering", "Junior Developer", "$55,000", "Active"),
            ("006", "Lisa Anderson", "Finance", "Financial Analyst", "$70,000", "Active"),
            ("007", "Robert Taylor", "Engineering", "Tech Lead", "$105,000", "Active"),
            ("008", "Jennifer Martinez", "Design", "UX Designer", "$75,000", "Active"),
            ("009", "James Garcia", "Sales", "Sales Manager", "$90,000", "Active"),
            ("010", "Mary Rodriguez", "Marketing", "Content Specialist", "$62,000", "Active"),
            ("011", "William Lee", "IT", "System Administrator", "$72,000", "Active"),
            ("012", "Patricia Hernandez", "HR", "HR Manager", "$88,000", "Active"),
            ("013", "Thomas Lopez", "Engineering", "DevOps Engineer", "$92,000", "Active"),
            ("014", "Linda Gonzalez", "Finance", "Accountant", "$68,000", "Active"),
            ("015", "Charles Wilson", "Sales", "Business Development", "$78,000", "Active"),
        ]
        
        for emp_id, name, dept, position, salary, status in employees:
            item = ListViewItem({
                'Text': emp_id,
                'SubItems': [name, dept, position, salary, status],
                'ImageIndex': 0  # Use the 'person' icon
            })
            self.listview.Items.Add(item)
        
        self._update_status()
    
    def _update_status(self):
        """Update status bar with current info."""
        total = len(self.listview.Items)
        selected = len(self.listview.SelectedItems)
        checked = len(self.listview.CheckedItems) if self.listview.CheckBoxes else 0
        
        status = f'Ready | Total Items: {total} | Selected: {selected}'
        if self.listview.CheckBoxes:
            status += f' | Checked: {checked}'
        
        self.lbl_status.Text = status
    
    # Event Handlers
    def _on_view_changed(self, sender, e):
        """Handle view mode change."""
        view_name = self.combo_view.SelectedItem
        if view_name == 'Details':
            self.listview.View = View.Details
        elif view_name == 'List':
            self.listview.View = View.List
        elif view_name == 'LargeIcon':
            self.listview.View = View.LargeIcon
        elif view_name == 'SmallIcon':
            self.listview.View = View.SmallIcon
    
    def _on_gridlines_changed(self, sender, e):
        """Handle grid lines toggle."""
        self.listview.GridLines = self.chk_gridlines.Checked
        # Force visual update
        if hasattr(self.listview, 'Refresh'):
            self.listview.Refresh()
    
    def _on_fullrow_changed(self, sender, e):
        """Handle full row select toggle."""
        self.listview.FullRowSelect = self.chk_fullrow.Checked
        # Force visual update
        if hasattr(self.listview, 'Refresh'):
            self.listview.Refresh()
    
    def _on_checkboxes_changed(self, sender, e):
        """Handle checkboxes toggle."""
        self.listview.CheckBoxes = self.chk_checkboxes.Checked
        # Force refresh of the listview
        if hasattr(self.listview, 'Refresh'):
            self.listview.Refresh()
        self._update_status()
    
    def _on_multiselect_changed(self, sender, e):
        """Handle multi-select toggle."""
        self.listview.MultiSelect = self.chk_multiselect.Checked
    
    def _on_selection_changed(self, sender, e):
        """Handle selection change."""
        self._update_status()
    
    def _on_column_click(self, sender, e):
        """Handle column header click for sorting."""
        MessageBox.Show(f"Column clicked: {e.Data.get('Column', 'Unknown')}", "Column Click")
    
    def _on_item_activate(self, sender, e):
        """Handle item double-click/activation."""
        selected = self.listview.SelectedItems
        if selected:
            item = selected[0]
            info = f"Employee Details:\n\n"
            info += f"ID: {item.Text}\n"
            info += f"Name: {item.SubItems[0] if len(item.SubItems) > 0 else 'N/A'}\n"
            info += f"Department: {item.SubItems[1] if len(item.SubItems) > 1 else 'N/A'}\n"
            info += f"Position: {item.SubItems[2] if len(item.SubItems) > 2 else 'N/A'}\n"
            info += f"Salary: {item.SubItems[3] if len(item.SubItems) > 3 else 'N/A'}\n"
            info += f"Status: {item.SubItems[4] if len(item.SubItems) > 4 else 'N/A'}"
            MessageBox.Show(info, "Item Details")
    
    def _on_search(self, sender, e):
        """Handle search button click."""
        search_text = self.txt_search.Text.strip().lower()
        if not search_text:
            MessageBox.Show("Please enter search text", "Search")
            return
        
        # Clear current selection
        for item in self.listview.Items:
            item.Selected = False
        
        # Find and select matching items
        found_count = 0
        for item in self.listview.Items:
            # Search in Text and all subitems
            match = search_text in item.Text.lower() or any(search_text in str(subitem).lower() for subitem in item.SubItems)
            if match:
                item.Selected = True
                found_count += 1
        
        MessageBox.Show(f"Found {found_count} matching item(s)", "Search Results")
        self._update_status()
    
    def _on_add_item(self, sender, e):
        """Handle add item button click."""
        # Generate new ID
        new_id = str(len(self.listview.Items) + 1).zfill(3)
        new_item = ListViewItem({
            'Text': new_id,
            'SubItems': [
                "New Employee",
                "Unassigned",
                "To Be Determined",
                "$0",
                "Pending"
            ],
            'ImageIndex': 0  # Use the 'person' icon
        })
        self.listview.Items.Add(new_item)
        self._update_status()
        MessageBox.Show(f"Added new item with ID: {new_id}", "Add Item")
    
    def _on_remove_item(self, sender, e):
        """Handle remove item button click."""
        selected = self.listview.SelectedItems
        if not selected:
            MessageBox.Show("Please select item(s) to remove", "Remove Item")
            return
        
        count = len(selected)
        for item in selected:
            self.listview.Items.Remove(item)
        
        self._update_status()
        MessageBox.Show(f"Removed {count} item(s)", "Remove Item")
    
    def _on_clear_all(self, sender, e):
        """Handle clear all button click."""
        if len(self.listview.Items) == 0:
            MessageBox.Show("ListView is already empty", "Clear All")
            return
        
        result = MessageBox.Show(
            "Are you sure you want to remove all items?",
            "Confirm Clear",
            "YesNo"
        )
        if result == DialogResult.Yes:
            self.listview.Items.Clear()
            self._update_status()
            MessageBox.Show("All items cleared", "Clear All")
    
    def _on_show_selection_info(self, sender, e):
        """Show information about selected items."""
        selected = self.listview.SelectedItems
        if not selected:
            MessageBox.Show("No items selected", "Selection Info")
            return
        
        info = f"Selected Items: {len(selected)}\n\n"
        for i, item in enumerate(selected[:5], 1):  # Show first 5
            name = item.SubItems[1] if len(item.SubItems) > 1 else "N/A"
            info += f"{i}. {name}\n"
        
        if len(selected) > 5:
            info += f"\n... and {len(selected) - 5} more"
        
        MessageBox.Show(info, "Selection Info")
    
    def _on_show_checked_info(self, sender, e):
        """Show information about checked items."""
        if not self.listview.CheckBoxes:
            MessageBox.Show("Checkboxes are not enabled", "Checked Info")
            return
        
        checked = self.listview.CheckedItems
        if not checked:
            MessageBox.Show("No items checked", "Checked Info")
            return
        
        info = f"Checked Items: {len(checked)}\n\n"
        for i, item in enumerate(checked[:5], 1):
            # Text is the ID, SubItems[0] is the Name
            name = item.SubItems[0] if len(item.SubItems) > 0 else item.Text
            info += f"{i}. {name}\n"
        
        if len(checked) > 5:
            info += f"\n... and {len(checked) - 5} more"
        
        MessageBox.Show(info, "Checked Info")
    
    def _on_edit_item(self, sender=None, e=None):
        """Handle edit item from context menu."""
        selected = self.listview.SelectedItems
        if selected:
            MessageBox.Show("Edit functionality would open an edit dialog here", "Edit Item")
    
    def _on_select_all(self, sender=None, e=None):
        """Handle select all from context menu."""
        for item in self.listview.Items:
            item.Selected = True
        self._update_status()


def main():
    """Application entry point."""
    app = ListViewExampleForm()
    Application.Run(app)


if __name__ == '__main__':
    main()


