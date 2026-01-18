"""
Module: web_browser_ui.py
Description: Full-featured Web Browser application similar to Windows Explorer.

Provides a complete web browser experience with:
- Tabbed browsing (multiple tabs)
- Menu bar (File, Edit, View, Favorites, Tools, Help)
- Navigation toolbar with Back/Forward/Refresh/Home
- Address bar with autocomplete-style suggestions
- Favorites/Bookmarks sidebar
- History panel
- Downloads panel
- Status bar with progress indicator
- Keyboard shortcuts

Uses WebBrowserPanel for the browser rendering.
Requires: tkinterweb (pip install tkinterweb)
"""

import sys
import os
import json
from datetime import datetime

# Add project root to path for direct execution
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..', '..', '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy.winformpy import (
    Form, Panel, Button, Label, TextBox, ProgressBar,
    MenuStrip, ToolStripMenuItem,
    TabControl, TabPage,
    DockStyle, AnchorStyles, FlatStyle, Font, FontStyle,
    MessageBox, DialogResult,
    Application, InputBox, Clipboard,
    TKINTERWEB_AVAILABLE, _ensure_tkinterweb
)
from winformpy.ui_elements.web_browser.web_browser_panel import WebBrowserPanel

import tkinter as tk


class WebBrowserUI(Form):
    """
    Full-featured Web Browser application similar to Windows Explorer/Internet Explorer.
    
    Features:
    - Tabbed browsing with add/close tab buttons
    - Menu bar with File, Edit, View, Favorites, Tools, Help
    - Navigation toolbar
    - Favorites/Bookmarks management
    - Browsing history
    - Downloads tracking
    - Collapsible sidebar
    - Status bar with page load progress
    - Keyboard shortcuts (Ctrl+T, Ctrl+W, Ctrl+L, F5, etc.)
    
    Properties:
        CurrentTab (WebBrowserPanel): The active browser tab.
        Favorites (list): List of favorite URLs.
        History (list): Browsing history.
        
    Methods:
        NewTab(url): Opens a new tab.
        CloseTab(index): Closes a tab.
        Navigate(url): Navigates the current tab.
        AddFavorite(title, url): Adds a favorite.
        ShowSidebar(panel): Shows sidebar with specified panel.
        HideSidebar(): Hides the sidebar.
    """
    
    # Default settings
    DEFAULT_HOME = "https://www.google.com"
    DEFAULT_SEARCH = "https://www.google.com/search?q="
    
    def __init__(self, props=None):
        """Initialize the WebBrowserUI."""
        if not _ensure_tkinterweb():
            raise ImportError(
                "tkinterweb is required for WebBrowserUI. "
                "Install it with: pip install tkinterweb"
            )
        
        # Default form properties
        default_props = {
            'Text': 'WinFormPy Browser',
            'Width': 1280,
            'Height': 900,
            'StartPosition': 'CenterScreen'
        }
        if props:
            default_props.update(props)
        
        super().__init__(default_props)
        
        # Data storage
        self._favorites = []
        self._history = []
        self._downloads = []
        self._tabs = []
        self._current_tab_index = -1
        self._sidebar_visible = False
        self._sidebar_panel = None
        
        # Load saved data
        self._load_data()
        
        # Apply layout before adding controls
        self.ApplyLayout()
        
        # Build UI
        self._create_menu_bar()
        self._create_navigation_bar()
        self._create_status_bar()
        self._create_main_content()
        
        # Bind keyboard shortcuts
        self._bind_shortcuts()
        
        # Open initial tab
        self.NewTab(self.DEFAULT_HOME)
    
    def _create_menu_bar(self):
        """Create the menu bar."""
        self._menu = MenuStrip(self)
        
        # === File Menu ===
        file_menu = ToolStripMenuItem(self._menu, {'Text': 'File'})
        
        new_tab = ToolStripMenuItem(file_menu, {'Text': 'New Tab\tCtrl+T'})
        new_tab.Click = lambda s, e: self.NewTab()
        
        new_window = ToolStripMenuItem(file_menu, {'Text': 'New Window\tCtrl+N'})
        new_window.Click = lambda s, e: self._new_window()
        
        ToolStripMenuItem(file_menu, {'Text': '-'})
        
        open_file = ToolStripMenuItem(file_menu, {'Text': 'Open File...\tCtrl+O'})
        open_file.Click = lambda s, e: self._open_file()
        
        save_page = ToolStripMenuItem(file_menu, {'Text': 'Save Page As...\tCtrl+S'})
        save_page.Click = lambda s, e: self._save_page()
        
        ToolStripMenuItem(file_menu, {'Text': '-'})
        
        print_page = ToolStripMenuItem(file_menu, {'Text': 'Print...\tCtrl+P'})
        print_page.Click = lambda s, e: self._print_page()
        
        ToolStripMenuItem(file_menu, {'Text': '-'})
        
        close_tab = ToolStripMenuItem(file_menu, {'Text': 'Close Tab\tCtrl+W'})
        close_tab.Click = lambda s, e: self._close_current_tab()
        
        exit_item = ToolStripMenuItem(file_menu, {'Text': 'Exit\tAlt+F4'})
        exit_item.Click = lambda s, e: self.Close()
        
        # === Edit Menu ===
        edit_menu = ToolStripMenuItem(self._menu, {'Text': 'Edit'})
        
        cut = ToolStripMenuItem(edit_menu, {'Text': 'Cut\tCtrl+X'})
        cut.Click = lambda s, e: self._edit_cut()
        
        copy = ToolStripMenuItem(edit_menu, {'Text': 'Copy\tCtrl+C'})
        copy.Click = lambda s, e: self._edit_copy()
        
        paste = ToolStripMenuItem(edit_menu, {'Text': 'Paste\tCtrl+V'})
        paste.Click = lambda s, e: self._edit_paste()
        
        ToolStripMenuItem(edit_menu, {'Text': '-'})
        
        select_all = ToolStripMenuItem(edit_menu, {'Text': 'Select All\tCtrl+A'})
        select_all.Click = lambda s, e: self._select_all()
        
        ToolStripMenuItem(edit_menu, {'Text': '-'})
        
        find = ToolStripMenuItem(edit_menu, {'Text': 'Find on Page...\tCtrl+F'})
        find.Click = lambda s, e: self._find_on_page()
        
        # === View Menu ===
        view_menu = ToolStripMenuItem(self._menu, {'Text': 'View'})
        
        toolbar = ToolStripMenuItem(view_menu, {'Text': 'Toolbar', 'Checked': True})
        toolbar.Click = lambda s, e: self._toggle_toolbar()
        
        statusbar = ToolStripMenuItem(view_menu, {'Text': 'Status Bar', 'Checked': True})
        statusbar.Click = lambda s, e: self._toggle_statusbar()
        
        ToolStripMenuItem(view_menu, {'Text': '-'})
        
        sidebar_fav = ToolStripMenuItem(view_menu, {'Text': 'Favorites Sidebar\tCtrl+I'})
        sidebar_fav.Click = lambda s, e: self._show_favorites_sidebar()
        
        sidebar_hist = ToolStripMenuItem(view_menu, {'Text': 'History Sidebar\tCtrl+H'})
        sidebar_hist.Click = lambda s, e: self._show_history_sidebar()
        
        sidebar_down = ToolStripMenuItem(view_menu, {'Text': 'Downloads\tCtrl+J'})
        sidebar_down.Click = lambda s, e: self._show_downloads_sidebar()
        
        ToolStripMenuItem(view_menu, {'Text': '-'})
        
        refresh = ToolStripMenuItem(view_menu, {'Text': 'Refresh\tF5'})
        refresh.Click = lambda s, e: self._refresh_page()
        
        stop = ToolStripMenuItem(view_menu, {'Text': 'Stop\tEsc'})
        stop.Click = lambda s, e: self._stop_loading()
        
        ToolStripMenuItem(view_menu, {'Text': '-'})
        
        zoom_in = ToolStripMenuItem(view_menu, {'Text': 'Zoom In\tCtrl++'})
        zoom_in.Click = lambda s, e: self._zoom_in()
        
        zoom_out = ToolStripMenuItem(view_menu, {'Text': 'Zoom Out\tCtrl+-'})
        zoom_out.Click = lambda s, e: self._zoom_out()
        
        zoom_reset = ToolStripMenuItem(view_menu, {'Text': 'Reset Zoom\tCtrl+0'})
        zoom_reset.Click = lambda s, e: self._zoom_reset()
        
        ToolStripMenuItem(view_menu, {'Text': '-'})
        
        fullscreen = ToolStripMenuItem(view_menu, {'Text': 'Full Screen\tF11'})
        fullscreen.Click = lambda s, e: self._toggle_fullscreen()
        
        # === Favorites Menu ===
        fav_menu = ToolStripMenuItem(self._menu, {'Text': 'Favorites'})
        
        add_fav = ToolStripMenuItem(fav_menu, {'Text': 'Add to Favorites\tCtrl+D'})
        add_fav.Click = lambda s, e: self._add_current_to_favorites()
        
        manage_fav = ToolStripMenuItem(fav_menu, {'Text': 'Manage Favorites...'})
        manage_fav.Click = lambda s, e: self._manage_favorites()
        
        ToolStripMenuItem(fav_menu, {'Text': '-'})
        
        # Favorites will be added dynamically
        self._favorites_menu = fav_menu
        
        # === Tools Menu ===
        tools_menu = ToolStripMenuItem(self._menu, {'Text': 'Tools'})
        
        clear_history = ToolStripMenuItem(tools_menu, {'Text': 'Clear History...'})
        clear_history.Click = lambda s, e: self._clear_history()
        
        clear_cache = ToolStripMenuItem(tools_menu, {'Text': 'Clear Cache...'})
        clear_cache.Click = lambda s, e: self._clear_cache()
        
        ToolStripMenuItem(tools_menu, {'Text': '-'})
        
        options = ToolStripMenuItem(tools_menu, {'Text': 'Options...'})
        options.Click = lambda s, e: self._show_options()
        
        # === Help Menu ===
        help_menu = ToolStripMenuItem(self._menu, {'Text': 'Help'})
        
        help_item = ToolStripMenuItem(help_menu, {'Text': 'Help Contents\tF1'})
        help_item.Click = lambda s, e: self._show_help()
        
        ToolStripMenuItem(help_menu, {'Text': '-'})
        
        about = ToolStripMenuItem(help_menu, {'Text': 'About WinFormPy Browser'})
        about.Click = lambda s, e: self._show_about()
    
    def _create_navigation_bar(self):
        """Create the main navigation bar."""
        self._nav_bar = Panel(self, {
            'Height': 40,
            'Dock': DockStyle.Top,
            'BackColor': '#F5F5F5'
        })
        
        # Back button
        self._btn_back = Button(self._nav_bar, {
            'Text': '←',
            'Left': 5,
            'Top': 5,
            'Width': 32,
            'Height': 30,
            'FlatStyle': FlatStyle.Flat,
            'Font': Font('Segoe UI', 14)
        })
        self._btn_back.Click = lambda s, e: self._go_back()
        
        # Forward button
        self._btn_forward = Button(self._nav_bar, {
            'Text': '→',
            'Left': 40,
            'Top': 5,
            'Width': 32,
            'Height': 30,
            'FlatStyle': FlatStyle.Flat,
            'Font': Font('Segoe UI', 14)
        })
        self._btn_forward.Click = lambda s, e: self._go_forward()
        
        # Refresh button
        self._btn_refresh = Button(self._nav_bar, {
            'Text': '⟳',
            'Left': 75,
            'Top': 5,
            'Width': 32,
            'Height': 30,
            'FlatStyle': FlatStyle.Flat,
            'Font': Font('Segoe UI', 14)
        })
        self._btn_refresh.Click = lambda s, e: self._refresh_page()
        
        # Home button
        self._btn_home = Button(self._nav_bar, {
            'Text': '⌂',
            'Left': 110,
            'Top': 5,
            'Width': 32,
            'Height': 30,
            'FlatStyle': FlatStyle.Flat,
            'Font': Font('Segoe UI', 14)
        })
        self._btn_home.Click = lambda s, e: self._go_home()
        
        # URL TextBox
        self._txt_url = TextBox(self._nav_bar, {
            'Left': 150,
            'Top': 8,
            'Width': 900,
            'Height': 24,
            'Font': Font('Segoe UI', 10)
        })
        
        # Bind Enter key for navigation using WinFormPy method
        self._txt_url.BindKey('Return', lambda s, e: self._navigate_from_url_bar())
        
        # Go button
        self._btn_go = Button(self._nav_bar, {
            'Text': 'Go',
            'Top': 5,
            'Width': 50,
            'Height': 30,
            'FlatStyle': FlatStyle.Flat,
            'Font': Font('Segoe UI', 10)
        })
        self._btn_go.Click = lambda s, e: self._navigate_from_url_bar()
        
        # Favorites button (star)
        self._btn_fav = Button(self._nav_bar, {
            'Text': '☆',
            'Top': 5,
            'Width': 32,
            'Height': 30,
            'FlatStyle': FlatStyle.Flat,
            'Font': Font('Segoe UI', 14)
        })
        self._btn_fav.Click = lambda s, e: self._add_current_to_favorites()
        
        # Position URL and buttons on right (will be adjusted on resize)
        self._position_nav_elements()
    
    def _position_nav_elements(self):
        """Position navigation bar elements based on window width."""
        w = self.Width
        # URL bar stretches to fill
        url_width = w - 280  # Leave space for buttons
        if url_width < 200:
            url_width = 200
        self._txt_url.Width = url_width
        # Go button after URL
        self._btn_go.Left = 150 + url_width + 5
        # Favorites button at the end
        self._btn_fav.Left = 150 + url_width + 60
    
    def _navigate_from_url_bar(self):
        """Navigate to the URL in the address bar."""
        url = self._txt_url.Text.strip()
        if url:
            # Add protocol if missing
            if not url.startswith('http://') and not url.startswith('https://') and not url.startswith('file://'):
                # Check if it looks like a URL or a search query
                if '.' in url and ' ' not in url:
                    url = 'https://' + url
                else:
                    # Treat as search query
                    url = self.DEFAULT_SEARCH + url
            self.Navigate(url)
    
    def _update_url_bar(self, url):
        """Update the URL bar with the current URL."""
        if hasattr(self, '_txt_url'):
            self._txt_url.Text = url or ''
    
    def _create_status_bar(self):
        """Create the status bar using Panel."""
        self._status_bar = Panel(self, {
            'Height': 25,
            'Dock': DockStyle.Bottom,
            'BackColor': '#F0F0F0'
        })
        
        self._status_label = Label(self._status_bar, {
            'Text': 'Ready',
            'Left': 5,
            'Top': 4,
            'Width': 600,
            'Height': 18,
            'Font': Font('Segoe UI', 9)
        })
        
        self._progress_bar = ProgressBar(self._status_bar, {
            'Left': 700,
            'Top': 3,
            'Width': 150,
            'Height': 18,
            'Visible': False
        })
        
        self._zoom_label = Label(self._status_bar, {
            'Text': '100%',
            'Top': 4,
            'Width': 50,
            'Height': 18,
            'Font': Font('Segoe UI', 9)
        })
        
        # Position elements on right
        self._position_status_elements()
    
    def _position_status_elements(self):
        """Position status bar elements."""
        w = self.Width
        self._progress_bar.Left = w - 220
        self._zoom_label.Left = w - 60
    
    def _create_main_content(self):
        """Create the main content area with sidebar and tabs.
        
        CRITICAL: Dock order matters!
        1. DockStyle.Top first
        2. DockStyle.Left/Right next  
        3. DockStyle.Fill LAST
        """
        # Main container - Fill goes last but we create it first as parent
        self._main_container = Panel(self, {
            'Dock': DockStyle.Fill
        })
        
        # IMPORTANT: Inside main_container, create in correct order:
        # 1. Sidebar (Left) - create first but it's Left dock
        # 2. Tab container (Fill) - must be created AFTER sidebar
        
        # Sidebar panel (hidden by default) - DockStyle.Left
        self._sidebar = Panel(self._main_container, {
            'Width': 250,
            'Dock': DockStyle.Left,
            'BackColor': '#F5F5F5',
            'Visible': False
        })
        
        # Sidebar header - DockStyle.Top first inside sidebar
        self._sidebar_header = Panel(self._sidebar, {
            'Height': 35,
            'Dock': DockStyle.Top,
            'BackColor': '#E0E0E0'
        })
        
        self._sidebar_title = Label(self._sidebar_header, {
            'Text': 'Sidebar',
            'Left': 10,
            'Top': 8,
            'Font': Font('Segoe UI', 10, FontStyle.Bold)
        })
        
        self._sidebar_close = Button(self._sidebar_header, {
            'Text': '✕',
            'Width': 30,
            'Height': 25,
            'Top': 5,
            'FlatStyle': FlatStyle.Flat
        })
        self._sidebar_close.Left = 210
        self._sidebar_close.Click = lambda s, e: self.HideSidebar()
        
        # Sidebar content area - DockStyle.Fill AFTER Top
        self._sidebar_content = Panel(self._sidebar, {
            'Dock': DockStyle.Fill,
            'BackColor': '#FFFFFF'
        })
        
        # TabControl for browser tabs - DockStyle.Fill
        self._tab_control = TabControl(self._main_container, {
            'Dock': DockStyle.Fill
        })
        
        # Wire tab change event (handler can be called with or without args)
        self._tab_control.SelectedIndexChanged = lambda *args: self._on_tab_selected_changed()
        
        # Add tab control buttons (floating over the tab bar area)
        self._create_tab_buttons()
        
        # Setup right-click context menu on tabs
        self._setup_tab_context_menu()
        
        # Bind resize to update button positions
        if hasattr(self, '_root') and self._root:
            self._root.bind('<Configure>', lambda e: self._on_window_resize())
    
    def _create_tab_buttons(self):
        """Create floating buttons for tab management (+ and x) on the tab bar."""
        if not hasattr(self._tab_control, '_tk_widget') or not self._tab_control._tk_widget:
            return
        
        notebook = self._tab_control._tk_widget
        
        # Create a frame to hold the buttons, placed on the tab bar area
        self._tab_buttons_frame = tk.Frame(notebook, bg='#E8E8E8')
        
        # New tab button '+'
        self._btn_new_tab = tk.Button(
            self._tab_buttons_frame,
            text='+',
            font=('Segoe UI', 12, 'bold'),
            width=2,
            height=1,
            relief='flat',
            bg='#D0D0D0',
            command=self.NewTab
        )
        self._btn_new_tab.pack(side='left', padx=2)
        
        # Close current tab button '✕'
        self._btn_close_tab = tk.Button(
            self._tab_buttons_frame,
            text='✕',
            font=('Segoe UI', 9),
            width=2,
            height=1,
            relief='flat',
            bg='#D0D0D0',
            command=self._close_current_tab
        )
        self._btn_close_tab.pack(side='left', padx=2)
        
        # Tab info label
        self._tab_info_label = tk.Label(
            self._tab_buttons_frame,
            text='Tab 1 of 1',
            font=('Segoe UI', 8),
            bg='#E8E8E8'
        )
        self._tab_info_label.pack(side='left', padx=5)
        
        # Place the frame - will be positioned on window resize
        self._position_tab_buttons()
    
    def _setup_tab_context_menu(self):
        """Setup right-click context menu on tab headers."""
        if hasattr(self._tab_control, '_tk_widget') and self._tab_control._tk_widget:
            notebook = self._tab_control._tk_widget
            
            # Create context menu
            self._tab_menu = tk.Menu(notebook, tearoff=0)
            self._tab_menu.add_command(label="New Tab", command=self.NewTab)
            self._tab_menu.add_command(label="Duplicate Tab", command=self._duplicate_current_tab)
            self._tab_menu.add_separator()
            self._tab_menu.add_command(label="Close Tab", command=self._close_current_tab)
            self._tab_menu.add_command(label="Close Other Tabs", command=self._close_other_tabs)
            self._tab_menu.add_command(label="Close Tabs to the Right", command=self._close_tabs_to_right)
            self._tab_menu.add_separator()
            self._tab_menu.add_command(label="Reload Tab", command=self._refresh_page)
            
            # Bind right-click
            notebook.bind('<Button-3>', self._on_tab_right_click)
    
    def _on_tab_right_click(self, event):
        """Handle right-click on tab."""
        try:
            # Get tab index at click position
            notebook = self._tab_control._tk_widget
            tab_id = notebook.identify(event.x, event.y)
            if 'label' in str(tab_id) or notebook.index('@%d,%d' % (event.x, event.y)) is not None:
                # Show context menu
                self._tab_menu.tk_popup(event.x_root, event.y_root)
        except Exception:
            pass
        finally:
            self._tab_menu.grab_release()
    
    def _position_tab_buttons(self):
        """Position the tab buttons frame on the right side of the tab bar."""
        if not hasattr(self, '_tab_buttons_frame') or not self._tab_buttons_frame:
            return
        
        try:
            notebook = self._tab_control._tk_widget
            # Get notebook width
            notebook.update_idletasks()
            nb_width = notebook.winfo_width()
            
            # Place on the right side of the tab header area
            # The frame needs to be placed using place() for absolute positioning
            self._tab_buttons_frame.place(x=nb_width - 150, y=2, width=145, height=26)
        except Exception:
            pass
    
    def _on_window_resize(self):
        """Handle window resize to reposition elements."""
        self._position_status_elements()
        self._position_nav_elements()
        self._position_tab_buttons()
        self._update_tab_info()
    
    def _update_tab_info(self):
        """Update tab info label."""
        if hasattr(self, '_tab_info_label'):
            count = len(self._tabs)
            current = self._current_tab_index + 1 if self._current_tab_index >= 0 else 0
            # Use tkinter config for tk.Label
            if hasattr(self._tab_info_label, 'config'):
                self._tab_info_label.config(text=f'Tab {current} of {count}')
            elif hasattr(self._tab_info_label, 'Text'):
                self._tab_info_label.Text = f'Tab {current} of {count}'
    
    def _duplicate_current_tab(self):
        """Duplicate the current tab."""
        if self.CurrentTab and hasattr(self.CurrentTab, 'Url'):
            url = self.CurrentTab.Url
            if url:
                self.NewTab(url)
    
    def _close_other_tabs(self):
        """Close all tabs except the current one."""
        if len(self._tabs) <= 1:
            return
        current_tab = self._tabs[self._current_tab_index]
        # Close all tabs from the end to avoid index issues
        for i in range(len(self._tabs) - 1, -1, -1):
            if self._tabs[i] is not current_tab:
                self.CloseTab(i)
    
    def _close_tabs_to_right(self):
        """Close all tabs to the right of the current one."""
        if self._current_tab_index >= len(self._tabs) - 1:
            return
        # Close from the end to avoid index issues
        for i in range(len(self._tabs) - 1, self._current_tab_index, -1):
            self.CloseTab(i)
    
    def _bind_shortcuts(self):
        """Bind keyboard shortcuts."""
        if hasattr(self, '_root') and self._root:
            root = self._root
            
            # Tab management
            root.bind('<Control-t>', lambda e: self.NewTab())
            root.bind('<Control-T>', lambda e: self.NewTab())
            root.bind('<Control-w>', lambda e: self._close_current_tab())
            root.bind('<Control-W>', lambda e: self._close_current_tab())
            root.bind('<Control-Tab>', lambda e: self._next_tab())
            root.bind('<Control-Shift-Tab>', lambda e: self._prev_tab())
            
            # Navigation
            root.bind('<F5>', lambda e: self._refresh_page())
            root.bind('<Control-r>', lambda e: self._refresh_page())
            root.bind('<Control-R>', lambda e: self._refresh_page())
            root.bind('<Escape>', lambda e: self._stop_loading())
            root.bind('<Alt-Left>', lambda e: self._go_back())
            root.bind('<Alt-Right>', lambda e: self._go_forward())
            root.bind('<Alt-Home>', lambda e: self._go_home())
            
            # Address bar
            root.bind('<Control-l>', lambda e: self._focus_address_bar())
            root.bind('<Control-L>', lambda e: self._focus_address_bar())
            root.bind('<F6>', lambda e: self._focus_address_bar())
            
            # Sidebars
            root.bind('<Control-i>', lambda e: self._show_favorites_sidebar())
            root.bind('<Control-I>', lambda e: self._show_favorites_sidebar())
            root.bind('<Control-h>', lambda e: self._show_history_sidebar())
            root.bind('<Control-H>', lambda e: self._show_history_sidebar())
            root.bind('<Control-j>', lambda e: self._show_downloads_sidebar())
            root.bind('<Control-J>', lambda e: self._show_downloads_sidebar())
            
            # Favorites
            root.bind('<Control-d>', lambda e: self._add_current_to_favorites())
            root.bind('<Control-D>', lambda e: self._add_current_to_favorites())
            
            # View
            root.bind('<F11>', lambda e: self._toggle_fullscreen())
            root.bind('<Control-plus>', lambda e: self._zoom_in())
            root.bind('<Control-minus>', lambda e: self._zoom_out())
            root.bind('<Control-0>', lambda e: self._zoom_reset())
            
            # Find
            root.bind('<Control-f>', lambda e: self._find_on_page())
            root.bind('<Control-F>', lambda e: self._find_on_page())
    
    # ========== Tab Management ==========
    
    def NewTab(self, url=None):
        """Open a new browser tab."""
        url = url or self.DEFAULT_HOME
        
        # Create TabPage for the browser
        tab_page = TabPage(self._tab_control, {
            'Text': 'New Tab',
            'Padding': (0, 0, 0, 0)
        })
        
        # Create browser panel inside the TabPage
        # ShowNavigationBar: False - each tab only shows the web content
        # Navigation is handled by the main browser toolbar
        browser = WebBrowserPanel(tab_page, {
            'Dock': DockStyle.Fill,
            'ShowNavigationBar': False,
            'ShowStatusBar': False
        })
        
        # Wire events
        browser.DocumentTitleChanged = lambda s, e: self._on_tab_title_changed(browser)
        browser.Navigated = lambda s, e: self._on_tab_navigated(browser, e)
        browser.Navigating = lambda s, e: self._on_tab_navigating(browser, e)
        browser.DocumentCompleted = lambda s, e: self._on_document_completed(browser, e)
        
        # Add to tabs list
        tab_index = len(self._tabs)
        self._tabs.append({
            'browser': browser,
            'tab_page': tab_page,
            'title': 'New Tab',
            'url': url
        })
        
        # Switch to new tab
        self._current_tab_index = tab_index
        self._tab_control.SelectedIndex = tab_index
        
        # Update tab info
        self._update_tab_info()
        
        # Navigate
        browser.Navigate(url)
        
        return browser
    
    def _on_tab_selected_changed(self):
        """Handle TabControl selection change."""
        new_index = self._tab_control.SelectedIndex
        if new_index >= 0 and new_index < len(self._tabs):
            self._current_tab_index = new_index
            tab = self._tabs[new_index]
            self.Text = f"{tab['title']} - WinFormPy Browser"
            self._update_tab_info()
            # Update URL bar with current tab's URL
            self._update_url_bar(tab.get('url', ''))
    
    def _switch_to_tab(self, index):
        """Switch to the specified tab."""
        if index < 0 or index >= len(self._tabs):
            return
        
        self._current_tab_index = index
        self._tab_control.SelectedIndex = index
    
    def CloseTab(self, index):
        """Close a tab."""
        if len(self._tabs) <= 1:
            # Don't close last tab, open new one instead
            self.NewTab()
        
        if index < 0 or index >= len(self._tabs):
            return
        
        tab = self._tabs[index]
        
        # Remove browser
        if tab['browser'] and hasattr(tab['browser'], '_tk_widget'):
            tab['browser']._tk_widget.destroy()
        
        # Remove TabPage from TabControl
        if tab['tab_page'] and hasattr(self._tab_control, 'RemoveTab'):
            self._tab_control.RemoveTab(tab['tab_page'])
        elif tab['tab_page'] and hasattr(tab['tab_page'], '_tk_widget'):
            # Fallback: destroy the TabPage widget
            tab['tab_page']._tk_widget.destroy()
        
        # Remove from list
        self._tabs.pop(index)
        
        # Switch to appropriate tab
        if self._current_tab_index >= len(self._tabs):
            self._current_tab_index = len(self._tabs) - 1
        if self._current_tab_index >= 0:
            self._switch_to_tab(self._current_tab_index)
        
        # Update tab info
        self._update_tab_info()
    
    def _close_current_tab(self):
        """Close the current tab."""
        if self._current_tab_index >= 0:
            self.CloseTab(self._current_tab_index)
    
    def _next_tab(self):
        """Switch to next tab."""
        if len(self._tabs) > 1:
            new_index = (self._current_tab_index + 1) % len(self._tabs)
            self._switch_to_tab(new_index)
    
    def _prev_tab(self):
        """Switch to previous tab."""
        if len(self._tabs) > 1:
            new_index = (self._current_tab_index - 1) % len(self._tabs)
            self._switch_to_tab(new_index)
    
    @property
    def CurrentTab(self):
        """Get the current browser tab."""
        if 0 <= self._current_tab_index < len(self._tabs):
            return self._tabs[self._current_tab_index]['browser']
        return None
    
    # ========== Tab Events ==========
    
    def _on_tab_title_changed(self, browser):
        """Handle tab title change."""
        for i, tab in enumerate(self._tabs):
            if tab['browser'] is browser:
                title = browser.DocumentTitle or 'New Tab'
                tab['title'] = title
                if tab.get('tab_page'):
                    display_title = title[:20] + '...' if len(title) > 20 else title
                    tab['tab_page'].Text = display_title
                if i == self._current_tab_index:
                    self.Text = f"{title} - WinFormPy Browser"
                break
    
    def _on_tab_navigated(self, browser, e):
        """Handle navigation completed."""
        url = e.Url if hasattr(e, 'Url') else str(e)
        
        for i, tab in enumerate(self._tabs):
            if tab['browser'] is browser:
                tab['url'] = url
                # Update URL bar if this is the current tab
                if i == self._current_tab_index:
                    self._update_url_bar(url)
                break
        
        # Add to history
        self._add_to_history(browser.DocumentTitle or url, url)
        
        # Update status
        self._status_label.Text = f'Done - {url}'
        self._progress_bar.Visible = False
    
    def _on_tab_navigating(self, browser, e):
        """Handle navigation starting."""
        url = e.Url if hasattr(e, 'Url') else str(e)
        self._status_label.Text = f'Loading {url}...'
        self._progress_bar.Visible = True
        self._progress_bar.Value = 30
    
    def _on_document_completed(self, browser, e):
        """Handle document fully loaded."""
        self._progress_bar.Value = 100
        self._progress_bar.Visible = False
        self._status_label.Text = 'Done'
    
    # ========== Navigation ==========
    
    def _go_back(self):
        """Go back in current tab."""
        if self.CurrentTab:
            self.CurrentTab.GoBack()
    
    def _go_forward(self):
        """Go forward in current tab."""
        if self.CurrentTab:
            self.CurrentTab.GoForward()
    
    def _go_home(self):
        """Go to home page."""
        if self.CurrentTab:
            self.CurrentTab.Navigate(self.DEFAULT_HOME)
    
    def _refresh_page(self):
        """Refresh current page."""
        if self.CurrentTab:
            self.CurrentTab.Refresh()
    
    def _stop_loading(self):
        """Stop loading current page."""
        if self.CurrentTab:
            self.CurrentTab.Stop()
        self._progress_bar.Visible = False
        self._status_label.Text = 'Stopped'
    
    def _focus_address_bar(self):
        """Focus the address bar."""
        if self.CurrentTab and hasattr(self.CurrentTab, '_txt_url'):
            self.CurrentTab._txt_url.Focus()
            self.CurrentTab._txt_url.SelectAll()
    
    def Navigate(self, url):
        """Navigate the current tab to URL."""
        if self.CurrentTab:
            self.CurrentTab.Navigate(url)
    
    # ========== Sidebar ==========
    
    def ShowSidebar(self, panel_type):
        """Show sidebar with specified content."""
        # Clear existing content using WinFormPy method
        self._sidebar_content.ClearChildren()
        
        self._sidebar_title.Text = panel_type.title()
        
        if panel_type == 'favorites':
            self._populate_favorites_sidebar()
        elif panel_type == 'history':
            self._populate_history_sidebar()
        elif panel_type == 'downloads':
            self._populate_downloads_sidebar()
        
        self._sidebar.Visible = True
        self._sidebar_visible = True
        self._sidebar_panel = panel_type
    
    def HideSidebar(self):
        """Hide the sidebar."""
        self._sidebar.Visible = False
        self._sidebar_visible = False
    
    def _show_favorites_sidebar(self):
        """Show favorites sidebar."""
        if self._sidebar_visible and self._sidebar_panel == 'favorites':
            self.HideSidebar()
        else:
            self.ShowSidebar('favorites')
    
    def _show_history_sidebar(self):
        """Show history sidebar."""
        if self._sidebar_visible and self._sidebar_panel == 'history':
            self.HideSidebar()
        else:
            self.ShowSidebar('history')
    
    def _show_downloads_sidebar(self):
        """Show downloads sidebar."""
        if self._sidebar_visible and self._sidebar_panel == 'downloads':
            self.HideSidebar()
        else:
            self.ShowSidebar('downloads')
    
    def _populate_favorites_sidebar(self):
        """Populate favorites in sidebar."""
        y = 5
        for fav in self._favorites:
            btn = Button(self._sidebar_content, {
                'Text': fav.get('title', fav.get('url', ''))[:30],
                'Left': 5,
                'Top': y,
                'Width': 230,
                'Height': 28,
                'FlatStyle': FlatStyle.Flat,
                'TextAlign': 'MiddleLeft'
            })
            url = fav.get('url', '')
            btn.Click = lambda s, e, u=url: self.Navigate(u)
            y += 32
        
        if not self._favorites:
            Label(self._sidebar_content, {
                'Text': 'No favorites yet.\nPress Ctrl+D to add.',
                'Left': 10,
                'Top': 20,
                'Width': 220,
                'Height': 50
            })
    
    def _populate_history_sidebar(self):
        """Populate history in sidebar."""
        y = 5
        for item in reversed(self._history[-50:]):  # Last 50 items
            title = item.get('title', item.get('url', ''))[:30]
            btn = Button(self._sidebar_content, {
                'Text': title,
                'Left': 5,
                'Top': y,
                'Width': 230,
                'Height': 28,
                'FlatStyle': FlatStyle.Flat,
                'TextAlign': 'MiddleLeft'
            })
            url = item.get('url', '')
            btn.Click = lambda s, e, u=url: self.Navigate(u)
            y += 32
            
            if y > 500:  # Limit visible items
                break
        
        if not self._history:
            Label(self._sidebar_content, {
                'Text': 'No browsing history.',
                'Left': 10,
                'Top': 20,
                'Width': 220,
                'Height': 30
            })
    
    def _populate_downloads_sidebar(self):
        """Populate downloads in sidebar."""
        if not self._downloads:
            Label(self._sidebar_content, {
                'Text': 'No downloads.',
                'Left': 10,
                'Top': 20,
                'Width': 220,
                'Height': 30
            })
    
    # ========== Favorites ==========
    
    @property
    def Favorites(self):
        """Get favorites list."""
        return self._favorites.copy()
    
    def AddFavorite(self, title, url):
        """Add a favorite."""
        self._favorites.append({
            'title': title,
            'url': url,
            'added': datetime.now().isoformat()
        })
        self._save_data()
        self._update_favorites_menu()
    
    def _add_current_to_favorites(self):
        """Add current page to favorites."""
        if self.CurrentTab:
            title = self.CurrentTab.DocumentTitle or 'Untitled'
            url = self.CurrentTab.Url or ''
            
            # Check if already in favorites
            for fav in self._favorites:
                if fav.get('url') == url:
                    MessageBox.Show(
                        'This page is already in your favorites.',
                        'Favorites',
                        'OK'
                    )
                    return
            
            self.AddFavorite(title, url)
            self._status_label.Text = f'Added to favorites: {title}'
    
    def _update_favorites_menu(self):
        """Update favorites menu items."""
        # This would need to rebuild menu items dynamically
        pass
    
    def _manage_favorites(self):
        """Open favorites manager."""
        self._show_favorites_sidebar()
    
    # ========== History ==========
    
    @property
    def History(self):
        """Get history list."""
        return self._history.copy()
    
    def _add_to_history(self, title, url):
        """Add entry to history."""
        if url and not url.startswith('about:'):
            self._history.append({
                'title': title,
                'url': url,
                'visited': datetime.now().isoformat()
            })
            # Keep only last 1000 entries
            if len(self._history) > 1000:
                self._history = self._history[-1000:]
            self._save_data()
    
    def _clear_history(self):
        """Clear browsing history."""
        result = MessageBox.Show(
            'Are you sure you want to clear all browsing history?',
            'Clear History',
            'YesNo'
        )
        if result == DialogResult.Yes:
            self._history.clear()
            self._save_data()
            self._status_label.Text = 'History cleared'
    
    # ========== Data Persistence ==========
    
    def _get_data_file(self):
        """Get path to data file."""
        return os.path.join(_current_dir, 'browser_data.json')
    
    def _load_data(self):
        """Load saved favorites and history."""
        try:
            data_file = self._get_data_file()
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._favorites = data.get('favorites', [])
                    self._history = data.get('history', [])
        except Exception:
            pass
    
    def _save_data(self):
        """Save favorites and history."""
        try:
            data = {
                'favorites': self._favorites,
                'history': self._history
            }
            with open(self._get_data_file(), 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass
    
    # ========== File Operations ==========
    
    def _new_window(self):
        """Open new browser window."""
        # Create new instance
        new_browser = WebBrowserUI()
        new_browser.Show()
    
    def _open_file(self):
        """Open local HTML file."""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            title='Open File',
            filetypes=[
                ('HTML Files', '*.html;*.htm'),
                ('All Files', '*.*')
            ]
        )
        if filename:
            self.Navigate(f'file://{filename}')
    
    def _save_page(self):
        """Save current page."""
        # Would need to get page source and save
        self._status_label.Text = 'Save not implemented'
    
    def _print_page(self):
        """Print current page."""
        self._status_label.Text = 'Print not implemented'
    
    # ========== Edit Operations ==========
    
    def _edit_cut(self):
        """Cut to clipboard."""
        if hasattr(self, '_root'):
            self._root.event_generate('<<Cut>>')
    
    def _edit_copy(self):
        """Copy to clipboard."""
        if hasattr(self, '_root'):
            self._root.event_generate('<<Copy>>')
    
    def _edit_paste(self):
        """Paste from clipboard."""
        if hasattr(self, '_root'):
            self._root.event_generate('<<Paste>>')
    
    def _select_all(self):
        """Select all."""
        if hasattr(self, '_root'):
            self._root.event_generate('<<SelectAll>>')
    
    def _find_on_page(self):
        """Show find dialog."""
        query = InputBox("Find on page:", "Find")
        if query:
            self._status_label.Text = f'Find: {query} (not implemented)'
    
    # ========== View Operations ==========
    
    def _toggle_toolbar(self):
        """Toggle toolbar visibility."""
        if self.CurrentTab and hasattr(self.CurrentTab, '_nav_panel'):
            visible = self.CurrentTab._nav_panel.Visible
            self.CurrentTab._nav_panel.Visible = not visible
    
    def _toggle_statusbar(self):
        """Toggle status bar visibility."""
        self._status_bar.Visible = not self._status_bar.Visible
    
    def _zoom_in(self):
        """Zoom in."""
        self._status_label.Text = 'Zoom: 110% (visual zoom not supported)'
    
    def _zoom_out(self):
        """Zoom out."""
        self._status_label.Text = 'Zoom: 90% (visual zoom not supported)'
    
    def _zoom_reset(self):
        """Reset zoom."""
        self._zoom_label.Text = '100%'
    
    def _toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        if hasattr(self, '_root') and self._root:
            current = self._root.attributes('-fullscreen')
            self._root.attributes('-fullscreen', not current)
    
    # ========== Tools ==========
    
    def _clear_cache(self):
        """Clear browser cache."""
        result = MessageBox.Show(
            'Clear browser cache?',
            'Clear Cache',
            'YesNo'
        )
        if result == DialogResult.Yes:
            self._status_label.Text = 'Cache cleared (simulated)'
    
    def _show_options(self):
        """Show options dialog."""
        MessageBox.Show(
            'Options dialog not implemented yet.',
            'Options',
            'OK'
        )
    
    # ========== Help ==========
    
    def _show_help(self):
        """Show help."""
        self.NewTab('https://github.com/YourRepo/WinFormPy')
    
    def _show_about(self):
        """Show about dialog."""
        MessageBox.Show(
            "WinFormPy Browser\n\n"
            "A full-featured web browser built with WinFormPy.\n\n"
            "Features:\n"
            "• Tabbed browsing\n"
            "• Favorites & History\n"
            "• Keyboard shortcuts\n"
            "• Sidebar panels\n\n"
            "Powered by tkinterweb.",
            "About WinFormPy Browser",
            "OK"
        )


# Backward compatibility alias
BrowserUI = WebBrowserUI


# ========== Demo ==========

if __name__ == "__main__":
    print("=" * 60)
    print("WinFormPy Browser - Full Featured Web Browser")
    print("=" * 60)
    print("\nFeatures:")
    print("  • Tabbed browsing (Ctrl+T new, Ctrl+W close)")
    print("  • Navigation (Back, Forward, Refresh, Home)")
    print("  • Favorites (Ctrl+D to add, Ctrl+I sidebar)")
    print("  • History (Ctrl+H sidebar)")
    print("  • Downloads (Ctrl+J sidebar)")
    print("  • Keyboard shortcuts (F5 refresh, F11 fullscreen)")
    print("  • Menu bar with full options")
    print("  • Status bar with progress")
    print("\nStarting browser...")
    
    browser = WebBrowserUI()
    Application.Run(browser)
