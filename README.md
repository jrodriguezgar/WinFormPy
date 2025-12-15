# WinFormPy

**A comprehensive Python library that maps Windows Forms/VB syntax and objects to Tkinter**

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.0.2-blue.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Overview

WinFormPy is a complete library designed to help developers familiar with Windows Forms (VB6/VB.NET) transition their applications to Python using Tkinter. It provides a familiar API that closely mimics Windows Forms controls, properties, events, and behaviors.

## Features

- **Complete Windows Forms API mapping** - Controls, properties, and events that match VB.NET/VB6 syntax
- **Comprehensive control library** including:
  - Basic controls: Button, Label, TextBox, CheckBox, ComboBox, ListBox
  - Advanced controls: DataGridView, TreeView, TabControl, Panel, GroupBox, PictureBox, Line
  - Dialogs: OpenFileDialog, SaveFileDialog, PrintDialog, MessageBox, InputBox
  - Specialized controls: MaskedTextBox, CheckedListBox, ProgressBar, TrackBar
- **New Modules**:
  - **mauipy**: Create modern applications with MAUI-style architecture (Shell, Pages, Layouts).
  - **mdipy**: Support for Multiple Document Interface (MDI) applications.
- **Flexible initialization** - Support for both traditional property assignment and dictionary-based setup (`props`)
- **Event-driven programming** with familiar VB-style event handlers
- **Form management** with UserControl and Form base classes
- **Built-in utilities**: ImageList, Timer, ToolTip, ContextMenuStrip, MenuStrip, StatusBar
- **AutoSize support** for automatic control resizing with size constraints
- **CSS styling support** for enhanced customization
- **VB-style properties**: Location, Size, Enabled, Visible, BackColor, Font, etc.

## Installation

### Using UV (Recommended)

