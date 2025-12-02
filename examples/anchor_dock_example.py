"""
Refactored Anchor and Dock Example for WinFormPy.

This example demonstrates:
1. Docking: A panel docked to the left side.
2. Anchoring: Buttons anchored to the bottom-right corner.
"""

import os
import sys
import importlib.util

# --- Boilerplate to load winformpy from lib directory ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
lib_dir = os.path.join(parent_dir, "lib")
module_path = os.path.join(lib_dir, "winformpy.py")

if not os.path.exists(module_path):
    print(f"Error: Could not find winformpy.py at {module_path}")
    sys.exit(1)

spec = importlib.util.spec_from_file_location("winform_py", module_path)
winform_py = importlib.util.module_from_spec(spec)
spec.loader.exec_module(winform_py)

# Import classes
Form = winform_py.Form
Button = winform_py.Button
Label = winform_py.Label
Panel = winform_py.Panel
# --------------------------------------------------------

def main():
    # 1. Create the Main Form
    form = Form()
    form.Text = "Anchor & Dock Demo"
    form.Width = 600
    form.Height = 400
    
    # 2. DOCKING EXAMPLE
    # Create a panel docked to the Left
    panel_menu = Panel(form)
    panel_menu.Width = 150  # Initial width
    panel_menu.BackColor = "#DDDDDD" # Light gray
    panel_menu.Dock = 'Left' # Dock to left edge
    
    # Add content to the docked panel
    lbl_menu = Label(panel_menu)
    lbl_menu.Text = "Docked Panel (Left)"
    lbl_menu.Top = 10
    lbl_menu.Left = 10
    lbl_menu.Width = 130
    
    # 3. ANCHORING EXAMPLE
    # Create a button anchored to Bottom-Right
    # We want it to stay 20px from Right and 20px from Bottom
    
    btn_ok = Button(form)
    btn_ok.Text = "OK"
    btn_ok.Width = 80
    btn_ok.Height = 30
    
    # Calculate initial position based on Form Size (600x400)
    # Note: Form.Width usually maps to Window Size, so Client Size is smaller (e.g. ~540x320)
    # We use a safe margin to ensure visibility.
    # Left = 420 (approx 540 - 80 - 40)
    btn_ok.Left = 420
    btn_ok.Top = 250  # Moved up further to ensure visibility
    
    # Set Anchor AFTER setting position
    btn_ok.Anchor = ['Bottom', 'Right']
    
    # Another button anchored to Bottom-Right (Cancel)
    btn_cancel = Button(form)
    btn_cancel.Text = "Cancel"
    btn_cancel.Width = 80
    btn_cancel.Height = 30
    
    # Left = 420 - 80 - 10 (gap) = 330
    btn_cancel.Left = 330
    btn_cancel.Top = 250  # Moved up further to ensure visibility
    btn_cancel.Anchor = ['Bottom', 'Right']
    
    # 4. ANCHORING TOP-RIGHT
    btn_help = Button(form)
    btn_help.Text = "Help"
    btn_help.Width = 60
    btn_help.Height = 25
    
    # Left = 440 (approx 540 - 60 - 40)
    btn_help.Left = 440
    btn_help.Top = 10
    btn_help.Anchor = ['Top', 'Right']
    
    # 5. CENTER STRETCH (Anchor all sides)
    txt_content = Label(form) # Using Label as a placeholder for text area
    txt_content.Text = "Resize the window!\n\n- Gray Panel is DOCKED Left.\n- Buttons are ANCHORED Bottom-Right.\n- Help button is ANCHORED Top-Right.\n- This text area is ANCHORED to all sides."
    txt_content.BackColor = "white"
    txt_content.BorderStyle = "fixed" # Simulating a text box style
    
    # Position relative to docked panel and margins
    # Left = 150 (panel) + 20 (margin) = 170
    # Top = 50
    # Width = 600 - 170 - 20 (right margin) = 410
    # Height = 250 (buttons top) - 50 (top) - 20 (gap) = 180
    txt_content.Left = 170
    txt_content.Top = 50
    txt_content.Width = 410
    txt_content.Height = 180
    txt_content.Anchor = ['Top', 'Bottom', 'Left', 'Right']

    # Show the form
    form.Show()

if __name__ == "__main__":
    main()
