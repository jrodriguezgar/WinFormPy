"""
Refactored Anchor and Dock Example for WinFormPy.

Demonstrates the new API pattern with direct property assignment.

ANCHOR - Maintains fixed distances to window edges during resize
DOCK - Attaches controls to complete edges (Top, Bottom, Left, Right, Fill)

Run this script and resize windows to see the behaviors.
"""

import os
import sys
import importlib.util

# Load winform-py.py from parent directory
parent_dir = os.path.dirname(os.path.dirname(__file__))
module_path = os.path.join(parent_dir, "winform-py.py")

spec = importlib.util.spec_from_file_location("winform_py", module_path)
winform_py = importlib.util.module_from_spec(spec)
spec.loader.exec_module(winform_py)

# Import required classes
Form = winform_py.Form
Button = winform_py.Button
Label = winform_py.Label
Panel = winform_py.Panel
MessageBox = winform_py.MessageBox


def anchor_example():
    """
    Demonstrates ALL ANCHOR combinations - controls maintain fixed distances to specified edges.
    Shows 9 different anchor combinations in a grid layout.
    Resize the window to see how each control behaves differently.
    """
    # Create form
    form = Form()
    form.Text = "ANCHOR - All Combinations (Resize to see effects)"
    form.Width = 700
    form.Height = 600
    form.BackColor = '#F5F5F5'
    
    # Title - stretches horizontally (Top, Left, Right)
    title = Label(form)
    title.Text = 'ANCHOR - All Combinations'
    title.Left = 10
    title.Top = 10
    title.Width = 680
    title.Height = 40
    title.BackColor = '#0078D7'
    title.ForeColor = 'white'
    title.Font = ('Segoe UI', 12, 'bold')
    title.TextAlign = 'center'
    title.Anchor = ['Top', 'Left', 'Right']
    
    # === ROW 1: TOP ANCHORS ===
    
    # Top, Left (fixed position)
    btn1 = Button(form)
    btn1.Text = 'Top, Left\n(Fixed)'
    btn1.Left = 10
    btn1.Top = 70
    btn1.Width = 140
    btn1.Height = 60
    btn1.BackColor = '#E3F2FD'
    btn1.Anchor = ['Top', 'Left']
    
    # Top (centered horizontally, moves to maintain center)
    btn2 = Button(form)
    btn2.Text = 'Top\n(Centered)'
    btn2.Left = 280
    btn2.Top = 70
    btn2.Width = 140
    btn2.Height = 60
    btn2.BackColor = '#E1F5FE'
    btn2.Anchor = ['Top']
    
    # Top, Right (moves with right edge)
    btn3 = Button(form)
    btn3.Text = 'Top, Right\n(Moves right)'
    btn3.Left = 550
    btn3.Top = 70
    btn3.Width = 140
    btn3.Height = 60
    btn3.BackColor = '#B3E5FC'
    btn3.Anchor = ['Top', 'Right']
    
    # === ROW 2: MIDDLE ANCHORS ===
    
    # Left (vertically centered, moves to maintain center)
    btn4 = Button(form)
    btn4.Text = 'Left\n(V-Centered)'
    btn4.Left = 10
    btn4.Top = 270
    btn4.Width = 140
    btn4.Height = 60
    btn4.BackColor = '#C8E6C9'
    btn4.Anchor = ['Left']
    
    # No anchor (centered both ways)
    btn5 = Button(form)
    btn5.Text = 'None\n(Centered)'
    btn5.Left = 280
    btn5.Top = 270
    btn5.Width = 140
    btn5.Height = 60
    btn5.BackColor = '#F0F4C3'
    btn5.Anchor = []
    
    # Right (vertically centered, moves with right edge)
    btn6 = Button(form)
    btn6.Text = 'Right\n(V-Centered)'
    btn6.Left = 550
    btn6.Top = 270
    btn6.Width = 140
    btn6.Height = 60
    btn6.BackColor = '#FFF9C4'
    btn6.Anchor = ['Right']
    
    # === ROW 3: BOTTOM ANCHORS ===
    
    # Bottom, Left (moves down)
    btn7 = Button(form)
    btn7.Text = 'Bottom, Left\n(Moves down)'
    btn7.Left = 10
    btn7.Top = 490
    btn7.Width = 140
    btn7.Height = 60
    btn7.BackColor = '#FFCCBC'
    btn7.Anchor = ['Bottom', 'Left']
    
    # Bottom (moves down, centered)
    btn8 = Button(form)
    btn8.Text = 'Bottom\n(Down+Center)'
    btn8.Left = 280
    btn8.Top = 490
    btn8.Width = 140
    btn8.Height = 60
    btn8.BackColor = '#FFAB91'
    btn8.Anchor = ['Bottom']
    
    # Bottom, Right (corner)
    btn9 = Button(form)
    btn9.Text = 'Bottom, Right\n(Corner)'
    btn9.Left = 550
    btn9.Top = 490
    btn9.Width = 140
    btn9.Height = 60
    btn9.BackColor = '#FF8A65'
    btn9.Anchor = ['Bottom', 'Right']
    
    # === STRETCH EXAMPLES ===
    
    # Top, Left, Right (stretches horizontally)
    btn_stretch_h = Label(form)
    btn_stretch_h.Text = 'Top, Left, Right (Stretches Horizontally)'
    btn_stretch_h.Left = 10
    btn_stretch_h.Top = 150
    btn_stretch_h.Width = 680
    btn_stretch_h.Height = 35
    btn_stretch_h.BackColor = '#A5D6A7'
    btn_stretch_h.Font = ('Segoe UI', 9, 'bold')
    btn_stretch_h.TextAlign = 'center'
    btn_stretch_h.Anchor = ['Top', 'Left', 'Right']
    
    # Left, Bottom, Right (bottom + stretches horizontally)
    btn_stretch_h_bottom = Label(form)
    btn_stretch_h_bottom.Text = 'Bottom, Left, Right (Bottom + Stretches Horizontally)'
    btn_stretch_h_bottom.Left = 10
    btn_stretch_h_bottom.Top = 440
    btn_stretch_h_bottom.Width = 680
    btn_stretch_h_bottom.Height = 35
    btn_stretch_h_bottom.BackColor = '#FFAB91'
    btn_stretch_h_bottom.Font = ('Segoe UI', 9, 'bold')
    btn_stretch_h_bottom.TextAlign = 'center'
    btn_stretch_h_bottom.Anchor = ['Bottom', 'Left', 'Right']
    
    # Top, Bottom, Left (stretches vertically)
    btn_stretch_v_left = Label(form)
    btn_stretch_v_left.Text = 'Top\nBottom\nLeft\n\n(Stretches\nVertically)'
    btn_stretch_v_left.Left = 165
    btn_stretch_v_left.Top = 200
    btn_stretch_v_left.Width = 100
    btn_stretch_v_left.Height = 225
    btn_stretch_v_left.BackColor = '#CE93D8'
    btn_stretch_v_left.Font = ('Segoe UI', 8, 'bold')
    btn_stretch_v_left.TextAlign = 'center'
    btn_stretch_v_left.Anchor = ['Top', 'Bottom', 'Left']
    
    # Top, Bottom, Right (stretches vertically on right)
    btn_stretch_v_right = Label(form)
    btn_stretch_v_right.Text = 'Top\nBottom\nRight\n\n(Stretches\nVertically)'
    btn_stretch_v_right.Left = 435
    btn_stretch_v_right.Top = 200
    btn_stretch_v_right.Width = 100
    btn_stretch_v_right.Height = 225
    btn_stretch_v_right.BackColor = '#F48FB1'
    btn_stretch_v_right.Font = ('Segoe UI', 8, 'bold')
    btn_stretch_v_right.TextAlign = 'center'
    btn_stretch_v_right.Anchor = ['Top', 'Bottom', 'Right']
    
    # Top, Bottom, Left, Right (stretches in all directions)
    lbl_center = Label(form)
    lbl_center.Text = 'Top, Bottom, Left, Right\n\nStretches in ALL directions'
    lbl_center.Left = 280
    lbl_center.Top = 200
    lbl_center.Width = 140
    lbl_center.Height = 225
    lbl_center.BackColor = '#E1BEE7'
    lbl_center.Font = ('Segoe UI', 9, 'bold')
    lbl_center.TextAlign = 'center'
    lbl_center.Anchor = ['Top', 'Bottom', 'Left', 'Right']
    
    form.Show()
    MessageBox.Show("Resize Window to See Demo", "WinFormPy Demo", icon='Information')


