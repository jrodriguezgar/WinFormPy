"""
LayoutManager Example - Demonstrating the new LayoutManager capabilities
(Updated with Up-Down Wrap)

This example shows how to use LayoutManager with different distributions and alignments.
"""

import sys
import os
import importlib.util
import tkinter as tk

# Load winformpy.py from lib directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
winform_py_path = os.path.join(parent_dir, "winformpy", "winformpy.py")

spec = importlib.util.spec_from_file_location("winform_py", winform_py_path)
winform_py = importlib.util.module_from_spec(spec)
spec.loader.exec_module(winform_py)

# Load winformpy_tools.py
winform_py_tools_path = os.path.join(parent_dir, "winformpy", "winformpy_tools.py")

spec_tools = importlib.util.spec_from_file_location("winform_py_tools", winform_py_tools_path)
winform_py_tools = importlib.util.module_from_spec(spec_tools)
spec_tools.loader.exec_module(winform_py_tools)

# Now we can use the modules
Form = winform_py.Form
Panel = winform_py.Panel
Label = winform_py.Label
Button = winform_py.Button
TextBox = winform_py.TextBox
CheckBox = winform_py.CheckBox
TabControl = winform_py.TabControl
TabPage = winform_py.TabPage
LayoutManager = winform_py_tools.LayoutManager

