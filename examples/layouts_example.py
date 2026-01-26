"""
Layouts Example - FlowLayoutPanel and TableLayoutPanel Demonstration

This example demonstrates the two main container layout controls in WinFormPy:

1. FlowLayoutPanel - Automatic flowing layout with configurable direction
2. TableLayoutPanel - Grid-based layout with rows and columns

FEATURES DEMONSTRATED:
- FlowDirection: LeftToRight, TopDown, RightToLeft, BottomUp
- WrapContents: Enable/disable automatic wrapping
- ColumnStyles: Percent, Absolute, AutoSize
- RowStyles: Percent, Absolute, AutoSize
- Column/Row spanning for merged cells
- Nested layouts (TableLayout containing FlowLayout)
"""

from winformpy.winformpy import (
    Application, Form, FlowLayoutPanel, TableLayoutPanel,
    Button, Label, ComboBox, CheckBox, Panel, TabControl, TabPage,
    DockStyle, Font, FontStyle
)


def create_flowlayout_tab(tab_control):
    """Create FlowLayoutPanel demonstration tab."""
    tab = TabPage(tab_control, {'Text': 'FlowLayoutPanel'})
    
    # Top panel for title
    title_panel = Panel(tab, {
        'Height': 90,
        'BackColor': '#F0F0F0'
    })
    title_panel.Dock = DockStyle.Top
    
    Label(title_panel, {
        'Text': 'FlowLayoutPanel - Items flow automatically in the specified direction',
        'Font': Font('Segoe UI', 10, FontStyle.Bold),
        'Top': 10,
        'Left': 20,
        'AutoSize': True,
        'ForeColor': '#0078D4',
        'BackColor': '#F0F0F0'
    })
    
    Label(title_panel, {
        'Text': 'Change direction and wrap settings to see how items reorganize automatically',
        'Top': 35,
        'Left': 20,
        'AutoSize': True,
        'ForeColor': '#666666',
        'BackColor': '#F0F0F0',
        'Font': Font('Segoe UI', 9)
    })
    
    Label(title_panel, {
        'Text': 'Perfect for creating toolbars, button groups, or tag collections',
        'Top': 55,
        'Left': 20,
        'AutoSize': True,
        'ForeColor': '#666666',
        'BackColor': '#F0F0F0',
        'Font': Font('Segoe UI', 9)
    })
    
    # Configuration panel
    config_panel = Panel(tab, {
        'Height': 60,
        'BackColor': '#FFFFFF',
        'BorderStyle': 'FixedSingle'
    })
    config_panel.Dock = DockStyle.Top
    
    # Direction label
    Label(config_panel, {
        'Text': 'Flow Direction:',
        'Left': 20,
        'Top': 20,
        'AutoSize': True,
        'BackColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })
    
    # Direction combo
    combo_direction = ComboBox(config_panel, {
        'Items': ['LeftToRight', 'TopDown', 'RightToLeft', 'BottomUp'],
        'Left': 140,
        'Top': 17,
        'Width': 150
    })
    combo_direction.SelectedIndex = 0
    
    # Wrap checkbox
    chk_wrap = CheckBox(config_panel, {
        'Text': 'Enable Wrap Contents',
        'Left': 320,
        'Top': 19,
        'Width': 180,
        'Checked': True,
        'BackColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9)
    })
    
    # FlowLayoutPanel fills remaining space
    flow_panel = FlowLayoutPanel(tab, {
        'BorderStyle': 'FixedSingle',
        'BackColor': '#FFFFFF',
        'FlowDirection': 'LeftToRight',
        'WrapContents': True,
        'Padding': (15, 15, 15, 15)
    })
    flow_panel.Dock = DockStyle.Fill
    
    # Add sample items with colors
    colors = ["#E74C3C", "#3498DB", "#2ECC71", "#F39C12", "#9B59B6", "#1ABC9C", "#E67E22", "#95A5A6"]
    for i in range(20):
        btn = Button(flow_panel, {
            'Text': f'Item {i+1}',
            'Width': 100,
            'Height': 50,
            'BackColor': colors[i % len(colors)],
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9, FontStyle.Bold),
            'Margin': (5, 5, 5, 5)
        })
        flow_panel.AddControl(btn)
    
    # Event handlers
    def on_direction_change(sender, e):
        selected = combo_direction.SelectedItem
        if selected:
            # Use setter method to properly reconfigure and apply layout
            flow_panel.set_FlowDirection(selected)
    
    def on_wrap_change(sender, e):
        # Use setter method to properly reconfigure and apply layout
        flow_panel.set_WrapContents(chk_wrap.Checked)
    
    combo_direction.SelectedIndexChanged = on_direction_change
    chk_wrap.CheckedChanged = on_wrap_change


def create_tablelayout_tab(tab_control):
    """Create TableLayoutPanel demonstration tab - Simple 2x2 Grid Example."""
    tab = TabPage(tab_control, {'Text': 'TableLayoutPanel'})
    
    # Top panel for title
    title_panel = Panel(tab, {
        'Height': 90,
        'BackColor': '#F0F0F0'
    })
    title_panel.Dock = DockStyle.Top
    
    Label(title_panel, {
        'Text': 'TableLayoutPanel - Simple 2x2 Grid Example',
        'Font': Font('Segoe UI', 12, FontStyle.Bold),
        'Top': 15,
        'Left': 20,
        'AutoSize': True,
        'ForeColor': '#0078D4',
        'BackColor': '#F0F0F0'
    })
    
    Label(title_panel, {
        'Text': 'A grid layout with 2 columns (50% each) and 2 rows (50% each)',
        'Top': 45,
        'Left': 20,
        'AutoSize': True,
        'ForeColor': '#666666',
        'BackColor': '#F0F0F0',
        'Font': Font('Segoe UI', 9)
    })
    
    Label(title_panel, {
        'Text': 'Perfect for creating card layouts, dashboards, or organized content sections',
        'Top': 65,
        'Left': 20,
        'AutoSize': True,
        'ForeColor': '#666666',
        'BackColor': '#F0F0F0',
        'Font': Font('Segoe UI', 9)
    })
    
    # TableLayoutPanel - Simple 2x2 Grid
    table = TableLayoutPanel(tab, {
        'Left': 40,
        'Top': 110,
        'Width': 820,
        'Height': 450,
        'CellBorderStyle': 'Single',
        'BackColor': '#DDDDDD',
        'ColumnCount': 2,
        'RowCount': 2,
        'ColumnStyles': [
            ('Percent', 50),
            ('Percent', 50)
        ],
        'RowStyles': [
            ('Percent', 50),
            ('Percent', 50)
        ]
    })
    
    # Cell [0, 0]: Top-Left - Dashboard Card
    cell_1 = Panel(table, {
        'Dock': DockStyle.Fill,
        'BackColor': '#E74C3C',
        'BorderStyle': 'FixedSingle'
    })
    Label(cell_1, {
        'Text': '📊 SALES DASHBOARD\n\nTotal Sales: $45,230\nNew Orders: 128\nGrowth: +15%',
        'Dock': DockStyle.Fill,
        'TextAlign': 'MiddleCenter',
        'Font': Font('Segoe UI', 12, FontStyle.Bold),
        'ForeColor': '#FFFFFF',
        'BackColor': '#E74C3C'
    })
    table.AddControl(cell_1, 0, 0)
    
    # Cell [1, 0]: Top-Right - User Stats
    cell_2 = Panel(table, {
        'Dock': DockStyle.Fill,
        'BackColor': '#3498DB',
        'BorderStyle': 'FixedSingle'
    })
    Label(cell_2, {
        'Text': '👥 ACTIVE USERS\n\nOnline Now: 1,254\nNew Today: 89\nRetention: 92%',
        'Dock': DockStyle.Fill,
        'TextAlign': 'MiddleCenter',
        'Font': Font('Segoe UI', 12, FontStyle.Bold),
        'ForeColor': '#FFFFFF',
        'BackColor': '#3498DB'
    })
    table.AddControl(cell_2, 1, 0)
    
    # Cell [0, 1]: Bottom-Left - System Status
    cell_3 = Panel(table, {
        'Dock': DockStyle.Fill,
        'BackColor': '#2ECC71',
        'BorderStyle': 'FixedSingle'
    })
    Label(cell_3, {
        'Text': '⚙️ SYSTEM STATUS\n\nServer: Online ✓\nDatabase: Healthy ✓\nUptime: 99.9%',
        'Dock': DockStyle.Fill,
        'TextAlign': 'MiddleCenter',
        'Font': Font('Segoe UI', 12, FontStyle.Bold),
        'ForeColor': '#FFFFFF',
        'BackColor': '#2ECC71'
    })
    table.AddControl(cell_3, 0, 1)
    
    # Cell [1, 1]: Bottom-Right - Quick Actions
    cell_4 = Panel(table, {
        'Dock': DockStyle.Fill,
        'BackColor': '#F39C12',
        'BorderStyle': 'FixedSingle'
    })
    
    # Use FlowLayout for buttons in this cell
    flow = FlowLayoutPanel(cell_4, {
        'Dock': DockStyle.Fill,
        'FlowDirection': 'TopDown',
        'BackColor': '#F39C12',
        'Padding': (20, 40, 20, 20)
    })
    
    Label(flow, {
        'Text': '⚡ QUICK ACTIONS',
        'AutoSize': True,
        'Font': Font('Segoe UI', 12, FontStyle.Bold),
        'ForeColor': '#FFFFFF',
        'BackColor': '#F39C12',
        'Margin': (0, 0, 0, 20)
    })
    
    for action in ['New Report', 'Export Data', 'Settings']:
        Button(flow, {
            'Text': action,
            'Width': 180,
            'Height': 40,
            'Margin': (0, 5, 0, 5),
            'BackColor': '#FFFFFF',
            'ForeColor': '#F39C12',
            'Font': Font('Segoe UI', 10, FontStyle.Bold)
        })
    
    table.AddControl(cell_4, 1, 1)


def create_nested_tab(tab_control):
    """Create nested layouts demonstration tab - Simple Contact Card Example."""
    tab = TabPage(tab_control, {'Text': 'Nested Layouts'})
    
    # Top panel for title
    title_panel = Panel(tab, {
        'Height': 90,
        'BackColor': '#F0F0F0'
    })
    title_panel.Dock = DockStyle.Top
    
    Label(title_panel, {
        'Text': 'Nested Layouts - Contact Card Example',
        'Font': Font('Segoe UI', 12, FontStyle.Bold),
        'Top': 15,
        'Left': 20,
        'AutoSize': True,
        'ForeColor': '#0078D4',
        'BackColor': '#F0F0F0'
    })
    
    Label(title_panel, {
        'Text': 'Using TableLayoutPanel to create a structured contact card with profile section and details',
        'Top': 45,
        'Left': 20,
        'AutoSize': True,
        'ForeColor': '#666666',
        'BackColor': '#F0F0F0',
        'Font': Font('Segoe UI', 9)
    })
    
    Label(title_panel, {
        'Text': 'Demonstrates how to combine FlowLayoutPanel inside TableLayoutPanel cells',
        'Top': 65,
        'Left': 20,
        'AutoSize': True,
        'ForeColor': '#666666',
        'BackColor': '#F0F0F0',
        'Font': Font('Segoe UI', 9)
    })
    
    # Main TableLayoutPanel - 2 columns (Fixed 250px left, rest fills)
    main_table = TableLayoutPanel(tab, {
        'Left': 40,
        'Top': 110,
        'Width': 820,
        'Height': 450,
        'CellBorderStyle': 'Single',
        'BackColor': '#CCCCCC',
        'ColumnCount': 2,
        'RowCount': 1,
        'ColumnStyles': [
            ('Absolute', 250),
            ('Percent', 100)
        ],
        'RowStyles': [
            ('Percent', 100)
        ]
    })
    
    # LEFT CELL: Profile Photo and Basic Info (Using FlowLayout)
    left_cell = Panel(main_table, {
        'Dock': DockStyle.Fill,
        'BackColor': '#34495E',
        'BorderStyle': 'FixedSingle'
    })
    
    left_flow = FlowLayoutPanel(left_cell, {
        'Dock': DockStyle.Fill,
        'FlowDirection': 'TopDown',
        'BackColor': '#34495E',
        'Padding': (20, 30, 20, 20)
    })
    
    # Profile photo placeholder
    photo = Label(left_flow, {
        'Text': '👤',
        'Width': 120,
        'Height': 120,
        'TextAlign': 'MiddleCenter',
        'Font': Font('Segoe UI', 60),
        'BackColor': '#2C3E50',
        'ForeColor': '#ECF0F1',
        'BorderStyle': 'FixedSingle',
        'Margin': (25, 0, 0, 20)
    })
    
    # Name
    Label(left_flow, {
        'Text': 'John Doe',
        'AutoSize': True,
        'Font': Font('Segoe UI', 16, FontStyle.Bold),
        'ForeColor': '#FFFFFF',
        'BackColor': '#34495E',
        'Margin': (0, 10, 0, 5)
    })
    
    # Title
    Label(left_flow, {
        'Text': 'Senior Developer',
        'AutoSize': True,
        'Font': Font('Segoe UI', 11),
        'ForeColor': '#BDC3C7',
        'BackColor': '#34495E',
        'Margin': (0, 0, 0, 20)
    })
    
    # Contact button
    Button(left_flow, {
        'Text': '✉ Send Message',
        'Width': 200,
        'Height': 40,
        'BackColor': '#3498DB',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 10, FontStyle.Bold),
        'Margin': (0, 10, 0, 10)
    })
    
    main_table.AddControl(left_cell, 0, 0)
    
    # RIGHT CELL: Nested TableLayout for organized details
    right_cell = Panel(main_table, {
        'Dock': DockStyle.Fill,
        'BackColor': '#FFFFFF',
        'BorderStyle': 'FixedSingle'
    })
    
    # Nested TableLayout - 1 column, 4 rows for different sections
    details_table = TableLayoutPanel(right_cell, {
        'Dock': DockStyle.Fill,
        'BackColor': '#F8F8F8',
        'CellBorderStyle': 'Single',
        'ColumnCount': 1,
        'RowCount': 4,
        'ColumnStyles': [('Percent', 100)],
        'RowStyles': [
            ('Percent', 25),
            ('Percent', 25),
            ('Percent', 25),
            ('Percent', 25)
        ]
    })
    
    # Section 1: Contact Info
    section1 = Panel(details_table, {
        'Dock': DockStyle.Fill,
        'BackColor': '#ECF0F1'
    })
    flow1 = FlowLayoutPanel(section1, {
        'Dock': DockStyle.Fill,
        'FlowDirection': 'TopDown',
        'Padding': (15, 10, 15, 10),
        'BackColor': '#ECF0F1'
    })
    Label(flow1, {
        'Text': '📧 CONTACT',
        'AutoSize': True,
        'Font': Font('Segoe UI', 10, FontStyle.Bold),
        'ForeColor': '#2C3E50',
        'BackColor': '#ECF0F1',
        'Margin': (0, 0, 0, 10)
    })
    Label(flow1, {
        'Text': 'Email: john.doe@company.com\nPhone: +1 (555) 123-4567',
        'AutoSize': True,
        'Font': Font('Segoe UI', 9),
        'ForeColor': '#34495E',
        'BackColor': '#ECF0F1'
    })
    details_table.AddControl(section1, 0, 0)
    
    # Section 2: Location
    section2 = Panel(details_table, {
        'Dock': DockStyle.Fill,
        'BackColor': '#FFFFFF'
    })
    flow2 = FlowLayoutPanel(section2, {
        'Dock': DockStyle.Fill,
        'FlowDirection': 'TopDown',
        'Padding': (15, 10, 15, 10),
        'BackColor': '#FFFFFF'
    })
    Label(flow2, {
        'Text': '📍 LOCATION',
        'AutoSize': True,
        'Font': Font('Segoe UI', 10, FontStyle.Bold),
        'ForeColor': '#2C3E50',
        'BackColor': '#FFFFFF',
        'Margin': (0, 0, 0, 10)
    })
    Label(flow2, {
        'Text': 'Office: New York, USA\nTimezone: EST (UTC-5)',
        'AutoSize': True,
        'Font': Font('Segoe UI', 9),
        'ForeColor': '#34495E',
        'BackColor': '#FFFFFF'
    })
    details_table.AddControl(section2, 0, 1)
    
    # Section 3: Department
    section3 = Panel(details_table, {
        'Dock': DockStyle.Fill,
        'BackColor': '#ECF0F1'
    })
    flow3 = FlowLayoutPanel(section3, {
        'Dock': DockStyle.Fill,
        'FlowDirection': 'TopDown',
        'Padding': (15, 10, 15, 10),
        'BackColor': '#ECF0F1'
    })
    Label(flow3, {
        'Text': '🏢 DEPARTMENT',
        'AutoSize': True,
        'Font': Font('Segoe UI', 10, FontStyle.Bold),
        'ForeColor': '#2C3E50',
        'BackColor': '#ECF0F1',
        'Margin': (0, 0, 0, 10)
    })
    Label(flow3, {
        'Text': 'Team: Engineering\nManager: Jane Smith',
        'AutoSize': True,
        'Font': Font('Segoe UI', 9),
        'ForeColor': '#34495E',
        'BackColor': '#ECF0F1'
    })
    details_table.AddControl(section3, 0, 2)
    
    # Section 4: Skills
    section4 = Panel(details_table, {
        'Dock': DockStyle.Fill,
        'BackColor': '#FFFFFF'
    })
    flow4 = FlowLayoutPanel(section4, {
        'Dock': DockStyle.Fill,
        'FlowDirection': 'TopDown',
        'Padding': (15, 10, 15, 10),
        'BackColor': '#FFFFFF'
    })
    Label(flow4, {
        'Text': '💼 SKILLS',
        'AutoSize': True,
        'Font': Font('Segoe UI', 10, FontStyle.Bold),
        'ForeColor': '#2C3E50',
        'BackColor': '#FFFFFF',
        'Margin': (0, 0, 0, 10)
    })
    Label(flow4, {
        'Text': 'Python • JavaScript • C# • SQL\nDesign Patterns • Cloud Architecture',
        'AutoSize': True,
        'Font': Font('Segoe UI', 9),
        'ForeColor': '#34495E',
        'BackColor': '#FFFFFF'
    })
    details_table.AddControl(section4, 0, 3)
    
    main_table.AddControl(right_cell, 1, 0)


