"""
WinFormPy Extended Controls Module
=================================

This module provides extended UI controls and advanced layout management 
components that build upon the core WinFormPy library. 

Controls included:
- PhotoImage: Wrapper for tkinter.PhotoImage to avoid direct tkinter usage.
- ExtendedLabel: Label with dynamic text wrapping.
- ConsoleTextBox: Multi-line text display with colored text support.
- DatePickerBox: Custom date picker with formatted text field and dropdown calendar.

For WinUI 3 styled controls, see the winui3.py module.
"""

# =============================================================
# Module: winformpy_extended.py
# Author: DatamanEdge
# Date: 2025-01-27
# Version: 1.0.2
# Description: 
# WinFormPy Extension for custom controls and advanced layout management.
# Note: WinUI 3 controls have been moved to winui3.py module.
# =============================================================

import tkinter as tk
import tkinter.ttk as ttk
import sys
import os
import subprocess
from datetime import datetime, date
from enum import Enum

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
        except:
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


def _find_uv_venv() -> str:
    """
    Find a uv-managed .venv directory in the project.
    Returns the path to site-packages if found, None otherwise.
    """
    project_dir = _find_pyproject_dir()
    if not project_dir:
        return None
    
    venv_dir = os.path.join(project_dir, '.venv')
    pyvenv_cfg = os.path.join(venv_dir, 'pyvenv.cfg')
    
    if os.path.exists(pyvenv_cfg):
        try:
            with open(pyvenv_cfg, 'r') as f:
                content = f.read()
                if 'uv =' in content or 'uv=' in content:
                    # Windows uses Lib, Unix uses lib
                    site_packages = os.path.join(venv_dir, 'Lib', 'site-packages')
                    if not os.path.exists(site_packages):
                        site_packages = os.path.join(venv_dir, 'lib', 'site-packages')
                    if os.path.exists(site_packages):
                        return site_packages
        except:
            pass
    return None


def install_library(library_name: str, import_name: str = None) -> bool:
    """
    Checks if a library is installed and, if not, attempts to install it.
    Uses 'uv pip install' if the environment is uv-managed, otherwise uses pip.
    
    After installation, refreshes Python's import system to make the new
    package available in the current session.
    """
    import importlib
    import site
    check_name = import_name if import_name else library_name
    
    # Check if there's a uv-managed venv in the project (even if not running from it)
    uv_site_packages = _find_uv_venv()
    
    # Ensure uv venv's site-packages is in sys.path for imports
    if uv_site_packages and uv_site_packages not in sys.path:
        sys.path.insert(0, uv_site_packages)
    
    # First, try to import the module
    try:
        importlib.import_module(check_name)
        return True
    except ImportError:
        pass
    
    # Module not found, try to install it
    print(f"Installing '{library_name}'...")
    try:
        # Prefer uv if there's a uv-managed venv in the project
        if uv_site_packages or _is_uv_managed_environment():
            if uv_site_packages:
                # Install to the project's .venv using uv
                subprocess.check_call(["uv", "pip", "install", "--target", uv_site_packages, library_name])
            else:
                # Running from within a uv venv
                venv_dir = os.path.dirname(os.path.dirname(sys.executable))
                site_packages = os.path.join(venv_dir, 'Lib', 'site-packages')
                subprocess.check_call(["uv", "pip", "install", "--target", site_packages, library_name])
        else:
            subprocess.check_call([sys.executable, "-m", "pip", "install", library_name])
        
        # Refresh import system to find newly installed packages
        importlib.invalidate_caches()
        
        # Remove from sys.modules if it was cached as failed/None
        # This is necessary because Python may have cached a failed import
        if check_name in sys.modules:
            del sys.modules[check_name]
        # Also remove any submodules that might have been partially loaded
        to_remove = [key for key in sys.modules if key.startswith(check_name + '.')]
        for key in to_remove:
            del sys.modules[key]
        
        # Try to import again after installation
        try:
            importlib.import_module(check_name)
            print(f"✓ '{library_name}' installed and loaded")
            return True
        except ImportError as e:
            print(f"✗ '{library_name}' installed but import failed: {e}")
            return False
            
    except subprocess.CalledProcessError:
        print(f"✗ Failed to install '{library_name}'")
        return False
    except FileNotFoundError:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", library_name])
            importlib.invalidate_caches()
            if check_name in sys.modules:
                del sys.modules[check_name]
            try:
                importlib.import_module(check_name)
                print(f"✓ '{library_name}' installed and loaded")
                return True
            except ImportError:
                return False
        except subprocess.CalledProcessError:
            print(f"✗ Failed. For uv envs: uv add {library_name}")
            return False

# To avoid circular imports with __init__.py and ensure we get the core classes
# we try to import directly from the winformpy module file.
try:
    # Try relative import first (when part of a package)
    from .winformpy import (
        Label, AnchorStyles, ContentAlignment, TabControl, 
        TabAlignment, Panel, Button, DockStyle, FlatStyle,
        TextBox, ProgressBar, ControlBase, MaskedTextBox, 
        MonthCalendar, Font, FontStyle, _resolve_master_widget
    )
except (ImportError, ValueError):
    try:
        # Try absolute import from the module file
        from winformpy import (
            Label, AnchorStyles, ContentAlignment, TabControl, 
            TabAlignment, Panel, Button, DockStyle, FlatStyle,
            TextBox, ProgressBar, ControlBase, MaskedTextBox,
            MonthCalendar, Font, FontStyle, _resolve_master_widget
        )
    except ImportError:
        # Fallback for direct execution or unusual path setups
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.append(current_dir)
        from winformpy import (
            Label, AnchorStyles, ContentAlignment, TabControl, 
            TabAlignment, Panel, Button, DockStyle, FlatStyle,
            TextBox, ProgressBar, ControlBase, MaskedTextBox,
            MonthCalendar, Font, FontStyle, _resolve_master_widget
        )


# =============================================================
# PhotoImage Wrapper
# =============================================================

