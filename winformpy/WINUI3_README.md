# WinUI 3 for WinFormPy

Modern controls following the Windows 11 Fluent Design System. These controls are pre-styled with rounded corners, modern typography, and accent coloring.

## Control Naming
WinUI 3 controls use the official naming from the Windows App SDK:

- `TextBlock` (instead of `Label`)
- `Button` (WinUI 3 style)
- `TextBox` (WinUI 3 style with accent underline)
- `InfoBar` (Notification banner)
- `ItemsView` (Modern ListBox/ListView)
- `NumberBox` (Modern NumericUpDown)
- `ProgressBar` (Modern clean line)
- `NavigationView` (Sidebar navigation)

## Theme Integration
The module is fully integrated with `winformpy.themes.winui3_theme`.

```python
from winformpy.winui3 import Form, Button, TextBlock, Colors, Fonts

form = Form()
btn = Button(form, {"Text": "Modern Button", "BackColor": Colors.Accent})
lbl = TextBlock(form, {"Text": "Fluent Header", "Typography": Fonts.Title})
```

## Available Components
| Component | WinForms Equivalent |
| --- | --- |
| **TextBlock** | Label |
| **ToggleSwitch** | CheckBox (Switch style) |
| **Expander** | Collapsible Panel |
| **InfoBar** | Status notification |
| **ContentDialog** | Modal overlay |

See `examples/winui3_example.py` for a full demonstration.
