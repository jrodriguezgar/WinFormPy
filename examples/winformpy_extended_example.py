"""
Example of using ExtendedLabel from winformpy_extended.
"""

from winformpy import (
    Form, Panel, Button, Application,
    AnchorStyles, ContentAlignment, DockStyle, Font, FontStyle
)
from winformpy.winformpy_extended import ExtendedLabel

def main():
    # =========================================================================
    # Create main form
    # =========================================================================
    form = Form({
        'Text': 'ExtendedLabel Example',
        'Width': 800,
        'Height': 600,
        'StartPosition': 'CenterScreen'
    })
    form.ApplyLayout()
    
    # =========================================================================
    # TOP PANEL - Title bar
    # =========================================================================
    top_panel = Panel(form, {
        'Height': 80,
        'BackColor': '#0078D4'
    })
    top_panel.Dock = DockStyle.Top
    
    ExtendedLabel(top_panel, {
        'Text': 'EXTENDED LABEL DEMONSTRATION',
        'Left': 20,
        'Top': 12,
        'AutoSize': True,
        'Font': Font('Segoe UI', 16, FontStyle.Bold),
        'ForeColor': '#FFFFFF',
        'BackColor': '#0078D4'
    })
    
    ExtendedLabel(top_panel, {
        'Text': 'Dynamic text wrapping with anchor support - Resize the window to see the effect',
        'Left': 20,
        'Top': 45,
        'AutoSize': True,
        'Font': Font('Segoe UI', 9),
        'ForeColor': '#E0E0E0',
        'BackColor': '#0078D4'
    })
    
    # =========================================================================
    # BOTTOM PANEL - Control buttons
    # =========================================================================
    bottom_panel = Panel(form, {
        'Height': 70,
        'BackColor': '#ECF0F1'
    })
    bottom_panel.Dock = DockStyle.Bottom
    
    ExtendedLabel(bottom_panel, {
        'Text': 'Text Alignment:',
        'Left': 20,
        'Top': 25,
        'AutoSize': True,
        'Font': Font('Segoe UI', 9, FontStyle.Bold),
        'BackColor': '#ECF0F1',
        'ForeColor': '#2C3E50'
    })
    
    # =========================================================================
    # MAIN PANEL - Content area
    # =========================================================================
    main_panel = Panel(form, {
        'BackColor': '#F5F5F5',
        'Padding': 20
    })
    main_panel.Dock = DockStyle.Fill
    
    # Instructions
    lbl_info = ExtendedLabel(main_panel, {
        'Text': '📋 Instructions: Resize the window to see the text wrap dynamically. Use buttons below to change alignment.',
        'Left': 20,
        'Top': 20,
        'Width': 740,
        'Height': 40,
        'Anchor': AnchorStyles.Left | AnchorStyles.Right | AnchorStyles.Top,
        'TextAlign': ContentAlignment.TopLeft,
        'BackColor': '#FFF9E6',
        'BorderStyle': 'FixedSingle',
        'Font': Font('Segoe UI', 9),
        'ForeColor': '#856404'
    })
    
    # The Extended Label
    long_text = (
        "This is an ExtendedLabel control. It is designed to wrap text automatically "
        "based on the width of the control. Unlike the standard Label with AutoSize=True, "
        "this control allows you to define the width (or anchor it) and the text will "
        "flow within those bounds.\n\n"
        "Try resizing the window horizontally! The text should re-wrap to fit the new width. "
        "This is useful for responsive layouts where you want text to fill the available space "
        "without expanding the control beyond its limits.\n\n"
        "Features:\n"
        "• Automatic text wrapping based on control width\n"
        "• Support for Anchor styles (Left, Right, Top, Bottom)\n"
        "• Configurable text alignment (Left, Center, Right)\n"
        "• Responsive to window resize events"
    )
    
    lbl_extended = ExtendedLabel(main_panel, {
        'Text': long_text,
        'Left': 20,
        'Top': 80,
        'Width': 740,
        'Height': 310,
        'Anchor': AnchorStyles.Left | AnchorStyles.Right | AnchorStyles.Top | AnchorStyles.Bottom,
        'BorderStyle': 'FixedSingle',
        'TextAlign': ContentAlignment.TopLeft,
        'BackColor': '#FFFFFF',
        'Font': Font('Segoe UI', 10),
        'ForeColor': '#2C3E50'
    })
    
    # Buttons to change alignment
    def set_align_left(sender, e):
        lbl_extended.TextAlign = ContentAlignment.TopLeft
        
    def set_align_center(sender, e):
        lbl_extended.TextAlign = ContentAlignment.TopCenter
        
    def set_align_right(sender, e):
        lbl_extended.TextAlign = ContentAlignment.TopRight

    btn_left = Button(bottom_panel, {
        'Text': '⬅️ Left Align',
        'Left': 140,
        'Top': 18,
        'Width': 120,
        'Height': 35,
        'BackColor': '#3498DB',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })
    btn_left.Click = set_align_left
    
    btn_center = Button(bottom_panel, {
        'Text': '↔️ Center Align',
        'Left': 270,
        'Top': 18,
        'Width': 130,
        'Height': 35,
        'BackColor': '#9B59B6',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })
    btn_center.Click = set_align_center
    
    btn_right = Button(bottom_panel, {
        'Text': 'Right Align ➡️',
        'Left': 410,
        'Top': 18,
        'Width': 130,
        'Height': 35,
        'BackColor': '#E74C3C',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })
    btn_right.Click = set_align_right
    
    # Run the application
    Application.Run(form)

if __name__ == '__main__':
    main()