class PhotoImage:
    """
    WinFormPy wrapper for tkinter.PhotoImage.
    
    This class provides a WinForms-style interface for creating and managing images
    without requiring direct tkinter imports in user code.
    
    Usage:
        # Create blank image
        img = PhotoImage(width=32, height=32)
        
        # Create from file
        img = PhotoImage(file='icon.png')
        
        # Create from data (base64 or XPM)
        img = PhotoImage(data=gif_data_string)
        
        # Set pixel color
        img.put('#FF0000', (10, 10))  # Red pixel at (10, 10)
        
        # Get underlying tkinter PhotoImage
        tk_image = img.get_image()
    """
    
    def __init__(self, **kwargs):
        """
        Initialize a PhotoImage.
        
        Parameters:
            file (str): Path to image file (GIF, PGM, PPM, PNG with PIL)
            data (str): Image data in base64 or XPM format
            width (int): Width for blank image
            height (int): Height for blank image
            format (str): Image format ('gif', 'png', 'ppm', 'pgm')
            master: Tkinter master widget (optional)
        """
        # Import tkinter PhotoImage only when needed
        import tkinter as tk
        from tkinter import PhotoImage as TkPhotoImage
        
        # Ensure there's a default root window if needed
        # PhotoImage requires a Tk root to exist
        if 'master' not in kwargs:
            try:
                # Try to get existing root
                root = tk._default_root
                if root is None:
                    # Create a hidden root if none exists
                    root = tk.Tk()
                    root.withdraw()  # Hide the root window
            except:
                # If that fails, just pass - let tkinter handle it
                pass
        
        # Create the underlying tkinter PhotoImage
        self._tk_image = TkPhotoImage(**kwargs)
    
    def put(self, color, to=None):
        """
        Set pixel color(s) in the image.
        
        Parameters:
            color (str): Color in format '#RRGGBB' or color name
            to (tuple or None): 
                - (x, y) for single pixel
                - ((x1, y1), (x2, y2)) for rectangle
                - None to fill entire image
        
        Example:
            img.put('#FF0000', (10, 10))  # Single red pixel
            img.put('#00FF00', ((0, 0), (10, 10)))  # Green rectangle
            img.put('#0000FF')  # Fill with blue
        """
        if to is None:
            # Fill entire image
            self._tk_image.put(color)
        elif isinstance(to, tuple) and len(to) == 2:
            if isinstance(to[0], (int, float)):
                # Single pixel (x, y)
                self._tk_image.put(color, to=to)
            else:
                # Rectangle ((x1, y1), (x2, y2))
                self._tk_image.put(color, to=to)
        else:
            self._tk_image.put(color, to=to)
    
    def get(self, x, y):
        """
        Get the color of a pixel.
        
        Parameters:
            x (int): X coordinate
            y (int): Y coordinate
            
        Returns:
            tuple: RGB values (r, g, b)
        """
        return self._tk_image.get(x, y)
    
    def copy(self):
        """
        Create a copy of this image.
        
        Returns:
            PhotoImage: New PhotoImage with same content
        """
        new_image = PhotoImage.__new__(PhotoImage)
        new_image._tk_image = self._tk_image.copy()
        return new_image
    
    def subsample(self, x, y=None):
        """
        Return a reduced-size version of the image.
        
        Parameters:
            x (int): X subsample factor
            y (int): Y subsample factor (defaults to x if not provided)
            
        Returns:
            PhotoImage: Subsampled image
        """
        new_image = PhotoImage.__new__(PhotoImage)
        if y is None:
            new_image._tk_image = self._tk_image.subsample(x)
        else:
            new_image._tk_image = self._tk_image.subsample(x, y)
        return new_image
    
    def zoom(self, x, y=None):
        """
        Return an enlarged version of the image.
        
        Parameters:
            x (int): X zoom factor
            y (int): Y zoom factor (defaults to x if not provided)
            
        Returns:
            PhotoImage: Zoomed image
        """
        new_image = PhotoImage.__new__(PhotoImage)
        if y is None:
            new_image._tk_image = self._tk_image.zoom(x)
        else:
            new_image._tk_image = self._tk_image.zoom(x, y)
        return new_image
    
    def write(self, filename, format=None, from_coords=None):
        """
        Write image to file.
        
        Parameters:
            filename (str): Output file path
            format (str): Image format ('gif', 'ppm', 'pgm')
            from_coords (tuple): Optional ((x1, y1), (x2, y2)) to write portion
        """
        if from_coords:
            self._tk_image.write(filename, format=format, from_coords=from_coords)
        elif format:
            self._tk_image.write(filename, format=format)
        else:
            self._tk_image.write(filename)
    
    def width(self):
        """
        Get image width.
        
        Returns:
            int: Width in pixels
        """
        return self._tk_image.width()
    
    def height(self):
        """
        Get image height.
        
        Returns:
            int: Height in pixels
        """
        return self._tk_image.height()
    
    def get_image(self):
        """
        Get the underlying tkinter PhotoImage object.
        
        This is needed for internal WinFormPy use when passing images
        to ImageList or other controls.
        
        Returns:
            tkinter.PhotoImage: The underlying tkinter PhotoImage
        """
        return self._tk_image
    
    def __str__(self):
        """Return string representation."""
        return str(self._tk_image)
    
    def __repr__(self):
        """Return detailed representation."""
        return f"PhotoImage({self._tk_image.width()}x{self._tk_image.height()})"


