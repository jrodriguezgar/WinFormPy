"""
Navigation Rail Template
========================

A template demonstrating a "Navigation Rail" layout.
This pattern features a permanent, compact vertical bar on the left
for top-level navigation, leaving more room for content.

USAGE
-----
    uv run python templates/navigation_rail_template.py

FEATURES
--------
- Fixed vertical navigation rail
- Icon-based navigation nodes
- Active state indication
- Content switching
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from winformpy import (
    Form, Panel, Button, Label, 
    AnchorStyles, DockStyle, Font, FontStyle
)

class RailButton(Button):
    """A button customized for the rail."""
    def __init__(self, parent, icon, tooltip, y_pos, click_handler):
        super().__init__(parent, {
            'Text': icon,
            'Left': 0,
            'Top': y_pos,
            'Width': 64,
            'Height': 56,
            'FlatStyle': 'Flat',
            'Font': Font('Segoe UI Emoji', 16),
            'BackColor': '#e6e6e6', # Default rail color
            'ForeColor': '#444444'
        })
        self.Click = click_handler
        self.active = False
        self.default_bg = '#e6e6e6'
        self.active_bg = '#ffffff'
        self.hover_bg = '#d0d0d0'
        
        # Use WinFormPy events for hover effect
        self.MouseEnter = lambda s, e: self._on_hover()
        self.MouseLeave = lambda s, e: self._on_leave()

    def _on_hover(self):
        if not self.active:
            self.BackColor = self.hover_bg

    def _on_leave(self):
        if not self.active:
            self.BackColor = self.default_bg

    def set_active(self, is_active):
        self.active = is_active
        if is_active:
            self.BackColor = self.active_bg
            # Add a colored strip indicator logic if desired (e.g. using an image or border)
            self.ForeColor = '#0067c0'
        else:
            self.BackColor = self.default_bg
            self.ForeColor = '#444444'

class NavigationRailApp:
    def __init__(self):
        self.col_rail = '#e6e6e6'
        self.col_content = '#ffffff'
        
        # Main Form
        self.form = Form({
            'Text': 'Navigation Rail Template',
            'Width': 1100,
            'Height': 700,
            'StartPosition': 'CenterScreen',
            'BackColor': self.col_content
        })
        
        # CRITICAL: Apply geometry before adding child controls
        self.form.ApplyLayout()
        
        # --- Rail ---
        self.rail = Panel(self.form, {
            'Width': 64,
            'Dock': 'Left',
            'BackColor': self.col_rail
        })
        
        self.rail_buttons = {}
        self.current_key = None
        
        # Define items
        items = [
            ("dashboard", "📊", "Dashboard"),
            ("projects", "📁", "Projects"),
            ("tasks", "✅", "Tasks"),
            ("team", "👥", "Team"),
            ("analytics", "📈", "Analytics"),
        ]
        
        # Create Buttons (Top aligned)
        for i, (key, icon, tooltip) in enumerate(items):
            btn = RailButton(self.rail, icon, tooltip, i * 60, 
                             lambda s, e, k=key: self.navigate(k))
            self.rail_buttons[key] = btn

        # Settings Button (Bottom aligned)
        self.btn_settings = RailButton(self.rail, "⚙", "Settings", 0, 
                                       lambda s, e: self.navigate("settings"))
        self.btn_settings.Anchor = AnchorStyles.Bottom | AnchorStyles.Left
        self.btn_settings.Top = 700 - 60 # Initial position, Anchor handles resize
        self.rail_buttons["settings"] = self.btn_settings

        # --- Content Area ---
        self.content_panel = Panel(self.form, {
            'Dock': 'Fill',
            'BackColor': self.col_content,
            'Padding': (40, 40, 40, 40)
        })
        
        # Header in content
        self.lbl_header = Label(self.content_panel, {
            'Text': 'Content',
            'Left': 40,
            'Top': 40,
            'AutoSize': True,
            'Font': Font('Segoe UI', 22, FontStyle.Bold)
        })
        
        # Description
        self.lbl_desc = Label(self.content_panel, {
            'Text': 'Description text goes here...',
            'Left': 40,
            'Top': 90,
            'Width': 600,
            'Height': 100,
            'Font': Font('Segoe UI', 11)
        })

        # Initial Navigation
        self.navigate("dashboard")

    def navigate(self, key):
        """Switch content."""
        if self.current_key == key:
            return
            
        # Deactivate old
        if self.current_key in self.rail_buttons:
            self.rail_buttons[self.current_key].set_active(False)
            
        # Activate new
        self.current_key = key
        if key in self.rail_buttons:
            self.rail_buttons[key].set_active(True)
            
        # Update Content
        self._update_content(key)
        
    def _update_content(self, key):
        titles = {
            "dashboard": "Dashboard Overview",
            "projects": "Active Projects",
            "tasks": "My Tasks",
            "team": "Team Directory",
            "analytics": "Performance Analytics",
            "settings": "System Settings"
        }
        
        descs = {
            "dashboard": "Welcome back! Here is a summary of your key metrics/activity.",
            "projects": "List of current ongoing projects and their status.",
            "tasks": "Checklist of pending items assigned to you.",
            "team": "Contact information and hierarchy of team members.",
            "analytics": "Charts and graphs showing performance trends.",
            "settings": "Configure application preferences and user account."
        }
        
        self.lbl_header.Text = titles.get(key, "Unknown")
        self.lbl_desc.Text = descs.get(key, "")

    def run(self):
        self.form.ShowDialog()

if __name__ == "__main__":
    app = NavigationRailApp()
    app.run()
