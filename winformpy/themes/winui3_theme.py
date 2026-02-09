"""
WinUI 3 / Fluent Design Theme Configuration for WinFormPy.

Accent colors and smooth shadows following Fluent Design System guidelines.
"""

# =============================================================================
# LIGHT THEME
# =============================================================================

LIGHT = {
    # Backgrounds
    "background": "#F3F3F3",
    "background_solid": "#FFFFFF",
    "layer": "#FFFFFF",
    "layer_alt": "#F9F9F9",
    "card": "#FFFFFF",
    
    # Text
    "text_primary": "#000000",
    "text_secondary": "#5D5D5D",
    "text_tertiary": "#8A8A8A",
    "text_disabled": "#A0A0A0",
    
    # Accents (Windows Blue by default)
    "accent": "#005FB8",
    "accent_light1": "#0078D4",
    "accent_light2": "#47A0E7",
    "accent_light3": "#7DC0F0",
    "accent_dark1": "#003E7E",
    "accent_dark2": "#002754",
    "on_accent": "#FFFFFF",
    
    # Controls
    "control": "#FDFDFD",
    "control_alt": "#F2F2F2",
    "control_border": "#E5E5E5",
    "control_border_default": "#8A8A8A",
    "control_strong": "#767676",
    
    # States
    "hover": "#E5E5E5", # Simplified for Tkinter
    "pressed": "#D5D5D5",
    "disabled": "#F2F2F2",
    
    # Semantic
    "success": "#0F7B0F",
    "warning": "#9D5D00",
    "error": "#C42B1C",
    "info": "#0078D4",
}

# =============================================================================
# DARK THEME
# =============================================================================

DARK = {
    # Backgrounds
    "background": "#202020",
    "background_solid": "#1C1C1C",
    "layer": "#2D2D2D",
    "layer_alt": "#282828",
    "card": "#2D2D2D",
    
    # Text
    "text_primary": "#FFFFFF",
    "text_secondary": "#D4D4D4",
    "text_tertiary": "#9D9D9D",
    "text_disabled": "#6D6D6D",
    
    # Accents
    "accent": "#60CDFF",
    "accent_light1": "#77D7FF",
    "accent_light2": "#99E1FF",
    "accent_light3": "#BBEAFF",
    "accent_dark1": "#0093E0",
    "accent_dark2": "#006DAA",
    "on_accent": "#003D73",
    
    # Controls
    "control": "#2D2D2D",
    "control_alt": "#323232",
    "control_border": "#454545",
    "control_border_default": "#6D6D6D",
    "control_strong": "#9D9D9D",
    
    # States
    "hover": "#3D3D3D",
    "pressed": "#4D4D4D",
    "disabled": "#2D2D2D",
    
    # Semantic
    "success": "#6CCB5F",
    "warning": "#FCE100",
    "error": "#FF99A4",
    "info": "#60CDFF",
}

# =============================================================================
# TYPOGRAPHY
# =============================================================================

TYPOGRAPHY = {
    "font_family": "Segoe UI Variable",
    "font_family_fallback": "Segoe UI, sans-serif",
    "sizes": {
        "caption": 10,
        "body": 12,
        "body_strong": 12,
        "subtitle": 18,
        "title": 24,
        "title_large": 36,
        "display": 60,
    },
    "weights": {
        "regular": "normal",
        "semibold": "bold",
        "bold": "bold",
    },
}

# =============================================================================
# SPACING AND BORDERS
# =============================================================================

SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 12,
    "lg": 16,
    "xl": 24,
    "xxl": 32,
}

BORDERS = {
    "radius_sm": 4,
    "radius_md": 8,
    "radius_lg": 12,
    "radius_full": 99,
}

class Colors:
    """Helper class to access colors as attributes for WinFormPy."""
    # Primary accent colors
    Accent = LIGHT["accent"]
    AccentLight1 = LIGHT["accent_light1"]
    AccentLight2 = LIGHT["accent_light2"]
    AccentLight3 = LIGHT["accent_light3"]
    AccentDark1 = LIGHT["accent_dark1"]
    AccentDark2 = LIGHT["accent_dark2"]
    on_accent = LIGHT["on_accent"]
    
    # Text colors
    AccentText = LIGHT["on_accent"]
    TextPrimary = LIGHT["text_primary"]
    TextSecondary = LIGHT["text_secondary"]
    TextTertiary = LIGHT["text_tertiary"]
    TextDisabled = LIGHT["text_disabled"]
    
    # Background colors
    WindowBg = LIGHT["background"]
    ContentBg = LIGHT["background_solid"]
    CardBg = LIGHT["card"]
    LayerBg = LIGHT["layer"]
    
    # Border colors
    Border = LIGHT["control_border"]
    BorderFocused = LIGHT["accent"]
    CardBorder = LIGHT["control_border"]
    
    # State colors
    ErrorBg = "#FDE7E9" # Default fallback
    ErrorText = LIGHT["error"]
    WarningBg = "#FFF4CE"
    WarningText = LIGHT["warning"]
    SuccessBg = "#DFF6DD"
    SuccessText = LIGHT["success"]
    InfoBg = "#E7F3FD"
    InfoText = LIGHT["info"]
    
    # Control states
    ControlBorder = LIGHT["control_border"]
    ControlBorderHover = LIGHT["accent"]
    ControlBorderPressed = LIGHT["accent_dark1"]
    ControlBg = LIGHT["background_solid"]
    ControlBgHover = LIGHT["hover"]
    ControlBgPressed = LIGHT["pressed"]
    ControlBgDisabled = LIGHT["disabled"]


class Fonts:
    """WinUI 3 Typography ramp."""
    _family = TYPOGRAPHY["font_family"]
    
    Display = (_family, TYPOGRAPHY["sizes"]["display"], "normal")
    TitleLarge = (_family, TYPOGRAPHY["sizes"]["title_large"], "bold")
    Title = (_family, TYPOGRAPHY["sizes"]["title"], "bold")
    SubtitleLarge = (_family, TYPOGRAPHY["sizes"]["subtitle"], "bold")
    Subtitle = (_family, 16, "bold")
    BodyLarge = (_family, 18, "normal")
    BodyStrong = (_family, TYPOGRAPHY["sizes"]["body_strong"], "bold")
    Body = (_family, TYPOGRAPHY["sizes"]["body"], "normal")
    Caption = (_family, TYPOGRAPHY["sizes"]["caption"], "normal")
    CaptionStrong = (_family, TYPOGRAPHY["sizes"]["caption"], "bold")
    
    # Legacy
    Header = Subtitle
    Default = Caption

# Instance for easy access
winui_colors = Colors()
winui_fonts = Fonts()
