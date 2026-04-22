# =============================================================
# Module: mauipy.py
# Author: DatamanEdge
# Date: 2025-12-07
# Version: 1.0.4
# License: MIT
#
# Description:
#   MAUIPy is a comprehensive Python library that bridges the
#   .NET MAUI (Multi-platform App UI) development paradigm with
#   Python's Tkinter GUI toolkit. It enables developers familiar
#   with Windows/.NET development patterns to create modern,
#   cross-platform desktop applications using Pythonic syntax.
#
# Features:
#   - Shell-based navigation with flyout menus
#   - MVVM-friendly page architecture (ContentPage, TabbedPage)
#   - Modern UI controls (Switch, Slider, DatePicker, etc.)
#   - Material Design components (FAB, Cards, BottomSheet)
#   - Responsive layouts (Grid, StackLayout)
#   - WinFormPy-style property assignment via defaults dict
#   - All controls support props parameter for bulk property config
#   - Event properties with getter/setter (Click, TextChanged, etc.)
#
# Dependencies:
#   - Python 3.10+
#   - tkinter (standard library)
#   - Pillow (optional, for image support - auto-installed on demand)
# =============================================================

from datetime import datetime, date, time
import sys
import os
import subprocess

# Windows 11 Font support
if sys.platform == "win32":
    DEFAULT_FONT_FAMILY = "Segoe UI Variable Display"
    DEFAULT_FONT_TEXT = "Segoe UI Variable Text"
    DEFAULT_FONT_ICONS = "Segoe Fluent Icons"
else:
    DEFAULT_FONT_FAMILY = "Segoe UI"
    DEFAULT_FONT_TEXT = "Segoe UI"
    DEFAULT_FONT_ICONS = "Segoe UI"

# Import WinFormPy base controls
try:
    # Try relative import first (when part of a package)
    from .winformpy import (
        Application, Form, ControlBase, DockStyle, Size, Color, Font,
        MessageBox, Panel, Label as WinFormLabel, Button as WinFormButton,
        FormStartPosition, get_tk_root, Native,
        TOP, BOTTOM, LEFT, RIGHT, BOTH, X, Y, CENTER, END, VERTICAL, HORIZONTAL, SOLID, WORD, FLAT, ARC
    )
except (ImportError, ValueError):
    try:
        # Try absolute import from the module file
        from winformpy import (
            Application, Form, ControlBase, DockStyle, Size, Color, Font,
            MessageBox, Panel, Label as WinFormLabel, Button as WinFormButton,
            FormStartPosition, get_tk_root, Native,
            TOP, BOTTOM, LEFT, RIGHT, BOTH, X, Y, CENTER, END, VERTICAL, HORIZONTAL, SOLID, WORD, FLAT, ARC
        )
    except ImportError:
        # Fallback for direct execution or unusual path setups
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.append(current_dir)
        try:
            from winformpy import (
                Application, Form, ControlBase, DockStyle, Size, Color, Font,
                MessageBox, Panel, Label as WinFormLabel, Button as WinFormButton,
                FormStartPosition, get_tk_root, Native,
                TOP, BOTTOM, LEFT, RIGHT, BOTH, X, Y, CENTER, END, VERTICAL, HORIZONTAL, SOLID, WORD, FLAT, ARC
            )
        except ImportError:
            # winformpy not available
            pass


# =============================================================
# Lazy Library Import Management (supports pip and uv)
# =============================================================

def _is_uv_managed_environment() -> bool:
    """Check if the current Python environment is managed by uv."""
    if os.environ.get('UV_PROJECT_ENVIRONMENT'):
        return True
    if 'uv' in sys.executable.lower():
        return True
    exe_dir = os.path.dirname(sys.executable)
    venv_dir = os.path.dirname(exe_dir)
    pyvenv_cfg = os.path.join(venv_dir, 'pyvenv.cfg')
    if os.path.exists(pyvenv_cfg):
        try:
            with open(pyvenv_cfg, 'r') as f:
                content = f.read()
                if 'uv =' in content or 'uv=' in content:
                    return True
        except Exception:
            pass
    return False


def _find_pyproject_dir() -> str:
    """Find the directory containing pyproject.toml."""
    current = os.getcwd()
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, 'pyproject.toml')):
            return current
        current = os.path.dirname(current)
    return None


def install_library(library_name: str, import_name: str = None) -> bool:
    """
    Checks if a library is installed and, if not, attempts to install it.
    Uses 'uv add' if the environment is uv-managed, otherwise uses pip.
    """
    check_name = import_name if import_name else library_name
    try:
        __import__(check_name)
        return True
    except ImportError:
        print(f"Installing '{library_name}'...")
        try:
            if _is_uv_managed_environment():
                project_dir = _find_pyproject_dir()
                if project_dir:
                    subprocess.check_call(["uv", "add", library_name], cwd=project_dir)
                else:
                    subprocess.check_call(["uv", "pip", "install", "--system", library_name])
            else:
                subprocess.check_call([sys.executable, "-m", "pip", "install", library_name])
            print(f"✓ '{library_name}' installed")
            return True
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install '{library_name}'")
            return False
        except FileNotFoundError:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", library_name])
                return True
            except subprocess.CalledProcessError:
                print(f"✗ Failed. For uv envs: uv add {library_name}")
                return False


class EventArgs:
    """Base class for event data."""
    def __init__(self, event=None, **kwargs):
        # Default properties
        self.X = 0
        self.Y = 0
        self.Width = 0
        self.Height = 0
        self.Button = 0
        self.KeyChar = ''
        self.KeyCode = ''
        self.Delta = 0
        self.Shift = False
        self.Control = False
        self.Alt = False
        self.Data = None

        if event is not None:
            if hasattr(event, 'x'):
                # Map Tkinter event properties to WinForms-friendly names
                self.X = getattr(event, 'x', 0)
                self.Y = getattr(event, 'y', 0)
                self.Width = getattr(event, 'width', 0)
                self.Height = getattr(event, 'height', 0)
                self.Button = getattr(event, 'num', 0)
                self.KeyChar = getattr(event, 'char', '')
                self.KeyCode = getattr(event, 'keysym', '')
                self.Delta = getattr(event, 'delta', 0)

                # State masks for modifiers
                state = getattr(event, 'state', 0)
                if isinstance(state, int):
                    self.Shift = bool(state & 0x0001)
                    self.Control = bool(state & 0x0004)
                    self.Alt = bool(state & 0x20000) or bool(state & 0x0020) or bool(state & 8)
            else:
                self.Data = event

        # Apply additional custom data/overrides
        for key, value in kwargs.items():
            setattr(self, key, value)
            if key.lower() == 'data':
                self.Data = value

    @property
    def Empty(self):
        return EventArgs()

EventArgs.Empty = EventArgs()


# =============================================================================
# MAUI VIEW & LAYOUT BASE CLASSES
# =============================================================================

class View:
    """
    Base class for all MAUI visual elements.

    Equivalent to Microsoft.Maui.Controls.View in .NET MAUI.
    Provides common properties, events, and parent resolution for all
    controls that participate in MAUI pack/grid-based layouts.

    This is distinct from winformpy.ControlBase which uses absolute
    (place-based) positioning for WinForms scenarios.

    Properties:
        IsVisible (bool): Gets or sets whether the control is visible.
        IsEnabled (bool): Gets or sets whether the control is enabled.

    Methods:
        GetTkWidget(): Returns the underlying Tkinter widget (read-only escape hatch).
    """

    def __init__(self, master, side=TOP, use_grid=False):
        self._master = master
        self._side = side
        self._use_grid = use_grid
        self._is_visible = True
        self._is_enabled = True

        # Resolve parent frame (MAUI parent resolution)
        if hasattr(master, '_frame'):
            self._parent = master._frame
        else:
            self._parent = master

        # Standard mouse events (.NET MAUI pattern)
        self.Click = lambda sender, e: None
        self.DoubleClick = lambda sender, e: None
        self.MouseDown = lambda sender, e: None
        self.MouseUp = lambda sender, e: None
        self.MouseMove = lambda sender, e: None
        self.MouseEnter = lambda sender, e: None
        self.MouseLeave = lambda sender, e: None

    def _bind_standard_events(self):
        """Binds standard mouse events to self._tk_widget."""
        _bind_standard_mouse_events(self._tk_widget, self)

    def _get_parent_bg(self):
        """Gets the parent background color."""
        try:
            return self._parent.cget("bg")
        except Exception:
            return "#FAFAFA"

    @property
    def IsVisible(self):
        """Gets or sets whether the control is visible."""
        return self._is_visible

    @IsVisible.setter
    def IsVisible(self, value):
        self._is_visible = value
        target = getattr(self, '_container', getattr(self, '_frame', self._tk_widget))
        if value:
            target.pack(side=self._side)
        else:
            target.pack_forget()

    @property
    def IsEnabled(self):
        """Gets or sets whether the control is enabled."""
        return self._is_enabled

    @IsEnabled.setter
    def IsEnabled(self, value):
        self._is_enabled = value
        state = "normal" if value else "disabled"
        try:
            self._tk_widget.configure(state=state)
        except Exception:
            pass

    def GetTkWidget(self):
        """Returns the underlying Tkinter widget (read-only escape hatch)."""
        return self._tk_widget

    # -- Tkinter geometry proxies so callers can fine-tune layout after init --

    def pack(self, **kwargs):
        """Delegates pack() to the underlying Tkinter widget."""
        self._tk_widget.pack(**kwargs)

    def pack_forget(self):
        """Delegates pack_forget() to the underlying Tkinter widget."""
        self._tk_widget.pack_forget()

    def pack_configure(self, **kwargs):
        """Delegates pack_configure() to the underlying Tkinter widget."""
        self._tk_widget.pack_configure(**kwargs)

    def configure(self, **kwargs):
        """Delegates configure() to the underlying Tkinter widget."""
        self._tk_widget.configure(**kwargs)


class Layout:
    """
    Base class for MAUI layout containers.

    Equivalent to Microsoft.Maui.Controls.Layout in .NET MAUI.
    Provides common container functionality for arranging child elements
    with Spacing and Padding support.

    Properties:
        Spacing (int): Space between child elements in pixels.
        Padding (tuple): Container padding as (left, top, right, bottom).
        BackColor (str): Background color of the layout container.
    """

    def __init__(self, master, props=None):
        defaults = {
            'Spacing': 4,
            'Padding': (20, 20, 20, 20),
            'BackColor': None
        }
        if props:
            defaults.update(props)

        self._master = master
        self.Spacing = defaults['Spacing']
        self.Padding = defaults['Padding']
        self.BackColor = defaults['BackColor']
        self._children = []

        # Resolve parent (layouts check _content first for ContentPage/Card)
        if hasattr(master, '_content'):
            parent = master._content
        elif hasattr(master, '_frame'):
            parent = master._frame
        else:
            parent = master

        self._bg = self.BackColor if self.BackColor else parent.cget("bg")
        self._frame = Native.Frame(parent, bg=self._bg)
        self._frame.pack(fill=X, padx=(self.Padding[0], self.Padding[2]),
                        pady=(self.Padding[1], self.Padding[3]))


class StackLayout(Layout):
    """
    Arranges child elements in a single line (vertical or horizontal).

    Equivalent to Microsoft.Maui.Controls.StackLayout in .NET MAUI.
    Unifies VerticalStackLayout and HorizontalStackLayout with an
    Orientation property.

    Properties:
        Orientation (str): 'Vertical' or 'Horizontal' (default: 'Vertical').
        Spacing (int): Space between children in pixels.
        Padding (tuple): Container padding as (left, top, right, bottom).

    Methods:
        AddChild(widget_class, **kwargs): Adds a child widget to the layout.

    Example:
        >>> stack = StackLayout(page.Content, props={'Orientation': 'Horizontal', 'Spacing': 10})
        >>> stack.AddChild(Button, text='Save')
        >>> stack.AddChild(Button, text='Cancel')
    """

    def __init__(self, master, props=None):
        if props is None:
            props = {}
        self._orientation = props.pop('Orientation', 'Vertical')
        super().__init__(master, props=props)

    def AddChild(self, widget_class, **kwargs):
        """Adds a child widget to the layout."""
        # Add spacing if not first child
        if self._children:
            if self._orientation == 'Horizontal':
                spacer = Native.Frame(self._frame, width=self.Spacing, bg=self._bg)
                spacer.pack(side=LEFT)
            else:
                spacer = Native.Frame(self._frame, height=self.Spacing, bg=self._bg)
                spacer.pack(fill=X)

        # Create widget
        if self._orientation == 'Horizontal':
            widget = widget_class(self._frame, side=LEFT, **kwargs)
        else:
            widget = widget_class(self._frame, **kwargs)

        self._children.append(widget)
        return widget

    @property
    def Orientation(self):
        """Gets the layout orientation ('Vertical' or 'Horizontal')."""
        return self._orientation


# =============================================================================
# SHELL - Main Application Container
# =============================================================================

class Shell(Form):
    """
    Main application container with integrated navigation and flyout menu.

    The Shell class serves as the root container for MAUI-style applications,
    providing a consistent navigation experience with a hamburger menu (flyout),
    header bar, and content area for hosting pages.

    Features:
        - Collapsible flyout sidebar menu with customizable items
        - Header bar with title and menu toggle button
        - Page navigation stack with back navigation support
        - Centralized visual hierarchy management

    Properties:
        Text (str): Window title displayed in the title bar.
        FlyoutWidth (int): Width of the flyout menu in pixels (default: 250).
        HeaderTitle (str): Text displayed in the header bar.
        HeaderColor (str): Background color of the header bar.

    Methods:
        AddMenuItem(text, command, icon): Adds a menu item to the flyout.
        AddMenuSeparator(): Adds a visual separator in the flyout menu.
        NavigateTo(page_class): Navigates to a new page.
        GoBack(): Returns to the previous page in the navigation stack.
        Run(): Starts the application main loop.

    Example:
        >>> app = Shell(props={'Text': 'My App'})
        >>> app.AddMenuItem('Home', lambda: app.NavigateTo(HomePage), '🏠')
        >>> app.NavigateTo(HomePage)
        >>> app.Run()
    """
    def __init__(self, props=None):
        # Default values - WinFormPy style
        defaults = {
            'Text': 'MAUI App',
            'Width': 1000,
            'Height': 700,
            'BackColor': '#FAFAFA',
            'HeaderColor': '#512BD4',
            'HeaderTextColor': 'white',
            'FlyoutWidth': 250,
            'FlyoutBackgroundColor': '#F0F0F0',
            'FlyoutTextColor': '#333333',
            'FlyoutSelectedColor': '#E0E0E0',
            'HeaderHeight': 50,
            'FontFamily': DEFAULT_FONT_FAMILY,
            'CenterOnScreen': True,
            'FlyoutBehavior': 'Flyout', # Options: Flyout, Locked, Disabled
            'WindowState': 'Normal',
            'FlyoutIsPresented': False
        }

        # Apply props over defaults
        if props:
            defaults.update(props)

        # Convert MAUI props to WinFormPy props where they overlap
        wf_props = {
            'Text': defaults['Text'],
            'Width': defaults['Width'],
            'Height': defaults['Height'],
            'BackColor': defaults['BackColor'],
            'WindowState': defaults['WindowState']
        }

        if defaults['CenterOnScreen']:
            # StartPosition is how winformpy handles centering
            wf_props['StartPosition'] = FormStartPosition.CenterScreen

        # Initialize base Form
        super().__init__(wf_props)

        # Internal state
        self._flyout_width = defaults['FlyoutWidth']
        self._flyout_visible = False
        self._flyout_behavior = defaults['FlyoutBehavior']
        self._flyout_is_presented = defaults['FlyoutIsPresented']
        self._header_height = defaults['HeaderHeight']
        self._header_color = defaults['HeaderColor']
        self._header_text_color = defaults['HeaderTextColor']
        self._flyout_bg_color = defaults['FlyoutBackgroundColor']
        self._flyout_fg_color = defaults['FlyoutTextColor']
        self._flyout_sel_color = defaults['FlyoutSelectedColor']
        self._font_family = defaults['FontFamily']

        # Build UI structure
        self._build_shell_structure()

        # Apply behavior and initial state
        self.FlyoutBehavior = self._flyout_behavior
        if self._flyout_is_presented:
            self.FlyoutIsPresented = True

        # Apply initial window title
        if 'Text' in defaults:
            self.Text = defaults['Text']

    def _build_shell_structure(self):
        """Builds the internal shell structure."""
        # Header Bar
        self._header = Native.Frame(self._root, bg=self._header_color, height=self._header_height)
        self._header.pack(fill=X, side=TOP)
        Native.PackPropagate(self._header, False)

        # Menu toggle button
        self._menu_btn = Native.Button(
            self._header,
            text="☰",
            font=(self._font_family, 14),
            bg=self._header_color,
            fg=self._header_text_color,
            bd=0,
            activebackground=self._header_color,
            activeforeground=self._header_text_color,
            cursor="hand2",
            command=self._toggle_flyout
        )
        self._menu_btn.pack(side=LEFT, padx=10)

        # Title label
        self._title_label = Native.Label(
            self._header,
            text="",
            font=(self._font_family, 12, "bold"),
            bg=self._header_color,
            fg=self._header_text_color
        )
        self._title_label.pack(side=LEFT, padx=10)

        # Main container (holds flyout and content)
        self._main_container = Native.Frame(self._root, bg=self._root.cget("bg"))
        self._main_container.pack(fill=BOTH, expand=True)

        # Flyout Panel (sidebar menu) - starts hidden (not packed)
        self._flyout_frame = Native.Frame(self._main_container, bg=self._flyout_bg_color, width=self._flyout_width)
        Native.PackPropagate(self._flyout_frame, False)

        # Flyout content area
        self._flyout_content = Native.Frame(self._flyout_frame, bg=self._flyout_bg_color)
        self._flyout_content.pack(fill=BOTH, expand=True, pady=10)

        # Content Area (main content)
        self._content_frame = Native.Frame(self._main_container, bg="#FAFAFA")
        self._content_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Navigation stack
        self._page_stack = []
        self._current_page = None

    def _toggle_flyout(self):
        """Toggles the flyout menu visibility."""
        if self._flyout_visible:
            self._hide_flyout()
        else:
            self._show_flyout()

    def _show_flyout(self):
        """Shows the flyout menu."""
        self._flyout_visible = True
        # Unpack content so flyout gets space first, then re-pack content
        self._content_frame.pack_forget()
        self._flyout_frame.pack(side=LEFT, fill=Y)
        self._content_frame.pack(side=LEFT, fill=BOTH, expand=True)

    def _hide_flyout(self):
        """Hides the flyout menu."""
        self._flyout_visible = False
        self._flyout_frame.pack_forget()

    @property
    def Text(self):
        """Gets or sets the window title."""
        return self._root.title()

    @Text.setter
    def Text(self, value):
        self._root.title(value)

    @property
    def FlyoutWidth(self):
        """Gets or sets the flyout width."""
        return self._flyout_width

    @FlyoutWidth.setter
    def FlyoutWidth(self, value):
        self._flyout_width = value
        if self._flyout_visible:
            self._flyout_frame.configure(width=value)

    @property
    def HeaderTitle(self):
        """Gets or sets the header title."""
        return self._title_label.cget("text")

    @HeaderTitle.setter
    def HeaderTitle(self, value):
        self._title_label.configure(text=value)

    @property
    def HeaderColor(self):
        """Gets or sets the header background color."""
        return self._header.cget("bg")

    @HeaderColor.setter
    def HeaderColor(self, value):
        self._header_color = value
        self._header.configure(bg=value)
        self._menu_btn.configure(bg=value, activebackground=value)
        self._title_label.configure(bg=value)

    @property
    def HeaderTextColor(self):
        """Gets or sets the header text color."""
        return self._header_text_color

    @HeaderTextColor.setter
    def HeaderTextColor(self, value):
        self._header_text_color = value
        self._menu_btn.configure(fg=value, activeforeground=value)
        self._title_label.configure(fg=value)

    @property
    def FlyoutBehavior(self):
        """Gets or sets the flyout behavior (Flyout, Locked, Disabled)."""
        return self._flyout_behavior

    @FlyoutBehavior.setter
    def FlyoutBehavior(self, value):
        self._flyout_behavior = value
        if value == "Disabled":
            self._hide_flyout()
            self._menu_btn.pack_forget()
        elif value == "Locked":
            self._show_flyout()
            self._menu_btn.pack_forget()
        else: # Flyout
            # If behavior is set to Flyout, we respect current visibility
            # unless it was initialized with FlyoutIsPresented=True
            if not getattr(self, '_flyout_visible', False):
                self._hide_flyout()

            if hasattr(self, '_menu_btn'):
                self._menu_btn.pack(side=LEFT, padx=10)

    @property
    def FlyoutIsPresented(self):
        """Gets or sets whether the flyout is currently presented (open)."""
        return self._flyout_visible

    @FlyoutIsPresented.setter
    def FlyoutIsPresented(self, value):
        if value:
            self._show_flyout()
        else:
            self._hide_flyout()

    def AddMenuItem(self, text, command=None, icon=""):
        """Adds a menu item to the flyout."""
        display_text = f"{icon}  {text}" if icon else text

        # Wrap command to close flyout if in Flyout mode
        def wrapped_command():
            if self._flyout_behavior == "Flyout":
                self._hide_flyout()
            if command:
                command()

        btn = Native.Button(
            self._flyout_content,
            text=display_text,
            font=(self._font_family, 11),
            bg=self._flyout_bg_color,
            fg=self._flyout_fg_color,
            bd=0,
            anchor="w",
            padx=20,
            pady=12,
            activebackground=self._flyout_sel_color,
            activeforeground=self._flyout_fg_color,
            cursor="hand2",
            command=wrapped_command
        )
        btn.pack(fill=X)

        # Hover effects
        btn.bind("<Enter>", lambda e: btn.configure(bg=self._flyout_sel_color))
        btn.bind("<Leave>", lambda e: btn.configure(bg=self._flyout_bg_color))

        return btn

    def AddMenuSeparator(self):
        """Adds a separator line to the flyout menu."""
        # Use a shade slightly different from background
        sep_color = "#D0D0D0" if self._flyout_bg_color.lower() in ["#f0f0f0", "white", "#ffffff"] else "#404040"
        sep = Native.Frame(self._flyout_content, bg=sep_color, height=1)
        sep.pack(fill=X, padx=10, pady=5)

    def NavigateTo(self, page_class, *args, **kwargs):
        """Navigates to a new page."""
        # Auto-hide flyout on navigation if in Flyout mode
        if self._flyout_behavior == "Flyout":
            self._hide_flyout()

        # Create page instance
        page = page_class(self._content_frame, *args, **kwargs)

        # Hide current page
        if self._current_page:
            self._current_page._frame.pack_forget()

        # Show new page
        page._frame.pack(fill=BOTH, expand=True)
        Native.Lift(page._frame)
        Native.Focus(page._frame)

        # Update stack and title
        self._page_stack.append(page)
        self._current_page = page
        self.HeaderTitle = getattr(page, 'Title', '')

        # Force update to ensure layout is calculated and visible
        Native.Update(self._root)
        Native.Update(self._root)

        return page

    def GoBack(self):
        """Goes back to the previous page."""
        if len(self._page_stack) > 1:
            # Remove current page
            current = self._page_stack.pop()
            Native.Destroy(current._frame)

            # Show previous page
            self._current_page = self._page_stack[-1]
            self._current_page._frame.pack(fill=BOTH, expand=True)
            self.HeaderTitle = getattr(self._current_page, 'Title', '')

    @property
    def CanGoBack(self):
        """Returns True if there's a previous page to go back to."""
        return len(self._page_stack) > 1

    @property
    def CurrentPage(self):
        """Gets the currently displayed page."""
        return self._current_page

    def Show(self):
        """Displays the shell window (winformpy Application.Run compatibility)."""
        super().Show()
        if Native.Exists(self._root):
            Native.Deiconify(self._root)
            Native.Lift(self._root)
            Native.ForceFocus(self._root)

    def Run(self):
        """Starts the application main loop."""
        if isinstance(self._root, Native.Window):
            self.Show()
        else:
            Native.Mainloop(self._root)


# =============================================================================
# PAGE CLASSES
# =============================================================================

