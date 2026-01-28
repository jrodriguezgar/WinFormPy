"""
Professional Form Example - Best Practices UX/UI
=================================================

This example demonstrates best practices for creating professional forms:
- Zero overlapping: Strict Dock/Anchor layout system
- Proportional sizing: Responsive widgets
- Consistent padding/spacing: Professional appearance
- Type-appropriate controls: Right widget for each data type
- Strict typing: Controls match expected data types
- Validation: Input validation before processing

Form includes:
- Text fields (string)
- Numeric fields (int, float)
- Date selection (datetime)
- Boolean toggles (bool)
- Selection from list (enum)
- Multi-line text (string)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from winformpy.winformpy import (
    Form, Panel, Label, TextBox, Button, CheckBox, ComboBox,
    NumericUpDown, DateTimePicker, RadioButton, GroupBox,
    DockStyle, AnchorStyles, MessageBox, DialogResult, Font, FontStyle
)
from datetime import datetime
from decimal import Decimal, InvalidOperation


class FieldValidator:
    """Utility class for field validation with strict typing."""
    
    @staticmethod
    def validate_required(value, field_name):
        """Validate that a required field is not empty."""
        if not value or (isinstance(value, str) and not value.strip()):
            raise ValueError(f"{field_name} is required")
        return True
    
    @staticmethod
    def validate_string(value, field_name, min_length=None, max_length=None):
        """Validate string field."""
        FieldValidator.validate_required(value, field_name)
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")
        
        value = value.strip()
        if min_length and len(value) < min_length:
            raise ValueError(f"{field_name} must be at least {min_length} characters")
        if max_length and len(value) > max_length:
            raise ValueError(f"{field_name} must not exceed {max_length} characters")
        
        return value
    
    @staticmethod
    def validate_integer(value, field_name, min_value=None, max_value=None):
        """Validate integer field."""
        try:
            int_value = int(value)
            if min_value is not None and int_value < min_value:
                raise ValueError(f"{field_name} must be at least {min_value}")
            if max_value is not None and int_value > max_value:
                raise ValueError(f"{field_name} must not exceed {max_value}")
            return int_value
        except (ValueError, TypeError) as e:
            raise ValueError(f"{field_name} must be a valid integer") from e
    
    @staticmethod
    def validate_decimal(value, field_name, min_value=None, max_value=None, decimals=2):
        """Validate decimal/float field."""
        try:
            decimal_value = Decimal(str(value)).quantize(Decimal(10) ** -decimals)
            if min_value is not None and decimal_value < Decimal(str(min_value)):
                raise ValueError(f"{field_name} must be at least {min_value}")
            if max_value is not None and decimal_value > Decimal(str(max_value)):
                raise ValueError(f"{field_name} must not exceed {max_value}")
            return float(decimal_value)
        except (InvalidOperation, ValueError, TypeError) as e:
            raise ValueError(f"{field_name} must be a valid decimal number") from e
    
    @staticmethod
    def validate_email(value, field_name):
        """Validate email format."""
        value = FieldValidator.validate_string(value, field_name)
        if '@' not in value or '.' not in value.split('@')[1]:
            raise ValueError(f"{field_name} must be a valid email address")
        return value
    
    @staticmethod
    def validate_date(value, field_name, min_date=None, max_date=None):
        """Validate date field."""
        if not isinstance(value, datetime):
            raise TypeError(f"{field_name} must be a datetime object")
        
        if min_date and value < min_date:
            raise ValueError(f"{field_name} must be after {min_date.strftime('%Y-%m-%d')}")
        if max_date and value > max_date:
            raise ValueError(f"{field_name} must be before {max_date.strftime('%Y-%m-%d')}")
        
        return value


class ProfessionalFormExample(Form):
    """
    Professional form with proper layout management and validation.
    
    Layout structure:
    - Header Panel (Dock.Top): Title and description
    - Content Panel (Dock.Fill): Scrollable form fields
    - Footer Panel (Dock.Bottom): Action buttons
    """
    
    # Constants for consistent spacing
    PADDING = 16
    FIELD_SPACING = 12
    LABEL_HEIGHT = 20
    INPUT_HEIGHT = 28
    BUTTON_HEIGHT = 36
    
    def __init__(self):
        super().__init__()
        self.Text = "Professional Registration Form"
        self.Width = 700
        self.Height = 800
        self.BackColor = '#F5F5F5'
        self.StartPosition = 'CenterScreen'
        
        # Apply layout before adding controls (CRITICAL for Dock)
        self.ApplyLayout()
        
        # Data storage
        self.form_data = {}
        
        # Create layout sections
        self._create_header()
        self._create_footer()
        self._create_content()
    
    def _create_header(self):
        """Create header section with title and description."""
        header = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 100,
            'BackColor': '#FFFFFF',
            'Padding': self.PADDING
        })
        
        # Title
        title = Label(header, {
            'Text': 'User Registration',
            'Font': Font('Segoe UI', 16, FontStyle.Bold),
            'ForeColor': '#2C3E50',
            'Left': self.PADDING,
            'Top': self.PADDING,
            'AutoSize': True
        })
        
        # Description
        description = Label(header, {
            'Text': 'Please fill out all required fields. Fields marked with * are mandatory.',
            'Font': Font('Segoe UI', 9),
            'ForeColor': '#7F8C8D',
            'Left': self.PADDING,
            'Top': self.PADDING + 35,
            'Width': 650,
            'Height': 40
        })
    
    def _create_footer(self):
        """Create footer section with action buttons."""
        footer = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': 70,
            'BackColor': '#FFFFFF',
            'Padding': self.PADDING
        })
        
        # Submit button
        self.btn_submit = Button(footer, {
            'Text': 'Submit',
            'Width': 120,
            'Height': self.BUTTON_HEIGHT,
            'Anchor': AnchorStyles.Bottom | AnchorStyles.Right,
            'BackColor': '#3498DB',
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 10, FontStyle.Bold)
        })
        self.btn_submit.Left = footer.Width - self.PADDING - 120
        self.btn_submit.Top = self.PADDING
        self.btn_submit.Click = self._on_submit
        
        # Cancel button
        self.btn_cancel = Button(footer, {
            'Text': 'Cancel',
            'Width': 120,
            'Height': self.BUTTON_HEIGHT,
            'Anchor': AnchorStyles.Bottom | AnchorStyles.Right,
            'BackColor': '#95A5A6',
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 10)
        })
        self.btn_cancel.Left = footer.Width - self.PADDING - 260
        self.btn_cancel.Top = self.PADDING
        self.btn_cancel.Click = lambda s, e: self.Close()
        
        # Clear button
        self.btn_clear = Button(footer, {
            'Text': 'Clear Form',
            'Width': 120,
            'Height': self.BUTTON_HEIGHT,
            'Anchor': AnchorStyles.Bottom | AnchorStyles.Left,
            'BackColor': '#E74C3C',
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 10)
        })
        self.btn_clear.Left = self.PADDING
        self.btn_clear.Top = self.PADDING
        self.btn_clear.Click = self._on_clear
    
    def _create_content(self):
        """Create scrollable content area with form fields."""
        # Main content panel (fills remaining space)
        content = Panel(self, {
            'Dock': DockStyle.Fill,
            'BackColor': '#F5F5F5',
            'AutoScroll': True,
            'Padding': self.PADDING
        })
        
        # Inner panel to hold all fields with proper spacing
        inner = Panel(content, {
            'Left': self.PADDING,
            'Top': self.PADDING,
            'Width': 640,
            'Height': 1000,  # Will expand as needed
            'BackColor': '#F5F5F5'
        })
        
        y_position = 0
        
        # Section 1: Personal Information
        y_position = self._create_section(inner, "Personal Information", y_position)
        
        # Full Name (String, required, 2-100 chars)
        self.txt_fullname, y_position = self._create_text_field(
            inner, "Full Name *", y_position, "Enter your full name"
        )
        
        # Email (String, required, email format)
        self.txt_email, y_position = self._create_text_field(
            inner, "Email Address *", y_position, "example@email.com"
        )
        
        # Age (Integer, 18-120)
        self.num_age, y_position = self._create_numeric_field(
            inner, "Age *", y_position, min_val=18, max_val=120, default_val=25
        )
        
        # Birth Date (Date, not in future)
        self.dtp_birthdate, y_position = self._create_date_field(
            inner, "Birth Date *", y_position
        )
        
        y_position += self.FIELD_SPACING
        
        # Section 2: Account Information
        y_position = self._create_section(inner, "Account Information", y_position)
        
        # Username (String, required, 4-20 chars)
        self.txt_username, y_position = self._create_text_field(
            inner, "Username *", y_position, "Choose a username"
        )
        
        # Account Type (ComboBox - enum/selection)
        self.cmb_account_type, y_position = self._create_dropdown_field(
            inner, "Account Type *", y_position,
            ['Personal', 'Business', 'Enterprise', 'Educational']
        )
        
        # Monthly Budget (Decimal, 0-1000000)
        self.num_budget, y_position = self._create_decimal_field(
            inner, "Monthly Budget (USD)", y_position, min_val=0, max_val=1000000, default_val=1000
        )
        
        y_position += self.FIELD_SPACING
        
        # Section 3: Preferences
        y_position = self._create_section(inner, "Preferences", y_position)
        
        # Newsletter (Boolean)
        self.chk_newsletter, y_position = self._create_checkbox_field(
            inner, "Subscribe to newsletter", y_position
        )
        
        # Terms & Conditions (Boolean, required)
        self.chk_terms, y_position = self._create_checkbox_field(
            inner, "I agree to the Terms and Conditions *", y_position
        )
        
        # Notification Method (Radio buttons - enum)
        self.radio_group, y_position = self._create_radio_group(
            inner, "Preferred Notification Method *", y_position,
            ['Email', 'SMS', 'Push Notification', 'None']
        )
        
        y_position += self.FIELD_SPACING
        
        # Section 4: Additional Information
        y_position = self._create_section(inner, "Additional Information", y_position)
        
        # Bio/Comments (Multi-line string, optional)
        self.txt_bio, y_position = self._create_multiline_field(
            inner, "Bio (Optional)", y_position, "Tell us about yourself..."
        )
    
    def _create_section(self, parent, title, y_pos):
        """Create a section header."""
        label = Label(parent, {
            'Text': title,
            'Font': Font('Segoe UI', 12, FontStyle.Bold),
            'ForeColor': '#2C3E50',
            'Left': 0,
            'Top': y_pos,
            'Width': 620,
            'Height': 30,
            'BackColor': '#ECF0F1'
        })
        
        return y_pos + 35
    
    def _create_text_field(self, parent, label_text, y_pos, placeholder=""):
        """Create a labeled text input field."""
        # Label
        lbl = Label(parent, {
            'Text': label_text,
            'Left': 0,
            'Top': y_pos,
            'Width': 200,
            'Height': self.LABEL_HEIGHT,
            'Font': Font('Segoe UI', 9)
        })
        
        # TextBox
        txt = TextBox(parent, {
            'Left': 210,
            'Top': y_pos - 2,
            'Width': 410,
            'Height': self.INPUT_HEIGHT,
            'Font': Font('Segoe UI', 9)
        })
        txt.Text = placeholder
        txt.ForeColor = '#95A5A6'
        
        # Clear placeholder on focus
        def on_focus(s, e):
            if txt.Text == placeholder:
                txt.Text = ""
                txt.ForeColor = '#000000'
        
        txt.GotFocus = on_focus
        
        return txt, y_pos + self.INPUT_HEIGHT + self.FIELD_SPACING
    
    def _create_numeric_field(self, parent, label_text, y_pos, min_val=0, max_val=100, default_val=0):
        """Create a labeled numeric input field (integer)."""
        # Label
        lbl = Label(parent, {
            'Text': label_text,
            'Left': 0,
            'Top': y_pos,
            'Width': 200,
            'Height': self.LABEL_HEIGHT,
            'Font': Font('Segoe UI', 9)
        })
        
        # NumericUpDown
        num = NumericUpDown(parent, {
            'Left': 210,
            'Top': y_pos - 2,
            'Width': 150,
            'Height': self.INPUT_HEIGHT,
            'Minimum': min_val,
            'Maximum': max_val,
            'Value': default_val,
            'Font': Font('Segoe UI', 9)
        })
        
        return num, y_pos + self.INPUT_HEIGHT + self.FIELD_SPACING
    
    def _create_decimal_field(self, parent, label_text, y_pos, min_val=0, max_val=100, default_val=0):
        """Create a labeled decimal input field (float)."""
        # Label
        lbl = Label(parent, {
            'Text': label_text,
            'Left': 0,
            'Top': y_pos,
            'Width': 200,
            'Height': self.LABEL_HEIGHT,
            'Font': Font('Segoe UI', 9)
        })
        
        # NumericUpDown with decimal places
        num = NumericUpDown(parent, {
            'Left': 210,
            'Top': y_pos - 2,
            'Width': 200,
            'Height': self.INPUT_HEIGHT,
            'Minimum': min_val,
            'Maximum': max_val,
            'Value': default_val,
            'DecimalPlaces': 2,
            'Increment': 10,
            'Font': Font('Segoe UI', 9)
        })
        
        # Add currency symbol
        currency_lbl = Label(parent, {
            'Text': '$',
            'Left': 190,
            'Top': y_pos,
            'Width': 15,
            'Height': self.LABEL_HEIGHT,
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'ForeColor': '#27AE60'
        })
        
        return num, y_pos + self.INPUT_HEIGHT + self.FIELD_SPACING
    
    def _create_date_field(self, parent, label_text, y_pos):
        """Create a labeled date picker field."""
        # Label
        lbl = Label(parent, {
            'Text': label_text,
            'Left': 0,
            'Top': y_pos,
            'Width': 200,
            'Height': self.LABEL_HEIGHT,
            'Font': Font('Segoe UI', 9)
        })
        
        # DateTimePicker
        dtp = DateTimePicker(parent, {
            'Left': 210,
            'Top': y_pos - 2,
            'Width': 250,
            'Height': self.INPUT_HEIGHT,
            'Format': 'Short',
            'Font': Font('Segoe UI', 9)
        })
        
        return dtp, y_pos + self.INPUT_HEIGHT + self.FIELD_SPACING
    
    def _create_dropdown_field(self, parent, label_text, y_pos, items):
        """Create a labeled dropdown/combobox field."""
        # Label
        lbl = Label(parent, {
            'Text': label_text,
            'Left': 0,
            'Top': y_pos,
            'Width': 200,
            'Height': self.LABEL_HEIGHT,
            'Font': Font('Segoe UI', 9)
        })
        
        # ComboBox
        cmb = ComboBox(parent, {
            'Left': 210,
            'Top': y_pos - 2,
            'Width': 300,
            'Height': self.INPUT_HEIGHT,
            'DropDownStyle': 'DropDownList',
            'Items': items,
            'Font': Font('Segoe UI', 9)
        })
        cmb.SelectedIndex = 0
        
        return cmb, y_pos + self.INPUT_HEIGHT + self.FIELD_SPACING
    
    def _create_checkbox_field(self, parent, label_text, y_pos):
        """Create a checkbox field."""
        chk = CheckBox(parent, {
            'Text': label_text,
            'Left': 0,
            'Top': y_pos,
            'Width': 620,
            'Height': 24,
            'Font': Font('Segoe UI', 9)
        })
        
        return chk, y_pos + 30
    
    def _create_radio_group(self, parent, label_text, y_pos, options):
        """Create a group of radio buttons."""
        # GroupBox
        group = GroupBox(parent, {
            'Text': label_text,
            'Left': 0,
            'Top': y_pos,
            'Width': 620,
            'Height': 30 + (len(options) * 30),
            'Font': Font('Segoe UI', 9)
        })
        
        # Radio buttons
        radio_buttons = []
        for i, option in enumerate(options):
            rb = RadioButton(group, {
                'Text': option,
                'Left': 10,
                'Top': 25 + (i * 30),
                'Width': 590,
                'Height': 24,
                'Font': Font('Segoe UI', 9)
            })
            radio_buttons.append(rb)
        
        # Select first option by default
        if radio_buttons:
            radio_buttons[0].Checked = True
        
        return radio_buttons, y_pos + group.Height + self.FIELD_SPACING
    
    def _create_multiline_field(self, parent, label_text, y_pos, placeholder=""):
        """Create a labeled multi-line text field."""
        # Label
        lbl = Label(parent, {
            'Text': label_text,
            'Left': 0,
            'Top': y_pos,
            'Width': 200,
            'Height': self.LABEL_HEIGHT,
            'Font': Font('Segoe UI', 9)
        })
        
        # Multi-line TextBox
        txt = TextBox(parent, {
            'Left': 0,
            'Top': y_pos + 25,
            'Width': 620,
            'Height': 100,
            'Multiline': True,
            'ScrollBars': 'Vertical',
            'Font': Font('Segoe UI', 9)
        })
        txt.Text = placeholder
        txt.ForeColor = '#95A5A6'
        
        # Clear placeholder on focus
        def on_focus(s, e):
            if txt.Text == placeholder:
                txt.Text = ""
                txt.ForeColor = '#000000'
        
        txt.GotFocus = on_focus
        
        return txt, y_pos + 130
    
    def _validate_form(self):
        """
        Validate all form fields with strict type checking.
        Returns tuple: (success: bool, errors: list)
        """
        errors = []
        
        try:
            # Validate Full Name (String, required, 2-100 chars)
            self.form_data['full_name'] = FieldValidator.validate_string(
                self.txt_fullname.Text, "Full Name", min_length=2, max_length=100
            )
        except ValueError as e:
            errors.append(str(e))
        
        try:
            # Validate Email (String, required, email format)
            self.form_data['email'] = FieldValidator.validate_email(
                self.txt_email.Text, "Email Address"
            )
        except ValueError as e:
            errors.append(str(e))
        
        try:
            # Validate Age (Integer, 18-120)
            self.form_data['age'] = FieldValidator.validate_integer(
                self.num_age.Value, "Age", min_value=18, max_value=120
            )
        except ValueError as e:
            errors.append(str(e))
        
        try:
            # Validate Birth Date (Date, not in future)
            self.form_data['birth_date'] = FieldValidator.validate_date(
                self.dtp_birthdate.Value, "Birth Date", max_date=datetime.now()
            )
        except ValueError as e:
            errors.append(str(e))
        
        try:
            # Validate Username (String, required, 4-20 chars)
            self.form_data['username'] = FieldValidator.validate_string(
                self.txt_username.Text, "Username", min_length=4, max_length=20
            )
        except ValueError as e:
            errors.append(str(e))
        
        # Account Type (always valid from dropdown)
        self.form_data['account_type'] = self.cmb_account_type.Text
        
        try:
            # Validate Budget (Decimal, 0-1000000)
            self.form_data['budget'] = FieldValidator.validate_decimal(
                self.num_budget.Value, "Budget", min_value=0, max_value=1000000
            )
        except ValueError as e:
            errors.append(str(e))
        
        # Newsletter (Boolean)
        self.form_data['newsletter'] = bool(self.chk_newsletter.Checked)
        
        # Terms & Conditions (Boolean, required)
        if not self.chk_terms.Checked:
            errors.append("You must agree to the Terms and Conditions")
        self.form_data['terms_accepted'] = bool(self.chk_terms.Checked)
        
        # Notification Method (String from radio group)
        selected_notification = None
        for rb in self.radio_group:
            if rb.Checked:
                selected_notification = rb.Text
                break
        
        if not selected_notification:
            errors.append("Please select a notification method")
        self.form_data['notification_method'] = selected_notification
        
        # Bio (String, optional)
        bio_text = self.txt_bio.Text.strip()
        if bio_text and bio_text != "Tell us about yourself...":
            self.form_data['bio'] = bio_text
        else:
            self.form_data['bio'] = ""
        
        return len(errors) == 0, errors
    
    def _on_submit(self, sender, e):
        """Handle form submission with validation."""
        # Validate form
        is_valid, errors = self._validate_form()
        
        if not is_valid:
            # Show validation errors
            error_message = "Please correct the following errors:\n\n"
            error_message += "\n".join(f"• {error}" for error in errors)
            
            MessageBox.Show(
                error_message,
                "Validation Error",
                "OK",
                "Error"
            )
            return
        
        # Show success message with data summary
        summary = "Form submitted successfully!\n\n"
        summary += f"Full Name: {self.form_data['full_name']}\n"
        summary += f"Email: {self.form_data['email']}\n"
        summary += f"Age: {self.form_data['age']}\n"
        summary += f"Birth Date: {self.form_data['birth_date'].strftime('%Y-%m-%d')}\n"
        summary += f"Username: {self.form_data['username']}\n"
        summary += f"Account Type: {self.form_data['account_type']}\n"
        summary += f"Budget: ${self.form_data['budget']:.2f}\n"
        summary += f"Newsletter: {'Yes' if self.form_data['newsletter'] else 'No'}\n"
        summary += f"Notification: {self.form_data['notification_method']}\n"
        
        if self.form_data['bio']:
            summary += f"Bio: {self.form_data['bio'][:50]}...\n"
        
        result = MessageBox.Show(
            summary,
            "Success",
            "OKCancel",
            "Information"
        )
        
        if result == DialogResult.OK:
            self.Close()
    
    def _on_clear(self, sender, e):
        """Clear all form fields."""
        result = MessageBox.Show(
            "Are you sure you want to clear all fields?",
            "Confirm Clear",
            "YesNo",
            "Question"
        )
        
        if result == DialogResult.Yes:
            # Reset all fields
            self.txt_fullname.Text = "Enter your full name"
            self.txt_fullname.ForeColor = '#95A5A6'
            
            self.txt_email.Text = "example@email.com"
            self.txt_email.ForeColor = '#95A5A6'
            
            self.num_age.Value = 25
            
            self.dtp_birthdate.Value = datetime.now()
            
            self.txt_username.Text = "Choose a username"
            self.txt_username.ForeColor = '#95A5A6'
            
            self.cmb_account_type.SelectedIndex = 0
            
            self.num_budget.Value = 1000
            
            self.chk_newsletter.Checked = False
            self.chk_terms.Checked = False
            
            if self.radio_group:
                self.radio_group[0].Checked = True
            
            self.txt_bio.Text = "Tell us about yourself..."
            self.txt_bio.ForeColor = '#95A5A6'
            
            self.form_data.clear()


if __name__ == '__main__':
    form = ProfessionalFormExample()
    form.ShowDialog()
