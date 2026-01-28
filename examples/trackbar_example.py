"""
TrackBar Example - TrackBar Control Demonstration

This example demonstrates the TrackBar control in WinFormPy with:
1. Horizontal and vertical trackbars
2. Value change events
3. Tick marks and intervals
4. Minimum and maximum values
5. Different orientations
6. Real-world use cases (volume, brightness, zoom, etc.)

FEATURES DEMONSTRATED:
- TrackBar creation and orientation
- Value property and events
- Minimum and Maximum values
- TickFrequency for tick marks
- LargeChange and SmallChange
- ValueChanged event
- Practical applications
"""

from winformpy.winformpy import (
    Application, Form, TrackBar, Panel, Button, Label, ProgressBar,
    DockStyle, Font, FontStyle, Orientation
)


class TrackBarExampleForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "WinFormPy TrackBar Example"
        self.Width = 1100
        self.Height = 750
        self.StartPosition = "CenterScreen"
        self.ApplyLayout()
        
        # Initialize components
        self._create_top_panel()
        self._create_content_area()
        self._create_bottom_status()
    
    def _create_top_panel(self):
        """Create top title panel."""
        top_panel = Panel(self, {
            'Height': 70,
            'BackColor': '#0078D4'
        })
        top_panel.Dock = DockStyle.Top
        
        Label(top_panel, {
            'Text': 'TRACKBAR CONTROL DEMONSTRATION',
            'Left': 20,
            'Top': 12,
            'AutoSize': True,
            'Font': Font('Segoe UI', 16, FontStyle.Bold),
            'ForeColor': '#FFFFFF',
            'BackColor': '#0078D4'
        })
        
        Label(top_panel, {
            'Text': 'Interactive sliders for adjusting values - volume, brightness, zoom, and more',
            'Left': 20,
            'Top': 42,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9),
            'ForeColor': '#E0E0E0',
            'BackColor': '#0078D4'
        })
    
    def _create_content_area(self):
        """Create main content area."""
        content_panel = Panel(self, {
            'BackColor': '#F5F5F5',
            'Padding': (20, 20, 20, 20)
        })
        content_panel.Dock = DockStyle.Fill
        
        # Volume Control Section
        self._create_volume_section(content_panel)
        
        # Brightness Control Section
        self._create_brightness_section(content_panel)
        
        # Zoom Control Section
        self._create_zoom_section(content_panel)
        
        # RGB Color Mixer Section
        self._create_rgb_section(content_panel)
        
        # Settings Section
        self._create_settings_section(content_panel)
    
    def _create_volume_section(self, parent):
        """Create volume control section."""
        # Section panel
        section = Panel(parent, {
            'Left': 20,
            'Top': 20,
            'Width': 500,
            'Height': 120,
            'BackColor': '#FFFFFF',
            'BorderStyle': 'FixedSingle'
        })
        
        Label(section, {
            'Text': '🔊 Volume Control',
            'Left': 15,
            'Top': 10,
            'AutoSize': True,
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'ForeColor': '#0078D4'
        })
        
        # Volume trackbar
        self.track_volume = TrackBar(section, {
            'Left': 15,
            'Top': 40,
            'Width': 350,
            'Height': 50,
            'Minimum': 0,
            'Maximum': 100,
            'Value': 50,
            'TickFrequency': 10,
            'Orientation': Orientation.Horizontal
        })
        self.track_volume.ValueChanged = self._on_volume_changed
        
        # Volume label
        self.lbl_volume = Label(section, {
            'Text': '50%',
            'Left': 380,
            'Top': 50,
            'Width': 100,
            'Font': Font('Segoe UI', 14, FontStyle.Bold),
            'ForeColor': '#2ECC71'
        })
        
        # Mute button
        self.btn_mute = Button(section, {
            'Text': '🔇 Mute',
            'Left': 15,
            'Top': 80,
            'Width': 80,
            'Height': 25
        })
        self.btn_mute.Click = self._on_mute_toggle
        
        # Max button
        btn_max = Button(section, {
            'Text': 'Max',
            'Left': 100,
            'Top': 80,
            'Width': 60,
            'Height': 25
        })
        btn_max.Click = lambda s, e: setattr(self.track_volume, 'Value', 100)
    
    def _create_brightness_section(self, parent):
        """Create brightness control section."""
        section = Panel(parent, {
            'Left': 540,
            'Top': 20,
            'Width': 500,
            'Height': 120,
            'BackColor': '#FFFFFF',
            'BorderStyle': 'FixedSingle'
        })
        
        Label(section, {
            'Text': '☀️ Brightness',
            'Left': 15,
            'Top': 10,
            'AutoSize': True,
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'ForeColor': '#0078D4'
        })
        
        # Brightness trackbar
        self.track_brightness = TrackBar(section, {
            'Left': 15,
            'Top': 40,
            'Width': 350,
            'Height': 50,
            'Minimum': 0,
            'Maximum': 100,
            'Value': 70,
            'TickFrequency': 10,
            'Orientation': Orientation.Horizontal
        })
        self.track_brightness.ValueChanged = self._on_brightness_changed
        
        # Brightness label
        self.lbl_brightness = Label(section, {
            'Text': '70%',
            'Left': 380,
            'Top': 50,
            'Width': 100,
            'Font': Font('Segoe UI', 14, FontStyle.Bold),
            'ForeColor': '#F39C12'
        })
        
        # Visual brightness indicator
        self.brightness_indicator = Label(section, {
            'Text': '💡 Brightness Level',
            'Left': 15,
            'Top': 85,
            'Width': 350,
            'Height': 25,
            'BackColor': '#B8B8B8',
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'ForeColor': '#000000',
            'BorderStyle': 'FixedSingle'
        })
    
    def _create_zoom_section(self, parent):
        """Create zoom control section."""
        section = Panel(parent, {
            'Left': 20,
            'Top': 160,
            'Width': 500,
            'Height': 140,
            'BackColor': '#FFFFFF',
            'BorderStyle': 'FixedSingle'
        })
        
        Label(section, {
            'Text': '🔍 Zoom Level',
            'Left': 15,
            'Top': 10,
            'AutoSize': True,
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'ForeColor': '#0078D4'
        })
        
        # Zoom trackbar (10% to 200%)
        self.track_zoom = TrackBar(section, {
            'Left': 15,
            'Top': 40,
            'Width': 350,
            'Height': 50,
            'Minimum': 10,
            'Maximum': 200,
            'Value': 100,
            'TickFrequency': 25,
            'Orientation': Orientation.Horizontal
        })
        self.track_zoom.ValueChanged = self._on_zoom_changed
        
        # Zoom label
        self.lbl_zoom = Label(section, {
            'Text': '100%',
            'Left': 380,
            'Top': 50,
            'Width': 100,
            'Font': Font('Segoe UI', 14, FontStyle.Bold),
            'ForeColor': '#3498DB'
        })
        
        # Preset buttons
        Label(section, {
            'Text': 'Presets:',
            'Left': 15,
            'Top': 95,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        
        btn_50 = Button(section, {'Text': '50%', 'Left': 80, 'Top': 92, 'Width': 50, 'Height': 25})
        btn_50.Click = lambda s, e: self._set_zoom(50)
        
        btn_100 = Button(section, {'Text': '100%', 'Left': 135, 'Top': 92, 'Width': 50, 'Height': 25})
        btn_100.Click = lambda s, e: self._set_zoom(100)
        
        btn_150 = Button(section, {'Text': '150%', 'Left': 190, 'Top': 92, 'Width': 50, 'Height': 25})
        btn_150.Click = lambda s, e: self._set_zoom(150)
        
        btn_200 = Button(section, {'Text': '200%', 'Left': 245, 'Top': 92, 'Width': 50, 'Height': 25})
        btn_200.Click = lambda s, e: self._set_zoom(200)
    
    def _create_rgb_section(self, parent):
        """Create RGB color mixer section."""
        section = Panel(parent, {
            'Left': 540,
            'Top': 160,
            'Width': 500,
            'Height': 220,
            'BackColor': '#FFFFFF',
            'BorderStyle': 'FixedSingle'
        })
        
        Label(section, {
            'Text': '🎨 RGB Color Mixer',
            'Left': 15,
            'Top': 10,
            'AutoSize': True,
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'ForeColor': '#0078D4'
        })
        
        # Red channel
        Label(section, {'Text': 'Red:', 'Left': 15, 'Top': 45, 'Width': 40, 'ForeColor': '#E74C3C', 'Font': Font('Segoe UI', 9, FontStyle.Bold)})
        self.track_red = TrackBar(section, {
            'Left': 60, 'Top': 40, 'Width': 300, 'Height': 50,
            'Minimum': 0, 'Maximum': 255, 'Value': 128, 'TickFrequency': 25
        })
        self.track_red.ValueChanged = self._on_rgb_changed
        self.lbl_red = Label(section, {'Text': '128', 'Left': 370, 'Top': 50, 'Width': 40, 'ForeColor': '#E74C3C', 'Font': Font('Segoe UI', 10, FontStyle.Bold)})
        
        # Green channel
        Label(section, {'Text': 'Green:', 'Left': 15, 'Top': 85, 'Width': 40, 'ForeColor': '#2ECC71', 'Font': Font('Segoe UI', 9, FontStyle.Bold)})
        self.track_green = TrackBar(section, {
            'Left': 60, 'Top': 80, 'Width': 300, 'Height': 50,
            'Minimum': 0, 'Maximum': 255, 'Value': 128, 'TickFrequency': 25
        })
        self.track_green.ValueChanged = self._on_rgb_changed
        self.lbl_green = Label(section, {'Text': '128', 'Left': 370, 'Top': 90, 'Width': 40, 'ForeColor': '#2ECC71', 'Font': Font('Segoe UI', 10, FontStyle.Bold)})
        
        # Blue channel
        Label(section, {'Text': 'Blue:', 'Left': 15, 'Top': 125, 'Width': 40, 'ForeColor': '#3498DB', 'Font': Font('Segoe UI', 9, FontStyle.Bold)})
        self.track_blue = TrackBar(section, {
            'Left': 60, 'Top': 120, 'Width': 300, 'Height': 50,
            'Minimum': 0, 'Maximum': 255, 'Value': 128, 'TickFrequency': 25
        })
        self.track_blue.ValueChanged = self._on_rgb_changed
        self.lbl_blue = Label(section, {'Text': '128', 'Left': 370, 'Top': 130, 'Width': 40, 'ForeColor': '#3498DB', 'Font': Font('Segoe UI', 10, FontStyle.Bold)})
        
        # Color preview
        Label(section, {'Text': 'Color Preview:', 'Left': 15, 'Top': 175, 'AutoSize': True, 'Font': Font('Segoe UI', 9, FontStyle.Bold)})
        self.color_preview = Panel(section, {
            'Left': 120, 'Top': 170, 'Width': 240, 'Height': 35,
            'BackColor': '#808080', 'BorderStyle': 'FixedSingle'
        })
        
        self.lbl_rgb_hex = Label(section, {
            'Text': '#808080',
            'Left': 370,
            'Top': 177,
            'Width': 100,
            'Font': Font('Consolas', 10, FontStyle.Bold)
        })
    
    def _create_settings_section(self, parent):
        """Create settings section."""
        section = Panel(parent, {
            'Left': 20,
            'Top': 320,
            'Width': 500,
            'Height': 220,
            'BackColor': '#FFFFFF',
            'BorderStyle': 'FixedSingle'
        })
        
        Label(section, {
            'Text': '⚙️ Settings',
            'Left': 15,
            'Top': 10,
            'AutoSize': True,
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'ForeColor': '#0078D4'
        })
        
        # Quality setting
        Label(section, {'Text': 'Quality:', 'Left': 15, 'Top': 45, 'Width': 80, 'Font': Font('Segoe UI', 9, FontStyle.Bold)})
        self.track_quality = TrackBar(section, {
            'Left': 100, 'Top': 40, 'Width': 250, 'Height': 50,
            'Minimum': 1, 'Maximum': 5, 'Value': 3, 'TickFrequency': 1
        })
        self.track_quality.ValueChanged = self._on_quality_changed
        
        quality_labels = ['', 'Low', 'Medium', 'High', 'Ultra', 'Max']
        self.lbl_quality = Label(section, {
            'Text': quality_labels[3],
            'Left': 360,
            'Top': 50,
            'Width': 100,
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'ForeColor': '#9B59B6'
        })
        
        # Transparency
        Label(section, {'Text': 'Opacity:', 'Left': 15, 'Top': 95, 'Width': 80, 'Font': Font('Segoe UI', 9, FontStyle.Bold)})
        self.track_opacity = TrackBar(section, {
            'Left': 100, 'Top': 90, 'Width': 250, 'Height': 50,
            'Minimum': 0, 'Maximum': 100, 'Value': 100, 'TickFrequency': 10
        })
        self.track_opacity.ValueChanged = self._on_opacity_changed
        self.lbl_opacity = Label(section, {'Text': '100%', 'Left': 360, 'Top': 100, 'Width': 100, 'Font': Font('Segoe UI', 10, FontStyle.Bold)})
        
        # Speed
        Label(section, {'Text': 'Speed:', 'Left': 15, 'Top': 145, 'Width': 80, 'Font': Font('Segoe UI', 9, FontStyle.Bold)})
        self.track_speed = TrackBar(section, {
            'Left': 100, 'Top': 140, 'Width': 250, 'Height': 50,
            'Minimum': 1, 'Maximum': 10, 'Value': 5, 'TickFrequency': 1
        })
        self.track_speed.ValueChanged = self._on_speed_changed
        self.lbl_speed = Label(section, {'Text': '5x', 'Left': 360, 'Top': 150, 'Width': 100, 'Font': Font('Segoe UI', 10, FontStyle.Bold)})
        
        # Progress indicator
        Label(section, {'Text': 'Progress:', 'Left': 15, 'Top': 190, 'Width': 80, 'Font': Font('Segoe UI', 9, FontStyle.Bold)})
        self.progress_demo = ProgressBar(section, {
            'Left': 100, 'Top': 188, 'Width': 360, 'Height': 20, 'Value': 50
        })
    
    def _create_bottom_status(self):
        """Create bottom status panel."""
        status_panel = Panel(self, {
            'Height': 35,
            'BackColor': '#34495E'
        })
        status_panel.Dock = DockStyle.Bottom
        
        self.lbl_status = Label(status_panel, {
            'Text': 'Ready | Adjust any trackbar to see real-time changes',
            'Left': 15,
            'Top': 8,
            'Width': 1000,
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9),
            'BackColor': '#34495E'
        })
    
    # Event Handlers
    def _on_volume_changed(self, sender, e):
        """Handle volume change."""
        value = self.track_volume.Value
        self.lbl_volume.Text = f"{value}%"
        self.lbl_status.Text = f"Volume: {value}%"
    
    def _on_brightness_changed(self, sender, e):
        """Handle brightness change."""
        value = self.track_brightness.Value
        self.lbl_brightness.Text = f"{value}%"
        
        # Simulate brightness change (0=black, 100=white)
        brightness_val = int((value / 100) * 255)
        brightness_color = f"#{brightness_val:02X}{brightness_val:02X}{brightness_val:02X}"
        self.brightness_indicator.BackColor = brightness_color
        
        # Adjust text color for better contrast
        text_color = '#FFFFFF' if value < 50 else '#000000'
        self.brightness_indicator.ForeColor = text_color
        
        self.lbl_status.Text = f"Brightness: {value}%"
    
    def _on_zoom_changed(self, sender, e):
        """Handle zoom change."""
        value = self.track_zoom.Value
        self.lbl_zoom.Text = f"{value}%"
        self.lbl_status.Text = f"Zoom: {value}%"
    
    def _set_zoom(self, value):
        """Set zoom value and update label."""
        self.track_zoom.Value = value
        self.lbl_zoom.Text = f"{value}%"
        self.lbl_status.Text = f"Zoom: {value}%"
    
    def _on_rgb_changed(self, sender, e):
        """Handle RGB color change."""
        r = self.track_red.Value
        g = self.track_green.Value
        b = self.track_blue.Value
        
        self.lbl_red.Text = str(r)
        self.lbl_green.Text = str(g)
        self.lbl_blue.Text = str(b)
        
        # Convert to hex color
        hex_color = f"#{r:02X}{g:02X}{b:02X}"
        self.color_preview.BackColor = hex_color
        self.lbl_rgb_hex.Text = hex_color
        
        self.lbl_status.Text = f"RGB: ({r}, {g}, {b}) = {hex_color}"
    
    def _on_quality_changed(self, sender, e):
        """Handle quality change."""
        value = self.track_quality.Value
        quality_labels = ['', 'Low', 'Medium', 'High', 'Ultra', 'Max']
        self.lbl_quality.Text = quality_labels[value]
        self.lbl_status.Text = f"Quality: {quality_labels[value]}"
    
    def _on_opacity_changed(self, sender, e):
        """Handle opacity change."""
        value = self.track_opacity.Value
        self.lbl_opacity.Text = f"{value}%"
        self.lbl_status.Text = f"Opacity: {value}%"
    
    def _on_speed_changed(self, sender, e):
        """Handle speed change."""
        value = self.track_speed.Value
        self.lbl_speed.Text = f"{value}x"
        self.progress_demo.Value = value * 10
        self.lbl_status.Text = f"Speed: {value}x"
    
    def _on_mute_toggle(self, sender, e):
        """Toggle mute."""
        if self.track_volume.Value > 0:
            self._volume_before_mute = self.track_volume.Value
            self.track_volume.Value = 0
            self.btn_mute.Text = "🔊 Unmute"
        else:
            self.track_volume.Value = getattr(self, '_volume_before_mute', 50)
            self.btn_mute.Text = "🔇 Mute"


def main():
    """Application entry point."""
    app = TrackBarExampleForm()
    Application.Run(app)


if __name__ == '__main__':
    main()
