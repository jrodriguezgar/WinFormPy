"""
WinUI 3 Controls Module for WinFormPy
=====================================

This module provides WinUI 3 styled controls that follow Windows 11 design guidelines.
All controls inherit from WinFormPy base controls and apply WinUI 3 visual styling.

Controls included:
- WinUIButton: Button with WinUI 3 accent styling
- WinUITextBox: TextBox with accent underline (no borders)
- WinUILabel: Label with WinUI 3 typography
- WinUIProgressBar: ProgressBar with accent colors
- WinUIToggleSwitch: Toggle switch control
- WinUIExpander: Collapsible container with header
- WinUICheckBox: CheckBox with WinUI 3 styling
- WinUIRadioButton: RadioButton with WinUI 3 styling
- WinUIComboBox: ComboBox with WinUI 3 styling
- WinUIPanel: Panel with card-style background

Design Guidelines:
- Accent color: #0078D4 (Blue)
- Typography: Segoe UI font family
- Rounded corners where applicable
- Minimal borders, emphasis on content
- Subtle shadows for elevation
"""

# =============================================================
# Module: winui3.py
# Author: DatamanEdge
# Date: 2025-01-27
# Version: 1.0.0
# Description: 
# WinUI 3 styled controls for WinFormPy
# =============================================================

import tkinter as tk
import tkinter.ttk as ttk
import sys
import os

# Import WinFormPy base controls
try:
    # Try relative import first (when part of a package)
    from .winformpy import (
        Button, Label, TextBox, Panel, CheckBox, RadioButton, ComboBox,
        ProgressBar, ProgressBarStyle, DockStyle, FlatStyle, 
        ContentAlignment, AnchorStyles
    )
except (ImportError, ValueError):
    try:
        # Try absolute import from the module file
        from winformpy import (
            Button, Label, TextBox, Panel, CheckBox, RadioButton, ComboBox,
            ProgressBar, ProgressBarStyle, DockStyle, FlatStyle,
            ContentAlignment, AnchorStyles
        )
    except ImportError:
        # Fallback for direct execution or unusual path setups
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.append(current_dir)
        from winformpy import (
            Button, Label, TextBox, Panel, CheckBox, RadioButton, ComboBox,
            ProgressBar, ProgressBarStyle, DockStyle, FlatStyle,
            ContentAlignment, AnchorStyles
        )


# =============================================================================
# WinUI 3 Color Palette
# =============================================================================

class WinUIColors:
    """
    WinUI 3 color palette following Windows 11 design system.
    
    Colors are based on the Fluent Design System:
    https://docs.microsoft.com/en-us/windows/apps/design/style/color
    """
    # Primary accent colors
    Accent = "#0078D4"  # Primary blue accent
    AccentDark1 = "#106EBE"
    AccentDark2 = "#005A9E"
    AccentDark3 = "#004578"
    AccentLight1 = "#429CE3"
    AccentLight2 = "#5EB3E4"
    AccentLight3 = "#74C0E5"
    
    # Text colors
    AccentText = "#FFFFFF"  # Text on accent background
    TextPrimary = "#000000"
    TextSecondary = "#666666"
    TextTertiary = "#949494"
    TextDisabled = "#CCCCCC"
    
    # Background colors
    WindowBg = "#FFFFFF"
    ContentBg = "#F3F3F3"
    CardBg = "#FFFFFF"
    LayerBg = "#FAFAFA"
    
    # Border colors
    Border = "#E5E5E5"
    BorderFocused = "#0078D4"
    CardBorder = "#EBEBEB"
    
    # State colors
    ErrorBg = "#FDE7E9"
    ErrorText = "#C42B1C"
    WarningBg = "#FFF4CE"
    WarningText = "#9D5D00"
    SuccessBg = "#DFF6DD"
    SuccessText = "#107C10"
    InfoBg = "#E7F3FD"
    InfoText = "#0078D4"
    
    # Control states
    ControlBorder = "#E5E5E5"
    ControlBorderHover = "#0078D4"
    ControlBorderPressed = "#005A9E"
    ControlBg = "#FFFFFF"
    ControlBgHover = "#F9F9F9"
    ControlBgPressed = "#F3F3F3"
    ControlBgDisabled = "#F3F3F3"


