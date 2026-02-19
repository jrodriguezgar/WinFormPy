# WinFormPy Extended Controls

Advanced controls and enhanced versions of core components for complex UI scenarios.

## Module: `winformpy_extended.py`

All extended controls use the `Native` bridge from `winformpy.py` — no direct `tkinter` imports.

### Controls Reference

| Control | Description |
| --- | --- |
| **ExtendedLabel** | Label with automatic text wrapping and resize response |
| **ConsoleTextBox** | Multi-colored text control for logs and terminals |
| **DatePickerBox** | Date input with calendar dropdown |
| **PhotoImage** | Image wrapper (scaling, base64, pixel manipulation) |

### 1. ExtendedLabel
Label with automatic text wrapping and alignment.
- Handles paragraphs of text that need to fit within a specific width.
- Responds to window resizing.

```python
from winformpy import ExtendedLabel

lbl = ExtendedLabel(form, {'Text': 'A long paragraph...', 'Width': 400})
```

### 2. ConsoleTextBox
Multi-colored text control optimized for logs and terminals.
- `WriteError`, `WriteWarning`, `WriteSuccess`, `WriteInfo`.
- Auto-scroll and MaxLines management.

```python
from winformpy import ConsoleTextBox

console = ConsoleTextBox(form, {'Width': 600, 'Height': 300})
console.WriteSuccess("Operation completed")
console.WriteError("Something went wrong")
console.WriteWarning("Disk space low")
console.WriteInfo("Processing...")
```

### 3. DatePickerBox
Date input control with a calendar popup.
- Configurable date formats via `DateFormat` enum.
- Min/max date constraints.
- `DateChanged` event.

```python
from winformpy import DatePickerBox
from winformpy.winformpy_extended import DateFormat

picker = DatePickerBox(form, {
    'Format': DateFormat.ShortDate,
    'Left': 20, 'Top': 50, 'Width': 200
})
picker.DateChanged = lambda s, e: print(picker.Value)
```

### 4. PhotoImage Wrapper
Manage images without importing Tkinter directly — uses `Native.PhotoImage` internally.
- Scaling (subsample/zoom).
- Pixel-level manipulation.
- Base64 support.

```python
from winformpy import PhotoImage

img = PhotoImage(file="logo.png")
img_small = img.subsample(2, 2)
```
