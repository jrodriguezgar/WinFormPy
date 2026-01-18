"""
Navigation Pane Template
========================

A template demonstrating a collapsible "Hamburger Menu" style navigation pane.
Commonly used in modern Windows applications and mobile-style layouts.

USAGE
-----
    uv run python templates/navigation_pane_template.py

FEATURES
--------
- Collapsible Sidebar (Expanded/Compact modes)
- Hamburger toggle button
- Adaptive layout
- Page navigation simulation
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from winformpy import (
    Form, Panel, Button, Label, 
    AnchorStyles, DockStyle, Font
)

class NavItem(Button):
    """A styled button for the navigation pane."""
    def __init__(self, parent, text, icon, y_pos, click_handler):
        super().__init__(parent, {
            'Text': f"  {icon}    {text}",
            'Left': 0,
            'Top': y_pos,
            'Width': 250, # Initial expanded width
            'Height': 45,
            'FlatStyle': 'Flat',
            'TextAlign': 'MiddleLeft',
            'Font': Font('Segoe UI', 11),
            'BackColor': '#f3f3f3',
            'ForeColor': '#000000',
            'Anchor': AnchorStyles.Top | AnchorStyles.Left
        })
        self._full_text = f"  {icon}    {text}"
        self._icon_text = f"{icon}"
        self.Click = click_handler
        # Use WinFormPy method to remove borders
        self.RemoveBorders()

    def set_mode(self, expanded):
        """Switch between icon-only and full text."""
        if expanded:
            self.Text = self._full_text
            self.TextAlign = 'MiddleLeft'
        else:
            self.Text = self._icon_text
            self.TextAlign = 'MiddleCenter'

class NavigationPaneApp:
    def __init__(self):
        self.is_expanded = True
        self.expanded_width = 250
        self.collapsed_width = 50
        self.current_page = None
        
        # Colors
        self.col_sidebar = '#f3f3f3'
        self.col_content = '#ffffff'
        self.col_accent = '#0067c0'
        
        # Main Form
        self.form = Form({
            'Text': 'Navigation Pane Template',
            'Width': 1000,
            'Height': 700,
            'StartPosition': 'CenterScreen',
            'BackColor': self.col_content
        })
        
        # CRITICAL: Apply layout before adding child controls
        self.form.ApplyLayout()
        
        # --- Top Header ---
        self.header = Panel(self.form, {
            'Height': 48,
            'Dock': 'Top',
            'BackColor': self.col_content,
            'Width': 1000
        })
        
        # Toggle Button (Hamburger)
        self.btn_toggle = Button(self.header, {
            'Text': '☰',
            'Left': 0,
            'Top': 0,
            'Width': 48, 
            'Height': 48,
            'FlatStyle': 'Flat',
            'Font': Font('Segoe UI', 14),
            'BackColor': self.col_content
        })
        # Use WinFormPy method to remove borders
        self.btn_toggle.RemoveBorders()
        self.btn_toggle.Click = lambda s, e: self.toggle_sidebar()

        # App Title
        self.lbl_title = Label(self.header, {
            'Text': 'My Application',
            'Left': 60,
            'Top': 12,
            'AutoSize': True,
            'Font': Font('Segoe UI', 12, 'bold')
        })
        
        # --- Sidebar ---
        self.sidebar = Panel(self.form, {
            'Width': self.expanded_width,
            'Dock': 'Left',
            'BackColor': self.col_sidebar
        })
        
        # Sidebar Items
        self.nav_items = []
        items_data = [
            ("Home", "🏠", self._show_home),
            ("Profile", "👤", self._show_profile),
            ("Calendar", "📅", self._show_calendar),
            ("Settings", "⚙", self._show_settings),
        ]
        
        for i, (text, icon, handler) in enumerate(items_data):
            # Create button
            btn = NavItem(self.sidebar, text, icon, i * 45, handler)
            # Add some hover effect manually if desired, or rely on winformpy defaults
            self.nav_items.append(btn)

        # --- Content Area ---
        self.content_panel = Panel(self.form, {
            'Dock': 'Fill',
            'BackColor': self.col_content
        })
        
        # Title of current page
        self.lbl_page_title = Label(self.content_panel, {
            'Text': 'Home',
            'Left': 40,
            'Top': 40,
            'Font': Font('Segoe UI', 24),
            'AutoSize': True
        })
        
        # Initial State
        self._show_home(None, None)

    def toggle_sidebar(self):
        """Animates/Toggles sidebar width."""
        self.is_expanded = not self.is_expanded
        target_width = self.expanded_width if self.is_expanded else self.collapsed_width
        
        # Update width
        self.sidebar.Width = target_width
        
        # Update items appearance and width
        for btn in self.nav_items:
            btn.set_mode(self.is_expanded)
            btn.Width = target_width
            
    def _update_page(self, title, color):
        self.lbl_page_title.Text = title
        self.lbl_page_title.ForeColor = color

    def _show_home(self, s, e):
        self._update_page("Home Dashboard", "#000000")
        
    def _show_profile(self, s, e):
        self._update_page("User Profile", "#0078d7")
        
    def _show_calendar(self, s, e):
        self._update_page("Calendar Events", "#107c10")
        
    def _show_settings(self, s, e):
        self._update_page("Application Settings", "#777777")
        
    def run(self):
        self.form.ShowDialog()

if __name__ == "__main__":
    app = NavigationPaneApp()
    app.run()