def dock_example():
    """
    Demonstrates ALL DOCK positions - controls attach to complete edges.
    Order matters: Top/Bottom dock first, then Left/Right, then Fill takes remaining space.
    Resize to see how docked controls maintain their edge attachment.
    """
    # Create form
    form = Form()
    form.Text = "DOCK - All Positions (Resize to see effects)"
    form.Width = 700
    form.Height = 500
    
    # Top panel #1 - docked to top edge (full width)
    lbl_top1 = Label(form)
    lbl_top1.Text = 'DOCK: TOP #1 - Title Bar'
    lbl_top1.BackColor = '#1976D2'
    lbl_top1.ForeColor = 'white'
    lbl_top1.Font = ('Segoe UI', 11, 'bold')
    lbl_top1.TextAlign = 'center'
    lbl_top1.Height = 45
    lbl_top1.Dock = 'Top'
    
    # Top panel #2 - second top panel (stacks below first)
    lbl_top2 = Label(form)
    lbl_top2.Text = 'DOCK: TOP #2 - Menu Bar (stacks below previous Top)'
    lbl_top2.BackColor = '#2196F3'
    lbl_top2.ForeColor = 'white'
    lbl_top2.Font = ('Segoe UI', 9)
    lbl_top2.TextAlign = 'center'
    lbl_top2.Height = 35
    lbl_top2.Dock = 'Top'
    
    # Bottom panel #1 - docked to bottom edge (full width)
    lbl_bottom1 = Label(form)
    lbl_bottom1.Text = 'DOCK: BOTTOM #1 - Status Bar'
    lbl_bottom1.BackColor = '#F57C00'
    lbl_bottom1.ForeColor = 'white'
    lbl_bottom1.Font = ('Segoe UI', 9)
    lbl_bottom1.TextAlign = 'center'
    lbl_bottom1.Height = 30
    lbl_bottom1.Dock = 'Bottom'
    
    # Bottom panel #2 - second bottom panel (stacks above first)
    lbl_bottom2 = Label(form)
    lbl_bottom2.Text = 'DOCK: BOTTOM #2 - Footer (stacks above previous Bottom)'
    lbl_bottom2.BackColor = '#FF9800'
    lbl_bottom2.ForeColor = 'white'
    lbl_bottom2.Font = ('Segoe UI', 9)
    lbl_bottom2.TextAlign = 'center'
    lbl_bottom2.Height = 30
    lbl_bottom2.Dock = 'Bottom'
    
    # Left panel #1 - docked to left edge (remaining height between top/bottom)
    lbl_left1 = Label(form)
    lbl_left1.Text = 'DOCK:\nLEFT #1\n\nMain\nSidebar'
    lbl_left1.BackColor = '#388E3C'
    lbl_left1.ForeColor = 'white'
    lbl_left1.Font = ('Segoe UI', 10, 'bold')
    lbl_left1.TextAlign = 'center'
    lbl_left1.Width = 100
    lbl_left1.Dock = 'Left'
    
    # Left panel #2 - second left panel (stacks to the right of first)
    lbl_left2 = Label(form)
    lbl_left2.Text = 'DOCK:\nLEFT #2\n\nSecond\nPanel'
    lbl_left2.BackColor = '#4CAF50'
    lbl_left2.ForeColor = 'white'
    lbl_left2.Font = ('Segoe UI', 9)
    lbl_left2.TextAlign = 'center'
    lbl_left2.Width = 80
    lbl_left2.Dock = 'Left'
    
    # Right panel #1 - docked to right edge (remaining height)
    lbl_right1 = Label(form)
    lbl_right1.Text = 'DOCK:\nRIGHT #1\n\nMain\nRight\nPanel'
    lbl_right1.BackColor = '#7B1FA2'
    lbl_right1.ForeColor = 'white'
    lbl_right1.Font = ('Segoe UI', 10, 'bold')
    lbl_right1.TextAlign = 'center'
    lbl_right1.Width = 100
    lbl_right1.Dock = 'Right'
    
    # Right panel #2 - second right panel (stacks to the left of first)
    lbl_right2 = Label(form)
    lbl_right2.Text = 'DOCK:\nRIGHT #2\n\nTools'
    lbl_right2.BackColor = '#9C27B0'
    lbl_right2.ForeColor = 'white'
    lbl_right2.Font = ('Segoe UI', 9)
    lbl_right2.TextAlign = 'center'
    lbl_right2.Width = 80
    lbl_right2.Dock = 'Right'
    
    # Center area - fills all remaining space
    lbl_center = Label(form)
    lbl_center.Text = 'DOCK: FILL\n\nTakes all remaining space\n\nThis is the content area'
    lbl_center.BackColor = '#E0E0E0'
    lbl_center.Font = ('Segoe UI', 12, 'bold')
    lbl_center.TextAlign = 'center'
    lbl_center.Dock = 'Fill'
    
    form.Show()


