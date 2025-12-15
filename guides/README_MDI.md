# MDI (Multiple Document Interface) in WinFormPy

This guide explains how to use the `mdipy` module to create Multiple Document Interface (MDI) applications in WinFormPy.

## Overview

MDI applications allow you to display multiple documents (child forms) within a single main window (parent form). This is common in applications like text editors, image processors, and IDEs.

## Core Classes

### MDIParent
The `MDIParent` class represents the main container window. It manages the child windows and the main menu.

```python
from winformpy.mdipy import MDIParent

class MyApp(MDIParent):
    def __init__(self):
        super().__init__()
        self.Text = "MDI Application"
        self.IsMdiContainer = True
```

### MDIChild
The `MDIChild` class represents a document window inside the parent.

```python
from winformpy.mdipy import MDIChild

def create_child(parent):
    child = MDIChild(mdi_parent=parent)
    child.Text = "Document 1"
    child.Show()
```

## Features

### Menu Merging
When an MDI child is maximized or activated, its menu can be merged with the parent's menu. The `MDIParent` handles this automatically if the child has a `Menu` property set.

### Window List
You can designate a menu item to automatically list all open child windows, allowing users to switch between them easily.

```python
# In MDIParent setup
self.MdiWindowListItem = windowMenu # A ToolStripMenuItem
```

### Layouts
The `MDIParent` provides methods to arrange child windows:
- `LayoutMdi(0)`: Cascade
- `LayoutMdi(1)`: Tile Horizontal
- `LayoutMdi(2)`: Tile Vertical

## Example

Here is a basic example of an MDI application:

```python
from winformpy.winformpy import Application, MenuStrip, ToolStripMenuItem
from winformpy.mdipy import MDIParent, MDIChild

class MdiApp(MDIParent):
    def __init__(self):
        super().__init__()
        self.Text = "MDI Example"
        self.Size = (800, 600)
        
        # Create Menu
        self.MainMenuStrip = MenuStrip(self)
        
        # File Menu
        fileMenu = ToolStripMenuItem("File")
        newChild = ToolStripMenuItem("New Window")
        newChild.Click = self.new_child_click
        fileMenu.DropDownItems.Add(newChild)
        
        # Window Menu
        windowMenu = ToolStripMenuItem("Window")
        cascade = ToolStripMenuItem("Cascade")
        cascade.Click = lambda s, e: self.LayoutMdi(0)
        windowMenu.DropDownItems.Add(cascade)
        
        self.MainMenuStrip.Items.Add(fileMenu)
        self.MainMenuStrip.Items.Add(windowMenu)
        
        self.Menu = self.MainMenuStrip
        self.MdiWindowListItem = windowMenu

    def new_child_click(self, sender, e):
        child = MDIChild(mdi_parent=self)
        child.Text = "Child Window"
        child.Show()

if __name__ == "__main__":
    app = MdiApp()
    Application.Run(app)
```

See `examples/mdi_example.py` for a more comprehensive example.