def main():
    form = Form()
    form.Text = "LayoutManager Demo"
    form.Width = 800
    form.Height = 600
    form.WindowState = "Maximized"

    # Create TabControl
    tab_control = TabControl(form)
    tab_control.Dock = "Fill"
    form.AddControl(tab_control)

    # --- Vertical Layout (Default) ---
    tab_vertical = TabPage(tab_control)
    tab_vertical.Text = "Vertical"
    # Auto-registered, no need to add manually

    lbl_vertical = Label(tab_vertical)
    lbl_vertical.Text = "Vertical Layout (UpDown)"
    lbl_vertical.Font = ("Segoe UI", 10, "bold")
    lbl_vertical.Top = 10
    lbl_vertical.Left = 10
    lbl_vertical.AutoSize = True
    tab_vertical.AddControl(lbl_vertical)

    panel_vertical = Panel(tab_vertical)
    panel_vertical.Top = 40
    panel_vertical.Left = 10
    panel_vertical.Width = 200
    panel_vertical.Height = 400
    panel_vertical.BorderStyle = "FixedSingle"
    panel_vertical.BackColor = "white"
    # panel_vertical.AutoSize = True  <-- Handled by LayoutManager now
    tab_vertical.AddControl(panel_vertical)

    layout_v = LayoutManager(panel_vertical, margin=5, padding=10, autosize_container=True)
    # Default is UpDown, TopLeft

    # Add enough controls for 2 "rows" (conceptually, though vertical is one column)
    # We'll add enough to fill vertical space
    for i in range(10):
        lbl = Label(panel_vertical)
        lbl.Text = f"{i*2+1}. Field {i+1}:"
        lbl.AutoSize = True
        layout_v.add_control(lbl)
        
        txt = TextBox(panel_vertical)
        txt.Text = f"{i*2+2}. Value {i+1}"
        txt.Width = 150
        layout_v.add_control(txt)

    # --- Horizontal Layout (LeftRight) ---
    tab_horizontal = TabPage(tab_control)
    tab_horizontal.Text = "Horizontal"

    lbl_horizontal = Label(tab_horizontal)
    lbl_horizontal.Text = "Horizontal Layout (LeftRight)"
    lbl_horizontal.Font = ("Segoe UI", 10, "bold")
    lbl_horizontal.Top = 10
    lbl_horizontal.Left = 10
    lbl_horizontal.AutoSize = True
    tab_horizontal.AddControl(lbl_horizontal)

    panel_horizontal = Panel(tab_horizontal)
    panel_horizontal.Top = 40
    panel_horizontal.Left = 10
    panel_horizontal.Width = 600
    panel_horizontal.Height = 100
    panel_horizontal.BorderStyle = "FixedSingle"
    panel_horizontal.BackColor = "white"
    # panel_horizontal.AutoSize = True <-- Handled by LayoutManager now
    tab_horizontal.AddControl(panel_horizontal)

    layout_h = LayoutManager(panel_horizontal, margin=5, padding=10, autosize_container=True)
    layout_h.distribution = LayoutManager.Distribution.LeftRight

    # Add enough controls to show horizontal spread
    for i in range(10):
        btn = Button(panel_horizontal)
        btn.Text = f"{i*2+1}. Action"
        btn.Width = 80
        layout_h.add_control(btn)
        
        chk = CheckBox(panel_horizontal)
        chk.Text = f"{i*2+2}. Enable"
        chk.Width = 80
        layout_h.add_control(chk)

    # --- Flow Layout (Wrapping) ---
    tab_flow = TabPage(tab_control)
    tab_flow.Text = "Flow Layout"

    lbl_flow = Label(tab_flow)
    lbl_flow.Text = "Flow Layout (LeftRight + Wrap)"
    lbl_flow.Font = ("Segoe UI", 10, "bold")
    lbl_flow.Top = 10
    lbl_flow.Left = 10
    lbl_flow.AutoSize = True
    tab_flow.AddControl(lbl_flow)

    panel_flow = Panel(tab_flow)
    panel_flow.Top = 40
    panel_flow.Left = 10
    panel_flow.Width = 300 # Narrow width to force wrap
    panel_flow.Height = 300
    panel_flow.BorderStyle = "FixedSingle"
    # panel_flow.AutoSize = True <-- Handled by LayoutManager now
    panel_flow.BackColor = "white"
    tab_flow.AddControl(panel_flow)

    layout_flow = LayoutManager(panel_flow, margin=5, padding=10, autosize_container=True)
    layout_flow.layout_type = LayoutManager.LayoutType.FlowLayout
    layout_flow.distribution = LayoutManager.Distribution.LeftRight

    # Add enough controls for multiple rows
    for i in range(20):
        btn = Button(panel_flow)
        btn.Text = f"{i*2+1}. Item"
        btn.Width = 60
        layout_flow.add_control(btn)
        
        txt = TextBox(panel_flow)
        txt.Text = f"{i*2+2}. Val"
        txt.Width = 50
        layout_flow.add_control(txt)

    # --- Up-Down Wrap Layout ---
    tab_updown_wrap = TabPage(tab_control)
    tab_updown_wrap.Text = "Up-Down Wrap"

    lbl_ud_wrap = Label(tab_updown_wrap)
    lbl_ud_wrap.Text = "Up-Down Layout (Wrap)"
    lbl_ud_wrap.Font = ("Segoe UI", 10, "bold")
    lbl_ud_wrap.Top = 10
    lbl_ud_wrap.Left = 10
    lbl_ud_wrap.AutoSize = True
    tab_updown_wrap.AddControl(lbl_ud_wrap)

    panel_ud_wrap = Panel(tab_updown_wrap)
    panel_ud_wrap.Top = 40
    panel_ud_wrap.Left = 10
    panel_ud_wrap.Width = 400
    panel_ud_wrap.Height = 300
    panel_ud_wrap.BorderStyle = "FixedSingle"
    # panel_ud_wrap.AutoSize = True <-- Handled by LayoutManager now
    panel_ud_wrap.BackColor = "white"
    tab_updown_wrap.AddControl(panel_ud_wrap)

    layout_ud_wrap = LayoutManager(panel_ud_wrap, margin=5, padding=10, autosize_container=True)
    layout_ud_wrap.distribution = LayoutManager.Distribution.UpDown
    layout_ud_wrap.layout_type = LayoutManager.LayoutType.FlowLayout

    # Add enough controls for multiple columns
    for i in range(20):
        btn = Button(panel_ud_wrap)
        btn.Text = f"{i*2+1}. Cmd"
        btn.Width = 70
        layout_ud_wrap.add_control(btn)
        
        chk = CheckBox(panel_ud_wrap)
        chk.Text = f"{i*2+2}. Opt"
        layout_ud_wrap.add_control(chk)

    # --- Fixed Wrap Horizontal (5 items per row) ---
    tab_fixed_h = TabPage(tab_control)
    tab_fixed_h.Text = "Fixed Wrap H (5)"

    lbl_fixed_h = Label(tab_fixed_h)
    lbl_fixed_h.Text = "Fixed Wrap Horizontal (5 items per row)"
    lbl_fixed_h.Font = ("Segoe UI", 10, "bold")
    lbl_fixed_h.Top = 10
    lbl_fixed_h.Left = 10
    lbl_fixed_h.AutoSize = True
    tab_fixed_h.AddControl(lbl_fixed_h)

    panel_fixed_h = Panel(tab_fixed_h)
    panel_fixed_h.Top = 40
    panel_fixed_h.Left = 10
    panel_fixed_h.Width = 400
    panel_fixed_h.Height = 300
    panel_fixed_h.BorderStyle = "FixedSingle"
    panel_fixed_h.BackColor = "white"
    tab_fixed_h.AddControl(panel_fixed_h)

    # Initialize with wrap_count=5
    layout_fixed_h = LayoutManager(panel_fixed_h, margin=5, padding=10, autosize_container=True, wrap_count=5)
    layout_fixed_h.layout_type = LayoutManager.LayoutType.FlowLayout
    layout_fixed_h.distribution = LayoutManager.Distribution.LeftRight

    for i in range(20):
        btn = Button(panel_fixed_h)
        btn.Text = f"{i+1}. Item"
        btn.Width = 80
        layout_fixed_h.add_control(btn)

    # --- Fixed Wrap Vertical (5 items per column) ---
    tab_fixed_v = TabPage(tab_control)
    tab_fixed_v.Text = "Fixed Wrap V (5)"

    lbl_fixed_v = Label(tab_fixed_v)
    lbl_fixed_v.Text = "Fixed Wrap Vertical (5 items per column)"
    lbl_fixed_v.Font = ("Segoe UI", 10, "bold")
    lbl_fixed_v.Top = 10
    lbl_fixed_v.Left = 10
    lbl_fixed_v.AutoSize = True
    tab_fixed_v.AddControl(lbl_fixed_v)

    panel_fixed_v = Panel(tab_fixed_v)
    panel_fixed_v.Top = 40
    panel_fixed_v.Left = 10
    panel_fixed_v.Width = 400
    panel_fixed_v.Height = 300
    panel_fixed_v.BorderStyle = "FixedSingle"
    panel_fixed_v.BackColor = "white"
    tab_fixed_v.AddControl(panel_fixed_v)

    # Initialize with wrap_count=5
    layout_fixed_v = LayoutManager(panel_fixed_v, margin=5, padding=10, autosize_container=True, wrap_count=5)
    layout_fixed_v.layout_type = LayoutManager.LayoutType.FlowLayout
    layout_fixed_v.distribution = LayoutManager.Distribution.UpDown

    for i in range(20):
        btn = Button(panel_fixed_v)
        btn.Text = f"{i+1}. Item"
        btn.Width = 80
        layout_fixed_v.add_control(btn)

    form.ShowDialog()

if __name__ == "__main__":
    main()