def combined_example():
    """
    Demonstrates ANCHOR and DOCK working together.
    Dock creates layout structure, Anchor controls behavior within panels.
    """
    # Create form
    form = Form()
    form.Text = "ANCHOR + DOCK Combined (Resize to see interaction)"
    form.Width = 800
    form.Height = 600
    form.BackColor = '#F5F5F5'
    
    # === DOCKED PANELS ===
    
    # Top toolbar (Dock: Top)
    panel_top = Label(form)
    panel_top.Text = ''
    panel_top.BackColor = '#0078D7'
    panel_top.Height = 60
    panel_top.Dock = 'Top'
    
    # Buttons in top panel with ANCHOR
    btn_top1 = Button(panel_top)
    btn_top1.Text = 'File'
    btn_top1.Left = 10
    btn_top1.Top = 10
    btn_top1.Width = 80
    btn_top1.Height = 40
    btn_top1.BackColor = '#1976D2'
    btn_top1.ForeColor = 'white'
    btn_top1.Anchor = ['Top', 'Left']
    
    btn_top2 = Button(panel_top)
    btn_top2.Text = 'Edit'
    btn_top2.Left = 100
    btn_top2.Top = 10
    btn_top2.Width = 80
    btn_top2.Height = 40
    btn_top2.BackColor = '#1976D2'
    btn_top2.ForeColor = 'white'
    btn_top2.Anchor = ['Top', 'Left']
    
    btn_top3 = Button(panel_top)
    btn_top3.Text = 'Settings'
    btn_top3.Left = 710
    btn_top3.Top = 10
    btn_top3.Width = 80
    btn_top3.Height = 40
    btn_top3.BackColor = '#1976D2'
    btn_top3.ForeColor = 'white'
    btn_top3.Anchor = ['Top', 'Right']  # Anchored to right
    
    # Bottom status bar (Dock: Bottom)
    panel_bottom = Label(form)
    panel_bottom.Text = ''
    panel_bottom.BackColor = '#FF9800'
    panel_bottom.Height = 40
    panel_bottom.Dock = 'Bottom'
    
    # Labels in bottom panel with ANCHOR
    lbl_status1 = Label(panel_bottom)
    lbl_status1.Text = 'Ready'
    lbl_status1.Left = 10
    lbl_status1.Top = 10
    lbl_status1.Width = 200
    lbl_status1.Height = 20
    lbl_status1.BackColor = '#FF9800'
    lbl_status1.ForeColor = 'white'
    lbl_status1.Font = ('Segoe UI', 9, 'bold')
    lbl_status1.Anchor = ['Top', 'Left']
    
    lbl_status2 = Label(panel_bottom)
    lbl_status2.Text = 'Line 1, Col 1'
    lbl_status2.Left = 590
    lbl_status2.Top = 10
    lbl_status2.Width = 200
    lbl_status2.Height = 20
    lbl_status2.BackColor = '#FF9800'
    lbl_status2.ForeColor = 'white'
    lbl_status2.Font = ('Segoe UI', 9)
    lbl_status2.TextAlign = 'right'
    lbl_status2.Anchor = ['Top', 'Right']  # Anchored to right
    
    # Left sidebar (Dock: Left)
    panel_left = Label(form)
    panel_left.Text = ''
    panel_left.BackColor = '#4CAF50'
    panel_left.Width = 150
    panel_left.Dock = 'Left'
    
    # Buttons in left panel with ANCHOR
    for i in range(5):
        btn = Button(panel_left)
        btn.Text = f'Item {i+1}'
        btn.Left = 10
        btn.Top = 10 + (i * 60)
        btn.Width = 130
        btn.Height = 50
        btn.BackColor = '#66BB6A'
        btn.Anchor = ['Top', 'Left', 'Right']  # Stretches horizontally
    
    # Right sidebar (Dock: Right)
    panel_right = Label(form)
    panel_right.Text = ''
    panel_right.BackColor = '#9C27B0'
    panel_right.Width = 150
    panel_right.Dock = 'Right'
    
    # Buttons in right panel with ANCHOR
    btn_right_top = Button(panel_right)
    btn_right_top.Text = 'Top Tool'
    btn_right_top.Left = 10
    btn_right_top.Top = 10
    btn_right_top.Width = 130
    btn_right_top.Height = 50
    btn_right_top.BackColor = '#BA68C8'
    btn_right_top.Anchor = ['Top', 'Left', 'Right']
    
    btn_right_bottom = Button(panel_right)
    btn_right_bottom.Text = 'Bottom Tool'
    btn_right_bottom.Left = 10
    btn_right_bottom.Top = 450
    btn_right_bottom.Width = 130
    btn_right_bottom.Height = 50
    btn_right_bottom.BackColor = '#BA68C8'
    btn_right_bottom.Anchor = ['Bottom', 'Left', 'Right']  # Anchored to bottom
    
    # Center content area (Dock: Fill)
    panel_center = Label(form)
    panel_center.Text = ''
    panel_center.BackColor = 'white'
    panel_center.Dock = 'Fill'
    
    # Controls in center with ANCHOR showing different behaviors
    lbl_title = Label(panel_center)
    lbl_title.Text = 'ANCHOR controls inside DOCKED panels'
    lbl_title.Left = 10
    lbl_title.Top = 10
    lbl_title.Width = 480
    lbl_title.Height = 30
    lbl_title.BackColor = '#E3F2FD'
    lbl_title.Font = ('Segoe UI', 11, 'bold')
    lbl_title.TextAlign = 'center'
    lbl_title.Anchor = ['Top', 'Left', 'Right']  # Stretches with panel
    
    btn_center1 = Button(panel_center)
    btn_center1.Text = 'Fixed Button\n(Top, Left)'
    btn_center1.Left = 10
    btn_center1.Top = 60
    btn_center1.Width = 150
    btn_center1.Height = 60
    btn_center1.BackColor = '#FFECB3'
    btn_center1.Anchor = ['Top', 'Left']
    
    btn_center2 = Button(panel_center)
    btn_center2.Text = 'Moves Right\n(Top, Right)'
    btn_center2.Left = 340
    btn_center2.Top = 60
    btn_center2.Width = 150
    btn_center2.Height = 60
    btn_center2.BackColor = '#FFF9C4'
    btn_center2.Anchor = ['Top', 'Right']
    
    lbl_stretch = Label(panel_center)
    lbl_stretch.Text = 'Stretches Horizontally (Top, Left, Right)'
    lbl_stretch.Left = 10
    lbl_stretch.Top = 140
    lbl_stretch.Width = 480
    lbl_stretch.Height = 40
    lbl_stretch.BackColor = '#C8E6C9'
    lbl_stretch.Font = ('Segoe UI', 9, 'bold')
    lbl_stretch.TextAlign = 'center'
    lbl_stretch.Anchor = ['Top', 'Left', 'Right']
    
    lbl_center_all = Label(panel_center)
    lbl_center_all.Text = 'Stretches in ALL directions\n(Top, Bottom, Left, Right)'
    lbl_center_all.Left = 10
    lbl_center_all.Top = 200
    lbl_center_all.Width = 480
    lbl_center_all.Height = 210
    lbl_center_all.BackColor = '#E1BEE7'
    lbl_center_all.Font = ('Segoe UI', 10, 'bold')
    lbl_center_all.TextAlign = 'center'
    lbl_center_all.Anchor = ['Top', 'Bottom', 'Left', 'Right']
    
    btn_bottom_left = Button(panel_center)
    btn_bottom_left.Text = 'Bottom Left\n(Bottom, Left)'
    btn_bottom_left.Left = 10
    btn_bottom_left.Top = 430
    btn_bottom_left.Width = 150
    btn_bottom_left.Height = 60
    btn_bottom_left.BackColor = '#FFCCBC'
    btn_bottom_left.Anchor = ['Bottom', 'Left']
    
    btn_bottom_right = Button(panel_center)
    btn_bottom_right.Text = 'Bottom Right\n(Bottom, Right)'
    btn_bottom_right.Left = 340
    btn_bottom_right.Top = 430
    btn_bottom_right.Width = 150
    btn_bottom_right.Height = 60
    btn_bottom_right.BackColor = '#FFAB91'
    btn_bottom_right.Anchor = ['Bottom', 'Right']
    
    form.Show()


