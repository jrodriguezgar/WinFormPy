# =============================================================
# Module: mauipy.py
# Author: Vibe coding by DatamanEdge 
# Date: 2025-12-07
# Version: 1.0.0
# Description: 
# MAUIPy is a Python library designed to bridge the gap between
# the MAUI (Multi-platform App UI) development paradigm and
# Python's standard GUI toolkit, Tkinter. It empowers developers
# with Windows development experience to create cross-platform
# applications in Python using familiar concepts, thereby
# reducing the learning curve associated with Tkinter.
# This module is an extension of the winformpy library.
# =============================================================

import tkinter as tk
from .winformpy import (
    ControlBase, Panel, DockStyle, AnchorStyles, SystemColors, 
    FlowLayoutPanel, TableLayoutPanel, FlowDirection, Form, Application,
    Label as WinLabel, Button as WinButton, TextBox as WinTextBox, 
    PictureBox as WinPictureBox, PictureBoxSizeMode, ContentAlignment, FlatStyle
)

class Shell(Form):
    """
    The Shell class reduces the complexity of app development by providing 
    the fundamental features that most apps require, including:
    - A single place to describe the visual hierarchy of an app.
    - A common navigation user experience.
    - A URI-based navigation scheme.
    - An integrated search handler.
    """
    def __init__(self):
        super().__init__()
        self.Text = "MAUI App"
        self.Size = (1000, 700)
        self.BackColor = "white"
        
        # Initialize with a FlyoutPage structure by default
        self._flyout_page = FlyoutPage(self)
        self._flyout_page.Dock = DockStyle.Fill
        
        # Expose Flyout and Detail for easy access
        self.Flyout = self._flyout_page.Flyout
        self.Detail = self._flyout_page.Detail
        
        # Default Flyout content (Menu)
        self.FlyoutMenu = FlyoutMenu(self.Flyout)
        
        # Default Detail content (NavigationPage)
        self.Navigation = NavigationPage(self.Detail)
        self.Navigation.Dock = DockStyle.Fill
        
    @property
    def CurrentPage(self):
        """Gets the currently displayed page."""
        if self.Navigation._stack:
            return self.Navigation._stack[-1]
        return None
        
    def GoToAsync(self, page, animate=True):
        """Navigates to the specified page."""
        self.Navigation.PushAsync(page)

class VerticalStackLayout(FlowLayoutPanel):
    """
    A layout that organizes child views in a one-dimensional vertical stack.
    """
    def __init__(self, master_form, props=None):
        super().__init__(master_form, props)
        self.FlowDirection = FlowDirection.TopDown
        self.WrapContents = False
        self.Dock = DockStyle.Top # Default to stacking from top
        self.AutoSize = True
        self.AutoSizeMode = 1 # GrowOnly
        self.BackColor = "transparent"

class HorizontalStackLayout(FlowLayoutPanel):
    """
    A layout that organizes child views in a one-dimensional horizontal stack.
    """
    def __init__(self, master_form, props=None):
        super().__init__(master_form, props)
        self.FlowDirection = FlowDirection.LeftToRight
        self.WrapContents = False
        self.Dock = DockStyle.Top
        self.AutoSize = True
        self.AutoSizeMode = 1
        self.BackColor = "transparent"

class Grid(TableLayoutPanel):
    """
    A layout that organizes child views in rows and columns.
    """
    def __init__(self, master_form, props=None):
        super().__init__(master_form, props)
        self.BackColor = "transparent"
        # Grid defaults

class Label(WinLabel):
    """MAUI-style Label"""
    def __init__(self, master_form, text="", props=None):
        super().__init__(master_form, props)
        self.Text = text
        self.AutoSize = True

class Button(WinButton):
    """MAUI-style Button"""
    def __init__(self, master_form, text="", props=None):
        super().__init__(master_form, props)
        self.Text = text
        self.Height = 40
        self.FlatStyle = FlatStyle.Flat
        self.BackColor = "#512BD4" # MAUI Purple
        self.ForeColor = "white"
        self.Font = ("Segoe UI", 10, "bold")

