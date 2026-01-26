"""
Basic Controls Demo

This example demonstrates basic WinFormPy controls with countdown timer:

- Line (separators)
- Timer (countdown functionality)
- ProgressBar (visual feedback)
- Button (actions and interactions)
- Label (text display)
- TextBox (text input)
- RadioButton (single choice selection)
- ComboBox (dropdown selection)
- CheckBox (multiple choice selection)
"""

from winformpy import (
    Form, Label, Button, TextBox, CheckBox, RadioButton,
    ComboBox, ProgressBar, Timer, Line, Panel,
    Font, FontStyle
)


def main():
    # =========================================================================
    # Create main form
    # =========================================================================
    form = Form({
        'Text': 'Basic Controls Demo',
        'Width': 720,
        'Height': 620,
        'StartPosition': 'CenterScreen',
        'BackColor': '#FFFFFF'
    })
    
    # =========================================================================
    # Title Panel
    # =========================================================================
    title_panel = Panel(form, {
        'Left': 0,
        'Top': 0,
        'Width': 720,
        'Height': 50,
        'BackColor': '#0078D4'
    })
    
    title_label = Label(title_panel, {
        'Text': 'Basic Controls Demo',
        'Left': 20,
        'Top': 12,
        'AutoSize': True,
        'Font': Font('Segoe UI', 16, FontStyle.Bold),
        'ForeColor': '#FFFFFF',
        'BackColor': '#0078D4'
    })
    
    # =========================================================================
    # COUNTDOWN SECTION
    # =========================================================================
    
    # Horizontal line separator
    line1 = Line(form, {
        'Left': 20,
        'Top': 60,
        'Width': 660,
        'Height': 5,
        'BackColor': '#0078D4'
    })
    
    # Countdown label
    lbl_countdown = Label(form, {
        'Text': 'Initializing... 5 seconds',
        'Left': 20,
        'Top': 75,
        'Width': 400,
        'Height': 25,
        'Font': Font('Segoe UI', 12, FontStyle.Bold),
        'ForeColor': '#D83B01',
        'BackColor': '#FFFACD'
    })
    
    # Progress bar
    progress = ProgressBar(form, {
        'Left': 20,
        'Top': 105,
        'Width': 660,
        'Height': 25,
        'Maximum': 5,
        'Value': 0
    })
    
    # Timer for countdown
    countdown_value = [5]
    timer = Timer(form, {'Interval': 1000})
    
    # Button initially disabled
    btn_continue = Button(form, {
        'Text': 'Please wait...',
        'Left': 20,
        'Top': 140,
        'Width': 150,
        'Height': 35,
        'Enabled': False,
        'Font': Font('Segoe UI', 10)
    })
    
    # =========================================================================
    # CONTROLS DEMONSTRATION SECTION
    # =========================================================================
    
    # Section separator
    line2 = Line(form, {
        'Left': 20,
        'Top': 190,
        'Width': 660,
        'Height': 1,
        'BackColor': '#000000'
    })
    
    lbl_section = Label(form, {
        'Text': 'Control Examples',
        'Left': 20,
        'Top': 200,
        'Width': 300,
        'Font': Font('Segoe UI', 12, FontStyle.Bold),
        'ForeColor': '#000000'
    })
    
    # -------------------------------------------------------------------------
    # 1. TextBox example
    # -------------------------------------------------------------------------
    lbl_textbox = Label(form, {
        'Text': '1. TextBox - Enter your name:',
        'Left': 20,
        'Top': 235,
        'Width': 200,
        'ForeColor': '#000000'
    })
    
    txt_name = TextBox(form, {
        'Text': 'Enter your name here',
        'Left': 230,
        'Top': 232,
        'Width': 250,
        'Height': 25,
        'SelectAllOnClick': True
    })
    
    lbl_result = Label(form, {
        'Text': 'Type something...',
        'Left': 490,
        'Top': 235,
        'Width': 180,
        'ForeColor': '#107C10'
    })
    
    def on_textbox_changed(sender=None, e=None):
        text = txt_name.Text
        if text:
            lbl_result.Text = f'Hello, {text}!'
        else:
            lbl_result.Text = 'Type something...'
    
    txt_name.TextChanged = on_textbox_changed
    
    # -------------------------------------------------------------------------
    # 2. CheckBox example
    # -------------------------------------------------------------------------
    lbl_checkbox = Label(form, {
        'Text': '2. CheckBox - Select options:',
        'Left': 20,
        'Top': 275,
        'Width': 200,
        'ForeColor': '#000000'
    })
    
    chk_option1 = CheckBox(form, {
        'Text': 'Option A',
        'Left': 230,
        'Top': 273,
        'Width': 100,
        'Checked': False
    })
    
    chk_option2 = CheckBox(form, {
        'Text': 'Option B',
        'Left': 340,
        'Top': 273,
        'Width': 100,
        'Checked': True
    })
    
    lbl_checkbox_result = Label(form, {
        'Text': 'B selected',
        'Left': 450,
        'Top': 275,
        'Width': 220,
        'ForeColor': '#8764B8'
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
            lbl_checkbox_result.Text = 'None selected'
    
    chk_option1.CheckedChanged = update_checkbox_result
    chk_option2.CheckedChanged = update_checkbox_result
    
    # -------------------------------------------------------------------------
    # 3. RadioButton example
    # -------------------------------------------------------------------------
    lbl_radio = Label(form, {
        'Text': '3. RadioButton - Choose one:',
        'Left': 20,
        'Top': 315,
        'Width': 200,
        'ForeColor': '#000000'
    })
    
    radio1 = RadioButton(form, {
        'Text': 'Red',
        'Left': 230,
        'Top': 313,
        'Width': 80,
        'Checked': True
    })
    
    radio2 = RadioButton(form, {
        'Text': 'Blue',
        'Left': 320,
        'Top': 313,
        'Width': 80,
        'Checked': False
    })
    
    radio3 = RadioButton(form, {
        'Text': 'Green',
        'Left': 410,
        'Top': 313,
        'Width': 80,
        'Checked': False
    })
    
    lbl_radio_result = Label(form, {
        'Text': 'Color: Red',
        'Left': 500,
        'Top': 315,
        'Width': 170,
        'ForeColor': '#FF0000'
    })
    
    def on_radio_changed(sender=None, e=None):
        if radio1.Checked:
            lbl_radio_result.Text = 'Color: Red'
            lbl_radio_result.ForeColor = '#FF0000'
        elif radio2.Checked:
            lbl_radio_result.Text = 'Color: Blue'
            lbl_radio_result.ForeColor = '#0000FF'
        elif radio3.Checked:
            lbl_radio_result.Text = 'Color: Green'
            lbl_radio_result.ForeColor = '#008000'
    
    radio1.CheckedChanged = on_radio_changed
    radio2.CheckedChanged = on_radio_changed
    radio3.CheckedChanged = on_radio_changed
    
    # -------------------------------------------------------------------------
    # 4. ComboBox example
    # -------------------------------------------------------------------------
    lbl_combo = Label(form, {
        'Text': '4. ComboBox - Select a city:',
        'Left': 20,
        'Top': 355,
        'Width': 200,
        'ForeColor': '#000000'
    })
    
    combo_cities = ComboBox(form, {
        'Left': 230,
        'Top': 352,
        'Width': 200,
        'Items': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao']
    })
    combo_cities.SelectedIndex = 0
    
    lbl_combo_result = Label(form, {
        'Text': 'Selected: Madrid',
        'Left': 440,
        'Top': 355,
        'Width': 230,
        'ForeColor': '#FF8C00'
    })
    
    def on_combo_changed(sender=None, e=None):
        if combo_cities.SelectedItem:
            lbl_combo_result.Text = f'Selected: {combo_cities.SelectedItem}'
    
    combo_cities.SelectedIndexChanged = on_combo_changed
    
    # -------------------------------------------------------------------------
    # 5. Button example
    # -------------------------------------------------------------------------
    lbl_button = Label(form, {
        'Text': '5. Button - Click action:',
        'Left': 20,
        'Top': 395,
        'Width': 200,
        'ForeColor': '#000000'
    })
    
    click_count = [0]
    
    btn_action = Button(form, {
        'Text': 'Click Me!',
        'Left': 230,
        'Top': 390,
        'Width': 120,
        'Height': 35
    })
    
    lbl_button_result = Label(form, {
        'Text': 'Clicks: 0',
        'Left': 360,
        'Top': 395,
        'Width': 310,
        'ForeColor': '#008080'
    })
    
    def on_action_click(sender=None, e=None):
        click_count[0] += 1
        lbl_button_result.Text = f'Clicks: {click_count[0]} - Last clicked at {countdown_value[0]}s remaining'
        btn_action.Text = f'Clicked {click_count[0]}x'
    
    btn_action.Click = on_action_click
    
    # =========================================================================
    # SUMMARY SECTION
    # =========================================================================
    
    # Separator line
    line3 = Line(form, {
        'Left': 20,
        'Top': 445,
        'Width': 660,
        'Height': 5,
        'BackColor': '#808080'
    })
    
    # Summary labels
    lbl_summary_title = Label(form, {
        'Text': 'Controls Demonstrated:',
        'Left': 20,
        'Top': 460,
        'Width': 660,
        'Font': Font('Segoe UI', 10, FontStyle.Bold),
        'ForeColor': '#000000'
    })
    
    lbl_summary = Label(form, {
        'Text': '✓ Line (separators)  ✓ Timer (countdown)  ✓ ProgressBar (visual feedback)\n' +
                '✓ Button (actions)  ✓ Label (text display)  ✓ TextBox (text input)\n' +
                '✓ RadioButton (single choice)  ✓ ComboBox (dropdown)  ✓ CheckBox (multiple choice)',
        'Left': 20,
        'Top': 485,
        'Width': 660,
        'Height': 80,
        'Font': Font('Segoe UI', 9),
        'ForeColor': '#000000'
    })
    
    # =========================================================================
    # Event Handlers
    # =========================================================================
    
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
            lbl_countdown.ForeColor = '#107C10'
            lbl_countdown.BackColor = '#90EE90'
            progress.Value = 5
    
    timer.Tick = on_timer_tick
    
    # Start timer automatically when form loads
    def on_form_load(sender=None, e=None):
        timer.Start()
    
    form.Load = on_form_load
    
    # Continue button click (just for demonstration)
    def on_continue_click(sender=None, e=None):
        txt_name.Text = 'Demo User'
        combo_cities.SelectedIndex = 2  # Valencia
        on_textbox_changed()
        on_combo_changed()
    
    btn_continue.Click = on_continue_click
    
    # =========================================================================
    # Show the form
    # =========================================================================
    form.Show()


if __name__ == '__main__':
    main()