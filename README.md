# WinFormPy

**A comprehensive Python library that maps Windows Forms/VB syntax and objects to Tkinter**

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
  - [Control Reference](#control-reference)
- [API Reference](#api-reference)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Guides](#guides)
- [Examples](#examples)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [License](#license)

---

## Overview

WinFormPy is a complete library designed to help developers familiar with Windows Forms (VB6/VB.NET) transition their applications to Python using Tkinter. It provides a familiar API that closely mimics Windows Forms controls, properties, events, and behaviors.

---

## Features

### Core Capabilities

- **Complete Windows Forms API mapping** — Controls, properties, and events that match VB.NET/VB6 syntax
- **Flexible initialization** — Support for both traditional property assignment and dictionary-based setup (`props`)
- **Event-driven programming** — Familiar VB-style event handlers
- **Form management** — UserControl and Form base classes
- **AutoSize support** — Automatic control resizing with size constraints
- **CSS styling support** — Enhanced customization options
- **VB-style properties** — Location, Size, Enabled, Visible, BackColor, Font, etc.

### Modules

| Module                 | Description                                     |
| ---------------------- | ----------------------------------------------- |
| `winformpy`          | Core Windows Forms controls and dialogs         |
| `winformpy_extended` | Extended controls                               |
| `winformpy_tools`    | Helper tools and utilities                      |
| `mauipy`             | MAUI-style architecture (Shell, Pages, Layouts) |
| `mdipy`              | Multiple Document Interface (MDI) support       |

---

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
pip install -e .
```

---

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

---

## Documentation

### Control Reference

#### Basic Controls

| Control                        | Description                  |
| ------------------------------ | ---------------------------- |
| [Button](#button)                 | Standard clickable button    |
| [Label](#label)                   | Static text display          |
| [LinkLabel](#linklabel)           | Clickable hyperlink label    |
| [TextBox](#textbox)               | Single/multi-line text input |
| [RichTextBox](#richtextbox)       | Rich text editor             |
| [MaskedTextBox](#maskedtextbox)   | Input with mask formatting   |
| [CheckBox](#checkbox)             | Boolean toggle control       |
| [RadioButton](#radiobutton)       | Mutually exclusive option    |
| [ComboBox](#combobox)             | Dropdown selection list      |
| [ListBox](#listbox)               | Scrollable item list         |
| [CheckedListBox](#checkedlistbox) | List with checkboxes         |

#### Numeric Controls

| Control                      | Description             |
| ---------------------------- | ----------------------- |
| [NumericUpDown](#numericupdown) | Numeric spinner control |
| [DomainUpDown](#domainupdown)   | Text spinner control    |
| [TrackBar](#trackbar)           | Slider control          |
| [ProgressBar](#progressbar)     | Progress indicator      |

#### Date and Time Controls

| Control                      | Description            |
| ---------------------------- | ---------------------- |
| [DatePicker](#datepicker)       | Date selection control |
| [MonthCalendar](#monthcalendar) | Calendar display       |

#### Container Controls

| Control                            | Description              |
| ---------------------------------- | ------------------------ |
| [Form](#form)                         | Main application window  |
| [UserControl](#usercontrol)           | Custom composite control |
| [Panel](#panel)                       | Basic container          |
| [GroupBox](#groupbox)                 | Titled border container  |
| [TabControl](#tabcontrol)             | Tabbed container         |
| [TabPage](#tabpage)                   | Individual tab page      |
| [SplitContainer](#splitcontainer)     | Resizable split panels   |
| [FlowLayoutPanel](#flowlayoutpanel)   | Auto-flowing layout      |
| [TableLayoutPanel](#tablelayoutpanel) | Grid-based layout        |

#### Data Display Controls

| Control                    | Description               |
| -------------------------- | ------------------------- |
| [DataGridView](#datagridview) | Tabular data display      |
| [ListView](#listview)         | Multi-column list         |
| [TreeView](#treeview)         | Hierarchical data display |

#### Media Controls

| Control                | Description       |
| ---------------------- | ----------------- |
| [PictureBox](#picturebox) | Image display     |
| [Line](#line)             | Graphical line    |
| [CanvasLine](#canvasline) | Canvas-based line |

#### Menu and Toolbar Controls

| Control                                    | Description        |
| ------------------------------------------ | ------------------ |
| [MenuStrip](#menustrip)                       | Main menu bar      |
| [ToolStrip](#toolstrip)                       | Toolbar container  |
| [StatusStrip](#statusstrip)                   | Status bar         |
| [StatusBar](#statusbar)                       | Classic status bar |
| [ToolStripButton](#toolstripbutton)           | Toolbar button     |
| [ToolStripLabel](#toolstriplabel)             | Toolbar label      |
| [ToolStripMenuItem](#toolstripmenuitem)       | Menu item          |
| [ToolStripSeparator](#toolstripseparator)     | Toolbar separator  |
| [ToolStripTextBox](#toolstriptextbox)         | Toolbar text input |
| [ToolStripComboBox](#toolstripcombobox)       | Toolbar dropdown   |
| [ToolStripProgressBar](#toolstripprogressbar) | Toolbar progress   |
| [ToolStripStatusLabel](#toolstripstatuslabel) | Status bar label   |

#### Scroll Controls

| Control                | Description          |
| ---------------------- | -------------------- |
| [HScrollBar](#hscrollbar) | Horizontal scrollbar |
| [VScrollBar](#vscrollbar) | Vertical scrollbar   |

#### Dialogs

| Dialog                                 | Description            |
| -------------------------------------- | ---------------------- |
| [MessageBox](#messagebox)                 | Message display dialog |
| [InputBox](#inputbox)                     | Text input dialog      |
| [OpenFileDialog](#openfiledialog)         | File open dialog       |
| [SaveFileDialog](#savefiledialog)         | File save dialog       |
| [ColorDialog](#colordialog)               | Color picker dialog    |
| [FontDialog](#fontdialog)                 | Font selection dialog  |
| [PrintDialog](#printdialog)               | Print settings dialog  |
| [PageSetupDialog](#pagesetupdialog)       | Page setup dialog      |
| [PrintPreviewDialog](#printpreviewdialog) | Print preview dialog   |

#### Utilities

| Utility              | Description           |
| -------------------- | --------------------- |
| [Timer](#timer)         | Interval-based events |
| [ToolTip](#tooltip)     | Hover tooltips        |
| [ImageList](#imagelist) | Image collection      |
| [Screen](#screen)       | Screen information    |

#### Extended Controls (`winformpy_extended`)

| Control       | Description                                    |
| ------------- | ---------------------------------------------- |
| ExtendedLabel | Label with dynamic text wrapping and alignment |

#### MDI Components (`mdipy`)

Multiple Document Interface (MDI) allows creating applications with a parent window that contains multiple child windows, similar to classic Windows applications like Excel or Word.

| Component | Description                                                  |
| --------- | ------------------------------------------------------------ |
| MDIParent | MDI parent form that contains child windows in a client area |
| MDIChild  | MDI child window embedded within the parent's client area    |

#### MAUI Components (`mauipy`)

MAUI-style components provide a modern approach to building cross-platform-like applications with navigation patterns, layouts, and UI components inspired by .NET MAUI.

| Component             | Description                 |
| --------------------- | --------------------------- |
| Shell                 | Application shell container |
| ContentPage           | Basic page container        |
| NavigationPage        | Navigation stack            |
| TabbedPage            | Tabbed navigation           |
| FlyoutPage            | Side menu page              |
| FlyoutMenu            | Slide-out menu              |
| CarouselView          | Swipeable carousel          |
| VerticalStackLayout   | Vertical stacking           |
| HorizontalStackLayout | Horizontal stacking         |
| Grid                  | Grid-based layout           |
| SwipeLayout           | Swipe gesture container     |
| PopUpFlyout           | Popup menu                  |
| ToastNotification     | Toast messages              |
| SearchBarComponent    | Search input                |
| ChipTag               | Tag/chip display            |
| StepperControl        | Step increment control      |

#### Tools and Managers (`winformpy_tools`)

| Class             | Description                                                |
| ----------------- | ---------------------------------------------------------- |
| FontManager       | System fonts retrieval and management                      |
| ColorManager      | System colors retrieval via Windows API                    |
| CSSManager        | CSS parsing and conversion to Tkinter/WinFormPy properties |
| LayoutManager     | Automatic control distribution (Flow, AutoSize, etc.)      |
| AutoLayoutManager | Alias for LayoutManager                                    |

**FontManager Methods:**

| Method                        | Description                                               |
| ----------------------------- | --------------------------------------------------------- |
| `get_system_fonts()`        | Get dictionary with all system fonts                      |
| `get_system_font(type)`     | Get a specific system font (default, menu, caption, etc.) |
| `get_all_available_fonts()` | Get list of all available fonts on the system             |

**ColorManager Methods:**

| Method                     | Description                                               |
| -------------------------- | --------------------------------------------------------- |
| `get_system_colors()`    | Get dictionary with Windows system colors                 |
| `get_system_color(type)` | Get a specific system color (control, window, text, etc.) |

**CSSManager Methods:**

| Method                                      | Description                          |
| ------------------------------------------- | ------------------------------------ |
| `parse_css_string(css)`                   | Parse CSS string to dictionary       |
| `css_to_winform_props(css)`               | Convert CSS to WinFormPy properties  |
| `css_to_tkinter_config(css)`              | Convert CSS to Tkinter config        |
| `apply_css_to_widget(widget, css)`        | Apply CSS directly to Tkinter widget |
| `apply_css_to_winform_control(ctrl, css)` | Apply CSS to WinFormPy control       |

**LayoutManager Properties:**

| Property         | Description                                     |
| ---------------- | ----------------------------------------------- |
| `Distribution` | UpDown (vertical) or LeftRight (horizontal)     |
| `Alignment`    | Up, Down, Left, Right, Center                   |
| `LayoutType`   | FlowLayout, Autosize, Dock, Anchor, TableLayout |
| `margin`       | Space between controls                          |
| `padding`      | Space from container borders                    |
| `wrap_count`   | Items per row/column before wrapping            |

#### UI Elements (`ui_elements`)

UI Elements are pre-built, reusable high-level components that combine multiple controls to provide complete functionality for common application needs. These components are designed to be easily integrated into your applications, saving development time.

##### Database Connection Components

A complete solution for managing database connections with support for multiple database types, connection testing, and CRUD operations.

| Component           | Description                                             |
| ------------------- | ------------------------------------------------------- |
| DBConnectionManager | Service layer for database connection CRUD operations   |
| DBConnectionPanel   | Embeddable Panel for connection management              |
| DBConnectionUI      | Standalone Form for connection management with ListView |

**Supported Database Types:**

- SQL: Oracle, MySQL, PostgreSQL, SQLite, SQL Server, Access
- NoSQL: MongoDB, Cassandra, Neo4j, Elasticsearch, Redis

**DBConnectionManager Methods:**

| Method                             | Description                    |
| ---------------------------------- | ------------------------------ |
| `save(name, data)`               | Save or update a connection    |
| `read(name)`                     | Read a specific connection     |
| `read_all()`                     | Read all connections           |
| `delete(name)`                   | Delete a connection            |
| `list_names()`                   | List all connection names      |
| `test_connection(data)`          | Test database connectivity     |
| `validate_connection_data(data)` | Validate connection parameters |

#### System Classes

| Class        | Description             |
| ------------ | ----------------------- |
| SystemColors | System color palette    |
| SystemFonts  | System font definitions |
| SystemStyles | System UI styles        |
| Color        | Color manipulation      |
| Font         | Font configuration      |
| Size         | Width/height tuple      |
| Point        | X/Y coordinate tuple    |
| Rectangle    | Bounds definition       |
| Cursors      | Cursor types            |

#### Enumerations

| Enum                | Description           |
| ------------------- | --------------------- |
| AnchorStyles        | Control anchoring     |
| AutoSizeMode        | AutoSize behavior     |
| BorderStyle         | Border appearance     |
| CheckState          | Checkbox state        |
| ContentAlignment    | Content positioning   |
| DockStyle           | Docking position      |
| FlowDirection       | Flow layout direction |
| FormBorderStyle     | Form border type      |
| FormStartPosition   | Form initial position |
| FormWindowState     | Window state          |
| HorizontalAlignment | Horizontal alignment  |
| Orientation         | Horizontal/vertical   |
| PictureBoxSizeMode  | Image sizing mode     |
| ScrollBars          | Scrollbar visibility  |
| SelectionMode       | Selection behavior    |
| TabAlignment        | Tab position          |
| View                | ListView view mode    |

---

## API Reference

### Common Properties

All controls inherit these standard properties:

| Property        | Type             | Description        |
| --------------- | ---------------- | ------------------ |
| `Name`        | `str`          | Control identifier |
| `Text`        | `str`          | Display text       |
| `Left`        | `int`          | X position         |
| `Top`         | `int`          | Y position         |
| `Width`       | `int`          | Control width      |
| `Height`      | `int`          | Control height     |
| `Location`    | `tuple`        | (Left, Top)        |
| `Size`        | `tuple`        | (Width, Height)    |
| `Enabled`     | `bool`         | Enable/disable     |
| `Visible`     | `bool`         | Show/hide          |
| `BackColor`   | `str`          | Background color   |
| `ForeColor`   | `str`          | Text color         |
| `Font`        | `tuple`        | Font (name, size)  |
| `BorderStyle` | `Enum`         | Border appearance  |
| `Dock`        | `DockStyle`    | Docking behavior   |
| `Anchor`      | `AnchorStyles` | Anchoring behavior |
| `AutoSize`    | `bool`         | Automatic sizing   |
| `Padding`     | `tuple`        | Internal padding   |
| `Margin`      | `tuple`        | External margin    |
| `TabIndex`    | `int`          | Tab order          |
| `TabStop`     | `bool`         | Include in tab     |
| `Cursor`      | `str`          | Mouse cursor       |

### Common Events

| Event           | Description           |
| --------------- | --------------------- |
| `Click`       | Mouse click           |
| `DoubleClick` | Mouse double-click    |
| `MouseDown`   | Mouse button pressed  |
| `MouseUp`     | Mouse button released |
| `MouseEnter`  | Mouse enters control  |
| `MouseLeave`  | Mouse leaves control  |
| `MouseMove`   | Mouse movement        |
| `KeyDown`     | Key pressed           |
| `KeyUp`       | Key released          |
| `KeyPress`    | Character typed       |
| `Enter`       | Control gains focus   |
| `Leave`       | Control loses focus   |
| `Paint`       | Control repaint       |
| `Resize`      | Control resized       |
| `Load`        | Control loaded        |

### Common Methods

| Method                  | Description          |
| ----------------------- | -------------------- |
| `Show()`              | Display control      |
| `Hide()`              | Hide control         |
| `Focus()`             | Set keyboard focus   |
| `Refresh()`           | Force repaint        |
| `BringToFront()`      | Raise z-order        |
| `SendToBack()`        | Lower z-order        |
| `AddControl(ctrl)`    | Add child control    |
| `RemoveControl(ctrl)` | Remove child control |

---

## Control Examples

### Button

```python
button = Button(form)
button.Text = "Submit"
button.Location = (10, 10)
button.Size = (100, 30)
button.Click = lambda sender, e: print("Clicked!")
```

### Label

```python
label = Label(form)
label.Text = "Hello World"
label.AutoSize = True
label.Font = ("Arial", 12)
```

### TextBox

```python
textbox = TextBox(form)
textbox.Text = ""
textbox.Multiline = False
textbox.PasswordChar = "*"
textbox.TextChanged = lambda s, e: print(textbox.Text)
```

### ComboBox

```python
combo = ComboBox(form)
combo.Items = ["Option 1", "Option 2", "Option 3"]
combo.SelectedIndex = 0
combo.SelectedIndexChanged = lambda s, e: print(combo.SelectedItem)
```

### CheckBox

```python
checkbox = CheckBox(form)
checkbox.Text = "Enable feature"
checkbox.Checked = True
checkbox.CheckedChanged = lambda s, e: print(checkbox.Checked)
```

### RadioButton

```python
radio = RadioButton(form)
radio.Text = "Option A"
radio.Checked = True
radio.CheckedChanged = lambda s, e: print(radio.Checked)
```

### ListBox

```python
listbox = ListBox(form)
listbox.Items = ["Item 1", "Item 2", "Item 3"]
listbox.SelectionMode = SelectionMode.Multiple
listbox.SelectedIndexChanged = lambda s, e: print(listbox.SelectedItems)
```

### DataGridView

```python
dgv = DataGridView(form)
dgv.Columns = ["Name", "Age", "City"]
dgv.DataSource = [
    {"Name": "John", "Age": 30, "City": "New York"},
    {"Name": "Jane", "Age": 25, "City": "London"}
]
```

### TreeView

```python
tree = TreeView(form)
root = tree.AddNode("Root")
child1 = tree.AddNode("Child 1", parent=root)
child2 = tree.AddNode("Child 2", parent=root)
```

### GroupBox

```python
group = GroupBox(form, {'Text': 'Options', 'Width': 200, 'Height': 150})
radio1 = RadioButton(group, {'Text': 'Option 1', 'Checked': True})
radio2 = RadioButton(group, {'Text': 'Option 2', 'Top': 30})
```

### Panel

```python
panel = Panel(form)
panel.BorderStyle = BorderStyle.FixedSingle
panel.Dock = DockStyle.Fill
panel.AutoScroll = True
```

### TabControl

```python
tabs = TabControl(form)
page1 = TabPage(tabs, {'Text': 'Tab 1'})
page2 = TabPage(tabs, {'Text': 'Tab 2'})
tabs.TabPages.Add(page1)
tabs.TabPages.Add(page2)
```

### MessageBox

```python
result = MessageBox.Show(
    "Do you want to continue?",
    "Confirmation",
    buttons="YesNo",
    icon="Question"
)
```

### OpenFileDialog

```python
dialog = OpenFileDialog()
dialog.Filter = "Text Files|*.txt|All Files|*.*"
dialog.Title = "Select a file"
filename = dialog.ShowDialog()
```

### Timer

```python
timer = Timer()
timer.Interval = 1000  # milliseconds
timer.Tick = lambda s, e: print("Tick!")
timer.Start()
```

### ProgressBar

```python
progress = ProgressBar(form)
progress.Minimum = 0
progress.Maximum = 100
progress.Value = 50
progress.Style = ProgressBarStyle.Continuous
```

### TrackBar

```python
trackbar = TrackBar(form)
trackbar.Minimum = 0
trackbar.Maximum = 100
trackbar.Value = 50
trackbar.TickFrequency = 10
trackbar.ValueChanged = lambda s, e: print(trackbar.Value)
```

### NumericUpDown

```python
numeric = NumericUpDown(form)
numeric.Minimum = 0
numeric.Maximum = 100
numeric.Value = 50
numeric.Increment = 5
numeric.ValueChanged = lambda s, e: print(numeric.Value)
```

### DatePicker

```python
datepicker = DatePicker(form)
datepicker.Format = DatePickerFormat.Short
datepicker.ValueChanged = lambda s, e: print(datepicker.Value)
```

### MaskedTextBox

```python
masked = MaskedTextBox(form)
masked.Mask = "(999) 000-0000"  # Phone format
masked.PromptChar = "_"
```

### PictureBox

```python
picture = PictureBox(form)
picture.Image = "path/to/image.png"
picture.SizeMode = PictureBoxSizeMode.Zoom
```

### MenuStrip

```python
menu = MenuStrip(form)
file_menu = ToolStripMenuItem(menu, {'Text': 'File'})
exit_item = ToolStripMenuItem(file_menu, {'Text': 'Exit'})
exit_item.Click = lambda s, e: form.Close()
```

### StatusStrip

```python
status = StatusStrip(form)
label = ToolStripStatusLabel(status, {'Text': 'Ready'})
```

### ExtendedLabel

```python
from winformpy.winformpy_extended import ExtendedLabel

# Label with automatic text wrapping
label = ExtendedLabel(form, {
    'Text': 'This is a long text that will automatically wrap to fit the control width.',
    'Width': 200,
    'Height': 100,
    'TextAlign': 'MiddleCenter'
})
```

### FontManager

```python
from winformpy.winformpy_tools import FontManager

# Get all system fonts
fonts = FontManager.get_system_fonts()
print(fonts['default'])  # ('Segoe UI', 9)

# Get a specific system font
caption_font = FontManager.get_system_font('caption')  # ('Segoe UI', 9, 'bold')

# Get all available fonts
all_fonts = FontManager.get_all_available_fonts()
```

### ColorManager

```python
from winformpy.winformpy_tools import ColorManager

# Get all system colors
colors = ColorManager.get_system_colors()
print(colors['window'])     # '#FFFFFF'
print(colors['highlight'])  # '#0078D7'

# Get a specific system color
control_color = ColorManager.get_system_color('control')  # '#F0F0F0'
```

### CSSManager

```python
from winformpy.winformpy_tools import CSSManager

# Parse CSS string
styles = CSSManager.parse_css_string("color: blue; font-size: 12px")

# Convert CSS to WinFormPy properties
props = CSSManager.css_to_winform_props(
    "background-color: #F0F0F0; font-family: Arial; font-size: 14px"
)
# Result: {'BackColor': '#F0F0F0', 'Font': ('Arial', 14)}

# Apply CSS to a control
CSSManager.apply_css_to_winform_control(button, "color: white; background-color: blue")
```

### LayoutManager

```python
from winformpy.winformpy_tools import LayoutManager

# Create a panel with automatic layout
panel = Panel(form, {'Width': 400, 'Height': 300})

# Initialize layout manager
layout = LayoutManager(panel, margin=10, padding=5, autosize_container=True)
layout.distribution = LayoutManager.Distribution.UpDown  # Vertical layout

# Add controls - they will be positioned automatically
layout.add_control(Button(panel, {'Text': 'Button 1', 'Width': 100, 'Height': 30}))
layout.add_control(Button(panel, {'Text': 'Button 2', 'Width': 100, 'Height': 30}))
layout.add_control(Button(panel, {'Text': 'Button 3', 'Width': 100, 'Height': 30}))

# Horizontal flow layout with wrapping
layout2 = LayoutManager(panel, margin=5, wrap_count=3)
layout2.distribution = LayoutManager.Distribution.LeftRight
```

### DBConnectionManager

```python
from winformpy.ui_elements.db_connection import DBConnectionManager

# Initialize with your storage backend
manager = DBConnectionManager(storage_backend)

# Save a connection
manager.save('my_database', {
    'type': 'postgresql',
    'host': 'localhost',
    'port': 5432,
    'database': 'mydb',
    'user': 'admin',
    'password': 'secret'
})

# Read a connection
config = manager.read('my_database')

# List all connections
names = manager.list_names()

# Test connectivity
success, message = manager.test_connection(config)
```

### DBConnectionPanel

```python
from winformpy.ui_elements.db_connection import DBConnectionManager, DBConnectionPanel

# Embeddable panel for connection management
manager = DBConnectionManager(storage_backend)
panel = DBConnectionPanel(form, manager, {
    'Left': 10,
    'Top': 10,
    'Width': 500,
    'Height': 400
})
```

### DBConnectionUI

```python
from winformpy.ui_elements.db_connection import DBConnectionManager, DBConnectionUI

# Standalone form with ListView
manager = DBConnectionManager(storage_backend)
ui = DBConnectionUI(manager)
ui.ShowDialog()
```

---

## Architecture

WinFormPy is built on three main layers:

```
┌─────────────────────────────────────────────┐
│              Application Layer              │
│         (Forms, UserControls, MDI)          │
├─────────────────────────────────────────────┤
│              Control Layer                  │
│    (Button, Label, TextBox, DataGridView)   │
├─────────────────────────────────────────────┤
│              Base Layer                     │
│   (ControlBase, ScrollableControlMixin)     │
├─────────────────────────────────────────────┤
│              Tkinter                        │
└─────────────────────────────────────────────┘
```

1. **ControlBase** — Base class providing common functionality for all controls
2. **Specific Controls** — Individual control implementations (Button, Label, etc.)
3. **Container Controls** — Forms, Panels, and UserControls that host other controls
4. **Mixins** — ScrollableControlMixin for scrolling support

---

## Project Structure

```
WinFormPy/
├── winformpy/
│   ├── __init__.py                  # Package initialization
│   ├── winformpy.py                 # Core library (controls, dialogs, enums)
│   ├── winformpy_extended.py        # Extended controls (ExtendedLabel)
│   ├── winformpy_tools.py           # Utilities (FontManager, ColorManager, CSSManager, LayoutManager)
│   ├── mauipy.py                    # MAUI-style components (Shell, Pages, Layouts)
│   ├── mdipy.py                     # MDI components (MDIParent, MDIChild)
│   └── ui_elements/                 # Reusable UI components
│       └── db_connection/           # Database connection management
│           ├── __init__.py          # Module exports
│           ├── db_connection_manager.py  # Service layer (CRUD, validation)
│           ├── db_connection_panel.py    # Embeddable Panel component
│           ├── db_connection_ui.py       # Standalone Form with ListView
│           └── README.md            # Component documentation
├── examples/                        # Example applications
├── guides/                          # Documentation guides
├── tests/                           # Unit tests
├── pyproject.toml                   # Project configuration
├── LICENSE                          # MIT License
├── LLMs.txt                     # LLM context file
└── README.md                    # This file
```

---

## Guides

Detailed documentation guides covering specific aspects of the library:

| Guide                                                             | Description                  |
| ----------------------------------------------------------------- | ---------------------------- |
| [AutoSize behavior](guides/README_Autosize.md)                       | Control automatic sizing     |
| [Container best practices](guides/README_Container_Best_Practice.md) | Container usage patterns     |
| [Dock and Anchor](guides/README_Dock_Anchor.md)                      | Layout anchoring and docking |
| [GroupBox usage](guides/README_GroupBox.md)                          | GroupBox container guide     |
| [Labelframe container](guides/README_Labelframe_Container.md)        | Labelframe patterns          |
| [MaskedTextBox](guides/README_MaskedTextBox.md)                      | Input masking guide          |
| [MAUI concepts](guides/README_MAUI.md)                               | MAUI-style architecture      |
| [MDI patterns](guides/README_MDI.md)                                 | Multiple Document Interface  |
| [Naming conventions](guides/README_Naming.md)                        | Naming best practices        |
| [WinFormPy extended](guides/README_winformpy_extended.md)            | Extended module guide        |
| [WinFormPy tools](guides/README_winformpy_tools.md)                  | Tools module guide           |

---

## Examples

The `examples/` directory contains demonstration scripts for different library features:

| Example                                                                                            | Description                                 |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| [autolayout_nested_example.py](examples/autolayout_nested_example.py)                                 | Nested AutoLayout containers                |
| [autosize_example.py](examples/autosize_example.py)                                                   | AutoSize behavior                           |
| [basic_controls_example.py](examples/basic_controls_example.py)                                       | Core controls (Button, Label, TextBox)      |
| [dialogs_example.py](examples/dialogs_example.py)                                                     | Common dialogs usage                        |
| [dock_anchor_example.py](examples/dock_anchor_example.py)                                             | Dock and Anchor settings                    |
| [groupbox_autosizemode_radiobutton_example.py](examples/groupbox_autosizemode_radiobutton_example.py) | GroupBox with AutoSizeMode and RadioButtons |
| [hierarchical_visibility_example.py](examples/hierarchical_visibility_example.py)                     | Parent-child visibility rules               |
| [layouts_example.py](examples/layouts_example.py)                                                     | Layout patterns overview                    |
| [layout_manager_example.py](examples/layout_manager_example.py)                                       | Layout manager usage                        |
| [maskedtextbox_example.py](examples/maskedtextbox_example.py)                                         | MaskedTextBox control                       |
| [maui_example.py](examples/maui_example.py)                                                           | MAUI-style shell/pages                      |
| [mdi_example.py](examples/mdi_example.py)                                                             | MDI forms                                   |
| [more_controls_example.py](examples/more_controls_example.py)                                         | Additional controls showcase                |
| [tooltip_example.py](examples/tooltip_example.py)                                                     | ToolTip configuration                       |
| [winformpy_extended_example.py](examples/winformpy_extended_example.py)                               | Extended APIs demo                          |

**Run any example:**

```bash
uv run examples/<example_name>.py
```

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

For major changes, please open an issue first to discuss what you would like to change.

---

## Roadmap

- [X] Implement basic WinForms controls
- [X] Add MAUI-style architecture support
- [X] Add MDI support
- [X] Unit tests
- [ ] Add more examples and tutorials
- [ ] Enhanced styling and theming support
- [ ] PyPI package distribution
- [ ] Complete API documentation

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Author

**DatamanEdge**

---

## Acknowledgments

- Inspired by Windows Forms API from Microsoft
- Built on Python's Tkinter library
- Designed to ease migration from VB6/VB.NET to Python

---

## Support

For issues, questions, or suggestions, please [open an issue](https://github.com/DatamanEdge/WinFormPy/issues) on GitHub.

---

> **Note**: This library is in active development. APIs may change in future versions.