# =============================================================================
# WinUI 3 Typography
# =============================================================================

class WinUIFonts:
    """
    WinUI 3 typography system using Segoe UI font family.
    
    Based on the Windows 11 type ramp:
    https://docs.microsoft.com/en-us/windows/apps/design/style/typography
    """
    # Display styles (large headings)
    Display = ("Segoe UI", 68, "normal")
    
    # Title styles
    TitleLarge = ("Segoe UI", 40, "bold")
    Title = ("Segoe UI", 28, "bold")
    
    # Subtitle styles
    SubtitleLarge = ("Segoe UI", 20, "bold")
    Subtitle = ("Segoe UI", 16, "bold")
    
    # Body styles
    BodyLarge = ("Segoe UI", 18, "normal")
    BodyStrong = ("Segoe UI", 14, "bold")
    Body = ("Segoe UI", 14, "normal")
    
    # Caption styles
    Caption = ("Segoe UI", 12, "normal")
    CaptionStrong = ("Segoe UI", 12, "bold")
    
    # Legacy compatibility
    Header = ("Segoe UI", 16, "bold")  # Alias for Subtitle
    Default = ("Segoe UI", 12, "normal")  # Alias for Caption


# =============================================================================
# WinUI 3 Button
# =============================================================================

class WinUIButton(Button):
    """
    WinUI 3 styled Button with accent color and hover effects.
    
    Features:
    - Multiple button styles: Accent (default), Success, Warning, Danger, Standard
    - Flat style with no borders
    - Customizable via ButtonStyle parameter or AccentColor property
    - Inherits all Button functionality
    
    Example:
        # Accent button (default)
        btn = WinUIButton(form, {
            'Text': 'Click Me',
            'Width': 120,
            'Height': 32
        })
        
        # Success button
        btn_success = WinUIButton(form, {
            'Text': 'Save',
            'ButtonStyle': 'Success'
        })
    """
    
    def __init__(self, master_form, props=None):
        if props is None: props = {}
        
        # Detectar estilo antes de aplicar defaults
        style = props.pop('ButtonStyle', 'Accent')
        colors = {
            'Accent': (WinUIColors.Accent, WinUIColors.AccentText),
            'Success': (WinUIColors.SuccessText, WinUIColors.AccentText),
            'Warning': (WinUIColors.WarningText, WinUIColors.AccentText),
            'Danger': (WinUIColors.ErrorText, WinUIColors.AccentText),
            'Standard': (WinUIColors.ControlBg, WinUIColors.TextPrimary)
        }
        bg, fg = colors.get(style, colors['Accent'])

        defaults = {
            'BackColor': bg,
            'ForeColor': fg,
            'FlatStyle': FlatStyle.Flat,
            'Font': WinUIFonts.Body,
            'Height': 32
        }
        
        for key, value in defaults.items():
            if key not in props: props[key] = value
            
        super().__init__(master_form, props)
        
        # Remove borders for clean WinUI look using WinFormPy properties
        self.BorderWidth = 0
        self.HighlightThickness = 0
        # Si es Standard, añadir un borde sutil para que no desaparezca en el fondo
        if style == 'Standard':
            self.HighlightThickness = 1
        
        # Store the button style
        self._button_style = style
    
    @property
    def AccentColor(self):
        """Gets the accent background color."""
        return self.BackColor
    
    @AccentColor.setter
    def AccentColor(self, value):
        """Sets the accent background color."""
        self.BackColor = value
    
    @property
    def ButtonStyle(self):
        """Gets the button style (Accent, Success, Warning, Danger, Standard)."""
        return getattr(self, '_button_style', 'Accent')
    
    @ButtonStyle.setter
    def ButtonStyle(self, value):
        """Sets the button style and applies corresponding colors."""
        colors = {
            'Accent': (WinUIColors.Accent, WinUIColors.AccentText),
            'Success': (WinUIColors.SuccessText, WinUIColors.AccentText),
            'Warning': (WinUIColors.WarningText, WinUIColors.AccentText),
            'Danger': (WinUIColors.ErrorText, WinUIColors.AccentText),
            'Standard': (WinUIColors.ControlBg, WinUIColors.TextPrimary)
        }
        bg, fg = colors.get(value, colors['Accent'])
        self.BackColor = bg
        self.ForeColor = fg
        self._button_style = value
        
        # Update border for Standard style using WinFormPy properties
        if value == 'Standard':
            self.HighlightThickness = 1
        else:
            self.HighlightThickness = 0