class ContentPage:
    """
    Base page class for displaying scrollable content in MAUI-style applications.

    ContentPage provides a scrollable container for hosting UI controls and layouts.
    It serves as the foundation for building individual screens in an application,
    with built-in vertical scrolling and mouse wheel support.

    Properties:
        Title (str): Page title displayed in the Shell header when navigated to.
        BackColor (str): Background color of the page content area.
        Content (Frame): The scrollable content frame for adding child controls.

    Example:
        >>> class HomePage(ContentPage):
        ...     def __init__(self, master):
        ...         super().__init__(master, props={'Title': 'Home'})
        ...         Label(self.Content, text='Welcome!')
    """
    def __init__(self, master, props=None):
        # Default values - WinFormPy style
        defaults = {
            'Title': '',
            'BackColor': '#FAFAFA'
        }

        # Apply props over defaults
        if props:
            defaults.update(props)

        self._master = master
        self.Title = defaults['Title']
        self.BackColor = defaults['BackColor']

        # Create main frame
        self._frame = Native.Frame(master, bg=self.BackColor)

        # Content area with scrolling
        self._canvas = Native.Canvas(self._frame, bg=self.BackColor, highlightthickness=0)
        self._scrollbar = Native.Scrollbar(self._frame, orient=VERTICAL, command=self._canvas.yview)
        self._content = Native.Frame(self._canvas, bg=self.BackColor)

        # Configure scrolling
        self._content.bind("<Configure>", lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))
        self._canvas_window = self._canvas.create_window((0, 0), window=self._content, anchor="nw")
        self._canvas.configure(yscrollcommand=self._scrollbar.set)

        # Pack scrollable area
        self._scrollbar.pack(side=RIGHT, fill=Y)
        self._canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Bind canvas resize to content width
        self._canvas.bind("<Configure>", self._on_canvas_configure)

        # Mouse wheel scrolling
        self._frame.bind("<Enter>", lambda e: self._bind_mousewheel())
        self._frame.bind("<Leave>", lambda e: self._unbind_mousewheel())

    @property
    def BackColor(self):
        """Gets or sets the background color."""
        return self._back_color

    @BackColor.setter
    def BackColor(self, value):
        self._back_color = value
        if hasattr(self, '_frame'):
            self._frame.configure(bg=value)
        if hasattr(self, '_canvas'):
            self._canvas.configure(bg=value)
        if hasattr(self, '_content'):
            self._content.configure(bg=value)

    def _on_canvas_configure(self, event):
        """Adjusts content width to canvas width."""
        # Ensure minimum width to avoid being invisible
        width = max(event.width, 10)
        self._canvas.itemconfig(self._canvas_window, width=width)

    def _bind_mousewheel(self):
        """Binds mouse wheel to scrolling."""
        self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        # Force a configured event to ensure components are sized correctly
        Native.Wait(self._frame, 10, lambda: self._on_canvas_configure(EventArgs(width=Native.GetSize(self._canvas)[0])))

    def _unbind_mousewheel(self):
        """Unbinds mouse wheel scrolling."""
        self._canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Handles mouse wheel scrolling."""
        self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    @property
    def Content(self):
        """Returns the content frame where controls should be added."""
        return self._content


class NavigationPage:
    """
    Container page with built-in navigation bar and hierarchical page stack.

    NavigationPage manages a stack of child pages with automatic back button
    handling and title updates. Ideal for drill-down navigation patterns
    where users navigate deeper into content hierarchies.

    Properties:
        Title (str): Current page title shown in the navigation bar.
        BackColor (str): Background color of the page.
        NavBarColor (str): Background color of the navigation bar.
        NavBarHeight (int): Height of the navigation bar in pixels.

    Methods:
        PushAsync(page_class): Pushes a new page onto the navigation stack.
        PopAsync(): Removes the current page and returns to the previous one.

    Example:
        >>> nav = NavigationPage(root, root_page_class=MainPage)
        >>> nav.PushAsync(DetailPage)  # Navigate forward
        >>> nav.PopAsync()  # Go back
    """
    def __init__(self, master, root_page_class=None, props=None):
        # Default values - WinFormPy style
        defaults = {
            'Title': '',
            'BackColor': '#FAFAFA',
            'NavBarColor': '#2196F3',
            'NavBarHeight': 50
        }

        # Apply props over defaults
        if props:
            defaults.update(props)

        self._master = master
        self.Title = defaults['Title']
        self.BackColor = defaults['BackColor']
        self.NavBarColor = defaults['NavBarColor']
        self.NavBarHeight = defaults['NavBarHeight']

        # Create main frame
        self._frame = Native.Frame(master, bg=self.BackColor)

        # Navigation bar
        self._navbar = Native.Frame(self._frame, bg=self.NavBarColor, height=self.NavBarHeight)
        self._navbar.pack(fill=X, side=TOP)
        Native.PackPropagate(self._navbar, False)

        # Back button
        self._back_btn = Native.Button(
            self._navbar,
            text="←",
            font=("Segoe UI", 14, "bold"),
            bg=self.NavBarColor,
            fg="white",
            bd=0,
            activebackground=self.NavBarColor,
            activeforeground="white",
            cursor="hand2",
            command=self._go_back
        )
        self._back_btn.pack(side=LEFT, padx=10)
        self._back_btn.pack_forget()  # Hidden initially

        # Title label
        self._nav_title = Native.Label(
            self._navbar,
            text="",
            font=("Segoe UI", 12, "bold"),
            bg=self.NavBarColor,
            fg="white"
        )
        self._nav_title.pack(side=LEFT, padx=10)

        # Content area
        self._content_container = Native.Frame(self._frame, bg=self.BackColor)
        self._content_container.pack(fill=BOTH, expand=True)

        # Page stack
        self._stack = []
        self._current = None

        # Push root page if provided
        if root_page_class:
            self.PushAsync(root_page_class)

    def PushAsync(self, page_class, *args, **kwargs):
        """Pushes a new page onto the navigation stack."""
        # Create page
        page = page_class(self._content_container, *args, **kwargs)

        # Hide current
        if self._current:
            self._current._frame.pack_forget()

        # Show new page
        page._frame.pack(fill=BOTH, expand=True)

        # Update stack
        self._stack.append(page)
        self._current = page

        # Update navbar
        self._update_navbar()

        return page

    def PopAsync(self):
        """Pops the current page from the stack."""
        if len(self._stack) > 1:
            # Remove current
            page = self._stack.pop()
            Native.Destroy(page._frame)

            # Show previous
            self._current = self._stack[-1]
            self._current._frame.pack(fill=BOTH, expand=True)

            # Update navbar
            self._update_navbar()

    def _go_back(self):
        """Internal back button handler."""
        self.PopAsync()

    def _update_navbar(self):
        """Updates the navigation bar state."""
        if self._current:
            self._nav_title.configure(text=getattr(self._current, 'Title', ''))

        # Show/hide back button
        if len(self._stack) > 1:
            self._back_btn.pack(side=LEFT, padx=10)
        else:
            self._back_btn.pack_forget()

class TabbedPage:
    """
    Multi-tab container page with switchable content sections.

    TabbedPage organizes content into multiple tabs, allowing users to switch
    between different views within the same page. Supports lazy loading of
    tab content and customizable tab positioning.

    Properties:
        Title (str): Page title for the tabbed container.
        TabPosition (str): Tab bar position - 'top' or 'bottom' (default: 'top').
        BackColor (str): Background color of the page.
        TabBarColor (str): Background color of the tab bar.
        SelectedColor (str): Color for the selected tab.
        UnselectedColor (str): Color for unselected tabs.

    Methods:
        AddTab(title, page_class, icon): Adds a new tab with the specified content.

    Example:
        >>> tabs = TabbedPage(master, props={'TabPosition': 'bottom'})
        >>> tabs.AddTab('Home', HomePage, '🏠')
        >>> tabs.AddTab('Settings', SettingsPage, '⚙️')
    """
    def __init__(self, master, props=None):
        # Default values - WinFormPy style
        defaults = {
            'Title': '',
            'TabPosition': 'top',
            'BackColor': '#FAFAFA',
            'TabBarColor': '#E0E0E0',
            'SelectedColor': '#512BD4',
            'UnselectedColor': '#666666'
        }

        # Apply props over defaults
        if props:
            defaults.update(props)

        self._master = master
        self.Title = defaults['Title']
        self.TabPosition = defaults['TabPosition']
        self.BackColor = defaults['BackColor']
        self.TabBarColor = defaults['TabBarColor']
        self.SelectedColor = defaults['SelectedColor']
        self.UnselectedColor = defaults['UnselectedColor']

        # Create main frame
        self._frame = Native.Frame(master, bg=self.BackColor)

        # Tab bar
        self._tab_bar = Native.Frame(self._frame, bg=self.TabBarColor)

        # Content area
        self._content_area = Native.Frame(self._frame, bg=self.BackColor)

        # Pack based on position
        if self.TabPosition == "bottom":
            self._content_area.pack(fill=BOTH, expand=True)
            self._tab_bar.pack(fill=X, side=BOTTOM)
        else:
            self._tab_bar.pack(fill=X, side=TOP)
            self._content_area.pack(fill=BOTH, expand=True)

        # Tabs data
        self._tabs = []
        self._current_index = -1

    def AddTab(self, title, page_class, icon=""):
        """Adds a new tab."""
        index = len(self._tabs)

        # Create tab button
        display_text = f"{icon} {title}" if icon else title
        btn = Native.Button(
            self._tab_bar,
            text=display_text,
            font=("Segoe UI", 10),
            bg=self.TabBarColor,
            fg=self.UnselectedColor,
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=lambda: self._select_tab(index)
        )
        btn.pack(side=LEFT)

        # Create page instance (lazy - only when selected)
        self._tabs.append({
            'title': title,
            'button': btn,
            'page_class': page_class,
            'page': None
        })

        # Select first tab automatically
        if len(self._tabs) == 1:
            self._select_tab(0)

    def _select_tab(self, index):
        """Selects a tab by index."""
        if index == self._current_index:
            return

        # Update button styles
        for i, tab in enumerate(self._tabs):
            if i == index:
                tab['button'].configure(bg=self.SelectedColor, fg="white")
            else:
                tab['button'].configure(bg=self.TabBarColor, fg=self.UnselectedColor)

        # Hide current page
        if self._current_index >= 0 and self._tabs[self._current_index]['page']:
            self._tabs[self._current_index]['page']._frame.pack_forget()

        # Create page if needed
        tab = self._tabs[index]
        if tab['page'] is None:
            tab['page'] = tab['page_class'](self._content_area)

        # Show page
        tab['page']._frame.pack(fill=BOTH, expand=True)
        self._current_index = index


# =============================================================================
# LAYOUT CLASSES
# =============================================================================

class VerticalStackLayout(StackLayout):
    """
    Layout container that arranges child elements in a vertical stack.

    VerticalStackLayout positions child controls one below another with
    configurable spacing and padding. Ideal for forms, lists, and any
    UI requiring vertical arrangement of elements.

    Inherits from StackLayout with Orientation='Vertical'.

    Properties:
        Spacing (int): Vertical space between child elements in pixels (default: 4).
        Padding (tuple): Container padding as (left, top, right, bottom) (default: 20,20,20,20).
        BackColor (str): Background color of the layout container.

    Methods:
        AddChild(widget_class, **kwargs): Adds a child widget to the layout.

    Example:
        >>> layout = VerticalStackLayout(page.Content, props={'Spacing': 15})
        >>> layout.AddChild(Label, text='Name:')
        >>> layout.AddChild(Entry, placeholder='Enter name')
    """
    def __init__(self, master, props=None):
        if props is None:
            props = {}
        props.setdefault('Orientation', 'Vertical')
        props.setdefault('Spacing', 4)
        props.setdefault('Padding', (20, 20, 20, 20))
        super().__init__(master, props=props)


class StackPanel(VerticalStackLayout):
    """
    XAML-style StackPanel (alias for VerticalStackLayout).
    Arranges child elements in a single line that can be oriented horizontally or vertically.
    Inherits from VerticalStackLayout → StackLayout → Layout.
    """
    def __init__(self, master, props=None, **kwargs):
        # Default XAML Margin="20" Spacing="4"
        xaml_props = {'Spacing': 4, 'Padding': (20, 20, 20, 20)}
        if props:
            xaml_props.update(props)
        super().__init__(master, props=xaml_props)


class HorizontalStackLayout(StackLayout):
    """
    Layout container that arranges child elements in a horizontal row.

    HorizontalStackLayout positions child controls side by side with
    configurable spacing. Perfect for button groups, toolbars, and
    horizontal arrangements of related controls.

    Inherits from StackLayout with Orientation='Horizontal'.

    Properties:
        Spacing (int): Horizontal space between child elements in pixels (default: 10).
        Padding (tuple): Container padding as (left, top, right, bottom) (default: 20,10,20,10).
        BackColor (str): Background color of the layout container.

    Methods:
        AddChild(widget_class, **kwargs): Adds a child widget to the layout.

    Example:
        >>> row = HorizontalStackLayout(container)
        >>> row.AddChild(Button, text='Save')
        >>> row.AddChild(Button, text='Cancel')
    """
    def __init__(self, master, props=None):
        if props is None:
            props = {}
        props.setdefault('Orientation', 'Horizontal')
        props.setdefault('Spacing', 10)
        props.setdefault('Padding', (20, 10, 20, 10))
        super().__init__(master, props=props)


class Grid:
    """
    Flexible grid-based layout for arranging widgets in rows and columns.

    Grid provides a powerful two-dimensional layout system where child
    elements can be positioned at specific row/column coordinates with
    optional spanning across multiple cells.

    Properties:
        Rows (int): Number of rows in the grid.
        Columns (int): Number of columns in the grid.
        RowSpacing (int): Vertical space between rows in pixels (default: 10).
        ColumnSpacing (int): Horizontal space between columns in pixels (default: 10).
        Padding (tuple): Grid padding as (left, top, right, bottom).
        BackColor (str): Background color of the grid container.

    Methods:
        AddChild(widget_class, row, column, rowspan=1, columnspan=1, **kwargs):
            Adds a widget at the specified grid position.

    Example:
        >>> grid = Grid(container, rows=2, columns=2)
        >>> grid.AddChild(Label, row=0, column=0, text='Name:')
        >>> grid.AddChild(Entry, row=0, column=1)
        >>> grid.AddChild(Button, row=1, column=0, columnspan=2, text='Submit')
    """
    def __init__(self, master, rows=1, columns=1, props=None):
        # Default values - WinFormPy style
        defaults = {
            'Rows': rows,
            'Columns': columns,
            'RowSpacing': 10,
            'ColumnSpacing': 10,
            'Padding': (20, 20, 20, 20),
            'BackColor': None
        }

        # Apply props over defaults
        if props:
            defaults.update(props)

        self._master = master
        self.Rows = defaults['Rows']
        self.Columns = defaults['Columns']
        self.RowSpacing = defaults['RowSpacing']
        self.ColumnSpacing = defaults['ColumnSpacing']
        self.Padding = defaults['Padding']
        self.BackColor = defaults['BackColor']

        # Determine parent frame
        if hasattr(master, '_content'):
            parent = master._content
        elif hasattr(master, '_frame'):
            parent = master._frame
        else:
            parent = master

        bg = self.BackColor if self.BackColor else parent.cget("bg")
        self._frame = Native.Frame(parent, bg=bg)
        self._frame.pack(fill=BOTH, expand=True,
                        padx=(self.Padding[0], self.Padding[2]),
                        pady=(self.Padding[1], self.Padding[3]))

        # Configure grid weights
        for i in range(self.Columns):
            self._frame.columnconfigure(i, weight=1)
        for i in range(self.Rows):
            self._frame.rowconfigure(i, weight=1)

    def AddChild(self, widget_class, row, column, rowspan=1, columnspan=1, sticky="nsew", **kwargs):
        """Adds a widget at the specified grid position."""
        widget = widget_class(self._frame, use_grid=True, **kwargs)

        # Determine which widget to actually grid (the container if it exists, otherwise the tk_widget)
        # Using getattr to be safe across different control implementations
        target = getattr(widget, '_container', None) or (widget.GetTkWidget() if hasattr(widget, 'GetTkWidget') else widget._tk_widget)

        target.grid(
            row=row, column=column,
            rowspan=rowspan, columnspan=columnspan,
            padx=self.ColumnSpacing // 2,
            pady=self.RowSpacing // 2,
            sticky=sticky
        )
        return widget

    def AddChildLayout(self, layout_class, row, column, rowspan=1, columnspan=1, sticky="nsew", **kwargs):
        """Adds a layout container (HorizontalStackLayout, etc.) at a grid position.

        Unlike AddChild which creates winformpy controls, this creates a mauipy
        layout container and places its _frame in the specified grid cell.

        Args:
            layout_class: The layout class (e.g., HorizontalStackLayout).
            row (int): Grid row position.
            column (int): Grid column position.
            rowspan (int): Number of rows to span (default: 1).
            columnspan (int): Number of columns to span (default: 1).
            sticky (str): Tkinter sticky directions (default: 'nsew').
            **kwargs: Passed as props to the layout constructor.

        Returns:
            The newly created layout instance.
        """
        # Create a transparent parent frame for the layout
        cell_frame = Native.Frame(self._frame, bg=self._frame.cget('bg'))
        cell_frame.grid(
            row=row, column=column,
            rowspan=rowspan, columnspan=columnspan,
            padx=self.ColumnSpacing // 2,
            pady=self.RowSpacing // 2,
            sticky=sticky
        )
        layout = layout_class(cell_frame, props=kwargs if kwargs else None)
        return layout


# =============================================================================
# BASIC DISPLAY & INPUT CONTROLS
# =============================================================================

def _bind_standard_mouse_events(widget, owner):
    """Bind standard mouse events (Click, DoubleClick, MouseDown/Up/Move/Enter/Leave) to the owner's event handlers."""
    widget.bind("<Button-1>", lambda e: owner.Click(owner, EventArgs(e)))
    widget.bind("<Double-Button-1>", lambda e: owner.DoubleClick(owner, EventArgs(e)))
    widget.bind("<ButtonPress>", lambda e: owner.MouseDown(owner, EventArgs(e)))
    widget.bind("<ButtonRelease>", lambda e: owner.MouseUp(owner, EventArgs(e)))
    widget.bind("<Motion>", lambda e: owner.MouseMove(owner, EventArgs(e)))
    widget.bind("<Enter>", lambda e: owner.MouseEnter(owner, EventArgs(e)))
    widget.bind("<Leave>", lambda e: owner.MouseLeave(owner, EventArgs(e)))


