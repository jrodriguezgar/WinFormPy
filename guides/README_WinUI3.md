# WinUI 3 Controls for WinFormPy

## Overview

The `winui3.py` module provides Windows 11 styled controls that follow the WinUI 3 design system. These controls inherit from WinFormPy base controls and apply modern visual styling consistent with Windows 11 applications.

## Design Principles

WinUI 3 controls follow these design principles:

- **Segoe UI Typography**: All controls use the Segoe UI font family with proper type ramp
- **Accent Color**: Primary accent color is `#0078D4` (blue)
- **Minimal Borders**: Clean appearance with emphasis on content over chrome
- **Flat Design**: No 3D effects, simple and modern
- **Proper Spacing**: Consistent padding and margins

## Color Palette

### WinUIColors

The `WinUIColors` class provides the complete WinUI 3 color palette:

```python
from winformpy.winui3 import WinUIColors

# Primary accent colors
WinUIColors.Accent = "#0078D4"
WinUIColors.AccentText = "#FFFFFF"

# Text colors
WinUIColors.TextPrimary = "#000000"
WinUIColors.TextSecondary = "#666666"

# Background colors
WinUIColors.WindowBg = "#FFFFFF"
WinUIColors.CardBg = "#FFFFFF"

# State colors
WinUIColors.ErrorText = "#C42B1C"
WinUIColors.WarningText = "#9D5D00"
WinUIColors.SuccessText = "#107C10"
```

## Typography

### WinUIFonts

The `WinUIFonts` class provides the WinUI 3 type ramp:

```python
from winformpy.winui3 import WinUIFonts

# Display and titles
WinUIFonts.Display = ("Segoe UI", 68, "normal")
WinUIFonts.Title = ("Segoe UI", 28, "bold")
WinUIFonts.Subtitle = ("Segoe UI", 16, "bold")

# Body text
WinUIFonts.Body = ("Segoe UI", 14, "normal")
WinUIFonts.BodyStrong = ("Segoe UI", 14, "bold")

# Captions
WinUIFonts.Caption = ("Segoe UI", 12, "normal")
```

## Available Controls

### WinUIButton

Button with WinUI 3 accent styling and multiple style options.

```python
from winformpy.winui3 import WinUIButton

# Default accent button
btn = WinUIButton(form, {
    'Text': 'Click Me',
    'Width': 120,
    'Height': 32
})
btn.Click = lambda s, e: print("Clicked!")

# Button with specific style
btn_success = WinUIButton(form, {
    'Text': 'Save',
    'ButtonStyle': 'Success'
})

btn_danger = WinUIButton(form, {
    'Text': 'Delete',
    'ButtonStyle': 'Danger'
})

# Custom accent color
btn.AccentColor = '#0078D4'

# Change button style dynamically
btn.ButtonStyle = 'Warning'
```

**Features:**
- Multiple button styles: **Accent** (default blue), **Success** (green), **Warning** (orange), **Danger** (red), **Standard** (white with border)
- Flat style with no borders (except Standard)
- Customizable accent color
- ButtonStyle property for easy style changes

---

### WinUILabel

Label with WinUI 3 typography support.

```python
from winformpy.winui3 import WinUILabel, WinUIFonts

# Using typography presets
title = WinUILabel(form, {
    'Text': 'Title Text',
    'Typography': WinUIFonts.Title
})

subtitle = WinUILabel(form, {
    'Text': 'Subtitle',
    'Typography': WinUIFonts.Subtitle
})

# Change typography
title.Typography = WinUIFonts.Display
```

**Features:**
- Segoe UI font by default
- Typography presets (Title, Subtitle, Body, Caption)
- TextPrimary color by default

---

### WinUITextBox

TextBox with accent underline that responds to focus.

```python
from winformpy.winui3 import WinUITextBox

txt = WinUITextBox(form, {
    'Width': 200,
    'Height': 32
})

# Custom underline color (when focused)
txt.UnderlineColor = '#00FF00'
```

**Features:**
- Thin underline at the bottom (2px)
- Gray color when idle, accent color when focused (interactive feedback)
- No visible borders
- Customizable underline color via UnderlineColor property
- All TextBox functionality

---

### WinUIProgressBar

ProgressBar with accent colors.

```python
from winformpy.winui3 import WinUIProgressBar

pb = WinUIProgressBar(form, {
    'Width': 200,
    'Height': 4,
    'Value': 50
})

# Custom colors
pb.BarColor = '#0078D4'
pb.TroughColor = '#E5E5E5'
```

**Features:**
- Blue accent bar color
- Light gray trough
- Thin 4px height (WinUI 3 style)
- Customizable colors

---

### WinUIToggleSwitch

Toggle switch control with capsule design.

```python
from winformpy.winui3 import WinUIToggleSwitch

switch = WinUIToggleSwitch(
    parent=form,
    text="Enable Feature",
    on_toggle=lambda state: print(f"State: {state}")
)

# Get/set state
if switch.IsOn:
    print("Switch is ON")

switch.IsOn = True  # Set without triggering callback
```

**Features:**
- Capsule-shaped switch
- Blue accent when ON
- Text label on right
- Callback support
- Inherits parent background

---

### WinUIExpander

Collapsible container with header.

```python
from winformpy.winui3 import WinUIExpander, WinUILabel

expander = WinUIExpander(
    parent=form,
    title="Advanced Settings",
    height_expanded=200
)

# Add controls to content
lbl = WinUILabel(expander.content, {
    'Text': 'Content goes here'
})
```

**Features:**
- Clickable header with arrow
- Blue accent color
- Collapsible content area
- Blue accent border
- Inherits parent background

---

### WinUICheckBox

CheckBox with accent color.

