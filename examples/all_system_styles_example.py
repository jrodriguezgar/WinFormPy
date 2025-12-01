"""
Complete test of the system styles on all supported controls.

This script demonstrates that the styles system works correctly on:
- Button, Label, TextBox
- ComboBox, ListBox, CheckedListBox
- CheckBox, RadioButton
- Panel, TreeView, StatusBar
"""

import sys
import os
import importlib.util

# Load winform-py.py from parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
module_path = os.path.join(parent_dir, "winform-py.py")

spec = importlib.util.spec_from_file_location("winform_py", module_path)
winform_py = importlib.util.module_from_spec(spec)
spec.loader.exec_module(winform_py)

# Load winform_py_tools.py
tools_path = os.path.join(parent_dir, "winform-py_tools.py")
spec_tools = importlib.util.spec_from_file_location("winform_py_tools", tools_path)
winform_py_tools = importlib.util.module_from_spec(spec_tools)
spec_tools.loader.exec_module(winform_py_tools)

# Import classes from the loaded module
Form = winform_py.Form
Button = winform_py.Button
Label = winform_py.Label
TextBox = winform_py.TextBox
ComboBox = winform_py.ComboBox
ListBox = winform_py.ListBox
CheckBox = winform_py.CheckBox
RadioButton = winform_py.RadioButton
CheckedListBox = winform_py.CheckedListBox
Panel = winform_py.Panel
TreeView = winform_py.TreeView
StatusBar = winform_py.StatusBar
SystemStyles = winform_py.SystemStyles
SystemColors = winform_py.SystemColors
SystemFonts = winform_py.SystemFonts

# Import from tools
FontManager = winform_py_tools.FontManager
ColorManager = winform_py_tools.ColorManager