# =============================================================================
# WinUI 3 Label
# =============================================================================

class WinUILabel(Label):
    """
    WinUI 3 styled Label with typography support.
    
    Features:
    - Segoe UI font by default
    - Typography presets (Title, Subtitle, Body, Caption)
    - TextPrimary color by default
    
    Example:
        lbl = WinUILabel(form, {
            'Text': 'Title Text',
            'Typography': WinUIFonts.Title
        })
    """
    
    def __init__(self, master_form, props=None):
        if props is None:
            props = {}
        
        # Extract Typography before calling super
        typography = props.pop('Typography', WinUIFonts.Body)
        
        # Apply WinUI 3 defaults
        defaults = {
            'Font': typography,
            'ForeColor': WinUIColors.TextPrimary,
            'BackColor': WinUIColors.WindowBg
        }
        
        # Merge with user props
        for key, value in defaults.items():
            if key not in props:
                props[key] = value
        
        super().__init__(master_form, props)
    
    @property
    def Typography(self):
        """Gets the typography style."""
        return self.Font
    
    @Typography.setter
    def Typography(self, value):
        """Sets the typography style using WinUIFonts."""
        self.Font = value


# =============================================================================
# WinUI 3 TextBox
# =============================================================================

class WinUITextBox(TextBox):
    """
    WinUI 3 styled TextBox with accent underline.
    
    Features:
    - Thin underline at the bottom that changes color on focus
    - Gray when idle, accent color when focused
    - No visible borders - clean modern look
    - Inherits all standard TextBox functionality
    - Customizable underline color via UnderlineColor property
    
    Example:
        txt = WinUITextBox(form, {
            'Width': 200,
            'Height': 32,
            'PlaceholderText': 'Enter text...'
        })
    """
    
    def __init__(self, master_form, props=None):
        if props is None: props = {}
        self._accent_color = props.get('UnderlineColor', WinUIColors.Accent)
        self._idle_color = WinUIColors.TextTertiary
        
        super().__init__(master_form, props)
        
        if not self.Multiline and hasattr(self, '_tk_widget'):
            # Crear la línea de acento usando Panel de WinFormPy en lugar de tk.Frame
            self._underline = Panel(self.master)
            self._underline.Height = 2
            self._underline.BackColor = self._idle_color
            self._place_underline()
            
            # Eventos para cambiar el color de la línea al entrar/salir usando BindEvent de WinFormPy
            self.BindEvent('FocusIn', lambda sender, e: setattr(self._underline, 'BackColor', self._accent_color))
            self.BindEvent('FocusOut', lambda sender, e: setattr(self._underline, 'BackColor', self._idle_color))

    def _place_underline(self):
        if hasattr(self, '_underline'):
            self._underline.Left = self.Left
            self._underline.Top = self.Top + self.Height - 1
            self._underline.Width = self.Width

    def _place_control(self, width=None, height=None):
        super()._place_control(width, height)
        self._place_underline()
    
    def set_Visible(self, value):
        """Override to sync underline visibility."""
        super().set_Visible(value)
        
        if hasattr(self, '_underline') and self._underline:
            try:
                if value and self._visible:
                    self._place_underline()
                    self._underline.Visible = True
                else:
                    self._underline.Visible = False
            except Exception:
                pass
            try:
                if value and self._visible:
                    self._place_underline()
                else:
                    self._underline.place_forget()
            except Exception:
                pass
    
    @property
    def UnderlineColor(self):
        """Gets the accent underline color (used when focused)."""
        return getattr(self, '_accent_color', WinUIColors.Accent)
    
    @UnderlineColor.setter
    def UnderlineColor(self, value):
        """Sets the accent underline color (used when focused)."""
        self._accent_color = value

