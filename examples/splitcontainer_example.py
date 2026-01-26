"""
SplitContainer Example

This example demonstrates the use of SplitContainer control with basic features:

- Horizontal and Vertical orientations
- Adjustable SplitterDistance
- Collapse/Expand panels
- Lock/Unlock splitter
- SplitterMoved event
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from winformpy.winformpy import (
    Form, Panel, Label, Button, TextBox, SplitContainer,
    DockStyle, Orientation, BorderStyle, Font, FontStyle
)


def main():
    """Main entry point for the SplitContainer example."""
    
    # =========================================================================
    # Create Form
    # =========================================================================
    form = Form({
        'Text': 'SplitContainer - Operations Demo',
        'Width': 1000,
        'Height': 650,
        'StartPosition': 'CenterScreen'
    })
    form.ApplyLayout()
    
    # =========================================================================
    # Title Panel
    # =========================================================================
    title_panel = Panel(form, {
        'Dock': DockStyle.Top,
        'Height': 50,
        'BackColor': '#0078D4'
    })
    
    title_label = Label(title_panel, {
        'Text': 'SplitContainer - Operations Demo',
        'Left': 20,
        'Top': 12,
        'AutoSize': True,
        'Font': Font('Segoe UI', 16, FontStyle.Bold),
        'ForeColor': '#FFFFFF',
        'BackColor': '#0078D4'
    })
    
    # =========================================================================
    # Control Panel
    # =========================================================================
    control_panel = Panel(form, {
        'Dock': DockStyle.Top,
        'Height': 90,
        'BackColor': '#F5F5F5'
    })
    
    # Row 1: Distance and Toggle Controls
    Label(control_panel, {
        'Text': 'Distance:',
        'Left': 20,
        'Top': 15,
        'Width': 90,
        'AutoSize': True,
        'Font': Font('Segoe UI', 9)
    })
    
    txt_distance = TextBox(control_panel, {
        'Text': '300',
        'Left': 120,
        'Top': 12,
        'Width': 60
    })
    
    btn_set_distance = Button(control_panel, {
        'Text': 'Set',
        'Left': 190,
        'Top': 10,
        'Width': 50,
        'Height': 25
    })
    
    btn_toggle_fixed = Button(control_panel, {
        'Text': 'Lock Splitter',
        'Left': 260,
        'Top': 10,
        'Width': 110,
        'Height': 25
    })
    
    btn_collapse_p1 = Button(control_panel, {
        'Text': 'Collapse Panel1',
        'Left': 385,
        'Top': 10,
        'Width': 120,
        'Height': 25
    })
    
    btn_collapse_p2 = Button(control_panel, {
        'Text': 'Collapse Panel2',
        'Left': 515,
        'Top': 10,
        'Width': 120,
        'Height': 25
    })
    
    btn_reset = Button(control_panel, {
        'Text': 'Reset All',
        'Left': 640,
        'Top': 10,
        'Width': 90,
        'Height': 25
    })
    
    # Row 2: Orientation Controls
    Label(control_panel, {
        'Text': 'Orientation:',
        'Left': 20,
        'Top': 52,
        'Width': 90,
        'AutoSize': True,
        'Font': Font('Segoe UI', 9)
    })
    
    btn_vertical = Button(control_panel, {
        'Text': 'Vertical (L|R)',
        'Left': 120,
        'Top': 50,
        'Width': 120,
        'Height': 25,
        'BackColor': '#E3F2FD'
    })
    
    btn_horizontal = Button(control_panel, {
        'Text': 'Horizontal (T|B)',
        'Left': 250,
        'Top': 50,
        'Width': 120,
        'Height': 25
    })
    
    status_label = Label(control_panel, {
        'Text': 'Status: Ready - Drag the splitter to resize panels',
        'Left': 450,
        'Top': 50,
        'Width': 500,
        'Height': 40,
        'AutoSize': False,
        'Font': Font('Segoe UI', 9)
    })
    
    # =========================================================================
    # Main SplitContainer (Vertical - Left | Right)
    # =========================================================================
    split_main = SplitContainer(form, {
        'Dock': DockStyle.Fill,
        'Orientation': Orientation.Vertical,
        'SplitterDistance': 300,
        'SplitterWidth': 8,
        'BorderStyle': BorderStyle.Fixed3D
    })
    
    # =========================================================================
    # Panel 1 (Left)
    # =========================================================================
    panel1_header = Label(split_main.Panel1, {
        'Text': 'PANEL 1 (LEFT)',
        'Dock': DockStyle.Top,
        'Height': 40,
        'BackColor': '#E3F2FD',
        'Font': Font('Segoe UI', 12, FontStyle.Bold),
        'TextAlign': 'MiddleCenter'
    })
    
    panel1_content = TextBox(split_main.Panel1, {
        'Dock': DockStyle.Fill,
        'Multiline': True,
        'Text': '''PANEL 1 - Left Side

SplitContainer Operations:

• Drag the splitter to resize panels
• Set specific distance with textbox
• Lock/unlock the splitter
• Collapse/expand panels
• Change orientation (Vertical/Horizontal)
• Reset all settings

Try all the controls to test the operations!
''',
        'Font': Font('Segoe UI', 10),
        'ScrollBars': 'Vertical'
    })
    
    # =========================================================================
    # Panel 2 (Right)
    # =========================================================================
    panel2_header = Label(split_main.Panel2, {
        'Text': 'PANEL 2 (RIGHT)',
        'Dock': DockStyle.Top,
        'Height': 40,
        'BackColor': '#FFF3E0',
        'Font': Font('Segoe UI', 12, FontStyle.Bold),
        'TextAlign': 'MiddleCenter'
    })
    
    panel2_content = TextBox(split_main.Panel2, {
        'Dock': DockStyle.Fill,
        'Multiline': True,
        'Text': '''PANEL 2 - Right Side

Properties:

• Orientation: Vertical (Left | Right)
• SplitterDistance: 300px
• SplitterWidth: 8px
• BorderStyle: Fixed3D

Events:

• SplitterMoved: Triggered when splitter moves

Try the controls above to test all operations!
''',
        'Font': Font('Segoe UI', 10),
        'ScrollBars': 'Vertical'
    })
    
    # =========================================================================
    # Event Handlers
    # =========================================================================
    
    def on_splitter_moved(sender, e):
        distance = split_main.SplitterDistance
        status_label.Text = f'Status: Splitter at {distance}px'
        txt_distance.Text = str(distance)
    
    def on_set_distance(sender, e):
        try:
            distance = int(txt_distance.Text)
            split_main.SplitterDistance = distance
            status_label.Text = f'Status: Distance set to {distance}px'
        except ValueError:
            status_label.Text = 'Status: Invalid distance value!'
    
    def on_toggle_fixed(sender, e):
        split_main.IsSplitterFixed = not split_main.IsSplitterFixed
        if split_main.IsSplitterFixed:
            btn_toggle_fixed.Text = 'Unlock Splitter'
            status_label.Text = 'Status: Splitter LOCKED (cannot drag)'
        else:
            btn_toggle_fixed.Text = 'Lock Splitter'
            status_label.Text = 'Status: Splitter UNLOCKED (can drag)'
    
    def on_collapse_p1(sender, e):
        split_main.Panel1Collapsed = not split_main.Panel1Collapsed
        if split_main.Panel1Collapsed:
            btn_collapse_p1.Text = 'Expand Panel1'
            status_label.Text = 'Status: Panel1 COLLAPSED'
        else:
            btn_collapse_p1.Text = 'Collapse Panel1'
            status_label.Text = 'Status: Panel1 EXPANDED'
    
    def on_collapse_p2(sender, e):
        split_main.Panel2Collapsed = not split_main.Panel2Collapsed
        if split_main.Panel2Collapsed:
            btn_collapse_p2.Text = 'Expand Panel2'
            status_label.Text = 'Status: Panel2 COLLAPSED'
        else:
            btn_collapse_p2.Text = 'Collapse Panel2'
            status_label.Text = 'Status: Panel2 EXPANDED'
    
    def on_reset(sender, e):
        split_main.Panel1Collapsed = False
        split_main.Panel2Collapsed = False
        split_main.IsSplitterFixed = False
        split_main.SplitterDistance = 300
        
        btn_collapse_p1.Text = 'Collapse Panel1'
        btn_collapse_p2.Text = 'Collapse Panel2'
        btn_toggle_fixed.Text = 'Lock Splitter'
        txt_distance.Text = '300'
        status_label.Text = 'Status: All settings reset to defaults'
    
    def on_set_vertical(sender, e):
        split_main.Orientation = Orientation.Vertical
        btn_vertical.BackColor = '#E3F2FD'
        btn_horizontal.BackColor = '#F0F0F0'
        status_label.Text = 'Status: Orientation changed to VERTICAL (Left | Right)'
    
    def on_set_horizontal(sender, e):
        split_main.Orientation = Orientation.Horizontal
        btn_horizontal.BackColor = '#E3F2FD'
        btn_vertical.BackColor = '#F0F0F0'
        status_label.Text = 'Status: Orientation changed to HORIZONTAL (Top | Bottom)'
    
    # =========================================================================
    # Bind Events
    # =========================================================================
    split_main.SplitterMoved = on_splitter_moved
    btn_set_distance.Click = on_set_distance
    btn_toggle_fixed.Click = on_toggle_fixed
    btn_collapse_p1.Click = on_collapse_p1
    btn_collapse_p2.Click = on_collapse_p2
    btn_reset.Click = on_reset
    btn_vertical.Click = on_set_vertical
    btn_horizontal.Click = on_set_horizontal
    
    # =========================================================================
    # Show Form
    # =========================================================================
    form.Show()


if __name__ == '__main__':
    main()
