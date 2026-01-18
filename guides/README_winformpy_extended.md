# WinFormPy Extended

**Module:** `winformpy_extended.py`  
**Description:** Extension module for WinFormPy that provides custom controls, WinUI 3 styled controls, and advanced layout management capabilities not present in the core library.

---

## Standard Extended Controls

### ExtendedLabel

A specialized Label control designed for handling multiline text with dynamic wrapping and alignment capabilities. Unlike the standard `Label`, this control prioritizes the container's size over the text's size for layout calculations.

#### Key Features

*   **Dynamic Wrapping:** Text automatically wraps to fit the width of the control. If the control is resized (e.g., via Anchors), the text re-wraps instantly.
*   **Control-First Sizing:** `AutoSize` is set to `False` by default. The text flows within the bounds you define, rather than the control expanding to fit the text.
*   **Dynamic Alignment:** Supports changing `TextAlign` at runtime, properly updating both the anchor position and text justification.

#### Properties

| Property | Description | Default |
| :--- | :--- | :--- |
| `AutoSize` | Determines if the control resizes to fit its contents. Forced to `False` by default to enable wrapping within bounds. | `False` |
| `TextAlign` | Aligns the text within the control (e.g., `TopLeft`, `MiddleCenter`, `TopRight`). Updates `anchor` and `justify` behavior. | `TopLeft` |

#### Usage Example

```python
from winformpy import Form, AnchorStyles, ContentAlignment
from winformpy_extended import ExtendedLabel

# Create a form
form = Form({'Text': 'Extended Label Demo', 'Width': 400, 'Height': 300})

# Create an ExtendedLabel
lbl = ExtendedLabel(form, {
    'Text': "This is a long text that will automatically wrap...",
    'Left': 10,
    'Top': 10,
    'Width': 360,
    'Height': 100,
    'Anchor': AnchorStyles.Left | AnchorStyles.Right | AnchorStyles.Top,
    'TextAlign': ContentAlignment.TopLeft,
    'BorderStyle': 'FixedSingle'
})

# Change alignment dynamically
lbl.TextAlign = ContentAlignment.MiddleCenter

form.ShowDialog()
```

#### When to use

Use `ExtendedLabel` instead of `Label` when:
1.  You have a paragraph of text that needs to fit within a specific width.
2.  You want text to wrap automatically when the window is resized.
3.  You need multiline text with specific alignment that respects the control's boundaries.

---

## WinUI 3 Controls

All WinUI 3 styled controls use the `WinUI` prefix and follow Windows 11 Fluent Design guidelines.

### WinUIColors

A utility class containing the standard WinUI 3 color palette.

| Color | Value | Description |
| :--- | :--- | :--- |
| `Accent` | `#0078D4` | Windows 11 accent blue |
| `AccentText` | `#FFFFFF` | Text color on accent backgrounds |
| `WindowBg` | `#FFFFFF` | Window background |
| `ContentBg` | `#F3F3F3` | Content area background |
| `TextPrimary` | `#000000` | Primary text color |
| `TextSecondary` | `#666666` | Secondary/caption text color |
| `Border` | `#CCCCCC` | Standard border color |
| `CardBg` | `#FFFFFF` | Card/panel background |
| `CardBorder` | `#E5E5E5` | Card border color |

### WinUIFonts

A utility class containing the standard WinUI 3 font definitions using Segoe UI.

| Font | Size | Style |
| :--- | :--- | :--- |
| `Title` | 16 | Bold |
| `Subtitle` | 14 | Regular |
| `Body` | 12 | Regular |
| `Caption` | 10 | Regular |

---

### WinUIToggleSwitch

A WinUI 3 styled toggle switch control. Simulates the Windows 11 ToggleSwitch using a Canvas.

#### Key Features

*   **Modern Toggle Graphics:** Animated-style toggle with rounded switch and track
*   **Background Inheritance:** Automatically inherits `BackColor` from parent control
*   **Callback Support:** Execute custom function when toggled

#### Constructor

```python
WinUIToggleSwitch(parent, text="Toggle", on_toggle=None)
```

| Parameter | Description |
| :--- | :--- |
| `parent` | Parent control (Form, Panel, etc.) |
| `text` | Label text displayed next to the toggle |
| `on_toggle` | Callback function receiving boolean state |

#### Usage Example

```python
from winformpy import Form
from winformpy_extended import WinUIToggleSwitch

form = Form({'Text': 'Toggle Demo', 'Width': 300, 'Height': 200})
form.ApplyLayout()

def on_wifi_toggle(is_on):
    print(f"WiFi is {'ON' if is_on else 'OFF'}")

toggle = WinUIToggleSwitch(form, text="WiFi Connection", on_toggle=on_wifi_toggle)
toggle.Location = (20, 50)

form.Show()
```

---

### WinUIExpander

A WinUI 3 styled expander control with collapsible content area.

#### Key Features

*   **Collapsible Content:** Header click toggles content visibility
*   **Accent Colored Header:** Uses WinUI accent blue for header text
*   **Background Inheritance:** Automatically inherits `BackColor` from parent
*   **Customizable Height:** Set expanded height via constructor

