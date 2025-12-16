"""
Example demonstrating FlowLayoutPanel and TableLayoutPanel in WinFormPy.
"""

import sys
import os

# Add parent directory to path to import winformpy
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from winformpy.winformpy import (
    Application, Form, FlowLayoutPanel, TableLayoutPanel, 
    Button, Label, ComboBox, CheckBox, GroupBox, DockStyle
)

def create_layout_example():
    # 1. Main Form
    form = Form(None, {
        'Text': 'WinFormPy Layouts Example',
        'Width': 900,
        'Height': 700,
        'StartPosition': 'CenterScreen'
    })

    # 2. FlowLayoutPanel Section
    gb_flow = GroupBox(form, {
        'Text': 'FlowLayoutPanel Demo',
        'Left': 10, 'Top': 10, 'Width': 400, 'Height': 350
    })
    form.AddControl(gb_flow)

    # Controls to modify FlowLayoutPanel
    lbl_direction = Label(gb_flow, {'Text': 'Direction:', 'Left': 10, 'Top': 20, 'Width': 60})
    gb_flow.AddControl(lbl_direction)

    combo_direction = ComboBox(gb_flow, {
        'Left': 75, 'Top': 18, 'Width': 120,
        'Items': ['LeftToRight', 'TopDown', 'RightToLeft', 'BottomUp']
    })
    combo_direction.SelectedIndex = 0
    gb_flow.AddControl(combo_direction)

    chk_wrap = CheckBox(gb_flow, {'Text': 'Wrap Contents', 'Left': 210, 'Top': 20, 'Checked': True})
    gb_flow.AddControl(chk_wrap)

    # The FlowLayoutPanel itself
    flow_panel = FlowLayoutPanel(gb_flow, {
        'Left': 10, 'Top': 50, 'Width': 380, 'Height': 280,
        'BorderStyle': 'FixedSingle',
        'BackColor': 'White',
        'AutoScroll': True
    })
    gb_flow.AddControl(flow_panel)

    # Add many buttons to demonstrate flow
    for i in range(1, 13):
        btn = Button(flow_panel, {
            'Text': f'Btn {i}',
            'Width': 80, 'Height': 40,
            'Margin': (3, 3, 3, 3)
        })
        flow_panel.AddControl(btn)

    # Events for FlowLayoutPanel configuration
    def on_direction_change(sender, e):
        flow_panel.FlowDirection = combo_direction.SelectedItem
    combo_direction.SelectedIndexChanged = on_direction_change

    def on_wrap_change(sender, e):
        flow_panel.WrapContents = chk_wrap.Checked
    chk_wrap.CheckedChanged = on_wrap_change


    # 3. TableLayoutPanel Section
    gb_table = GroupBox(form, {
        'Text': 'TableLayoutPanel Demo',
        'Left': 420, 'Top': 10, 'Width': 450, 'Height': 350
    })
    form.AddControl(gb_table)

    # The TableLayoutPanel
    # 3 Columns: 25%, 50%, 25%
    # 3 Rows: Absolute 40px, Percent 100%, AutoSize
    table_panel = TableLayoutPanel(gb_table, {
        'Left': 10, 'Top': 20, 'Width': 430, 'Height': 310,
        'ColumnCount': 3,
        'RowCount': 3,
        'ColumnStyles': [
            ('Percent', 25),
            ('Percent', 50),
            ('Percent', 25)
        ],
        'RowStyles': [
            ('Absolute', 40),
            ('Percent', 100),
            ('AutoSize', 0)
        ],
        'CellBorderStyle': 'Single',
        'BackColor': 'WhiteSmoke'
    })
    gb_table.AddControl(table_panel)

    # Row 0: Header spanning all columns
    lbl_header = Label(table_panel, {
        'Text': 'Header (Spans 3 Columns)',
        'TextAlign': 'MiddleCenter',
        'Dock': 'Fill',
        'BackColor': 'LightBlue',
        'Font': ('Segoe UI', 10, 'bold')
    })
    table_panel.AddControl(lbl_header, 0, 0)
    table_panel.SetColumnSpan(lbl_header, 3)

    # Row 1, Col 0: Left Sidebar
    btn_left = Button(table_panel, {'Text': 'Left\n(25%)', 'Dock': 'Fill'})
    table_panel.AddControl(btn_left, 0, 1)

    # Row 1, Col 1: Main Content
    txt_content = Label(table_panel, {
        'Text': 'Main Content Area (50%)\nResizes with window if anchored properly.',
        'Dock': 'Fill',
        'BackColor': 'White',
        'BorderStyle': 'Fixed3D',
        'TextAlign': 'MiddleCenter'
    })
    table_panel.AddControl(txt_content, 1, 1)

    # Row 1, Col 2: Right Sidebar
    btn_right = Button(table_panel, {'Text': 'Right\n(25%)', 'Dock': 'Fill'})
    table_panel.AddControl(btn_right, 2, 1)

    # Row 2: Footer (AutoSize)
    lbl_footer = Label(table_panel, {
        'Text': 'Footer (AutoSize Row) - Spans 3 Columns',
        'Dock': 'Fill',
        'BackColor': 'LightGray',
        'Height': 30  # Preferred height for AutoSize
    })
    table_panel.AddControl(lbl_footer, 0, 2)
    table_panel.SetColumnSpan(lbl_footer, 3)


    # 4. Complex Nested Layout (Table inside Flow)
    gb_nested = GroupBox(form, {
        'Text': 'Nested Layouts',
        'Left': 10, 'Top': 370, 'Width': 860, 'Height': 280,
        'Anchor': ['Top', 'Left', 'Right', 'Bottom']
    })
    form.AddControl(gb_nested)

    nested_table = TableLayoutPanel(gb_nested, {
        'Dock': 'Fill',
        'ColumnCount': 2,
        'RowCount': 1,
        'Padding': (10, 10, 10, 10)
    })
    gb_nested.AddControl(nested_table)

    # Left side of nested: A FlowLayoutPanel acting as a toolbar
    toolbar_flow = FlowLayoutPanel(nested_table, {
        'Dock': 'Fill',
        'FlowDirection': 'TopDown',
        'BorderStyle': 'Fixed3D'
    })
    nested_table.AddControl(toolbar_flow, 0, 0)

    for i in range(5):
        toolbar_flow.AddControl(Button(toolbar_flow, {'Text': f'Tool {i+1}', 'Width': 100}))

    # Right side: A large area
    display_area = Label(nested_table, {
        'Text': 'Nested TableLayoutPanel > Cell 1\nContains this Label\n\nCell 0 contains a FlowLayoutPanel',
        'Dock': 'Fill',
        'BackColor': 'AliceBlue',
        'TextAlign': 'MiddleCenter',
        'BorderStyle': 'FixedSingle'
    })
    nested_table.AddControl(display_area, 1, 0)

    Application.Run(form)

if __name__ == '__main__':
    create_layout_example()
