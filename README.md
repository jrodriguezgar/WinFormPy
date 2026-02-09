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

Following Windows Forms object model, WinFormPy is built on the principle of simplicity and encapsulation. The framework leverages its established user base and provides an intuitive way to encapsulate and manage visual object logic, making GUI development straightforward and maintainable.

Additionally, WinFormPy is a complete library to help developers familiar with Windows Forms (VB6/VB.NET) transition their applications to Python using Tkinter. It provides a familiar API that closely mimics Windows Forms controls, properties, events, and behaviors.

---

## Features

### Core Capabilities

- **Complete Windows Forms API mapping** — Controls, properties, and events that match VB.NET/VB6 syntax
- **Flexible initialization** — Support for both traditional property assignment and dictionary-based setup (`props`)
- **Event-driven programming** — Familiar VB-style event handlers
- **Form management** — UserControl and Form base classes
- **AutoSize support** — Automatic control resizing with size constraints
- **CSS styling support** — Enhanced customization options
- **Precision Border Control** — New `BorderWidth` property for individual pixel-perfect border control (essential for modern flat/Fluent UI)
- **VB-style properties** — Location, Size, Enabled, Visible, BackColor, Font, etc.

### Modules and Documentation

WinFormPy is organized into several modules, each with its own detailed documentation:

- 🏛️ **[WinFormPy Core](winformpy/README.md)**: Standard Windows Forms API (Buttons, Forms, Dialogs).
- 🎨 **[WinUI 3 Module](winformpy/WINUI3_README.md)**: Modern Fluent Design controls for Windows 11.
- 🔧 **[WinFormPy Tools](winformpy/TOOLS_REAMDE.md)**: Font, Color, CSS, and Layout utilities.
- 🏗️ **[WinFormPy Extended](winformpy/EXTENDED_README.md)**: Complex controls like `ConsoleTextBox` and `ExtendedLabel`.
- 🧩 **[UI Elements](winformpy/ui_elements/README.md)**: Pre-built components (Chat, DataGrid, DB Manager).
- 📋 **[Templates](winformpy/templates/README.md)**: Full application boilerplates (Explorer, Studio, Browser).
- 🚀 **[Examples](examples/README.md)**: Visual catalog of library features.

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

### Optional Dependencies

WinFormPy uses **lazy import** pattern for optional dependencies, ensuring the library works even if they are not installed:

```bash
# For ImageList with advanced image processing (auto-resize, format conversion)
pip install Pillow

# For web browser control
pip install tkinterweb

# For calendar controls
pip install tkcalendar
```

**Note:** All examples and library code use lazy import, so they will run with degraded functionality if optional packages are missing, showing helpful status messages instead of crashing.

See [Lazy Import Guide](guides/README_Lazy_Import.md) for implementation details.

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

## Event Handling

WinFormPy follows the standard .NET/Windows Forms event pattern. All event handlers receive two parameters:

1. `sender`: The object that raised the event.
2. `e`: An `EventArgs` object containing event data.

### Basic Event Binding

You can bind an event by assigning a method or a lambda function to the event property:

```python
# Using a method
self.button.Click = self.on_button_click

# Using a lambda
self.button.Click = lambda sender, e: print(f"Clicked {sender.Name}")
```

### Accessing Event Data

The `EventArgs` object provides properties that map to the underlying event details:

```python
def on_form_click(self, sender, e):
    # e.X and e.Y are relative to the control
    print(f"Mouse clicked at: {e.X}, {e.Y}")
  
    # Check for modifiers
    if e.Control:
        print("Control key was pressed")
```

### Event Arguments Properties

| Property                        | Description                                                      |
| ------------------------------- | ---------------------------------------------------------------- |
| `X`, `Y`                    | Mouse coordinates relative to the sender                         |
| `Button`                      | Mouse button number (1=Left, 2=Middle, 3=Right)                  |
| `KeyChar`                     | The character correspond to the key press                        |
| `KeyCode`                     | The Tkinter keysym string (e.g. 'Return', 'Escape')              |
| `Shift`, `Control`, `Alt` | Boolean flags for modifier keys                                  |
| `Data`                        | Extra data for complex controls (e.g.`NewIndex` in TabControl) |
| `Cancel`                      | Used in events like `FormClosing` to prevent the action        |

