"""
WinUI 3 Controls Example - Professional UX/UI Design
=====================================================

This example demonstrates all WinUI 3 styled controls with best practices:
- Zero overlapping: Strict Dock/Anchor layout system
- Proportional sizing: Responsive design that adapts to window size
- Consistent spacing: Professional appearance with defined constants
- Type-appropriate controls: Right widget for each data type
- Validation: Input validation for interactive elements

WinUI 3 controls follow Windows 11 design guidelines with:
- Segoe UI typography
- Blue accent color (#0078D4)
- Minimal borders
- Clean, modern appearance
- Card-based layout
- Consistent spacing (using 4px grid)

Controls demonstrated:
- Button: Button with multiple styles (Accent, Success, Warning, Danger, Standard)
- TextBlock: Label with typography support
- TextBox: TextBox with accent underline that responds to focus
- ProgressBar: ProgressBar with accent colors
- ToggleSwitch: Toggle switch control
- Expander: Collapsible container
- CheckBox: CheckBox with accent color
- RadioButton: RadioButton with accent color
- ComboBox: ComboBox with WinUI styling
- Panel: Panel with card background
- Slider: Slider with Windows 11 aesthetics
- HyperlinkButton: Button styled as hyperlink
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from winformpy.winformpy import Form, Panel as BasePanel, DockStyle, AnchorStyles, ScrollBars
from winformpy.winui3 import (
    Button, TextBlock, TextBox, ProgressBar,
    ToggleSwitch, Expander, CheckBox, RadioButton,
    ComboBox, Panel, Slider, HyperlinkButton,
    Colors, Fonts
)


class WinUI3ExampleForm(Form):
    """
    Main form demonstrating WinUI 3 controls with professional UX/UI design.
    
    Layout structure:
    - Header Panel (Dock.Top): Title and description - no overlap
    - Content Panel (Dock.Fill): Scrollable cards with consistent spacing
    - All controls use proper positioning to prevent visual conflicts
    """
    
    # Constants for consistent spacing (4px grid system)
    CARD_SPACING = 20      # Space between cards
    CARD_PADDING = 20      # Inner padding for cards
    SECTION_SPACING = 16   # Space between sections
    CONTROL_SPACING = 10   # Space between controls
    
    def __init__(self):
        super().__init__()
        self.Text = "WinUI 3 Controls Gallery"
        self.Width = 1170
        self.Height = 750
        self.BackColor = Colors.WindowBg
        self.StartPosition = 'CenterScreen'
        
        # Apply layout before adding controls (CRITICAL for Dock)
        self.ApplyLayout()
        
        # Header area with title and description (Dock.Top - no overlap)
        self.create_header()
        
        # Scrollable main content area (Dock.Fill - fills remaining space)
        self.content_panel = BasePanel(self, {
            'Dock': DockStyle.Fill,
            'BackColor': Colors.WindowBg,
            'AutoScroll': True
        })
        
        # Create cards with proper spacing to prevent overlap
        y_position = self.CARD_SPACING
        
        # Card 1: Buttons (left column)
        card1 = self.create_card("Buttons", y_position, 550, 160)
        self.add_buttons_content(card1)
        
        # Card 2: Selection Controls (right column, aligned with Card 1)
        card2 = self.create_card("Selection Controls", y_position, 560, 360, x_position=590)
        self.add_selection_content(card2)
        
        y_position += 180
        
        # Card 3: Input Controls (left column)
        card3 = self.create_card("Text Input", y_position, 550, 160)
        self.add_input_content(card3)
        
        y_position += 180
        
        # Card 4: Progress & Feedback (left column)
        card4 = self.create_card("Progress & Feedback", y_position, 550, 320)
        self.add_progress_content(card4)
        
        # Ensure we're below both columns to prevent overlap
        # Card Progress ends at y_position (380) + height (320) = 700
        y_position = 720
        
        # Card 5: Advanced Controls (full width - no overlap)
        card5 = self.create_card("Advanced Controls", y_position, 1130, 250)
        self.add_advanced_content(card5)
    
    def create_header(self):
        """
        Create header section with proper Dock positioning.
        Uses Dock.Top to prevent overlap with content area.
        """
        header_panel = BasePanel(self, {
            'Dock': DockStyle.Top,
            'Height': 120,
            'BackColor': Colors.WindowBg
        })
        
        # Title label with consistent spacing
        title = TextBlock(header_panel, {
            'Text': 'WinUI 3 Controls Gallery',
            'Typography': Fonts.TitleLarge,
            'Left': self.CARD_SPACING,
            'Top': self.CARD_SPACING,
            'AutoSize': True
        })
        
        # Subtitle with proper vertical spacing (Title size ~48px height + spacing)
        subtitle = TextBlock(header_panel, {
            'Text': 'Modern Windows 11 styled controls with professional UX/UI design',
            'Typography': Fonts.Body,
            'ForeColor': Colors.TextSecondary,
            'Left': self.CARD_SPACING,
            'Top': self.CARD_SPACING + 55,
            'Width': 1000,
            'AutoSize': False
        })
        
        # Debug Button (Right side of header)
        debug_btn = Button(header_panel, {
            'Text': 'Toggle Layout Traces',
            'Left': self.Width - 200,
            'Top': self.CARD_SPACING,
            'Width': 160,
            'Height': 32,
            'ButtonStyle': 'Standard'
        })
        debug_btn.Click = lambda s, e: self.toggle_debug_visuals()

    def toggle_debug_visuals(self):
        """Visual debug helper: highlights backgrounds of containers to see boundaries."""
        debug_color = "#FFE0E0"  # Light red for debugging
        self._debug_active = getattr(self, '_debug_active', False)
        
        target_color = debug_color if not self._debug_active else Colors.CardBg
        content_target_color = "#F0F0F0" if not self._debug_active else Colors.WindowBg
        
        # Update content panel
        self.content_panel.BackColor = content_target_color
        
        # Update all panels inside content (Cards)
        for ctrl in self.content_panel.Controls:
            if isinstance(ctrl, BasePanel):
                ctrl.BackColor = target_color
        
        self._debug_active = not self._debug_active
        status = "Active" if self._debug_active else "Inactive"
        self.show_notification(f"Visual Debug: {status}")
    
    def create_card(self, title, y_pos, width, height, x_position=None):
        """
        Create a card panel with title and content area.
        Uses consistent spacing to prevent overlap.
        
        Args:
            title: Card title text
            y_pos: Vertical position
            width: Card width
            height: Card height
            x_position: Horizontal position (defaults to CARD_SPACING)
        """
        if x_position is None:
            x_position = self.CARD_SPACING
        
        # Card container with proper positioning
        card = Panel(self.content_panel, {
            'Left': x_position,
            'Top': y_pos,
            'Width': width,
            'Height': height,
            'BackColor': Colors.CardBg
        })
        
        # Card title with consistent padding
        title_label = TextBlock(card, {
            'Text': title,
            'Typography': Fonts.Subtitle,
            'Left': self.CARD_PADDING,
            'Top': self.SECTION_SPACING,
            'AutoSize': True
        })
        
        # Divider line with proper spacing
        divider = BasePanel(card, {
            'Left': self.CARD_PADDING,
            'Top': 50,
            'Width': width - (self.CARD_PADDING * 2),
            'Height': 1,
            'BackColor': Colors.Border
        })
        
        # Content area properties (used by add_* methods)
        card._content_top = 68
        card._content_left = self.CARD_PADDING
        return card
    
    def add_buttons_content(self, card):
        """
        Add button examples with consistent spacing.
        Demonstrates type-appropriate control (Button) for action triggers.
        """
        button_width = 90
        button_height = 32
        button_spacing = self.CONTROL_SPACING
        
        # Calculate positions to prevent overlap
        buttons = [
            ('Accent', None, "Accent button clicked!"),
            ('Success', 'Success', "Success!"),
            ('Warning', 'Warning', "Warning!"),
            ('Danger', 'Danger', "Danger!"),
            ('Standard', 'Standard', "Standard button clicked!")
        ]
        
        for i, (text, style, message) in enumerate(buttons):
            x_pos = card._content_left + (i * (button_width + button_spacing))
            btn = Button(card, {
                'Text': text,
                'Left': x_pos,
                'Top': card._content_top,
                'Width': button_width,
                'Height': button_height,
                'ButtonStyle': style or 'Accent'
            })
            btn.Click = lambda s, e, msg=message: self.show_notification(msg)
        
        # Description with proper spacing
        desc = TextBlock(card, {
            'Text': 'WinUI buttons with multiple styles: Accent (blue), Success (green), Warning (orange), Danger (red), and Standard (white with border).',
            'Typography': Fonts.Caption,
            'ForeColor': Colors.TextSecondary,
            'Left': card._content_left,
            'Top': card._content_top + button_height + self.SECTION_SPACING,
            'Width': 520,
            'WrapLength': 520,
            'AutoSize': True
        })
    
    def add_input_content(self, card):
        """
        Add input control examples with proper spacing.
        Demonstrates type-appropriate control (TextBox) for string input.
        Includes basic validation on text change.
        """
        textbox_width = 220
        textbox_height = 32
        textbox_spacing = 20
        
        # Standard TextBox (String input)
        txt1 = TextBox(card, {
            'Left': card._content_left,
            'Top': card._content_top,
            'Width': textbox_width,
            'Height': textbox_height
        })
        txt1.Text = "Standard input"
        
        # Add validation on text change
        def validate_text1(sender, e):
            if len(txt1.Text) > 50:
                self.show_notification("Text exceeds maximum length (50 chars)")
        txt1.TextChanged = validate_text1
        
        # TextBox with custom underline (positioned to prevent overlap)
        txt2 = TextBox(card, {
            'Left': card._content_left + textbox_width + textbox_spacing,
            'Top': card._content_top,
            'Width': textbox_width,
            'Height': textbox_height,
            'UnderlineColor': Colors.SuccessText
        })
        txt2.Text = "Custom accent color"
        
        # Description with proper vertical spacing
        desc = TextBlock(card, {
            'Text': 'WinUI TextBox with thin accent underline and no borders.\nFocuses on content with minimal visual chrome. Max 50 characters.',
            'Typography': Fonts.Caption,
            'ForeColor': Colors.TextSecondary,
            'Left': card._content_left,
            'Top': card._content_top + textbox_height + self.SECTION_SPACING,
            'Width': 520,
            'WrapLength': 520,
            'AutoSize': True
        })
    
    def add_selection_content(self, card):
        """
        Add selection control examples with consistent spacing.
        Demonstrates type-appropriate controls:
        - CheckBox for Boolean (multiple selections)
        - RadioButton for Enum (single selection from group)
        - ComboBox for Enum (dropdown selection)
        """
        # Constants for layout
        checkbox_spacing = 32
        column_spacing = 270
        section_gap = 160
        
        # CheckBoxes section (Boolean type - multiple selections allowed)
        chk_label = TextBlock(card, {
            'Text': 'CheckBoxes (Boolean):',
            'Typography': Fonts.BodyStrong,
            'Left': card._content_left,
            'Top': card._content_top,
            'AutoSize': True
        })
        
        # Create checkboxes with consistent spacing
        checkbox_options = ['Enable feature A', 'Enable feature B', 'Enable feature C']
        self.checkboxes = []
        for i, text in enumerate(checkbox_options):
            chk = CheckBox(card, {
                'Text': text,
                'Left': card._content_left,
                'Top': card._content_top + checkbox_spacing + (i * checkbox_spacing),
                'AutoSize': True,
                'Checked': i == 0  # First one checked by default
            })
            # Add change handler for validation
            chk.CheckedChanged = lambda s, e, option=text: self.on_checkbox_changed(option, s.Checked)
            self.checkboxes.append(chk)
        
        # RadioButtons section (Enum type - single selection from group)
        rb_label = TextBlock(card, {
            'Text': 'RadioButtons (Enum):',
            'Typography': Fonts.BodyStrong,
            'Left': card._content_left + column_spacing,
            'Top': card._content_top,
            'AutoSize': True
        })
        
        # Create radio buttons with consistent spacing
        radio_options = ['Option 1', 'Option 2', 'Option 3']
        self.radiobuttons = []
        for i, text in enumerate(radio_options):
            rb = RadioButton(card, {
                'Text': text,
                'Left': card._content_left + column_spacing,
                'Top': card._content_top + checkbox_spacing + (i * checkbox_spacing),
                'AutoSize': True,
                'Checked': i == 0  # First one checked by default
            })
            # Add change handler for validation
            rb.CheckedChanged = lambda s, e, option=text: self.on_radio_changed(option, s.Checked)
            self.radiobuttons.append(rb)
        
        # ComboBox section (Enum type - dropdown selection)
        combo_label = TextBlock(card, {
            'Text': 'ComboBox (Enum):',
            'Typography': Fonts.BodyStrong,
            'Left': card._content_left,
            'Top': card._content_top + section_gap,
            'AutoSize': True
        })
        
        self.combo_os = ComboBox(card, {
            'Left': card._content_left,
            'Top': card._content_top + section_gap + checkbox_spacing,
            'Width': 220,
            'Height': 32,
            'Items': ['Windows 11', 'Windows 10', 'Windows 8.1', 'Windows 7']
        })
        self.combo_os.SelectedIndex = 0
        
        # Add selection changed handler
        def on_combo_changed(sender, e):
            selected = self.combo_os.Text
            self.show_notification(f"OS Selected: {selected}")
        self.combo_os.SelectedIndexChanged = on_combo_changed
        
        # Description with proper spacing
        desc = TextBlock(card, {
            'Text': 'Selection controls with accent color when selected.\nUse appropriate control type for data type.',
            'Typography': Fonts.Caption,
            'ForeColor': Colors.TextSecondary,
            'Left': card._content_left + column_spacing,
            'Top': card._content_top + section_gap + checkbox_spacing,
            'Width': 260,
            'WrapLength': 260,
            'AutoSize': True
        })
    
    def on_checkbox_changed(self, option, checked):
        """Handle checkbox state changes with validation."""
        state = "selected" if checked else "unselected"
        self.show_notification(f"CheckBox {option}: {state}")
        
    def on_radio_changed(self, option, checked):
        """Handle radio button selection changes."""
        if checked: # Only notify when selected
            self.show_notification(f"RadioButton {option}: selected")
    
    def add_progress_content(self, card):
        """
        Add progress and feedback control examples with proper spacing.
        Demonstrates type-appropriate controls:
        - ProgressBar for Integer (0-100 progress value)
        - ToggleSwitch for Boolean (on/off state)
        - Slider for Decimal (range value)
        """
        # Constants for consistent spacing
        row_spacing = 60
        column_offset = 250
        
        # ProgressBar section (Integer: 0-100)
        pb_label = TextBlock(card, {
            'Text': 'ProgressBar (Integer 0-100):',
            'Typography': Fonts.BodyStrong,
            'Left': card._content_left,
            'Top': card._content_top,
            'AutoSize': True
        })
        
        self.progress = ProgressBar(card, {
            'Left': card._content_left,
            'Top': card._content_top + 30,
            'Width': 360,
            'Height': 4,
            'Value': 65
        })
        
        # Percentage label (validates range: 0-100)
        self.progress_label = TextBlock(card, {
            'Text': '65%',
            'Left': card._content_left + 370,
            'Top': card._content_top + 25,
            'AutoSize': True,
            'Typography': Fonts.Caption
        })
        
        # ToggleSwitches section (Boolean: True/False)
        switch_label = TextBlock(card, {
            'Text': 'Toggle Switches (Boolean):',
            'Typography': Fonts.BodyStrong,
            'Left': card._content_left,
            'Top': card._content_top + row_spacing,
            'AutoSize': True
        })
        
        # Create toggle switches with proper spacing
        switch1 = ToggleSwitch(
            card,
            text="Enable dark mode",
            on_toggle=lambda state: self.on_switch_toggle("Dark mode", state)
        )
        switch1.Location = (card._content_left, card._content_top + row_spacing + 30)
        
        switch2 = ToggleSwitch(
            card,
            text="Enable notifications",
            on_toggle=lambda state: self.on_switch_toggle("Notifications", state)
        )
        switch2.Location = (card._content_left + column_offset, card._content_top + row_spacing + 30)
        
        # Animate progress button (positioned to avoid overlap)
        btn_animate = Button(card, {
            'Text': 'Animate Progress',
            'Left': card._content_left,
            'Top': card._content_top + row_spacing * 2 + 10,
            'Width': 140,
            'Height': 32
        })
        btn_animate.Click = lambda s, e: self.animate_progress()
        
        # Slider section (Decimal: range value)
        slider_label = TextBlock(card, {
            'Text': 'Slider (Decimal 0-100):',
            'Typography': Fonts.BodyStrong,
            'Left': card._content_left + column_offset,
            'Top': card._content_top + row_spacing * 2 + 10,
            'AutoSize': True
        })
        
        self.slider = Slider(card, {
            'Width': 200,
            'Left': card._content_left + column_offset,
            'Top': card._content_top + row_spacing * 2 + 50
        })
        
        # Slider value label
        self.slider_label = TextBlock(card, {
            'Text': '50',
            'Left': card._content_left + column_offset + 210,
            'Top': card._content_top + row_spacing * 2 + 50,
            'Width': 30,
            'Height': 20,
            'AutoSize': False,
            'Typography': Fonts.Caption
        })
        
        # Hyperlink Button (positioned below other controls)
        link = HyperlinkButton(card, {
            'Text': 'Learn more about WinUI 3',
            'Left': card._content_left,
            'Top': card._content_top + row_spacing * 2 + 90,
            'Width': 200,
            'Height': 32
        })
        link.Click = lambda s, e: self.show_notification("Link clicked!")
    
    def add_advanced_content(self, card):
        """
        Add advanced control examples with proper spacing.
        Demonstrates collapsible containers with validation.
        """
        # Constants for layout
        expander_spacing = 565
        inner_padding = 16
        
        # Expander 1 - Basic Settings
        expander1 = Expander(
            card,
            title="Basic Settings (String Input with Validation)",
            height_expanded=160
        )
        expander1.Location = (card._content_left, card._content_top)
        expander1.Width = 500
        
        # Content for expander 1 with validation
        exp1_txt = TextBox(expander1.content, {
            'Left': inner_padding,
            'Top': inner_padding,
            'Width': 300,
            'Height': 32
        })
        exp1_txt.Text = "Enter your name"
        
        # Save button with validation
        exp1_btn = Button(expander1.content, {
            'Text': 'Save',
            'Left': 326,
            'Top': inner_padding,
            'Width': 80,
            'Height': 32
        })
        
        # Validation function
        def save_with_validation(s, e):
            name = exp1_txt.Text.strip()
            # Validate: string type, not empty, min 2 chars, max 50 chars
            if not name or name == "Enter your name":
                self.show_notification("⚠ Name is required!")
            elif len(name) < 2:
                self.show_notification("⚠ Name must be at least 2 characters")
            elif len(name) > 50:
                self.show_notification("⚠ Name must not exceed 50 characters")
            elif not name.replace(" ", "").isalpha():
                self.show_notification("⚠ Name must contain only letters")
            else:
                self.show_notification(f"✓ Saved: {name}")
        
        exp1_btn.Click = save_with_validation
        
        # Help text
        exp1_label = TextBlock(expander1.content, {
            'Text': 'Enter your name (2-50 letters). Click Save to validate.\nClick the header above to collapse this section.',
            'Typography': Fonts.Caption,
            'ForeColor': Colors.TextSecondary,
            'Left': inner_padding,
            'Top': 60,
            'Width': 460,
            'WrapLength': 460,
            'AutoSize': True
        })
        
        # Expander 2 - Info Card (positioned to prevent overlap)
        expander2 = Expander(
            card,
            title="Information Panel",
            height_expanded=200
        )
        expander2.Location = (card._content_left + expander_spacing, card._content_top)
        expander2.Width = 500
        
        # Info panel inside expander with proper spacing
        info_panel = Panel(expander2.content, {
            'Left': inner_padding,
            'Top': inner_padding,
            'Width': 468,
            'Height': 140,
            'BackColor': Colors.InfoBg
        })
        
        info_title = TextBlock(info_panel, {
            'Text': 'ℹ️  Design Principles',
            'Typography': Fonts.BodyStrong,
            'ForeColor': Colors.InfoText,
            'Left': inner_padding,
            'Top': 12,
            'AutoSize': True
        })
        
        info_text = TextBlock(info_panel, {
            'Text': 'This example demonstrates professional UX/UI:\n• Zero overlap with strict layout system\n• Consistent spacing using defined constants\n• Type-appropriate controls with validation',
            'Typography': Fonts.Caption,
            'ForeColor': Colors.InfoText,
            'Left': inner_padding,
            'Top': 36,
            'Width': 436,
            'WrapLength': 436,
            'AutoSize': True
        })
    
    def show_notification(self, message):
        """
        Display a notification message in the title bar.
        Provides user feedback for actions and validations.
        """
        original_title = "WinUI 3 Controls Gallery"
        self.Text = f"{original_title} • {message}"
        # Reset title after 2.5 seconds using WinFormPy InvokeAsync
        self.InvokeAsync(lambda: setattr(self, 'Text', original_title), 2500)
    
    def on_switch_toggle(self, name, state):
        """
        Handle toggle switch state changes.
        Demonstrates Boolean type validation.
        """
        # Validate: state must be Boolean type
        if not isinstance(state, bool):
            self.show_notification(f"⚠ Error: Invalid state type for {name}")
            return
        
        state_text = "ON" if state else "OFF"
        self.show_notification(f"{name}: {state_text}")
    
    def animate_progress(self):
        """
        Animate the progress bar from 0 to 100.
        Demonstrates Integer type validation (0-100 range).
        """
        def update_progress(value):
            # Validate: value must be integer in range 0-100
            if not isinstance(value, int):
                self.show_notification("⚠ Error: Progress value must be integer")
                return
            
            if value < 0 or value > 100:
                self.show_notification("⚠ Error: Progress must be 0-100")
                return
            
            if value <= 100:
                self.progress.Value = value
                self.progress_label.Text = f"{value}%"
                # Use WinFormPy InvokeAsync instead of _root.after
                self.InvokeAsync(lambda: update_progress(value + 1), 20)
            else:
                # Reset to 65%
                self.InvokeAsync(lambda: (
                    setattr(self.progress, 'Value', 65),
                    setattr(self.progress_label, 'Text', '65%')
                ), 500)
        
        # Start animation from 0 (validated integer)
        update_progress(0)


if __name__ == '__main__':
    form = WinUI3ExampleForm()
    form.ShowDialog()