def main():
    """Application entry point."""
    # =========================================================================
    # Create main form
    # =========================================================================
    form = Form({
        'Text': 'WinFormPy Layouts - FlowLayoutPanel & TableLayoutPanel',
        'Width': 950,
        'Height': 720,
        'StartPosition': 'CenterScreen'
    })
    form.ApplyLayout()
    
    # =========================================================================
    # TOP PANEL - Title bar
    # =========================================================================
    top_panel = Panel(form, {
        'Height': 60,
        'BackColor': '#0078D4'
    })
    top_panel.Dock = DockStyle.Top
    
    Label(top_panel, {
        'Text': 'LAYOUTS DEMONSTRATION',
        'Left': 20,
        'Top': 10,
        'AutoSize': True,
        'Font': Font('Segoe UI', 16, FontStyle.Bold),
        'ForeColor': '#FFFFFF',
        'BackColor': '#0078D4'
    })
    
    Label(top_panel, {
        'Text': 'FlowLayoutPanel & TableLayoutPanel Examples',
        'Left': 20,
        'Top': 38,
        'AutoSize': True,
        'Font': Font('Segoe UI', 9),
        'ForeColor': '#E0E0E0',
        'BackColor': '#0078D4'
    })
    
    # =========================================================================
    # BOTTOM PANEL - Status bar
    # =========================================================================
    bottom_panel = Panel(form, {
        'Height': 35,
        'BackColor': '#34495E'
    })
    bottom_panel.Dock = DockStyle.Bottom
    
    Label(bottom_panel, {
        'Text': '⚡ Status: Ready | Layouts Active',
        'Left': 15,
        'Top': 8,
        'AutoSize': True,
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9),
        'BackColor': '#34495E'
    })
    
    # =========================================================================
    # MAIN PANEL - TabControl fills remaining space
    # =========================================================================
    main_panel = Panel(form, {
        'BackColor': '#F5F5F5'
    })
    main_panel.Dock = DockStyle.Fill
    
    # TabControl
    tabs = TabControl(main_panel, {
        'Dock': DockStyle.Fill,
        'Font': Font('Segoe UI', 9)
    })
    
    # Create tabs
    create_flowlayout_tab(tabs)
    create_tablelayout_tab(tabs)
    create_nested_tab(tabs)
    
    # Run application
    Application.Run(form)


if __name__ == '__main__':
    main()
