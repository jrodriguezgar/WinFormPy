# WinFormPy Core Library

This module provides the core Windows Forms-style objects, controls, and components for Python using Tkinter as the underlying engine.

## Table of Contents
- [Architecture](#architecture)
- [Control Reference](#control-reference)
- [System Classes](#system-classes)
- [API Reference](#api-reference)
- [Control Examples](#control-examples)

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

1. **ControlBase** — Base class providing common functionality for all controls.
2. **Specific Controls** — Individual control implementations (Button, Label, etc.).
3. **Container Controls** — Forms, Panels, and UserControls that host other controls.
4. **Mixins** — ScrollableControlMixin for scrolling support.

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
| **CheckBox** | Boolean toggle control |
| **RadioButton** | Mutually exclusive option |
| **ComboBox** | Dropdown selection list |
| **ListBox** | Scrollable item list |

### Container Controls
| Control | Description |
| --- | --- |
| **Form** | Main application window |
| **Panel** | Basic container |
| **GroupBox** | Titled border container |
| **TabControl** | Tabbed container |
| **SplitContainer** | Resizable split panels |
| **FlowLayoutPanel** | Auto-flowing layout |
| **TableLayoutPanel** | Grid-based layout |

### Data and Advanced Controls
| Control | Description |
| --- | --- |
| **DataGridView** | Tabular data display |
| **ListView** | Multi-column list with icons |
| **TreeView** | Hierarchical data display |
| **ProgressBar** | Progress indicator |
| **TrackBar** | Slider control |
| **NumericUpDown** | Numeric spinner |

---

## System Classes

| Class | Description |
| --- | --- |
| **SystemColors** | Access to system colors (Control, Window, etc.) |
| **SystemFonts** | Access to system fonts (Default, Caption, etc.) |
| **MessageBox** | Display standard dialog boxes |
| **Application** | Manage application lifecycle (`Run`, `Exit`) |
| **Clipboard** | Access system clipboard |

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
| `KeyDown` / `KeyUp` | Keyboard interaction |

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

### RichTextBox with Formatting
```python
from winformpy import RichTextBox

rtb = RichTextBox(form)
rtb.WriteLine("Success!", color="green")
rtb.SelectionBold = True
rtb.Write("Bold text")
```

For more detailed guides, see the `guides/` directory.
