"""
DatePicker Example - WinFormPy

This example demonstrates the DatePicker control with different formats and configurations:
- Different date/time formats
- Custom format strings
- Value change events
- Show/hide checkbox
- Range validation
"""

from winformpy import (
    Application, Form, Label, DatePicker, Button, TextBox,
    Panel, Line, MessageBox, DockStyle, Font, FontStyle
)
from datetime import datetime, timedelta


class DatePickerForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "DatePicker Demo"
        self.Width = 900
        self.Height = 700
        self.StartPosition = "CenterScreen"
        
        # Apply layout before adding controls
        self.ApplyLayout()
        
        self._init_header()
        self._init_format_examples()
        self._init_custom_format_section()
        self._init_range_section()
        self._init_events_section()
        self._init_footer()
    
    def _init_header(self):
        """Initialize header panel"""
        header = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 60,
            'BackColor': '#2c3e50'
        })
        
        title = Label(header, {
            'Text': 'DatePicker Control Examples',
            'Font': Font('Segoe UI', 16, FontStyle.Bold),
            'ForeColor': 'white',
            'BackColor': '#2c3e50',
            'Left': 20,
            'Top': 15,
            'AutoSize': True
        })
    
    def _init_format_examples(self):
        """Initialize different format examples"""
        panel = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 200,
            'BackColor': 'white'
        })
        
        # Section title
        Label(panel, {
            'Text': 'Different Formats',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 20,
            'Top': 15,
            'AutoSize': True
        })
        
        y = 50
        
        # Long format
        Label(panel, {
            'Text': 'Long Date:',
            'Left': 20,
            'Top': y,
            'Width': 150
        })
        
        self.dtp_long = DatePicker(panel, {
            'Format': 'Long',
            'Left': 180,
            'Top': y,
            'Width': 250
        })
        
        # Short format
        y += 35
        Label(panel, {
            'Text': 'Short Date:',
            'Left': 20,
            'Top': y,
            'Width': 150
        })
        
        self.dtp_short = DatePicker(panel, {
            'Format': 'Short',
            'Left': 180,
            'Top': y,
            'Width': 150
        })
        
        # Time format
        y += 35
        Label(panel, {
            'Text': 'Time:',
            'Left': 20,
            'Top': y,
            'Width': 150
        })
        
        self.dtp_time = DatePicker(panel, {
            'Format': 'Time',
            'ShowUpDown': True,
            'Left': 180,
            'Top': y,
            'Width': 150
        })
        
        # With checkbox
        y += 35
        Label(panel, {
            'Text': 'With Checkbox:',
            'Left': 20,
            'Top': y,
            'Width': 150
        })
        
        self.dtp_checkbox = DatePicker(panel, {
            'Format': 'Long',
            'ShowCheckBox': True,
            'Left': 180,
            'Top': y,
            'Width': 250
        })
        
        # Display values button
        btn_show_values = Button(panel, {
            'Text': 'Show Selected Values',
            'Left': 500,
            'Top': 80,
            'Width': 200,
            'Height': 40
        })
        btn_show_values.Click = self._show_format_values
    
    def _init_custom_format_section(self):
        """Initialize custom format section"""
        panel = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 180,
            'BackColor': '#f8f9fa'
        })
        
        # Section title
        Label(panel, {
            'Text': 'Custom Formats',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 20,
            'Top': 15,
            'AutoSize': True
        })
        
        y = 50
        
        # Custom format 1
        Label(panel, {
            'Text': "yyyy-MM-dd:",
            'Left': 20,
            'Top': y,
            'Width': 150
        })
        
        self.dtp_custom1 = DatePicker(panel, {
            'Format': 'Custom',
            'CustomFormat': 'yyyy-MM-dd',
            'Left': 180,
            'Top': y,
            'Width': 150
        })
        
        # Custom format 2
        y += 35
        Label(panel, {
            'Text': "dd/MM/yyyy HH:mm:",
            'Left': 20,
            'Top': y,
            'Width': 150
        })
        
        self.dtp_custom2 = DatePicker(panel, {
            'Format': 'Custom',
            'CustomFormat': 'dd/MM/yyyy HH:mm',
            'Left': 180,
            'Top': y,
            'Width': 200
        })
        
        # Custom format 3
        y += 35
        Label(panel, {
            'Text': "MMMM dd, yyyy:",
            'Left': 20,
            'Top': y,
            'Width': 150
        })
        
        self.dtp_custom3 = DatePicker(panel, {
            'Format': 'Custom',
            'CustomFormat': 'MMMM dd, yyyy',
            'Left': 180,
            'Top': y,
            'Width': 200
        })
        
        # Info label
        Label(panel, {
            'Text': 'Custom format strings:\nyyyy=year, MM=month, dd=day\nHH=hour (24h), mm=minute, ss=second',
            'Left': 500,
            'Top': 50,
            'Width': 350,
            'Height': 80,
            'ForeColor': '#666666'
        })
    
    def _init_range_section(self):
        """Initialize date range section"""
        panel = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 180,
            'BackColor': 'white'
        })
        
        # Section title
        Label(panel, {
            'Text': 'Date Range Validation',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 20,
            'Top': 15,
            'AutoSize': True
        })
        
        y = 50
        
        # Min date
        Label(panel, {
            'Text': 'Min Date (Today):',
            'Left': 20,
            'Top': y,
            'Width': 150
        })
        
        today = datetime.now()
        max_date = today + timedelta(days=30)
        
        self.dtp_min = DatePicker(panel, {
            'Format': 'Long',
            'MinDate': today,
            'Value': today,
            'Left': 180,
            'Top': y,
            'Width': 250
        })
        
        # Max date
        y += 35
        Label(panel, {
            'Text': 'Max Date (+30 days):',
            'Left': 20,
            'Top': y,
            'Width': 150
        })
        
        self.dtp_max = DatePicker(panel, {
            'Format': 'Long',
            'MaxDate': max_date,
            'Value': today,
            'Left': 180,
            'Top': y,
            'Width': 250
        })
        
        # Range picker
        y += 35
        Label(panel, {
            'Text': 'Range (Today to +30):',
            'Left': 20,
            'Top': y,
            'Width': 150
        })
        
        self.dtp_range = DatePicker(panel, {
            'Format': 'Short',
            'MinDate': today,
            'MaxDate': max_date,
            'Value': today,
            'Left': 180,
            'Top': y,
            'Width': 150
        })
        
        # Info
        Label(panel, {
            'Text': 'Try selecting dates outside the allowed range.\nThe control will prevent invalid selections.',
            'Left': 500,
            'Top': 80,
            'Width': 350,
            'Height': 60,
            'ForeColor': '#666666'
        })
    
    def _init_events_section(self):
        """Initialize events section"""
        panel = Panel(self, {
            'Dock': DockStyle.Fill,
            'BackColor': '#f8f9fa'
        })
        
        # Section title
        Label(panel, {
            'Text': 'Value Change Events',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 20,
            'Top': 15,
            'AutoSize': True
        })
        
        # Event picker
        Label(panel, {
            'Text': 'Select a date:',
            'Left': 20,
            'Top': 50,
            'Width': 150
        })
        
        self.dtp_event = DatePicker(panel, {
            'Format': 'Long',
            'Left': 180,
            'Top': 50,
            'Width': 250
        })
        self.dtp_event.ValueChanged = self._on_date_changed
        
        # Event log
        Label(panel, {
            'Text': 'Event Log:',
            'Left': 20,
            'Top': 90,
            'AutoSize': True
        })
        
        self.txt_log = TextBox(panel, {
            'Multiline': True,
            'ReadOnly': True,
            'Left': 20,
            'Top': 120,
            'Width': 840,
            'Height': 100,
            'ScrollBars': 'Vertical'
        })
    
    def _init_footer(self):
        """Initialize footer panel"""
        footer = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': 60,
            'BackColor': '#ecf0f1'
        })
        
        btn_reset = Button(footer, {
            'Text': 'Reset All to Today',
            'Left': 20,
            'Top': 15,
            'Width': 150,
            'Height': 30
        })
        btn_reset.Click = self._reset_all
        
        btn_close = Button(footer, {
            'Text': 'Close',
            'Left': 750,
            'Top': 15,
            'Width': 100,
            'Height': 30
        })
        btn_close.Click = lambda s, e: self.Close()
    
    def _show_format_values(self, sender, e):
        """Show all selected values"""
        values = []
        values.append(f"Long Format: {self.dtp_long.Value}")
        values.append(f"Short Format: {self.dtp_short.Value}")
        values.append(f"Time Format: {self.dtp_time.Value}")
        
        if self.dtp_checkbox.Checked:
            values.append(f"With Checkbox: {self.dtp_checkbox.Value}")
        else:
            values.append("With Checkbox: [Not checked]")
        
        MessageBox.Show('\n'.join(values), 'Selected Values', 'OK', 'Information')
    
    def _on_date_changed(self, sender, e):
        """Handle date change event"""
        new_value = self.dtp_event.Value
        log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] Date changed to: {new_value}\n"
        self.txt_log.Text = log_entry + self.txt_log.Text
    
    def _reset_all(self, sender, e):
        """Reset all pickers to today"""
        today = datetime.now()
        
        self.dtp_long.Value = today
        self.dtp_short.Value = today
        self.dtp_time.Value = today
        self.dtp_checkbox.Value = today
        self.dtp_custom1.Value = today
        self.dtp_custom2.Value = today
        self.dtp_custom3.Value = today
        self.dtp_min.Value = today
        self.dtp_max.Value = today
        self.dtp_range.Value = today
        self.dtp_event.Value = today
        
        MessageBox.Show('All date pickers reset to today', 'Reset Complete', 'OK', 'Information')


def main():
    form = DatePickerForm()
    Application.Run(form)


if __name__ == '__main__':
    main()

