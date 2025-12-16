# WinFormPy Tools Documentation

`winformpy_tools` is a utility module included in WinFormPy that provides advanced tools for font management, colors, CSS styles, and automatic control layout.

## Contents

1. [FontManager](#fontmanager)
2. [ColorManager](#colormanager)
3. [CSSManager](#cssmanager)
4. [LayoutManager](#layoutmanager)

---

## FontManager

The `FontManager` class facilitates the management of system fonts and obtaining available fonts.

### Main Methods

* `get_system_fonts()`: Returns a dictionary with all configured system fonts (default, menu, caption, etc.).
* `get_system_font(font_type)`: Obtains a specific system font.
  * Types: `'default'`, `'menu'`, `'caption'`, `'status'`, `'message'`, etc.
* `get_all_available_fonts()`: Returns a sorted list of all font families installed on the system.

### Usage Example

```python
from winformpy.winformpy_tools import FontManager

# Get the system's default font
font = FontManager.get_system_font('default')
label.Font = font

# Get window title font
caption_font = FontManager.get_system_font('caption')
header_label.Font = caption_font
```

---

## ColorManager

The `ColorManager` class allows access to Windows system colors, useful for creating interfaces that integrate natively with the user's theme.

### Main Methods

* `get_system_colors()`: Returns a dictionary with all system colors in hexadecimal format.
* `get_system_color(color_type)`: Obtains a specific system color.
  * Types: `'control'`, `'window'`, `'text'`, `'highlight'`, `'active'`, `'inactive'`, etc.

### Usage Example

```python
from winformpy.winformpy_tools import ColorManager

# Use the standard control background color
panel.BackColor = ColorManager.get_system_color('control')

# Use the system's highlight color
button.BackColor = ColorManager.get_system_color('highlight')
button.ForeColor = ColorManager.get_system_color('highlight_text')
```

---

## CSSManager

The `CSSManager` class allows applying styles to controls using standard CSS syntax, facilitating design and style separation.

### Main Methods

* `parse_css_string(css_string)`: Parses a CSS string into a dictionary.
* `css_to_winform_props(css_string)`: Converts CSS to WinFormPy control properties.
* `apply_css_to_winform_control(control, css_string)`: Directly applies styles to a control.

### Supported Properties

* `color` -> `ForeColor`
* `background-color` -> `BackColor`
* `font-family`, `font-size`, `font-weight` -> `Font`
* `width`, `height` -> `Width`, `Height`
* `left`, `top` -> `Left`, `Top`
* `border`, `border-style` -> `BorderStyle`

### Usage Example

```python
from winformpy.winformpy_tools import CSSManager

style = """
    background-color: #ffffff;
    color: #333333;
    font-family: Segoe UI;
    font-size: 12px;
    font-weight: bold;
    border: solid;
"""

CSSManager.apply_css_to_winform_control(my_label, style)
```

---

## LayoutManager

The `LayoutManager` class (formerly `AutoLayoutManager`) provides a flexible system for automatically distributing controls within a container.

### Features

* **Automatic Distribution**: Places controls sequentially without needing to manually calculate coordinates.
* **Flow Layout**: Automatic line/column adjustment when space is filled.
* **Auto-Size Container**: Ability to adjust the container size to the content.
* **Fixed Wrap**: Ability to force line/column breaks after a fixed number of elements.

### Initialization

```python
layout = LayoutManager(
    container, 
    margin=5,               # Space between controls
    padding=10,             # Space from the container's edge
    autosize_container=True, # Adjust container to content
    wrap_count=None         # Elements per row/column (None = automatic)
)
```

### Configuration

* `layout_type`:
  * `LayoutType.FlowLayout`: Continuous flow with automatic wrap.
* `distribution`:
  * `Distribution.UpDown`: Vertical (Top to Bottom).
  * `Distribution.LeftRight`: Horizontal (Left to Right).
* `wrap_count`: Integer defining how many elements to place before wrapping to the next row/column. If `None`, wraps based on container size.

### Methods

* `add_control(control)`: Adds a control to the layout and calculates its position.
* `recalculate_layout()`: Recalculates positions of all managed controls.
* `reset()`: Resets internal position counters.

### Usage Examples

#### 1. Simple Vertical List

```python
layout = LayoutManager(panel, margin=5)
layout.distribution = LayoutManager.Distribution.UpDown

for i in range(5):
    btn = Button(panel)
    btn.Text = f"Item {i}"
    layout.add_control(btn)
```

#### 2. Horizontal Flow Layout (Gallery)

```python
layout = LayoutManager(panel, margin=10, padding=10)
layout.layout_type = LayoutManager.LayoutType.FlowLayout
layout.distribution = LayoutManager.Distribution.LeftRight

# Controls will be added to the right and wrap to the next line
# automatically when they don't fit in the panel's width.
for i in range(20):
    img_box = PictureBox(panel)
    layout.add_control(img_box)
```

#### 3. Fixed Grid (Fixed Wrap)

```python
# Creates a 3-column grid
layout = LayoutManager(panel, margin=5, wrap_count=3)
layout.distribution = LayoutManager.Distribution.LeftRight

for i in range(9):
    btn = Button(panel)
    layout.add_control(btn)
# Visual result:
# [Btn] [Btn] [Btn]
# [Btn] [Btn] [Btn]
# [Btn] [Btn] [Btn]
```

#### 4. Auto-Adjustable Container

```python
# The panel will grow to accommodate all controls
layout = LayoutManager(panel, autosize_container=True)
layout.add_control(big_control)
---