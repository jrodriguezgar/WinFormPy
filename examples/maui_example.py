import sys
import os
# Add parent directory to path to import winformpy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from winformpy.winformpy import Application, MessageBox, DockStyle
from winformpy.mauipy import (
    Shell, ContentPage, VerticalStackLayout, HorizontalStackLayout, 
    Label, Button, Entry, Image, FlyoutMenu
)

class MyApp(Shell):
    def __init__(self):
        super().__init__()
        self.Text = "MAUI Example Application"
        
        # Setup Flyout Menu
        # We add items to the FlyoutMenu which is automatically created by Shell
        self.FlyoutMenu.AddItem("  🏠  Home", lambda: self.GoToAsync(HomePage(self.Detail)))
        self.FlyoutMenu.AddItem("  👤  Profile", lambda: self.GoToAsync(ProfilePage(self.Detail)))
        self.FlyoutMenu.AddItem("  ⚙️  Settings", lambda: self.GoToAsync(SettingsPage(self.Detail)))
        
        # Initial Page
        self.GoToAsync(HomePage(self.Detail))

class HomePage(ContentPage):
    def __init__(self, master):
        super().__init__(master)
        self.Title = "Home"
        self.BackColor = "white"
        
        # Main Layout
        layout = VerticalStackLayout(self)
        layout.Dock = DockStyle.Fill
        layout.Padding = (40, 40, 40, 40)
        
        # Title
        lbl = Label(layout, "Welcome to MAUI in Python!")
        lbl.Font = ("Segoe UI", 24, "bold")
        lbl.ForeColor = "#512BD4" # MAUI Purple
        lbl.Margin = (0, 0, 0, 20)
        
        # Description
        lbl2 = Label(layout, "This example demonstrates how to build cross-platform apps using the MAUI style with WinFormPy.")
        lbl2.Font = ("Segoe UI", 14)
        lbl2.ForeColor = "#333333"
        lbl2.Margin = (0, 0, 0, 30)
        
        # Button
        btn = Button(layout, "Click Me!")
        btn.Width = 200
        btn.Click = lambda s, e: MessageBox.Show("Hello from MAUI!", "MAUI Alert")
        
        # Add controls to layout
        layout.Controls.append(lbl)
        layout.Controls.append(lbl2)
        layout.Controls.append(btn)

class ProfilePage(ContentPage):
    def __init__(self, master):
        super().__init__(master)
        self.Title = "Profile"
        self.BackColor = "#f8f9fa"
        
        layout = VerticalStackLayout(self)
        layout.Dock = DockStyle.Fill
        layout.Padding = (20, 20, 20, 20)
        
        lbl = Label(layout, "User Profile")
        lbl.Font = ("Segoe UI", 20, "bold")
        lbl.Margin = (0, 0, 0, 20)
        
        # Form
        name_lbl = Label(layout, "Name:")
        name_entry = Entry(layout, "Enter your name")
        name_entry.Width = 300
        name_entry.Margin = (0, 0, 0, 10)
        
        email_lbl = Label(layout, "Email:")
        email_entry = Entry(layout, "Enter your email")
        email_entry.Width = 300
        email_entry.Margin = (0, 0, 0, 20)
        
        save_btn = Button(layout, "Save Profile")
        save_btn.Width = 150
        save_btn.Click = lambda s, e: MessageBox.Show(f"Profile Saved:\nName: {name_entry.Text}\nEmail: {email_entry.Text}")
        
        layout.Controls.append(lbl)
        layout.Controls.append(name_lbl)
        layout.Controls.append(name_entry)
        layout.Controls.append(email_lbl)
        layout.Controls.append(email_entry)
        layout.Controls.append(save_btn)

class SettingsPage(ContentPage):
    def __init__(self, master):
        super().__init__(master)
        self.Title = "Settings"
        self.BackColor = "white"
        
        layout = VerticalStackLayout(self)
        layout.Dock = DockStyle.Fill
        layout.Padding = (20, 20, 20, 20)
        
        layout.Controls.append(Label(layout, "Settings"))
        layout.Controls.append(Label(layout, "Version 1.0.0"))

if __name__ == "__main__":
    app = MyApp()
    Application.Run(app)
