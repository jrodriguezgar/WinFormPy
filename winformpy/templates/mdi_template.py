import sys
import os
# Add project root directory to path to import winformpy
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from winformpy.winformpy import Application, MenuStrip, ToolStripMenuItem, Form, Label, DockStyle, Size
from winformpy.mdipy import MDIParent, MDIChild

class MdiApp(MDIParent):
    def __init__(self):
        super().__init__()
        self.Text = "MDI Example Application"
        self.Width = 800
        self.Height = 600
        self.IsMdiContainer = True
        
        # Create Menu
        self.MainMenuStrip = MenuStrip(self)
        
        # File Menu
        fileMenu = ToolStripMenuItem("File")
        
        newChild = ToolStripMenuItem("New Child")
        newChild.Click = self.new_child_click
        
        exitItem = ToolStripMenuItem("Exit")
        exitItem.Click = lambda s, e: Application.Exit()
        
        fileMenu.DropDownItems.Add(newChild)
        fileMenu.DropDownItems.Add(ToolStripMenuItem("-"))
        fileMenu.DropDownItems.Add(exitItem)
        
        # Window Menu
        windowMenu = ToolStripMenuItem("Window")
        
        cascade = ToolStripMenuItem("Cascade")
        cascade.Click = lambda s, e: self.LayoutMdi(0)
        
        tileH = ToolStripMenuItem("Tile Horizontal")
        tileH.Click = lambda s, e: self.LayoutMdi(1)
        
        tileV = ToolStripMenuItem("Tile Vertical")
        tileV.Click = lambda s, e: self.LayoutMdi(2)
        
        windowMenu.DropDownItems.Add(cascade)
        windowMenu.DropDownItems.Add(tileH)
        windowMenu.DropDownItems.Add(tileV)
        windowMenu.DropDownItems.Add(ToolStripMenuItem("-"))
        
        self.MainMenuStrip.Items.Add(fileMenu)
        self.MainMenuStrip.Items.Add(windowMenu)
        
        # Assign to Menu property to use native menu bar
        self.Menu = self.MainMenuStrip
        self.MdiWindowListItem = windowMenu
        
        self.child_count = 0

    def new_child_click(self, sender, e):
        self.child_count += 1
        child = MDIChild(mdi_parent=self)
        child.Text = f"Child Document {self.child_count}"
        child.Width = 350
        child.Height = 250
        # Offset each new child
        child.Left = 20 + (self.child_count - 1) * 30
        child.Top = 20 + (self.child_count - 1) * 30
        
        # Add a label to the child's content area
        lbl = Label(child._content_frame)
        lbl.Text = f"This is content for document {self.child_count}"
        lbl.Left = 10
        lbl.Top = 10
        child.AddControl(lbl)
        
        child.Show()

if __name__ == "__main__":
    form = MdiApp()
    Application.Run(form)
