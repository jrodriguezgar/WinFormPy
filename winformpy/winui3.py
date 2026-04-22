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
# Version: 1.0.4
# Description:
# WinUI 3 styled controls for WinFormPy
# =============================================================

import sys
import os

# Import WinFormPy base controls
try:
    # Try relative import first (when part of a package)
    from .winformpy import (
        Native,
        Button as BaseButton, Label as BaseLabel, TextBox as BaseTextBox,
        Panel as BasePanel, CheckBox as BaseCheckBox, RadioButton as BaseRadioButton,
        ComboBox as BaseComboBox, ProgressBar as BaseProgressBar,
        ProgressBarStyle, DockStyle, FlatStyle,
        ContentAlignment, AnchorStyles
    )
except (ImportError, ValueError):
    try:
        # Try absolute import from the module file
        from winformpy import (
            Native,
            Button as BaseButton, Label as BaseLabel, TextBox as BaseTextBox,
            Panel as BasePanel, CheckBox as BaseCheckBox, RadioButton as BaseRadioButton,
            ComboBox as BaseComboBox, ProgressBar as BaseProgressBar,
            ProgressBarStyle, DockStyle, FlatStyle,
            ContentAlignment, AnchorStyles
        )
    except ImportError:
        # Fallback for direct execution or unusual path setups
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.append(current_dir)
        from winformpy import (
            Native,
            Button as BaseButton, Label as BaseLabel, TextBox as BaseTextBox,
            Panel as BasePanel, CheckBox as BaseCheckBox, RadioButton as BaseRadioButton,
            ComboBox as BaseComboBox, ProgressBar as BaseProgressBar,
            DockStyle, FlatStyle,
            AnchorStyles
        )


# Import WinUI 3 Theme
try:
    from .themes.winui3_theme import winui_colors as Colors, winui_fonts as Fonts
except (ImportError, ValueError):
    try:
        from themes.winui3_theme import winui_colors as Colors, winui_fonts as Fonts
    except ImportError:
        # Fallback if themes folder not found
        class Colors:
            Accent = "#0078D4"
            AccentText = "#FFFFFF"
            TextPrimary = "#000000"
            TextSecondary = "#666666"
            WindowBg = "#FFFFFF"
            ControlBg = "#FFFFFF"
            ControlBorder = "#E5E5E5"
            SuccessText = "#107C10"
            WarningText = "#9D5D00"
            ErrorText = "#C42B1C"
        class Fonts:
            Title = ("Segoe UI", 28, "bold")
            Subtitle = ("Segoe UI", 16, "bold")
            Body = ("Segoe UI", 14, "normal")
            Caption = ("Segoe UI", 12, "normal")

# Aliases for backward compatibility
WinUIColors = Colors
WinUIFonts = Fonts


# =============================================================================
# WinUI 3 Button
# =============================================================================