# =============================================================================
# WinUI 3 ProgressBar
# =============================================================================

class WinUIProgressBar(ProgressBar):
    """
    WinUI 3 styled ProgressBar with accent colors.
    
    Features:
    - Blue accent bar color (default: #0078D4)
    - Light gray trough/background (#E5E5E5)
    - Customizable via BarColor and TroughColor properties
    
    Example:
        pb = WinUIProgressBar(form, {
            'Width': 200,
            'Height': 4,
            'Value': 50
        })
    """
    
    def __init__(self, master_form, props=None):
        if props is None:
            props = {}
        
        # Extract WinUI colors before calling super
        self._bar_color = props.pop('BarColor', WinUIColors.Accent)
        self._trough_color = props.pop('TroughColor', WinUIColors.Border)
        
        # Apply WinUI 3 defaults
        defaults = {
            'Height': 4  # Thin progress bar like WinUI 3
        }
        
        # Merge with user props
        for key, value in defaults.items():
            if key not in props:
                props[key] = value
        
        super().__init__(master_form, props)
        
        # Create unique style for this instance
        self._style_name = f"WinUI.Progressbar.{id(self)}.Horizontal.TProgressbar"
        self._style = ttk.Style()
        
        # Use 'clam' theme as base for better color support
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
                darkcolor=self._bar_color,
                thickness=4  # Thin bar
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
        return getattr(self, '_trough_color', WinUIColors.Border)
    
    @TroughColor.setter
    def TroughColor(self, value):
        """Sets the progress bar background/trough color."""
        self._trough_color = value
        self._apply_winui_colors()


# =============================================================================
# WinUI 3 ToggleSwitch
# =============================================================================

class WinUIToggleSwitch(Panel):
    """
    WinUI 3 ToggleSwitch control with animated capsule design.
    
    Features:
    - Capsule-shaped switch with sliding knob
    - Blue accent color when ON
    - Gray outline when OFF
    - Text label on the right
    - Automatically inherits BackColor from parent
    - Callback support via on_toggle parameter
    
    Example:
        switch = WinUIToggleSwitch(
            parent=form,
            text="Enable Feature",
            on_toggle=lambda state: print(f"Toggled: {state}")
        )
    """
    
    def __init__(self, parent, text="Toggle", on_toggle=None):
        """
        Initialize a WinUI 3 ToggleSwitch.
        
        Args:
            parent: Parent container
            text: Label text displayed next to switch
            on_toggle: Callback function called when toggled (receives bool state)
        """
        super().__init__(parent)
        self.Size = (200, 30)
        
        # Inherit background color from parent
        self._bg_color = self._get_parent_bg_color(parent)
        self._is_on = False
        self._command = on_toggle
        
        # Text label (Right of switch)
        self.label = Label(self)
        self.label.Text = text
        self.label.AutoSize = True
        self.label.Location = (50, 4)
        self.label.Font = WinUIFonts.Body
        self.label.BackColor = self._bg_color
        self.label.ForeColor = WinUIColors.TextPrimary

        # Switch graphic using Canvas for custom drawing
        # NOTE: Using direct tk.Canvas access as WinFormPy doesn't have drawing primitives yet
        # This is an exception - Canvas allows custom shape drawing needed for the switch capsule
        # A proper WinFormPy Canvas control should be created in the future
        self.canvas = tk.Canvas(
            self._tk_widget, 
            width=40, 
            height=20, 
            bg=self._bg_color, 
            highlightthickness=0
        )
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
        if hasattr(parent, 'BackColor') and parent.BackColor:
            return parent.BackColor
        if hasattr(parent, '_tk_widget') and parent._tk_widget:
            try:
                return parent._tk_widget.cget('bg')
            except:
                pass
        return WinUIColors.CardBg

    def _apply_background(self):
        """Apply background color to all internal widgets."""
        # Apply to main widget
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
        # Note: Direct tkinter access - canvas.configure() used as WinFormPy Canvas doesn't exist yet
        if hasattr(self, 'canvas') and self.canvas:
            try:
                self.canvas.configure(bg=self._bg_color)
            except:
                pass
        if hasattr(self, 'label') and self.label:
            self.label.BackColor = self._bg_color

    @property
    def BackColor(self):
        """Gets the background color."""
        return self._bg_color
    
    @BackColor.setter
    def BackColor(self, value):
        """Sets the background color."""
        self._bg_color = value
        self._apply_background()
        if hasattr(self, 'canvas'):
            self._draw_switch()

    @property
    def IsOn(self):
        """Gets whether the switch is ON."""
        return self._is_on
    
    @IsOn.setter
    def IsOn(self, value):
        """Sets the switch state without triggering callback."""
        if self._is_on != value:
            self._is_on = value
            self._draw_switch()

    def _draw_switch(self):
        """Redraws the switch based on current state."""
        self.canvas.delete("all")
        
        # Theme colors based on state
        fill = WinUIColors.Accent if self._is_on else self._bg_color
        outline = WinUIColors.Accent if self._is_on else WinUIColors.TextSecondary
        knob_color = WinUIColors.AccentText if self._is_on else WinUIColors.TextSecondary
        
        # Knob position (left when OFF, right when ON)
        kx = 28 if self._is_on else 12
        
        # Background capsule shape (using thick line with round caps)
        self.canvas.create_line(10, 10, 30, 10, width=18, fill=fill, capstyle="round")
        
        if not self._is_on:
            # Border for OFF state
            self.canvas.create_line(10, 10, 30, 10, width=16, fill=self._bg_color, capstyle="round")
            self.canvas.create_line(10, 10, 30, 10, width=2, fill=outline, capstyle="round")

        # Knob circle
        self.canvas.create_oval(kx-6, 4, kx+6, 16, fill=knob_color, outline="")

    def toggle(self):
        """Toggles the switch state and triggers the callback."""
        self._is_on = not self._is_on
        self._draw_switch()
        if self._command:
            self._command(self._is_on)


