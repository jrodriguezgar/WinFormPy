# WinFormPy Extended

**Module:** `winformpy_extended.py`  
**Description:** Extension module for WinFormPy that provides custom controls, WinUI 3 styled controls, and advanced layout management capabilities not present in the core library.

---

## Image and Graphics Classes

### PhotoImage

A WinFormPy wrapper for `tkinter.PhotoImage` that provides a WinForms-style interface for creating and managing images without requiring direct tkinter imports in user code.

#### Key Features

*   **No Direct Tkinter Import:** Use images without importing tkinter directly in your code
*   **Multiple Creation Methods:** Create blank images, load from files, or use base64 data
*   **Pixel Manipulation:** Set and get individual pixel colors
*   **Image Transformation:** Copy, subsample (reduce), and zoom (enlarge) images
*   **File I/O:** Write images to files in various formats

#### Constructor

```python
PhotoImage(**kwargs)
```

**Parameters:**
- `file` (str): Path to image file (GIF, PGM, PPM, PNG with PIL)
- `data` (str): Image data in base64 or XPM format
- `width` (int): Width for blank image
- `height` (int): Height for blank image
- `format` (str): Image format ('gif', 'png', 'ppm', 'pgm')

#### Methods

| Method | Description |
| :--- | :--- |
| `put(color, to=None)` | Set pixel color(s). `to` can be (x,y) for single pixel or ((x1,y1),(x2,y2)) for rectangle |
| `get(x, y)` | Get RGB values of pixel at (x, y) |
| `copy()` | Create a copy of the image |
| `subsample(x, y=None)` | Return a reduced-size version (divides by x and y) |
| `zoom(x, y=None)` | Return an enlarged version (multiplies by x and y) |
| `write(filename, format=None)` | Write image to file |
| `width()` | Get image width in pixels |
| `height()` | Get image height in pixels |
| `get_image()` | Get underlying tkinter PhotoImage (for internal use) |

#### Usage Examples

**Create a blank image and draw pixels:**
```python
from winformpy_extended import PhotoImage

# Create 32x32 blank image
img = PhotoImage(width=32, height=32)

# Draw a blue square with white center
for y in range(32):
    for x in range(32):
        if 4 <= x <= 27 and 4 <= y <= 27:
            img.put('#3498DB', (x, y))  # Blue background
            if 12 <= x <= 19 and 8 <= y <= 14:
                img.put('#FFFFFF', (x, y))  # White circle for head
```

**Load from file:**
```python
img = PhotoImage(file='icon.png')
```

**Use with ImageList:**
```python
from winformpy import ImageList
from winformpy_extended import PhotoImage

# Create ImageList
image_list = ImageList({'ImageSize': (32, 32)})

# Create and add icon
icon = PhotoImage(width=32, height=32)
icon.put('#FF0000')  # Fill with red
image_list.Images.Add(icon, 0)
```

**Transform images:**
```python
# Create original image
original = PhotoImage(width=64, height=64)

# Make smaller version (32x32)
smaller = original.subsample(2, 2)

# Make larger version (128x128)
larger = original.zoom(2, 2)

# Copy image
copy = original.copy()
```

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
| `ConsoleTextBox` | Standard | Multi-colored text output control for console-style display |
| `WinUIColors` | Utility | WinUI 3 color palette |
| `WinUIFonts` | Utility | WinUI 3 font definitions |
| `WinUIToggleSwitch` | WinUI | Windows 11 style toggle switch |
| `WinUIExpander` | WinUI | Collapsible content container |
| `WinUITextBox` | WinUI | TextBox with accent underline |
| `WinUIProgressBar` | WinUI | ProgressBar with accent colors |

---

## ConsoleTextBox

A multi-line text control with support for multiple text colors. Ideal for console-style output, log viewers, or any multi-colored text display.

### Key Features

*   **Colored Text:** Write text in different colors using tags
*   **Auto-Scroll:** Automatically scrolls to show new content
*   **Read-Only Mode:** Optional read-only mode for output-only displays
*   **Auto-Hide Scrollbar:** Scrollbar only appears when content exceeds visible area
*   **MaxLines:** Limit the number of lines to prevent memory issues
*   **Predefined Methods:** `WriteError`, `WriteWarning`, `WriteSuccess`, `WriteInfo` for common scenarios

### Properties

| Property | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| `Text` | `str` | Gets/sets all text content | `''` |
| `BackColor` | `str` | Background color | `'#FFFFFF'` |
| `ForeColor` | `str` | Default text color | `'#000000'` |
| `ReadOnly` | `bool` | If True, text cannot be edited | `False` |
| `WordWrap` | `bool` | Enable word wrapping | `True` |
| `MaxLines` | `int` | Maximum lines to keep (0 = unlimited) | `0` |
| `Font` | `Font` | Font for the text | System default |
| `Lines` | `list` | Gets all lines as a list | - |
| `LineCount` | `int` | Gets the number of lines | - |

### Methods

| Method | Description |
| :--- | :--- |
| `Write(text, color=None)` | Write text without newline |
| `WriteLine(text='', color=None)` | Write text with newline |
| `WriteError(text)` | Write in red (#FF6B6B) |
| `WriteWarning(text)` | Write in yellow (#FFD93D) |
| `WriteSuccess(text)` | Write in green (#6BCB77) |
| `WriteInfo(text)` | Write in blue (#4D96FF) |
| `Clear()` | Clear all text |
| `ScrollToEnd()` | Scroll to bottom |
| `ScrollToStart()` | Scroll to top |
| `AppendText(text, color=None)` | Append text (alias for Write) |
| `ConfigureTag(name, **kwargs)` | Configure a custom tag style |
| `WriteWithTag(text, tag_name)` | Write text using a custom tag |

### Usage Example

```python
from winformpy import Form, DockStyle
from winformpy import ConsoleTextBox

form = Form({'Text': 'Console Demo', 'Width': 600, 'Height': 400})
form.ApplyLayout()

# Create a dark-themed console
console = ConsoleTextBox(form, {
    'Dock': DockStyle.Fill,
    'BackColor': '#1E1E1E',
    'ForeColor': '#CCCCCC',
    'ReadOnly': True,
    'MaxLines': 1000
})

# Write different types of messages
console.WriteLine("Application started")
console.WriteSuccess("Connection established")
console.WriteWarning("Cache is getting full")
console.WriteError("Failed to load configuration")
console.WriteInfo("Processing 150 items...")

# Write with custom colors
console.WriteLine("Custom purple text", '#9B59B6')
console.WriteLine("Custom orange text", '#E67E22')

# Configure and use custom tags
console.ConfigureTag('highlight', foreground='#FFFF00', background='#333333')
console.WriteWithTag("Highlighted text\n", 'highlight')

form.ShowDialog()
```

### When to Use

Use `ConsoleTextBox` when you need:
1.  A log viewer or debug output panel
2.  Console-style output with colored messages
3.  Terminal emulator displays
4.  Status messages with different severity levels