class Entry(WinTextBox):
    """MAUI-style Entry (Single line text input)"""
    def __init__(self, master_form, placeholder="", props=None):
        super().__init__(master_form, props)
        self.PlaceholderText = placeholder
        self.Height = 35

class Image(WinPictureBox):
    """MAUI-style Image"""
    def __init__(self, master_form, source=None, props=None):
        super().__init__(master_form, props)
        self.SizeMode = PictureBoxSizeMode.Zoom
        if source:
            self.Load(source)

class FlyoutPage(Panel):
    """
    A control that manages two panes of information: 
    a master pane that presents data, and a detail pane that displays details about data.
    """
    def __init__(self, master_form, props=None):
        super().__init__(master_form, props)
        
        # Defaults
        self._is_presented = False
        self._flyout_width = 250
        self._flyout_layout_behavior = "Popover" # Split, Popover
        
        # Create internal panels
        # Detail Panel (Main Content)
        self.Detail = Panel(self)
        self.Detail.Dock = DockStyle.None_ # Manual layout
        self.Detail.BackColor = "white"
        
        # Flyout Panel (Menu/Sidebar)
        self.Flyout = Panel(self)
        self.Flyout.Width = self._flyout_width
        self.Flyout.Dock = DockStyle.None_ # Manual layout
        self.Flyout.BackColor = "#f0f0f0"
        
        # Apply properties if provided
        if props:
            if 'FlyoutWidth' in props: self.FlyoutWidth = props['FlyoutWidth']
            if 'IsPresented' in props: self.IsPresented = props['IsPresented']
            if 'FlyoutLayoutBehavior' in props: self.FlyoutLayoutBehavior = props['FlyoutLayoutBehavior']
            
        # Bind resize to update layout
        if hasattr(self, '_tk_widget'):
            self._tk_widget.bind('<Configure>', self._on_resize)
            
        # Initial State
        self._update_layout()

    @property
    def IsPresented(self):
        """Gets or sets whether the Flyout is presented."""
        return self._is_presented

    @IsPresented.setter
    def IsPresented(self, value):
        self._is_presented = value
        self._update_layout()

    @property
    def FlyoutWidth(self):
        """Gets or sets the width of the Flyout."""
        return self._flyout_width

    @FlyoutWidth.setter
    def FlyoutWidth(self, value):
        self._flyout_width = value
        self.Flyout.Width = value
        self._update_layout()
        
    @property
    def FlyoutLayoutBehavior(self):
        """Gets or sets the layout behavior of the Flyout (Split or Popover)."""
        return self._flyout_layout_behavior
        
    @FlyoutLayoutBehavior.setter
    def FlyoutLayoutBehavior(self, value):
        self._flyout_layout_behavior = value
        self._update_layout()

    def _on_resize(self, event):
        self._update_layout()

    def _update_layout(self):
        """Updates the visibility and layout of the Flyout."""
        if not hasattr(self, '_tk_widget') or not self._tk_widget:
            return
            
        w = self._tk_widget.winfo_width()
        h = self._tk_widget.winfo_height()
        
        # If not yet mapped, use requested size or default
        if w <= 1: w = self.Width
        if h <= 1: h = self.Height
        
        # Layout Detail
        if self._flyout_layout_behavior == 'Split' and self._is_presented:
            detail_x = self._flyout_width
            detail_w = max(0, w - self._flyout_width)
        else:
            detail_x = 0
            detail_w = w
            
        # Update Detail position
        if hasattr(self.Detail, '_tk_widget'):
            self.Detail.Left = detail_x
            self.Detail.Top = 0
            self.Detail.Width = detail_w
            self.Detail.Height = h
            self.Detail._tk_widget.place(x=detail_x, y=0, width=detail_w, height=h)
        
        # Layout Flyout
        if self._is_presented:
            if hasattr(self.Flyout, '_tk_widget'):
                self.Flyout.Visible = True
                self.Flyout.Left = 0
                self.Flyout.Top = 0
                self.Flyout.Width = self._flyout_width
                self.Flyout.Height = h
                self.Flyout._tk_widget.place(x=0, y=0, width=self._flyout_width, height=h)
                self.Flyout.BringToFront()
        else:
            if hasattr(self.Flyout, '_tk_widget'):
                self.Flyout.Visible = False
                self.Flyout._tk_widget.place_forget()


