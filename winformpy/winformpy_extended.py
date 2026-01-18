"""
WinFormPy Extended Controls Module
=================================

This module provides extended UI controls and advanced layout management 
components that build upon the core WinFormPy library. 

Controls included:
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
