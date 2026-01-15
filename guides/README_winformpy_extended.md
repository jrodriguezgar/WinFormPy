# WinFormPy Extended

**Module:** `winformpy_extended.py`  
**Description:** Extension module for WinFormPy that provides custom controls and advanced layout management capabilities not present in the core library.

## Controls

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
    'Text': "This is a long text that will automatically wrap to fit the width of this control. Try resizing the window!",
    'Left': 10,
    'Top': 10,
    'Width': 360,
    'Height': 100,
    # Anchor allows the control to resize with the form
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
3.  You need multiline text with specific alignment (Left, Center, Right) that respects the control's boundaries.
