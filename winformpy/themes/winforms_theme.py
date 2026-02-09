"""
WinForms Theme Configuration for WinFormPy.

Classic Windows system gray with strong 3D borders.
"""

# =============================================================================
# SYSTEM COLORS (Classic Windows)
# =============================================================================

SYSTEM_COLORS = {
    # Backgrounds
    "control": "#F0F0F0",           # SystemColors.Control
    "control_light": "#E3E3E3",     # SystemColors.ControlLight
    "control_light_light": "#FFFFFF", # SystemColors.ControlLightLight
    "control_dark": "#A0A0A0",      # SystemColors.ControlDark
    "control_dark_dark": "#696969", # SystemColors.ControlDarkDark
    "window": "#FFFFFF",            # SystemColors.Window
    
    # Text
    "control_text": "#000000",      # SystemColors.ControlText
    "window_text": "#000000",       # SystemColors.WindowText
    "gray_text": "#6D6D6D",         # SystemColors.GrayText (disabled)
    "highlight_text": "#FFFFFF",    # SystemColors.HighlightText
    
    # Selection / Highlight
    "highlight": "#0078D7",         # SystemColors.Highlight
    "highlight_text": "#FFFFFF",    # SystemColors.HighlightText
    "inactive_caption": "#BFCDDB",  # SystemColors.InactiveCaption
    "active_caption": "#99B4D1",    # SystemColors.ActiveCaption
    "active_caption_text": "#000000", # SystemColors.ActiveCaptionText
    
    # Menu
    "menu": "#F0F0F0",              # SystemColors.Menu
    "menu_text": "#000000",         # SystemColors.MenuText
    "menu_bar": "#F0F0F0",          # SystemColors.MenuBar (Flat menu bar background)
    
    # 3D Borders
    "button_face": "#F0F0F0",       # SystemColors.ButtonFace
    "button_text": "#000000",       # SystemColors.ButtonText
    "button_highlight": "#FFFFFF",  # SystemColors.ButtonHighlight (light border)
    "button_shadow": "#A0A0A0",     # SystemColors.ButtonShadow (dark border)
    
    # Tooltips
    "info": "#FFFFE1",              # SystemColors.Info
    "info_text": "#000000",         # SystemColors.InfoText

    # Others
    "app_workspace": "#ABABAB",     # SystemColors.AppWorkspace
    "active_border": "#B4B4B4",     # SystemColors.ActiveBorder
    "inactive_border": "#F4F7FC",   # SystemColors.InactiveBorder
    "desktop": "#000000",           # SystemColors.Desktop
}

# =============================================================================
# 3D BORDERS (Classic WinForms Style)
# =============================================================================

BORDERS_3D = {
    # Fixed3D: sunken effect (for TextBox, ListBox)
    "fixed3d": {
        "top": SYSTEM_COLORS["button_shadow"],
        "left": SYSTEM_COLORS["button_shadow"],
        "bottom": SYSTEM_COLORS["button_highlight"],
        "right": SYSTEM_COLORS["button_highlight"],
        "inner_top": SYSTEM_COLORS["control_dark_dark"],
        "inner_left": SYSTEM_COLORS["control_dark_dark"],
        "inner_bottom": SYSTEM_COLORS["control_light_light"],
        "inner_right": SYSTEM_COLORS["control_light_light"],
    },
    # Raised3D: elevated effect (for Button)
    "raised": {
        "top": SYSTEM_COLORS["button_highlight"],
        "left": SYSTEM_COLORS["button_highlight"],
        "bottom": SYSTEM_COLORS["button_shadow"],
        "right": SYSTEM_COLORS["button_shadow"],
        "inner_top": SYSTEM_COLORS["control_light_light"],
        "inner_left": SYSTEM_COLORS["control_light_light"],
        "inner_bottom": SYSTEM_COLORS["control_dark"],
        "inner_right": SYSTEM_COLORS["control_dark"],
    },
    # FixedSingle: simple border
    "fixed_single": {
        "color": SYSTEM_COLORS["control_dark"],
        "width": 1,
    },
}

# =============================================================================
# TYPOGRAPHY
# =============================================================================

TYPOGRAPHY = {
    "font_family": "Segoe UI",
    "font_family_fallback": "Microsoft Sans Serif, Tahoma, Arial",
    "sizes": {
        "default": 9,       # Standard size in points (pt)
        "small": 8,
        "large": 12,
        "title": 14,
    },
    "weight": "regular",       # WinForms uses regular by default
}

# =============================================================================
# COMPONENT COLORS
# =============================================================================

COMPONENT_COLORS = {
    "label": {
        "background": "transparent",
        "foreground": SYSTEM_COLORS["control_text"],
    },
    "button": {
        "background": SYSTEM_COLORS["control"],
        "foreground": SYSTEM_COLORS["control_text"],
        "border": SYSTEM_COLORS["control_dark"],
    },
    "textbox": {
        "background": SYSTEM_COLORS["window"],
        "foreground": SYSTEM_COLORS["window_text"],
        "border": SYSTEM_COLORS["button_shadow"],
        "disabled_background": SYSTEM_COLORS["control"],
        "disabled_foreground": SYSTEM_COLORS["gray_text"],
    },
    "checkbox": {
        "background": SYSTEM_COLORS["window"],
        "foreground": SYSTEM_COLORS["control_text"],
        "check_color": SYSTEM_COLORS["control_text"],
    },
    "panel": {
        "background": SYSTEM_COLORS["control"],
        "border": SYSTEM_COLORS["control_dark"],
    },
    "form": {
        "background": SYSTEM_COLORS["control"],
        "foreground": SYSTEM_COLORS["control_text"],
    },
}

# =============================================================================
# STATES
# =============================================================================

STATES = {
    "normal": {
        "background": SYSTEM_COLORS["control"],
        "foreground": SYSTEM_COLORS["control_text"],
    },
    "hover": {
        "background": SYSTEM_COLORS["control_light"],
        "border": SYSTEM_COLORS["highlight"],
    },
    "pressed": {
        "background": SYSTEM_COLORS["control_dark"],
    },
    "disabled": {
        "foreground": SYSTEM_COLORS["gray_text"],
        "background": SYSTEM_COLORS["control"],
    },
    "focused": {
        "border": SYSTEM_COLORS["highlight"],
    },
}

class Colors:
    """Helper class to access colors as attributes for WinFormPy."""
    def __init__(self):
        for k, v in SYSTEM_COLORS.items():
            # Convert snake_case to PascalCase
            name = "".join(x.capitalize() for x in k.split("_"))
            setattr(self, name, v)

class Fonts:
    """WinForms Typography."""
    _family = TYPOGRAPHY["font_family"]
    
    DefaultFont = (_family, TYPOGRAPHY["sizes"]["default"], "normal")
    DialogFont = (_family, TYPOGRAPHY["sizes"]["default"], "normal")
    MenuFont = (_family, TYPOGRAPHY["sizes"]["default"], "normal")
    StatusFont = (_family, TYPOGRAPHY["sizes"]["default"], "normal")
    CaptionFont = (_family, TYPOGRAPHY["sizes"]["default"], "bold")
    SmallCaptionFont = (_family, TYPOGRAPHY["sizes"]["small"], "normal")
    Small = (_family, TYPOGRAPHY["sizes"]["small"], "normal")
    Large = (_family, TYPOGRAPHY["sizes"]["large"], "normal")
    Title = (_family, TYPOGRAPHY["sizes"]["title"], "bold")

# Instances for easy access
winforms_colors = Colors()
winforms_fonts = Fonts()