def main():
    # Get system styles using FontManager and ColorManager
    system_font = FontManager.get_system_font('default')
    system_colors = ColorManager.get_system_colors()
    
    # Configure global system styles
    SystemStyles.SetGlobalFont(system_font)
    SystemStyles.SetGlobalColors(BackColor=system_colors['window'], ForeColor=system_colors['text'])
    
    # Create form
    form = Form({'Text': 'Complete System Styles Test', 'Width': 900, 'Height': 700})
    form.BackColor = system_colors['window']
    
    # ========================================================================
    # SECTION 1: Basic Controls (Column 1)
    # ========================================================================
    
    # Section 1 title
    lbl_title1 = Label(form)
    lbl_title1.Text = "BASIC CONTROLS"
    lbl_title1.Left = 20
    lbl_title1.Top = 10
    lbl_title1.Width = 280
    lbl_title1.Height = 25
    lbl_title1.Font = ("Arial", 10, "bold")
    lbl_title1.BackColor = "#1ABC9C"
    lbl_title1.ForeColor = "#FFFFFF"
    
    # Button with system styles
    btn1 = Button(form, {'UseSystemStyles': True})
    btn1.Text = "Button with styles"
    btn1.Left = 20
    btn1.Top = 45
    btn1.Width = 250
    btn1.Height = 30
    
    # Label with system styles
    lbl1 = Label(form, {'UseSystemStyles': True})
    lbl1.Text = "Label with system styles"
    lbl1.Left = 20
    lbl1.Top = 85
    lbl1.Width = 250
    
    # TextBox with system styles
    txt1 = TextBox(form, {'UseSystemStyles': True})
    txt1.Text = "TextBox with styles"
    txt1.Left = 20
    txt1.Top = 115
    txt1.Width = 250
    
    # ComboBox with system styles
    cmb1 = ComboBox(form, {'UseSystemStyles': True})
    cmb1.Items = ["Option 1", "Option 2", "Option 3"]
    cmb1.Left = 20
    cmb1.Top = 150
    cmb1.Width = 250
    
    # CheckBox with system styles
    chk1 = CheckBox(form, {'UseSystemStyles': True})
    chk1.Text = "CheckBox with styles"
    chk1.Left = 20
    chk1.Top = 185
    chk1.Width = 250
    
    # RadioButton with system styles
    radio1 = RadioButton(form, {'UseSystemStyles': True})
    radio1.Text = "RadioButton 1"
    radio1.Left = 20
    radio1.Top = 220
    radio1.Width = 120
    
    radio2 = RadioButton(form, {'UseSystemStyles': True})
    radio2.Text = "RadioButton 2"
    radio2.Left = 150
    radio2.Top = 220
    radio2.Width = 120
    
    # ========================================================================
    # SECTION 2: List Controls (Column 2)
    # ========================================================================
    
    # Section 2 title
    lbl_title2 = Label(form)
    lbl_title2.Text = "LIST CONTROLS"
    lbl_title2.Left = 310
    lbl_title2.Top = 10
    lbl_title2.Width = 280
    lbl_title2.Height = 25
    lbl_title2.Font = ("Arial", 10, "bold")
    lbl_title2.BackColor = "#3498DB"
    lbl_title2.ForeColor = "#FFFFFF"
    
    # ListBox with system styles
    lst1 = ListBox(form, {'UseSystemStyles': True})
    lst1.Items = ["Item 1", "Item 2", "Item 3", "Item 4"]
    lst1.Left = 310
    lst1.Top = 45
    lst1.Width = 250
    lst1.Height = 100
    
    # CheckedListBox with system styles
    clst1 = CheckedListBox(form, {'UseSystemStyles': True})
    clst1.Items = ["Task 1", "Task 2", "Task 3"]
    clst1.Left = 310
    clst1.Top = 155
    clst1.Width = 250
    clst1.Height = 90
    
    # ========================================================================
    # SECTION 3: Panel with Nested Controls (Column 3)
    # ========================================================================
    
    # Section 3 title
    lbl_title3 = Label(form)
    lbl_title3.Text = "PANEL WITH CONTROLS"
    lbl_title3.Left = 600
    lbl_title3.Top = 10
    lbl_title3.Width = 280
    lbl_title3.Height = 25
    lbl_title3.Font = ("Arial", 10, "bold")
    lbl_title3.BackColor = "#9B59B6"
    lbl_title3.ForeColor = "#FFFFFF"
    
    # Panel with system styles
    panel1 = Panel(form, {'UseSystemStyles': True})
    panel1.Left = 600
    panel1.Top = 45
    panel1.Width = 260
    panel1.Height = 200
    panel1.BorderStyle = "ridge"
    
    # Controls inside the panel
    lbl_panel = Label(form, {'UseSystemStyles': True})
    lbl_panel.Text = "Controls inside the Panel:"
    lbl_panel.Left = 610
    lbl_panel.Top = 55
    lbl_panel.Width = 240
    
    for i in range(3):
        btn_panel = Button(form, {'UseSystemStyles': True})
        btn_panel.Text = f"Panel Button {i+1}"
        btn_panel.Left = 610
        btn_panel.Top = 85 + (i * 40)
        btn_panel.Width = 220
        btn_panel.Height = 30
    
    # ========================================================================
    # SECTION 4: TreeView (Full Width)
    # ========================================================================
    
    # Section 4 title
    lbl_title4 = Label(form)
    lbl_title4.Text = "TREEVIEW WITH STYLES"
    lbl_title4.Left = 20
    lbl_title4.Top = 260
    lbl_title4.Width = 860
    lbl_title4.Height = 25
    lbl_title4.Font = ("Arial", 10, "bold")
    lbl_title4.BackColor = "#E67E22"
    lbl_title4.ForeColor = "#FFFFFF"
    
    # TreeView with system styles
    tree1 = TreeView(form, {'UseSystemStyles': True})
    tree1.Left = 20
    tree1.Top = 295
    tree1.Width = 860
    tree1.Height = 200
    
    # ========================================================================
    # SECTION 5: StatusBar (Bottom)
    # ========================================================================
    
    # StatusBar with system styles
    status = StatusBar(form, {'UseSystemStyles': True})
    status.Text = "System styles obtained with FontManager and ColorManager applied to 11 control types"
    status.Left = 0
    status.Top = 640
    status.Width = 900
    status.Height = 30
    status.Font = system_font
    
    # ========================================================================
    # SECTION 6: Information and Controls
    # ========================================================================
    
    # Information panel
    info_panel = Panel(form)
    info_panel.Left = 20
    info_panel.Top = 510
    info_panel.Width = 860
    info_panel.Height = 120
    info_panel.BackColor = "#34495E"
    info_panel.BorderStyle = "ridge"
    
    # Info title
    lbl_info_title = Label(form)
    lbl_info_title.Text = "SYSTEM STYLES INFORMATION"
    lbl_info_title.Left = 30
    lbl_info_title.Top = 520
    lbl_info_title.Width = 840
    lbl_info_title.Height = 20
    lbl_info_title.Font = ("Arial", 9, "bold")
    lbl_info_title.ForeColor = "#1ABC9C"
    
    # Info text
    lbl_info = Label(form)
    lbl_info.Text = (
        f"✓ Global Styles: Font={system_font}, BackColor='{system_colors['window']}', ForeColor='{system_colors['text']}'\n"
        "✓ All visible controls use UseSystemStyles=True\n"
        "✓ 11 control types fully support the styles system\n"
        "✓ Styles are obtained from the system using FontManager and ColorManager"
    )
    lbl_info.Left = 30
    lbl_info.Top = 545
    lbl_info.Width = 840
    lbl_info.Height = 70
    lbl_info.Font = system_font
    lbl_info.ForeColor = system_colors['text']
    
    # Button to toggle styles
    def toggle_styles():
        current = SystemStyles._use_system_styles_by_default
        SystemStyles.SetUseSystemStylesByDefault(not current)
        status.Text = f"System styles: {'DISABLED' if current else 'ENABLED'}"
    
    btn_toggle = Button(form)
    btn_toggle.Text = "Toggle System Styles"
    btn_toggle.Left = 700
    btn_toggle.Top = 560
    btn_toggle.Width = 160
    btn_toggle.Height = 40
    btn_toggle.BackColor = "#E74C3C"
    btn_toggle.ForeColor = "#FFFFFF"
    btn_toggle.Font = ("Segoe UI", 9, "bold")
    btn_toggle.Click = toggle_styles
    
    # Mostrar formulario
    form.Show()


if __name__ == '__main__':
    main()
