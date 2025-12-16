"""
AutoLayout Nested Example - Demonstrating Nested AutoLayoutManager

This example shows how to use AutoLayoutManager at two levels:
1. To arrange controls INSIDE a Panel.
2. To arrange multiple Panels WITHIN the main Form.
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
AutoLayoutManager = winform_py_tools.AutoLayoutManager

def create_content_panel(parent_form, index, on_update_layout=None):
    """Creates a panel with 3 internal controls arranged automatically."""
    panel = Panel(parent_form)
    panel.Width = 350
    panel.Height = 110 
    panel.BorderStyle = "FixedSingle"
    panel.BackColor = "white"
    panel.AutoSize = True
    panel.AutoSizeMode = 'GrowOnly'
    # Ensure padding is 0 so internal layout starts at 0,0
    panel.Padding = (5, 5) 
    
    # Layout manager for INSIDE the panel
    # We'll use a small spacing between controls
    # Note: Since we added Padding(5,5), the visual (0,0) is shifted by 5px.
    # But AutoLayoutManager sets Left/Top relative to the container content area.
    # Wait, WinFormPy Panel implementation handles Padding in the widget config (padx/pady).
    # So if we set Left=0, Top=0, it will be at the top-left of the content area.
    internal_layout = AutoLayoutManager(panel, spacing=5)
    
    # 1. Label
    lbl = Label(panel)
    lbl.Text = f"Panel {index} - Header"
    lbl.Font = ("Segoe UI", 9, "bold")
    lbl.AutoSize = True
    panel.AddControl(lbl)
    internal_layout.add_control(lbl)
    
    # 2. TextBox
    txt = TextBox(panel)
    txt.Text = f"Sample Text {index}"
    txt.Width = 200
    panel.AddControl(txt)
    internal_layout.add_control(txt)
    
    # 3. Button
    btn = Button(panel)
    btn.Text = "Añadir Objeto"
    btn.Width = 100
    panel.AddControl(btn)
    # Position button to the right of the textbox
    btn.Left = txt.Left + txt.Width + 10
    btn.Top = txt.Top
    
    # Keep track of controls for dynamic addition
    panel_controls = [lbl, txt, btn]
    
    def on_add_object_click():
        # Create new item - TextBox (like the initial input)
        new_item = TextBox(panel)
        new_item.Text = f"New Item {len(panel_controls)}"
        new_item.Width = 200
        
        panel.AddControl(new_item)
        
        # Insert before button (last item)
        panel_controls.insert(len(panel_controls)-1, new_item)
        
        # Rearrange internal layout
        internal_layout.arrange_all(panel_controls)
        
        # Force button to front to ensure it's not covered
        if hasattr(btn, '_tk_widget'):
            btn._tk_widget.lift()
        
        # Update main layout if callback provided
        if on_update_layout:
            on_update_layout()
            
    btn.Click = on_add_object_click
    
    return panel

def main():
    # Create the main form
    form = Form()
    form.Text = "Nested AutoLayout Example"
    form.Width = 800
    form.Height = 800
    form.WindowState = "Maximized"
    
    # Layout manager for the FORM (to arrange the panels)
    # Spacing between panels
    form_layout = AutoLayoutManager(form, spacing=15)
    
    # Add a title to the form
    title = Label(form)
    title.Text = "Nested Layouts Demo"
    title.Font = ("Segoe UI", 14, "bold")
    title.AutoSize = True
    title.Left = 10 # AutoLayout will overwrite this
    
    if hasattr(form, 'AddControl'):
        form.AddControl(title)
    
    form_layout.add_control(title)
    
    # List to track controls for re-arrangement
    # Start with title
    form_controls = [title]
    
    def update_main_layout():
        form_layout.arrange_all(form_controls)
    
    # Create initial panel (Panel 1)
    panel1 = create_content_panel(form, 1, update_main_layout)
    if hasattr(form, 'AddControl'):
        form.AddControl(panel1)
    form_layout.add_control(panel1)
    form_controls.append(panel1)
    
    # Add "Duplicate Panel" button
    btn_dup = Button(form)
    btn_dup.Text = "Duplicate Panel"
    btn_dup.Width = 150
    btn_dup.Height = 30
    if hasattr(form, 'AddControl'):
        form.AddControl(btn_dup)
    form_layout.add_control(btn_dup)
    form_controls.append(btn_dup)
    
    # Counter for panels
    panel_count = [1]
    
    def on_duplicate_click():
        panel_count[0] += 1
        idx = panel_count[0]
        
        # Create new panel
        new_panel = create_content_panel(form, idx, update_main_layout)
        if hasattr(form, 'AddControl'):
            form.AddControl(new_panel)
            
        # Insert before button
        form_controls.insert(len(form_controls)-1, new_panel)
        
        # Re-arrange all
        update_main_layout()
        
    btn_dup.Click = on_duplicate_click

    form.ShowDialog()

if __name__ == "__main__":
    main()
