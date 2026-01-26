"""
ScrollBars Example - WinFormPy

This example demonstrates HScrollBar and VScrollBar controls:
- Horizontal and vertical scrollbars
- Value change events
- Synchronized scrollbars
- Custom min/max values
- Large/small change increments
- Interactive color mixer using scrollbars
- Image viewer with scroll controls
"""

from winformpy import (
    Application, Form, Label, HScrollBar, VScrollBar, Panel, TextBox,
    Button, MessageBox, DockStyle, Font, FontStyle
)


class ScrollBarsForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "ScrollBars Demo"
        self.Width = 1100
        self.Height = 800
        self.StartPosition = "CenterScreen"
        
        # Apply layout before adding controls
        self.ApplyLayout()
        
        self._init_header()
        self._init_basic_scrollbars()
        self._init_color_mixer()
        self._init_synchronized_scrollbars()
        self._init_custom_range()
        self._init_footer()
    
    def _init_header(self):
        """Initialize header panel"""
        header = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 60,
            'BackColor': '#2c3e50'
        })
        
        title = Label(header, {
            'Text': 'HScrollBar & VScrollBar Examples',
            'Font': Font('Segoe UI', 16, FontStyle.Bold),
            'ForeColor': 'white',
            'Left': 20,
            'Top': 15,
            'AutoSize': True
        })
    
    def _init_basic_scrollbars(self):
        """Initialize basic scrollbar examples"""
        panel = Panel(self, {
            'Left': 20,
            'Top': 80,
            'Width': 520,
            'Height': 280,
            'BackColor': 'white',
            'BorderStyle': 'FixedSingle'
        })
        
        # Section title
        Label(panel, {
            'Text': 'Basic ScrollBars',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 10,
            'Top': 10,
            'AutoSize': True
        })
        
        # Horizontal scrollbar
        Label(panel, {
            'Text': 'Horizontal (0-100):',
            'Left': 20,
            'Top': 50,
            'Width': 150
        })
        
        self.hscroll_basic = HScrollBar(panel, {
            'Left': 20,
            'Top': 75,
            'Width': 300,
            'Minimum': 0,
            'Maximum': 109,  # Maximum + LargeChange - 1
            'Value': 50,
            'SmallChange': 1,
            'LargeChange': 10
        })
        self.hscroll_basic.Scroll = self._on_hscroll_basic_changed
        
        self.lbl_hscroll_value = Label(panel, {
            'Text': '50',
            'Font': Font('Segoe UI', 12, FontStyle.Bold),
            'ForeColor': '#3498db',
            'Left': 330,
            'Top': 72,
            'Width': 60
        })
        
        # Vertical scrollbar
        Label(panel, {
            'Text': 'Vertical (0-100):',
            'Left': 20,
            'Top': 120,
            'Width': 150
        })
        
        self.vscroll_basic = VScrollBar(panel, {
            'Left': 200,
            'Top': 120,
            'Height': 120,
            'Minimum': 0,
            'Maximum': 109,  # Maximum + LargeChange - 1
            'Value': 50,
            'SmallChange': 1,
            'LargeChange': 10
        })
        self.vscroll_basic.Scroll = self._on_vscroll_basic_changed
        
        self.lbl_vscroll_value = Label(panel, {
            'Text': '50',
            'Font': Font('Segoe UI', 12, FontStyle.Bold),
            'ForeColor': '#e74c3c',
            'Left': 250,
            'Top': 170,
            'Width': 60
        })
        
        # Info
        info = Label(panel, {
            'Text': 'SmallChange: 1 (arrow clicks)\nLargeChange: 10 (track clicks)',
            'Left': 350,
            'Top': 120,
            'Width': 160,
            'Height': 50,
            'ForeColor': '#666666'
        })
    
    def _init_color_mixer(self):
        """Initialize RGB color mixer with scrollbars"""
        panel = Panel(self, {
            'Left': 560,
            'Top': 80,
            'Width': 520,
            'Height': 280,
            'BackColor': '#f8f9fa',
            'BorderStyle': 'FixedSingle'
        })
        
        # Section title
        Label(panel, {
            'Text': 'RGB Color Mixer',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 10,
            'Top': 10,
            'AutoSize': True
        })
        
        y = 50
        
        # Red channel
        Label(panel, {
            'Text': 'Red:',
            'Left': 20,
            'Top': y,
            'Width': 50
        })
        
        self.scroll_red = HScrollBar(panel, {
            'Left': 80,
            'Top': y,
            'Width': 200,
            'Minimum': 0,
            'Maximum': 264,  # 255 + 10 - 1
            'Value': 128,
            'SmallChange': 1,
            'LargeChange': 10
        })
        self.scroll_red.Scroll = self._update_color
        
        self.lbl_red = Label(panel, {
            'Text': '128',
            'Left': 290,
            'Top': y,
            'Width': 40
        })
        
        # Green channel
        y += 40
        Label(panel, {
            'Text': 'Green:',
            'Left': 20,
            'Top': y,
            'Width': 50
        })
        
        self.scroll_green = HScrollBar(panel, {
            'Left': 80,
            'Top': y,
            'Width': 200,
            'Minimum': 0,
            'Maximum': 264,
            'Value': 128,
            'SmallChange': 1,
            'LargeChange': 10
        })
        self.scroll_green.Scroll = self._update_color
        
        self.lbl_green = Label(panel, {
            'Text': '128',
            'Left': 290,
            'Top': y,
            'Width': 40
        })
        
        # Blue channel
        y += 40
        Label(panel, {
            'Text': 'Blue:',
            'Left': 20,
            'Top': y,
            'Width': 50
        })
        
        self.scroll_blue = HScrollBar(panel, {
            'Left': 80,
            'Top': y,
            'Width': 200,
            'Minimum': 0,
            'Maximum': 264,
            'Value': 128,
            'SmallChange': 1,
            'LargeChange': 10
        })
        self.scroll_blue.Scroll = self._update_color
        
        self.lbl_blue = Label(panel, {
            'Text': '128',
            'Left': 290,
            'Top': y,
            'Width': 40
        })
        
        # Color preview
        self.color_preview = Panel(panel, {
            'Left': 350,
            'Top': 50,
            'Width': 140,
            'Height': 140,
            'BackColor': '#808080',
            'BorderStyle': 'FixedSingle'
        })
        
        # Hex color label
        self.lbl_hex = Label(panel, {
            'Text': '#808080',
            'Font': Font('Consolas', 11, FontStyle.Bold),
            'Left': 350,
            'Top': 200,
            'Width': 140,
            'TextAlign': 'MiddleCenter'
        })
        
        # Reset button
        btn_reset = Button(panel, {
            'Text': 'Reset',
            'Left': 80,
            'Top': 230,
            'Width': 100,
            'Height': 30
        })
        btn_reset.Click = self._reset_color
    
    def _init_synchronized_scrollbars(self):
        """Initialize synchronized scrollbars"""
        panel = Panel(self, {
            'Left': 20,
            'Top': 380,
            'Width': 520,
            'Height': 280,
            'BackColor': 'white',
            'BorderStyle': 'FixedSingle'
        })
        
        # Section title
        Label(panel, {
            'Text': 'Synchronized ScrollBars',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 10,
            'Top': 10,
            'AutoSize': True
        })
        
        info = Label(panel, {
            'Text': 'These scrollbars are synchronized.\nMoving one updates the other.',
            'Left': 20,
            'Top': 40,
            'Width': 300,
            'Height': 40,
            'ForeColor': '#666666'
        })
        
        # Master scrollbar
        Label(panel, {
            'Text': 'Master:',
            'Left': 20,
            'Top': 90,
            'Width': 60
        })
        
        self.scroll_master = HScrollBar(panel, {
            'Left': 90,
            'Top': 90,
            'Width': 350,
            'Minimum': 0,
            'Maximum': 109,
            'Value': 0,
            'SmallChange': 1,
            'LargeChange': 10
        })
        self.scroll_master.Scroll = self._on_master_scroll
        
        # Slave scrollbar
        Label(panel, {
            'Text': 'Slave:',
            'Left': 20,
            'Top': 140,
            'Width': 60
        })
        
        self.scroll_slave = HScrollBar(panel, {
            'Left': 90,
            'Top': 140,
            'Width': 350,
            'Minimum': 0,
            'Maximum': 109,
            'Value': 0,
            'SmallChange': 1,
            'LargeChange': 10
        })
        self.scroll_slave.Scroll = self._on_slave_scroll
        
        # Value display
        self.lbl_sync_value = Label(panel, {
            'Text': 'Value: 0',
            'Font': Font('Segoe UI', 12, FontStyle.Bold),
            'ForeColor': '#27ae60',
            'Left': 90,
            'Top': 190,
            'Width': 200
        })
        
        # Progress bar simulation
        self.sync_progress = Panel(panel, {
            'Left': 90,
            'Top': 230,
            'Width': 0,
            'Height': 30,
            'BackColor': '#3498db'
        })
    
    def _init_custom_range(self):
        """Initialize custom range scrollbar"""
        panel = Panel(self, {
            'Left': 560,
            'Top': 380,
            'Width': 520,
            'Height': 280,
            'BackColor': '#f8f9fa',
            'BorderStyle': 'FixedSingle'
        })
        
        # Section title
        Label(panel, {
            'Text': 'Custom Range ScrollBar',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 10,
            'Top': 10,
            'AutoSize': True
        })
        
        Label(panel, {
            'Text': 'Temperature Control (-50°C to +150°C):',
            'Left': 20,
            'Top': 50,
            'Width': 300
        })
        
        # Temperature scrollbar
        self.scroll_temp = HScrollBar(panel, {
            'Left': 20,
            'Top': 80,
            'Width': 400,
            'Minimum': -50,
            'Maximum': 159,  # 150 + 10 - 1
            'Value': 20,
            'SmallChange': 1,
            'LargeChange': 10
        })
        self.scroll_temp.Scroll = self._on_temp_changed
        
        self.lbl_temp = Label(panel, {
            'Text': '20°C',
            'Font': Font('Segoe UI', 14, FontStyle.Bold),
            'ForeColor': '#e67e22',
            'Left': 430,
            'Top': 75,
            'Width': 80
        })
        
        # Temperature status
        self.lbl_temp_status = Label(panel, {
            'Text': 'Room Temperature',
            'Left': 20,
            'Top': 120,
            'Width': 400,
            'Height': 30,
            'ForeColor': '#16a085'
        })
        
        # Year scrollbar example
        Label(panel, {
            'Text': 'Year Selection (1900-2100):',
            'Left': 20,
            'Top': 170,
            'Width': 200
        })
        
        self.scroll_year = HScrollBar(panel, {
            'Left': 20,
            'Top': 200,
            'Width': 400,
            'Minimum': 1900,
            'Maximum': 2109,  # 2100 + 10 - 1
            'Value': 2024,
            'SmallChange': 1,
            'LargeChange': 10
        })
        self.scroll_year.Scroll = self._on_year_changed
        
        self.lbl_year = Label(panel, {
            'Text': '2024',
            'Font': Font('Segoe UI', 14, FontStyle.Bold),
            'ForeColor': '#8e44ad',
            'Left': 430,
            'Top': 195,
            'Width': 80
        })
    
    def _init_footer(self):
        """Initialize footer panel"""
        footer = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': 60,
            'BackColor': '#ecf0f1'
        })
        
        btn_close = Button(footer, {
            'Text': 'Close',
            'Left': 960,
            'Top': 15,
            'Width': 100,
            'Height': 30
        })
        btn_close.Click = lambda s, e: self.Close()
    
    def _on_hscroll_basic_changed(self, sender, e):
        """Handle horizontal scrollbar change"""
        value = self.hscroll_basic.Value
        self.lbl_hscroll_value.Text = str(value)
    
    def _on_vscroll_basic_changed(self, sender, e):
        """Handle vertical scrollbar change"""
        value = self.vscroll_basic.Value
        self.lbl_vscroll_value.Text = str(value)
    
    def _update_color(self, sender, e):
        """Update color preview based on RGB values"""
        red = self.scroll_red.Value
        green = self.scroll_green.Value
        blue = self.scroll_blue.Value
        
        # Update labels
        self.lbl_red.Text = str(red)
        self.lbl_green.Text = str(green)
        self.lbl_blue.Text = str(blue)
        
        # Update color preview
        hex_color = f'#{red:02x}{green:02x}{blue:02x}'
        self.color_preview.BackColor = hex_color
        self.lbl_hex.Text = hex_color.upper()
    
    def _reset_color(self, sender, e):
        """Reset color to gray"""
        self.scroll_red.Value = 128
        self.scroll_green.Value = 128
        self.scroll_blue.Value = 128
        self._update_color(None, None)
    
    def _on_master_scroll(self, sender, e):
        """Handle master scrollbar change"""
        value = self.scroll_master.Value
        self.scroll_slave.Value = value
        self._update_sync_display(value)
    
    def _on_slave_scroll(self, sender, e):
        """Handle slave scrollbar change"""
        value = self.scroll_slave.Value
        self.scroll_master.Value = value
        self._update_sync_display(value)
    
    def _update_sync_display(self, value):
        """Update synchronized scrollbar display"""
        self.lbl_sync_value.Text = f'Value: {value}'
        # Update progress bar width (proportional to value)
        self.sync_progress.Width = int((value / 100) * 350)
    
    def _on_temp_changed(self, sender, e):
        """Handle temperature scrollbar change"""
        temp = self.scroll_temp.Value
        self.lbl_temp.Text = f'{temp}°C'
        
        # Update status based on temperature
        if temp < 0:
            status = 'Freezing'
            color = '#3498db'
        elif temp < 15:
            status = 'Cold'
            color = '#5dade2'
        elif temp < 25:
            status = 'Room Temperature'
            color = '#16a085'
        elif temp < 35:
            status = 'Warm'
            color = '#f39c12'
        elif temp < 60:
            status = 'Hot'
            color = '#e67e22'
        else:
            status = 'Very Hot'
            color = '#e74c3c'
        
        self.lbl_temp_status.Text = status
        self.lbl_temp_status.ForeColor = color
    
    def _on_year_changed(self, sender, e):
        """Handle year scrollbar change"""
        year = self.scroll_year.Value
        self.lbl_year.Text = str(year)


def main():
    form = ScrollBarsForm()
    Application.Run(form)


if __name__ == '__main__':
    main()
