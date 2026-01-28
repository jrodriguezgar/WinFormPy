"""
ScrollBars Example - WinFormPy

This example demonstrates HScrollBar and VScrollBar controls:
- Horizontal and vertical scrollbars
- Value change events  
- RGB color mixer using scrollbars
- Custom min/max values
- Large/small change increments
"""

from winformpy import (
    Application, Form, Label, HScrollBar, VScrollBar, Panel, Button,
    DockStyle, Font, FontStyle
)


class ScrollBarsForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "ScrollBars Demo"
        self.Width = 900
        self.Height = 700
        self.StartPosition = "CenterScreen"
        
        # Apply layout before adding controls
        self.ApplyLayout()
        
        self._init_header()
        self._init_basic_scrollbars()
        self._init_color_mixer()
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
            'BackColor': '#2c3e50',
            'Left': 20,
            'Top': 15,
            'AutoSize': True
        })
    
    def _init_basic_scrollbars(self):
        """Initialize basic scrollbar examples"""
        panel = Panel(self, {
            'Left': 20,
            'Top': 80,
            'Width': 850,
            'Height': 250,
            'BackColor': 'white',
            'BorderStyle': 'FixedSingle'
        })
        
        # Section title
        Label(panel, {
            'Text': 'Basic ScrollBars - Horizontal & Vertical',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 10,
            'Top': 10,
            'AutoSize': True
        })
        
        # Horizontal scrollbar
        Label(panel, {
            'Text': 'Horizontal ScrollBar (0-100):',
            'Left': 20,
            'Top': 50,
            'Width': 200
        })
        
        self.hscroll_basic = HScrollBar(panel, {
            'Left': 230,
            'Top': 50,
            'Width': 400,
            'Minimum': 0,
            'Maximum': 109,  # Maximum + LargeChange - 1
            'Value': 50,
            'SmallChange': 1,
            'LargeChange': 10
        })
        self.hscroll_basic.Scroll = self._on_hscroll_basic_changed
        
        self.lbl_hscroll_value = Label(panel, {
            'Text': 'Value: 50',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'ForeColor': '#3498db',
            'Left': 650,
            'Top': 47,
            'Width': 150
        })
        
        # Vertical scrollbar
        Label(panel, {
            'Text': 'Vertical ScrollBar (0-100):',
            'Left': 20,
            'Top': 100,
            'Width': 200
        })
        
        self.vscroll_basic = VScrollBar(panel, {
            'Left': 230,
            'Top': 100,
            'Width': 20,
            'Height': 120,
            'Minimum': 0,
            'Maximum': 109,
            'Value': 50,
            'SmallChange': 1,
            'LargeChange': 10
        })
        self.vscroll_basic.Scroll = self._on_vscroll_basic_changed
        
        self.lbl_vscroll_value = Label(panel, {
            'Text': 'Value: 50',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'ForeColor': '#27ae60',
            'Left': 270,
            'Top': 140,
            'Width': 150
        })
        
        # Info
        Label(panel, {
            'Text': 'SmallChange: 1 (arrow clicks)\nLargeChange: 10 (track clicks)',
            'Left': 450,
            'Top': 140,
            'Width': 200,
            'Height': 50,
            'ForeColor': '#666666'
        })
    
    def _init_color_mixer(self):
        """Initialize RGB color mixer"""
        panel = Panel(self, {
            'Left': 20,
            'Top': 350,
            'Width': 850,
            'Height': 260,
            'BackColor': '#f8f9fa',
            'BorderStyle': 'FixedSingle'
        })
        
        # Section title
        Label(panel, {
            'Text': 'RGB Color Mixer - Use scrollbars to adjust color',
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
            'Top': y + 3,
            'Width': 50
        })
        
        self.scroll_red = HScrollBar(panel, {
            'Left': 80,
            'Top': y,
            'Width': 350,
            'Minimum': 0,
            'Maximum': 264,  # 255 + 10 - 1
            'Value': 128,
            'SmallChange': 1,
            'LargeChange': 10
        })
        self.scroll_red.Scroll = self._update_color
        
        self.lbl_red = Label(panel, {
            'Text': '128',
            'Left': 445,
            'Top': y + 3,
            'Width': 40,
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        
        # Green channel
        y += 40
        Label(panel, {
            'Text': 'Green:',
            'Left': 20,
            'Top': y + 3,
            'Width': 50
        })
        
        self.scroll_green = HScrollBar(panel, {
            'Left': 80,
            'Top': y,
            'Width': 350,
            'Minimum': 0,
            'Maximum': 264,
            'Value': 128,
            'SmallChange': 1,
            'LargeChange': 10
        })
        self.scroll_green.Scroll = self._update_color
        
        self.lbl_green = Label(panel, {
            'Text': '128',
            'Left': 445,
            'Top': y + 3,
            'Width': 40,
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        
        # Blue channel
        y += 40
        Label(panel, {
            'Text': 'Blue:',
            'Left': 20,
            'Top': y + 3,
            'Width': 50
        })
        
        self.scroll_blue = HScrollBar(panel, {
            'Left': 80,
            'Top': y,
            'Width': 350,
            'Minimum': 0,
            'Maximum': 264,
            'Value': 128,
            'SmallChange': 1,
            'LargeChange': 10
        })
        self.scroll_blue.Scroll = self._update_color
        
        self.lbl_blue = Label(panel, {
            'Text': '128',
            'Left': 445,
            'Top': y + 3,
            'Width': 40,
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        
        # Color preview
        self.color_preview = Panel(panel, {
            'Left': 520,
            'Top': 50,
            'Width': 300,
            'Height': 130,
            'BackColor': '#808080',
            'BorderStyle': 'FixedSingle'
        })
        
        # Hex color label
        self.lbl_hex = Label(panel, {
            'Text': '#808080',
            'Font': Font('Segoe UI', 14, FontStyle.Bold),
            'Left': 520,
            'Top': 190,
            'Width': 150,
            'ForeColor': '#2c3e50'
        })
        
        # Reset button
        btn_reset = Button(panel, {
            'Text': 'Reset to Gray',
            'Left': 680,
            'Top': 185,
            'Width': 140,
            'Height': 35
        })
        btn_reset.Click = self._reset_color
    
    def _init_footer(self):
        """Initialize footer panel"""
        footer = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': 50,
            'BackColor': '#ecf0f1'
        })
        
        Label(footer, {
            'Text': 'Use arrow keys or click the track to change scrollbar values',
            'Left': 20,
            'Top': 15,
            'Width': 600,
            'ForeColor': '#666666'
        })
        
        btn_close = Button(footer, {
            'Text': 'Close',
            'Left': 760,
            'Top': 10,
            'Width': 100,
            'Height': 30
        })
        btn_close.Click = lambda s, e: self.Close()
    
    def _on_hscroll_basic_changed(self, sender, e):
        """Handle horizontal scrollbar value change"""
        value = self.hscroll_basic.Value
        self.lbl_hscroll_value.Text = f'Value: {value}'
    
    def _on_vscroll_basic_changed(self, sender, e):
        """Handle vertical scrollbar value change"""
        value = self.vscroll_basic.Value
        self.lbl_vscroll_value.Text = f'Value: {value}'
    
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


def main():
    form = ScrollBarsForm()
    Application.Run(form)


if __name__ == '__main__':
    main()
