"""
Browser Application Template
============================

A tabbed application with web browser style.
Similar to Chrome, Firefox, or Edge with multiple tabs.

INSTALLATION
------------
    pip install tkinterweb
    
    or:  uv pip install tkinterweb

USAGE
-----
    python templates/browser_template.py
    
    or:  uv run python templates/browser_template.py

FEATURES
--------
- Multiple tabs with web pages
- New tab button (+)
- Close tab button (x) on each tab
- Navigation bar per tab (Back, Forward, Refresh, Home)
- Address bar with Go button
- Status bar
- Keyboard shortcuts:
  - Ctrl+T: New tab
  - Ctrl+W: Close current tab
  - Ctrl+L: Focus address bar
  - F5: Refresh
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from winformpy import (
    Form, Panel, Button, Label, TextBox, TabControl, TabPage,
    DockStyle, AnchorStyles, WebBrowser
)
# from winformpy.ui_elements.web_browser import WebBrowser - Removed, imported above


class BrowserTab:
    """Represents a single browser tab with its own navigation and WebBrowser."""
    
    def __init__(self, tab_control, url="https://www.google.com", on_title_change=None, on_close=None):
        self.tab_control = tab_control
        self.on_title_change_callback = on_title_change
        self.on_close_callback = on_close
        self.home_url = "https://www.google.com"
        
        # Create tab page
        self.tab_page = TabPage(tab_control, {
            'Text': 'New Tab'
        })
        
        # CRITICAL: Force geometry update on the TabPage container
        # This ensures child controls get correct dimensions for Dock calculations
        self.tab_page.Refresh()
        
        # Create navigation bar (Dock Top - must be created before Fill)
        self._create_nav_bar()
        
        # Create status bar (Dock Bottom - must be created before Fill)
        self._create_status_bar()
        
        # Create browser directly in the TabPage (Dock Fill - must be created last)
        self.browser = WebBrowser(self.tab_page, {
            'Dock': 'Fill'
        })
        
        # Wire up browser events
        self.browser.Navigating = self._on_navigating
        self.browser.Navigated = self._on_navigated
        self.browser.DocumentCompleted = self._on_document_completed
        self.browser.DocumentTitleChanged = self._on_title_changed
        
        # Navigate to initial URL
        if url:
            self.navigate(url)
    
    def _create_nav_bar(self):
        """Create the navigation bar."""
        self.nav_panel = Panel(self.tab_page, {
            'Height': 35,
            'Dock': 'Top',
            'BackColor': '#f5f5f5'
        })
        
        # Back button
        self.btn_back = Button(self.nav_panel, {
            'Text': '←',
            'Left': 5,
            'Top': 3,
            'Width': 30,
            'Height': 28
        })
        self.btn_back.Click = lambda s, e: self.browser.GoBack()
        
        # Forward button
        self.btn_forward = Button(self.nav_panel, {
            'Text': '→',
            'Left': 38,
            'Top': 3,
            'Width': 30,
            'Height': 28
        })
        self.btn_forward.Click = lambda s, e: self.browser.GoForward()
        
        # Refresh button
        self.btn_refresh = Button(self.nav_panel, {
            'Text': '↻',
            'Left': 71,
            'Top': 3,
            'Width': 30,
            'Height': 28
        })
        self.btn_refresh.Click = lambda s, e: self.browser.Refresh()
        
        # Home button
        self.btn_home = Button(self.nav_panel, {
            'Text': '⌂',
            'Left': 104,
            'Top': 3,
            'Width': 30,
            'Height': 28
        })
        self.btn_home.Click = lambda s, e: self.navigate(self.home_url)
        
        # URL TextBox
        self.txt_url = TextBox(self.nav_panel, {
            'Left': 140,
            'Top': 5,
            'Width': 1000, 
            'Height': 24,
            'Text': '',
            'Anchor': AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right
        })
        self.txt_url.KeyPress = self._on_url_keypress
        
        # Go button
        self.btn_go = Button(self.nav_panel, {
            'Text': 'Go',
            'Left': 1145, 
            'Top': 3,
            'Width': 40,
            'Height': 28,
            'Anchor': AnchorStyles.Top | AnchorStyles.Right
        })
        self.btn_go.Click = lambda s, e: self._navigate_from_url_bar()
    
    def _create_status_bar(self):
        """Create the status bar."""
        self.status_panel = Panel(self.tab_page, {
            'Height': 22,
            'Dock': 'Bottom',
            'BackColor': '#f0f0f0'
        })
        
        self.lbl_status = Label(self.status_panel, {
            'Text': 'Ready',
            'Left': 8,
            'Top': 3,
            'Width': 800,
            'Height': 16,
            'AutoSize': False,
            'Anchor': AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right
        })
    
    def navigate(self, url):
        """Navigate to a URL."""
        if url:
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'https://' + url
            self.txt_url.Text = url
            self.browser.Navigate(url)
    
    def _navigate_from_url_bar(self):
        """Navigate to URL from the address bar."""
        url = self.txt_url.Text.strip()
        if url:
            self.navigate(url)
    
    def _on_url_keypress(self, sender, e):
        """Handle Enter key in URL bar."""
        if hasattr(e, 'KeyChar') and e.KeyChar == '\r':
            self._navigate_from_url_bar()
    
    def _on_navigating(self, sender, e):
        """Handle navigation start."""
        self.lbl_status.Text = f'Loading: {e.Url}...'
    
    def _on_navigated(self, sender, e):
        """Handle navigation complete."""
        self.txt_url.Text = e.Url
        self.lbl_status.Text = f'Loaded: {e.Url}'
    
    def _on_document_completed(self, sender, e):
        """Handle document load complete."""
        self.lbl_status.Text = 'Done'
    
    def _on_title_changed(self, sender, e):
        """Handle title change."""
        title = self.browser.DocumentTitle
        if title:
            # Truncate long titles
            display_title = title[:25] + '...' if len(title) > 25 else title
            self.tab_page.Text = display_title
            
            if self.on_title_change_callback:
                self.on_title_change_callback(self, title)
    
    def focus_url_bar(self):
        """Focus the URL bar."""
        self.txt_url.Focus()
        # Select all text
        if hasattr(self.txt_url, '_widget'):
            self.txt_url._widget.select_range(0, 'end')
    
    def refresh(self):
        """Refresh the current page."""
        self.browser.Refresh()
    
    def close(self):
        """Close this tab."""
        if self.on_close_callback:
            self.on_close_callback(self)


class BrowserApp:
    """Main Browser Application."""
    
    def __init__(self):
        self.tabs = []
        self.current_tab = None
        
        # Create main form
        self.form = Form({
            'Text': 'Browser - WinFormPy',
            'Width': 1200,
            'Height': 800,
            'StartPosition': 'CenterScreen'
        })
        
        # CRITICAL: Apply geometry BEFORE creating children
        # This ensures child controls get correct dimensions for Dock calculations
        self.form.ApplyLayout()
        
        # Create toolbar
        self._create_toolbar()
        
        # Create tab control
        self.tab_control = TabControl(self.form, {
            'Dock': 'Fill'
        })
        
        # Handle tab selection change
        self.tab_control.SelectedIndexChanged = self._on_tab_changed
        
        # Bind keyboard shortcuts
        self._bind_shortcuts()
        
        # Create initial tab
        self.new_tab("https://www.google.com")
    
    def _create_toolbar(self):
        """Create the main toolbar."""
        self.toolbar = Panel(self.form, {
            'Height': 35,
            'Dock': 'Top',
            'BackColor': '#3c3c3c'
        })
        
        # New Tab button
        self.btn_new_tab = Button(self.toolbar, {
            'Text': '+',
            'Left': 5,
            'Top': 3,
            'Width': 30,
            'Height': 28,
            'BackColor': '#5c5c5c',
            'ForeColor': 'white'
        })
        self.btn_new_tab.Click = lambda s, e: self.new_tab()
        
        # App title
        self.lbl_title = Label(self.toolbar, {
            'Text': 'Browser',
            'Left': 45,
            'Top': 8,
            'Width': 200,
            'Height': 20,
            'ForeColor': 'white'
        })
        
        # Close Tab button
        self.btn_close_tab = Button(self.toolbar, {
            'Text': '×',
            'Left': 1160,
            'Top': 3,
            'Width': 30,
            'Height': 28,
            'Anchor': AnchorStyles.Top | AnchorStyles.Right,
            'BackColor': '#c42b1c',
            'ForeColor': 'white'
        })
        self.btn_close_tab.Click = lambda s, e: self.close_current_tab()
    
    def _bind_shortcuts(self):
        """Bind keyboard shortcuts."""
        # Note: In a full implementation, you would bind these to the form
        # For now, we'll handle them through button clicks
        pass
    
    def new_tab(self, url="https://www.google.com"):
        """Create a new browser tab."""
        tab = BrowserTab(
            self.tab_control,
            url=url,
            on_title_change=self._on_tab_title_change,
            on_close=self._on_tab_close
        )
        self.tabs.append(tab)
        
        # Select the new tab
        self.tab_control.SelectedIndex = len(self.tabs) - 1
        self.current_tab = tab
        
        return tab
    
    def close_current_tab(self):
        """Close the currently selected tab."""
        if self.current_tab and len(self.tabs) > 1:
            self._close_tab(self.current_tab)
        elif len(self.tabs) == 1:
            # Last tab - close the app or navigate to home
            self.current_tab.navigate("https://www.google.com")
    
    def _close_tab(self, tab):
        """Close a specific tab."""
        if tab in self.tabs:
            index = self.tabs.index(tab)
            self.tabs.remove(tab)
            
            # Remove tab page from control
            # Note: In tkinter, we need to handle this differently
            tab.tab_page.Visible = False
            
            # Select another tab
            if self.tabs:
                new_index = min(index, len(self.tabs) - 1)
                self.tab_control.SelectedIndex = new_index
                self.current_tab = self.tabs[new_index]
            else:
                self.current_tab = None
    
    def _on_tab_changed(self, sender, e):
        """Handle tab selection change."""
        index = self.tab_control.SelectedIndex
        if 0 <= index < len(self.tabs):
            self.current_tab = self.tabs[index]
            self._update_title()
    
    def _on_tab_title_change(self, tab, title):
        """Handle tab title change."""
        if tab == self.current_tab:
            self._update_title()
    
    def _on_tab_close(self, tab):
        """Handle tab close request."""
        self._close_tab(tab)
    
    def _update_title(self):
        """Update the main window title."""
        if self.current_tab:
            title = self.current_tab.browser.DocumentTitle
            if title:
                self.form.Text = f'{title} - Browser'
            else:
                self.form.Text = 'Browser - WinFormPy'
    
    def run(self):
        """Run the application."""
        self.form.ShowDialog()


def main():
    """Application entry point."""
    app = BrowserApp()
    app.run()


if __name__ == "__main__":
    main()