```python
from winformpy.winui3 import WinUICheckBox

chk = WinUICheckBox(form, {
    'Text': 'Enable feature',
    'Checked': True
})
```

**Features:**
- Blue accent when checked
- Segoe UI font
- All CheckBox functionality

---

### WinUIRadioButton

RadioButton with accent color.

```python
from winformpy.winui3 import WinUIRadioButton

rb1 = WinUIRadioButton(form, {
    'Text': 'Option 1',
    'Checked': True
})

rb2 = WinUIRadioButton(form, {
    'Text': 'Option 2'
})
```

**Features:**
- Blue accent when selected
- Segoe UI font
- All RadioButton functionality

---

### WinUIComboBox

ComboBox with WinUI 3 styling.

```python
from winformpy.winui3 import WinUIComboBox

combo = WinUIComboBox(form, {
    'Width': 200,
    'Items': ['Option 1', 'Option 2', 'Option 3']
})
combo.SelectedIndex = 0
```

**Features:**
- Segoe UI font
- Clean border styling
- 32px height
- All ComboBox functionality

---

### WinUIPanel

Panel with card background.

```python
from winformpy.winui3 import WinUIPanel

card = WinUIPanel(form, {
    'Width': 300,
    'Height': 200
})
```

**Features:**
- White card background
- Optional border
- All Panel functionality

---

### WinUISlider

Slider control with Windows 11 aesthetics.

```python
from winformpy.winui3 import WinUISlider

slider = WinUISlider(form, {
    'Width': 200,
    'Left': 20,
    'Top': 50
})

# Access slider value (0.0 to 1.0)
print(f"Value: {slider._value}")
```

**Features:**
- Accent-colored progress line
- Gray background track
- Circular thumb with white border
- Draggable thumb control
- Value range: 0.0 to 1.0

---

### WinUIHyperlinkButton

Button that looks and behaves like a hyperlink.

```python
from winformpy.winui3 import WinUIHyperlinkButton

link = WinUIHyperlinkButton(form, {
    'Text': 'Learn more',
    'Left': 20,
    'Top': 100
})
link.Click = lambda s, e: print("Link clicked")
```

**Features:**
- Accent-colored text (blue)
- Transparent background
- Hand cursor on hover
- Underline effect on hover
- Darker accent color when active

---

## Complete Example

```python
from winformpy.winformpy import Form, DockStyle
from winformpy.winui3 import (
    WinUIButton, WinUILabel, WinUITextBox,
    WinUIToggleSwitch, WinUIColors, WinUIFonts
)

class MyForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "WinUI 3 Example"
        self.Width = 400
        self.Height = 300
        self.BackColor = WinUIColors.WindowBg
        self.ApplyLayout()
        
        # Title
        title = WinUILabel(self, {
            'Text': 'My Application',
            'Typography': WinUIFonts.Title,
            'Left': 20,
            'Top': 20,
            'AutoSize': True
        })
        
        # TextBox
        txt = WinUITextBox(self, {
            'Left': 20,
            'Top': 80,
            'Width': 250,
            'Height': 32
        })
        
        # Button
        btn = WinUIButton(self, {
            'Text': 'Submit',
            'Left': 20,
            'Top': 130,
            'Width': 100,
            'Height': 32
        })
        btn.Click = lambda s, e: print(f"Value: {txt.Text}")
        
        # Toggle
        switch = WinUIToggleSwitch(
            self,
            text="Enable dark mode",
            on_toggle=lambda state: print(f"Dark mode: {state}")
        )
        switch.Location = (20, 180)

if __name__ == '__main__':
    form = MyForm()
    form.ShowDialog()
```

## Best Practices

### 1. Use Typography Presets

Instead of setting fonts manually, use the typography presets:

```python
# ✅ Good
label.Typography = WinUIFonts.Title

# ❌ Avoid
label.Font = ("Segoe UI", 28, "bold")
```

### 2. Use Color Constants

Use the predefined color constants for consistency:

```python
# ✅ Good
panel.BackColor = WinUIColors.CardBg
label.ForeColor = WinUIColors.TextSecondary

# ❌ Avoid
panel.BackColor = "#FFFFFF"
label.ForeColor = "#666666"
```

### 3. Consistent Sizing

Follow WinUI 3 sizing guidelines:

- **Buttons**: 32px height
- **TextBoxes**: 32px height
- **ProgressBars**: 4px height
- **Spacing**: Use multiples of 4px (4, 8, 12, 16, 20, 24...)

### 4. Background Inheritance

WinUI 3 controls that contain other controls (ToggleSwitch, Expander) automatically inherit the background color from their parent. Set the parent's background first:

```python
# Set parent background
panel.BackColor = '#F3F3F3'

# Controls inherit automatically
switch = WinUIToggleSwitch(panel, text="Toggle")
```

## Migration from Standard Controls

To convert existing code to use WinUI 3 controls:

1. **Import WinUI 3 controls**:
   ```python
   from winformpy.winui3 import WinUIButton, WinUILabel
   ```

2. **Replace control names**:
   ```python
   # Before
   btn = Button(form, {'Text': 'Click'})
   
   # After
   btn = WinUIButton(form, {'Text': 'Click'})
   ```

3. **Apply WinUI colors** (optional):
   ```python
   form.BackColor = WinUIColors.WindowBg
   ```

4. **Use typography presets** (optional):
   ```python
   label.Typography = WinUIFonts.Title
   ```

## See Also

- [WinFormPy Documentation](../README.md)
- [Example: winui3_example.py](../examples/winui3_example.py)
- [Microsoft WinUI 3 Design Guidelines](https://docs.microsoft.com/en-us/windows/apps/design/)