Ensure you have [UV](https://github.com/astral-sh/uv) installed. Then:

```bash
git clone https://github.com/DatamanEdge/WinFormPy.git
cd WinFormPy
uv sync
```

### From Source (Manual)

```bash
git clone https://github.com/DatamanEdge/WinFormPy.git
cd WinFormPy
pip install -r requirements.txt  # If requirements.txt exists
```

### Using pip (if published)

```bash
pip install winformpy
```

## Quick Start

Here's a simple example showing how to create a form with a button:

```python
from winformpy import Form, Button, Label, MessageBox, Application

class MyForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "My First WinFormPy App"
        self.Width = 400
        self.Height = 300
        self.StartPosition = "CenterScreen"
    
        # Create a label
        self.label = Label(self)
        self.label.Text = "Hello, WinFormPy!"
        self.label.Left = 50
        self.label.Top = 50
        self.label.Font = ("Arial", 14)
    
        # Create a button
        self.button = Button(self)
        self.button.Text = "Click Me!"
        self.button.Left = 50
        self.button.Top = 100
        self.button.Width = 120
        self.button.Height = 40
        self.button.Click = self.button_click
  
    def button_click(self, sender, e):
        MessageBox.Show("Button was clicked!", "Info")

if __name__ == "__main__":
    app = MyForm()
    Application.Run(app)
```

## Examples

The `examples/` directory contains various demonstration scripts showing different features of the library:

- `basic_controls_example.py` - Basic controls usage (Button, Label, TextBox)
- `system_fonts_colors_example.py` - Demonstration of system fonts and colors
- `autosize_example.py` - AutoSize functionality
- `tooltip_example.py` - ToolTip usage
- `anchor_dock_example.py` - Anchor and Dock properties
- `css_set_controls_example.py` - CSS styling examples
- `hierarchical_visibility_example.py` - Control visibility management
- `all_system_styles_example.py` - System styles demonstration
- `groupbox_example.py` - GroupBox container control with RadioButtons and CheckBoxes

To run any example:

```bash
uv run examples/example_name.py
```

## Documentation

### Basic Controls

#### Button

```python
button = Button(form)
button.Text = "Submit"
button.Left = 10
button.Top = 10
button.Width = 100
button.Height = 30
button.Enabled = True
button.Visible = True

button.Click = lambda sender, e: print("Button clicked!")
```

#### TextBox

```python
textbox = TextBox(form)
textbox.Text = ""
textbox.Left = 10
textbox.Top = 50
textbox.Width = 200
textbox.Height = 25
textbox.Multiline = False
textbox.ReadOnly = False
textbox.PasswordChar = "*"  # For password fields

textbox.TextChanged = lambda sender, e: print(f"Text: {textbox.Text}")
```

#### ComboBox

```python
combo = ComboBox(form)
combo.Items = ["Option 1", "Option 2", "Option 3"]
combo.Left = 10
combo.Top = 90
combo.Width = 200
combo.SelectedIndex = 0

combo.SelectedIndexChanged = lambda sender, e: print(f"Selected: {combo.SelectedItem}")
```

### Advanced Controls

#### DataGridView

```python
dgv = DataGridView(form)
dgv.Left = 10
dgv.Top = 10
dgv.Width = 400
dgv.Height = 200
dgv.Columns = ["Name", "Age", "City"]

# Add data
data = [
    {"Name": "John", "Age": 30, "City": "New York"},
    {"Name": "Jane", "Age": 25, "City": "London"}
]
dgv.DataSource = data
```

#### TreeView

```python
tree = TreeView(form)
tree.Left = 10
tree.Top = 10
tree.Width = 250
tree.Height = 300

# Add nodes
root = tree.AddNode("Root Node")
child1 = tree.AddNode("Child 1", parent=root)
child2 = tree.AddNode("Child 2", parent=root)
```

### Dialogs

#### OpenFileDialog

```python
dialog = OpenFileDialog()
dialog.Filter = "Text Files|*.txt|All Files|*.*"
dialog.Title = "Select a file"
filename = dialog.ShowDialog()
if filename:
    print(f"Selected: {filename}")
```

#### MessageBox

```python
result = MessageBox.Show(
    "Do you want to continue?",
    "Confirmation",
    buttons="YesNo",
    icon="Question"
)
if result == "Yes":
    print("User clicked Yes")
```

### Form and UserControl

```python
class CustomControl(UserControl):
    def __init__(self, parent):
        super().__init__(parent)
        self.Width = 300
        self.Height = 200
        self.BackColor = "lightgray"
    
        # Add controls to the UserControl
        self.label = Label(self)
        self.label.Text = "Custom Control"
        self.label.Left = 10
        self.label.Top = 10

class MainForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "Main Form"
        self.Width = 500
        self.Height = 400
    
        # Add custom control
        self.custom = CustomControl(self)
        self.custom.Location = (50, 50)
```

### GroupBox

GroupBox is a container control that provides a visual grouping for other controls with a titled border.

```python
# Create a GroupBox
group = GroupBox(form, {
    'Text': 'Options',
    'Left': 10,
    'Top': 10,
    'Width': 200,
    'Height': 150
})
form.AddControl(group)

# Add controls to the GroupBox
radio1 = RadioButton(group, {
    'Text': 'Option 1',
    'Left': 10,
    'Top': 10,
    'Checked': True
})
group.AddControl(radio1)

radio2 = RadioButton(group, {
    'Text': 'Option 2', 
    'Left': 10,
    'Top': 35
})
group.AddControl(radio2)

checkbox = CheckBox(group, {
    'Text': 'Enable feature',
    'Left': 10,
    'Top': 70
})
group.AddControl(checkbox)
```

**GroupBox Properties:**

- `Text` - Title displayed on the border
- `Padding` - Internal padding (left, top, right, bottom)
- `BorderStyle` - Border appearance ('None', 'Fixed3D', 'FixedSingle')
- All standard control properties (Location, Size, Enabled, Visible, etc.)

**GroupBox Methods:**

- `AddControl(control)` - Add a control to the GroupBox
- `RemoveControl(control)` - Remove a control from the GroupBox

## API Reference

### Control Properties (Common)

- `Name` - Control identifier
- `Text` - Display text
- `Left`, `Top` - Position
- `Width`, `Height` - Size
- `Location` - Tuple (Left, Top)
- `Enabled` - Enable/disable control
- `Visible` - Show/hide control
- `BackColor` - Background color
- `ForeColor` - Text color
- `Font` - Font tuple (name, size)
- `BorderStyle` - Border appearance

### Control Events (Common)

- `Click` - Mouse click
- `DoubleClick` - Mouse double-click
- `MouseDown`, `MouseUp` - Mouse button events
- `MouseEnter`, `MouseLeave` - Mouse hover events
- `KeyDown`, `KeyUp`, `KeyPress` - Keyboard events
- `Enter`, `Leave` - Focus events (GotFocus, LostFocus)
- `Paint` - Control repaint
- `Resize` - Control resized

## Architecture

WinFormPy is built on three main layers:

1. **ControlBase** - Base class providing common functionality for all controls
2. **Specific Controls** - Individual control implementations (Button, Label, etc.)
3. **Container Controls** - Forms, Panels, and UserControls that host other controls

## Project Structure

```
WinFormPy/
├── winformpy/
│   ├── __init__.py         # Package initialization
│   ├── winformpy.py        # Main library file
│   ├── mauipy.py           # MAUI-style components
│   └── mdipy.py            # MDI components
├── examples/               # Example applications
├── guides/                 # Documentation guides
├── tests/                  # Unit tests
├── LICENSE                 # MIT License
└── README.md               # This file
```

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- Optional: PIL/Pillow for advanced image support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Roadmap

- [x] Implement basic WinForms controls
- [x] Add MAUI-style architecture support
- [x] Add MDI support
- [x] Unit tests
- [ ] Add more examples and tutorials
- [ ] Enhanced styling and theming support
- [ ] PyPI package distribution

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**DatamanEdge**

- Version: 1.0.6

## Acknowledgments

- Inspired by Windows Forms API from Microsoft
- Built on Python's Tkinter library
- Designed to ease migration from VB6/VB.NET to Python

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Note**: This library is in active development. APIs may change in future versions.