class ExtendedLabel(Label):
    """
    Extended Label control that supports multiline text with dynamic wrapping
    and alignment.
    
    Features:
    - Dynamic Wrapping: Text wraps to fit the control's width automatically.
    - Width-bound layout: Control size determines text layout (AutoSize=False).
    - Resizing: Updates wrapping when control is resized (e.g. via Anchors or Dock).
    - TextAlign: Supports dynamic alignment updates via ContentAlignment.
    """
    def __init__(self, master_form, props=None):
        if props is None:
            props = {}
            
        # Ensure AutoSize is False so we control the size
        # This allows text to wrap based on control width instead of expanding control to text
        if 'AutoSize' not in props:
            props['AutoSize'] = False
            
        super().__init__(master_form, props)
        
        # Bind the resize event to update text wrapping with add='+' to keep base class bindings
        self._tk_widget.bind('<Configure>', self._update_wrapping, add="+")
        
        # Initial wrap update
        self._tk_widget.after(10, self._update_wrapping)
        
    def _update_wrapping(self, event=None):
        """Updates the wraplength of the label to match its current width."""
        if self._tk_widget:
            # Set wraplength to the current width of the widget
            # Subtract a small padding to ensure it fits comfortably
            # event.width is available on resize, otherwise use winfo_width
            width = event.width if event else self._tk_widget.winfo_width()
            
            # Only update if width is valid and changed
            if width > 10:
                # Subtract padding to avoid jitter at the edge
                self._tk_widget.config(wraplength=width - 8)

    @property
    def TextAlign(self):
        """Gets or sets the alignment of the text in the label."""
        return getattr(self, '_text_align', ContentAlignment.TopLeft)

    @TextAlign.setter
    def TextAlign(self, value):
        self._text_align = value
        if self._tk_widget:
            # Alignment maps
            anchor_map = {
                ContentAlignment.TopLeft: 'nw', ContentAlignment.TopCenter: 'n', ContentAlignment.TopRight: 'ne',
                ContentAlignment.MiddleLeft: 'w', ContentAlignment.MiddleCenter: 'center', ContentAlignment.MiddleRight: 'e',
                ContentAlignment.BottomLeft: 'sw', ContentAlignment.BottomCenter: 's', ContentAlignment.BottomRight: 'se',
                # String fallbacks
                'TopLeft': 'nw', 'TopCenter': 'n', 'TopRight': 'ne',
                'MiddleLeft': 'w', 'MiddleCenter': 'center', 'MiddleRight': 'e',
                'BottomLeft': 'sw', 'BottomCenter': 's', 'BottomRight': 'se',
                'left': 'w', 'center': 'center', 'right': 'e'
            }
            
            justify_map = {
                ContentAlignment.TopLeft: 'left', ContentAlignment.TopCenter: 'center', ContentAlignment.TopRight: 'right',
                ContentAlignment.MiddleLeft: 'left', ContentAlignment.MiddleCenter: 'center', ContentAlignment.MiddleRight: 'right',
                ContentAlignment.BottomLeft: 'left', ContentAlignment.BottomCenter: 'center', ContentAlignment.BottomRight: 'right',
                 # String fallbacks
                'TopLeft': 'left', 'TopCenter': 'center', 'TopRight': 'right',
                'MiddleLeft': 'left', 'MiddleCenter': 'center', 'MiddleRight': 'right',
                'BottomLeft': 'left', 'BottomCenter': 'center', 'BottomRight': 'right',
                'left': 'left', 'center': 'center', 'right': 'right'
            }
            
            self._tk_widget.config(
                anchor=anchor_map.get(value, 'w'),
                justify=justify_map.get(value, 'left')
            )


