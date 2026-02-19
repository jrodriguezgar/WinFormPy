# WinUI 3 for WinFormPy

Modern controls following the Windows 11 Fluent Design System. These controls are pre-styled with modern typography, accent coloring, and a clean visual language.

## Module: `winui3.py`

All WinUI 3 controls inherit from WinFormPy base controls and apply Fluent Design styling automatically.

## Control Naming
WinUI 3 controls use the official naming from the Windows App SDK:

- `TextBlock` (instead of `Label`)
- `Button` (WinUI 3 accent style)
- `TextBox` (accent underline on focus)
- `InfoBar` (inline notification banner)
- `InfoBadge` (severity-colored badge)
- `NumberBox` (numeric input with spinner)
- `ProgressBar` (thin accent line)
- `ProgressRing` (circular animated indicator)
- `ToggleSwitch` (capsule on/off switch)
- `Expander` (collapsible container)
- `HyperlinkButton` (link-styled button)
- `Slider` (accent-colored slider)
- `BreadcrumbBar` (path navigation with separators)

## Theme Integration
The module is fully integrated with `winformpy.themes.winui3_theme`.

```python
from winformpy.winui3 import Button, TextBlock, Panel, Colors, Fonts

btn = Button(form, {"Text": "Modern Button", "ButtonStyle": "Accent"})
lbl = TextBlock(form, {"Text": "Fluent Header", "Typography": Fonts.Title})
card = Card(form, {"Width": 300, "Height": 200})
```

## Available Components

### Input Controls
| Component | WinForms Equivalent | Description |
| --- | --- | --- |
| **Button** | Button | Accent/Success/Warning/Danger/Standard styles |
| **TextBox** | TextBox | Accent underline on focus |
| **CheckBox** | CheckBox | WinUI 3 styling and hover |
| **RadioButton** | RadioButton | WinUI 3 styling and hover |
| **ComboBox** | ComboBox | Clean dropdown |
| **NumberBox** | NumericUpDown | Numeric input with up/down buttons |
| **ToggleSwitch** | CheckBox (switch) | Animated capsule toggle |
| **Slider** | TrackBar | Accent-colored slider with thumb |
| **HyperlinkButton** | LinkLabel | Underline-on-hover hyperlink button |

### Display Controls
| Component | WinForms Equivalent | Description |
| --- | --- | --- |
| **TextBlock** | Label | Typography presets (Title, Subtitle, Body, Caption) |
| **InfoBadge** | — | Severity-colored notification dot/number |
| **InfoBar** | — | Inline notification with title, message, close |
| **ProgressBar** | ProgressBar | Thin accent progress line |
| **ProgressRing** | — | Circular animated progress indicator |
| **PersonPicture** | — | Circular avatar with initials |
| **RatingControl** | — | Star rating selector |

### Container Controls
| Component | WinForms Equivalent | Description |
| --- | --- | --- |
| **Panel** | Panel | Card-style background |
| **Card** | — | Panel with subtle border |
| **Expander** | — | Collapsible header + content |
| **StackPanel** | FlowLayoutPanel | Vertical/horizontal auto-stacking |
| **TabView** | TabControl | Modern tab interface with accent bar |

### Navigation Controls
| Component | WinForms Equivalent | Description |
| --- | --- | --- |
| **BreadcrumbBar** | — | Path segments with clickable links |

## Button Styles

```python
from winformpy.winui3 import Button

# Available ButtonStyle values: Accent, Success, Warning, Danger, Standard
btn_accent = Button(form, {"Text": "Primary", "ButtonStyle": "Accent"})
btn_success = Button(form, {"Text": "Save", "ButtonStyle": "Success"})
btn_danger = Button(form, {"Text": "Delete", "ButtonStyle": "Danger"})
btn_std = Button(form, {"Text": "Cancel", "ButtonStyle": "Standard"})
```

## InfoBar Severities

```python
from winformpy.winui3 import InfoBar
from winformpy import DockStyle

# Severity values: Informational, Success, Warning, Error
bar = InfoBar(form, {
    "Title": "Update Available",
    "Message": "Version 2.0 is ready.",
    "Severity": "Informational",
    "Dock": DockStyle.Top
})
```

## ToggleSwitch

```python
from winformpy.winui3 import ToggleSwitch

switch = ToggleSwitch(form, text="Dark Mode", on_toggle=lambda state: print(state))
switch.IsOn = True  # Set state programmatically
```

## Colors and Fonts

Access the theme constants directly:

```python
from winformpy.winui3 import WinUIColors, WinUIFonts

# Colors
WinUIColors.Accent       # "#0078D4"
WinUIColors.AccentText   # "#FFFFFF"
WinUIColors.TextPrimary  # "#000000"
WinUIColors.WindowBg     # "#FFFFFF"
WinUIColors.SuccessText  # "#107C10"
WinUIColors.ErrorText    # "#C42B1C"

# Fonts
WinUIFonts.Title         # ("Segoe UI", 28, "bold")
WinUIFonts.Subtitle      # ("Segoe UI", 16, "bold")
WinUIFonts.Body          # ("Segoe UI", 14, "normal")
WinUIFonts.Caption       # ("Segoe UI", 12, "normal")
```

## Note on Canvas Usage

Some controls (`ProgressRing`, `ToggleSwitch`, `Slider`) use direct `tk.Canvas` access internally for custom drawing (arcs, capsule shapes, slider tracks). This is noted in the source as an exception — WinFormPy does not yet provide a general-purpose Canvas control.

See `templates/winui3_template.py` for a full interactive gallery.