# =============================================================================
# WinUI 3 Expander
# =============================================================================

class WinUIExpander(Panel):
    """
    WinUI 3 Expander: Collapsible container with header and content area.
    
    Features:
    - Clickable header with expand/collapse arrow
    - Blue accent color for header text and arrow
    - Content panel that shows/hides on toggle
    - Customizable expanded height
    - Automatically inherits BackColor from parent
    - Blue accent border at bottom
    
    Example:
        expander = WinUIExpander(
            parent=form,
            title="Advanced Settings",
            height_expanded=200
        )
        
        # Add controls to expander.content
        lbl = Label(expander.content)
        lbl.Text = "Content goes here"
    """
    
    def __init__(self, parent, title="Expander Title", height_expanded=150):
        """
        Initialize a WinUI 3 Expander.
        
        Args:
            parent: Parent container
            title: Header text
            height_expanded: Height when expanded (collapsed is always 40px)
        """
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
        self.header.Text = "  ▶  " + title  # Right arrow when collapsed
        self.header.Dock = DockStyle.Top
        self.header.Height = 40
        self.header.FlatStyle = FlatStyle.Flat
        self.header.TextAlign = 'w'
        self.header.BackColor = self._bg_color
        self.header.ForeColor = WinUIColors.Accent  # Blue accent color
        self.header.Font = WinUIFonts.Body
        if hasattr(self.header, '_tk_widget'):
            self.header._tk_widget.configure(borderwidth=0, highlightthickness=0, bg=self._bg_color)
        
        self.header.Click = self.toggle

        # Content panel (where child controls are added)
        self.content = Panel(self)
        self.content.Dock = DockStyle.Fill
        self.content.Visible = False  # Hidden by default
        
        # Accent border at bottom
        self._border = Panel(self)
        self._border.Height = 2
        self._border.Dock = DockStyle.Bottom
        self._border.BackColor = WinUIColors.Accent
        
        # Apply background to all
        self._apply_background()

    def _get_parent_bg_color(self, parent):
        """Get background color from parent control."""
        if hasattr(parent, 'BackColor') and parent.BackColor:
            return parent.BackColor
        if hasattr(parent, '_tk_widget') and parent._tk_widget:
            try:
                return parent._tk_widget.cget('bg')
            except:
                pass
        return WinUIColors.CardBg

    def _apply_background(self):
        """Apply background color to all internal widgets."""
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
        if hasattr(self, 'header') and self.header:
            self.header.BackColor = self._bg_color
            if hasattr(self.header, '_tk_widget') and self.header._tk_widget:
                try:
                    self.header._tk_widget.configure(bg=self._bg_color)
                except:
                    pass
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
        """Gets the background color."""
        return self._bg_color
    
    @BackColor.setter
    def BackColor(self, value):
        """Sets the background color."""
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
# WinUI 3 CheckBox
# =============================================================================

