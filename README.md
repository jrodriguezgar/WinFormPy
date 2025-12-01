# WinFormPy

**A comprehensive Python library that maps Windows Forms/VB syntax and objects to Tkinter**

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Overview

WinFormPy is a complete library designed to help developers familiar with Windows Forms (VB6/VB.NET) transition their applications to Python using Tkinter. It provides a familiar API that closely mimics Windows Forms controls, properties, events, and behaviors.

## Features

- **Complete Windows Forms API mapping** - Controls, properties, and events that match VB.NET/VB6 syntax
- **Comprehensive control library** including:
  - Basic controls: Button, Label, TextBox, CheckBox, ComboBox, ListBox
  - Advanced controls: DataGridView, TreeView, TabControl, Panel, PictureBox
  - Dialogs: OpenFileDialog, SaveFileDialog, PrintDialog, MessageBox, InputBox
  - Specialized controls: MaskedTextBox, CheckedListBox, ProgressBar, TrackBar
- **Event-driven programming** with familiar VB-style event handlers
- **Form management** with UserControl and Form base classes
- **Built-in utilities**: ImageList, Timer, ToolTip, ContextMenuStrip, MenuStrip
- **CSS styling support** for enhanced customization
- **VB-style properties**: Location, Size, Enabled, Visible, BackColor, Font, etc.

## Installation

### From Source

```bash
git clone https://github.com/DatamanEdge/WinFormPy.git
cd WinFormPy
```

### Using pip (if published)

```bash
pip install winformpy
```

## Quick Start

Here's a simple example showing how to create a form with a button:

```python
import tkinter as tk
from lib.winform_py import Form, Button, Label, MessageBox

class MyForm(Form):
    def __init__(self):
        super().__init__(
            Text="My First WinFormPy App",
            Width=400,
            Height=300,
            StartPosition="CenterScreen"
        )
        
        # Create a label
        self.label = Label(
            self,
            Text="Hello, WinFormPy!",
            Left=50,
            Top=50,
            Font=("Arial", 14)
        )
        
        # Create a button
        self.button = Button(
            self,
            Text="Click Me!",
            Left=50,
            Top=100,
            Width=120,
            Height=40
        )
        self.button.Click = self.button_click
    
    def button_click(self):
        MessageBox.Show("Button was clicked!", "Info")

if __name__ == "__main__":
    app = MyForm()
    app.Show()
```

## Documentation

### Basic Controls

#### Button
```python
button = Button(
    form,
    Text="Submit",
    Left=10,
    Top=10,
    Width=100,
    Height=30,
    Enabled=True,
    Visible=True
)
button.Click = lambda: print("Button clicked!")
```

#### TextBox
```python
textbox = TextBox(
    form,
    Text="",
    Left=10,
    Top=50,
    Width=200,
    Height=25,
    Multiline=False,
    ReadOnly=False,
    PasswordChar="*"  # For password fields
)
textbox.TextChanged = lambda: print(f"Text: {textbox.get_Text()}")
```

#### ComboBox
```python
combo = ComboBox(
    form,
    Items=["Option 1", "Option 2", "Option 3"],
    Left=10,
    Top=90,
    Width=200,
    SelectedIndex=0
)
combo.SelectedIndexChanged = lambda: print(f"Selected: {combo.get_SelectedItem()}")
```

### Advanced Controls

#### DataGridView
```python
dgv = DataGridView(
    form,
    Left=10,
    Top=10,
    Width=400,
    Height=200,
    Columns=["Name", "Age", "City"]
)

# Add data
data = [
    {"Name": "John", "Age": 30, "City": "New York"},
    {"Name": "Jane", "Age": 25, "City": "London"}
]
dgv.set_DataSource(data)
```

#### TreeView
```python
tree = TreeView(
    form,
    Left=10,
    Top=10,
    Width=250,
    Height=300
)

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
        super().__init__(
            parent,
            Width=300,
            Height=200,
            BackColor="lightgray"
        )
        
        # Add controls to the UserControl
        self.label = Label(self, Text="Custom Control", Left=10, Top=10)

class MainForm(Form):
    def __init__(self):
        super().__init__(Text="Main Form", Width=500, Height=400)
        
        # Add custom control
        self.custom = CustomControl(self)
        self.custom.Location = (50, 50)
```

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
├── lib/
│   └── winform_py.py       # Main library file
├── examples/               # Example applications (coming soon)
├── LICENSE                 # MIT License
└── README.md              # This file
```

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- Optional: PIL/Pillow for advanced image support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Roadmap

- [ ] Add more examples and tutorials
- [ ] Implement remaining WinForms controls
- [ ] Enhanced styling and theming support
- [ ] Better documentation with API reference
- [ ] Unit tests
- [ ] PyPI package distribution

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**DatamanEdge**
- Version: 1.0.0
- Date: 2025-11-29

## Acknowledgments

- Inspired by Windows Forms API from Microsoft
- Built on Python's Tkinter library
- Designed to ease migration from VB6/VB.NET to Python

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Note**: This library is in active development. APIs may change in future versions.
