"""
DataGridView Example - Comprehensive DataGridView Control Demonstration

This example demonstrates the DataGridView control in WinFormPy with:
1. Display tabular data in a grid
2. Column management and customization
3. Row selection and manipulation
4. Sorting and filtering
5. Add, edit, and delete rows
6. Data binding with different sources
7. Cell formatting and styling

FEATURES DEMONSTRATED:
- DataGridView with columns
- Row and column manipulation
- Data binding from lists and dictionaries
- Selection modes
- Read-only and editable grids
- Cell styling
- Dynamic data updates
"""

from winformpy.winformpy import (
    Application, Form, DataGridView, Panel, Button, Label,
    ComboBox, CheckBox, TextBox, DockStyle, Font, FontStyle,
    MessageBox, DataGridViewColumn, DataGridViewSelectionMode
)


class DataGridViewExampleForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "WinFormPy DataGridView Example"
        self.Width = 1200
        self.Height = 750
        self.StartPosition = "CenterScreen"
        self.ApplyLayout()
        
        # Initialize components
        self._create_top_panel()
        self._create_control_panel()
        self._create_datagridview()
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
            'Text': 'DATAGRIDVIEW CONTROL DEMONSTRATION',
            'Left': 20,
            'Top': 12,
            'AutoSize': True,
            'Font': Font('Segoe UI', 16, FontStyle.Bold),
            'ForeColor': '#FFFFFF',
            'BackColor': '#0078D4'
        })
        
        Label(top_panel, {
            'Text': 'Display and manage tabular data with sorting, filtering, and editing capabilities',
            'Left': 20,
            'Top': 42,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9),
            'ForeColor': '#E0E0E0',
            'BackColor': '#0078D4'
        })
    
    def _create_control_panel(self):
        """Create control panel with grid options."""
        control_panel = Panel(self, {
            'Height': 100,
            'BackColor': '#F5F5F5',
            'BorderStyle': 'FixedSingle'
        })
        control_panel.Dock = DockStyle.Top
        
        # Options Section
        Label(control_panel, {
            'Text': 'Grid Options:',
            'Left': 20,
            'Top': 15,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9, FontStyle.Bold),
            'BackColor': '#F5F5F5'
        })
        
        self.chk_readonly = CheckBox(control_panel, {
            'Text': 'Read Only',
            'Left': 20,
            'Top': 35,
            'Checked': False,
            'BackColor': '#F5F5F5'
        })
        self.chk_readonly.CheckedChanged = self._on_readonly_changed
        
        self.chk_row_headers = CheckBox(control_panel, {
            'Text': 'Row Headers',
            'Left': 20,
            'Top': 60,
            'Checked': True,
            'BackColor': '#F5F5F5'
        })
        self.chk_row_headers.CheckedChanged = self._on_row_headers_changed
        
        self.chk_col_headers = CheckBox(control_panel, {
            'Text': 'Column Headers',
            'Left': 140,
            'Top': 35,
            'Checked': True,
            'BackColor': '#F5F5F5'
        })
        self.chk_col_headers.CheckedChanged = self._on_col_headers_changed
        
        self.chk_allow_add = CheckBox(control_panel, {
            'Text': 'Allow Add Rows',
            'Left': 140,
            'Top': 60,
            'Checked': False,
            'BackColor': '#F5F5F5'
        })
        self.chk_allow_add.CheckedChanged = self._on_allow_add_changed
        
        # Selection Mode
        Label(control_panel, {
            'Text': 'Selection Mode:',
            'Left': 280,
            'Top': 15,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9, FontStyle.Bold),
            'BackColor': '#F5F5F5'
        })
        
        self.combo_selection = ComboBox(control_panel, {
            'Items': ['FullRowSelect', 'CellSelect', 'FullColumnSelect'],
            'Left': 280,
            'Top': 35,
            'Width': 150
        })
        self.combo_selection.SelectedIndex = 0
        self.combo_selection.SelectedIndexChanged = self._on_selection_mode_changed
        
        # Data Source
        Label(control_panel, {
            'Text': 'Data Source:',
            'Left': 450,
            'Top': 15,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9, FontStyle.Bold),
            'BackColor': '#F5F5F5'
        })
        
        self.combo_datasource = ComboBox(control_panel, {
            'Items': ['Employees', 'Products', 'Sales'],
            'Left': 450,
            'Top': 35,
            'Width': 150
        })
        self.combo_datasource.SelectedIndex = 0
        self.combo_datasource.SelectedIndexChanged = self._on_datasource_changed
        
        # Action Buttons
        btn_add = Button(control_panel, {
            'Text': '➕ Add Row',
            'Left': 630,
            'Top': 15,
            'Width': 120,
            'Height': 30,
            'BackColor': '#2ECC71',
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        btn_add.Click = self._on_add_row
        
        btn_delete = Button(control_panel, {
            'Text': '➖ Delete Row',
            'Left': 760,
            'Top': 15,
            'Width': 120,
            'Height': 30,
            'BackColor': '#E74C3C',
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        btn_delete.Click = self._on_delete_row
        
        btn_clear = Button(control_panel, {
            'Text': '🗑️ Clear All',
            'Left': 890,
            'Top': 15,
            'Width': 120,
            'Height': 30,
            'BackColor': '#95A5A6',
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        btn_clear.Click = self._on_clear_all
        
        btn_info = Button(control_panel, {
            'Text': 'ℹ️ Row Info',
            'Left': 1020,
            'Top': 15,
            'Width': 140,
            'Height': 30,
            'BackColor': '#3498DB',
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        btn_info.Click = self._on_show_row_info
        
        # Filter
        Label(control_panel, {
            'Text': 'Filter:',
            'Left': 630,
            'Top': 55,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9, FontStyle.Bold),
            'BackColor': '#F5F5F5'
        })
        
        self.txt_filter = TextBox(control_panel, {
            'Left': 680,
            'Top': 52,
            'Width': 200
        })
        
        btn_filter = Button(control_panel, {
            'Text': 'Apply',
            'Left': 890,
            'Top': 50,
            'Width': 60,
            'Height': 26
        })
        btn_filter.Click = self._on_apply_filter
        
        btn_clear_filter = Button(control_panel, {
            'Text': 'Clear',
            'Left': 960,
            'Top': 50,
            'Width': 60,
            'Height': 26
        })
        btn_clear_filter.Click = self._on_clear_filter
    
    def _create_datagridview(self):
        """Create the main DataGridView control."""
        self.datagridview = DataGridView(self, {
            'ReadOnly': False,
            'AllowUserToAddRows': False,
            'AllowUserToDeleteRows': False,
            'RowHeadersVisible': True,
            'ColumnHeadersVisible': True,
            'SelectionMode': DataGridViewSelectionMode.FullRowSelect,
            'BackColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9)
        })
        self.datagridview.Dock = DockStyle.Fill
        
        # Bind events
        self.datagridview.SelectionChanged = self._on_selection_changed
        self.datagridview.CellClick = self._on_cell_click
    
    def _create_bottom_panel(self):
        """Create bottom status panel."""
        bottom_panel = Panel(self, {
            'Height': 40,
            'BackColor': '#34495E'
        })
        bottom_panel.Dock = DockStyle.Bottom
        
        self.lbl_status = Label(bottom_panel, {
            'Text': 'Ready | Total Rows: 0 | Selected: 0',
            'Left': 15,
            'Top': 10,
            'Width': 1100,
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9),
            'BackColor': '#34495E'
        })
    
    def _populate_sample_data(self):
        """Populate DataGridView with sample employee data."""
        # Store different datasets
        self.datasets = {
            'Employees': [
                {'ID': '001', 'Name': 'John Smith', 'Department': 'Engineering', 'Position': 'Senior Developer', 'Salary': 95000, 'Status': 'Active'},
                {'ID': '002', 'Name': 'Sarah Johnson', 'Department': 'Marketing', 'Position': 'Marketing Manager', 'Salary': 85000, 'Status': 'Active'},
                {'ID': '003', 'Name': 'Michael Brown', 'Department': 'Sales', 'Position': 'Sales Rep', 'Salary': 65000, 'Status': 'Active'},
                {'ID': '004', 'Name': 'Emily Davis', 'Department': 'HR', 'Position': 'HR Specialist', 'Salary': 60000, 'Status': 'On Leave'},
                {'ID': '005', 'Name': 'David Wilson', 'Department': 'Engineering', 'Position': 'Junior Developer', 'Salary': 55000, 'Status': 'Active'},
                {'ID': '006', 'Name': 'Lisa Anderson', 'Department': 'Finance', 'Position': 'Financial Analyst', 'Salary': 70000, 'Status': 'Active'},
                {'ID': '007', 'Name': 'Robert Taylor', 'Department': 'Engineering', 'Position': 'Tech Lead', 'Salary': 105000, 'Status': 'Active'},
                {'ID': '008', 'Name': 'Jennifer Martinez', 'Department': 'Design', 'Position': 'UX Designer', 'Salary': 75000, 'Status': 'Active'},
                {'ID': '009', 'Name': 'James Garcia', 'Department': 'Sales', 'Position': 'Sales Manager', 'Salary': 90000, 'Status': 'Active'},
                {'ID': '010', 'Name': 'Mary Rodriguez', 'Department': 'Marketing', 'Position': 'Content Specialist', 'Salary': 62000, 'Status': 'Active'},
            ],
            'Products': [
                {'Code': 'P001', 'Name': 'Laptop Pro 15', 'Category': 'Electronics', 'Price': 1299.99, 'Stock': 45, 'Supplier': 'TechSupply Co'},
                {'Code': 'P002', 'Name': 'Wireless Mouse', 'Category': 'Accessories', 'Price': 29.99, 'Stock': 150, 'Supplier': 'GadgetWorld'},
                {'Code': 'P003', 'Name': 'Mechanical Keyboard', 'Category': 'Accessories', 'Price': 89.99, 'Stock': 78, 'Supplier': 'KeyMaster Inc'},
                {'Code': 'P004', 'Name': 'USB-C Hub', 'Category': 'Accessories', 'Price': 49.99, 'Stock': 120, 'Supplier': 'ConnectPlus'},
                {'Code': 'P005', 'Name': '27" Monitor', 'Category': 'Electronics', 'Price': 349.99, 'Stock': 32, 'Supplier': 'ScreenTech'},
                {'Code': 'P006', 'Name': 'Webcam HD', 'Category': 'Electronics', 'Price': 79.99, 'Stock': 65, 'Supplier': 'VisionPro'},
                {'Code': 'P007', 'Name': 'Desk Lamp LED', 'Category': 'Office', 'Price': 39.99, 'Stock': 90, 'Supplier': 'LightWorks'},
                {'Code': 'P008', 'Name': 'Ergonomic Chair', 'Category': 'Furniture', 'Price': 299.99, 'Stock': 25, 'Supplier': 'ComfortSeating'},
            ],
            'Sales': [
                {'InvoiceID': 'INV-1001', 'Customer': 'Acme Corp', 'Product': 'Laptop Pro 15', 'Quantity': 5, 'Amount': 6499.95, 'Date': '2026-01-15'},
                {'InvoiceID': 'INV-1002', 'Customer': 'TechStart Inc', 'Product': 'Wireless Mouse', 'Quantity': 20, 'Amount': 599.80, 'Date': '2026-01-16'},
                {'InvoiceID': 'INV-1003', 'Customer': 'Global Systems', 'Product': '27" Monitor', 'Quantity': 10, 'Amount': 3499.90, 'Date': '2026-01-17'},
                {'InvoiceID': 'INV-1004', 'Customer': 'DataTech LLC', 'Product': 'USB-C Hub', 'Quantity': 15, 'Amount': 749.85, 'Date': '2026-01-18'},
                {'InvoiceID': 'INV-1005', 'Customer': 'Innovation Labs', 'Product': 'Mechanical Keyboard', 'Quantity': 8, 'Amount': 719.92, 'Date': '2026-01-19'},
                {'InvoiceID': 'INV-1006', 'Customer': 'CloudNet Services', 'Product': 'Webcam HD', 'Quantity': 12, 'Amount': 959.88, 'Date': '2026-01-20'},
                {'InvoiceID': 'INV-1007', 'Customer': 'SmartOffice Co', 'Product': 'Ergonomic Chair', 'Quantity': 3, 'Amount': 899.97, 'Date': '2026-01-21'},
            ]
        }
        
        # Load initial dataset
        self._load_dataset('Employees')
        self._update_status()
    
    def _load_dataset(self, dataset_name):
        """Load a specific dataset into the DataGridView."""
        if dataset_name not in self.datasets:
            return
        
        # Set datasource (this will auto-generate columns)
        self.datagridview.DataSource = self.datasets[dataset_name]
        
        # Adjust column widths
        if self.datagridview.Columns:
            for col in self.datagridview.Columns:
                if col.Name in ['ID', 'Code']:
                    col.Width = 60
                elif col.Name in ['InvoiceID']:
                    col.Width = 100
                elif col.Name in ['Name', 'Customer', 'Product']:
                    col.Width = 180
                elif col.Name in ['Department', 'Category', 'Position']:
                    col.Width = 140
                elif col.Name in ['Salary', 'Price', 'Amount']:
                    col.Width = 100
                elif col.Name in ['Stock', 'Quantity']:
                    col.Width = 80
                elif col.Name in ['Status', 'Date']:
                    col.Width = 100
                else:
                    col.Width = 120
    
    def _update_status(self):
        """Update status bar with current info."""
        total = len(self.datagridview.Rows)
        selected = len(self.datagridview.SelectedRows)
        
        self.lbl_status.Text = f'Ready | Total Rows: {total} | Selected: {selected}'
    
    # Event Handlers
    def _on_readonly_changed(self, sender, e):
        """Handle read-only toggle."""
        self.datagridview.ReadOnly = self.chk_readonly.Checked
    
    def _on_row_headers_changed(self, sender, e):
        """Handle row headers visibility toggle."""
        self.datagridview.RowHeadersVisible = self.chk_row_headers.Checked
    
    def _on_col_headers_changed(self, sender, e):
        """Handle column headers visibility toggle."""
        self.datagridview.ColumnHeadersVisible = self.chk_col_headers.Checked
    
    def _on_allow_add_changed(self, sender, e):
        """Handle allow add rows toggle."""
        self.datagridview.AllowUserToAddRows = self.chk_allow_add.Checked
    
    def _on_selection_mode_changed(self, sender, e):
        """Handle selection mode change."""
        mode_name = self.combo_selection.SelectedItem
        if mode_name == 'FullRowSelect':
            self.datagridview.SelectionMode = DataGridViewSelectionMode.FullRowSelect
        elif mode_name == 'CellSelect':
            self.datagridview.SelectionMode = DataGridViewSelectionMode.CellSelect
        elif mode_name == 'FullColumnSelect':
            self.datagridview.SelectionMode = DataGridViewSelectionMode.FullColumnSelect
    
    def _on_datasource_changed(self, sender, e):
        """Handle data source change."""
        dataset_name = self.combo_datasource.SelectedItem
        if dataset_name:
            self._load_dataset(dataset_name)
            self._update_status()
    
    def _on_selection_changed(self, sender, e):
        """Handle selection change."""
        self._update_status()
    
    def _on_cell_click(self, sender, e):
        """Handle cell click."""
        # Could show cell details here
        pass
    
    def _on_add_row(self, sender, e):
        """Handle add row button click."""
        dataset_name = self.combo_datasource.SelectedItem
        if not dataset_name:
            return
        
        # Create a new empty row based on dataset type
        if dataset_name == 'Employees':
            new_row = {
                'ID': f'{len(self.datasets[dataset_name]) + 1:03d}',
                'Name': 'New Employee',
                'Department': 'Unassigned',
                'Position': 'TBD',
                'Salary': 0,
                'Status': 'Pending'
            }
        elif dataset_name == 'Products':
            new_row = {
                'Code': f'P{len(self.datasets[dataset_name]) + 1:03d}',
                'Name': 'New Product',
                'Category': 'General',
                'Price': 0.0,
                'Stock': 0,
                'Supplier': 'TBD'
            }
        else:  # Sales
            new_row = {
                'InvoiceID': f'INV-{1000 + len(self.datasets[dataset_name]) + 1}',
                'Customer': 'New Customer',
                'Product': 'TBD',
                'Quantity': 0,
                'Amount': 0.0,
                'Date': '2026-01-26'
            }
        
        self.datasets[dataset_name].append(new_row)
        self._load_dataset(dataset_name)
        self._update_status()
        MessageBox.Show("New row added", "Add Row")
    
    def _on_delete_row(self, sender, e):
        """Handle delete row button click."""
        selected_rows = self.datagridview.SelectedRows
        if not selected_rows:
            MessageBox.Show("Please select row(s) to delete", "Delete Row")
            return
        
        dataset_name = self.combo_datasource.SelectedItem
        if not dataset_name:
            return
        
        # Get indices to delete (from end to start to avoid index issues)
        indices = []
        for row in selected_rows:
            try:
                idx = self.datagridview.Rows.IndexOf(row)
                if idx >= 0:
                    indices.append(idx)
            except:
                pass
        
        indices.sort(reverse=True)
        
        # Delete from dataset
        for idx in indices:
            if 0 <= idx < len(self.datasets[dataset_name]):
                del self.datasets[dataset_name][idx]
        
        self._load_dataset(dataset_name)
        self._update_status()
        MessageBox.Show(f"Deleted {len(indices)} row(s)", "Delete Row")
    
    def _on_clear_all(self, sender, e):
        """Handle clear all button click."""
        dataset_name = self.combo_datasource.SelectedItem
        if not dataset_name:
            return
        
        if len(self.datasets[dataset_name]) == 0:
            MessageBox.Show("Grid is already empty", "Clear All")
            return
        
        result = MessageBox.Show(
            "Are you sure you want to remove all rows?",
            "Confirm Clear",
            "YesNo"
        )
        if result == "Yes":
            self.datasets[dataset_name].clear()
            self._load_dataset(dataset_name)
            self._update_status()
            MessageBox.Show("All rows cleared", "Clear All")
    
    def _on_show_row_info(self, sender, e):
        """Show information about selected row."""
        selected_rows = self.datagridview.SelectedRows
        if not selected_rows:
            MessageBox.Show("No row selected", "Row Info")
            return
        
        row = selected_rows[0]
        dataset_name = self.combo_datasource.SelectedItem
        idx = self.datagridview.Rows.IndexOf(row)
        
        if 0 <= idx < len(self.datasets[dataset_name]):
            data = self.datasets[dataset_name][idx]
            info = f"Row {idx + 1} Details:\n\n"
            for key, value in data.items():
                info += f"{key}: {value}\n"
            MessageBox.Show(info, "Row Information")
    
    def _on_apply_filter(self, sender, e):
        """Apply filter to grid."""
        filter_text = self.txt_filter.Text.strip().lower()
        if not filter_text:
            MessageBox.Show("Please enter filter text", "Filter")
            return
        
        dataset_name = self.combo_datasource.SelectedItem
        if not dataset_name:
            return
        
        # Filter data
        original_data = self.datasets[dataset_name]
        filtered_data = []
        
        for row in original_data:
            # Search in all values
            if any(filter_text in str(value).lower() for value in row.values()):
                filtered_data.append(row)
        
        # Temporarily set filtered data
        self.datagridview.DataSource = filtered_data
        self._update_status()
        MessageBox.Show(f"Showing {len(filtered_data)} matching row(s)", "Filter Applied")
    
    def _on_clear_filter(self, sender, e):
        """Clear filter and show all data."""
        self.txt_filter.Text = ""
        dataset_name = self.combo_datasource.SelectedItem
        if dataset_name:
            self._load_dataset(dataset_name)
            self._update_status()


def main():
    """Application entry point."""
    app = DataGridViewExampleForm()
    Application.Run(app)


if __name__ == '__main__':
    main()
