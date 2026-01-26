# Dock and Anchor in Windows Forms and winformpy

This document explains the `Dock` and `Anchor` properties of Windows Forms and how they are implemented in the `winformpy` library, which allows developing graphical interfaces similar to VB.NET/WinForms in Python using Tkinter.

## Index

1. [Introduction](#introduction)
2. [Dock Property](#dock-property)
3. [Anchor Property](#anchor-property)
4. [Implementation in winformpy](#implementation-in-winformpy)
5. [Usage Examples](#usage-examples)
6. [Best Practices](#best-practices)
7. [Technical Notes](#technical-notes)

## Introduction

In Windows Forms (VB.NET/C#), the `Dock` and `Anchor` properties are fundamental for creating responsive interfaces that automatically adapt to the resizing of forms and containers.

- **Dock**: "Docks" a control to an edge of the container, making it occupy all available space in that direction.
- **Anchor**: "Anchors" a control to one or more edges of the container, maintaining fixed distances while allowing resizing.

These properties eliminate the need to manually calculate positions and sizes when resizing the window.

## Dock Property

### Concept in Windows Forms

The `Dock` property specifies which edge of the parent container the control should be "docked" to. When a control is docked:

- It occupies all available space in the specified direction
- It automatically resizes when the container's size changes
- It can be combined with other docked controls to create complex layouts

### Dock Values

The `Dock` property accepts values from the `DockStyle` enum or their string representations:

- **`DockStyle.None_`** (or `'None_'`): No docking, absolute positioning (default).
- **`DockStyle.Top`** (or `'Top'`): Docked to the top edge.
- **`DockStyle.Bottom`** (or `'Bottom'`): Docked to the bottom edge.
- **`DockStyle.Left`** (or `'Left'`): Docked to the left edge.
- **`DockStyle.Right`** (or `'Right'`): Docked to the right edge.
- **`DockStyle.Fill`** (or `'Fill'`): Occupies all remaining space.

### Docking Order

When multiple controls are docked in the same container, the **Z-order** (stacking order) determines priority:

1. Controls at the **bottom** of the Z-order (added first) are docked first and take the full edge.
2. Subsequent controls are docked into the *remaining* space.
3. A control with `Dock.Fill` occupies whatever space is left after all other docked controls are placed.

To change the docking priority, use `BringToFront()` (moves to top of Z-order, docked last) or `SendToBack()` (moves to bottom of Z-order, docked first).

## Anchor Property

### Concept in Windows Forms

The `Anchor` property specifies which edges of the parent container should maintain a fixed distance from the control. It is useful for:

- Maintaining constant margins when resizing
- Allowing controls to grow or move with the window
- Creating layouts where some controls remain fixed while others adjust

### Anchor Values

`Anchor` accepts a combination of `AnchorStyles` flags or a comma-separated string:

- **`AnchorStyles.Top`** (or `'Top'`): Fixed distance to the top edge.
- **`AnchorStyles.Bottom`** (or `'Bottom'`): Fixed distance to the bottom edge.
- **`AnchorStyles.Left`** (or `'Left'`): Fixed distance to the left edge.
- **`AnchorStyles.Right`** (or `'Right'`): Fixed distance to the right edge.
- **`AnchorStyles.None_`** (or `'None_'`): Not anchored to any edge (moves relatively).

**Common combinations:**

- **`'Top, Left'`** (default): Top-left corner fixed, control does not resize.
- **`'Top, Bottom, Left'`**: Variable height, fixed width, left edge fixed.
- **`'Top, Left, Right'`**: Variable width, fixed height, top edge fixed.
- **`'Top, Bottom, Left, Right'`**: Control resizes in both directions.

### Behavior

- If anchored to opposite sides (Left+Right), the control stretches horizontally.
- If anchored to opposite sides (Top+Bottom), the control stretches vertically.
- Initial distances to edges are calculated when the control is first displayed or when the property is set.

## Implementation in winformpy

### Compatibility with Windows Forms

`winformpy` implements `Dock` and `Anchor` with high fidelity to Windows Forms. You can set these properties using the Enum or strings in the constructor (via `props`) or directly on the object.

```python
from winformpy import Form, Button, Panel, DockStyle, AnchorStyles

# Create form
form = Form({'Text': 'Dock and Anchor Demo', 'Width': 600, 'Height': 400})

# Panel docked to fill the entire window
# Using string shortcut in props
main_panel = Panel(form, {'Dock': 'Fill'})

# Button anchored to the bottom-right corner
# Using direct property assignment with string
btn_close = Button(main_panel)
btn_close.Text = "Close"
btn_close.Left = 500
btn_close.Top = 350
btn_close.Anchor = "Bottom, Right"

# Button docked to the top
# Using Enum
btn_top = Button(main_panel)
btn_top.Text = "I am at the Top"
btn_top.Height = 50
btn_top.Dock = DockStyle.Top
```
button = Button(main_panel, {
    'Text': 'OK',
    'Anchor': ['Bottom', 'Right'],
    'Width': 80,
    'Height': 30
})
```

### Specific Properties

#### Dock

```python
control.Dock = 'Fill'  # Occupies all available space
control.Dock = 'Top'   # Docked to top
control.Dock = 'None'  # No docking (default)
```

#### Anchor

```python
control.Anchor = ['Top', 'Left']        # Default
control.Anchor = ['Top', 'Bottom', 'Left', 'Right']  # Stretches in both directions
control.Anchor = ['Bottom', 'Right']    # Bottom-right corner fixed
```

### Margin Support

Both systems respect the control's `Margin` property:

```python
button = Button(panel, {
    'Text': 'Button with margin',
    'Dock': 'Bottom',
    'Margin': (10, 5, 10, 5)  # Left, Top, Right, Bottom
})
```

### Resizing Events

- `Dock` updates automatically on container `<Configure>` events
- `Anchor` calculates initial distances on the first `<Map>` or `<Configure>` event
- Changes are applied in real-time without programmer intervention

## Usage Examples

### Example 1: Basic Layout with Dock (RECOMMENDED PATTERN)

```python
from winformpy import Form, Panel, Button, TextBox, DockStyle

# Create form and apply layout FIRST
form = Form({'Text': 'Layout with Dock', 'Width': 500, 'Height': 400})
form.ApplyLayout()  # CRITICAL: Call before adding controls

# Toolbar at the top - assign Dock as property
toolbar = Panel(form, {
    'Height': 50,
    'BackColor': 'LightBlue'
})
toolbar.Dock = DockStyle.Top

# Status bar at the bottom
status_bar = Panel(form, {
    'Height': 30,
    'BackColor': 'LightGray'
})
status_bar.Dock = DockStyle.Bottom

# Main panel occupying the remaining space - created LAST
main_panel = Panel(form, {
    'BackColor': 'White'
})
main_panel.Dock = DockStyle.Fill  # Fill should be LAST

# Content in the main panel
text_box = TextBox(main_panel, {
    'Multiline': True
})
text_box.Dock = DockStyle.Fill
```

### Example 2: Form with Anchor

```python
from winformpy import Form, Label, TextBox, Button

form = Form({'Text': 'Form with Anchor', 'Width': 400, 'Height': 300})

# Label that stretches horizontally
title_label = Label(form, {
    'Text': 'Form Title',
    'Anchor': ['Top', 'Left', 'Right'],
    'Top': 20,
    'Left': 20,
    'Right': 20,
    'Height': 30,
    'TextAlign': 'center'
})

# Text field that stretches
name_textbox = TextBox(form, {
    'Anchor': ['Top', 'Left', 'Right'],
    'Top': 70,
    'Left': 20,
    'Width': 360, # 400 (Form Width) - 20 (Left) - 20 (Right Margin)
    'Height': 25
})

# Buttons anchored to the bottom-right corner
# Note: Initial position must be calculated correctly.
# Form Width: 400, Height: 300
ok_button = Button(form, {
    'Text': 'OK',
    'Anchor': ['Bottom', 'Right'],
    'Width': 80,
    'Height': 30,
    'Left': 300, # 400 - 80 - 20 (Margin)
    'Top': 250   # 300 - 30 - 20 (Margin)
})

cancel_button = Button(form, {
    'Text': 'Cancel',
    'Anchor': ['Bottom', 'Right'],
    'Width': 80,
    'Height': 30,
    'Left': 200, # 400 - 80 - 120 (Margin)
    'Top': 250   # 300 - 30 - 20 (Margin)
})
```

### Example 3: Complex Combined Layout

```python
from winformpy import Form, Panel, Button, ListBox, TextBox

form = Form({'Text': 'Complex Layout', 'Width': 800, 'Height': 600})

# Left panel for navigation
nav_panel = Panel(form, {
    'Dock': 'Left',
    'Width': 200,
    'BackColor': 'LightGray'
})

# Navigation list
nav_list = ListBox(nav_panel, {
    'Dock': 'Fill'
})

# Right panel occupying the rest
content_panel = Panel(form, {
    'Dock': 'Fill'
})

# Toolbar in the content
toolbar = Panel(content_panel, {
    'Dock': 'Top',
    'Height': 40,
    'BackColor': 'WhiteSmoke'
})

# Main content area
main_area = Panel(content_panel, {
    'Dock': 'Fill'
})

# Floating button anchored bottom-right
# Note: Coordinates must be calculated based on estimated container size
action_button = Button(main_area, {
    'Text': 'Action',
    'Anchor': ['Bottom', 'Right'],
    'Width': 100,
    'Height': 35,
    'Left': 480, # Example: 600 (Approx Width) - 100 - 20
    'Top': 505   # Example: 560 (Approx Height) - 35 - 20
})
```

## CRITICAL: Form Initialization and Control Creation Order

### ⚠️ MUST call ApplyLayout() BEFORE adding controls

**For Dock to work correctly, you MUST call `form.ApplyLayout()` BEFORE creating any child controls:**

```python
# ✅ CORRECT - ApplyLayout() called FIRST
form = Form({'Width': 1024, 'Height': 768})
form.ApplyLayout()  # MUST be called before adding children

# Now Dock will work correctly
sidebar = Panel(form, {'Dock': DockStyle.Left, 'Width': 200})
content = Panel(form, {'Dock': DockStyle.Fill})
```

```python
# ❌ WRONG - Controls created before ApplyLayout()
form = Form({'Width': 1024, 'Height': 768})
panel = Panel(form, {'Dock': DockStyle.Fill})  # Won't work properly!
form.ApplyLayout()  # Too late
```

### ⚠️ Control Creation Order Matters

Controls are docked in the order they are created. Create them in this order:

1. **DockStyle.Top** panels first
2. **DockStyle.Bottom** panels next
3. **DockStyle.Left** / **DockStyle.Right** panels
4. **DockStyle.Fill** panel LAST (fills remaining space)

```python
# ✅ CORRECT order
header = Panel(form, {'Dock': DockStyle.Top, 'Height': 50})
footer = Panel(form, {'Dock': DockStyle.Bottom, 'Height': 30})
sidebar = Panel(form, {'Dock': DockStyle.Left, 'Width': 200})
content = Panel(form, {'Dock': DockStyle.Fill})  # LAST
```

### ⚠️ Use Enums, Not Strings

**IMPORTANT: For reliable behavior, use enum values instead of strings:**

```python
# ✅ CORRECT - Use enums
panel.Dock = DockStyle.Fill
button.Anchor = AnchorStyles.Top | AnchorStyles.Right
font = Font('Segoe UI', 12, FontStyle.Bold)

# ❌ AVOID - Strings may cause issues in some cases
panel.Dock = 'Fill'
button.Anchor = ['Top', 'Right']
font = Font('Segoe UI', 12, 'bold')
```

### ⚠️ Workaround: Assign Dock/Anchor as Properties

**If you experience issues with Dock/Anchor not working when passed in the constructor dictionary, assign them as properties AFTER creation:**

```python
# ✅ WORKAROUND - Assign Dock as property after creation
top_panel = Panel(form, {
    'Height': 100,
    'BackColor': '#0078D4'
})
top_panel.Dock = DockStyle.Top  # Assign AFTER creation

# Same for Anchor
button = Button(panel, {
    'Text': 'OK',
    'Left': 20,
    'Top': 20,
    'Width': 100,
    'Height': 30
})
button.Anchor = AnchorStyles.Bottom | AnchorStyles.Right  # Assign AFTER creation
```

This ensures the control is properly registered in the parent's `Controls` collection before Dock/Anchor is applied.

## Best Practices

### Choosing between Dock and Anchor

- **Use Dock when:**

  - You want a control to occupy all available space in one direction
  - Creating layouts with distinct sections (header, sidebar, footer, content)
  - The control should resize proportionally with the container
- **Use Anchor when:**

  - You want to maintain fixed margins around a control
  - Some controls should remain in fixed positions while others adjust
  - Creating dialogs or forms with elements that should not stretch

### Design Tips

1. **Creation order**: Create Dock controls in logical order (Top, then Bottom, then Left, Right, Fill).
2. **Exclusivity**: **Do not use Dock and Anchor on the same control**. Setting one property automatically overrides the other.
3. **Test resizing**: Always test how the interface behaves when resizing.
4. **Use container panels**: Group related controls in Panels for more complex layouts.
5. **Consider MinimumSize**: Set minimum sizes to prevent controls from becoming too small.
6. **Consider MinimumSize**: Set minimum sizes to prevent controls from becoming too small.

### Performance

- Dock and Anchor update automatically on resize events
- For complex interfaces, consider using nested Panels to reduce calculations
- Avoid creating too many Anchor controls in highly dynamic containers

## Technical Notes

### Internal Implementation

`winformpy` implements Dock and Anchor through:

- **Tkinter Events**: Binds `<Configure>` to detect size changes
- **Geometry Calculations**: Maintains relative and absolute distances
- **Automatic Layout**: Reorganizes controls when properties change
- **Container Hierarchy**: Respects the parent-child structure of controls
- **Z-Order**: Respects the standard Windows Forms Z-Order (back controls have priority for outer docking).

### Limitations vs Windows Forms

- **Subpixel positioning**: Tkinter may have slight differences in positioning
- **Complex layouts**: For very complex layouts, consider using `TableLayoutPanel` or `FlowLayoutPanel`
- **Animation**: Changes are immediate

### Compatibility

- ✅ Works with all `winformpy` controls
- ✅ Compatible with `AutoSize` and other layout properties
- ✅ Respects `Margin` and `Padding`

### Debugging Layout Issues

#### Common Symptoms and Causes

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Panel has 0 or very small height | Control created BEFORE `form.ApplyLayout()` | Call `form.ApplyLayout()` before creating controls |
| Dock.Fill doesn't fill space | Wrong creation order | Create Fill panel LAST |
| Controls overlap incorrectly | Wrong docking order | Create Top/Bottom first, then Left/Right, then Fill |
| Dock/Anchor not applying | Assigned in constructor dict | Assign as property AFTER creation |
| Container frame not positioned | Layout code using wrong widget | Check for `_container_frame` attribute |

#### Debug Steps

**1. Check control dimensions after window shows:**

```python
def debug():
    print(f'Widget: {control._tk_widget.winfo_width()}x{control._tk_widget.winfo_height()}')
    if hasattr(control, '_container_frame') and control._container_frame:
        print(f'Container: {control._container_frame.winfo_width()}x{control._container_frame.winfo_height()}')

form._root.after(500, debug)
```

**2. Verify control is in parent's Controls:**

```python
print(f'In Controls: {control in parent.Controls}')
print(f'Controls count: {len(parent.Controls)}')
```

**3. View current properties:**

```python
print(f"Dock: {control.Dock}")
print(f"Anchor: {control.Anchor}")
print(f"Size: {control.Size}")
print(f"Location: {control.Location}")
```

**4. Force layout recalculation:**

```python
from winformpy.winformpy import ControlBase
ControlBase._layout_docked_children(form._root)
```

**5. Check for container frames:**

```python
# Some controls (TextBox, RichTextBox, ListBox with scrollbars) use _container_frame
if hasattr(control, '_container_frame'):
    print('Control has container frame - use it for positioning')
```

---
