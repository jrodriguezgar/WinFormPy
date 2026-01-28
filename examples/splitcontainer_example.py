"""
SplitContainer Example - Feature Demonstration

Demonstrates SplitContainer features:
- Switch between Horizontal/Vertical orientation
- Collapse/Expand panels (Panel1 and Panel2)
- Lock/Unlock splitter (disable dragging)
- Adjust splitter distance
- Customize splitter width
- Drag to resize panels
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from winformpy.winformpy import (
    Form, Panel, Label, Button, SplitContainer, TextBox, ToolTip,
    DockStyle, Orientation, Font, FontStyle, AnchorStyles
)


def main():
    # Create Form
    form = Form({
        'Text': 'SplitContainer - Feature Demo',
        'Width': 900,
        'Height': 650,
        'StartPosition': 'CenterScreen'
    })
    form.ApplyLayout()
    
    # Title Panel
    panel_title = Panel(form, {
        'Dock': DockStyle.Top,
        'Height': 60,
        'BackColor': '#0078D4'
    })
    
    Label(panel_title, {
        'Text': 'SplitContainer Demo',
        'Left': 20,
        'Top': 8,
        'Width': 860,
        'Height': 25,
        'BackColor': '#0078D4',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 14, FontStyle.Bold)
    })
    
    Label(panel_title, {
        'Text': 'Drag the splitter to resize panels • Use buttons to test features',
        'Left': 20,
        'Top': 35,
        'Width': 860,
        'Height': 20,
        'BackColor': '#0078D4',
        'ForeColor': '#E0E0E0',
        'Font': Font('Segoe UI', 9)
    })
    
    # Control Panel
    panel_controls = Panel(form, {
        'Dock': DockStyle.Top,
        'Height': 120,
        'BackColor': '#F5F5F5'
    })
    
    # Row 1: Orientation Controls
    Label(panel_controls, {
        'Text': 'Orientation:',
        'Left': 20,
        'Top': 15,
        'Width': 100,
        'Height': 25,
        'Font': Font('Segoe UI', 10, FontStyle.Bold)
    })
    
    btn_vertical = Button(panel_controls, {
        'Text': 'Vertical (Left|Right)',
        'Left': 130,
        'Top': 12,
        'Width': 150,
        'Height': 30,
        'BackColor': '#4CAF50',
        'ForeColor': '#FFFFFF'
    })
    
    btn_horizontal = Button(panel_controls, {
        'Text': 'Horizontal (Top|Bottom)',
        'Left': 290,
        'Top': 12,
        'Width': 150,
        'Height': 30
    })
    
    # Row 2: Panel Controls
    Label(panel_controls, {
        'Text': 'Panel Control:',
        'Left': 20,
        'Top': 55,
        'Width': 100,
        'Height': 25,
        'Font': Font('Segoe UI', 10, FontStyle.Bold)
    })
    
    btn_collapse1 = Button(panel_controls, {
        'Text': 'Collapse Panel1',
        'Left': 130,
        'Top': 52,
        'Width': 130,
        'Height': 30
    })
    
    btn_collapse2 = Button(panel_controls, {
        'Text': 'Collapse Panel2',
        'Left': 270,
        'Top': 52,
        'Width': 130,
        'Height': 30
    })
    
    btn_lock = Button(panel_controls, {
        'Text': 'Lock Splitter',
        'Left': 410,
        'Top': 52,
        'Width': 120,
        'Height': 30
    })
    
    # Row 3: Splitter Customization
    Label(panel_controls, {
        'Text': 'Distance:',
        'Left': 20,
        'Top': 93,
        'Width': 70,
        'Height': 25,
        'Font': Font('Segoe UI', 9)
    })
    
    txt_distance = TextBox(panel_controls, {
        'Text': '300',
        'Left': 90,
        'Top': 90,
        'Width': 60,
        'Height': 25
    })
    
    btn_set_distance = Button(panel_controls, {
        'Text': 'Apply',
        'Left': 160,
        'Top': 88,
        'Width': 60,
        'Height': 28
    })
    
    Label(panel_controls, {
        'Text': 'Width:',
        'Left': 240,
        'Top': 93,
        'Width': 50,
        'Height': 25,
        'Font': Font('Segoe UI', 9)
    })
    
    txt_width = TextBox(panel_controls, {
        'Text': '8',
        'Left': 290,
        'Top': 90,
        'Width': 40,
        'Height': 25
    })
    
    btn_set_width = Button(panel_controls, {
        'Text': 'Apply',
        'Left': 340,
        'Top': 88,
        'Width': 60,
        'Height': 28
    })
    
    btn_reset = Button(panel_controls, {
        'Text': 'Reset All',
        'Left': 420,
        'Top': 88,
        'Width': 100,
        'Height': 28,
        'BackColor': '#FFC107'
    })
    
    # ToolTips
    ToolTip(btn_collapse1, {'Text': 'Hides Panel1 completely and expands Panel2 to full size'})
    ToolTip(btn_collapse2, {'Text': 'Hides Panel2 completely and expands Panel1 to full size'})
    ToolTip(btn_lock, {'Text': 'Disables splitter dragging to prevent resizing panels'})
    ToolTip(btn_vertical, {'Text': 'Changes orientation to vertical (Left | Right panels)'})
    ToolTip(btn_horizontal, {'Text': 'Changes orientation to horizontal (Top | Bottom panels)'})
    
    # SplitContainer
    split = SplitContainer(form, {
        'Dock': DockStyle.Fill,
        'Orientation': Orientation.Vertical,
        'SplitterDistance': 300,
        'SplitterWidth': 8
    })
    
    # Panel1 Content
    label1 = Label(split.Panel1, {
        'Text': 'PANEL 1\n\n(Left Panel in Vertical mode)\n(Top Panel in Horizontal mode)\n\n' +
                'This is the first panel of the SplitContainer.\n' +
                'You can collapse, expand, and resize it.',
        'Dock': DockStyle.Fill,
        'BackColor': '#2E3440',
        'ForeColor': '#ECEFF4',
        'Font': Font('Segoe UI', 11),
        'TextAlign': 'MiddleCenter'
    })
    
    # Panel2 Content
    label2 = Label(split.Panel2, {
        'Text': 'PANEL 2\n\n(Right Panel in Vertical mode)\n(Bottom Panel in Horizontal mode)\n\n' +
                'This is the second panel of the SplitContainer.\n' +
                'Drag the splitter between panels to resize them.',
        'Dock': DockStyle.Fill,
        'BackColor': '#3B4252',
        'ForeColor': '#D8DEE9',
        'Font': Font('Segoe UI', 11),
        'TextAlign': 'MiddleCenter'
    })
    
    # Event Handlers
    def set_vertical(sender, e):
        split.Orientation = Orientation.Vertical
        split.SplitterDistance = 300
        btn_vertical.BackColor = '#4CAF50'
        btn_vertical.ForeColor = '#FFFFFF'
        btn_horizontal.BackColor = '#E0E0E0'
        btn_horizontal.ForeColor = '#000000'
        label1.Text = 'PANEL 1\n\n(Left Panel in Vertical mode)\n\n' + \
                      'Vertical orientation splits the container into\nleft and right panels.'
        label2.Text = 'PANEL 2\n\n(Right Panel in Vertical mode)\n\n' + \
                      'Drag the vertical splitter to adjust panel widths.'
    
    def set_horizontal(sender, e):
        split.Orientation = Orientation.Horizontal
        split.SplitterDistance = 200
        btn_horizontal.BackColor = '#4CAF50'
        btn_horizontal.ForeColor = '#FFFFFF'
        btn_vertical.BackColor = '#E0E0E0'
        btn_vertical.ForeColor = '#000000'
        label1.Text = 'PANEL 1\n\n(Top Panel in Horizontal mode)\n\n' + \
                      'Horizontal orientation splits the container into\ntop and bottom panels.'
        label2.Text = 'PANEL 2\n\n(Bottom Panel in Horizontal mode)\n\n' + \
                      'Drag the horizontal splitter to adjust panel heights.'
    
    def toggle_panel1(sender, e):
        split.Panel1Collapsed = not split.Panel1Collapsed
        btn_collapse1.Text = 'Expand Panel1' if split.Panel1Collapsed else 'Collapse Panel1'
    
    def toggle_panel2(sender, e):
        split.Panel2Collapsed = not split.Panel2Collapsed
        btn_collapse2.Text = 'Expand Panel2' if split.Panel2Collapsed else 'Collapse Panel2'
    
    def toggle_lock(sender, e):
        split.IsSplitterFixed = not split.IsSplitterFixed
        btn_lock.Text = 'Unlock Splitter' if split.IsSplitterFixed else 'Lock Splitter'
        btn_lock.BackColor = '#F44336' if split.IsSplitterFixed else '#E0E0E0'
        btn_lock.ForeColor = '#FFFFFF' if split.IsSplitterFixed else '#000000'
    
    def apply_distance(sender, e):
        try:
            distance = int(txt_distance.Text)
            split.SplitterDistance = max(50, min(distance, 700))
        except ValueError:
            txt_distance.Text = str(split.SplitterDistance)
    
    def apply_width(sender, e):
        try:
            width = int(txt_width.Text)
            split.SplitterWidth = max(1, min(width, 20))
            txt_width.Text = str(split.SplitterWidth)
        except ValueError:
            txt_width.Text = str(split.SplitterWidth)
    
    def reset_all(sender, e):
        split.Orientation = Orientation.Vertical
        split.SplitterDistance = 300
        split.SplitterWidth = 8
        split.Panel1Collapsed = False
        split.Panel2Collapsed = False
        split.IsSplitterFixed = False
        
        btn_vertical.BackColor = '#4CAF50'
        btn_vertical.ForeColor = '#FFFFFF'
        btn_horizontal.BackColor = '#E0E0E0'
        btn_horizontal.ForeColor = '#000000'
        btn_collapse1.Text = 'Collapse Panel1'
        btn_collapse2.Text = 'Collapse Panel2'
        btn_lock.Text = 'Lock Splitter'
        btn_lock.BackColor = '#E0E0E0'
        btn_lock.ForeColor = '#000000'
        txt_distance.Text = '300'
        txt_width.Text = '8'
        
        label1.Text = 'PANEL 1\n\n(Left Panel in Vertical mode)\n\n' + \
                      'This is the first panel of the SplitContainer.\n' + \
                      'You can collapse, expand, and resize it.'
        label2.Text = 'PANEL 2\n\n(Right Panel in Vertical mode)\n\n' + \
                      'This is the second panel of the SplitContainer.\n' + \
                      'Drag the splitter between panels to resize them.'
    
    # Bind Events
    btn_vertical.Click = set_vertical
    btn_horizontal.Click = set_horizontal
    btn_collapse1.Click = toggle_panel1
    btn_collapse2.Click = toggle_panel2
    btn_lock.Click = toggle_lock
    btn_set_distance.Click = apply_distance
    btn_set_width.Click = apply_width
    btn_reset.Click = reset_all
    
    # Show Form
    form.Show()


if __name__ == '__main__':
    main()
