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

from winformpy import (
    Form, Button, Label, TextBox, CheckBox, Panel, ToolTip,
    DockStyle, Font, FontStyle, Application
)


def main():
    """Main function."""
    # =========================================================================
    # Create main form
    # =========================================================================
    form = Form({
        'Text': 'ToolTip - Complete Example',
        'Width': 900,
        'Height': 780,
        'StartPosition': 'CenterScreen'
    })
    form.ApplyLayout()
    
    # Variables
    click_count = [0]
    
    # =========================================================================
    # TOP PANEL - Title bar
    # =========================================================================
    top_panel = Panel(form, {
        'Height': 80,
        'BackColor': '#0078D4'
    })
    top_panel.Dock = DockStyle.Top
    
    Label(top_panel, {
        'Text': 'TOOLTIP DEMONSTRATION',
        'Left': 20,
        'Top': 12,
        'AutoSize': True,
        'Font': Font('Segoe UI', 16, FontStyle.Bold),
        'ForeColor': '#FFFFFF',
        'BackColor': '#0078D4'
    })
    
    Label(top_panel, {
        'Text': 'Hover over controls to see tooltips with helpful information',
        'Left': 20,
        'Top': 45,
        'AutoSize': True,
        'Font': Font('Segoe UI', 9),
        'ForeColor': '#E0E0E0',
        'BackColor': '#0078D4'
    })
    
    # =========================================================================
    # BOTTOM PANEL - Status bar
    # =========================================================================
    bottom_panel = Panel(form, {
        'Height': 35,
        'BackColor': '#34495E'
    })
    bottom_panel.Dock = DockStyle.Bottom
    
    status_label = Label(bottom_panel, {
        'Text': '💡 Tip: Hover over any control to see its tooltip',
        'Left': 15,
        'Top': 8,
        'AutoSize': True,
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9),
        'BackColor': '#34495E'
    })
    
    # =========================================================================
    # MAIN PANEL - Content area
    # =========================================================================
    main_panel = Panel(form, {
        'BackColor': '#F5F5F5',
        'Padding': 20
    })
    main_panel.Dock = DockStyle.Fill
    
    # ===== TITLE =====
    title = Label(form, {
        'Text': "ToolTip Examples - Hover over controls to see tooltips",
        'Left': 20, 'Top': 20,
        'Font': ('Arial', 14, 'bold'),
        'Width': 650
    })
    
    # ===== SECTION 1: Buttons with Tooltips =====
    section1_label = Label(main_panel, {
        'Text': '1. Buttons with Tooltips:',
        'Left': 20,
        'Top': 20,
        'Font': Font('Segoe UI', 11, FontStyle.Bold),
        'Width': 300,
        'BackColor': '#F5F5F5',
        'ForeColor': '#2C3E50'
    })
    
    # Create tooltips for buttons
    btn_save = Button(main_panel, {
        'Text': '💾 Save',
        'Left': 20,
        'Top': 50,
        'Width': 120,
        'Height': 35,
        'BackColor': '#27AE60',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })
    tooltip_save = ToolTip(btn_save, {
        'Text': 'Save the current document\n(Ctrl+S)',
        'UseSystemStyles': True
    })
    
    btn_open = Button(main_panel, {
        'Text': '📂 Open',
        'Left': 150,
        'Top': 50,
        'Width': 120,
        'Height': 35,
        'BackColor': '#3498DB',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })
    tooltip_open = ToolTip(btn_open, {
        'Text': 'Open an existing file\nSupported formats: .txt, .doc, .pdf',
        'UseSystemStyles': True
    })
    
    btn_delete = Button(main_panel, {
        'Text': '🗑️ Delete',
        'Left': 280,
        'Top': 50,
        'Width': 120,
        'Height': 35,
        'BackColor': '#E74C3C',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })
    tooltip_delete = ToolTip(btn_delete, {
        'Text': '⚠️ WARNING: This action cannot be undone\nPermanently deletes the selected item',
        'UseSystemStyles': True
    })
    
    # ===== SECTION 2: Labels with Information =====
    section2_label = Label(main_panel, {
        'Text': '2. Labels with Additional Information:',
        'Left': 20,
        'Top': 110,
        'Font': Font('Segoe UI', 11, FontStyle.Bold),
        'Width': 400,
        'BackColor': '#F5F5F5',
        'ForeColor': '#2C3E50'
    })
    
    info_label = Label(main_panel, {
        'Text': 'ℹ️ Software Version',
        'Left': 20,
        'Top': 140,
        'Width': 200,
        'ForeColor': '#3498DB',
        'BackColor': '#F5F5F5',
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })
    tooltip_version = ToolTip(info_label, {
        'Text': 'Version: 2.0.1\nRelease Date: Nov 27, 2025\nAuthor: Your Name',
        'UseSystemStyles': True
    })
    
    cpu_label = Label(main_panel, {
        'Text': 'CPU: 45%',
        'Left': 230,
        'Top': 140,
        'Width': 150,
        'BackColor': '#F5F5F5',
        'ForeColor': '#E67E22',
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })
    tooltip_cpu = ToolTip(cpu_label, {
        'Text': 'Central Processing Unit\nCurrent processor usage',
        'UseSystemStyles': True
    })
    
    # ===== SECTION 3: TextBoxes with Help =====
    section3_label = Label(main_panel, {
        'Text': '3. Text Fields with Help:',
        'Left': 20,
        'Top': 190,
        'Font': Font('Segoe UI', 11, FontStyle.Bold),
        'Width': 300,
        'BackColor': '#F5F5F5',
        'ForeColor': '#2C3E50'
    })
    
    username_label = Label(main_panel, {
        'Text': 'Username:',
        'Left': 20,
        'Top': 220,
        'Width': 150,
        'BackColor': '#F5F5F5',
        'Font': Font('Segoe UI', 9)
    })
    
    username_textbox = TextBox(main_panel, {
        'Left': 180,
        'Top': 220,
        'Width': 300
    })
    tooltip_username = ToolTip(username_textbox, {
        'Text': 'Enter your username\nMinimum 4 characters, no spaces',
        'UseSystemStyles': True
    })
    
    email_label = Label(main_panel, {
        'Text': 'Email:',
        'Left': 20,
        'Top': 255,
        'Width': 150,
        'BackColor': '#F5F5F5',
        'Font': Font('Segoe UI', 9)
    })
    
    email_textbox = TextBox(main_panel, {
        'Left': 180,
        'Top': 255,
        'Width': 300
    })
    tooltip_email = ToolTip(email_textbox, {
        'Text': 'Format: user@domain.com\nExample: john.doe@company.com',
        'UseSystemStyles': True
    })
    
    # ===== SECTION 4: CheckBoxes with Explanation =====
    section4_label = Label(main_panel, {
        'Text': '4. Options with Explanation:',
        'Left': 20,
        'Top': 310,
        'Font': Font('Segoe UI', 11, FontStyle.Bold),
        'Width': 300,
        'BackColor': '#F5F5F5',
        'ForeColor': '#2C3E50'
    })
    
    check_auto_save = CheckBox(main_panel, {
        'Text': 'Auto-save',
        'Left': 20,
        'Top': 340,
        'Width': 250,
        'BackColor': '#F5F5F5',
        'Font': Font('Segoe UI', 9)
    })
    tooltip_autosave = ToolTip(check_auto_save, {
        'Text': 'Automatically saves changes every 5 minutes\nPrevents data loss in case of unexpected closure',
        'UseSystemStyles': True
    })
    
    check_notifications = CheckBox(main_panel, {
        'Text': 'Show notifications',
        'Left': 20,
        'Top': 370,
        'Width': 250,
        'BackColor': '#F5F5F5',
        'Font': Font('Segoe UI', 9)
    })
    tooltip_notifications = ToolTip(check_notifications, {
        'Text': 'Display system notifications for:\n• Available updates\n• New messages\n• Important alerts',
        'UseSystemStyles': True
    })
    
    # ===== SECTION 5: Dynamic Tooltip Updates =====
    section5_label = Label(main_panel, {
        'Text': '5. Dynamic Tooltip Update:',
        'Left': 20,
        'Top': 420,
        'Font': Font('Segoe UI', 11, FontStyle.Bold),
        'Width': 300,
        'BackColor': '#F5F5F5',
        'ForeColor': '#2C3E50'
    })
    
    # Counter button with dynamic tooltip
    counter_button = Button(main_panel, {
        'Text': 'Click here (0)',
        'Left': 20,
        'Top': 450,
        'Width': 150,
        'Height': 35,
        'BackColor': '#9B59B6',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })
    tooltip_counter = ToolTip(counter_button, {
        'Text': 'Click to increment the counter',
        'UseSystemStyles': True
    })
    
    def increment_counter():
        click_count[0] += 1
        counter_button.Text = f'Click here ({click_count[0]})'
        
        # Update tooltip dynamically
        if click_count[0] == 1:
            tooltip_counter.Text = 'First click! Keep clicking...'
            status_label.Text = '🎉 First click registered!'
        elif click_count[0] < 5:
            tooltip_counter.Text = f'You have {click_count[0]} clicks. Keep going!'
            status_label.Text = f'📊 Click count: {click_count[0]}'
        elif click_count[0] < 10:
            tooltip_counter.Text = f'{click_count[0]} clicks - You\'re doing great!'
            status_label.Text = f'⭐ Great! {click_count[0]} clicks'
        else:
            tooltip_counter.Text = f'Impressive! {click_count[0]} clicks\nYou\'re a tooltip expert 🎉'
            status_label.Text = f'🏆 Expert level: {click_count[0]} clicks!'
    
    counter_button.Click = increment_counter
    
    # Reset button
    reset_button = Button(main_panel, {
        'Text': 'Reset',
        'Left': 180,
        'Top': 450,
        'Width': 100,
        'Height': 35,
        'BackColor': '#95A5A6',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })
    tooltip_reset = ToolTip(reset_button, {
        'Text': 'Reset counter to zero',
        'UseSystemStyles': True
    })
    
    def reset_counter():
        click_count[0] = 0
        counter_button.Text = 'Click here (0)'
        tooltip_counter.Text = 'Click to increment the counter'
        status_label.Text = '💡 Counter reset to zero'
    
    reset_button.Click = reset_counter
    
    # ===== INFORMATION =====
    info_label = Label(main_panel, {
        'Text': '📋 Features demonstrated:',
        'Left': 20,
        'Top': 510,
        'Font': Font('Segoe UI', 11, FontStyle.Bold),
        'Width': 400,
        'BackColor': '#F5F5F5',
        'ForeColor': '#2C3E50'
    })
    
    info_text = '''• ToolTip with UseSystemStyles for consistent appearance
• Multi-line tooltips using \\n
• Tooltips on Buttons, Labels, TextBoxes, CheckBoxes
• Dynamic tooltip updates based on user interaction
• Rich formatting with emojis and special characters'''
    
    info_display = Label(main_panel, {
        'Text': info_text.strip(),
        'Left': 20,
        'Top': 540,
        'Width': 650,
        'Height': 80,
        'Font': Font('Segoe UI', 9),
        'BackColor': '#ECF0F1',
        'BorderStyle': 'FixedSingle',
        'ForeColor': '#34495E'
    })
    
    # Run the application
    Application.Run(form)


if __name__ == '__main__':
    main()
