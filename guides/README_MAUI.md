# MAUI Style in WinFormPy

This guide explains how to use the `mauipy` module to create cross-platform applications with a MAUI (Multi-platform App UI) style using WinFormPy.

## Core Concepts

### Shell
The `Shell` is the main container for your application. It provides a standard navigation structure with a Flyout menu and a content area.

```python
from winformpy.mauipy import Shell

class MyApp(Shell):
    def __init__(self):
        super().__init__()
        self.Text = "My App"
        
        # Add items to the Flyout Menu
        self.FlyoutMenu.AddItem("Home", lambda: self.GoToAsync(HomePage(self.Detail)))
```

### Pages
- **ContentPage**: A basic page that displays a single view.
- **FlyoutPage**: A page that manages a master/detail view (used internally by Shell).
- **NavigationPage**: A page that manages a stack of pages with a back button.
- **TabbedPage**: A page that displays tabs.

### Layouts
- **VerticalStackLayout**: Arranges children vertically.
- **HorizontalStackLayout**: Arranges children horizontally.
- **Grid**: Arranges children in rows and columns.

### Controls
MAUI-style controls are wrappers around WinFormPy controls with default styling and simplified APIs:
- **Label**
- **Button**
- **Entry** (TextBox)
- **Image** (PictureBox)

## Example

See `examples/maui_example.py` for a complete working example.