class Button(BaseButton):
    """
    WinUI 3 styled Button with accent color and hover effects.

    Features:
    - Multiple button styles: Accent (default), Success, Warning, Danger, Standard
    - Flat style with no borders
    - Customizable via ButtonStyle parameter or AccentColor property
    - Inherits all Button functionality

    Example:
        # Accent button (default)
        btn = Button(form, {
            'Text': 'Click Me',
            'Width': 120,
            'Height': 32
        })

        # Success button
        btn_success = Button(form, {
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
# WinUI 3 TextBlock
# =============================================================================

class TextBlock(BaseLabel):
    """
    WinUI 3 styled TextBlock (Label) with typography support.

    Features:
    - Segoe UI font by default
    - Typography presets (Title, Subtitle, Body, Caption)
    - TextPrimary color by default

    Example:
        lbl = TextBlock(form, {
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
# WinUI 3 InfoBadge
# =============================================================================

class InfoBadge(BaseLabel):
    """
    WinUI 3 styled InfoBadge for notifications and status indicators.

    Features:
    - Small circular badge (dot) or numeric badge
    - Different severities: Attention (default), Success, Caution, Critical, Informational
    - Corner rounding using WinFormPy borders

    Example:
        badge = InfoBadge(form, {
            'Text': '5',
            'Severity': 'Attention'
        })
    """

    def __init__(self, master_form, props=None):
        if props is None: props = {}

        severity = props.pop('Severity', 'Attention')
        colors = {
            'Attention': ("#C42B1C", "#FFFFFF"), # Red
            'Success': ("#107C10", "#FFFFFF"),   # Green
            'Caution': ("#9D5D00", "#FFFFFF"),   # Yellow/Orange
            'Critical': ("#C42B1C", "#FFFFFF"),  # Red
            'Informational': ("#0078D4", "#FFFFFF") # Blue
        }
        bg, fg = colors.get(severity, colors['Attention'])

        defaults = {
            'BackColor': bg,
            'ForeColor': fg,
            'Font': ("Segoe UI", 9, "bold"),
            'TextAlign': 'MiddleCenter',
            'Width': 18,
            'Height': 18
        }

        for key, value in defaults.items():
            if key not in props: props[key] = value

        super().__init__(master_form, props)

        # WinUI 3 badges are circular
        # Note: Tkinter labels don't support border-radius natively,
        # but we can simulate it if the background is small enough.
        # For now, we use standard label styling.

    @property
    def Severity(self):
        """Gets the severity level."""
        return getattr(self, '_severity', 'Attention')

    @Severity.setter
    def Severity(self, value):
        """Sets the severity level and updates colors."""
        colors = {
            'Attention': ("#C42B1C", "#FFFFFF"),
            'Success': ("#107C10", "#FFFFFF"),
            'Caution': ("#9D5D00", "#FFFFFF"),
            'Critical': ("#C42B1C", "#FFFFFF"),
            'Informational': ("#0078D4", "#FFFFFF")
        }
        bg, fg = colors.get(value, colors['Attention'])
        self.BackColor = bg
        self.ForeColor = fg
        self._severity = value


# =============================================================================
# WinUI 3 TextBox
# =============================================================================

class TextBox(BaseTextBox):
    """
    WinUI 3 styled TextBox with accent underline.

    Features:
    - Thin underline at the bottom that changes color on focus
    - Gray when idle, accent color when focused
    - No visible borders - clean modern look
    - Inherits all standard TextBox functionality
    - Customizable underline color via UnderlineColor property

    Example:
        txt = TextBox(form, {
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

class ProgressBar(BaseProgressBar):
    """
    WinUI 3 styled ProgressBar with accent colors.

    Features:
    - Blue accent bar color (default: #0078D4)
    - Light gray trough/background (#E5E5E5)
    - Customizable via BarColor and TroughColor properties

    Example:
        pb = ProgressBar(form, {
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
        self._style = Native.Style()

        # Use 'clam' theme as base for better color support
        try:
            self._style.theme_use('clam')
        except Exception:
            pass

        # Apply WinUI colors
        self._apply_winui_colors()

        # Update widget to use new style
        w = self.GetTkWidget()
        if w:
            w.configure(style=self._style_name)

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
# WinUI 3 ProgressRing
# =============================================================================

class ProgressRing(BasePanel):
    """
    WinUI 3 styled circular progress indicator.

    Features:
    - Animated rotation for indeterminate state
    - Accent color for the active ring
    - Configurable size and thickness

    Example:
        ring = ProgressRing(form, {
            'Width': 40,
            'Height': 40,
            'IsActive': True
        })
    """

    def __init__(self, master_form, props=None):
        if props is None: props = {}

        self._is_active = props.pop('IsActive', True)
        self._bar_color = props.pop('BarColor', WinUIColors.Accent)
        self._trough_color = props.pop('TroughColor', WinUIColors.Border)
        self._thickness = props.pop('Thickness', 3)
        self._angle = 0

        defaults = {
            'Width': 32,
            'Height': 32,
            'BackColor': WinUIColors.WindowBg
        }

        for key, value in defaults.items():
            if key not in props: props[key] = value

        super().__init__(master_form, props)

        self.canvas = Native.Canvas(
            self._tk_widget,
            width=self.Width,
            height=self.Height,
            bg=self.BackColor,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        if self._is_active:
            self._animate()

    def _draw_ring(self):
        self.canvas.delete("all")
        margin = self._thickness + 2

        # Background ring (trough)
        self.canvas.create_oval(
            margin, margin, self.Width - margin, self.Height - margin,
            outline=self._trough_color, width=self._thickness
        )

        # Active segment (arc)
        self.canvas.create_arc(
            margin, margin, self.Width - margin, self.Height - margin,
            outline=self._bar_color, width=self._thickness,
            start=self._angle, extent=90, style="arc"
        )

    def _animate(self):
        if not self._is_active: return

        self._angle = (self._angle - 10) % 360
        self._draw_ring()

        # WinUI 3 animation speed
        if hasattr(self, '_tk_widget'):
            self.InvokeDelayed(30, self._animate)

    @property
    def IsActive(self):
        """Gets whether the ring is animating."""
        return self._is_active

    @IsActive.setter
    def IsActive(self, value):
        """Sets whether the ring is animating."""
        if self._is_active != value:
            self._is_active = value
            if value:
                self._animate()
            else:
                self.canvas.delete("all")
                self._draw_ring()


# =============================================================================
# WinUI 3 ToggleSwitch
# =============================================================================

class ToggleSwitch(BasePanel):
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
        switch = ToggleSwitch(
            parent=form,
            text="Enable Feature",
            on_toggle=lambda state: None
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
        self.label = BaseLabel(self)
        self.label.Text = text
        self.label.AutoSize = True
        self.label.Location = (50, 4)
        self.label.Font = WinUIFonts.Body
        self.label.BackColor = self._bg_color
        self.label.ForeColor = WinUIColors.TextPrimary

        # Switch graphic using Canvas for custom drawing
        self.canvas = Native.Canvas(
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
        if hasattr(parent, 'GetTkWidget') and parent.GetTkWidget():
            try:
                return parent.GetTkWidget().cget('bg')
            except Exception:
                pass
        return WinUIColors.CardBg

    def _apply_background(self):
        """Apply background color to all internal widgets."""
        # Apply to main widget via GetTkWidget (avoid recursion with BackColor setter)
        w = self.GetTkWidget() if hasattr(self, 'GetTkWidget') else None
        if w:
            try:
                w.configure(bg=self._bg_color)
            except Exception:
                pass
        if hasattr(self, '_container') and self._container:
            try:
                self._container.configure(bg=self._bg_color)
            except Exception:
                pass
        # Note: Direct tkinter access - canvas.configure() used as WinFormPy Canvas doesn't exist yet
        if hasattr(self, 'canvas') and self.canvas:
            try:
                self.canvas.configure(bg=self._bg_color)
            except Exception:
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

class Expander(BasePanel):
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
        expander = Expander(
            parent=form,
            title="Advanced Settings",
            height_expanded=200
        )

        # Add controls to expander.content
        lbl = BaseLabel(expander.content)
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
        self.header = BaseButton(self)
        self.header.Text = "  ▶  " + title  # Right arrow when collapsed
        self.header.Dock = DockStyle.Top
        self.header.Height = 40
        self.header.FlatStyle = FlatStyle.Flat
        self.header.TextAlign = 'w'
        self.header.BackColor = self._bg_color
        self.header.ForeColor = WinUIColors.Accent  # Blue accent color
        self.header.Font = WinUIFonts.Body
        w = self.header.GetTkWidget() if hasattr(self.header, 'GetTkWidget') else None
        if w:
            w.configure(borderwidth=0, highlightthickness=0)

        self.header.Click = self.toggle

        # Content panel (where child controls are added)
        self.content = BasePanel(self)
        self.content.Dock = DockStyle.Fill
        self.content.Visible = False  # Hidden by default

        # Accent border at bottom
        self._border = BasePanel(self)
        self._border.Height = 2
        self._border.Dock = DockStyle.Bottom
        self._border.BackColor = WinUIColors.Accent

        # Apply background to all
        self._apply_background()

    def _get_parent_bg_color(self, parent):
        """Get background color from parent control."""
        if hasattr(parent, 'BackColor') and parent.BackColor:
            return parent.BackColor
        if hasattr(parent, 'GetTkWidget') and parent.GetTkWidget():
            try:
                return parent.GetTkWidget().cget('bg')
            except Exception:
                pass
        return WinUIColors.CardBg

    def _apply_background(self):
        """Apply background color to all internal widgets."""
        # Apply to main widget via GetTkWidget (avoid recursion with BackColor setter)
        w = self.GetTkWidget() if hasattr(self, 'GetTkWidget') else None
        if w:
            try:
                w.configure(bg=self._bg_color)
            except Exception:
                pass
        if hasattr(self, '_container') and self._container:
            try:
                self._container.configure(bg=self._bg_color)
            except Exception:
                pass
        if hasattr(self, 'header') and self.header:
            self.header.BackColor = self._bg_color
        if hasattr(self, 'content') and self.content:
            self.content.BackColor = self._bg_color

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

class CheckBox(BaseCheckBox):
    """
    WinUI 3 styled CheckBox with accent color.

    Features:
    - Blue accent color when checked
    - Segoe UI font
    - Inherits all CheckBox functionality

    Example:
        chk = CheckBox(form, {
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

        # Apply Hover effects if desired
        w = self.GetTkWidget()
        if w:
            try:
                w.configure(
                    activebackground=WinUIColors.ControlBgHover,
                    activeforeground=WinUIColors.TextPrimary
                )
            except Exception:
                pass


# =============================================================================
# WinUI 3 RadioButton
# =============================================================================

class RadioButton(BaseRadioButton):
    """
    WinUI 3 styled RadioButton with accent color.

    Features:
    - Blue accent color when selected
    - Segoe UI font
    - Inherits all RadioButton functionality

    Example:
        rb = RadioButton(form, {
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

        # Apply hover effects
        w = self.GetTkWidget()
        if w:
            try:
                w.configure(
                    activebackground=WinUIColors.ControlBgHover,
                    activeforeground=WinUIColors.TextPrimary
                )
            except Exception:
                pass


# =============================================================================
# WinUI 3 InfoBar
# =============================================================================

class InfoBar(BasePanel):
    """
    WinUI 3 styled InfoBar for inline notifications.

    Features:
    - Built-in severity icons and colors
    - Title and Message support
    - Close button to dismiss
    - Accent bar on the left

    Example:
        infobar = InfoBar(form, {
            'Title': 'Update Available',
            'Message': 'A new version of WinFormPy is ready to install.',
            'Severity': 'Informational',
            'Dock': DockStyle.Top
        })
    """

    def __init__(self, master_form, props=None):
        if props is None: props = {}

        severity = props.pop('Severity', 'Informational')
        self._title_text = props.pop('Title', '')
        self._message_text = props.pop('Message', '')

        # Setup colors based on severity
        # Format: (SideBarColor, BackgroundColor, TitleColor, Icon)
        severity_map = {
            'Informational': (WinUIColors.InfoText, WinUIColors.InfoBg, WinUIColors.InfoText, "ℹ"),
            'Success': (WinUIColors.SuccessText, WinUIColors.SuccessBg, WinUIColors.SuccessText, "✔"),
            'Warning': (WinUIColors.WarningText, WinUIColors.WarningBg, WinUIColors.WarningText, "⚠"),
            'Error': (WinUIColors.ErrorText, WinUIColors.ErrorBg, WinUIColors.ErrorText, "ⓧ")
        }

        sidebar_color, bg_color, title_color, icon = severity_map.get(severity, severity_map['Informational'])

        defaults = {
            'BackColor': bg_color,
            'Height': 60,
            'Padding': 10
        }

        for key, value in defaults.items():
            if key not in props: props[key] = value

        super().__init__(master_form, props)

        # 1. Left Accent Bar
        self._sidebar = BasePanel(self)
        self._sidebar.Width = 4
        self._sidebar.Dock = DockStyle.Left
        self._sidebar.BackColor = sidebar_color

        # 2. Icon Label
        self._icon_label = BaseLabel(self)
        self._icon_label.Text = icon
        self._icon_label.ForeColor = sidebar_color
        self._icon_label.BackColor = bg_color
        self._icon_label.Font = ("Segoe UI", 14, "bold")
        self._icon_label.Location = (15, 18)
        self._icon_label.Width = 30

        # 3. Content Area
        self._title_label = BaseLabel(self)
        self._title_label.Text = self._title_text
        self._title_label.Font = WinUIFonts.BodyStrong
        self._title_label.ForeColor = WinUIColors.TextPrimary
        self._title_label.BackColor = bg_color
        self._title_label.Location = (50, 10)
        self._title_label.AutoSize = True

        self._message_label = BaseLabel(self)
        self._message_label.Text = self._message_text
        self._message_label.Font = WinUIFonts.Caption
        self._message_label.ForeColor = WinUIColors.TextSecondary
        self._message_label.BackColor = bg_color
        self._message_label.Location = (50, 30)
        self._message_label.AutoSize = True

        # 4. Close Button
        self._close_btn = BaseButton(self)
        self._close_btn.Text = "✕"
        self._close_btn.FontSize = 10
        self._close_btn.FlatStyle = FlatStyle.Flat
        self._close_btn.BackColor = bg_color
        self._close_btn.ForeColor = WinUIColors.TextSecondary
        self._close_btn.Width = 30
        self._close_btn.Height = 30
        self._close_btn.Anchor = AnchorStyles.Top | AnchorStyles.Right
        self._close_btn.Location = (self.Width - 40, 5)
        self._close_btn.Click = lambda s, e: setattr(self, 'Visible', False)

        self._severity = severity

    @property
    def Title(self):
        """Gets the InfoBar title."""
        return self._title_text

    @Title.setter
    def Title(self, value):
        """Sets the InfoBar title."""
        self._title_text = value
        self._title_label.Text = value

    @property
    def Message(self):
        """Gets the InfoBar message."""
        return self._message_text

    @Message.setter
    def Message(self, value):
        """Sets the InfoBar message."""
        self._message_text = value
        self._message_label.Text = value


# =============================================================================
# WinUI 3 ComboBox
# =============================================================================

class ComboBox(BaseComboBox):
    """
    WinUI 3 styled ComboBox.

    Features:
    - Clean border styling
    - Segoe UI font
    - Inherits all ComboBox functionality

    Example:
        cmb = ComboBox(form, {
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

class Panel(BasePanel):
    """
    WinUI 3 styled Panel with card background.

    Features:
    - White card background
    - Optional border
    - Inherits all Panel functionality

    Example:
        card = Panel(form, {
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

class Slider(BasePanel):
    """Control deslizante con estética de Windows 11."""
    def __init__(self, parent, props=None):
        if props is None: props = {}
        # Ensure height is standard for WinUI 3 Slider
        props['Height'] = props.get('Height', 32)
        props['Width'] = props.get('Width', 200)

        super().__init__(parent, props)

        self._value = 0.5 # 0.0 a 1.0

        self.canvas = Native.Canvas(self._tk_widget, height=self.Height, width=self.Width,
                               bg=Colors.WindowBg if hasattr(Colors, 'WindowBg') else "#FFFFFF",
                               highlightthickness=0)
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

class HyperlinkButton(BaseButton):
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
# WinUI 3 NumberBox
# =============================================================================

class NumberBox(BasePanel):
    """
    WinUI 3 styled NumberBox for numeric input.

    Features:
    - Numeric input text box
    - Increment/Decrement spinner buttons
    - Minimum/Maximum value constraints
    - Custom steps

    Example:
        nb = NumberBox(form, {
            'Value': 10,
            'Step': 1,
            'Minimum': 0,
            'Maximum': 100
        })
    """

    def __init__(self, master_form, props=None):
        if props is None: props = {}

        self._value = props.pop('Value', 0.0)
        self._step = props.pop('Step', 1.0)
        self._min = props.pop('Minimum', float('-inf'))
        self._max = props.pop('Maximum', float('inf'))

        defaults = {
            'Width': 120,
            'Height': 32,
            'BackColor': WinUIColors.ControlBg
        }

        for key, value in defaults.items():
            if key not in props: props[key] = value

        super().__init__(master_form, props)

        # 1. Input Entry
        self.entry = TextBox(self)
        self.entry.Text = str(self._value)
        self.entry.Dock = DockStyle.Fill
        self.entry.TextChanged = self._on_text_changed

        # 2. Buttons Panel
        self._btns_pnl = BasePanel(self)
        self._btns_pnl.Width = 30
        self._btns_pnl.Dock = DockStyle.Right
        self._btns_pnl.BackColor = self.BackColor

        # 3. Plus Button
        self.btn_up = BaseButton(self._btns_pnl)
        self.btn_up.Text = "▴"
        self.btn_up.Height = 16
        self.btn_up.Dock = DockStyle.Top
        self.btn_up.FlatStyle = FlatStyle.Flat
        self.btn_up.FontSize = 8
        self.btn_up.Click = lambda s, e: self.Increment()

        # 4. Minus Button
        self.btn_down = BaseButton(self._btns_pnl)
        self.btn_down.Text = "▾"
        self.btn_down.Height = 16
        self.btn_down.Dock = DockStyle.Bottom
        self.btn_down.FlatStyle = FlatStyle.Flat
        self.btn_down.FontSize = 8
        self.btn_down.Click = lambda s, e: self.Decrement()

    def _on_text_changed(self, sender, e):
        """Update value when user types."""
        try:
            val = self.entry.Text
            if val:
                self._value = float(val)
        except ValueError:
            pass

    def Increment(self):
        """Increments the current value by Step."""
        new_val = self._value + self._step
        if new_val <= self._max:
            self.Value = new_val

    def Decrement(self):
        """Decrements the current value by Step."""
        new_val = self._value - self._step
        if new_val >= self._min:
            self.Value = new_val

    @property
    def Value(self):
        """Gets the numeric value."""
        return self._value

    @Value.setter
    def Value(self, val):
        """Sets the numeric value and updates UI."""
        self._value = val
        self.entry.Text = str(val)


# =============================================================================
# WinUI 3 StackPanel
# =============================================================================

class StackPanel(BasePanel):
    """
    WinUI 3 styled layout panel that stacks children vertically or horizontally.

    Features:
    - Spacing between items
    - Orientation (Vertical by default)

    Example:
        stack = StackPanel(form, {
            'Spacing': 10,
            'Orientation': 'Vertical'
        })
    """

    def __init__(self, master_form, props=None):
        if props is None: props = {}

        self.Spacing = props.pop('Spacing', 4)
        self.Orientation = props.pop('Orientation', 'Vertical')

        super().__init__(master_form, props)
        self._children_count = 0

    def AddControl(self, control):
        """Override to apply automatic positioning based on orientation and spacing."""
        super().AddControl(control)

        if self._children_count > 0:
            # Apply spacing
            if self.Orientation == 'Vertical':
                last_y = 0
                for c in self.Controls:
                    if c != control:
                         last_y = max(last_y, c.Top + c.Height)
                control.Top = last_y + self.Spacing
            else:
                last_x = 0
                for c in self.Controls:
                    if c != control:
                         last_x = max(last_x, c.Left + c.Width)
                control.Left = last_x + self.Spacing

        self._children_count += 1


# =============================================================================
# WinUI 3 PersonPicture
# =============================================================================

class PersonPicture(BasePanel):
    """
    WinUI 3 styled circular avatar with image or initials.

    Features:
    - Circular clipping for images
    - Fallback to initials if no image
    - Accent background for initials

    Example:
        avatar = PersonPicture(form, {
            'Width': 40,
            'Height': 40,
            'Initials': 'JD'
        })
    """

    def __init__(self, master_form, props=None):
        if props is None: props = {}

        self._initials = props.pop('Initials', '??')
        self._image_path = props.pop('ImageSource', None)

        defaults = {
            'Width': 48,
            'Height': 48,
            'BackColor': WinUIColors.Accent
        }

        for key, value in defaults.items():
            if key not in props: props[key] = value

        super().__init__(master_form, props)

        # Label for initials
        self._lbl = BaseLabel(self)
        self._lbl.Text = self._initials
        self._lbl.ForeColor = WinUIColors.AccentText
        self._lbl.BackColor = self.BackColor
        self._lbl.Font = ("Segoe UI", int(self.Height * 0.35), "bold")
        self._lbl.Dock = DockStyle.Fill
        self._lbl.TextAlign = 'MiddleCenter'


# =============================================================================
# WinUI 3 RatingControl
# =============================================================================

class RatingControl(BasePanel):
    """
    WinUI 3 styled star rating control.

    Features:
    - 5-star rating by default
    - Hover effects
    - Accent color for selected stars

    Example:
        rating = RatingControl(form, {
            'Value': 3.5
        })
    """

    def __init__(self, master_form, props=None):
        if props is None: props = {}

        self._value = props.pop('Value', 0.0)
        self._max = props.pop('Max', 5)
        self._stars = []

        defaults = {
            'Width': self._max * 24 + 10,
            'Height': 30,
            'BackColor': WinUIColors.WindowBg
        }

        for key, value in defaults.items():
            if key not in props: props[key] = value

        super().__init__(master_form, props)

        for i in range(self._max):
            star = BaseLabel(self)
            star.Text = "★" if i < int(self._value) else "☆"
            star.Font = ("Segoe UI", 16)
            star.ForeColor = WinUIColors.Accent if i < int(self._value) else WinUIColors.TextTertiary
            star.BackColor = self.BackColor
            star.Location = (i * 24, 0)
            star.Width = 24
            star.Click = lambda s, e, idx=i+1: self._on_star_click(idx)
            self._stars.append(star)

    def _on_star_click(self, val):
        self.Value = val

    @property
    def Value(self):
        """Gets the rating value."""
        return self._value

    @Value.setter
    def Value(self, val):
        """Sets the rating value and updates stars."""
        self._value = val
        for i, star in enumerate(self._stars):
            star.Text = "★" if i < int(val) else "☆"
            star.ForeColor = WinUIColors.Accent if i < int(val) else WinUIColors.TextTertiary


# =============================================================================
# WinUI 3 Card
# =============================================================================

class Card(Panel):
    """
    WinUI 3 specialized card container with borders and padding.

    Features:
    - Default padding for content
    - Subtle border (CardBorder)
    - Inherits from Panel

    Example:
        card = Card(form, {
            'Width': 250,
            'Height': 150
        })
    """

    def __init__(self, master_form, props=None):
        if props is None: props = {}

        defaults = {
            'Padding': 16,
            'BackColor': WinUIColors.CardBg
        }

        for key, value in defaults.items():
            if key not in props: props[key] = value

        super().__init__(master_form, props)

        # Note: Tkinter frames don't support border-radius natively.
        # We use highlightthickness to simulate a subtle border.
        w = self.GetTkWidget()
        if w:
            try:
                w.configure(
                    highlightbackground=WinUIColors.CardBorder,
                    highlightthickness=1
                )
            except Exception:
                pass


# =============================================================================
# WinUI 3 TabView
# =============================================================================

class TabView(BasePanel):
    """
    WinUI 3 styled TabView control.

    Features:
    - Modern tab appearance
    - Accent bar for selected tab
    - Simple page switching

    Example:
        tabs = TabView(form, {
            'Dock': DockStyle.Fill
        })
        tabs.AddTab("Home", home_page_panel)
        tabs.AddTab("Settings", settings_panel)
    """

    def __init__(self, master_form, props=None):
        if props is None: props = {}

        defaults = {
            'BackColor': WinUIColors.WindowBg
        }

        for key, value in defaults.items():
            if key not in props: props[key] = value

        super().__init__(master_form, props)

        # 1. Tab Headers Bar
        self._headers_pnl = BasePanel(self)
        self._headers_pnl.Height = 40
        self._headers_pnl.Dock = DockStyle.Top
        self._headers_pnl.BackColor = WinUIColors.LayerBg

        # 2. Pages Container
        self._pages_container = BasePanel(self)
        self._pages_container.Dock = DockStyle.Fill
        self._pages_container.BackColor = self.BackColor

        self._tabs = []
        self._selected_index = -1

    def AddTab(self, title, content_panel):
        """Adds a new tab with the given title and content panel."""
        tab_idx = len(self._tabs)

        # Create tab button
        btn = BaseButton(self._headers_pnl)
        btn.Text = title
        btn.Width = 120
        btn.FlatStyle = FlatStyle.Flat
        btn.BackColor = self._headers_pnl.BackColor
        btn.ForeColor = WinUIColors.TextSecondary
        btn.Font = WinUIFonts.Body
        btn.Location = (tab_idx * 122, 0)
        btn.Height = 38

        # Accent bar for this tab
        accent_bar = BasePanel(btn)
        accent_bar.Height = 2
        accent_bar.Dock = DockStyle.Bottom
        accent_bar.BackColor = WinUIColors.Accent
        accent_bar.Visible = False

        btn.Click = lambda s, e, idx=tab_idx: self.SelectTab(idx)

        # Ensure content_panel is managed by us
        content_panel.Parent = self._pages_container
        content_panel.Dock = DockStyle.Fill
        content_panel.Visible = False

        self._tabs.append({
            'button': btn,
            'panel': content_panel,
            'accent': accent_bar
        })

        if self._selected_index == -1:
            self.SelectTab(0)

    def SelectTab(self, index):
        """Selects the tab at the specified index."""
        if not (0 <= index < len(self._tabs)): return

        # Hide current
        if self._selected_index >= 0:
            current = self._tabs[self._selected_index]
            current['panel'].Visible = False
            current['accent'].Visible = False
            current['button'].ForeColor = WinUIColors.TextSecondary
            current['button'].Font = WinUIFonts.Body

        # Show new
        self._selected_index = index
        selected = self._tabs[index]
        selected['panel'].Visible = True
        selected['accent'].Visible = True
        selected['button'].ForeColor = WinUIColors.Accent
        selected['button'].Font = WinUIFonts.BodyStrong


# =============================================================================
# WinUI 3 BreadcrumbBar
# =============================================================================

class BreadcrumbBar(StackPanel):
    """
    WinUI 3 styled BreadcrumbBar navigation.

    Features:
    - Path navigation with separators
    - Clickable segments

    Example:
        bc = BreadcrumbBar(form, {
            'Items': ['Home', 'Documents', 'Finance']
        })
    """

    def __init__(self, master_form, props=None):
        if props is None: props = {}

        items = props.pop('Items', [])
        props['Orientation'] = 'Horizontal'
        props['Spacing'] = 8
        props['Height'] = 30

        super().__init__(master_form, props)

        for i, item in enumerate(items):
            # Breadcrumb segment
            btn = HyperlinkButton(self)
            btn.Text = item
            btn.AutoSize = True
            self.AddControl(btn)

            # Separator (except for last)
            if i < len(items) - 1:
                sep = BaseLabel(self)
                sep.Text = ">"
                sep.ForeColor = WinUIColors.TextTertiary
                sep.AutoSize = True
                self.AddControl(sep)


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    # Colors and Fonts
    'WinUIColors',
    'WinUIFonts',

    # Controls
    'Button',
    'TextBlock',
    'TextBox',
    'ProgressBar',
    'ProgressRing',
    'InfoBar',
    'InfoBadge',
    'NumberBox',
    'ToggleSwitch',
    'Expander',
    'CheckBox',
    'RadioButton',
    'ComboBox',
    'Panel',
    'Slider',
    'HyperlinkButton',
    'StackPanel',
    'PersonPicture',
    'RatingControl',
    'Card',
    'TabView',
    'BreadcrumbBar'
]