class PopUpFlyout:
    """
    A popup control that can be displayed as a modal or non-modal dialog.
    It provides a 'Content' Panel where you can add your controls.
    """
    def __init__(self, master_form, props=None):
        self.master_form = master_form
        
        # Resolve master widget for Toplevel
        master = master_form
        if hasattr(master_form, '_tk_widget'):
            master = master_form._tk_widget
        elif hasattr(master_form, '_root'):
            master = master_form._root
            
        self._tk_widget = tk.Toplevel(master)
        self._tk_widget.withdraw() # Hide initially
        self._tk_widget.overrideredirect(True) # No window decorations (popup style)
        
        # Defaults
        self._width = 300
        self._height = 200
        
        if props:
            if 'Width' in props: self._width = props['Width']
            if 'Height' in props: self._height = props['Height']
            
        self._tk_widget.geometry(f"{self._width}x{self._height}")
        
        # Create a wrapper to act as a parent for the Content Panel
        class WindowWrapper:
            def __init__(self, widget): 
                self._tk_widget = widget
                self.Controls = []
            def AddControl(self, c): 
                self.Controls.append(c)
            
        self.wrapper = WindowWrapper(self._tk_widget)
        
        # Content Panel - This is where the user adds controls
        self.Content = Panel(self.wrapper)
        self.Content.Dock = DockStyle.Fill
        # Ensure Content fills the Toplevel
        self.Content.Width = self._width
        self.Content.Height = self._height
        
    @property
    def Width(self):
        return self._width
        
    @Width.setter
    def Width(self, value):
        self._width = value
        self._tk_widget.geometry(f"{self._width}x{self._height}")
        
    @property
    def Height(self):
        return self._height
        
    @Height.setter
    def Height(self, value):
        self._height = value
        self._tk_widget.geometry(f"{self._width}x{self._height}")

    def Show(self, x=None, y=None):
        """Shows the popup at the specified coordinates or centered if None."""
        if x is not None and y is not None:
            self._tk_widget.geometry(f"+{x}+{y}")
        else:
            # Center on parent
            master = self._tk_widget.master
            mx = master.winfo_rootx()
            my = master.winfo_rooty()
            mw = master.winfo_width()
            mh = master.winfo_height()
            
            px = mx + (mw - self._width) // 2
            py = my + (mh - self._height) // 2
            self._tk_widget.geometry(f"+{px}+{py}")
            
        self._tk_widget.deiconify()
        self._tk_widget.lift()
        
    def Hide(self):
        """Hides the popup."""
        self._tk_widget.withdraw()


class ContentPage(Panel):
    """
    A page that displays a single view.
    """
    def __init__(self, master_form, props=None):
        super().__init__(master_form, props)
        self.Title = ""
        self.Dock = DockStyle.Fill # Default to fill
        
        if props and 'Title' in props:
            self.Title = props['Title']
            
    @property
    def Text(self):
        """Alias for Title (for compatibility with TabPage)."""
        return self.Title
        
    @Text.setter
    def Text(self, value):
        self.Title = value


