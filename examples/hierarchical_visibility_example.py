"""Hierarchical visibility example using WinFormPy's new API pattern."""

import os
import sys
import importlib.util

# Load winformpy.py from lib directory
parent_dir = os.path.dirname(os.path.dirname(__file__))
lib_dir = os.path.join(parent_dir, "lib")
module_path = os.path.join(lib_dir, "winformpy.py")

spec = importlib.util.spec_from_file_location("winform_py", module_path)
winform_py = importlib.util.module_from_spec(spec)
spec.loader.exec_module(winform_py)

# Import required classes
Form = winform_py.Form
Panel = winform_py.Panel
Button = winform_py.Button
Label = winform_py.Label
CheckBox = winform_py.CheckBox

def hierarchical_visibility_example():
    """Interactive demo illustrating parent/child visibility behaviour."""

    form = Form()
    form.Text = "WinFormPy - Simple Visibility Demo"
    form.Width = 900
    form.Height = 500
    form.StartPosition = "CenterScreen"

    # --- 1. The Container (Target) ---
    # This is the main container we will show/hide
    container = Panel(form)
    container.Left = 20
    container.Top = 20
    container.Width = 300
    container.Height = 400
    container.BorderStyle = 'fixed_single'
    container.BackColor = 'lightblue'
    form.AddControl(container)
    
    lbl_container = Label(container)
    lbl_container.Text = "I am the Container"
    lbl_container.Left = 10
    lbl_container.Top = 10
    lbl_container.AutoSize = True
    lbl_container.Font = ('Segoe UI', 10, 'bold')
    container.AddControl(lbl_container)
    
    # Child 1: A Button
    btn_child = Button(container)
    btn_child.Text = "I am a Child Button"
    btn_child.Left = 50
    btn_child.Top = 100
    btn_child.AutoSize = True
    container.AddControl(btn_child)
    
    # Child 2: A Label
    lbl_child = Label(container)
    lbl_child.Text = "I am a Child Label"
    lbl_child.Left = 50
    lbl_child.Top = 200
    lbl_child.BackColor = 'white'
    lbl_child.AutoSize = True
    container.AddControl(lbl_child)
    
    # --- 2. Controls (Right Side) ---
    
    # Control Panel Area
    ctrl_panel = Panel(form)
    ctrl_panel.Left = 350
    ctrl_panel.Top = 20
    ctrl_panel.Width = 500
    ctrl_panel.Height = 400
    form.AddControl(ctrl_panel)
    
    # Header
    lbl_ctrl = Label(ctrl_panel)
    lbl_ctrl.Text = "Control & Monitor"
    lbl_ctrl.Font = ('Segoe UI', 14, 'bold')
    lbl_ctrl.Left = 10
    lbl_ctrl.Top = 10
    lbl_ctrl.AutoSize = True
    ctrl_panel.AddControl(lbl_ctrl)
    
    # --- Actions Section ---
    lbl_actions = Label(ctrl_panel)
    lbl_actions.Text = "Actions (Set Internal Visibility):"
    lbl_actions.Left = 10
    lbl_actions.Top = 50
    lbl_actions.Font = ('Segoe UI', 10, 'bold')
    lbl_actions.AutoSize = True
    ctrl_panel.AddControl(lbl_actions)

    # Container Toggle
    chk_container = CheckBox(ctrl_panel)
    chk_container.Text = "Show Container (Parent)"
    chk_container.Checked = True
    chk_container.Left = 20
    chk_container.Top = 80
    chk_container.AutoSize = True
    ctrl_panel.AddControl(chk_container)
    
    # Child 1 Toggle
    chk_child1 = CheckBox(ctrl_panel)
    chk_child1.Text = "Show Child Button"
    chk_child1.Checked = True
    chk_child1.Left = 40
    chk_child1.Top = 110
    chk_child1.AutoSize = True
    ctrl_panel.AddControl(chk_child1)
    
    # Child 2 Toggle
    chk_child2 = CheckBox(ctrl_panel)
    chk_child2.Text = "Show Child Label"
    chk_child2.Checked = True
    chk_child2.Left = 40
    chk_child2.Top = 140
    chk_child2.AutoSize = True
    ctrl_panel.AddControl(chk_child2)
    
    # --- Monitor Section ---
    
    lbl_monitor = Label(ctrl_panel)
    lbl_monitor.Text = "Effective Visibility (Real-time Status):"
    lbl_monitor.Left = 10
    lbl_monitor.Top = 190
    lbl_monitor.Font = ('Segoe UI', 10, 'bold')
    lbl_monitor.AutoSize = True
    ctrl_panel.AddControl(lbl_monitor)
    
    # Status Labels
    lbl_status_container = Label(ctrl_panel)
    lbl_status_container.Left = 20
    lbl_status_container.Top = 220
    lbl_status_container.AutoSize = True
    lbl_status_container.Font = ('Consolas', 10)
    ctrl_panel.AddControl(lbl_status_container)
    
    lbl_status_child1 = Label(ctrl_panel)
    lbl_status_child1.Left = 20
    lbl_status_child1.Top = 250
    lbl_status_child1.AutoSize = True
    lbl_status_child1.Font = ('Consolas', 10)
    ctrl_panel.AddControl(lbl_status_child1)
    
    lbl_status_child2 = Label(ctrl_panel)
    lbl_status_child2.Left = 20
    lbl_status_child2.Top = 280
    lbl_status_child2.AutoSize = True
    lbl_status_child2.Font = ('Consolas', 10)
    ctrl_panel.AddControl(lbl_status_child2)
    
    # Explanation
    lbl_explanation = Label(ctrl_panel)
    lbl_explanation.Text = "NOTE: A child control is only visible if BOTH:\n1. Its internal visibility is True (Checkbox checked)\n2. Its Parent Container is Visible"
    lbl_explanation.Left = 10
    lbl_explanation.Top = 320
    lbl_explanation.Width = 480
    lbl_explanation.Height = 60
    lbl_explanation.BackColor = '#FFFFE0'
    lbl_explanation.BorderStyle = 'fixed_single'
    ctrl_panel.AddControl(lbl_explanation)

    # Logic
    def update_state():
        # Apply user intentions (Internal State)
        container.Visible = chk_container.Checked
        btn_child.Visible = chk_child1.Checked
        lbl_child.Visible = chk_child2.Checked
        
        # Helper to generate status text
        def get_status_text(name, control, internal_chk):
            effective = control.Visible
            internal = internal_chk.Checked
            
            status = "VISIBLE" if effective else "HIDDEN "
            reason = ""
            
            if not effective:
                if not internal:
                    reason = "(Self hidden)"
                elif not container.Visible and control != container:
                    reason = "(Parent hidden)"
            
            color = "#008800" if effective else "#CC0000"
            return f"{name:<15}: {status} {reason}", color

        # Update Monitor Labels
        txt, col = get_status_text("Container", container, chk_container)
        lbl_status_container.Text = txt
        lbl_status_container.ForeColor = col
        
        txt, col = get_status_text("Child Button", btn_child, chk_child1)
        lbl_status_child1.Text = txt
        lbl_status_child1.ForeColor = col
        
        txt, col = get_status_text("Child Label", lbl_child, chk_child2)
        lbl_status_child2.Text = txt
        lbl_status_child2.ForeColor = col

    # Bindings
    chk_container.CheckedChanged = update_state
    chk_child1.CheckedChanged = update_state
    chk_child2.CheckedChanged = update_state
    
    # Initial update
    update_state()
    
    form.Show()


if __name__ == "__main__":
    hierarchical_visibility_example()