def all_examples():
    """Muestra ejemplos ANCHOR, DOCK y combinados en una sola ventana."""

    form = Form()
    form.Text = "All Examples - Anchor, Dock, Combined"
    form.Width = 1280
    form.Height = 960
    form.BackColor = '#F5F5F5'

    form.Load = lambda: form._root.after(
        200,
        lambda: MessageBox.Show("Resize Window to See Demo", "WinFormPy Demo", icon='Information', modal=True)
    )

    instructions = Label(form)
    instructions.AutoSize = False
    instructions.Text = (
        '1. Resize the main window to observe how controls react.\n'
        '2. Look at each colored section: ANCHOR (left), DOCK (right) and the combined view below.\n'
        '3. Interact with the buttons to confirm they remain in their anchored position.'
    )
    instructions.Left = 10
    instructions.Top = 10
    instructions.Width = 1260
    instructions.Height = 70
    instructions.BackColor = '#D1C4E9'
    instructions.ForeColor = '#311B92'
    instructions.Font = ('Segoe UI', 10, 'bold')
    instructions.TextAlign = 'center'
    instructions.Anchor = ['Top', 'Left', 'Right']
    form.AddControl(instructions)

    # === ANCHOR SECTION ===
    anchor_section = Panel(form)
    anchor_section.Left = 10
    anchor_section.Top = 90
    anchor_section.Width = 620
    anchor_section.Height = 400
    anchor_section.BackColor = '#FFE5E9'
    anchor_section.BorderStyle = 'ridge'
    anchor_section.Anchor = ['Top', 'Left']
    form.AddControl(anchor_section)

    anchor_header = Label(form)
    anchor_header.AutoSize = False
    anchor_header.Text = 'ANCHOR BEHAVIORS'
    anchor_header.Left = 10
    anchor_header.Top = 10
    anchor_header.Width = 600
    anchor_header.Height = 36
    anchor_header.BackColor = '#C62828'
    anchor_header.ForeColor = 'white'
    anchor_header.Font = ('Segoe UI', 11, 'bold')
    anchor_header.TextAlign = 'center'
    anchor_section.AddControl(anchor_header)

    anchor_info = Label(form)
    anchor_info.AutoSize = False
    anchor_info.Text = 'Each button maintains its configured distances when you resize the window.'
    anchor_info.Left = 10
    anchor_info.Top = 56
    anchor_info.Width = 600
    anchor_info.Height = 32
    anchor_info.BackColor = '#FFCDD2'
    anchor_info.TextAlign = 'center'
    anchor_section.AddControl(anchor_info)

    anchor_top_left = Button(form)
    anchor_top_left.Text = 'Top + Left'
    anchor_top_left.Left = 20
    anchor_top_left.Top = 110
    anchor_top_left.Width = 180
    anchor_top_left.Height = 80
    anchor_top_left.BackColor = '#EF9A9A'
    anchor_top_left.Anchor = ['Top', 'Left']
    anchor_section.AddControl(anchor_top_left)

    anchor_top = Button(form)
    anchor_top.Text = 'Top (centrado)'
    anchor_top.Left = 220
    anchor_top.Top = 110
    anchor_top.Width = 180
    anchor_top.Height = 80
    anchor_top.BackColor = '#F48FB1'
    anchor_top.Anchor = ['Top']
    anchor_section.AddControl(anchor_top)

    anchor_top_right = Button(form)
    anchor_top_right.Text = 'Top + Right'
    anchor_top_right.Left = 420
    anchor_top_right.Top = 110
    anchor_top_right.Width = 180
    anchor_top_right.Height = 80
    anchor_top_right.BackColor = '#F06292'
    anchor_top_right.Anchor = ['Top', 'Right']
    anchor_section.AddControl(anchor_top_right)

    anchor_center_label = Label(form)
    anchor_center_label.AutoSize = False
    anchor_center_label.Text = 'Anchor = [] (se mantiene centrado)'
    anchor_center_label.Left = 180
    anchor_center_label.Top = 210
    anchor_center_label.Width = 260
    anchor_center_label.Height = 60
    anchor_center_label.BackColor = '#F8BBD0'
    anchor_center_label.TextAlign = 'center'
    anchor_center_label.Anchor = []
    anchor_section.AddControl(anchor_center_label)

    anchor_fill = Label(form)
    anchor_fill.AutoSize = False
    anchor_fill.Text = 'Top + Bottom + Left + Right (se estira)'
    anchor_fill.Left = 20
    anchor_fill.Top = 250
    anchor_fill.Width = 580
    anchor_fill.Height = 60
    anchor_fill.BackColor = '#FCE4EC'
    anchor_fill.TextAlign = 'center'
    anchor_fill.Font = ('Segoe UI', 10, 'bold')
    anchor_fill.Anchor = ['Top', 'Bottom', 'Left', 'Right']
    anchor_section.AddControl(anchor_fill)

    anchor_bottom_left = Button(form)
    anchor_bottom_left.Text = 'Bottom + Left'
    anchor_bottom_left.Left = 20
    anchor_bottom_left.Top = 330
    anchor_bottom_left.Width = 180
    anchor_bottom_left.Height = 60
    anchor_bottom_left.BackColor = '#EF9A9A'
    anchor_bottom_left.Anchor = ['Bottom', 'Left']
    anchor_section.AddControl(anchor_bottom_left)

    anchor_bottom_right = Button(form)
    anchor_bottom_right.Text = 'Bottom + Right'
    anchor_bottom_right.Left = 420
    anchor_bottom_right.Top = 330
    anchor_bottom_right.Width = 180
    anchor_bottom_right.Height = 60
    anchor_bottom_right.BackColor = '#F06292'
    anchor_bottom_right.Anchor = ['Bottom', 'Right']
    anchor_section.AddControl(anchor_bottom_right)

    # === DOCK SECTION ===
    dock_section = Panel(form)
    dock_section.Left = 650
    dock_section.Top = 90
    dock_section.Width = 620
    dock_section.Height = 400
    dock_section.BackColor = '#E5F3FF'
    dock_section.BorderStyle = 'ridge'
    dock_section.Anchor = ['Top', 'Right']
    form.AddControl(dock_section)

    dock_header = Label(form)
    dock_header.AutoSize = False
    dock_header.Text = 'DOCK POSITIONS'
    dock_header.Left = 10
    dock_header.Top = 10
    dock_header.Width = 600
    dock_header.Height = 36
    dock_header.BackColor = '#1565C0'
    dock_header.ForeColor = 'white'
    dock_header.Font = ('Segoe UI', 11, 'bold')
    dock_header.TextAlign = 'center'
    dock_section.AddControl(dock_header)

    dock_info = Label(form)
    dock_info.AutoSize = False
    dock_info.Text = 'Order matters: Top/Bottom first, then Left/Right and finally Fill.'
    dock_info.Left = 10
    dock_info.Top = 56
    dock_info.Width = 600
    dock_info.Height = 32
    dock_info.BackColor = '#BBDEFB'
    dock_info.TextAlign = 'center'
    dock_section.AddControl(dock_info)

    dock_top_main = Label(form)
    dock_top_main.AutoSize = False
    dock_top_main.Text = 'Dock: Top #1 (barra de título)'
    dock_top_main.Height = 44
    dock_top_main.BackColor = '#1E88E5'
    dock_top_main.ForeColor = 'white'
    dock_top_main.Font = ('Segoe UI', 10, 'bold')
    dock_top_main.TextAlign = 'center'
    dock_top_main.Dock = 'Top'
    dock_section.AddControl(dock_top_main)

    dock_top_secondary = Label(form)
    dock_top_secondary.AutoSize = False
    dock_top_secondary.Text = 'Dock: Top #2 (barra de menús)'
    dock_top_secondary.Height = 32
    dock_top_secondary.BackColor = '#42A5F5'
    dock_top_secondary.ForeColor = 'white'
    dock_top_secondary.TextAlign = 'center'
    dock_top_secondary.Dock = 'Top'
    dock_section.AddControl(dock_top_secondary)

    dock_bottom_status = Label(form)
    dock_bottom_status.AutoSize = False
    dock_bottom_status.Text = 'Dock: Bottom #1 (status bar)'
    dock_bottom_status.Height = 30
    dock_bottom_status.BackColor = '#FB8C00'
    dock_bottom_status.ForeColor = 'white'
    dock_bottom_status.TextAlign = 'center'
    dock_bottom_status.Dock = 'Bottom'
    dock_section.AddControl(dock_bottom_status)

    dock_bottom_footer = Label(form)
    dock_bottom_footer.AutoSize = False
    dock_bottom_footer.Text = 'Dock: Bottom #2 (footer)'
    dock_bottom_footer.Height = 30
    dock_bottom_footer.BackColor = '#FFB74D'
    dock_bottom_footer.ForeColor = 'white'
    dock_bottom_footer.TextAlign = 'center'
    dock_bottom_footer.Dock = 'Bottom'
    dock_section.AddControl(dock_bottom_footer)

    dock_left_main = Label(form)
    dock_left_main.AutoSize = False
    dock_left_main.Text = 'Dock: Left #1'
    dock_left_main.Width = 120
    dock_left_main.BackColor = '#43A047'
    dock_left_main.ForeColor = 'white'
    dock_left_main.Font = ('Segoe UI', 10, 'bold')
    dock_left_main.TextAlign = 'center'
    dock_left_main.Dock = 'Left'
    dock_section.AddControl(dock_left_main)

    dock_left_secondary = Label(form)
    dock_left_secondary.AutoSize = False
    dock_left_secondary.Text = 'Dock: Left #2'
    dock_left_secondary.Width = 100
    dock_left_secondary.BackColor = '#66BB6A'
    dock_left_secondary.ForeColor = 'white'
    dock_left_secondary.TextAlign = 'center'
    dock_left_secondary.Dock = 'Left'
    dock_section.AddControl(dock_left_secondary)

    dock_right_tools = Label(form)
    dock_right_tools.AutoSize = False
    dock_right_tools.Text = 'Dock: Right #1'
    dock_right_tools.Width = 120
    dock_right_tools.BackColor = '#8E24AA'
    dock_right_tools.ForeColor = 'white'
    dock_right_tools.Font = ('Segoe UI', 10, 'bold')
    dock_right_tools.TextAlign = 'center'
    dock_right_tools.Dock = 'Right'
    dock_section.AddControl(dock_right_tools)

    dock_right_secondary = Label(form)
    dock_right_secondary.AutoSize = False
    dock_right_secondary.Text = 'Dock: Right #2'
    dock_right_secondary.Width = 100
    dock_right_secondary.BackColor = '#AB47BC'
    dock_right_secondary.ForeColor = 'white'
    dock_right_secondary.TextAlign = 'center'
    dock_right_secondary.Dock = 'Right'
    dock_section.AddControl(dock_right_secondary)

    dock_fill = Label(form)
    dock_fill.AutoSize = False
    dock_fill.Text = 'Dock: Fill (zona de contenido)'
    dock_fill.BackColor = '#E0E0E0'
    dock_fill.Font = ('Segoe UI', 11, 'bold')
    dock_fill.TextAlign = 'center'
    dock_fill.Dock = 'Fill'
    dock_section.AddControl(dock_fill)

    # === COMBINED SECTION ===
    combined_section = Panel(form)
    combined_section.Left = 10
    combined_section.Top = 520
    combined_section.Width = 1260
    combined_section.Height = 400
    combined_section.BackColor = '#E8F5E9'
    combined_section.BorderStyle = 'ridge'
    combined_section.Anchor = ['Bottom', 'Left', 'Right']
    form.AddControl(combined_section)

    combined_header = Label(form)
    combined_header.AutoSize = False
    combined_header.Text = 'ANCHOR + DOCK (Diseño completo)'
    combined_header.Left = 10
    combined_header.Top = 10
    combined_header.Width = 1240
    combined_header.Height = 36
    combined_header.BackColor = '#2E7D32'
    combined_header.ForeColor = 'white'
    combined_header.Font = ('Segoe UI', 11, 'bold')
    combined_header.TextAlign = 'center'
    combined_section.AddControl(combined_header)

    combined_info = Label(form)
    combined_info.AutoSize = False
    combined_info.Text = 'Dock defines the structure; Anchor maintains controls within each panel.'
    combined_info.Left = 10
    combined_info.Top = 56
    combined_info.Width = 1240
    combined_info.Height = 32
    combined_info.BackColor = '#C8E6C9'
    combined_info.TextAlign = 'center'
    combined_section.AddControl(combined_info)

    toolbar_panel = Panel(form)
    toolbar_panel.Height = 60
    toolbar_panel.BackColor = '#388E3C'
    toolbar_panel.Dock = 'Top'
    combined_section.AddControl(toolbar_panel)

    toolbar_file = Button(form)
    toolbar_file.Text = 'File'
    toolbar_file.Left = 10
    toolbar_file.Top = 10
    toolbar_file.Width = 90
    toolbar_file.Height = 40
    toolbar_file.BackColor = '#66BB6A'
    toolbar_file.ForeColor = 'white'
    toolbar_file.Anchor = ['Top', 'Left']
    toolbar_panel.AddControl(toolbar_file)

    toolbar_edit = Button(form)
    toolbar_edit.Text = 'Edit'
    toolbar_edit.Left = 110
    toolbar_edit.Top = 10
    toolbar_edit.Width = 90
    toolbar_edit.Height = 40
    toolbar_edit.BackColor = '#66BB6A'
    toolbar_edit.ForeColor = 'white'
    toolbar_edit.Anchor = ['Top', 'Left']
    toolbar_panel.AddControl(toolbar_edit)

    toolbar_settings = Button(form)
    toolbar_settings.Text = 'Settings'
    toolbar_settings.Left = 1130
    toolbar_settings.Top = 10
    toolbar_settings.Width = 120
    toolbar_settings.Height = 40
    toolbar_settings.BackColor = '#2E7D32'
    toolbar_settings.ForeColor = 'white'
    toolbar_settings.Anchor = ['Top', 'Right']
    toolbar_panel.AddControl(toolbar_settings)

    status_panel = Panel(form)
    status_panel.Height = 40
    status_panel.BackColor = '#81C784'
    status_panel.Dock = 'Bottom'
    combined_section.AddControl(status_panel)

    status_ready = Label(form)
    status_ready.AutoSize = False
    status_ready.Text = 'Ready'
    status_ready.Left = 10
    status_ready.Top = 10
    status_ready.Width = 200
    status_ready.Height = 20
    status_ready.BackColor = '#81C784'
    status_ready.Font = ('Segoe UI', 9, 'bold')
    status_ready.TextAlign = 'left'
    status_ready.Anchor = ['Top', 'Left']
    status_panel.AddControl(status_ready)

    status_position = Label(form)
    status_position.AutoSize = False
    status_position.Text = 'Line 1, Col 1'
    status_position.Left = 1040
    status_position.Top = 10
    status_position.Width = 200
    status_position.Height = 20
    status_position.BackColor = '#81C784'
    status_position.TextAlign = 'right'
    status_position.Anchor = ['Top', 'Right']
    status_panel.AddControl(status_position)

    nav_panel = Panel(form)
    nav_panel.Width = 180
    nav_panel.BackColor = '#A5D6A7'
    nav_panel.Dock = 'Left'
    combined_section.AddControl(nav_panel)

    for idx, caption in enumerate(['Dashboard', 'Reports', 'Settings', 'Logs']):
        nav_btn = Button(form)
        nav_btn.Text = caption
        nav_btn.Left = 10
        nav_btn.Top = 10 + idx * 60
        nav_btn.Width = 160
        nav_btn.Height = 50
        nav_btn.BackColor = '#C5E1A5'
        nav_btn.Anchor = ['Top', 'Left', 'Right']
        nav_panel.AddControl(nav_btn)

    details_panel = Panel(form)
    details_panel.Width = 200
    details_panel.BackColor = '#C5E1A5'
    details_panel.Dock = 'Right'
    combined_section.AddControl(details_panel)

    details_label = Label(form)
    details_label.AutoSize = False
    details_label.Text = 'Tools / Help area'
    details_label.Left = 10
    details_label.Top = 10
    details_label.Width = 180
    details_label.Height = 50
    details_label.BackColor = '#AED581'
    details_label.TextAlign = 'center'
    details_label.Anchor = ['Top', 'Left', 'Right']
    details_panel.AddControl(details_label)

    details_bottom_button = Button(form)
    details_bottom_button.Text = 'Support'
    details_bottom_button.Left = 10
    details_bottom_button.Top = 300
    details_bottom_button.Width = 180
    details_bottom_button.Height = 50
    details_bottom_button.BackColor = '#8BC34A'
    details_bottom_button.Anchor = ['Bottom', 'Left', 'Right']
    details_panel.AddControl(details_bottom_button)

    content_panel = Panel(form)
    content_panel.BackColor = 'white'
    content_panel.Dock = 'Fill'
    combined_section.AddControl(content_panel)

    content_title = Label(form)
    content_title.AutoSize = False
    content_title.Text = 'Main Content'
    content_title.Left = 20
    content_title.Top = 20
    content_title.Width = 760
    content_title.Height = 32
    content_title.BackColor = '#E8F5E9'
    content_title.Font = ('Segoe UI', 11, 'bold')
    content_title.TextAlign = 'left'
    content_title.Anchor = ['Top', 'Left', 'Right']
    content_panel.AddControl(content_title)

    content_summary = Label(form)
    content_summary.AutoSize = False
    content_summary.Text = (
        'The central panel uses Anchor to keep titles at the top, cards that stretch and buttons in the corners.'
    )
    content_summary.Left = 20
    content_summary.Top = 60
    content_summary.Width = 760
    content_summary.Height = 48
    content_summary.BackColor = '#F1F8E9'
    content_summary.TextAlign = 'left'
    content_summary.Anchor = ['Top', 'Left', 'Right']
    content_panel.AddControl(content_summary)

    content_stretch = Label(form)
    content_stretch.AutoSize = False
    content_stretch.Text = 'Section that stretches with the window'
    content_stretch.Left = 20
    content_stretch.Top = 120
    content_stretch.Width = 760
    content_stretch.Height = 180
    content_stretch.BackColor = '#C8E6C9'
    content_stretch.TextAlign = 'center'
    content_stretch.Font = ('Segoe UI', 10, 'bold')
    content_stretch.Anchor = ['Top', 'Bottom', 'Left', 'Right']
    content_panel.AddControl(content_stretch)

    content_bottom_left = Button(form)
    content_bottom_left.Text = 'Cancel'
    content_bottom_left.Left = 20
    content_bottom_left.Top = 320
    content_bottom_left.Width = 140
    content_bottom_left.Height = 48
    content_bottom_left.BackColor = '#FFAB91'
    content_bottom_left.Anchor = ['Bottom', 'Left']
    content_panel.AddControl(content_bottom_left)

    content_bottom_right = Button(form)
    content_bottom_right.Text = 'Save Changes'
    content_bottom_right.Left = 600
    content_bottom_right.Top = 320
    content_bottom_right.Width = 140
    content_bottom_right.Height = 48
    content_bottom_right.BackColor = '#FF7043'
    content_bottom_right.Anchor = ['Bottom', 'Right']
    content_panel.AddControl(content_bottom_right)

    form.Show()