class NavigationPage(Panel):
    """
    A page that manages the navigation of a stack of other pages.
    """
    def __init__(self, master_form, root_page=None, props=None):
        super().__init__(master_form, props)
        self.Dock = DockStyle.Fill
        
        # Navigation Bar
        self.NavBar = Panel(self)
        self.NavBar.Dock = DockStyle.Top
        self.NavBar.Height = 50
        self.NavBar.BackColor = "#2196F3" # Default blue
        self.NavBar.Padding = (10, 0, 10, 0)
        
        # Back Button
        from .winformpy import Button, Label, FlatStyle
        self.BackButton = Button(self.NavBar)
        self.BackButton.Text = "<"
        self.BackButton.Width = 40
        self.BackButton.Height = 30
        self.BackButton.Top = 10
        self.BackButton.Dock = DockStyle.Left
        self.BackButton.FlatStyle = FlatStyle.Flat
        self.BackButton.ForeColor = "white"
        self.BackButton.Click = self.PopAsync
        self.BackButton.Visible = False
        self.BackButton.Font = ("Segoe UI", 12, "bold")
        
        # Title Label
        self.TitleLabel = Label(self.NavBar)
        self.TitleLabel.Text = ""
        self.TitleLabel.Dock = DockStyle.Fill
        self.TitleLabel.TextAlign = "MiddleCenter"
        self.TitleLabel.ForeColor = "white"
        self.TitleLabel.Font = ("Segoe UI", 12, "bold")
        self.TitleLabel.Top = 10
        
        self._stack = []
        
        if root_page:
            self.PushAsync(root_page)

    def PushAsync(self, page):
        """Pushes a page onto the navigation stack."""
        # Hide current page if exists
        if self._stack:
            current = self._stack[-1]
            current.Visible = False
            
        self._stack.append(page)
        
        # Setup new page
        # Ensure it fills the remaining space
        page.Dock = DockStyle.Fill
        page.Visible = True
        page.BringToFront()
        
        self._update_navbar()

    def PopAsync(self):
        """Pops the current page from the navigation stack."""
        if len(self._stack) > 1:
            page = self._stack.pop()
            page.Visible = False
            
            new_current = self._stack[-1]
            new_current.Visible = True
            new_current.BringToFront()
            
            self._update_navbar()
            
    def _update_navbar(self):
        if not self._stack:
            return
            
        current = self._stack[-1]
        self.TitleLabel.Text = getattr(current, 'Title', '')
        
        # Show back button if more than 1 page
        self.BackButton.Visible = len(self._stack) > 1


class TabbedPage(Panel):
    """
    A page that consists of a list of tabs.
    Wraps a TabControl to provide a MAUI-like interface.
    """
    def __init__(self, master_form, props=None):
        super().__init__(master_form, props)
        self.Dock = DockStyle.Fill
        
        from .winformpy import TabControl
        
        self._tab_control = TabControl(self)
        self._tab_control.Dock = DockStyle.Fill
        
    @property
    def Children(self):
        """Returns the list of pages (tabs)."""
        return self._tab_control.TabPages
        
    def Add(self, page):
        """Adds a ContentPage as a tab."""
        # We treat ContentPage as a TabPage
        # It needs a _frame property for TabControl to work, 
        # but ContentPage (Panel) has _container or _tk_widget.
        # winformpy TabControl uses _frame.
        
        if not hasattr(page, '_frame'):
            # If it's a Panel, it might have _container or _tk_widget
            if hasattr(page, '_container'):
                page._frame = page._container
            elif hasattr(page, '_tk_widget'):
                page._frame = page._tk_widget
                
        # Ensure Text property exists (mapped to Title in ContentPage)
        if not hasattr(page, 'Text') and hasattr(page, 'Title'):
            page.Text = page.Title
            
        self._tab_control.AddTab(page)