class Label(View):
    """
    Text display control with automatic sizing and styling.

    Label displays read-only text content with customizable font, color,
    and alignment. Supports text wrapping for multi-line content.

    Inherits from View (Microsoft.Maui.Controls.Label).

    Properties:
        Text (str): The text content displayed by the label.
        Font (tuple): Font specification as (family, size, style).
        ForeColor (str): Text color in hex format (e.g., '#333333').

    Args:
        master: Parent container (Page, Layout, or Frame).
        text (str): Initial text content.
        font (tuple): Font specification (default: 'Segoe UI', 11).
        fg (str): Text foreground color.
        anchor (str): Text alignment ('w', 'center', 'e').
        wraplength (int): Maximum line width before wrapping (0 = no wrap).

    Example:
        >>> Label(container, text='Hello World', fg='#0078D4')
    """
    def __init__(self, master, text="", side=TOP, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        defaults = {
            'Text': text,
            'Font': (DEFAULT_FONT_TEXT, 11),
            'ForeColor': '#333333',
            'BackColor': None,
            'Anchor': 'w',
            'WrapLength': 0
        }
        if props:
            defaults.update(props)
        if 'font' in kwargs:
            defaults['Font'] = kwargs['font']
        if 'fg' in kwargs:
            defaults['ForeColor'] = kwargs['fg']
        if 'bg' in kwargs:
            defaults['BackColor'] = kwargs['bg']
        if 'anchor' in kwargs:
            defaults['Anchor'] = kwargs['anchor']
        if 'wraplength' in kwargs:
            defaults['WrapLength'] = kwargs['wraplength']

        bg_color = defaults['BackColor'] if defaults['BackColor'] else self._get_parent_bg()

        self._tk_widget = Native.Label(
            self._parent,
            text=defaults['Text'],
            font=defaults['Font'],
            fg=defaults['ForeColor'],
            bg=bg_color,
            anchor=defaults['Anchor'],
            wraplength=defaults['WrapLength']
        )

        if not use_grid:
            self._tk_widget.pack(side=side, anchor="w", fill=X)

        self._bind_standard_events()

    @property
    def Text(self):
        return self._tk_widget.cget("text")

    @Text.setter
    def Text(self, value):
        self._tk_widget.configure(text=value)

    @property
    def Font(self):
        return self._tk_widget.cget("font")

    @Font.setter
    def Font(self, value):
        self._tk_widget.configure(font=value)

    @property
    def ForeColor(self):
        return self._tk_widget.cget("fg")

    @ForeColor.setter
    def ForeColor(self, value):
        self._tk_widget.configure(fg=value)


class TextBlock(Label):
    """
    WinUI3-style TextBlock for displaying read-only text.

    TextBlock is a lightweight control for displaying read-only text.
    It provides a WinUI-aligned naming for general text display.
    """
    def __init__(self, master, text="", **kwargs):
        # Apply BodyStrongTextBlockStyle defaults from XAML
        if 'font' not in kwargs:
            # Default to "Strong" style (bold) as seen in the provided XAML
            kwargs['font'] = (DEFAULT_FONT_TEXT, 10, "bold")

        super().__init__(master, text=text, **kwargs)

        # Apply XAML Margin (0,0,0,8) -> bottom padding 8
        if hasattr(self, '_tk_widget'):
            self._tk_widget.pack_configure(pady=(0, 8))


class Button(View):
    """
    Interactive button control with modern styling and hover effects.

    Button provides a clickable control with customizable appearance,
    including background color, text, and hover state transitions.
    Follows Material Design principles for visual feedback.

    Inherits from View (Microsoft.Maui.Controls.Button).

    Properties:
        Text (str): The button label text.
        Click (callable): Event handler called when button is clicked.

    Args:
        master: Parent container (Page, Layout, or Frame).
        text (str): Button label text.
        bg (str): Background color (default: '#512BD4' - MAUI purple).
        fg (str): Text color (default: 'white').
        hover_bg (str): Background color on hover.
        padx (int): Horizontal padding inside the button.
        pady (int): Vertical padding inside the button.

    Example:
        >>> btn = Button(container, text='Click Me', bg='#2196F3')
        >>> btn.Click = lambda: print('Clicked!')
    """
    def __init__(self, master, text="", side=TOP, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        # Button-specific events (in addition to View's standard events)
        self.GotFocus = lambda sender, e: None
        self.LostFocus = lambda sender, e: None

        defaults = {
            'Text': text,
            'Font': (DEFAULT_FONT_TEXT, 10, "bold"),
            'BackColor': '#512BD4',
            'ForeColor': 'white',
            'HoverColor': '#6B3FA0',
            'ActiveBackColor': '#6B3FA0',
            'PaddingX': 20,
            'PaddingY': 10,
            'Width': None,
            'Anchor': 'w'
        }
        if props:
            defaults.update(props)
        if 'font' in kwargs:
            defaults['Font'] = kwargs['font']
        if 'bg' in kwargs:
            defaults['BackColor'] = kwargs['bg']
        if 'fg' in kwargs:
            defaults['ForeColor'] = kwargs['fg']
        if 'hover_bg' in kwargs:
            defaults['HoverColor'] = kwargs['hover_bg']
        if 'activebackground' in kwargs:
            defaults['ActiveBackColor'] = kwargs['activebackground']
        if 'padx' in kwargs:
            defaults['PaddingX'] = kwargs['padx']
        if 'pady' in kwargs:
            defaults['PaddingY'] = kwargs['pady']
        if 'width' in kwargs:
            defaults['Width'] = kwargs['width']
        if 'anchor' in kwargs:
            defaults['Anchor'] = kwargs['anchor']

        self._tk_widget = Native.Button(
            self._parent,
            text=defaults['Text'],
            font=defaults['Font'],
            bg=defaults['BackColor'],
            fg=defaults['ForeColor'],
            bd=0,
            padx=defaults['PaddingX'],
            pady=defaults['PaddingY'],
            activebackground=defaults['ActiveBackColor'],
            activeforeground=defaults['ForeColor'],
            cursor="hand2"
        )

        if not use_grid:
            if defaults['Width']:
                self._tk_widget.configure(width=defaults['Width'] // 10)  # Approximate char width
            self._tk_widget.pack(side=side, anchor=defaults['Anchor'])

        # Hover effects
        self._bg = defaults['BackColor']
        self._hover_bg = defaults['HoverColor']

        # Bind events: standard mouse + custom handlers for hover/click/focus
        self._bind_standard_events()
        self._tk_widget.bind("<Button-1>", self._on_click)
        self._tk_widget.bind("<Enter>", self._on_mouse_enter)
        self._tk_widget.bind("<Leave>", self._on_mouse_leave)
        self._tk_widget.bind("<FocusIn>", lambda e: self.GotFocus(self, EventArgs(e)))
        self._tk_widget.bind("<FocusOut>", lambda e: self.LostFocus(self, EventArgs(e)))

    def _on_click(self, event):
        self.Click(self, EventArgs(event))

    def _on_mouse_enter(self, event):
        self._tk_widget.configure(bg=self._hover_bg)
        self.MouseEnter(self, EventArgs(event))

    def _on_mouse_leave(self, event):
        self._tk_widget.configure(bg=self._bg)
        self.MouseLeave(self, EventArgs(event))

    @property
    def Text(self):
        return self._tk_widget.cget("text")

    @Text.setter
    def Text(self, value):
        self._tk_widget.configure(text=value)


class Entry(View):
    """
    Single-line text input control with placeholder support.

    Entry provides a text input field for user data entry with optional
    placeholder text that disappears on focus. Suitable for forms,
    search boxes, and any single-line text input needs.

    Inherits from View (Microsoft.Maui.Controls.Entry).

    Properties:
        Text (str): The current text content of the entry field.

    Args:
        master: Parent container (Page, Layout, or Frame).
        placeholder (str): Hint text shown when the field is empty.
        font (tuple): Font specification for the input text.
        fg (str): Text foreground color.
        bg (str): Background color.
        width (int): Field width in pixels.

    Example:
        >>> email = Entry(form, placeholder='Enter your email')
        >>> print(email.Text)  # Get entered text
    """
    def __init__(self, master, placeholder="", side=TOP, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        # Entry-specific events
        self.TextChanged = lambda sender, e: None
        self.GotFocus = lambda sender, e: None
        self.LostFocus = lambda sender, e: None
        self.KeyDown = lambda sender, e: None
        self.KeyUp = lambda sender, e: None

        defaults = {
            'Placeholder': placeholder,
            'Font': (DEFAULT_FONT_TEXT, 11),
            'ForeColor': '#333333',
            'BackColor': 'white',
            'Width': 300,
            'Fill': False,
            'IsPassword': False,  # Mask text input
            'PasswordChar': '●'   # Mask character (fluent style bullet)
        }
        if props:
            defaults.update(props)
        if 'font' in kwargs:
            defaults['Font'] = kwargs['font']
        if 'fg' in kwargs:
            defaults['ForeColor'] = kwargs['fg']
        if 'bg' in kwargs:
            defaults['BackColor'] = kwargs['bg']
        if 'width' in kwargs:
            defaults['Width'] = kwargs['width']
        if 'fill' in kwargs:
            defaults['Fill'] = kwargs['fill']
        if 'is_password' in kwargs:
            defaults['IsPassword'] = kwargs['is_password']

        self._placeholder = defaults['Placeholder']
        self._is_password = defaults['IsPassword']
        self._password_char = defaults['PasswordChar']

        # Create container frame for border styling (WinUI look)
        self._container = Native.Frame(self._parent, bg="#E5E5E5", padx=1, pady=1)

        # TK char width is roughly 1/8 of pixel width for standard font
        tk_width = defaults['Width'] // 8 if defaults['Width'] > 40 else defaults['Width']

        # Create entry
        self._tk_widget = Native.Entry(
            self._container,
            font=defaults['Font'],
            fg=defaults['ForeColor'],
            bg=defaults['BackColor'],
            bd=0,
            width=tk_width, # Use the calculated char width
            insertbackground=defaults['ForeColor']
        )

        self._tk_widget.pack(fill=BOTH, expand=True)

        if not use_grid:
            fill = X if defaults['Fill'] else None
            self._container.pack(side=side, anchor="w", fill=fill)

        # Apply password mask if not showing placeholder
        if self._is_password and not placeholder:
            self._tk_widget.configure(show=self._password_char)

        # Bind events: standard mouse + custom key/focus handlers
        self._bind_standard_events()
        self._tk_widget.bind("<KeyRelease>", self._on_text_changed)
        self._tk_widget.bind("<KeyPress>", lambda e: self.KeyDown(self, EventArgs(e)))
        self._tk_widget.bind("<KeyRelease>", lambda e: self.KeyUp(self, EventArgs(e)), add='+')

        # Placeholder handling
        if placeholder:
            self._show_placeholder()
            self._tk_widget.bind("<FocusIn>", self._on_focus_in)
            self._tk_widget.bind("<FocusOut>", self._on_focus_out)
        else:
            self._tk_widget.bind("<FocusIn>", lambda e: self.GotFocus(self, EventArgs(e)))
            self._tk_widget.bind("<FocusOut>", lambda e: self.LostFocus(self, EventArgs(e)))

    def _on_focus_in(self, event):
        if self._tk_widget.get() == self._placeholder:
            self._tk_widget.delete(0, END)
            self._tk_widget.configure(fg="#333333")
            if self._is_password:
                self._tk_widget.configure(show=self._password_char)
        self.GotFocus(self, EventArgs(event))

    def _on_focus_out(self, event):
        if not self._tk_widget.get():
            self._show_placeholder()
        self.LostFocus(self, EventArgs(event))

    def _on_text_changed(self, event):
        """Handles text change events."""
        text = self._tk_widget.get()
        if text != self._placeholder:
            self.TextChanged(self, EventArgs(event))

    @property
    def Text(self):
        """Gets or sets the current text."""
        text = self._tk_widget.get()
        if text == self._placeholder:
            return ""
        return text

    @Text.setter
    def Text(self, value):
        self._tk_widget.delete(0, END)
        if value:
            self._tk_widget.configure(fg="#333333")
            if self._is_password:
                self._tk_widget.configure(show=self._password_char)
            self._tk_widget.insert(0, value)
        else:
            self._show_placeholder()

    def _show_placeholder(self):
        """Shows the placeholder text."""
        if self._is_password:
            self._tk_widget.configure(show="")
        self._tk_widget.delete(0, END)
        self._tk_widget.insert(0, self._placeholder)
        self._tk_widget.configure(fg="#999999")


class Image(View):
    """
    Image display control supporting various image formats.

    Image displays bitmap images from files with automatic format detection.
    Supports GIF, PNG, JPG (with Pillow), and native Tkinter formats.

    Inherits from View (Microsoft.Maui.Controls.Image).

    Methods:
        Load(source): Loads an image from the specified file path.

    Args:
        master: Parent container (Page, Layout, or Frame).
        source (str): Path to the image file to display.

    Note:
        For JPG/PNG support, the Pillow library must be installed.
        Without Pillow, only GIF, PGM, and PPM formats are supported.

    Example:
        >>> img = Image(container, source='logo.png')
        >>> img.Load('new_image.jpg')  # Load different image
    """
    def __init__(self, master, source=None, side=TOP, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        defaults = {
            'Source': source,
            'BackColor': None
        }
        if props:
            defaults.update(props)

        self._image = None
        self._click_command = None

        bg_color = defaults['BackColor'] if defaults['BackColor'] else self._get_parent_bg()
        self._tk_widget = Native.Label(self._parent, bg=bg_color)

        if not use_grid:
            self._tk_widget.pack(side=side)

        self._bind_standard_events()

        if defaults['Source']:
            self.Load(defaults['Source'])

    def Load(self, source):
        """Loads an image from file."""
        # Try to use Pillow with lazy install
        if install_library("Pillow", "PIL"):
            try:
                from PIL import Image as PILImage, ImageTk
                img = PILImage.open(source)
                self._image = ImageTk.PhotoImage(img)
                self._tk_widget.configure(image=self._image)
                return
            except Exception:
                pass

        # Fallback for GIF/PGM/PPM without Pillow
        try:
            self._image = Native.PhotoImage(file=source)
            self._tk_widget.configure(image=self._image)
        except Exception:
            self._tk_widget.configure(text=f"[Image: {source}]")

# =============================================================================
# NAVIGATION & INTERACTIVE COMPONENTS
# =============================================================================

class FlyoutMenu:
    """
    Standalone flyout menu component for custom navigation implementations.

    FlyoutMenu provides a vertical list of clickable menu items with icons
    and hover effects. Can be used independently of Shell for custom
    navigation patterns or contextual menus.

    Methods:
        AddItem(text, command, icon): Adds a clickable menu item.

    Args:
        master: Parent container for the flyout menu.

    Example:
        >>> menu = FlyoutMenu(sidebar)
        >>> menu.AddItem('Dashboard', show_dashboard, '📊')
        >>> menu.AddItem('Settings', show_settings, '⚙️')
    """
    def __init__(self, master, props=None):
        # Default values - WinFormPy style
        defaults = {
            'BackColor': '#F0F0F0',
            'ForeColor': '#333333',
            'HoverColor': '#E0E0E0',
            'Font': ('Segoe UI', 11)
        }

        # Apply props over defaults
        if props:
            defaults.update(props)

        self._master = master
        self._items = []
        self._back_color = defaults['BackColor']
        self._fore_color = defaults['ForeColor']
        self._hover_color = defaults['HoverColor']
        self._font = defaults['Font']

        if hasattr(master, '_frame'):
            parent = master._frame
        else:
            parent = master

        self._frame = Native.Frame(parent, bg=self._back_color)
        self._frame.pack(fill=BOTH, expand=True)

    def AddItem(self, text, command=None, icon=""):
        """Adds a menu item."""
        display_text = f"{icon}  {text}" if icon else text

        btn = Native.Button(
            self._frame,
            text=display_text,
            font=self._font,
            bg=self._back_color,
            fg=self._fore_color,
            bd=0,
            anchor="w",
            padx=20,
            pady=12,
            cursor="hand2"
        )
        btn.pack(fill=X)

        if command:
            btn.configure(command=command)

        hover_color = self._hover_color
        back_color = self._back_color
        btn.bind("<Enter>", lambda e: btn.configure(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.configure(bg=back_color))

        self._items.append(btn)
        return btn


class CarouselView(View):
    """
    Swipeable carousel control for browsing through a collection of items.

    CarouselView displays one item at a time with navigation controls to
    move between items. Includes previous/next buttons and a position
    indicator showing the current item number.

    Inherits from View (Microsoft.Maui.Controls.CarouselView).

    Methods:
        SetItems(items): Sets the collection of items to display.

    Args:
        master: Parent container for the carousel.

    Example:
        >>> carousel = CarouselView(container)
        >>> carousel.SetItems(['Slide 1', 'Slide 2', 'Slide 3'])
    """
    def __init__(self, master, side=TOP, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        # Override parent resolution: CarouselView supports ContentPage directly
        if hasattr(master, '_content'):
            self._parent = master._content

        defaults = {
            'BackColor': None,
            'NavButtonFont': ('Segoe UI', 12),
            'IndicatorFont': ('Segoe UI', 10),
            'ContentFont': ('Segoe UI', 16)
        }
        if props:
            defaults.update(props)

        self._items = []
        self._current_index = 0
        self._content_font = defaults['ContentFont']

        # CarouselView-specific event
        self.PositionChanged = lambda sender, e: None

        bg_color = defaults['BackColor'] if defaults['BackColor'] else self._get_parent_bg()

        self._frame = Native.Frame(self._parent, bg=bg_color, **kwargs)
        self._tk_widget = self._frame # Alias for consistency

        if not use_grid:
            self._frame.pack(side=side, fill=BOTH, expand=True)

        # Content area
        self._content = Native.Frame(self._frame, bg=bg_color)
        self._content.pack(fill=BOTH, expand=True)

        # Navigation
        self._nav = Native.Frame(self._frame, bg=bg_color)
        self._nav.pack(fill=X, pady=10)

        self._prev_btn = Native.Button(self._nav, text="◀", command=self._prev, font=defaults['NavButtonFont'])
        self._prev_btn.pack(side=LEFT, padx=20)

        self._indicator = Native.Label(self._nav, text="0 / 0", font=defaults['IndicatorFont'], bg=bg_color)
        self._indicator.pack(side=LEFT, expand=True)

        self._next_btn = Native.Button(self._nav, text="▶", command=self._next, font=defaults['NavButtonFont'])
        self._next_btn.pack(side=RIGHT, padx=20)

    def SetItems(self, items):
        """Sets the carousel items."""
        self._items = items
        self._current_index = 0
        self._update_view()

    def _update_view(self):
        """Updates the current view."""
        # Clear content
        for child in Native.GetChildren(self._content):
            Native.Destroy(child)

        if not self._items:
            self._indicator.configure(text="0 / 0")
            return

        # Show current item
        item = self._items[self._current_index]
        lbl = Native.Label(
            self._content,
            text=str(item),
            font=("Segoe UI", 16),
            bg=self._content.cget("bg")
        )
        lbl.pack(expand=True)

        # Update indicator
        self._indicator.configure(text=f"{self._current_index + 1} / {len(self._items)}")

    def _prev(self):
        if self._current_index > 0:
            self._current_index -= 1
            self._update_view()
            self.PositionChanged(self, EventArgs())

    def _next(self):
        if self._current_index < len(self._items) - 1:
            self._current_index += 1
            self._update_view()
            self.PositionChanged(self, EventArgs())


class ToastNotification:
    """
    Temporary popup notification for displaying brief messages to users.

    ToastNotification displays a non-intrusive message at the bottom of
    the window that automatically disappears after a specified duration.
    Commonly used for confirmations, status updates, and non-critical alerts.

    Methods:
        Show(master, message, duration): Displays a toast notification.

    Args:
        master: Parent window or Shell instance.
        message (str): Text message to display.
        duration (int): Display duration in milliseconds (default: 2000).

    Example:
        >>> ToastNotification.Show(app, 'Settings saved successfully!', 3000)
    """
    @staticmethod
    def Show(master, message, duration=2000):
        """Shows a toast notification."""
        try:
            # Use centralized WinFormPy utility to resolve the root window
            root = get_tk_root(master)
            if not root:
                return

            # Create toast
            toast = Native.Toplevel(root)
            Native.Overrideredirect(toast, True)

            # Style
            frame = Native.Frame(toast, bg="#333333", padx=20, pady=10)
            frame.pack()

            label = Native.Label(
                frame,
                text=message,
                font=("Segoe UI", 10),
                bg="#333333",
                fg="white"
            )
            label.pack()

            # Position at bottom center
            Native.Update(toast)
            tw, th = Native.GetSize(toast)

            Native.Update(root)
            rx, ry = Native.GetPosition(root)
            rw, rh = Native.GetSize(root)

            x = rx + (rw - tw) // 2
            y = ry + rh - th - 50

            Native.Geometry(toast, f"+{x}+{y}")

            # Auto-close
            Native.Wait(toast, duration, lambda: Native.Destroy(toast) if Native.Exists(toast) else None)
        except (Native.TclError, RuntimeError):
            # Application or widget destroyed during setup
            pass


class SearchBar(View):
    """
    Search input control with integrated search button and placeholder text.

    SearchBar provides a text input field specifically designed for search
    functionality, including a search button and Enter key binding for
    triggering searches.

    Inherits from View (Microsoft.Maui.Controls.SearchBar).

    Properties:
        Text (str): Current search query text.
        SearchCommand (callable): Event handler called when search is triggered.

    Args:
        master: Parent container for the search bar.
        placeholder (str): Hint text shown in empty field (default: 'Search...').

    Example:
        >>> search = SearchBar(header, placeholder='Search products...')
        >>> search.SearchCommand = lambda query: filter_results(query)
    """
    def __init__(self, master, placeholder="Search...", side=TOP, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        # Override parent resolution: SearchBar supports ContentPage directly
        if hasattr(master, '_content'):
            self._parent = master._content

        defaults = {
            'Placeholder': placeholder,
            'Font': ('Segoe UI', 11),
            'ButtonFont': ('Segoe UI', 10),
            'ButtonText': '🔍',
            'ForeColor': '#333333',
            'PlaceholderColor': '#999999',
            'PaddingX': 20,
            'PaddingY': 10
        }
        if props:
            defaults.update(props)

        # SearchBar-specific event
        self.Search = lambda sender, e: None
        self._placeholder = defaults['Placeholder']
        self._fg_color = defaults['ForeColor']
        self._placeholder_color = defaults['PlaceholderColor']

        self._frame = Native.Frame(self._parent, bg=self._get_parent_bg(), **kwargs)
        self._tk_widget = self._frame # Alias for consistency

        if not use_grid:
            self._frame.pack(side=side, fill=X, padx=defaults['PaddingX'], pady=defaults['PaddingY'])

        # Search entry
        self._entry = Native.Entry(
            self._frame,
            font=defaults['Font'],
            bd=1,
            relief=SOLID
        )
        self._entry.pack(side=LEFT, fill=X, expand=True)
        self._entry.insert(0, self._placeholder)
        self._entry.configure(fg=self._placeholder_color)

        # Placeholder handling
        self._entry.bind("<FocusIn>", self._on_focus_in)
        self._entry.bind("<FocusOut>", self._on_focus_out)
        self._entry.bind("<Return>", lambda e: self._on_search())

        # Search button
        self._btn = Native.Button(
            self._frame,
            text=defaults['ButtonText'],
            font=defaults['ButtonFont'],
            bd=1,
            command=self._on_search
        )
        self._btn.pack(side=RIGHT, padx=(5, 0))

    def _on_focus_in(self, event):
        if self._entry.get() == self._placeholder:
            self._entry.delete(0, END)
            self._entry.configure(fg=self._fg_color)

    def _on_focus_out(self, event):
        if not self._entry.get():
            self._entry.insert(0, self._placeholder)
            self._entry.configure(fg="#999999")

    def _on_search(self):
        text = self._entry.get()
        if text != self._placeholder:
            self.Search(self, EventArgs(text))

    @property
    def Text(self):
        text = self._entry.get()
        return "" if text == self._placeholder else text

    @Text.setter
    def Text(self, value):
        self._entry.delete(0, END)
        if value:
            self._entry.configure(fg="#333333")
            self._entry.insert(0, value)
        else:
            self._entry.insert(0, self._placeholder)
            self._entry.configure(fg="#999999")


class ChipTag(View):
    """
    Compact chip/tag control for displaying categorical information.

    ChipTag displays small, compact elements typically used for tags,
    categories, filters, or selections. Optionally includes a close
    button for removable chips.

    Inherits from View (Microsoft.Maui.Controls.ChipTag).

    Properties:
        Text (str): The text displayed in the chip.
        CloseCommand (callable): Event handler called when close button is clicked.

    Args:
        master: Parent container for the chip.
        text (str): Text content of the chip (default: 'Tag').
        closable (bool): Whether to show a close/remove button (default: False).

    Example:
        >>> chip = ChipTag(container, text='Python', closable=True)
        >>> chip.CloseCommand = lambda: remove_filter('Python')
    """
    def __init__(self, master, text="Tag", closable=False, side=LEFT, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        defaults = {
            'Text': text,
            'Closable': closable,
            'BackColor': '#E0E0E0',
            'ForeColor': '#333333',
            'CloseButtonColor': '#666666',
            'Font': ('Segoe UI', 9),
            'PaddingX': 8,
            'PaddingY': 4
        }
        if props:
            defaults.update(props)

        # ChipTag-specific event
        self.Close = lambda sender, e: None
        self._back_color = defaults['BackColor']
        self._fore_color = defaults['ForeColor']
        self._font = defaults['Font']

        self._frame = Native.Frame(self._parent, bg=self._back_color,
                              padx=defaults['PaddingX'], pady=defaults['PaddingY'], **kwargs)
        self._tk_widget = self._frame # Alias for consistency

        if not use_grid:
            self._frame.pack(side=side, padx=2, pady=2)

        # Text
        self._label = Native.Label(
            self._frame,
            text=defaults['Text'],
            font=self._font,
            bg=self._back_color,
            fg=self._fore_color
        )
        self._label.pack(side=LEFT)

        # Close button
        if defaults['Closable']:
            self._close_btn = Native.Button(
                self._frame,
                text="×",
                font=self._font,
                bg=self._back_color,
                fg=defaults['CloseButtonColor'],
                bd=0,
                padx=2,
                cursor="hand2",
                command=self._on_close
            )
            self._close_btn.pack(side=LEFT, padx=(5, 0))

    def _on_close(self):
        self.Close(self, EventArgs())
        Native.Destroy(self._frame)

    @property
    def Text(self):
        return self._label.cget("text")

    @Text.setter
    def Text(self, value):
        self._label.configure(text=value)


class Stepper(View):
    """
    Numeric input control with increment and decrement buttons.

    Stepper provides a user-friendly way to select numeric values within
    a defined range using plus/minus buttons. Ideal for quantity selectors,
    counters, and any numeric input requiring bounded values.

    Inherits from View (Microsoft.Maui.Controls.Stepper).

    Properties:
        Value (int/float): Current numeric value.
        ValueChanged (callable): Event handler called when value changes.

    Args:
        master: Parent container for the stepper.
        min_val (int): Minimum allowed value (default: 0).
        max_val (int): Maximum allowed value (default: 100).
        step (int): Increment/decrement step size (default: 1).
        value (int): Initial value (default: 0).

    Example:
        >>> qty = Stepper(cart, min_val=1, max_val=10, value=1)
        >>> qty.ValueChanged = lambda v: update_total(v)
    """
    def __init__(self, master, min_val=0, max_val=100, step=1, value=0, side=TOP, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        defaults = {
            'Minimum': min_val,
            'Maximum': max_val,
            'Step': step,
            'Value': value,
            'ButtonFont': ('Segoe UI', 12, 'bold'),
            'ValueFont': ('Segoe UI', 12),
            'ButtonWidth': 3,
            'ValueWidth': 5,
            'BackColor': None
        }
        if props:
            defaults.update(props)

        self._min = defaults['Minimum']
        self._max = defaults['Maximum']
        self._step = defaults['Step']
        self._value = defaults['Value']

        # Stepper-specific event
        self.ValueChanged = lambda sender, e: None

        bg_color = defaults['BackColor'] if defaults['BackColor'] else self._get_parent_bg()

        self._frame = Native.Frame(self._parent, bg=bg_color, **kwargs)
        self._tk_widget = self._frame # Alias for consistency

        if not use_grid:
            self._frame.pack(side=side, pady=5)

        # Minus button
        self._minus_btn = Native.Button(
            self._frame,
            text="-",
            font=defaults['ButtonFont'],
            width=defaults['ButtonWidth'],
            command=self._decrement
        )
        self._minus_btn.pack(side=LEFT)

        # Value label
        self._value_label = Native.Label(
            self._frame,
            text=str(self._value),
            font=defaults['ValueFont'],
            width=defaults['ValueWidth'],
            bg=bg_color
        )
        self._value_label.pack(side=LEFT, padx=10)

        # Plus button
        self._plus_btn = Native.Button(
            self._frame,
            text="+",
            font=defaults['ButtonFont'],
            width=defaults['ButtonWidth'],
            command=self._increment
        )
        self._plus_btn.pack(side=LEFT)

    def _increment(self):
        new_val = min(self._max, self._value + self._step)
        if new_val != self._value:
            self._value = new_val
            self._value_label.configure(text=str(self._value))
            self.ValueChanged(self, EventArgs(self._value))

    def _decrement(self):
        new_val = max(self._min, self._value - self._step)
        if new_val != self._value:
            self._value = new_val
            self._value_label.configure(text=str(self._value))
            self.ValueChanged(self, EventArgs(self._value))

    @property
    def Value(self):
        return self._value

    @Value.setter
    def Value(self, value):
        self._value = max(self._min, min(self._max, value))
        self._value_label.configure(text=str(self._value))


class PopUpFlyout:
    """
    Modal popup dialog for displaying content overlaying the main window.

    PopUpFlyout creates a floating panel that appears above other content,
    useful for confirmations, forms, or detailed information that requires
    user attention before continuing.

    Properties:
        Content (Frame): Container frame for adding popup content.

    Methods:
        Show(x, y): Displays the popup at specified coordinates (or centered).
        Hide(): Closes the popup.

    Args:
        master: Parent window or container.
        width (int): Popup width in pixels (default: 300).
        height (int): Popup height in pixels (default: 200).

    Example:
        >>> popup = PopUpFlyout(app, width=400, height=300)
        >>> Label(popup.Content, text='Confirm action?')
        >>> popup.Show()
    """
    def __init__(self, master, width=300, height=200, props=None):
        # Default values - WinFormPy style
        defaults = {
            'Width': width,
            'Height': height,
            'BackColor': 'white',
            'BorderWidth': 1
        }

        # Apply props over defaults
        if props:
            defaults.update(props)

        self._master = master
        self._width = defaults['Width']
        self._height = defaults['Height']

        # Resolve root window using centralized utility
        root = get_tk_root(master)

        self._popup = Native.Toplevel(root)
        Native.Withdraw(self._popup)
        Native.Overrideredirect(self._popup, True)
        Native.Geometry(self._popup, f"{self._width}x{self._height}")

        # Content frame
        self._frame = Native.Frame(self._popup, bg=defaults['BackColor'],
                              bd=defaults['BorderWidth'], relief=SOLID)
        self._frame.pack(fill=BOTH, expand=True)

        # Close on click outside
        self._popup.bind("<FocusOut>", lambda e: self.Hide())

    def Show(self, x=None, y=None):
        """Shows the popup at specified coordinates."""
        try:
            if x is None or y is None:
                # Center on parent
                root = self._popup.master
                Native.Update(root)
                rx, ry = Native.GetPosition(root)
                rw, rh = Native.GetSize(root)

                x = rx + (rw - self._width) // 2
                y = ry + (rh - self._height) // 2

            Native.Geometry(self._popup, f"+{x}+{y}")
            Native.Deiconify(self._popup)
            Native.Lift(self._popup)
            Native.Focus(self._popup)
        except (Native.TclError, RuntimeError):
            pass

    def Hide(self):
        """Hides the popup."""
        if Native.Exists(self._popup):
            Native.Withdraw(self._popup)

    @property
    def Content(self):
        """Returns the content frame."""
        return self._frame


############# Form Input Controls #############

# =============================================================================
# SWITCH - Toggle Control
# =============================================================================

class Switch(View):
    """
    Toggle switch control for binary on/off states.

    Switch provides a modern sliding toggle control similar to iOS/Android
    switches. Features smooth visual transitions between states with
    customizable on/off colors.

    Inherits from View (Microsoft.Maui.Controls.Switch).

    Properties:
        IsToggled (bool): Current toggle state (True = on, False = off).
        OnColor (str): Background color when toggled on (default: '#512BD4').
        Toggled (callable): Event handler called when toggle state changes.

    Args:
        master: Parent container for the switch.
        is_toggled (bool): Initial toggle state (default: False).
        props (dict): Additional properties including OnColor, OffColor.

    Example:
        >>> dark_mode = Switch(settings, is_toggled=False)
        >>> dark_mode.Toggled = lambda state: toggle_theme(state)
    """
    def __init__(self, master, is_toggled=False, side=TOP, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        defaults = {
            'IsToggled': is_toggled,
            'OnColor': '#0078D4',
            'OffColor': '#CCCCCC',
            'ThumbColor': 'white',
            'Width': 50,
            'Height': 26,
            'ThumbSize': 20,
            'Padding': 3
        }
        if props:
            defaults.update(props)

        self._is_toggled = defaults['IsToggled']

        # Switch-specific events (in addition to View's standard events)
        self.Toggled = lambda sender, e: None
        self.GotFocus = lambda sender, e: None
        self.LostFocus = lambda sender, e: None

        # Colors
        self._on_color = defaults['OnColor']
        self._off_color = defaults['OffColor']
        self._thumb_color = defaults['ThumbColor']

        # Dimensions
        self._width = defaults['Width']
        self._height = defaults['Height']
        self._thumb_size = defaults['ThumbSize']
        self._padding = defaults['Padding']

        # Create canvas for drawing
        self._canvas = Native.Canvas(
            self._parent,
            width=self._width,
            height=self._height,
            bg=self._get_parent_bg(),
            highlightthickness=0,
            cursor="hand2",
            **kwargs
        )
        self._tk_widget = self._canvas # Alias for consistency

        if not use_grid:
            self._canvas.pack(side=side, pady=5)

        # Draw initial state
        self._draw()

        # Bind events
        self._canvas.bind("<Button-1>", self._on_click)
        self._canvas.bind("<Double-Button-1>", lambda e: self.DoubleClick(self, e))
        self._canvas.bind("<Enter>", lambda e: self.MouseEnter(self, e))
        self._canvas.bind("<Leave>", lambda e: self.MouseLeave(self, e))
        self._canvas.bind("<FocusIn>", lambda e: self.GotFocus(self, e))
        self._canvas.bind("<FocusOut>", lambda e: self.LostFocus(self, e))

    def _draw(self):
        """Draws the switch."""
        self._canvas.delete("all")

        # Background track
        bg_color = self._on_color if self._is_toggled else self._off_color

        # Draw rounded rectangle for track
        r = self._height // 2
        self._canvas.create_oval(0, 0, self._height, self._height, fill=bg_color, outline=bg_color)
        self._canvas.create_oval(self._width - self._height, 0, self._width, self._height, fill=bg_color, outline=bg_color)
        self._canvas.create_rectangle(r, 0, self._width - r, self._height, fill=bg_color, outline=bg_color)

        # Draw thumb
        if self._is_toggled:
            thumb_x = self._width - self._thumb_size - self._padding
        else:
            thumb_x = self._padding

        thumb_y = self._padding
        self._canvas.create_oval(
            thumb_x, thumb_y,
            thumb_x + self._thumb_size, thumb_y + self._thumb_size,
            fill=self._thumb_color, outline=self._thumb_color
        )

    def _on_click(self, event):
        """Handles click to toggle."""
        self._is_toggled = not self._is_toggled
        self._draw()

        self.Toggled(self, EventArgs(event))
        self.Click(self, EventArgs(event))

    @property
    def IsToggled(self):
        return self._is_toggled

    @IsToggled.setter
    def IsToggled(self, value):
        self._is_toggled = value
        self._draw()

    @property
    def OnColor(self):
        return self._on_color

    @OnColor.setter
    def OnColor(self, value):
        self._on_color = value
        self._draw()


# =============================================================================
# CHECKBOX - Check Control
# =============================================================================

class CheckBox(View):
    """
    Checkbox control for boolean selection with accompanying label.

    CheckBox displays a toggleable checkbox with an optional text label.
    Supports custom colors and visual feedback on state changes.
    Commonly used in forms for options, agreements, and multi-select scenarios.

    Inherits from View (Microsoft.Maui.Controls.CheckBox).

    Properties:
        IsChecked (bool): Current checked state.
        Text (str): Label text displayed next to the checkbox.
        CheckedChanged (callable): Event handler called when state changes.

    Args:
        master: Parent container for the checkbox.
        text (str): Label text to display.
        is_checked (bool): Initial checked state (default: False).
        props (dict): Additional styling properties.

    Example:
        >>> agree = CheckBox(form, text='I agree to the terms', is_checked=False)
        >>> agree.CheckedChanged = lambda checked: enable_submit(checked)
    """
    def __init__(self, master, text="", is_checked=False, side=TOP, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        defaults = {
            'Text': text,
            'IsChecked': is_checked,
            'CheckColor': '#512BD4',
            'UncheckedColor': '#CCCCCC',
            'ForeColor': '#333333',
            'BoxSize': 20
        }
        if props:
            defaults.update(props)

        self._text = defaults['Text']
        self._is_checked = defaults['IsChecked']

        # CheckBox-specific events (in addition to View's standard events)
        self.CheckedChanged = lambda sender, e: None
        self.GotFocus = lambda sender, e: None
        self.LostFocus = lambda sender, e: None

        # Colors
        self._check_color = defaults['CheckColor']
        self._unchecked_color = defaults['UncheckedColor']
        self._fg_color = defaults['ForeColor']

        # Size
        self._box_size = defaults['BoxSize']

        self._bg = self._get_parent_bg()

        # Container frame
        self._frame = Native.Frame(self._parent, bg=self._bg, **kwargs)
        self._tk_widget = self._frame # Alias for consistency

        if not use_grid:
            self._frame.pack(side=side, anchor="w", pady=3)

        # Canvas for checkbox
        self._canvas = Native.Canvas(
            self._frame,
            width=self._box_size,
            height=self._box_size,
            bg=self._bg,
            highlightthickness=0,
            cursor="hand2"
        )
        self._canvas.pack(side=LEFT)

        # Label
        self._label = Native.Label(
            self._frame,
            text=self._text,
            font=("Segoe UI", 10),
            fg=self._fg_color,
            bg=self._bg,
            cursor="hand2"
        )
        self._label.pack(side=LEFT, padx=(8, 0))

        # Draw initial state
        self._draw()

        # Bind events
        self._canvas.bind("<Button-1>", self._on_click)
        self._label.bind("<Button-1>", self._on_click)
        self._canvas.bind("<Double-Button-1>", lambda e: self.DoubleClick(self, e))
        self._label.bind("<Double-Button-1>", lambda e: self.DoubleClick(self, e))
        self._canvas.bind("<Enter>", lambda e: self.MouseEnter(self, e))
        self._label.bind("<Enter>", lambda e: self.MouseEnter(self, e))
        self._canvas.bind("<Leave>", lambda e: self.MouseLeave(self, e))
        self._label.bind("<Leave>", lambda e: self.MouseLeave(self, e))
        self._canvas.bind("<FocusIn>", lambda e: self.GotFocus(self, e))
        self._canvas.bind("<FocusOut>", lambda e: self.LostFocus(self, e))

    def _draw(self):
        """Draws the checkbox."""
        self._canvas.delete("all")

        if self._is_checked:
            # Filled box with checkmark
            self._canvas.create_rectangle(
                2, 2, self._box_size - 2, self._box_size - 2,
                fill=self._check_color, outline=self._check_color, width=2
            )
            # Checkmark
            self._canvas.create_line(
                5, self._box_size // 2,
                self._box_size // 2 - 2, self._box_size - 6,
                fill="white", width=2
            )
            self._canvas.create_line(
                self._box_size // 2 - 2, self._box_size - 6,
                self._box_size - 4, 5,
                fill="white", width=2
            )
        else:
            # Empty box
            self._canvas.create_rectangle(
                2, 2, self._box_size - 2, self._box_size - 2,
                fill="white", outline=self._unchecked_color, width=2
            )

    def _on_click(self, event):
        """Handles click to toggle."""
        self._is_checked = not self._is_checked
        self._draw()

        self.CheckedChanged(self, EventArgs(event))
        self.Click(self, EventArgs(event))

    @property
    def IsChecked(self):
        return self._is_checked

    @IsChecked.setter
    def IsChecked(self, value):
        self._is_checked = value
        self._draw()

    @property
    def Text(self):
        return self._text

    @Text.setter
    def Text(self, value):
        self._text = value
        self._label.configure(text=value)


# =============================================================================
# RADIOBUTTON & RADIOBUTTONGROUP
# =============================================================================

class RadioButton(View):
    """
    Radio button control for exclusive single selection within a group.

    RadioButton provides mutually exclusive selection when used with
    RadioButtonGroup. Only one radio button in a group can be selected
    at a time - selecting one automatically deselects others.

    Inherits from View (Microsoft.Maui.Controls.RadioButton).

    Properties:
        IsChecked (bool): Whether this radio button is currently selected.
        Value (any): The value associated with this option.
        Text (str): Label text displayed next to the radio button.
        CheckedChanged (callable): Event handler called when selection changes.

    Args:
        master: Parent container for the radio button.
        text (str): Label text to display.
        value (any): Value to associate with this option (default: text).
        group (RadioButtonGroup): Group for mutual exclusion (optional).
        props (dict): Additional styling properties.

    Example:
        >>> group = RadioButtonGroup()
        >>> opt1 = RadioButton(form, text='Option A', value='A', group=group)
        >>> opt2 = RadioButton(form, text='Option B', value='B', group=group)
    """
    def __init__(self, master, text="", value=None, group=None, side=TOP, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        defaults = {
            'Text': text,
            'Value': value if value is not None else text,
            'IsChecked': False,
            'CheckColor': '#512BD4',
            'UncheckedColor': '#CCCCCC',
            'ForeColor': '#333333',
            'RadioSize': 20
        }
        if props:
            defaults.update(props)

        self._text = defaults['Text']
        self._value = defaults['Value']
        self._is_checked = defaults['IsChecked']
        self._group = group

        # RadioButton-specific event
        self.CheckedChanged = lambda sender, e: None

        # Colors
        self._check_color = defaults['CheckColor']
        self._unchecked_color = defaults['UncheckedColor']
        self._fg_color = defaults['ForeColor']

        # Size
        self._radio_size = defaults['RadioSize']

        self._bg = self._get_parent_bg()

        # Container frame
        self._frame = Native.Frame(self._parent, bg=self._bg, **kwargs)
        self._tk_widget = self._frame # Alias for consistency

        if not use_grid:
            self._frame.pack(side=side, anchor="w", pady=3)

        # Canvas for radio button
        self._canvas = Native.Canvas(
            self._frame,
            width=self._radio_size,
            height=self._radio_size,
            bg=self._bg,
            highlightthickness=0,
            cursor="hand2"
        )
        self._canvas.pack(side=LEFT)

        # Label
        self._label = Native.Label(
            self._frame,
            text=self._text,
            font=("Segoe UI", 10),
            fg=self._fg_color,
            bg=self._bg,
            cursor="hand2"
        )
        self._label.pack(side=LEFT, padx=(8, 0))

        # Draw initial state
        self._draw()

        # Bind click
        self._canvas.bind("<Button-1>", self._on_click)
        self._label.bind("<Button-1>", self._on_click)

        # Register with group if provided
        if self._group:
            self._group._add_radio(self)

    def _draw(self):
        """Draws the radio button."""
        self._canvas.delete("all")

        r = self._radio_size // 2

        if self._is_checked:
            # Outer circle
            self._canvas.create_oval(
                2, 2, self._radio_size - 2, self._radio_size - 2,
                fill="white", outline=self._check_color, width=2
            )
            # Inner filled circle
            inner_r = r // 2
            self._canvas.create_oval(
                r - inner_r, r - inner_r,
                r + inner_r, r + inner_r,
                fill=self._check_color, outline=self._check_color
            )
        else:
            # Empty circle
            self._canvas.create_oval(
                2, 2, self._radio_size - 2, self._radio_size - 2,
                fill="white", outline=self._unchecked_color, width=2
            )

    def _on_click(self, event):
        """Handles click to select."""
        if not self._is_checked:
            if self._group:
                self._group._select(self)
            else:
                self._is_checked = True
                self._draw()
                self.CheckedChanged(self, EventArgs(True))

    @property
    def IsChecked(self):
        return self._is_checked

    @IsChecked.setter
    def IsChecked(self, value):
        self._is_checked = value
        self._draw()

    @property
    def Value(self):
        return self._value

    @property
    def Text(self):
        return self._text

    @Text.setter
    def Text(self, value):
        self._text = value
        self._label.configure(text=value)


class RadioButtonGroup:
    """
    Container for managing mutually exclusive RadioButton selections.

    RadioButtonGroup ensures that only one RadioButton within the group
    can be selected at any time. When a radio button is selected, all
    others in the group are automatically deselected.

    Properties:
        SelectedValue (any): Value of the currently selected radio button.
        SelectionChanged (callable): Event handler called when selection changes.

    Example:
        >>> group = RadioButtonGroup()
        >>> group.SelectionChanged = lambda val: print(f'Selected: {val}')
        >>> RadioButton(form, text='Small', value='S', group=group)
        >>> RadioButton(form, text='Medium', value='M', group=group)
        >>> RadioButton(form, text='Large', value='L', group=group)
    """
    def __init__(self):
        self._radios = []
        self._selected = None
        self.SelectionChanged = lambda sender, e: None

    def _add_radio(self, radio):
        """Adds a radio button to the group."""
        self._radios.append(radio)

    def _select(self, radio):
        """Selects a radio button and deselects others."""
        for r in self._radios:
            if r == radio:
                r._is_checked = True
                r._draw()
                r.CheckedChanged(r, EventArgs(True))
            else:
                if r._is_checked:
                    r._is_checked = False
                    r._draw()
                    r.CheckedChanged(r, EventArgs(False))

        self._selected = radio
        self.SelectionChanged(self, EventArgs(radio.Value))

    @property
    def SelectedValue(self):
        """Gets the selected value."""
        return self._selected.Value if self._selected else None

    @SelectedValue.setter
    def SelectedValue(self, value):
        """Sets the selected value."""
        for r in self._radios:
            if r.Value == value:
                self._select(r)
                break


# =============================================================================
# PICKER - Dropdown/ComboBox
# =============================================================================

class Picker(View):
    """
    Dropdown selection control for choosing from a list of options.

    Picker displays a dropdown (combobox) that allows users to select
    one item from a predefined list. Implements read-only selection
    to ensure valid choices from the available options.

    Inherits from View (Microsoft.Maui.Controls.Picker).

    Properties:
        Items (list): List of selectable options.
        SelectedIndex (int): Zero-based index of the selected item (-1 if none).
        SelectedItem (any): The currently selected item value.
        SelectedIndexChanged (callable): Event handler called when selection changes.

    Args:
        master: Parent container for the picker.
        items (list): List of options to display (default: []).
        title (str): Placeholder text shown before selection (default: 'Select').
        props (dict): Additional styling properties.

    Example:
        >>> colors = Picker(form, items=['Red', 'Green', 'Blue'], title='Choose color')
        >>> colors.SelectedIndexChanged = lambda idx: apply_color(colors.SelectedItem)
    """
    def __init__(self, master, items=None, title="Select", side=TOP, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        defaults = {
            'Items': items or [],
            'Title': title,
            'SelectedIndex': -1
        }
        if props:
            defaults.update(props)

        self._items = defaults['Items']
        self._title = defaults['Title']
        self._selected_index = defaults['SelectedIndex']

        # Picker-specific event
        self.SelectedIndexChanged = lambda sender, e: None

        self._bg = self._get_parent_bg()

        # Determine width (convert pixels to chars if provided)
        width_pixels = kwargs.pop('width', None)
        tk_width = width_pixels // 8 if width_pixels and width_pixels > 40 else width_pixels

        # Frame
        self._frame = Native.Frame(self._parent, bg=self._bg, **kwargs)
        self._tk_widget = self._frame # Alias for consistency

        if not use_grid:
            self._frame.pack(side=side, anchor="w", pady=5)

        # Combobox using ttk
        style = Native.Style()
        style.configure("Picker.TCombobox", padding=5)

        self._var = Native.StringVar()
        self._combo = Native.Combobox(
            self._frame,
            textvariable=self._var,
            values=self._items,
            state="readonly",
            font=("Segoe UI", 10),
            style="Picker.TCombobox",
            width=tk_width
        )
        self._combo.pack(fill=X if not tk_width else None)

        if self._items:
            self._combo.set(self._title)

        # Bind selection
        self._combo.bind("<<ComboboxSelected>>", self._on_select)

    def _on_select(self, event):
        """Handles selection change."""
        self._selected_index = self._combo.current()
        self.SelectedIndexChanged(self, EventArgs(self._selected_index))

    @property
    def Items(self):
        return self._items

    @Items.setter
    def Items(self, value):
        self._items = value
        self._combo['values'] = value

    @property
    def SelectedIndex(self):
        return self._selected_index

    @SelectedIndex.setter
    def SelectedIndex(self, value):
        if 0 <= value < len(self._items):
            self._selected_index = value
            self._combo.current(value)

    @property
    def SelectedItem(self):
        if 0 <= self._selected_index < len(self._items):
            return self._items[self._selected_index]
        return None

    @SelectedItem.setter
    def SelectedItem(self, value):
        if value in self._items:
            self.SelectedIndex = self._items.index(value)


# =============================================================================
# SLIDER - Range Control
# =============================================================================

class Slider(View):
    """
    Range slider control for selecting values within a continuous range.

    Slider provides a horizontal track with a draggable thumb for selecting
    numeric values between minimum and maximum bounds. Features visual
    feedback showing the filled portion of the range.

    Inherits from View (Microsoft.Maui.Controls.Slider).

    Properties:
        Value (float): Current slider position value.
        Minimum (float): Minimum allowed value (default: 0).
        Maximum (float): Maximum allowed value (default: 100).
        ValueChanged (callable): Event handler called when value changes.

    Args:
        master: Parent container for the slider.
        minimum (float): Minimum value of the range.
        maximum (float): Maximum value of the range.
        value (float): Initial slider position.
        props (dict): Additional properties (width, colors).

    Example:
        >>> volume = Slider(settings, minimum=0, maximum=100, value=50)
        >>> volume.ValueChanged = lambda v: set_volume(int(v))
    """
    def __init__(self, master, minimum=0, maximum=100, value=0, side=TOP, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        defaults = {
            'Minimum': minimum,
            'Maximum': maximum,
            'Value': value,
            'TrackColor': '#E0E0E0',
            'FillColor': '#512BD4',
            'ThumbColor': '#512BD4',
            'Width': 200,
            'Height': 30,
            'TrackHeight': 4,
            'ThumbSize': 20
        }
        if props:
            defaults.update(props)

        self._minimum = defaults['Minimum']
        self._maximum = defaults['Maximum']
        self._value = defaults['Value']

        # Slider-specific events (in addition to View's standard events)
        self.ValueChanged = lambda sender, e: None
        self.GotFocus = lambda sender, e: None
        self.LostFocus = lambda sender, e: None

        # Colors
        self._track_color = defaults['TrackColor']
        self._fill_color = defaults['FillColor']
        self._thumb_color = defaults['ThumbColor']

        # Dimensions
        self._width = defaults['Width']
        self._height = defaults['Height']
        self._track_height = defaults['TrackHeight']
        self._thumb_size = defaults['ThumbSize']

        self._bg = self._get_parent_bg()

        # Canvas
        self._canvas = Native.Canvas(
            self._parent,
            width=self._width,
            height=self._height,
            bg=self._bg,
            highlightthickness=0,
            cursor="hand2"
        )
        self._tk_widget = self._canvas # Alias for consistency

        if not use_grid:
            self._canvas.pack(side=side, pady=5)

        # Draw initial state
        self._draw()

        # Bind events
        self._canvas.bind("<Button-1>", self._on_click)
        self._canvas.bind("<B1-Motion>", self._on_drag)
        self._canvas.bind("<Double-Button-1>", lambda e: self.DoubleClick(self, e))
        self._canvas.bind("<Enter>", lambda e: self.MouseEnter(self, e))
        self._canvas.bind("<Leave>", lambda e: self.MouseLeave(self, e))
        self._canvas.bind("<FocusIn>", lambda e: self.GotFocus(self, e))
        self._canvas.bind("<FocusOut>", lambda e: self.LostFocus(self, e))

    def _draw(self):
        """Draws the slider."""
        self._canvas.delete("all")

        # Calculate positions
        track_y = self._height // 2
        track_start = self._thumb_size // 2
        track_end = self._width - self._thumb_size // 2
        track_width = track_end - track_start

        # Calculate thumb position
        ratio = (self._value - self._minimum) / (self._maximum - self._minimum) if self._maximum > self._minimum else 0
        thumb_x = track_start + ratio * track_width

        # Draw track background
        self._canvas.create_rectangle(
            track_start, track_y - self._track_height // 2,
            track_end, track_y + self._track_height // 2,
            fill=self._track_color, outline=self._track_color
        )

        # Draw filled portion
        self._canvas.create_rectangle(
            track_start, track_y - self._track_height // 2,
            thumb_x, track_y + self._track_height // 2,
            fill=self._fill_color, outline=self._fill_color
        )

        # Draw thumb
        self._canvas.create_oval(
            thumb_x - self._thumb_size // 2, track_y - self._thumb_size // 2,
            thumb_x + self._thumb_size // 2, track_y + self._thumb_size // 2,
            fill=self._thumb_color, outline=self._thumb_color
        )

    def _get_value_from_x(self, x):
        """Converts x coordinate to value."""
        track_start = self._thumb_size // 2
        track_end = self._width - self._thumb_size // 2
        track_width = track_end - track_start

        # Clamp x
        x = max(track_start, min(track_end, x))

        ratio = (x - track_start) / track_width
        return self._minimum + ratio * (self._maximum - self._minimum)

    def _on_click(self, event):
        """Handles click to set value."""
        new_value = self._get_value_from_x(event.x)
        self._set_value(new_value, event)
        self.Click(self, EventArgs(event))

    def _on_drag(self, event):
        """Handles drag to change value."""
        new_value = self._get_value_from_x(event.x)
        self._set_value(new_value, event)

    def _set_value(self, value, event=None):
        """Sets value and triggers event."""
        old_value = self._value
        self._value = max(self._minimum, min(self._maximum, value))
        self._draw()

        if old_value != self._value:
            self.ValueChanged(self, EventArgs(event) if event else EventArgs(data=self._value))

    @property
    def Value(self):
        return self._value

    @Value.setter
    def Value(self, value):
        self._set_value(value)

    @property
    def Minimum(self):
        return self._minimum

    @Minimum.setter
    def Minimum(self, value):
        self._minimum = value
        self._draw()

    @property
    def Maximum(self):
        return self._maximum

    @Maximum.setter
    def Maximum(self, value):
        self._maximum = value
        self._draw()


# =============================================================================
# EDITOR - Multiline Text Input
# =============================================================================

class Editor(View):
    """
    Multi-line text input control with scrolling and placeholder support.

    Editor provides a text area for entering and editing multi-line text
    content. Includes automatic vertical scrolling, placeholder text,
    and word wrapping for comfortable text editing.

    Inherits from View (Microsoft.Maui.Controls.Editor).

    Properties:
        Text (str): Current text content of the editor.
        Placeholder (str): Hint text shown when editor is empty.
        TextChanged (callable): Event handler called when text content changes.

    Args:
        master: Parent container for the editor.
        placeholder (str): Hint text displayed when empty.
        props (dict): Additional properties including height.

    Example:
        >>> notes = Editor(form, placeholder='Enter your notes here...')
        >>> notes.TextChanged = lambda text: auto_save(text)
    """
    def __init__(self, master, placeholder="", side=TOP, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        defaults = {
            'Placeholder': placeholder,
            'Height': 100,
            'Font': ('Segoe UI', 10),
            'ForeColor': '#333333',
            'PlaceholderColor': '#999999',
            'BackColor': None
        }
        if props:
            defaults.update(props)

        self._placeholder = defaults['Placeholder']
        self._showing_placeholder = False
        self._fg_color = defaults['ForeColor']
        self._placeholder_color = defaults['PlaceholderColor']
        self._height = defaults['Height']
        self._font = defaults['Font']

        # Editor-specific event
        self.TextChanged = lambda sender, e: None

        self._bg = defaults['BackColor'] if defaults['BackColor'] else self._get_parent_bg()

        # Frame
        self._frame = Native.Frame(self._parent, bg=self._bg, **kwargs)
        self._tk_widget = self._frame # Alias for consistency

        if not use_grid:
            self._frame.pack(side=side, fill=X, pady=5)

        # Text widget with scrollbar
        self._scrollbar = Native.Scrollbar(self._frame)
        self._scrollbar.pack(side=RIGHT, fill=Y)

        self._text = Native.Text(
            self._frame,
            font=self._font,
            wrap=WORD,
            bd=1,
            relief=SOLID,
            height=self._height // 20,  # Approximate lines
            yscrollcommand=self._scrollbar.set
        )
        self._text.pack(fill=BOTH, expand=True)

        self._scrollbar.config(command=self._text.yview)

        # Placeholder
        if self._placeholder:
            self._show_placeholder()
            self._text.bind("<FocusIn>", self._on_focus_in)
            self._text.bind("<FocusOut>", self._on_focus_out)

        # Text changed event
        self._text.bind("<KeyRelease>", self._on_key_release)

    def _show_placeholder(self):
        """Shows placeholder text."""
        if not self._text.get("1.0", END).strip():
            self._text.insert("1.0", self._placeholder)
            self._text.config(fg=self._placeholder_color)
            self._showing_placeholder = True

    def _on_focus_in(self, event):
        """Clears placeholder on focus."""
        if self._showing_placeholder:
            self._text.delete("1.0", END)
            self._text.config(fg=self._fg_color)
            self._showing_placeholder = False

    def _on_focus_out(self, event):
        """Shows placeholder if empty."""
        if not self._text.get("1.0", END).strip():
            self._show_placeholder()

    def _on_key_release(self, event):
        """Triggers TextChanged event."""
        if not self._showing_placeholder:
            self.TextChanged(self, EventArgs(self.Text))

    @property
    def Text(self):
        if self._showing_placeholder:
            return ""
        return self._text.get("1.0", END).strip()

    @Text.setter
    def Text(self, value):
        self._text.delete("1.0", END)
        if value:
            self._text.config(fg="#333333")
            self._text.insert("1.0", value)
            self._showing_placeholder = False
        else:
            self._show_placeholder()

    @property
    def Placeholder(self):
        return self._placeholder

    @Placeholder.setter
    def Placeholder(self, value):
        self._placeholder = value


############# Date & Time Controls #############

# =============================================================================
# DATEPICKER - Date Selection Control
# =============================================================================

class DatePicker(View):
    """
    Date selection control with interactive calendar popup.

    DatePicker displays a text entry with a calendar button that opens
    a popup calendar for date selection. Supports date range constraints
    and customizable date formats.

    Inherits from View (Microsoft.Maui.Controls.DatePicker).

    Properties:
        Date (datetime.date): Currently selected date.
        MinimumDate (datetime.date): Earliest selectable date (optional).
        MaximumDate (datetime.date): Latest selectable date (optional).
        DateSelected (callable): Event handler called when date is selected.

    Args:
        master: Parent container for the date picker.
        props (dict): Additional properties including format.

    Features:
        - Interactive calendar popup with month/year navigation
        - Manual date entry via text field
        - Date validation against min/max constraints
        - ISO 8601 date format by default (YYYY-MM-DD)

    Example:
        >>> birth_date = DatePicker(form)
        >>> birth_date.MaximumDate = date.today()
        >>> birth_date.DateSelected = lambda d: validate_age(d)
    """
    def __init__(self, master, side=TOP, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        defaults = {
            'Date': datetime.now().date(),
            'Format': '%Y-%m-%d',
            'MinimumDate': None,
            'MaximumDate': None
        }
        if props:
            defaults.update(props)

        self._date = defaults['Date']
        self._format = defaults['Format']
        self._min_date = defaults['MinimumDate']
        self._max_date = defaults['MaximumDate']

        # DatePicker-specific event
        self.DateSelected = lambda sender, e: None

        self._bg = self._get_parent_bg()

        # Main frame
        self._frame = Native.Frame(self._parent, bg=self._bg, **kwargs)
        self._tk_widget = self._frame # Alias for consistency

        if not use_grid:
            self._frame.pack(side=side, fill=X, pady=5)

        # Entry for date display
        self._entry = Native.Entry(self._frame, width=15)
        self._entry.pack(side=LEFT, padx=(0, 5))
        self._entry.insert(0, self._date.strftime(self._format))
        self._entry.bind("<Return>", self._parse_entry)

        # Calendar button
        self._btn = Native.Button(self._frame, text="📅", width=3, command=self._show_calendar)
        self._btn.pack(side=LEFT)

        self._calendar_popup = None

    def _parse_entry(self, event=None):
        """Parses date from entry."""
        try:
            new_date = datetime.strptime(self._entry.get(), self._format).date()
            if self._validate_date(new_date):
                self._date = new_date
                if self.DateSelected:
                    self.DateSelected(self._date)
        except ValueError:
            self._entry.delete(0, END)
            self._entry.insert(0, self._date.strftime(self._format))

    def _validate_date(self, date):
        """Validates date against min/max constraints."""
        if self._min_date and date < self._min_date:
            return False
        if self._max_date and date > self._max_date:
            return False
        return True

    def _show_calendar(self):
        """Shows calendar popup."""
        if Native.Exists(self._calendar_popup):
            Native.Destroy(self._calendar_popup)
            return

        # Get root window
        root = Native.GetRoot(self._frame)

        # Create popup
        self._calendar_popup = Native.Toplevel(root)
        Native.Overrideredirect(self._calendar_popup, True)

        # Position near button
        bx, by = Native.GetPosition(self._btn)
        _, bh = Native.GetSize(self._btn)
        Native.Geometry(self._calendar_popup, f"+{bx}+{by + bh}")

        # Calendar frame
        cal_frame = Native.Frame(self._calendar_popup, bg="white", bd=1, relief=SOLID)
        cal_frame.pack()

        # Month/Year navigation
        nav_frame = Native.Frame(cal_frame, bg="white")
        nav_frame.pack(fill=X, padx=5, pady=5)

        self._display_month = self._date.month
        self._display_year = self._date.year

        Native.Button(nav_frame, text="<", command=self._prev_month, width=2).pack(side=LEFT)
        self._month_label = Native.Label(nav_frame, bg="white", font=("Segoe UI", 10, "bold"))
        self._month_label.pack(side=LEFT, expand=True, fill=X)
        Native.Button(nav_frame, text=">", command=self._next_month, width=2).pack(side=RIGHT)

        # Days grid frame
        self._days_frame = Native.Frame(cal_frame, bg="white")
        self._days_frame.pack(padx=5, pady=5)

        self._draw_calendar()

        # Close on click outside
        self._calendar_popup.bind("<FocusOut>", lambda e: self._close_calendar_delayed())
        Native.Focus(self._calendar_popup)

    def _close_calendar_delayed(self):
        """Closes calendar with delay to allow button clicks."""
        if self._calendar_popup:
            Native.Wait(self._frame, 100, self._safe_close_calendar)

    def _safe_close_calendar(self):
        """Safely closes calendar if it exists."""
        if Native.Exists(self._calendar_popup):
            Native.Destroy(self._calendar_popup)

    def _draw_calendar(self):
        """Draws calendar grid."""
        # Clear previous
        for widget in Native.GetChildren(self._days_frame):
            Native.Destroy(widget)

        # Update label
        month_names = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
        self._month_label.config(text=f"{month_names[self._display_month-1]} {self._display_year}")

        # Day headers
        days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        for i, day in enumerate(days):
            Native.Label(self._days_frame, text=day, bg="white", width=3,
                    font=("Segoe UI", 8, "bold")).grid(row=0, column=i)

        # Get calendar data
        import calendar
        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(self._display_year, self._display_month)

        for row_idx, week in enumerate(month_days):
            for col_idx, day in enumerate(week):
                if day == 0:
                    Native.Label(self._days_frame, text="", bg="white", width=3).grid(row=row_idx+1, column=col_idx)
                else:
                    btn_bg = "#0078D4" if (day == self._date.day and
                                           self._display_month == self._date.month and
                                           self._display_year == self._date.year) else "white"
                    btn_fg = "white" if btn_bg == "#0078D4" else "black"
                    btn = Native.Label(self._days_frame, text=str(day), bg=btn_bg, fg=btn_fg,
                                  width=3, cursor="hand2")
                    btn.grid(row=row_idx+1, column=col_idx)
                    btn.bind("<Button-1>", lambda e, d=day: self._select_day(d))

    def _prev_month(self):
        """Goes to previous month."""
        self._display_month -= 1
        if self._display_month < 1:
            self._display_month = 12
            self._display_year -= 1
        self._draw_calendar()

    def _next_month(self):
        """Goes to next month."""
        self._display_month += 1
        if self._display_month > 12:
            self._display_month = 1
            self._display_year += 1
        self._draw_calendar()

    def _select_day(self, day):
        """Selects a day."""
        new_date = date(self._display_year, self._display_month, day)
        if self._validate_date(new_date):
            self._date = new_date
            self._entry.delete(0, END)
            self._entry.insert(0, self._date.strftime(self._format))
            self.DateSelected(self, EventArgs(self._date))
        Native.Destroy(self._calendar_popup)

    @property
    def Date(self):
        return self._date

    @Date.setter
    def Date(self, value):
        if isinstance(value, date) and self._validate_date(value):
            self._date = value
            self._entry.delete(0, END)
            self._entry.insert(0, self._date.strftime(self._format))

    @property
    def MinimumDate(self):
        return self._min_date

    @MinimumDate.setter
    def MinimumDate(self, value):
        self._min_date = value

    @property
    def MaximumDate(self):
        return self._max_date

    @MaximumDate.setter
    def MaximumDate(self, value):
        self._max_date = value


# =============================================================================
# TIMEPICKER - Time Selection Control
# =============================================================================

class TimePicker(View):
    """
    Time selection control with hour, minute, and second spinboxes.

    TimePicker provides an intuitive interface for selecting time values
    using individual spinbox controls for hours, minutes, and seconds.
    Values are automatically validated and clamped to valid ranges.

    Inherits from View (Microsoft.Maui.Controls.TimePicker).

    Properties:
        Time (datetime.time): Currently selected time.
        Hour (int): Hour component (0-23).
        Minute (int): Minute component (0-59).
        Second (int): Second component (0-59).
        TimeSelected (callable): Event handler called when time is selected.

    Args:
        master: Parent container for the time picker.
        props (dict): Additional properties including format_24h.

    Example:
        >>> alarm_time = TimePicker(settings)
        >>> alarm_time.Time = time(7, 30, 0)
        >>> alarm_time.TimeSelected = lambda t: set_alarm(t)
    """
    def __init__(self, master, side=TOP, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        defaults = {
            'Time': datetime.now().time(),
            'Format24h': True
        }
        if props:
            defaults.update(props)

        self._time = defaults['Time']
        self._format_24h = defaults['Format24h']

        # TimePicker-specific event
        self.TimeSelected = lambda sender, e: None

        self._bg = self._get_parent_bg()

        # Main frame
        self._frame = Native.Frame(self._parent, bg=self._bg, **kwargs)
        self._tk_widget = self._frame # Alias for consistency

        if not use_grid:
            self._frame.pack(side=side, fill=X, pady=5)

        # Hour spinbox
        self._hour_var = Native.StringVar(value=f"{self._time.hour:02d}")
        self._hour_spin = Native.Spinbox(
            self._frame, from_=0, to=23, width=3,
            textvariable=self._hour_var, format="%02.0f",
            command=self._on_time_change
        )
        self._hour_spin.pack(side=LEFT)

        # Separator
        Native.Label(self._frame, text=":", bg=self._bg, font=("Segoe UI", 12, "bold")).pack(side=LEFT)

        # Minute spinbox
        self._minute_var = Native.StringVar(value=f"{self._time.minute:02d}")
        self._minute_spin = Native.Spinbox(
            self._frame, from_=0, to=59, width=3,
            textvariable=self._minute_var, format="%02.0f",
            command=self._on_time_change
        )
        self._minute_spin.pack(side=LEFT)

        # Separator
        Native.Label(self._frame, text=":", bg=self._bg, font=("Segoe UI", 12, "bold")).pack(side=LEFT)

        # Second spinbox
        self._second_var = Native.StringVar(value=f"{self._time.second:02d}")
        self._second_spin = Native.Spinbox(
            self._frame, from_=0, to=59, width=3,
            textvariable=self._second_var, format="%02.0f",
            command=self._on_time_change
        )
        self._second_spin.pack(side=LEFT)

        # Bind validation
        for spin in [self._hour_spin, self._minute_spin, self._second_spin]:
            spin.bind("<FocusOut>", self._validate_and_update)
            spin.bind("<Return>", self._validate_and_update)

    def _on_time_change(self):
        """Handles time change from spinboxes."""
        self._validate_and_update()

    def _validate_and_update(self, event=None):
        """Validates and updates time."""
        try:
            hour = int(self._hour_var.get())
            minute = int(self._minute_var.get())
            second = int(self._second_var.get())

            # Clamp values
            hour = max(0, min(23, hour))
            minute = max(0, min(59, minute))
            second = max(0, min(59, second))

            # Update vars
            self._hour_var.set(f"{hour:02d}")
            self._minute_var.set(f"{minute:02d}")
            self._second_var.set(f"{second:02d}")

            # Create time
            self._time = time(hour, minute, second)

            self.TimeSelected(self, EventArgs(self._time))

        except ValueError:
            # Reset to current time
            self._hour_var.set(f"{self._time.hour:02d}")
            self._minute_var.set(f"{self._time.minute:02d}")
            self._second_var.set(f"{self._time.second:02d}")

    @property
    def Time(self):
        return self._time

    @Time.setter
    def Time(self, value):
        if isinstance(value, time):
            self._time = value
            self._hour_var.set(f"{value.hour:02d}")
            self._minute_var.set(f"{value.minute:02d}")
            self._second_var.set(f"{value.second:02d}")

    @property
    def Hour(self):
        return self._time.hour

    @property
    def Minute(self):
        return self._time.minute

    @property
    def Second(self):
        return self._time.second


############# Progress & Activity Controls #############

# =============================================================================
# ACTIVITYINDICATOR - Loading Spinner
# =============================================================================

class ActivityIndicator(View):
    """
    Animated loading spinner to indicate ongoing operations.

    ActivityIndicator displays a spinning arc animation to communicate
    that a background process is running. The animation continues until
    explicitly stopped, making it ideal for async operations.

    Inherits from View (Microsoft.Maui.Controls.ActivityIndicator).

    Properties:
        IsRunning (bool): Whether the spinner animation is active.
        Color (str): Color of the spinning arc (default: '#0078D4').

    Methods:
        Start(): Begins the spinning animation.
        Stop(): Stops the spinning animation.

    Args:
        master: Parent container for the indicator.
        props (dict): Additional properties including color, size.

    Example:
        >>> loader = ActivityIndicator(container, props={'Color': '#FF5722'})
        >>> loader.Start()  # Show loading
        >>> # ... perform async operation ...
        >>> loader.Stop()   # Hide loading
    """
    def __init__(self, master, side=TOP, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        defaults = {
            'Color': '#0078D4',
            'Size': 30,
            'IsRunning': False
        }
        if props:
            defaults.update(props)

        self._is_running = defaults['IsRunning']
        self._color = defaults['Color']
        self._size = defaults['Size']
        self._angle = 0
        self._animation_id = None

        self._bg = self._get_parent_bg()

        # Frame container
        self._frame = Native.Frame(self._parent, bg=self._bg, **kwargs)
        self._tk_widget = self._frame # Alias for consistency

        if not use_grid:
            self._frame.pack(side=side, pady=5)

        # Canvas for drawing
        self._canvas = Native.Canvas(
            self._frame,
            width=self._size,
            height=self._size,
            bg=self._bg,
            highlightthickness=0
        )
        self._canvas.pack()

        self._draw()

    def _draw(self):
        """Draws the spinner."""
        self._canvas.delete("all")

        if not self._is_running:
            return

        cx = self._size // 2
        cy = self._size // 2
        radius = self._size // 2 - 4
        arc_length = 90  # degrees

        # Draw arc
        start = self._angle
        self._canvas.create_arc(
            cx - radius, cy - radius,
            cx + radius, cy + radius,
            start=start, extent=arc_length,
            style=ARC, outline=self._color, width=3
        )

    def _animate(self):
        """Animation loop."""
        if self._is_running:
            self._angle = (self._angle + 15) % 360
            self._draw()
            self._animation_id = Native.Wait(self._frame, 50, self._animate)

    @property
    def IsRunning(self):
        return self._is_running

    @IsRunning.setter
    def IsRunning(self, value):
        self._is_running = value
        if value:
            self._animate()
        else:
            if self._animation_id:
                Native.CancelWait(self._frame, self._animation_id)
                self._animation_id = None
            self._draw()

    @property
    def Color(self):
        return self._color

    @Color.setter
    def Color(self, value):
        self._color = value
        self._draw()

    def Start(self):
        """Starts the animation."""
        self.IsRunning = True

    def Stop(self):
        """Stops the animation."""
        self.IsRunning = False


# =============================================================================
# PROGRESSBAR - Progress Indicator
# =============================================================================

class ProgressBar(View):
    """
    Horizontal progress indicator for determinate and indeterminate states.

    ProgressBar displays progress as a filled horizontal bar. Supports both
    determinate mode (showing specific progress 0-100%) and indeterminate
    mode (animated moving segment for unknown duration operations).

    Inherits from View (Microsoft.Maui.Controls.ProgressBar).

    Properties:
        Progress (float): Progress value from 0.0 to 1.0 (determinate mode).
        IsIndeterminate (bool): Whether to show indeterminate animation.
        ProgressColor (str): Color of the progress fill.

    Args:
        master: Parent container for the progress bar.
        props (dict): Additional properties including color, isindeterminate.

    Example:
        >>> # Determinate progress
        >>> progress = ProgressBar(container)
        >>> progress.Progress = 0.75  # 75% complete
        >>>
        >>> # Indeterminate progress
        >>> loading = ProgressBar(container, props={'IsIndeterminate': True})
    """
    def __init__(self, master, side=TOP, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        defaults = {
            'Progress': 0.0,
            'ProgressColor': '#0078D4',
            'TrackColor': '#E0E0E0',
            'Height': 6,
            'IsIndeterminate': False
        }
        if props:
            defaults.update(props)

        self._progress = max(0.0, min(1.0, defaults['Progress']))
        self._color = defaults['ProgressColor']
        self._track_color = defaults['TrackColor']
        self._height = defaults['Height']
        self._is_indeterminate = defaults['IsIndeterminate']
        self._animation_id = None
        self._indeterminate_pos = 0

        self._bg = self._get_parent_bg()

        # Frame
        self._frame = Native.Frame(self._parent, bg=self._bg, **kwargs)
        self._tk_widget = self._frame # Alias for consistency

        if not use_grid:
            self._frame.pack(side=side, fill=X, pady=5)

        # Canvas for progress
        self._canvas = Native.Canvas(
            self._frame,
            height=self._height,
            bg=self._track_color,
            highlightthickness=0
        )
        self._canvas.pack(fill=X)

        # Bind resize
        self._canvas.bind("<Configure>", lambda e: self._draw())

        if self._is_indeterminate:
            self._animate_indeterminate()

    def _draw(self):
        """Draws the progress bar."""
        self._canvas.delete("all")

        width = Native.GetSize(self._canvas)[0]
        height = self._height

        if self._is_indeterminate:
            # Moving segment
            seg_width = width // 4
            x1 = self._indeterminate_pos
            x2 = x1 + seg_width
            self._canvas.create_rectangle(
                x1, 0, x2, height,
                fill=self._color, outline=""
            )
        else:
            # Progress fill
            fill_width = width * self._progress
            if fill_width > 0:
                self._canvas.create_rectangle(
                    0, 0, fill_width, height,
                    fill=self._color, outline=""
                )

    def _animate_indeterminate(self):
        """Animates indeterminate progress."""
        if self._is_indeterminate:
            width = Native.GetSize(self._canvas)[0]
            seg_width = width // 4

            self._indeterminate_pos += 5
            if self._indeterminate_pos > width:
                self._indeterminate_pos = -seg_width

            self._draw()
            self._animation_id = Native.Wait(self._frame, 30, self._animate_indeterminate)

    @property
    def Progress(self):
        return self._progress

    @Progress.setter
    def Progress(self, value):
        self._progress = max(0.0, min(1.0, value))
        if not self._is_indeterminate:
            self._draw()

    @property
    def IsIndeterminate(self):
        return self._is_indeterminate

    @IsIndeterminate.setter
    def IsIndeterminate(self, value):
        self._is_indeterminate = value
        if value:
            self._animate_indeterminate()
        else:
            if self._animation_id:
                Native.CancelWait(self._frame, self._animation_id)
                self._animation_id = None
            self._draw()

    @property
    def ProgressColor(self):
        return self._color

    @ProgressColor.setter
    def ProgressColor(self, value):
        self._color = value
        self._draw()


############# Container & Card Controls #############

# =============================================================================
# FRAME - Bordered Container
# =============================================================================

class Frame:
    """
    Bordered container control for grouping related content.

    Frame provides a visual boundary around child content with customizable
    border color, background, and optional shadow effect. Useful for
    creating visual sections and grouping related UI elements.

    Properties:
        Content (Frame): Container frame for adding child elements.
        BorderColor (str): Color of the frame border.
        BackgroundColor (str): Background color inside the frame.

    Args:
        master: Parent container for the frame.
        props (dict): Properties including BorderColor, BackgroundColor,
                     CornerRadius, Padding, HasShadow.

    Example:
        >>> card = Frame(page, props={'HasShadow': True, 'Padding': 15})
        >>> Label(card.Content, text='Frame content here')
    """
    def __init__(self, master, props=None):
        # Default values - WinFormPy style
        defaults = {
            'BorderColor': '#CCCCCC',
            'BackgroundColor': 'white',
            'CornerRadius': 5,
            'Padding': 10,
            'Height': None,
            'HasShadow': False
        }

        # Apply props over defaults
        if props:
            defaults.update(props)

        self._master = master
        self._border_color = defaults['BorderColor']
        self._background_color = defaults['BackgroundColor']
        self._corner_radius = defaults['CornerRadius']
        self._padding = defaults['Padding']
        self._height = defaults['Height']
        self._has_shadow = defaults['HasShadow']
        self._pack_propagate = True

        # Determine parent
        if hasattr(master, '_frame'):
            parent = master._frame
        else:
            parent = master

        self._bg = parent.cget("bg")

        # Outer frame for shadow effect
        if self._has_shadow:
            self._shadow_frame = Native.Frame(parent, bg="#AAAAAA")
            self._shadow_frame.pack(fill=X, pady=(5, 7), padx=(5, 7))
            container_parent = self._shadow_frame
            pack_pady = (0, 2)
            pack_padx = (0, 2)
        else:
            container_parent = parent
            pack_pady = 5
            pack_padx = 0

        # Main frame — apply fixed height if specified
        frame_kwargs = dict(
            bg=self._background_color,
            bd=1,
            relief=SOLID,
            highlightbackground=self._border_color,
            highlightthickness=1
        )
        if self._height is not None:
            frame_kwargs['height'] = self._height

        self._frame = Native.Frame(container_parent, **frame_kwargs)
        self._frame.pack(fill=X, pady=pack_pady, padx=pack_padx)

        # Disable pack propagation when a fixed height is set
        if self._height is not None:
            self._pack_propagate = False
            self._frame.pack_propagate(False)

        # Content frame with padding
        # Support int, 2-tuple (x, y), or 4-tuple (left, top, right, bottom)
        pad = self._padding
        if isinstance(pad, (list, tuple)):
            if len(pad) == 4:
                content_padx = (pad[0], pad[2])
                content_pady = (pad[1], pad[3])
            elif len(pad) == 2:
                content_padx = pad[0]
                content_pady = pad[1]
            else:
                content_padx = content_pady = pad[0] if pad else 0
        else:
            content_padx = content_pady = pad

        self._content = Native.Frame(
            self._frame,
            bg=self._background_color,
        )
        self._content.pack(fill=BOTH, expand=True, padx=content_padx, pady=content_pady)

    @property
    def Content(self):
        """Returns the content frame for adding children."""
        return self._content

    @property
    def BorderColor(self):
        return self._border_color

    @BorderColor.setter
    def BorderColor(self, value):
        self._border_color = value
        self._frame.config(highlightbackground=value)

    @property
    def BackgroundColor(self):
        return self._background_color

    @BackgroundColor.setter
    def BackgroundColor(self, value):
        self._background_color = value
        self._frame.config(bg=value)
        self._content.config(bg=value)

    @property
    def PackPropagate(self):
        """Gets or sets whether the frame propagates child geometry.

        When False, the frame keeps its fixed size regardless of child content.
        Typically used with the Height property for fixed-height containers.
        """
        return self._pack_propagate

    @PackPropagate.setter
    def PackPropagate(self, value):
        self._pack_propagate = value
        self._frame.pack_propagate(value)

    @property
    def Height(self):
        """Gets or sets the fixed height of the frame."""
        return self._height

    @Height.setter
    def Height(self, value):
        self._height = value
        if value is not None:
            self._frame.config(height=value)
            if not self._pack_propagate:
                self._frame.pack_propagate(False)

    def Show(self):
        """Shows the frame (re-packs it)."""
        self._frame.pack(fill=X, pady=5)

    def Hide(self):
        """Hides the frame (removes it from layout)."""
        self._frame.pack_forget()

    @property
    def IsVisible(self):
        """Gets whether the frame is currently visible."""
        return Native.IsViewable(self._frame)

    @IsVisible.setter
    def IsVisible(self, value):
        if value:
            self.Show()
        else:
            self.Hide()

    def Fill(self, control):
        """Hosts a WinFormPy control inside this Frame, filling the entire content area.

        WinFormPy controls use `place()` geometry by default, which may not
        integrate well with `pack()`-managed mauipy containers. This method
        removes the `place()` positioning and instead packs the control to
        fill the Frame's content area using `pack(fill=BOTH, expand=True)`.

        Args:
            control: A WinFormPy control instance (e.g., CheckedListBox, ListBox).

        Example:
            >>> wrapper = layout.AddChild(Frame, props={'Height': 200, 'Padding': 0})
            >>> my_list = CheckedListBox(wrapper.Content, props={...})
            >>> wrapper.Fill(my_list)
        """
        widget = (control.GetTkWidget() if hasattr(control, 'GetTkWidget') else getattr(control, '_tk_widget', None)) or getattr(control, '_container_frame', None)
        if widget:
            try:
                widget.place_forget()
            except Exception:
                pass
            widget.pack(in_=self._content, fill=BOTH, expand=True)

    # -- Tkinter geometry proxies so callers can fine-tune layout after init --

    def pack(self, **kwargs):
        """Delegates pack() to the outer frame widget."""
        self._frame.pack(**kwargs)

    def pack_forget(self):
        """Delegates pack_forget() to the outer frame widget."""
        self._frame.pack_forget()

    def pack_configure(self, **kwargs):
        """Delegates pack_configure() to the outer frame widget."""
        self._frame.pack_configure(**kwargs)

    def configure(self, **kwargs):
        """Delegates configure() to the outer frame widget."""
        self._frame.configure(**kwargs)


# =============================================================================
# CARD - Elevated Container (Material Design style)
# =============================================================================

class Card:
    """
    Material Design elevated card container with shadow effect.

    Card creates a raised surface with shadow layers to convey elevation,
    following Material Design principles. Supports optional title and
    subtitle headers with consistent spacing and typography.

    Properties:
        Content (Frame): Container frame for adding card body content.
        Title (str): Bold header text displayed at the top.
        Subtitle (str): Secondary text below the title.

    Args:
        master: Parent container for the card.
        title (str): Card title text (optional).
        subtitle (str): Card subtitle text (optional).
        props (dict): Properties including BackgroundColor, Elevation, Padding.

    Example:
        >>> card = Card(page, title='User Profile', subtitle='Account settings')
        >>> Button(card.Content, text='Edit Profile')
    """
    def __init__(self, master, title="", subtitle="", props=None):
        # Default values - WinFormPy style
        defaults = {
            'Title': title,
            'Subtitle': subtitle,
            'BackgroundColor': 'white',
            'Elevation': 2,
            'Padding': 15
        }

        # Apply props over defaults
        if props:
            defaults.update(props)

        self._master = master
        self._title = defaults['Title']
        self._subtitle = defaults['Subtitle']
        self._background_color = defaults['BackgroundColor']
        self._elevation = defaults['Elevation']
        self._padding = defaults['Padding']

        # Determine parent
        if hasattr(master, '_frame'):
            parent = master._frame
        else:
            parent = master

        self._bg = parent.cget("bg")

        # Shadow effect (multiple layers based on elevation)
        shadow_colors = ["#E0E0E0", "#D0D0D0", "#C0C0C0"]
        self._shadow_frames = []

        current_parent = parent
        for i in range(min(self._elevation, len(shadow_colors))):
            shadow = Native.Frame(current_parent, bg=shadow_colors[i])
            shadow.pack(fill=X, pady=(5, 3), padx=(5, 3))
            self._shadow_frames.append(shadow)
            current_parent = shadow

        # Main card frame
        self._frame = Native.Frame(
            current_parent,
            bg=self._background_color,
            bd=0,
            relief=FLAT
        )
        self._frame.pack(fill=X, pady=(0, self._elevation), padx=(0, self._elevation))

        # Header section (if title/subtitle)
        if self._title or self._subtitle:
            self._header = Native.Frame(self._frame, bg=self._background_color)
            self._header.pack(fill=X, padx=self._padding, pady=(self._padding, 5))

            if self._title:
                self._title_label = Native.Label(
                    self._header,
                    text=self._title,
                    font=("Segoe UI", 12, "bold"),
                    bg=self._background_color,
                    fg="#333333",
                    anchor="w"
                )
                self._title_label.pack(fill=X)

            if subtitle:
                self._subtitle_label = Native.Label(
                    self._header,
                    text=subtitle,
                    font=("Segoe UI", 9),
                    bg=self._background_color,
                    fg="#666666",
                    anchor="w"
                )
                self._subtitle_label.pack(fill=X)

        # Content frame
        self._content = Native.Frame(
            self._frame,
            bg=self._background_color,
            padx=self._padding,
            pady=self._padding if not (title or subtitle) else 5
        )
        self._content.pack(fill=BOTH, expand=True)

    @property
    def Content(self):
        """Returns the content frame for adding children."""
        return self._content

    @property
    def Title(self):
        return self._title

    @Title.setter
    def Title(self, value):
        self._title = value
        if hasattr(self, '_title_label'):
            self._title_label.config(text=value)

    @property
    def Subtitle(self):
        return self._subtitle

    @Subtitle.setter
    def Subtitle(self, value):
        self._subtitle = value
        if hasattr(self, '_subtitle_label'):
            self._subtitle_label.config(text=value)


# =============================================================================
# SETTINGSCARD - Settings Option Card
# =============================================================================

class SettingsCard(View):
    """
    Settings card with icon, header, description, and action content.

    SettingsCard provides a consistent way to display settings options with
    an optional icon, title, description, and interactive content on the right.

    Inherits from View (Microsoft.Maui.Controls equivalent).

    Properties:
        Header (str): Primary setting title.
        Description (str): Explanatory text under the title.
        HeaderIcon (str): Emoji or icon text displayed on the left.
        Content (Frame): Container for right-side action (Switch, Button, etc.).
        IsClickEnabled (bool): Whether the card is clickable.
        Click (callable): Event fired when card is clicked.

    Example:
        >>> card = SettingsCard(container, header="Notifications",
        ...                     description="Enable push alerts", icon="\U0001f514")
        >>> switch = Switch(card.Content)
    """

    def __init__(self, master, header="", description="", icon=None,
                 side=TOP, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        defaults = {
            'Header': header,
            'Description': description,
            'HeaderIcon': icon,
            'BackgroundColor': 'white',
            'BorderColor': '#E5E5E5',
            'Padding': (12, 12),
            'IsClickEnabled': False,
            'HoverColor': '#F9F9F9'
        }
        if props:
            defaults.update(props)
        if 'header' in kwargs:
            defaults['Header'] = kwargs['header']
        if 'description' in kwargs:
            defaults['Description'] = kwargs['description']
        if 'icon' in kwargs:
            defaults['HeaderIcon'] = kwargs['icon']

        self._header_text = defaults['Header']
        self._description_text = defaults['Description']
        self._icon_text = defaults['HeaderIcon']
        self._is_click_enabled = defaults['IsClickEnabled']
        self._hover_color = defaults['HoverColor']
        self._bg_color = defaults['BackgroundColor']

        # Main border frame
        self._frame = Native.Frame(
            self._parent,
            bg=defaults['BorderColor'],
            padx=1, pady=1
        )
        self._tk_widget = self._frame

        if not use_grid:
            self._frame.pack(side=side, fill=X, pady=2, padx=2)

        # Inner content frame
        self._inner = Native.Frame(
            self._frame,
            bg=self._bg_color,
            cursor="hand2" if self._is_click_enabled else ""
        )
        self._inner.pack(fill=BOTH, expand=True)

        # Grid layout for internal structure
        self._inner.columnconfigure(1, weight=1)

        # Icon (Column 0)
        self._icon_label = None
        if self._icon_text:
            self._icon_label = Native.Label(
                self._inner,
                text=self._icon_text,
                font=(DEFAULT_FONT_ICONS, 14),
                bg=self._bg_color,
                fg="#333333",
                padx=15
            )
            self._icon_label.grid(row=0, column=0, rowspan=2, sticky="nsew")

        # Text container (Column 1)
        self._text_container = Native.Frame(self._inner, bg=self._bg_color, padx=10, pady=10)
        self._text_container.grid(row=0, column=1, rowspan=2, sticky="w")

        self._header_label = Native.Label(
            self._text_container,
            text=self._header_text,
            font=(DEFAULT_FONT_TEXT, 10, "bold"),
            bg=self._bg_color,
            fg="#1A1A1A",
            anchor="w"
        )
        self._header_label.pack(fill=X)

        self._desc_label = None
        if self._description_text:
            self._desc_label = Native.Label(
                self._text_container,
                text=self._description_text,
                font=(DEFAULT_FONT_TEXT, 9),
                bg=self._bg_color,
                fg="#5E5E5E",
                anchor="w",
                justify=LEFT
            )
            self._desc_label.pack(fill=X)

        # Action content (Column 2)
        self._action_frame = Native.Frame(self._inner, bg=self._bg_color, padx=15)
        self._action_frame.grid(row=0, column=2, rowspan=2, sticky="e")

        # Interactions
        if self._is_click_enabled:
            clickable = [self._inner, self._text_container, self._header_label, self._action_frame]
            if self._icon_label:
                clickable.append(self._icon_label)
            if self._desc_label:
                clickable.append(self._desc_label)
            for w in clickable:
                w.bind("<Button-1>", self._on_card_click)
                w.bind("<Enter>", self._on_enter)
                w.bind("<Leave>", self._on_leave)

    def _on_enter(self, e):
        bg = self._hover_color
        for w in [self._inner, self._text_container, self._header_label, self._action_frame]:
            w.config(bg=bg)
        if self._icon_label:
            self._icon_label.config(bg=bg)
        if self._desc_label:
            self._desc_label.config(bg=bg)

    def _on_leave(self, e):
        bg = self._bg_color
        for w in [self._inner, self._text_container, self._header_label, self._action_frame]:
            w.config(bg=bg)
        if self._icon_label:
            self._icon_label.config(bg=bg)
        if self._desc_label:
            self._desc_label.config(bg=bg)

    def _on_card_click(self, e):
        self.Click(self, EventArgs(e))

    @property
    def Content(self):
        """Returns the frame for adding right-side action controls."""
        return self._action_frame

    @property
    def Header(self):
        return self._header_text

    @Header.setter
    def Header(self, value):
        self._header_text = value
        self._header_label.config(text=value)

    @property
    def Description(self):
        return self._description_text

    @Description.setter
    def Description(self, value):
        self._description_text = value
        if self._desc_label:
            self._desc_label.config(text=value)


############# Notification & Overlay Controls #############

# =============================================================================
# BADGE - Notification Badge
# =============================================================================

class Badge:
    """
    Notification badge for displaying counts or status indicators.

    Badge renders a small pill-shaped indicator typically used to show
    notification counts, status dots, or categorical labels. Automatically
    resizes to fit content while maintaining a minimum circular shape.

    Properties:
        Text (str): Text content displayed in the badge (usually a number).
        BackgroundColor (str): Badge background color (default: '#FF3B30' red).
        IsVisible (bool): Whether the badge is currently displayed.

    Args:
        master: Parent container for the badge.
        text (str): Initial badge text (optional).
        props (dict): Properties including backgroundcolor, textcolor, size.

    Example:
        >>> notification_badge = Badge(icon_container, text='5')
        >>> notification_badge.Text = '99+'  # Update count
        >>> notification_badge.IsVisible = False  # Hide when no notifications
    """
    def __init__(self, master, text="", props=None):
        # Default values - WinFormPy style
        defaults = {
            'Text': text,
            'BackgroundColor': '#FF3B30',
            'TextColor': 'white',
            'Size': 20,
            'Font': ('Segoe UI', 9, 'bold')
        }

        # Apply props over defaults
        if props:
            defaults.update(props)

        self._master = master
        self._text = defaults['Text']
        self._background_color = defaults['BackgroundColor']
        self._text_color = defaults['TextColor']
        self._size = defaults['Size']
        self._font = defaults['Font']

        # Determine parent
        if hasattr(master, '_frame'):
            parent = master._frame
        else:
            parent = master

        self._bg = parent.cget("bg")

        # Calculate dimensions
        self._width = max(self._size, len(str(self._text)) * 8 + 10) if self._text else self._size
        self._height = self._size

        # Canvas for rounded badge
        self._canvas = Native.Canvas(
            parent,
            width=self._width,
            height=self._height,
            bg=self._bg,
            highlightthickness=0
        )
        self._canvas.pack(pady=2)

        self._draw()

    def _draw(self):
        """Draws the badge."""
        self._canvas.delete("all")

        width = self._width
        height = self._height
        radius = height // 2

        # Draw rounded rectangle (pill shape)
        # Top left arc
        self._canvas.create_arc(0, 0, radius*2, height, start=90, extent=180,
                               fill=self._background_color, outline="")
        # Top right arc
        self._canvas.create_arc(width-radius*2, 0, width, height, start=-90, extent=180,
                               fill=self._background_color, outline="")
        # Center rectangle
        self._canvas.create_rectangle(radius, 0, width-radius, height,
                                     fill=self._background_color, outline="")

        # Text
        if self._text:
            self._canvas.create_text(
                width // 2, height // 2,
                text=self._text,
                fill=self._text_color,
                font=("Segoe UI", 9, "bold")
            )

    @property
    def Text(self):
        return self._text

    @Text.setter
    def Text(self, value):
        self._text = str(value)
        self._width = max(self._size, len(self._text) * 8 + 10) if self._text else self._size
        self._canvas.config(width=self._width)
        self._draw()

    @property
    def BackgroundColor(self):
        return self._background_color

    @BackgroundColor.setter
    def BackgroundColor(self, value):
        self._background_color = value
        self._draw()

    @property
    def IsVisible(self):
        return Native.IsViewable(self._canvas)

    @IsVisible.setter
    def IsVisible(self, value):
        if value:
            self._canvas.pack(pady=2)
        else:
            self._canvas.pack_forget()


# =============================================================================
# EXPANDER - Collapsible Panel
# =============================================================================

class Expander:
    """
    Collapsible panel control with expandable/collapsible content section.

    Expander provides a header that users can click to show or hide
    associated content. Features an animated indicator showing the
    current expansion state. Ideal for FAQs, settings groups, and
    information that can be progressively disclosed.

    Properties:
        Content (Frame): Container frame for expandable content.
        Header (str): Text displayed in the clickable header.
        IsExpanded (bool): Current expansion state.
        ExpandedChanged (callable): Event handler called when state changes.

    Methods:
        Expand(): Expands the content panel.
        Collapse(): Collapses the content panel.

    Args:
        master: Parent container for the expander.
        header (str): Header text.
        is_expanded (bool): Initial expansion state (default: False).
        props (dict): Properties including headerbg, contentbg.

    Example:
        >>> details = Expander(page, header='Advanced Options', is_expanded=False)
        >>> CheckBox(details.Content, text='Enable logging')
    """
    def __init__(self, master, header="", is_expanded=False, props=None):
        # Default values - WinFormPy style
        defaults = {
            'Header': header,
            'IsExpanded': is_expanded,
            'HeaderBackColor': '#F5F5F5',
            'ContentBackColor': 'white',
            'HeaderFont': (DEFAULT_FONT_TEXT, 10, 'bold'),
            'HeaderForeColor': '#333333',
            'IndicatorFont': (DEFAULT_FONT_ICONS, 10),
            'IndicatorColor': '#666666',
            'HeaderAlign': 'w',
            'PaddingX': 10,
            'PaddingY': 10
        }

        # Apply props over defaults
        if props:
            defaults.update(props)

        self._master = master
        self._header_text = defaults['Header']
        self._is_expanded = defaults['IsExpanded']
        self._header_bg = defaults['HeaderBackColor']
        self._content_bg = defaults['ContentBackColor']
        self.ExpandedChanged = lambda sender, e: None

        # Determine parent
        if hasattr(master, '_frame'):
            parent = master._frame
        else:
            parent = master

        self._bg = parent.cget("bg")

        # Main container
        self._frame = Native.Frame(parent, bg=self._bg, bd=1, relief=SOLID)
        self._frame.pack(fill=X, pady=5)

        # Header (clickable)
        self._header = Native.Frame(self._frame, bg=self._header_bg, cursor="hand2")
        self._header.pack(fill=X)

        # Expand/Collapse indicator
        self._indicator = Native.Label(
            self._header,
            text="▼" if self._is_expanded else "▶",
            font=defaults['IndicatorFont'],
            bg=self._header_bg,
            fg=defaults['IndicatorColor'],
            padx=defaults['PaddingX'],
            pady=8
        )
        self._indicator.pack(side=LEFT)

        # Header label
        self._header_label = Native.Label(
            self._header,
            text=self._header_text,
            font=defaults['HeaderFont'],
            bg=self._header_bg,
            fg=defaults['HeaderForeColor'],
            anchor=defaults['HeaderAlign'],
            pady=8
        )
        self._header_label.pack(side=LEFT, fill=X, expand=True)

        # Bind click events
        for widget in [self._header, self._indicator, self._header_label]:
            widget.bind("<Button-1>", self._toggle)

        # Content frame
        self._content = Native.Frame(self._frame, bg=self._content_bg,
                                padx=defaults['PaddingX'], pady=defaults['PaddingY'])

        if self._is_expanded:
            self._content.pack(fill=BOTH, expand=True)

    def _toggle(self, event=None):
        """Toggles expanded state."""
        self._is_expanded = not self._is_expanded

        if self._is_expanded:
            self._content.pack(fill=BOTH, expand=True)
            self._indicator.config(text="▼")
        else:
            self._content.pack_forget()
            self._indicator.config(text="▶")

        self.ExpandedChanged(self, EventArgs(self._is_expanded))

    @property
    def Content(self):
        """Returns the content frame for adding children."""
        return self._content

    @property
    def Header(self):
        return self._header_text

    @Header.setter
    def Header(self, value):
        self._header_text = value
        self._header_label.config(text=value)

    @property
    def IsExpanded(self):
        return self._is_expanded

    @IsExpanded.setter
    def IsExpanded(self, value):
        if value != self._is_expanded:
            self._toggle()

    def Expand(self):
        """Expands the panel."""
        if not self._is_expanded:
            self._toggle()

    def Collapse(self):
        """Collapses the panel."""
        if self._is_expanded:
            self._toggle()

    def Show(self, before=None):
        """Shows the expander (re-packs it into the layout).

        Args:
            before: Optional widget reference. If provided, the expander
                    is inserted before this widget in the pack order.
        """
        if before is not None:
            before_frame = before._frame if hasattr(before, '_frame') else before
            self._frame.pack(fill=X, pady=5, before=before_frame)
        else:
            self._frame.pack(fill=X, pady=5)

    def Hide(self):
        """Hides the expander (removes it from layout)."""
        self._frame.pack_forget()

    @property
    def IsVisible(self):
        """Gets whether the expander is currently visible in the layout."""
        return Native.IsViewable(self._frame)

    @IsVisible.setter
    def IsVisible(self, value):
        if value:
            self.Show()
        else:
            self.Hide()


############# Material Design Controls #############

# =============================================================================
# FLOATING ACTION BUTTON (FAB) - Material Design FAB
# =============================================================================

class FloatingActionButton:
    """
    Material Design floating action button (FAB) for primary actions.

    FloatingActionButton creates a prominent circular button typically
    positioned in the bottom-right corner of the screen. Used for the
    primary or most common action on a screen (e.g., compose, add, create).

    Properties:
        Icon (str): Icon character or emoji displayed in the button.
        BackgroundColor (str): Button background color.
        IsVisible (bool): Whether the FAB is currently displayed.
        Clicked (callable): Event handler called when button is clicked.

    Args:
        master: Parent container for the FAB.
        icon (str): Icon to display (default: '+').
        props (dict): Properties including backgroundcolor, foregroundcolor, mini.

    Features:
        - Automatic positioning at bottom-right corner
        - Shadow effect for elevation appearance
        - Hover state with color lightening
        - Mini variant option for secondary actions

    Example:
        >>> fab = FloatingActionButton(page, icon='➕')
        >>> fab.Clicked = lambda: open_create_dialog()
    """
    def __init__(self, master, icon="+", props=None):
        # Default values - WinFormPy style
        defaults = {
            'Icon': icon,
            'BackgroundColor': '#0078D4',
            'ForegroundColor': 'white',
            'Size': 56,
            'Mini': False
        }

        # Apply props over defaults
        if props:
            defaults.update(props)

        self._master = master
        self._icon = defaults['Icon']
        self._background_color = defaults['BackgroundColor']
        self._foreground_color = defaults['ForegroundColor']
        self._size = 40 if defaults['Mini'] else defaults['Size']
        self._mini = defaults['Mini']
        self.Clicked = lambda sender, e: None

        # Get root window for positioning
        if hasattr(master, '_frame'):
            self._root = Native.GetRoot(master._frame) or master._frame
            parent = master._frame
        else:
            self._root = Native.GetRoot(master) or master
            parent = master

        self._bg = parent.cget("bg") if hasattr(parent, 'cget') else "white"

        # Canvas for circular button
        self._canvas = Native.Canvas(
            parent,
            width=self._size,
            height=self._size,
            bg=self._bg,
            highlightthickness=0,
            cursor="hand2"
        )

        # Position at bottom-right using place
        self._canvas.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

        self._draw()

        # Bind events
        self._canvas.bind("<Button-1>", self._on_click)
        self._canvas.bind("<Enter>", self._on_enter)
        self._canvas.bind("<Leave>", self._on_leave)

    def _draw(self, hover=False):
        """Draws the FAB."""
        self._canvas.delete("all")

        size = self._size
        cx = size // 2
        cy = size // 2
        radius = size // 2 - 2

        # Adjust color for hover
        bg_color = self._lighten_color(self._background_color) if hover else self._background_color

        # Draw shadow
        self._canvas.create_oval(
            cx - radius + 2, cy - radius + 2,
            cx + radius + 2, cy + radius + 2,
            fill="#00000033", outline=""
        )

        # Draw circle
        self._canvas.create_oval(
            cx - radius, cy - radius,
            cx + radius, cy + radius,
            fill=bg_color, outline=""
        )

        # Draw icon
        font_size = 20 if not self._mini else 14
        self._canvas.create_text(
            cx, cy,
            text=self._icon,
            fill=self._foreground_color,
            font=("Segoe UI", font_size, "bold")
        )

    def _lighten_color(self, color):
        """Returns a lighter version of the color."""
        # Simple lightening for hover effect
        if color.startswith("#"):
            try:
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
                r = min(255, r + 30)
                g = min(255, g + 30)
                b = min(255, b + 30)
                return f"#{r:02x}{g:02x}{b:02x}"
            except Exception:
                pass
        return color

    def _on_click(self, event):
        """Handles click."""
        self.Clicked(self, EventArgs(event))

    def _on_enter(self, event):
        """Hover enter."""
        self._draw(hover=True)

    def _on_leave(self, event):
        """Hover leave."""
        self._draw(hover=False)

    @property
    def Icon(self):
        return self._icon

    @Icon.setter
    def Icon(self, value):
        self._icon = value
        self._draw()

    @property
    def BackgroundColor(self):
        return self._background_color

    @BackgroundColor.setter
    def BackgroundColor(self, value):
        self._background_color = value
        self._draw()

    @property
    def IsVisible(self):
        return Native.IsViewable(self._canvas)

    @IsVisible.setter
    def IsVisible(self, value):
        if value:
            self._canvas.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")
        else:
            self._canvas.place_forget()


# =============================================================================
# BOTTOMSHEET - Slide-up Panel
# =============================================================================

class BottomSheet:
    """
    Slide-up modal panel anchored to the bottom of the screen.

    BottomSheet provides a surface that slides up from the bottom edge,
    overlaying the main content with a semi-transparent backdrop. Used
    for contextual actions, detail views, and supplementary information
    without leaving the current screen.

    Properties:
        Content (Frame): Container frame for sheet content.
        IsOpen (bool): Whether the bottom sheet is currently visible.
        Title (str): Optional title displayed at the top of the sheet.
        StateChanged (callable): Event handler called when open/close state changes.

    Methods:
        Open(): Slides the bottom sheet into view.
        Close(): Dismisses the bottom sheet.

    Args:
        master: Parent window or container.
        title (str): Header title text (optional).
        props (dict): Properties including height, backgroundcolor.

    Features:
        - Drag handle for touch-like interaction
        - Click-outside-to-dismiss behavior
        - Overlay backdrop for focus

    Example:
        >>> sheet = BottomSheet(app, title='Share via', props={'height': 400})
        >>> Button(sheet.Content, text='Email')
        >>> sheet.Open()
    """
    def __init__(self, master, title="", props=None):
        # Default values - WinFormPy style
        defaults = {
            'Title': title,
            'Height': 300,
            'BackgroundColor': 'white',
            'HandleColor': '#CCCCCC',
            'TitleFont': ('Segoe UI', 14, 'bold'),
            'TitleForeColor': '#333333',
            'PaddingX': 20,
            'PaddingY': 10
        }

        # Apply props over defaults
        if props:
            defaults.update(props)

        self._master = master
        self._title = defaults['Title']
        self._is_open = False
        self._height = defaults['Height']
        self._background_color = defaults['BackgroundColor']
        self.StateChanged = lambda sender, e: None

        # Use centralized WinFormPy utility to resolve the root window
        self._root = get_tk_root(master)

        # Create overlay (semi-transparent background)
        self._overlay = Native.Frame(self._root, bg="#000000")
        self._overlay.bind("<Button-1>", lambda e: self.Close())

        # Sheet frame
        self._sheet = Native.Frame(self._root, bg=self._background_color)

        # Handle bar
        self._handle_frame = Native.Frame(self._sheet, bg=self._background_color, cursor="hand2")
        self._handle_frame.pack(fill=X, pady=10)

        # Draw handle
        self._handle = Native.Canvas(
            self._handle_frame,
            width=40, height=5,
            bg=self._background_color,
            highlightthickness=0
        )
        self._handle.pack()
        self._handle.create_rectangle(0, 0, 40, 5, fill=defaults['HandleColor'], outline="")

        # Title (optional)
        if title:
            self._title_label = Native.Label(
                self._sheet,
                text=title,
                font=("Segoe UI", 14, "bold"),
                bg=self._background_color,
                fg="#333333"
            )
            self._title_label.pack(pady=(0, 10))

        # Content frame
        self._content = Native.Frame(self._sheet, bg=self._background_color, padx=20, pady=10)
        self._content.pack(fill=BOTH, expand=True)

        # Bind handle for dragging
        self._handle_frame.bind("<Button-1>", self._start_drag)
        self._handle.bind("<Button-1>", self._start_drag)

    def _start_drag(self, event):
        """Initiates drag."""
        self._drag_y = event.y_root
        self._handle_frame.bind("<B1-Motion>", self._on_drag)
        self._handle_frame.bind("<ButtonRelease-1>", self._end_drag)

    def _on_drag(self, event):
        """Handles drag motion."""
        delta = event.y_root - self._drag_y
        if delta > 50:  # Threshold to close
            self.Close()

    def _end_drag(self, event):
        """Ends drag."""
        self._handle_frame.unbind("<B1-Motion>")
        self._handle_frame.unbind("<ButtonRelease-1>")

    @property
    def Content(self):
        """Returns the content frame for adding children."""
        return self._content

    @property
    def IsOpen(self):
        return self._is_open

    def Open(self):
        """Opens the bottom sheet."""
        if self._is_open:
            return

        try:
            self._is_open = True

            # Show overlay with transparency effect
            self._overlay.place(x=0, y=0, relwidth=1, relheight=1)
            Native.Lift(self._overlay)

            # Position sheet at bottom
            Native.Update(self._root)
            root_width, root_height = Native.GetSize(self._root)

            self._sheet.place(x=0, y=root_height - self._height,
                             width=root_width, height=self._height)
            Native.Lift(self._sheet)

            self.StateChanged(self, EventArgs(True))
        except (Native.TclError, RuntimeError):
            self._is_open = False

    def Close(self):
        """Closes the bottom sheet."""
        if not self._is_open:
            return

        try:
            self._is_open = False
            self._overlay.place_forget()
            self._sheet.place_forget()

            self.StateChanged(self, EventArgs(False))
        except (Native.TclError, RuntimeError):
            pass

    @property
    def Title(self):
        return self._title

    @Title.setter
    def Title(self, value):
        self._title = value
        if hasattr(self, '_title_label'):
            self._title_label.config(text=value)


# =============================================================================
# AVATAR - Circular Profile Image/Initials
# =============================================================================

class Avatar:
    """
    Circular avatar control displaying user image or initials.

    Avatar renders a circular representation of a user or entity,
    displaying either a profile image or auto-generated initials
    from the provided name. Falls back to a default person icon
    when no image or text is provided.

    Properties:
        Text (str): Name used to generate initials (e.g., 'John Doe' → 'JD').
        BackgroundColor (str): Circle background color for initials mode.
        Size (int): Diameter of the avatar in pixels (default: 40).

    Args:
        master: Parent container for the avatar.
        text (str): Name for generating initials.
        image_path (str): Path to profile image file (optional).
        props (dict): Properties including size, backgroundcolor, textcolor.

    Example:
        >>> avatar = Avatar(header, text='Jane Smith', props={'size': 50})
        >>> avatar.BackgroundColor = '#4CAF50'  # Green background
    """
    def __init__(self, master, text="", image_path=None, props=None):
        # Default values - WinFormPy style
        defaults = {
            'Text': text,
            'ImagePath': image_path,
            'Size': 40,
            'BackgroundColor': '#0078D4',
            'TextColor': 'white',
            'Font': None  # Will be calculated from size
        }

        # Apply props over defaults
        if props:
            defaults.update(props)

        self._master = master
        self._text = defaults['Text']
        self._image_path = defaults['ImagePath']
        self._size = defaults['Size']
        self._background_color = defaults['BackgroundColor']
        self._text_color = defaults['TextColor']
        self._photo_image = None
        self._click_command = None

        # Determine parent
        if hasattr(master, '_frame'):
            parent = master._frame
        else:
            parent = master

        self._bg = parent.cget("bg")

        # Canvas for circular avatar
        self._canvas = Native.Canvas(
            parent,
            width=self._size,
            height=self._size,
            bg=self._bg,
            highlightthickness=0,
            cursor="hand2"
        )
        self._canvas.pack(pady=5)

        # Bind click event
        self._canvas.bind("<Button-1>", self._on_click)

        self._draw()

    def _draw(self):
        """Draws the avatar."""
        self._canvas.delete("all")

        size = self._size
        cx = size // 2
        cy = size // 2
        radius = size // 2 - 1

        # Draw circle
        self._canvas.create_oval(
            cx - radius, cy - radius,
            cx + radius, cy + radius,
            fill=self._background_color, outline=""
        )

        # Draw text (initials) or placeholder
        if self._text:
            initials = self._get_initials(self._text)
            font_size = self._size // 3
            self._canvas.create_text(
                cx, cy,
                text=initials,
                fill=self._text_color,
                font=("Segoe UI", font_size, "bold")
            )
        elif not self._image_path:
            # Default person icon
            font_size = self._size // 3
            self._canvas.create_text(
                cx, cy,
                text="👤",
                font=("Segoe UI", font_size)
            )

    def _get_initials(self, text):
        """Extracts initials from text."""
        words = text.strip().split()
        if len(words) >= 2:
            return (words[0][0] + words[-1][0]).upper()
        elif len(words) == 1 and len(words[0]) >= 2:
            return words[0][:2].upper()
        elif len(words) == 1:
            return words[0][0].upper()
        return ""

    @property
    def Text(self):
        return self._text

    @Text.setter
    def Text(self, value):
        self._text = value
        self._draw()

    @property
    def BackgroundColor(self):
        return self._background_color

    @BackgroundColor.setter
    def BackgroundColor(self, value):
        self._background_color = value
        self._draw()

    @property
    def Size(self):
        return self._size

    @Size.setter
    def Size(self, value):
        self._size = value
        self._canvas.config(width=value, height=value)
        self._draw()

    def _on_click(self, event):
        """Handles click event."""
        if self._click_command:
            self._click_command()

    @property
    def Click(self):
        """Gets or sets the click event handler."""
        return self._click_command

    @Click.setter
    def Click(self, value):
        self._click_command = value


############# Collection & Data Controls #############

# =============================================================================
# INDICATORVIEW - Page Indicator Dots
# =============================================================================

class IndicatorView:
    """
    Page indicator dots for carousel and pager navigation.

    IndicatorView displays a row of circular dots representing pages
    or items in a carousel, with one dot highlighted to show the
    current position. Supports click-to-navigate interaction.

    Properties:
        Count (int): Total number of indicator dots.
        Position (int): Index of the currently selected dot (0-based).
        IndicatorColor (str): Color of unselected dots.
        SelectedColor (str): Color of the selected dot.
        PositionChanged (callable): Event handler called when position changes.

    Args:
        master: Parent container for the indicators.
        count (int): Number of indicator dots (default: 3).
        props (dict): Properties including indicatorcolor, selectedcolor, indicatorsize.

    Example:
        >>> indicators = IndicatorView(carousel_container, count=5)
        >>> indicators.PositionChanged = lambda pos: carousel.go_to(pos)
    """
    def __init__(self, master, count=3, props=None):
        # Default values - WinFormPy style
        defaults = {
            'Count': count,
            'SelectedIndex': 0,
            'IndicatorColor': '#CCCCCC',
            'SelectedColor': '#0078D4',
            'IndicatorSize': 8,
            'Spacing': 6
        }

        # Apply props over defaults
        if props:
            defaults.update(props)

        self._master = master
        self._count = defaults['Count']
        self._selected_index = defaults['SelectedIndex']
        self._indicator_color = defaults['IndicatorColor']
        self._selected_color = defaults['SelectedColor']
        self._indicator_size = defaults['IndicatorSize']
        self._spacing = defaults['Spacing']
        self.PositionChanged = None

        # Determine parent
        if hasattr(master, '_frame'):
            parent = master._frame
        else:
            parent = master

        self._bg = parent.cget("bg")

        # Calculate canvas size
        total_width = self._count * self._indicator_size + (self._count - 1) * self._spacing

        # Canvas
        self._canvas = Native.Canvas(
            parent,
            width=total_width,
            height=self._indicator_size,
            bg=self._bg,
            highlightthickness=0
        )
        self._canvas.pack(pady=10)

        # Bind click for navigation
        self._canvas.bind("<Button-1>", self._on_click)

        self._draw()

    def _draw(self):
        """Draws the indicator dots."""
        self._canvas.delete("all")

        for i in range(self._count):
            x = i * (self._indicator_size + self._spacing) + self._indicator_size // 2
            y = self._indicator_size // 2
            r = self._indicator_size // 2

            color = self._selected_color if i == self._selected_index else self._indicator_color

            self._canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=color, outline=""
            )

    def _on_click(self, event):
        """Handles click to select indicator."""
        # Determine which dot was clicked
        x = event.x
        dot_width = self._indicator_size + self._spacing
        index = int(x / dot_width)

        if 0 <= index < self._count:
            self._selected_index = index
            self._draw()
            if self.PositionChanged:
                self.PositionChanged(index)

    @property
    def Count(self):
        return self._count

    @Count.setter
    def Count(self, value):
        self._count = value
        total_width = value * self._indicator_size + (value - 1) * self._spacing
        self._canvas.config(width=total_width)
        self._draw()

    @property
    def Position(self):
        return self._selected_index

    @Position.setter
    def Position(self, value):
        if 0 <= value < self._count:
            self._selected_index = value
            self._draw()

    @property
    def IndicatorColor(self):
        return self._indicator_color

    @IndicatorColor.setter
    def IndicatorColor(self, value):
        self._indicator_color = value
        self._draw()

    @property
    def SelectedColor(self):
        return self._selected_color

    @SelectedColor.setter
    def SelectedColor(self, value):
        self._selected_color = value
        self._draw()


# =============================================================================
# REFRESHVIEW - Pull-to-Refresh Container
# =============================================================================

class RefreshView:
    """
    Container with pull-to-refresh functionality for refreshable content.

    RefreshView wraps content that can be refreshed by user action,
    displaying an activity indicator while the refresh operation is
    in progress. Simulates mobile pull-to-refresh pattern for desktop.

    Properties:
        Content (Frame): Container frame for refreshable content.
        IsRefreshing (bool): Whether refresh operation is in progress.
        Refreshing (callable): Event handler called when refresh is triggered.

    Methods:
        BeginRefresh(): Shows the refresh indicator and starts refresh state.
        EndRefresh(): Hides the indicator and ends refresh state.
        ShowRefreshButton(show): Toggles visibility of manual refresh button.

    Args:
        master: Parent container for the refresh view.
        props (dict): Properties including refreshcolor.

    Example:
        >>> refresh = RefreshView(page)
        >>> refresh.Refreshing = lambda: load_data_async()
        >>> # When data loading completes:
        >>> refresh.EndRefresh()
    """
    def __init__(self, master, props=None, **kwargs):
        # Default values - WinFormPy style
        defaults = {
            'RefreshColor': '#0078D4',
            'IndicatorSize': 24,
            'ButtonText': '↻ Refresh',
            'IndicatorHeight': 40,
            'BackColor': None
        }

        # Apply props over defaults
        if props:
            defaults.update(props)

        self._master = master
        self._is_refreshing = False
        self._refresh_color = defaults['RefreshColor']
        self.Refreshing = lambda sender, e: None

        # Determine parent
        if hasattr(master, '_frame'):
            parent = master._frame
        else:
            parent = master

        self._bg = defaults['BackColor'] if defaults['BackColor'] else parent.cget("bg")

        # Main frame
        self._frame = Native.Frame(parent, bg=self._bg, **kwargs)
        self._frame.pack(fill=BOTH, expand=True)

        # Refresh indicator (hidden initially)
        self._indicator_frame = Native.Frame(self._frame, bg=self._bg, height=defaults['IndicatorHeight'])

        self._indicator = ActivityIndicator(self._indicator_frame, props={
            'Color': self._refresh_color,
            'Size': defaults['IndicatorSize']
        })

        # Content frame
        self._content = Native.Frame(self._frame, bg=self._bg)
        self._content.pack(fill=BOTH, expand=True)

        # Refresh button (simulates pull)
        self._refresh_btn = Native.Button(self._frame, text=defaults['ButtonText'], command=self._on_refresh)
        self._refresh_btn.pack(side=TOP, pady=5)
        self._refresh_btn.pack_forget()  # Hidden by default

    def _on_refresh(self):
        """Triggers refresh."""
        if not self._is_refreshing:
            self.BeginRefresh()
            self.Refreshing(self, EventArgs())

    @property
    def Content(self):
        """Returns the content frame for adding children."""
        return self._content

    @property
    def IsRefreshing(self):
        return self._is_refreshing

    @IsRefreshing.setter
    def IsRefreshing(self, value):
        if value:
            self.BeginRefresh()
        else:
            self.EndRefresh()

    def BeginRefresh(self):
        """Shows refresh indicator."""
        if self._is_refreshing:
            return

        self._is_refreshing = True
        self._indicator_frame.pack(side=TOP, fill=X, before=self._content)
        self._indicator.Start()

    def EndRefresh(self):
        """Hides refresh indicator."""
        if not self._is_refreshing:
            return

        self._is_refreshing = False
        self._indicator.Stop()
        self._indicator_frame.pack_forget()

    def ShowRefreshButton(self, show=True):
        """Shows or hides the refresh button."""
        if show:
            self._refresh_btn.pack(side=TOP, pady=5, before=self._content)
        else:
            self._refresh_btn.pack_forget()


# =============================================================================
# COLLECTIONVIEW - Templated List/Grid View
# =============================================================================

class CollectionView:
    """
    Templated collection control for displaying lists and grids of data.

    CollectionView renders a scrollable collection of items using a
    customizable item template. Supports vertical list, horizontal list,
    and grid layouts with single or multiple selection modes.

    Properties:
        ItemsSource (list): Data collection to display.
        SelectedItem (any): Currently selected item (single selection mode).
        SelectedItems (list): List of selected items (multiple selection mode).
        SelectedIndex (int): Index of the selected item.
        SelectionChanged (callable): Event handler for selection changes.
        ItemTapped (callable): Event handler called when an item is tapped.

    Args:
        master: Parent container for the collection view.
        items (list): Initial data items.
        item_template (callable): Function(parent, item) to render each item.
        props (dict): Properties including LayoutMode ('vertical', 'horizontal', 'grid'),
                     GridColumns, ItemHeight, SelectionMode ('none', 'single', 'multiple').

    Example:
        >>> def render_item(parent, item):
        ...     Label(parent, text=item['name'])
        >>>
        >>> collection = CollectionView(page, items=data, item_template=render_item)
        >>> collection.ItemTapped = lambda idx, item: show_detail(item)
    """
    def __init__(self, master, items=None, item_template=None, props=None):
        # Default values - WinFormPy style
        defaults = {
            'Items': items or [],
            'LayoutMode': 'vertical',
            'GridColumns': 2,
            'ItemHeight': 60,
            'SelectionMode': 'single'
        }

        # Apply props over defaults
        if props:
            defaults.update(props)

        self._master = master
        self._items = defaults['Items']
        self._item_template = item_template  # Callback(parent, item) -> widget
        self._layout_mode = defaults['LayoutMode']
        self._grid_columns = defaults['GridColumns']
        self._item_height = defaults['ItemHeight']
        self._selection_mode = defaults['SelectionMode']
        self._selected_indices = []
        self.SelectionChanged = None
        self.ItemTapped = None

        # Determine parent
        if hasattr(master, '_frame'):
            parent = master._frame
        else:
            parent = master

        self._bg = parent.cget("bg")

        # Main frame with scrollbar
        self._frame = Native.Frame(parent, bg=self._bg)
        self._frame.pack(fill=BOTH, expand=True, pady=5)

        # Canvas for scrolling
        self._canvas = Native.Canvas(self._frame, bg=self._bg, highlightthickness=0)
        self._scrollbar = Native.Scrollbar(self._frame, orient="vertical", command=self._canvas.yview)

        self._scrollable_frame = Native.Frame(self._canvas, bg=self._bg)

        self._scrollable_frame.bind(
            "<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        )

        self._canvas.create_window((0, 0), window=self._scrollable_frame, anchor="nw")
        self._canvas.configure(yscrollcommand=self._scrollbar.set)

        # Pack
        self._scrollbar.pack(side=RIGHT, fill=Y)
        self._canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Mouse wheel binding
        self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Render items
        self._item_widgets = []
        self._render_items()

    def _on_mousewheel(self, event):
        """Handles mouse wheel scrolling."""
        self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _render_items(self):
        """Renders all items."""
        # Clear existing
        for widget in Native.GetChildren(self._scrollable_frame):
            Native.Destroy(widget)
        self._item_widgets.clear()

        if self._layout_mode == "grid":
            self._render_grid()
        else:
            self._render_list()

    def _render_list(self):
        """Renders items as list."""
        for idx, item in enumerate(self._items):
            item_frame = Native.Frame(
                self._scrollable_frame,
                bg="white",
                height=self._item_height,
                bd=1,
                relief=SOLID
            )

            if self._layout_mode == "horizontal":
                item_frame.pack(side=LEFT, padx=2, pady=2)
            else:
                item_frame.pack(fill=X, padx=2, pady=2)

            Native.PackPropagate(item_frame, False)

            # Use template or default
            if self._item_template:
                self._item_template(item_frame, item)
            else:
                self._default_template(item_frame, item)

            # Bind click
            item_frame.bind("<Button-1>", lambda e, i=idx: self._on_item_click(i))
            for child in Native.GetChildren(item_frame):
                child.bind("<Button-1>", lambda e, i=idx: self._on_item_click(i))

            self._item_widgets.append(item_frame)

    def _render_grid(self):
        """Renders items as grid."""
        row = 0
        col = 0

        for idx, item in enumerate(self._items):
            item_frame = Native.Frame(
                self._scrollable_frame,
                bg="white",
                height=self._item_height,
                bd=1,
                relief=SOLID
            )
            item_frame.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            Native.PackPropagate(item_frame, False)

            # Use template or default
            if self._item_template:
                self._item_template(item_frame, item)
            else:
                self._default_template(item_frame, item)

            # Bind click
            item_frame.bind("<Button-1>", lambda e, i=idx: self._on_item_click(i))
            for child in Native.GetChildren(item_frame):
                child.bind("<Button-1>", lambda e, i=idx: self._on_item_click(i))

            self._item_widgets.append(item_frame)

            col += 1
            if col >= self._grid_columns:
                col = 0
                row += 1

        # Configure grid columns
        for c in range(self._grid_columns):
            self._scrollable_frame.columnconfigure(c, weight=1)

    def _default_template(self, parent, item):
        """Default item template."""
        text = str(item) if not isinstance(item, dict) else item.get('title', str(item))
        label = Native.Label(parent, text=text, bg="white", anchor="w", padx=10)
        label.pack(fill=BOTH, expand=True)

    def _on_item_click(self, index):
        """Handles item click."""
        if self._selection_mode == "none":
            pass
        elif self._selection_mode == "single":
            # Deselect previous
            for i, widget in enumerate(self._item_widgets):
                widget.config(bg="white")
                for child in Native.GetChildren(widget):
                    child.config(bg="white")
            # Select new
            self._selected_indices = [index]
            self._item_widgets[index].config(bg="#E3F2FD")
            for child in Native.GetChildren(self._item_widgets[index]):
                child.config(bg="#E3F2FD")
        elif self._selection_mode == "multiple":
            if index in self._selected_indices:
                self._selected_indices.remove(index)
                self._item_widgets[index].config(bg="white")
                for child in Native.GetChildren(self._item_widgets[index]):
                    child.config(bg="white")
            else:
                self._selected_indices.append(index)
                self._item_widgets[index].config(bg="#E3F2FD")
                for child in Native.GetChildren(self._item_widgets[index]):
                    child.config(bg="#E3F2FD")

        if self.ItemTapped:
            self.ItemTapped(index, self._items[index])

        if self.SelectionChanged:
            self.SelectionChanged(self._selected_indices)

    @property
    def ItemsSource(self):
        return self._items

    @ItemsSource.setter
    def ItemsSource(self, value):
        self._items = value or []
        self._selected_indices.clear()
        self._render_items()

    @property
    def SelectedItem(self):
        if self._selected_indices:
            return self._items[self._selected_indices[0]]
        return None

    @property
    def SelectedItems(self):
        return [self._items[i] for i in self._selected_indices]

    @property
    def SelectedIndex(self):
        return self._selected_indices[0] if self._selected_indices else -1

    @SelectedIndex.setter
    def SelectedIndex(self, value):
        if 0 <= value < len(self._items):
            self._on_item_click(value)


############# Navigation Bar Controls #############

# =============================================================================
# TOOLBAR - Toolbar with Actions
# =============================================================================

class Toolbar:
    """
    Horizontal toolbar control for grouping action buttons and tools.

    Toolbar provides a container for action items with icons and labels,
    positioned at the top or bottom of a page. Supports separators and
    spacers for organizing toolbar items into logical groups.

    Properties:
        BackgroundColor (str): Toolbar background color.

    Methods:
        AddItem(icon, text, command, is_primary): Adds a toolbar action item.
        AddSeparator(): Adds a vertical separator line.
        AddSpacer(): Adds expandable space to push items apart.
        RemoveItem(index): Removes a toolbar item by index.

    Args:
        master: Parent container for the toolbar.
        props (dict): Properties including BackgroundColor, Position ('top', 'bottom').

    Example:
        >>> toolbar = Toolbar(page, props={'Position': 'top'})
        >>> toolbar.AddItem('💾', 'Save', save_document)
        >>> toolbar.AddSeparator()
        >>> toolbar.AddItem('✂️', 'Cut', cut_selection)
    """
    def __init__(self, master, props=None):
        # Default values - WinFormPy style
        defaults = {
            'BackgroundColor': '#F5F5F5',
            'Position': 'top'
        }

        # Apply props over defaults
        if props:
            defaults.update(props)

        self._master = master
        self._items = []
        self._background_color = defaults['BackgroundColor']
        self._position = defaults['Position']

        # Determine parent
        if hasattr(master, '_frame'):
            parent = master._frame
        else:
            parent = master

        self._bg = parent.cget("bg")

        # Toolbar frame
        self._frame = Native.Frame(parent, bg=self._background_color, height=44)

        if self._position == "bottom":
            self._frame.pack(side=BOTTOM, fill=X)
        else:
            self._frame.pack(side=TOP, fill=X)

        Native.PackPropagate(self._frame, False)

        # Items container
        self._items_frame = Native.Frame(self._frame, bg=self._background_color)
        self._items_frame.pack(fill=BOTH, expand=True)

    def AddItem(self, icon="", text="", command=None, is_primary=False):
        """Adds a toolbar item."""
        item_frame = Native.Frame(self._items_frame, bg=self._background_color, cursor="hand2")

        if is_primary:
            item_frame.pack(side=RIGHT, padx=10)
        else:
            item_frame.pack(side=LEFT, padx=10)

        # Icon
        if icon:
            icon_label = Native.Label(
                item_frame,
                text=icon,
                font=("Segoe UI", 14),
                bg=self._background_color
            )
            icon_label.pack(side=TOP if text else LEFT)
            icon_label.bind("<Button-1>", lambda e: command() if command else None)

        # Text
        if text:
            text_label = Native.Label(
                item_frame,
                text=text,
                font=("Segoe UI", 9),
                bg=self._background_color,
                fg="#333333"
            )
            text_label.pack(side=TOP if icon else LEFT)
            text_label.bind("<Button-1>", lambda e: command() if command else None)

        item_frame.bind("<Button-1>", lambda e: command() if command else None)

        self._items.append({
            'frame': item_frame,
            'icon': icon,
            'text': text,
            'command': command
        })

        return len(self._items) - 1

    def AddSeparator(self):
        """Adds a separator."""
        sep = Native.Frame(self._items_frame, bg="#CCCCCC", width=1)
        sep.pack(side=LEFT, fill=Y, padx=5, pady=8)

    def AddSpacer(self):
        """Adds expandable spacer."""
        spacer = Native.Frame(self._items_frame, bg=self._background_color)
        spacer.pack(side=LEFT, fill=BOTH, expand=True)

    def RemoveItem(self, index):
        """Removes toolbar item by index."""
        if 0 <= index < len(self._items):
            Native.Destroy(self._items[index]['frame'])
            del self._items[index]

    @property
    def BackgroundColor(self):
        return self._background_color

    @BackgroundColor.setter
    def BackgroundColor(self, value):
        self._background_color = value
        self._frame.config(bg=value)
        self._items_frame.config(bg=value)


# =============================================================================
# BOTTOMNAVIGATIONBAR - Bottom Navigation
# =============================================================================

class BottomNavigationBar:
    """
    Material Design bottom navigation bar for app-level navigation.

    BottomNavigationBar provides a fixed navigation bar at the bottom
    of the screen with icon/label items for switching between primary
    destinations. Highlights the selected item and supports click handlers.

    Properties:
        SelectedIndex (int): Index of the currently selected navigation item.
        SelectedIndexChanged (callable): Event handler for navigation changes.

    Methods:
        AddItem(icon, label, command): Adds a navigation destination.

    Args:
        master: Parent container for the navigation bar.
        props (dict): Properties including BackgroundColor, SelectedColor, UnselectedColor.

    Features:
        - Fixed height (56px) per Material Design specs
        - Top border for visual separation
        - Color-coded selected/unselected states

    Example:
        >>> nav = BottomNavigationBar(app)
        >>> nav.AddItem('🏠', 'Home', lambda: show_page('home'))
        >>> nav.AddItem('🔍', 'Search', lambda: show_page('search'))
        >>> nav.AddItem('👤', 'Profile', lambda: show_page('profile'))
    """
    def __init__(self, master, props=None):
        # Default values - WinFormPy style
        defaults = {
            'BackgroundColor': 'white',
            'SelectedColor': '#0078D4',
            'UnselectedColor': '#666666',
            'SelectedIndex': 0
        }

        # Apply props over defaults
        if props:
            defaults.update(props)

        self._master = master
        self._items = []
        self._selected_index = defaults['SelectedIndex']
        self._background_color = defaults['BackgroundColor']
        self._selected_color = defaults['SelectedColor']
        self._unselected_color = defaults['UnselectedColor']
        self.SelectedIndexChanged = None

        # Determine parent
        if hasattr(master, '_frame'):
            parent = master._frame
        else:
            parent = master

        # Navigation bar frame
        self._frame = Native.Frame(parent, bg=self._background_color, height=56, bd=0)
        self._frame.pack(side=BOTTOM, fill=X)
        Native.PackPropagate(self._frame, False)

        # Top border
        self._border = Native.Frame(self._frame, bg="#E0E0E0", height=1)
        self._border.pack(side=TOP, fill=X)

        # Items container
        self._items_frame = Native.Frame(self._frame, bg=self._background_color)
        self._items_frame.pack(fill=BOTH, expand=True)

    def AddItem(self, icon="", label="", command=None):
        """Adds a navigation item."""
        index = len(self._items)

        item_frame = Native.Frame(self._items_frame, bg=self._background_color, cursor="hand2")
        item_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Icon
        color = self._selected_color if index == self._selected_index else self._unselected_color
        icon_label = Native.Label(
            item_frame,
            text=icon,
            font=("Segoe UI", 16),
            bg=self._background_color,
            fg=color
        )
        icon_label.pack(pady=(8, 2))

        # Label
        text_label = Native.Label(
            item_frame,
            text=label,
            font=("Segoe UI", 9),
            bg=self._background_color,
            fg=color
        )
        text_label.pack()

        # Store item
        self._items.append({
            'frame': item_frame,
            'icon_label': icon_label,
            'text_label': text_label,
            'command': command
        })

        # Bind click
        for widget in [item_frame, icon_label, text_label]:
            widget.bind("<Button-1>", lambda e, i=index: self._on_item_click(i))

        return index

    def _on_item_click(self, index):
        """Handles item click."""
        if index == self._selected_index:
            return

        # Update colors
        for i, item in enumerate(self._items):
            color = self._selected_color if i == index else self._unselected_color
            item['icon_label'].config(fg=color)
            item['text_label'].config(fg=color)

        self._selected_index = index

        # Execute command
        if self._items[index]['command']:
            self._items[index]['command']()

        if self.SelectedIndexChanged:
            self.SelectedIndexChanged(index)

    @property
    def SelectedIndex(self):
        return self._selected_index

    @SelectedIndex.setter
    def SelectedIndex(self, value):
        if 0 <= value < len(self._items):
            self._on_item_click(value)


# =============================================================================
# ITEMSREPEATER - Collection Display Control
# =============================================================================

class ItemsRepeater:
    """
    WinUI3-style ItemsRepeater for displaying a collection of items using a template.

    ItemsRepeater takes a list of data items and a template function to render
    each item into a layout.

    Properties:
        ItemsSource (list): The collection of data items to display.
        ItemTemplate (callable): Function that takes (parent, item_data) and returns a control.
    """
    def __init__(self, master, items_source=None, item_template=None, props=None):
        defaults = {
            'Spacing': 10,
            'Padding': (0, 0, 0, 0),
            'Orientation': 'vertical' # horizontal or vertical
        }
        if props: defaults.update(props)

        self._master = master
        self._items_source = items_source or []
        self._item_template = item_template
        self._spacing = defaults['Spacing']
        self._padding = defaults['Padding']
        self._orientation = defaults['Orientation']

        # Determine parent
        if hasattr(master, '_frame'):
            parent = master._frame
        else:
            parent = master

        self._bg = parent.cget("bg")

        # Layout container
        if self._orientation == 'horizontal':
            self._layout = HorizontalStackLayout(parent, props={'Spacing': self._spacing, 'Padding': self._padding})
        else:
            self._layout = VerticalStackLayout(parent, props={'Spacing': self._spacing, 'Padding': self._padding})

        self._tk_widget = self._layout._frame

        if self._items_source:
            self.Reload()

    def Reload(self):
        """Re-renders all items from ItemsSource."""
        # Clear existing
        for child in Native.GetChildren(self._layout._frame):
            Native.Destroy(child)

        if not self._item_template:
            return

        for item in self._items_source:
            self._item_template(self._layout, item)

    @property
    def ItemsSource(self):
        return self._items_source

    @ItemsSource.setter
    def ItemsSource(self, value):
        self._items_source = value
        self.Reload()

    @property
    def ItemTemplate(self):
        return self._item_template

    @ItemTemplate.setter
    def ItemTemplate(self, value):
        self._item_template = value
        self.Reload()


# =============================================================================
# FONTICON - Icon Glyph Display
# =============================================================================

class FontIcon(View):
    """
    Displays a single glyph from an icon font.

    FontIcon renders a Unicode glyph character using a specified font family,
    commonly used with icon fonts like Segoe Fluent Icons, Segoe MDL2 Assets,
    or Font Awesome.

    Inherits from View (Microsoft.Maui.Controls.FontIcon equivalent).

    Properties:
        Glyph (str): Unicode character to display (e.g. '\\uE710').
        FontFamily (str): Icon font family name.
        FontSize (int): Size of the glyph in points.
        ForeColor (str): Glyph color in hex format.

    Example:
        >>> icon = FontIcon(container, glyph='\\uE710', font_size=16)
        >>> icon.ForeColor = '#0078D4'
    """

    # Common Segoe Fluent Icons glyphs for convenience
    GLYPHS = {
        'Home': '\uE80F', 'Settings': '\uE713', 'Search': '\uE721',
        'Add': '\uE710', 'Delete': '\uE74D', 'Edit': '\uE70F',
        'Save': '\uE74E', 'Cancel': '\uE711', 'Back': '\uE72B',
        'Forward': '\uE72A', 'Up': '\uE74A', 'Down': '\uE74B',
        'Refresh': '\uE72C', 'Mail': '\uE715', 'Calendar': '\uE787',
        'People': '\uE716', 'Phone': '\uE717', 'Pin': '\uE718',
        'Link': '\uE71B', 'Filter': '\uE71C', 'Zoom': '\uE71E',
        'Camera': '\uE722', 'Attach': '\uE723', 'Send': '\uE724',
        'Copy': '\uE8C8', 'Paste': '\uE77F', 'Cut': '\uE8C6',
        'Undo': '\uE7A7', 'Redo': '\uE7A6', 'Share': '\uE72D',
        'Download': '\uE896', 'Upload': '\uE898', 'Folder': '\uE8B7',
        'Document': '\uE8A5', 'Print': '\uE749', 'Lock': '\uE72E',
        'Unlock': '\uE785', 'Heart': '\uEB51', 'Star': '\uE734',
        'Warning': '\uE7BA', 'Info': '\uE946', 'Error': '\uEA39',
        'CheckMark': '\uE73E', 'Globe': '\uE774', 'Cloud': '\uE753',
        'Network': '\uE968', 'Database': '\uEE94', 'Key': '\uE8D7',
        'User': '\uE77B', 'Admin': '\uE7EF', 'Group': '\uE902',
        'Notification': '\uEA8F', 'Volume': '\uE767', 'Mute': '\uE74F',
        'Play': '\uE768', 'Pause': '\uE769', 'Stop': '\uE71A',
    }

    def __init__(self, master, glyph="\uE710", font_family="Segoe MDL2 Assets",
                 font_size=14, side=TOP, use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        defaults = {
            'Glyph': glyph,
            'FontFamily': font_family,
            'FontSize': font_size,
            'ForeColor': '#333333',
            'BackColor': None,
        }
        if props:
            defaults.update(props)
        if 'fg' in kwargs:
            defaults['ForeColor'] = kwargs['fg']
        if 'bg' in kwargs:
            defaults['BackColor'] = kwargs['bg']

        bg_color = defaults['BackColor'] if defaults['BackColor'] else self._get_parent_bg()

        self._tk_widget = Native.Label(
            self._parent,
            text=defaults['Glyph'],
            font=(defaults['FontFamily'], defaults['FontSize']),
            fg=defaults['ForeColor'],
            bg=bg_color,
        )

        if not use_grid:
            self._tk_widget.pack(side=side, anchor="w")

        self._bind_standard_events()

    @property
    def Glyph(self):
        """Gets or sets the Unicode glyph character."""
        return self._tk_widget.cget("text")

    @Glyph.setter
    def Glyph(self, value):
        self._tk_widget.configure(text=value)

    @property
    def FontFamily(self):
        """Gets the font family name."""
        return self._tk_widget.cget("font")[0] if isinstance(self._tk_widget.cget("font"), tuple) else str(self._tk_widget.cget("font"))

    @FontFamily.setter
    def FontFamily(self, value):
        current = self._tk_widget.cget("font")
        size = current[1] if isinstance(current, tuple) and len(current) > 1 else 14
        self._tk_widget.configure(font=(value, size))

    @property
    def FontSize(self):
        """Gets or sets the glyph font size."""
        current = self._tk_widget.cget("font")
        return current[1] if isinstance(current, tuple) and len(current) > 1 else 14

    @FontSize.setter
    def FontSize(self, value):
        current = self._tk_widget.cget("font")
        family = current[0] if isinstance(current, tuple) else str(current)
        self._tk_widget.configure(font=(family, value))

    @property
    def ForeColor(self):
        return self._tk_widget.cget("fg")

    @ForeColor.setter
    def ForeColor(self, value):
        self._tk_widget.configure(fg=value)


# =============================================================================
# SYMBOLICON - Predefined Symbol Display
# =============================================================================

class SymbolIcon(FontIcon):
    """
    Displays a predefined symbol icon by name.

    SymbolIcon is a convenience wrapper over FontIcon that maps symbol names
    to their Unicode glyph values, following the WinUI Symbol enum pattern.
    Uses Segoe MDL2 Assets font for rendering.

    Inherits from FontIcon.

    Properties:
        Symbol (str): Symbol name from the predefined set (e.g. 'Home', 'Settings').

    Available symbols:
        Home, Settings, Search, Add, Delete, Edit, Save, Cancel, Back, Forward,
        Up, Down, Refresh, Mail, Calendar, People, Phone, Pin, Link, Filter,
        Zoom, Camera, Attach, Send, Copy, Paste, Cut, Undo, Redo, Share,
        Download, Upload, Folder, Document, Print, Lock, Unlock, Heart, Star,
        Warning, Info, Error, CheckMark, Globe, Cloud, Network, Database, Key,
        User, Admin, Group, Notification, Volume, Mute, Play, Pause, Stop.

    Example:
        >>> icon = SymbolIcon(container, symbol='Home', font_size=18)
        >>> icon.ForeColor = '#0078D4'
    """

    def __init__(self, master, symbol="Home", font_size=14,
                 side=TOP, use_grid=False, props=None, **kwargs):
        glyph = FontIcon.GLYPHS.get(symbol, symbol)
        super().__init__(
            master, glyph=glyph, font_family="Segoe MDL2 Assets",
            font_size=font_size, side=side, use_grid=use_grid, props=props, **kwargs
        )
        self._symbol_name = symbol

    @property
    def Symbol(self):
        """Gets or sets the symbol name."""
        return self._symbol_name

    @Symbol.setter
    def Symbol(self, value):
        self._symbol_name = value
        self.Glyph = FontIcon.GLYPHS.get(value, value)


# =============================================================================
# TOGGLESWITCH - Toggle Switch with Label
# =============================================================================

class ToggleSwitch(View):
    """
    On/off toggle switch control with text label.

    ToggleSwitch combines a sliding toggle with a text header label,
    following the WinUI3 ToggleSwitch pattern. It extends the basic
    Switch with Header text, OnContent/OffContent status labels,
    and a capsule-style visual design.

    Inherits from View.

    Properties:
        IsOn (bool): Current toggle state.
        Header (str): Label text displayed next to the switch.
        OnContent (str): Text shown when switch is ON (default: 'On').
        OffContent (str): Text shown when switch is OFF (default: 'Off').
        OnColor (str): Track color when ON.
        Toggled (callable): Event fired when state changes.

    Example:
        >>> toggle = ToggleSwitch(container, header="Dark Mode")
        >>> toggle.Toggled = lambda sender, e: apply_theme(toggle.IsOn)
    """

    def __init__(self, master, header="", is_on=False, side=TOP,
                 use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        defaults = {
            'IsOn': is_on,
            'Header': header,
            'OnContent': 'On',
            'OffContent': 'Off',
            'OnColor': '#0078D4',
            'OffColor': '#CCCCCC',
            'ThumbColor': 'white',
            'Font': (DEFAULT_FONT_TEXT, 11),
            'ForeColor': '#333333',
        }
        if props:
            defaults.update(props)

        self._is_on = defaults['IsOn']
        self._on_content = defaults['OnContent']
        self._off_content = defaults['OffContent']
        self._on_color = defaults['OnColor']
        self._off_color = defaults['OffColor']
        self._thumb_color = defaults['ThumbColor']

        # Events
        self.Toggled = lambda sender, e: None

        bg = self._get_parent_bg()

        # Container frame
        self._container = Native.Frame(self._parent, bg=bg, bd=0, highlightthickness=0)
        self._tk_widget = self._container

        if not use_grid:
            self._container.pack(side=side, anchor="w", fill=X, pady=4)

        # Header label (left)
        self._header_label = Native.Label(
            self._container, text=defaults['Header'],
            font=defaults['Font'], fg=defaults['ForeColor'], bg=bg, anchor="w"
        )
        self._header_label.pack(side=LEFT, padx=(0, 12))

        # Switch canvas (capsule style)
        self._switch_w, self._switch_h = 44, 22
        self._canvas = Native.Canvas(
            self._container, width=self._switch_w, height=self._switch_h,
            bg=bg, highlightthickness=0, cursor="hand2"
        )
        self._canvas.pack(side=LEFT)

        # Status label (right of switch)
        self._status_label = Native.Label(
            self._container, text="", font=(DEFAULT_FONT_TEXT, 10),
            fg="#888888", bg=bg, anchor="w"
        )
        self._status_label.pack(side=LEFT, padx=(8, 0))

        # Draw and bind
        self._draw()
        self._canvas.bind("<Button-1>", self._on_click)
        self._header_label.bind("<Button-1>", self._on_click)
        _bind_standard_mouse_events(self._container, self)

    def _draw(self):
        """Redraws the switch capsule."""
        self._canvas.delete("all")
        w, h = self._switch_w, self._switch_h
        r = h // 2

        fill = self._on_color if self._is_on else self._off_color
        outline = fill

        # Capsule background
        self._canvas.create_oval(0, 0, h, h, fill=fill, outline=outline)
        self._canvas.create_oval(w - h, 0, w, h, fill=fill, outline=outline)
        self._canvas.create_rectangle(r, 0, w - r, h, fill=fill, outline=fill)

        if not self._is_on:
            # Hollow style for OFF: draw inner oval to create border effect
            inner = 2
            inner_bg = self._canvas.cget("bg")
            self._canvas.create_oval(inner, inner, h - inner, h - inner, fill=inner_bg, outline=inner_bg)
            self._canvas.create_oval(w - h + inner, inner, w - inner, h - inner, fill=inner_bg, outline=inner_bg)
            self._canvas.create_rectangle(r, inner, w - r, h - inner, fill=inner_bg, outline=inner_bg)
            # Redraw border
            self._canvas.create_oval(0, 0, h, h, fill='', outline=self._off_color, width=2)
            self._canvas.create_oval(w - h, 0, w, h, fill='', outline=self._off_color, width=2)
            self._canvas.create_rectangle(r, 0, w - r, 2, fill=self._off_color, outline=self._off_color)
            self._canvas.create_rectangle(r, h - 2, w - r, h, fill=self._off_color, outline=self._off_color)

        # Knob
        knob_r = 7
        if self._is_on:
            cx = w - r
        else:
            cx = r
        cy = h // 2
        knob_color = self._thumb_color if self._is_on else self._off_color
        self._canvas.create_oval(cx - knob_r, cy - knob_r, cx + knob_r, cy + knob_r,
                                 fill=knob_color, outline=knob_color)

        # Update status text
        self._status_label.configure(
            text=self._on_content if self._is_on else self._off_content
        )

    def _on_click(self, event=None):
        self._is_on = not self._is_on
        self._draw()
        self.Toggled(self, EventArgs(event))
        self.Click(self, EventArgs(event))

    @property
    def IsOn(self):
        return self._is_on

    @IsOn.setter
    def IsOn(self, value):
        if self._is_on != value:
            self._is_on = value
            self._draw()

    @property
    def Header(self):
        return self._header_label.cget("text")

    @Header.setter
    def Header(self, value):
        self._header_label.configure(text=value)

    @property
    def OnContent(self):
        return self._on_content

    @OnContent.setter
    def OnContent(self, value):
        self._on_content = value
        self._draw()

    @property
    def OffContent(self):
        return self._off_content

    @OffContent.setter
    def OffContent(self, value):
        self._off_content = value
        self._draw()

    @property
    def OnColor(self):
        return self._on_color

    @OnColor.setter
    def OnColor(self, value):
        self._on_color = value
        self._draw()


# =============================================================================
# BREADCRUMBBAR - Navigation Path Control
# =============================================================================

class BreadcrumbBar(View):
    """
    BreadcrumbBar for displaying the navigation path.

    BreadcrumbBar renders a horizontal row of clickable path segments
    separated by chevron characters. The last segment is highlighted
    as the current (active) location.

    Inherits from View (Microsoft.Maui.Controls equivalent).

    Properties:
        ItemsSource (list): List of strings representing the path.
        ItemClicked (callable): Event handler called when a segment is clicked.

    Example:
        >>> bc = BreadcrumbBar(container, items_source=["Home", "Documents", "Finance"])
        >>> bc.ItemClicked = lambda sender, e: print(f"Clicked index {e.Data}")
    """

    def __init__(self, master, items_source=None, side=TOP,
                 use_grid=False, props=None, **kwargs):
        super().__init__(master, side=side, use_grid=use_grid)

        defaults = {
            'Separator': "  \u203a  ",
            'FontSize': 10,
            'TextColor': '#5E5E5E',
            'ActiveColor': '#1A1A1A',
            'Padding': (0, 5, 0, 15)
        }
        if props:
            defaults.update(props)

        self._items_source = items_source or []
        self._separator = defaults['Separator']
        self._font_size = defaults['FontSize']
        self._text_color = defaults['TextColor']
        self._active_color = defaults['ActiveColor']

        self.ItemClicked = lambda sender, e: None

        bg = self._get_parent_bg()

        # Main container
        self._frame = Native.Frame(self._parent, bg=bg)
        self._tk_widget = self._frame

        if not use_grid:
            self._frame.pack(side=side, fill=X,
                             padx=defaults['Padding'][0], pady=defaults['Padding'][1])

        self._render()

    def _render(self):
        """Renders the breadcrumb segments."""
        for child in self._frame.winfo_children():
            child.destroy()

        bg = self._frame.cget("bg")

        for i, item in enumerate(self._items_source):
            is_last = (i == len(self._items_source) - 1)

            fg = self._active_color if is_last else self._text_color
            cursor = "" if is_last else "hand2"
            weight = "bold" if is_last else "normal"

            lbl = Native.Label(
                self._frame,
                text=str(item),
                font=(DEFAULT_FONT_TEXT, self._font_size, weight),
                bg=bg, fg=fg, cursor=cursor
            )
            lbl.pack(side=LEFT)

            if not is_last:
                def _on_click(e, idx=i):
                    args = EventArgs()
                    args.Data = idx
                    self.ItemClicked(self, args)
                lbl.bind("<Button-1>", _on_click)

                sep = Native.Label(
                    self._frame,
                    text=self._separator,
                    font=(DEFAULT_FONT_TEXT, self._font_size),
                    bg=bg, fg=self._text_color
                )
                sep.pack(side=LEFT)

    @property
    def ItemsSource(self):
        return self._items_source

    @ItemsSource.setter
    def ItemsSource(self, value):
        self._items_source = value
        self._render()


# =============================================================================
# MAUI DEMO APPLICATION (Example usage)
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
        search = SearchBar(self, placeholder="Type to search...")
        search.Search = lambda sender, e: ToastNotification.Show(self._master, f"Searching: {e.Data}", 1500)

        # Carousel Section
        layout.AddChild(Label, text="Carousel View", font=("Segoe UI", 14, "bold"), fg="#512BD4")
        carousel = CarouselView(self)
        carousel.SetItems([
            "🌟 Slide 1: Welcome to MAUI",
            "🚀 Slide 2: Fast Development",
            "💡 Slide 3: Modern Design",
            "🎯 Slide 4: Easy to Use",
            "✨ Slide 5: Beautiful UI"
        ])

        # Chip Tags Section
        layout.AddChild(Label, text="Chip Tags", font=("Segoe UI", 14, "bold"), fg="#512BD4")

        chips_layout = HorizontalStackLayout(self, props={'Spacing': 5, 'Padding': (0, 5, 0, 5)})
        chips_layout.AddChild(ChipTag, text="Python", closable=True)
        chips_layout.AddChild(ChipTag, text="MAUI", closable=True)
        chips_layout.AddChild(ChipTag, text="Tkinter", closable=True)
        chips_layout.AddChild(ChipTag, text="WinFormPy", closable=False)

        # Stepper Section
        layout.AddChild(Label, text="Stepper Control", font=("Segoe UI", 14, "bold"), fg="#512BD4")
        stepper = Stepper(self, min_val=0, max_val=10, step=1, value=5)
        stepper.ValueChanged = lambda val: ToastNotification.Show(self._master, f"Value: {val}", 800)


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

        theme_layout = HorizontalStackLayout(self, props={'Spacing': 10})

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


class MAUIDemoApp(Shell):
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


if __name__ == "__main__":
    app = MAUIDemoApp()
    Application.Run(app)
