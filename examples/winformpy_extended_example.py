"""
Example of using ExtendedLabel from winformpy_extended.
"""
import sys
import os

# Add the winformpy directory to sys.path
# This script is in pentano/gui/windows/examples/
# winformpy is in pentano/gui/windows/winformpy/
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up to 'windows' then down to 'winformpy'
winformpy_dir = os.path.join(os.path.dirname(current_dir), 'winformpy')
sys.path.insert(0, winformpy_dir)

try:
    from winformpy import Form, AnchorStyles, Button, ContentAlignment
    from winformpy_extended import ExtendedLabel
except ImportError as e:
    print(f"Error importing winformpy: {e}")
    print(f"sys.path: {sys.path}")
    sys.exit(1)

def main():
    form = Form({
        'Text': 'Extended Label Example',
        'Width': 500,
        'Height': 450
    })
    
    # Instructions
    lbl_info = ExtendedLabel(form, {
        'Text': "Resize the window to see the text wrap dynamically. Use buttons below to change alignment.",
        'Left': 10,
        'Top': 10,
        'Width': 460,
        'Height': 40,
        'Anchor': AnchorStyles.Left | AnchorStyles.Right | AnchorStyles.Top,
        'TextAlign': 'TopLeft'
    })
    
    # The Extended Label
    long_text = (
        "This is an ExtendedLabel control. It is designed to wrap text automatically "
        "based on the width of the control. Unlike the standard Label with AutoSize=True, "
        "this control allows you to define the width (or anchor it) and the text will "
        "flow within those bounds.\n\n"
        "Try resizing the window horizontally! The text should re-wrap to fit the new width. "
        "This is useful for responsive layouts where you want text to fill the available space "
        "without expanding the control beyond its limits."
    )
    
    lbl_extended = ExtendedLabel(form, {
        'Text': long_text,
        'Left': 10,
        'Top': 60,
        'Width': 460,
        'Height': 200,
        'Anchor': AnchorStyles.Left | AnchorStyles.Right | AnchorStyles.Top | AnchorStyles.Bottom,
        'BorderStyle': 'FixedSingle', # Visible border to see the control bounds
        'TextAlign': 'TopLeft',
        'BackColor': '#f0f0f0'
    })
    
    # Buttons to change alignment
    def set_align_left(sender, e):
        lbl_extended.TextAlign = ContentAlignment.TopLeft
        
    def set_align_center(sender, e):
        lbl_extended.TextAlign = ContentAlignment.TopCenter
        
    def set_align_right(sender, e):
        lbl_extended.TextAlign = ContentAlignment.TopRight

    btn_left = Button(form, {
        'Text': 'Left Align',
        'Left': 10,
        'Top': 270,
        'Width': 100,
        'Anchor': AnchorStyles.Left | AnchorStyles.Bottom
    })
    btn_left.Click = set_align_left
    
    btn_center = Button(form, {
        'Text': 'Center Align',
        'Left': 120,
        'Top': 270,
        'Width': 100,
        'Anchor': AnchorStyles.Left | AnchorStyles.Bottom
    })
    btn_center.Click = set_align_center
    
    btn_right = Button(form, {
        'Text': 'Right Align',
        'Left': 230,
        'Top': 270,
        'Width': 100,
        'Anchor': AnchorStyles.Left | AnchorStyles.Bottom
    })
    btn_right.Click = set_align_right
    
    form.ShowDialog()

if __name__ == '__main__':
    main()
