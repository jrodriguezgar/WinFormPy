"""
MAUI Example Application
========================
This example demonstrates how to build a modern application using
MAUI-style components with WinFormPy.

Features demonstrated:
- Shell with flyout navigation menu
- Multiple pages with navigation
- Layouts (VerticalStackLayout, HorizontalStackLayout)
- MAUI-style controls (Label, Button, Entry)
- Toast notifications
- Search bar
- Carousel view
- Chip tags
- Stepper control
"""

import sys
import os
# Add project root directory to path to import winformpy
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from winformpy.mauipy import (
    Shell, ContentPage, VerticalStackLayout, HorizontalStackLayout, Label, Button, Entry, ToastNotification, SearchBar, CarouselView, ChipTag, Stepper
)


# =============================================================================
# PAGE DEFINITIONS
# =============================================================================

class HomePage(ContentPage):
    """Main home page with welcome message and features."""

    def __init__(self, master):
        super().__init__(master)
        self.Title = "Home"

        # Main vertical layout
        layout = VerticalStackLayout(self, props={'Spacing': 15, 'Padding': (40, 40, 40, 40)})

        # Welcome title
        layout.AddChild(Label, text="Welcome to MAUI in Python!",
                       font=("Segoe UI", 28, "bold"), fg="#512BD4")

        # Description
        layout.AddChild(Label,
                       text="This example demonstrates how to build modern, cross-platform-style applications using the MAUI design pattern with WinFormPy.",
                       font=("Segoe UI", 12), fg="#666666", wraplength=600)

        # Feature list
        layout.AddChild(Label, text="✨ Features", font=("Segoe UI", 16, "bold"), fg="#333333")

        features = [
            "• Shell with flyout navigation menu",
            "• Multiple pages with easy navigation",
            "• Modern MAUI-style controls",
            "• Responsive layouts (Vertical, Horizontal, Grid)",
            "• Toast notifications",
            "• Search functionality",
            "• Carousel views",
            "• And much more!"
        ]

        for feature in features:
            layout.AddChild(Label, text=feature, font=("Segoe UI", 11), fg="#555555")

        # Call to action button
        btn = layout.AddChild(Button, text="Get Started →", width=200)
        btn.Click = lambda sender, e: ToastNotification.Show(self._master, "Let's explore the app!", 2000)


class ProfilePage(ContentPage):
    """User profile page with form inputs."""

    def __init__(self, master):
        super().__init__(master)
        self.Title = "Profile"
        self.BackColor = "#F5F5F5"

        layout = VerticalStackLayout(self, props={'Spacing': 12, 'Padding': (40, 30, 40, 30)})

        # Header
        layout.AddChild(Label, text="👤 User Profile", font=("Segoe UI", 22, "bold"), fg="#333333")
        layout.AddChild(Label, text="Manage your personal information", font=("Segoe UI", 11), fg="#666666")

        # Form fields
        layout.AddChild(Label, text="Full Name", font=("Segoe UI", 10, "bold"), fg="#444444")
        self.name_entry = layout.AddChild(Entry, placeholder="Enter your full name")

        layout.AddChild(Label, text="Email Address", font=("Segoe UI", 10, "bold"), fg="#444444")
        self.email_entry = layout.AddChild(Entry, placeholder="Enter your email")

        layout.AddChild(Label, text="Phone Number", font=("Segoe UI", 10, "bold"), fg="#444444")
        self.phone_entry = layout.AddChild(Entry, placeholder="Enter your phone number")

        layout.AddChild(Label, text="Location", font=("Segoe UI", 10, "bold"), fg="#444444")
        self.location_entry = layout.AddChild(Entry, placeholder="City, Country")

        # Save button
        save_btn = layout.AddChild(Button, text="Save Profile", width=150)
        save_btn.Click = self._save_profile

    def _save_profile(self, sender, e):
        """Handles save button click."""
        name = self.name_entry.Text
        email = self.email_entry.Text

        if name and email:
            ToastNotification.Show(self._master, f"Profile saved for {name}!", 2500)
        else:
            ToastNotification.Show(self._master, "Please fill in required fields", 2000)


class ComponentsPage(ContentPage):
    """Page showcasing various MAUI components."""

    def __init__(self, master):
        super().__init__(master)
        self.Title = "Components"

        layout = VerticalStackLayout(self, props={'Spacing': 20, 'Padding': (40, 30, 40, 30)})

        # Header
        layout.AddChild(Label, text="🎨 Component Showcase", font=("Segoe UI", 22, "bold"), fg="#333333")

        # Search Bar Section
        layout.AddChild(Label, text="Search Bar", font=("Segoe UI", 14, "bold"), fg="#512BD4")
        search = layout.AddChild(SearchBar, placeholder="Type to search...")
        search.Search = lambda sender, e: ToastNotification.Show(self._master, f"Searching: {e.Data}", 1500)

        # Carousel Section
        layout.AddChild(Label, text="Carousel View", font=("Segoe UI", 14, "bold"), fg="#512BD4")
        carousel = layout.AddChild(CarouselView)
        carousel.SetItems([
            "🌟 Slide 1: Welcome to MAUI",
            "🚀 Slide 2: Fast Development",
            "💡 Slide 3: Modern Design",
            "🎯 Slide 4: Easy to Use",
            "✨ Slide 5: Beautiful UI"
        ])

        # Chip Tags Section
        layout.AddChild(Label, text="Chip Tags", font=("Segoe UI", 14, "bold"), fg="#512BD4")

        chips_layout = layout.AddChild(HorizontalStackLayout, props={'Spacing': 5, 'Padding': (0, 5, 0, 5)})
        chips_layout.AddChild(ChipTag, text="Python", closable=True)
        chips_layout.AddChild(ChipTag, text="MAUI", closable=True)
        chips_layout.AddChild(ChipTag, text="Tkinter", closable=True)
        chips_layout.AddChild(ChipTag, text="WinFormPy", closable=False)

        # Stepper Section
        layout.AddChild(Label, text="Stepper Control", font=("Segoe UI", 14, "bold"), fg="#512BD4")
        stepper = layout.AddChild(Stepper, min_val=0, max_val=10, step=1, value=5)
        stepper.ValueChanged = lambda sender, e: ToastNotification.Show(self._master, f"Value: {e.Data}", 800)


