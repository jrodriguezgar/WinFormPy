"""
StatusStrip Example - StatusStrip Control Demonstration

This example demonstrates the StatusStrip control in WinFormPy with:
1. Creating a status bar with multiple panels
2. Displaying different types of information
3. Updating status information dynamically
4. Progress indicators
5. Icons and text in status panels

FEATURES DEMONSTRATED:
- StatusStrip creation
- ToolStripStatusLabel for text display
- ToolStripProgressBar for progress indication
- Dynamic status updates
- Multiple status panels
- Real-time information display
"""

from winformpy.winformpy import (
    Application, Form, StatusStrip, ToolStripStatusLabel, Panel, Button,
    Label, TextBox, ProgressBar, DockStyle, Font, FontStyle, CheckBox
)
import time
from datetime import datetime


class StatusStripExampleForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "WinFormPy StatusStrip Example"
        self.Width = 1000
        self.Height = 650
        self.StartPosition = "CenterScreen"
        self.ApplyLayout()
        
        # State variables
        self.char_count = 0
        self.word_count = 0
        self.line_count = 1
        
        # Initialize components
        self._create_top_panel()
        self._create_content_area()
        self._create_statusstrip()
        
        # Start clock update
        self._update_clock()
    
    def _create_top_panel(self):
        """Create top title panel."""
        top_panel = Panel(self, {
            'Height': 70,
            'BackColor': '#0078D4'
        })
        top_panel.Dock = DockStyle.Top
        
        Label(top_panel, {
            'Text': 'STATUSSTRIP CONTROL DEMONSTRATION',
            'Left': 20,
            'Top': 12,
            'AutoSize': True,
            'Font': Font('Segoe UI', 16, FontStyle.Bold),
            'ForeColor': '#FFFFFF',
            'BackColor': '#0078D4'
        })
        
        Label(top_panel, {
            'Text': 'Status bar at the bottom displays real-time information and status',
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
        
        # Title
        Label(content_panel, {
            'Text': 'Interactive Demo',
            'Left': 20,
            'Top': 20,
            'AutoSize': True,
            'Font': Font('Segoe UI', 14, FontStyle.Bold),
            'ForeColor': '#0078D4'
        })
        
        # Text editor section
        Label(content_panel, {
            'Text': 'Type in the text area below to see live statistics in the status bar:',
            'Left': 20,
            'Top': 55,
            'Width': 900,
            'Font': Font('Segoe UI', 9)
        })
        
        self.txt_editor = TextBox(content_panel, {
            'Left': 20,
            'Top': 80,
            'Width': 920,
            'Height': 200,
            'Multiline': True,
            'ScrollBars': 'Both',
            'Font': Font('Consolas', 10)
        })
        self.txt_editor.TextChanged = self._on_text_changed
        
        # Progress simulation section
        Label(content_panel, {
            'Text': 'Progress Simulation:',
            'Left': 20,
            'Top': 300,
            'AutoSize': True,
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'ForeColor': '#0078D4'
        })
        
        Label(content_panel, {
            'Text': 'Click the button below to simulate a long-running process with progress updates:',
            'Left': 20,
            'Top': 330,
            'Width': 900,
            'Font': Font('Segoe UI', 9)
        })
        
        btn_simulate = Button(content_panel, {
            'Text': '▶️ Start Process Simulation',
            'Left': 20,
            'Top': 360,
            'Width': 200,
            'Height': 35,
            'BackColor': '#2ECC71',
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        btn_simulate.Click = self._on_simulate_process
        
        self.progress_local = ProgressBar(content_panel, {
            'Left': 240,
            'Top': 360,
            'Width': 500,
            'Height': 35,
            'Value': 0
        })
        
        # Status display buttons
        Label(content_panel, {
            'Text': 'Status Messages:',
            'Left': 20,
            'Top': 420,
            'AutoSize': True,
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'ForeColor': '#0078D4'
        })
        
        btn_ready = Button(content_panel, {
            'Text': 'Ready',
            'Left': 20,
            'Top': 450,
            'Width': 100,
            'Height': 30,
            'BackColor': '#95A5A6'
        })
        btn_ready.Click = lambda s, e: self._set_status("Ready", "normal")
        
        btn_working = Button(content_panel, {
            'Text': 'Working...',
            'Left': 130,
            'Top': 450,
            'Width': 100,
            'Height': 30,
            'BackColor': '#3498DB'
        })
        btn_working.Click = lambda s, e: self._set_status("Working...", "normal")
        
        btn_success = Button(content_panel, {
            'Text': 'Success',
            'Left': 240,
            'Top': 450,
            'Width': 100,
            'Height': 30,
            'BackColor': '#2ECC71'
        })
        btn_success.Click = lambda s, e: self._set_status("✓ Operation completed successfully", "success")
        
        btn_warning = Button(content_panel, {
            'Text': 'Warning',
            'Left': 350,
            'Top': 450,
            'Width': 100,
            'Height': 30,
            'BackColor': '#F39C12'
        })
        btn_warning.Click = lambda s, e: self._set_status("⚠ Warning: Check your input", "warning")
        
        btn_error = Button(content_panel, {
            'Text': 'Error',
            'Left': 460,
            'Top': 450,
            'Width': 100,
            'Height': 30,
            'BackColor': '#E74C3C'
        })
        btn_error.Click = lambda s, e: self._set_status("✖ Error: Operation failed", "error")
        
        # Info section
        Label(content_panel, {
            'Text': 'Status Bar Features:',
            'Left': 20,
            'Top': 500,
            'AutoSize': True,
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'ForeColor': '#0078D4'
        })
        
        features = [
            "• Real-time text statistics (characters, words, lines)",
            "• Live clock showing current time",
            "• Progress indicator for long operations",
            "• Status messages with different states",
            "• Multiple status panels with different information"
        ]
        
        y = 525
        for feature in features:
            Label(content_panel, {
                'Text': feature,
                'Left': 40,
                'Top': y,
                'Width': 900,
                'Font': Font('Segoe UI', 9),
                'ForeColor': '#333333'
            })
            y += 22
    
    def _create_statusstrip(self):
        """Create status strip at bottom."""
        self.statusstrip = StatusStrip(self, {
            'BackColor': '#F0F0F0',
            'Height': 28
        })
        self.statusstrip.Dock = DockStyle.Bottom
        
        # Status message label
        self.lbl_status = ToolStripStatusLabel(self.statusstrip)
        self.lbl_status.Text = "Ready"
        self.lbl_status.Width = 250
        self.statusstrip.Items.Add(self.lbl_status)
        
        # Separator (using empty label with border)
        sep1 = ToolStripStatusLabel(self.statusstrip)
        sep1.Text = "|"
        sep1.Width = 10
        self.statusstrip.Items.Add(sep1)
        
        # Character count
        self.lbl_chars = ToolStripStatusLabel(self.statusstrip)
        self.lbl_chars.Text = "Chars: 0"
        self.lbl_chars.Width = 80
        self.statusstrip.Items.Add(self.lbl_chars)
        
        # Word count
        self.lbl_words = ToolStripStatusLabel(self.statusstrip)
        self.lbl_words.Text = "Words: 0"
        self.lbl_words.Width = 80
        self.statusstrip.Items.Add(self.lbl_words)
        
        # Line count
        self.lbl_lines = ToolStripStatusLabel(self.statusstrip)
        self.lbl_lines.Text = "Lines: 1"
        self.lbl_lines.Width = 80
        self.statusstrip.Items.Add(self.lbl_lines)
        
        # Separator
        sep2 = ToolStripStatusLabel(self.statusstrip)
        sep2.Text = "|"
        sep2.Width = 10
        self.statusstrip.Items.Add(sep2)
        
        # Progress indicator
        self.lbl_progress = ToolStripStatusLabel(self.statusstrip)
        self.lbl_progress.Text = "Progress: 0%"
        self.lbl_progress.Width = 100
        self.statusstrip.Items.Add(self.lbl_progress)
        
        # Separator
        sep3 = ToolStripStatusLabel(self.statusstrip)
        sep3.Text = "|"
        sep3.Width = 10
        self.statusstrip.Items.Add(sep3)
        
        # Clock
        self.lbl_clock = ToolStripStatusLabel(self.statusstrip)
        self.lbl_clock.Text = datetime.now().strftime("%H:%M:%S")
        self.lbl_clock.Width = 100
        self.statusstrip.Items.Add(self.lbl_clock)
    
    def _on_text_changed(self, sender, e):
        """Handle text change in editor."""
        text = self.txt_editor.Text
        
        # Count characters
        self.char_count = len(text)
        
        # Count words
        self.word_count = len(text.split()) if text.strip() else 0
        
        # Count lines
        self.line_count = text.count('\n') + 1 if text else 1
        
        # Update status bar
        self.lbl_chars.Text = f"Chars: {self.char_count}"
        self.lbl_words.Text = f"Words: {self.word_count}"
        self.lbl_lines.Text = f"Lines: {self.line_count}"
    
    def _on_simulate_process(self, sender, e):
        """Simulate a long-running process."""
        # Disable button during simulation
        sender.Enabled = False
        self._set_status("Processing...", "normal")
        
        # Simulate progress
        for i in range(0, 101, 10):
            self.progress_local.Value = i
            self.lbl_progress.Text = f"Progress: {i}%"
            
            # Force UI update
            if hasattr(self, '_root'):
                self._root.update()
            
            # Small delay to simulate work
            time.sleep(0.2)
        
        # Complete
        self._set_status("✓ Process completed!", "success")
        sender.Enabled = True
    
    def _set_status(self, message, status_type="normal"):
        """Set status message with type."""
        self.lbl_status.Text = message
        
        # Could change color based on status_type
        # This would require ForeColor support in ToolStripStatusLabel
    
    def _update_clock(self):
        """Update clock display."""
        self.lbl_clock.Text = datetime.now().strftime("%H:%M:%S")
        
        # Schedule next update (1000ms = 1 second)
        if hasattr(self, '_root'):
            self._root.after(1000, self._update_clock)


def main():
    """Application entry point."""
    app = StatusStripExampleForm()
    Application.Run(app)


if __name__ == '__main__':
    main()