class CarouselView(Panel):
    """
    A view for presenting data in a scrollable layout, where users can swipe to move through a collection of items.
    """
    def __init__(self, master_form, props=None):
        super().__init__(master_form, props)
        self.Dock = DockStyle.Fill
        self.ItemsSource = []
        self.ItemTemplate = None # Function that returns a control for an item
        self.Position = 0
        
        # Layout
        from .winformpy import Button, Label, DockStyle, FlatStyle
        
        # Main container for the current item
        self._current_item_container = Panel(self)
        self._current_item_container.Dock = DockStyle.Fill
        
        # Navigation controls (since we don't have swipe gestures easily)
        self._nav_panel = Panel(self)
        self._nav_panel.Dock = DockStyle.Bottom
        self._nav_panel.Height = 40
        self._nav_panel.BackColor = "transparent"
        
        self._btn_prev = Button(self._nav_panel)
        self._btn_prev.Text = "<"
        self._btn_prev.Width = 40
        self._btn_prev.Dock = DockStyle.Left
        self._btn_prev.Click = self._prev_item
        
        self._btn_next = Button(self._nav_panel)
        self._btn_next.Text = ">"
        self._btn_next.Width = 40
        self._btn_next.Dock = DockStyle.Right
        self._btn_next.Click = self._next_item
        
        self._lbl_indicator = Label(self._nav_panel)
        self._lbl_indicator.Text = "0 / 0"
        self._lbl_indicator.Dock = DockStyle.Fill
        self._lbl_indicator.TextAlign = "MiddleCenter"

    def SetItemsSource(self, items):
        self.ItemsSource = items
        self.Position = 0
        self._update_view()
        
    def _update_view(self):
        from .winformpy import Label, DockStyle
        # Clear current container
        for child in self._current_item_container.Controls[:]:
            if hasattr(child, '_tk_widget'):
                child._tk_widget.destroy()
            self._current_item_container.Controls.remove(child)
            
        if not self.ItemsSource:
            self._lbl_indicator.Text = "0 / 0"
            return
            
        # Update indicator
        self._lbl_indicator.Text = f"{self.Position + 1} / {len(self.ItemsSource)}"
        
        # Create item view
        item = self.ItemsSource[self.Position]
        if self.ItemTemplate:
            view = self.ItemTemplate(item)
            # Add to container
            # We need to ensure the view is parented to _current_item_container
            # If ItemTemplate created it with another parent, we might have issues.
            # Assuming ItemTemplate takes parent as argument or we reparent.
            # For now, let's assume ItemTemplate returns a control that we can place.
            
            # If the view was created with a different parent, we can't easily move it in Tkinter
            # without recreating. So ItemTemplate should probably accept a parent.
            # Or we pass _current_item_container to ItemTemplate?
            pass
        else:
            # Default view: Label
            lbl = Label(self._current_item_container)
            lbl.Text = str(item)
            lbl.Dock = DockStyle.Fill
            lbl.TextAlign = "MiddleCenter"
            lbl.Font = ("Segoe UI", 14)
            
    def _prev_item(self):
        if self.Position > 0:
            self.Position -= 1
            self._update_view()
            
    def _next_item(self):
        if self.Position < len(self.ItemsSource) - 1:
            self.Position += 1
            self._update_view()


class FlyoutMenu(Panel):
    """
    A vertical menu typically used in a FlyoutPage.
    """
    def __init__(self, master_form, props=None):
        super().__init__(master_form, props)
        self.Dock = DockStyle.Fill
        self.BackColor = "#f0f0f0"
        self.Padding = (0, 10, 0, 0)
        self._items = []
        
    def AddItem(self, text, command=None, icon=None):
        from .winformpy import Button, DockStyle, FlatStyle, ContentAlignment
        
        btn = Button(self)
        btn.Text = text
        btn.Dock = DockStyle.Top
        btn.Height = 45
        btn.FlatStyle = FlatStyle.Flat
        btn.TextAlign = ContentAlignment.MiddleLeft
        btn.Padding = (15, 0, 0, 0)
        btn.BackColor = self.BackColor
        btn.ForeColor = "black"
        btn.Font = ("Segoe UI", 10)
        
        # Remove border
        if hasattr(btn._tk_widget, 'configure'):
            btn._tk_widget.configure(borderwidth=0)
            
        if command:
            btn.Click = command
            
        # Hover effect
        def on_enter():
            btn.BackColor = "#e0e0e0"
        def on_leave():
            btn.BackColor = self.BackColor
            
        btn.MouseEnter = on_enter
        btn.MouseLeave = on_leave
        
        self._items.append(btn)
        # Reverse order because Dock=Top stacks from bottom if added sequentially? 
        # No, Dock=Top adds to top, pushing others down. 
        # So first added is at bottom? No, first added is at top.
        # Wait, in WinForms Dock=Top: last added is at top.
        # In Tkinter pack(side=TOP): first added is at top.
        # winformpy uses pack. So first added is at top. Correct.
        return btn


