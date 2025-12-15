# GroupBox - Windows Forms Container Control

## Description

The `GroupBox` is a Windows Forms container control implemented in winform-py that is used to visually and logically group related controls in the user interface.

It provides a rectangular border with an optional title to visually delimit a section, improving the organization and usability of the form.

## Internal Implementation

In `winformpy`, the `GroupBox` is implemented using the native Tkinter widget `tk.LabelFrame`. This provides:
- An integrated title in the top border.
- Automatic management of internal margins (`padx`/`pady`) based on the `Padding` property.
- An internal container (`tk.Frame`) where child controls are hosted, ensuring they respect the borders and title.

## Main Features

### Inheritance

`GroupBox` inherits from `ControlBase` and acts as a container to group related controls.

### Visual Representation

- Rectangular frame with border (style dependent on `FlatStyle`).
- Area at the top for the title (property `Text`).
- Configurable internal padding to space child controls.
- Customizable background color and font.

## Properties

### Visual Properties

| Property     | Type      | Description                                              | Default Value    |
| ------------- | --------- | --------------------------------------------------------- | ---------------- |
| `Text`      | str       | Title text displayed at the top of the frame             | `'GroupBox'`     |
| `Width`     | int       | Width of the control in pixels                           | `200`            |
| `Height`    | int       | Height of the control in pixels                          | `100`            |
| `Left`      | int       | X position relative to the parent container              | `0`              |
| `Top`       | int       | Y position relative to the parent container              | `0`              |
| `BackColor` | str       | Background color of the area inside the frame            | `None` (system)  |
| `ForeColor` | str       | Color of the title text                                  | `None` (system)  |
| `Font`      | str/tuple | Font used for the title text                             | `None` (system)  |
| `Padding`   | tuple     | Internal spacing (left, top, right, bottom)              | `(10, 20, 10, 10)` |
| `FlatStyle` | Enum      | Visual style (`Standard`, `Flat`, `Popup`, `System`)     | `Standard`       |

### Automatic Layout Properties

| Property      | Type | Description                                                                 |
| -------------- | ---- | --------------------------------------------------------------------------- |
| `AutoSize`     | bool | If `True`, the control resizes to fit its content.                          |
| `AutoSizeMode` | Enum | `GrowOnly` (grows but does not shrink) or `GrowAndShrink` (exact fit).      |
| `MinimumSize`  | tuple| Guaranteed minimum size `(width, height)`.                                 |
| `MaximumSize`  | tuple| Allowed maximum size `(width, height)`.                                    |

#### AutoSize Behavior

The `AutoSize` calculation in `GroupBox` is robust and considers:
1. **Content:** The position and size of all child controls (`max_right`, `max_bottom`).
2. **Title:** Measures the width and height of the title text using the current font to ensure it is not cut off.
3. **Borders and Padding:** Adds the border thickness and configured padding.
4. **Visual Correction:** Adds an extra safety margin to the right (30px) to compensate for the curvature of the `LabelFrame` border and prevent controls attached to the right edge from appearing clipped.
5. **Anchor:** If the control grows and is anchored to the right (`Right`) or bottom (`Bottom`), it automatically adjusts its `Left` or `Top` position to keep the anchored edge fixed.

### State Properties

| Property   | Type | Description                                                            | Default Value |
| ----------- | ---- | ----------------------------------------------------------------------- | ------------- |
| `Enabled` | bool | Determines if the GroupBox and all its child controls are enabled      | `True`        |
| `Visible` | bool | Determines if the GroupBox and all its child controls are visible      | `True`        |
| `Name`    | str  | Name of the control for identification                                 | `''`          |

### Navigation Properties

| Property    | Type | Description                                               | Default Value |
| ------------ | ---- | ---------------------------------------------------------- | ------------- |
| `TabStop`  | bool | Determines if the control can receive focus via Tab       | `False`       |
| `TabIndex` | int  | Tab order of the control                                   | `0`           |

### Controls Collection

| Property    | Type | Description                                                           |
| ------------ | ---- | ---------------------------------------------------------------------- |
| `Controls` | list | List containing all secondary controls within the GroupBox            |

## Events

### Container Events

| Event             | Parameters | Description                                                               |
| ------------------ | ----------- | -------------------------------------------------------------------------- |
| `ControlAdded`   | `control` | Occurs when a control is dynamically added to the Controls collection    |
| `ControlRemoved` | `control` | Occurs when a control is removed from the Controls collection             |

### Interaction Events

| Event    | Parameters | Description                                                        |
| --------- | ----------- | ------------------------------------------------------------------- |
| `Enter` | -           | Occurs when the user enters the GroupBox (navigation with Tab)     |
| `Leave` | -           | Occurs when the user leaves the GroupBox area                      |
| `Click` | -           | Occurs when the user clicks on the container area                  |

### Rendering Events

| Event    | Parameters | Description                                |
| --------- | ----------- | ------------------------------------------- |
| `Paint` | -           | Occurs when the control needs to be drawn  |

## Methods

### Control Management

#### `AddControl(control)`

Adds a control to the GroupBox with relative positions.

**Behavior:**

- The control is added to the GroupBox (becomes its parent).
- The control will only be visible if its own `Visible` property is `True` AND the GroupBox is also visible.
- Controls inherit the `Enabled` state from the GroupBox.
- **Recommendation:** It is more efficient to create the control by passing the GroupBox as parent in the constructor (`Button(groupbox, ...)`) than using `AddControl` afterwards, as the latter involves recreating the Tkinter widget internally.

```python
# Recommended way
group = GroupBox(form, {'Text': 'Options', 'Left': 10, 'Top': 10})
check = CheckBox(group, {'Text': 'Option 1', 'Left': 20, 'Top': 30})

# Alternative way (less efficient)
check2 = CheckBox(form, {'Text': 'Option 2'}) # Created on the form
group.AddControl(check2) # Moved to group (internal recreation)
```

## Usage Example

```python
from winformpy import Form, GroupBox, RadioButton, Application

class MainForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "GroupBox Example"
        self.Width = 300
        self.Height = 250

        # Create GroupBox
        self.gb_options = GroupBox(self)
        self.gb_options.Text = "Select an option"
        self.gb_options.Left = 20
        self.gb_options.Top = 20
        self.gb_options.Width = 240
        self.gb_options.Height = 150
        self.gb_options.AutoSize = True # Automatic adjustment to content
        self.gb_options.AutoSizeMode = "GrowAndShrink"

        # Add options
        self.rb_option1 = RadioButton(self.gb_options)
        self.rb_option1.Text = "Option A"
        self.rb_option1.Top = 30
        self.rb_option1.Left = 20

        self.rb_option2 = RadioButton(self.gb_options)
        self.rb_option2.Text = "Option B"
        self.rb_option2.Top = 60
        self.rb_option2.Left = 20

if __name__ == "__main__":
    form = MainForm()
    Application.Run(form)
``` GroupBox - Control Contenedor de Windows Forms