class WinUICheckBox(CheckBox):
    """
    WinUI 3 styled CheckBox with accent color.
    
    Features:
    - Blue accent color when checked
    - Segoe UI font
    - Inherits all CheckBox functionality
    
    Example:
        chk = WinUICheckBox(form, {
            'Text': 'Enable feature',
            'Checked': True
        })
    """
    
    def __init__(self, master_form, props=None):
        if props is None:
            props = {}
        
        # Apply WinUI 3 defaults
        defaults = {
            'Font': WinUIFonts.Body,
            'ForeColor': WinUIColors.TextPrimary
        }
        
        # Merge with user props
        for key, value in defaults.items():
            if key not in props:
                props[key] = value
        
        super().__init__(master_form, props)
        
        # Apply accent color styling if possible
        if hasattr(self, '_tk_widget') and self._tk_widget:
            try:
                self._tk_widget.configure(
                    selectcolor=WinUIColors.Accent,
                    activebackground=WinUIColors.ControlBgHover,
                    activeforeground=WinUIColors.TextPrimary
                )
            except Exception:
                pass


# =============================================================================
# WinUI 3 RadioButton
# =============================================================================

class WinUIRadioButton(RadioButton):
    """
    WinUI 3 styled RadioButton with accent color.
    
    Features:
    - Blue accent color when selected
    - Segoe UI font
    - Inherits all RadioButton functionality
    
    Example:
        rb = WinUIRadioButton(form, {
            'Text': 'Option 1',
            'Checked': True
        })
    """
    
    def __init__(self, master_form, props=None):
        if props is None:
            props = {}
        
        # Apply WinUI 3 defaults
        defaults = {
            'Font': WinUIFonts.Body,
            'ForeColor': WinUIColors.TextPrimary
        }
        
        # Merge with user props
        for key, value in defaults.items():
            if key not in props:
                props[key] = value
        
        super().__init__(master_form, props)
        
        # Apply accent color styling
        if hasattr(self, '_tk_widget') and self._tk_widget:
            try:
                self._tk_widget.configure(
                    selectcolor=WinUIColors.Accent,
                    activebackground=WinUIColors.ControlBgHover,
                    activeforeground=WinUIColors.TextPrimary
                )
            except Exception:
                pass


# =============================================================================
# WinUI 3 ComboBox
# =============================================================================

class WinUIComboBox(ComboBox):
    """
    WinUI 3 styled ComboBox.
    
    Features:
    - Clean border styling
    - Segoe UI font
    - Inherits all ComboBox functionality
    
    Example:
        cmb = WinUIComboBox(form, {
            'Width': 200,
            'Items': ['Option 1', 'Option 2', 'Option 3']
        })
    """
    
    def __init__(self, master_form, props=None):
        if props is None:
            props = {}
        
        # Apply WinUI 3 defaults
        defaults = {
            'Font': WinUIFonts.Body,
            'Height': 32
        }
        
        # Merge with user props
        for key, value in defaults.items():
            if key not in props:
                props[key] = value
        
        super().__init__(master_form, props)


# =============================================================================
# WinUI 3 Panel (Card)
# =============================================================================

