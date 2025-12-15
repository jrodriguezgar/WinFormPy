"""
Dock and Anchor Demonstration for WinFormPy.

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

import sys
import os
sys.path.append(os.getcwd())

from winformpy.winformpy import Form, Button, Panel, Label, Application

def main():
    """Main entry point for the Dock and Anchor demonstration."""
    form = Form()
    form.Text = "Dock and Anchor Demo - WinFormPy"
    form.Size = (1000, 700)
    
    print("Creating panels...")

    # ================================================================
    # TOP PANEL - Created first to claim top edge
    # ================================================================
    top_panel = Panel(form)
    top_panel.BackColor = "lightblue"
    top_panel.Dock = "Top"
    top_panel.Height = 120
    print(f"Top panel created: {top_panel}, Dock={top_panel.Dock}")
    
    # Add label to top panel
    lbl_top = Label(top_panel)
    lbl_top.Text = "[PANEL] TOP PANEL - Docked to Top"
    lbl_top.Location = (10, 10)
    lbl_top.AutoSize = True
    lbl_top.Font = ('Arial', 12, 'bold')

    # Add buttons to top panel
    btn1 = Button(top_panel)
    btn1.Text = "[Button] 1"
    btn1.Location = (10, 50)
    btn1.Size = (100, 30)
    
    btn2 = Button(top_panel)
    btn2.Text = "[Button] 2"
    btn2.Location = (120, 50)
    btn2.Size = (100, 30)

    # ================================================================
    # BOTTOM PANEL - Created second with HIGH VISIBILITY
    # ================================================================
    bottom_panel = Panel(form)
    bottom_panel.BackColor = "red"  # BRIGHT RED for maximum visibility
    bottom_panel.Dock = "Bottom"
    bottom_panel.Height = 120  # Increased height
    bottom_panel.BorderStyle = "raised"
    bottom_panel.BringToFront()  # FORCE to front of z-order
    print(f"Bottom panel created: {bottom_panel}, Dock={bottom_panel.Dock}, Height={bottom_panel.Height}")
    
    # Status label with large font
    lbl_status = Label(bottom_panel)
    lbl_status.Text = "[Label] ⬇️ BOTTOM PANEL - THIS SHOULD BE VISIBLE ⬇️"
    lbl_status.Location = (10, 10)
    lbl_status.AutoSize = True
    lbl_status.ForeColor = "yellow"
    lbl_status.Font = ('Arial', 12, 'bold')
    
    # Add multiple buttons to bottom panel for visibility
    btn_bottom1 = Button(bottom_panel)
    btn_bottom1.Text = "[Button] Test 1"
    btn_bottom1.Location = (10, 60)
    btn_bottom1.Size = (120, 40)
    btn_bottom1.BackColor = "lime"
    
    btn_bottom2 = Button(bottom_panel)
    btn_bottom2.Text = "[Button] Test 2"
    btn_bottom2.Location = (140, 60)
    btn_bottom2.Size = (120, 40)
    btn_bottom2.BackColor = "cyan"
    
    btn_bottom3 = Button(bottom_panel)
    btn_bottom3.Text = "[Button] Test 3"
    btn_bottom3.Location = (270, 60)
    btn_bottom3.Size = (120, 40)
    btn_bottom3.BackColor = "yellow"

    # ================================================================
    # LEFT PANEL - Created third
    # ================================================================
    left_panel = Panel(form)
    left_panel.BackColor = "lightsteelblue"
    left_panel.Dock = "Left"
    left_panel.Width = 150
    print(f"Left panel created: {left_panel}, Dock={left_panel.Dock}")
    
    # Add label to left panel
    lbl_left = Label(left_panel)
    lbl_left.Text = "[PANEL]\nLEFT\nPANEL"
    lbl_left.Location = (35, 50)
    lbl_left.AutoSize = True
    lbl_left.Font = ('Arial', 10, 'bold')

    # ================================================================
    # MAIN PANEL - Created last, fills remaining space
    # ================================================================
    main_panel = Panel(form)
    main_panel.BackColor = "whitesmoke"
    main_panel.Dock = "Fill"
    print(f"Main panel created: {main_panel}, Dock={main_panel.Dock}")
    
    # Title
    lbl_title = Label(main_panel)
    lbl_title.Text = "[PANEL] ⚓ ANCHORING DEMONSTRATION - Resize the window!"
    lbl_title.Location = (20, 15)
    lbl_title.AutoSize = True
    lbl_title.Font = ('Arial', 12, 'bold')
    
    # Info label
    lbl_info = Label(main_panel)
    lbl_info.Text = "[Label] Anchor controls maintain FIXED DISTANCE from edges"
    lbl_info.Location = (20, 45)
    lbl_info.AutoSize = True
    lbl_info.Font = ('Arial', 9)
    
    # Top-Left button (default anchor)
    btn_tl = Button(main_panel)
    btn_tl.Text = "[Button]\nTop+Left\n(Default)"
    btn_tl.Location = (20, 80)
    btn_tl.Size = (110, 60)
    btn_tl.Anchor = ["Top", "Left"]
    btn_tl.BackColor = "dodgerblue"
    btn_tl.ForeColor = "white"
    
    def on_tl_click(sender, event):
        lbl_status.Text = "Status: Top+Left anchor - Fixed position"
    btn_tl.Click = on_tl_click
    
    # Top-Right button
    btn_tr = Button(main_panel)
    btn_tr.Text = "[Button]\nTop+Right\n→ Moves"
    btn_tr.Location = (580, 80)
    btn_tr.Size = (110, 60)
    btn_tr.Anchor = ["Top", "Right"]
    btn_tr.BackColor = "seagreen"
    btn_tr.ForeColor = "white"
    
    def on_tr_click(sender, event):
        lbl_status.Text = "Status: Top+Right anchor - Moves right on resize"
    btn_tr.Click = on_tr_click
    
    # Center label demonstrating vertical stretch
    lbl_stretch_v = Label(main_panel)
    lbl_stretch_v.Text = "[Label]\nTop+Bottom+Left\nStretches\nVertically"
    lbl_stretch_v.Location = (200, 80)
    lbl_stretch_v.Size = (200, 150)
    lbl_stretch_v.Anchor = ["Top", "Bottom", "Left"]
    lbl_stretch_v.BackColor = "lightyellow"
    lbl_stretch_v.BorderStyle = "fixed"
    lbl_stretch_v.TextAlign = "center"
    lbl_stretch_v.Font = ('Arial', 14, 'bold')
    
    # Bottom-Left button
    btn_bl = Button(main_panel)
    btn_bl.Text = "[Button]\nBottom+Left\n↓ Moves"
    btn_bl.Location = (20, 350)
    btn_bl.Size = (110, 60)
    btn_bl.Anchor = ["Bottom", "Left"]
    btn_bl.BackColor = "mediumpurple"
    btn_bl.ForeColor = "white"
    
    def on_bl_click(sender, event):
        lbl_status.Text = "Status: Bottom+Left anchor - Moves down on resize"
    btn_bl.Click = on_bl_click
    
    # Bottom-Right button
    btn_br = Button(main_panel)
    btn_br.Text = "[Button]\nBottom+Right\n↘ Corner"
    btn_br.Location = (580, 350)
    btn_br.Size = (110, 60)
    btn_br.Anchor = ["Bottom", "Right"]
    btn_br.BackColor = "indianred"
    btn_br.ForeColor = "white"
    
    def on_br_click(sender, event):
        lbl_status.Text = "Status: Bottom+Right anchor - Moves to corner"
    btn_br.Click = on_br_click
    
    # Stretch button (Bottom+Left+Right)
    btn_stretch = Button(main_panel)
    btn_stretch.Text = "[Button] Bottom+Left+Right → STRETCHES HORIZONTALLY ←"
    btn_stretch.Location = (20, 420)
    btn_stretch.Size = (670, 40)
    btn_stretch.Anchor = ["Bottom", "Left", "Right"]
    btn_stretch.BackColor = "orange"
    btn_stretch.ForeColor = "white"
    btn_stretch.Font = ('Arial', 10, 'bold')
    
    def on_stretch_click(sender, event):
        lbl_status.Text = "Status: Bottom+Left+Right anchor - Stretches horizontally!"
    btn_stretch.Click = on_stretch_click
    
    print("All controls created. Starting application...")
    print(f"Form size: {form.Size}")
    
    # ================================================================
    # RUN THE APPLICATION
    # ================================================================
    Application.Run(form)


if __name__ == "__main__":
    # Entry point: Execute the demonstration
    main()
