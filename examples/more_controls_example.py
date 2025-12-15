"""
Advanced Controls Example - WinFormPy
Demonstrates: LinkLabel, DomainUpDown, NumericUpDown, RichTextBox
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from winformpy.winformpy import (
    Form, Label, LinkLabel, DomainUpDown, NumericUpDown, 
    RichTextBox, Button, Line, MessageBox, ColorDialog, DialogResult,
    Color, Font, FontStyle
)
import webbrowser


class MoreControlsForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "Advanced Controls Demo"
        self.Size = (1024, 620)
        self.StartPosition = "CenterScreen"
        
        self._init_linklabel_section()
        self._init_updown_section()
        self._init_richtextbox_section()
        self._init_action_buttons()
    
    def _init_linklabel_section(self):
        """Initialize LinkLabel controls"""
        # Section title
        lbl_section1 = Label(self)
        lbl_section1.Text = "LinkLabel Examples"
        lbl_section1.Location = (10, 10)
        lbl_section1.Size = (360, 20)
        lbl_section1.Font = Font("Segoe UI", 10, FontStyle.Bold).ToTkFont()
        lbl_section1.ForeColor = Color(Color.Navy)
        
        # Separator line
        sep1 = Line(self, {'Left': 10, 'Top': 35, 'Width': 480, 'Height': 2, 'BackColor': str(Color(Color.Navy))})
        
        # Simple LinkLabel
        lbl1 = Label(self)
        lbl1.Text = "Simple Link:"
        lbl1.Location = (20, 45)
        lbl1.Size = (100, 20)
        
        self.link1 = LinkLabel(self)
        self.link1.Text = "Visit Python.org"
        self.link1.Location = (130, 45)
        self.link1.Size = (230, 20)
        self.link1.Click = self.on_link1_click
        
        # LinkLabel with action (no URL)
        lbl2 = Label(self)
        lbl2.Text = "Action Link:"
        lbl2.Location = (20, 75)
        lbl2.Size = (100, 20)
        
        self.link2 = LinkLabel(self)
        self.link2.Text = "Show Message"
        self.link2.Location = (130, 75)
        self.link2.Size = (230, 20)
        self.link2.Click = self.on_link2_click
        
        # Info label
        lbl_info = Label(self)
        lbl_info.Text = "Click links to open URLs or trigger actions."
        lbl_info.Location = (20, 105)
        lbl_info.Size = (360, 20)
        lbl_info.ForeColor = Color.Gray
    
    def _init_updown_section(self):
        """Initialize UpDown controls"""
        # Section title
        lbl_section2 = Label(self)
        lbl_section2.Text = "UpDown Controls"
        lbl_section2.Location = (510, 10)
        lbl_section2.Size = (480, 20)
        lbl_section2.Font = Font("Segoe UI", 10, FontStyle.Bold).ToTkFont()
        lbl_section2.ForeColor = Color(Color.DarkGreen)
        
        # Separator line
        sep2 = Line(self, {'Left': 510, 'Top': 35, 'Width': 480, 'Height': 2, 'BackColor': str(Color(Color.DarkGreen))})
        
        # DomainUpDown
        lbl_domain = Label(self)
        lbl_domain.Text = "DomainUpDown (Days):"
        lbl_domain.Location = (520, 45)
        lbl_domain.Size = (180, 20)
        
        self.domain_updown = DomainUpDown(self)
        self.domain_updown.Location = (710, 43)
        self.domain_updown.Size = (260, 25)
        # Add items using the Items collection
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            self.domain_updown.Items.Add(day)
        self.domain_updown.SelectedIndex = 0
        self.domain_updown.ReadOnly = True
        self.domain_updown.Wrap = True
        
        # NumericUpDown - Integer
        lbl_numeric1 = Label(self)
        lbl_numeric1.Text = "NumericUpDown (0-100):"
        lbl_numeric1.Location = (520, 80)
        lbl_numeric1.Size = (180, 20)
        
        self.numeric_updown1 = NumericUpDown(self)
        self.numeric_updown1.Location = (710, 78)
        self.numeric_updown1.Size = (260, 25)
        self.numeric_updown1.Minimum = 0
        self.numeric_updown1.Maximum = 100
        self.numeric_updown1.Value = 50
        self.numeric_updown1.Increment = 5
        
        # NumericUpDown - Decimal
        lbl_numeric2 = Label(self)
        lbl_numeric2.Text = "NumericUpDown (Decimal):"
        lbl_numeric2.Location = (520, 115)
        lbl_numeric2.Size = (180, 20)
        
        self.numeric_updown2 = NumericUpDown(self)
        self.numeric_updown2.Location = (710, 113)
        self.numeric_updown2.Size = (260, 25)
        self.numeric_updown2.Minimum = 0.0
        self.numeric_updown2.Maximum = 10.0
        self.numeric_updown2.Value = 5.5
        self.numeric_updown2.Increment = 0.5
        self.numeric_updown2.DecimalPlaces = 2
    
    def _init_richtextbox_section(self):
        """Initialize RichTextBox control"""
        # Section title
        lbl_section3 = Label(self)
        lbl_section3.Text = "RichTextBox - Formatted Text Editor"
        lbl_section3.Location = (10, 170)
        lbl_section3.Size = (990, 20)
        lbl_section3.Font = Font("Segoe UI", 10, FontStyle.Bold).ToTkFont()
        lbl_section3.ForeColor = Color(Color.DarkRed)
        
        # Separator line
        sep3 = Line(self, {'Left': 10, 'Top': 195, 'Width': 990, 'Height': 2, 'BackColor': str(Color(Color.DarkRed))})
        
        # RichTextBox
        self.richtextbox = RichTextBox(self)
        self.richtextbox.Location = (20, 205)
        self.richtextbox.Size = (980, 240)
        self.richtextbox.Text = "Welcome to RichTextBox!\n\n"
        self.richtextbox.Text += "This control supports rich text formatting.\n"
        self.richtextbox.Text += "You can change font, color, and style.\n\n"
        self.richtextbox.Text += "Try typing here and using the buttons below to format text."
        
        # Formatting buttons
        y_pos = 455
        
        btn_bold = Button(self)
        btn_bold.Text = "Bold"
        btn_bold.Location = (20, y_pos)
        btn_bold.Size = (80, 30)
        btn_bold.Click = self.on_bold_click
        
        btn_italic = Button(self)
        btn_italic.Text = "Italic"
        btn_italic.Location = (110, y_pos)
        btn_italic.Size = (80, 30)
        btn_italic.Click = self.on_italic_click
        
        btn_underline = Button(self)
        btn_underline.Text = "Underline"
        btn_underline.Location = (200, y_pos)
        btn_underline.Size = (80, 30)
        btn_underline.Click = self.on_underline_click
        
        btn_red = Button(self)
        btn_red.Text = "Red"
        btn_red.Location = (290, y_pos)
        btn_red.Size = (70, 30)
        btn_red.BackColor = Color.Red
        btn_red.ForeColor = Color.White
        btn_red.Click = self.on_red_click
        
        btn_blue = Button(self)
        btn_blue.Text = "Blue"
        btn_blue.Location = (370, y_pos)
        btn_blue.Size = (70, 30)
        btn_blue.BackColor = Color.Blue
        btn_blue.ForeColor = Color.White
        btn_blue.Click = self.on_blue_click
        
        btn_green = Button(self)
        btn_green.Text = "Green"
        btn_green.Location = (450, y_pos)
        btn_green.Size = (70, 30)
        btn_green.BackColor = Color.Green
        btn_green.ForeColor = Color.White
        btn_green.Click = self.on_green_click
        
        btn_custom_color = Button(self)
        btn_custom_color.Text = "Custom..."
        btn_custom_color.Location = (530, y_pos)
        btn_custom_color.Size = (90, 30)
        btn_custom_color.BackColor = Color(Color.Orange)
        btn_custom_color.ForeColor = Color.White
        btn_custom_color.Click = self.on_custom_color_click
        
        btn_clear_format = Button(self)
        btn_clear_format.Text = "Clear Format"
        btn_clear_format.Location = (630, y_pos)
        btn_clear_format.Size = (100, 30)
        btn_clear_format.Click = self.on_clear_format_click
        
        btn_clear_all = Button(self)
        btn_clear_all.Text = "Clear All"
        btn_clear_all.Location = (740, y_pos)
        btn_clear_all.Size = (100, 30)
        btn_clear_all.Click = self.on_clear_all_click
        
        # Info label
        lbl_info2 = Label(self)
        lbl_info2.Text = "Select text and click format buttons. Use Ctrl+A to select all."
        lbl_info2.Location = (20, 495)
        lbl_info2.Size = (980, 20)
        lbl_info2.ForeColor = Color.Gray
    
    def _init_action_buttons(self):
        """Initialize action buttons"""
        btn_get_values = Button(self)
        btn_get_values.Text = "Get All Values"
        btn_get_values.Location = (10, 530)
        btn_get_values.Size = (150, 40)
        btn_get_values.Click = self.on_get_values_click
        
        btn_reset = Button(self)
        btn_reset.Text = "Reset All"
        btn_reset.Location = (170, 530)
        btn_reset.Size = (150, 40)
        btn_reset.Click = self.on_reset_click
        
        btn_close = Button(self)
        btn_close.Text = "Close"
        btn_close.Location = (630, 540)
        btn_close.Size = (150, 40)
        btn_close.Click = lambda s, e: self.Close()
    
    # LinkLabel event handlers
    def on_link1_click(self, sender, event):
        """Open Python.org website"""
        webbrowser.open("https://www.python.org")
        self.link1.LinkVisited = True
    
    def on_link2_click(self, sender, event):
        """Show a message dialog"""
        MessageBox.Show(
            "This is an action link that shows a message instead of opening a URL!",
            "Action Link",
            "OK",
            "Information"
        )
        self.link2.LinkVisited = True
    
    # RichTextBox formatting event handlers
    def on_bold_click(self, sender, event):
        """Apply bold formatting to selected text"""
        font = Font("Segoe UI", 9, FontStyle.Bold)
        self.richtextbox.SelectionFont = font.ToTkFont()
    
    def on_italic_click(self, sender, event):
        """Apply italic formatting to selected text"""
        font = Font("Segoe UI", 9, FontStyle.Italic)
        self.richtextbox.SelectionFont = font.ToTkFont()
    
    def on_underline_click(self, sender, event):
        """Apply underline formatting to selected text"""
        font = Font("Segoe UI", 9, FontStyle.Underline)
        self.richtextbox.SelectionFont = font.ToTkFont()
    
    def on_red_click(self, sender, event):
        """Change selected text color to red"""
        self.richtextbox.SelectionColor = Color.Red
    
    def on_blue_click(self, sender, event):
        """Change selected text color to blue"""
        self.richtextbox.SelectionColor = Color.Blue
    
    def on_green_click(self, sender, event):
        """Change selected text color to green"""
        self.richtextbox.SelectionColor = Color.Green
    
    def on_custom_color_click(self, sender, event):
        """Open color picker and apply selected color to text"""
        color_dialog = ColorDialog()
        color_dialog.Color = Color(Color.Black)  # Default color
        
        if color_dialog.ShowDialog(self) == DialogResult.OK:
            # The Color class now accepts the color from the dialog directly
            selected_color = color_dialog.Color
            self.richtextbox.SelectionColor = selected_color
            
            # Update button background to show selected color
            sender.BackColor = selected_color
            
            # Show confirmation message with RGB values
            MessageBox.Show(
                f"Selected Color: {selected_color}\nRGB: ({selected_color.R}, {selected_color.G}, {selected_color.B})",
                "Color Selected",
                "OK",
                "Information"
            )
    
    def on_clear_format_click(self, sender, event):
        """Clear formatting from selected text"""
        # Restore default font (TkDefaultFont is the system default)
        from tkinter import font as tkfont
        default_font = tkfont.nametofont("TkDefaultFont")
        self.richtextbox.SelectionFont = default_font
        self.richtextbox.SelectionColor = "black"
    
    def on_clear_all_click(self, sender, event):
        """Clear all text"""
        self.richtextbox.Clear()
    
    def on_get_values_click(self, sender, event):
        """Display all current values"""
        message = "Current Values:\n\n"
        message += f"LinkLabel 1 Visited: {self.link1.LinkVisited}\n"
        message += f"LinkLabel 2 Visited: {self.link2.LinkVisited}\n\n"
        message += f"DomainUpDown: {self.domain_updown.Text}\n"
        message += f"DomainUpDown Index: {self.domain_updown.SelectedIndex}\n\n"
        message += f"NumericUpDown 1: {self.numeric_updown1.Value}\n"
        message += f"NumericUpDown 2: {self.numeric_updown2.Value}\n\n"
        message += f"RichTextBox Length: {len(self.richtextbox.Text)} characters\n"
        message += f"RichTextBox Lines: {len(self.richtextbox.Lines)} lines"
        
        MessageBox.Show(message, "Current Values", "OK", "Information")
    
    def on_reset_click(self, sender, event):
        """Reset all controls to default values"""
        # Reset LinkLabels
        self.link1.LinkVisited = False
        self.link2.LinkVisited = False
        
        # Reset DomainUpDown
        self.domain_updown.SelectedIndex = 0
        
        # Reset NumericUpDowns
        self.numeric_updown1.Value = 50
        self.numeric_updown2.Value = 5.5
        
        # Reset RichTextBox
        self.richtextbox.Clear()
        self.richtextbox.Text = "Welcome to RichTextBox!\n\n"
        self.richtextbox.Text += "This control supports rich text formatting.\n"
        self.richtextbox.Text += "You can change font, color, and style.\n\n"
        self.richtextbox.Text += "Try typing here and using the buttons below to format text."
        
        MessageBox.Show("All controls have been reset!", "Reset", "OK", "Information")


if __name__ == "__main__":
    form = MoreControlsForm()
    form.ShowDialog()