class WinUIPanel(Panel):
    """
    WinUI 3 styled Panel with card background.
    
    Features:
    - White card background
    - Optional border
    - Inherits all Panel functionality
    
    Example:
        card = WinUIPanel(form, {
            'Width': 300,
            'Height': 200,
            'Padding': 16
        })
    """
    
    def __init__(self, master_form, props=None):
        if props is None:
            props = {}
        
        # Apply WinUI 3 defaults
        defaults = {
            'BackColor': WinUIColors.CardBg
        }
        
        # Merge with user props
        for key, value in defaults.items():
            if key not in props:
                props[key] = value
        
        super().__init__(master_form, props)

# =============================================================================
# WinUI 3 Slider
# =============================================================================

class WinUISlider(Panel):
    """Control deslizante con estética de Windows 11."""
    def __init__(self, parent, props=None):
        super().__init__(parent)
        self.Height = 32
        self.Width = props.get('Width', 200) if props else 200
        self._value = 0.5 # 0.0 a 1.0
        
        # NOTE: Using direct tk.Canvas access as WinFormPy doesn't have drawing primitives yet
        # This is an exception - Canvas allows drawing custom lines and circles for the slider
        # A proper WinFormPy Canvas control should be created in the future
        self.canvas = tk.Canvas(self._tk_widget, height=32, width=self.Width, 
                               bg=WinUIColors.WindowBg, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self._draw_slider()
        
        # Use BindEvent would be ideal but canvas.bind is needed for coordinates
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<Button-1>", self._on_drag)

    def _draw_slider(self):
        self.canvas.delete("all")
        w, h = self.Width, 32
        mid_y = h // 2
        # Línea de fondo
        self.canvas.create_line(10, mid_y, w-10, mid_y, fill=WinUIColors.Border, width=4, capstyle="round")
        # Línea de progreso
        self.canvas.create_line(10, mid_y, 10 + (w-20)*self._value, mid_y, fill=WinUIColors.Accent, width=4, capstyle="round")
        # El "Thumb" (círculo)
        cx = 10 + (w-20)*self._value
        self.canvas.create_oval(cx-8, mid_y-8, cx+8, mid_y+8, fill=WinUIColors.Accent, outline="white", width=2)

    def _on_drag(self, event):
        rel_x = max(10, min(event.x, self.Width - 10))
        self._value = (rel_x - 10) / (self.Width - 20)
        self._draw_slider()

# =============================================================================
# WinUI 3 HyperlinkButton
# =============================================================================

class WinUIHyperlinkButton(Button):
    """Botón que se comporta y luce como un enlace."""
    def __init__(self, master_form, props=None):
        if props is None: props = {}
        props['BackColor'] = props.get('BackColor', WinUIColors.WindowBg)
        props['ForeColor'] = WinUIColors.Accent
        props['FlatStyle'] = FlatStyle.Flat
        super().__init__(master_form, props)
        
        # Store original font for hover effect
        self._original_font = WinUIFonts.Body
        self._underline_font = (WinUIFonts.Body[0], WinUIFonts.Body[1], "underline")
        
        # Use WinFormPy BindEvent for hover effects
        self.BindEvent('Enter', self._on_enter)
        self.BindEvent('Leave', self._on_leave)
    
    def _on_enter(self, sender, e):
        """Handler for mouse enter event."""
        self.Font = self._underline_font
        self.ForeColor = WinUIColors.AccentDark1
    
    def _on_leave(self, sender, e):
        """Handler for mouse leave event."""
        self.Font = self._original_font
        self.ForeColor = WinUIColors.Accent

# =============================================================================
# Exports
# =============================================================================

__all__ = [
    # Colors and Fonts
    'WinUIColors',
    'WinUIFonts',
    
    # Controls
    'WinUIButton',
    'WinUILabel',
    'WinUITextBox',
    'WinUIProgressBar',
    'WinUIToggleSwitch',
    'WinUIExpander',
    'WinUICheckBox',
    'WinUIRadioButton',
    'WinUIComboBox',
    'WinUIPanel',
    'WinUISlider',
    'WinUIHyperlinkButton'
]
