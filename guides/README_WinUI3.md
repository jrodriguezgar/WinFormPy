# WinUI 3 (Fluent Design) for WinFormPy

WinFormPy includes a specialized module for creating applications with a **WinUI 3 (Fluent Design)** aesthetic, based on the Windows App SDK design system. This module provides a set of modern controls that inherit from the base WinFormPy controls but are pre-styled with Fluent Design properties like rounded corners, specific color palettes, and modern typography.

## Quick Start

To use the WinUI 3 styled controls, import them from the `winformpy.winui3` module:

```python
from winformpy.winui3 import (
    Form, Button, TextBlock, TextBox, 
    Colors, Fonts, InfoBar, InfoBarSeverity
)
from winformpy import Application, DockStyle

class MyModernForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "WinUI 3 App"
        self.Width = 600
        self.Height = 400
        self.ApplyLayout()

        # Modern TextBlock (Label)
        self.title = TextBlock(self, {
            'Text': 'Welcome to Fluent Design',
            'Dock': DockStyle.Top,
            'Height': 60,
            'Typography': Fonts.Title,
            'Padding': (20, 20)
        })

        # InfoBar for messages
        self.info = InfoBar(self, {
            'Title': 'Update Available',
            'Message': 'A new version of WinFormPy is ready to install.',
            'Severity': InfoBarSeverity.Informational,
            'IsOpen': True,
            'Dock': DockStyle.Top
        })

        # Modern Button
        self.btn = Button(self, {
            'Text': 'Click Me',
            'Left': 20,
            'Top': 150,
            'Width': 120,
            'Height': 32
        })

if __name__ == "__main__":
    app = MyModernForm()
    Application.Run(app)
```

## Theme System

WinFormPy uses a modular theme system located in `winformpy/themes/`. The `winui3` module uses the Fluent Design theme by default.

### Accessing Colors and Fonts

You can access the WinUI 3 color palette and typography ramp through the `Colors` and `Fonts` classes:

```python
from winformpy.winui3 import Colors, Fonts

# Using colors
my_button.BackColor = Colors.Accent
my_label.ForeColor = Colors.TextPrimary

# Using fonts
my_label.Typography = Fonts.Title  # Large title font
my_text.Typography = Fonts.Body    # Standard body font
```

### Available Themes
- **WinUI 3 (Fluent)**: `from winformpy.winui3 import Colors, Fonts` (or `from winformpy import winui_colors, winui_fonts`)
- **Windows Forms (Classic)**: `from winformpy import winforms_colors, winforms_fonts`

## Available Controls

The WinUI 3 module uses official Windows App SDK nomenclature. All controls inherit from their WinForm/Tkinter base but come pre-styled:

| WinUI 3 Control | WinFormPy Base | Description |
|-----------------|----------------|-------------|
| `Button` | `Button` | Modern button with rounded corners and hover states |
| `TextBlock` | `Label` | Read-only text display with modern typography |
| `TextBox` | `TextBox` | Text input with accent underline and focus states |
| `CheckBox` | `CheckBox` | Fluent-style toggle with checkmark |
| `RadioButton` | `RadioButton` | Fluent-style radio button |
| `NumberBox` | `NumericUpDown` | Modern numeric input (Spinner) |
| `ProgressBar` | `ProgressBar` | Clean, flat progress indicator (4px height) |
| `Slider` | `TrackBar` | Modern slider with rounded thumb |
| `ComboBox` | `ComboBox` | Styled dropdown selection |
| `ItemsView` | `ListView` | Modern list display with flat styling |
| `TreePropertyView`| `TreeView` | Modern tree hierarchy |
| `CalendarView` | `MonthCalendar` | Clean calendar display |
| `DatePicker` | `DatePicker` | Fluent date selection |
| `TimePicker` | `UserControl` | Specialized time selection control |
| `Expander` | `Panel` | Collapsible content container with arrow |
| `InfoBar` | `Panel` | Status/Notification banner (Info, Success, Warning, Error) |
| `ContentDialog` | `Form` | Modern overlay dialog with standard buttons |
| `NavigationView` | `UserControl` | Modern sidebar navigation |
| `HyperlinkButton`| `Button` | Button styled as a clickable link |
| `ToggleSwitch` | `UserControl` | Capsule-shaped ON/OFF switch |

## Key Differences from Standard Controls

1. **Official Naming**: Controls use WinUI 3 names (e.g., `TextBlock` instead of `Label`, `ItemsView` instead of `ListView`).
2. **Visual Properties**: Default `BackColor`, `ForeColor`, `Font`, and `BorderWidth` are pre-configured to match Fluent Design.
3. **Corner Radius**: Many controls implement simulated rounded corners.
4. **Interactive States**: WinUI 3 controls include built-in `MouseEnter` and `MouseLeave` handlers to manage hover and pressed visual states automatically.
5. **Base Inheritance**: For portability, you can still use standard properties:
   ```python
   # This is a WinUI 3 Button, but it's still a WinFormPy Button
   btn = Button(parent)
   btn.Left = 10 
   btn.Click = my_handler
   ```

## Legacy Compatibility

For projects migrating from older versions of WinFormPy that used the `WinUI*` prefixes, we provide aliases:

```python
from winformpy.winui3 import WinUIButton, WinUILabel, WinUITextBox

# These are now aliases to the unprefixed names
btn = WinUIButton(form, {'Text': 'Legacy OK'}) # Works as Button
```

## Best Practices

1. **Use WinUI Form**: Import `Form` from `winformpy.winui3` to get the correct background and window behavior.
2. **Typography**: Always use the `Typography` property with `Fonts` constants for consistent branding.
3. **Layout**: WinUI 3 looks best with ample spacing (usually multiples of 4px).
4. **Theming**: If you need to switch between Classic and Fluent styles, use the theme modules in `winformpy.themes`.