#### Constructor

```python
WinUIExpander(parent, title="Expander Title", height_expanded=150)
```

| Parameter | Description |
| :--- | :--- |
| `parent` | Parent control |
| `title` | Header text |
| `height_expanded` | Height when expanded (collapsed height is 40px) |

#### Properties

| Property | Description |
| :--- | :--- |
| `content` | The Panel where child controls should be added |
| `is_expanded` | Boolean indicating current state |

#### Usage Example

```python
from winformpy import Form, DockStyle
from winformpy_extended import WinUIExpander, ExtendedLabel

form = Form({'Text': 'Expander Demo', 'Width': 400, 'Height': 300})
form.ApplyLayout()

exp = WinUIExpander(form, title="Click to expand", height_expanded=120)
exp.Location = (20, 50)
exp.Width = 350

# Add content inside the expander
lbl = ExtendedLabel(exp.content)
lbl.Text = "This content is hidden until the expander is opened."
lbl.Dock = DockStyle.Fill

form.Show()
```

---

### WinUITextBox

A WinUI 3 styled TextBox with a thin accent-colored underline.

#### Key Features

*   **Accent Underline:** 1px blue underline at the bottom (single-line mode only)
*   **Full TextBox Compatibility:** Inherits all standard TextBox functionality
*   **Customizable Color:** Change underline color via `UnderlineColor` property

#### Properties

| Property | Description | Default |
| :--- | :--- | :--- |
| `UnderlineColor` | Color of the accent underline | `#0078D4` (WinUI Accent) |

#### Usage Example

```python
from winformpy import Form
from winformpy_extended import WinUITextBox

form = Form({'Text': 'WinUI TextBox Demo', 'Width': 400, 'Height': 200})
form.ApplyLayout()

txt = WinUITextBox(form, {
    'Left': 20,
    'Top': 50,
    'Width': 300,
    'Height': 25
})
txt.Text = "WinUI styled text box"

# Custom underline color
txt.UnderlineColor = "#FF5722"  # Orange accent

form.Show()
```

---

### WinUIProgressBar

A WinUI 3 styled ProgressBar with accent colors.

#### Key Features

*   **WinUI Accent Bar:** Blue progress bar matching Windows 11 style
*   **Customizable Colors:** Change bar and trough colors
*   **Full ProgressBar Compatibility:** Inherits all standard ProgressBar functionality

#### Properties

| Property | Description | Default |
| :--- | :--- | :--- |
| `BarColor` | Color of the progress bar | `#0078D4` (WinUI Accent) |
| `TroughColor` | Color of the background trough | `#E5E5E5` (Light gray) |

#### Usage Example

```python
from winformpy import Form
from winformpy_extended import WinUIProgressBar

form = Form({'Text': 'WinUI ProgressBar Demo', 'Width': 400, 'Height': 200})
form.ApplyLayout()

pb = WinUIProgressBar(form)
pb.Location = (20, 50)
pb.Size = (350, 25)
pb.Value = 75

# Custom colors
pb.BarColor = "#00C853"     # Green progress
pb.TroughColor = "#F0F0F0"  # Light background

form.Show()
```

---

## Complete Example

```python
from winformpy import Form, DockStyle
from winformpy_extended import (
    ExtendedLabel, 
    WinUIToggleSwitch, 
    WinUIExpander, 
    WinUITextBox, 
    WinUIProgressBar,
    WinUIColors
)

form = Form({'Text': 'WinFormPy Extended Demo', 'Width': 500, 'Height': 400})
form.BackColor = WinUIColors.ContentBg
form.ApplyLayout()

# Search box with accent underline
search = WinUITextBox(form, {'Left': 20, 'Top': 20, 'Width': 300, 'Height': 25})
search.Text = "Search..."

# Toggle switch
toggle = WinUIToggleSwitch(form, text="Dark Mode", on_toggle=lambda on: print(f"Dark: {on}"))
toggle.Location = (20, 70)

# Progress indicator
progress = WinUIProgressBar(form)
progress.Location = (20, 120)
progress.Size = (450, 20)
progress.Value = 45

# Expander with content
exp = WinUIExpander(form, title="Advanced Options", height_expanded=100)
exp.Location = (20, 160)
exp.Width = 450

info = ExtendedLabel(exp.content)
info.Text = "These options are hidden by default. Click the header to reveal them."
info.Dock = DockStyle.Fill

form.Show()
```

---

## Summary of Controls

| Control | Type | Description |
| :--- | :--- | :--- |
| `ExtendedLabel` | Standard | Multiline label with dynamic text wrapping |
| `WinUIColors` | Utility | WinUI 3 color palette |
| `WinUIFonts` | Utility | WinUI 3 font definitions |
| `WinUIToggleSwitch` | WinUI | Windows 11 style toggle switch |
| `WinUIExpander` | WinUI | Collapsible content container |
| `WinUITextBox` | WinUI | TextBox with accent underline |
| `WinUIProgressBar` | WinUI | ProgressBar with accent colors |
