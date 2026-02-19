# WinFormPy Core Library

This module provides the core Windows Forms-style objects, controls, and components for Python using Tkinter as the underlying engine.

## Table of Contents
- [Architecture](#architecture)
- [Native Bridge](#native-bridge)
- [Control Reference](#control-reference)
- [Navigation Controls](#navigation-controls)
- [System Classes](#system-classes)
- [Constants](#constants)
- [API Reference](#api-reference)
- [Control Examples](#control-examples)
- [Related Modules](#related-modules)

---

## Architecture

WinFormPy is built on four main layers:

```
┌─────────────────────────────────────────────┐
│              Application Layer              │
│         (Forms, UserControls, MDI)          │
├─────────────────────────────────────────────┤
│              Control Layer                  │
│  (Button, Label, TextBox, BreadcrumbBar...) │
├─────────────────────────────────────────────┤
│              Base Layer                     │
│   (ControlBase, ScrollableControlMixin)     │
├─────────────────────────────────────────────┤
│              Native Bridge                  │
│  (Static proxy for all Tkinter operations)  │
├─────────────────────────────────────────────┤
│              Tkinter                        │
└─────────────────────────────────────────────┘
```

1. **Native** — Static proxy class that encapsulates all direct Tkinter/ttk calls. No module outside `winformpy.py` should import `tkinter` directly.
2. **ControlBase** — Base class providing common functionality for all controls.
3. **Specific Controls** — Individual control implementations (Button, Label, etc.).
4. **Container Controls** — Forms, Panels, and UserControls that host other controls.
5. **Mixins** — ScrollableControlMixin for scrolling support.

---

## Native Bridge

The `Native` class is the single point of contact with Tkinter. All higher-level modules (`mauipy`, `mdipy`, `winformpy_extended`) use `Native` instead of importing `tkinter` directly.

```python
from winformpy import Native

# Create low-level widgets through the bridge
frame = Native.Frame(parent, bg="#FFFFFF")
label = Native.Label(parent, text="Hello", font=("Segoe UI", 10))
button = Native.Button(parent, text="Click")
canvas = Native.Canvas(parent, width=200, height=100)

# Utility methods
Native.Wait(widget, 1000, callback)   # Safe after()
Native.Update(widget)                  # Safe update_idletasks()
```

### Available Widgets and Utilities

| Member | Type | Tkinter Equivalent |
| --- | --- | --- |
| `Native.Frame()` | Static method | `tk.Frame` |
| `Native.Toplevel()` | Static method | `tk.Toplevel` |
| `Native.Label()` | Static method | `tk.Label` |
| `Native.Button()` | Static method | `tk.Button` |
| `Native.Entry()` | Static method | `tk.Entry` |
| `Native.Canvas()` | Static method | `tk.Canvas` |
| `Native.Scrollbar()` | Static method | `tk.Scrollbar` |
| `Native.Text()` | Static method | `tk.Text` |
| `Native.Listbox()` | Static method | `tk.Listbox` |
| `Native.Combobox()` | Static method | `ttk.Combobox` |
| `Native.Spinbox()` | Static method | `ttk.Spinbox` |
| `Native.Progressbar()` | Static method | `ttk.Progressbar` |
| `Native.Scale()` | Static method | `ttk.Scale` |
| `Native.PhotoImage()` | Static method | `tk.PhotoImage` |
| `Native.Wait()` | Static method | `widget.after()` |
| `Native.Update()` | Static method | `widget.update_idletasks()` |
| `Native.Window` | Class attr | `tk.Tk` |
| `Native.TclError` | Class attr | `tk.TclError` |
| `Native.StringVar` | Class attr | `tk.StringVar` |
| `Native.IntVar` | Class attr | `tk.IntVar` |
| `Native.BooleanVar` | Class attr | `tk.BooleanVar` |
| `Native.DoubleVar` | Class attr | `tk.DoubleVar` |
| `Native.Style` | Class attr | `ttk.Style` |
| `Native.Menu` | Class attr | `tk.Menu` |

---

## Control Reference

### Basic Controls
| Control | Description |
| --- | --- |
| **Button** | Standard clickable button |
| **Label** | Static text display |
| **LinkLabel** | Clickable hyperlink label |
| **TextBox** | Single/multi-line text input |
| **RichTextBox** | Rich text editor with RTF support |
| **MaskedTextBox** | Input with format mask |
| **CheckBox** | Boolean toggle control |
| **RadioButton** | Mutually exclusive option |
| **ComboBox** | Dropdown selection list |
| **ListBox** | Scrollable item list |
| **CheckedListBox** | List with checkboxes |
| **DomainUpDown** | String spinner control |
| **NumericUpDown** | Numeric spinner control |

### Container Controls
| Control | Description |
| --- | --- |
| **Form** | Main application window |
| **Panel** | Basic container |
| **GroupBox** | Titled border container |
| **TabControl** / **TabPage** | Tabbed container and pages |
| **SplitContainer** | Resizable split panels |
| **FlowLayoutPanel** | Auto-flowing layout |
| **TableLayoutPanel** | Grid-based layout |
| **UserControl** | Custom composite control |

### Navigation Controls
| Control | Description |
| --- | --- |
| **BreadcrumbBar** | Path-based navigation with clickable segments |
| **SettingsCard** | WinUI3-style settings card with icon, header, description, and action content |

### Data and Advanced Controls
| Control | Description |
| --- | --- |
| **DataGridView** | Tabular data display |
| **ListView** | Multi-column list with icons |
| **TreeView** | Hierarchical data display |
| **ProgressBar** | Progress indicator |
| **TrackBar** | Slider control |
| **PictureBox** | Image display |
| **MonthCalendar** | Calendar control |
| **DatePicker** | Date selection |
| **WebBrowser** | Embedded web browser |

### Visual Elements
| Control | Description |
| --- | --- |
| **Line** | Horizontal/vertical separator |
| **ScrollBar** / **HScrollBar** / **VScrollBar** | Scroll controls |
| **StatusBar** | Window status bar |

### Menus and Toolbars
| Control | Description |
| --- | --- |
| **MenuStrip** | Main menu bar |
| **ToolStrip** | Toolbar with buttons |
| **StatusStrip** | Status bar with panels |
| **ContextMenuStrip** | Right-click context menu |
| **ToolStripButton** / **ToolStripLabel** / **ToolStripSeparator** | Toolbar items |
| **ToolStripMenuItem** | Menu item |
| **ToolStripTextBox** / **ToolStripComboBox** | Toolbar input items |
| **ToolStripProgressBar** | Toolbar progress indicator |

### Dialogs
| Control | Description |
| --- | --- |
| **MessageBox** | Standard message dialog |
| **InputBox** | Simple text input dialog |
| **OpenFileDialog** / **SaveFileDialog** | File dialogs |
| **ColorDialog** | Color picker |
| **FontDialog** | Font picker |
| **PrintDialog** | Print configuration |
| **PageSetupDialog** | Page setup |
| **PrintPreviewDialog** | Print preview |

---

## System Classes

| Class | Description |
| --- | --- |
| **SystemColors** | Access to system colors (Control, Window, etc.) |
| **SystemFonts** | Access to system fonts (Default, Caption, etc.) |
| **SystemStyles** | Apply system-consistent styles to control defaults |
| **MessageBox** | Display standard dialog boxes |
| **Application** | Manage application lifecycle (`Run`, `Exit`) |
| **Clipboard** | Access system clipboard |
| **Screen** | Screen dimensions and DPI detection |
| **ErrorProvider** | Validation error indicators |
| **ImageList** | Shared image collection for controls |
| **Timer** | Interval-based event timer |

---

## Constants

### Layout Constants
Exported for use in all modules without importing `tkinter`:

| Constant | Value | Description |
| --- | --- | --- |
| `TOP` | `"top"` | Pack/place to top |
| `BOTTOM` | `"bottom"` | Pack/place to bottom |
| `LEFT` | `"left"` | Pack/place to left |
| `RIGHT` | `"right"` | Pack/place to right |
| `BOTH` | `"both"` | Fill both directions |
| `X` | `"x"` | Fill horizontal |
| `Y` | `"y"` | Fill vertical |
| `CENTER` | `"center"` | Center alignment |
| `END` | `"end"` | End alignment |
| `VERTICAL` | `"vertical"` | Vertical orientation |
| `HORIZONTAL` | `"horizontal"` | Horizontal orientation |

### Font Constants

| Constant | Description |
| --- | --- |
| `DEFAULT_FONT_TEXT` | `"Segoe UI Variable Text"` on Windows, `"Segoe UI"` elsewhere |
| `DEFAULT_FONT_ICONS` | `"Segoe Fluent Icons"` on Windows, `"Segoe MDL2 Assets"` elsewhere |

---

## API Reference

### Common Properties
All controls inherit these standard properties:
- `Name`, `Text`, `Left`, `Top`, `Width`, `Height`, `Enabled`, `Visible`, `BackColor`, `ForeColor`, `Font`, `Dock`, `Anchor`.

### Common Events
| Event | Description |
| --- | --- |
| `Click` | Mouse click |
| `DoubleClick` | Mouse double-click |
| `TextChanged` | Text content changed |
| `MouseMove` | Mouse movement |
| `MouseDown` / `MouseUp` | Mouse button press/release |
| `MouseEnter` / `MouseLeave` | Mouse hover |
| `MouseWheel` | Mouse scroll |
| `KeyDown` / `KeyUp` | Keyboard interaction |

### Enumerations
Key enumerations for control configuration:

| Enum | Values |
| --- | --- |
| `DockStyle` | `None_`, `Top`, `Bottom`, `Left`, `Right`, `Fill` |
| `AnchorStyles` | `Top`, `Bottom`, `Left`, `Right` (combinable with `\|`) |
| `FlatStyle` | `Standard`, `Flat`, `Popup`, `System` |
| `BorderStyle` | `None_`, `FixedSingle`, `Fixed3D` |
| `FormStartPosition` | `Manual`, `CenterScreen`, `WindowsDefaultLocation`, `CenterParent` |
| `FormWindowState` | `Normal`, `Minimized`, `Maximized` |
| `ContentAlignment` | `TopLeft`, `TopCenter`, `TopRight`, `MiddleLeft`, `MiddleCenter`, `MiddleRight`, `BottomLeft`, `BottomCenter`, `BottomRight` |
| `ProgressBarStyle` | `Blocks`, `Continuous`, `Marquee` |

---

## Control Examples

### Form and Button
```python
from winformpy import Form, Button, Application

form = Form({'Text': 'My Form', 'Width': 300, 'Height': 200})
btn = Button(form, {'Text': 'Click Me', 'Left': 100, 'Top': 80})
btn.Click = lambda s, e: print("Hello!")

Application.Run(form)
```

### BreadcrumbBar Navigation
```python
from winformpy import BreadcrumbBar

bc = BreadcrumbBar(container, items_source=["Home", "Documents", "Finance"])
bc.ItemClicked = lambda sender, e: print(f"Navigated to index {e.data}")

# Update path dynamically
bc.ItemsSource = ["Home", "Documents", "Finance", "Reports"]
```

### SettingsCard
```python
from winformpy import SettingsCard

card = SettingsCard(container, header="Dark Mode", description="Enable dark theme", icon="\uE790")
# Access the action frame to add controls (e.g., a Switch)
action_frame = card.Content
card.Header = "Updated Title"
```

### RichTextBox with Formatting
```python
from winformpy import RichTextBox

rtb = RichTextBox(form)
rtb.WriteLine("Success!", color="green")
rtb.SelectionBold = True
rtb.Write("Bold text")
```

### Panel with Dock Layout
```python
from winformpy import Form, Panel, Label, DockStyle, Application

form = Form({'Text': 'Dock Demo', 'Width': 600, 'Height': 400})

header = Panel(form, {'Dock': DockStyle.Top, 'Height': 50, 'BackColor': '#0078D4'})
sidebar = Panel(form, {'Dock': DockStyle.Left, 'Width': 200, 'BackColor': '#F0F0F0'})
content = Panel(form, {'Dock': DockStyle.Fill})

Application.Run(form)
```

---

## Related Modules

| Module | Description | Documentation |
| --- | --- | --- |
| `winformpy_extended` | Advanced controls (ExtendedLabel, ConsoleTextBox, DatePickerBox) | [EXTENDED_README.md](EXTENDED_README.md) |
| `winformpy_tools` | Utilities (FontManager, ColorManager, CSSManager, LayoutManager) | [TOOLS_README.md](TOOLS_README.md) |
| `winui3` | Windows 11 Fluent Design controls | [WINUI3_README.md](WINUI3_README.md) |
| `mauipy` | .NET MAUI Shell and layouts | — |
| `mdipy` | Multiple Document Interface (MDIParent, MDIChild) | — |
| `themes/` | Theme colors and fonts (winforms_theme, winui3_theme) | — |
| `templates/` | Ready-to-use application templates | [templates/README.md](templates/README.md) |
| `ui_elements/` | Pre-built embeddable UI components | [ui_elements/README.md](ui_elements/README.md) |