class SwipeLayout(Panel):
    """
    A container that simulates swipe actions (SwipeView).
    Since swipe gestures are limited, it uses a 'Reveal' button or right-click to show actions.
    """
    def __init__(self, master_form, props=None):
        super().__init__(master_form, props)
        self.Height = 60 # Default height for a list item
        
        # Content (Main view)
        self.Content = Panel(self)
        self.Content.Dock = DockStyle.Fill
        self.Content.BackColor = "white"
        
        # Actions Panel (Hidden initially)
        self.RightItems = Panel(self)
        self.RightItems.Width = 0 # Hidden
        self.RightItems.Dock = DockStyle.Right
        self.RightItems.BackColor = "#dddddd"
        
        # Reveal Button (Simulates swipe)
        from .winformpy import Button, DockStyle
        self._btn_reveal = Button(self.Content)
        self._btn_reveal.Text = "..."
        self._btn_reveal.Width = 30
        self._btn_reveal.Dock = DockStyle.Right
        self._btn_reveal.Click = self._toggle_actions
        
        self._is_open = False
        
    def AddRightItem(self, text, command, bg_color="red", text_color="white"):
        from .winformpy import Button, DockStyle, FlatStyle
        btn = Button(self.RightItems)
        btn.Text = text
        btn.Dock = DockStyle.Left
        btn.Width = 60
        btn.BackColor = bg_color
        btn.ForeColor = text_color
        btn.FlatStyle = FlatStyle.Flat
        if command:
            btn.Click = command
            
    def _toggle_actions(self):
        if self._is_open:
            self.RightItems.Width = 0
            self._is_open = False
            self._btn_reveal.Text = "..."
        else:
            # Calculate width based on children
            width = 0
            for child in self.RightItems.Controls:
                width += child.Width
            self.RightItems.Width = width if width > 0 else 100
            self._is_open = True
            self._btn_reveal.Text = ">"


class ToastNotification:
    """
    Displays a brief message that disappears automatically.
    """
    @staticmethod
    def Show(master_form, text, duration=2000):
        import tkinter as tk
        
        # Resolve master
        master = master_form
        if hasattr(master_form, '_tk_widget'):
            master = master_form._tk_widget
        elif hasattr(master_form, '_root'):
            master = master_form._root
            
        # Create Toplevel for toast
        toast = tk.Toplevel(master)
        toast.overrideredirect(True)
        
        # Style
        bg_color = "#333333"
        fg_color = "white"
        
        label = tk.Label(toast, text=text, bg=bg_color, fg=fg_color, padx=20, pady=10, font=("Segoe UI", 10))
        label.pack()
        
        # Position (Bottom Center)
        toast.update_idletasks()
        width = toast.winfo_width()
        height = toast.winfo_height()
        
        # Get parent position
        if isinstance(master, tk.Tk) or isinstance(master, tk.Toplevel):
            px = master.winfo_x()
            py = master.winfo_y()
            pw = master.winfo_width()
            ph = master.winfo_height()
        else:
            # Fallback to screen
            px = 0
            py = 0
            pw = master.winfo_screenwidth()
            ph = master.winfo_screenheight()
            
        x = px + (pw - width) // 2
        y = py + ph - height - 50 # 50px from bottom
        
        toast.geometry(f"{width}x{height}+{x}+{y}")
        
        # Auto close
        toast.after(duration, toast.destroy)