---

## Quick Start

Here's a simple example showing how to create a form with a button:

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
│   ├── templates/                   # Application boilerplates
│   │   ├── winui3_template.py       # Fluent Design / WinUI 3 style
│   │   └── dashboard_template.py    # Enterprise dashboard style
│   └── ui_elements/                 # Reusable UI components
│       ├── db_connection/           # Database connection management
│       │   ├── __init__.py          # Module exports
│       │   ├── db_connection_manager.py  # Service layer (CRUD, validation)
│       │   ├── db_connection_panel.py    # Embeddable Panel component
│       │   ├── db_connection_ui.py       # Standalone Form with ListView
│       │   └── README.md            # Component documentation
│       └── web_browser/             # Web browser suite
│           ├── __init__.py          # Module exports
│           ├── web_browser.py       # Basic WebBrowser control
│           ├── web_browser_panel.py # Panel with navigation bar
│           ├── web_browser_ui.py    # Multi-tab browser application
│           └── README.md            # Component documentation
├── examples/                        # Example applications
│   └── ui_elements/                 # UI elements examples
│       ├── db_connection_example.py # Database connection demo
│       └── web_browser_example.py   # Web browser demo
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
| [**Dock and Anchor** ⚠️](guides/README_Dock_Anchor.md)               | **Layout anchoring and docking (includes CRITICAL initialization rules)** |
| [GroupBox usage](guides/README_GroupBox.md)                          | GroupBox container guide     |
| [Labelframe container](guides/README_Labelframe_Container.md)        | Labelframe patterns          |
| [**Lazy Import Pattern**](guides/README_Lazy_Import.md)              | **Optional dependencies lazy loading (PIL, tkinterweb, etc.)** |
| [MaskedTextBox](guides/README_MaskedTextBox.md)                      | Input masking guide          |
| [MAUI concepts](guides/README_MAUI.md)                               | MAUI-style architecture      |
| [MDI patterns](guides/README_MDI.md)                                 | Multiple Document Interface  |
| [Naming conventions](guides/README_Naming.md)                        | Naming best practices        |
| [PrinterSettings](guides/README_PrinterSettings.md)                  | Printer configuration object |
| [WinFormPy extended](guides/README_winformpy_extended.md)            | Extended module guide        |
| [WinFormPy tools](guides/README_winformpy_tools.md)                  | Tools module guide           |

> **⚠️ IMPORTANT:** When using Dock or Anchor properties, read the [Dock and Anchor guide](guides/README_Dock_Anchor.md) for critical initialization rules. Failure to follow these rules may result in controls not positioning or sizing correctly.

---

## Examples

The `examples/` directory contains demonstration scripts for different library features:

