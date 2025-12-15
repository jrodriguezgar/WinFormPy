"""
Example demonstrating container controls in WinFormPy
Containers: GroupBox, Panel, TabControl with TabPages
"""

import sys
import os
import importlib.util

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lib_dir = os.path.join(parent_dir, "winformpy")
sys.path.insert(0, parent_dir)

# Import winformpy.py
module_path = os.path.join(lib_dir, "winformpy.py")
spec = importlib.util.spec_from_file_location("winform_py", module_path)
winform_py = importlib.util.module_from_spec(spec)
spec.loader.exec_module(winform_py)

# Extract classes
Form = winform_py.Form
Label = winform_py.Label
Button = winform_py.Button
TextBox = winform_py.TextBox
CheckBox = winform_py.CheckBox
RadioButton = winform_py.RadioButton
ComboBox = winform_py.ComboBox
GroupBox = winform_py.GroupBox
Panel = winform_py.Panel
TabControl = winform_py.TabControl
TabPage = winform_py.TabPage


def main():
    # Create main form
    form = Form()
    form.Text = "Containers Demo - WinFormPy"
    form.Width = 900
    form.Height = 650
    form.StartPosition = "CenterScreen"
    form.BackColor = "white"
    
    # ===== TITLE =====
    lbl_title = Label(form, {
        'Text': 'Container Controls Demo',
        'Left': 20,
        'Top': 10,
        'Width': 860,
        'Height': 30,
        'Font': ('Arial', 16, 'bold'),
        'ForeColor': '#2c3e50'
    })
    
    # ==================== GROUPBOX SECTION ====================
    lbl_groupbox_section = Label(form, {
        'Text': '1. GroupBox Container',
        'Left': 20,
        'Top': 50,
        'Width': 250,
        'Height': 20,
        'Font': ('Arial', 10, 'bold'),
        'ForeColor': '#34495e'
    })
    
    groupbox = GroupBox(form, {
        'Text': 'User Information',
        'Left': 20,
        'Top': 75,
        'Width': 400,
        'Height': 180,
        'Font': ('Arial', 9, 'bold'),
        'ForeColor': '#2980b9'
    })
    
    lbl_name = Label(groupbox, {
        'Text': 'Name:',
        'Left': 10,
        'Top': 20,
        'Width': 60,
        'Height': 25
    })
    
    txt_name = TextBox(groupbox, {
        'Left': 75,
        'Top': 20,
        'Width': 300,
        'Height': 25,
        'Text': 'John Doe'
    })
    
    lbl_email = Label(groupbox, {
        'Text': 'Email:',
        'Left': 10,
        'Top': 55,
        'Width': 60,
        'Height': 25
    })
    
    txt_email = TextBox(groupbox, {
        'Left': 75,
        'Top': 55,
        'Width': 300,
        'Height': 25,
        'Text': 'john@example.com'
    })
    
    chk_active = CheckBox(groupbox, {
        'Text': 'Active Account',
        'Left': 10,
        'Top': 95,
        'Width': 150,
        'Height': 25,
        'Checked': True
    })
    
    chk_notifications = CheckBox(groupbox, {
        'Text': 'Receive Notifications',
        'Left': 10,
        'Top': 125,
        'Width': 180,
        'Height': 25,
        'Checked': False
    })
    
    # ==================== PANEL SECTION ====================
    lbl_panel_section = Label(form, {
        'Text': '2. Panel Container (with Border)',
        'Left': 450,
        'Top': 50,
        'Width': 250,
        'Height': 20,
        'Font': ('Arial', 10, 'bold'),
        'ForeColor': '#34495e'
    })
    
    panel = Panel(form, {
        'Left': 450,
        'Top': 75,
        'Width': 400,
        'Height': 180,
        'BackColor': 'lightgray',
        'BorderStyle': 1  # FixedSingle (solid border, more visible)
    })
    
    Label(panel, {
        'Text': 'Preferences (Inside Panel)',
        'Left': 10,
        'Top': 10,
        'Width': 200,
        'Height': 25,
        'Font': ('Arial', 9, 'bold', 'underline')
    })
    
    Label(panel, {
        'Text': 'Theme:',
        'Left': 10,
        'Top': 45,
        'Width': 60,
        'Height': 25
    })
    
    rb_light = RadioButton(panel, {
        'Text': 'Light Theme',
        'Left': 80,
        'Top': 45,
        'Width': 120,
        'Height': 25,
        'Checked': True
    })
    
    rb_dark = RadioButton(panel, {
        'Text': 'Dark Theme',
        'Left': 210,
        'Top': 45,
        'Width': 120,
        'Height': 25
    })
    
    Label(panel, {
        'Text': 'Language:',
        'Left': 10,
        'Top': 80,
        'Width': 70,
        'Height': 25
    })
    
    cmb_lang = ComboBox(panel, {
        'Left': 80,
        'Top': 80,
        'Width': 200,
        'Height': 25
    })
    cmb_lang.Items.append("English")
    cmb_lang.Items.append("Spanish")
    cmb_lang.Items.append("French")
    cmb_lang.SelectedIndex = 0
    
    Button(panel, {
        'Text': 'Save Preferences',
        'Left': 80,
        'Top': 130,
        'Width': 150,
        'Height': 30,
        'BackColor': '#2ecc71',
        'ForeColor': 'white'
    })
    
    # ==================== TABCONTROL SECTION ====================
    lbl_tab_section = Label(form, {
        'Text': '3. TabControl Container',
        'Left': 20,
        'Top': 280,
        'Width': 250,
        'Height': 20,
        'Font': ('Arial', 10, 'bold'),
        'ForeColor': '#34495e'
    })
    
    tab_control = TabControl(form, {
        'Left': 20,
        'Top': 305,
        'Width': 850,
        'Height': 270
    })
    
    # Create TabPages
    tab_info = TabPage({'Text': 'Personal', 'Name': 'tabInfo'})
    tab_contact = TabPage({'Text': 'Contact', 'Name': 'tabContact'})
    tab_settings = TabPage({'Text': 'Settings', 'Name': 'tabSettings'})
    
    # Add TabPages to TabControl
    tab_control.AddTab(tab_info)
    tab_control.AddTab(tab_contact)
    tab_control.AddTab(tab_settings)
    
    # ===== TAB 1: Personal Info =====
    Label(tab_info, {
        'Text': 'Personal Information',
        'Left': 20,
        'Top': 15,
        'Width': 300,
        'Height': 25,
        'Font': ('Arial', 12, 'bold'),
        'ForeColor': '#2c3e50'
    })
    
    Label(tab_info, {
        'Text': 'First Name:',
        'Left': 20,
        'Top': 50,
        'Width': 100,
        'Height': 25
    })
    
    txt_firstname = TextBox(tab_info, {
        'Left': 130,
        'Top': 50,
        'Width': 200,
        'Height': 25
    })
    
    Label(tab_info, {
        'Text': 'Last Name:',
        'Left': 20,
        'Top': 85,
        'Width': 100,
        'Height': 25
    })
    
    txt_lastname = TextBox(tab_info, {
        'Left': 130,
        'Top': 85,
        'Width': 200,
        'Height': 25
    })
    
    Label(tab_info, {
        'Text': 'Age:',
        'Left': 20,
        'Top': 120,
        'Width': 100,
        'Height': 25
    })
    
    txt_age = TextBox(tab_info, {
        'Left': 130,
        'Top': 120,
        'Width': 80,
        'Height': 25
    })
    
    # ===== TAB 2: Contact Info =====
    Label(tab_contact, {
        'Text': 'Contact Information',
        'Left': 20,
        'Top': 15,
        'Width': 300,
        'Height': 25,
        'Font': ('Arial', 12, 'bold'),
        'ForeColor': '#2c3e50'
    })
    
    Label(tab_contact, {
        'Text': 'Phone:',
        'Left': 20,
        'Top': 50,
        'Width': 100,
        'Height': 25
    })
    
    txt_phone = TextBox(tab_contact, {
        'Left': 130,
        'Top': 50,
        'Width': 200,
        'Height': 25
    })
    
    Label(tab_contact, {
        'Text': 'Address:',
        'Left': 20,
        'Top': 85,
        'Width': 100,
        'Height': 25
    })
    
    txt_address = TextBox(tab_contact, {
        'Left': 130,
        'Top': 85,
        'Width': 400,
        'Height': 25
    })
    
    Label(tab_contact, {
        'Text': 'City:',
        'Left': 20,
        'Top': 120,
        'Width': 100,
        'Height': 25
    })
    
    txt_city = TextBox(tab_contact, {
        'Left': 130,
        'Top': 120,
        'Width': 200,
        'Height': 25
    })
    
    # ===== TAB 3: Settings with nested containers =====
    Label(tab_settings, {
        'Text': 'Application Settings',
        'Left': 20,
        'Top': 15,
        'Width': 300,
        'Height': 25,
        'Font': ('Arial', 12, 'bold'),
        'ForeColor': '#2c3e50'
    })
    
    # Nested GroupBox in Tab
    grp_nested = GroupBox(tab_settings, {
        'Text': 'Display',
        'Left': 20,
        'Top': 50,
        'Width': 380,
        'Height': 160,
        'Font': ('Arial', 9, 'bold')
    })
    
    CheckBox(grp_nested, {
        'Text': 'Fullscreen Mode',
        'Left': 15,
        'Top': 20,
        'Width': 200,
        'Height': 25
    })
    
    CheckBox(grp_nested, {
        'Text': 'Show Toolbar',
        'Left': 15,
        'Top': 50,
        'Width': 200,
        'Height': 25,
        'Checked': True
    })
    
    CheckBox(grp_nested, {
        'Text': 'Show Status Bar',
        'Left': 15,
        'Top': 80,
        'Width': 200,
        'Height': 25,
        'Checked': True
    })
    
    # Nested Panel in Tab
    panel_nested = Panel(tab_settings, {
        'Left': 420,
        'Top': 50,
        'Width': 400,  # Increased width to fit all controls
        'Height': 140,
        'BackColor': '#e8f8f5',
        'BorderStyle': 2,  # Fixed3D for more visible border
        'AutoSize': True
    })
    
    Label(panel_nested, {
        'Text': 'Advanced',
        'Left': 10,
        'Top': 10,
        'Width': 360,
        'Height': 25,
        'Font': ('Arial', 9, 'bold')
    })
    
    CheckBox(panel_nested, {
        'Text': 'Debug Mode',
        'Left': 15,
        'Top': 40,
        'Width': 200,
        'Height': 25
    })
    
    CheckBox(panel_nested, {
        'Text': 'Logging Enabled',
        'Left': 15,
        'Top': 70,
        'Width': 200,
        'Height': 25,
        'Checked': True
    })
    
    CheckBox(panel_nested, {
        'Text': 'Performance Monitor',
        'Left': 15,
        'Top': 100,
        'Width': 200,
        'Height': 25
    })
    
    # Force update of the Panel to apply AutoSize and border changes
    panel_nested.Refresh()
    
    # ===== STATUS BAR =====
    status_label = Label(form, {
        'Text': 'Ready - Demonstrating GroupBox and TabControl containers',
        'Left': 20,
        'Top': 600,
        'Width': 850,
        'Height': 30,
        'BackColor': '#34495e',
        'ForeColor': 'white',
        'Font': ('Arial', 9)
    })
    
    # ===== EVENT HANDLERS =====
    def on_tab_changed():
        tab_names = ['Personal', 'Contact', 'Settings']
        idx = tab_control.SelectedIndex
        if 0 <= idx < len(tab_names):
            status_label.Text = f"Current tab: {tab_names[idx]}"
    
    tab_control.SelectedIndexChanged = on_tab_changed
    
    
    # Force update before showing (required for complex layouts with containers)
    form.Refresh()
    
    # Show form
    form.ShowDialog()


if __name__ == "__main__":
    main()
