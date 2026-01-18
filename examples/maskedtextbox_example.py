"""
Complete MaskedTextBox Implementation Example - WinFormPy
Demonstrates various mask formats and validation scenarios
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
MaskedTextBox = winform_py.MaskedTextBox
ComboBox = winform_py.ComboBox
CheckBox = winform_py.CheckBox
GroupBox = winform_py.GroupBox
ToolTip = winform_py.ToolTip


def main():
    # Create main form
    form = Form()
    form.Text = "MaskedTextBox Complete Demo - WinFormPy"
    form.Width = 700
    form.Height = 710
    form.StartPosition = "CenterScreen"
    form.BackColor = "whitesmoke"
    
    # ===== TITLE SECTION =====
    lbl_title = Label(form, {
        'Text': 'MaskedTextBox Control Demonstration',
        'Left': 20,
        'Top': 15,
        'Width': 650,
        'Height': 30,
        'Font': ('Segoe UI', 16, 'bold'),
        'ForeColor': 'darkblue'
    })
    
    # ===== MASK SELECTOR SECTION =====
    lbl_select = Label(form, {
        'Text': 'Select Mask Format:',
        'Left': 20,
        'Top': 55,
        'Width': 150,
        'Font': ('Segoe UI', 10, 'bold')
    })
    
    # Dictionary of available masks
    masks = {
        'Phone (US)': '(000) 000-0000',
        'Phone (Int)': '+00 (000) 000-0000',
        'SSN': '000-00-0000',
        'Password (8 chars)': '&&&&&&&&',
        'Date (MM/DD/YYYY)': '00/00/0000',
        'Date (DD/MM/YYYY)': '00/00/0000',
        'Date (ISO)': '0000-00-00',
        'Time (HH:MM)': '00:00',
        'Time (HH:MM:SS)': '00:00:00',
        'ZIP Code': '00000',
        'ZIP+4': '00000-9999',
        'Credit Card': '0000-0000-0000-0000',
        'Product Code': '>LLL-000',
        'Serial Number': '>AAAA-AAAA-AAAA',
        'IP Address': '000.000.000.000',
        'MAC Address': '>AA:AA:AA:AA:AA:AA',
        'Currency': '$0,000.00',
        'Email Prefix': '<llllllll',
        'License Plate': '>LLL-0000',
    }
    
    # Mask descriptions
    mask_descriptions = {
        'Phone (US)': 'Standard US phone: (555) 123-4567',
        'Phone (Int)': 'International: +1 (555) 123-4567',
        'SSN': 'Social Security: 123-45-6789',
        'Password (8 chars)': 'Password: 8 required characters',
        'Date (MM/DD/YYYY)': 'US date format: 12/09/2025',
        'Date (DD/MM/YYYY)': 'European date: 09/12/2025',
        'Date (ISO)': 'ISO format: 2025-12-09',
        'Time (HH:MM)': '24-hour time: 14:30',
        'Time (HH:MM:SS)': 'Full time: 14:30:45',
        'ZIP Code': 'Basic ZIP: 12345',
        'ZIP+4': 'Extended ZIP: 12345-6789',
        'Credit Card': 'Card number: 1234-5678-9012-3456',
        'Product Code': 'Uppercase code: ABC-123',
        'Serial Number': 'Alphanumeric: AB12-CD34-EF56',
        'IP Address': 'IPv4: 192.168.001.001',
        'MAC Address': 'Network MAC: 1A:2B:3C:4D:5E:6F',
        'Currency': 'Money format: $1,234.56',
        'Email Prefix': 'Lowercase: username',
        'License Plate': 'Vehicle plate: ABC-1234',
    }
    
    # ComboBox for mask selection
    combo_mask = ComboBox(form, {
        'Left': 175,
        'Top': 52,
        'Width': 250,
        'Items': list(masks.keys())
    })
    combo_mask.SelectedIndex = 0
    
    # ===== INPUT SECTION =====
    lbl_input = Label(form, {
        'Text': 'Enter Data:',
        'Left': 20,
        'Top': 95,
        'Width': 150,
        'Font': ('Segoe UI', 10, 'bold')
    })
    
    # MaskedTextBox - main control
    txt_masked = MaskedTextBox(form, {
        'Mask': masks['Phone (US)'],
        'Left': 175,
        'Top': 92,
        'Width': 300,
        'Height': 25,
        'Font': ('Courier New', 11),
        'PromptChar': '_',
        'BeepOnError': False
    })
    
    # ===== INFO DISPLAY =====
    lbl_mask_info = Label(form, {
        'Text': f"Mask Pattern: {masks['Phone (US)']}",
        'Left': 175,
        'Top': 125,
        'Width': 500,
        'Font': ('Consolas', 9),
        'ForeColor': 'blue'
    })
    
    lbl_description = Label(form, {
        'Text': mask_descriptions['Phone (US)'],
        'Left': 175,
        'Top': 145,
        'Width': 500,
        'Font': ('Segoe UI', 9, 'italic'),
        'ForeColor': 'darkgreen'
    })
    
    # ===== STATUS SECTION =====
    lbl_status = Label(form, {
        'Text': 'Status: Empty',
        'Left': 175,
        'Top': 175,
        'Width': 500,
        'Height': 25,
        'Font': ('Segoe UI', 10),
        'ForeColor': 'gray'
    })
    
    lbl_completion = Label(form, {
        'Text': 'Required: ☐  |  All Filled: ☐',
        'Left': 175,
        'Top': 200,
        'Width': 500,
        'Font': ('Segoe UI', 9)
    })
    
    # ===== OPTIONS SECTION =====
    lbl_options_help = Label(form, {
        'Text': 'Configure MaskedTextBox behavior. Select options and click "Apply Options" to update settings.',
        'Left': 20,
        'Top': 240,
        'Width': 650,
        'Height': 30,
        'Font': ('Segoe UI', 9, 'italic'),
        'ForeColor': 'darkblue'
    })
    
    # Separator line
    from winformpy import Line
    Line = winform_py.Line
    
    line_top = Line(form, {
        'Left': 20,
        'Top': 275,
        'Width': 650,
        'Height': 2,
        'BackColor': 'darkgray'
    })
    
    lbl_options_title = Label(form, {
        'Text': 'Options:',
        'Left': 20,
        'Top': 285,
        'Width': 150,
        'Font': ('Segoe UI', 10, 'bold')
    })
    
    chk_beep = CheckBox(form, {
        'Text': 'Beep on Error',
        'Left': 20,
        'Top': 310,
        'Width': 150,
        'Checked': False
    })
    ToolTip(chk_beep, {
        'Text': 'Play a beep sound when invalid input is entered',
        'UseSystemStyles': True
    })
    

    
    chk_password = CheckBox(form, {
        'Text': 'Password Mode (*)',
        'Left': 370,
        'Top': 310,
        'Width': 180,
        'Checked': False
    })
    ToolTip(chk_password, {
        'Text': 'Display all characters as asterisks (*) for password entry',
        'UseSystemStyles': True
    })
    
    chk_ascii = CheckBox(form, {
        'Text': 'ASCII Only',
        'Left': 20,
        'Top': 340,
        'Width': 150,
        'Checked': False
    })
    ToolTip(chk_ascii, {
        'Text': 'Reject non-ASCII characters (ñ, á, ü, etc.)',
        'UseSystemStyles': True
    })
    
    chk_skip_literals = CheckBox(form, {
        'Text': 'Skip Literals',
        'Left': 180,
        'Top': 340,
        'Width': 180,
        'Checked': True
    })
    ToolTip(chk_skip_literals, {
        'Text': 'Automatically skip over literal characters (/, -, spaces) when typing',
        'UseSystemStyles': True
    })
    
    lbl_prompt_char = Label(form, {
        'Text': 'Prompt Char:',
        'Left': 370,
        'Top': 343,
        'Width': 90
    })
    ToolTip(lbl_prompt_char, {
        'Text': 'Character used to indicate empty positions in the mask',
        'UseSystemStyles': True
    })
    
    combo_prompt = ComboBox(form, {
        'Left': 465,
        'Top': 340,
        'Width': 60,
        'Items': ['_', '-', '*', '•', ' ']
    })
    combo_prompt.SelectedIndex = 0
    ToolTip(combo_prompt, {
        'Text': 'Select the prompt character to display for unfilled positions',
        'UseSystemStyles': True
    })
    
    btn_apply_options = Button(form, {
        'Text': 'Apply Options',
        'Left': 20,
        'Top': 375,
        'Width': 120,
        'Height': 25
    })
    
    # Separator line bottom
    line_bottom = Line(form, {
        'Left': 20,
        'Top': 410,
        'Width': 650,
        'Height': 2,
        'BackColor': 'darkgray'
    })
    
    # ===== RESULT SECTION =====
    lbl_result_title = Label(form, {
        'Text': 'Text Output:',
        'Left': 20,
        'Top': 425,
        'Width': 150,
        'Font': ('Segoe UI', 10, 'bold')
    })
    
    lbl_text_value = Label(form, {
        'Text': 'Text: (empty)',
        'Left': 175,
        'Top': 425,
        'Width': 500,
        'Font': ('Courier New', 9),
        'ForeColor': 'darkblue'
    })
    
    lbl_text_no_prompt = Label(form, {
        'Text': 'Without Prompts: (empty)',
        'Left': 175,
        'Top': 445,
        'Width': 500,
        'Font': ('Courier New', 9),
        'ForeColor': 'darkgreen'
    })
    
    lbl_text_no_literals = Label(form, {
        'Text': 'Without Literals: (empty)',
        'Left': 175,
        'Top': 465,
        'Width': 500,
        'Font': ('Courier New', 9),
        'ForeColor': 'darkorange'
    })
    
    # ===== VALIDATION SECTION =====
    lbl_validation_title = Label(form, {
        'Text': 'Validation:',
        'Left': 20,
        'Top': 500,
        'Width': 150,
        'Font': ('Segoe UI', 10, 'bold')
    })
    
    lbl_validation_result = Label(form, {
        'Text': '',
        'Left': 175,
        'Top': 500,
        'Width': 500,
        'Height': 60,
        'Font': ('Segoe UI', 9),
        'ForeColor': 'black'
    })
    
    # ===== ACTION BUTTONS =====
    btn_validate = Button(form, {
        'Text': 'Validate',
        'Left': 20,
        'Top': 555,
        'Width': 100,
        'Height': 30
    })
    
    btn_clear = Button(form, {
        'Text': 'Clear',
        'Left': 130,
        'Top': 555,
        'Width': 100,
        'Height': 30
    })
    
    btn_set_sample = Button(form, {
        'Text': 'Set Sample Data',
        'Left': 240,
        'Top': 555,
        'Width': 120,
        'Height': 30
    })
    
    btn_copy = Button(form, {
        'Text': 'Copy Text',
        'Left': 370,
        'Top': 555,
        'Width': 100,
        'Height': 30
    })
    
    # ===== EVENT HANDLERS =====
    
    def update_status():
        """Update status labels based on current text"""
        text = txt_masked.Text
        
        # Status message
        if not text or text.replace('_', '').replace('-', '').replace('(', '').replace(')', '').replace(' ', '').strip() == '':
            lbl_status.Text = "Status: Empty"
            lbl_status.ForeColor = 'gray'
        elif txt_masked.MaskFull:
            lbl_status.Text = "Status: Complete (all positions filled)"
            lbl_status.ForeColor = 'green'
        elif txt_masked.MaskCompleted:
            lbl_status.Text = "Status: Valid (required positions filled)"
            lbl_status.ForeColor = 'darkgreen'
        else:
            lbl_status.Text = "Status: Incomplete (fill required positions)"
            lbl_status.ForeColor = 'orange'
        
        # Completion indicators
        completed_check = '☑' if txt_masked.MaskCompleted else '☐'
        full_check = '☑' if txt_masked.MaskFull else '☐'
        lbl_completion.Text = f'Required: {completed_check}  |  All Filled: {full_check}'
        
        # Text outputs (simulated different formats)
        lbl_text_value.Text = f"Text: {text if text else '(empty)'}"
        
        # Remove prompts
        text_no_prompt = text.replace('_', '') if text else ''
        lbl_text_no_prompt.Text = f"Without Prompts: {text_no_prompt if text_no_prompt else '(empty)'}"
        
        # Remove literals (simplified - removes common separators)
        text_no_literals = text.replace('(', '').replace(')', '').replace('-', '').replace('/', '').replace(':', '').replace(' ', '').replace('_', '') if text else ''
        lbl_text_no_literals.Text = f"Without Literals: {text_no_literals if text_no_literals else '(empty)'}"
    
    def on_mask_changed(sender=None, e=None):
        """Handle mask selection change"""
        selected = combo_mask.SelectedItem
        if selected and selected in masks:
            txt_masked.Mask = masks[selected]
            lbl_mask_info.Text = f"Mask Pattern: {masks[selected]}"
            lbl_description.Text = mask_descriptions[selected]
            update_status()
    
    def on_text_changed(sender=None, e=None):
        """Handle text input changes"""
        update_status()
    
    def on_input_rejected(sender=None, e=None):
        """Handle invalid input rejection"""
        lbl_validation_result.Text = "⚠ Invalid character entered!\nThe character doesn't match the mask pattern."
        lbl_validation_result.ForeColor = 'red'
        form.SetTimeout(lambda: setattr(lbl_validation_result, 'Text', ''), 2000)
    
    def on_apply_options(sender=None, e=None):
        """Apply selected options to MaskedTextBox"""
        # Apply behavior options
        txt_masked.BeepOnError = chk_beep.Checked
        txt_masked.AsciiOnly = chk_ascii.Checked
        txt_masked.SkipLiterals = chk_skip_literals.Checked
        
        # Apply prompt char (setter handles visual update)
        prompt_char = combo_prompt.SelectedItem
        if prompt_char:
            txt_masked.PromptChar = prompt_char
        
        # Apply password char
        if chk_password.Checked:
            txt_masked.PasswordChar = '*'
        else:
            txt_masked.PasswordChar = None
        
        lbl_validation_result.Text = "✓ Options applied successfully!"
        lbl_validation_result.ForeColor = 'green'
        form.SetTimeout(lambda: setattr(lbl_validation_result, 'Text', ''), 2000)
    
    def on_validate(sender=None, e=None):
        """Validate current input"""
        if txt_masked.MaskCompleted:
            lbl_validation_result.Text = f"✓ Valid Input!\n{txt_masked.Text}"
            lbl_validation_result.ForeColor = 'green'
        else:
            lbl_validation_result.Text = "✗ Incomplete Input\nPlease fill all required positions."
            lbl_validation_result.ForeColor = 'red'
    
    def on_clear(sender=None, e=None):
        """Clear the input"""
        txt_masked.Text = ""
        update_status()
        lbl_validation_result.Text = ""
    
    def on_set_sample(sender=None, e=None):
        """Set sample data based on current mask"""
        selected = combo_mask.SelectedItem
        samples = {
            'Phone (US)': '5551234567',
            'Phone (Int)': '15551234567',
            'SSN': '123456789',
            'Password (8 chars)': 'Pass1234',
            'Date (MM/DD/YYYY)': '12092025',
            'Date (DD/MM/YYYY)': '09122025',
            'Date (ISO)': '20251209',
            'Time (HH:MM)': '1430',
            'Time (HH:MM:SS)': '143045',
            'ZIP Code': '12345',
            'ZIP+4': '123456789',
            'Credit Card': '1234567890123456',
            'Product Code': 'ABC123',
            'Serial Number': 'AB12CD34EF56',
            'IP Address': '192168001001',
            'MAC Address': '1A2B3C4D5E6F',
            'Currency': '123456',
            'Email Prefix': 'username',
            'License Plate': 'ABC1234',
        }
        
        if selected in samples:
            txt_masked.Text = samples[selected]
            update_status()
    
    def on_copy(sender=None, e=None):
        """Copy text to clipboard"""
        text = txt_masked.Text
        if text:
            try:
                form.SetClipboard(text)
                lbl_validation_result.Text = "✓ Text copied to clipboard!"
                lbl_validation_result.ForeColor = 'blue'
                form.SetTimeout(lambda: setattr(lbl_validation_result, 'Text', ''), 2000)
            except:
                lbl_validation_result.Text = "✗ Failed to copy to clipboard"
                lbl_validation_result.ForeColor = 'red'
    
    # Bind events
    combo_mask.SelectedIndexChanged = on_mask_changed
    txt_masked.TextChanged = on_text_changed
    txt_masked.MaskInputRejected = on_input_rejected
    btn_apply_options.Click = on_apply_options
    btn_validate.Click = on_validate
    btn_clear.Click = on_clear
    btn_set_sample.Click = on_set_sample
    btn_copy.Click = on_copy
    
    # ===== FOOTER INFO =====
    lbl_footer = Label(form, {
        'Text': 'Mask Characters: 0=digit(req), 9=digit(opt), L=letter(req), ?=letter(opt), A=alnum(req), a=alnum(opt)',
        'Left': 20,
        'Top': 620,
        'Width': 650,
        'Height': 20,
        'Font': ('Segoe UI', 8),
        'ForeColor': 'black'
    })
    
    lbl_footer2 = Label(form, {
        'Text': '&=char(req), C=char(opt), <=lowercase, >=uppercase',
        'Left': 20,
        'Top': 640,
        'Width': 650,
        'Height': 20,
        'Font': ('Segoe UI', 8),
        'ForeColor': 'black'
    })
    
    # Initial status update
    update_status()
    
    form.Show()


if __name__ == "__main__":
    main()
