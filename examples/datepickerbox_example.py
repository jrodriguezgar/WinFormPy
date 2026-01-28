"""
DatePickerBox Example - WinFormPy Extended

This example demonstrates the DatePickerBox custom control with:
- Different date formats (Short, Long, ISO, US, Custom)
- Calendar dropdown for visual date selection
- Value change events
- Min/Max date validation
- Custom styling options
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path to import winformpy without installation
sys.path.insert(0, str(Path(__file__).parent.parent))

from winformpy import (
    Application, Form, Label, Button, Panel, TextBox,
    DockStyle, Font, FontStyle, MessageBox
)
from winformpy.winformpy_extended import DatePickerBox, DateFormat


class DatePickerBoxForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "DatePickerBox Demo"
        self.Width = 700
        self.Height = 600
        self.StartPosition = "CenterScreen"
        
        # Apply layout before adding controls
        self.ApplyLayout()
        
        self._init_header()
        self._init_format_examples()
        self._init_events_section()
        self._init_range_section()
    
    def _init_header(self):
        """Initialize header panel."""
        header = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 60,
            'BackColor': '#2c3e50'
        })
        
        Label(header, {
            'Text': 'DatePickerBox Control Demo',
            'Font': Font('Segoe UI', 16, FontStyle.Bold),
            'ForeColor': 'white',
            'BackColor': '#2c3e50',
            'Left': 20,
            'Top': 15,
            'AutoSize': True
        })
    
    def _init_format_examples(self):
        """Initialize different format examples."""
        panel = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 220,
            'BackColor': 'white'
        })
        
        # Section title
        Label(panel, {
            'Text': 'Different Date Formats',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 20,
            'Top': 15,
            'AutoSize': True
        })
        
        y = 50
        x_label = 20
        x_picker = 180
        picker_width = 220
        row_height = 40
        
        # Short format (dd/MM/yyyy)
        Label(panel, {
            'Text': 'Short (dd/MM/yyyy):',
            'Left': x_label,
            'Top': y + 5,
            'Width': 150
        })
        
        self.picker_short = DatePickerBox(panel, {
            'Format': DateFormat.Short,
            'Left': x_picker,
            'Top': y,
            'Width': picker_width
        })
        y += row_height
        
        # Long format (dd MMMM yyyy)
        Label(panel, {
            'Text': 'Long (dd MMMM yyyy):',
            'Left': x_label,
            'Top': y + 5,
            'Width': 150
        })
        
        self.picker_long = DatePickerBox(panel, {
            'Format': DateFormat.Long,
            'Left': x_picker,
            'Top': y,
            'Width': picker_width + 50
        })
        y += row_height
        
        # ISO format (yyyy-MM-dd)
        Label(panel, {
            'Text': 'ISO (yyyy-MM-dd):',
            'Left': x_label,
            'Top': y + 5,
            'Width': 150
        })
        
        self.picker_iso = DatePickerBox(panel, {
            'Format': DateFormat.ISO,
            'Left': x_picker,
            'Top': y,
            'Width': picker_width
        })
        y += row_height
        
        # US format (MM/dd/yyyy)
        Label(panel, {
            'Text': 'US (MM/dd/yyyy):',
            'Left': x_label,
            'Top': y + 5,
            'Width': 150
        })
        
        self.picker_us = DatePickerBox(panel, {
            'Format': DateFormat.US,
            'Left': x_picker,
            'Top': y,
            'Width': picker_width
        })
    
    def _init_events_section(self):
        """Initialize events demonstration section."""
        panel = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 150,
            'BackColor': '#f8f9fa'
        })
        
        # Section title
        Label(panel, {
            'Text': 'Events & Interaction',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 20,
            'Top': 15,
            'AutoSize': True
        })
        
        y = 50
        
        # Date picker with events
        Label(panel, {
            'Text': 'Select a date:',
            'Left': 20,
            'Top': y + 5,
            'Width': 150
        })
        
        self.picker_events = DatePickerBox(panel, {
            'Format': DateFormat.Short,
            'Left': 180,
            'Top': y,
            'Width': 220,
            'CalendarTitleBackColor': '#e74c3c',
            'CalendarSelectBackground': '#e74c3c'
        })
        self.picker_events.ValueChanged = self._on_date_changed
        self.picker_events.CalendarOpened = self._on_calendar_opened
        self.picker_events.CalendarClosed = self._on_calendar_closed
        
        # Event log
        Label(panel, {
            'Text': 'Event Log:',
            'Left': 420,
            'Top': y + 5,
            'Width': 80
        })
        
        self.event_log = TextBox(panel, {
            'Left': 420,
            'Top': y + 25,
            'Width': 250,
            'Height': 60,
            'Multiline': True,
            'ReadOnly': True,
            'BackColor': '#ffffff'
        })
    
    def _init_range_section(self):
        """Initialize date range validation section."""
        panel = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 150,
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
        
        # Range info
        today = datetime.now()
        min_date = today - timedelta(days=30)
        max_date = today + timedelta(days=30)
        
        Label(panel, {
            'Text': f'Range: {min_date.strftime("%d/%m/%Y")} - {max_date.strftime("%d/%m/%Y")}',
            'Left': 20,
            'Top': y + 5,
            'Width': 300,
            'ForeColor': '#666666'
        })
        y += 30
        
        Label(panel, {
            'Text': 'Select date:',
            'Left': 20,
            'Top': y + 5,
            'Width': 150
        })
        
        self.picker_range = DatePickerBox(panel, {
            'Format': DateFormat.Short,
            'Left': 180,
            'Top': y,
            'Width': 220,
            'MinDate': min_date,
            'MaxDate': max_date,
            'Value': today,
            'CalendarTitleBackColor': '#27ae60',
            'CalendarSelectBackground': '#27ae60'
        })
        
        # Current value display
        Label(panel, {
            'Text': 'Selected:',
            'Left': 420,
            'Top': y + 5,
            'Width': 80
        })
        
        self.lbl_range_value = Label(panel, {
            'Text': today.strftime("%d/%m/%Y"),
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'ForeColor': '#27ae60',
            'Left': 500,
            'Top': y + 5,
            'Width': 150
        })
        
        self.picker_range.ValueChanged = self._on_range_date_changed
    
    def _on_date_changed(self, sender, e):
        """Handle date value change."""
        new_value = e.Data['Value']
        self._log_event(f"ValueChanged: {new_value.strftime('%d/%m/%Y')}")
    
    def _on_calendar_opened(self, sender, e):
        """Handle calendar opened."""
        self._log_event("Calendar opened")
    
    def _on_calendar_closed(self, sender, e):
        """Handle calendar closed."""
        self._log_event("Calendar closed")
    
    def _on_range_date_changed(self, sender, e):
        """Handle range picker date change."""
        new_value = e.Data['Value']
        self.lbl_range_value.Text = new_value.strftime("%d/%m/%Y")
    
    def _log_event(self, message):
        """Add message to event log."""
        current = self.event_log.Text
        timestamp = datetime.now().strftime("%H:%M:%S")
        new_text = f"[{timestamp}] {message}\n" + current
        # Keep only last 5 lines
        lines = new_text.split('\n')[:5]
        self.event_log.Text = '\n'.join(lines)


def main():
    """Run the DatePickerBox example."""
    form = DatePickerBoxForm()
    Application.Run(form)


if __name__ == "__main__":
    main()