class ConsoleTextBox:
    """
    Represents a ConsoleTextBox control with support for multiple text colors.
    
    This control provides a multi-line text display with:
    - Support for colored text segments (via tags)
    - Integrated vertical scrollbar
    - Read-only mode for output display
    - Methods for writing colored text
    
    Ideal for console-style output, log viewers, or any multi-colored text display.
    
    Example:
        ctb = ConsoleTextBox(form, {
            'Dock': DockStyle.Fill,
            'BackColor': '#1E1E1E',
            'ForeColor': '#CCCCCC',
            'ReadOnly': True
        })
        
        ctb.WriteLine("Normal text")
        ctb.WriteLine("Error message", '#FF0000')
        ctb.WriteLine("Success!", '#00FF00')
    """
    
    def __init__(self, master_form, props=None):
        """Initializes a ConsoleTextBox.

        Args:
            master_form: The parent form or container
            props: Optional dictionary with initial properties:
                - BackColor: Background color
                - ForeColor: Default text color
                - Font: Font object or tuple (family, size)
                - ReadOnly: If True, text cannot be edited by user
                - WordWrap: Enable/disable word wrapping
                - ShowScrollBar: Show vertical scrollbar (default True)
                - MaxLines: Maximum lines to keep (0 = unlimited)
                - BorderWidth: Border width (default 0)
                - Padding: Internal padding (default 8)
        """
        defaults = {
            'Left': 0,
            'Top': 0,
            'Width': 400,
            'Height': 300,
            'Name': '',
            'BackColor': '#FFFFFF',
            'ForeColor': '#000000',
            'Font': None,
            'ReadOnly': False,
            'WordWrap': True,
            'ShowScrollBar': True,
            'MaxLines': 0,
            'BorderWidth': 0,
            'Padding': 8,
            'Visible': True,
            'Enabled': True,
            'SelectionBackColor': '#264F78',
            'SelectionForeColor': None,
            'InsertCursorColor': None
        }
        
        if props:
            defaults.update(props)
        
        # Resolve the Tkinter widget and keep the original parent container
        from .winformpy import _resolve_master_widget, ControlBase, EventArgs
        master_widget, parent_container = _resolve_master_widget(master_form)
        
        # Initialize base attributes manually (not inheriting from ControlBase for simplicity)
        self.master = master_widget
        self.Left = defaults['Left']
        self.Top = defaults['Top']
        
        # Store the parent container for auto-registration
        self._parent_container = parent_container
        
        # Store properties
        self.Name = defaults['Name']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self._back_color = defaults['BackColor']
        self._fore_color = defaults['ForeColor']
        self._font = defaults['Font']
        self._read_only = defaults['ReadOnly']
        self._word_wrap = defaults['WordWrap']
        self._show_scrollbar = defaults['ShowScrollBar']
        self._max_lines = defaults['MaxLines']
        self._border_width = defaults['BorderWidth']
        self._padding = defaults['Padding']
        self._visible = defaults['Visible']
        self._enabled = defaults['Enabled']
        self._selection_back_color = defaults['SelectionBackColor']
        self._selection_fore_color = defaults['SelectionForeColor']
        self._insert_cursor_color = defaults['InsertCursorColor'] or self._fore_color
        
        # Dock/Anchor support
        self._dock = defaults.get('Dock', None)
        self._anchor = defaults.get('Anchor', None)
        
        # Events
        self.TextChanged = lambda sender=None, e=None: None
        
        # Create the widget
        self._create_widget()
        
        # Apply Dock/Anchor if specified
        if 'Dock' in defaults and defaults['Dock']:
            self.Dock = defaults['Dock']
        if 'Anchor' in defaults and defaults['Anchor']:
            self.Anchor = defaults['Anchor']
        
        # Auto-register with the parent container
        self._auto_register_with_parent()
    
    def _auto_register_with_parent(self):
        """Register this control with its parent container."""
        if hasattr(self, '_parent_container') and self._parent_container:
            if hasattr(self._parent_container, 'Controls'):
                if self not in self._parent_container.Controls:
                    self._parent_container.Controls.append(self)
    
    def _create_widget(self):
        """Create the underlying Tkinter widgets."""
        # Container frame for text + scrollbar
        self._container_frame = tk.Frame(
            self.master, 
            bg=self._back_color,
            borderwidth=self._border_width,
            highlightthickness=0
        )
        
        # Get font
        tk_font = None
        if self._font:
            if hasattr(self._font, '_tk_font'):
                tk_font = self._font._tk_font
            elif hasattr(self._font, 'GetTkFont'):
                tk_font = self._font.GetTkFont()
            elif isinstance(self._font, tuple):
                tk_font = self._font
        
        # Text widget
        wrap_mode = 'word' if self._word_wrap else 'none'
        self._tk_widget = tk.Text(
            self._container_frame,
            wrap=wrap_mode,
            bg=self._back_color,
            fg=self._fore_color,
            insertbackground=self._insert_cursor_color,
            selectbackground=self._selection_back_color,
            selectforeground=self._selection_fore_color or self._fore_color,
            borderwidth=0,
            highlightthickness=0,
            padx=self._padding,
            pady=self._padding,
            cursor='arrow' if self._read_only else 'xterm'
        )
        
        if tk_font:
            self._tk_widget.config(font=tk_font)
        
        if self._read_only:
            self._tk_widget.config(state='disabled')
        
        # Scrollbar (auto-hide behavior - only shown when needed)
        self._scrollbar = None
        self._scrollbar_visible = False
        if self._show_scrollbar:
            self._scrollbar = tk.Scrollbar(self._container_frame, command=self._tk_widget.yview)
            self._tk_widget.config(yscrollcommand=self._on_scroll_update)
            # Don't pack initially - will be shown when needed
        
        # Pack text widget
        self._tk_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind configure event to check scrollbar visibility
        self._tk_widget.bind('<Configure>', self._on_text_configure)
        
        # Place container
        self._container_frame.place(x=self.Left, y=self.Top, width=self.Width, height=self.Height)
        
        # Apply visibility
        self.set_Visible(self._visible)
    
    def _on_scroll_update(self, first, last):
        """Handle scroll updates and auto-hide scrollbar."""
        if self._scrollbar:
            self._scrollbar.set(first, last)
            self._update_scrollbar_visibility()
    
    def _on_text_configure(self, event=None):
        """Handle text widget resize - update scrollbar visibility."""
        self._tk_widget.after_idle(self._update_scrollbar_visibility)
    
    def _update_scrollbar_visibility(self):
        """Show/hide scrollbar based on whether it's needed."""
        if not self._scrollbar or not self._show_scrollbar:
            return
        
        try:
            first, last = self._scrollbar.get()
            needed = not (float(first) <= 0.0 and float(last) >= 1.0)
            
            if needed and not self._scrollbar_visible:
                self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y, before=self._tk_widget)
                self._scrollbar_visible = True
            elif not needed and self._scrollbar_visible:
                self._scrollbar.pack_forget()
                self._scrollbar_visible = False
        except (tk.TclError, ValueError):
            pass
    
    def _place_control(self, width=None, height=None):
        """Override to handle container frame placement."""
        x_coord = self.Left
        y_coord = self.Top
        place_args = {'x': x_coord, 'y': y_coord, 'in_': self.master}
        if width is not None:
            place_args['width'] = width
        if height is not None:
            place_args['height'] = height
        try:
            self._container_frame.place(**place_args)
        except tk.TclError:
            pass
    
    def set_Visible(self, value):
        """Sets the visibility state."""
        self._visible = value
        
        if hasattr(self, '_container_frame') and self._container_frame:
            if value:
                self._container_frame.place(x=self.Left, y=self.Top, width=self.Width, height=self.Height)
            else:
                self._container_frame.place_forget()
    
    def PerformLayout(self):
        """Force layout recalculation for the control."""
        if not hasattr(self, '_container_frame') or not self._container_frame:
            return
        
        # Force geometry update
        self._container_frame.update_idletasks()
        
        # Get current dimensions
        width = self._container_frame.winfo_width()
        height = self._container_frame.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Re-place the container with current dimensions
        self._container_frame.place_configure(width=width, height=height)
        
        # Repack text widget
        try:
            self._tk_widget.pack_forget()
        except:
            pass
        self._tk_widget.pack(side='left', fill='both', expand=True)
        
        # Update scrollbar visibility (auto-hide behavior)
        self._update_scrollbar_visibility()
        
        self._container_frame.update_idletasks()
    
    # =========================================================================
    # Dock/Anchor Properties
    # =========================================================================
    
    @property
    def Dock(self):
        """Gets the dock style."""
        return self._dock
    
    @Dock.setter
    def Dock(self, value):
        """Sets the dock style."""
        self._dock = value
        # Trigger parent layout if available
        if self._parent_container and hasattr(self._parent_container, 'PerformLayout'):
            self._parent_container.PerformLayout()
    
    @property
    def Anchor(self):
        """Gets the anchor style."""
        return self._anchor
    
    @Anchor.setter
    def Anchor(self, value):
        """Sets the anchor style."""
        self._anchor = value
    
    # =========================================================================
    # Properties
    # =========================================================================
    
    @property
    def Text(self):
        """Gets all text in the ConsoleTextBox."""
        return self._tk_widget.get('1.0', 'end-1c')
    
    @Text.setter
    def Text(self, value):
        """Sets all text in the ConsoleTextBox."""
        was_disabled = self._read_only
        if was_disabled:
            self._tk_widget.config(state='normal')
        self._tk_widget.delete('1.0', 'end')
        self._tk_widget.insert('1.0', value)
        if was_disabled:
            self._tk_widget.config(state='disabled')
    
    @property
    def BackColor(self):
        """Gets the background color."""
        return self._back_color
    
    @BackColor.setter
    def BackColor(self, value):
        """Sets the background color."""
        self._back_color = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._tk_widget.config(bg=value)
        if hasattr(self, '_container_frame') and self._container_frame:
            self._container_frame.config(bg=value)
    
    @property
    def ForeColor(self):
        """Gets the default foreground color."""
        return self._fore_color
    
    @ForeColor.setter
    def ForeColor(self, value):
        """Sets the default foreground color."""
        self._fore_color = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._tk_widget.config(fg=value, insertbackground=value)
    
    @property
    def ReadOnly(self):
        """Gets whether the control is read-only."""
        return self._read_only
    
    @ReadOnly.setter
    def ReadOnly(self, value):
        """Sets whether the control is read-only."""
        self._read_only = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._tk_widget.config(state='disabled' if value else 'normal')
            self._tk_widget.config(cursor='arrow' if value else 'xterm')
    
    @property
    def WordWrap(self):
        """Gets whether word wrap is enabled."""
        return self._word_wrap
    
    @WordWrap.setter
    def WordWrap(self, value):
        """Sets whether word wrap is enabled."""
        self._word_wrap = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._tk_widget.config(wrap='word' if value else 'none')
    
    @property
    def Font(self):
        """Gets the font."""
        return self._font
    
    @Font.setter
    def Font(self, value):
        """Sets the font."""
        self._font = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            tk_font = None
            if hasattr(value, '_tk_font'):
                tk_font = value._tk_font
            elif hasattr(value, 'GetTkFont'):
                tk_font = value.GetTkFont()
            elif isinstance(value, tuple):
                tk_font = value
            if tk_font:
                self._tk_widget.config(font=tk_font)
    
    @property
    def MaxLines(self):
        """Gets the maximum number of lines to keep."""
        return self._max_lines
    
    @MaxLines.setter
    def MaxLines(self, value):
        """Sets the maximum number of lines to keep."""
        self._max_lines = value
        self._trim_lines()
    
    @property
    def Lines(self):
        """Gets the lines of text."""
        return self.Text.split('\n')
    
    @property
    def LineCount(self):
        """Gets the number of lines."""
        return int(self._tk_widget.index('end-1c').split('.')[0])
    
    @property
    def Visible(self):
        """Gets the visibility state."""
        return self._visible
    
    @Visible.setter
    def Visible(self, value):
        """Sets the visibility state."""
        self.set_Visible(value)
    
    # =========================================================================
    # Methods
    # =========================================================================
    
    def Write(self, text, color=None):
        """
        Write text without a newline.
        
        Args:
            text: The text to write
            color: Optional color for this text (e.g., '#FF0000')
        """
        was_disabled = self._read_only
        if was_disabled:
            self._tk_widget.config(state='normal')
        
        if color:
            # Create a tag for this color
            tag_name = f'color_{color.replace("#", "").replace("(", "").replace(")", "").replace(",", "_")}'
            self._tk_widget.tag_configure(tag_name, foreground=color)
            self._tk_widget.insert('end', text, tag_name)
        else:
            self._tk_widget.insert('end', text)
        
        if was_disabled:
            self._tk_widget.config(state='disabled')
        
        self._tk_widget.see('end')
        self._trim_lines()
        self.TextChanged(self, None)
    
    def WriteLine(self, text='', color=None):
        """
        Write text with a newline.
        
        Args:
            text: The text to write
            color: Optional color for this text
        """
        self.Write(text + '\n', color)
    
    def WriteError(self, text):
        """Write error text (red)."""
        self.WriteLine(text, '#FF6B6B')
    
    def WriteWarning(self, text):
        """Write warning text (yellow)."""
        self.WriteLine(text, '#FFD93D')
    
    def WriteSuccess(self, text):
        """Write success text (green)."""
        self.WriteLine(text, '#6BCB77')
    
    def WriteInfo(self, text):
        """Write info text (blue)."""
        self.WriteLine(text, '#4D96FF')
    
    def Clear(self):
        """Clear all text."""
        was_disabled = self._read_only
        if was_disabled:
            self._tk_widget.config(state='normal')
        self._tk_widget.delete('1.0', 'end')
        if was_disabled:
            self._tk_widget.config(state='disabled')
    
    def ScrollToEnd(self):
        """Scroll to the end of the text."""
        self._tk_widget.see('end')
    
    def ScrollToStart(self):
        """Scroll to the start of the text."""
        self._tk_widget.see('1.0')
    
    def AppendText(self, text, color=None):
        """
        Append text to the end.
        
        Args:
            text: The text to append
            color: Optional color
        """
        self.Write(text, color)
    
    def Focus(self):
        """Set focus to the control."""
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._tk_widget.focus_set()
    
    def SelectAll(self):
        """Select all text."""
        self._tk_widget.tag_add('sel', '1.0', 'end')
    
    def DeselectAll(self):
        """Deselect all text."""
        self._tk_widget.tag_remove('sel', '1.0', 'end')
    
    def Copy(self):
        """Copy selected text to clipboard."""
        try:
            self._tk_widget.event_generate('<<Copy>>')
        except:
            pass
    
    def _trim_lines(self):
        """Trim to MaxLines if exceeded."""
        if self._max_lines <= 0:
            return
        
        was_disabled = self._read_only
        if was_disabled:
            self._tk_widget.config(state='normal')
        
        line_count = self.LineCount
        if line_count > self._max_lines:
            excess = line_count - self._max_lines
            self._tk_widget.delete('1.0', f'{excess + 1}.0')
        
        if was_disabled:
            self._tk_widget.config(state='disabled')
    
    def ConfigureTag(self, tag_name, **kwargs):
        """
        Configure a text tag for styling.
        
        Args:
            tag_name: Name of the tag
            **kwargs: Tag configuration (foreground, background, font, etc.)
        """
        self._tk_widget.tag_configure(tag_name, **kwargs)
    
    def WriteWithTag(self, text, tag_name):
        """
        Write text with a specific tag.
        
        Args:
            text: The text to write
            tag_name: The tag name to apply
        """
        was_disabled = self._read_only
        if was_disabled:
            self._tk_widget.config(state='normal')
        self._tk_widget.insert('end', text, tag_name)
        if was_disabled:
            self._tk_widget.config(state='disabled')
        self._tk_widget.see('end')


