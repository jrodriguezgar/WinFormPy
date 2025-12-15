"""
Example demonstrating basic WinFormPy controls with countdown timer
Controls: Line, Timer, ProgressBar, Button, Label, TextBox, RadioButton, ComboBox, CheckBox
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
ProgressBar = winform_py.ProgressBar
Timer = winform_py.Timer
Line = winform_py.Line


def main():
    # Create main form
    form = Form()
    form.Text = "Basic Controls Demo - WinFormPy"
    form.Width = 720
    form.Height = 620
    form.StartPosition = "CenterScreen"
    form.BackColor = "white"
    
    # ===== COUNTDOWN SECTION =====
    # Title label
    lbl_title = Label(form, {
        'Text': 'WinFormPy Basic Controls Demo',
        'Left': 20,
        'Top': 20,
        'Width': 660,
        'Height': 30,
        'Font': ('Segoe UI', 16, 'bold'),
        'ForeColor': 'navy'
    })
    
    # Horizontal line separator using Line control
    line1 = Line(form, {
        'Left': 20,
        'Top': 55,
        'Width': 660,
        'Height': 5,
        'BackColor': 'blue'
    })
    
    # Countdown label (Label control demonstration)
    lbl_countdown = Label(form, {
        'Text': 'Initializing... 5 seconds',
        'Left': 20,
        'Top': 70,
        'Width': 400,
        'Height': 25,
        'Font': ('Segoe UI', 12, 'bold'),
        'ForeColor': 'red',
        'BackColor': 'lightyellow'
    })
    
    # Progress bar (ProgressBar control demonstration)
    progress = ProgressBar(form, {
        'Left': 20,
        'Top': 100,
        'Width': 660,
        'Height': 25,
        'Maximum': 5,
        'Value': 0
    })
    
    # Timer for countdown (Timer control demonstration)
    countdown_value = [5]  # Use list to modify in nested function
    timer = Timer(form._root)
    timer.Interval = 1000  # 1 second
    
    # Button initially disabled (Button control demonstration)
    btn_continue = Button(form, {
        'Text': 'Please wait...',
        'Left': 20,
        'Top': 135,
        'Width': 150,
        'Height': 35,
        'Enabled': False,
        'Font': ('Segoe UI', 10)
    })
    
    # ===== CONTROLS DEMONSTRATION SECTION =====
    # Section separator (default: black, 1px)
    line2 = Line(form, {
        'Left': 20,
        'Top': 185,
        'Width': 660
    })
    
    lbl_section = Label(form, {
        'Text': 'Control Examples',
        'Left': 20,
        'Top': 195,
        'Width': 300,
        'Font': ('Segoe UI', 12, 'bold'),
        'ForeColor': 'black'
    })
    
    # TextBox example
    lbl_textbox = Label(form, {
        'Text': '1. TextBox - Enter your name:',
        'Left': 20,
        'Top': 230,
        'Width': 200,
        'ForeColor': 'black'
    })
    
    txt_name = TextBox(form, {
        'Text': 'Enter your name here',
        'Left': 230,
        'Top': 227,
        'Width': 250,
        'Height': 25,
        'SelectAllOnClick': True
    })
    
    lbl_result = Label(form, {
        'Text': 'Type something...',
        'Left': 490,
        'Top': 230,
        'Width': 180,
        'ForeColor': 'green'
    })
    
    def on_textbox_changed(sender=None, e=None):
        text = txt_name.Text
        if text:
            lbl_result.Text = f"Hello, {text}!"
        else:
            lbl_result.Text = "Type something..."
    
    txt_name.TextChanged = on_textbox_changed
    
    # CheckBox example
    lbl_checkbox = Label(form, {
        'Text': '2. CheckBox - Select options:',
        'Left': 20,
        'Top': 270,
        'Width': 200,
        'ForeColor': 'black'
    })
    
    chk_option1 = CheckBox(form, {
        'Text': 'Option A',
        'Left': 230,
        'Top': 268,
        'Width': 100,
        'Checked': False
    })
    
    chk_option2 = CheckBox(form, {
        'Text': 'Option B',
        'Left': 340,
        'Top': 268,
        'Width': 100,
        'Checked': True
    })
    
    lbl_checkbox_result = Label(form, {
        'Text': 'B selected',
        'Left': 450,
        'Top': 270,
        'Width': 220,
        'ForeColor': 'purple'
    })
    
    def update_checkbox_result(sender=None, e=None):
        selected = []
        if chk_option1.Checked:
            selected.append('A')
        if chk_option2.Checked:
            selected.append('B')
        
        if selected:
            lbl_checkbox_result.Text = f"Selected: {', '.join(selected)}"
        else:
            lbl_checkbox_result.Text = "None selected"
    
    chk_option1.CheckedChanged = update_checkbox_result
    chk_option2.CheckedChanged = update_checkbox_result
    
    # RadioButton example
    lbl_radio = Label(form, {
        'Text': '3. RadioButton - Choose one:',
        'Left': 20,
        'Top': 310,
        'Width': 200,
        'ForeColor': 'black'
    })
    
    radio1 = RadioButton(form, {
        'Text': 'Red',
        'Left': 230,
        'Top': 308,
        'Width': 80,
        'Checked': True
    })
    
    radio2 = RadioButton(form, {
        'Text': 'Blue',
        'Left': 320,
        'Top': 308,
        'Width': 80,
        'Checked': False
    })
    
    radio3 = RadioButton(form, {
        'Text': 'Green',
        'Left': 410,
        'Top': 308,
        'Width': 80,
        'Checked': False
    })
    
    lbl_radio_result = Label(form, {
        'Text': 'Color: Red',
        'Left': 500,
        'Top': 310,
        'Width': 170,
        'ForeColor': 'red'
    })
    
    def on_radio_changed(sender=None, e=None):
        if radio1.Checked:
            lbl_radio_result.Text = "Color: Red"
            lbl_radio_result.ForeColor = "red"
        elif radio2.Checked:
            lbl_radio_result.Text = "Color: Blue"
            lbl_radio_result.ForeColor = "blue"
        elif radio3.Checked:
            lbl_radio_result.Text = "Color: Green"
            lbl_radio_result.ForeColor = "green"
    
    radio1.CheckedChanged = on_radio_changed
    radio2.CheckedChanged = on_radio_changed
    radio3.CheckedChanged = on_radio_changed
    
    # ComboBox example
    lbl_combo = Label(form, {
        'Text': '4. ComboBox - Select a city:',
        'Left': 20,
        'Top': 350,
        'Width': 200,
        'ForeColor': 'black'
    })
    
    combo_cities = ComboBox(form, {
        'Left': 230,
        'Top': 347,
        'Width': 200,
        'Items': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao']
    })
    combo_cities.SelectedIndex = 0
    
    lbl_combo_result = Label(form, {
        'Text': 'Selected: Madrid',
        'Left': 440,
        'Top': 350,
        'Width': 230,
        'ForeColor': 'darkorange'
    })
    
    def on_combo_changed(sender=None, e=None):
        if combo_cities.SelectedItem:
            lbl_combo_result.Text = f"Selected: {combo_cities.SelectedItem}"
    
    combo_cities.SelectedIndexChanged = on_combo_changed
    
    # Action Button example (different from countdown button)
    lbl_button = Label(form, {
        'Text': '5. Button - Click action:',
        'Left': 20,
        'Top': 390,
        'Width': 200,
        'ForeColor': 'black'
    })
    
    click_count = [0]
    
    btn_action = Button(form, {
        'Text': 'Click Me!',
        'Left': 230,
        'Top': 385,
        'Width': 120,
        'Height': 35
    })
    
    lbl_button_result = Label(form, {
        'Text': 'Clicks: 0',
        'Left': 360,
        'Top': 390,
        'Width': 310,
        'ForeColor': 'teal'
    })
    
    def on_action_click(sender=None, e=None):
        click_count[0] += 1
        lbl_button_result.Text = f"Clicks: {click_count[0]} - Last clicked at {countdown_value[0]}s remaining"
        btn_action.Text = f"Clicked {click_count[0]}x"
    
    btn_action.Click = on_action_click
    
    # Separator line
    line3 = Line(form, {
        'Left': 20,
        'Top': 440,
        'Width': 660,
        'Height': 5,
        'BackColor': 'gray'
    })
    
    # Summary labels
    lbl_summary_title = Label(form, {
        'Text': 'Controls Demonstrated:',
        'Left': 20,
        'Top': 455,
        'Width': 660,
        'Font': ('Segoe UI', 10, 'bold'),
        'ForeColor': 'black'
    })
    
    lbl_summary = Label(form, {
        'Text': '✓ Line (separators)  ✓ Timer (countdown)  ✓ ProgressBar (visual feedback)\n' +
                '✓ Button (actions)  ✓ Label (text display)  ✓ TextBox (text input)\n' +
                '✓ RadioButton (single choice)  ✓ ComboBox (dropdown)  ✓ CheckBox (multiple choice)',
        'Left': 20,
        'Top': 480,
        'Width': 660,
        'Height': 80,
        'Font': ('Segoe UI', 9),
        'ForeColor': 'black'
    })
    
    # Timer tick event handler
    def on_timer_tick(sender=None, e=None):
        countdown_value[0] -= 1
        lbl_countdown.Text = f'Loading controls... {countdown_value[0]} seconds'
        progress.Value = 5 - countdown_value[0]
        
        # Force visual update
        lbl_countdown.Invalidate()
        progress.Invalidate()
        
        if countdown_value[0] <= 0:
            timer.Stop()
            btn_continue.Enabled = True
            btn_continue.Text = 'Ready! ✓'
            lbl_countdown.Text = 'All controls loaded!'
            lbl_countdown.ForeColor = 'green'
            lbl_countdown.BackColor = 'lightgreen'
            progress.Value = 5
    
    timer.Tick = on_timer_tick
    
    # Start timer automatically when form loads
    def on_form_load(sender=None, e=None):
        timer.Start()
    
    form.Load = on_form_load
    
    # Continue button click (just for demonstration)
    def on_continue_click(sender=None, e=None):
        txt_name.Text = "Demo User"
        combo_cities.SelectedIndex = 2  # Valencia
        on_textbox_changed()
        on_combo_changed()
    
    btn_continue.Click = on_continue_click
    
    form.Show()


if __name__ == "__main__":
    main()