class SearchBarComponent(Panel):
    """
    A user interface control that provides a search box.
    """
    def __init__(self, master_form, props=None):
        super().__init__(master_form, props)
        self.Height = 40
        self.Padding = (5, 5, 5, 5)
        
        from .winformpy import TextBox, Button, DockStyle, FlatStyle
        
        self.SearchCommand = None
        
        # Search Button (Icon)
        self._btn_search = Button(self)
        self._btn_search.Text = "🔍"
        self._btn_search.Width = 30
        self._btn_search.Dock = DockStyle.Right
        self._btn_search.FlatStyle = FlatStyle.Flat
        self._btn_search.Click = self._on_search
        
        # Text Box
        self.TextBox = TextBox(self)
        self.TextBox.Dock = DockStyle.Fill
        self.TextBox.PlaceholderText = "Search..."
        # Bind Enter key
        if hasattr(self.TextBox, '_tk_widget'):
            self.TextBox._tk_widget.bind('<Return>', lambda e: self._on_search())
            
    @property
    def Text(self):
        return self.TextBox.Text
        
    @Text.setter
    def Text(self, value):
        self.TextBox.Text = value
        
    @property
    def Placeholder(self):
        return self.TextBox.PlaceholderText
        
    @Placeholder.setter
    def Placeholder(self, value):
        self.TextBox.PlaceholderText = value
        
    def _on_search(self):
        if self.SearchCommand:
            self.SearchCommand(self.Text)


class ChipTag(Panel):
    """
    A compact element that represents an input, attribute, or action.
    """
    def __init__(self, master_form, text="Chip", props=None):
        super().__init__(master_form, props)
        self.AutoSize = True
        self.AutoSizeMode = 1 # GrowOnly
        self.Padding = (2, 2, 2, 2)
        self.BackColor = "#e0e0e0"
        
        # Rounded corners are hard in pure Tkinter without canvas, 
        # so we simulate with a frame and padding.
        
        from .winformpy import Label, Button, DockStyle, FlatStyle
        
        self.CloseCommand = None
        
        # Close Button (Optional)
        self._btn_close = Button(self)
        self._btn_close.Text = "×"
        self._btn_close.Width = 20
        self._btn_close.Dock = DockStyle.Right
        self._btn_close.FlatStyle = FlatStyle.Flat
        self._btn_close.BackColor = "transparent"
        self._btn_close.Click = self._on_close
        self._btn_close.Visible = False # Hidden by default
        
        # Text Label
        self.Label = Label(self)
        self.Label.Text = text
        self.Label.Dock = DockStyle.Fill
        self.Label.TextAlign = "MiddleCenter"
        self.Label.Padding = (5, 0, 5, 0)
        self.Label.BackColor = "transparent"
        
    @property
    def Text(self):
        return self.Label.Text
        
    @Text.setter
    def Text(self, value):
        self.Label.Text = value
        
    @property
    def IsClosable(self):
        return self._btn_close.Visible
        
    @IsClosable.setter
    def IsClosable(self, value):
        self._btn_close.Visible = value
        
    def _on_close(self):
        if self.CloseCommand:
            self.CloseCommand()
        else:
            self.Visible = False


class StepperControl(Panel):
    """
    A control that allows the user to select a double value from a range of values.
    """
    def __init__(self, master_form, props=None):
        super().__init__(master_form, props)
        self.Height = 30
        self.Width = 120
        
        self.Minimum = 0
        self.Maximum = 100
        self.Increment = 1
        self._value = 0
        
        from .winformpy import Button, Label, DockStyle
        
        self._btn_minus = Button(self)
        self._btn_minus.Text = "-"
        self._btn_minus.Width = 30
        self._btn_minus.Dock = DockStyle.Left
        self._btn_minus.Click = self._decrement
        
        self._btn_plus = Button(self)
        self._btn_plus.Text = "+"
        self._btn_plus.Width = 30
        self._btn_plus.Dock = DockStyle.Right
        self._btn_plus.Click = self._increment
        
        self._lbl_value = Label(self)
        self._lbl_value.Text = str(self._value)
        self._lbl_value.Dock = DockStyle.Fill
        self._lbl_value.TextAlign = "MiddleCenter"
        
        self.ValueChanged = lambda value: None
        
    @property
    def Value(self):
        return self._value
        
    @Value.setter
    def Value(self, value):
        # Clamp
        val = max(self.Minimum, min(self.Maximum, value))
        if self._value != val:
            self._value = val
            self._lbl_value.Text = str(val)
            self.ValueChanged(val)
            
    def _increment(self):
        self.Value += self.Increment
        
    def _decrement(self):
        self.Value -= self.Increment

