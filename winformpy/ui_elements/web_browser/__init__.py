"""
Web Browser Module.

This module provides a WinForms-style WebBrowser control using tkinterweb.
Based on System.Windows.Forms.WebBrowser from Microsoft .NET.

Architecture:
    ┌─────────────────────────────────────┐
    │  Visual Layer                       │
    │  - WebBrowser (Core Control)        │
    │  - WebBrowserPanel (Panel embed)    │
    │  - WebBrowserUI (Full browser app)  │
    └─────────────────────────────────────┘

The tkinterweb library provides HTML rendering capabilities.
The core implementation is the WebBrowser class in winformpy.winformpy.

Features:
    - Navigate to URLs
    - Load HTML content directly
    - Forward/Back navigation
    - Page title and URL tracking
    - Navigation events
    - Tabbed browsing (WebBrowserUI)
    - Favorites & History
    - WinForms-compatible API

Example:
    >>> from winformpy.ui_elements.web_browser import WebBrowser, WebBrowserPanel, WebBrowserUI
    >>> 
    >>> # Option 1: As standalone control in a Form
    >>> browser = WebBrowser(form, {'Dock': 'Fill'})
    >>> browser.Navigate("https://www.python.org")
    >>> 
    >>> # Option 2: Embeddable Panel with navigation bar
    >>> panel = WebBrowserPanel(form, {'Dock': 'Fill'})
    >>> panel.Navigate("https://www.google.com")
    >>>
    >>> # Option 3: Full-featured browser application
    >>> browser_app = WebBrowserUI()
    >>> Application.Run(browser_app)
"""

# Core WebBrowser from winformpy
from winformpy.winformpy import (
    WebBrowser,
    WebBrowserReadyState,
    WebBrowserNavigatingEventArgs,
    WebBrowserNavigatedEventArgs,
    WebBrowserDocumentCompletedEventArgs,
    WebBrowserProgressChangedEventArgs,
    TKINTERWEB_AVAILABLE
)

# Panel and UI components
from .web_browser_panel import WebBrowserPanel
from .web_browser_ui import WebBrowserUI, BrowserUI

__all__ = [
    # Core control
    'WebBrowser',
    'WebBrowserReadyState',
    'WebBrowserNavigatingEventArgs',
    'WebBrowserNavigatedEventArgs',
    'WebBrowserDocumentCompletedEventArgs',
    'WebBrowserProgressChangedEventArgs',
    'TKINTERWEB_AVAILABLE',
    # Panel
    'WebBrowserPanel',
    # Full browser app
    'WebBrowserUI',
    'BrowserUI'  # Alias
]
