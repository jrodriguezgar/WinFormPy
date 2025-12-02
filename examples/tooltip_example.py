"""
ToolTip Example - Windows Forms

This example demonstrates how to use tooltips on different controls:
- Button with ToolTip
- Label with ToolTip
- TextBox with ToolTip
- CheckBox with ToolTip
- Dynamic tooltip updates
- UseSystemStyles for ToolTip
"""

import sys
import os

# Add module path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from winformpy.py file
import importlib.util
spec = importlib.util.spec_from_file_location("winform_py", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib", "winformpy.py"))
winform_py = importlib.util.module_from_spec(spec)
spec.loader.exec_module(winform_py)

Form = winform_py.Form
Button = winform_py.Button
Label = winform_py.Label
TextBox = winform_py.TextBox
CheckBox = winform_py.CheckBox
ToolTip = winform_py.ToolTip


def main():
    """Main function."""
    # Create form
    form = Form()
    form.Text = "ToolTip - Complete Example"
    form.Width = 700
    form.Height = 620
    form.StartPosition = "CenterScreen"
    
    # Variables
    click_count = [0]
    
    # ===== TITLE =====
    title = Label(form, {
        'Text': "ToolTip Examples - Hover over controls to see tooltips",
        'Left': 20, 'Top': 20,
        'Font': ('Arial', 14, 'bold'),
        'Width': 650
    })
    
    # ===== SECTION 1: Buttons with Tooltips =====
    section1_label = Label(form, {
        'Text': "1. Buttons with Tooltips:",
        'Left': 20, 'Top': 60,
        'Font': ('Arial', 11, 'bold'),
        'Width': 300
    })
    
    # Create tooltips for buttons
    btn_save = Button(form, {
        'Text': "💾 Save",
        'Left': 20, 'Top': 90,
        'Width': 120
    })
    tooltip_save = ToolTip(btn_save._tk_widget, {
        'Text': "Save the current document\n(Ctrl+S)",
        'UseSystemStyles': True
    })
    
    btn_open = Button(form, {
        'Text': "📂 Open",
        'Left': 150, 'Top': 90,
        'Width': 120
    })
    tooltip_open = ToolTip(btn_open._tk_widget, {
        'Text': "Open an existing file\nSupported formats: .txt, .doc, .pdf",
        'UseSystemStyles': True
    })
    
    btn_delete = Button(form, {
        'Text': "🗑️ Delete",
        'Left': 280, 'Top': 90,
        'Width': 120
    })
    tooltip_delete = ToolTip(btn_delete._tk_widget, {
        'Text': "⚠️ WARNING: This action cannot be undone\nPermanently deletes the selected item",
        'UseSystemStyles': True
    })
    
    # ===== SECTION 2: Labels with Information =====
    section2_label = Label(form, {
        'Text': "2. Labels with Additional Information:",
        'Left': 20, 'Top': 140,
        'Font': ('Arial', 11, 'bold'),
        'Width': 400
    })
    
    info_label = Label(form, {
        'Text': "ℹ️ Software Version",
        'Left': 20, 'Top': 170,
        'Width': 200,
        'ForeColor': 'blue'
    })
    tooltip_version = ToolTip(info_label._tk_widget, {
        'Text': "Version: 2.0.1\nRelease Date: Nov 27, 2025\nAuthor: Your Name",
        'UseSystemStyles': True
    })
    
    cpu_label = Label(form, {
        'Text': "CPU: 45%",
        'Left': 230, 'Top': 170,
        'Width': 150
    })
    tooltip_cpu = ToolTip(cpu_label._tk_widget, {
        'Text': "Central Processing Unit\nCurrent processor usage",
        'UseSystemStyles': True
    })
    
    # ===== SECTION 3: TextBoxes with Help =====
    section3_label = Label(form, {
        'Text': "3. Text Fields with Help:",
        'Left': 20, 'Top': 210,
        'Font': ('Arial', 11, 'bold'),
        'Width': 300
    })
    
    username_label = Label(form, {
        'Text': "Username:",
        'Left': 20, 'Top': 240,
        'Width': 150
    })
    
    username_textbox = TextBox(form, {
        'Left': 180, 'Top': 240,
        'Width': 300
    })
    tooltip_username = ToolTip(username_textbox._tk_widget, {
        'Text': "Enter your username\nMinimum 4 characters, no spaces",
        'UseSystemStyles': True
    })
    
    email_label = Label(form, {
        'Text': "Email:",
        'Left': 20, 'Top': 280,
        'Width': 150
    })
    
    email_textbox = TextBox(form, {
        'Left': 180, 'Top': 280,
        'Width': 300
    })
    tooltip_email = ToolTip(email_textbox._tk_widget, {
        'Text': "Format: user@domain.com\nExample: john.doe@company.com",
        'UseSystemStyles': True
    })
    
    # ===== SECTION 4: CheckBoxes with Explanation =====
    section4_label = Label(form, {
        'Text': "4. Options with Explanation:",
        'Left': 20, 'Top': 320,
        'Font': ('Arial', 11, 'bold'),
        'Width': 300
    })
    
    check_auto_save = CheckBox(form, {
        'Text': "Auto-save",
        'Left': 20, 'Top': 350,
        'Width': 250
    })
    tooltip_autosave = ToolTip(check_auto_save._tk_widget, {
        'Text': "Automatically saves changes every 5 minutes\nPrevents data loss in case of unexpected closure",
        'UseSystemStyles': True
    })
    
    check_notifications = CheckBox(form, {
        'Text': "Show notifications",
        'Left': 20, 'Top': 380,
        'Width': 250
    })
    tooltip_notifications = ToolTip(check_notifications._tk_widget, {
        'Text': "Display system notifications for:\n• Available updates\n• New messages\n• Important alerts",
        'UseSystemStyles': True
    })
    
    # ===== SECTION 5: Dynamic Tooltip Updates =====
    section5_label = Label(form, {
        'Text': "5. Dynamic Tooltip Update:",
        'Left': 20, 'Top': 420,
        'Font': ('Arial', 11, 'bold'),
        'Width': 300
    })
    
    # Counter button with dynamic tooltip
    counter_button = Button(form, {
        'Text': "Click here (0)",
        'Left': 20, 'Top': 450,
        'Width': 150
    })
    tooltip_counter = ToolTip(counter_button._tk_widget, {
        'Text': "Click to increment the counter",
        'UseSystemStyles': True
    })
    
    def increment_counter():
        click_count[0] += 1
        counter_button.Text = f"Click here ({click_count[0]})"
        
        # Update tooltip dynamically
        if click_count[0] == 1:
            tooltip_counter.Text = "First click! Keep clicking..."
        elif click_count[0] < 5:
            tooltip_counter.Text = f"You have {click_count[0]} clicks. Keep going!"
        elif click_count[0] < 10:
            tooltip_counter.Text = f"{click_count[0]} clicks - You're doing great!"
        else:
            tooltip_counter.Text = f"Impressive! {click_count[0]} clicks\nYou're a tooltip expert 🎉"
    
    counter_button.Click = increment_counter
    
    # Reset button
    reset_button = Button(form, {
        'Text': "Reset",
        'Left': 180, 'Top': 450,
        'Width': 100
    })
    tooltip_reset = ToolTip(reset_button._tk_widget, {
        'Text': "Reset counter to zero",
        'UseSystemStyles': True
    })
    
    def reset_counter():
        click_count[0] = 0
        counter_button.Text = "Click here (0)"
        tooltip_counter.Text = "Click to increment the counter"
    
    reset_button.Click = reset_counter
    
    # ===== INFORMATION =====
    info_label = Label(form, {
        'Text': "💡 Features demonstrated:",
        'Left': 20, 'Top': 500,
        'Font': ('Arial', 11, 'bold'),
        'Width': 400
    })
    
    info_text = """• ToolTip with UseSystemStyles for consistent appearance
• Multi-line tooltips using \\n
• Tooltips on Buttons, Labels, TextBoxes, CheckBoxes
• Dynamic tooltip updates based on user interaction
• Rich formatting with emojis and special characters"""
    
    info_display = Label(form, {
        'Text': info_text.strip(),
        'Left': 20, 'Top': 530,
        'Width': 650,
        'Height': 70,
        'Font': ('Consolas', 9)
    })
    
    # Show form
    form.Show()


if __name__ == "__main__":
    main()