# =============================================================
# DatePickerBox - Custom Date Picker Control
# =============================================================

class DateFormat(Enum):
    """Date format options for DatePickerBox."""
    Short = "dd/MM/yyyy"       # 28/01/2026
    Long = "dd MMMM yyyy"      # 28 January 2026
    ISO = "yyyy-MM-dd"         # 2026-01-28
    US = "MM/dd/yyyy"          # 01/28/2026
    Custom = "custom"          # User-defined format


class DatePickerBox(ControlBase):
    """
    Custom date picker control with formatted text field and dropdown calendar.
    
    This control combines a MaskedTextBox for formatted date input with a 
    dropdown MonthCalendar for visual date selection.
    
    Features:
        - Formatted date text field with mask validation
        - Dropdown calendar button to show/hide calendar
        - Multiple date format options (Short, Long, ISO, US, Custom)
        - Configurable date range (MinDate, MaxDate)
        - Events for value changes and calendar visibility
        - Keyboard navigation support
    
    Properties:
        Value (datetime): The selected date/time value
        Format (DateFormat): The display format for the date
        CustomFormat (str): Custom format string when Format is Custom
        MinDate (datetime): Minimum selectable date
        MaxDate (datetime): Maximum selectable date
        CalendarVisible (bool): Whether the calendar dropdown is shown
        Enabled (bool): Whether the control is enabled
        ReadOnly (bool): Whether the text field is read-only
    
    Events:
        ValueChanged: Fired when the date value changes
        CalendarOpened: Fired when the calendar dropdown opens
        CalendarClosed: Fired when the calendar dropdown closes
    
    Example:
        from winformpy_extended import DatePickerBox, DateFormat
        
        picker = DatePickerBox(form, {
            'Left': 20, 'Top': 50,
            'Width': 250,
            'Format': DateFormat.Short,
            'Value': datetime.now()
        })
        picker.ValueChanged = lambda s, e: print(f"Selected: {e.Data['Value']}")
    """
    
    # Layout constants
    BUTTON_WIDTH = 28
    CALENDAR_WIDTH = 280
    CALENDAR_HEIGHT = 260
    
    # Default date range
    MinDateTime = datetime(1900, 1, 1)
    MaxDateTime = datetime(2100, 12, 31)
    
    def __init__(self, master_form, props=None):
        """
        Initialize the DatePickerBox.
        
        Args:
            master_form: Parent Form or Panel
            props: Optional properties dictionary
        """
        # Initialize internal widget references BEFORE super().__init__
        # because ControlBase may set Enabled which uses these
        self._text_entry = None
        self._dropdown_btn = None
        self._frame = None
        self._calendar_window = None
        self._calendar = None
        self._calendar_visible = False
        self._enabled = True
        self._read_only = False
        
        defaults = {
            'Left': 10,
            'Top': 10,
            'Width': 200,
            'Height': 28,
            'Name': '',
            'Value': datetime.now(),
            'Format': DateFormat.Short,
            'CustomFormat': 'dd/MM/yyyy',
            'MinDate': self.MinDateTime,
            'MaxDate': self.MaxDateTime,
            'Enabled': True,
            'ReadOnly': False,
            'BackColor': '#FFFFFF',
            'ForeColor': '#000000',
            'ButtonBackColor': '#F0F0F0',
            'ButtonForeColor': '#333333',
            'Font': None,
            # Calendar styling
            'CalendarBackColor': '#FFFFFF',
            'CalendarTitleBackColor': '#0078D4',
            'CalendarTitleForeColor': '#FFFFFF',
            'CalendarSelectBackground': '#0078D4',
            'CalendarSelectForeground': '#FFFFFF'
        }
        
        if props:
            defaults.update(props)
        
        # Resolve master widget
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        self._parent_container = parent_container
        
        # Store properties
        self.Name = defaults['Name']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self._enabled = defaults['Enabled']
        self._read_only = defaults['ReadOnly']
        
        # Date properties
        self._value = defaults['Value'] if isinstance(defaults['Value'], datetime) else datetime.now()
        self._format = defaults['Format']
        self._custom_format = defaults['CustomFormat']
        self._min_date = defaults['MinDate']
        self._max_date = defaults['MaxDate']
        
        # Styling
        self._back_color = defaults['BackColor']
        self._fore_color = defaults['ForeColor']
        self._button_back_color = defaults['ButtonBackColor']
        self._button_fore_color = defaults['ButtonForeColor']
        self._font = defaults['Font']
        self._calendar_styles = {
            'BackColor': defaults['CalendarBackColor'],
            'TitleBackColor': defaults['CalendarTitleBackColor'],
            'TitleForeColor': defaults['CalendarTitleForeColor'],
            'SelectBackground': defaults['CalendarSelectBackground'],
            'SelectForeground': defaults['CalendarSelectForeground']
        }
        
        # State (already initialized above, just update calendar_panel)
        self._calendar_panel = None
        
        # Events
        self.ValueChanged = lambda sender, e: None
        self.CalendarOpened = lambda sender, e: None
        self.CalendarClosed = lambda sender, e: None
        
        # Create the control
        self._create_control()
        
        # Auto-register
        self._auto_register_with_parent()
    
    def _create_control(self):
        """Create the control UI."""
        # Main container frame
        self._frame = tk.Frame(self.master, bg=self._back_color)
        self._tk_widget = self._frame
        
        # Calculate dimensions
        text_width = self.Width - self.BUTTON_WIDTH - 2
        
        # Create the date text field
        self._text_entry = tk.Entry(
            self._frame,
            font=('Segoe UI', 10),
            bg=self._back_color,
            fg=self._fore_color,
            relief='solid',
            borderwidth=1
        )
        self._text_entry.place(x=0, y=0, width=text_width, height=self.Height)
        
        # Bind text field events
        self._text_entry.bind('<FocusOut>', self._on_text_focus_out)
        self._text_entry.bind('<Return>', self._on_text_enter)
        self._text_entry.bind('<Escape>', self._on_escape)
        
        # Create dropdown button
        self._dropdown_btn = tk.Button(
            self._frame,
            text='▼',
            font=('Segoe UI', 8),
            bg=self._button_back_color,
            fg=self._button_fore_color,
            relief='flat',
            borderwidth=1,
            command=self._toggle_calendar
        )
        self._dropdown_btn.place(x=text_width + 1, y=0, width=self.BUTTON_WIDTH, height=self.Height)
        
        # Bind hover effects
        self._dropdown_btn.bind('<Enter>', lambda e: self._dropdown_btn.config(bg='#E0E0E0'))
        self._dropdown_btn.bind('<Leave>', lambda e: self._dropdown_btn.config(bg=self._button_back_color))
        
        # Place the main control
        self._place_control(self.Width, self.Height)
        
        # Update display with initial value
        self._update_display()
    
    def _get_mask_for_format(self):
        """Get the mask string for the current format."""
        if self._format == DateFormat.Short:
            return "00/00/0000"
        elif self._format == DateFormat.ISO:
            return "0000-00-00"
        elif self._format == DateFormat.US:
            return "00/00/0000"
        elif self._format == DateFormat.Custom:
            # Convert format to mask
            mask = self._custom_format
            mask = mask.replace('yyyy', '0000').replace('yy', '00')
            mask = mask.replace('MMMM', '&&&&&&&&&&').replace('MMM', '&&&').replace('MM', '00').replace('M', '00')
            mask = mask.replace('dd', '00').replace('d', '00')
            return mask
        return "00/00/0000"
    
    def _format_date(self, dt):
        """Format date according to current format setting."""
        if not dt:
            return ""
        
        if self._format == DateFormat.Short:
            return dt.strftime("%d/%m/%Y")
        elif self._format == DateFormat.Long:
            return dt.strftime("%d %B %Y")
        elif self._format == DateFormat.ISO:
            return dt.strftime("%Y-%m-%d")
        elif self._format == DateFormat.US:
            return dt.strftime("%m/%d/%Y")
        elif self._format == DateFormat.Custom:
            # Convert custom format to Python strftime
            fmt = self._custom_format
            fmt = fmt.replace('yyyy', '%Y').replace('yy', '%y')
            fmt = fmt.replace('MMMM', '%B').replace('MMM', '%b').replace('MM', '%m')
            fmt = fmt.replace('dd', '%d')
            fmt = fmt.replace('HH', '%H').replace('mm', '%M').replace('ss', '%S')
            return dt.strftime(fmt)
        return dt.strftime("%d/%m/%Y")
    
    def _parse_date(self, text):
        """Parse date from text according to current format."""
        if not text or not text.strip():
            return None
        
        text = text.strip()
        
        # Try different parse formats
        parse_formats = []
        
        if self._format == DateFormat.Short:
            parse_formats = ["%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y"]
        elif self._format == DateFormat.Long:
            parse_formats = ["%d %B %Y", "%d %b %Y"]
        elif self._format == DateFormat.ISO:
            parse_formats = ["%Y-%m-%d", "%Y/%m/%d"]
        elif self._format == DateFormat.US:
            parse_formats = ["%m/%d/%Y", "%m-%d-%Y"]
        else:
            # Try common formats
            parse_formats = [
                "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d",
                "%d-%m-%Y", "%Y/%m/%d", "%d.%m.%Y"
            ]
        
        for fmt in parse_formats:
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                continue
        
        return None
    
    def _update_display(self):
        """Update the text field with the current value."""
        formatted = self._format_date(self._value)
        self._text_entry.delete(0, 'end')
        self._text_entry.insert(0, formatted)
    
    def _on_text_focus_out(self, event):
        """Handle text field losing focus."""
        self._validate_and_apply_text()
    
    def _on_text_enter(self, event):
        """Handle Enter key in text field."""
        self._validate_and_apply_text()
    
    def _on_escape(self, event):
        """Handle Escape key."""
        if self._calendar_visible:
            self._hide_calendar()
        else:
            # Restore original value
            self._update_display()
    
    def _validate_and_apply_text(self):
        """Validate text input and apply if valid."""
        text = self._text_entry.get()
        parsed = self._parse_date(text)
        
        if parsed:
            # Validate date range
            if parsed < self._min_date:
                parsed = self._min_date
            if parsed > self._max_date:
                parsed = self._max_date
            
            old_value = self._value
            self._value = parsed
            self._update_display()
            
            if old_value != parsed:
                self._fire_value_changed(old_value, parsed)
        else:
            # Invalid date, restore previous value
            self._update_display()
    
    def _toggle_calendar(self):
        """Toggle calendar visibility."""
        if self._calendar_visible:
            self._hide_calendar()
        else:
            self._show_calendar()
    
    def _show_calendar(self):
        """Show the calendar dropdown."""
        if self._calendar_visible:
            return
        
        # Get position for calendar
        x = self._frame.winfo_rootx()
        y = self._frame.winfo_rooty() + self.Height
        
        # Create toplevel window for calendar
        self._calendar_window = tk.Toplevel(self.master)
        self._calendar_window.wm_overrideredirect(True)
        self._calendar_window.geometry(f"{self.CALENDAR_WIDTH}x{self.CALENDAR_HEIGHT}+{x}+{y}")
        
        # Create calendar frame with border
        calendar_frame = tk.Frame(
            self._calendar_window,
            bg=self._calendar_styles['TitleBackColor'],
            relief='solid',
            borderwidth=1
        )
        calendar_frame.pack(fill='both', expand=True)
        
        # Try to use tkcalendar if available (with lazy install)
        if install_library("tkcalendar"):
            try:
                from tkcalendar import Calendar
                
                self._calendar = Calendar(
                    calendar_frame,
                    selectmode='day',
                    year=self._value.year,
                    month=self._value.month,
                    day=self._value.day,
                    mindate=self._min_date,
                    maxdate=self._max_date,
                    showweeknumbers=False,
                    showothermonthdays=True,
                    background=self._calendar_styles['BackColor'],
                    headersbackground=self._calendar_styles['TitleBackColor'],
                    headersforeground=self._calendar_styles['TitleForeColor'],
                    selectbackground=self._calendar_styles['SelectBackground'],
                    selectforeground=self._calendar_styles['SelectForeground']
                )
                self._calendar.pack(fill='both', expand=True, padx=2, pady=2)
                self._calendar.bind('<<CalendarSelected>>', self._on_calendar_select)
            except ImportError:
                # Fallback if import fails after install
                self._create_fallback_calendar(calendar_frame)
        else:
            # Fallback: simple month/year selector
            self._create_fallback_calendar(calendar_frame)
        
        # Bind click outside to close
        self._calendar_window.bind('<FocusOut>', self._on_calendar_focus_out)
        self._calendar_window.bind('<Escape>', lambda e: self._hide_calendar())
        
        # Bind click outside detection
        self.master.winfo_toplevel().bind('<Button-1>', self._on_click_outside, add='+')
        
        self._calendar_visible = True
        self._dropdown_btn.config(text='▲')
        
        # Fire event
        self.CalendarOpened(self, type('EventArgs', (), {'Data': {}})())
    
    def _create_fallback_calendar(self, parent):
        """Create a simple fallback calendar when tkcalendar is not available."""
        # Header with month/year
        header = tk.Frame(parent, bg=self._calendar_styles['TitleBackColor'])
        header.pack(fill='x', padx=2, pady=2)
        
        tk.Label(
            header,
            text=self._value.strftime("%B %Y"),
            font=('Segoe UI', 11, 'bold'),
            bg=self._calendar_styles['TitleBackColor'],
            fg=self._calendar_styles['TitleForeColor']
        ).pack(pady=5)
        
        # Message
        msg = tk.Label(
            parent,
            text="Install tkcalendar for\nfull calendar support:\n\npip install tkcalendar",
            font=('Segoe UI', 9),
            bg=self._calendar_styles['BackColor'],
            fg='#666666',
            justify='center'
        )
        msg.pack(expand=True)
        
        # OK button to close
        ok_btn = tk.Button(
            parent,
            text="OK",
            command=self._hide_calendar,
            bg=self._calendar_styles['SelectBackground'],
            fg=self._calendar_styles['SelectForeground']
        )
        ok_btn.pack(pady=5)
    
    def _on_calendar_select(self, event):
        """Handle calendar date selection."""
        if self._calendar:
            try:
                selected = self._calendar.selection_get()
                if isinstance(selected, date) and not isinstance(selected, datetime):
                    selected = datetime.combine(selected, self._value.time())
                
                old_value = self._value
                self._value = selected
                self._update_display()
                self._hide_calendar()
                
                if old_value != selected:
                    self._fire_value_changed(old_value, selected)
            except:
                pass
    
    def _on_calendar_focus_out(self, event):
        """Handle calendar losing focus."""
        # Small delay to allow for button clicks
        self.master.after(100, self._check_and_hide_calendar)
    
    def _on_click_outside(self, event):
        """Handle click outside calendar."""
        if not self._calendar_visible:
            return
        
        # Check if click is inside calendar window
        try:
            if self._calendar_window:
                x = event.x_root
                y = event.y_root
                wx = self._calendar_window.winfo_rootx()
                wy = self._calendar_window.winfo_rooty()
                ww = self._calendar_window.winfo_width()
                wh = self._calendar_window.winfo_height()
                
                # Also check if click is on dropdown button
                bx = self._dropdown_btn.winfo_rootx()
                by = self._dropdown_btn.winfo_rooty()
                bw = self._dropdown_btn.winfo_width()
                bh = self._dropdown_btn.winfo_height()
                
                in_calendar = wx <= x <= wx + ww and wy <= y <= wy + wh
                in_button = bx <= x <= bx + bw and by <= y <= by + bh
                
                if not in_calendar and not in_button:
                    self._hide_calendar()
        except:
            pass
    
    def _check_and_hide_calendar(self):
        """Check focus and hide calendar if needed."""
        try:
            focused = self.master.focus_get()
            if focused and self._calendar_window:
                # Check if focus is still in calendar
                if str(focused).startswith(str(self._calendar_window)):
                    return
            self._hide_calendar()
        except:
            self._hide_calendar()
    
    def _hide_calendar(self):
        """Hide the calendar dropdown."""
        if not self._calendar_visible:
            return
        
        try:
            if self._calendar_window:
                self._calendar_window.destroy()
                self._calendar_window = None
            self._calendar = None
        except:
            pass
        
        self._calendar_visible = False
        self._dropdown_btn.config(text='▼')
        
        # Remove click outside binding
        try:
            self.master.winfo_toplevel().unbind('<Button-1>')
        except:
            pass
        
        # Fire event
        self.CalendarClosed(self, type('EventArgs', (), {'Data': {}})())
    
    def _fire_value_changed(self, old_value, new_value):
        """Fire the ValueChanged event."""
        e = type('EventArgs', (), {
            'Data': {
                'OldValue': old_value,
                'Value': new_value,
                'NewValue': new_value
            }
        })()
        self.ValueChanged(self, e)
    
    # ===========================================
    # Properties
    # ===========================================
    
    @property
    def Value(self):
        """Gets or sets the selected date value."""
        return self._value
    
    @Value.setter
    def Value(self, value):
        if not isinstance(value, datetime):
            if isinstance(value, date):
                value = datetime.combine(value, datetime.min.time())
            else:
                raise ValueError("Value must be a datetime or date object")
        
        if value < self._min_date:
            value = self._min_date
        if value > self._max_date:
            value = self._max_date
        
        old_value = self._value
        self._value = value
        self._update_display()
        
        if old_value != value:
            self._fire_value_changed(old_value, value)
    
    @property
    def Format(self):
        """Gets or sets the date format."""
        return self._format
    
    @Format.setter
    def Format(self, value):
        self._format = value
        self._update_display()
    
    @property
    def CustomFormat(self):
        """Gets or sets the custom format string."""
        return self._custom_format
    
    @CustomFormat.setter
    def CustomFormat(self, value):
        self._custom_format = value
        if self._format == DateFormat.Custom:
            self._update_display()
    
    @property
    def MinDate(self):
        """Gets or sets the minimum selectable date."""
        return self._min_date
    
    @MinDate.setter
    def MinDate(self, value):
        self._min_date = value
        if self._value < value:
            self.Value = value
    
    @property
    def MaxDate(self):
        """Gets or sets the maximum selectable date."""
        return self._max_date
    
    @MaxDate.setter
    def MaxDate(self, value):
        self._max_date = value
        if self._value > value:
            self.Value = value
    
    @property
    def CalendarVisible(self):
        """Gets whether the calendar dropdown is visible."""
        return self._calendar_visible
    
    @property
    def Enabled(self):
        """Gets or sets whether the control is enabled."""
        return self._enabled
    
    @Enabled.setter
    def Enabled(self, value):
        self._enabled = value
        if self._text_entry and self._dropdown_btn:
            state = 'normal' if value else 'disabled'
            self._text_entry.config(state=state)
            self._dropdown_btn.config(state=state)
    
    @property
    def ReadOnly(self):
        """Gets or sets whether the text field is read-only."""
        return self._read_only
    
    @ReadOnly.setter
    def ReadOnly(self, value):
        self._read_only = value
        if self._text_entry:
            state = 'readonly' if value else 'normal'
            self._text_entry.config(state=state)
    
    @property
    def BackColor(self):
        """Gets or sets the background color."""
        return self._back_color
    
    @BackColor.setter
    def BackColor(self, value):
        self._back_color = value
        if self._text_entry:
            self._text_entry.config(bg=value)
        if self._frame:
            self._frame.config(bg=value)
    
    @property
    def ForeColor(self):
        """Gets or sets the foreground color."""
        return self._fore_color
    
    @ForeColor.setter
    def ForeColor(self, value):
        self._fore_color = value
        if self._text_entry:
            self._text_entry.config(fg=value)
    
    # ===========================================
    # Methods
    # ===========================================
    
    def ShowCalendar(self):
        """Programmatically show the calendar dropdown."""
        self._show_calendar()
    
    def HideCalendar(self):
        """Programmatically hide the calendar dropdown."""
        self._hide_calendar()
    
    def Focus(self):
        """Set focus to the text field."""
        self._text_entry.focus_set()
    
    def SelectAll(self):
        """Select all text in the text field."""
        self._text_entry.select_range(0, 'end')
    
    def Clear(self):
        """Clear the text field and set value to today."""
        self.Value = datetime.now()

