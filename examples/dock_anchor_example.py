"""
Dock and Anchor Demonstration

This example demonstrates the two main layout mechanisms in WinFormPy:

DOCKING:
- Attaches controls to container edges (Top, Bottom, Left, Right, Fill)
- Docked controls automatically resize with their parent
- Z-order determines docking priority (first added = outer edge)

ANCHORING:
- Maintains fixed distance from specified edges
- Default is [Top, Left] - control stays in fixed position
- Anchor to opposite edges (e.g., Top+Bottom) makes control stretch
- Perfect for buttons that should move with window resize

This demo shows practical examples of both mechanisms.
"""

from winformpy import (
    Form, Button, Panel, Label, Application,
    DockStyle, AnchorStyles, Font, FontStyle
)



def main():
    # =========================================================================
    # Create main form
    # =========================================================================
    form = Form({
        'Text': 'Dock and Anchor Demo',
        'Width': 1000,
        'Height': 700,
        'StartPosition': 'CenterScreen'
    })
    form.ApplyLayout()

    # =========================================================================
    # TOP PANEL - Docked to top edge
    # =========================================================================
    top_panel = Panel(form, {
        'Height': 100,
        'BackColor': '#0078D4'
    })
    top_panel.Dock = DockStyle.Top
    
    Label(top_panel, {
        'Text': 'TOP PANEL - Docked to Top',
        'Left': 10,
        'Top': 10,
        'AutoSize': True,
        'Font': Font('Segoe UI', 12, FontStyle.Bold),
        'ForeColor': '#FFFFFF',
        'BackColor': '#0078D4'
    })

    Button(top_panel, {
        'Text': 'Button 1',
        'Left': 10,
        'Top': 50,
        'Width': 100,
        'Height': 30
    })
    
    Button(top_panel, {
        'Text': 'Button 2',
        'Left': 120,
        'Top': 50,
        'Width': 100,
        'Height': 30
    })

    # =========================================================================
    # BOTTOM PANEL - Docked to bottom edge
    # =========================================================================
    bottom_panel = Panel(form, {
        'Height': 100,
        'BackColor': '#D83B01'
    })
    bottom_panel.Dock = DockStyle.Bottom
    
    lbl_status = Label(bottom_panel, {
        'Text': '⬇️ BOTTOM PANEL - Status: Ready',
        'Left': 10,
        'Top': 10,
        'AutoSize': True,
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 11, FontStyle.Bold),
        'BackColor': '#D83B01'
    })
    
    Button(bottom_panel, {
        'Text': 'Test 1',
        'Left': 10,
        'Top': 50,
        'Width': 100,
        'Height': 35,
        'BackColor': '#90EE90'
    })
    
    Button(bottom_panel, {
        'Text': 'Test 2',
        'Left': 120,
        'Top': 50,
        'Width': 100,
        'Height': 35,
        'BackColor': '#00CED1'
    })
    
    Button(bottom_panel, {
        'Text': 'Test 3',
        'Left': 230,
        'Top': 50,
        'Width': 100,
        'Height': 35,
        'BackColor': '#FFFF00',
        'ForeColor': '#000000'
    })

    # =========================================================================
    # LEFT PANEL - Docked to left edge
    # =========================================================================
    left_panel = Panel(form, {
        'Width': 150,
        'BackColor': '#B0C4DE'
    })
    left_panel.Dock = DockStyle.Left
    
    Label(left_panel, {
        'Text': 'LEFT\nPANEL',
        'Left': 40,
        'Top': 50,
        'AutoSize': True,
        'Font': Font('Segoe UI', 10, FontStyle.Bold),
        'ForeColor': '#000000'
    })

    # =========================================================================
    # MAIN PANEL - Fills remaining space
    # =========================================================================
    main_panel = Panel(form, {
        'BackColor': '#F5F5F5'
    })
    main_panel.Dock = DockStyle.Fill
    
    # Title
    Label(main_panel, {
        'Text': '⚓ ANCHORING DEMONSTRATION - Resize the window!',
        'Left': 20,
        'Top': 15,
        'AutoSize': True,
        'Font': Font('Segoe UI', 12, FontStyle.Bold),
        'ForeColor': '#000000'
    })
    
    # Info label
    Label(main_panel, {
        'Text': 'Anchor controls maintain FIXED DISTANCE from edges',
        'Left': 20,
        'Top': 45,
        'AutoSize': True,
        'Font': Font('Segoe UI', 9),
        'ForeColor': '#666666'
    })
    
    # =========================================================================
    # Anchored Buttons - Demonstrate different anchor combinations
    # =========================================================================
    
    # Top-Left button (default anchor)
    btn_tl = Button(main_panel, {
        'Text': 'Top+Left\n(Default)',
        'Left': 20,
        'Top': 80,
        'Width': 110,
        'Height': 60,
        'BackColor': '#1E90FF',
        'ForeColor': '#FFFFFF'
    })
    btn_tl.Anchor = AnchorStyles.Top | AnchorStyles.Left
    
    def on_tl_click(sender, event):
        lbl_status.Text = 'Status: Top+Left anchor - Fixed position'
    btn_tl.Click = on_tl_click
    
    # Top-Right button
    btn_tr = Button(main_panel, {
        'Text': 'Top+Right\n→ Moves',
        'Left': 580,
        'Top': 80,
        'Width': 110,
        'Height': 60,
        'BackColor': '#2E8B57',
        'ForeColor': '#FFFFFF'
    })
    btn_tr.Anchor = AnchorStyles.Top | AnchorStyles.Right
    
    def on_tr_click(sender, event):
        lbl_status.Text = 'Status: Top+Right anchor - Moves right on resize'
    btn_tr.Click = on_tr_click
    
    # Center label demonstrating vertical stretch
    lbl_stretch_v = Label(main_panel, {
        'Text': 'Top+Bottom+Left\nStretches\nVertically',
        'Left': 200,
        'Top': 80,
        'Width': 200,
        'Height': 150,
        'BackColor': '#FFFFE0',
        'BorderStyle': 'solid',
        'TextAlign': 'center',
        'Font': Font('Segoe UI', 14, FontStyle.Bold)
    })
    lbl_stretch_v.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left
    
    # Bottom-Left button
    btn_bl = Button(main_panel, {
        'Text': 'Bottom+Left\n↓ Moves',
        'Left': 20,
        'Top': 350,
        'Width': 110,
        'Height': 60,
        'BackColor': '#9370DB',
        'ForeColor': '#FFFFFF'
    })
    btn_bl.Anchor = AnchorStyles.Bottom | AnchorStyles.Left
    
    def on_bl_click(sender, event):
        lbl_status.Text = 'Status: Bottom+Left anchor - Moves down on resize'
    btn_bl.Click = on_bl_click
    
    # Bottom-Right button
    btn_br = Button(main_panel, {
        'Text': 'Bottom+Right\n↘ Corner',
        'Left': 580,
        'Top': 350,
        'Width': 110,
        'Height': 60,
        'BackColor': '#CD5C5C',
        'ForeColor': '#FFFFFF'
    })
    btn_br.Anchor = AnchorStyles.Bottom | AnchorStyles.Right
    
    def on_br_click(sender, event):
        lbl_status.Text = 'Status: Bottom+Right anchor - Moves to corner'
    btn_br.Click = on_br_click
    
    # Stretch button (Bottom+Left+Right)
    btn_stretch = Button(main_panel, {
        'Text': 'Bottom+Left+Right → STRETCHES HORIZONTALLY ←',
        'Left': 20,
        'Top': 420,
        'Width': 670,
        'Height': 40,
        'BackColor': '#FFA500',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 10, FontStyle.Bold)
    })
    btn_stretch.Anchor = AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right
    
    def on_stretch_click(sender, event):
        lbl_status.Text = 'Status: Bottom+Left+Right anchor - Stretches horizontally!'
    btn_stretch.Click = on_stretch_click

    # =========================================================================
    # Run the application
    # =========================================================================
    Application.Run(form)


if __name__ == '__main__':
    main()
