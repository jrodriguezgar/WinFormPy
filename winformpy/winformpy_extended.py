"""
WinFormPy Extended Controls Module
=================================

This module provides extended UI controls and advanced layout management 
components that build upon the core WinFormPy library. 

Controls included:
- PhotoImage: Wrapper for tkinter.PhotoImage to avoid direct tkinter usage.
- ExtendedLabel: Label with dynamic text wrapping.
- ToggleSwitch: WinUI 3 style toggle switch component.
- Expander: Collapsible container for organizing UI content.
- WinUI 3 simulated themes (Colors and Fonts).
"""

# =============================================================
# Module: winformpy_extended.py
# Author: DatamanEdge
# Date: 2025-12-08
# Version: 1.0.1
# Description: 
# WinFormPy Extension for custom controls and advanced layout management.
# =============================================================

import tkinter as tk
import tkinter.ttk as ttk
import sys
import os

# To avoid circular imports with __init__.py and ensure we get the core classes
# we try to import directly from the winformpy module file.
try:
    # Try relative import first (when part of a package)
    from .winformpy import (
        Label, AnchorStyles, ContentAlignment, TabControl, 
        TabAlignment, Panel, Button, DockStyle, FlatStyle,
        TextBox, ProgressBar
    )
except (ImportError, ValueError):
    try:
        # Try absolute import from the module file
        from winformpy import (
            Label, AnchorStyles, ContentAlignment, TabControl, 
            TabAlignment, Panel, Button, DockStyle, FlatStyle,
            TextBox, ProgressBar
        )
    except ImportError:
        # Fallback for direct execution or unusual path setups
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.append(current_dir)
        from winformpy import (
            Label, AnchorStyles, ContentAlignment, TabControl, 
            TabAlignment, Panel, Button, DockStyle, FlatStyle,
            TextBox, ProgressBar
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


# =============================================================================
# WinUI 3 Controls Section
# =============================================================================
# Simulated WinUI 3 controls using Tkinter. All controls in this section
# use the WinUI prefix and follow Windows 11 design guidelines.

class WinUIColors:
    """Basic WinUI 3 colors for UI simulation."""
    Accent = "#0078D4"
    AccentText = "#FFFFFF"
    WindowBg = "#FFFFFF"
    ContentBg = "#F3F3F3"
    TextPrimary = "#000000"
    TextSecondary = "#666666"
    Border = "#CCCCCC"
    CardBg = "#FFFFFF"
    CardBorder = "#E5E5E5"


class WinUIFonts:
    """Basic WinUI 3 fonts for UI simulation."""
    Title = ("Segoe UI", 16, "bold")
    Subtitle = ("Segoe UI", 14)
    Body = ("Segoe UI", 12)
    Caption = ("Segoe UI", 10)

class WinUIToggleSwitch(Panel):
    """
    WinUI 3 ToggleSwitch simulation using a Canvas.
    Automatically inherits BackColor from parent control.
    """
    def __init__(self, parent, text="Toggle", on_toggle=None):
        super().__init__(parent)
        self.Size = (200, 30)
        
        # Inherit background color from parent
        self._bg_color = self._get_parent_bg_color(parent)
        self._is_on = False
        self._command = on_toggle
        
        # 1. Text label (Right of switch)
        self.label = Label(self)
        self.label.Text = text
        self.label.AutoSize = True
        self.label.Location = (50, 4) # Position after the switch graphics
        self.label.Font = WinUIFonts.Body
        self.label.BackColor = self._bg_color
        self.label.ForeColor = WinUIColors.TextPrimary

        # 2. Switch graphic (using tk canvas direct for shape drawing)
        # We use direct tk access as WinFormPy doesn't have drawing primitives yet
        self.canvas = tk.Canvas(self._tk_widget, width=40, height=20, 
                                bg=self._bg_color, highlightthickness=0)
        self.canvas.place(x=0, y=4)
        
        # Apply background to all internal widgets
        self._apply_background()
        
        # Draw initial state (OFF)
        self._draw_switch()
        
        # Click events
        self.canvas.bind("<Button-1>", lambda e: self.toggle())
        self.label.Click = lambda s, e: self.toggle()

    def _get_parent_bg_color(self, parent):
        """Get background color from parent control."""
        # Try to get BackColor from parent
        if hasattr(parent, 'BackColor') and parent.BackColor:
            return parent.BackColor
        # Try to get from parent's tk widget
        if hasattr(parent, '_tk_widget') and parent._tk_widget:
            try:
                return parent._tk_widget.cget('bg')
            except:
                pass
        # Default to CardBg (white) for WinUI style
        return WinUIColors.CardBg

    def _apply_background(self):
        """Apply background color to all internal widgets."""
        # Apply to Panel's internal containers
        if hasattr(self, '_tk_widget') and self._tk_widget:
            try:
                self._tk_widget.configure(bg=self._bg_color)
            except:
                pass
        if hasattr(self, '_container') and self._container:
            try:
                self._container.configure(bg=self._bg_color)
            except:
                pass
        # Apply to canvas
        if hasattr(self, 'canvas') and self.canvas:
            try:
                self.canvas.configure(bg=self._bg_color)
            except:
                pass
        # Apply to label
        if hasattr(self, 'label') and self.label:
            self.label.BackColor = self._bg_color

    @property
    def BackColor(self):
        return self._bg_color
    
    @BackColor.setter
    def BackColor(self, value):
        self._bg_color = value
        self._apply_background()
        # Redraw switch to update OFF state background
        if hasattr(self, 'canvas'):
            self._draw_switch()

    def _draw_switch(self):
        """Redraws the switch based on current state."""
        self.canvas.delete("all")
        
        # Theme colors
        fill = WinUIColors.Accent if self._is_on else self._bg_color
        outline = WinUIColors.Accent if self._is_on else WinUIColors.TextSecondary
        knob_color = WinUIColors.AccentText if self._is_on else WinUIColors.TextSecondary
        
        # Knob (circle) position
        kx = 28 if self._is_on else 12
        
        # Background CAPSULE shape
        # Simulated using a thick line with round cap style
        self.canvas.create_line(10, 10, 30, 10, width=18, fill=fill, capstyle="round")
        
        if not self._is_on:
             # Border for OFF state
             self.canvas.create_line(10, 10, 30, 10, width=16, fill=self._bg_color, capstyle="round")
             self.canvas.create_line(10, 10, 30, 10, width=2, fill=outline, capstyle="round")

        # Knob circle
        self.canvas.create_oval(kx-6, 4, kx+6, 16, fill=knob_color, outline="")

    def toggle(self):
        """Toggles the switch state and triggers the command."""
        self._is_on = not self._is_on
        self._draw_switch()
        if self._command:
            self._command(self._is_on)


class WinUIExpander(Panel):
    """
    WinUI 3 Expander: A container control with a header and a collapsible content area.
    Uses WinUI 3 accent color (blue) for the header text and arrow.
    Automatically inherits BackColor from parent control.
    """
    def __init__(self, parent, title="Expander Title", height_expanded=150):
        super().__init__(parent)
        self.dock_style = DockStyle.Top
        self.expanded_height = height_expanded
        self.collapsed_height = 40
        self.Height = self.collapsed_height
        self.is_expanded = False
        self._title = title
        
        # Inherit background color from parent
        self._bg_color = self._get_parent_bg_color(parent)
        
        # Header (Clickable button) - Create FIRST for Top dock
        self.header = Button(self)
        self.header.Text = "  ▶  " + title # Unicode arrow icon
        self.header.Dock = DockStyle.Top
        self.header.Height = 40
        self.header.FlatStyle = FlatStyle.Flat
        self.header.TextAlign = 'w'
        self.header.BackColor = self._bg_color
        self.header.ForeColor = WinUIColors.Accent  # Blue accent color
        if hasattr(self.header, '_tk_widget'):
            self.header._tk_widget.configure(borderwidth=0, highlightthickness=0, bg=self._bg_color)
        
        self.header.Click = self.toggle

        # Content panel (where children controls are added)
        self.content = Panel(self)
        self.content.Dock = DockStyle.Fill
        self.content.Visible = False # Hidden by default
        
        # Visual card style - accent colored border at bottom
        self._border = Panel(self) # Bottom border/separator with accent
        self._border.Height = 2
        self._border.Dock = DockStyle.Bottom
        self._border.BackColor = WinUIColors.Accent  # Blue accent border
        
        # Apply background to all
        self._apply_background()

    def _get_parent_bg_color(self, parent):
        """Get background color from parent control."""
        # Try to get BackColor from parent
        if hasattr(parent, 'BackColor') and parent.BackColor:
            return parent.BackColor
        # Try to get from parent's tk widget
        if hasattr(parent, '_tk_widget') and parent._tk_widget:
            try:
                return parent._tk_widget.cget('bg')
            except:
                pass
        # Default to CardBg (white) for WinUI style
        return WinUIColors.CardBg

    def _apply_background(self):
        """Apply background color to all internal widgets."""
        # Apply to Panel's internal containers
        if hasattr(self, '_tk_widget') and self._tk_widget:
            try:
                self._tk_widget.configure(bg=self._bg_color)
            except:
                pass
        if hasattr(self, '_container') and self._container:
            try:
                self._container.configure(bg=self._bg_color)
            except:
                pass
        # Apply to header
        if hasattr(self, 'header') and self.header:
            self.header.BackColor = self._bg_color
            if hasattr(self.header, '_tk_widget') and self.header._tk_widget:
                try:
                    self.header._tk_widget.configure(bg=self._bg_color)
                except:
                    pass
        # Apply to content
        if hasattr(self, 'content') and self.content:
            self.content.BackColor = self._bg_color
            if hasattr(self.content, '_tk_widget') and self.content._tk_widget:
                try:
                    self.content._tk_widget.configure(bg=self._bg_color)
                except:
                    pass
            if hasattr(self.content, '_container') and self.content._container:
                try:
                    self.content._container.configure(bg=self._bg_color)
                except:
                    pass

    @property
    def BackColor(self):
        return self._bg_color
    
    @BackColor.setter
    def BackColor(self, value):
        self._bg_color = value
        self._apply_background()

    def toggle(self, sender, e):
        """Toggles the expanded/collapsed state of the content panel."""
        self.is_expanded = not self.is_expanded
        
        if self.is_expanded:
            self.Height = self.expanded_height
            self.content.Visible = True
            self.header.Text = "  ▼  " + self._title  # Down arrow when expanded
        else:
            self.Height = self.collapsed_height
            self.content.Visible = False
            self.header.Text = "  ▶  " + self._title  # Right arrow when collapsed


# =============================================================================
# WinUI 3 Extended Controls
# =============================================================================

# Import additional base controls for WinUI extensions
try:
    from .winformpy import TextBox, ProgressBar, ProgressBarStyle
except ImportError:
    try:
        from winformpy import TextBox, ProgressBar, ProgressBarStyle
    except ImportError:
        pass


class WinUITextBox(TextBox):
    """
    WinUI 3 styled TextBox with accent underline.
    
    Features:
    - Thin accent-colored underline at the bottom (1px)
    - No visible borders - clean modern look
    - Inherits all standard TextBox functionality
    - Customizable underline color via UnderlineColor property
    """
    
    def __init__(self, master_form, props=None):
        if props is None:
            props = {}
        
        # Store underline color before calling super
        self._underline_color = props.pop('UnderlineColor', WinUIColors.Accent)
        
        super().__init__(master_form, props)
        
        # Remove ALL borders from Entry widget - WinUI style has no border, only underline
        # Must apply ALL these settings to completely remove borders on Windows
        if not self.Multiline and hasattr(self, '_tk_widget') and self._tk_widget:
            try:
                bg_color = self._tk_widget.cget('background')
                self._tk_widget.configure(
                    relief='flat',
                    bd=0,
                    borderwidth=0,
                    highlightthickness=0,
                    highlightbackground=bg_color,
                    highlightcolor=bg_color,
                    insertwidth=1,  # Thin cursor
                    selectborderwidth=0  # No selection border
                )
                # Additional Windows-specific border removal
                try:
                    self._tk_widget.configure(readonlybackground=bg_color)
                except tk.TclError:
                    pass
            except Exception:
                pass
        
        # Create underline for single-line TextBox only
        if not self.Multiline:
            self._underline = tk.Frame(
                self.master, 
                height=2,  # 2px for better visibility
                bg=self._underline_color, 
                highlightthickness=0, 
                bd=0
            )
            # Position underline
            self._place_underline()
    
    def _place_underline(self):
        """Position the accent underline below the TextBox."""
        if hasattr(self, '_underline') and self._underline:
            try:
                self._underline.place(
                    x=self.Left, 
                    y=self.Top + self.Height - 1, 
                    width=self.Width, 
                    height=1
                )
            except Exception:
                pass
    
    def _place_control(self, width=None, height=None):
        """Override to also position the underline."""
        super()._place_control(width, height)
        self._place_underline()
    
    def set_Visible(self, value):
        """Override to sync underline visibility."""
        super().set_Visible(value)
        
        if hasattr(self, '_underline') and self._underline:
            try:
                if value and self._visible:
                    self._place_underline()
                else:
                    self._underline.place_forget()
            except Exception:
                pass
    
    @property
    def UnderlineColor(self):
        """Gets the accent underline color."""
        return getattr(self, '_underline_color', WinUIColors.Accent)
    
    @UnderlineColor.setter
    def UnderlineColor(self, value):
        """Sets the accent underline color."""
        self._underline_color = value
        if hasattr(self, '_underline') and self._underline:
            try:
                self._underline.configure(bg=value)
            except Exception:
                pass


class WinUIProgressBar(ProgressBar):
    """
    WinUI 3 styled ProgressBar with accent colors.
    
    Features:
    - Blue accent bar color (default: #0078D4)
    - Light gray trough/background
    - Customizable via BarColor and TroughColor properties
    """
    
    def __init__(self, master_form, props=None):
        if props is None:
            props = {}
        
        # Extract WinUI colors before calling super
        # Use WinUI 3 accent blue (#0078D4) and light gray trough
        self._bar_color = props.pop('BarColor', '#0078D4')
        self._trough_color = props.pop('TroughColor', '#E5E5E5')
        
        super().__init__(master_form, props)
        
        # Create unique style for this instance
        self._style_name = f"WinUI.Progressbar.{id(self)}.Horizontal.TProgressbar"
        self._style = ttk.Style()
        
        # Use 'clam' theme as base for better color support (Windows native theme ignores colors)
        try:
            self._style.theme_use('clam')
        except Exception:
            pass
        
        # Apply WinUI colors
        self._apply_winui_colors()
        
        # Update widget to use new style
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._tk_widget.configure(style=self._style_name)
    
    def _apply_winui_colors(self):
        """Apply WinUI accent colors to the progress bar style."""
        try:
            self._style.configure(
                self._style_name, 
                background=self._bar_color, 
                troughcolor=self._trough_color,
                bordercolor=self._trough_color,
                lightcolor=self._bar_color,
                darkcolor=self._bar_color
            )
        except Exception:
            pass
    
    @property
    def BarColor(self):
        """Gets the progress bar fill color."""
        return getattr(self, '_bar_color', WinUIColors.Accent)
    
    @BarColor.setter
    def BarColor(self, value):
        """Sets the progress bar fill color."""
        self._bar_color = value
        self._apply_winui_colors()
    
    @property
    def TroughColor(self):
        """Gets the progress bar background/trough color."""
        return getattr(self, '_trough_color', '#E5E5E5')
    
    @TroughColor.setter
    def TroughColor(self, value):
        """Sets the progress bar background/trough color."""
        self._trough_color = value
        self._apply_winui_colors()


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