def main():
    """
    Main menu to launch anchor, dock, or combined examples.
    Uses the new API pattern with direct property assignment.
    """
    # Create main form
    form = Form()
    form.Text = "Anchor and Dock Examples - Complete Demo"
    form.Width = 500
    form.Height = 320
    form.BackColor = '#F5F5F5'
    
    # Title header
    title = Label(form)
    title.Text = 'ANCHOR & DOCK - Complete Examples'
    title.Left = 10
    title.Top = 10
    title.Width = 480
    title.Height = 40
    title.BackColor = '#0078D7'
    title.ForeColor = 'white'
    title.Font = ('Segoe UI', 13, 'bold')
    title.TextAlign = 'center'
    
    # Info label
    info = Label(form)
    info.Text = 'Select an example to see all possibilities:'
    info.Left = 10
    info.Top = 60
    info.Width = 480
    info.Height = 25
    info.Font = ('Segoe UI', 10, 'bold')
    info.TextAlign = 'center'
    
    # Anchor example button
    btn_anchor = Button(form)
    btn_anchor.Text = 'ANCHOR - All 13 Combinations\n(Fixed distances to edges)'
    btn_anchor.Left = 50
    btn_anchor.Top = 100
    btn_anchor.Width = 400
    btn_anchor.Height = 50
    btn_anchor.BackColor = '#E3F2FD'
    btn_anchor.Font = ('Segoe UI', 10)
    btn_anchor.Click = lambda: anchor_example()
    
    # Dock example button
    btn_dock = Button(form)
    btn_dock.Text = 'DOCK - All 5 Positions + Stacking\n(Attach to complete edges)'
    btn_dock.Left = 50
    btn_dock.Top = 160
    btn_dock.Width = 400
    btn_dock.Height = 50
    btn_dock.BackColor = '#FFF9C4'
    btn_dock.Font = ('Segoe UI', 10)
    btn_dock.Click = lambda: dock_example()
    
    # Combined example button
    btn_combined = Button(form)
    btn_combined.Text = 'COMBINED - Anchor + Dock Together\n(Real-world application layout)'
    btn_combined.Left = 50
    btn_combined.Top = 220
    btn_combined.Width = 400
    btn_combined.Height = 50
    btn_combined.BackColor = '#C8E6C9'
    btn_combined.Font = ('Segoe UI', 10)
    btn_combined.Click = lambda: combined_example()
    
    # Tip label
    tip = Label(form)
    tip.Text = '💡 Resize each window to see how controls behave differently'
    tip.Left = 10
    tip.Top = 280
    tip.Width = 480
    tip.Height = 25
    tip.Font = ('Segoe UI', 9, 'italic')
    tip.ForeColor = '#666666'
    tip.TextAlign = 'center'
    
    form.Show()


if __name__ == "__main__":
    all_examples()
