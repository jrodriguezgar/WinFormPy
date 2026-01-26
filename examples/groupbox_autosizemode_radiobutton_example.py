"""
GroupBox AutoSizeMode and RadioButton Example

Demonstrates how GroupBox automatically adjusts its size when adding options.
Shows the difference between GrowAndShrink and GrowOnly modes.
"""

from winformpy import (
    Form, Panel, GroupBox, RadioButton, Button, Label, Application,
    Font, FontStyle, AutoSizeMode
)


def main():
    # =========================================================================
    # Create main form
    # =========================================================================
    form = Form({
        'Text': 'GroupBox AutoSizeMode with RadioButtons',
        'Width': 900,
        'Height': 650,
        'StartPosition': 'CenterScreen'
    })
    form.ApplyLayout()

    # =========================================================================
    # Title Panel
    # =========================================================================
    title_panel = Panel(form, {
        'Height': 60,
        'BackColor': '#0078D4'
    })
    title_panel.Dock = 'Top'
    
    Label(title_panel, {
        'Text': 'GroupBox AutoSizeMode Demo',
        'Left': 20,
        'Top': 15,
        'AutoSize': True,
        'Font': Font('Segoe UI', 16, FontStyle.Bold),
        'ForeColor': '#FFFFFF',
        'BackColor': '#0078D4'
    })

    # =========================================================================
    # Main Content Panel
    # =========================================================================
    main_panel = Panel(form, {
        'BackColor': '#F5F5F5'
    })
    main_panel.Dock = 'Fill'

    # =========================================================================
    # GroupBox 1: GrowAndShrink (adjusts exactly to content)
    # =========================================================================
    gb_shrink = GroupBox(main_panel, {
        'Text': 'Mode: GrowAndShrink',
        'Left': 20,
        'Top': 20,
        'AutoSize': True,
        'AutoSizeMode': AutoSizeMode.GrowAndShrink,
        'BackColor': '#e6f7ff',
        'Font': Font('Segoe UI', 10, FontStyle.Bold)
    })

    # Add initial RadioButtons
    RadioButton(gb_shrink, {
        'Text': 'Option A',
        'Left': 15,
        'Top': 25,
        'Width': 100,
        'Checked': True,
        'Font': Font('Segoe UI', 9)
    })

    RadioButton(gb_shrink, {
        'Text': 'Option B',
        'Left': 15,
        'Top': 55,
        'Width': 100,
        'Font': Font('Segoe UI', 9)
    })

    # =========================================================================
    # GroupBox 2: GrowOnly (grows but doesn't shrink beyond original size)
    # =========================================================================
    gb_grow = GroupBox(main_panel, {
        'Text': 'Mode: GrowOnly (Min 200x60)',
        'Left': 400,
        'Top': 20,
        'Width': 200,
        'Height': 60,
        'AutoSize': True,
        'AutoSizeMode': AutoSizeMode.GrowOnly,
        'BackColor': '#f6ffed',
        'Font': Font('Segoe UI', 10, FontStyle.Bold)
    })

    RadioButton(gb_grow, {
        'Text': 'Option 1',
        'Left': 15,
        'Top': 25,
        'Width': 100,
        'Checked': True,
        'Font': Font('Segoe UI', 9)
    })

    # =========================================================================
    # Info Labels
    # =========================================================================
    lbl_info = Label(main_panel, {
        'Text': 'Add or remove options to see how GroupBoxes behave:',
        'Left': 20,
        'Top': 250,
        'Width': 450,
        'AutoSize': True,
        'Font': Font('Segoe UI', 10)
    })

    lbl_size_shrink = Label(main_panel, {
        'Text': 'Size: 0x0',
        'Left': 20,
        'Top': 280,
        'Width': 150,
        'ForeColor': '#0078D4',
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })

    lbl_size_grow = Label(main_panel, {
        'Text': 'Size: 0x0',
        'Left': 400,
        'Top': 280,
        'Width': 150,
        'ForeColor': '#107C10',
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })

    # =========================================================================
    # Layout Adjustment Function
    # =========================================================================
    def adjust_layout():
        """Adjusts control positions to avoid overlapping."""
        # Force geometry update
        form.UpdateLayout()
        
        # Update size labels
        lbl_size_shrink.Text = f"Size: {gb_shrink.Width}x{gb_shrink.Height}"
        lbl_size_grow.Text = f"Size: {gb_grow.Width}x{gb_grow.Height}"
        
        # Horizontal adjustment
        min_x_right = gb_shrink.Left + gb_shrink.Width + 20
        new_x_right = max(400, min_x_right)
        
        gb_grow.Left = new_x_right
        lbl_size_grow.Left = new_x_right
        btn_add_grow_v.Left = new_x_right
        btn_add_grow_h.Left = new_x_right
        btn_remove_grow.Left = new_x_right
        
        # Vertical adjustment
        bottom_shrink = gb_shrink.Top + gb_shrink.Height
        bottom_grow = gb_grow.Top + gb_grow.Height
        max_bottom = max(bottom_shrink, bottom_grow)
        
        margin = 20
        start_y = max(250, max_bottom + margin)
        
        lbl_info.Top = start_y
        lbl_size_shrink.Top = start_y + 30
        lbl_size_grow.Top = start_y + 30
        
        btn_add_shrink_v.Top = start_y + 60
        btn_add_shrink_h.Top = start_y + 95
        btn_remove_shrink.Top = start_y + 130
        
        btn_add_grow_v.Top = start_y + 60
        btn_add_grow_h.Top = start_y + 95
        btn_remove_grow.Top = start_y + 130
        
        # Force visual update
        controls_to_update = [
            gb_grow, lbl_info, lbl_size_shrink, lbl_size_grow,
            btn_add_shrink_v, btn_add_shrink_h, btn_remove_shrink,
            btn_add_grow_v, btn_add_grow_h, btn_remove_grow
        ]
        
        for c in controls_to_update:
            c.PerformLayout()
        
        # Adjust form size if needed
        required_width = new_x_right + gb_grow.Width + 40
        required_height = btn_remove_grow.Top + btn_remove_grow.Height + 60
        
        if form.Width < required_width:
            form.Width = required_width
            form.SetGeometry(form.Width, form.Height)
        if form.Height < required_height:
            form.Height = required_height
            form.SetGeometry(form.Width, form.Height)
        
        form.Update()

    # Bind resize events
    gb_shrink.Resize = adjust_layout
    gb_grow.Resize = adjust_layout

    # =========================================================================
    # Button Event Handlers - GrowAndShrink GroupBox
    # =========================================================================
    def add_shrink_vertical():
        """Add a RadioButton vertically to the GrowAndShrink GroupBox."""
        max_bottom = 0
        for c in gb_shrink.Controls:
            if hasattr(c, 'Top') and hasattr(c, 'Height'):
                max_bottom = max(max_bottom, c.Top + c.Height)
        
        if max_bottom == 0:
            max_bottom = 10
        
        count = len([c for c in gb_shrink.Controls if isinstance(c, RadioButton)])
        RadioButton(gb_shrink, {
            'Text': f'V-{count+1}',
            'Left': 15,
            'Top': max_bottom + 5,
            'Width': 80,
            'Font': Font('Segoe UI', 9)
        })
        adjust_layout()

    def add_shrink_horizontal():
        """Add a RadioButton horizontally to the GrowAndShrink GroupBox."""
        max_right = 0
        for c in gb_shrink.Controls:
            c.Refresh()
            if hasattr(c, 'Left') and hasattr(c, 'Width'):
                max_right = max(max_right, c.Left + c.Width)
        
        if max_right == 0:
            max_right = 10
        
        count = len([c for c in gb_shrink.Controls if isinstance(c, RadioButton)])
        RadioButton(gb_shrink, {
            'Text': f'H-{count+1}',
            'Left': max_right + 5,
            'Top': 25,
            'Width': 80,
            'Font': Font('Segoe UI', 9)
        })
        adjust_layout()

    def remove_option_shrink():
        """Remove the last RadioButton from the GrowAndShrink GroupBox."""
        radios = [c for c in gb_shrink.Controls if isinstance(c, RadioButton)]
        if radios:
            gb_shrink.RemoveControl(radios[-1])
        adjust_layout()

    # Buttons for GrowAndShrink GroupBox
    btn_add_shrink_v = Button(main_panel, {
        'Text': 'Add Option (V)',
        'Left': 20,
        'Top': 310,
        'Width': 150,
        'Height': 30,
        'BackColor': '#0078D4',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9)
    })
    btn_add_shrink_v.Click = lambda s, e: add_shrink_vertical()

    btn_add_shrink_h = Button(main_panel, {
        'Text': 'Add Option (H)',
        'Left': 20,
        'Top': 345,
        'Width': 150,
        'Height': 30,
        'BackColor': '#0078D4',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9)
    })
    btn_add_shrink_h.Click = lambda s, e: add_shrink_horizontal()

    btn_remove_shrink = Button(main_panel, {
        'Text': 'Remove Last (-)',
        'Left': 20,
        'Top': 380,
        'Width': 150,
        'Height': 30,
        'BackColor': '#D83B01',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9)
    })
    btn_remove_shrink.Click = lambda s, e: remove_option_shrink()

    # =========================================================================
    # Button Event Handlers - GrowOnly GroupBox
    # =========================================================================
    def add_grow_vertical():
        """Add a RadioButton vertically to the GrowOnly GroupBox."""
        max_bottom = 0
        for c in gb_grow.Controls:
            if hasattr(c, 'Top') and hasattr(c, 'Height'):
                max_bottom = max(max_bottom, c.Top + c.Height)
        
        if max_bottom == 0:
            max_bottom = 10
        
        count = len([c for c in gb_grow.Controls if isinstance(c, RadioButton)])
        RadioButton(gb_grow, {
            'Text': f'V-{count+1}',
            'Left': 15,
            'Top': max_bottom + 5,
            'Width': 80,
            'Font': Font('Segoe UI', 9)
        })
        adjust_layout()

    def add_grow_horizontal():
        """Add a RadioButton horizontally to the GrowOnly GroupBox."""
        max_right = 0
        for c in gb_grow.Controls:
            c.Refresh()
            if hasattr(c, 'Left') and hasattr(c, 'Width'):
                max_right = max(max_right, c.Left + c.Width)
        
        if max_right == 0:
            max_right = 10
        
        count = len([c for c in gb_grow.Controls if isinstance(c, RadioButton)])
        RadioButton(gb_grow, {
            'Text': f'H-{count+1}',
            'Left': max_right + 5,
            'Top': 25,
            'Width': 80,
            'Font': Font('Segoe UI', 9)
        })
        adjust_layout()

    def remove_option_grow():
        """Remove the last RadioButton from the GrowOnly GroupBox."""
        radios = [c for c in gb_grow.Controls if isinstance(c, RadioButton)]
        if radios:
            gb_grow.RemoveControl(radios[-1])
        adjust_layout()

    # Buttons for GrowOnly GroupBox
    btn_add_grow_v = Button(main_panel, {
        'Text': 'Add Option (V)',
        'Left': 400,
        'Top': 310,
        'Width': 150,
        'Height': 30,
        'BackColor': '#107C10',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9)
    })
    btn_add_grow_v.Click = lambda s, e: add_grow_vertical()

    btn_add_grow_h = Button(main_panel, {
        'Text': 'Add Option (H)',
        'Left': 400,
        'Top': 345,
        'Width': 150,
        'Height': 30,
        'BackColor': '#107C10',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9)
    })
    btn_add_grow_h.Click = lambda s, e: add_grow_horizontal()

    btn_remove_grow = Button(main_panel, {
        'Text': 'Remove Last (-)',
        'Left': 400,
        'Top': 380,
        'Width': 150,
        'Height': 30,
        'BackColor': '#D83B01',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9)
    })
    btn_remove_grow.Click = lambda s, e: remove_option_grow()

    # =========================================================================
    # Initialize and run
    # =========================================================================
    adjust_layout()
    Application.Run(form)


if __name__ == '__main__':
    main()