| Example                                                                                            | Description                                       |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| [autosize_example.py](examples/autosize_example.py)                                                   | AutoSize behavior                                 |
| [basic_controls_example.py](examples/basic_controls_example.py)                                       | Core controls (Button, Label, TextBox)            |
| [chat_example.py](examples/chat_example.py)                                                           | Chat UI with smart response handler               |
| [console_example.py](examples/console_example.py)                                                     | Console with full command handler                 |
| [datagridview_example.py](examples/datagridview_example.py)                                           | DataGridView with data binding and filtering      |
| [data_grid_crud_example.py](examples/data_grid_crud_example.py)                                       | Complete CRUD operations with DataGrid            |
| [db_connection_example.py](examples/db_connection_example.py)                                         | Database connection manager demo                  |
| [dialogs_example.py](examples/dialogs_example.py)                                                     | Common dialogs usage                              |
| [dock_anchor_example.py](examples/dock_anchor_example.py)                                             | Dock and Anchor settings                          |
| [email_example.py](examples/email_example.py)                                                         | Email client with folders and composition         |
| [groupbox_autosizemode_radiobutton_example.py](examples/groupbox_autosizemode_radiobutton_example.py) | GroupBox with AutoSizeMode and RadioButtons       |
| [hierarchical_visibility_example.py](examples/hierarchical_visibility_example.py)                     | Parent-child visibility rules                     |
| [imagelist_example.py](examples/imagelist_example.py)                                                 | ImageList with ListView, TreeView, and Buttons    |
| [layouts_example.py](examples/layouts_example.py)                                                     | FlowLayoutPanel and TableLayoutPanel              |
| [layout_manager_example.py](examples/layout_manager_example.py)                                       | Layout manager usage                              |
| [listbox_checkedlistbox_example.py](examples/listbox_checkedlistbox_example.py)                       | ListBox and CheckedListBox controls               |
| [listview_example.py](examples/listview_example.py)                                                   | ListView with columns, sorting, and selection     |
| [login_example.py](examples/login_example.py)                                                         | Login form with multiple users                    |
| [maskedtextbox_example.py](examples/maskedtextbox_example.py)                                         | MaskedTextBox control                             |
| [master_detail_example.py](examples/master_detail_example.py)                                         | Master-detail layouts (vertical/horizontal)       |
| [menustrip_example.py](examples/menustrip_example.py)                                                 | MenuStrip with hierarchical menus                 |
| [more_controls_example.py](examples/more_controls_example.py)                                         | Additional controls showcase                      |
| [printersettings_example.py](examples/printersettings_example.py)                                     | PrinterSettings object usage and dialogs          |
| [record_form_example.py](examples/record_form_example.py)                                             | RecordForm in different modes                     |
| [richtextbox_example.py](examples/richtextbox_example.py)                                             | RichTextBox control with formatting               |
| [splitcontainer_example.py](examples/splitcontainer_example.py)                                       | SplitContainer with resizable panels              |
| [statusbar_example.py](examples/statusbar_example.py)                                                 | StatusBar control (.NET 1.x)                      |
| [dotnet2_controls_example.py](examples/dotnet2_controls_example.py)                                   | .NET 2.0 controls (MenuStrip, ToolStrip, StatusStrip, ContextMenuStrip) |
| [tooltip_example.py](examples/tooltip_example.py)                                                     | ToolTip configuration                             |
| [trackbar_example.py](examples/trackbar_example.py)                                                   | TrackBar slider controls                          |
| [treeview_example.py](examples/treeview_example.py)                                                   | TreeView with hierarchical data                   |
| [web_browser_example.py](examples/web_browser_example.py)                                             | Web browser with tabs and navigation              |
| [winformpy_extended_example.py](examples/winformpy_extended_example.py)                               | Extended APIs demo                                |
| [word_processor_example.py](examples/word_processor_example.py)                                       | WordPad-style word processor                      |

**Run any example:**

```bash
uv run examples/<example_name>.py
```

> **Note:** Each UI Element module (in `winformpy/ui_elements/`) includes its own runnable demo when executed directly. For example:
>
> ```bash
> uv run winformpy/ui_elements/data_grid/data_grid_panel.py
> uv run winformpy/ui_elements/login/login_panel.py
> ```

---

## Application Templates

The `winformpy/templates/` directory contains complete application templates demonstrating real-world usage patterns and modern UI styles:

| Template                  | Description                                                                            | Run Command                                                |
| ------------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **Studio App**      | IDE-style application (like VS Code) with activity bar, sidebar, and editor tabs       | `uv run winformpy/templates/studio_template.py`          |
| **File Explorer**   | Windows 11 File Explorer style app with navigation pane, breadcrumbs, and command bar  | `uv run winformpy/templates/explorer_template.py`        |
| **Web Browser**     | Chrome-style web browser with tabs, address bar, and history (requires `tkinterweb`) | `uv run winformpy/templates/browser_template.py`         |
| **MAUI App**        | Multi-platform App UI architecture pattern                                             | `uv run winformpy/templates/maui_template.py`            |
| **MDI App**         | Multiple Document Interface application                                                | `uv run winformpy/templates/mdi_template.py`             |
| **Navigation Pane** | Collapsible sidebar (hamburger menu) layout                                            | `uv run winformpy/templates/navigation_pane_template.py` |
| **Navigation Rail** | Slim vertical navigation rail with fixed icons                                         | `uv run winformpy/templates/navigation_rail_template.py` |
| **WinUI 3 Gallery** | WinUI 3 style interactive controls gallery                                             | `uv run winformpy/templates/winui3_template.py`          |

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
