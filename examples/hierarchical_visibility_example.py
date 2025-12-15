"""Hierarchical visibility example using WinFormPy."""

import os
import sys

# Add parent directory to path to import winformpy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from winformpy import Form, Panel, Button, Label, CheckBox, Application, Color

class VisibilityDemoForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "WinFormPy - Hierarchical Visibility Demo"
        self.Width = 900
        self.Height = 500
        self.StartPosition = "CenterScreen"

        # --- 1. The Container (Target) ---
        # This is the main container we will show/hide
        self.container = Panel(self)
        self.container.Left = 20
        self.container.Top = 20
        self.container.Width = 300
        self.container.Height = 400
        self.container.BorderStyle = "fixed_single"
        self.container.BackColor = "lightblue"
        self.AddControl(self.container)
        
        self.lbl_container = Label(self.container)
        self.lbl_container.Text = "I am the Container"
        self.lbl_container.Left = 10
        self.lbl_container.Top = 10
        self.lbl_container.AutoSize = True
        self.lbl_container.Font = ("Segoe UI", 10, "bold")
        self.container.AddControl(self.lbl_container)
        
        # Child 1: A Button
        self.btn_child = Button(self.container)
        self.btn_child.Text = "I am a Child Button"
        self.btn_child.Left = 50
        self.btn_child.Top = 100
        self.btn_child.AutoSize = True
        self.container.AddControl(self.btn_child)
        
        # Child 2: A Label
        self.lbl_child = Label(self.container)
        self.lbl_child.Text = "I am a Child Label"
        self.lbl_child.Left = 50
        self.lbl_child.Top = 200
        self.lbl_child.BackColor = "white"
        self.lbl_child.AutoSize = True
        self.container.AddControl(self.lbl_child)
        
        # --- 2. Controls (Right Side) ---
        
        # Control Panel Area
        self.ctrl_panel = Panel(self)
        self.ctrl_panel.Left = 350
        self.ctrl_panel.Top = 20
        self.ctrl_panel.Width = 500
        self.ctrl_panel.Height = 400
        self.AddControl(self.ctrl_panel)
        
        # Header
        self.lbl_ctrl = Label(self.ctrl_panel)
        self.lbl_ctrl.Text = "Control & Monitor"
        self.lbl_ctrl.Font = ("Segoe UI", 14, "bold")
        self.lbl_ctrl.Left = 10
        self.lbl_ctrl.Top = 10
        self.lbl_ctrl.AutoSize = True
        self.ctrl_panel.AddControl(self.lbl_ctrl)
        
        # --- Actions Section ---
        self.lbl_actions = Label(self.ctrl_panel)
        self.lbl_actions.Text = "Actions (Set Internal Visibility):"
        self.lbl_actions.Left = 10
        self.lbl_actions.Top = 50
        self.lbl_actions.Font = ("Segoe UI", 10, "bold")
        self.lbl_actions.AutoSize = True
        self.ctrl_panel.AddControl(self.lbl_actions)

        # Container Toggle
        self.chk_container = CheckBox(self.ctrl_panel, {'Checked': True})
        self.chk_container.Text = "Show Container (Parent)"
        self.chk_container.Left = 20
        self.chk_container.Top = 80
        self.chk_container.AutoSize = True
        self.chk_container.CheckedChanged = self.update_state
        self.ctrl_panel.AddControl(self.chk_container)
        
        # Child 1 Toggle
        self.chk_child1 = CheckBox(self.ctrl_panel, {'Checked': True})
        self.chk_child1.Text = "Show Child Button"
        self.chk_child1.Left = 40
        self.chk_child1.Top = 110
        self.chk_child1.AutoSize = True
        self.chk_child1.CheckedChanged = self.update_state
        self.ctrl_panel.AddControl(self.chk_child1)
        
        # Child 2 Toggle
        self.chk_child2 = CheckBox(self.ctrl_panel, {'Checked': True})
        self.chk_child2.Text = "Show Child Label"
        self.chk_child2.Left = 40
        self.chk_child2.Top = 140
        self.chk_child2.AutoSize = True
        self.chk_child2.CheckedChanged = self.update_state
        self.ctrl_panel.AddControl(self.chk_child2)
        
        # --- Monitor Section ---
        
        self.lbl_monitor = Label(self.ctrl_panel)
        self.lbl_monitor.Text = "Effective Visibility (Real-time Status):"
        self.lbl_monitor.Left = 10
        self.lbl_monitor.Top = 190
        self.lbl_monitor.Font = ("Segoe UI", 10, "bold")
        self.lbl_monitor.AutoSize = True
        self.ctrl_panel.AddControl(self.lbl_monitor)
        
        # Status Labels
        self.lbl_status_container = Label(self.ctrl_panel)
        self.lbl_status_container.Left = 20
        self.lbl_status_container.Top = 220
        self.lbl_status_container.AutoSize = True
        self.lbl_status_container.Font = ("Consolas", 10)
        self.ctrl_panel.AddControl(self.lbl_status_container)
        
        self.lbl_status_child1 = Label(self.ctrl_panel)
        self.lbl_status_child1.Left = 20
        self.lbl_status_child1.Top = 250
        self.lbl_status_child1.AutoSize = True
        self.lbl_status_child1.Font = ("Consolas", 10)
        self.ctrl_panel.AddControl(self.lbl_status_child1)
        
        self.lbl_status_child2 = Label(self.ctrl_panel)
        self.lbl_status_child2.Left = 20
        self.lbl_status_child2.Top = 280
        self.lbl_status_child2.AutoSize = True
        self.lbl_status_child2.Font = ("Consolas", 10)
        self.ctrl_panel.AddControl(self.lbl_status_child2)
        
        # Explanation
        self.lbl_explanation = Label(self.ctrl_panel)
        self.lbl_explanation.Text = "NOTE: A child control is only visible if BOTH:\n1. Its internal visibility is True (Checkbox checked)\n2. Its Parent Container is Visible"
        self.lbl_explanation.Left = 10
        self.lbl_explanation.Top = 320
        self.lbl_explanation.Width = 480
        self.lbl_explanation.Height = 60
        self.lbl_explanation.BackColor = "#FFFFE0"
        self.lbl_explanation.BorderStyle = "fixed_single"
        self.ctrl_panel.AddControl(self.lbl_explanation)

        # Initial update
        self.update_state()

    def update_state(self, sender=None, e=None):
        # Apply user intentions (Internal State)
        self.container.Visible = self.chk_container.Checked
        self.btn_child.Visible = self.chk_child1.Checked
        self.lbl_child.Visible = self.chk_child2.Checked
        
        # Update Monitor Labels
        self.update_status_label(self.lbl_status_container, "Container", self.container, self.chk_container)
        self.update_status_label(self.lbl_status_child1, "Child Button", self.btn_child, self.chk_child1)
        self.update_status_label(self.lbl_status_child2, "Child Label", self.lbl_child, self.chk_child2)

    def update_status_label(self, label_control, name, control, internal_chk):
        effective = control.Visible
        internal = internal_chk.Checked
        
        status = "VISIBLE" if effective else "HIDDEN "
        reason = ""
        
        if not effective:
            if not internal:
                reason = "(Self hidden)"
            elif not self.container.Visible and control != self.container:
                reason = "(Parent hidden)"
        
        color = "#008800" if effective else "#CC0000"
        label_control.Text = f"{name:<15}: {status} {reason}"
        label_control.ForeColor = color

if __name__ == "__main__":
    form = VisibilityDemoForm()
    Application.Run(form)