class SettingsPage(ContentPage):
    """Application settings page."""

    def __init__(self, master):
        super().__init__(master)
        self.Title = "Settings"
        self.BackColor = "#FAFAFA"

        layout = VerticalStackLayout(self, props={'Spacing': 15, 'Padding': (40, 30, 40, 30)})

        # Header
        layout.AddChild(Label, text="⚙️ Settings", font=("Segoe UI", 22, "bold"), fg="#333333")

        # Theme section
        layout.AddChild(Label, text="Appearance", font=("Segoe UI", 14, "bold"), fg="#512BD4")
        layout.AddChild(Label, text="Configure the look and feel of your application",
                       font=("Segoe UI", 11), fg="#666666")

        theme_layout = layout.AddChild(HorizontalStackLayout, props={'Spacing': 10})

        light_btn = theme_layout.AddChild(Button, text="☀️ Light", bg="#E0E0E0", fg="#333333",
                                         hover_bg="#D0D0D0")
        light_btn.Click = lambda sender, e: ToastNotification.Show(self._master, "Light theme selected", 1500)

        dark_btn = theme_layout.AddChild(Button, text="🌙 Dark", bg="#333333", fg="white",
                                        hover_bg="#444444")
        dark_btn.Click = lambda sender, e: ToastNotification.Show(self._master, "Dark theme selected", 1500)

        # Notifications section
        layout.AddChild(Label, text="Notifications", font=("Segoe UI", 14, "bold"), fg="#512BD4")
        layout.AddChild(Label, text="Manage your notification preferences",
                       font=("Segoe UI", 11), fg="#666666")

        notif_btn = layout.AddChild(Button, text="🔔 Test Notification", width=180)
        notif_btn.Click = lambda sender, e: ToastNotification.Show(self._master, "This is a test notification!", 3000)

        # About section
        layout.AddChild(Label, text="About", font=("Segoe UI", 14, "bold"), fg="#512BD4")
        layout.AddChild(Label, text="MAUI Example Application", font=("Segoe UI", 11), fg="#666666")
        layout.AddChild(Label, text="Built with WinFormPy - mauipy module", font=("Segoe UI", 10), fg="#999999")
        layout.AddChild(Label, text="© 2025 DatamanEdge", font=("Segoe UI", 10), fg="#999999")


class HelpPage(ContentPage):
    """Help and documentation page."""

    def __init__(self, master):
        super().__init__(master)
        self.Title = "Help"

        layout = VerticalStackLayout(self, props={'Spacing': 15, 'Padding': (40, 30, 40, 30)})

        # Header
        layout.AddChild(Label, text="❓ Help & Documentation", font=("Segoe UI", 22, "bold"), fg="#333333")

        # Quick start
        layout.AddChild(Label, text="Quick Start Guide", font=("Segoe UI", 14, "bold"), fg="#512BD4")

        guide_text = """
1. Use the hamburger menu (☰) to navigate between pages
2. Each page demonstrates different MAUI components
3. Click buttons to see interactive responses
4. Try the search bar and carousel on the Components page
5. Customize settings on the Settings page
        """
        layout.AddChild(Label, text=guide_text.strip(), font=("Segoe UI", 11), fg="#555555")

        # Key concepts
        layout.AddChild(Label, text="Key Concepts", font=("Segoe UI", 14, "bold"), fg="#512BD4")

        concepts = [
            ("Shell", "The main application container with flyout navigation"),
            ("ContentPage", "A page that displays scrollable content"),
            ("VerticalStackLayout", "Stacks controls vertically with spacing"),
            ("HorizontalStackLayout", "Stacks controls horizontally"),
            ("ToastNotification", "Brief popup messages for feedback"),
        ]

        for name, desc in concepts:
            layout.AddChild(Label, text=f"• {name}: {desc}", font=("Segoe UI", 11), fg="#555555")


# =============================================================================
# MAIN APPLICATION
# =============================================================================

class MyApp(Shell):
    """Main application class using MAUI Shell pattern."""

    def __init__(self):
        super().__init__()
        self.Text = "MAUI Example Application"
        self.HeaderColor = "#512BD4"

        # Setup flyout menu items
        self.AddMenuItem("Home", lambda: self.NavigateTo(HomePage), icon="🏠")
        self.AddMenuItem("Profile", lambda: self.NavigateTo(ProfilePage), icon="👤")
        self.AddMenuItem("Components", lambda: self.NavigateTo(ComponentsPage), icon="🎨")
        self.AddMenuSeparator()
        self.AddMenuItem("Settings", lambda: self.NavigateTo(SettingsPage), icon="⚙️")
        self.AddMenuItem("Help", lambda: self.NavigateTo(HelpPage), icon="❓")

        # Navigate to initial page
        self.NavigateTo(HomePage)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    app = MyApp()
    app.Run()
