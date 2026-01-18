"""
Example: WebBrowser Control Demo
================================

Demonstrates the WebBrowser control from WinFormPy.
Based on Microsoft System.Windows.Forms.WebBrowser API.

INSTALLATION
------------
    pip install tkinterweb
    
    or:  uv pip install tkinterweb

USAGE
-----
    python examples/ui_elements/web_browser_example.py
    
    or:  uv run python examples/ui_elements/web_browser_example.py

CONTROLS
--------
- WebBrowser: HTML rendering control with navigation capabilities
- Navigation: Back, Forward, Refresh, Home buttons
- Address bar: Enter URL and press Enter or click Go
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from winformpy import Form, Panel, Button, Label, TextBox
from winformpy.ui_elements.web_browser import WebBrowser


def main():
    """Simple WebBrowser demo."""
    
    # Create main form
    form = Form({
        'Text': 'WebBrowser Demo - WinFormPy',
        'Width': 1024,
        'Height': 768,
        'StartPosition': 'CenterScreen'
    })
    
    # ===== Navigation Bar =====
    nav_panel = Panel(form, {
        'Height': 40,
        'Dock': 'Top',
        'BackColor': '#f0f0f0'
    })
    
    # Back button
    btn_back = Button(nav_panel, {
        'Text': '←',
        'Left': 5,
        'Top': 5,
        'Width': 40,
        'Height': 30
    })
    
    # Forward button
    btn_forward = Button(nav_panel, {
        'Text': '→',
        'Left': 50,
        'Top': 5,
        'Width': 40,
        'Height': 30
    })
    
    # Refresh button
    btn_refresh = Button(nav_panel, {
        'Text': '↻',
        'Left': 95,
        'Top': 5,
        'Width': 40,
        'Height': 30
    })
    
    # Home button
    btn_home = Button(nav_panel, {
        'Text': '⌂',
        'Left': 140,
        'Top': 5,
        'Width': 40,
        'Height': 30
    })
    
    # URL TextBox
    txt_url = TextBox(nav_panel, {
        'Left': 190,
        'Top': 8,
        'Width': 600,
        'Height': 25,
        'Text': 'https://www.google.com'
    })
    
    # Go button
    btn_go = Button(nav_panel, {
        'Text': 'Go',
        'Left': 800,
        'Top': 5,
        'Width': 50,
        'Height': 30
    })
    
    # ===== Status Bar =====
    status_panel = Panel(form, {
        'Height': 25,
        'Dock': 'Bottom',
        'BackColor': '#e0e0e0'
    })
    
    lbl_status = Label(status_panel, {
        'Text': 'Ready',
        'Left': 10,
        'Top': 5,
        'Width': 800,
        'Height': 20
    })
    
    # ===== WebBrowser Control =====
    browser = WebBrowser(form, {
        'Dock': 'Fill'
    })
    
    # ===== Event Handlers =====
    def navigate_to_url():
        url = txt_url.Text.strip()
        if url:
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'https://' + url
            txt_url.Text = url
            browser.Navigate(url)
    
    def on_go_click(sender, e):
        navigate_to_url()
    
    def on_url_keypress(sender, e):
        if hasattr(e, 'KeyChar') and e.KeyChar == '\r':
            navigate_to_url()
    
    def on_back_click(sender, e):
        browser.GoBack()
    
    def on_forward_click(sender, e):
        browser.GoForward()
    
    def on_refresh_click(sender, e):
        browser.Refresh()
    
    def on_home_click(sender, e):
        txt_url.Text = 'https://www.google.com'
        browser.Navigate('https://www.google.com')
    
    def on_navigating(sender, e):
        lbl_status.Text = f'Loading: {e.Url}...'
    
    def on_navigated(sender, e):
        txt_url.Text = e.Url
        lbl_status.Text = f'Loaded: {e.Url}'
    
    def on_document_completed(sender, e):
        lbl_status.Text = 'Done'
    
    def on_title_changed(sender, e):
        title = browser.DocumentTitle
        if title:
            form.Text = f'{title} - WebBrowser Demo'
        else:
            form.Text = 'WebBrowser Demo - WinFormPy'
    
    # Wire up events
    btn_go.Click = on_go_click
    btn_back.Click = on_back_click
    btn_forward.Click = on_forward_click
    btn_refresh.Click = on_refresh_click
    btn_home.Click = on_home_click
    txt_url.KeyPress = on_url_keypress
    
    browser.Navigating = on_navigating
    browser.Navigated = on_navigated
    browser.DocumentCompleted = on_document_completed
    browser.DocumentTitleChanged = on_title_changed
    
    # Navigate to Google on startup
    browser.Navigate('https://www.google.com')
    
    # Show form
    form.ShowDialog()


if __name__ == "__main__":
    main()
