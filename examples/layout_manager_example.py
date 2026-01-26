"""LayoutManager Example

Demonstrates LayoutManager capabilities with different distributions and alignments:
- Vertical Layout (UpDown)
- Horizontal Layout (LeftRight)
- Flow Layout with wrapping
- Up-Down Wrap Layout
- Fixed Wrap Horizontal/Vertical
"""

from winformpy import (
    Form, Panel, Label, Button, TextBox, CheckBox,
    TabControl, TabPage, Application, Font, FontStyle, DockStyle
)
from winformpy.winformpy_tools import LayoutManager


def main():
    # =========================================================================
    # Create main form
    # =========================================================================
    form = Form({
        'Text': 'LayoutManager Demo',
        'Width': 900,
        'Height': 700,
        'StartPosition': 'CenterScreen',
        'WindowState': 'Maximized'
    })
    form.ApplyLayout()

    # =========================================================================
    # Title Panel
    # =========================================================================
    title_panel = Panel(form, {
        'Height': 60,
        'BackColor': '#0078D4'
    })
    title_panel.Dock = DockStyle.Top
    
    Label(title_panel, {
        'Text': 'LayoutManager - Auto Layout Demonstrations',
        'Left': 20,
        'Top': 15,
        'AutoSize': True,
        'Font': Font('Segoe UI', 16, FontStyle.Bold),
        'ForeColor': '#FFFFFF',
        'BackColor': '#0078D4'
    })

    # =========================================================================
    # Main Content - TabControl
    # =========================================================================
    tab_control = TabControl(form, {
        'Font': Font('Segoe UI', 9)
    })
    tab_control.Dock = DockStyle.Fill

    # =========================================================================
    # Tab 1: Vertical Layout (Default)
    # =========================================================================
    tab_vertical = TabPage(tab_control, {
        'Text': 'Vertical'
    })

    Label(tab_vertical, {
        'Text': 'Vertical Layout (UpDown)',
        'Font': Font('Segoe UI', 10, FontStyle.Bold),
        'Top': 10,
        'Left': 10,
        'AutoSize': True,
        'ForeColor': '#0078D4'
    })

    panel_vertical = Panel(tab_vertical, {
        'Top': 40,
        'Left': 10,
        'Width': 200,
        'Height': 400,
        'BorderStyle': 'FixedSingle',
        'BackColor': '#FFFFFF'
    })

    layout_v = LayoutManager(panel_vertical, margin=5, padding=10, autosize_container=True)
    # Default is UpDown, TopLeft

    # Add controls for vertical layout
    for i in range(10):
        lbl = Label(panel_vertical, {
            'Text': f'{i*2+1}. Field {i+1}:',
            'AutoSize': True,
            'Font': Font('Segoe UI', 9)
        })
        layout_v.add_control(lbl)
        
        txt = TextBox(panel_vertical, {
            'Text': f'{i*2+2}. Value {i+1}',
            'Width': 150,
            'Font': Font('Segoe UI', 9)
        })
        layout_v.add_control(txt)

    # =========================================================================
    # Tab 2: Horizontal Layout (LeftRight)
    # =========================================================================
    tab_horizontal = TabPage(tab_control, {
        'Text': 'Horizontal'
    })

    Label(tab_horizontal, {
        'Text': 'Horizontal Layout (LeftRight)',
        'Font': Font('Segoe UI', 10, FontStyle.Bold),
        'Top': 10,
        'Left': 10,
        'AutoSize': True,
        'ForeColor': '#0078D4'
    })

    panel_horizontal = Panel(tab_horizontal, {
        'Top': 40,
        'Left': 10,
        'Width': 700,
        'Height': 200,
        'BorderStyle': 'FixedSingle',
        'BackColor': '#FFFFFF'
    })

    layout_h = LayoutManager(panel_horizontal, margin=5, padding=10, autosize_container=True)
    layout_h.layout_type = LayoutManager.LayoutType.FlowLayout
    layout_h.distribution = LayoutManager.Distribution.LeftRight

    # Add controls for horizontal layout
    for i in range(6):  # Reduced to 6 for better visualization
        btn = Button(panel_horizontal, {
            'Text': f'{i*2+1}. Action',
            'Width': 90,
            'Height': 30,
            'Font': Font('Segoe UI', 9)
        })
        layout_h.add_control(btn)
        
        chk = CheckBox(panel_horizontal, {
            'Text': f'{i*2+2}. Enable',
            'Width': 90,
            'Font': Font('Segoe UI', 9)
        })
        layout_h.add_control(chk)

    # =========================================================================
    # Tab 3: Flow Layout (Wrapping)
    # =========================================================================
    tab_flow = TabPage(tab_control, {
        'Text': 'Flow Layout'
    })

    Label(tab_flow, {
        'Text': 'Flow Layout (LeftRight + Auto Wrap) - Controls wrap to next row when space runs out',
        'Font': Font('Segoe UI', 10, FontStyle.Bold),
        'Top': 10,
        'Left': 10,
        'Width': 700,
        'ForeColor': '#0078D4'
    })

    panel_flow = Panel(tab_flow, {
        'Top': 50,
        'Left': 10,
        'Width': 520,  # Width for 6 buttons per row (6 * 80 + 2 * 10 padding)
        'Height': 350,
        'BorderStyle': 'FixedSingle',
        'BackColor': '#F9F9F9'
    })

    layout_flow = LayoutManager(panel_flow, margin=5, padding=10, autosize_container=False)
    layout_flow.layout_type = LayoutManager.LayoutType.FlowLayout
    layout_flow.distribution = LayoutManager.Distribution.LeftRight

    # Add 24 buttons - 4 rows of 6 buttons with alternating colors
    for i in range(24):
        row_num = i // 6  # Which row (0-3)
        btn = Button(panel_flow, {
            'Text': f'{i+1}',
            'Width': 75,
            'Height': 30,
            'Font': Font('Segoe UI', 9, FontStyle.Bold),
            'BackColor': '#0078D4' if row_num % 2 == 0 else '#107C10',  # Blue for rows 0,2 / Green for rows 1,3
            'ForeColor': '#FFFFFF'
        })
        layout_flow.add_control(btn)

    # =========================================================================
    # Tab 4: Up-Down Wrap Layout
    # =========================================================================
    tab_updown_wrap = TabPage(tab_control, {
        'Text': 'Up-Down Wrap'
    })

    Label(tab_updown_wrap, {
        'Text': 'Up-Down Layout (Wrap)',
        'Font': Font('Segoe UI', 10, FontStyle.Bold),
        'Top': 10,
        'Left': 10,
        'AutoSize': True,
        'ForeColor': '#0078D4'
    })

    panel_ud_wrap = Panel(tab_updown_wrap, {
        'Top': 40,
        'Left': 10,
        'Width': 400,
        'Height': 300,
        'BorderStyle': 'FixedSingle',
        'BackColor': '#FFFFFF'
    })

    layout_ud_wrap = LayoutManager(panel_ud_wrap, margin=5, padding=10, autosize_container=True)
    layout_ud_wrap.distribution = LayoutManager.Distribution.UpDown
    layout_ud_wrap.layout_type = LayoutManager.LayoutType.FlowLayout

    # Add controls for up-down wrap layout
    for i in range(20):
        btn = Button(panel_ud_wrap, {
            'Text': f'{i*2+1}. Cmd',
            'Width': 70,
            'Font': Font('Segoe UI', 8)
        })
        layout_ud_wrap.add_control(btn)
        
        chk = CheckBox(panel_ud_wrap, {
            'Text': f'{i*2+2}. Opt',
            'Font': Font('Segoe UI', 8)
        })
        layout_ud_wrap.add_control(chk)

    # =========================================================================
    # Tab 5: Fixed Wrap Horizontal (5 items per row)
    # =========================================================================
    tab_fixed_h = TabPage(tab_control, {
        'Text': 'Fixed Wrap H (5)'
    })

    Label(tab_fixed_h, {
        'Text': 'Fixed Wrap Horizontal (5 items per row)',
        'Font': Font('Segoe UI', 10, FontStyle.Bold),
        'Top': 10,
        'Left': 10,
        'AutoSize': True,
        'ForeColor': '#0078D4'
    })

    panel_fixed_h = Panel(tab_fixed_h, {
        'Top': 40,
        'Left': 10,
        'Width': 400,
        'Height': 300,
        'BorderStyle': 'FixedSingle',
        'BackColor': '#FFFFFF'
    })

    # Initialize with wrap_count=5
    layout_fixed_h = LayoutManager(panel_fixed_h, margin=5, padding=10, autosize_container=True, wrap_count=5)
    layout_fixed_h.layout_type = LayoutManager.LayoutType.FlowLayout
    layout_fixed_h.distribution = LayoutManager.Distribution.LeftRight

    for i in range(20):
        btn = Button(panel_fixed_h, {
            'Text': f'{i+1}. Item',
            'Width': 80,
            'Font': Font('Segoe UI', 9)
        })
        layout_fixed_h.add_control(btn)

    # =========================================================================
    # Tab 6: Fixed Wrap Vertical (5 items per column)
    # =========================================================================
    tab_fixed_v = TabPage(tab_control, {
        'Text': 'Fixed Wrap V (5)'
    })

    Label(tab_fixed_v, {
        'Text': 'Fixed Wrap Vertical (5 items per column)',
        'Font': Font('Segoe UI', 10, FontStyle.Bold),
        'Top': 10,
        'Left': 10,
        'AutoSize': True,
        'ForeColor': '#0078D4'
    })

    panel_fixed_v = Panel(tab_fixed_v, {
        'Top': 40,
        'Left': 10,
        'Width': 400,
        'Height': 300,
        'BorderStyle': 'FixedSingle',
        'BackColor': '#FFFFFF'
    })

    # Initialize with wrap_count=5
    layout_fixed_v = LayoutManager(panel_fixed_v, margin=5, padding=10, autosize_container=True, wrap_count=5)
    layout_fixed_v.layout_type = LayoutManager.LayoutType.FlowLayout
    layout_fixed_v.distribution = LayoutManager.Distribution.UpDown

    for i in range(20):
        btn = Button(panel_fixed_v, {
            'Text': f'{i+1}. Item',
            'Width': 80,
            'Font': Font('Segoe UI', 9)
        })
        layout_fixed_v.add_control(btn)

    # =========================================================================
    # Run application
    # =========================================================================
    Application.Run(form)


if __name__ == "__main__":
    main()
