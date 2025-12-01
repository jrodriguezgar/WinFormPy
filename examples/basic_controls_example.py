"""
Example demonstrating a countdown timer with progress bar and sequential control display
"""

import sys
import os
import importlib.util

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import winform-py.py
module_path = os.path.join(parent_dir, "winform-py.py")
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
ListBox = winform_py.ListBox
ProgressBar = winform_py.ProgressBar
Panel = winform_py.Panel
Timer = winform_py.Timer


def main():
    # Create main form
    form = Form()
    form.Text = "Countdown Controls Demo"
    form.Width = 600
    form.Height = 500
    form.StartPosition = "CenterScreen"
    form.WindowState = "Maximized"  # Maximize the window
    
    # Title label
    lbl_title = Label(form, {
        'Text': 'Countdown Timer Demo',
        'Left': 20,
        'Top': 20,
        'Width': 300,
        'Font': ('Segoe UI', 14, 'bold')
    })
    
    # Countdown label
    lbl_countdown = Label(form, {
        'Text': 'Time remaining: 5 seconds',
        'Left': 20,
        'Top': 60,
        'Width': 200
    })
    
    # Progress bar
    progress = ProgressBar(form, {
        'Left': 20,
        'Top': 90,
        'Width': 300,
        'Height': 20,
        'Maximum': 5,
        'Value': 5  # Start full, will empty as countdown progresses
    })
    
    # Button to show controls (initially disabled)
    btn_show = Button(form, {
        'Text': 'Show Controls',
        'Left': 350,
        'Top': 85,
        'Width': 150,
        'Enabled': False
    })
    
    # Timer for countdown
    countdown_value = 5
    timer = Timer(form._root)
    timer.Interval = 1000  # 1 second
    
    def on_timer_tick():
        nonlocal countdown_value
        countdown_value -= 1
        lbl_countdown.Text = f'Time remaining: {countdown_value} seconds'
        progress.Value = countdown_value  # Empty the progress bar as countdown progresses
        
        # Force GUI update
        form._root.update_idletasks()
        
        if countdown_value <= 0:
            timer.Stop()
            btn_show.Enabled = True
            lbl_countdown.Text = 'Countdown complete! Click the button to see controls.'
    
    timer.Tick = on_timer_tick
    timer.Start()
    
    # List of controls to show
    controls_to_show = [
        ('Label', 'This is a Label'),
        ('TextBox', 'TextBox example'),
        ('Button', 'Sample Button'),
        ('CheckBox', 'CheckBox example'),
        ('RadioButton', 'RadioButton example'),
        ('ComboBox', ['Item 1', 'Item 2', 'Item 3']),
        ('ListBox', ['List Item 1', 'List Item 2', 'List Item 3']),
        ('Panel', 'Panel with Border')
    ]
    
    current_control_index = 0
    y_position = 140
    
    def on_button_click():
        nonlocal current_control_index, y_position
        if current_control_index < len(controls_to_show):
            control_name, control_value = controls_to_show[current_control_index]
            
            # Add a label above the control
            info_label = Label(form, {
                'Text': f'{current_control_index + 1}. {control_name}',
                'Left': 20,
                'Top': y_position - 25,
                'Width': 200,
                'Font': ('Segoe UI', 10, 'bold')
            })
            
            # Create the control based on type
            if control_name == 'Label':
                control = Label(form, {'Text': control_value, 'Left': 20, 'Top': y_position, 'Width': 200})
            elif control_name == 'TextBox':
                control = TextBox(form, {'Text': control_value, 'Left': 20, 'Top': y_position, 'Width': 200})
            elif control_name == 'Button':
                control = Button(form, {'Text': control_value, 'Left': 20, 'Top': y_position, 'Width': 150})
            elif control_name == 'CheckBox':
                control = CheckBox(form, {'Text': control_value, 'Left': 20, 'Top': y_position})
            elif control_name == 'RadioButton':
                control = RadioButton(form, {'Text': control_value, 'Left': 20, 'Top': y_position})
            elif control_name == 'ComboBox':
                control = ComboBox(form, {'Left': 20, 'Top': y_position, 'Width': 200, 'Items': control_value})
            elif control_name == 'ListBox':
                control = ListBox(form, {'Left': 20, 'Top': y_position, 'Width': 200, 'Height': 80, 'Items': control_value})
            elif control_name == 'Panel':
                control = Panel(form, {'Left': 20, 'Top': y_position, 'Width': 200, 'Height': 80, 'BackColor': 'lightblue', 'Text': control_value, 'BorderStyle': 'Fixed3D'})
                # Add a RadioButton inside the panel
                inner_radiobutton = RadioButton(control, {'Text': 'RadioButton inside Panel', 'Left': 10, 'Top': 10, 'Width': 180})
                control.AddControl(inner_radiobutton)
            
            y_position += 80  # Space for next control
            current_control_index += 1
            
            if current_control_index >= len(controls_to_show):
                btn_show.Text = 'All controls shown!'
                btn_show.Enabled = False
        else:
            btn_show.Enabled = False
    
    btn_show.Click = on_button_click
    
    form.ShowDialog()


if __name__ == "__main__":
    main()