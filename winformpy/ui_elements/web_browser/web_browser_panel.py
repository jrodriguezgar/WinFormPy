"""
Module: web_browser_panel.py
Description: Embeddable Panel with WebBrowser control and navigation bar.

Provides a complete WebBrowser panel that can be embedded in any Form or Panel,
with a built-in navigation bar including:
- Back/Forward buttons
- URL address bar
- Go/Refresh buttons
- Loading indicator

Uses the WebBrowser class from winformpy (based on System.Windows.Forms.WebBrowser).
Requires: tkinterweb (pip install tkinterweb)
"""

import sys
import os

# Add project root to path for direct execution
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..', '..', '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy.winformpy import (
    Panel, Button, TextBox, Label, WebBrowser,
    DockStyle, AnchorStyles, FlatStyle, Font, FontStyle,
    TKINTERWEB_AVAILABLE, _ensure_tkinterweb
)


class WebBrowserPanel(Panel):
    """
    Embeddable Panel with WebBrowser control and navigation bar.
    
    Provides a complete browsing experience with:
    - Navigation bar with back/forward buttons
    - URL address bar with Go button
    - Refresh and Stop buttons
    - Status bar with loading indicator
    
    Properties:
        Url (str): Gets or sets the current URL.
        DocumentTitle (str): Gets the title of the current document.
        ShowNavigationBar (bool): Gets or sets navigation bar visibility.
        ShowStatusBar (bool): Gets or sets status bar visibility.
        Browser (WebBrowser): Gets the underlying WebBrowser control.
    
    Methods:
        Navigate(url): Navigates to the specified URL.
        GoBack(): Navigates to the previous page.
        GoForward(): Navigates to the next page.
        Refresh(): Reloads the current page.
        Stop(): Stops the current navigation.
    
    Events:
        Navigating: Occurs before navigation begins.
        Navigated: Occurs after navigation completes.
        DocumentCompleted: Occurs when the document is fully loaded.
        DocumentTitleChanged: Occurs when the document title changes.
    
    Example:
        >>> panel = WebBrowserPanel(form, {'Dock': DockStyle.Fill})
        >>> panel.Navigate("https://www.python.org")
        >>> 
        >>> def on_title_changed(sender, e):
        ...     form.Text = panel.DocumentTitle
        >>> panel.DocumentTitleChanged = on_title_changed
    """
    
    def __init__(self, parent, props=None):
        """
        Initialize the WebBrowserPanel.
        
        Args:
            parent: Parent Form, Panel, or container.
            props: Dictionary of properties to apply.
        """
        # Use lazy loading check
        if not _ensure_tkinterweb():
            raise ImportError(
                "tkinterweb is required for WebBrowserPanel. "
                "Install it with: pip install tkinterweb"
            )
        
        # Extract custom properties before calling super
        self._custom_props = {
            'ShowNavigationBar': True,
            'ShowStatusBar': True,
            'ShowNavigationButtons': True,  # Back/Forward buttons together
            'ShowRefreshButton': True,
            'ShowHomeButton': True,
            'ShowAddressBar': True,  # Address bar and Go button together
            'HomeUrl': 'https://www.google.com',
        }
        
        if props:
            for key in list(props.keys()):
                if key in self._custom_props:
                    self._custom_props[key] = props.pop(key)
        
        # Initialize Panel base class
        super().__init__(parent, props)
        
        # Create UI components using WinFormPy controls
        self._create_navigation_bar()
        self._create_browser()
        self._create_status_bar()
        
        # Wire up events
        self._wire_browser_events()
        
        # Apply initial visibility
        self._apply_visibility()
    
    def _create_navigation_bar(self):
        """Create the navigation bar using WinFormPy controls."""
        self._nav_panel = Panel(self, {
            'Height': 40,
            'Dock': DockStyle.Top,
            'BackColor': '#F0F0F0'
        })
        
        # Back button
        self._btn_back = Button(self._nav_panel, {
            'Text': '◀',
            'Left': 5,
            'Top': 5,
            'Width': 35,
            'Height': 30,
            'FlatStyle': FlatStyle.Flat,
            'Font': Font('Segoe UI', 10),
            'Enabled': False
        })
        self._btn_back.Click = lambda s, e: self._on_back_click()
        
        # Forward button
        self._btn_forward = Button(self._nav_panel, {
            'Text': '▶',
            'Left': 45,
            'Top': 5,
            'Width': 35,
            'Height': 30,
            'FlatStyle': FlatStyle.Flat,
            'Font': Font('Segoe UI', 10),
            'Enabled': False
        })
        self._btn_forward.Click = lambda s, e: self._on_forward_click()
        
        # Refresh button
        self._btn_refresh = Button(self._nav_panel, {
            'Text': '↻',
            'Left': 85,
            'Top': 5,
            'Width': 35,
            'Height': 30,
            'FlatStyle': FlatStyle.Flat,
            'Font': Font('Segoe UI', 12)
        })
        self._btn_refresh.Click = lambda s, e: self._on_refresh_click()
        
        # Home button
        self._btn_home = Button(self._nav_panel, {
            'Text': '🏠',
            'Left': 125,
            'Top': 5,
            'Width': 35,
            'Height': 30,
            'FlatStyle': FlatStyle.Flat,
            'Font': Font('Segoe UI Emoji', 10)
        })
        self._btn_home.Click = lambda s, e: self._on_home_click()
        
        # URL TextBox - anchored to stretch with window
        self._txt_url = TextBox(self._nav_panel, {
            'Left': 170,
            'Top': 7,
            'Width': 500,
            'Height': 26,
            'Anchor': AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right
        })
        self._txt_url.KeyDown = self._on_url_keydown
        
        # Bind Enter key for reliable navigation using WinFormPy method
        self._txt_url.BindKey('Return', lambda s, e: self._on_go_click())
        
        # Go button - anchored to right
        self._btn_go = Button(self._nav_panel, {
            'Text': 'Go',
            'Top': 5,
            'Width': 50,
            'Height': 30,
            'FlatStyle': FlatStyle.Flat,
            'Anchor': AnchorStyles.Top | AnchorStyles.Right
        })
        self._btn_go.Click = lambda s, e: self._on_go_click()
        
        # Position Go button relative to right edge
        self._position_go_button()
    
    def _position_go_button(self):
        """Position the Go button at the right edge."""
        nav_width = self._nav_panel.Width if self._nav_panel.Width > 0 else 800
        self._btn_go.Left = nav_width - 60
        # Also update URL textbox width
        self._txt_url.Width = nav_width - 240
    
    def _create_browser(self):
        """Create the WebBrowser control."""
        self._browser = WebBrowser(self, {'Dock': DockStyle.Fill})
    
    def _create_status_bar(self):
        """Create the status bar using WinFormPy controls."""
        self._status_panel = Panel(self, {
            'Height': 25,
            'Dock': DockStyle.Bottom,
            'BackColor': '#F0F0F0'
        })
        
        # Status label
        self._lbl_status = Label(self._status_panel, {
            'Text': 'Ready',
            'Left': 10,
            'Top': 3,
            'Width': 500,
            'Height': 20,
            'Anchor': AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right
        })
        
        # Progress label (right-aligned)
        self._lbl_progress = Label(self._status_panel, {
            'Text': '',
            'Top': 3,
            'Width': 80,
            'Height': 20,
            'Anchor': AnchorStyles.Top | AnchorStyles.Right
        })
        self._position_progress_label()
    
    def _position_progress_label(self):
        """Position the progress label at the right edge."""
        status_width = self._status_panel.Width if self._status_panel.Width > 0 else 800
        self._lbl_progress.Left = status_width - 90
    
    def _apply_visibility(self):
        """Apply visibility settings for nav bar, status bar, and individual buttons."""
        self._nav_panel.Visible = self._custom_props.get('ShowNavigationBar', True)
        self._status_panel.Visible = self._custom_props.get('ShowStatusBar', True)
        
        # Individual button visibility
        show_nav_buttons = self._custom_props.get('ShowNavigationButtons', True)
        self._btn_back.Visible = show_nav_buttons
        self._btn_forward.Visible = show_nav_buttons
        self._btn_refresh.Visible = self._custom_props.get('ShowRefreshButton', True)
        self._btn_home.Visible = self._custom_props.get('ShowHomeButton', True)
        show_address_bar = self._custom_props.get('ShowAddressBar', True)
        self._txt_url.Visible = show_address_bar
        self._btn_go.Visible = show_address_bar
    
    def _wire_browser_events(self):
        """Connect browser events to UI updates."""
        
        def on_navigating(sender, e):
            self._lbl_status.Text = f"Navigating to {e.Url}..."
            self._lbl_progress.Text = "Loading..."
            self._update_buttons()
        
        def on_navigated(sender, e):
            self._txt_url.Text = e.Url
            self._lbl_status.Text = f"Loaded: {e.Url}"
            self._update_buttons()
        
        def on_document_completed(sender, e):
            self._lbl_progress.Text = ""
            self._lbl_status.Text = "Done"
            self._update_buttons()
        
        def on_title_changed(sender, e):
            title = self._browser.DocumentTitle
            self._lbl_status.Text = title or "Ready"
        
        self._browser.Navigating = on_navigating
        self._browser.Navigated = on_navigated
        self._browser.DocumentCompleted = on_document_completed
        self._browser.DocumentTitleChanged = on_title_changed
    
    def _update_buttons(self):
        """Update button states based on browser state."""
        self._btn_back.Enabled = self._browser.CanGoBack
        self._btn_forward.Enabled = self._browser.CanGoForward
    
    # ========== Event Handlers ==========
    
    def _on_back_click(self):
        """Handle Back button click."""
        self._browser.GoBack()
    
    def _on_forward_click(self):
        """Handle Forward button click."""
        self._browser.GoForward()
    
    def _on_refresh_click(self):
        """Handle Refresh button click."""
        self._browser.Refresh()
    
    def _on_home_click(self):
        """Handle Home button click."""
        home_url = self._custom_props.get('HomeUrl', 'about:blank')
        self._browser.Navigate(home_url)
    
    def _on_go_click(self):
        """Handle Go button click."""
        url = self._txt_url.Text.strip()
        if url:
            # Add protocol if missing
            if not url.startswith(('http://', 'https://', 'file://')):
                url = 'https://' + url
            self._browser.Navigate(url)
    
    def _on_url_keydown(self, sender, e):
        """Handle key press in URL bar."""
        # Check for Enter key
        if hasattr(e, 'KeyCode') and e.KeyCode == 13:  # Enter key
            self._on_go_click()
        elif hasattr(e, 'keysym') and e.keysym == 'Return':
            self._on_go_click()
    
    # ========== Properties ==========
    
    @property
    def Url(self):
        """Gets the current URL."""
        return self._browser.Url
    
    @Url.setter
    def Url(self, value):
        """Sets the current URL and navigates to it."""
        self._browser.Navigate(value)
    
    @property
    def DocumentTitle(self):
        """Gets the title of the current document."""
        return self._browser.DocumentTitle
    
    @property
    def DocumentText(self):
        """Gets the HTML content of the document."""
        return self._browser.DocumentText
    
    @DocumentText.setter
    def DocumentText(self, value):
        """Sets the HTML content of the document."""
        self._browser.DocumentText = value
    
    @property
    def ShowNavigationBar(self):
        """Gets or sets navigation bar visibility."""
        return self._custom_props.get('ShowNavigationBar', True)
    
    @ShowNavigationBar.setter
    def ShowNavigationBar(self, value):
        """Sets navigation bar visibility."""
        self._custom_props['ShowNavigationBar'] = value
        self._nav_panel.Visible = value
    
    @property
    def ShowStatusBar(self):
        """Gets or sets status bar visibility."""
        return self._custom_props.get('ShowStatusBar', True)
    
    @ShowStatusBar.setter
    def ShowStatusBar(self, value):
        """Sets status bar visibility."""
        self._custom_props['ShowStatusBar'] = value
        self._status_panel.Visible = value
    
    @property
    def HomeUrl(self):
        """Gets or sets the home URL."""
        return self._custom_props.get('HomeUrl', 'https://www.google.com')
    
    @HomeUrl.setter
    def HomeUrl(self, value):
        """Sets the home URL."""
        self._custom_props['HomeUrl'] = value
    
    @property
    def ShowNavigationButtons(self):
        """Gets or sets back/forward buttons visibility."""
        return self._custom_props.get('ShowNavigationButtons', True)
    
    @ShowNavigationButtons.setter
    def ShowNavigationButtons(self, value):
        """Sets back/forward buttons visibility."""
        self._custom_props['ShowNavigationButtons'] = value
        self._btn_back.Visible = value
        self._btn_forward.Visible = value
    
    @property
    def ShowRefreshButton(self):
        """Gets or sets refresh button visibility."""
        return self._custom_props.get('ShowRefreshButton', True)
    
    @ShowRefreshButton.setter
    def ShowRefreshButton(self, value):
        """Sets refresh button visibility."""
        self._custom_props['ShowRefreshButton'] = value
        self._btn_refresh.Visible = value
    
    @property
    def ShowHomeButton(self):
        """Gets or sets home button visibility."""
        return self._custom_props.get('ShowHomeButton', True)
    
    @ShowHomeButton.setter
    def ShowHomeButton(self, value):
        """Sets home button visibility."""
        self._custom_props['ShowHomeButton'] = value
        self._btn_home.Visible = value
    
    @property
    def ShowAddressBar(self):
        """Gets or sets address bar (URL textbox and Go button) visibility."""
        return self._custom_props.get('ShowAddressBar', True)
    
    @ShowAddressBar.setter
    def ShowAddressBar(self, value):
        """Sets address bar visibility."""
        self._custom_props['ShowAddressBar'] = value
        self._txt_url.Visible = value
        self._btn_go.Visible = value
    
    @property
    def Browser(self):
        """Gets the underlying WebBrowser control."""
        return self._browser
    
    # ========== Events (delegated to browser) ==========
    
    @property
    def Navigating(self):
        """Event that occurs before navigation begins."""
        return self._browser.Navigating
    
    @Navigating.setter
    def Navigating(self, handler):
        """Sets the Navigating event handler."""
        # Chain with internal handler
        def chained_handler(sender, e):
            # Update UI
            self._lbl_status.Text = f"Navigating to {e.Url}..."
            self._lbl_progress.Text = "Loading..."
            self._update_buttons()
            # Call user handler
            if handler:
                handler(sender, e)
        self._browser._navigating_handler = chained_handler
    
    @property
    def Navigated(self):
        """Event that occurs after navigation completes."""
        return self._browser.Navigated
    
    @Navigated.setter
    def Navigated(self, handler):
        """Sets the Navigated event handler."""
        def chained_handler(sender, e):
            # Update UI
            self._txt_url.Text = e.Url
            self._lbl_status.Text = f"Loaded: {e.Url}"
            self._update_buttons()
            # Call user handler
            if handler:
                handler(sender, e)
        self._browser._navigated_handler = chained_handler
    
    @property
    def DocumentCompleted(self):
        """Event that occurs when the document is fully loaded."""
        return self._browser.DocumentCompleted
    
    @DocumentCompleted.setter
    def DocumentCompleted(self, handler):
        """Sets the DocumentCompleted event handler."""
        def chained_handler(sender, e):
            # Update UI
            self._lbl_progress.Text = ""
            self._lbl_status.Text = "Done"
            self._update_buttons()
            # Call user handler
            if handler:
                handler(sender, e)
        self._browser._document_completed_handler = chained_handler
    
    @property
    def DocumentTitleChanged(self):
        """Event that occurs when the document title changes."""
        return self._browser.DocumentTitleChanged
    
    @DocumentTitleChanged.setter
    def DocumentTitleChanged(self, handler):
        """Sets the DocumentTitleChanged event handler."""
        self._browser.DocumentTitleChanged = handler
    
    # ========== Methods ==========
    
    def Navigate(self, url):
        """
        Navigates to the specified URL.
        
        Args:
            url (str): The URL to navigate to.
        """
        self._browser.Navigate(url)
    
    def GoBack(self):
        """Navigates to the previous page in history."""
        self._browser.GoBack()
    
    def GoForward(self):
        """Navigates to the next page in history."""
        self._browser.GoForward()
    
    def Refresh(self):
        """Reloads the current page."""
        self._browser.Refresh()
    
    def Stop(self):
        """Stops the current navigation."""
        self._browser.Stop()
    
    def GoHome(self):
        """Navigates to the home page."""
        self._on_home_click()
    
    def LoadHtml(self, html, base_url=None):
        """
        Loads HTML content directly.
        
        Args:
            html (str): The HTML content to load.
            base_url (str, optional): Base URL for resolving relative links.
        """
        self._browser.LoadHtml(html, base_url)
    
    def Focus(self):
        """Sets focus to the URL bar."""
        self._txt_url.Focus()
    
    def FocusBrowser(self):
        """Sets focus to the browser control."""
        self._browser.Focus()
    
    def Dispose(self):
        """Releases resources used by the panel."""
        self._browser.Dispose()
        super().Dispose() if hasattr(super(), 'Dispose') else None


