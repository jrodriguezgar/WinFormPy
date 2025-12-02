"""
AutoSize Example - Windows Forms

This example demonstrates the AutoSize functionality:
- Label with AutoSize automatically adjusting to text
- Button with AutoSize growing/shrinking based on content
- CheckBox with AutoSize adapting to text length
- RadioButton with AutoSize responding to text changes
- Dynamic text updates showing real-time resizing
"""

import sys
import os

# Add module path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from winformpy.py file
import importlib.util
spec = importlib.util.spec_from_file_location("winform_py", 
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib", "winformpy.py"))
winform_py = importlib.util.module_from_spec(spec)
spec.loader.exec_module(winform_py)

Form = winform_py.Form
Button = winform_py.Button
Label = winform_py.Label
CheckBox = winform_py.CheckBox
RadioButton = winform_py.RadioButton
TextBox = winform_py.TextBox
Panel = winform_py.Panel


def main():
    """Main function."""
    # Create form
    form = Form()
    form.Text = "AutoSize - Complete Example"
    form.Width = 1200
    form.Height = 1200
    form.StartPosition = "Manual"
    form.Left = 0
    form.Top = 0
    form.WindowState = "Maximized"
    
    # ===== TITLE =====
    title = Label(form, {
        'Text': "AutoSize Feature Demo - Controls automatically resize to fit content",
        'Left': 20, 'Top': 10,
        'Width': 660,
        'Font': ('Arial', 12, 'bold')
    })
    
    # ===== SECTION 1: Labels with AutoSize =====
    section1 = Label(form, {
        'Text': "1. Labels with AutoSize:",
        'Left': 20, 'Top': 50,
        'Font': ('Arial', 11, 'bold'),
        'Width': 300
    })
    
    # Label with AutoSize
    lbl_auto = Label(form, {
        'Text': "Short text",
        'Left': 20, 'Top': 80,
        'AutoSize': True,
        'BackColor': 'yellow',
        'BorderStyle': 'solid',
        'UseSystemStyles': True
    })
    
    # Size info label
    lbl_info = Label(form, {
        'Text': f"Size: {lbl_auto.Width}x{lbl_auto.Height}",
        'Left': 200, 'Top': 80,
        'Width': 200
    })
    
    # ===== SECTION 2: Buttons with AutoSize =====
    section2 = Label(form, {
        'Text': "2. Buttons with AutoSize:",
        'Left': 20, 'Top': 130,
        'Font': ('Arial', 11, 'bold'),
        'Width': 300
    })
    
    # Button with AutoSize
    btn_auto = Button(form, {
        'Text': "Click",
        'Left': 20, 'Top': 160,
        'AutoSize': True,
        'BorderStyle': 'solid'
    })
    
    # Button size info
    btn_info = Label(form, {
        'Text': f"Size: {btn_auto.Width}x{btn_auto.Height}",
        'Left': 200, 'Top': 160,
        'Width': 200
    })
    
    # ===== SECTION 3: CheckBox with AutoSize =====
    section3 = Label(form, {
        'Text': "3. CheckBox with AutoSize:",
        'Left': 20, 'Top': 210,
        'Font': ('Arial', 11, 'bold'),
        'Width': 300
    })
    
    # CheckBox with AutoSize
    chk_auto = CheckBox(form, {
        'Text': 'Option',
        'Left': 20, 'Top': 240,
        'AutoSize': True,
        'BackColor': 'lightblue',
        'BorderStyle': 'solid'
    })
    
    # CheckBox size info
    chk_info = Label(form, {
        'Text': f"Size: {chk_auto.Width}x{chk_auto.Height}",
        'Left': 200, 'Top': 240,
        'Width': 200
    })
    
    # ===== SECTION 4: RadioButton with AutoSize =====
    section4 = Label(form, {
        'Text': "4. RadioButton with AutoSize:",
        'Left': 20, 'Top': 290,
        'Font': ('Arial', 11, 'bold'),
        'Width': 300
    })
    
    # RadioButton with AutoSize
    rad_auto = RadioButton(form, {
        'Text': "Choice",
        'Left': 20, 'Top': 320,
        'AutoSize': True,
        'BackColor': 'lightgreen',
        'BorderStyle': 'solid'
    })
    
    # RadioButton size info
    rad_info = Label(form, {
        'Text': f"Size: {rad_auto.Width}x{rad_auto.Height}",
        'Left': 200, 'Top': 320,
        'Width': 200
    })
    
    # ===== CONTROL BUTTONS =====
    control_label = Label(form, {
        'Text': "Control Panel - Update text to see AutoSize in action:",
        'Left': 20, 'Top': 370,
        'Font': ('Arial', 11, 'bold'),
        'Width': 500
    })
    
    # Text options
    text_options = [
        "Short",
        "Medium length text",
        "This is a much longer text to demonstrate AutoSize",
        "🎉 Text with emojis! 🚀✨"
    ]
    current_index = [0]
    
    def update_control_text(control, text):
        """Helper to update text and force autosize recalculation."""
        control.Text = text
        # Force autosize recalculation by calling the setter
        if hasattr(control, '_apply_autosize'):
            control._apply_autosize()
        # Refresh pending GUI work without touching _root directly
        form.ForceUpdate()
    
    def update_to_short():
        text = text_options[0]
        update_control_text(lbl_auto, text)
        update_control_text(btn_auto, text)
        update_control_text(chk_auto, text)
        update_control_text(rad_auto, text)
        update_info()
    
    def update_to_medium():
        text = text_options[1]
        update_control_text(lbl_auto, text)
        update_control_text(btn_auto, text)
        update_control_text(chk_auto, text)
        update_control_text(rad_auto, text)
        update_info()
    
    def update_to_long():
        text = text_options[2]
        update_control_text(lbl_auto, text)
        update_control_text(btn_auto, text)
        update_control_text(chk_auto, text)
        update_control_text(rad_auto, text)
        update_info()
    
    def update_to_emoji():
        text = text_options[3]
        update_control_text(lbl_auto, text)
        update_control_text(btn_auto, text)
        update_control_text(chk_auto, text)
        update_control_text(rad_auto, text)
        update_info()
    
    def cycle_text():
        current_index[0] = (current_index[0] + 1) % len(text_options)
        text = text_options[current_index[0]]
        update_control_text(lbl_auto, text)
        update_control_text(btn_auto, text)
        update_control_text(chk_auto, text)
        update_control_text(rad_auto, text)
        update_info()
    
    def update_info():
        # Use a small delay to ensure autosize has been applied
        form._root.after(50, lambda: _update_info_labels())
    
    def _update_info_labels():
        lbl_info.Text = f"Size: {lbl_auto.Width}x{lbl_auto.Height} px"
        btn_info.Text = f"Size: {btn_auto.Width}x{btn_auto.Height} px"
        chk_info.Text = f"Size: {chk_auto.Width}x{chk_auto.Height} px"
        rad_info.Text = f"Size: {rad_auto.Width}x{rad_auto.Height} px"
    
    # Control buttons
    btn_short = Button(form, {
        'Text': "Short",
        'Left': 20, 'Top': 400,
        'Width': 100
    })
    btn_short.Click = update_to_short
    
    btn_medium = Button(form, {
        'Text': "Medium",
        'Left': 130, 'Top': 400,
        'Width': 100
    })
    btn_medium.Click = update_to_medium
    
    btn_long = Button(form, {
        'Text': "Long",
        'Left': 240, 'Top': 400,
        'Width': 100
    })
    btn_long.Click = update_to_long
    
    btn_emoji = Button(form, {
        'Text': "Emoji",
        'Left': 350, 'Top': 400,
        'Width': 100
    })
    btn_emoji.Click = update_to_emoji
    
    btn_cycle = Button(form, {
        'Text': "Cycle All",
        'Left': 460, 'Top': 400,
        'Width': 100,
        'Font': ('Arial', 9, 'bold')
    })
    btn_cycle.Click = cycle_text
    
    # ===== INFORMATION =====
    info_label = Label(form, {
        'Text': "💡 How AutoSize works:",
        'Left': 20, 'Top': 450,
        'Font': ('Arial', 11, 'bold'),
        'Width': 300
    })
    
    info_text = """• AutoSize=True: Control automatically resizes to fit content
• Works with: Label, Button, CheckBox, RadioButton
• Updates dynamically when Text property changes
• Preserves font size and style during resize
• Useful for multilingual apps and dynamic content"""
    
    info_display = Label(form, {
        'Text': info_text.strip(),
        'Left': 20, 'Top': 480,
        'Width': 660,
        'Height': 90,
        'Font': ('Consolas', 9)
    })
    
    # Show form
    form.Show()


if __name__ == "__main__":
    main()
