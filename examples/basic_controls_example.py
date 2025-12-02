"""
Example demonstrating a countdown timer with progress bar and sequential control display
"""

import sys
import os
import importlib.util

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lib_dir = os.path.join(parent_dir, "lib")
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
ListBox = winform_py.ListBox
ProgressBar = winform_py.ProgressBar
Panel = winform_py.Panel
GroupBox = winform_py.GroupBox
Timer = winform_py.Timer


def main():
    # Create main form
    form = Form()
    form.Text = "Countdown Controls Demo"
    form.Width = 550
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
        'Value': 0  # Start empty, will fill as countdown progresses
    })
    
    # Button to show controls (initially enabled to start countdown)
    btn_show = Button(form, {
        'Text': 'Start Countdown',
        'Left': 350,
        'Top': 85,
        'Width': 150,
        'Enabled': True
    })
    
    # Timer for countdown
    countdown_value = 5
    timer = Timer(form._root)
    timer.Interval = 1000  # 1 second
    countdown_started = False
    
    def on_timer_tick():
        nonlocal countdown_value
        countdown_value -= 1
        lbl_countdown.Text = f'Time remaining: {countdown_value} seconds'
        progress.Value = 5 - countdown_value  # Fill the progress bar as countdown progresses
        
        # Force GUI update
        form._root.update_idletasks()
        
        if countdown_value <= 0:
            timer.Stop()
            btn_show.Enabled = True
            btn_show.Text = 'Show Controls'
            lbl_countdown.Text = 'Countdown complete! Click the button to see controls.'
    
    timer.Tick = on_timer_tick
    # Don't start timer yet
    
    # List of controls to show
    controls_to_show = [
        ('Label', 'This is a Label'),
        ('TextBox', 'TextBox example'),
        ('Button', 'Sample Button'),
        ('CheckBox', 'CheckBox example'),
        ('RadioButton', 'RadioButton example'),
        ('ComboBox', ['Item 1', 'Item 2', 'Item 3']),
        ('ListBox', ['List Item 1', 'List Item 2', 'List Item 3']),
        ('Panel', 'Panel with Border'),
        ('GroupBox', 'GroupBox with controls')
    ]
    
    current_control_index = 0
    left_column_y = 140  # Posición Y para la columna izquierda
    right_column_y = 140  # Posición Y para la columna derecha
    
    def on_button_click():
        nonlocal current_control_index, left_column_y, right_column_y, countdown_started, countdown_value
        if not countdown_started:
            # Start the countdown
            countdown_started = True
            countdown_value = 5  # Reset countdown
            progress.Value = 0
            lbl_countdown.Text = 'Time remaining: 5 seconds'
            btn_show.Enabled = False
            btn_show.Text = 'Countdown in progress...'
            timer.Start()
            return
        
        # Show controls logic
        if current_control_index < len(controls_to_show):
            control_name, control_value = controls_to_show[current_control_index]
            
            # Determinar si va en columna izquierda o derecha
            is_left_column = current_control_index % 2 == 0
            x_position = 20 if is_left_column else 250  # Columna izquierda: 20, derecha: 250
            y_position = left_column_y if is_left_column else right_column_y
            
            # Add a label above the control
            info_label = Label(form, {
                'Text': f'{current_control_index + 1}. {control_name}',
                'Left': x_position,
                'Top': y_position - 25,
                'Width': 200,
                'Font': ('Segoe UI', 10, 'bold')
            })
            
            # Create the control based on type
            if control_name == 'Label':
                control = Label(form, {'Text': control_value, 'Left': x_position, 'Top': y_position, 'Width': 200})
            elif control_name == 'TextBox':
                control = TextBox(form, {'Text': control_value, 'Left': x_position, 'Top': y_position, 'Width': 200})
            elif control_name == 'Button':
                control = Button(form, {'Text': control_value, 'Left': x_position, 'Top': y_position, 'Width': 150})
            elif control_name == 'CheckBox':
                control = CheckBox(form, {'Text': control_value, 'Left': x_position, 'Top': y_position})
            elif control_name == 'RadioButton':
                control = RadioButton(form, {'Text': control_value, 'Left': x_position, 'Top': y_position})
            elif control_name == 'ComboBox':
                control = ComboBox(form, {'Left': x_position, 'Top': y_position, 'Width': 200, 'Items': control_value})
            elif control_name == 'ListBox':
                control = ListBox(form, {'Left': x_position, 'Top': y_position, 'Width': 200, 'Height': 80, 'Items': control_value})
            elif control_name == 'Panel':
                control = Panel(form, {'Left': x_position, 'Top': y_position, 'Width': 200, 'Height': 80, 'BackColor': 'lightblue', 'Text': control_value, 'BorderStyle': 'Fixed3D'})
                # Add a RadioButton inside the panel
                inner_radiobutton = RadioButton(control, {'Text': 'RadioButton inside Panel', 'Left': 10, 'Top': 10, 'Width': 180})
                control.AddControl(inner_radiobutton)
            elif control_name == 'GroupBox':
                control = GroupBox(form, {'Left': x_position, 'Top': y_position, 'Width': 200, 'Height': 80, 'Text': control_value})
                # Add controls inside the GroupBox
                inner_checkbox = CheckBox(control, {'Text': 'Option inside GroupBox', 'Left': 10, 'Top': 10, 'Width': 180})
                control.AddControl(inner_checkbox)
                inner_radiobutton = RadioButton(control, {'Text': 'Radio inside GroupBox', 'Left': 10, 'Top': 35, 'Width': 180})
                control.AddControl(inner_radiobutton)
            
            # Incrementar la posición Y de la columna correspondiente
            if is_left_column:
                left_column_y += 100  # Espacio para el siguiente control en columna izquierda
            else:
                right_column_y += 100  # Espacio para el siguiente control en columna derecha
                
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