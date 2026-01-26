"""
MonthCalendar Example - WinFormPy

Demonstrates the MonthCalendar control with:
- Date selection and DateChanged event
- Bold dates highlighting
- Week numbers display
- Color customization
- Min/Max date range
- First day of week configuration
"""

import sys
from pathlib import Path

# Add parent directory to path to import winformpy without installation
sys.path.insert(0, str(Path(__file__).parent.parent))

from winformpy import (
    Application, Form, Label, MonthCalendar, Button, Panel, 
    MessageBox, CheckBox, Font, FontStyle, Day
)
from datetime import datetime, timedelta


class MonthCalendarForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "MonthCalendar Demo"
        self.Width = 680
        self.Height = 560
        self.StartPosition = "CenterScreen"
        
        # Apply layout before adding controls
        self.ApplyLayout()
        
        # Header
        header = Panel(self, {
            'Left': 0,
            'Top': 0,
            'Width': 680,
            'Height': 50,
            'BackColor': '#2c3e50'
        })
        
        Label(header, {
            'Text': 'MonthCalendar Control',
            'Font': Font('Segoe UI', 14, FontStyle.Bold),
            'ForeColor': 'white',
            'BackColor': '#2c3e50',
            'Left': 20,
            'Top': 12,
            'AutoSize': True
        })
        
        # Calendar with custom colors
        self.calendar = MonthCalendar(self, {
            'Left': 30,
            'Top': 70,
            'ShowWeekNumbers': True,
            'TitleBackColor': '#3498db',
            'TitleForeColor': 'white',
            'SelectBackground': '#e74c3c',
            'SelectForeground': 'white'
        })
        self.calendar.DateChanged = self._on_date_changed
        
        # Selected date display
        Label(self, {
            'Text': 'Selected:',
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'Left': 30,
            'Top': 290,
            'Width': 80
        })
        
        self.lbl_date = Label(self, {
            'Text': str(datetime.now().date()),
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'ForeColor': '#e74c3c',
            'Left': 110,
            'Top': 289,
            'Width': 200
        })
        
        # Info label
        self.lbl_info = Label(self, {
            'Text': 'Select a date',
            'Left': 30,
            'Top': 318,
            'Width': 280,
            'ForeColor': '#7f8c8d'
        })
        
        # Configuration panel
        config_panel = Panel(self, {
            'Left': 340,
            'Top': 70,
            'Width': 320,
            'Height': 268,
            'BackColor': '#ecf0f1',
            'BorderStyle': 'FixedSingle'
        })
        
        Label(config_panel, {
            'Text': 'Configuration',
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'Left': 10,
            'Top': 10,
            'AutoSize': True
        })
        
        # Week numbers checkbox
        self.chk_week_numbers = CheckBox(config_panel, {
            'Text': 'Show Week Numbers',
            'Left': 15,
            'Top': 40,
            'Width': 180,
            'Checked': True
        })
        self.chk_week_numbers.CheckedChanged = self._toggle_week_numbers
        
        # First day of week
        Label(config_panel, {
            'Text': 'First Day of Week:',
            'Left': 15,
            'Top': 70,
            'Width': 120
        })
        
        Button(config_panel, {
            'Text': 'Sunday',
            'Left': 15,
            'Top': 95,
            'Width': 90,
            'Height': 28
        }).Click = lambda s, e: self._set_first_day(Day.Sunday)
        
        Button(config_panel, {
            'Text': 'Monday',
            'Left': 115,
            'Top': 95,
            'Width': 90,
            'Height': 28
        }).Click = lambda s, e: self._set_first_day(Day.Monday)
        
        # Date range
        Label(config_panel, {
            'Text': 'Date Range Limits:',
            'Font': Font('Segoe UI', 9, FontStyle.Bold),
            'Left': 15,
            'Top': 135,
            'Width': 120
        })
        
        Button(config_panel, {
            'Text': 'This Month Only',
            'Left': 15,
            'Top': 160,
            'Width': 135,
            'Height': 28
        }).Click = self._limit_to_month
        
        Button(config_panel, {
            'Text': 'Clear Limits',
            'Left': 160,
            'Top': 160,
            'Width': 135,
            'Height': 28
        }).Click = self._clear_limits
        
        # Colors
        Label(config_panel, {
            'Text': 'Colors:',
            'Font': Font('Segoe UI', 9, FontStyle.Bold),
            'Left': 15,
            'Top': 200,
            'Width': 120
        })
        
        Button(config_panel, {
            'Text': 'Blue Theme',
            'Left': 15,
            'Top': 225,
            'Width': 90,
            'Height': 28
        }).Click = self._apply_blue_theme
        
        Button(config_panel, {
            'Text': 'Green Theme',
            'Left': 115,
            'Top': 225,
            'Width': 90,
            'Height': 28
        }).Click = self._apply_green_theme
        
        Button(config_panel, {
            'Text': 'Red Theme',
            'Left': 215,
            'Top': 225,
            'Width': 90,
            'Height': 28
        }).Click = self._apply_red_theme
        
        # Bold dates section
        Label(self, {
            'Text': 'Bold Dates:',
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'Left': 30,
            'Top': 360,
            'Width': 100
        })
        
        Button(self, {
            'Text': 'Bold Today',
            'Left': 30,
            'Top': 390,
            'Width': 110,
            'Height': 30
        }).Click = self._bold_today
        
        Button(self, {
            'Text': 'Bold Weekends',
            'Left': 150,
            'Top': 390,
            'Width': 120,
            'Height': 30
        }).Click = self._bold_weekends
        
        Button(self, {
            'Text': 'Clear Bold',
            'Left': 280,
            'Top': 390,
            'Width': 110,
            'Height': 30
        }).Click = self._clear_bold
        
        # Action buttons
        Button(self, {
            'Text': 'Go to Today',
            'Left': 30,
            'Top': 475,
            'Width': 120,
            'Height': 35
        }).Click = self._go_to_today
        
        Button(self, {
            'Text': 'Info',
            'Left': 160,
            'Top': 475,
            'Width': 100,
            'Height': 35
        }).Click = self._show_info
        
        # Close button
        Button(self, {
            'Text': 'Close',
            'Left': 550,
            'Top': 475,
            'Width': 100,
            'Height': 35
        }).Click = lambda s, e: self.Close()
        
        # Trigger initial date display
        self._on_date_changed(None, None)
    
    def _on_date_changed(self, sender, e):
        """Handle date selection"""
        selected = self.calendar.SelectionStart
        if not selected:
            selected = datetime.now()
        
        self.lbl_date.Text = selected.strftime("%A, %B %d, %Y")
        
        # Calculate days difference
        today = datetime.now().date()
        selected_date = selected.date() if hasattr(selected, 'date') else selected
        days_diff = (selected_date - today).days
        
        if days_diff == 0:
            self.lbl_info.Text = "Today"
        elif days_diff > 0:
            self.lbl_info.Text = f"{days_diff} day(s) from today"
        else:
            self.lbl_info.Text = f"{abs(days_diff)} day(s) ago"
    
    def _toggle_week_numbers(self, sender, e):
        """Toggle week numbers display"""
        self.calendar.ShowWeekNumbers = self.chk_week_numbers.Checked
    
    def _set_first_day(self, day):
        """Set the first day of week"""
        self.calendar.FirstDayOfWeek = day
        day_name = "Sunday" if day == Day.Sunday else "Monday"
        MessageBox.Show(f'First day set to {day_name}', 'Configuration', 'OK', 'Information')
    
    def _limit_to_month(self, sender, e):
        """Limit calendar to current month only"""
        today = datetime.now()
        first_day = datetime(today.year, today.month, 1)
        
        # Last day of month
        if today.month == 12:
            last_day = datetime(today.year, 12, 31)
        else:
            last_day = datetime(today.year, today.month + 1, 1) - timedelta(days=1)
        
        self.calendar.MinDate = first_day
        self.calendar.MaxDate = last_day
        MessageBox.Show(
            f'Calendar limited to:\n{first_day.strftime("%B %Y")}',
            'Date Range', 'OK', 'Information'
        )
    
    def _clear_limits(self, sender, e):
        """Clear min/max date limits"""
        self.calendar.MinDate = None
        self.calendar.MaxDate = None
        MessageBox.Show('Date range limits cleared', 'Date Range', 'OK', 'Information')
    
    def _apply_blue_theme(self, sender, e):
        """Apply blue color theme"""
        self.calendar.TitleBackColor = '#3498db'
        self.calendar.SelectBackground = '#2980b9'
        self.calendar.SelectForeground = 'white'
    
    def _apply_green_theme(self, sender, e):
        """Apply green color theme"""
        self.calendar.TitleBackColor = '#27ae60'
        self.calendar.SelectBackground = '#229954'
        self.calendar.SelectForeground = 'white'
    
    def _apply_red_theme(self, sender, e):
        """Apply red color theme"""
        self.calendar.TitleBackColor = '#e74c3c'
        self.calendar.SelectBackground = '#c0392b'
        self.calendar.SelectForeground = 'white'
    
    def _bold_today(self, sender, e):
        """Bold today's date"""
        self.calendar.AddBoldedDate(datetime.now())
        self.calendar.UpdateBoldedDates()
    
    def _bold_weekends(self, sender, e):
        """Bold all weekend dates in current month"""
        today = datetime.now()
        count = 0
        
        for day in range(1, 32):
            try:
                date = datetime(today.year, today.month, day)
                if date.weekday() in [5, 6]:  # Saturday or Sunday
                    self.calendar.AddBoldedDate(date)
                    count += 1
            except ValueError:
                break
        
        self.calendar.UpdateBoldedDates()
        MessageBox.Show(f'Bolded {count} weekend dates', 'Bold Dates', 'OK', 'Information')
    
    def _clear_bold(self, sender, e):
        """Clear all bold dates"""
        self.calendar.RemoveAllBoldedDates()
        self.calendar.UpdateBoldedDates()
    
    def _go_to_today(self, sender, e):
        """Navigate to today's date"""
        self.calendar.SetDate(datetime.now())
    
    def _show_info(self, sender, e):
        """Show calendar information"""
        selected = self.calendar.SelectionStart
        info = []
        info.append(f"Selected Date: {selected.strftime('%B %d, %Y')}")
        info.append(f"Day of Week: {selected.strftime('%A')}")
        info.append(f"Week Number: {selected.strftime('%U')}")
        info.append(f"")
        info.append(f"Show Week Numbers: {self.calendar.ShowWeekNumbers}")
        
        if self.calendar.MinDate:
            info.append(f"Min Date: {self.calendar.MinDate.strftime('%B %d, %Y')}")
        if self.calendar.MaxDate:
            info.append(f"Max Date: {self.calendar.MaxDate.strftime('%B %d, %Y')}")
        
        MessageBox.Show('\n'.join(info), 'Calendar Information', 'OK', 'Information')


def main():
    form = MonthCalendarForm()
    Application.Run(form)


if __name__ == '__main__':
    main()