# ========== Test/Demo ==========

if __name__ == "__main__":
    from winformpy.winformpy import Form, CheckBox
    
    form = Form({
        'Text': 'WebBrowserPanel Test - Visibility Demo',
        'Width': 1200,
        'Height': 768
    })
    
    # CRITICAL: Apply layout before adding child controls
    form.ApplyLayout()
    
    # Create left panel for visibility controls
    control_panel = Panel(form, {
        'Dock': DockStyle.Left,
        'Width': 200,
        'BackColor': '#E8E8E8'
    })
    
    # Title label
    lbl_title = Label(control_panel, {
        'Text': 'Visibility Controls',
        'Left': 10,
        'Top': 10,
        'Width': 180,
        'Height': 25,
        'Font': Font('Segoe UI', 11, FontStyle.Bold)
    })
    
    # Create browser panel with some visibility options disabled to demo
    # Available properties:
    #   ShowNavigationBar: bool - Show/hide entire navigation bar (default: True)
    #   ShowStatusBar: bool - Show/hide status bar (default: True)
    #   ShowNavigationButtons: bool - Show/hide Back/Forward buttons (default: True)
    #   ShowRefreshButton: bool - Show/hide Refresh button (default: True)
    #   ShowHomeButton: bool - Show/hide Home button (default: True)
    #   ShowAddressBar: bool - Show/hide URL textbox and Go button (default: True)
    #   HomeUrl: str - URL for Home button (default: 'https://www.google.com')
    
    panel = WebBrowserPanel(form, {
        'Dock': DockStyle.Fill,
        'HomeUrl': 'about:blank',
        'ShowNavigationBar': True,
        'ShowStatusBar': True,
        'ShowNavigationButtons': True,
        'ShowRefreshButton': True,
        'ShowHomeButton': True,
        'ShowAddressBar': True,
    })
    
    # Create checkboxes to toggle visibility
    chk_nav_bar = CheckBox(control_panel, {
        'Text': 'Navigation Bar',
        'Left': 10,
        'Top': 50,
        'Width': 180,
        'Checked': True
    })
    
    chk_status_bar = CheckBox(control_panel, {
        'Text': 'Status Bar',
        'Left': 10,
        'Top': 80,
        'Width': 180,
        'Checked': True
    })
    
    chk_nav_buttons = CheckBox(control_panel, {
        'Text': 'Back/Forward Buttons',
        'Left': 10,
        'Top': 110,
        'Width': 180,
        'Checked': True
    })
    
    chk_refresh = CheckBox(control_panel, {
        'Text': 'Refresh Button',
        'Left': 10,
        'Top': 140,
        'Width': 180,
        'Checked': True
    })
    
    chk_home = CheckBox(control_panel, {
        'Text': 'Home Button',
        'Left': 10,
        'Top': 170,
        'Width': 180,
        'Checked': True
    })
    
    chk_address = CheckBox(control_panel, {
        'Text': 'Address Bar + Go',
        'Left': 10,
        'Top': 200,
        'Width': 180,
        'Checked': True
    })
    
    # Wire up checkbox events
    def on_nav_bar_changed(sender, e):
        panel.ShowNavigationBar = chk_nav_bar.Checked
    chk_nav_bar.CheckedChanged = on_nav_bar_changed
    
    def on_status_bar_changed(sender, e):
        panel.ShowStatusBar = chk_status_bar.Checked
    chk_status_bar.CheckedChanged = on_status_bar_changed
    
    def on_nav_buttons_changed(sender, e):
        panel.ShowNavigationButtons = chk_nav_buttons.Checked
    chk_nav_buttons.CheckedChanged = on_nav_buttons_changed
    
    def on_refresh_changed(sender, e):
        panel.ShowRefreshButton = chk_refresh.Checked
    chk_refresh.CheckedChanged = on_refresh_changed
    
    def on_home_changed(sender, e):
        panel.ShowHomeButton = chk_home.Checked
    chk_home.CheckedChanged = on_home_changed
    
    def on_address_changed(sender, e):
        panel.ShowAddressBar = chk_address.Checked
    chk_address.CheckedChanged = on_address_changed
    
    def on_title_changed(sender, e):
        title = panel.DocumentTitle
        if title:
            form.Text = f"{title} - Visibility Demo"
    
    panel.DocumentTitleChanged = on_title_changed
    
    # Start with blank page (default)
    # The browser will show about:blank initially
    
    form.ShowDialog()
