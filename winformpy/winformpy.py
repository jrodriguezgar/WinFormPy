# =============================================================
# Module: winformpy.py
# Author: Vibe coding by DatamanEdge 
# Date: 2025-12-15
# Version: 1.0.6
# Description: 
# WinFormPy is a complete Python library designed to
# bridge the gap between the graphical user interface (GUI) 
# development paradigm of Visual Basic (VB.NET / WinForms) 
# and Python's standard toolkit, Tkinter.
# This tool allows developers with 
# VB experience to leverage their existing knowledge to create 
# cross-platform desktop applications in Python, minimizing the 
# learning curve of Tkinter's specific conventions.
# =============================================================


import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import tkinter.font as tkfont
import tkinter.font as tkfont
import os
from enum import Enum, IntFlag, IntEnum
from datetime import datetime, date
try:
    import winsound
except ImportError:
    winsound = None
from datetime import date, datetime
import sys
import subprocess
import importlib
from typing import List, Tuple, Optional, Union, Literal

 # Import winformpy_tools utilities
try:
    from .winformpy_tools import css_to_tkinter_config, apply_css_to_widget
except ImportError:
    try:
        from winformpy_tools import css_to_tkinter_config, apply_css_to_widget
    except ImportError:
        # Fallback if import fails
        def css_to_tkinter_config(css_string, current_widget=None):
            return {}
        def apply_css_to_widget(widget, css_string):
            pass

import warnings


# =============================================================
# Lazy Library Import Management
# =============================================================

def install_library(library_name: str, import_name: str = None) -> bool:
    """
    Checks if a library is installed and, if not, attempts to install it via pip.
    """
    try:
        if import_name:
            library_name = import_name
        __import__(library_name)
        return True
    except ImportError:
        print(f"Library '{library_name}' not found. Attempting to install...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", library_name])
            print(f"Library '{library_name}' installed successfully.")
            return True
        except subprocess.CalledProcessError:
            print(f"Error: Failed to install '{library_name}'.")
            return False


def _resolve_master_widget(master_form):
    """Resolves the Tkinter widget from a Form/Panel/GroupBox container.
    
    Args:
        master_form: Can be a Form, Panel, GroupBox, or direct Tkinter widget
    
    Returns:
        tuple: (tkinter_widget, original_container)
        - tkinter_widget: The Tkinter widget where the control will be created
        - original_container: The original Form/Panel/GroupBox container for Parent
    """
    # Save the original container
    parent_container = master_form
    
    # Check if it's already a Tkinter widget (Tk or Widget)
    if isinstance(master_form, (tk.Tk, tk.Widget)):
        master_widget = master_form
        parent_container = None
    # Resolve to the Tkinter widget
    elif hasattr(master_form, '_container'):
        # Panel or GroupBox with _container
        master_widget = master_form._container
    elif hasattr(master_form, '_root'):
        # Form with _root
        master_widget = master_form._root
    elif hasattr(master_form, '_frame'):
        # TabPage with _frame
        master_widget = master_form._frame
    elif hasattr(master_form, '_tk_widget'):
        # Other control with _tk_widget
        master_widget = master_form._tk_widget
    else:
        # Already a Tkinter widget (fallback)
        master_widget = master_form
        parent_container = None  # No wrapper container
    
    return master_widget, parent_container


# =======================================================================
# MAIN MODULE: winformpy.py
# =======================================================================

class SystemColors:
    """Windows Forms system colors."""
    Control = "#F0F0F0"  # Control background color
    ControlText = "#000000"  # Control text color
    Window = "#FFFFFF"  # Window background color
    WindowText = "#000000"  # Window text color
    Highlight = "#0078D7"  # Highlight/selection color
    HighlightText = "#FFFFFF"  # Highlighted text color
    GrayText = "#6D6D6D"  # Disabled text color
    ButtonFace = "#F0F0F0"  # Button background color
    ButtonText = "#000000"  # Button text color
    ActiveCaption = "#0078D7"  # Active title bar color
    ActiveCaptionText = "#FFFFFF" # Active title bar text color
    InactiveCaption = "#BFBFBF"  # Inactive title bar color
    ActiveBorder = "#B4B4B4"  # Active border color
    InactiveBorder = "#F4F4F4"  # Inactive border color
    AppWorkspace = "#ABABAB"  # MDI workspace background color
    Desktop = "#000000"  # Desktop background color
    MenuBar = "#F0F0F0"  # Menu bar background color
    Menu = "#F0F0F0"  # Menu background color
    MenuText = "#000000"  # Menu text color
    Info = "#FFFFE1"  # Tooltip background color
    InfoText = "#000000"  # Tooltip text color


class SystemFonts:
    """Windows Forms system fonts."""
    DefaultFont = ("Segoe UI", 9)  # Default system font
    MessageBoxFont = ("Segoe UI", 9)  # MessageBox font
    CaptionFont = ("Segoe UI", 9)  # Title bar font
    SmallCaptionFont = ("Segoe UI", 8)  # Small title bar font
    MenuFont = ("Segoe UI", 9)  # Menu font
    StatusFont = ("Segoe UI", 9)  # Status bar font
    IconTitleFont = ("Segoe UI", 9)  # Icon title font
    DialogFont = ("Segoe UI", 9)  # Dialog font


class SystemStyles:
    """Class to manage system styles and allow global customization.
    
    Usage:
        # Use system styles (default)
        button = Button(form, {'UseSystemStyles': True})
        
        # Or set custom global styles
        SystemStyles.SetGlobalFont(("Arial", 10))
        SystemStyles.SetGlobalColors(BackColor="#FFFFFF", ForeColor="#000000")
    """
    
    # Global configuration (None = use system values)
    _global_font = None
    _global_back_color = None
    _global_fore_color = None
    _use_system_styles_by_default = True
    
    @staticmethod
    def SetGlobalFont(font):
        """Sets a global font for all new controls.
        
        Args:
            font: Tuple (font_name, size) or None to use system font
        """
        SystemStyles._global_font = font
    
    @staticmethod
    def SetGlobalColors(BackColor=None, ForeColor=None):
        """Sets global colors for all new controls.
        
        Args:
            BackColor: Background color or None to use system color
            ForeColor: Text color or None to use system color
        """
        if BackColor is not None:
            SystemStyles._global_back_color = BackColor
        if ForeColor is not None:
            SystemStyles._global_fore_color = ForeColor
    
    @staticmethod
    def SetUseSystemStylesByDefault(value):
        """Sets whether to use system styles by default.
        
        Args:
            value: True to use system styles, False to use None
        """
        SystemStyles._use_system_styles_by_default = value
    
    @staticmethod
    def GetDefaultFont(control_type="Control"):
        """Gets the default font according to configuration.
        
        Args:
            control_type: Control type ("Control", "Menu", "Status", etc.)
        
        Returns:
            Font to use or None if not to be applied
        """
        # Priority: global > system > None
        if SystemStyles._global_font is not None:
            return SystemStyles._global_font
        
        if SystemStyles._use_system_styles_by_default:
            if control_type == "Menu":
                return SystemFonts.MenuFont
            elif control_type == "Status":
                return SystemFonts.StatusFont
            elif control_type == "Dialog":
                return SystemFonts.DialogFont
            else:
                return SystemFonts.DefaultFont
        
        return None
    
    @staticmethod
    def GetDefaultBackColor(control_type="Control"):
        """Gets the default background color according to configuration.
        
        Args:
            control_type: Control type ("Control", "Window", "Button", etc.)
        
        Returns:
            Color to use or None if not to be applied
        """
        # Priority: global > system > None
        if SystemStyles._global_back_color is not None:
            return SystemStyles._global_back_color
        
        if SystemStyles._use_system_styles_by_default:
            if control_type == "Window":
                return SystemColors.Window
            elif control_type == "Button":
                return SystemColors.ButtonFace
            else:
                return SystemColors.Control
        
        return None
    
    @staticmethod
    def GetDefaultForeColor(control_type="Control"):
        """Gets the default text color according to configuration.
        
        Args:
            control_type: Control type ("Control", "Window", "Button", etc.)
        
        Returns:
            Color to use or None if not to be applied
        """
        # Priority: global > system > None
        if SystemStyles._global_fore_color is not None:
            return SystemStyles._global_fore_color
        
        if SystemStyles._use_system_styles_by_default:
            if control_type == "Window":
                return SystemColors.WindowText
            elif control_type == "Button":
                return SystemColors.ButtonText
            else:
                return SystemColors.ControlText
        
        return None
    
    @staticmethod
    def ApplyToDefaults(defaults, control_type="Control", use_system_styles=None):
        """Applies system styles to a defaults dictionary if enabled.
        
        Args:
            defaults: Dictionary of default values
            control_type: Control type to determine appropriate styles
            use_system_styles: True/False to force, None to use global configuration
        
        Returns:
            Modified defaults dictionary
        """
        # Determine whether to apply system styles
        apply = use_system_styles if use_system_styles is not None else SystemStyles._use_system_styles_by_default
        
        if not apply:
            return defaults
        
        # Apply only if the value is None in defaults
        if 'Font' in defaults and defaults['Font'] is None:
            defaults['Font'] = SystemStyles.GetDefaultFont(control_type)
        
        if 'BackColor' in defaults and defaults['BackColor'] is None:
            defaults['BackColor'] = SystemStyles.GetDefaultBackColor(control_type)
        
        if 'ForeColor' in defaults and defaults['ForeColor'] is None:
            defaults['ForeColor'] = SystemStyles.GetDefaultForeColor(control_type)
        
        return defaults


############# Enumerates #############

class DialogResult(Enum):
    None_ = 0
    OK = 1
    Cancel = 2
    Abort = 3
    Retry = 4
    Ignore = 5
    Yes = 6
    No = 7

class Appearance(Enum):
    Normal = 0
    Button = 1

class AutoSizeMode(Enum):
    """Specifies how a control sizes itself to its content."""
    GrowAndShrink = 0
    GrowOnly = 1

class BorderStyle(Enum):
    """Specifies the border style for a control."""
    None_ = 0  # 'None' is a keyword in Python
    FixedSingle = 1
    Fixed3D = 2

class CheckState(IntEnum):
    Unchecked = 0
    Checked = 1
    Indeterminate = 2

class ContentAlignment(Enum):
    TopLeft = 1
    TopCenter = 2
    TopRight = 4
    MiddleLeft = 16
    MiddleCenter = 32
    MiddleRight = 64
    BottomLeft = 256
    BottomCenter = 512
    BottomRight = 1024

class DialogResult(Enum):
    None_ = 0
    OK = 1
    Cancel = 2
    Abort = 3
    Retry = 4
    Ignore = 5
    Yes = 6
    No = 7

class DockStyle(Enum):
    None_ = 0
    Top = 1
    Bottom = 2
    Left = 3
    Right = 4
    Fill = 5

class AnchorStyles(IntFlag):
    None_ = 0
    Top = 1
    Bottom = 2
    Left = 4
    Right = 8

class FlowDirection(Enum):
    LeftToRight = 0
    TopDown = 1
    RightToLeft = 2
    BottomUp = 3

class FormBorderStyle(Enum):
    None_ = 0
    FixedSingle = 1
    Fixed3D = 2
    FixedDialog = 3
    Sizable = 4
    FixedToolWindow = 5
    SizableToolWindow = 6

class FormStartPosition(Enum):
    Manual = 0
    CenterScreen = 1
    WindowsDefaultLocation = 2
    WindowsDefaultBounds = 3
    CenterParent = 4

class FormWindowState(Enum):
    Normal = 0
    Minimized = 1
    Maximized = 2


class Orientation(Enum):
    Horizontal = 0
    Vertical = 1

class FixedPanel(Enum):
    None_ = 0
    Panel1 = 1
    Panel2 = 2

class SizeType(Enum):
    AutoSize = 0
    Absolute = 1
    Percent = 2

class TableLayoutPanelCellBorderStyle(Enum):
    None_ = 0
    Single = 1
    Inset = 2
    InsetDouble = 3
    Outset = 4
    OutsetDouble = 5
    OutsetPartial = 6

class TableLayoutPanelGrowStyle(Enum):
    FixedSize = 0
    AddRows = 1
    AddColumns = 2

class TabAppearance(Enum):
    Normal = 0
    Buttons = 1
    FlatButtons = 2

class TabAlignment(Enum):
    Top = 0
    Bottom = 1
    Left = 2
    Right = 3

class TabSizeMode(Enum):
    Normal = 0
    Fixed = 1
    FillToRight = 2


class ScrollBars(Enum):
    None_ = 0
    Horizontal = 1
    Vertical = 2
    Both = 3

class SelectionMode(Enum):
    None_ = 0
    One = 1
    MultiSimple = 2
    MultiExtended = 3

class View(Enum):
    LargeIcon = 0
    Details = 1
    SmallIcon = 2
    List = 3
    Tile = 4

class ColumnHeaderStyle(Enum):
    None_ = 0
    Nonclickable = 1
    Clickable = 2

class SortOrder(Enum):
    None_ = 0
    Ascending = 1
    Descending = 2

class DatePickerFormat(Enum):
    """Date format patterns supported by DatePicker (tkcalendar DateEntry)."""
    USFormat = "mm/dd/yyyy"  # US format: 12/31/2025
    EUFormat = "dd/mm/yyyy"  # European format: 31/12/2025
    ISOFormat = "yyyy-mm-dd"  # ISO format: 2025-12-31
    Custom = "custom"         # Custom format defined by CustomFormat property

class DataGridViewSelectionMode(Enum):
    CellSelect = 0
    FullRowSelect = 1
    RowHeaderSelect = 2
    FullColumnSelect = 3
    ColumnHeaderSelect = 4

class DataGridViewAutoSizeColumnsMode(Enum):
    None_ = 0
    ColumnHeader = 1
    AllCells = 2
    AllCellsExceptHeader = 3
    DisplayedCells = 4
    DisplayedCellsExceptHeader = 5
    Fill = 6

class DataGridViewColumnHeadersHeightSizeMode(Enum):
    EnableResizing = 0
    DisableResizing = 1
    AutoSize = 2

class TreeViewAction(Enum):
    Unknown = 0
    ByKeyboard = 1
    ByMouse = 2
    Collapse = 3
    Expand = 4

class Day(Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6
    Default = 7

class ProgressBarStyle(Enum):
    Blocks = 0
    Continuous = 1
    Marquee = 2

class TickStyle(Enum):
    None_ = 0
    TopLeft = 1
    BottomRight = 2
    Both = 3

class PictureBoxSizeMode(Enum):
    Normal = 0
    StretchImage = 1
    AutoSize = 2
    CenterImage = 3
    Zoom = 4

class AutoSizeMode(Enum):
    GrowAndShrink = 0
    GrowOnly = 1

class TextImageRelation(Enum):
    Overlay = 0
    ImageAboveText = 1
    TextAboveImage = 2
    ImageBeforeText = 4
    TextBeforeImage = 8

class FlatStyle(Enum):
    Flat = 0
    Popup = 1
    Standard = 2
    System = 3

class HorizontalAlignment(Enum):
    Left = 0
    Right = 1
    Center = 2

class LeftRightAlignment(Enum):
    Left = 0
    Right = 1

class CharacterCasing(Enum):
    Normal = 0
    Upper = 1
    Lower = 2

class AutoCompleteMode(Enum):
    None_ = 0
    Suggest = 1
    Append = 2
    SuggestAppend = 3

class AutoCompleteSource(Enum):
    FileSystem = 1
    HistoryList = 2
    RecentlyUsedList = 4
    AllUrl = 6
    AllSystemSources = 7
    FileSystemDirectories = 32
    CustomSource = 64
    None_ = 128
    ListItems = 256

class ComboBoxStyle(Enum):
    Simple = 0
    DropDown = 1
    DropDownList = 2


# =============================================================
# Helper Classes and Decorators
# =============================================================

class classproperty:
    """Descriptor for class properties."""
    
    def __init__(self, fget):
        self.fget = fget
    
    def __get__(self, obj, cls=None):
        return self.fget(cls)


class Color:
    """Represents an ARGB (alpha, red, green, blue) color.
    
    This class provides WinForms-like color handling with support for:
    - Named colors (Color.Red, Color.Blue, etc.)
    - RGB values
    - Hex color strings
    - System colors
    
    Usage:
        color1 = Color.Red
        color2 = Color.FromRgb(255, 0, 0)
        color3 = Color.FromHex("#FF0000")
        color4 = Color.FromName("red")
        color5 = Color.FromSystemColor("Control")
    """
    
    # Named colors (common HTML/CSS colors)
    AliceBlue = "#F0F8FF"
    AntiqueWhite = "#FAEBD7"
    Aqua = "#00FFFF"
    Aquamarine = "#7FFFD4"
    Azure = "#F0FFFF"
    Beige = "#F5F5DC"
    Bisque = "#FFE4C4"
    Black = "#000000"
    BlanchedAlmond = "#FFEBCD"
    Blue = "#0000FF"
    BlueViolet = "#8A2BE2"
    Brown = "#A52A2A"
    BurlyWood = "#DEB887"
    CadetBlue = "#5F9EA0"
    Chartreuse = "#7FFF00"
    Chocolate = "#D2691E"
    Coral = "#FF7F50"
    CornflowerBlue = "#6495ED"
    Cornsilk = "#FFF8DC"
    Crimson = "#DC143C"
    Cyan = "#00FFFF"
    DarkBlue = "#00008B"
    DarkCyan = "#008B8B"
    DarkGoldenrod = "#B8860B"
    DarkGray = "#A9A9A9"
    DarkGreen = "#006400"
    DarkKhaki = "#BDB76B"
    DarkMagenta = "#8B008B"
    DarkOliveGreen = "#556B2F"
    DarkOrange = "#FF8C00"
    DarkOrchid = "#9932CC"
    DarkRed = "#8B0000"
    DarkSalmon = "#E9967A"
    DarkSeaGreen = "#8FBC8F"
    DarkSlateBlue = "#483D8B"
    DarkSlateGray = "#2F4F4F"
    DarkTurquoise = "#00CED1"
    DarkViolet = "#9400D3"
    DeepPink = "#FF1493"
    DeepSkyBlue = "#00BFFF"
    DimGray = "#696969"
    DodgerBlue = "#1E90FF"
    Firebrick = "#B22222"
    FloralWhite = "#FFFAF0"
    ForestGreen = "#228B22"
    Fuchsia = "#FF00FF"
    Gainsboro = "#DCDCDC"
    GhostWhite = "#F8F8FF"
    Gold = "#FFD700"
    Goldenrod = "#DAA520"
    Gray = "#808080"
    Green = "#008000"
    GreenYellow = "#ADFF2F"
    Honeydew = "#F0FFF0"
    HotPink = "#FF69B4"
    IndianRed = "#CD5C5C"
    Indigo = "#4B0082"
    Ivory = "#FFFFF0"
    Khaki = "#F0E68C"
    Lavender = "#E6E6FA"
    LavenderBlush = "#FFF0F5"
    LawnGreen = "#7CFC00"
    LemonChiffon = "#FFFACD"
    LightBlue = "#ADD8E6"
    LightCoral = "#F08080"
    LightCyan = "#E0FFFF"
    LightGoldenrodYellow = "#FAFAD2"
    LightGray = "#D3D3D3"
    LightGreen = "#90EE90"
    LightPink = "#FFB6C1"
    LightSalmon = "#FFA07A"
    LightSeaGreen = "#20B2AA"
    LightSkyBlue = "#87CEFA"
    LightSlateGray = "#778899"
    LightSteelBlue = "#B0C4DE"
    LightYellow = "#FFFFE0"
    Lime = "#00FF00"
    LimeGreen = "#32CD32"
    Linen = "#FAF0E6"
    Magenta = "#FF00FF"
    Maroon = "#800000"
    MediumAquamarine = "#66CDAA"
    MediumBlue = "#0000CD"
    MediumOrchid = "#BA55D3"
    MediumPurple = "#9370DB"
    MediumSeaGreen = "#3CB371"
    MediumSlateBlue = "#7B68EE"
    MediumSpringGreen = "#00FA9A"
    MediumTurquoise = "#48D1CC"
    MediumVioletRed = "#C71585"
    MidnightBlue = "#191970"
    MintCream = "#F5FFFA"
    MistyRose = "#FFE4E1"
    Moccasin = "#FFE4B5"
    NavajoWhite = "#FFDEAD"
    Navy = "#000080"
    OldLace = "#FDF5E6"
    Olive = "#808000"
    OliveDrab = "#6B8E23"
    Orange = "#FFA500"
    OrangeRed = "#FF4500"
    Orchid = "#DA70D6"
    PaleGoldenrod = "#EEE8AA"
    PaleGreen = "#98FB98"
    PaleTurquoise = "#AFEEEE"
    PaleVioletRed = "#DB7093"
    PapayaWhip = "#FFEFD5"
    PeachPuff = "#FFDAB9"
    Peru = "#CD853F"
    Pink = "#FFC0CB"
    Plum = "#DDA0DD"
    PowderBlue = "#B0E0E6"
    Purple = "#800080"
    Red = "#FF0000"
    RosyBrown = "#BC8F8F"
    RoyalBlue = "#4169E1"
    SaddleBrown = "#8B4513"
    Salmon = "#FA8072"
    SandyBrown = "#F4A460"
    SeaGreen = "#2E8B57"
    SeaShell = "#FFF5EE"
    Sienna = "#A0522D"
    Silver = "#C0C0C0"
    SkyBlue = "#87CEEB"
    SlateBlue = "#6A5ACD"
    SlateGray = "#708090"
    Snow = "#FFFAFA"
    SpringGreen = "#00FF7F"
    SteelBlue = "#4682B4"
    Tan = "#D2B48C"
    Teal = "#008080"
    Thistle = "#D8BFD8"
    Tomato = "#FF6347"
    Transparent = ""
    Turquoise = "#40E0D0"
    Violet = "#EE82EE"
    Wheat = "#F5DEB3"
    White = "#FFFFFF"
    WhiteSmoke = "#F5F5F5"
    Yellow = "#FFFF00"
    YellowGreen = "#9ACD32"
    
    def __init__(self, value=None, r=None, g=None, b=None):
        """Initialize a Color with various input formats.
        
        Args:
            value: Can be:
                - Hex string (e.g., "#FF0000" or "FF0000")
                - Named color string (e.g., "red")
                - RGB tuple/list (e.g., (255, 0, 0) or [255, 0, 0])
                - Another Color object
                - None (defaults to black)
            r: Red component (0-255) if creating from individual RGB values
            g: Green component (0-255) if creating from individual RGB values
            b: Blue component (0-255) if creating from individual RGB values
        """
        # If individual RGB components provided
        if r is not None and g is not None and b is not None:
            r = max(0, min(255, int(r)))
            g = max(0, min(255, int(g)))
            b = max(0, min(255, int(b)))
            self._value = f"#{r:02X}{g:02X}{b:02X}"
        # If value is None, default to black
        elif value is None:
            self._value = "#000000"
        # If value is a Color object, copy its value
        elif isinstance(value, Color):
            self._value = value._value
        # If value is a tuple or list (RGB format)
        elif isinstance(value, (tuple, list)):
            if len(value) >= 3:
                r = max(0, min(255, int(value[0])))
                g = max(0, min(255, int(value[1])))
                b = max(0, min(255, int(value[2])))
                self._value = f"#{r:02X}{g:02X}{b:02X}"
            else:
                self._value = "#000000"
        # If value is a string
        elif isinstance(value, str):
            if not value:
                self._value = "#000000"
            else:
                value = value.strip()
                # If it starts with #, assume it's hex
                if value.startswith('#'):
                    self._value = value
                # If it looks like hex without #
                elif len(value) == 6 and all(c in '0123456789ABCDEFabcdef' for c in value):
                    self._value = '#' + value
                # Otherwise assume it's a named color
                else:
                    self._value = value
        # Default case
        else:
            self._value = "#000000"
    
    def __str__(self):
        """Return the color as a hex string."""
        return self._value
    
    def __repr__(self):
        """Return the color representation."""
        return f"Color('{self._value}')"
    
    @staticmethod
    def FromRgb(r, g, b, a=255):
        """Create a Color from RGB values (0-255).
        
        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
            a: Alpha component (0-255), default 255 (opaque)
        
        Returns:
            Color object
        """
        r = max(0, min(255, int(r)))
        g = max(0, min(255, int(g)))
        b = max(0, min(255, int(b)))
        hex_color = f"#{r:02X}{g:02X}{b:02X}"
        return Color(hex_color)
    
    @staticmethod
    def FromHex(hex_string):
        """Create a Color from a hex string.
        
        Args:
            hex_string: Hex color string (e.g., "#FF0000" or "FF0000")
        
        Returns:
            Color object
        """
        if not hex_string:
            return Color("#000000")
        
        hex_string = hex_string.strip()
        if not hex_string.startswith('#'):
            hex_string = '#' + hex_string
        
        return Color(hex_string)
    
    @staticmethod
    def FromName(name):
        """Create a Color from a color name.
        
        Args:
            name: Color name (e.g., "red", "blue", "Red", "Blue")
        
        Returns:
            Color object
        """
        # Convert to title case to match class attributes
        name_title = name.title().replace(" ", "")
        
        # Check if it's a named color
        if hasattr(Color, name_title):
            value = getattr(Color, name_title)
            return Color(value)
        
        # If not found, return as-is (Tkinter might understand it)
        return Color(name.lower())
    
    @staticmethod
    def FromSystemColor(system_color_name):
        """Create a Color from a SystemColors attribute.
        
        Args:
            system_color_name: Name of the SystemColors attribute
        
        Returns:
            Color object
        """
        if hasattr(SystemColors, system_color_name):
            value = getattr(SystemColors, system_color_name)
            return Color(value)
        
        return Color(SystemColors.Control)
    
    @property
    def Name(self):
        """Get the name of the color if it's a known color."""
        # Try to find a matching named color
        for attr_name in dir(Color):
            if not attr_name.startswith('_') and attr_name[0].isupper():
                attr_value = getattr(Color, attr_name)
                if isinstance(attr_value, str) and attr_value.upper() == self._value.upper():
                    return attr_name
        return self._value
    
    @property
    def R(self):
        """Get the red component (0-255)."""
        if self._value.startswith('#') and len(self._value) >= 7:
            return int(self._value[1:3], 16)
        return 0
    
    @property
    def G(self):
        """Get the green component (0-255)."""
        if self._value.startswith('#') and len(self._value) >= 7:
            return int(self._value[3:5], 16)
        return 0
    
    @property
    def B(self):
        """Get the blue component (0-255)."""
        if self._value.startswith('#') and len(self._value) >= 7:
            return int(self._value[5:7], 16)
        return 0
    
    @property
    def A(self):
        """Get the alpha component (0-255)."""
        return 255  # Default opaque


class Font:
    """Represents a font for text rendering.
    
    This class provides WinForms-like font handling compatible with Tkinter.
    
    Usage:
        font1 = Font("Arial", 12)
        font2 = Font("Segoe UI", 10, FontStyle.Bold)
        font3 = Font("Consolas", 9, FontStyle.Bold | FontStyle.Italic)
        font4 = Font.FromSystemFont()
    """
    
    def __init__(self, family=None, size=None, style=None):
        """Initialize a Font.
        
        Args:
            family: Font family name (default: system default)
            size: Font size in points (default: 9)
            style: FontStyle flags (default: FontStyle.Regular)
        """
        self._family = family or SystemFonts.DefaultFont[0]
        self._size = size if size is not None else SystemFonts.DefaultFont[1]
        self._style = style if style is not None else FontStyle.Regular
        self._tk_font = None
        self._create_tk_font()
    
    def _create_tk_font(self):
        """Create the underlying Tkinter font."""
        weight = "bold" if (self._style & FontStyle.Bold) else "normal"
        slant = "italic" if (self._style & FontStyle.Italic) else "roman"
        underline = bool(self._style & FontStyle.Underline)
        overstrike = bool(self._style & FontStyle.Strikeout)
        
        self._tk_font = tkfont.Font(
            family=self._family,
            size=self._size,
            weight=weight,
            slant=slant,
            underline=underline,
            overstrike=overstrike
        )
    
    @staticmethod
    def FromSystemFont(font_type="Default"):
        """Create a Font from a system font.
        
        Args:
            font_type: Type of system font ("Default", "Menu", "Status", "Dialog", etc.)
        
        Returns:
            Font object
        """
        font_attr = f"{font_type}Font"
        if hasattr(SystemFonts, font_attr):
            sys_font = getattr(SystemFonts, font_attr)
            return Font(sys_font[0], sys_font[1])
        
        return Font()
    
    @property
    def Name(self):
        """Get the font family name."""
        return self._family
    
    @Name.setter
    def Name(self, value):
        """Set the font family name."""
        self._family = value
        self._create_tk_font()
    
    @property
    def Size(self):
        """Get the font size in points."""
        return self._size
    
    @Size.setter
    def Size(self, value):
        """Set the font size in points."""
        self._size = value
        self._create_tk_font()
    
    @property
    def Style(self):
        """Get the font style."""
        return self._style
    
    @Style.setter
    def Style(self, value):
        """Set the font style."""
        self._style = value
        self._create_tk_font()
    
    @property
    def Bold(self):
        """Get whether the font is bold."""
        return bool(self._style & FontStyle.Bold)
    
    @Bold.setter
    def Bold(self, value):
        """Set whether the font is bold."""
        if value:
            self._style |= FontStyle.Bold
        else:
            self._style &= ~FontStyle.Bold
        self._create_tk_font()
    
    @property
    def Italic(self):
        """Get whether the font is italic."""
        return bool(self._style & FontStyle.Italic)
    
    @Italic.setter
    def Italic(self, value):
        """Set whether the font is italic."""
        if value:
            self._style |= FontStyle.Italic
        else:
            self._style &= ~FontStyle.Italic
        self._create_tk_font()
    
    @property
    def Underline(self):
        """Get whether the font is underlined."""
        return bool(self._style & FontStyle.Underline)
    
    @Underline.setter
    def Underline(self, value):
        """Set whether the font is underlined."""
        if value:
            self._style |= FontStyle.Underline
        else:
            self._style &= ~FontStyle.Underline
        self._create_tk_font()
    
    @property
    def Strikeout(self):
        """Get whether the font has strikeout."""
        return bool(self._style & FontStyle.Strikeout)
    
    @Strikeout.setter
    def Strikeout(self, value):
        """Set whether the font has strikeout."""
        if value:
            self._style |= FontStyle.Strikeout
        else:
            self._style &= ~FontStyle.Strikeout
        self._create_tk_font()
    
    def ToTkFont(self):
        """Get the Tkinter Font object."""
        return self._tk_font
    
    def ToTuple(self):
        """Convert to a tuple format (family, size, style_string)."""
        style_parts = []
        if self.Bold:
            style_parts.append("bold")
        if self.Italic:
            style_parts.append("italic")
        if self.Underline:
            style_parts.append("underline")
        if self.Strikeout:
            style_parts.append("overstrike")
        
        if style_parts:
            return (self._family, self._size, " ".join(style_parts))
        else:
            return (self._family, self._size)
    
    def __str__(self):
        """Return a string representation of the font."""
        return f"Font: {self._family}, {self._size}pt"
    
    def __repr__(self):
        """Return a detailed representation of the font."""
        style_str = []
        if self.Bold:
            style_str.append("Bold")
        if self.Italic:
            style_str.append("Italic")
        if self.Underline:
            style_str.append("Underline")
        if self.Strikeout:
            style_str.append("Strikeout")
        
        style_repr = " | ".join(style_str) if style_str else "Regular"
        return f"Font('{self._family}', {self._size}, {style_repr})"


class FontStyle(IntFlag):
    """Specifies style information applied to text."""
    Regular = 0
    Bold = 1
    Italic = 2
    Underline = 4
    Strikeout = 8


class Size:
    """Represents a size with width and height."""
    
    def __init__(self, width=0, height=0):
        self.Width = width
        self.Height = height


class Point:
    def __init__(self, x=0, y=0):
        self.X = x
        self.Y = y
    
    def __str__(self):
        return f"{{X={self.X},Y={self.Y}}}"


class Rectangle:
    def __init__(self, x=0, y=0, width=0, height=0):
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height
        
    @property
    def Left(self): return self.X
    
    @property
    def Top(self): return self.Y
    
    @property
    def Right(self): return self.X + self.Width
    
    @property
    def Bottom(self): return self.Y + self.Height
    
    def Contains(self, x, y):
        return self.X <= x < self.X + self.Width and self.Y <= y < self.Y + self.Height
        
    def __str__(self):
        return f"{{X={self.X},Y={self.Y},Width={self.Width},Height={self.Height}}}"


class ScrollableControlMixin:
    """
    Mixin to add scrolling capabilities to a control (Panel, TabPage, etc.).
    """

    def _init_scroll_properties(self, defaults):
        """Initialize scroll-related properties."""
        self.AutoScroll = defaults.get('AutoScroll', False)
        self.AutoScrollMinSize = defaults.get('AutoScrollMinSize', None)
        self.AutoScrollPosition = defaults.get('AutoScrollPosition', (0, 0))
        self.AutoScrollMargin = defaults.get('AutoScrollMargin', (0, 0))
        
        # Internal widgets
        self._canvas = None
        self._v_scrollbar = None
        self._h_scrollbar = None
        self._scroll_frame = None
        self._scroll_frame_id = None
        self._container = None # The container where children are added

    def _setup_scroll_infrastructure(self, parent_widget, bg_color):
        """
        Sets up the infrastructure for scrolling: Canvas + Scrollbars + Frame.
        
        Args:
            parent_widget: The widget that will contain the canvas (usually self._tk_widget)
            bg_color: Background color
        """
        # If AutoScroll is not enabled, we don't create the scroll structure
        if not self.AutoScroll:
            self._container = parent_widget
            return

        # Create a container frame for canvas and scrollbars if parent is not already a frame we can pack into
        # But usually parent_widget is a Frame or LabelFrame.
        
        # Create Canvas
        self._canvas = tk.Canvas(parent_widget, bg=bg_color, highlightthickness=0)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create Scrollbars
        self._v_scrollbar = tk.Scrollbar(parent_widget, orient=tk.VERTICAL, command=self._canvas.yview)
        self._v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self._h_scrollbar = tk.Scrollbar(parent_widget, orient=tk.HORIZONTAL, command=self._canvas.xview)
        self._h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure Canvas
        self._canvas.configure(yscrollcommand=self._v_scrollbar.set, xscrollcommand=self._h_scrollbar.set)
        
        # Create inner Frame (the actual container for controls)
        self._scroll_frame = tk.Frame(self._canvas, bg=bg_color)
        
        # Create window in canvas
        # We start with a default size, it will be updated by _update_scroll_region
        self._scroll_frame_id = self._canvas.create_window((0, 0), window=self._scroll_frame, anchor="nw")
        
        # Set _container to the inner frame so controls are added there
        self._container = self._scroll_frame
        
        # Bind events for updating scroll region
        self._scroll_frame.bind("<Configure>", self._on_scroll_frame_configure)
        self._canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Mouse wheel scrolling
        self._bind_mouse_wheel(self._canvas)
        self._bind_mouse_wheel(self._scroll_frame)
        
        # Initial update
        self._update_scroll_region()

    def _on_scroll_frame_configure(self, event):
        """Update scroll region when the inner frame changes size."""
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        """Resize the inner frame to match the canvas width (if we want to fit width)."""
        # For now, we don't force width to allow horizontal scrolling if needed
        pass

    def _update_scroll_region(self):
        """Manually update the scroll region based on child controls."""
        if not self._canvas or not self._scroll_frame:
            return
            
        if hasattr(self, 'Invalidate'):
            self.Invalidate()
        else:
            self._scroll_frame.update_idletasks()
        
        # Calculate bounding box of all children in _scroll_frame
        req_width = 0
        req_height = 0
        
        # Iterate over children to find max bounds
        children = self._scroll_frame.winfo_children()
        
        if not children:
            # If no children, use a minimum size or 0
            req_width = 1
            req_height = 1
        else:
            for child in children:
                try:
                    # Force update to get accurate info
                    # child.update_idletasks() 
                    
                    x = child.winfo_x()
                    y = child.winfo_y()
                    w = child.winfo_width()
                    h = child.winfo_height()
                    
                    # If unmapped or 1x1, try to use requested size
                    if w <= 1: w = child.winfo_reqwidth()
                    if h <= 1: h = child.winfo_reqheight()
                    
                    req_width = max(req_width, x + w)
                    req_height = max(req_height, y + h)
                except Exception:
                    pass
        
        # Add margins
        margin_x, margin_y = self.AutoScrollMargin if hasattr(self, 'AutoScrollMargin') else (0, 0)
        req_width += margin_x + 20 # Extra padding
        req_height += margin_y + 20 # Extra padding
        
        # Apply AutoScrollMinSize if set
        if self.AutoScrollMinSize:
            min_w, min_h = self.AutoScrollMinSize
            req_width = max(req_width, min_w)
            req_height = max(req_height, min_h)
            
        # Resize the scroll frame window in the canvas
        self._canvas.itemconfig(self._scroll_frame_id, width=req_width, height=req_height)
        
        # Update scrollregion
        self._canvas.configure(scrollregion=(0, 0, req_width, req_height))

    def _bind_mouse_wheel(self, widget):
        """Bind mouse wheel events for scrolling."""
        # Windows
        widget.bind("<MouseWheel>", self._on_mousewheel)
        # Linux
        widget.bind("<Button-4>", self._on_mousewheel)
        widget.bind("<Button-5>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        """Handle mouse wheel event."""
        if self._canvas:
            # Check if vertical scrollbar is active/needed
            if self._v_scrollbar.get() != (0.0, 1.0):
                if event.num == 4 or event.delta > 0:
                    self._canvas.yview_scroll(-1, "units")
                elif event.num == 5 or event.delta < 0:
                    self._canvas.yview_scroll(1, "units")


# =======================================================================
# WINDOWS FORMS CONTROLS
# =======================================================================

class Screen:
    """Represents the screen (Screen)."""
    
    def __init__(self, monitor_info=None):
        # Internal constructor.
        # monitor_info: dict with keys 'Bounds', 'WorkingArea', 'Primary', 'DeviceName', 'BitsPerPixel'
        
        # Try to get existing root or create one (careful with side effects)
        self._root = tk._default_root
        if self._root is None:
            # If we create a root here, it might pop up a window. 
            # Ideally we assume the app has started. 
            # If not, we create a hidden one?
            self._root = tk.Tk()
            self._root.withdraw()

        if monitor_info:
            self._bounds = monitor_info.get('Bounds')
            self._working_area = monitor_info.get('WorkingArea')
            self._primary = monitor_info.get('Primary', True)
            self._device_name = monitor_info.get('DeviceName', "Primary Screen")
            self._bits_per_pixel = monitor_info.get('BitsPerPixel', 32)
        else:
            # Default to primary screen info from Tkinter
            w = self._root.winfo_screenwidth()
            h = self._root.winfo_screenheight()
            self._bounds = Rectangle(0, 0, w, h)
            # Tkinter doesn't easily give working area (excluding taskbar). 
            # We'll assume full screen for now.
            self._working_area = Rectangle(0, 0, w, h) 
            self._primary = True
            self._device_name = "Primary Screen"
            self._bits_per_pixel = 32

    @classproperty
    def AllScreens(cls):
        """Gets an array of all screens on the system."""
        # Tkinter limitation: usually only sees the virtual screen or primary.
        # We return a list containing just the primary screen.
        return [Screen.PrimaryScreen]

    @property
    def BitsPerPixel(self):
        """Gets the number of bits of memory, associated with one pixel of data."""
        return self._bits_per_pixel

    @property
    def Bounds(self):
        """Gets the bounds of the screen."""
        return self._bounds

    @property
    def DeviceName(self):
        """Gets the device name associated with a display."""
        return self._device_name

    @property
    def Primary(self):
        """Gets a value indicating whether a particular display is the primary device."""
        return self._primary

    @classproperty
    def PrimaryScreen(cls):
        """Gets the primary display."""
        return Screen()

    @property
    def WorkingArea(self):
        """Gets the working area of the screen."""
        return self._working_area

    def Equals(self, obj):
        """Gets or sets a value indicating whether the specified object is equal to this Screen."""
        if isinstance(obj, Screen):
            return self.DeviceName == obj.DeviceName
        return False

    @staticmethod
    def FromControl(control):
        """Retrieves a Screen for the display that contains the largest portion of the specified control."""
        # In single-screen assumption, it's always PrimaryScreen
        return Screen.PrimaryScreen

    @staticmethod
    def FromHandle(handle):
        """Retrieves a Screen for the display that contains the largest portion of the object referred to by the specified handle."""
        return Screen.PrimaryScreen

    @staticmethod
    def FromPoint(point):
        """Retrieves a Screen for the display that contains the specified point."""
        return Screen.PrimaryScreen

    @staticmethod
    def FromRectangle(rect):
        """Retrieves a Screen for the display that contains the largest portion of the rectangle."""
        return Screen.PrimaryScreen

    @staticmethod
    def GetBounds(arg):
        """Retrieves the bounds of the screen that contains the specified point, rectangle, or control."""
        # arg can be Point, Rectangle, or Control
        # Since we only have one screen, the bounds are always that screen's bounds.
        return Screen.PrimaryScreen.Bounds

    def GetHashCode(self):
        """Computes and retrieves a hash code for an object."""
        return hash(self.DeviceName)

    @staticmethod
    def GetWorkingArea(arg):
        """Retrieves the working area of the screen that contains the specified point, rectangle, or control."""
        return Screen.PrimaryScreen.WorkingArea

    def ToString(self):
        """Retrieves a string that represents this object."""
        return f"Screen[Bounds={self.Bounds}, WorkingArea={self.WorkingArea}, Primary={self.Primary}, DeviceName={self.DeviceName}]"

    def __str__(self):
        return self.ToString()

    def __repr__(self):
        return self.ToString()
    
    # System events (placeholders)
    DisplaySettingsChanging = lambda sender, e: None
    DisplaySettingsChanged = lambda sender, e: None


############# Dialogs #############

class MessageBox:
    """Represents a MessageBox for messages with VB.NET-style parameters."""
    
    @staticmethod
    def Show(
        text,
        caption="Message",
        buttons="OK",
        icon=None,
        defaultButton=None,
        options=None,
        modal=True
    ):
        """Show a message and return the result.

        Parameters:
        - text: The main message.
        - caption: The title.
        - buttons: 'OK', 'OKCancel', 'YesNo', 'YesNoCancel', 'RetryCancel', 'AbortRetryIgnore'
        - icon: 'Information', 'Warning', 'Error', 'Question', 'None'
        - defaultButton: 'Button1', 'Button2', 'Button3' (not implemented in Tkinter)
        - options: 'RightAlign', 'RtlReading', etc. (partially supported)
        """
        # Determine parent widget for modal dialogs
        parent_widget = tk._default_root if modal else None

        # Map icon to messagebox function
        icon_map = {
            'Information': 'info',
            'Warning': 'warning',
            'Error': 'error',
            'Question': 'question',
            'None': 'info'
        }
        msg_type = icon_map.get(icon, 'info')
        
        # Adjust text for options
        display_text = text
        if options and 'RightAlign' in options:
            # Simulate right align (placeholder)
            display_text = text  # Tkinter doesn't support easily
        
        # Map buttons to Tkinter functions
        if buttons == "OK":
            if msg_type == 'warning':
                messagebox.showwarning(caption, display_text, parent=parent_widget)
            elif msg_type == 'error':
                messagebox.showerror(caption, display_text, parent=parent_widget)
            else:
                messagebox.showinfo(caption, display_text, parent=parent_widget)
            return DialogResult.OK
        elif buttons == "OKCancel":
            return DialogResult.OK if messagebox.askokcancel(caption, display_text, parent=parent_widget) else DialogResult.Cancel
        elif buttons == "YesNo":
            if msg_type == 'question':
                return DialogResult.Yes if messagebox.askyesno(caption, display_text, parent=parent_widget) else DialogResult.No
            else:
                return DialogResult.Yes if messagebox.askyesno(caption, display_text, parent=parent_widget) else DialogResult.No
        elif buttons == "YesNoCancel":
            result = messagebox.askyesnocancel(caption, display_text, parent=parent_widget)
            if result is True:
                return DialogResult.Yes
            elif result is False:
                return DialogResult.No
            else:
                return DialogResult.Cancel
        elif buttons == "RetryCancel":
            return DialogResult.Retry if messagebox.askretrycancel(caption, display_text, parent=parent_widget) else DialogResult.Cancel
        elif buttons == "AbortRetryIgnore":
            # Tkinter no tiene AbortRetryIgnore, simular con YesNoCancel o custom
            result = messagebox.askyesnocancel(
                caption,
                f"{display_text}\n\nAbort = Yes, Retry = No, Ignore = Cancel",
                parent=parent_widget
            )
            if result is True:
                return DialogResult.Abort
            elif result is False:
                return DialogResult.Retry
            else:
                return DialogResult.Ignore
        # Default
        messagebox.showinfo(caption, display_text, parent=parent_widget)
        return DialogResult.OK
    

class InputBox:
    """Represents an InputBox for text entry with VB.NET-style parameters."""
    
    @staticmethod
    def Show(prompt, title="Input", defaultResponse="", xpos=None, ypos=None, modal=True):
        """Show an input dialog and return the text.
        
        Parameters:
        - prompt: The main message.
        - title: The title.
        - defaultResponse: Default value in the text box.
        - xpos: X position (not implemented in Tkinter simpledialog).
        - ypos: Y position (not implemented in Tkinter simpledialog).
        """
        from tkinter import simpledialog
        parent_widget = tk._default_root if modal else None
        result = simpledialog.askstring(title, prompt, initialvalue=defaultResponse, parent=parent_widget)
        return result if result is not None else ""


class FileDialog:
    """Base class for file dialogs."""
    
    def __init__(self):
        self.FileName = ""
        self.FileNames = []
        self.Filter = ""
        self.FilterIndex = 1
        self.InitialDirectory = ""
        self.Title = ""
        self.DefaultExt = ""
        self.AddExtension = True
        self.CheckFileExists = True
        self.CheckPathExists = True
        self.RestoreDirectory = False
        self.ValidateNames = True
        self.ShowHelp = False
        
        # VB Events
        self.FileOk = lambda sender, e: None
        self.HelpRequest = lambda sender, hlpevent: None
        self.Disposed = lambda sender, e: None
    
    def _parse_filter(self):
        """Parse the Filter string into filetypes for Tkinter."""
        if not self.Filter:
            return [("All files", "*.*")]
        # Simple parsing: "Description|*.ext|Description2|*.ext2"
        parts = self.Filter.split('|')
        filetypes = []
        for i in range(0, len(parts), 2):
            if i+1 < len(parts):
                filetypes.append((parts[i], parts[i+1]))
        return filetypes
    
    def __del__(self):
        """Destructor to trigger Disposed event."""
        self.Disposed(self, None)


class OpenFileDialog(FileDialog):
    """Represents an OpenFileDialog."""
    
    def __init__(self):
        super().__init__()
        self.Multiselect = False
        self.ReadOnlyChecked = False
        self.ShowReadOnly = False
        self.SafeFileName = ""
    
    def ShowDialog(self):
        """Shows the dialog and returns the selected file."""
        from tkinter import filedialog
        if self.Multiselect:
            files = filedialog.askopenfilenames(
                initialdir=self.InitialDirectory or None,
                title=self.Title or None,
                filetypes=self._parse_filter(),
                defaultextension=self.DefaultExt if self.AddExtension else None
            )
            self.FileNames = list(files)
            self.FileName = self.FileNames[0] if self.FileNames else ""
            self.SafeFileName = os.path.basename(self.FileName) if self.FileName else ""
        else:
            self.FileName = filedialog.askopenfilename(
                initialdir=self.InitialDirectory or None,
                title=self.Title or None,
                filetypes=self._parse_filter(),
                defaultextension=self.DefaultExt if self.AddExtension else None
            )
            self.FileNames = [self.FileName] if self.FileName else []
            self.SafeFileName = os.path.basename(self.FileName) if self.FileName else ""
        
        # Trigger FileOk event
        self.FileOk(self, None)
        
        return self.FileName


class SaveFileDialog(FileDialog):
    """Represents a SaveFileDialog."""
    
    def __init__(self):
        super().__init__()
        self.OverwritePrompt = True
        self.CreatePrompt = False
    
    def ShowDialog(self):
        """Shows the dialog and returns the selected file."""
        from tkinter import filedialog
        self.FileName = filedialog.asksaveasfilename(
            initialdir=self.InitialDirectory or None,
            title=self.Title or None,
            filetypes=self._parse_filter(),
            defaultextension=self.DefaultExt if self.AddExtension else None
        )
        self.FileNames = [self.FileName] if self.FileName else []
        
        # Trigger FileOk event
        self.FileOk(self, None)
        
        return self.FileName


class PrintDialog:
    """Represents a PrintDialog with main VB.NET properties."""
    
    def __init__(self):
        self.Document = None  # The PrintDocument object to be printed
        self.PrinterSettings = None  # Selected printer settings
        self.AllowCurrentPage = False  # Enables "Current page" option
        self.AllowSelection = False  # Enables 'Selection' option
        self.AllowPrintToFile = False  # Shows 'Print to file' checkbox
        self.AllowSomePages = False  # Enables 'Pages' option
        self.ShowHelp = False  # Shows Help button
        self.ShowNetwork = False  # Allows access to network printers
        self.UseEXDialog = True  # Use modern dialog (default True)
        self.PrintToFile = False  # Set by user if 'Print to file' is checked
        self.PrinterName = ""  # Name of the selected printer
        self.Copies = 1
        self.FromPage = 1
        self.ToPage = 1
    
    def ShowDialog(self, owner=None):
        """Shows a simulated print dialog and returns the result."""
        dialog = tk.Toplevel()
        dialog.title("Print")
        dialog.geometry("450x350")
        dialog.resizable(False, False)
        
        # Handle owner for transient
        parent_window = None
        if owner:
            if hasattr(owner, '_tk_widget'):
                parent_window = owner._tk_widget
            elif hasattr(owner, 'winfo_toplevel'):
                parent_window = owner.winfo_toplevel()
            elif isinstance(owner, tk.Widget):
                parent_window = owner
        
        if parent_window:
            try:
                dialog.transient(parent_window)
            except tk.TclError:
                pass
            
        dialog.grab_set()
        
        # Result container
        result = {'status': DialogResult.Cancel}
        
        # --- Printer Section ---
        frame_printer = tk.LabelFrame(dialog, text="Printer", padx=10, pady=10)
        frame_printer.pack(fill='x', padx=10, pady=5)
        
        tk.Label(frame_printer, text="Name:").grid(row=0, column=0, sticky='w')
        
        # Simulated printers
        printers = ["Microsoft Print to PDF", "Microsoft XPS Document Writer", "Fax", "OneNote"]
        cbo_printer = ttk.Combobox(frame_printer, values=printers, state="readonly")
        cbo_printer.current(0)
        cbo_printer.grid(row=0, column=1, sticky='ew', padx=5)
        frame_printer.columnconfigure(1, weight=1)
        
        chk_print_to_file = tk.Checkbutton(frame_printer, text="Print to file")
        if self.AllowPrintToFile:
            chk_print_to_file.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        else:
            chk_print_to_file.config(state='disabled')
            
        # --- Page Range Section ---
        frame_range = tk.LabelFrame(dialog, text="Page range", padx=10, pady=10)
        frame_range.pack(fill='x', padx=10, pady=5)
        
        range_var = tk.IntVar(value=0) # 0=All, 1=Selection, 2=Current, 3=Pages
        
        tk.Radiobutton(frame_range, text="All", variable=range_var, value=0).grid(row=0, column=0, sticky='w')
        
        rb_selection = tk.Radiobutton(frame_range, text="Selection", variable=range_var, value=1)
        if not self.AllowSelection: rb_selection.config(state='disabled')
        rb_selection.grid(row=1, column=0, sticky='w')
        
        rb_current = tk.Radiobutton(frame_range, text="Current Page", variable=range_var, value=2)
        if not self.AllowCurrentPage: rb_current.config(state='disabled')
        rb_current.grid(row=2, column=0, sticky='w')
        
        frame_pages = tk.Frame(frame_range)
        frame_pages.grid(row=3, column=0, sticky='w', columnspan=2)
        
        rb_pages = tk.Radiobutton(frame_pages, text="Pages:", variable=range_var, value=3)
        if not self.AllowSomePages: rb_pages.config(state='disabled')
        rb_pages.pack(side='left')
        
        entry_pages = tk.Entry(frame_pages, width=10)
        if not self.AllowSomePages: entry_pages.config(state='disabled')
        entry_pages.pack(side='left', padx=5)
        
        # --- Copies Section ---
        frame_copies = tk.LabelFrame(dialog, text="Copies", padx=10, pady=10)
        frame_copies.pack(fill='x', padx=10, pady=5)
        
        tk.Label(frame_copies, text="Number of copies:").pack(side='left')
        spin_copies = tk.Spinbox(frame_copies, from_=1, to=99, width=5)
        spin_copies.pack(side='left', padx=5)
        
        # --- Buttons ---
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(fill='x', pady=10, padx=10)
        
        def on_ok():
            result['status'] = DialogResult.OK
            self.PrinterName = cbo_printer.get()
            # self.PrintToFile = ... (get var)
            try:
                self.Copies = int(spin_copies.get())
            except:
                self.Copies = 1
            dialog.destroy()
            
        def on_cancel():
            dialog.destroy()
            
        btn_cancel = tk.Button(btn_frame, text="Cancel", command=on_cancel)
        btn_cancel.pack(side='right', padx=5)
        btn_ok = tk.Button(btn_frame, text="Print", command=on_ok)
        btn_ok.pack(side='right', padx=5)
        
        dialog.wait_window()
        
        return result['status']


class ColorDialog:
    """Represents a common dialog box that displays available colors along with controls that enable the user to define custom colors."""

    def __init__(self):
        self.AllowFullOpen = True
        self.AnyColor = True
        self.Color = Color.Black  # Default black as Color object
        self.CustomColors = []
        self.FullOpen = False
        self.ShowHelp = False
        self.SolidColorOnly = False
        
        # VB Events
        self.HelpRequest = lambda sender, hlpevent: None
        self.Disposed = lambda sender, e: None

    def ShowDialog(self, owner=None):
        """Runs a common dialog box with a default owner."""
        from tkinter import colorchooser
        
        # Get initial color (support both Color object and string)
        initial_color = str(self.Color) if isinstance(self.Color, Color) else self.Color
        
        # Tkinter's askcolor returns ((r, g, b), '#rrggbb')
        # If cancelled, returns (None, None)
        result = colorchooser.askcolor(
            initialcolor=initial_color,
            title="Color"
        )
        
        if result[1]:
            # Create Color object - can use either RGB tuple or hex string
            # Prefer hex string for consistency, but RGB tuple also works now
            self.Color = Color(result[1])  # Hex string: '#rrggbb'
            # Alternative: self.Color = Color(result[0])  # RGB tuple: (r, g, b)
            return DialogResult.OK
        else:
            return DialogResult.Cancel

    def Reset(self):
        """Resets all options to their default values."""
        self.AllowFullOpen = True
        self.AnyColor = True
        self.Color = Color.Black
        self.CustomColors = []
        self.FullOpen = False
        self.ShowHelp = False
        self.SolidColorOnly = False


class FontDialog:
    """Represents a common dialog box that displays a list of fonts that are currently installed on the system."""

    def __init__(self):
        self.Font = Font.FromSystemFont()  # Default font as Font object
        self.Color = Color.Black  # Color as Color object
        self.MaxSize = 0
        self.MinSize = 0
        self.ShowApply = False
        self.ShowColor = False
        self.ShowEffects = True
        self.ShowHelp = False
        
        # VB Events
        self.Apply = lambda sender, e: None
        self.HelpRequest = lambda sender, hlpevent: None

    def ShowDialog(self, owner=None):
        """Shows the dialog and returns the result."""
        # Since Tkinter does not have a standard cross-platform FontDialog,
        # we implement a basic one using Toplevel and standard widgets.
        import tkinter.font as tkfont
        
        dialog = tk.Toplevel()
        dialog.title("Font")
        dialog.geometry("400x350")
        
        # Handle owner for transient
        parent_window = None
        if owner:
            if hasattr(owner, '_tk_widget'):
                parent_window = owner._tk_widget
            elif hasattr(owner, 'winfo_toplevel'):
                parent_window = owner.winfo_toplevel()
            elif isinstance(owner, tk.Widget):
                parent_window = owner
        
        if parent_window:
            try:
                dialog.transient(parent_window)
            except tk.TclError:
                pass # Ignore if parent is not valid
            
        dialog.grab_set()
        
        # Result container
        result = {'status': DialogResult.Cancel, 'font': self.Font}
        
        # Layout frames
        main_frame = tk.Frame(dialog, padx=10, pady=10)
        main_frame.pack(fill='both', expand=True)
        
        # Font Family
        lbl_family = tk.Label(main_frame, text="Font:")
        lbl_family.grid(row=0, column=0, sticky='w')
        
        list_family = tk.Listbox(main_frame, exportselection=False)
        list_family.grid(row=1, column=0, sticky='nsew')
        scrollbar_family = tk.Scrollbar(main_frame, orient="vertical", command=list_family.yview)
        scrollbar_family.grid(row=1, column=1, sticky='ns')
        list_family.config(yscrollcommand=scrollbar_family.set)
        
        families = sorted(tkfont.families())
        for f in families:
            list_family.insert(tk.END, f)
            
        # Font Style (Bold, Italic)
        lbl_style = tk.Label(main_frame, text="Font style:")
        lbl_style.grid(row=0, column=2, sticky='w', padx=(10, 0))
        
        list_style = tk.Listbox(main_frame, exportselection=False, width=15)
        list_style.grid(row=1, column=2, sticky='nsew', padx=(10, 0))
        styles = ["Regular", "Bold", "Italic", "Bold Italic"]
        for s in styles:
            list_style.insert(tk.END, s)
            
        # Size
        lbl_size = tk.Label(main_frame, text="Size:")
        lbl_size.grid(row=0, column=3, sticky='w', padx=(10, 0))
        
        list_size = tk.Listbox(main_frame, exportselection=False, width=10)
        list_size.grid(row=1, column=3, sticky='nsew', padx=(10, 0))
        sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]
        for s in sizes:
            list_size.insert(tk.END, str(s))

        # Preview - handle both Font object and tuple
        preview_font = self.Font.ToTuple() if isinstance(self.Font, Font) else self.Font
        lbl_preview = tk.Label(main_frame, text="AaBbYyZz", font=preview_font, relief="sunken", height=3)
        lbl_preview.grid(row=2, column=0, columnspan=4, sticky='ew', pady=(20, 0))
        
        # Selection Logic - handle both Font object and tuple
        if isinstance(self.Font, Font):
            current_family = self.Font.Name
            current_size = self.Font.Size
            current_style_flags = self.Font.Style
        elif isinstance(self.Font, tuple) and len(self.Font) > 0:
            current_family = self.Font[0]
            current_size = self.Font[1] if len(self.Font) > 1 else 9
            current_style = self.Font[2] if len(self.Font) > 2 else ""
            current_style_flags = FontStyle.Regular
        else:
            current_family = "Segoe UI"
            current_size = 9
            current_style_flags = FontStyle.Regular
            
        # Set initial selections
        try:
            idx = families.index(current_family)
            list_family.selection_set(idx)
            list_family.see(idx)
        except ValueError:
            pass
            
        try:
            # Approximate size match
            size_str = str(current_size)
            if size_str in [str(s) for s in sizes]:
                idx = [str(s) for s in sizes].index(size_str)
                list_size.selection_set(idx)
                list_size.see(idx)
        except ValueError:
            pass
            
        # Style mapping - handle FontStyle flags
        if isinstance(self.Font, Font):
            if (current_style_flags & FontStyle.Bold) and (current_style_flags & FontStyle.Italic):
                list_style.selection_set(3)
            elif current_style_flags & FontStyle.Bold:
                list_style.selection_set(1)
            elif current_style_flags & FontStyle.Italic:
                list_style.selection_set(2)
            else:
                list_style.selection_set(0)
        elif isinstance(self.Font, tuple) and len(self.Font) > 2:
            current_style = self.Font[2].lower()
            if "bold" in current_style and "italic" in current_style:
                list_style.selection_set(3)
            elif "bold" in current_style:
                list_style.selection_set(1)
            elif "italic" in current_style:
                list_style.selection_set(2)
            else:
                list_style.selection_set(0)
        else:
            list_style.selection_set(0)

        def update_preview(event=None):
            f = list_family.get(list_family.curselection()) if list_family.curselection() else current_family
            s = list_size.get(list_size.curselection()) if list_size.curselection() else current_size
            st_idx = list_style.curselection()
            st_text = list_style.get(st_idx) if st_idx else "Regular"
            
            tk_style = ""
            if "Bold" in st_text: tk_style += "bold "
            if "Italic" in st_text: tk_style += "italic"
            tk_style = tk_style.strip()
            
            new_font = (f, int(s), tk_style) if tk_style else (f, int(s))
            lbl_preview.config(font=new_font)
            return new_font

        list_family.bind('<<ListboxSelect>>', update_preview)
        list_size.bind('<<ListboxSelect>>', update_preview)
        list_style.bind('<<ListboxSelect>>', update_preview)

        # Buttons
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(fill='x', pady=10, padx=10)
        
        def on_ok():
            result['status'] = DialogResult.OK
            # Get selected values
            f = list_family.get(list_family.curselection()) if list_family.curselection() else current_family
            s = list_size.get(list_size.curselection()) if list_size.curselection() else current_size
            st_idx = list_style.curselection()
            st_text = list_style.get(st_idx) if st_idx else "Regular"
            
            # Convert to FontStyle flags
            font_style = FontStyle.Regular
            if "Bold" in st_text:
                font_style |= FontStyle.Bold
            if "Italic" in st_text:
                font_style |= FontStyle.Italic
            
            # Create Font object
            result['font'] = Font(f, int(s), font_style)
            dialog.destroy()
            
        def on_cancel():
            dialog.destroy()
            
        btn_cancel = tk.Button(btn_frame, text="Cancel", command=on_cancel)
        btn_cancel.pack(side='right', padx=5)
        btn_ok = tk.Button(btn_frame, text="OK", command=on_ok)
        btn_ok.pack(side='right', padx=5)
        
        dialog.wait_window()
        
        if result['status'] == DialogResult.OK:
            self.Font = result['font']
            
        return result['status']

    def Reset(self):
        """Resets all options to their default values."""
        self.Font = Font.FromSystemFont()
        self.Color = Color.Black
        self.MaxSize = 0
        self.MinSize = 0
        self.ShowApply = False
        self.ShowColor = False
        self.ShowEffects = True
        self.ShowHelp = False


class PageSetupDialog:
    """Represents a dialog box that allows the user to manipulate page settings, including margins and paper orientation."""

    def __init__(self):
        self.PageSettings = None
        self.PrinterSettings = None
        self.AllowMargins = True
        self.AllowOrientation = True
        self.AllowPaper = True
        self.AllowPrinter = True
        self.MinMargins = None
        self.ShowHelp = False
        self.ShowNetwork = False
        
        # Results
        self.Margins = (10, 10, 10, 10) # Left, Right, Top, Bottom
        self.Orientation = "Portrait"
        self.PaperSize = "A4"
        
    def ShowDialog(self, owner=None):
        """Shows the dialog and returns the result."""
        dialog = tk.Toplevel()
        dialog.title("Page Setup")
        dialog.geometry("400x350")
        dialog.resizable(False, False)
        
        # Handle owner for transient
        parent_window = None
        if owner:
            if hasattr(owner, '_tk_widget'):
                parent_window = owner._tk_widget
            elif hasattr(owner, 'winfo_toplevel'):
                parent_window = owner.winfo_toplevel()
            elif isinstance(owner, tk.Widget):
                parent_window = owner
        
        if parent_window:
            try:
                dialog.transient(parent_window)
            except tk.TclError:
                pass
            
        dialog.grab_set()
        
        result = {'status': DialogResult.Cancel}
        
        # --- Paper Section ---
        frame_paper = tk.LabelFrame(dialog, text="Paper", padx=10, pady=10)
        frame_paper.pack(fill='x', padx=10, pady=5)
        
        tk.Label(frame_paper, text="Size:").grid(row=0, column=0, sticky='w')
        cbo_size = ttk.Combobox(frame_paper, values=["Letter", "Legal", "A4", "A3", "Executive"], state="readonly")
        cbo_size.set(self.PaperSize)
        cbo_size.grid(row=0, column=1, sticky='ew', padx=5)
        if not self.AllowPaper: cbo_size.config(state='disabled')
        
        tk.Label(frame_paper, text="Source:").grid(row=1, column=0, sticky='w', pady=5)
        cbo_source = ttk.Combobox(frame_paper, values=["Automatically Select", "Tray 1", "Tray 2"], state="readonly")
        cbo_source.current(0)
        cbo_source.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        if not self.AllowPaper: cbo_source.config(state='disabled')
        
        frame_paper.columnconfigure(1, weight=1)
        
        # --- Orientation Section ---
        frame_orient = tk.LabelFrame(dialog, text="Orientation", padx=10, pady=10)
        frame_orient.pack(fill='x', padx=10, pady=5)
        
        orient_var = tk.StringVar(value=self.Orientation)
        
        rb_port = tk.Radiobutton(frame_orient, text="Portrait", variable=orient_var, value="Portrait")
        rb_port.pack(side='left', padx=10)
        
        rb_land = tk.Radiobutton(frame_orient, text="Landscape", variable=orient_var, value="Landscape")
        rb_land.pack(side='left', padx=10)
        
        if not self.AllowOrientation:
            rb_port.config(state='disabled')
            rb_land.config(state='disabled')
            
        # --- Margins Section ---
        frame_margins = tk.LabelFrame(dialog, text="Margins (mm)", padx=10, pady=10)
        frame_margins.pack(fill='x', padx=10, pady=5)
        
        tk.Label(frame_margins, text="Left:").grid(row=0, column=0)
        entry_left = tk.Entry(frame_margins, width=5)
        entry_left.insert(0, str(self.Margins[0]))
        entry_left.grid(row=0, column=1, padx=5)
        
        tk.Label(frame_margins, text="Right:").grid(row=0, column=2)
        entry_right = tk.Entry(frame_margins, width=5)
        entry_right.insert(0, str(self.Margins[1]))
        entry_right.grid(row=0, column=3, padx=5)
        
        tk.Label(frame_margins, text="Top:").grid(row=1, column=0, pady=5)
        entry_top = tk.Entry(frame_margins, width=5)
        entry_top.insert(0, str(self.Margins[2]))
        entry_top.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame_margins, text="Bottom:").grid(row=1, column=2, pady=5)
        entry_bottom = tk.Entry(frame_margins, width=5)
        entry_bottom.insert(0, str(self.Margins[3]))
        entry_bottom.grid(row=1, column=3, padx=5, pady=5)
        
        if not self.AllowMargins:
            for e in [entry_left, entry_right, entry_top, entry_bottom]:
                e.config(state='disabled')

        # --- Buttons ---
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(fill='x', pady=10, padx=10)
        
        def on_ok():
            result['status'] = DialogResult.OK
            self.PaperSize = cbo_size.get()
            self.Orientation = orient_var.get()
            try:
                self.Margins = (
                    int(entry_left.get()),
                    int(entry_right.get()),
                    int(entry_top.get()),
                    int(entry_bottom.get())
                )
            except:
                pass
            dialog.destroy()
            
        def on_cancel():
            dialog.destroy()
            
        btn_cancel = tk.Button(btn_frame, text="Cancel", command=on_cancel)
        btn_cancel.pack(side='right', padx=5)
        btn_ok = tk.Button(btn_frame, text="OK", command=on_ok)
        btn_ok.pack(side='right', padx=5)
        
        dialog.wait_window()
        
        return result['status']

    def Reset(self):
        """Resets all options to their default values."""
        self.PageSettings = None
        self.PrinterSettings = None
        self.AllowMargins = True
        self.AllowOrientation = True
        self.AllowPaper = True
        self.AllowPrinter = True
        self.Margins = (10, 10, 10, 10)
        self.Orientation = "Portrait"
        self.PaperSize = "A4"


class PrintPreviewDialog:
    """Represents a dialog box form that contains a PrintPreviewControl for printing."""

    def __init__(self):
        self.Document = None
        self.UseAntiAlias = False
        self.AutoZoom = True
        self.ShowHelp = False
        self.Zoom = 1.0
        
    def ShowDialog(self, owner=None):
        """Shows the dialog and returns the result."""
        dialog = tk.Toplevel()
        dialog.title("Print Preview")
        dialog.geometry("800x600")
        
        # Handle owner
        parent_window = None
        if owner:
            if hasattr(owner, '_tk_widget'):
                parent_window = owner._tk_widget
            elif hasattr(owner, 'winfo_toplevel'):
                parent_window = owner.winfo_toplevel()
            elif isinstance(owner, tk.Widget):
                parent_window = owner
        
        if parent_window:
            try:
                dialog.transient(parent_window)
            except tk.TclError:
                pass
            
        # Toolbar
        toolbar = tk.Frame(dialog, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        def do_print():
            # In a real implementation, this would trigger self.Document.Print()
            from tkinter import messagebox
            messagebox.showinfo("Print", "Sending document to printer...")
            dialog.destroy()
            
        btn_print = tk.Button(toolbar, text="Print", command=do_print)
        btn_print.pack(side=tk.LEFT, padx=2, pady=2)
        
        def zoom_in():
            self.Zoom += 0.25
            update_preview()
            
        def zoom_out():
            if self.Zoom > 0.25:
                self.Zoom -= 0.25
                update_preview()
                
        btn_zoom_in = tk.Button(toolbar, text="Zoom In (+)", command=zoom_in)
        btn_zoom_in.pack(side=tk.LEFT, padx=2, pady=2)
        
        btn_zoom_out = tk.Button(toolbar, text="Zoom Out (-)", command=zoom_out)
        btn_zoom_out.pack(side=tk.LEFT, padx=2, pady=2)
        
        btn_close = tk.Button(toolbar, text="Close", command=dialog.destroy)
        btn_close.pack(side=tk.RIGHT, padx=2, pady=2)
        
        # Preview Area
        container = tk.Frame(dialog, bg="darkgray")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scroll = tk.Scrollbar(container, orient=tk.VERTICAL)
        h_scroll = tk.Scrollbar(container, orient=tk.HORIZONTAL)
        
        canvas = tk.Canvas(container, bg="darkgray", 
                           yscrollcommand=v_scroll.set, 
                           xscrollcommand=h_scroll.set)
        
        v_scroll.config(command=canvas.yview)
        h_scroll.config(command=canvas.xview)
        
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        def update_preview():
            canvas.delete("all")
            
            # A4 size approx in pixels at 96 DPI: 794 x 1123
            base_w, base_h = 794, 1123
            
            w = int(base_w * self.Zoom)
            h = int(base_h * self.Zoom)
            
            # Center in canvas if smaller than canvas
            cw = canvas.winfo_width()
            ch = canvas.winfo_height()
            
            # Avoid division by zero if canvas is not yet mapped
            if cw <= 1: cw = 800
            if ch <= 1: ch = 600
            
            x = max(20, (cw - w) // 2)
            y = 20
            
            # Draw "Paper"
            canvas.create_rectangle(x, y, x+w, y+h, fill="white", outline="black", tags="paper")
            
            # Draw "Content" placeholder
            font_size = int(12 * self.Zoom)
            doc_name = "Document"
            if self.Document and hasattr(self.Document, 'DocumentName'):
                doc_name = self.Document.DocumentName
                
            canvas.create_text(x + w//2, y + h//2, text=f"{doc_name} Preview\n(Simulated)", 
                               font=("Segoe UI", font_size), justify=tk.CENTER)
            
            # Update scrollregion
            canvas.config(scrollregion=(0, 0, x + w + 20, y + h + 20))

        # Bind configure to center
        canvas.bind("<Configure>", lambda e: update_preview())
        
        # Initial draw
        dialog.update_idletasks()
        update_preview()
        
        dialog.wait_window()
        return DialogResult.OK




class ControlBase:
    """Base class for all WinFormPy controls."""
    
    def __init__(self, master_tk_widget, Left=0, Top=0):
        # The actual Tkinter widget (e.g., tk.Button, tk.Label)
        self._tk_widget = None 
        # Reference to the container widget (Form or UserControl)
        self.master = master_tk_widget 
        
        # VB-style position properties (Backing fields)
        self._left = Left
        self._top = Top
        self._width = None
        self._height = None
        
        # MousePointer property (mouse cursor)
        self.MousePointer = "arrow"
        
        # New VB properties
        self.Enabled = True
        self.BackColor = None
        self.BorderStyle = None  # e.g., 'flat', 'raised', 'sunken', 'ridge', 'groove'
        self.BackgroundImage = None
        self.Font = None
        self.FontColor = None
        self.ForeColor = None
        self.Tag = None
        self.BackgroundImageLayout = "Tile" # None, Tile, Center, Stretch, Zoom
        self.ContextMenuStrip = None
        self.AllowDrop = False
        
        # AutoSize properties
        self._autosize = False
        self._autosizemode = AutoSizeMode.GrowAndShrink  # Basic controls use GrowAndShrink
        self.MinimumSize = None  # (width, height) or None
        self.MaximumSize = None  # (width, height) or None
        self._original_size = None  # For AutoSizeMode.GrowOnly
        
        # Layout properties
        self._margin = (3, 3, 3, 3)  # Left, Top, Right, Bottom
        self._padding = (0, 0, 0, 0)  # Left, Top, Right, Bottom
        
        # Anchor and Dock properties
        self._anchor = [AnchorStyles.Top, AnchorStyles.Left]  # Default: Top, Left
        self._dock = DockStyle.None_  # None, Top, Bottom, Left, Right, Fill
        self._initial_distance = {}  # Stores initial distances to edges
        self._container_size = None  # Initial container size
        
        # ToolTip
        self._tooltip_text = ""
        self._tooltip_instance = None
        
        # Common VB events (callbacks)
        self.MouseDown = lambda button=None, x=None, y=None: None
        self.MouseUp = lambda button=None, x=None, y=None: None
        self.MouseEnter = lambda sender=None, e=None: None
        self.MouseLeave = lambda sender=None, e=None: None
        self.Enter = lambda sender=None, e=None: None  # GotFocus
        self.Leave = lambda sender=None, e=None: None  # LostFocus
        self.KeyDown = lambda sender=None, e=None: None
        self.Click = lambda sender=None, e=None: None
        self.DoubleClick = lambda sender=None, e=None: None
        self.Paint = lambda sender=None, e=None: None
        self.Resize = lambda sender=None, e=None: None
        self.KeyPress = lambda sender=None, e=None: None
        self.KeyUp = lambda sender=None, e=None: None
        
        # Reference to the original parent container (before resolving to Tkinter widget)
        self._parent_container = None
        
        # Flag to indicate control is still initializing (prevents premature notifications)
        self._initializing = True
    
    def _finish_initialization(self):
        """Marks the control as fully initialized.
        
        Should be called at the end of each control's __init__ after the widget
        is created and all properties are set. This enables parent notifications
        for property changes made after initialization.
        """
        self._initializing = False
    
    def _auto_register_with_parent(self):
        """Auto-registers this control with its parent container if possible.
        
        Finds the parent container stored in _parent_container and automatically
        adds itself to its Controls list. This allows for cleaner syntax:
        
        Before (manual):
            button = Button(panel, {...})
            panel.AddControl(button)
        
        Now (automatic):
            button = Button(panel, {...})  # Automatically added
        
        IMPORTANT: This method should be called AFTER the control is fully initialized (at the end of each specific control's __init__).
        """
        parent_container = getattr(self, '_parent_container', None)
        
        if parent_container is None:
            return
        
        # Check that the container has AddControl and Controls
        if not (hasattr(parent_container, 'AddControl') and hasattr(parent_container, 'Controls')):
            return
        
        # Check that it is not already registered (avoid duplicates)
        if self in parent_container.Controls:
            return
        
        # Auto-register using AddControl for correct configuration
        try:
            # Call AddControl which handles master, visibility, etc.
            parent_container.AddControl(self)
            
            # AddControl already does all the necessary work:
            # - Adds to Controls
            # - Configures master
            # - Registers wrapper
            # - Invokes ControlAdded
        except Exception:
            # If it fails, do not interrupt the creation of the control
            pass
        
        # Mark initialization as complete - this allows property setters to notify parent
        # This MUST be called after _auto_register_with_parent() to ensure all controls
        # properly complete their initialization phase
        self._finish_initialization()

    def BringToFront(self):
        """Moves the control to the front of the z-order."""
        if self._tk_widget:
            self._tk_widget.lift()
        
        if getattr(self, '_parent_container', None) and hasattr(self._parent_container, 'Controls'):
            try:
                if self in self._parent_container.Controls:
                    self._parent_container.Controls.remove(self)
                    self._parent_container.Controls.append(self)
            except ValueError:
                pass

    def SendToBack(self):
        """Moves the control to the back of the z-order."""
        if self._tk_widget:
            self._tk_widget.lower()
            
        if getattr(self, '_parent_container', None) and hasattr(self._parent_container, 'Controls'):
            try:
                if self in self._parent_container.Controls:
                    self._parent_container.Controls.remove(self)
                    self._parent_container.Controls.insert(0, self)
            except ValueError:
                pass

    def ZOrder(self, position=0):
        """Sets the Z-order of the control.
        
        Args:
            position (int): 0 to bring to front, 1 to send to back.
        """
        if position == 0:
            self.BringToFront()
        else:
            self.SendToBack()

    def _notify_parent_layout_changed(self):
        """Notifies the parent container that this control's layout has changed.
        
        This triggers the parent to recalculate its AutoSize if enabled.
        Prevents recursion by checking if parent is already applying AutoSize.
        """
        # Get the parent container wrapper
        parent = None
        if hasattr(self, 'master') and self.master:
            # Check if master has a _control_wrapper reference (Panel, GroupBox, etc.)
            if hasattr(self.master, '_control_wrapper'):
                parent = self.master._control_wrapper
        
        # If parent has AutoSize enabled, recalculate it
        if parent and hasattr(parent, 'AutoSize') and parent.AutoSize:
            # Prevent recursion: don't notify if parent is already applying AutoSize
            if getattr(parent, '_applying_autosize', False):
                return
                
            if hasattr(parent, '_apply_autosize_panel'):
                parent._apply_autosize_panel()
            elif hasattr(parent, '_apply_autosize'):
                parent._apply_autosize()

    @property
    def Left(self):
        return self._left

    @Left.setter
    def Left(self, value):
        self._left = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._place_control(self.Width, self.Height)
        # Notify parent only after initialization is complete
        if not getattr(self, '_initializing', False):
            self._notify_parent_layout_changed()

    @property
    def Top(self):
        return self._top

    @Top.setter
    def Top(self, value):
        self._top = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._place_control(self.Width, self.Height)
        # Notify parent only after initialization is complete
        if not getattr(self, '_initializing', False):
            self._notify_parent_layout_changed()

    @property
    def Width(self):
        return self._width

    @Width.setter
    def Width(self, value):
        self._width = value
        # Update _original_size when Width is set with AutoSize disabled
        if not self.AutoSize and self._height is not None:
            self._original_size = (value, self._height)
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._place_control(self.Width, self.Height)
        # Notify parent only after initialization is complete
        if not getattr(self, '_initializing', False):
            self._notify_parent_layout_changed()

    @property
    def Height(self):
        return self._height

    @Height.setter
    def Height(self, value):
        self._height = value
        # Update _original_size when Height is set with AutoSize disabled
        if not self.AutoSize and self._width is not None:
            self._original_size = (self._width, value)
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._place_control(self.Width, self.Height)
        # Notify parent only after initialization is complete
        if not getattr(self, '_initializing', False):
            self._notify_parent_layout_changed()

    @property
    def Location(self):
        return (self._left, self._top)

    @Location.setter
    def Location(self, value):
        if isinstance(value, (tuple, list)) and len(value) >= 2:
            self._left = value[0]
            self._top = value[1]
            if hasattr(self, '_tk_widget') and self._tk_widget:
                self._place_control(self.Width, self.Height)

    @property
    def Size(self):
        return (self._width, self._height)

    @Size.setter
    def Size(self, value):
        """Sets the size of the control. Updates both Width and Height properties.
        
        Args:
            value: Can be a tuple/list (width, height) or an object with Width and Height attributes
        """
        if isinstance(value, (tuple, list)) and len(value) >= 2:
            self._width = value[0]
            self._height = value[1]
            if hasattr(self, '_tk_widget') and self._tk_widget:
                self._place_control(self.Width, self.Height)
        elif hasattr(value, 'Width') and hasattr(value, 'Height'):
            self._width = value.Width
            self._height = value.Height
            if hasattr(self, '_tk_widget') and self._tk_widget:
                self._place_control(self.Width, self.Height)
        
    @property
    def AutoSize(self):
        """Gets or sets whether the control resizes automatically."""
        return self._autosize

    @AutoSize.setter
    def AutoSize(self, value):
        # Store current size before changing AutoSize state
        if not value and self._autosize and self._tk_widget:
            # Transitioning from True to False: save current size as fixed size
            try:
                self._tk_widget.update_idletasks()
                self._original_size = (self.Width, self.Height)
            except (tk.TclError, AttributeError):
                pass
        elif value and not self._autosize:
            # Transitioning from False to True: reset original size for GrowAndShrink controls
            if self.AutoSizeMode == AutoSizeMode.GrowAndShrink:
                self._original_size = None
        
        old_value = self._autosize
        self._autosize = value
        
        if value and self._tk_widget:
            # AutoSize enabled: apply automatic sizing immediately
            try:
                # Force widget update to ensure accurate measurements
                self._tk_widget.update_idletasks()
                
                # Apply autosize if the method exists
                if hasattr(self, '_apply_autosize'):
                    self._apply_autosize()
                
                # Reposition control with new size if visible
                if hasattr(self, 'Visible') and self.Visible and hasattr(self, '_place_control'):
                    if hasattr(self, 'Width') and hasattr(self, 'Height'):
                        self._place_control(self.Width, self.Height)
            except (tk.TclError, AttributeError):
                pass
        elif not value and self._original_size:
            # AutoSize disabled: restore fixed size from _original_size
            fixed_width, fixed_height = self._original_size
            self.Width = fixed_width
            self.Height = fixed_height
            try:
                if hasattr(self, 'Visible') and self.Visible and hasattr(self, '_place_control'):
                    self._place_control(fixed_width, fixed_height)
            except (tk.TclError, AttributeError):
                pass

    @property
    def AutoSizeMode(self):
        """Gets or sets the mode by which the control automatically resizes itself."""
        return self._autosizemode

    @AutoSizeMode.setter
    def AutoSizeMode(self, value):
        self._autosizemode = value
        if self.AutoSize:
            self._apply_autosize()

    @property
    def Margin(self):
        """Gets or sets the space between controls."""
        return self._margin

    @Margin.setter
    def Margin(self, value):
        if isinstance(value, int):
            self._margin = (value, value, value, value)
        elif isinstance(value, (tuple, list)) and len(value) == 4:
            self._margin = tuple(value)
        
        # Trigger layout update if parent is a layout container
        parent = self.get_Parent()
        if parent and hasattr(parent, '_apply_flow_layout'):
             parent._apply_flow_layout()
        elif parent and hasattr(parent, '_apply_layout'):
             parent._apply_layout()

    @property
    def Padding(self):
        """Gets or sets the internal padding of the control."""
        return self._padding

    @Padding.setter
    def Padding(self, value):
        if isinstance(value, int):
            self._padding = (value, value, value, value)
        elif isinstance(value, (tuple, list)) and len(value) == 4:
            self._padding = tuple(value)
        
        # Trigger autosize or repaint if supported
        if self.AutoSize:
            self._apply_autosize()


    @property
    def Font(self):
        """Gets or sets the font of the control."""
        return getattr(self, '_font', None)

    @Font.setter
    def Font(self, value):
        """Gets or sets the font of the control."""
        self._font = value
        if self._tk_widget:
            self._apply_visual_config()
            if self.AutoSize:
                self._apply_autosize()
                # If the control is visible, reposition
                if hasattr(self, 'Visible') and self.Visible and hasattr(self, '_place_control'):
                    if hasattr(self, 'Width') and hasattr(self, 'Height'):
                        self._place_control(self.Width, self.Height)

    @property
    def BackColor(self):
        """Gets or sets the background color of the control."""
        return self._backcolor

    @BackColor.setter
    def BackColor(self, value):
        """Sets the background color of the control."""
        self._backcolor = value
        if self._tk_widget:
            self._apply_visual_config()

    @property
    def ForeColor(self):
        """Gets or sets the text color of the control."""
        return self._forecolor

    @ForeColor.setter
    def ForeColor(self, value):
        """Sets the text color of the control."""
        self._forecolor = value
        if self._tk_widget:
            self._apply_visual_config()

    @property
    def Enabled(self):
        """Gets or sets whether the control is enabled."""
        return self._enabled

    @Enabled.setter
    def Enabled(self, value):
        """Sets whether the control is enabled."""
        self._enabled = value
        if self._tk_widget:
            self._apply_visual_config()

    @property
    def BorderStyle(self):
        """Gets or sets the border style of the control."""
        return self._borderstyle

    @BorderStyle.setter
    def BorderStyle(self, value):
        """Sets the border style of the control."""
        self._borderstyle = value
        if self._tk_widget:
            self._apply_visual_config()

    @property
    def Tag(self):
        """Gets or sets the object that contains data about the control."""
        return getattr(self, '_tag', None)

    @Tag.setter
    def Tag(self, value):
        self._tag = value

    def Invalidate(self):
        """Marks the control as invalid and requests repainting.
        
        This Windows Forms method marks the control or form as 
        invalid and adds a message to the user interface message 
        queue to be repainted when the system is free.
        It is more efficient as it allows the system to combine several 
        repaint requests.
        """
        if hasattr(self, '_tk_widget') and self._tk_widget:
            try:
                self._tk_widget.update_idletasks()
            except tk.TclError:
                pass

    def Update(self):
        """Forces the control to repaint.
        
        This Windows Forms method forces the control to repaint 
        its client area.
        """
        if hasattr(self, '_tk_widget') and self._tk_widget:
            try:
                self._tk_widget.update()
            except tk.TclError:
                pass

    def Refresh(self):
        """Forces an immediate repaint of the control.
        
        This Windows Forms method forces an immediate repaint 
        by calling Invalidate() and then Update(), which skips the 
        message queue and repaints the control immediately.
        It is equivalent to Invalidate() + Update() in Windows Forms.
        """
        if hasattr(self, '_tk_widget') and self._tk_widget:
            try:
                self._tk_widget.update_idletasks()
                self._tk_widget.update()
            except tk.TclError:
                pass

    def _place_control(self, width=None, height=None):
        """Uses the 'place' geometry manager to position the control."""
        if self._tk_widget:
            # Coordinates are always relative to master
            # If master is a _container (Frame inside GroupBox/Panel),
            # coordinates are already correct without adjustments
            x_coord = self.Left
            y_coord = self.Top
            
            # Initial positioning
            place_args = {
                'x': x_coord,
                'y': y_coord,
                'in_': self.master
            }
            if width is not None:
                place_args['width'] = width
            if height is not None:
                place_args['height'] = height
                
            try:
                # print(f"DEBUG: Placing {self.Name} at {x_coord},{y_coord} size {width}x{height} in {self.master}")
                self._tk_widget.place(**place_args)
            except tk.TclError:
                # Widget might be destroyed or invalid
                return
            
            # Bind resize events only once
            if not hasattr(self, '_anchor_dock_initialized'):
                self._anchor_dock_initialized = True
                # Wait for the window to be fully rendered
                self.master.after(100, self._initialize_anchor_dock)
            
            # Update scroll region if parent has AutoScroll enabled
            if hasattr(self.master, '_control_wrapper'):
                parent = self.master._control_wrapper
                if hasattr(parent, '_update_scroll_region') and getattr(parent, 'AutoScroll', False):
                    parent._update_scroll_region()
            
            # Set the cursor
            self._tk_widget.config(cursor=self.MousePointer)
            
            # Apply visual configuration
            self._apply_visual_config()
            
            # Force update to ensure visual changes are applied immediately
            self.Invalidate()

    def _bind_common_events(self):
        """Binds common events to the widget."""
        if self._tk_widget:
            self._tk_widget.bind('<Button-1>', self._on_click)
            self._tk_widget.bind('<ButtonPress>', self._on_mouse_down)
            self._tk_widget.bind('<ButtonRelease>', self._on_mouse_up)
            self._tk_widget.bind('<Enter>', self._on_mouse_enter)
            self._tk_widget.bind('<Leave>', self._on_mouse_leave)
            self._tk_widget.bind('<FocusIn>', self._on_enter)
            self._tk_widget.bind('<FocusOut>', self._on_leave)
            self._tk_widget.bind('<Key>', self._on_key_down)
            self._tk_widget.bind('<Double-Button-1>', self._on_double_click)
            self._tk_widget.bind('<Configure>', self._on_paint)
            self._tk_widget.bind('<KeyPress>', self._on_key_press)
            self._tk_widget.bind('<KeyRelease>', self._on_key_up)
            # Context Menu
            self._tk_widget.bind('<Button-3>', self._on_right_click)

    def _on_right_click(self, event):
        """Handler for Right Click (Context Menu)."""
        if self.ContextMenuStrip:
            # Pass the control itself as the source and relative position
            self.ContextMenuStrip.Show(self, Point(event.x, event.y))

    def _on_mouse_down(self, event):
        """Handler for MouseDown event."""
        self.MouseDown(event.num, event.x, event.y)

    def _on_mouse_up(self, event):
        """Handler for MouseUp event."""
        self.MouseUp(event.num, event.x, event.y)

    def _on_mouse_enter(self, event):
        """Handler for MouseEnter event."""
        self.MouseEnter()

    def _on_mouse_leave(self, event):
        """Handler for MouseLeave event."""
        self.MouseLeave()

    def _on_enter(self, event):
        """Handler for Enter (GotFocus) event."""
        self.Enter()

    def _on_leave(self, event):
        """Handler for Leave (LostFocus) event."""
        self.Leave()

    def _on_key_down(self, event):
        """Handler for KeyDown event."""
        self.KeyDown(event.keysym)

    def _on_click(self, event):
        """Handler for Click event."""
        self.Click()

    def _on_double_click(self, event):
        """Handler for DoubleClick event."""
        self.DoubleClick()

    def _on_paint(self, event):
        """Handler for Paint and Resize events."""
        self.Paint()
        self.Resize()

    def _on_key_press(self, event):
        """Handler for KeyPress event."""
        self.KeyPress(event.char)

    def _on_key_up(self, event):
        """Handler for KeyUp event."""
        self.KeyUp(event.keysym)

    def apply_css(self, css_string):
        """Applies CSS styles to the control using the winform-py_tools utility."""
        apply_css_to_widget(self._tk_widget, css_string)

    def get_Parent(self):
        """Gets the parent control (container) of this control.
        
        Returns:
            The parent control if it exists, None otherwise.
        """
        # Prefer the explicitly stored parent container
        if getattr(self, '_parent_container', None):
            return self._parent_container

        # Search for the parent control by traversing master until finding a control
        # that has the Controls list (Panel, Form, TabPage, etc.)
        parent = None
        current_master = self.master
        
        # Search the Tkinter widget hierarchy until a container is found
        while current_master is not None:
            # Check if there is a wrapper object containing this widget
            if hasattr(current_master, '_control_wrapper'):
                parent = current_master._control_wrapper
                break
            # Try to get the master of the current widget
            try:
                current_master = current_master.master
            except AttributeError:
                break
        
        return parent
    
    def set_Parent(self, new_parent):
        """Sets the parent control (container) of this control.
        
        Allows dynamically moving a control from one container to another.
        When changing the Parent:
        - The control is removed from the previous container
        - It is added to the new container
        - Left/Top coordinates remain relative to the new Parent
        
        Args:
            new_parent: The new container control (Form, Panel, GroupBox, TabPage, etc.)
        
        Example:
            # Move a button from one panel to another
            button.Parent = panel2
        """
        if self.get_Parent() == new_parent:
            return

        # Remove from current Parent if exists
        old_parent = self.get_Parent()
        if old_parent and hasattr(old_parent, 'Controls'):
            if self in old_parent.Controls:
                old_parent.Controls.remove(self)
        
        self._parent_container = new_parent

        if new_parent is None:
            if self._tk_widget:
                self._tk_widget.place_forget()
            return
        
        # Determine the Tkinter widget of the new parent
        if hasattr(new_parent, '_container'):
            # For Panel/GroupBox with _container
            new_master = new_parent._container
        elif hasattr(new_parent, '_frame'):
            # For TabPage with _frame
            new_master = new_parent._frame
        elif hasattr(new_parent, '_root'):
            # For Form with _root
            new_master = new_parent._root
        elif hasattr(new_parent, '_tk_widget'):
            # For other controls with _tk_widget
            new_master = new_parent._tk_widget
        else:
            new_master = new_parent
        
        # Update the master of this control
        self.master = new_master
        
        # Register the new parent as wrapper
        if not hasattr(new_master, '_control_wrapper'):
            new_master._control_wrapper = new_parent
        
        # Add to the new container
        if hasattr(new_parent, 'Controls'):
            if self not in new_parent.Controls:
                new_parent.Controls.append(self)
        
        # Reposition the control in the new container
        if self._tk_widget:
            self._place_control(self.Width, self.Height)
    
    @property
    def Parent(self):
        """Gets or sets the parent control (container) of this control.
        
        The Parent property is fundamental in the visual and logical hierarchy:
        - Determines relative coordinates (Left/Top are relative to Parent)
        - Affects visibility (a child is only visible if the Parent is visible)
        - Manages lifecycle (Parent cleans up its children when closed)
        
        Returns:
            The immediate container control (Form, Panel, GroupBox, etc.)
        
        Example:
            # Access the parent container
            parent_panel = button.Parent
            
            # Move to another container
            button.Parent = groupbox2
        """
        return self.get_Parent()
    
    @Parent.setter
    def Parent(self, value):
        """Sets the parent control via the property."""
        self.set_Parent(value)
    
    def FindForm(self):
        """Finds the top-level Form that contains this control.
        
        Unlike Parent, which only returns the immediate container,
        FindForm() traverses the entire hierarchy to find the root Form,
        regardless of how deeply nested the control is.
        
        Returns:
            The Form object that contains this control, or None if not in a Form.
        
        Example:
            # A button inside: Form -> Panel -> GroupBox -> Button
            button.Parent  # Returns GroupBox (immediate container)
            button.FindForm()  # Returns Form (root form)
            
            # Useful for closing the form from any control
            self.FindForm().Close()
        """
        # Start from the current control
        current = self
        
        # Go up the hierarchy until finding the Form
        while current is not None:
            # Check if it is a Form (has Show, _root, and does not inherit from ControlBase)
            if (hasattr(current, 'Show') and 
                hasattr(current, '_root') and 
                hasattr(current, 'Controls') and
                hasattr(current, 'ShowDialog')):  # Form-specific method
                return current
            
            # Continue going up the hierarchy
            if hasattr(current, 'get_Parent'):
                current = current.get_Parent()
            else:
                break
        
        return None
    
    @property
    def Visible(self):
        """Gets the effective visibility state of the control.
    
        A control is only visible if its Visible property is True
        and all its parent containers are also visible.
        """
        return self.get_Visible()

    @Visible.setter
    def Visible(self, value):
        """Sets the visibility state of the control."""
        self.set_Visible(value)

    def get_Visible(self):
        """Gets the effective visibility state of the control.
        
        Implements the Windows Forms visibility hierarchy:
        - A control is only visible if its own _visible property is True
        - And all its parent containers also have _visible = True
        
        Returns:
            True if the control and all its parents are visible, False otherwise.
        """
        # Check own _visible property
        if not getattr(self, '_visible', True):
            return False
        
        # Check visibility of all parents in the hierarchy
        parent = self.get_Parent()
        while parent is not None:
            if not getattr(parent, '_visible', True):
                return False
            # Go up to the next level in the hierarchy
            parent = parent.get_Parent() if hasattr(parent, 'get_Parent') else None
        
        return True

    def set_Visible(self, value):
        """Sets the visibility state of the control.
        
        Implements the Windows Forms visibility hierarchy:
        - Sets the _visible property of the control
        - If the control is a container (Panel, etc.), propagates the change to its children
        - Only physically shows or hides the widget if the effective visibility changes
        
        Args:
            value: True to make visible, False to hide
        """
        old_visible = getattr(self, '_visible', True)
        self._visible = value
        
        # Determine if the control should be physically shown or hidden
        # Only show if value is True AND all parents are also visible
        should_be_visible = value
        if value:
            # Check parent visibility
            parent = self.get_Parent()
            while parent is not None:
                if not getattr(parent, '_visible', True):
                    should_be_visible = False
                    break
                parent = parent.get_Parent() if hasattr(parent, 'get_Parent') else None
        
        # Apply physical visibility to the widget
        if hasattr(self, '_tk_widget') and self._tk_widget:
            if should_be_visible:
                # Show the control using place with its current position and size
                if hasattr(self, 'Width') and hasattr(self, 'Height'):
                    self._place_control(self.Width, self.Height)
                else:
                    self._tk_widget.place(x=self.Left, y=self.Top)
            elif not self._visible:
                # Hide the control only if explicitly hidden
                # If hidden due to parent, we keep it placed ("ubicar en su sitio")
                self._tk_widget.place_forget()
        
        # If it is a container with child controls, propagate the change
        if hasattr(self, 'Controls'):
            for control in self.Controls:
                if hasattr(control, '_visible'):
                    # Only update the physical visibility if the child has _visible = True
                    if control._visible:
                        if should_be_visible:
                            # The container becomes visible, show visible children
                            if hasattr(control, '_place_control'):
                                if hasattr(control, 'Width') and hasattr(control, 'Height'):
                                    control._place_control(control.Width, control.Height)
                                else:
                                    control._place_control()
                        # else:
                        #     # The container is hidden, hide all children
                        #     # NOT NECESSARY: Tkinter hides children automatically if parent is hidden
                        #     # And keeping them placed preserves layout state ("ubicar en su sitio")
                        #     pass
                    # If the child is propagating changes to its own children (e.g. Panel inside Panel)
                    if hasattr(control, 'set_Visible') and old_visible != value:
                        # Re-evaluate the child's visibility so it propagates to its children
                        control_visible = control._visible
                        control.set_Visible(control_visible)
    
    @property
    def ToolTipText(self):
        """Gets the tooltip text for the control."""
        return self._tooltip_text
    
    @ToolTipText.setter
    def ToolTipText(self, value):
        """Sets the tooltip text for the control."""
        self._tooltip_text = value
        # Create or update the tooltip
        if self._tk_widget:
            if value and value.strip():
                if self._tooltip_instance:
                    # Update existing text
                    self._tooltip_instance.update_text(value)
                else:
                    # Create new tooltip
                    self._tooltip_instance = ToolTip(self._tk_widget, value)
            else:
                # Remove tooltip if the text is empty
                if self._tooltip_instance:
                    self._tooltip_instance._hide_tooltip()
                    self._tooltip_instance = None
    
    def _initialize_anchor_dock(self):
        """Initializes Anchor or Dock after the container is ready."""
        if self._dock != DockStyle.None_:
            # Apply Dock
            self._apply_dock()
            # Bind resizing for Dock
            self.master.bind('<Configure>', self._on_dock_resize, add='+')
        elif self._anchor:
            # Calculate initial distances for Anchor
            self._calculate_initial_distances()
            # Bind resizing for Anchor
            self.master.bind('<Configure>', self._on_container_resize, add='+')
            # Also bind to the map event for when the window is shown
            self.master.bind('<Map>', lambda e: self._calculate_initial_distances(), add='+')
    
    def _calculate_initial_distances(self):
        """Calculates the initial distances of the control to the container edges."""
        self.master.update_idletasks()
        container_width = self.master.winfo_width()
        container_height = self.master.winfo_height()
        
        # If the container does not yet have a valid size, retry
        if container_width <= 1 or container_height <= 1:
            self.master.after(50, self._calculate_initial_distances)
            return

        # Check if container size matches Form size (if applicable) to avoid default 200x200
        if hasattr(self.master, '_control_wrapper'):
            form = self.master._control_wrapper
            if hasattr(form, 'Width') and hasattr(form, 'Height'):
                # If container is significantly smaller than Form (e.g. default 200 vs 600), wait.
                # We use a 80% threshold to account for window borders/decorations.
                # This ensures we don't calculate anchors based on a not-yet-resized window.
                if (container_width < form.Width * 0.8) or (container_height < form.Height * 0.8):
                     self.master.after(50, self._calculate_initial_distances)
                     return
        
        # Get the actual current position of the widget
        self._tk_widget.update_idletasks()
        
        # Calculate coordinates relative to self.master (the logical container)
        # This is necessary because the Tkinter widget may have a different parent (e.g. _root)
        # but be visually positioned inside self.master using place(in_=...)
        if self._tk_widget.master != self.master:
            try:
                actual_x = self._tk_widget.winfo_rootx() - self.master.winfo_rootx()
                actual_y = self._tk_widget.winfo_rooty() - self.master.winfo_rooty()
            except Exception:
                # Fallback if there is an error (e.g. widget not mapped)
                actual_x = self._tk_widget.winfo_x()
                actual_y = self._tk_widget.winfo_y()
        else:
            actual_x = self._tk_widget.winfo_x()
            actual_y = self._tk_widget.winfo_y()
            
        actual_width = self._tk_widget.winfo_width()
        actual_height = self._tk_widget.winfo_height()
        
        # If the widget has not yet been sized (width/height <= 1), try to use property values
        if actual_width <= 1:
            if self.Width is not None and self.Width > 1:
                actual_width = self.Width
            
        if actual_height <= 1:
            if self.Height is not None and self.Height > 1:
                actual_height = self.Height
            
        # Determine if we should wait (if size is still <= 1 and it wasn't explicitly set to be small)
        # We wait if actual dimension is <= 1 AND (property is None OR property > 1)
        # This allows explicit 1px controls to proceed, but waits for uninitialized ones
        wait_width = (actual_width <= 1) and (self.Width is None or self.Width > 1)
        wait_height = (actual_height <= 1) and (self.Height is None or self.Height > 1)
        
        if wait_width or wait_height:
             self.master.after(50, self._calculate_initial_distances)
             return
        
        # Use properties as source of truth for initial calculation
        # This avoids issues where Tkinter widgets report 0,0 or 1x1 before being fully mapped
        current_left = self.Left if self.Left is not None else actual_x
        current_top = self.Top if self.Top is not None else actual_y
        current_width = self.Width if self.Width is not None and self.Width > 0 else actual_width
        current_height = self.Height if self.Height is not None and self.Height > 0 else actual_height
        
        self._container_size = (container_width, container_height)
        self._initial_distance = {
            'left': current_left,
            'top': current_top,
            'right': container_width - (current_left + current_width),
            'bottom': container_height - (current_top + current_height)
        }
    
    def _on_container_resize(self, event=None):
        """Handles container resizing to apply Anchor."""
        if not self._tk_widget or self._dock != DockStyle.None_:
            return
        
        # Filter events: only process if the event is from the master or there is no event
        if event and hasattr(event, 'widget'):
            if event.widget != self.master and not self._is_ancestor(event.widget, self.master):
                return
        
        # DEBUG: Check for recursion
        # print(f"DEBUG: _on_container_resize {self} Anchor={self._anchor}")

        # Get new container size
        new_width = self.master.winfo_width()
        new_height = self.master.winfo_height()
        
        # Ignore events from containers without a valid size
        if new_width <= 1 or new_height <= 1:
            return
        
        # If there are no initial distances, calculate them
        if not self._initial_distance or not self._container_size:
            self._calculate_initial_distances()
            return
        
        # Apply Anchor
        new_left = self.Left
        new_top = self.Top
        new_width_ctrl = self.Width
        new_height_ctrl = self.Height
        
        # Anchor Left: keep left distance
        if AnchorStyles.Left in self._anchor:
            new_left = self._initial_distance['left']
        
        # Anchor Right: keep right distance
        if AnchorStyles.Right in self._anchor:
            if AnchorStyles.Left in self._anchor:
                # Anchored to both sides: stretch horizontally
                new_width_ctrl = new_width - self._initial_distance['left'] - self._initial_distance['right']
            else:
                # Only Right: move the control
                new_left = new_width - self._initial_distance['right'] - self.Width
        
        # Anchor Top: keep top distance
        if AnchorStyles.Top in self._anchor:
            new_top = self._initial_distance['top']
        
        # Anchor Bottom: keep bottom distance
        if AnchorStyles.Bottom in self._anchor:
            if AnchorStyles.Top in self._anchor:
                # Anchored top and bottom: stretch vertically
                new_height_ctrl = new_height - self._initial_distance['top'] - self._initial_distance['bottom']
            else:
                # Only Bottom: move the control
                new_top = new_height - self._initial_distance['bottom'] - self.Height
        
        # Update position and size
        try:
            # Check if values actually changed to avoid infinite loops
            if (self.Left != int(new_left) or 
                self.Top != int(new_top) or 
                self.Width != int(new_width_ctrl) or 
                self.Height != int(new_height_ctrl)):
                
                # Ensure dimensions are valid before applying
                if int(new_width_ctrl) <= 0 or int(new_height_ctrl) <= 0:
                    return

                self.Left = int(new_left)
                self.Top = int(new_top)
                self.Width = int(new_width_ctrl)
                self.Height = int(new_height_ctrl)
                
                # print(f"DEBUG: Resized {self.Name} to {self.Left},{self.Top} {self.Width}x{self.Height}")
                
                # Reposition with the new size
                self._tk_widget.place(x=self.Left, y=self.Top, width=self.Width, height=self.Height)
        except tk.TclError:
            return
        
        # Update container size
        self._container_size = (new_width, new_height)
    
    def _apply_dock(self):
        """Applies the Dock property to the control with Margin support.
        
        Full implementation of the Windows Forms Dock system:
        - Supports Top, Bottom, Left, Right, Fill
        - Respects margins (Margin)
        - Automatically adapts to container resizing
        - Can be applied at any time
        """
        if not self._tk_widget or self._dock == DockStyle.None_:
            return
        
        self._layout_container_dock()
    
    def _on_dock_resize(self, event=None):
        """Handles container resizing to apply Dock."""
        if not self._tk_widget or self._dock == DockStyle.None_:
            return
        
        # Filter events: only process if from master or if there is no event
        if event and hasattr(event, 'widget'):
            if event.widget != self.master and not self._is_ancestor(event.widget, self.master):
                return
        
        self._layout_container_dock()

    def _layout_container_dock(self):
        """Recalculates the layout of all docked controls in the same container."""
        container = self.master
        ControlBase._layout_docked_children(container)

    @staticmethod
    def _layout_docked_children(container):
        """Shared layout for all Dock controls in a container."""
        if container is None:
            return
        
        # Avoid recursion/overlaps
        if getattr(container, '_dock_layout_in_progress', False):
            return

        # Ensure valid geometry of the container
        if hasattr(container, 'update_idletasks'):
            try:
                container.update_idletasks()
            except tk.TclError:
                return
        try:
            container_width = container.winfo_width()
            container_height = container.winfo_height()
        except tk.TclError:
            return

        if container_width <= 1 or container_height <= 1:
            try:
                container.after(50, lambda: ControlBase._layout_docked_children(container))
            except Exception:
                pass
            return

        parent_wrapper = getattr(container, '_control_wrapper', None)
        if parent_wrapper and hasattr(parent_wrapper, 'Controls'):
            controls = [
                ctrl for ctrl in parent_wrapper.Controls
                if getattr(ctrl, '_dock', DockStyle.None_) != DockStyle.None_
                and (ctrl.get_Visible() if hasattr(ctrl, 'get_Visible') else getattr(ctrl, '_visible', True))
            ]
        else:
            controls = []

        if not controls:
            return

        container._dock_layout_in_progress = True
        try:
            left = 0
            top = 0
            right = container_width
            bottom = container_height

            ordered_controls = list(controls)
            # WinForms docking: Control at bottom of Z-order (first added) is docked first.
            # controls list is in creation order (first added at index 0).
            # So we should process in order.

            for ctrl in ordered_controls:
                dock = getattr(ctrl, '_dock', DockStyle.None_)
                if dock == DockStyle.None_ or not getattr(ctrl, '_tk_widget', None):
                    continue

                margin = getattr(ctrl, 'Margin', (0, 0, 0, 0))
                if not isinstance(margin, (tuple, list)) or len(margin) != 4:
                    margin = (0, 0, 0, 0)
                ml, mt, mr, mb = margin

                available_width = max(0, right - left)
                available_height = max(0, bottom - top)

                # Get current or required dimensions
                desired_width = ctrl._width if getattr(ctrl, '_width', None) else ctrl._tk_widget.winfo_reqwidth()
                desired_height = ctrl._height if getattr(ctrl, '_height', None) else ctrl._tk_widget.winfo_reqheight()

                if dock == DockStyle.Top:
                    w = max(0, available_width - (ml + mr))
                    h = max(0, min(desired_height, available_height - (mt + mb)) if available_height else desired_height)
                    x = left + ml
                    y = top + mt
                    top = y + h + mb
                elif dock == DockStyle.Bottom:
                    w = max(0, available_width - (ml + mr))
                    h = max(0, min(desired_height, available_height - (mt + mb)) if available_height else desired_height)
                    x = left + ml
                    y = bottom - h - mb
                    bottom = y - mt
                elif dock == DockStyle.Left:
                    w = max(0, min(desired_width, available_width - (ml + mr)) if available_width else desired_width)
                    h = max(0, available_height - (mt + mb))
                    x = left + ml
                    y = top + mt
                    left = x + w + mr
                elif dock == DockStyle.Right:
                    w = max(0, min(desired_width, available_width - (ml + mr)) if available_width else desired_width)
                    h = max(0, available_height - (mt + mb))
                    x = right - w - mr
                    y = top + mt
                    right = x - ml
                else:  # Fill
                    w = max(0, available_width - (ml + mr))
                    h = max(0, available_height - (mt + mb))
                    x = left + ml
                    y = top + mt

                # Ensure valid dimensions
                w = max(0, w)
                h = max(0, h)

                try:
                    ctrl._tk_widget.place(x=x, y=y, width=w, height=h)
                except tk.TclError:
                    continue

                # Update backing fields without triggering manual reposition
                ctrl._left = x
                ctrl._top = y
                ctrl._width = w
                ctrl._height = h
                ctrl._container_size = (container_width, container_height)

                if getattr(ctrl, '_anchor', None):
                    ctrl._initial_distance = {
                        'left': x,
                        'top': y,
                        'right': container_width - (x + w),
                        'bottom': container_height - (y + h)
                    }

            # Restore original z-order by lifting in Controls order
            for ctrl in controls:
                if getattr(ctrl, '_tk_widget', None):
                    try:
                        ctrl._tk_widget.lift()
                    except tk.TclError:
                        pass
        finally:
            container._dock_layout_in_progress = False
    
    def _is_ancestor(self, widget, potential_ancestor):
        """Checks if widget is an ancestor of potential_ancestor."""
        try:
            current = potential_ancestor
            while current:
                if current == widget:
                    return True
                current = current.master if hasattr(current, 'master') else None
            return False
        except Exception:
            return False
    
    @property
    def Anchor(self):
        """Gets the anchor configuration of the control.
        
        Returns:
            List of AnchorStyles with the anchored edges.
        """
        return self._anchor.copy()
    
    @Anchor.setter
    def Anchor(self, value):
        """Sets the anchor configuration of the control.
        
        Args:
            value: List of AnchorStyles, AnchorStyles flag, or list of strings (legacy).
        """
        # Clear Dock if Anchor is set
        if self._dock != DockStyle.None_:
            self._dock = DockStyle.None_
            if hasattr(self, '_dock_resize_bound'):
                delattr(self, '_dock_resize_bound')
        
        # Handle legacy string input
        if isinstance(value, str):
            value = [v.strip() for v in value.split(',')]
        
        # Convert strings to Enums if necessary
        if isinstance(value, list):
            new_value = []
            for v in value:
                if isinstance(v, str):
                    try:
                        new_value.append(AnchorStyles[v])
                    except KeyError:
                        pass
                elif isinstance(v, AnchorStyles):
                    new_value.append(v)
            value = new_value
        elif isinstance(value, int): # IntFlag
             value = [flag for flag in AnchorStyles if flag in AnchorStyles(value) and flag != AnchorStyles.None_]
        
        self._anchor = value
        
        # Recalculate initial distances
        if hasattr(self, 'Width') and hasattr(self, 'Height'):
            self._calculate_initial_distances()
    
    @property
    def Dock(self):
        """Gets the dock configuration of the control.

        Returns:
            DockStyle enum.
        """
        return self._dock
    
    @Dock.setter
    def Dock(self, value):
        """Sets the control's dock configuration.

        Args:
            value: DockStyle enum or string (legacy).
        """
        # Handle legacy string input
        if isinstance(value, str):
            try:
                value = DockStyle[value]
            except KeyError:
                return # Invalid value
        
        # Clear Anchor if Dock is set
        if value != DockStyle.None_:
            self._anchor = []
            self._initial_distance = {}
        
        old_dock = self._dock
        self._dock = value
        
        # If it changes from None to something, or changes value, apply
        if self._tk_widget:
            if value != DockStyle.None_:
                # Register the resize binding if it does not exist
                if not hasattr(self, '_dock_resize_bound'):
                    # print(f"DEBUG: Binding <Configure> for {self.Name} on {self.master}")
                    self.master.bind('<Configure>', self._on_dock_resize, add='+')
                    self._dock_resize_bound = True
                # Apply dock immediately
                self._apply_dock()
            else:
                # If set to None, return to free positioning
                if old_dock != DockStyle.None_:
                    if not self._anchor:
                        # Restore default Anchor (Top, Left) as in WinForms
                        self._anchor = [AnchorStyles.Top, AnchorStyles.Left]
                    # Recalculate distances for Anchor in the new container
                    self.master.after(0, self._calculate_initial_distances)
                    self._place_control(self.Width, self.Height)
            # Readjust all Dock controls in the container
            self._layout_container_dock()

    @property
    def FlowBreak(self):
        """Gets or sets a value indicating whether a flow break occurs after this control."""
        return getattr(self, '_flow_break', False)

    @FlowBreak.setter
    def FlowBreak(self, value):
        """Sets the FlowBreak property."""
        self._flow_break = bool(value)
        # If the parent is a FlowLayoutPanel, trigger layout update
        if hasattr(self, 'master') and hasattr(self.master, '_apply_flow_layout'):
             # We need to find the FlowLayoutPanel instance wrapper, not just the tk widget
             # But usually _apply_flow_layout is on the wrapper.
             # The master of the tk widget is the inner container of the FlowLayoutPanel?
             # Or the FlowLayoutPanel itself?
             # In FlowLayoutPanel implementation: super().__init__(master_form, defaults) -> Panel -> ControlBase
             # Panel creates self._container.
             # Controls are added to self._container.
             # So self.master is self._container.
             # self._container.master is self._tk_widget (LabelFrame/Frame).
             # self._tk_widget.master is the parent of FlowLayoutPanel.
             # We need to reach the FlowLayoutPanel instance.
             # ControlBase stores self._parent_container?
             pass
        
        # Try to update layout if parent is FlowLayoutPanel
        if hasattr(self, '_parent_container') and hasattr(self._parent_container, '_apply_flow_layout'):
            self._parent_container._apply_flow_layout()
    
    def _apply_autosize(self):
        """Applies automatic resizing based on content.
        
        Standard AutoSize sequence for all controls:
        1. Verify AutoSize is enabled
        2. Force geometry update (update_idletasks)
        3. Get required size from widget
        4. Apply AutoSizeMode (GrowOnly vs GrowAndShrink)
        5. Apply MinimumSize/MaximumSize restrictions
        6. Adjust position if anchored Right/Bottom
        7. Update Width/Height properties
        8. Reposition/resize visually (always, visible or not)
        9. Notify parent container
        
        Should be overridden by specific controls that need
        custom AutoSize behavior.
        """
        if not self.AutoSize or not self._tk_widget:
            return
        
        # 1. Force widget update to get correct dimensions
        self._tk_widget.update_idletasks()
        
        # 2. Get required size from widget
        required_width = self._tk_widget.winfo_reqwidth()
        required_height = self._tk_widget.winfo_reqheight()
        
        # 3. Apply AutoSizeMode logic
        if self.AutoSizeMode == AutoSizeMode.GrowOnly and self._original_size:
            orig_w, orig_h = self._original_size
            required_width = max(required_width, orig_w)
            required_height = max(required_height, orig_h)
        
        # 4. Apply MinimumSize restrictions
        if self.MinimumSize:
            min_width, min_height = self.MinimumSize
            required_width = max(required_width, min_width)
            required_height = max(required_height, min_height)
        
        # 5. Apply MaximumSize restrictions
        if self.MaximumSize:
            max_width, max_height = self.MaximumSize
            if max_width > 0:
                required_width = min(required_width, max_width)
            if max_height > 0:
                required_height = min(required_height, max_height)
        
        # 6. Adjust position if Anchored to Right/Bottom
        self._apply_autosize_anchor_adjustment(required_width, required_height)

        # 7. Update dimensions
        self.Width = required_width
        self.Height = required_height
        
        # 8. Reposition with the new size (always, visible or not)
        if hasattr(self, '_place_control'):
            self._place_control(required_width, required_height)
        
        # 9. Notify parent container that this control's size changed
        self._notify_parent_layout_changed()

    def _apply_autosize_anchor_adjustment(self, required_width, required_height):
        """Adjusts Left/Top if anchored Right/Bottom during AutoSize."""
        if not hasattr(self, '_anchor'): return
        
        # If anchored Right (and not Left), grow to the left
        if AnchorStyles.Right in self._anchor and AnchorStyles.Left not in self._anchor:
            current_width = self.Width if self.Width is not None else required_width
            delta_w = required_width - current_width
            if delta_w != 0:
                self.Left -= delta_w
                
        # If anchored Bottom (and not Top), grow to the top
        if AnchorStyles.Bottom in self._anchor and AnchorStyles.Top not in self._anchor:
            current_height = self.Height if self.Height is not None else required_height
            delta_h = required_height - current_height
            if delta_h != 0:
                self.Top -= delta_h

    @property
    def Cursor(self):
        """Gets or sets the cursor that is displayed when the mouse pointer is over the control."""
        return self.MousePointer

    @Cursor.setter
    def Cursor(self, value):
        self.MousePointer = value
        if self._tk_widget:
            self._tk_widget.config(cursor=value)

    def PointToClient(self, point):
        """Computes the location of the specified screen point into client coordinates."""
        if not self._tk_widget:
            return point
        screen_x, screen_y = point
        client_x = screen_x - self._tk_widget.winfo_rootx()
        client_y = screen_y - self._tk_widget.winfo_rooty()
        return (client_x, client_y)

    def PointToScreen(self, point):
        """Computes the location of the specified client point into screen coordinates."""
        if not self._tk_widget:
            return point
        client_x, client_y = point
        screen_x = client_x + self._tk_widget.winfo_rootx()
        screen_y = client_y + self._tk_widget.winfo_rooty()
        return (screen_x, screen_y)
        
    def RectangleToClient(self, rect):
        """Computes the size and location of the specified screen rectangle in client coordinates."""
        x, y, w, h = rect.X, rect.Y, rect.Width, rect.Height
        client_pt = self.PointToClient((x, y))
        return Rectangle(client_pt[0], client_pt[1], w, h)
        
    def RectangleToScreen(self, rect):
        """Computes the size and location of the specified client rectangle in screen coordinates."""
        x, y, w, h = rect.X, rect.Y, rect.Width, rect.Height
        screen_pt = self.PointToScreen((x, y))
        return Rectangle(screen_pt[0], screen_pt[1], w, h)

    def GetChildAtPoint(self, point):
        """Retrieves the child control that is located at the specified coordinates."""
        if not hasattr(self, 'Controls'):
            return None
        
        x, y = point
        # Simple hit testing
        for control in self.Controls:
            if (control.Left <= x < control.Left + control.Width and
                control.Top <= y < control.Top + control.Height):
                return control
        return None

    def Contains(self, control):
        """Retrieves a value indicating whether the specified control is a child of the control."""
        if not hasattr(self, 'Controls'):
            return False
        return control in self.Controls

    def Focus(self):
        """Sets input focus to the control."""
        if self._tk_widget:
            self._tk_widget.focus_set()

    def Select(self):
        """Activates the control."""
        self.Focus()

    def _apply_visual_config(self):
        """Applies common visual configuration to all controls.
        
        This method sets basic visual properties such as colors,
        font, enabled state, etc. Can be overridden by specific controls
        that need additional configurations.
        """
        if not self._tk_widget:
            return
        
        config = {}
        
        # Apply colors
        if self.BackColor is not None:
            config['bg'] = self.BackColor
        if self.ForeColor is not None:
            config['fg'] = self.ForeColor
        
        # Apply font
        if self.Font is not None:
            config['font'] = self.Font
        
        # Apply enabled/disabled state
        if not self.Enabled:
            config['state'] = 'disabled'
        else:
            config['state'] = 'normal'
        
        # Apply border/relief
        if self.BorderStyle is not None:
            relief_map = {
                'None': 'flat', 'Fixed3D': 'groove', 'FixedSingle': 'solid',
                'fixed_single': 'solid', 'fixed_3d': 'groove',
                'flat': 'flat', 'groove': 'groove', 'raised': 'raised',
                'ridge': 'ridge', 'solid': 'solid', 'sunken': 'sunken',
                BorderStyle.None_: 'flat', BorderStyle.Fixed3D: 'groove', BorderStyle.FixedSingle: 'solid',
                0: 'flat', 1: 'solid', 2: 'groove'  # Integer BorderStyle values
            }
            config['relief'] = relief_map.get(self.BorderStyle, 'flat')
            
            # Set borderwidth
            if self.BorderStyle in ['FixedSingle', 'solid', 'fixed_single', BorderStyle.FixedSingle, 1]:
                config['borderwidth'] = 3  # Increased for better visibility
            elif self.BorderStyle in ['Fixed3D', 'ridge', 'groove', 'sunken', 'raised', 'fixed_3d', BorderStyle.Fixed3D, 2]:
                config['borderwidth'] = 3  # Increased for better visibility
            else:
                config['borderwidth'] = 0
        
        # Apply background image
        if self.BackgroundImage is not None:
            config['image'] = self.BackgroundImage
        
        # Apply configuration to widget
        if config:
            try:
                self._tk_widget.config(**config)
            except tk.TclError:
                # Some widgets do not support all options
                # Try to apply options one by one
                for key, value in config.items():
                    try:
                        self._tk_widget.config(**{key: value})
                    except tk.TclError:
                        pass  # Ignore unsupported options
    
    def Invalidate(self):
        """Marks the control as invalid and requests repaint.
        
        This Windows Forms method marks the control as invalid and
        adds a message to the UI message queue
        so it repaints when the system is free.
        It is more efficient as it allows the system to combine multiple
        repaint requests.
        """
        if self._tk_widget:
            try:
                self._tk_widget.update_idletasks()
            except tk.TclError:
                pass
    
    def Refresh(self):
        """Forces an immediate repaint of the control.
        
        This Windows Forms method forces an immediate repaint
        by calling Invalidate() and then Update(), which skips the
        message queue and repaints the control immediately.
        It is equivalent to Invalidate() + Update() in Windows Forms.
        """
        if self._tk_widget:
            try:
                # Invalidate() - marks as invalid and adds to queue
                self._tk_widget.update_idletasks()
                # Update() - processes the queue immediately
                self._tk_widget.update()
            except tk.TclError:
                pass


############# Classes for User Controls & ScrollBars #############

class ScrollBar(ControlBase):
    """Represents a ScrollBar (standalone scrollbar)."""
    
    def __init__(self, master_form, props=None):
        """Initializes a ScrollBar.

        Args:
            master_form: The parent form or container
            props: Optional dictionary with initial properties
        """
        defaults = {
            'Left': 0, 'Top': 0, 'Width': 200, 'Height': 20,
            'Minimum': 0, 'Maximum': 100, 'Value': 0,
            'SmallChange': 1, 'LargeChange': 10,
            'Orientation': Orientation.Horizontal,  # 'horizontal' or 'vertical'
            'Visible': True, 'Enabled': True, 'Name': '',
            'BackColor': None, 'ForeColor': None,
            'Font': None, 'AutoSize': False,
            'BorderStyle': BorderStyle.None_, 'UseSystemStyles': True
        }
        
        if props:
            defaults.update(props)
        
        # Configure system colors and styles
        if defaults.get('UseSystemStyles', True):
            SystemStyles.ApplyToDefaults(defaults, control_type="ScrollBar")
        
        # Resolve the Tkinter widget and store the parent container
        master_widget, parent_container = _resolve_master_widget(master_form)
        
        # Initialize ControlBase with position
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Save the parent container for auto-registration
        self._parent_container = parent_container
        
        self.Name = defaults['Name']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Minimum = defaults['Minimum']
        self.Maximum = defaults['Maximum']
        self.Value = defaults['Value']
        self.SmallChange = defaults['SmallChange']
        self.LargeChange = defaults['LargeChange']
        self.Orientation = defaults['Orientation']
        self.Visible = defaults['Visible']
        self.Enabled = defaults['Enabled']
        self.BackColor = defaults['BackColor']
        self.ForeColor = defaults['ForeColor']
        self.Font = defaults['Font']
        self.AutoSize = defaults['AutoSize']
        self.BorderStyle = defaults['BorderStyle']
        self.UseSystemStyles = defaults['UseSystemStyles']
        
        # Scroll event
        self.Scroll = None
        
        # Create the widget
        self._create_widget()
        
        # Apply initial properties
        self._apply_properties()
        
        # Auto-register with the parent container
        self._auto_register_with_parent()
    
    def _create_widget(self):
        """Create the underlying Tkinter widget."""
        # Use tk.Scale to implement ScrollBar
        orient = tk.HORIZONTAL if self.Orientation == Orientation.Horizontal else tk.VERTICAL
        self._tk_widget = tk.Scale(
            self.master,
            from_=self.Minimum,
            to=self.Maximum,
            orient=orient,
            resolution=self.SmallChange,
            showvalue=False,  # Do not display the numeric value
            command=self._on_scroll
        )
        
        # Set initial value
        self._tk_widget.set(self.Value)
        
        # Configure colors
        if self.BackColor:
            self._tk_widget.config(bg=self.BackColor)
        if self.ForeColor:
            self._tk_widget.config(fg=self.ForeColor)
        
        # Configure size
        self._place_control(self.Width, self.Height)
    
    def _on_scroll(self, value):
        """Handler for the scroll event."""
        if self.Scroll:
            self.Scroll()
    
    def _apply_properties(self):
        """Apply properties to the widget."""
        pass
    
    @property
    def Value(self):
        """Property getter for Value."""
        if hasattr(self, '_tk_widget') and self._tk_widget:
            return self._tk_widget.get()
        return self._value
    
    @Value.setter
    def Value(self, value):
        """Property setter for Value."""
        self._value = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._tk_widget.set(value)


class HScrollBar(ScrollBar):
    """Represents an HScrollBar (horizontal scrollbar)."""
    
    def __init__(self, master_form, props=None):
        """Initializes an HScrollBar."""
        if props is None:
            props = {}
        props['Orientation'] = Orientation.Horizontal
        super().__init__(master_form, props)


class VScrollBar(ScrollBar):
    """Represents a VScrollBar (vertical scrollbar)."""
    
    def __init__(self, master_form, props=None):
        """Initializes a VScrollBar."""
        if props is None:
            props = {}
        props['Orientation'] = Orientation.Vertical
        super().__init__(master_form, props)


class UserControl(ControlBase, ScrollableControlMixin):
    """Represents an empty user control used to create custom controls.

    Equivalent to System.Windows.Forms.UserControl.
    Provides an empty container with support for AutoScroll.
    """
    
    def __init__(self, parent=None, props=None):
        """Initializes a UserControl.

        Args:
            parent: The parent control (Form, Panel, etc.)
            props: Optional dictionary with initial properties
        """
        # Default values
        defaults = {
            'Left': 0,
            'Top': 0,
            'Width': 150,
            'Height': 150,
            'Name': 'UserControl1',
            'Text': '',
            'Enabled': True,
            'Visible': True,
            'BackColor': 'System.Control',
            'ForeColor': None,
            'BackgroundImage': None,
            'BorderStyle': BorderStyle.None_,
            'AutoScroll': False,
            'AutoScrollMinSize': None,
            'AutoScrollPosition': (0, 0),
            'AutoScrollMargin': (0, 0),
            'Dock': None,
            'Padding': (0, 0),
            'AutoSize': False,
            'AutoSizeMode': AutoSizeMode.GrowOnly,
            'MinimumSize': None,
            'MaximumSize': None
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Control", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Control")
            
        # Resolve the Tkinter widget and store the parent container
        master_widget, parent_container = _resolve_master_widget(parent)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Store the parent container for auto-registration
        self._parent_container = parent_container
        
        self.Name = defaults['Name']
        self._text = defaults['Text']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.BackColor = defaults['BackColor']
        self.ForeColor = defaults['ForeColor']
        self.BackgroundImage = defaults['BackgroundImage']
        self.BorderStyle = defaults['BorderStyle']
        
        # Initialize scroll properties using the Mixin
        self._init_scroll_properties(defaults)
        
        self.Dock = defaults['Dock']
        if 'Anchor' in defaults and defaults['Anchor'] is not None:
            self.Anchor = defaults['Anchor']
        if 'Margin' in defaults:
            self.Margin = defaults['Margin']
            
        self._padding = defaults['Padding']
        self.AutoSize = defaults['AutoSize']
        self.AutoSizeMode = defaults['AutoSizeMode']
        self.MinimumSize = defaults['MinimumSize']
        self.MaximumSize = defaults['MaximumSize']
        
        # Initialize _original_size for AutoSizeMode.GrowOnly
        self._original_size = (0, 0)
        self._initial_size = (defaults['Width'], defaults['Height'])
        
        self.Location = (self.Left, self.Top)
        
        # Create the Tkinter widget (Frame)
        padding = self.Padding
        if len(padding) == 4:
            pad_left, pad_top, pad_right, pad_bottom = padding
            padx = (pad_left + pad_right) // 2
            pady = (pad_top + pad_bottom) // 2
        else:
            padx, pady = padding
        
        # Mapear BorderStyle
        relief_map = {
            BorderStyle.None_: 'flat',
            BorderStyle.Fixed3D: 'ridge',
            BorderStyle.FixedSingle: 'solid'
        }
        
        config = {
            'width': self.Width,
            'height': self.Height,
            'bg': self.BackColor,
            'relief': relief_map.get(self.BorderStyle, 'flat'),
            'padx': padx,
            'pady': pady
        }
        
        if self.BorderStyle == BorderStyle.FixedSingle:
            config['borderwidth'] = 1
        elif self.BorderStyle == BorderStyle.Fixed3D:
            config['borderwidth'] = 2
        else:
            config['borderwidth'] = 0
            
        self._tk_widget = tk.Frame(self.master, **config)
        
        # Ensure the frame does not shrink
        self._tk_widget.pack_propagate(False)
        self._tk_widget.grid_propagate(False)
        
        # Configure scroll infrastructure using the Mixin
        self._setup_scroll_infrastructure(self._tk_widget, self.BackColor)
        
        # Initialize Controls collection
        self.Controls = []
        
        # Add _root for container functionality
        if hasattr(parent, 'FindForm'):
            form = parent.FindForm()
            if form:
                self._root = form._root
        elif hasattr(parent, '_root'):
            self._root = parent._root
        elif hasattr(parent, 'master_form') and hasattr(parent.master_form, '_root'):
            self._root = parent.master_form._root
        else:
             self._root = None

        if self.Visible:
            self._place_control(self.Width, self.Height)
        else:
            self._tk_widget.place_forget()
            
        # Events
        self.Load = lambda: None
        self.ControlAdded = lambda control: None
        self.ControlRemoved = lambda control: None
        self.Paint = lambda: None
        self.Resize = lambda: None
        
        self._tk_widget.bind('<Configure>', self._on_paint)
        
        # Auto-registration: Use centralized method from ControlBase
        self._auto_register_with_parent()
                
    def AddControl(self, control):
        """Adds a control to the UserControl."""
        # Avoid duplicates
        if control in self.Controls:
            return
        
        self.Controls.append(control)
        
        # Configure the control's container (use _container if AutoScroll is present)
        control.master = self._container if hasattr(self, '_container') else self._tk_widget
        
        # Register this UserControl as the container wrapper
        if not hasattr(control.master, '_control_wrapper'):
            control.master._control_wrapper = self
        
        # Reposition the control in the new container
        control._place_control()
        
        # Inherit properties from the container
        if hasattr(control, 'Enabled'):
            control.Enabled = self.Enabled
            if hasattr(control, '_tk_widget'):
                try:
                    control._tk_widget.config(state='normal' if self.Enabled else 'disabled')
                except tk.TclError:
                    pass
        
        # Apply visibility hierarchy
        if hasattr(control, '_visible'):
            control_should_be_visible = control._visible and self.get_Visible()
            if control_should_be_visible:
                control._place_control()
            else:
                if hasattr(control, '_tk_widget') and control._tk_widget:
                    control._tk_widget.place_forget()
        else:
            if self.get_Visible():
                control._place_control()
        
        # Update scroll region if AutoScroll is enabled
        if self.AutoScroll:
            self._update_scroll_region()
        
        # Apply AutoSize if enabled
        if self.AutoSize:
            self._apply_autosize()
        
        self.ControlAdded(control)

    def RemoveControl(self, control):
        """Removes a control from the UserControl."""
        if control in self.Controls:
            self.Controls.remove(control)
            
            # Update scroll region if AutoScroll is enabled
            if self.AutoScroll:
                self._update_scroll_region()
            
            # Apply AutoSize if enabled
            if self.AutoSize:
                self._apply_autosize()
                
            self.ControlRemoved(control)
            
    def _on_paint(self, event):
        """Handles the paint/resize event."""
        self.Paint()
        self.Resize()
    
    def _apply_autosize(self):
        """Applies AutoSize logic to the UserControl.

        The UserControl resizes to encompass all its child controls,
        respecting AutoSizeMode:
        - GrowOnly: Grows but does not shrink below the original size
        - GrowAndShrink: Adjusts exactly to the content

        Uses control properties directly to obtain sizes.
        """
        if not self.AutoSize or not hasattr(self, 'Controls') or not self.Controls:
            return
        
        # Prevent recursion: if already applying AutoSize, return
        if getattr(self, '_applying_autosize', False):
            return
        
        # Set flag to prevent child notifications from causing recursion
        self._applying_autosize = True
        
        try:
            # KEY: Force Tkinter geometry update
            container = self._container if hasattr(self, '_container') else self._tk_widget
            if container:
                container.update_idletasks()
                
            # Get border width to account for it
            border_width = 0
            try:
                border_width = int(self._tk_widget.cget('borderwidth'))
            except:
                pass
            
            # Calculate the area required to contain all child controls
            max_right = 0
            max_bottom = 0
            
            for control in self.Controls:
                # Use control's Left/Top/Width/Height properties directly
                # These are already updated when the control is positioned
                if hasattr(control, 'Left') and hasattr(control, 'Top'):
                    x = control.Left
                    y = control.Top
                    width = getattr(control, 'Width', 0)
                    height = getattr(control, 'Height', 0)
                    
                    control_right = x + width
                    control_bottom = y + height
                    max_right = max(max_right, control_right)
                    max_bottom = max(max_bottom, control_bottom)
            
            # Add padding
            padding = self.Padding
            if len(padding) == 4:
                pad_left, pad_top, pad_right, pad_bottom = padding
                padx = (pad_left + pad_right) // 2
                pady = (pad_top + pad_bottom) // 2
            else:
                padx, pady = padding
                
            # Calculate required size including padding AND border
            required_width = max_right + padx * 2 + border_width * 2
            required_height = max_bottom + pady * 2 + border_width * 2
            
            # Apply AutoSizeMode
            if self.AutoSizeMode == AutoSizeMode.GrowOnly:
                # Do not shrink below the maximum size ever reached
                if not hasattr(self, '_original_size'):
                    self._original_size = (0, 0)
                original_width, original_height = self._original_size
                required_width = max(required_width, original_width)
                required_height = max(required_height, original_height)
                # Update _original_size to the new maximum
                self._original_size = (required_width, required_height)
            # GrowAndShrink: use the calculated size as-is
            
            # Apply MinimumSize constraints
            if self.MinimumSize:
                min_width, min_height = self.MinimumSize
                required_width = max(required_width, min_width)
                required_height = max(required_height, min_height)
            
            # Apply MaximumSize constraints
            if self.MaximumSize:
                max_width, max_height = self.MaximumSize
                if max_width > 0:
                    required_width = min(required_width, max_width)
                if max_height > 0:
                    required_height = min(required_height, max_height)
            
            # Update dimensions only if changed to avoid infinite recursion loops
            if self.Width != required_width or self.Height != required_height:
                # Adjust position if Anchored to Right/Bottom
                if hasattr(self, '_apply_autosize_anchor_adjustment'):
                    self._apply_autosize_anchor_adjustment(required_width, required_height)
                
                # 7. Update dimensions
                self.Width = required_width
                self.Height = required_height
                
                # Force update of the widget size
                self._tk_widget.config(width=self.Width, height=self.Height)
                
                # 8. Reposition with the new size (always, visible or not)
                self._place_control(self.Width, self.Height)
                
                # 9. Notify parent container that this control's size changed
                self._notify_parent_layout_changed()
        finally:
            # Clear flag
            self._applying_autosize = False
    
    def set_Visible(self, value):
        """Set the UserControl visibility and propagate it to its child controls."""
        super().set_Visible(value)


############# Basic Controls #############

class Form(ScrollableControlMixin):
    """
    Represents the main window (Form).
    
    Usage - Option 1: form = Form(); form.Text = "My App"; form.Width = 800
    Usage - Option 2: form = Form({'Text': 'My App', 'Width': 800, 'Height': 600})
    """
    
    def __init__(self, props=None, parent=None):
        defaults = {
            'Title': "WinFormPy Application",
            'Width': 500,
            'Height': 300,
            'Name': "",
            'AutoScroll': False,
            'AutoScrollMinSize': None,
            'AutoScrollPosition': (0, 0),
            'AutoScrollMargin': (0, 0)
        }
        
        if props:
            defaults.update(props)
            # Alias: Text is equivalent to Title
            if 'Text' in props:
                defaults['Title'] = props['Text']
        
        if parent:
            self._root = tk.Toplevel(parent)
        elif tk._default_root:
            self._root = tk.Toplevel(tk._default_root)
        else:
            self._root = tk.Tk()
        
        # Main VB properties
        self.Name = defaults['Name'] or "Form1"
        self._text_value = defaults['Title']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Size = Size(self.Width, self.Height)
        self.Location = Point(0, 0)
        self.StartPosition = FormStartPosition.WindowsDefaultLocation
        self.FormBorderStyle = FormBorderStyle.Sizable
        self.MaximizeBox = True
        self.MinimizeBox = True
        self.ControlBox = True
        self.ShowIcon = True
        self.Icon = None
        self.BackColor = None
        self.Opacity = 1.0
        self.WindowState = FormWindowState.Normal
        self.Enabled = True
        self.Visible = True
        self.TopMost = False
        self.IsMdiContainer = False
        self.CancelButton = None
        self.AcceptButton = None
        
        # New properties
        self._dialog_result = DialogResult.None_
        self._owner = None
        self._show_in_taskbar = True
        self._transparency_key = None
        
        # Initialize scroll properties using the Mixin
        self._init_scroll_properties(defaults)
        
        # Internal list to keep a reference to all controls
        self.Controls = [] 
        
        # Additional properties
        self.BackgroundImage = None
        self.Font = None
        self.FontColor = None
        
        # Configure scroll infrastructure using the Mixin (only if AutoScroll is enabled)
        if self.AutoScroll:
            self._setup_scroll_infrastructure(self._root, self.BackColor)
        else:
            # Set container directly to root when no scrolling
            self._container = self._root 
        
        # VB Events for forms (inspired by ControlBase)
        self.Load = lambda: None  # Initialization, before showing the form
        self.Shown = lambda: None # Occurs whenever the form is first displayed
        self.FormClosing = lambda sender, e: None  # Before closing, allows cancellation
        self.FormClosed = lambda: None  # After closing
        self.Activated = lambda: None  # When the form is activated
        self.Deactivate = lambda: None  # When the form loses focus
        self.Resize = lambda: None  # On resize
        self.Move = lambda: None  # On move (placeholder)
        self.ControlAdded = lambda control: None  # When a control is added
        self.ControlRemoved = lambda control: None  # When a control is removed 

    @property
    def Visible(self):
        """Gets or sets the form visibility."""
        return getattr(self, '_visible', True)

    @Visible.setter
    def Visible(self, value):
        self._visible = value
        if hasattr(self, '_root') and self._root:
            if value:
                self._root.deiconify()
                # Propagate to children to ensure they are placed (if they were added while hidden)
                if hasattr(self, 'Controls'):
                    for control in self.Controls:
                        if hasattr(control, '_visible') and control._visible:
                            # Force update to propagate visibility change recursively
                            if hasattr(control, 'set_Visible'):
                                control.set_Visible(True)
                            elif hasattr(control, '_place_control'):
                                if hasattr(control, 'Width') and hasattr(control, 'Height'):
                                    control._place_control(control.Width, control.Height)
                                else:
                                    control._place_control()
            else:
                self._root.withdraw()

    @property
    def DialogResult(self):
        """Gets or sets the dialog result for the form."""
        return self._dialog_result

    @DialogResult.setter
    def DialogResult(self, value):
        self._dialog_result = value

    @property
    def Owner(self):
        """Gets or sets the form that owns this form."""
        return self._owner

    @Owner.setter
    def Owner(self, value):
        self._owner = value
        if hasattr(self, '_root') and self._root and value and hasattr(value, '_root'):
            self._root.transient(value._root)

    @property
    def TransparencyKey(self):
        """Gets or sets the color that will represent transparent areas of the form."""
        return self._transparency_key

    @TransparencyKey.setter
    def TransparencyKey(self, value):
        self._transparency_key = value
        if hasattr(self, '_root') and self._root:
            try:
                if value:
                    # Windows only usually
                    self._root.wm_attributes('-transparentcolor', value)
                else:
                    self._root.wm_attributes('-transparentcolor', '')
            except tk.TclError:
                pass

    @property
    def ShowInTaskbar(self):
        """Gets or sets a value indicating whether the form is displayed in the Windows taskbar."""
        return self._show_in_taskbar

    @ShowInTaskbar.setter
    def ShowInTaskbar(self, value):
        self._show_in_taskbar = value
        if hasattr(self, '_root') and self._root:
            try:
                # This is a best-effort mapping. 
                # toolwindow style removes it from taskbar but changes caption.
                self._root.wm_attributes("-toolwindow", 1 if not value else 0)
            except tk.TclError:
                pass

    @property
    def DesktopBounds(self):
        """Gets or sets the size and location of the form on the Windows desktop."""
        if hasattr(self, '_root') and self._root:
            geometry = self._root.geometry()
            # Parse geometry string "WxH+X+Y"
            import re
            match = re.match(r"(\d+)x(\d+)\+([-\d]+)\+([-\d]+)", geometry)
            if match:
                w, h, x, y = map(int, match.groups())
                return Rectangle(x, y, w, h)
        return Rectangle(self.Location.X, self.Location.Y, self.Width, self.Height)

    @DesktopBounds.setter
    def DesktopBounds(self, value):
        if hasattr(self, '_root') and self._root:
            self._root.geometry(f"{value.Width}x{value.Height}+{value.X}+{value.Y}")
            self.Width = value.Width
            self.Height = value.Height
            self.Location = Point(value.X, value.Y)

    @property
    def DesktopLocation(self):
        """Gets or sets the location of the form on the Windows desktop."""
        bounds = self.DesktopBounds
        return Point(bounds.X, bounds.Y)

    @DesktopLocation.setter
    def DesktopLocation(self, value):
        self.SetDesktopLocation(value.X, value.Y)

    def SetDesktopLocation(self, x, y):
        """Sets the location of the form on the Windows desktop."""
        if hasattr(self, '_root') and self._root:
            # Keep current size
            w = self.Width
            h = self.Height
            self._root.geometry(f"{w}x{h}+{x}+{y}")
            self.Location = Point(x, y)

    def CenterToScreen(self):
        """Centers the form on the current screen."""
        if hasattr(self, '_root') and self._root:
            self.Invalidate()
            width = self.Width
            height = self.Height
            screen_width = self._root.winfo_screenwidth()
            screen_height = self._root.winfo_screenheight()
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            self._root.geometry(f"{width}x{height}+{x}+{y}")
            self.Location = Point(x, y)

    def CenterToParent(self):
        """Centers the position of the form within the bounds of the parent form."""
        if self.Owner and hasattr(self.Owner, '_root'):
            parent = self.Owner
            parent_x = parent.Location.X
            parent_y = parent.Location.Y
            parent_w = parent.Width
            parent_h = parent.Height
            
            x = parent_x + (parent_w - self.Width) // 2
            y = parent_y + (parent_h - self.Height) // 2
            
            self.SetDesktopLocation(x, y)
        else:
            self.CenterToScreen()

    def Activate(self):
        """Activates the form and gives it focus."""
        if hasattr(self, '_root') and self._root:
            self._root.lift()
            self._root.focus_force()
            self.Activated()

    @property
    def Text(self):
        """Gets the form title."""
        return self._text_value

    @Text.setter
    def Text(self, value):
        """Sets the form title."""
        self._text_value = value
        if hasattr(self, '_root') and self._root:
            self._root.title(value)

    @property
    def Size(self):
        """Gets the size of the form as a tuple (width, height)."""
        return (self.Width, self.Height)

    @Size.setter
    def Size(self, value):
        """Sets the size of the form. Updates both Width and Height properties.
        
        Args:
            value: Can be a tuple/list (width, height) or a Size object with Width and Height attributes
        """
        if isinstance(value, (tuple, list)) and len(value) >= 2:
            self.Width = value[0]
            self.Height = value[1]
        elif hasattr(value, 'Width') and hasattr(value, 'Height'):
            self.Width = value.Width
            self.Height = value.Height

    @property
    def Menu(self):
        """Gets or sets the MainMenu that is displayed in the form."""
        return getattr(self, '_menu', None)

    @Menu.setter
    def Menu(self, value):
        self._menu = value
        if value:
            # Build Tkinter menu
            menubar = tk.Menu(self._root)
            for item in value.MenuItems:
                self._build_menu(menubar, item)
            self._root.config(menu=menubar)
        else:
            self._root.config(menu="")

    def _build_menu(self, parent_menu, item):
        if not item.Visible:
            return
            
        if item.MenuItems:
            # Submenu
            submenu = tk.Menu(parent_menu, tearoff=0)
            parent_menu.add_cascade(label=item.Text, menu=submenu)
            for subitem in item.MenuItems:
                self._build_menu(submenu, subitem)
        else:
            # Command
            if item.Text == "-":
                parent_menu.add_separator()
            else:
                state = "normal" if item.Enabled else "disabled"
                parent_menu.add_command(
                    label=item.Text, 
                    command=lambda i=item: i.PerformClick(),
                    accelerator=item.Shortcut if item.Shortcut else None,
                    state=state
                )

    def Show(self):
        """Starts the main loop."""
        # Ensure the form is visible
        self.Visible = True

        # Apply VB properties
        self._root.title(self.Text)
        
        # Size and Location - Use Width/Height properties directly instead of Size
        # to ensure the latest values are used
        width = self.Width
        height = self.Height
            
        if hasattr(self, 'Location'):
            if isinstance(self.Location, (tuple, list)):
                x = self.Location[0]
                y = self.Location[1]
            else:
                x = self.Location.X
                y = self.Location.Y
        else:
            x = 0
            y = 0

        self._root.geometry(f"{width}x{height}+{x}+{y}")
        
        if self.StartPosition == FormStartPosition.CenterScreen:
            self.CenterToScreen()
        elif self.StartPosition == FormStartPosition.WindowsDefaultLocation:
            # Tkinter default
            pass
        # For Manual, use Location
        
        # FormBorderStyle
        if self.FormBorderStyle == FormBorderStyle.FixedSingle:
            self._root.resizable(False, False)
        elif self.FormBorderStyle == FormBorderStyle.None_:
            self._root.overrideredirect(True)
        # Sizable is default
        
        # WindowState
        if self.WindowState == FormWindowState.Maximized:
            self._root.state('zoomed')
        elif self.WindowState == FormWindowState.Minimized:
            self._root.iconify()
        
        # Opacity
        self._root.attributes('-alpha', self.Opacity)
        
        # TopMost
        self._root.attributes('-topmost', self.TopMost)
        
        # Icon
        if self.Icon and self.ShowIcon:
            self._root.iconphoto(True, self.Icon)
            
        # ShowInTaskbar
        if not self.ShowInTaskbar:
             try:
                self._root.wm_attributes("-toolwindow", 1)
             except tk.TclError:
                pass
        
        # TransparencyKey
        if self.TransparencyKey:
             try:
                self._root.wm_attributes('-transparentcolor', self.TransparencyKey)
             except tk.TclError:
                pass
        
        # BackColor
        config = {}
        if self.BackColor is not None:
            config['bg'] = self.BackColor
        if self.BackgroundImage is not None:
            config['image'] = self.BackgroundImage
        if config:
            self._root.config(**config)
        
        # Bind CancelButton and AcceptButton
        if self.CancelButton:
            self._root.bind('<Escape>', lambda e: self.CancelButton._tk_widget.invoke())
        if self.AcceptButton:
            self._root.bind('<Return>', lambda e: self.AcceptButton._tk_widget.invoke())
        
        # Bind form events
        self._root.protocol("WM_DELETE_WINDOW", self._close)
        self._root.bind('<FocusIn>', lambda e: self.Activated())
        self._root.bind('<FocusOut>', lambda e: self.Deactivate())
        self._root.bind('<Configure>', lambda e: self.Resize())
        # Move placeholder
        
        # Trigger Load event
        self.Load()
        
        # Request repaint
        self.Invalidate()
        
        # Trigger Shown event
        self._root.after_idle(self.Shown)
        
        if isinstance(self._root, tk.Tk):
            self._root.mainloop()

    def ShowDialog(self):
        """Shows the form as a modal dialog."""
        if self.Owner and hasattr(self.Owner, '_root'):
             self._root.transient(self.Owner._root)
        
        # Show the form first (ensures it's created and visible)
        self.Show()
        
        # Make modal
        try:
            # Ensure it's visible before grabbing
            self.Update()
            self._root.grab_set()
        except tk.TclError:
            pass
        
        if not isinstance(self._root, tk.Tk):
            self._root.wait_window()
            
        return self.DialogResult
        
    def _close(self):
        """Handles the form closing."""
        e = {'Cancel': False}
        self.FormClosing(self, e)
        if not e['Cancel']:
            if self.DialogResult == DialogResult.None_:
                self.DialogResult = DialogResult.Cancel
            self._root.destroy()
            self.FormClosed()
    
    def Close(self):
        """Closes the form."""
        self._close()

    def ForceUpdate(self):
        """Processes pending GUI events and refreshes the window."""
        if hasattr(self, '_root') and self._root:
            try:
                self._root.update_idletasks()
                self._root.update()
            except tk.TclError:
                pass
    
    def Invalidate(self):
        """Marks the form as invalid and requests repainting.
        
        This Windows Forms method marks the control or form as 
        invalid and adds a message to the user interface message 
        queue to be repainted when the system is free.
        It is more efficient as it allows the system to combine several 
        repaint requests.
        """
        if hasattr(self, '_root') and self._root:
            try:
                self._root.update_idletasks()
            except tk.TclError:
                pass

    def Update(self):
        """Forces the form to repaint.
        
        This Windows Forms method forces the control to repaint 
        its client area.
        """
        if hasattr(self, '_root') and self._root:
            try:
                self._root.update()
            except tk.TclError:
                pass
    
    def Refresh(self):
        """Forces an immediate repaint of the form.
        
        This Windows Forms method forces an immediate repaint 
        by calling Invalidate() and then Update(), which skips the 
        message queue and repaints the control immediately.
        It is equivalent to Invalidate() + Update() in Windows Forms.
        """
        if hasattr(self, '_root') and self._root:
            try:
                # Invalidate() - marks as invalid and adds to queue
                self._root.update_idletasks()
                # Update() - processes the queue immediately
                self._root.update()
            except tk.TclError:
                pass
    
    def InvokeAsync(self, callback, delay=0):
        """Invokes a callback asynchronously after a delay.
        
        High-level method to schedule the execution of a function
        on the main GUI thread after a specified delay.
        It is equivalent to Control.BeginInvoke() in Windows Forms.
        
        Args:
            callback: Function to execute (lambda or normal function)
            delay: Delay in milliseconds before executing (0 = immediate)
        
        Example:
            # Execute immediately in the next event cycle
            form.InvokeAsync(lambda: MessageBox.Show("Hello"))
            
            # Execute after 1 second
            form.InvokeAsync(lambda: self.status_bar.Text = "Ready", 1000)
            
        REPLACES: self._root.after(0, lambda: ...)
        WITH: self.InvokeAsync(lambda: ...)
        """
        if hasattr(self, '_root') and self._root:
            try:
                self._root.after(delay, callback)
            except tk.TclError:
                pass
    
    def SetResizable(self, resizable_width=True, resizable_height=True):
        """Controls whether the form can be resized by the user.
        
        High-level method that encapsulates resizing control
        following the Windows Forms pattern where FormBorderStyle determines
        if the window is resizable.
        
        This method allows granular control over resizing:
        - Both True (default): Fully resizable window (FormBorderStyle = Sizable)
        - Both False: Fixed size window (FormBorderStyle = FixedSingle)
        - Mixed: Specific control per dimension (non-standard in Windows Forms, but useful)
        
        Args:
            resizable_width: If True, allows changing the window width
            resizable_height: If True, allows changing the window height
        
        Example:
            # Resizable window (default)
            form.SetResizable(True, True)
            
            # Fixed size window
            form.SetResizable(False, False)
            
            # Only height resizable (not common in Windows Forms)
            form.SetResizable(False, True)
        
        REPLACES: self._root.resizable(True, True)
        WITH: self.SetResizable(True, True)
        
        Windows Forms Equivalent:
            VB.NET: Me.FormBorderStyle = FormBorderStyle.Sizable ' (True, True)
            VB.NET: Me.FormBorderStyle = FormBorderStyle.FixedSingle ' (False, False)
        """
        if hasattr(self, '_root') and self._root:
            try:
                self._root.resizable(resizable_width, resizable_height)
                
                # Update FormBorderStyle for consistency
                if not resizable_width and not resizable_height:
                    self.FormBorderStyle = "FixedSingle"
                else:
                    self.FormBorderStyle = "Sizable"
            except tk.TclError:
                pass
    
    def LockWindowSize(self):
        """Locks the window size, preventing the user from resizing it.
        
        Convenience method equivalent to SetResizable(False, False).
        Useful during operations requiring fixed geometry, such as
        initial control creation.
        
        Example:
            form.LockWindowSize()
            # ... create controls ...
            form.UnlockWindowSize()
        
        REPLACES: self._root.resizable(False, False)
        WITH: self.LockWindowSize()
        
        Windows Forms Equivalent:
            VB.NET: Me.FormBorderStyle = FormBorderStyle.FixedSingle
        """
        self.SetResizable(False, False)
    
    def UnlockWindowSize(self):
        """Unlocks the window size, allowing the user to resize it.
        
        Convenience method equivalent to SetResizable(True, True).
        Restores resizing capability after having locked it.
        
        Example:
            form.LockWindowSize()
            # ... create controls ...
            form.UnlockWindowSize()
        
        REPLACES: self._root.resizable(True, True)
        WITH: self.UnlockWindowSize()
        
        Windows Forms Equivalent:
            VB.NET: Me.FormBorderStyle = FormBorderStyle.Sizable
        """
        self.SetResizable(True, True)

    def get_Parent(self):
        """Gets the parent control of the Form.

        For the main Form there is usually no parent (returns None).

        Returns:
            None for the main Form.
        """
        return None      


    def AddControl(self, control):
        """Adds a control to the Form with relative positions.
        
        Implements the Windows Forms visibility hierarchy:
        - The control is added to the Form (becomes its parent)
        - The control will only be visible if its own Visible property is True
        
        RECOMMENDED USAGE:
            form = Form({'Text': 'My Form'})
            button = Button(form, {'Text': 'OK', 'Left': 10, 'Top': 10})
            form.AddControl(button)
        
        Left/Top coordinates are relative to the Form.
        """
        self.Controls.append(control)
        
        # Configure the control container (use _container if AutoScroll is present)
        control.master = self._container if hasattr(self, '_container') else self._root
        
        # Register this Form as the container wrapper for the parent hierarchy
        if not hasattr(control.master, '_control_wrapper'):
            control.master._control_wrapper = self
        
        # Reposition the control in the new container
        control._place_control()
        
        # Inherit container properties
        if hasattr(control, 'Enabled') and hasattr(self, 'Enabled'):
            control.Enabled = self.Enabled
            if hasattr(control, '_tk_widget'):
                try:
                    control._tk_widget.config(state='normal' if self.Enabled else 'disabled')
                except tk.TclError:
                    pass
        
        # Update scroll region if AutoScroll is enabled
        if self.AutoScroll:
            self._update_scroll_region()
        
        # Invoke ControlAdded event
        self.ControlAdded(control)
    
    def RemoveControl(self, control):
        """Removes a control from the Form."""
        if control in self.Controls:
            self.Controls.remove(control)
            
            # Update scroll region if AutoScroll is enabled
            if self.AutoScroll:
                self._update_scroll_region()
                
            self.ControlRemoved(control)
    

class Timer:
    """
    Represents a Timer for timed events.
    
    Usage - Option 1: timer = Timer(root); timer.Interval = 2000; timer.Enabled = True
    Usage - Option 2: timer = Timer(root, {'Interval': 2000, 'Enabled': True})
    """
    
    def __init__(self, root, props=None):
        defaults = {
            'interval': 1000,
            'Name': "",
            'Enabled': False,
            'Tag': None,
            'Modifiers': "Private"
        }
        
        if props:
            defaults.update(props)
            # Alias: Interval (capitalized) is also valid
            if 'Interval' in props:
                defaults['interval'] = props['Interval']
        
        self._root = root
        self.Name = defaults['Name']
        self.Interval = defaults['interval']
        self._enabled = False  # Initialize _enabled before property setter usage
        self.Enabled = defaults['Enabled']
        self._tag = defaults['Tag']  # Custom object
        self.Modifiers = defaults['Modifiers']  # 'Public', 'Private', etc. (placeholder)
        self.Tick = lambda: None
        self._job = None
        
        # Start if Enabled
        if self.Enabled:
            self.Start()

    @property
    def Tag(self):
        """Gets or sets the object that contains data about the control."""
        return self._tag

    @Tag.setter
    def Tag(self, value):
        self._tag = value

    @property
    def Enabled(self):
        return self._enabled

    @Enabled.setter
    def Enabled(self, value):
        if value and not self._enabled:
            self.Start()
        elif not value and self._enabled:
            self.Stop()
        self._enabled = value

    def Start(self):
        """Starts the timer."""
        if not self._enabled:
            self._enabled = True
            self._schedule()

    def Stop(self):
        """Stops the timer."""
        self._enabled = False
        if self._job:
            self._root.after_cancel(self._job)

    def _schedule(self):
        """Schedules the next tick."""
        if self._enabled:
            self.Tick()
            self._job = self._root.after(self.Interval, self._schedule)


class ProgressBar(ControlBase):
    """
    Represents a ProgressBar control that visually indicates the progress of a long operation.
    
    The Style property determines the style of ProgressBar displayed.
    The Maximum and Minimum properties define the range of values to represent the progress of a task.
    The Value property represents the progress that the application has made toward completing the operation.
    """
    
    def __init__(self, master_form, props=None):
        """Initializes a ProgressBar.
        
        Args:
            master_form: The form or parent container
            props: Optional dictionary with initial properties
        """
        # Default values
        defaults = {
            'Left': 10,
            'Top': 10,
            'Width': 200,
            'Height': 20,
            'Minimum': 0,
            'Maximum': 100,
            'Value': 0,
            'Style': ProgressBarStyle.Blocks,
            'Step': 10,
            'MarqueeAnimationSpeed': 100,
            'RightToLeftLayout': False,
            'TabStop': False,
            'Name': "",
            'Enabled': True,
            'Visible': True,
            'Dock': None,
            'Anchor': None
        }
        
        if props:
            defaults.update(props)
        
        # Resolve Tkinter widget and save parent container
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Save parent container for auto-registration
        self._parent_container = parent_container
        
        self.Name = defaults['Name']
        self.Minimum = defaults['Minimum']
        self.Maximum = defaults['Maximum']
        self.Value = defaults['Value']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Style = defaults['Style']  # 'Blocks', 'Continuous', 'Marquee'
        self.Step = defaults['Step']
        self.MarqueeAnimationSpeed = defaults['MarqueeAnimationSpeed']
        self.RightToLeftLayout = defaults['RightToLeftLayout']
        self.TabStop = defaults['TabStop']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        
        # VB Events
        self.ValueChanged = lambda: None
        self.StyleChanged = lambda: None
        self.RightToLeftLayoutChanged = lambda sender, e: None
        
        # Determine mode based on Style
        mode = 'indeterminate' if self.Style == ProgressBarStyle.Marquee else 'determinate'
        
        # Create Tkinter widget
        self._tk_widget = ttk.Progressbar(self.master, orient='horizontal', length=self.Width, mode=mode)
        self._tk_widget['maximum'] = self.Maximum
        self._tk_widget['value'] = self.Value
        self._place_control(self.Width, self.Height)
        
        # Bind common events
        self._bind_common_events()
        
        # Start animation if Marquee
        if self.Style == ProgressBarStyle.Marquee:
            self._tk_widget.start(self.MarqueeAnimationSpeed)
        
        # Apply Dock and Anchor if specified in props
        if defaults['Dock']:
            self.Dock = defaults['Dock']
        if defaults['Anchor']:
            self.Anchor = defaults['Anchor']
        
        # Auto-register with parent container if necessary
        self._auto_register_with_parent()

    @property
    def Value(self):
        return getattr(self, '_value', 0)

    @Value.setter
    def Value(self, value):
        # Clamp value between Minimum and Maximum
        if value < self.Minimum: value = self.Minimum
        if value > self.Maximum: value = self.Maximum
        
        self._value = value
        if hasattr(self, '_tk_widget') and self._tk_widget is not None:
            self._tk_widget['value'] = value
        if hasattr(self, 'ValueChanged'):
            self.ValueChanged()

    def set_Style(self, style):
        """Sets the progress bar style."""
        if self.Style != style:
            self.Style = style
            mode = 'indeterminate' if style == ProgressBarStyle.Marquee else 'determinate'
            if hasattr(self, '_tk_widget') and self._tk_widget:
                self._tk_widget.config(mode=mode)
                if style == ProgressBarStyle.Marquee:
                    self._tk_widget.start(self.MarqueeAnimationSpeed)
                else:
                    self._tk_widget.stop()
                    self._tk_widget['value'] = self.Value
            self.StyleChanged()
            
    def Increment(self, value):
        """Advances the current position of the progress bar by the specified amount."""
        self.Value += value

    def PerformStep(self):
        """Advances the current position of the progress bar by the amount of the Step property."""
        self.Increment(self.Step)
        
    @property
    def RightToLeftLayout(self):
        return getattr(self, '_right_to_left_layout', False)
        
    @RightToLeftLayout.setter
    def RightToLeftLayout(self, value):
        if getattr(self, '_right_to_left_layout', False) != value:
            self._right_to_left_layout = value
            self.RightToLeftLayoutChanged(self, EventArgs.Empty)
            # Tkinter Progressbar doesn't natively support RTL layout easily without frame tricks
            # This is a placeholder for property compliance

    # Override TabStop to default to False (usually)
    @property
    def TabStop(self):
        return getattr(self, '_tab_stop', False)
        
    @TabStop.setter
    def TabStop(self, value):
        self._tab_stop = value
        # ttk.Progressbar is not typically a tab stop in Tkinter either unless configured


class Button(ControlBase):
    """Represents a button (CommandButton in VB6, Button in VB.NET)."""
    
    def __init__(self, master_form, props=None):
        """Initializes a Button.

        Args:
            master_form: The parent form or container
            props: Optional dictionary with initial properties
                   Example: {'Text': 'Click', 'Left': 10, 'Top': 20, 'BackColor': 'blue'}
                   Use {'UseSystemStyles': True} to apply system styles automatically
        """
        # Default values
        defaults = {
            'Left': 10,
            'Top': 10,
            'Width': 100,
            'Height': 30,
            'Name': '',
            'Text': 'Button',
            'Enabled': True,
            'Visible': True,
            'DialogResult': DialogResult.None_,
            'Font': None,
            'ForeColor': None,
            'BackColor': None,
            'FlatStyle': FlatStyle.Standard,
            'Image': None,
            'ImageAlign': ContentAlignment.MiddleLeft,
            'TextImageRelation': TextImageRelation.Overlay,
            'UseCompatibleTextRendering': False,
            'AutoSize': False,
            'MinimumSize': None,
            'MaximumSize': None,
            'ToolTipText': '',
            'AutoEllipsis': False,
            'Command': None,
            'CommandParameter': None,
            'FlatAppearance': None,
            'ImageIndex': -1,
            'ImageKey': '',
            'ImageList': None,
            'IsDefault': False,
            'UseMnemonic': True,
            'UseVisualStyleBackColor': True,
            'TextAlign': ContentAlignment.MiddleCenter
        }
        
        # Merge default values with provided props
        if props:
            # Extract UseSystemStyles before updating defaults
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            # Apply system styles if enabled
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Button", use_system_styles=True)
        else:
            # Apply system styles according to global configuration
            SystemStyles.ApplyToDefaults(defaults, control_type="Button")
        
        # Resolve the Tkinter widget and keep the original parent container
        master_widget, parent_container = _resolve_master_widget(master_form)
        
        # Initialize ControlBase with position
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Store the parent container for auto-registration
        self._parent_container = parent_container
        
        # Set basic properties
        self.Name = defaults['Name']
        self._text_value = defaults['Text']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.DialogResult = defaults['DialogResult']
        self.Font = defaults['Font']
        self.ForeColor = defaults['ForeColor']
        self.BackColor = defaults['BackColor']
        self._flatstyle = defaults['FlatStyle']
        self.Image = defaults['Image']
        self.ImageAlign = defaults['ImageAlign']
        self.TextImageRelation = defaults['TextImageRelation']
        self.UseCompatibleTextRendering = defaults['UseCompatibleTextRendering']
        self.AutoSize = defaults['AutoSize']
        self.MinimumSize = defaults['MinimumSize']
        self.MaximumSize = defaults['MaximumSize']
        self.AutoEllipsis = defaults['AutoEllipsis']
        self.Command = defaults['Command']
        self.CommandParameter = defaults['CommandParameter']
        self.FlatAppearance = defaults['FlatAppearance']
        self.ImageIndex = defaults['ImageIndex']
        self.ImageKey = defaults['ImageKey']
        self.ImageList = defaults['ImageList']
        self.IsDefault = defaults['IsDefault']
        self.UseMnemonic = defaults['UseMnemonic']
        self.UseVisualStyleBackColor = defaults['UseVisualStyleBackColor']
        self.TextAlign = defaults['TextAlign']
        
        # Events
        self.CommandCanExecuteChanged = lambda sender, e: None
        self.CommandChanged = lambda sender, e: None
        self.CommandParameterChanged = lambda sender, e: None
        
        # Location as a tuple
        self.Location = (self.Left, self.Top)
        
        # Create the Tkinter widget
        self._tk_widget = tk.Button(
            self.master, 
            text=self._text_value, 
            command=self._handle_click_event
        )
        
        # Apply visual configurations
        self._apply_visual_config()
        
        # Set tooltip
        if defaults['ToolTipText']:
            self.ToolTipText = defaults['ToolTipText']
        
        # Bind common events
        self._bind_common_events()
        
        # Unbind Button-1 because tk.Button uses command for clicks
        # This prevents double firing of the Click event
        if self._tk_widget:
            self._tk_widget.unbind('<Button-1>')
        
        # Position if visible
        if self.Visible:
            if self.AutoSize:
                self._apply_autosize()
            self._place_control(self.Width, self.Height)
        else:
            self._tk_widget.place_forget()
            
        # Apply Dock and Anchor if they were specified in props
        if 'Dock' in defaults and defaults['Dock']:
            self.Dock = defaults['Dock']
        if 'Anchor' in defaults and defaults['Anchor'] is not None:
            self.Anchor = defaults['Anchor']
        if 'Margin' in defaults:
            self.Margin = defaults['Margin']
        if 'Padding' in defaults:
            self.Padding = defaults['Padding']

        # AUTO-REGISTRATION: Automatically add to the parent container
        self._auto_register_with_parent()
    
    def _apply_visual_config(self):
        """Applies visual configuration to the widget."""
        # Call base method first
        super()._apply_visual_config()
        
        # Apply Button-specific configurations
        config = {}
        if self.Image:
            config['image'] = self.Image
        if self.TextImageRelation:
            # Map TextImageRelation to compound
            # Overlay=0, ImageAboveText=1, TextAboveImage=2, ImageBeforeText=4, TextBeforeImage=8
            compound_map = {
                TextImageRelation.Overlay: 'center',
                TextImageRelation.ImageAboveText: 'top',
                TextImageRelation.TextAboveImage: 'bottom',
                TextImageRelation.ImageBeforeText: 'left',
                TextImageRelation.TextBeforeImage: 'right',
                # String fallbacks
                'left': 'left', 'right': 'right', 'top': 'top', 'bottom': 'bottom', 'center': 'center'
            }
            config['compound'] = compound_map.get(self.TextImageRelation, 'none')
            
        # Map FlatStyle to relief
        relief_map = {
            FlatStyle.Standard: 'raised', 
            FlatStyle.Flat: 'flat', 
            FlatStyle.Popup: 'ridge', 
            FlatStyle.System: 'raised',
            # String fallbacks
            'Standard': 'raised', 'Flat': 'flat', 'Popup': 'ridge', 'System': 'raised'
        }
        config['relief'] = relief_map.get(self._flatstyle, 'raised')
        
        if config:
            try:
                self._tk_widget.config(**config)
            except tk.TclError:
                pass  # Ignore unsupported options

    def _handle_click_event(self):
        """Intermediate function to execute the assigned Click handler."""
        self.Click(self, None)

    def set_Enabled(self, enabled):
        """Sets whether the button is enabled."""
        self.Enabled = enabled
        self._tk_widget.config(state='normal' if enabled else 'disabled')

    @property
    def Text(self):
        """Property getter for Text in Button."""
        return self._text_value
    
    @Text.setter
    def Text(self, value):
        """Property setter for Text in Button."""
        self._text_value = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._tk_widget.config(text=value)
            # Apply AutoSize if enabled
            if self.AutoSize:
                # Force geometry update before applying autosize
                try:
                    self._tk_widget.update_idletasks()
                except:
                    pass
                self._apply_autosize()
                # _apply_autosize() already calls _place_control()
    
    @property
    def AutoSizeMode(self):
        """Basic controls always use GrowAndShrink mode."""
        return AutoSizeMode.GrowAndShrink
    
    @AutoSizeMode.setter
    def AutoSizeMode(self, value):
        """AutoSizeMode is not configurable for basic controls - always GrowAndShrink."""
        pass  # Ignore any attempts to change it
    
    @property
    def FlatStyle(self):
        """Property getter for FlatStyle."""
        return self._flatstyle
    
    @FlatStyle.setter
    def FlatStyle(self, value):
        """Property setter for FlatStyle."""
        self._flatstyle = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            relief_map = {
                FlatStyle.Standard: 'raised', 
                FlatStyle.Flat: 'flat', 
                FlatStyle.Popup: 'ridge', 
                FlatStyle.System: 'raised',
                # String fallbacks
                'Standard': 'raised', 'Flat': 'flat', 'Popup': 'ridge', 'System': 'raised'
            }
            self._tk_widget.config(relief=relief_map.get(value, 'raised'))

    def NotifyDefault(self, value):
        """Notifies the Button whether it is the default button."""
        self.IsDefault = value
        # Visual update if needed (e.g. thicker border)
        if self._tk_widget:
            if value:
                self._tk_widget.config(default='active')
            else:
                self._tk_widget.config(default='normal')

    def PerformClick(self):
        """Generates a Click event for the button."""
        if self.Enabled:
            self.Click()


class Label(ControlBase):
    """Represents a text label."""
    
    def __init__(self, master_form, props=None):
        """Initializes a Label.

        Args:
            master_form: The parent form or container
            props: Optional dictionary with initial properties
                   Use {'UseSystemStyles': True} to apply system styles automatically
        """
        # Default values
        defaults = {
            'Left': 10,
            'Top': 50,
            'Width': None,
            'Height': None,
            'Name': '',
            'Text': 'Label',
            'Enabled': True,
            'Visible': True,
            'Font': None,
            'ForeColor': None,
            'BackColor': None,
            'BorderStyle': BorderStyle.None_,
            'TextAlign': ContentAlignment.TopLeft,
            'AutoSize': True,
            'MinimumSize': None,
            'MaximumSize': None,
            'UseMnemonic': False,
            'Padding': (0, 0),
            'Margin': (0, 0),
            'ToolTipText': '',
            'AutoEllipsis': False,
            'FlatStyle': FlatStyle.Standard,
            'Image': None,
            'ImageAlign': ContentAlignment.MiddleCenter,
            'ImageIndex': -1,
            'ImageKey': '',
            'ImageList': None,
            'LiveSetting': 'off',
            'UseCompatibleTextRendering': False,
            'UseWaitCursor': False
        }
        
        if props:
            # Extract UseSystemStyles before updating defaults
            use_system_styles = props.pop('UseSystemStyles', None)
            
            # Smart AutoSize: If Width/Height are provided but AutoSize is not, disable AutoSize
            if ('Width' in props or 'Height' in props) and 'AutoSize' not in props:
                defaults['AutoSize'] = False
                
            defaults.update(props)
            # Apply system styles if enabled
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Control", use_system_styles=True)
        else:
            # Apply system styles according to global configuration
            SystemStyles.ApplyToDefaults(defaults, control_type="Control")
        
        # Resolve the Tkinter widget and keep the original parent container
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])

        # Store the parent container for auto-registration
        self._parent_container = parent_container
        
        # Propiedades VB
        self.Name = defaults['Name']
        self._text_value = defaults['Text']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.Font = defaults['Font']
        self.ForeColor = defaults['ForeColor']
        self.BackColor = defaults['BackColor']
        self.BorderStyle = defaults['BorderStyle']
        self.TextAlign = defaults['TextAlign']
        self.AutoSize = defaults['AutoSize']
        self.MinimumSize = defaults['MinimumSize']
        self.MaximumSize = defaults['MaximumSize']
        self.UseMnemonic = defaults['UseMnemonic']
        self.Padding = defaults['Padding']
        self.Margin = defaults['Margin']
        
        self._auto_ellipsis = defaults['AutoEllipsis']
        self._flat_style = defaults['FlatStyle']
        self._image = defaults['Image']
        self._image_align = defaults['ImageAlign']
        self._image_index = defaults['ImageIndex']
        self._image_key = defaults['ImageKey']
        self._image_list = defaults['ImageList']
        self._live_setting = defaults['LiveSetting']
        self._use_compatible_text_rendering = defaults['UseCompatibleTextRendering']
        self._use_wait_cursor = defaults['UseWaitCursor']
        
        # VB events
        self.TextChanged = lambda: None
        
        # Process UseMnemonic
        display_text = self._text_value
        underline = -1
        if self.UseMnemonic and '&' in self._text_value:
            idx = self._text_value.find('&')
            if idx + 1 < len(self._text_value):
                underline = idx
                display_text = self._text_value[:idx] + self._text_value[idx+1:]
        
        # Create the Tkinter widget
        self._tk_widget = tk.Label(self.master, text=display_text, underline=underline)
        
        # Apply properties
        if self.ForeColor:
            self._tk_widget.config(fg=self.ForeColor)
        if self.BackColor:
            self._tk_widget.config(bg=self.BackColor)
        if self.BorderStyle:
            # Mapear BorderStyle de VB.NET a tkinter
            relief_map = {
                BorderStyle.None_: 'flat', 
                BorderStyle.Fixed3D: 'ridge', 
                BorderStyle.FixedSingle: 'solid',
                # String fallbacks
                'None': 'flat', 'Fixed3D': 'ridge', 'FixedSingle': 'solid',
                'flat': 'flat', 'groove': 'groove', 'raised': 'raised',
                'ridge': 'ridge', 'solid': 'solid', 'sunken': 'sunken'
            }
            self._tk_widget.config(relief=relief_map.get(self.BorderStyle, 'flat'))
        if self.Font:
            self._tk_widget.config(font=self.Font)
        
        # Alignment
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
            anchor=anchor_map.get(self.TextAlign, 'w'),
            justify=justify_map.get(self.TextAlign, 'left')
        )
        
        # Padding
        padding = self.Padding
        if len(padding) == 4:
            pad_left, pad_top, pad_right, pad_bottom = padding
            padx = (pad_left + pad_right) // 2
            pady = (pad_top + pad_bottom) // 2
        else:
            padx, pady = padding
            
        self._tk_widget.config(padx=padx, pady=pady)
        
        # Enabled/Visible
        if not self.Enabled:
            self._tk_widget.config(state='disabled')
        if not self.Visible:
            self._tk_widget.place_forget()
        
        # Set tooltip
        if defaults['ToolTipText']:
            self.ToolTipText = defaults['ToolTipText']
        
        # Bind events
        self._bind_common_events()
        self._tk_widget.bind('<Button-1>', self._on_click)
        self._tk_widget.bind('<Double-Button-1>', self._on_double_click)
        self._tk_widget.bind('<Configure>', self._on_paint)  # Placeholder for Paint
        
        # AutoSize: automatically adjust size according to content
        if self.AutoSize:
            self._apply_autosize()
            self._place_control(self.Width, self.Height)
        else:
            # Fixed size
            if self.Width is None or self.Height is None:
                # If size is not specified, use auto
                self._place_control()
            else:
                self._place_control(self.Width, self.Height)
        
        # Apply Dock and Anchor if they were specified in props
        if 'Dock' in defaults and defaults['Dock']:
            self.Dock = defaults['Dock']
        if 'Anchor' in defaults and defaults['Anchor'] is not None:
            self.Anchor = defaults['Anchor']
        if 'Margin' in defaults:
            self.Margin = defaults['Margin']
        if 'Padding' in defaults:
            self.Padding = defaults['Padding']
            
        # AUTO-REGISTRATION: Automatically add to the parent container
        self._auto_register_with_parent()

    def set_Text(self, new_text):
        """Setter method to update the text at runtime."""
        self._text_value = new_text
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._tk_widget.config(text=new_text)
            try:
                self._tk_widget.update_idletasks()
            except tk.TclError:
                pass
        self.TextChanged()
        
        # Apply AutoSize if enabled
        if self.AutoSize:
            self._apply_autosize()
            # _apply_autosize() already calls _place_control()
    @property
    def Text(self):
        """Property getter for Text in Label."""
        return self._text_value
    
    @Text.setter
    def Text(self, value):
        """Property setter for Text in Label."""
        self.set_Text(value)

    @property
    def AutoEllipsis(self):
        """Property getter for AutoEllipsis."""
        return self._auto_ellipsis

    @AutoEllipsis.setter
    def AutoEllipsis(self, value):
        """Property setter for AutoEllipsis."""
        self._auto_ellipsis = value

    @property
    def AutoSizeMode(self):
        """Basic controls always use GrowAndShrink mode."""
        return AutoSizeMode.GrowAndShrink
    
    @AutoSizeMode.setter
    def AutoSizeMode(self, value):
        """AutoSizeMode is not configurable for basic controls - always GrowAndShrink."""
        pass  # Ignore any attempts to change it

    @property
    def FlatStyle(self):
        """Property getter for FlatStyle."""
        return self._flat_style

    @FlatStyle.setter
    def FlatStyle(self, value):
        """Property setter for FlatStyle."""
        self._flat_style = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            relief_map = {
                FlatStyle.Standard: 'raised', 
                FlatStyle.Flat: 'flat', 
                FlatStyle.Popup: 'ridge', 
                FlatStyle.System: 'raised',
                # String fallbacks
                'Standard': 'raised', 'Flat': 'flat', 'Popup': 'ridge', 'System': 'raised'
            }
            self._tk_widget.config(relief=relief_map.get(value, 'raised'))

    @property
    def Image(self):
        """Property getter for Image."""
        return self._image

    @Image.setter
    def Image(self, value):
        """Property setter for Image."""
        self._image = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            if value:
                self._tk_widget.config(image=value, compound=self._get_compound_alignment())
            else:
                self._tk_widget.config(image='', compound='none')

    @property
    def ImageAlign(self):
        """Property getter for ImageAlign."""
        return self._image_align

    @ImageAlign.setter
    def ImageAlign(self, value):
        """Property setter for ImageAlign."""
        self._image_align = value
        if hasattr(self, '_tk_widget') and self._tk_widget and self._image:
            self._tk_widget.config(compound=self._get_compound_alignment())

    @property
    def ImageIndex(self):
        """Property getter for ImageIndex."""
        return self._image_index

    @ImageIndex.setter
    def ImageIndex(self, value):
        """Property setter for ImageIndex."""
        self._image_index = value
        self._update_image_from_list()

    @property
    def ImageKey(self):
        """Property getter for ImageKey."""
        return self._image_key

    @ImageKey.setter
    def ImageKey(self, value):
        """Property setter for ImageKey."""
        self._image_key = value
        self._update_image_from_list()

    @property
    def ImageList(self):
        """Property getter for ImageList."""
        return self._image_list

    @ImageList.setter
    def ImageList(self, value):
        """Property setter for ImageList."""
        self._image_list = value
        self._update_image_from_list()

    @property
    def LiveSetting(self):
        """Property getter for LiveSetting."""
        return self._live_setting

    @LiveSetting.setter
    def LiveSetting(self, value):
        """Property setter for LiveSetting."""
        self._live_setting = value

    @property
    def UseCompatibleTextRendering(self):
        """Property getter for UseCompatibleTextRendering."""
        return self._use_compatible_text_rendering

    @UseCompatibleTextRendering.setter
    def UseCompatibleTextRendering(self, value):
        """Property setter for UseCompatibleTextRendering."""
        self._use_compatible_text_rendering = value

    @property
    def UseWaitCursor(self):
        """Property getter for UseWaitCursor."""
        return self._use_wait_cursor

    @UseWaitCursor.setter
    def UseWaitCursor(self, value):
        """Property setter for UseWaitCursor."""
        self._use_wait_cursor = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            if value:
                self._tk_widget.config(cursor='watch')
            else:
                self._tk_widget.config(cursor='arrow')

    def _get_compound_alignment(self):
        """Helper to map ImageAlign to Tkinter compound option."""
        align_map = {
            ContentAlignment.TopCenter: 'top', ContentAlignment.BottomCenter: 'bottom',
            ContentAlignment.MiddleLeft: 'left', ContentAlignment.MiddleRight: 'right',
            ContentAlignment.MiddleCenter: 'center', ContentAlignment.TopLeft: 'top',
            ContentAlignment.TopRight: 'top', ContentAlignment.BottomLeft: 'bottom', ContentAlignment.BottomRight: 'bottom',
            # String fallbacks
            'top_center': 'top', 'bottom_center': 'bottom',
            'middle_left': 'left', 'middle_right': 'right',
            'middle_center': 'center', 'top_left': 'top',
            'top_right': 'top', 'bottom_left': 'bottom', 'bottom_right': 'bottom'
        }
        return align_map.get(self.ImageAlign, 'none')

    def _update_image_from_list(self):
        """Updates the image from ImageList based on Index or Key."""
        if self.ImageList and (self.ImageIndex >= 0 or self.ImageKey):
            # Placeholder for ImageList logic
            pass


class TextBox(ControlBase):
    """Represents a simple text box."""
    
    def __init__(self, master_form, props=None):
        """Initializes a TextBox.

        Args:
            master_form: The parent form or container
            props: Optional dictionary with initial properties
                   Use {'UseSystemStyles': True} to apply system styles automatically
        """
        # Default values
        defaults = {
            'Left': 10,
            'Top': 80,
            'Width': 200,
            'Height': 25,
            'Name': '',
            'Text': '',
            'Enabled': True,
            'Visible': True,
            'ReadOnly': False,
            'Multiline': False,
            'ScrollBars': ScrollBars.None_,
            'PasswordChar': '',
            'UseSystemPasswordChar': False,
            'MaxLength': 0,
            'TextAlign': HorizontalAlignment.Left,
            'WordWrap': True,
            'AcceptsReturn': True,
            'AutoSize': False,
            'MinimumSize': None,
            'MaximumSize': None,
            'BackColor': None,
            'ForeColor': None,
            'Font': None,
            'AcceptsTab': False,
            'AutoCompleteCustomSource': None,
            'AutoCompleteMode': AutoCompleteMode.None_,
            'AutoCompleteSource': AutoCompleteSource.None_,
            'BorderStyle': BorderStyle.Fixed3D,
            'CharacterCasing': CharacterCasing.Normal,
            'HideSelection': True,
            'PlaceholderText': '',
            'ShortcutsEnabled': True,
            'UseWaitCursor': False,
            'SelectAllOnClick': False
        }
        
        if props:
            # Extract UseSystemStyles before updating defaults
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            # Apply system styles if enabled
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Window", use_system_styles=True)
        else:
            # Apply system styles according to global configuration
            SystemStyles.ApplyToDefaults(defaults, control_type="Window")
        
        # Resolve the Tkinter widget and keep the original parent container
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])

        # Store the parent container for auto-registration
        self._parent_container = parent_container
        
        # VB properties
        self.Name = defaults['Name']
        self._text_value = defaults['Text']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.ReadOnly = defaults['ReadOnly']
        self.Multiline = defaults['Multiline']
        self.ScrollBars = defaults['ScrollBars']
        self.PasswordChar = defaults['PasswordChar']
        self.UseSystemPasswordChar = defaults['UseSystemPasswordChar']
        self.MaxLength = defaults['MaxLength']
        self.TextAlign = defaults['TextAlign']
        self.WordWrap = defaults['WordWrap']
        self.AcceptsReturn = defaults['AcceptsReturn']
        self.AutoSize = defaults['AutoSize']
        self.MinimumSize = defaults['MinimumSize']
        self.MaximumSize = defaults['MaximumSize']
        self.BackColor = defaults['BackColor']
        self.ForeColor = defaults['ForeColor']
        self.Font = defaults['Font']
        
        self.AcceptsTab = defaults['AcceptsTab']
        self.AutoCompleteCustomSource = defaults['AutoCompleteCustomSource']
        self.AutoCompleteMode = defaults['AutoCompleteMode']
        self.AutoCompleteSource = defaults['AutoCompleteSource']
        self.BorderStyle = defaults['BorderStyle']
        self.CharacterCasing = defaults['CharacterCasing']
        self.HideSelection = defaults['HideSelection']
        self.PlaceholderText = defaults['PlaceholderText']
        self.ShortcutsEnabled = defaults['ShortcutsEnabled']
        self.UseWaitCursor = defaults['UseWaitCursor']
        self.SelectAllOnClick = defaults['SelectAllOnClick']
        
        # VB events (callbacks)
        self.TextChanged = lambda: None
        self.MouseMove = lambda x, y: None
        
        # Create the Tkinter widget
        if self.Multiline:
            # ScrollBars logic - determine what scrollbars to show
            show_vertical = self.ScrollBars in [ScrollBars.Vertical, ScrollBars.Both, 'vertical', 'both']
            show_horizontal = self.ScrollBars in [ScrollBars.Horizontal, ScrollBars.Both, 'horizontal', 'both']
            
            # If horizontal scrollbar is enabled, disable word wrap to allow horizontal scrolling
            wrap_mode = 'none' if show_horizontal else ('word' if self.WordWrap else 'none')
            
            # If scrollbars are needed, create a container frame
            if show_vertical or show_horizontal:
                self._container_frame = tk.Frame(self.master, width=self.Width, height=self.Height)
                self._tk_widget = tk.Text(self._container_frame, wrap=wrap_mode)
                
                if show_vertical:
                    vscroll = tk.Scrollbar(self._container_frame, command=self._tk_widget.yview)
                    self._tk_widget.config(yscrollcommand=vscroll.set)
                    vscroll.pack(side=tk.RIGHT, fill=tk.Y)
                
                if show_horizontal:
                    hscroll = tk.Scrollbar(self._container_frame, orient='horizontal', command=self._tk_widget.xview)
                    self._tk_widget.config(xscrollcommand=hscroll.set)
                    hscroll.pack(side=tk.BOTTOM, fill=tk.X)
                
                self._tk_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            else:
                self._container_frame = None
                self._tk_widget = tk.Text(self.master, height=self.Height//15, wrap=wrap_mode)
                
            self._tk_widget.insert('1.0', self._text_value)
            if self.ReadOnly:
                self._tk_widget.config(state='disabled')
            
            # Bind events for Text widget
            self._tk_widget.bind('<<Modified>>', self._on_text_changed)
            self._tk_widget.bind('<KeyRelease>', self._on_key_up)
            self._tk_widget.bind('<Button-1>', self._on_click)
            self._tk_widget.bind('<Double-Button-1>', self._on_double_click)
            self._tk_widget.bind('<Motion>', self._on_mouse_move)
        else:
            self._text_var = tk.StringVar(value=self._text_value)
            self._tk_widget = tk.Entry(self.master, textvariable=self._text_var)
            if self.PasswordChar:
                self._tk_widget.config(show=self.PasswordChar)
            elif self.UseSystemPasswordChar:
                self._tk_widget.config(show='*')
            if self.ReadOnly:
                self._tk_widget.config(state='readonly')
            if self.MaxLength > 0:
                vcmd = (self.master.register(self._validate_length), '%P')
                self._tk_widget.config(validate='key', validatecommand=vcmd)
            
            # Bind events for Entry widget
            self._text_var.trace('w', self._on_text_changed_entry)
            self._tk_widget.bind('<KeyRelease>', self._on_key_up)
            self._tk_widget.bind('<Button-1>', self._on_click)
            self._tk_widget.bind('<Double-Button-1>', self._on_double_click)
            self._tk_widget.bind('<Motion>', self._on_mouse_move)
        
        self._bind_common_events()
        
        # Apply style configurations
        config = {}
        if self.BackColor:
            config['bg'] = self.BackColor
        if self.ForeColor:
            config['fg'] = self.ForeColor
        if self.Font:
            config['font'] = self.Font
        if config:
            try:
                self._tk_widget.config(**config)
            except tk.TclError:
                pass  # Some widgets do not support all options
        
        # Apply alignment
        align_map = {
            HorizontalAlignment.Left: 'left',
            HorizontalAlignment.Right: 'right',
            HorizontalAlignment.Center: 'center',
            # String fallbacks
            'left': 'left', 'right': 'right', 'center': 'center'
        }
        
        # Only Entry widget supports justify. Text widget uses tags.
        if not self.Multiline:
            self._tk_widget.config(justify=align_map.get(self.TextAlign, 'left'))
        
        # Apply Enabled/Visible
        if not self.Enabled:
            self._tk_widget.config(state='disabled')
        if not self.Visible:
            self._tk_widget.place_forget()
        
        if self.AutoSize:
            self._apply_autosize_textbox()

        # Place the control (use container frame if it exists for multiline with scrollbars)
        if self.Multiline and hasattr(self, '_container_frame') and self._container_frame:
            # Place the container frame, not the text widget directly
            self._container_frame.place(x=self.Left, y=self.Top, width=self.Width, height=self.Height)
        else:
            self._place_control(self.Width, self.Height if not self.Multiline else self.Height)
        
        # Apply Dock and Anchor if they were specified in props
        if 'Dock' in defaults and defaults['Dock']:
            self.Dock = defaults['Dock']
        if 'Anchor' in defaults and defaults['Anchor']:
            self.Anchor = defaults['Anchor']
        
        # Auto-wire SelectAll on Click if enabled
        if self.SelectAllOnClick:
            def _select_all_on_click(sender=None, e=None):
                self.master.after_idle(self.SelectAll)
            self.Click = _select_all_on_click
            
        # AUTO-REGISTRATION: Automatically add to the parent container
        self._auto_register_with_parent()

    def _place_control(self, width=None, height=None):
        """Override to handle container frame for multiline with scrollbars."""
        # If we have a container frame (multiline with scrollbars), place it instead of the widget
        if self.Multiline and hasattr(self, '_container_frame') and self._container_frame:
            x_coord = self.Left
            y_coord = self.Top
            place_args = {
                'x': x_coord,
                'y': y_coord,
                'in_': self.master
            }
            if width is not None:
                place_args['width'] = width
            if height is not None:
                place_args['height'] = height
            try:
                self._container_frame.place(**place_args)
            except tk.TclError:
                pass
        else:
            # Use parent's implementation for single line or multiline without scrollbars
            super()._place_control(width, height)

    def _on_text_changed(self, event=None):
        """Handler for TextChanged event (Text widget)."""
        self.TextChanged()
        # Reset modified flag
        self._tk_widget.edit_modified(False)

    def _on_text_changed_entry(self, *args):
        """Handler for TextChanged event (Entry widget)."""
        self.TextChanged()

    def _on_mouse_move(self, event):
        """Handler for MouseMove event."""
        self.MouseMove(event.x, event.y)

    def _validate_length(self, new_text):
        return len(new_text) <= self.MaxLength

    def get_Text(self):
        """Gets the TextBox text."""
        if self.Multiline:
            # Check if widget is Text or Entry (fallback)
            if isinstance(self._tk_widget, tk.Text):
                return self._tk_widget.get('1.0', 'end-1c')
            else:
                return self._text_var.get()
        else:
            return self._text_var.get()

    def set_Text(self, new_text):
        """Sets the TextBox text."""
        self._text_value = new_text
        if self.Multiline:
            self._tk_widget.delete('1.0', 'end')
            self._tk_widget.insert('1.0', new_text)
        else:
            self._text_var.set(new_text)
        # Apply AutoSize if enabled
        if self.AutoSize:
            self._apply_autosize_textbox()
    
    def _apply_autosize_textbox(self):
        """Applies AutoSize specific behavior for TextBox.

        - For single-line TextBox: only adjusts height according to the font
        - For multiline TextBox: adjusts height to show all text
        """
        if not self.AutoSize or not self._tk_widget:
            return
        
        # Force geometry update to get correct dimensions
        try:
            self._tk_widget.update_idletasks()
        except:
            pass
        
        if self.Multiline:
            # For multiline, adjust height based on number of lines
            num_lines = int(self._tk_widget.index('end-1c').split('.')[0])
            # Estimate line height (approximately 20-25 pixels per line)
            line_height = 22
            required_height = num_lines * line_height + 10  # +10 for padding

            # Keep width, only adjust height
            self.Height = required_height
        else:
            # For a single line, only adjust height according to the font
            required_height = self._tk_widget.winfo_reqheight()
            self.Height = required_height
        
        # Apply MinimumSize constraints
        if self.MinimumSize:
            _, min_height = self.MinimumSize
            self.Height = max(self.Height, min_height)
        
        # Apply MaximumSize constraints
        if self.MaximumSize:
            _, max_height = self.MaximumSize
            if max_height > 0:
                self.Height = min(self.Height, max_height)
        
        # Reposicionar con nuevo tamaño
        if self.Visible:
            self._place_control(self.Width, self.Height)
    
    @property
    def Text(self):
        """Property getter for Text."""
        return self.get_Text()
    
    @Text.setter
    def Text(self, value):
        """Property setter for Text that calls set_Text()."""
        self.set_Text(value)

    @property
    def Lines(self):
        """Gets the lines of text in the TextBox."""
        return self.Text.split('\n')

    @Lines.setter
    def Lines(self, value):
        """Sets the lines of text in the TextBox."""
        if isinstance(value, list):
            self.Text = '\n'.join(value)
        else:
            self.Text = str(value)

    @property
    def Modified(self):
        """Gets a value indicating if the text has been modified by the user."""
        if self._tk_widget:
            try:
                return self._tk_widget.edit_modified()
            except:
                return False
        return False

    @Modified.setter
    def Modified(self, value):
        """Sets the modified flag."""
        if self._tk_widget:
            try:
                self._tk_widget.edit_modified(value)
            except:
                pass

    @property
    def SelectedText(self):
        """Gets or sets the selected text."""
        if not self._tk_widget:
            return ""
        
        try:
            if self.Multiline:
                return self._tk_widget.get("sel.first", "sel.last")
            else:
                return self._tk_widget.selection_get()
        except tk.TclError:
            return ""

    @SelectedText.setter
    def SelectedText(self, value):
        """Replaces the selected text with the specified value."""
        if not self._tk_widget:
            return
            
        try:
            if self.Multiline:
                if self._tk_widget.tag_ranges("sel"):
                    self._tk_widget.delete("sel.first", "sel.last")
                    self._tk_widget.insert("insert", value)
            else:
                if self._tk_widget.selection_present():
                    start = self._tk_widget.index("sel.first")
                    end = self._tk_widget.index("sel.last")
                    self._tk_widget.delete(start, end)
                    self._tk_widget.insert(start, value)
        except tk.TclError:
            pass

    @property
    def SelectionLength(self):
        """Gets or sets the number of characters selected."""
        if not self._tk_widget:
            return 0
            
        try:
            if self.Multiline:
                if not self._tk_widget.tag_ranges("sel"):
                    return 0
                text = self._tk_widget.get("sel.first", "sel.last")
                return len(text)
            else:
                if not self._tk_widget.selection_present():
                    return 0
                return self._tk_widget.index("sel.last") - self._tk_widget.index("sel.first")
        except tk.TclError:
            return 0

    @SelectionLength.setter
    def SelectionLength(self, value):
        """Sets the length of the selection."""
        # This is complex to implement perfectly without SelectionStart
        # Assuming SelectionStart is current cursor or start of selection
        pass

    @property
    def SelectionStart(self):
        """Gets or sets the starting point of text selected."""
        if not self._tk_widget:
            return 0
            
        try:
            if self.Multiline:
                if self._tk_widget.tag_ranges("sel"):
                    return len(self._tk_widget.get("1.0", "sel.first"))
                else:
                    return len(self._tk_widget.get("1.0", "insert"))
            else:
                if self._tk_widget.selection_present():
                    return self._tk_widget.index("sel.first")
                else:
                    return self._tk_widget.index("insert")
        except tk.TclError:
            return 0

    @SelectionStart.setter
    def SelectionStart(self, value):
        """Sets the starting point of text selected."""
        if not self._tk_widget:
            return
            
        if self.Multiline:
            # Convert index to line.col
            # This is tricky without knowing line lengths. 
            # Simplification: move to 1.0 + value chars
            pos = f"1.0 + {value} chars"
            self._tk_widget.mark_set("insert", pos)
        else:
            self._tk_widget.icursor(value)

    @property
    def TextLength(self):
        """Gets the length of text in the control."""
        return len(self.Text)

    def AppendText(self, text):
        """Appends text to the current text of the text box."""
        if self.Multiline:
            self._tk_widget.insert("end", text)
        else:
            self._tk_widget.insert("end", text)
        self.TextChanged()

    def Clear(self):
        """Clears all text from the text box."""
        self.Text = ""

    def ClearUndo(self):
        """Clears information about the most recent operation from the undo buffer."""
        if self.Multiline:
            try:
                self._tk_widget.edit_reset()
            except:
                pass

    def Copy(self):
        """Copies the current selection in the text box to the Clipboard."""
        if self._tk_widget:
            try:
                self._tk_widget.event_generate("<<Copy>>")
            except:
                pass

    def Cut(self):
        """Moves the current selection in the text box to the Clipboard."""
        if self._tk_widget:
            try:
                self._tk_widget.event_generate("<<Cut>>")
            except:
                pass

    def DeselectAll(self):
        """Deselects all text in the text box."""
        if self._tk_widget:
            try:
                if self.Multiline:
                    self._tk_widget.tag_remove("sel", "1.0", "end")
                else:
                    self._tk_widget.selection_clear()
            except:
                pass

    def Paste(self, text=None):
        """Replaces the current selection in the text box with the contents of the Clipboard."""
        if self._tk_widget:
            try:
                if text:
                    self.SelectedText = text
                else:
                    self._tk_widget.event_generate("<<Paste>>")
            except:
                pass

    def ScrollToCaret(self):
        """Scrolls the contents of the control to the current caret position."""
        if self._tk_widget:
            if self.Multiline:
                self._tk_widget.see("insert")
            else:
                self._tk_widget.xview_moveto(1) # Approximate

    def Select(self, start, length):
        """Selects a range of text in the text box."""
        if not self._tk_widget:
            return
            
        if self.Multiline:
            start_pos = f"1.0 + {start} chars"
            end_pos = f"1.0 + {start + length} chars"
            self._tk_widget.tag_add("sel", start_pos, end_pos)
            self._tk_widget.mark_set("insert", end_pos)
        else:
            self._tk_widget.selection_range(start, start + length)
            self._tk_widget.icursor(start + length)

    def SelectAll(self):
        """Selects all text in the text box."""
        if not self._tk_widget:
            return
            
        if self.Multiline:
            self._tk_widget.tag_add("sel", "1.0", "end")
            self._tk_widget.mark_set("insert", "end")
        else:
            self._tk_widget.selection_range(0, "end")
            self._tk_widget.icursor("end")

    def Undo(self):
        """Undoes the last edit operation in the text box."""
        if self.Multiline:
            try:
                self._tk_widget.edit_undo()
            except:
                pass


class RadioButton(ControlBase):
    """
    Represents a RadioButton control.
    
    Enables the user to select a single option from a group of choices when paired with other RadioButton controls.
    When a user selects one radio button within a group, the others clear automatically.
    """
    
    _group_vars = {}  # Class variable to store shared StringVars by group name
    
    def __init__(self, master_form, props=None):
        """Initializes a RadioButton.
        
        Args:
            master_form: The form or parent container
            props: Optional dictionary with initial properties
        """
        # Default values
        defaults = {
            'Left': 10,
            'Top': 140,
            'Width': 100,
            'Height': 25,
            'Name': '',
            'Text': 'Radio',
            'Group': None,
            'Checked': False,
            'Enabled': True,
            'Visible': True,
            'Font': None,
            'ForeColor': None,
            'BackColor': None,
            'TextAlign': ContentAlignment.MiddleLeft,
            'Appearance': Appearance.Normal,
            'AutoSize': False,
            'AutoCheck': True,
            'CheckAlign': ContentAlignment.MiddleLeft,
            'TabStop': True,
            'Dock': None,
            'Anchor': None
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Control", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Control")
        
        # Resolve the Tkinter widget and save the parent container
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Save the parent container for auto-registration
        self._parent_container = parent_container
        
        # VB Properties
        self.Name = defaults['Name']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self._text_value = defaults['Text']
        self.AutoCheck = defaults['AutoCheck']
        self.CheckAlign = defaults['CheckAlign']
        self.TabStop = defaults['TabStop']
        
        # Handle Group: if string, use shared StringVar; if StringVar, use it; else create new
        # In WinForms, grouping is automatic by container. Here we simulate it with 'Group' prop or container ID.
        # If no group specified, use parent container ID to group automatically like WinForms
        if defaults['Group']:
            if isinstance(defaults['Group'], str):
                group_name = defaults['Group']
                if group_name not in RadioButton._group_vars:
                    RadioButton._group_vars[group_name] = tk.StringVar()
                self.Group = RadioButton._group_vars[group_name]
            elif isinstance(defaults['Group'], tk.StringVar):
                self.Group = defaults['Group']
            else:
                self.Group = tk.StringVar()
        else:
            # Auto-group by parent container (WinForms behavior)
            container_id = str(id(parent_container))
            if container_id not in RadioButton._group_vars:
                RadioButton._group_vars[container_id] = tk.StringVar()
            self.Group = RadioButton._group_vars[container_id]
        
        self._checked_value = defaults['Checked']
        
        # Events
        self.CheckedChanged = lambda sender, e: None
        self.AppearanceChanged = lambda sender, e: None
        
        self.Font = defaults['Font']
        self.ForeColor = defaults['ForeColor']
        self.BackColor = defaults['BackColor']
        self.TextAlign = defaults['TextAlign']
        self.Appearance = defaults['Appearance']
        self.AutoSize = defaults['AutoSize']
        
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        
        # Create the Tkinter widget
        self._tk_widget = tk.Radiobutton(self.master, text=self._text_value, variable=self.Group, value=self._text_value)
        
        # Apply configurations
        config = {}
        if self.Font:
            config['font'] = self.Font
        if self.ForeColor:
            config['fg'] = self.ForeColor
        if self.BackColor:
            config['bg'] = self.BackColor
        
        # Map TextAlign to anchor
        anchor_map = {
            ContentAlignment.TopLeft: 'nw', ContentAlignment.TopCenter: 'n', ContentAlignment.TopRight: 'ne',
            ContentAlignment.MiddleLeft: 'w', ContentAlignment.MiddleCenter: 'center', ContentAlignment.MiddleRight: 'e',
            ContentAlignment.BottomLeft: 'sw', ContentAlignment.BottomCenter: 's', ContentAlignment.BottomRight: 'se',
            # String fallbacks
            'TopLeft': 'nw', 'TopCenter': 'n', 'TopRight': 'ne',
            'MiddleLeft': 'w', 'MiddleCenter': 'center', 'MiddleRight': 'e',
            'BottomLeft': 'sw', 'BottomCenter': 's', 'BottomRight': 'se',
            'w': 'w'
        }
        tk_anchor = anchor_map.get(self.TextAlign, 'w')
        if self.TextAlign in ['n', 's', 'e', 'w', 'nw', 'ne', 'sw', 'se', 'center']:
             tk_anchor = self.TextAlign
        config['anchor'] = tk_anchor
       
        if self.Appearance == "Button":
            config['indicatoron'] = 0
        if not self.Enabled:
            config['state'] = 'disabled'
        if config:
            self._tk_widget.config(**config)
        
        if self.AutoSize:
            self._apply_autosize()
            
        self._place_control(self.Width, self.Height)
        
        # Bind common events
        self._bind_common_events()
        
        # Set initial Checked
        if self._checked_value:
            self.Group.set(self._text_value)
        
        # Bind CheckedChanged
        self.Group.trace('w', self._on_checked_changed)
        
        # Apply Dock and Anchor if specified in props
        if defaults['Dock']:
            self.Dock = defaults['Dock']
        if defaults['Anchor']:
            self.Anchor = defaults['Anchor']
        
        # Auto-register with parent container if necessary
        self._auto_register_with_parent()

    def get_Checked(self):
        """Returns whether it is selected."""
        return self.Group.get() == self._text_value

    def set_Checked(self, value):
        """Sets whether it is selected."""
        self._checked_value = value
        if value:
            self.Group.set(self._text_value)
        elif self.get_Checked():
            # If setting to False and it was True, we need to clear the group selection
            # But RadioButtons in a group usually require one to be selected.
            # WinForms allows clearing by setting Checked=False.
            self.Group.set("") 

    def _on_checked_changed(self, *args):
        """Handler for CheckedChanged event."""
        old_checked = self._checked_value
        self._checked_value = self.get_Checked()
        if old_checked != self._checked_value:
            self.CheckedChanged(self, EventArgs.Empty)
    
    @property
    def Checked(self):
        """Property getter for Checked."""
        return self.get_Checked()
    
    @Checked.setter
    def Checked(self, value):
        """Property setter for Checked."""
        self.set_Checked(value)
        
    def PerformClick(self):
        """Generates a Click event for the control, simulating a click by a user."""
        if self.Enabled:
            self.Checked = True
            self.OnClick(EventArgs.Empty)

    @property
    def Appearance(self):
        return getattr(self, '_appearance', 'Normal')

    @Appearance.setter
    def Appearance(self, value):
        if getattr(self, '_appearance', None) != value:
            self._appearance = value
            if self._tk_widget:
                if value == 'Button':
                    self._tk_widget.config(indicatoron=0)
                else:
                    self._tk_widget.config(indicatoron=1)
            self.AppearanceChanged(self, EventArgs.Empty)

    @property
    def AutoCheck(self):
        return getattr(self, '_auto_check', True)

    @AutoCheck.setter
    def AutoCheck(self, value):
        self._auto_check = value
        # Tkinter handles this automatically via variable binding, 
        # disabling it would require intercepting clicks which is complex here.
        
    @property
    def CheckAlign(self):
        return getattr(self, '_check_align', ContentAlignment.MiddleLeft)

    @CheckAlign.setter
    def CheckAlign(self, value):
        self._check_align = value
        # Mapping WinForms alignment to Tkinter is limited
        # Tkinter Radiobutton has 'justify' and 'anchor' but indicator position is fixed to left usually
        pass
    
    @property
    def AutoSizeMode(self):
        """Basic controls always use GrowAndShrink mode."""
        return AutoSizeMode.GrowAndShrink
    
    @AutoSizeMode.setter
    def AutoSizeMode(self, value):
        """AutoSizeMode is not configurable for basic controls - always GrowAndShrink."""
        pass  # Ignore any attempts to change it
    
    @property
    def Text(self):
        """Property getter for Text in RadioButton."""
        return self._text_value
    
    @Text.setter
    def Text(self, value):
        """Property setter for Text in RadioButton."""
        self._text_value = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._tk_widget.config(text=value)
            # Update radio button value if necessary
            if hasattr(self, 'Group'):
                self._tk_widget.config(value=value)
            
            # Apply AutoSize if enabled
            if self.AutoSize:
                # Force geometry update before applying autosize
                try:
                    self._tk_widget.update_idletasks()
                except:
                    pass
                self._apply_autosize()
                # _apply_autosize() already calls _place_control()


class ComboBox(ControlBase):
    """Represents a ComboBox (drop-down)."""
    
    class ObjectCollection:
        def __init__(self, owner):
            self._owner = owner
            self._inner_list = []

        def Add(self, item):
            self._inner_list.append(item)
            self._owner._update_items()
            return len(self._inner_list) - 1

        def AddRange(self, items):
            self._inner_list.extend(items)
            self._owner._update_items()

        def Clear(self):
            self._inner_list.clear()
            self._owner._update_items()

        def Remove(self, item):
            if item in self._inner_list:
                self._inner_list.remove(item)
                self._owner._update_items()

        def RemoveAt(self, index):
            if 0 <= index < len(self._inner_list):
                del self._inner_list[index]
                self._owner._update_items()

        def Insert(self, index, item):
            self._inner_list.insert(index, item)
            self._owner._update_items()

        def Contains(self, item):
            return item in self._inner_list

        def IndexOf(self, item):
            try:
                return self._inner_list.index(item)
            except ValueError:
                return -1

        @property
        def Count(self):
            return len(self._inner_list)

        def __getitem__(self, index):
            return self._inner_list[index]

        def __setitem__(self, index, value):
            self._inner_list[index] = value
            self._owner._update_items()

        def __iter__(self):
            return iter(self._inner_list)

        def __len__(self):
            return len(self._inner_list)
            
        def __repr__(self):
            return repr(self._inner_list)
            
        def sort(self, key=None, reverse=False):
            self._inner_list.sort(key=key, reverse=reverse)
            self._owner._update_items()
            
        def index(self, item, start=0, end=9223372036854775807):
            return self._inner_list.index(item, start, end)

        # List compatibility aliases
        def append(self, item): return self.Add(item)
        def clear(self): self.Clear()
        def remove(self, item): self.Remove(item)
        def insert(self, index, item): self.Insert(index, item)
        def extend(self, items): self.AddRange(items)
    
    def __init__(self, master_form, props=None):
        """Initializes a ComboBox.

        Args:
            master_form: The parent form or container
            props: Optional dictionary with initial properties
                   Use {'UseSystemStyles': True} to apply system styles automatically
        """
        # Default values
        defaults = {
            'Left': 10,
            'Top': 110,
            'Width': 200,
            'Name': '',
            'Items': None,
            'DataSource': None,
            'DisplayMember': '',
            'ValueMember': '',
            'SelectedItem': None,
            'SelectedValue': None,
            'SelectedIndex': -1,
            'Text': '',
            'DropDownStyle': ComboBoxStyle.DropDown, # Simple, DropDown, DropDownList
            'DroppedDown': False,
            'MaxDropDownItems': 8,
            'MaxLength': 0,
            'Enabled': True,
            'Visible': True,
            'Font': None,
            'ForeColor': None,
            'BackColor': None,
            'AutoSize': False,
            'AutoCompleteMode': AutoCompleteMode.None_,
            'AutoCompleteSource': AutoCompleteSource.None_,
            'IntegralHeight': True,
            'ItemHeight': 13,
            'Sorted': False
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Control", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Control")
        
        # Resolve the Tkinter widget and keep the original parent container
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Store the parent container for auto-registration
        self._parent_container = parent_container
        
        # Propiedades VB
        self.Name = defaults['Name']
        self._items = self.ObjectCollection(self)
        if defaults['Items']:
            self._items.AddRange(defaults['Items'])
        self._data_source = defaults['DataSource']
        self._display_member = defaults['DisplayMember']
        self._value_member = defaults['ValueMember']
        self._selected_index = defaults['SelectedIndex']
        self._text_value = defaults['Text']
        self._drop_down_style = defaults['DropDownStyle']
        self._dropped_down = defaults['DroppedDown']
        self.MaxDropDownItems = defaults['MaxDropDownItems']
        self.MaxLength = defaults['MaxLength']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.Font = defaults['Font']
        self.ForeColor = defaults['ForeColor']
        self.BackColor = defaults['BackColor']
        self.AutoSize = defaults['AutoSize']
        self.AutoCompleteMode = defaults['AutoCompleteMode']
        self.AutoCompleteSource = defaults['AutoCompleteSource']
        self.IntegralHeight = defaults['IntegralHeight']
        self.ItemHeight = defaults['ItemHeight']
        self.Sorted = defaults['Sorted']
        
        # Eventos VB (callbacks)
        self.SelectedIndexChanged = lambda sender, e: None
        self.SelectionChangeCommitted = lambda sender, e: None
        self.TextChanged = lambda sender, e: None
        self.TextUpdate = lambda sender, e: None
        self.DropDown = lambda sender, e: None
        self.DropDownClosed = lambda sender, e: None
        self.Validating = lambda sender, e: None
        self.DrawItem = lambda sender, e: None
        self.MeasureItem = lambda sender, e: None
        self.DataSourceChanged = lambda sender, e: None
        self.DisplayMemberChanged = lambda sender, e: None
        self.ValueMemberChanged = lambda sender, e: None
        self.SelectedValueChanged = lambda sender, e: None
        
        self.Width = defaults['Width']
        self.Height = 21  # Standard height
        
        # Internal state
        self._updating = False
        self._ignore_change = False
        
        # If DataSource, populate Items
        if self._data_source:
            self._populate_from_datasource()
        
        self._selected_var = tk.StringVar(value=self._text_value)
        
        # Create the Tkinter widget
        # Map DropDownStyle to state
        state = 'normal'
        if self._drop_down_style == ComboBoxStyle.DropDownList:
            state = 'readonly'
        elif self._drop_down_style == ComboBoxStyle.Simple:
            # Tkinter Combobox doesn't support 'Simple' (always visible list), fallback to normal
            state = 'normal'
        # String fallback
        elif self._drop_down_style == 'DropDownList':
            state = 'readonly'
            
        self._tk_widget = ttk.Combobox(self.master, textvariable=self._selected_var, values=list(self._items), state=state)
        self._tk_widget.config(height=self.MaxDropDownItems)
        
        # Update items if they were added before widget creation
        self._update_items()
        
        if self.MaxLength > 0:
            vcmd = (self.master.register(self._validate_length), '%P')
            self._tk_widget.config(validate='key', validatecommand=vcmd)
        
        # Apply styles
        config = {}
        if self.Font:
            config['font'] = self.Font
        if self.BackColor:
            config['background'] = self.BackColor
        if self.ForeColor:
            config['foreground'] = self.ForeColor
        if config:
            try:
                self._tk_widget.config(**config)
            except tk.TclError:
                pass
        
        # Apply Enabled/Visible
        if not self.Enabled:
            self._tk_widget.config(state='disabled')
        if not self.Visible:
            self._tk_widget.place_forget()
        
        # Apply AutoSize if enabled
        if self.AutoSize:
            self._apply_autosize()
        
        self._place_control(self.Width, self.Height)
        
        # Apply Dock and Anchor if they were specified in props
        if 'Dock' in defaults and defaults['Dock']:
            self.Dock = defaults['Dock']
        if 'Anchor' in defaults and defaults['Anchor']:
            self.Anchor = defaults['Anchor']
        
        # Bind events
        self._tk_widget.bind('<<ComboboxSelected>>', self._on_selected_index_changed)
        # self._tk_widget.bind('<Post>', self._on_drop_down)
        self._tk_widget.bind('<Unmap>', self._on_drop_down_closed) # Approximation
        
        self._selected_var.trace('w', self._on_text_changed)
        
        self._tk_widget.bind('<FocusIn>', self._on_enter)
        self._tk_widget.bind('<FocusOut>', self._on_leave)
        self._tk_widget.bind('<Key>', self._on_key_down)
        self._tk_widget.bind('<KeyPress>', self._on_key_press)
        
        # Set initial selection
        if self._selected_index >= 0 and self._selected_index < len(self._items):
            self._tk_widget.current(self._selected_index)
        elif defaults['SelectedItem']:
            try:
                idx = self._items.index(defaults['SelectedItem'])
                self._tk_widget.current(idx)
            except ValueError:
                pass
        
        # Auto-register with the parent container if necessary
        self._auto_register_with_parent()

    def _update_items(self):
        if hasattr(self, '_tk_widget') and self._tk_widget is not None:
            # Convert to list for Tkinter
            self._tk_widget['values'] = list(self._items)

    @property
    def Items(self):
        return self._items

    @Items.setter
    def Items(self, value):
        self._items.Clear()
        if value:
            self._items.AddRange(value)

    @property
    def DataSource(self):
        return self._data_source

    @DataSource.setter
    def DataSource(self, value):
        if self._data_source != value:
            self._data_source = value
            self._populate_from_datasource()
            self.DataSourceChanged(self, None)

    @property
    def DisplayMember(self):
        return self._display_member

    @DisplayMember.setter
    def DisplayMember(self, value):
        if self._display_member != value:
            self._display_member = value
            self._populate_from_datasource()
            self.DisplayMemberChanged(self, None)

    @property
    def ValueMember(self):
        return self._value_member

    @ValueMember.setter
    def ValueMember(self, value):
        if self._value_member != value:
            self._value_member = value
            self.ValueMemberChanged(self, None)

    @property
    def DropDownStyle(self):
        return self._drop_down_style

    @DropDownStyle.setter
    def DropDownStyle(self, value):
        self._drop_down_style = value
        if value == 'DropDownList':
            self._tk_widget.config(state='readonly')
        else:
            self._tk_widget.config(state='normal')
        self.OnDropDownStyleChanged(None)

    def OnDropDownStyleChanged(self, e):
        pass # Event placeholder

    def _populate_from_datasource(self):
        """Populates Items from DataSource using DisplayMember."""
        if self._data_source:
            if self._display_member:
                self.Items = [getattr(item, self._display_member, str(item)) for item in self._data_source]
            else:
                self.Items = [str(item) for item in self._data_source]
        else:
            self.Items = []

    def _validate_length(self, new_text):
        return len(new_text) <= self.MaxLength

    @property
    def SelectedItem(self):
        """Gets or sets the selected item."""
        idx = self._tk_widget.current()
        if idx >= 0 and idx < len(self._items):
            if self._data_source:
                return self._data_source[idx]
            return self._items[idx]
        return None

    @SelectedItem.setter
    def SelectedItem(self, item):
        try:
            if self._data_source:
                idx = self._data_source.index(item)
            else:
                idx = self._items.index(item)
            self.SelectedIndex = idx
        except ValueError:
            pass

    @property
    def SelectedValue(self):
        """Gets or sets the ValueMember value of the selected item."""
        if self._data_source and self._value_member:
            item = self.SelectedItem
            if item:
                return getattr(item, self._value_member, None)
        return self.SelectedItem

    @SelectedValue.setter
    def SelectedValue(self, value):
        if self._data_source and self._value_member:
            for i, item in enumerate(self._data_source):
                if getattr(item, self._value_member, None) == value:
                    self.SelectedIndex = i
                    return
        self.SelectedItem = value

    @property
    def SelectedIndex(self):
        """Gets or sets the index of the selected item."""
        return self._tk_widget.current()

    @SelectedIndex.setter
    def SelectedIndex(self, index):
        if index >= -1 and index < len(self._items):
            self._tk_widget.current(index)
            self._on_selected_index_changed()

    @property
    def SelectedText(self):
        """Gets the selected text in the editable portion."""
        if self.DropDownStyle == 'DropDownList': return ""
        try:
            return self._tk_widget.selection_get()
        except:
            return ""

    @SelectedText.setter
    def SelectedText(self, value):
        # Not easily supported in ttk.Combobox
        pass

    @property
    def SelectionStart(self):
        if self.DropDownStyle == 'DropDownList': return 0
        return self._tk_widget.index("insert")

    @SelectionStart.setter
    def SelectionStart(self, value):
        if self.DropDownStyle != 'DropDownList':
            self._tk_widget.icursor(value)

    @property
    def SelectionLength(self):
        # Not directly supported
        return 0

    @SelectionLength.setter
    def SelectionLength(self, value):
        pass

    def _on_selected_index_changed(self, event=None):
        """Handler for SelectedIndexChanged event."""
        if self._ignore_change: return
        self.SelectedIndexChanged(self, None)
        self.SelectionChangeCommitted(self, None)
        self.SelectedValueChanged(self, None)

    def _on_text_changed(self, *args):
        """Handler for TextChanged event."""
        if self._ignore_change: return
        self.TextUpdate(self, None)
        self.TextChanged(self, None)

    def _on_drop_down(self, event):
        self.DroppedDown = True
        self.DropDown(self, None)

    def _on_drop_down_closed(self, event):
        # This is tricky in Tkinter, Unmap might fire for other reasons
        self.DroppedDown = False
        self.DropDownClosed(self, None)

    def _on_enter(self, event):
        self.Enter(self, None)

    def _on_leave(self, event):
        self.Leave(self, None)
        self.Validating(self, None)

    def _on_key_down(self, event):
        self.KeyDown(self, event.keysym)

    def _on_key_press(self, event):
        self.KeyPress(self, event.char)
    
    @property
    def Text(self):
        """Property getter for Text in ComboBox."""
        return self._tk_widget.get()

    @Text.setter
    def Text(self, value):
        """Property setter for Text in ComboBox."""
        self._text_value = value
        self._tk_widget.set(value)

    def BeginUpdate(self):
        self._updating = True
        self._ignore_change = True

    def EndUpdate(self):
        self._updating = False
        self._ignore_change = False
        self._update_items()

    def FindString(self, s, start_index=-1):
        s = s.lower()
        for i in range(start_index + 1, len(self._items)):
            if str(self._items[i]).lower().startswith(s):
                return i
        # Wrap around
        if start_index != -1:
            for i in range(0, start_index + 1):
                if str(self._items[i]).lower().startswith(s):
                    return i
        return -1

    def FindStringExact(self, s, start_index=-1):
        s = s.lower()
        for i in range(start_index + 1, len(self._items)):
            if str(self._items[i]).lower() == s:
                return i
        if start_index != -1:
            for i in range(0, start_index + 1):
                if str(self._items[i]).lower() == s:
                    return i
        return -1
        
    def Select(self, start, length):
        if self.DropDownStyle != 'DropDownList':
            self._tk_widget.selection_range(start, start + length)


class CheckBox(ControlBase):
    """Represents a CheckBox."""
    
    def __init__(self, master_form, props=None):
        """Initializes a CheckBox.

        Args:
            master_form: The parent form or container
            props: Optional dictionary with initial properties
        """
        # Default values
        defaults = {
            'Left': 10,
            'Top': 140,
            'Width': 100,
            'Height': 25,
            'Name': '',
            'Text': 'CheckBox',
            'Checked': False,
            'CheckState': CheckState.Unchecked,
            'ThreeState': False,
            'Enabled': True,
            'Visible': True,
            'Font': None,
            'ForeColor': None,
            'BackColor': None,
            'TextAlign': ContentAlignment.MiddleLeft,
            'Appearance': Appearance.Normal,
            'AutoSize': False,
            'AutoCheck': True,
            'CheckAlign': ContentAlignment.MiddleLeft,
            'FlatStyle': FlatStyle.Standard
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Control", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Control")
        
        # Resolve the Tkinter widget and store the parent container
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Store the parent container for auto-registration
        self._parent_container = parent_container
        
        self.Name = defaults['Name']
        self._text_value = defaults['Text']
        
        # Initialize state
        self._three_state = defaults['ThreeState']
        self._auto_check = defaults['AutoCheck']
        self._check_align = defaults['CheckAlign']
        self._appearance = defaults['Appearance']
        self._flat_style = defaults['FlatStyle']
        
        # Handle initial check state
        initial_state = defaults['CheckState']
        if defaults['Checked'] and initial_state == CheckState.Unchecked:
            initial_state = CheckState.Checked
        self._checkstate_value = initial_state
        
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.Font = defaults['Font']
        self.ForeColor = defaults['ForeColor']
        self.BackColor = defaults['BackColor']
        self.TextAlign = defaults['TextAlign']
        self.AutoSize = defaults['AutoSize']
        
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        
        self.Location = (self.Left, self.Top)
        
        # Variable based on ThreeState (Always use IntVar for flexibility)
        self._state_var = tk.IntVar(value=self._checkstate_value)
        
        # VB events
        self.CheckedChanged = lambda sender, e: None
        self.CheckStateChanged = lambda sender, e: None
        self.AppearanceChanged = lambda sender, e: None

        # Create the Tkinter widget
        # Note: onvalue/offvalue/tristatevalue must match CheckState values (0, 1, 2)
        self._tk_widget = tk.Checkbutton(
            self.master, 
            text=self._text_value, 
            variable=self._state_var, 
            command=self._on_check_click,
            onvalue=int(CheckState.Checked),
            offvalue=int(CheckState.Unchecked)
        )
        
        if self._three_state:
            self._tk_widget.config(tristatevalue=int(CheckState.Indeterminate))
        
        # Apply configurations
        self._apply_visual_config()
        
        # Place if visible
        if self.Visible:
            if self.AutoSize:
                self._apply_autosize()
            self._place_control(self.Width, self.Height)
        else:
            self._tk_widget.place_forget()
            
        # Apply Dock and Anchor if they were specified in props
        if 'Dock' in defaults and defaults['Dock']:
            self.Dock = defaults['Dock']
        if 'Anchor' in defaults and defaults['Anchor']:
            self.Anchor = defaults['Anchor']
        
        # Auto-register with the parent container if necessary
        self._auto_register_with_parent()

    def _apply_visual_config(self):
        """Applies visual properties to the widget."""
        if not self._tk_widget: return
        
        config = {}
        if self.Font:
            config['font'] = self.Font
        if self.ForeColor:
            config['fg'] = self.ForeColor
        if self.BackColor:
            config['bg'] = self.BackColor
            
        # Map TextAlign to anchor
        # Simplified mapping
        anchor_map = {
            ContentAlignment.TopLeft: 'nw', ContentAlignment.TopCenter: 'n', ContentAlignment.TopRight: 'ne',
            ContentAlignment.MiddleLeft: 'w', ContentAlignment.MiddleCenter: 'center', ContentAlignment.MiddleRight: 'e',
            ContentAlignment.BottomLeft: 'sw', ContentAlignment.BottomCenter: 's', ContentAlignment.BottomRight: 'se',
            # String fallbacks
            'TopLeft': 'nw', 'TopCenter': 'n', 'TopRight': 'ne',
            'MiddleLeft': 'w', 'MiddleCenter': 'center', 'MiddleRight': 'e',
            'BottomLeft': 'sw', 'BottomCenter': 's', 'BottomRight': 'se'
        }
        # Default to 'w' (MiddleLeft) if not found or if it's a simple string like 'w'
        tk_anchor = anchor_map.get(self.TextAlign, 'w')
        if self.TextAlign in ['n', 's', 'e', 'w', 'nw', 'ne', 'sw', 'se', 'center']:
             tk_anchor = self.TextAlign
             
        config['anchor'] = tk_anchor
        
        if self.Appearance == "Button":
            config['indicatoron'] = 0
        else:
            config['indicatoron'] = 1
            
        if not self.Enabled:
            config['state'] = 'disabled'
        else:
            config['state'] = 'normal'
            
        self._tk_widget.config(**config)

    def _apply_autosize(self):
        """Applies autosize logic."""
        if not self.AutoSize or not self._tk_widget:
            return
        
        # 1. Force widget update to get correct dimensions
        self._tk_widget.update_idletasks()
        
        # 2. Get required size from widget
        required_width = self._tk_widget.winfo_reqwidth()
        required_height = self._tk_widget.winfo_reqheight()
        
        # 3. Apply AutoSizeMode logic
        if self.AutoSizeMode == AutoSizeMode.GrowOnly and self._original_size:
            orig_w, orig_h = self._original_size
            required_width = max(required_width, orig_w)
            required_height = max(required_height, orig_h)
        
        # 4. Apply MinimumSize restrictions
        if self.MinimumSize:
            min_width, min_height = self.MinimumSize
            required_width = max(required_width, min_width)
            required_height = max(required_height, min_height)
        
        # 5. Apply MaximumSize restrictions
        if self.MaximumSize:
            max_width, max_height = self.MaximumSize
            if max_width > 0:
                required_width = min(required_width, max_width)
            if max_height > 0:
                required_height = min(required_height, max_height)
        
        # 6. Adjust position if Anchored to Right/Bottom
        if hasattr(self, '_apply_autosize_anchor_adjustment'):
            self._apply_autosize_anchor_adjustment(required_width, required_height)
        
        # 7. Update dimensions
        self.Width = required_width
        self.Height = required_height
        
        # 8. Reposition with the new size (always, visible or not)
        if hasattr(self, '_place_control'):
            self._place_control(required_width, required_height)
        
        # 9. Notify parent container that this control's size changed
        self._notify_parent_layout_changed()

    def _on_check_click(self):
        """Handles the checkbox click."""
        if not self.AutoCheck:
            # Revert change
            self._state_var.set(self._checkstate_value)
            return

        # Handle ThreeState cycling
        if self.ThreeState:
            # Tkinter toggles 0 <-> 1. We need to handle 2.
            # Cycle: Unchecked(0) -> Checked(1) -> Indeterminate(2) -> Unchecked(0)
            
            # Current value in var is what Tkinter set it to.
            # We calculate next state based on stored _checkstate_value
            next_state = CheckState.Unchecked
            if self._checkstate_value == CheckState.Unchecked: # Unchecked
                next_state = CheckState.Checked # Checked
            elif self._checkstate_value == CheckState.Checked: # Checked
                next_state = CheckState.Indeterminate # Indeterminate
            else: # Indeterminate
                next_state = CheckState.Unchecked # Unchecked
            
            self._state_var.set(next_state)
            
        # Update internal state and fire events
        new_state = self._state_var.get()
        
        if new_state != self._checkstate_value:
            old_checked = (self._checkstate_value != CheckState.Unchecked)
            self._checkstate_value = new_state
            new_checked = (self._checkstate_value != CheckState.Unchecked)
            
            self.OnCheckStateChanged(EventArgs.Empty)
            
            if old_checked != new_checked:
                self.OnCheckedChanged(EventArgs.Empty)
                
        self.Click()

    def OnCheckedChanged(self, e):
        """Raises the CheckedChanged event."""
        self.CheckedChanged(self, e)

    def OnCheckStateChanged(self, e):
        """Raises the CheckStateChanged event."""
        self.CheckStateChanged(self, e)
        
    def OnAppearanceChanged(self, e):
        """Raises the AppearanceChanged event."""
        self.AppearanceChanged(self, e)

    @property
    def AutoCheck(self):
        return self._auto_check

    @AutoCheck.setter
    def AutoCheck(self, value):
        self._auto_check = value

    @property
    def Appearance(self):
        return self._appearance

    @Appearance.setter
    def Appearance(self, value):
        if self._appearance != value:
            self._appearance = value
            self._apply_visual_config()
            self.OnAppearanceChanged(EventArgs.Empty)

    @property
    def CheckAlign(self):
        return self._check_align

    @CheckAlign.setter
    def CheckAlign(self, value):
        self._check_align = value
        # Visual implementation limited in Tkinter Checkbutton
        
    @property
    def Checked(self):
        """Gets or sets a value indicating whether the CheckBox is in the checked state."""
        return self._checkstate_value != CheckState.Unchecked # Checked or Indeterminate

    @Checked.setter
    def Checked(self, value):
        if value != self.Checked:
            self.CheckState = CheckState.Checked if value else CheckState.Unchecked

    @property
    def CheckState(self):
        """Gets or sets the state of the CheckBox."""
        return self._checkstate_value

    @CheckState.setter
    def CheckState(self, value):
        if self._checkstate_value != value:
            self._checkstate_value = value
            self._state_var.set(value)
            self.OnCheckStateChanged(EventArgs.Empty)
            self.OnCheckedChanged(EventArgs.Empty)

    @property
    def ThreeState(self):
        """Gets or sets a value indicating whether the CheckBox will allow three check states rather than two."""
        return self._three_state

    @ThreeState.setter
    def ThreeState(self, value):
        self._three_state = value
        if self._tk_widget:
            if value:
                self._tk_widget.config(tristatevalue=CheckState.Indeterminate)
            else:
                self._tk_widget.config(tristatevalue="")
                # If currently Indeterminate, switch to Checked
                if self._checkstate_value == CheckState.Indeterminate:
                    self.CheckState = CheckState.Checked
    
    @property
    def AutoSizeMode(self):
        """Basic controls always use GrowAndShrink mode."""
        return AutoSizeMode.GrowAndShrink
    
    @AutoSizeMode.setter
    def AutoSizeMode(self, value):
        """AutoSizeMode is not configurable for basic controls - always GrowAndShrink."""
        pass  # Ignore any attempts to change it
    
    @property
    def Text(self):
        """Property getter for Text on the CheckBox."""
        return self._text_value
    
    @Text.setter
    def Text(self, value):
        """Property setter for Text in CheckBox."""
        self._text_value = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._tk_widget.config(text=value)
            
            # Apply AutoSize if enabled
            if self.AutoSize:
                # Force geometry update before applying autosize
                try:
                    self._tk_widget.update_idletasks()
                except:
                    pass
                self._apply_autosize()
                # _apply_autosize() already calls _place_control()


############# More Controls #############

class ToolTip:
    """
    Class for creating tooltips (contextual information on mouse hover).
    
    Usage - Option 1: tooltip = ToolTip(widget); tooltip.Text = "Help text"
    Usage - Option 2: tooltip = ToolTip(widget, {'Text': 'Help text', 'Delay': 1000, 'BgColor': 'yellow'})
    Usage - Option 3: tooltip = ToolTip(widget, {'UseSystemStyles': True})  # Uses system colors
    """
    
    def __init__(self, widget, props=None):
        """Initializes a ToolTip for a widget.
        
        Args:
            widget: Tkinter widget to associate the tooltip with
            props: Optional dictionary with properties (Text, Delay, BgColor, FgColor, BorderColor, BorderWidth, Font)
                   Use {'UseSystemStyles': True} to automatically apply system styles
        """
        defaults = {
            'Text': "",
            'Delay': 500,
            'BgColor': None,
            'FgColor': None,
            'BorderColor': "black",
            'BorderWidth': 1,
            'Font': None
        }
        
        if props:
            # Extract UseSystemStyles before updating defaults
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            # Apply system styles if enabled (use Info colors)
            if use_system_styles:
                if defaults['BgColor'] is None:
                    defaults['BgColor'] = SystemColors.Info
                if defaults['FgColor'] is None:
                    defaults['FgColor'] = SystemColors.InfoText
                if defaults['Font'] is None:
                    defaults['Font'] = SystemFonts.DefaultFont
            # Aliases for compatibility
            if 'text' in props:
                defaults['Text'] = props['text']
            if 'bg' in props:
                defaults['BgColor'] = props['bg']
            if 'fg' in props:
                defaults['FgColor'] = props['fg']
            if 'delay' in props:
                defaults['Delay'] = props['delay']
            if 'bordercolor' in props:
                defaults['BorderColor'] = props['bordercolor']
            if 'borderwidth' in props:
                defaults['BorderWidth'] = props['borderwidth']
            if 'font' in props:
                defaults['Font'] = props['font']
        
        # Apply default values if still None
        if defaults['BgColor'] is None:
            defaults['BgColor'] = "lightyellow"
        if defaults['FgColor'] is None:
            defaults['FgColor'] = "black"
        if defaults['Font'] is None:
            defaults['Font'] = ("Segoe UI", 9)
        
        self.widget = widget
        self.text = defaults['Text']
        self.delay = defaults['Delay']
        self.bg = defaults['BgColor']
        self.fg = defaults['FgColor']
        self.bordercolor = defaults['BorderColor']
        self.borderwidth = defaults['BorderWidth']
        self.font = defaults['Font']
        self.Tag = None
        
        self._tooltip_window = None
        self._scheduled_id = None
        
        # Bind events
        self.widget.bind('<Enter>', self._on_enter)
        self.widget.bind('<Leave>', self._on_leave)
        self.widget.bind('<Motion>', self._on_motion)

    @property
    def Tag(self):
        """Gets or sets the object that contains data about the control."""
        return self._tag

    @Tag.setter
    def Tag(self, value):
        self._tag = value
    
    def _on_enter(self, event):
        """Handles mouse enter event."""
        self._schedule_tooltip(event)
    
    def _on_leave(self, event):
        """Handles mouse leave event."""
        self._cancel_tooltip()
        self._hide_tooltip()
    
    def _on_motion(self, event):
        """Handles mouse motion event."""
        if self._tooltip_window:
            # Update tooltip position
            x = event.x_root + 15
            y = event.y_root + 10
            self._tooltip_window.wm_geometry(f"+{x}+{y}")
    
    def _schedule_tooltip(self, event):
        """Schedules the appearance of the tooltip after the delay."""
        self._cancel_tooltip()
        if self.text:
            self._scheduled_id = self.widget.after(
                self.delay, 
                lambda: self._show_tooltip(event)
            )
    
    def _cancel_tooltip(self):
        """Cancels the scheduled appearance of the tooltip."""
        if self._scheduled_id:
            self.widget.after_cancel(self._scheduled_id)
            self._scheduled_id = None
    
    def _show_tooltip(self, event):
        """Shows the tooltip."""
        if self._tooltip_window or not self.text:
            return
        
        x = event.x_root + 15
        y = event.y_root + 10
        
        self._tooltip_window = tk.Toplevel(self.widget)
        self._tooltip_window.wm_overrideredirect(True)
        self._tooltip_window.wm_geometry(f"+{x}+{y}")
        
        # Create label with the text
        label = tk.Label(
            self._tooltip_window,
            text=self.text,
            background=self.bg,
            foreground=self.fg,
            relief="solid",
            borderwidth=self.borderwidth,
            font=self.font,
            padx=5,
            pady=2,
            justify='left'
        )
        label.pack()
        
        # Configure border
        if self.bordercolor != self.bg:
            label.config(highlightbackground=self.bordercolor, highlightthickness=self.borderwidth)
    
    def _hide_tooltip(self):
        """Hides the tooltip."""
        if self._tooltip_window:
            self._tooltip_window.destroy()
            self._tooltip_window = None
    
    def update_text(self, new_text):
        """Updates the tooltip text."""
        self.text = new_text
        if self._tooltip_window:
            # If it is visible, hide it and show it again with the new text
            self._hide_tooltip()


class LinkLabel(Label):
    """
    Represents a Windows Forms LinkLabel control.
    """
    
    class Link:
        """Represents a link within a LinkLabel."""
        def __init__(self, start=0, length=0, link_data=None):
            self.Start = start
            self.Length = length
            self.LinkData = link_data
            self.Enabled = True
            self.Name = ""
            self.Visited = False
            self.Tag = None
            self.Description = ""

    class LinkCollection:
        """Collection of links for LinkLabel."""
        def __init__(self, owner):
            self._owner = owner
            self._links = []

        def Add(self, start, length, link_data=None):
            link = LinkLabel.Link(start, length, link_data)
            self._links.append(link)
            return link
            
        def AddLink(self, link):
            self._links.append(link)
            return link

        def Clear(self):
            self._links.clear()

        def Remove(self, link):
            if link in self._links:
                self._links.remove(link)

        def __getitem__(self, index):
            return self._links[index]

        def __len__(self):
            return len(self._links)
        
        def __iter__(self):
            return iter(self._links)

    def __init__(self, master_form, props=None):
        defaults = {
            'LinkColor': 'blue',
            'ActiveLinkColor': 'red',
            'VisitedLinkColor': 'purple',
            'DisabledLinkColor': 'gray',
            'LinkBehavior': 'SystemDefault', # 'SystemDefault', 'AlwaysUnderline', 'HoverUnderline', 'NeverUnderline'
            'LinkVisited': False,
            'LinkArea': None # (start, length)
        }
        if props:
            defaults.update(props)
            
        super().__init__(master_form, defaults)
        
        self._link_color = defaults['LinkColor']
        self._active_link_color = defaults['ActiveLinkColor']
        self._visited_link_color = defaults['VisitedLinkColor']
        self._disabled_link_color = defaults['DisabledLinkColor']
        self._link_behavior = defaults['LinkBehavior']
        self._link_visited = defaults['LinkVisited']
        
        self._links = LinkLabel.LinkCollection(self)
        
        # Handle LinkArea
        if defaults['LinkArea']:
            self.LinkArea = defaults['LinkArea']
        else:
            # Default: whole text is a link
            self._links.Add(0, len(self.Text))
            self._link_area = (0, len(self.Text))
        
        self.LinkClicked = lambda sender, e: None
        
        self._apply_link_style()
        self._bind_link_events()

    @property
    def ActiveLinkColor(self):
        return self._active_link_color

    @ActiveLinkColor.setter
    def ActiveLinkColor(self, value):
        self._active_link_color = value

    @property
    def DisabledLinkColor(self):
        return self._disabled_link_color

    @DisabledLinkColor.setter
    def DisabledLinkColor(self, value):
        self._disabled_link_color = value
        if not self.Enabled:
            self._apply_link_style()

    @property
    def LinkBehavior(self):
        return self._link_behavior

    @LinkBehavior.setter
    def LinkBehavior(self, value):
        self._link_behavior = value
        self._apply_link_style()

    @property
    def LinkColor(self):
        return self._link_color

    @LinkColor.setter
    def LinkColor(self, value):
        self._link_color = value
        self._apply_link_style()

    @property
    def LinkVisited(self):
        return self._link_visited

    @LinkVisited.setter
    def LinkVisited(self, value):
        self._link_visited = value
        self._apply_link_style()

    @property
    def VisitedLinkColor(self):
        return self._visited_link_color

    @VisitedLinkColor.setter
    def VisitedLinkColor(self, value):
        self._visited_link_color = value
        self._apply_link_style()
        
    @property
    def LinkArea(self):
        return self._link_area

    @LinkArea.setter
    def LinkArea(self, value):
        self._link_area = value
        self._links.Clear()
        if value:
            self._links.Add(value[0], value[1])

    @property
    def Links(self):
        return self._links
        
    @property
    def Enabled(self):
        return self._enabled
        
    @Enabled.setter
    def Enabled(self, value):
        self._enabled = value
        if self._tk_widget:
            state = 'normal' if value else 'disabled'
            self._tk_widget.config(state=state)
        self._apply_link_style()

    def _apply_link_style(self):
        if self._tk_widget:
            if not self.Enabled:
                color = self.DisabledLinkColor
                cursor = "arrow"
            else:
                color = self.VisitedLinkColor if self.LinkVisited else self.LinkColor
                cursor = "hand2"
            
            self._tk_widget.config(fg=color, cursor=cursor)
            
            # Font underline logic
            try:
                from tkinter import font
                current_font = self._tk_widget.cget("font")
                f = font.Font(font=current_font)
                
                should_underline = False
                if self.LinkBehavior == 'AlwaysUnderline':
                    should_underline = True
                elif self.LinkBehavior == 'NeverUnderline':
                    should_underline = False
                elif self.LinkBehavior == 'SystemDefault':
                    should_underline = True
                # HoverUnderline handled in events
                
                f.configure(underline=should_underline)
                self._tk_widget.config(font=f)
            except:
                pass
            
    def _bind_link_events(self):
        if self._tk_widget:
            self._tk_widget.bind("<Button-1>", self._on_link_click)
            self._tk_widget.bind("<Enter>", self._on_mouse_enter)
            self._tk_widget.bind("<Leave>", self._on_mouse_leave)

    def _on_link_click(self, event):
        if not self.Enabled:
            return
            
        self.LinkVisited = True
        self._apply_link_style()
        
        # Pass the first link in collection as the link clicked (simplification)
        link = self.Links[0] if len(self.Links) > 0 else None
        
        # Create a mock event args object
        class LinkLabelLinkClickedEventArgs:
            def __init__(self, link, button):
                self.Link = link
                self.Button = button
        
        args = LinkLabelLinkClickedEventArgs(link, 'left')
        
        # Call both LinkClicked (specific) and Click (inherited from ControlBase)
        self.LinkClicked(self, args)
        if hasattr(self, 'Click') and self.Click:
            self.Click(self, args)
        
    def _on_mouse_enter(self, event):
        if not self.Enabled:
            return
            
        if self.LinkBehavior == 'HoverUnderline':
             try:
                from tkinter import font
                f = font.Font(font=self._tk_widget.cget("font"))
                f.configure(underline=True)
                self._tk_widget.config(font=f)
             except: pass
        self._tk_widget.config(fg=self.ActiveLinkColor)
        
    def _on_mouse_leave(self, event):
        if not self.Enabled:
            return

        if self.LinkBehavior == 'HoverUnderline':
             try:
                from tkinter import font
                f = font.Font(font=self._tk_widget.cget("font"))
                f.configure(underline=False)
                self._tk_widget.config(font=f)
             except: pass
        
        color = self.VisitedLinkColor if self.LinkVisited else self.LinkColor
        self._tk_widget.config(fg=color)
        


class DomainUpDownItemCollection:
    """Collection of items for DomainUpDown."""
    def __init__(self, owner):
        self.owner = owner
        self._items = []

    @property
    def Count(self):
        return len(self._items)
        
    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, value):
        self._items[index] = value
        if self.owner.Sorted:
            self._items.sort(key=str)
        self.owner._update_items()

    def Add(self, item):
        self._items.append(item)
        if self.owner.Sorted:
            self._items.sort(key=str)
        self.owner._update_items()
        return self.IndexOf(item)

    def Clear(self):
        self._items.clear()
        self.owner._update_items()

    def Contains(self, item):
        return item in self._items

    def IndexOf(self, item):
        try:
            return self._items.index(item)
        except ValueError:
            return -1

    def Insert(self, index, item):
        self._items.insert(index, item)
        if self.owner.Sorted:
            self._items.sort(key=str)
        self.owner._update_items()

    def Remove(self, item):
        if item in self._items:
            self._items.remove(item)
            self.owner._update_items()

    def RemoveAt(self, index):
        if 0 <= index < len(self._items):
            del self._items[index]
            self.owner._update_items()
            
    def __len__(self):
        return len(self._items)
        
    def __iter__(self):
        return iter(self._items)


class DomainUpDown(ControlBase):
    """
    Represents a Windows spin box (also known as an up-down control) that displays string values.
    """
    def __init__(self, master_form, props=None):
        defaults = {
            'Items': [],
            'SelectedIndex': -1,
            'Wrap': False,
            'ReadOnly': False,
            'Left': 0, 'Top': 0, 'Width': 120, 'Height': 20,
            'Name': '', 'Enabled': True, 'Visible': True,
            'Text': '',
            'Sorted': False,
            'TextAlign': HorizontalAlignment.Left,
            'InterceptArrowKeys': True,
            'UpDownAlign': LeftRightAlignment.Right
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Control", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Control")
        
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        self._parent_container = parent_container
        self.Name = defaults['Name']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        
        self._wrap = defaults['Wrap']
        self._read_only = defaults['ReadOnly']
        self._sorted = defaults['Sorted']
        self._text_align = defaults['TextAlign']
        self._intercept_arrow_keys = defaults['InterceptArrowKeys']
        self._up_down_align = defaults['UpDownAlign']
        
        # Collection
        self.Items = DomainUpDownItemCollection(self)
        if defaults['Items']:
            for item in defaults['Items']:
                self.Items.Add(item)
        
        self._selected_index = defaults['SelectedIndex']
        
        # Events
        self.SelectedItemChanged = lambda sender, e: None
        self.TextChanged = lambda sender, e: None
        
        # Create Tkinter Spinbox
        # Note: Tkinter Spinbox 'values' is a tuple.
        self._tk_widget = tk.Spinbox(
            self.master,
            wrap=self._wrap,
            command=self._on_spinbox_change
        )
        
        self._update_items()
        
        # Apply initial text or selection
        if self._selected_index >= 0 and self._selected_index < self.Items.Count:
            self.SelectedIndex = self._selected_index
        elif defaults['Text']:
            self.Text = defaults['Text']
            
        self._apply_visual_config()
        
        # Bindings
        self._tk_widget.bind('<KeyRelease>', self._on_key_release)
        self._bind_common_events()
        
        self._place_control(self.Width, self.Height)
        self._auto_register_with_parent()

    def _apply_visual_config(self):
        if not self._tk_widget: return
        
        config = {}
        if self.Font: config['font'] = self.Font
        if self.ForeColor: config['fg'] = self.ForeColor
        if self.BackColor: config['bg'] = self.BackColor
        
        if self._read_only:
            config['state'] = 'readonly'
        elif not self.Enabled:
            config['state'] = 'disabled'
        else:
            config['state'] = 'normal'
            
        # TextAlign
        align_map = {
            HorizontalAlignment.Left: 'left',
            HorizontalAlignment.Center: 'center',
            HorizontalAlignment.Right: 'right'
        }
        config['justify'] = align_map.get(self._text_align, 'left')
        
        self._tk_widget.config(**config)

    def _update_items(self):
        if self._tk_widget:
            # Spinbox values expects a tuple
            self._tk_widget.config(values=tuple(self.Items))

    def _on_spinbox_change(self):
        # Called when up/down buttons are clicked
        self._sync_selected_index()
        self.SelectedItemChanged(self, EventArgs.Empty)
        self.TextChanged(self, EventArgs.Empty)

    def _on_key_release(self, event):
        self._sync_selected_index()
        self.TextChanged(self, EventArgs.Empty)

    def _sync_selected_index(self):
        text = self.Text
        if hasattr(self.Items, 'IndexOf'):
            idx = self.Items.IndexOf(text)
        else:
            try:
                idx = self.Items.index(text)
            except ValueError:
                idx = -1
        self._selected_index = idx

    @property
    def SelectedIndex(self):
        return self._selected_index
        
    @SelectedIndex.setter
    def SelectedIndex(self, value):
        items_count = self.Items.Count if hasattr(self.Items, 'Count') else len(self.Items)
        if 0 <= value < items_count:
            self._selected_index = value
            item = self.Items[value]
            self.Text = str(item)
            self.SelectedItemChanged(self, EventArgs.Empty)
        else:
            self._selected_index = -1

    @property
    def SelectedItem(self):
        if self._selected_index != -1:
            return self.Items[self._selected_index]
        return None
        
    @SelectedItem.setter
    def SelectedItem(self, value):
        if hasattr(self.Items, 'IndexOf'):
            idx = self.Items.IndexOf(value)
        else:
            try:
                idx = self.Items.index(value)
            except ValueError:
                idx = -1
        if idx != -1:
            self.SelectedIndex = idx
        else:
            # If not in list, just set text? 
            # WinForms behavior: "The object becomes the string value... displayed"
            # But usually SelectedItem implies it is in the collection.
            # If we set Text, SelectedIndex becomes -1.
            self.Text = str(value)

    @property
    def Text(self):
        return self._tk_widget.get()
        
    @Text.setter
    def Text(self, value):
        self._tk_widget.delete(0, tk.END)
        self._tk_widget.insert(0, value)
        self._sync_selected_index()
        self.TextChanged(self, EventArgs.Empty)

    @property
    def ReadOnly(self):
        return self._read_only

    @ReadOnly.setter
    def ReadOnly(self, value):
        self._read_only = value
        self._apply_visual_config()

    @property
    def Wrap(self):
        return self._wrap

    @Wrap.setter
    def Wrap(self, value):
        self._wrap = value
        if self._tk_widget:
            self._tk_widget.config(wrap=value)

    @property
    def Sorted(self):
        return self._sorted

    @Sorted.setter
    def Sorted(self, value):
        self._sorted = value
        if value:
            # Sort existing items
            items = list(self.Items)
            items.sort(key=str)
            self.Items.Clear()
            for i in items: self.Items.Add(i)

    @property
    def TextAlign(self):
        return self._text_align

    @TextAlign.setter
    def TextAlign(self, value):
        self._text_align = value
        self._apply_visual_config()

    @property
    def InterceptArrowKeys(self):
        return self._intercept_arrow_keys

    @InterceptArrowKeys.setter
    def InterceptArrowKeys(self, value):
        self._intercept_arrow_keys = value
        # Tkinter Spinbox handles arrows. To disable, we might need to unbind.
        # Not fully implemented for now.

    @property
    def UpDownAlign(self):
        return self._up_down_align

    @UpDownAlign.setter
    def UpDownAlign(self, value):
        self._up_down_align = value
        # Tkinter Spinbox doesn't support changing button alignment easily (always right).

    def UpButton(self):
        """Displays the previous item in the collection."""
        try:
            self._tk_widget.invoke('buttonup')
        except:
            pass

    def DownButton(self):
        """Displays the next item in the collection."""
        try:
            self._tk_widget.invoke('buttondown')
        except:
            pass

    def UpdateEditText(self):
        """Updates the text in the spin box to display the selected item."""
        if self.SelectedItem:
            self.Text = str(self.SelectedItem)


class NumericUpDown(ControlBase):
    """
    Represents a Windows Forms NumericUpDown control.
    """
    def __init__(self, master_form, props=None):
        defaults = {
            'Minimum': 0,
            'Maximum': 100,
            'Value': 0,
            'Increment': 1,
            'DecimalPlaces': 0,
            'Hexadecimal': False,
            'ThousandsSeparator': False,
            'InterceptArrowKeys': True,
            'Left': 0, 'Top': 0, 'Width': 120, 'Height': 20,
            'Name': '', 'ReadOnly': False, 'TextAlign': HorizontalAlignment.Left,
            'UpDownAlign': LeftRightAlignment.Right
        }
        if props:
            defaults.update(props)
            
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        self._parent_container = parent_container
        self.Name = defaults['Name']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        
        self._minimum = defaults['Minimum']
        self._maximum = defaults['Maximum']
        self._value = float(defaults['Value'])
        self._increment = defaults['Increment']
        self._decimal_places = defaults['DecimalPlaces']
        self._hexadecimal = defaults['Hexadecimal']
        self._thousands_separator = defaults['ThousandsSeparator']
        self._intercept_arrow_keys = defaults['InterceptArrowKeys']
        self._readonly = defaults['ReadOnly']
        self._text_align = defaults['TextAlign']
        self._up_down_align = defaults['UpDownAlign']
        self._user_edit = False
        
        self.ValueChanged = lambda sender, e: None
        
        # Create Tkinter Spinbox
        self._tk_widget = tk.Spinbox(
            self.master,
            from_=self._minimum,
            to=self._maximum,
            increment=self._increment,
            command=self._on_spinbox_change
        )
        
        self._apply_visual_config()
        self.UpdateEditText()
        
        self._place_control(self.Width, self.Height)
        self._auto_register_with_parent()
        self._bind_common_events()
        
        # Bind key release to update value manually typed
        self._tk_widget.bind('<KeyRelease>', self._on_key_release)
        self._tk_widget.bind('<FocusOut>', self._on_focus_out)

    def _apply_visual_config(self):
        if not self._tk_widget: return
        
        config = {}
        if self._readonly:
            config['state'] = 'readonly'
        else:
            config['state'] = 'normal'
            
        # TextAlign
        align_map = {
            HorizontalAlignment.Left: 'left',
            HorizontalAlignment.Center: 'center',
            HorizontalAlignment.Right: 'right'
        }
        config['justify'] = align_map.get(self._text_align, 'left')
        
        # Format
        if not self._hexadecimal:
            config['format'] = f"%.{self._decimal_places}f"
        else:
            # Remove format for hex to avoid float formatting interference
            config['format'] = ""
            
        self._tk_widget.config(**config)

    def _on_spinbox_change(self):
        # Called when buttons are clicked
        # We validate the text in the box
        self.ValidateEditText()

    def _on_key_release(self, event):
        self._user_edit = True
        # Optional: Validate on key press or just wait for focus out/enter
        if event.keysym == 'Return':
            self.ValidateEditText()

    def _on_focus_out(self, event):
        self.ValidateEditText()

    def UpButton(self):
        """Increments the value."""
        self.Value = min(self.Maximum, self.Value + self.Increment)

    def DownButton(self):
        """Decrements the value."""
        self.Value = max(self.Minimum, self.Value - self.Increment)

    def ParseEditText(self):
        """Converts the text to a numeric value."""
        text = self._tk_widget.get()
        try:
            if self._hexadecimal:
                return int(text, 16)
            else:
                # Remove thousands separator if present
                if self._thousands_separator:
                    text = text.replace(',', '')
                return float(text)
        except ValueError:
            return self._value

    def UpdateEditText(self):
        """Updates the text in the spin box to display the current value."""
        if not self._tk_widget: return
        
        self._tk_widget.delete(0, "end")
        
        if self._hexadecimal:
            text = f"{int(self._value):X}"
        else:
            if self._thousands_separator:
                text = f"{self._value:,.{self._decimal_places}f}"
            else:
                text = f"{self._value:.{self._decimal_places}f}"
                
        self._tk_widget.insert(0, text)

    def ValidateEditText(self):
        """Validates and updates the text."""
        new_val = self.ParseEditText()
        
        # Clamp
        if new_val < self._minimum: new_val = self._minimum
        if new_val > self._maximum: new_val = self._maximum
        
        changed = (new_val != self._value)
        self._value = new_val
        
        self.UpdateEditText()
        self._user_edit = False
        
        if changed:
            self.ValueChanged(self, None)

    @property
    def Value(self):
        return self._value

    @Value.setter
    def Value(self, val):
        # Clamp
        if val < self._minimum: val = self._minimum
        if val > self._maximum: val = self._maximum
        
        if self._value != val:
            self._value = val
            self.UpdateEditText()
            self.ValueChanged(self, None)
            
    @property
    def Minimum(self): return self._minimum
    @Minimum.setter
    def Minimum(self, value):
        self._minimum = value
        self._tk_widget.config(from_=value)
        if self._value < value: self.Value = value

    @property
    def Maximum(self): return self._maximum
    @Maximum.setter
    def Maximum(self, value):
        self._maximum = value
        self._tk_widget.config(to=value)
        if self._value > value: self.Value = value
        
    @property
    def Increment(self): return self._increment
    @Increment.setter
    def Increment(self, value):
        self._increment = value
        self._tk_widget.config(increment=value)
        
    @property
    def DecimalPlaces(self): return self._decimal_places
    @DecimalPlaces.setter
    def DecimalPlaces(self, value):
        self._decimal_places = value
        self._apply_visual_config()
        self.UpdateEditText()
        
    @property
    def Hexadecimal(self): return self._hexadecimal
    @Hexadecimal.setter
    def Hexadecimal(self, value):
        self._hexadecimal = value
        self._apply_visual_config()
        self.UpdateEditText()

    @property
    def ThousandsSeparator(self): return self._thousands_separator
    @ThousandsSeparator.setter
    def ThousandsSeparator(self, value):
        self._thousands_separator = value
        self.UpdateEditText()

    @property
    def ReadOnly(self): return self._readonly
    @ReadOnly.setter
    def ReadOnly(self, value):
        self._readonly = value
        self._apply_visual_config()

    @property
    def TextAlign(self): return self._text_align
    @TextAlign.setter
    def TextAlign(self, value):
        self._text_align = value
        self._apply_visual_config()

    @property
    def InterceptArrowKeys(self): return self._intercept_arrow_keys
    @InterceptArrowKeys.setter
    def InterceptArrowKeys(self, value):
        self._intercept_arrow_keys = value
        # Logic to enable/disable arrow keys binding could go here

    @property
    def UpDownAlign(self): return self._up_down_align
    @UpDownAlign.setter
    def UpDownAlign(self, value):
        self._up_down_align = value
        # Tkinter Spinbox doesn't support changing button alignment easily

    @property
    def Accelerations(self):
        """Gets a collection of sorted acceleration objects for the NumericUpDown control."""
        # Not fully implemented in this version
        return []

    @property
    def UserEdit(self): return self._user_edit
    @UserEdit.setter
    def UserEdit(self, value): self._user_edit = value

    @property
    def Text(self):
        return self._tk_widget.get()
    
    @Text.setter
    def Text(self, value):
        self._tk_widget.delete(0, "end")
        self._tk_widget.insert(0, value)
        self.ValidateEditText()


class RichTextBox(TextBox):
    """
    Represents a RichTextBox control for displaying and editing formatted text.
    """
    def __init__(self, master_form, props=None):
        defaults = {
            'DetectUrls': False,
            'EnableAutoDragDrop': False,
            'RichTextShortcutsEnabled': True,
            'RightMargin': 0,
            'ScrollBars': 'both',
            'ShowSelectionMargin': False,
            'ZoomFactor': 1.0,
            'BulletIndent': 0,
            'AutoWordSelection': False,
            'LanguageOption': 0,
            'Multiline': True
        }
        if props:
            defaults.update(props)
        
        super().__init__(master_form, defaults)
        
        self.DetectUrls = defaults['DetectUrls']
        self.EnableAutoDragDrop = defaults['EnableAutoDragDrop']
        self.RichTextShortcutsEnabled = defaults['RichTextShortcutsEnabled']
        self.RightMargin = defaults['RightMargin']
        self.ShowSelectionMargin = defaults['ShowSelectionMargin']
        self._zoom_factor = defaults['ZoomFactor']
        self.BulletIndent = defaults['BulletIndent']
        self.AutoWordSelection = defaults['AutoWordSelection']
        self.LanguageOption = defaults['LanguageOption']
        
        # Events
        self.SelectionChanged = lambda sender, e: None
        self.LinkClicked = lambda sender, e: None
        self.ContentsResized = lambda sender, e: None
        self.HScroll = lambda sender, e: None
        self.VScroll = lambda sender, e: None
        self.ImeChange = lambda sender, e: None
        self.Protected = lambda sender, e: None
        
        # Bind selection event
        if self._tk_widget:
            self._tk_widget.bind('<<Selection>>', self._on_selection_changed)
            self._tk_widget.bind('<Configure>', self._on_contents_resized)
        
        # Tags management
        self._tag_counter = 0
        
        # Enable Undo/Redo
        if self._tk_widget:
            self._tk_widget.config(undo=True, maxundo=-1)

    def _on_selection_changed(self, event):
        self.SelectionChanged(self, event)

    def _on_contents_resized(self, event):
        self.ContentsResized(self, event)

    @property
    def ZoomFactor(self):
        return self._zoom_factor

    @ZoomFactor.setter
    def ZoomFactor(self, value):
        if value <= 0: return
        self._zoom_factor = value
        # Implementation of zoom would go here

    def Undo(self):
        try:
            self._tk_widget.edit_undo()
        except:
            pass

    def Redo(self):
        try:
            self._tk_widget.edit_redo()
        except:
            pass

    @property
    def CanUndo(self): return True
    @property
    def CanRedo(self): return True
    
    @property
    def RedoActionName(self): return "Redo"
    
    @property
    def UndoActionName(self): return "Undo"

    @property
    def SelectionIndent(self):
        return self._get_tag_property("lmargin1") or 0

    @SelectionIndent.setter
    def SelectionIndent(self, value):
        self._apply_tag_property("lmargin1", value)

    @property
    def SelectionRightIndent(self):
        return self._get_tag_property("rmargin") or 0

    @SelectionRightIndent.setter
    def SelectionRightIndent(self, value):
        self._apply_tag_property("rmargin", value)

    @property
    def SelectionHangingIndent(self):
        l1 = self._get_tag_property("lmargin1") or 0
        l2 = self._get_tag_property("lmargin2") or 0
        return l2 - l1

    @SelectionHangingIndent.setter
    def SelectionHangingIndent(self, value):
        l1 = self.SelectionIndent
        self._apply_tag_property("lmargin2", l1 + value)

    @property
    def SelectionCharOffset(self):
        return self._get_tag_property("offset") or 0

    @SelectionCharOffset.setter
    def SelectionCharOffset(self, value):
        self._apply_tag_property("offset", value)

    @property
    def SelectionBullet(self): 
        return False 
        
    @SelectionBullet.setter
    def SelectionBullet(self, value): 
        pass

    @property
    def SelectionProtected(self):
        return False

    @SelectionProtected.setter
    def SelectionProtected(self, value):
        pass

    @property
    def Rtf(self):
        """Gets or sets the text in RTF format (Simplified: returns Text)."""
        return self.Text

    @Rtf.setter
    def Rtf(self, value):
        """Sets the text in RTF format (Simplified: sets Text)."""
        self.Text = value
        
    @property
    def SelectedRtf(self):
        return self.SelectedText

    @SelectedRtf.setter
    def SelectedRtf(self, value):
        self.SelectedText = value

    @property
    def SelectedText(self):
        try:
            return self._tk_widget.get("sel.first", "sel.last")
        except tk.TclError:
            return ""

    @SelectedText.setter
    def SelectedText(self, value):
        if self.SelectionLength > 0:
            self._tk_widget.delete("sel.first", "sel.last")
            self._tk_widget.insert("sel.first", value)
        else:
            self._tk_widget.insert("insert", value)

    @property
    def SelectionStart(self):
        try:
            index = self._tk_widget.index("sel.first")
            return self._index_to_offset(index)
        except tk.TclError:
            return self._index_to_offset(self._tk_widget.index("insert"))

    @SelectionStart.setter
    def SelectionStart(self, value):
        # Move cursor to offset
        index = f"1.0+{value}c"
        self._tk_widget.mark_set("insert", index)
        # Clear selection
        self._tk_widget.tag_remove("sel", "1.0", "end")

    @property
    def SelectionLength(self):
        try:
            start = self._tk_widget.index("sel.first")
            end = self._tk_widget.index("sel.last")
            return len(self._tk_widget.get(start, end))
        except tk.TclError:
            return 0

    @SelectionLength.setter
    def SelectionLength(self, value):
        start_index = self._tk_widget.index("insert")
        end_index = f"{start_index}+{value}c"
        self._tk_widget.tag_add("sel", start_index, end_index)
        
    @property
    def SelectionType(self):
        if self.SelectionLength > 0:
            return "Text"
        return "Empty"

    @property
    def SelectionColor(self):
        return self._get_tag_property("foreground")

    @SelectionColor.setter
    def SelectionColor(self, value):
        self._apply_tag_property("foreground", value)

    @property
    def SelectionBackColor(self):
        return self._get_tag_property("background")

    @SelectionBackColor.setter
    def SelectionBackColor(self, value):
        self._apply_tag_property("background", value)

    @property
    def SelectionFont(self):
        return self._get_tag_property("font")

    @SelectionFont.setter
    def SelectionFont(self, value):
        self._apply_tag_property("font", value)
        
    @property
    def SelectionAlignment(self):
        return self._get_tag_property("justify")
        
    @SelectionAlignment.setter
    def SelectionAlignment(self, value):
        self._apply_tag_property("justify", value.lower())

    def _get_tag_property(self, prop):
        try:
            tags = self._tk_widget.tag_names("sel.first")
            for tag in reversed(tags):
                if tag.startswith("sel"): continue
                val = self._tk_widget.tag_cget(tag, prop)
                if val: return val
        except:
            pass
        return None

    def _apply_tag_property(self, prop, value):
        try:
            tag_name = f"fmt_{self._tag_counter}"
            self._tag_counter += 1
            kwargs = {prop: value}
            self._tk_widget.tag_config(tag_name, **kwargs)
            self._tk_widget.tag_add(tag_name, "sel.first", "sel.last")
        except tk.TclError:
            pass

    def LoadFile(self, path, file_type="PlainText"):
        with open(path, 'r') as f:
            content = f.read()
            self.Text = content
            
    def SaveFile(self, path, file_type="PlainText"):
        with open(path, 'w') as f:
            f.write(self.Text)
            
    def Find(self, text, start=0, end=-1, options=None):
        start_idx = f"1.0+{start}c"
        end_idx = "end" if end == -1 else f"1.0+{end}c"
        
        pos = self._tk_widget.search(text, start_idx, stopindex=end_idx)
        if pos:
            end_pos = f"{pos}+{len(text)}c"
            self.Select(self._index_to_offset(pos), len(text))
            return self._index_to_offset(pos)
        return -1
        
    def CanPaste(self, format):
        return True
        
    def GetLineFromCharIndex(self, index):
        pos = f"1.0+{index}c"
        return int(self._tk_widget.index(pos).split('.')[0]) - 1
        
    def GetPositionFromCharIndex(self, index):
        pos = f"1.0+{index}c"
        bbox = self._tk_widget.bbox(pos)
        if bbox:
            return (bbox[0], bbox[1])
        return (0, 0)

    def Select(self, start, length):
        # start can be index string or int offset
        if isinstance(start, int):
            start_index = f"1.0+{start}c"
        else:
            start_index = start
            
        if isinstance(length, int):
            end_index = f"{start_index}+{length}c"
        else:
            end_index = length # Assume it's an end index
            
        self._tk_widget.tag_remove("sel", "1.0", "end")
        self._tk_widget.tag_add("sel", start_index, end_index)
        self._tk_widget.mark_set("insert", end_index)
        self._tk_widget.see(end_index)
        
    def SelectAll(self):
        self._tk_widget.tag_add("sel", "1.0", "end")
        
    def DeselectAll(self):
        self._tk_widget.tag_remove("sel", "1.0", "end")

    def _index_to_offset(self, index):
        try:
            return self._tk_widget.count("1.0", index, "chars")[0]
        except:
            return 0


class MaskedTextProvider:
    """
    Implements a MaskedTextProvider for parsing and validating masked text input.
    
    This class provides functionality similar to System.ComponentModel.MaskedTextProvider
    from .NET Framework, supporting standard mask characters and text manipulation.
    
    Standard mask characters:
    - 0: Required digit (0-9)
    - 9: Optional digit (0-9) or space
    - #: Optional digit, space, or sign (+-) 
    - L: Required letter (a-z, A-Z)
    - ?: Optional letter (a-z, A-Z)
    - &: Required character (any printable)
    - C: Optional character (any printable)
    - A: Required alphanumeric (a-z, A-Z, 0-9)
    - a: Optional alphanumeric (a-z, A-Z, 0-9)
    - .: Decimal placeholder
    - ,: Thousands separator
    - :: Time separator
    - /: Date separator
    - $: Currency symbol
    - <: Converts characters to lowercase
    - >: Converts characters to uppercase
    - |: Disables case conversion
    - \\: Escapes the next character to literal
    """
    
    def __init__(self, mask, culture=None, allow_prompt_as_input=True, prompt_char='_',
                 password_char=None, restrict_to_ascii=False):
        """
        Initialize a MaskedTextProvider.
        
        Args:
            mask: The mask string defining the format
            culture: Culture info (not fully implemented)
            allow_prompt_as_input: Whether to allow prompt character as valid input
            prompt_char: Character used to represent missing input
            password_char: Character to display instead of actual input
            restrict_to_ascii: Whether to restrict input to ASCII characters only
        """
        self._mask = mask
        self._culture = culture
        self._allow_prompt_as_input = allow_prompt_as_input
        self._prompt_char = prompt_char
        self._password_char = password_char
        self._restrict_to_ascii = restrict_to_ascii
        
        # Parse mask into elements
        self._mask_elements = []
        self._parse_mask()
        
        # Internal state - character buffer
        self._buffer = [prompt_char if elem['type'] == 'input' else elem['char'] 
                       for elem in self._mask_elements]
        
        # Case conversion state
        self._case_mode = None  # None, 'upper', 'lower'
    
    def _parse_mask(self):
        """Parse the mask string into structured elements."""
        if not self._mask:
            return
        
        i = 0
        length = len(self._mask)
        escape = False
        case_mode = None
        
        while i < length:
            c = self._mask[i]
            
            # Handle escape character
            if escape:
                self._mask_elements.append({'type': 'literal', 'char': c})
                escape = False
                i += 1
                continue
            
            if c == '\\':
                escape = True
                i += 1
                continue
            
            # Case conversion modifiers
            if c == '<':
                case_mode = 'lower'
                i += 1
                continue
            elif c == '>':
                case_mode = 'upper'
                i += 1
                continue
            elif c == '|':
                case_mode = None
                i += 1
                continue
            
            # Input placeholders
            if c == '0':
                self._mask_elements.append({'type': 'input', 'validator': 'digit', 'required': True, 'case': case_mode})
            elif c == '9':
                self._mask_elements.append({'type': 'input', 'validator': 'digit_space', 'required': False, 'case': case_mode})
            elif c == '#':
                self._mask_elements.append({'type': 'input', 'validator': 'digit_space_sign', 'required': False, 'case': case_mode})
            elif c == 'L':
                self._mask_elements.append({'type': 'input', 'validator': 'letter', 'required': True, 'case': case_mode})
            elif c == '?':
                self._mask_elements.append({'type': 'input', 'validator': 'letter', 'required': False, 'case': case_mode})
            elif c == '&':
                self._mask_elements.append({'type': 'input', 'validator': 'char', 'required': True, 'case': case_mode})
            elif c == 'C':
                self._mask_elements.append({'type': 'input', 'validator': 'char', 'required': False, 'case': case_mode})
            elif c == 'A':
                self._mask_elements.append({'type': 'input', 'validator': 'alnum', 'required': True, 'case': case_mode})
            elif c == 'a':
                self._mask_elements.append({'type': 'input', 'validator': 'alnum', 'required': False, 'case': case_mode})
            else:
                # Literal character
                self._mask_elements.append({'type': 'literal', 'char': c})
            
            i += 1
    
    def _validate_char(self, char, elem):
        """Validate a character against a mask element."""
        if self._restrict_to_ascii and not char.isascii():
            return False
        
        validator = elem.get('validator')
        if validator == 'digit':
            return char.isdigit()
        elif validator == 'digit_space':
            return char.isdigit() or char == ' '
        elif validator == 'digit_space_sign':
            return char.isdigit() or char in ' +-'
        elif validator == 'letter':
            return char.isalpha()
        elif validator == 'alnum':
            return char.isalnum()
        elif validator == 'char':
            return char.isprintable()
        
        return True
    
    def _apply_case(self, char, elem):
        """Apply case conversion to a character."""
        case = elem.get('case')
        if case == 'upper':
            return char.upper()
        elif case == 'lower':
            return char.lower()
        return char
    
    @property
    def Mask(self):
        """Gets the input mask."""
        return self._mask
    
    @property
    def Length(self):
        """Gets the length of the mask."""
        return len(self._mask_elements)
    
    @property
    def PromptChar(self):
        """Gets the prompt character."""
        return self._prompt_char
    
    @PromptChar.setter
    def PromptChar(self, value):
        """Sets the prompt character."""
        if value and len(value) == 1:
            self._prompt_char = value
            # Refresh mask to apply new prompt char
            if self._mask:
                self._parse_mask()
                self._update_display_text()
    
    @property
    def AllowPromptAsInput(self):
        """Gets whether prompt character is allowed as input."""
        return self._allow_prompt_as_input
    
    @property
    def MaskCompleted(self):
        """Gets whether all required positions have been filled."""
        for i, elem in enumerate(self._mask_elements):
            if elem['type'] == 'input' and elem.get('required', False):
                if self._buffer[i] == self._prompt_char:
                    return False
        return True
    
    @property
    def MaskFull(self):
        """Gets whether all positions (required and optional) have been filled."""
        for i, elem in enumerate(self._mask_elements):
            if elem['type'] == 'input':
                if self._buffer[i] == self._prompt_char:
                    return False
        return True
    
    def ToString(self, include_prompt=True, include_literals=True):
        """
        Convert the current state to a string.
        
        Args:
            include_prompt: Whether to include prompt characters
            include_literals: Whether to include literal characters
        
        Returns:
            String representation of the masked text
        """
        result = []
        for i, elem in enumerate(self._mask_elements):
            if elem['type'] == 'literal':
                if include_literals:
                    result.append(elem['char'])
            else:  # input
                char = self._buffer[i]
                if char == self._prompt_char and not include_prompt:
                    result.append('')
                elif self._password_char and char != self._prompt_char:
                    result.append(self._password_char)
                else:
                    result.append(char)
        
        return ''.join(result)
    
    def ToDisplayString(self):
        """Gets the formatted string with prompt characters and literals."""
        return self.ToString(include_prompt=True, include_literals=True)
    
    def Add(self, input_char, position=None):
        """
        Add a character at the specified position or next available position.
        
        Args:
            input_char: Character to add
            position: Optional position index
        
        Returns:
            True if character was added successfully
        """
        if position is None:
            # Find next available input position
            position = self._find_next_input_position(0)
        
        if position is None or position >= len(self._mask_elements):
            return False
        
        elem = self._mask_elements[position]
        if elem['type'] != 'input':
            return False
        
        if not self._validate_char(input_char, elem):
            return False
        
        self._buffer[position] = self._apply_case(input_char, elem)
        return True
    
    def InsertAt(self, input_char, position):
        """
        Insert a character at the specified position.
        
        Args:
            input_char: Character to insert
            position: Position index
        
        Returns:
            True if character was inserted successfully
        """
        return self.Add(input_char, position)
    
    def RemoveAt(self, position):
        """
        Remove character at the specified position.
        
        Args:
            position: Position index
        
        Returns:
            True if character was removed successfully
        """
        if position < 0 or position >= len(self._mask_elements):
            return False
        
        elem = self._mask_elements[position]
        if elem['type'] == 'input':
            self._buffer[position] = self._prompt_char
            return True
        
        return False
    
    def Replace(self, input_char, position):
        """
        Replace character at the specified position.
        
        Args:
            input_char: Character to replace with
            position: Position index
        
        Returns:
            True if character was replaced successfully
        """
        if self.RemoveAt(position):
            return self.InsertAt(input_char, position)
        return False
    
    def Clear(self):
        """Clear all input positions to prompt character."""
        for i, elem in enumerate(self._mask_elements):
            if elem['type'] == 'input':
                self._buffer[i] = self._prompt_char
    
    def Set(self, input_string):
        """
        Set the entire input string, parsing and validating against mask.
        
        Args:
            input_string: String to set
        
        Returns:
            True if string was set successfully
        """
        self.Clear()
        
        input_pos = 0
        for i, elem in enumerate(self._mask_elements):
            if elem['type'] == 'input':
                if input_pos < len(input_string):
                    char = input_string[input_pos]
                    if self._validate_char(char, elem):
                        self._buffer[i] = self._apply_case(char, elem)
                    elif not elem.get('required', False):
                        pass  # Skip optional
                    else:
                        return False  # Required field failed
                    input_pos += 1
            else:
                # Skip literals in input string if they match
                if input_pos < len(input_string) and input_string[input_pos] == elem['char']:
                    input_pos += 1
        
        return True
    
    def _find_next_input_position(self, start_position):
        """Find the next input position from start_position."""
        for i in range(start_position, len(self._mask_elements)):
            if self._mask_elements[i]['type'] == 'input':
                return i
        return None
    
    def _find_previous_input_position(self, start_position):
        """Find the previous input position from start_position."""
        for i in range(start_position - 1, -1, -1):
            if self._mask_elements[i]['type'] == 'input':
                return i
        return None
    
    def FindEditPositionFrom(self, position, forward=True):
        """
        Find the next editable position.
        
        Args:
            position: Starting position
            forward: Search forward if True, backward if False
        
        Returns:
            Next editable position or -1 if none found
        """
        if forward:
            pos = self._find_next_input_position(position)
        else:
            pos = self._find_previous_input_position(position)
        
        return pos if pos is not None else -1
    
    def IsEditPosition(self, position):
        """Check if position is an editable input position."""
        if position < 0 or position >= len(self._mask_elements):
            return False
        return self._mask_elements[position]['type'] == 'input'
    
    def VerifyString(self, input_string):
        """
        Verify if a string would be valid for the current mask.
        
        Args:
            input_string: String to verify
        
        Returns:
            True if string is valid for the mask
        """
        # Create temporary copy to test
        temp_provider = MaskedTextProvider(
            self._mask, 
            self._culture,
            self._allow_prompt_as_input,
            self._prompt_char,
            self._password_char,
            self._restrict_to_ascii
        )
        return temp_provider.Set(input_string)


class MaskedTextBox(TextBox):
    """
    Represents a MaskedTextBox with mask validation and VB.NET-like properties.
    Supports standard Windows Forms mask characters and behavior.
    """
    
    def __init__(self, master_form, props=None):
        defaults = {
            'Mask': "",
            'Text': "",
            'Left': 10,
            'Top': 80,
            'Width': 200,
            'Name': "",
            'Multiline': False,  # MaskedTextBox must be single-line for password char to work
            'PromptChar': '_',
            'PasswordChar': None,
            'UseSystemPasswordChar': False,
            'BeepOnError': False,
            'CutCopyMaskFormat': 'IncludeLiterals',
            'InsertKeyMode': 'Insert',
            'AllowPromptAsInput': False,
            'FormatProvider': None,
            'TextMaskFormat': 'IncludeLiterals',
            'AsciiOnly': False,
            'ResetOnPrompt': True,
            'ResetOnSpace': True,
            'SkipLiterals': True,
            'ValidatingType': None,
            'RejectInputOnFirstFailure': False
        }
        
        if props:
            defaults.update(props)
            # MaskedTextBox MUST be single-line, ignore any Multiline setting from props
            if 'Multiline' in props:
                del props['Multiline']
        
        super().__init__(master_form, {
            'Text': defaults['Text'], 
            'Left': defaults['Left'], 
            'Top': defaults['Top'], 
            'Width': defaults['Width'], 
            'Name': defaults['Name'],
            'Multiline': False  # Force single-line Entry widget for password support
        })
        
        # Properties
        self._mask = defaults['Mask']
        self._prompt_char = defaults['PromptChar']  # Use private attribute to avoid calling setter during init
        self._password_char = None
        self._use_system_password_char = False
        self.BeepOnError = defaults['BeepOnError']
        self.CutCopyMaskFormat = defaults['CutCopyMaskFormat']
        self.InsertKeyMode = defaults['InsertKeyMode']
        self.AllowPromptAsInput = defaults['AllowPromptAsInput']
        self.FormatProvider = defaults['FormatProvider']
        self.TextMaskFormat = defaults['TextMaskFormat']
        self.AsciiOnly = defaults['AsciiOnly']
        self.ResetOnPrompt = defaults['ResetOnPrompt']
        self.ResetOnSpace = defaults['ResetOnSpace']
        self.SkipLiterals = defaults['SkipLiterals']
        self.ValidatingType = defaults['ValidatingType']
        self.RejectInputOnFirstFailure = defaults['RejectInputOnFirstFailure']
        
        # Events
        self.MaskInputRejected = lambda sender, e: None
        self.TypeValidationCompleted = lambda sender, e: None
        self.MaskChanged = lambda sender, e: None
        self.IsOverwriteModeChanged = lambda sender, e: None
        self.TextAlignChanged = lambda sender, e: None
        
        # Internal state
        self._mask_elements = []
        
        # Initialize private attributes before using properties
        self._password_char = None
        self._use_system_password_char = False
        
        # Delete inherited PasswordChar attributes from parent TextBox
        if 'PasswordChar' in self.__dict__:
            del self.__dict__['PasswordChar']
        if 'UseSystemPasswordChar' in self.__dict__:
            del self.__dict__['UseSystemPasswordChar']
        
        # Apply PasswordChar using properties (now they exist in this class)
        self.PasswordChar = defaults['PasswordChar']
        self.UseSystemPasswordChar = defaults['UseSystemPasswordChar']
        
        # Bindings for mask handling
        self._tk_widget.bind('<Key>', self._on_key_event)
        self._tk_widget.bind('<BackSpace>', self._on_backspace)
        self._tk_widget.bind('<Delete>', self._on_delete)
        self._tk_widget.bind('<FocusIn>', self._on_focus_in)
        self._tk_widget.bind('<FocusOut>', self._on_focus_out)
        self._tk_widget.bind('<Button-1>', self._on_click)
        
        # Disable standard validation to allow manual control
        self._tk_widget.config(validate='none')
        
        # Initialize
        self._parse_mask()
        self._update_display_text()
    
    @property
    def Multiline(self):
        """MaskedTextBox must always be single-line (read-only property)."""
        return False
    
    @Multiline.setter
    def Multiline(self, value):
        """Multiline cannot be changed for MaskedTextBox - it must always be False."""
        if value:
            raise ValueError("MaskedTextBox must be single-line. Multiline property cannot be set to True.")
    
    @property
    def PasswordChar(self):
        """Gets the password character."""
        return self._password_char
    
    @PasswordChar.setter
    def PasswordChar(self, value):
        """Sets the password character."""
        import tkinter as tk
        self._password_char = value
        
        # Only Entry widgets support 'show' option
        if isinstance(self._tk_widget, tk.Entry):
            if value:
                self._tk_widget.config(show=value)
            elif self.UseSystemPasswordChar:
                self._tk_widget.config(show='*')
            else:
                self._tk_widget.config(show='')
    
    @property
    def PromptChar(self):
        """Gets the prompt character."""
        return self._prompt_char
    
    @PromptChar.setter
    def PromptChar(self, value):
        """Sets the prompt character and refreshes display."""
        if value and len(value) == 1:
            self._prompt_char = value
            # Refresh display to show new prompt char
            if self._mask:
                self._parse_mask()
                self._update_display_text()
    
    @property
    def UseSystemPasswordChar(self):
        """Gets whether to use system password character."""
        return self._use_system_password_char
    
    @UseSystemPasswordChar.setter
    def UseSystemPasswordChar(self, value):
        """Sets whether to use system password character."""
        self._use_system_password_char = value
        
        # Only Entry widgets support 'show' option
        if hasattr(self._tk_widget, 'config'):
            try:
                if value:
                    self._tk_widget.config(show='*')
                elif self.PasswordChar:
                    self._tk_widget.config(show=self.PasswordChar)
                else:
                    self._tk_widget.config(show='')
            except tk.TclError:
                # Widget doesn't support 'show' option (e.g., Text widget)
                pass

    @property
    def Mask(self):
        return self._mask

    @Mask.setter
    def Mask(self, value):
        if self._mask != value:
            self._mask = value
            self._parse_mask()
            self._update_display_text()
            self.MaskChanged(self, None)

    def _parse_mask(self):
        """Parses the mask string into a list of element descriptors."""
        self._mask_elements = []
        if not self.Mask: return
        
        i = 0
        length = len(self.Mask)
        escape = False
        case_mode = None # None, 'upper', 'lower'
        
        while i < length:
            char = self.Mask[i]
            if escape:
                self._mask_elements.append({'type': 'literal', 'char': char})
                escape = False
            else:
                if char == '\\':
                    escape = True
                elif char == '<':
                    case_mode = 'lower'
                elif char == '>':
                    case_mode = 'upper'
                elif char == '|':
                    case_mode = None
                elif char in '09#L?&CAa':
                    # Input position
                    elem = {'type': 'input', 'mask_char': char, 'case': case_mode}
                    if char == '0': elem.update({'req': True, 'validator': 'digit'})
                    elif char == '9': elem.update({'req': False, 'validator': 'digit_space'})
                    elif char == '#': elem.update({'req': False, 'validator': 'digit_space_sign'})
                    elif char == 'L': elem.update({'req': True, 'validator': 'letter'})
                    elif char == '?': elem.update({'req': False, 'validator': 'letter'})
                    elif char == '&': elem.update({'req': True, 'validator': 'char'})
                    elif char == 'C': elem.update({'req': False, 'validator': 'char'})
                    elif char == 'A': elem.update({'req': True, 'validator': 'alnum'})
                    elif char == 'a': elem.update({'req': False, 'validator': 'alnum'})
                    self._mask_elements.append(elem)
                elif char in '.,:$/':
                    # Separators (simplified as literals)
                    self._mask_elements.append({'type': 'literal', 'char': char})
                else:
                    # Literal
                    self._mask_elements.append({'type': 'literal', 'char': char})
            i += 1

    def _update_display_text(self):
        """Rebuilds the display text based on mask and current values."""
        if not self.Mask: return
        
        current_val = self._tk_widget.get()
        new_text = ""
        
        # Rebuild text, preserving valid user input but updating prompt chars
        if current_val and len(current_val) == len(self._mask_elements):
            # Process each position
            for i, elem in enumerate(self._mask_elements):
                if elem['type'] == 'literal':
                    new_text += elem['char']
                else:
                    current_char = current_val[i] if i < len(current_val) else ''
                    # Validate if current char is valid input for this position
                    if current_char and self._validate_char(current_char, elem):
                        # Valid user input, preserve it
                        new_text += current_char
                    else:
                        # Empty or invalid (was prompt char), use new prompt
                        new_text += self.PromptChar
        else:
            # Empty or length mismatch, rebuild from scratch
            for elem in self._mask_elements:
                if elem['type'] == 'literal':
                    new_text += elem['char']
                else:
                    new_text += self.PromptChar

        self._tk_widget.delete(0, 'end')
        self._tk_widget.insert(0, new_text)

    def _on_key_event(self, event):
        if not self.Mask: return
        
        # Allow navigation and commands
        if event.keysym in ('Left', 'Right', 'Home', 'End', 'Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Tab', 'Return', 'Escape'):
            return
        if event.state & 4: # Control key
            return
            
        if len(event.char) == 1 and event.char.isprintable():
            self._handle_input(event.char)
            return "break" # Stop default insertion

    def _handle_input(self, char):
        try:
            idx = self._tk_widget.index("insert")
            if isinstance(idx, str): idx = int(idx.split('.')[1])
        except:
            idx = 0
            
        # Find next input position
        start_idx = idx
        while idx < len(self._mask_elements):
            elem = self._mask_elements[idx]
            if elem['type'] == 'literal':
                idx += 1
                continue
            
            # Validate
            if self._validate_char(char, elem):
                # Apply case
                if elem['case'] == 'upper': char = char.upper()
                elif elem['case'] == 'lower': char = char.lower()
                
                # Get current text as list
                current_text = list(self._tk_widget.get())
                if len(current_text) <= idx:
                    # Extend if needed
                    current_text.extend([' '] * (idx - len(current_text) + 1))
                current_text[idx] = char
                
                # Update entire text (needed for password char to work)
                self._tk_widget.delete(0, 'end')
                self._tk_widget.insert(0, ''.join(current_text))
                
                # Move cursor to next editable
                next_pos = idx + 1
                while next_pos < len(self._mask_elements) and self._mask_elements[next_pos]['type'] == 'literal':
                    next_pos += 1
                
                self._tk_widget.icursor(next_pos)
                return
            else:
                if self.BeepOnError and winsound: winsound.Beep(800, 100)
                self.MaskInputRejected(self, None)
                return
            break
            
        # If we reached here, maybe we were on a literal and user typed the literal char?
        # Auto-skip literal if user types it
        if start_idx < len(self._mask_elements):
            elem = self._mask_elements[start_idx]
            if elem['type'] == 'literal' and elem['char'] == char:
                self._tk_widget.icursor(start_idx + 1)
                # Try to process next char if any? No, just move.
                return

    def _validate_char(self, char, elem):
        v = elem['validator']
        if self.AsciiOnly and not char.isascii():
            return False
        
        if v == 'digit': return char.isdigit()
        if v == 'digit_space': return char.isdigit() or char == ' '
        if v == 'digit_space_sign': return char.isdigit() or char in ' +-'
        if v == 'letter': return char.isalpha()
        if v == 'alnum': return char.isalnum()
        if v == 'char': return char.isprintable()
        return True

    def _on_backspace(self, event):
        if not self.Mask: return
        
        try:
            idx = self._tk_widget.index("insert")
            if isinstance(idx, str): idx = int(idx.split('.')[1])
        except: return
        
        if idx > 0:
            target = idx - 1
            # Skip literals backwards
            while target >= 0 and self._mask_elements[target]['type'] == 'literal':
                target -= 1
            
            if target >= 0:
                # Get current text as list
                current_text = list(self._tk_widget.get())
                if target < len(current_text):
                    current_text[target] = self.PromptChar
                    # Update entire text (needed for password char to work)
                    self._tk_widget.delete(0, 'end')
                    self._tk_widget.insert(0, ''.join(current_text))
                    self._tk_widget.icursor(target)
        return "break"

    def _on_delete(self, event):
        if not self.Mask: return
        
        try:
            idx = self._tk_widget.index("insert")
            if isinstance(idx, str): idx = int(idx.split('.')[1])
        except: return
        
        if idx < len(self._mask_elements):
            # Skip literals forwards
            while idx < len(self._mask_elements) and self._mask_elements[idx]['type'] == 'literal':
                idx += 1
                
            if idx < len(self._mask_elements):
                # Get current text as list
                current_text = list(self._tk_widget.get())
                if idx < len(current_text):
                    current_text[idx] = self.PromptChar
                    # Update entire text (needed for password char to work)
                    self._tk_widget.delete(0, 'end')
                    self._tk_widget.insert(0, ''.join(current_text))
                    self._tk_widget.icursor(idx) # Stay put
        return "break"

    def _on_click(self, event):
        # Optional: Adjust cursor to nearest valid position
        pass

    def _on_focus_in(self, event):
        pass
    
    def _on_focus_out(self, event):
        if self.MaskCompleted:
            self.TypeValidationCompleted(self, None)
    
    @property
    def MaskFull(self):
        if not self.Mask: return True
        current = self._tk_widget.get()
        for i, elem in enumerate(self._mask_elements):
            if elem['type'] == 'input' and elem.get('req'):
                if i >= len(current) or current[i] == self.PromptChar:
                    return False
        return True
    
    @property
    def MaskCompleted(self):
        return self.MaskFull

    @property
    def IsOverwriteMode(self):
        return self.InsertKeyMode == 'Overwrite'

    # Unsupported methods/properties
    def ClearUndo(self): pass
    def GetFirstCharIndexFromLine(self, line): return -1
    def GetFirstCharIndexOfCurrentLine(self): return -1
    def GetLineFromCharIndex(self, index): return -1
    def ScrollToCaret(self): pass
    def Undo(self): pass
    
    @property
    def Multiline(self): return False
    @Multiline.setter
    def Multiline(self, value): pass
    
    @property
    def CanUndo(self): return False
    
    def ToString(self):
        return f"MaskedTextBox, Text: {self.Text}"


class PictureBox(ControlBase):
    """
    Represents a PictureBox to display images with VB.NET-like properties.
    
    Use the PictureBox control to display graphics from a bitmap, metafile, icon, JPEG, GIF, or PNG file.
    Set the Image property to the Image you want to display, either at design time or at run time.
    You can also specify the image by setting the ImageLocation property and loading the image
    synchronously using the Load method or asynchronously using the LoadAsync method.
    """
    
    def __init__(self, master_form, props=None):
        # Default values
        defaults = {
            'Image': None,
            'Left': 10,
            'Top': 10,
            'Width': 100,
            'Height': 100,
            'Name': "",
            'ImageLocation': "",
            'SizeMode': PictureBoxSizeMode.Normal,
            'BorderStyle': BorderStyle.None_,
            'Enabled': True,
            'Visible': True,
            'BackColor': None,
            'ErrorImage': None,
            'InitialImage': None,
            'WaitOnLoad': False,
            'TabStop': False # Not selectable by default
        }
        
        if props:
            defaults.update(props)
        
        # Resolve the Tkinter widget and store the parent container
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Save parent container for auto-registration
        self._parent_container = parent_container
        
        # Assign all properties
        self.Name = defaults['Name']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Image = defaults['Image']
        self.ImageLocation = defaults['ImageLocation']
        self.SizeMode = defaults['SizeMode']  # 'Normal', 'StretchImage', 'AutoSize', 'CenterImage', 'Zoom'
        self.BorderStyle = defaults['BorderStyle']  # 'None', 'FixedSingle', 'Fixed3D'
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.BackColor = defaults['BackColor']
        self.ErrorImage = defaults['ErrorImage']
        self.InitialImage = defaults['InitialImage']
        self.WaitOnLoad = defaults['WaitOnLoad']
        self.TabStop = defaults['TabStop']
        
        # VB-style events
        self.LoadCompleted = lambda sender, e: None
        self.LoadProgressChanged = lambda sender, e: None
        self.SizeModeChanged = lambda sender, e: None
        self.Error = lambda sender, e: None
        
        # Create the Tkinter widget (Label with image)
        self._tk_widget = tk.Label(self.master, image=self.Image)
        
        # Apply properties
        self._apply_properties()
        
        # Load image from ImageLocation if specified
        if self.ImageLocation:
            self.Load(self.ImageLocation)
        
        self._place_control(self.Width, self.Height)
        
        # Bind events
        self._tk_widget.bind('<Button-1>', self._on_click)
        self._tk_widget.bind('<Double-Button-1>', self._on_double_click)
        self._tk_widget.bind('<Configure>', self._on_paint)
        self._tk_widget.bind('<Enter>', self._on_mouse_enter)
        self._tk_widget.bind('<Leave>', self._on_mouse_leave)
        self._tk_widget.bind('<ButtonPress>', self._on_mouse_down)
        self._tk_widget.bind('<ButtonRelease>', self._on_mouse_up)
        
        # Auto-register with parent container if necessary
        self._auto_register_with_parent()
    
    def _apply_properties(self):
        """Apply properties to the Tkinter widget."""
        config = {}
        if self.Image:
            config['image'] = self.Image
        if self.BackColor:
            config['bg'] = self.BackColor
        if self.BorderStyle == BorderStyle.FixedSingle:
            config['relief'] = 'solid'
            config['bd'] = 1
        elif self.BorderStyle == BorderStyle.Fixed3D:
            config['relief'] = 'sunken'
            config['bd'] = 2
        else:
            config['relief'] = 'flat'
            config['bd'] = 0
        if not self.Enabled:
            config['state'] = 'disabled'
        if config:
            self._tk_widget.config(**config)
        
        # SizeMode mapping
        # Note: StretchImage and Zoom require PIL (Pillow) which might not be available.
        # We use standard Tkinter anchors for Normal and CenterImage.
        if self.SizeMode == PictureBoxSizeMode.Normal:
            self._tk_widget.config(anchor='nw')
        elif self.SizeMode == PictureBoxSizeMode.CenterImage:
            self._tk_widget.config(anchor='center')
        elif self.SizeMode == PictureBoxSizeMode.AutoSize:
            # In AutoSize, the control resizes to the image
            # Tkinter Label does this by default if we don't force geometry
            # But ControlBase forces geometry. We might need to update Width/Height
            if self.Image:
                try:
                    w = self.Image.width()
                    h = self.Image.height()
                    self.Width = w
                    self.Height = h
                    self._place_control(w, h)
                except:
                    pass
        elif self.SizeMode == PictureBoxSizeMode.StretchImage:
            # Requires PIL or complex canvas scaling. 
            # Placeholder for standard Tkinter (no-op or center)
            self._tk_widget.config(anchor='center')
        elif self.SizeMode == PictureBoxSizeMode.Zoom:
            # Requires PIL. Placeholder.
            self._tk_widget.config(anchor='center')
            
    def Load(self, url=None):
        """Loads the image synchronously."""
        if url:
            self.ImageLocation = url
        
        if self.ImageLocation:
            self._load_image_from_location()

    def LoadAsync(self, url=None):
        """Loads the image asynchronously."""
        if url:
            self.ImageLocation = url
            
        # Simple threading wrapper for async load
        import threading
        def async_loader():
            try:
                self._load_image_from_location()
                # Schedule event on main thread
                self._tk_widget.after(0, lambda: self.LoadCompleted(self, EventArgs.Empty))
            except Exception as e:
                self._tk_widget.after(0, lambda: self.Error(self, e))
                
        threading.Thread(target=async_loader, daemon=True).start()

    def CancelAsync(self):
        """Cancels an asynchronous image load."""
        # Not fully implemented in this simple wrapper
        pass

    def _load_image_from_location(self):
        """Load the image from ImageLocation."""
        try:
            # Basic implementation using tk.PhotoImage for supported formats (GIF, PNG, PPM/PGM)
            # For JPG and others, PIL is required but we avoid hard dependency here to prevent errors
            import threading
            new_image = tk.PhotoImage(file=self.ImageLocation)
            self.Image = new_image
            
            # Update UI on main thread if called from background
            def update_ui():
                self._tk_widget.config(image=self.Image)
                self._apply_properties()
                
            if threading.current_thread() is threading.main_thread():
                update_ui()
            else:
                self._tk_widget.after(0, update_ui)
                
        except Exception as e:
            if self.ErrorImage:
                # Load error image if available
                pass
            # Trigger Error event
            self.Error(self, e)
    
    def set_Image(self, image):
        """Set the image."""
        self.Image = image
        self._tk_widget.config(image=image)
        self._apply_properties()
    
    def set_ImageLocation(self, location):
        """Set the image location."""
        self.ImageLocation = location
        # Note: Setting ImageLocation doesn't auto-load in this implementation 
        # unless Load() is called, matching some .NET behaviors where you set then Load.
        # However, the constructor calls Load() if ImageLocation is set.
    
    def set_SizeMode(self, mode):
        """Set the SizeMode."""
        if self.SizeMode != mode:
            self.SizeMode = mode
            self._apply_properties()
            self.SizeModeChanged(self, EventArgs.Empty)
    
    def set_BorderStyle(self, style):
        """Set the border style."""
        self.BorderStyle = style
        self._apply_properties()
    
    def set_Enabled(self, enabled):
        """Set whether it is enabled."""
        self.Enabled = enabled
        self._tk_widget.config(state='normal' if enabled else 'disabled')

    def _on_click(self, event):
        """Handler for Click event."""
        self.Click()
    
    def _on_double_click(self, event):
        """Handler for DoubleClick event."""
        self.DoubleClick()
    
    def _on_paint(self, event):
        """Handler for Paint and Resize events."""
        self.Paint()
        self.Resize()


class CanvasLine:
    """
    Represents a line (System.Windows.Shapes.Line from WPF/UWP) drawn on a Canvas.
    
    Note: For simple horizontal/vertical separators in WinForms-style layouts,
    use the Line class instead. This class is for drawing arbitrary lines on a Canvas.

    Usage - Option 1 (property assignment):
        line = CanvasLine(form)
        line.X1 = 10
        line.Y1 = 10
        line.X2 = 200
        line.Y2 = 100
        line.Stroke = "blue"
        line.StrokeThickness = 2

    Usage - Option 2 (dictionary):
        line = CanvasLine(form, {'X1': 10, 'Y1': 10, 'X2': 200, 'Y2': 100, 'Stroke': 'blue'})
    """
    
    def __init__(self, master_form, props=None):
        defaults = {
            'X1': 0,
            'Y1': 0,
            'X2': 100,
            'Y2': 100,
            'Name': "",
            'Stroke': "black",
            'StrokeThickness': 1,
            'StrokeDashArray': None,
            'Visible': True,
            'Tag': None
        }
        
        if props:
            defaults.update(props)
        
        # Resolve the canvas or master widget
        if hasattr(master_form, '_canvas'):
            self._canvas = master_form._canvas
        elif hasattr(master_form, '_tk_widget') and isinstance(master_form._tk_widget, tk.Canvas):
            self._canvas = master_form._tk_widget
        elif isinstance(master_form, tk.Canvas):
            self._canvas = master_form
        else:
            # If there is no canvas, create one
            master_widget = getattr(master_form, '_root', getattr(master_form, '_tk_widget', getattr(master_form, '_frame', master_form)))
            self._canvas = tk.Canvas(master_widget, bg='white')
            self._canvas.pack(fill='both', expand=True)
        
        # WPF/UWP-like properties
        self.Name = defaults['Name']
        self.X1 = defaults['X1']
        self.Y1 = defaults['Y1']
        self.X2 = defaults['X2']
        self.Y2 = defaults['Y2']
        self.Stroke = defaults['Stroke']
        self.StrokeThickness = defaults['StrokeThickness']
        self.StrokeDashArray = defaults['StrokeDashArray']  # List like [5, 2, 3, 2] for dash pattern
        self._visible = defaults['Visible']
        self._tag = defaults['Tag']
        
        # UIElement Events (WPF/UWP)
        self.MouseEnter = lambda sender, e: None
        self.MouseLeave = lambda sender, e: None
        self.MouseLeftButtonDown = lambda sender, e: None
        self.MouseLeftButtonUp = lambda sender, e: None
        self.MouseMove = lambda sender, e: None
        self.MouseRightButtonDown = lambda sender, e: None
        self.MouseRightButtonUp = lambda sender, e: None
        self.ManipulationStarted = lambda sender, e: None
        self.ManipulationDelta = lambda sender, e: None
        self.ManipulationCompleted = lambda sender, e: None
        
        # Draw the line
        self._line_id = None
        self._draw()
        
        # Bind events if the line is visible
        if self.Visible:
            self._bind_events()

    @property
    def Tag(self):
        """Gets or sets the object that contains data about the control."""
        return self._tag

    @Tag.setter
    def Tag(self, value):
        self._tag = value
    
    @property
    def Visible(self):
        """Get the line visibility."""
        return self._visible
    
    @Visible.setter
    def Visible(self, value):
        """Sets the line visibility."""
        self.set_Visible(value)
    
    def _draw(self):
        """Draw or update the line on the canvas."""
        if self._line_id:
            # Update existing line
            self._canvas.coords(self._line_id, self.X1, self.Y1, self.X2, self.Y2)
            self._canvas.itemconfig(self._line_id, 
                                   fill=self.Stroke, 
                                   width=self.StrokeThickness,
                                   dash=self._convert_dash_array())
        else:
            # Create new line
            self._line_id = self._canvas.create_line(
                self.X1, self.Y1, self.X2, self.Y2,
                fill=self.Stroke,
                width=self.StrokeThickness,
                dash=self._convert_dash_array(),
                tags=self.Name if self.Name else None
            )
        
        # Apply visibility
        if self.Visible:
            self._canvas.itemconfig(self._line_id, state='normal')
        else:
            self._canvas.itemconfig(self._line_id, state='hidden')
    
    def _convert_dash_array(self):
        """Convert StrokeDashArray to tkinter format."""
        if self.StrokeDashArray:
            # Tkinter uses a tuple of ints for dash
            return tuple(int(x) for x in self.StrokeDashArray)
        return None
    
    def _bind_events(self):
        """Bind mouse events to the line."""
        if self._line_id:
            self._canvas.tag_bind(self._line_id, '<Enter>', self._on_mouse_enter)
            self._canvas.tag_bind(self._line_id, '<Leave>', self._on_mouse_leave)
            self._canvas.tag_bind(self._line_id, '<Button-1>', self._on_mouse_left_down)
            self._canvas.tag_bind(self._line_id, '<ButtonRelease-1>', self._on_mouse_left_up)
            self._canvas.tag_bind(self._line_id, '<Motion>', self._on_mouse_move)
            self._canvas.tag_bind(self._line_id, '<Button-3>', self._on_mouse_right_down)
            self._canvas.tag_bind(self._line_id, '<ButtonRelease-3>', self._on_mouse_right_up)
    
    def _on_mouse_enter(self, event):
        """Handler for MouseEnter."""
        self.MouseEnter(self, event)
    
    def _on_mouse_leave(self, event):
        """Handler for MouseLeave."""
        self.MouseLeave(self, event)
    
    def _on_mouse_left_down(self, event):
        """Handler for MouseLeftButtonDown."""
        self.MouseLeftButtonDown(self, event)
        # Basic simulation of ManipulationStarted
        self.ManipulationStarted(self, event)
    
    def _on_mouse_left_up(self, event):
        """Handler for MouseLeftButtonUp."""
        self.MouseLeftButtonUp(self, event)
        # Basic simulation of ManipulationCompleted
        self.ManipulationCompleted(self, event)
    
    def _on_mouse_move(self, event):
        """Handler for MouseMove."""
        self.MouseMove(self, event)
        # Basic simulation of ManipulationDelta
        self.ManipulationDelta(self, event)
    
    def _on_mouse_right_down(self, event):
        """Handler for MouseRightButtonDown."""
        self.MouseRightButtonDown(self, event)
    
    def _on_mouse_right_up(self, event):
        """Handler for MouseRightButtonUp."""
        self.MouseRightButtonUp(self, event)
    
    # Properties con getters/setters
    
    def set_X1(self, value):
        """Set the X coordinate of the start point."""
        self.X1 = value
        self._draw()
    
    def set_Y1(self, value):
        """Set the Y coordinate of the start point."""
        self.Y1 = value
        self._draw()
    
    def set_X2(self, value):
        """Set the X coordinate of the end point."""
        self.X2 = value
        self._draw()
    
    def set_Y2(self, value):
        """Set the Y coordinate of the end point."""
        self.Y2 = value
        self._draw()
    
    def set_Stroke(self, value):
        """Set the line color."""
        self.Stroke = value
        if self._line_id:
            self._canvas.itemconfig(self._line_id, fill=value)
    
    def set_StrokeThickness(self, value):
        """Set the line thickness."""
        self.StrokeThickness = value
        if self._line_id:
            self._canvas.itemconfig(self._line_id, width=value)
    
    def set_StrokeDashArray(self, value):
        """Set the line dash pattern.

        Parameter:
        - value: List of numbers [dash, space, dash, space, ...]
                Example: [5, 2] = 5px dash, 2px space
                         [5, 2, 1, 2] = 5px dash, 2px space, 1px dash, 2px space
        """
        self.StrokeDashArray = value
        if self._line_id:
            self._canvas.itemconfig(self._line_id, dash=self._convert_dash_array())
    
    def set_Visible(self, value):
        """Set the line visibility."""
        self._visible = value
        self._draw()
    
    def Delete(self):
        """Delete the line from the canvas."""
        if self._line_id:
            self._canvas.delete(self._line_id)
            self._line_id = None
    
    def BringToFront(self):
        """Bring the line to front (above other items)."""
        if self._line_id:
            self._canvas.tag_raise(self._line_id)
    
    def SendToBack(self):
        """Send the line to back (behind other items)."""
        if self._line_id:
            self._canvas.tag_lower(self._line_id)


############# Container Controls #############

class GroupBox(ControlBase):
    """Represents a GroupBox (bordered container with title) similar to Windows Forms.

    The GroupBox is a container control used to visually and logically group related
    controls. It provides an optional titled border to visually delimit a section.

    IMPORTANT - Recommended Usage:
    For better performance, create controls directly with the GroupBox as parent:

        # 1. Create the GroupBox
        group = GroupBox(form, {
            'Text': 'Settings',
            'Left': 10,
            'Top': 10,
            'Width': 300,
            'Height': 200
        })
        form.AddControl(group)

        # 2. Create controls WITH THE GROUPBOX as parent (RECOMMENDED)
        radio1 = RadioButton(group, {'Text': 'Option 1', 'Left': 10, 'Top': 10})
        group.AddControl(radio1)

        radio2 = RadioButton(group, {'Text': 'Option 2', 'Left': 10, 'Top': 40})
        group.AddControl(radio2)

    Note: Control Left/Top coordinates are relative to the GroupBox content area
    (just below the title), where (0,0) is the top-left corner.

    Alternative usage (less efficient):
        # Create controls with the form as parent
        radio1 = RadioButton(form, {'Text': 'Option 1'})
        group.AddControl(radio1)  # The widget will be recreated internally
    """
    
    def __init__(self, master_form, props=None):
        """Initializes a GroupBox.

        Args:
            master_form: The parent form or container
            props: Optional dictionary with initial properties
        """
        # Default values
        defaults = {
            'Left': 0,
            'Top': 0,
            'Width': 200,
            'Height': 100,
            'Name': '',
            'Text': 'GroupBox',
            'Enabled': True,
            'Visible': True,
            'BackColor': None,
            'ForeColor': None,
            'Font': None,
            'Padding': (10, 20, 10, 10),  # left, top, right, bottom
            'TabStop': False,
            'TabIndex': 0,
            'FlatStyle': FlatStyle.Standard,
            'AutoSize': False,
            'AutoSizeMode': AutoSizeMode.GrowOnly,
            'MinimumSize': None,
            'MaximumSize': None,
            'LabelAnchor': 'nw'
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Control", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Control")
        
        # Resolve the Tkinter widget and store the parent container
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Store the parent container for auto-registration
        self._parent_container = parent_container
        
        self.Name = defaults['Name']
        self._text = defaults['Text']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.BackColor = defaults['BackColor']
        self.ForeColor = defaults['ForeColor']
        self.Font = defaults['Font']
        self._padding = defaults['Padding']
        self.TabStop = defaults['TabStop']
        self.TabIndex = defaults['TabIndex']
        self.FlatStyle = defaults['FlatStyle']
        self.AutoSize = defaults['AutoSize']
        self.AutoSizeMode = defaults['AutoSizeMode']
        self.MinimumSize = defaults['MinimumSize']
        self.MaximumSize = defaults['MaximumSize']
        # Initialize with (0, 0) so GrowOnly mode calculates size correctly the first time
        self._original_size = (0, 0)
        self._initial_size = (defaults['Width'], defaults['Height'])
        self.LabelAnchor = defaults['LabelAnchor']
        
        self.Location = (self.Left, self.Top)
        self.Size = (self.Width, self.Height)
        
        # Get padding
        padding = self._padding
        if isinstance(padding, tuple) and len(padding) == 4:
            padx_left, pady_top, padx_right, pady_bottom = padding
            padx = (padx_left + padx_right) // 2
            pady = (pady_top + pady_bottom) // 2
        elif isinstance(padding, tuple) and len(padding) == 2:
            padx, pady = padding
        else:
            padx, pady = 10, 20  # Default values
        
        # Map FlatStyle to relief
        relief = 'groove'
        borderwidth = 2
        if self.FlatStyle == FlatStyle.Flat:
            relief = 'solid'
            borderwidth = 1
        elif self.FlatStyle == FlatStyle.Popup:
            relief = 'raised'
            borderwidth = 2
        elif self.FlatStyle == FlatStyle.System:
            relief = 'groove'
            borderwidth = 2
        
        # Create the main widget as a LabelFrame
        # This automatically handles title and margins
        self._tk_widget = tk.LabelFrame(
            self.master,
            text=self._text,
            width=self.Width,
            height=self.Height,
            relief=relief,
            borderwidth=borderwidth,
            bg=self.BackColor if self.BackColor else 'SystemButtonFace',
            fg=self.ForeColor if self.ForeColor else 'black',
            font=self.Font if self.Font else ('TkDefaultFont', 9),
            padx=padx,
            pady=pady,
            labelanchor=self.LabelAnchor,
            takefocus=0
        )
        
        # Ensure the frame does not shrink
        self._tk_widget.pack_propagate(False)
        self._tk_widget.grid_propagate(False)
        
        # Create the inner Frame as the container for child controls
        # With relwidth=1 and relheight=1, this Frame automatically respects
        # the LabelFrame padding
        self._container = tk.Frame(
            self._tk_widget,
            bg=self.BackColor if self.BackColor else self._tk_widget.cget('bg'),
            highlightthickness=0
        )
        # Use place with rel* so it respects the LabelFrame padding
        self._container.place(x=0, y=0, relwidth=1, relheight=1)
        self._container.pack_propagate(False)
        self._container.grid_propagate(False)
        
        # Add _root for container functionality
        self._root = master_form._root if hasattr(master_form, '_root') else master_form
        
        # List of controls inside the GroupBox
        self.Controls = []
        
        # Windows Forms events for GroupBox
        self.ControlAdded = lambda control=None: None
        self.ControlRemoved = lambda control=None: None
        self.Enter = lambda sender=None, e=None: None  # When entering the GroupBox (Tab)
        self.Leave = lambda sender=None, e=None: None  # When leaving the GroupBox
        self.Click = lambda sender=None, e=None: None  # When clicking in the GroupBox area
        self.Paint = lambda sender=None, e=None: None  # When it needs to be painted
        
        # Position the GroupBox
        if self.Visible:
            self._place_control(self.Width, self.Height)
        else:
            self._tk_widget.place_forget()
            
        # Apply Dock and Anchor if specified in props
        if 'Dock' in defaults and defaults['Dock']:
            self.Dock = defaults['Dock']
        if 'Anchor' in defaults and defaults['Anchor'] is not None:
            self.Anchor = defaults['Anchor']
        if 'Margin' in defaults:
            self.Margin = defaults['Margin']
        if 'Padding' in defaults:
            self.Padding = defaults['Padding']
        
        # Bind events
        self._tk_widget.bind('<Configure>', self._on_paint)
        self._tk_widget.bind('<Button-1>', self._on_click)
        self._tk_widget.bind('<FocusIn>', self._on_enter)
        self._tk_widget.bind('<FocusOut>', self._on_leave)
        self._bind_common_events()
        
        # Auto-register with the parent container if necessary
        self._auto_register_with_parent()
    
    def AddControl(self, control):
        """Adds a control to the GroupBox with relative positions.

        Implements the Windows Forms visibility hierarchy:
        - The control is added to the GroupBox (becomes its parent)
        - The control is visible only if its own Visible property is True
            AND the GroupBox (and all its parents) are also visible

        RECOMMENDATION: For better performance, create controls directly
        with the GroupBox as parent:
                button = Button(groupbox, {'Text': 'OK', 'Left': 10, 'Top': 10})

        If the control was already created with another parent (e.g., form), it
        will be recreated with the GroupBox as the new parent, which has a
        performance cost.
        """
        self.Controls.append(control)
        
        # If the widget already exists with a different master, recreate it
        if hasattr(control, '_tk_widget') and control._tk_widget and control.master != self._container:
            old_widget = control._tk_widget
            widget_class = type(old_widget)
            widget_class_name = widget_class.__name__
            
            # Save the full widget configuration
            old_config = {}
            try:
                for key in old_widget.keys():
                    try:
                        old_config[key] = old_widget.cget(key)
                    except Exception:
                        pass
            except Exception:
                pass
            
            # Remove the old widget from its location
            try:
                old_widget.place_forget()
            except Exception:
                pass
            
            # Destroy the old widget
            old_widget.destroy()
            
            # Change the control's master to the internal container
            control.master = self._container
            
            # Recreate the widget according to its type with the new master
            if widget_class_name == 'Button':
                control._tk_widget = tk.Button(self._container)
                if hasattr(control, '_handle_click_event'):
                    control._tk_widget.config(command=control._handle_click_event)
            elif widget_class_name == 'Checkbutton':
                control._tk_widget = tk.Checkbutton(self._container)
                if hasattr(control, '_checked_var'):
                    control._tk_widget.config(variable=control._checked_var)
                if hasattr(control, '_handle_checkchanged_event'):
                    control._tk_widget.config(command=control._handle_checkchanged_event)
            elif widget_class_name == 'Radiobutton':
                control._tk_widget = tk.Radiobutton(self._container)
                if hasattr(control, '_checked_var'):
                    control._tk_widget.config(variable=control._checked_var)
                if hasattr(control, '_handle_checkchanged_event'):
                    control._tk_widget.config(command=control._handle_checkchanged_event)
            elif widget_class_name == 'Entry':
                control._tk_widget = tk.Entry(self._container)
                if hasattr(control, '_text_var'):
                    control._tk_widget.config(textvariable=control._text_var)
            elif widget_class_name == 'Label':
                control._tk_widget = tk.Label(self._container)
            elif widget_class_name == 'Text':
                control._tk_widget = tk.Text(self._container)
            elif widget_class_name == 'Listbox':
                control._tk_widget = tk.Listbox(self._container)
            elif widget_class_name == 'Frame':
                control._tk_widget = tk.Frame(self._container)
            elif widget_class_name == 'LabelFrame':
                control._tk_widget = tk.LabelFrame(self._container)
            else:
                # Generic type - try to recreate with basic constructor
                try:
                    control._tk_widget = widget_class(self._container)
                except Exception:
                    # If fails, create a generic Frame
                    control._tk_widget = tk.Frame(self._container)
            
            # Restore visual configuration
            for key, value in old_config.items():
                try:
                    control._tk_widget.config(**{key: value})
                except Exception:
                    pass
            
            # Restore common bindings
            if hasattr(control, '_bind_common_events'):
                control._bind_common_events()
            
            # For Button, unbind Button-1 because it uses command
            if widget_class_name == 'Button':
                try:
                    control._tk_widget.unbind('<Button-1>')
                except Exception:
                    pass
        else:
            # If it has no widget yet, just change the master
            control.master = self._container
        
        # Register this GroupBox as the container wrapper for the hierarchy
        if not hasattr(self._container, '_control_wrapper'):
            self._container._control_wrapper = self
        
        # Register this GroupBox as the container wrapper for the hierarchy
        if not hasattr(self._tk_widget, '_control_wrapper'):
            self._tk_widget._control_wrapper = self
        
        # Inherit container properties
        if hasattr(control, 'Enabled'):
            # If GroupBox is disabled, child should be visually disabled
            # We do not change the child's logical Enabled property if possible,
            # but for now we ensure visual consistency.
            if not self.Enabled:
                if hasattr(control, '_tk_widget'):
                    try:
                        control._tk_widget.config(state='disabled')
                    except tk.TclError:
                        pass  # Some widgets do not support 'state'
        
        # Apply visibility hierarchy:
        # The control is shown only if its _visible is True AND the GroupBox is visible
        if hasattr(control, '_visible'):
            control_should_be_visible = control._visible and self.get_Visible()
            if control_should_be_visible:
                # Show the control (place with in_= will use the new master)
                control._place_control()
            else:
                # Hide the control
                if hasattr(control, '_tk_widget') and control._tk_widget:
                    control._tk_widget.place_forget()
        else:
            # If the control does not have _visible, use default behavior
            if self.get_Visible():
                control._place_control()
        
        # Invoke ControlAdded event
        self.ControlAdded(control)
        
        # Apply AutoSize if enabled
        if self.AutoSize:
            self._apply_autosize()
    
    def RemoveControl(self, control):
        """Removes a control from the GroupBox."""
        if control in self.Controls:
            self.Controls.remove(control)
            if hasattr(control, '_tk_widget') and control._tk_widget:
                control._tk_widget.place_forget()
            # Invoke ControlRemoved event
            self.ControlRemoved(control)
            # Apply AutoSize if enabled
            if self.AutoSize:
                self._apply_autosize()
    
    def _apply_autosize(self):
        """Apply GroupBox-specific AutoSize.

        The GroupBox is resized to encompass all child controls plus the title,
        respecting AutoSizeMode:
        - GrowOnly: Grows but does not shrink below the original size
        - GrowAndShrink: Adjusts exactly to the content

        Uses control properties directly to obtain sizes.
        """
        if not self.AutoSize or not self.Controls:
            return
        
        # Prevent recursion: if already applying AutoSize, return
        if getattr(self, '_applying_autosize', False):
            return
        
        # Set flag to prevent child notifications from causing recursion
        self._applying_autosize = True
        
        try:
            # KEY: Force Tkinter geometry update
            if self._container:
                self._container.update_idletasks()
                
            # Get border width
            border_width = 0
            try:
                border_width = int(self._tk_widget.cget('borderwidth'))
            except:
                pass
            
            # Calculate the area required to contain all child controls
            max_right = 0
            max_bottom = 0
            
            for control in self.Controls:
                # Use control's Left/Top/Width/Height properties directly
                # These are already updated when the control is positioned
                if hasattr(control, 'Left') and hasattr(control, 'Top'):
                    x = control.Left
                    y = control.Top
                    width = getattr(control, 'Width', 0)
                    height = getattr(control, 'Height', 0)
                    
                    control_right = x + width
                    control_bottom = y + height
                    max_right = max(max_right, control_right)
                    max_bottom = max(max_bottom, control_bottom)
            
            # Add padding
            padding = self.Padding
            if len(padding) == 4:
                pad_left, pad_top, pad_right, pad_bottom = padding
                padx = (pad_left + pad_right) // 2
                pady = (pad_top + pad_bottom) // 2
            else:
                padx, pady = padding
                
            # Calculate title metrics
            title_height = 0
            title_width = 0
            if self.Text:
                try:
                    font_val = self.Font
                    if not font_val:
                        font_val = ('TkDefaultFont', 9)
                    f = tkfont.Font(font=font_val)
                    title_height = f.metrics("linespace")
                    title_width = f.measure(self.Text)
                    # Add some margin for the title
                    title_height += 5
                    title_width += 20
                except:
                    title_height = 20
                    title_width = 0
                
            # Calculate required size including padding, border AND title
            # Add extra padding for right side to avoid visual clipping
            extra_right_padding = 30
            content_width = max_right + padx * 2 + border_width * 2 + extra_right_padding
            required_width = max(content_width, title_width + border_width * 2 + extra_right_padding)
            
            required_height = max_bottom + pady * 2 + border_width * 2 + title_height
            
            # Apply AutoSizeMode
            if self.AutoSizeMode == AutoSizeMode.GrowOnly:
                # Do not shrink below the maximum size ever reached
                original_width, original_height = self._original_size
                required_width = max(required_width, original_width)
                required_height = max(required_height, original_height)
                # Update _original_size to the new maximum
                self._original_size = (required_width, required_height)
            # GrowAndShrink: use the calculated size as-is
            
            # Apply MinimumSize constraints
            if self.MinimumSize:
                min_width, min_height = self.MinimumSize
                required_width = max(required_width, min_width)
                required_height = max(required_height, min_height)
            
            # Apply MaximumSize constraints
            if self.MaximumSize:
                max_width, max_height = self.MaximumSize
                if max_width > 0:
                    required_width = min(required_width, max_width)
                if max_height > 0:
                    required_height = min(required_height, max_height)
            
            # Update dimensions only if changed to avoid infinite recursion loops
            if self.Width != required_width or self.Height != required_height:
                # Adjust position if Anchored to Right/Bottom
                self._apply_autosize_anchor_adjustment(required_width, required_height)
                
                # 7. Update dimensions
                self.Width = int(required_width)
                self.Height = int(required_height)
                
                # Force update of the widget size
                self._tk_widget.config(width=self.Width, height=self.Height)
                
                # 8. Reposition with the new size (always, visible or not)
                self._place_control(self.Width, self.Height)
                
                # 9. Notify parent container that this control's size changed
                self._notify_parent_layout_changed()
        finally:
            # Clear flag
            self._applying_autosize = False
    
    @property
    def Enabled(self):
        return self._enabled

    @Enabled.setter
    def Enabled(self, value):
        """Sets whether the GroupBox is enabled and propagates to child controls."""
        self._enabled = value
        if self._tk_widget:
            # GroupBox itself might change appearance (e.g. text color)
            # But LabelFrame doesn't have a 'state' that grays out everything automatically in Tkinter
            # So we manually propagate to children
            pass
            
        # Propagate to children
        if hasattr(self, 'Controls'):
            for control in self.Controls:
                if hasattr(control, '_tk_widget'):
                    try:
                        # If GroupBox is disabled, child is disabled.
                        # If GroupBox is enabled, child state depends on its own Enabled property.
                        child_enabled = value and getattr(control, 'Enabled', True)
                        state = 'normal' if child_enabled else 'disabled'
                        control._tk_widget.config(state=state)
                    except tk.TclError:
                        pass

    @property
    def FlatStyle(self):
        """Gets the flat style appearance of the group box."""
        return getattr(self, '_flat_style', 'Standard')

    @FlatStyle.setter
    def FlatStyle(self, value):
        """Sets the flat style appearance of the group box."""
        self._flat_style = value
        if self._tk_widget:
            relief = 'groove'
            borderwidth = 2
            if value == 'Flat':
                relief = 'solid'
                borderwidth = 1
            elif value == 'Popup':
                relief = 'raised'
                borderwidth = 2
            elif value == 'System':
                relief = 'groove'
                borderwidth = 2
            
            self._tk_widget.config(relief=relief, borderwidth=borderwidth)

    def set_Visible(self, value):
        """Set the GroupBox visibility and propagate it to its controls.

        Implements the Windows Forms visibility hierarchy:
        - When the GroupBox is hidden (Visible = False), it automatically hides
            all its child controls regardless of their individual Visible property
        - When the GroupBox becomes visible (Visible = True), it only shows the
            child controls whose individual Visible property is True
        """
        # Use the base implementation that handles the complete hierarchy
        super().set_Visible(value)
    
    @property
    def Padding(self):
        """Get the GroupBox inner padding."""
        return self._padding
    
    @Padding.setter
    def Padding(self, value):
        """Set the GroupBox inner padding."""
        if isinstance(value, int):
            value = (value, value, value, value)
        elif isinstance(value, (tuple, list)) and len(value) == 2:
            value = (value[0], value[1], value[0], value[1])
            
        self._padding = value
        
        if self._tk_widget:
            pad_left, pad_top, pad_right, pad_bottom = value
            padx = (pad_left + pad_right) // 2
            pady = (pad_top + pad_bottom) // 2
            self._tk_widget.config(padx=padx, pady=pady)
        # Apply AutoSize if enabled
        if self.AutoSize:
            self._apply_autosize()
    
    @property
    def Text(self):
        """Get the GroupBox title text."""
        return self._text
    
    @Text.setter
    def Text(self, value):
        """Set the GroupBox title text."""
        self._text = value
        if self._tk_widget:
            self._tk_widget.config(text=value)
    
    @property
    def Font(self):
        """Gets the GroupBox title font."""
        return self._font
    
    @Font.setter
    def Font(self, value):
        """Set the GroupBox title font."""
        self._font = value
        if self._tk_widget and isinstance(self._tk_widget, tk.LabelFrame):
            self._tk_widget.config(font=value if value else ('TkDefaultFont', 9))
    
    @property
    def ForeColor(self):
        """Gets the GroupBox title text color."""
        return self._forecolor
    
    @ForeColor.setter
    def ForeColor(self, value):
        """Set the GroupBox title text color."""
        self._forecolor = value
        if self._tk_widget and isinstance(self._tk_widget, tk.LabelFrame):
            self._tk_widget.config(fg=value if value else 'black')
    
    def _on_paint(self, event):
        """Handler for Paint event."""
        self.Paint()
    
    def _on_enter(self, event):
        """Handler for Enter event."""
        self.Enter()
    
    def _on_leave(self, event):
        """Handler for Leave event."""
        self.Leave()


class Panel(ControlBase, ScrollableControlMixin):
    """Represents a Panel (container) similar to Windows Forms.

    The Panel is a container control that groups other controls.

    RECOMMENDED USAGE - Create controls with the Panel as the parent:

        panel = Panel(form, {'Left': 10, 'Top': 10, 'Width': 300, 'Height': 200})
        form.AddControl(panel)

        # Create controls WITH THE PANEL as parent
        button = Button(panel, {'Text': 'OK', 'Left': 10, 'Top': 10})
        panel.AddControl(button)

    Control Left/Top coordinates are relative to the Panel.
    """
    
    def __init__(self, master_form, props=None):
        """Initializes a Panel.

        Args:
            master_form: The parent form or container
            props: Optional dictionary with initial properties
        """
        # Default values
        defaults = {
            'Left': 0,
            'Top': 0,
            'Width': 200,
            'Height': 100,
            'Name': '',
            'Text': '',
            'Enabled': True,
            'Visible': True,
            'BackColor': 'lightgray',
            'ForeColor': None,
            'BackgroundImage': None,
            'BorderStyle': BorderStyle.None_,
            'AutoScroll': False,
            'AutoScrollMinSize': None,
            'AutoScrollPosition': (0, 0),
            'AutoScrollMargin': (0, 0),
            'Dock': DockStyle.None_,
            'Padding': (0, 0),
            'AutoSize': False,
            'AutoSizeMode': AutoSizeMode.GrowOnly,
            'MinimumSize': None,
            'MaximumSize': None
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Control", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Control")
        
        # Resolve the Tkinter widget and store the parent container
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Store the parent container for auto-registration
        self._parent_container = parent_container
        
        self.Name = defaults['Name']
        self._text = defaults['Text']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.BackColor = defaults['BackColor']
        self.ForeColor = defaults['ForeColor']
        self.BackgroundImage = defaults['BackgroundImage']
        self.BorderStyle = defaults['BorderStyle']
        
        # Initialize scroll properties using the Mixin
        self._init_scroll_properties(defaults)
        
        self.Dock = defaults['Dock']
        if 'Anchor' in defaults and defaults['Anchor'] is not None:
            self.Anchor = defaults['Anchor']
        if 'Margin' in defaults:
            self.Margin = defaults['Margin']
            
        self._padding = defaults['Padding']
        self.AutoSize = defaults['AutoSize']
        self.AutoSizeMode = defaults['AutoSizeMode']
        self.MinimumSize = defaults['MinimumSize']
        self.MaximumSize = defaults['MaximumSize']
        # Initialize with (0, 0) so GrowOnly mode calculates size correctly the first time
        self._original_size = (0, 0)
        self._initial_size = (defaults['Width'], defaults['Height'])
        
        self.Location = (self.Left, self.Top)
        
        # Create the Tkinter widget (Frame or LabelFrame depending on title)
        # Calculate padding for pack (inner container)
        pack_padx = 0
        pack_pady = 0
        
        if isinstance(self.Padding, tuple):
            if len(self.Padding) == 4:
                pack_padx = (self.Padding[0], self.Padding[2]) # left, right
                pack_pady = (self.Padding[1], self.Padding[3]) # top, bottom
            elif len(self.Padding) == 2:
                pack_padx = self.Padding[0]
                pack_pady = self.Padding[1]
        
        # Map BorderStyle from VB.NET to tkinter
        relief_map = {
            'None': 'flat',
            'Fixed3D': 'groove',
            'FixedSingle': 'solid',
            'fixed_single': 'solid',
            'fixed_3d': 'groove',
            'flat': 'flat',
            'groove': 'groove',
            'raised': 'raised',
            'ridge': 'ridge',
            'solid': 'solid',
            'sunken': 'sunken',
            BorderStyle.None_: 'flat',
            BorderStyle.Fixed3D: 'groove',
            BorderStyle.FixedSingle: 'solid',
            1: 'solid',  # FixedSingle as int
            2: 'groove'  # Fixed3D as int, more visible
        }
        
        config = {
            'width': self.Width,
            'height': self.Height,
            'bg': self.BackColor,
            'relief': relief_map.get(self.BorderStyle, 'flat')
            # Removed padx/pady from config as they are for geometry request, not internal padding
        }
        
        # If BorderStyle is 'FixedSingle' or 'solid', add border
        if self.BorderStyle in ['FixedSingle', 'solid', 'fixed_single', BorderStyle.FixedSingle, 1]:
            config['borderwidth'] = 3  # Increased from 1 to 3 for better visibility
        elif self.BorderStyle in ['Fixed3D', 'fixed_3d', 'sunken', 'raised', 'groove', 'ridge', BorderStyle.Fixed3D, 2]:
            config['borderwidth'] = 3  # Increased from 2 to 3 for better visibility
        else:
            config['borderwidth'] = 0
        
        # Create main widget (Always Frame for Panel, no caption)
        if self.BackgroundImage:
            config['image'] = self.BackgroundImage
        self._tk_widget = tk.Frame(self.master, **config)
        
        # Ensure the frame does not shrink
        self._tk_widget.pack_propagate(False)
        self._tk_widget.grid_propagate(False)
        
        # Configure scroll infrastructure using the Mixin
        self._setup_scroll_infrastructure(self._tk_widget, self.BackColor)
        
        # If AutoScroll is False, create an inner container to respect padding/borders
        # This mimics GroupBox behavior and ensures padding works with 'place'
        if not self.AutoScroll:
            self._container = tk.Frame(self._tk_widget, bg=self.BackColor, highlightthickness=0)
            # Use place to fill the outer frame, but leave space for the border
            # Calculate border width to adjust inner container positioning
            border_width = config.get('borderwidth', 0)
            if border_width > 0:
                # Position inner container with offset to show border
                self._container.place(x=border_width, y=border_width, 
                                     relwidth=1, relheight=1,
                                     width=-2*border_width, height=-2*border_width)
            else:
                # No border, fill completely
                self._container.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Define _container for AddControl (required if ScrollableControlMixin is not active)
        if not hasattr(self, '_container'):
            self._container = self._tk_widget
        
        # Add _root for container functionality
        self._root = master_form._root
        
        # Bind events
        self._tk_widget.bind('<Configure>', self._on_paint)
        self._tk_widget.bind('<Button-1>', self._on_click)
        self._tk_widget.bind('<Double-Button-1>', self._on_double_click)
        self._tk_widget.bind('<Enter>', self._on_mouse_enter)
        self._tk_widget.bind('<Leave>', self._on_mouse_leave)
        self._tk_widget.bind('<ButtonPress>', self._on_mouse_down)
        self._tk_widget.bind('<ButtonRelease>', self._on_mouse_up)
        
        # List of child controls inside the panel
        self.Controls = []
        
        # VB events
        self.ControlAdded = lambda control: None
        self.ControlRemoved = lambda control: None
        
        # Auto-register with the parent container if needed
        self._auto_register_with_parent()
        
        # Position the Panel (moved to end to ensure correct placement)
        if self.Visible:
            try:
                self.master.update_idletasks()
            except Exception:
                pass
            self._place_control(self.Width, self.Height)
        else:
            self._tk_widget.place_forget()



    def AddControl(self, control):
        """Adds a control to the Panel with relative positions.

        Implements Windows Forms visibility hierarchy:
        - The control is added to the Panel (becomes its parent)
        - The control is visible only if its own Visible property is True
            AND the Panel (and all its parents) are also visible
        """
        self.Controls.append(control)
        # Change the control's master to the appropriate container (scroll_frame or main widget)
        control.master = self._container
        
        # Register this Panel as the container wrapper for parent hierarchy
        if not hasattr(self._container, '_control_wrapper'):
            self._container._control_wrapper = self
        
        # Inherit container properties
        if hasattr(control, 'Enabled'):
            # If Panel is disabled, child should be visually disabled
            # We do not change the child's logical Enabled property if possible,
            # but for now we ensure visual consistency.
            if not self.Enabled:
                if hasattr(control, '_tk_widget'):
                    try:
                        control._tk_widget.config(state='disabled')
                    except tk.TclError:
                        pass
        
        # Apply visibility hierarchy:
        # The control is shown only if its _visible is True AND the Panel is visible
        if hasattr(control, '_visible'):
            control_should_be_visible = control._visible and self.get_Visible()
            if control_should_be_visible:
                # Show the control
                control._place_control()
            else:
                # Hide the control
                if hasattr(control, '_tk_widget') and control._tk_widget:
                    control._tk_widget.place_forget()
        else:
            # If the control has no _visible, use default behavior
            if self.get_Visible():
                control._place_control()

        # Trigger ControlAdded event
        self.ControlAdded(control)


        # Update scroll region if AutoScroll is enabled
        if self.AutoScroll:
            self._update_scroll_region()
        
        # Apply AutoSize if enabled
        if self.AutoSize:
            self._apply_autosize_panel()

    @property
    def Enabled(self):
        return self._enabled

    @Enabled.setter
    def Enabled(self, value):
        """Sets whether the panel is enabled and propagates to child controls."""
        self._enabled = value
        if self._tk_widget:
            self._apply_visual_config()
            
        # Propagate to children
        if hasattr(self, 'Controls'):
            for control in self.Controls:
                # We update the visual state of children to match parent
                # In a full implementation, we would check both parent and child enabled state
                if hasattr(control, '_tk_widget'):
                    try:
                        # If Panel is disabled, child is disabled.
                        # If Panel is enabled, child state depends on its own Enabled property.
                        child_enabled = value and getattr(control, 'Enabled', True)
                        state = 'normal' if child_enabled else 'disabled'
                        control._tk_widget.config(state=state)
                        
                        # If child is also a container (has Controls), we might need to propagate further
                        # But if we rely on the child's Enabled property not changing, 
                        # we only need to update visual if the child doesn't handle parent state.
                        # For now, this visual update is the most important part.
                    except tk.TclError:
                        pass

    def set_Visible(self, value):
        """Sets panel visibility and propagates it to its child controls.

        Implements Windows Forms visibility hierarchy:
        - When the Panel is hidden (Visible = False), it automatically hides
            all its child controls, regardless of their individual Visible property
        - When the Panel becomes visible (Visible = True), it only shows child
            controls whose individual Visible property is True
        """
        # Use the base implementation which handles the full hierarchy
        # This will automatically propagate to all children
        super().set_Visible(value)

    def RemoveControl(self, control):
        """Removes a control from the Panel."""
        if control in self.Controls:
            self.Controls.remove(control)
            
            # Hide the widget visually
            if hasattr(control, '_tk_widget') and control._tk_widget:
                control._tk_widget.place_forget()
            
            # Update scroll region if AutoScroll is enabled
            if self.AutoScroll:
                self._update_scroll_region()
                
            self.ControlRemoved(control)
            # Apply AutoSize if enabled
            if self.AutoSize:
                self._apply_autosize_panel()
    
    def _apply_autosize_panel(self):
        """Applies AutoSize specific behavior for Panel.

        The Panel resizes to encompass all its child controls,
        respecting AutoSizeMode:
        - GrowOnly: Grows but does not shrink below the original size
        - GrowAndShrink: Adjusts exactly to the content

        Uses Tkinter's winfo_reqwidth() and winfo_reqheight() to get actual sizes.
        """
        if not self.AutoSize or not self.Controls:
            return
        
        # Prevent recursion: if already applying AutoSize, return
        if getattr(self, '_applying_autosize', False):
            return
        
        # Set flag to prevent child notifications from causing recursion
        self._applying_autosize = True
        
        try:
            # KEY: Force Tkinter geometry update
            if self._container:
                self._container.update_idletasks()
                
            # Get border width to account for it
            border_width = 0
            try:
                border_width = int(self._tk_widget.cget('borderwidth'))
            except:
                pass
            
            # Calculate the area required to contain all child controls
            max_right = 0
            max_bottom = 0
            
            for control in self.Controls:
                # Use control's Left/Top/Width/Height properties directly
                # These are already updated when the control is positioned
                if hasattr(control, 'Left') and hasattr(control, 'Top'):
                    x = control.Left
                    y = control.Top
                    width = getattr(control, 'Width', 0)
                    height = getattr(control, 'Height', 0)
                    
                    control_right = x + width
                    control_bottom = y + height
                    max_right = max(max_right, control_right)
                    max_bottom = max(max_bottom, control_bottom)
            
            # Add padding
            padding = self.Padding
            if len(padding) == 4:
                pad_left, pad_top, pad_right, pad_bottom = padding
                padx = (pad_left + pad_right) // 2
                pady = (pad_top + pad_bottom) // 2
            else:
                padx, pady = padding
                
            # Calculate required size including padding AND border
            required_width = max_right + padx * 2 + border_width * 2
            required_height = max_bottom + pady * 2 + border_width * 2
            
            # Apply AutoSizeMode
            if self.AutoSizeMode == AutoSizeMode.GrowOnly:
                # Do not shrink below the maximum size ever reached
                original_width, original_height = self._original_size
                required_width = max(required_width, original_width)
                required_height = max(required_height, original_height)
                # Update _original_size to the new maximum
                self._original_size = (required_width, required_height)
            # GrowAndShrink: use the calculated size as-is
            
            # Apply MinimumSize constraints
            if self.MinimumSize:
                min_width, min_height = self.MinimumSize
                required_width = max(required_width, min_width)
                required_height = max(required_height, min_height)
            
            # Apply MaximumSize constraints
            if self.MaximumSize:
                max_width, max_height = self.MaximumSize
                if max_width > 0:
                    required_width = min(required_width, max_width)
                if max_height > 0:
                    required_height = min(required_height, max_height)
            
            # Update dimensions only if changed to avoid infinite recursion loops
            if self.Width != required_width or self.Height != required_height:
                # Adjust position if Anchored to Right/Bottom
                self._apply_autosize_anchor_adjustment(required_width, required_height)
                
                # 7. Update dimensions
                self.Width = required_width
                self.Height = required_height
                
                # Force update of the widget size
                self._tk_widget.config(width=self.Width, height=self.Height)
                
                # 8. Reposition with the new size (always, visible or not)
                self._place_control(self.Width, self.Height)
                
                # 9. Notify parent container that this control's size changed
                self._notify_parent_layout_changed()
        finally:
            # Clear flag
            self._applying_autosize = False

    def _apply_autosize(self):
        """Delegate AutoSize to the panel-specific implementation.
        
        This method is called by the AutoSize setter in ControlBase.
        """
        self._apply_autosize_panel()

    @property
    def BorderStyle(self):
        """Gets the border style of the panel."""
        return getattr(self, '_border_style', 'None')

    @BorderStyle.setter
    def BorderStyle(self, value):
        """Sets the border style of the panel."""
        self._border_style = value
        if self._tk_widget:
            # Map BorderStyle from VB.NET to tkinter
            relief_map = {
                'None': 'flat',
                'Fixed3D': 'sunken',
                'FixedSingle': 'solid',
                'flat': 'flat',
                'groove': 'groove',
                'raised': 'raised',
                'ridge': 'ridge',
                'solid': 'solid',
                'sunken': 'sunken'
            }
            
            relief = relief_map.get(value, 'flat')
            
            if value in ['FixedSingle', 'solid']:
                borderwidth = 1
            elif value == 'Fixed3D':
                borderwidth = 2
            elif value not in ['None', 'flat']:
                borderwidth = 2
            else:
                borderwidth = 0
                
            self._tk_widget.config(relief=relief, borderwidth=borderwidth)

    @property
    def Padding(self):
        """Get the Panel inner padding."""
        return self._padding

    @Padding.setter
    def Padding(self, value):
        """Set the Panel inner padding."""
        if isinstance(value, int):
            value = (value, value, value, value)
        elif isinstance(value, (tuple, list)) and len(value) == 2:
            value = (value[0], value[1], value[0], value[1])
            
        self._padding = value
        
        if self._tk_widget:
            # Tkinter only supports symmetric padding for frame
            pad_left, pad_top, pad_right, pad_bottom = value
            padx = (pad_left + pad_right) // 2
            pady = (pad_top + pad_bottom) // 2
            self._tk_widget.config(padx=padx, pady=pady)
            if self.AutoSize:
                self._apply_autosize_panel()

    @property
    def Text(self):
        """Gets the Panel title."""
        return self._text
    
    @Text.setter
    def Text(self, value):
        """Set the Panel title.
        
        Note: Unlike GroupBox, the Text property in Panel does not display a caption.
        It is stored but has no visual effect.
        """
        self._text = value

    def _on_paint(self, event):
        """Handler for Paint and Resize events."""
        self.Paint()
        self.Resize()


class Line:
    """
    Represents a horizontal or vertical line separator.
    
    Simplified class for creating visual separators in forms.
    A Line is a simple Frame control used as a visual separator.
    
    Usage - Horizontal line:
        line = Line(form, {'Left': 20, 'Top': 50, 'Width': 400, 'Height': 2})
    
    Usage - Vertical line:
        line = Line(form, {'Left': 20, 'Top': 50, 'Width': 2, 'Height': 400})
    
    Usage - With custom color:
        line = Line(form, {'Left': 20, 'Top': 50, 'Width': 400, 'Height': 2, 'BackColor': 'blue'})
    """
    
    def __init__(self, master_form, props=None):
        """Initialize a Line separator.
        
        Args:
            master_form: The parent form or container
            props: Optional dictionary with properties (Left, Top, Width, Height, BackColor)
        """
        # Set defaults optimized for a line separator
        defaults = {
            'Left': 0,
            'Top': 0,
            'Width': 100,
            'Height': 1,
            'BackColor': 'black',
            'Visible': True
        }
        
        if props:
            defaults.update(props)
        
        # Store properties
        self.Left = defaults['Left']
        self.Top = defaults['Top']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.BackColor = defaults['BackColor']
        self.Visible = defaults['Visible']
        
        # Get the master widget
        if hasattr(master_form, '_container'):
            self.master = master_form._container
        elif hasattr(master_form, '_root'):
            self.master = master_form._root
        else:
            self.master = master_form
        
        # Create a Frame widget for the line
        self._tk_widget = tk.Frame(
            self.master,
            width=self.Width,
            height=self.Height,
            bg=self.BackColor,
            relief='flat',
            bd=0
        )
        
        # Place the widget
        if self.Visible:
            self._tk_widget.place(x=self.Left, y=self.Top, width=self.Width, height=self.Height)



class TabPage(ControlBase, ScrollableControlMixin):
    """
    Represents a tab page for TabControl with VB.NET-like properties and AUTO-REGISTRATION.

    Now inherits from ControlBase, providing full control functionality including:
    - Width/Height/Size properties with proper placement
    - Dock/Anchor support
    - AutoSize capabilities
    - Margin/Padding
    - BringToFront/SendToBack
    - And all other ControlBase features

    NEW - Use with AUTO-REGISTRATION (recommended):
        tab_control = TabControl(form, {...})
        tab1 = TabPage(tab_control, {'Text': 'Tab 1'})
        # You NO LONGER need: tab_control.AddTab(tab1)! It auto-registers

    Traditional usage (without parent):
        page = TabPage({'Text': 'My Tab', 'Name': 'tabPage1'})
        tab_control.AddTab(page)  # Manual registration required
    """
    
    def __init__(self, parent=None, props=None):
        # If parent is not a dict, it's the TabControl; if it's a dict, it's props (compatibility)
        if isinstance(parent, dict):
            props = parent
            parent = None
        
        defaults = {
            'Text': "TabPage",
            'Name': "",
            'Left': 0,
            'Top': 0,
            'Width': 200,
            'Height': 100,
            'Enabled': True,
            'Visible': True,
            'ImageIndex': -1,
            'ImageKey': "",
            'ToolTipText': "",
            'UseVisualStyleBackColor': True,
            'Padding': (3, 3),
            'BackColor': None,
            'ForeColor': None,
            'Font': None,
            'AutoScroll': False,
            'AutoScrollMinSize': None,
            'AutoScrollPosition': (0, 0),
            'AutoScrollMargin': (0, 0),
            'Dock': None,
            'Anchor': [AnchorStyles.Top, AnchorStyles.Left],
            'AutoSize': False,
            'AutoSizeMode': AutoSizeMode.GrowOnly,
            'Margin': (3, 3, 3, 3),
            'MinimumSize': None,
            'MaximumSize': None
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Control", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Control")
        
        # Determine master widget for ControlBase initialization
        # If there is a parent (TabControl), use its internal widget (Notebook) as master
        if parent and hasattr(parent, '_tk_widget'):
            master_for_frame = parent._tk_widget
        elif parent and hasattr(parent, 'master_form'):
            master_for_frame = parent.master_form._root
        else:
            master_for_frame = tk._default_root if tk._default_root else tk.Tk()
        
        # Initialize ControlBase with dummy position (TabPages are managed by TabControl)
        ControlBase.__init__(self, master_for_frame, defaults['Left'], defaults['Top'])
        
        # Store parent container reference for potential future use
        self._parent_container = parent
        
        # TabPage-specific properties
        self.Name = defaults['Name'] or defaults['Text']
        self._text_value = defaults['Text']
        self._parent = None  # Assigned by TabControl
        self._image_index = defaults['ImageIndex']
        self._image_key = defaults['ImageKey']
        self._tooltip_text = defaults['ToolTipText']
        self.UseVisualStyleBackColor = defaults['UseVisualStyleBackColor']
        
        # Initialize scroll properties
        self._init_scroll_properties(defaults)
        
        # Create the frame with padding
        padding = defaults['Padding']
        if len(padding) == 4:
            pad_left, pad_top, pad_right, pad_bottom = padding
            padx = (pad_left + pad_right) // 2
            pady = (pad_top + pad_bottom) // 2
        else:
            padx, pady = padding
        
        self._tk_widget = tk.Frame(master_for_frame, padx=padx, pady=pady)
        
        # Create alias for compatibility with TabControl.AddTab()
        self._frame = self._tk_widget
        
        # Apply initial size from ControlBase
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        
        # Apply visual properties
        if defaults['BackColor']:
            self.BackColor = defaults['BackColor']
        if defaults['ForeColor']:
            self.ForeColor = defaults['ForeColor']
        if defaults['Font']:
            self.Font = defaults['Font']
        
        # Configure scroll infrastructure
        self._setup_scroll_infrastructure(self._tk_widget, self.BackColor)
        
        # Initialize Controls list
        self.Controls = []

        # VB events (override ControlBase defaults where needed)
        self.ControlAdded = lambda control=None: None
        self.ControlRemoved = lambda control=None: None
        self.ChangeUICues = lambda sender, e: None
        self.Disposed = lambda sender, e: None

        # Bind events
        self._tk_widget.bind('<Configure>', self._on_configure)
        self._tk_widget.bind('<FocusIn>', lambda e: self.ChangeUICues(self, e))
        self._tk_widget.bind('<FocusOut>', lambda e: self.ChangeUICues(self, e))
        
        # Auto-register with the parent TabControl if provided
        if parent and hasattr(parent, 'AddTab'):
            # Assign _root before registration so child controls can use it
            if hasattr(parent, 'master_form') and hasattr(parent.master_form, '_root'):
                self._root = parent.master_form._root
            parent.AddTab(self)

    @property
    def Parent(self):
        """Get the parent control of the TabPage.

        The parent of a TabPage is the TabControl that contains it.
        Follows the Visual Basic .NET pattern where each TabPage
        knows its parent TabControl.

        Returns:
            The parent TabControl if it exists, None otherwise.
        """
        return getattr(self, '_parent', None)
    
    @Parent.setter
    def Parent(self, value):
        """Set the parent control of the TabPage."""
        self._parent = value

    @property
    def Text(self):
        """Gets or sets the text displayed on the tab."""
        return self._text_value

    @Text.setter
    def Text(self, value):
        self._text_value = value
        # Update the tab text in the parent TabControl if it exists
        if self.Parent and hasattr(self.Parent, '_tk_widget'):
            try:
                self.Parent._tk_widget.tab(self._frame, text=value)
            except tk.TclError:
                pass

    # Override BackColor property to add scroll infrastructure support
    @property
    def BackColor(self):
        """Gets the background color of the TabPage."""
        return self._backcolor

    @BackColor.setter
    def BackColor(self, value):
        """Sets the background color with scroll infrastructure support."""
        self._backcolor = value
        if self._tk_widget:
            self._tk_widget.config(bg=value)
            # Also update the canvas background if it exists (from ScrollableControlMixin)
            if hasattr(self, '_canvas') and self._canvas:
                self._canvas.config(bg=value)
            if hasattr(self, '_scroll_frame') and self._scroll_frame:
                self._scroll_frame.config(bg=value)

    @property
    def ImageIndex(self):
        """Gets or sets the index of the image displayed on the tab."""
        return self._image_index

    @ImageIndex.setter
    def ImageIndex(self, value):
        self._image_index = value
        # Note: Updating the image requires ImageList support in TabControl which is complex in ttk

    @property
    def ImageKey(self):
        """Gets or sets the key of the image displayed on the tab."""
        return self._image_key

    @ImageKey.setter
    def ImageKey(self, value):
        self._image_key = value
        # Note: Updating the image requires ImageList support in TabControl which is complex in ttk

    @property
    def ToolTipText(self):
        """Gets or sets the tooltip text for the tab."""
        return self._tooltip_text

    @ToolTipText.setter
    def ToolTipText(self, value):
        self._tooltip_text = value
        # Note: ttk.Notebook does not support tooltips on tabs natively

    def Show(self):
        """Shows the control. 
        Note: For TabPage, this only affects the Visible property. 
        To show/hide the tab, add/remove it from TabControl.TabPages."""
        self._visible = True
        # If we wanted to mimic .NET behavior where Show() doesn't add it back to TabControl automatically
        # unless it was just hidden, we'd need more complex logic.
        # For now, we just set the flag.

    def Hide(self):
        """Hides the control.
        Note: For TabPage, this only affects the Visible property.
        To show/hide the tab, add/remove it from TabControl.TabPages."""
        self._visible = False

    def Dispose(self):
        """Releases all resources used by the TabPage."""
        if self.Parent and hasattr(self.Parent, 'RemoveTab'):
            self.Parent.RemoveTab(self)
        
        if self._frame:
            self._frame.destroy()
            self._frame = None
            
        self.Disposed(self, None)
    
    def AddControl(self, control):
        """Add a control to the TabPage with relative positions.

        NOTE: You no longer need to call this method manually when creating
        a control with TabPage as the parent. Auto-registration handles it.

        Implements the Windows Forms visibility hierarchy:
        - The control is added to the TabPage (becomes its parent)
        - The control will only be visible if its own Visible property is True
            AND the TabPage (and all its parents) are also visible

        RECOMMENDED USAGE - Create controls directly with the TabPage as parent:
                tab_page = TabPage({'Text': 'Page 1'})
                button = Button(tab_page, {'Text': 'OK', 'Left': 10, 'Top': 10})
                # You NO LONGER need: tab_page.AddControl(button)! It auto-registers

        Left/Top coordinates are relative to the TabPage.
        """
        # Avoid duplicates
        if control in self.Controls:
            return
        
        self.Controls.append(control)
        control.master = self._container

        # Register this TabPage as the wrapper of the frame for the parent hierarchy
        if not hasattr(self._container, '_control_wrapper'):
            self._container._control_wrapper = self
        
        # Inherit properties from the container
        if hasattr(control, 'Enabled'):
            control.Enabled = self.Enabled
            if hasattr(control, '_tk_widget'):
                try:
                    control._tk_widget.config(state='normal' if self.Enabled else 'disabled')
                except tk.TclError:
                    pass
        
        # Apply visibility hierarchy:
        # The control is only shown if its _visible is True AND the TabPage is visible
        if hasattr(control, '_visible'):
            # Calculate effective visibility of the TabPage
            tabpage_visible = getattr(self, '_visible', True)
            if hasattr(self, 'Parent') and self.Parent:
                # If the TabPage has a Parent (TabControl), check its visibility
                parent_visible = getattr(self.Parent, '_visible', True)
                tabpage_visible = tabpage_visible and parent_visible
            
            control_should_be_visible = control._visible and tabpage_visible
            if control_should_be_visible:
                # Show the control
                control._place_control()
            else:
                # Hide the control
                if hasattr(control, '_tk_widget') and control._tk_widget:
                    control._tk_widget.place_forget()
        else:
            # If the control does not have _visible, use default behavior
            control._place_control()
        
        # Reapply Dock or Anchor to integrate it with the new container
        if hasattr(control, '_dock') and control._dock and control._dock != 'None':
            control._apply_dock()
        elif hasattr(control, '_anchor') and control._anchor:
            # Recalculate distances for Anchor with the new container
            control.master.after(0, control._calculate_initial_distances)
        
        # Update scroll region if AutoScroll is enabled
            self._update_scroll_region()
            
        self.ControlAdded(control)

    def _on_configure(self, event):
        """Handler for Paint and Resize events."""
        self.Paint()
        self.Resize()

    def RemoveControl(self, control):
        """Removes a control from the TabPage."""
        if control in self.Controls:
            self.Controls.remove(control)
            
            # Update scroll region if AutoScroll is enabled
            if self.AutoScroll:
                self._update_scroll_region()
                
            self.ControlRemoved(control)


class TabControl(ControlBase):
    """
    Represents a TabControl with tabs.

    Usage - Option 1 (property assignment):
        tab = TabControl(form)
        tab.Left = 10
        tab.Top = 10
        tab.Width = 400
        tab.Height = 300

    Usage - Option 2 (dictionary):
        tab = TabControl(form, {'Left': 10, 'Top': 10, 'Width': 400, 'Height': 300})
    """
    
    def __init__(self, master_form, props=None):
        # Default values
        defaults = {
            'Left': 10,
            'Top': 10,
            'Width': 300,
            'Height': 200,
            'Name': "",
            'TabPages': None,
            'SelectedIndex': 0,
            'ImageList': None,
            'Appearance': TabAppearance.Normal,
            'Alignment': TabAlignment.Top,
            'Multiline': False,
            'SizeMode': TabSizeMode.Normal,
            'Enabled': True,
            'Visible': True,
            'Padding': (0, 0),
            'HotTrack': False,
            'Dock': None,  # 'Fill', 'Top', 'Bottom', 'Left', 'Right' - following VB.NET pattern
            'Margin': (0, 0, 0, 0)  # (left, top, right, bottom) - external margins
        }
        
        # Merge with props if provided
        if props:
            defaults.update(props)
        
        # Resolve the Tkinter widget and save the parent container
        # Resolve the Tkinter widget and save the parent container
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Save the parent container for auto-registration
        self._parent_container = parent_container
        # Save initial Dock to apply it after creating the widget
        initial_dock = defaults.get('Dock', None)
        
        # Assign properties
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        
        # Store master_form for container access
        self.master_form = master_form
        
        # VB Properties
        self.Name = defaults['Name']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.TabPages = defaults['TabPages'] or []
        self.SelectedIndex = defaults['SelectedIndex']
        self.ImageList = defaults['ImageList']
        self.Appearance = defaults['Appearance']
        self.Alignment = defaults['Alignment']
        self.Multiline = defaults['Multiline']
        self.SizeMode = defaults['SizeMode']
        self.Padding = defaults['Padding']  # (padx, pady)
        self.HotTrack = defaults['HotTrack']  # Placeholder
        self.Margin = defaults['Margin']  # (left, top, right, bottom) - external margins
        
        # VB Events
        self.SelectedIndexChanged = lambda: None
        self.Selecting = lambda sender, e: None
        self.Selected = lambda sender, e: None
        self.Deselecting = lambda sender, e: None
        self.Deselected = lambda sender, e: None
        self.DrawItem = lambda sender, e: None
        self.ControlAdded = lambda control: None
        self.ControlRemoved = lambda control: None
        
        # Create a unique style for this TabControl instance to support custom Alignment
        self._style_name = f"Custom.TNotebook_{id(self)}"
        self._style = ttk.Style()
        
        # Create the new style by copying the layout from TNotebook
        # This is required for the style to be recognized as a valid notebook style
        try:
            self._style.layout(self._style_name, self._style.layout("TNotebook"))
        except tk.TclError:
            pass
        
        # Configure the tab style (padding, font)
        # Note: TNotebook.Tab is the default, we create a specific one
        self._style.configure(f"{self._style_name}.Tab", 
                       padding=[15, 10],  # More horizontal and vertical padding
                       font=('TkDefaultFont', 10))  # Explicit font
        
        # Create the Tkinter widget (Notebook) with the custom style
        self._tk_widget = ttk.Notebook(self.master, style=self._style_name)
        
        # Apply Alignment (TabStripPlacement)
        self._update_alignment_style()
        
        # Apply configurations
        config = {}
        padding = self.Padding
        if len(padding) == 4:
            pad_left, pad_top, pad_right, pad_bottom = padding
            padx = (pad_left + pad_right) // 2
            pady = (pad_top + pad_bottom) // 2
        else:
            padx, pady = padding
        config['padding'] = (padx, pady)
        if config:
            self._tk_widget.config(**config)
        
        # Apply Dock (if specified) or normal placement
        if initial_dock and initial_dock != 'None':
            self.Dock = initial_dock
        else:
            self._place_control(self.Width, self.Height)
        
        # Track selected tab for events
        self._last_selected = self.SelectedIndex
        self._tk_widget.bind('<<NotebookTabChanged>>', self._on_tab_changed)
        
        # Add initial TabPages if any
        for tab in self.TabPages:
            self.AddTab(tab)
        
        # Set initial SelectedIndex
        if self.TabPages and 0 <= self.SelectedIndex < len(self.TabPages):
            self._tk_widget.select(self.SelectedIndex)
        
        # Auto-register with parent container if necessary
        self._auto_register_with_parent()

    @property
    def Alignment(self):
        """Gets or sets the area of the control (for example, along the top) where the tabs align."""
        return self._alignment

    @Alignment.setter
    def Alignment(self, value):
        self._alignment = value
        self._update_alignment_style()

    def _update_alignment_style(self):
        """Updates the tab position based on Alignment property."""
        if not hasattr(self, '_style_name') or not self._style:
            return
        
        # Map TabAlignment to ttk tabposition
        # TabAlignment: Top=0, Bottom=1, Left=2, Right=3
        position_map = {
            TabAlignment.Top: 'n',
            TabAlignment.Bottom: 's',
            TabAlignment.Left: 'w',
            TabAlignment.Right: 'e'
        }
        
        # Handle both Enum and integer values
        position = 'n'
        if isinstance(self._alignment, TabAlignment):
            position = position_map.get(self._alignment, 'n')
        elif isinstance(self._alignment, int):
            # Try to map int to enum
            try:
                enum_val = TabAlignment(self._alignment)
                position = position_map.get(enum_val, 'n')
            except ValueError:
                pass
                
        self._style.configure(self._style_name, tabposition=position)

    def AddTab(self, tab_page):
        """Add a TabPage to the TabControl with AUTO-REGISTRATION.

        IMPORTANT: You no longer need to call this method manually.
        Creating TabPage(tab_control, props) will auto-register it.

        Example (NEW - with auto-registration):
            tab1 = TabPage(tab_control, {'Text': 'Tab 1'})
            # You no longer need: tab_control.AddTab(tab1)!
        """
        # Avoid duplicates
        if tab_page in self.TabPages:
            return
            
        self.TabPages.append(tab_page)
        tab_page.Parent = self  # Assign Parent
        tab_page._root = self.master_form._root  # Assign _root for compatibility with child controls
        self._tk_widget.add(tab_page._frame, text=tab_page.Text)
        # Apply image if ImageList and ImageIndex/ImageKey
        if self.ImageList and hasattr(tab_page, 'ImageIndex') and tab_page.ImageIndex >= 0:
            # Placeholder: ttk.Notebook does not support images easily; use compound or custom
            pass
        # Force an update so that the tab text displays correctly
        if hasattr(self, 'master_form') and hasattr(self.master_form, 'Invalidate'):
            self.master_form.Invalidate()
        self.ControlAdded(tab_page)

    def InsertTab(self, index, tab_page):
        """Insert a TabPage at a specific index."""
        if tab_page in self.TabPages:
            self.RemoveTab(tab_page)
        
        self.TabPages.insert(index, tab_page)
        tab_page.Parent = self
        tab_page._root = self.master_form._root
        
        # ttk.Notebook.insert(index, child, **kw)
        self._tk_widget.insert(index, tab_page._frame, text=tab_page.Text)
        
        self.ControlAdded(tab_page)

    def RemoveTab(self, tab_page):
        """Remove a TabPage from the TabControl."""
        if tab_page in self.TabPages:
            index = self.TabPages.index(tab_page)
            self.TabPages.remove(tab_page)
            self._tk_widget.forget(tab_page._frame)
            self.ControlRemoved(tab_page)
            # If it was selected, select another or none
            if self.get_SelectedIndex() == index:
                if self.TabPages:
                    self.set_SelectedIndex(0)
                else:
                    self._last_selected = -1

    @property
    def SelectedTab(self):
        """Get the selected TabPage."""
        if self.TabPages and 0 <= self.SelectedIndex < len(self.TabPages):
            return self.TabPages[self.SelectedIndex]
        return None

    @SelectedTab.setter
    def SelectedTab(self, tab_page):
        """Set the selected TabPage."""
        if tab_page in self.TabPages:
            old_index = self.get_SelectedIndex()
            new_index = self.TabPages.index(tab_page)
            if old_index != new_index:
                # Trigger Selecting and Deselecting
                self.Selecting(self, {'TabPage': tab_page, 'TabPageIndex': new_index, 'Cancel': False})
                if old_index >= 0:
                    self.Deselecting(self, {'TabPage': self.TabPages[old_index], 'TabPageIndex': old_index, 'Cancel': False})
                # Proceed
                if old_index >= 0:
                    self.TabPages[old_index].Leave()
                    self.Deselected(self, {'TabPage': self.TabPages[old_index], 'TabPageIndex': old_index})
                self.SelectedIndex = new_index
                self._tk_widget.select(new_index)
                tab_page.Enter()
                self.Selected(self, {'TabPage': tab_page, 'TabPageIndex': new_index})
                self.SelectedIndexChanged()
                self._last_selected = new_index

    def get_SelectedIndex(self):
        """Get the index of the selected tab."""
        try:
            return self._tk_widget.index(self._tk_widget.select())
        except Exception:
            return -1

    def set_SelectedIndex(self, index):
        """Set the index of the selected tab."""
        if 0 <= index < len(self.TabPages):
            old_index = self.get_SelectedIndex()
            if old_index != index:
                # Trigger Selecting and Deselecting
                self.Selecting(self, {'TabPage': self.TabPages[index], 'TabPageIndex': index, 'Cancel': False})
                if old_index >= 0:
                    self.Deselecting(self, {'TabPage': self.TabPages[old_index], 'TabPageIndex': old_index, 'Cancel': False})
                # Proceed
                if old_index >= 0:
                    self.TabPages[old_index].Leave()
                    self.Deselected(self, {'TabPage': self.TabPages[old_index], 'TabPageIndex': old_index})
                self.SelectedIndex = index
                self._tk_widget.select(index)
                self.TabPages[index].Enter()
                self.Selected(self, {'TabPage': self.TabPages[index], 'TabPageIndex': index})
                self.SelectedIndexChanged()
                self._last_selected = index

    def SelectTab(self, tab_identifier):
        """Select a tab by index, name, or direct reference.

        Following Visual Basic .NET pattern:
        - SelectTab(0) -> Select by index
        - SelectTab("TabPageConfig") -> Select by name
        - SelectTab(tab_page_object) -> Select by reference

        Args:
            tab_identifier: Can be int (index), str (name), or TabPage (reference)

        Examples:
            # By index
            tab_control.SelectTab(0)

            # By name
            tab_control.SelectTab("TabPageConfig")

            # By reference
            config_page = tab_control.TabPages[1]
            tab_control.SelectTab(config_page)
        """
        target_index = None
        
        # Determine the index according to the identifier type
        if isinstance(tab_identifier, int):
            # By direct index
            target_index = tab_identifier
        elif isinstance(tab_identifier, str):
            # By name (Name property)
            for i, tab in enumerate(self.TabPages):
                if tab.Name == tab_identifier:
                    target_index = i
                    break
            if target_index is None:
                raise ValueError(f"TabPage with name '{tab_identifier}' not found")
        elif isinstance(tab_identifier, TabPage):
            # By direct reference
            if tab_identifier in self.TabPages:
                target_index = self.TabPages.index(tab_identifier)
            else:
                raise ValueError("The specified TabPage does not belong to this TabControl")
        else:
            raise TypeError(f"tab_identifier must be int, str or TabPage, not {type(tab_identifier).__name__}")
        
        # Validate index and change if different from current
        if target_index is not None and 0 <= target_index < len(self.TabPages):
            current_index = self.get_SelectedIndex()
            if current_index != target_index:
                self.set_SelectedIndex(target_index)
        elif target_index is not None:
            raise IndexError(f"Index {target_index} out of range. TabPages contains {len(self.TabPages)} items")

    def _on_tab_changed(self, event):
        """Handler for tab selection changes.
        
        Implements the SelectedIndexChanged event following the VB.NET pattern:
        - Fires when the user manually changes tabs
        - Allows executing specific logic when changing views
        """
        new_index = self.get_SelectedIndex()
        if new_index != self._last_selected:
            # Trigger Selecting and Deselecting
            if new_index >= 0:
                self.Selecting(self, {'TabPage': self.TabPages[new_index], 'TabPageIndex': new_index, 'Cancel': False})
            if self._last_selected >= 0:
                self.Deselecting(self, {'TabPage': self.TabPages[self._last_selected], 'TabPageIndex': self._last_selected, 'Cancel': False})
            # Proceed
            if self._last_selected >= 0:
                self.TabPages[self._last_selected].Leave()
                self.Deselected(self, {'TabPage': self.TabPages[self._last_selected], 'TabPageIndex': self._last_selected})
            
            # Update the SelectedIndex attribute to match the widget state
            self.SelectedIndex = new_index
            
            self._last_selected = new_index
            if new_index >= 0:
                self.TabPages[new_index].Enter()
                self.Selected(self, {'TabPage': self.TabPages[new_index], 'TabPageIndex': new_index})
            self.SelectedIndexChanged()


############# Nested Controls #############

class EventArgs:
    pass
EventArgs.Empty = EventArgs()


class ListBoxObjectCollection:
    """
    Collection of items for ListBox.
    Represents the collection of items in a ListBox.
    """
    def __init__(self, owner):
        self.owner = owner
        self._items = []

    @property
    def Count(self):
        """Obtiene el número de elementos de la colección."""
        return len(self._items)

    @property
    def IsReadOnly(self):
        """Obtiene un valor que indica si la colección es de solo lectura."""
        return False

    def __getitem__(self, index):
        """Obtiene el elemento en el índice especificado."""
        return self._items[index]

    def __setitem__(self, index, value):
        """Establece el elemento en el índice especificado."""
        if self.owner.DataSource:
            raise RuntimeError("Cannot modify Items collection when DataSource is set.")
        
        self._items[index] = value
        if hasattr(self.owner, '_tk_widget') and self.owner._tk_widget:
            self.owner._tk_widget.delete(index)
            self.owner._tk_widget.insert(index, value)

    def Add(self, item):
        """Agrega un elemento a la lista de elementos de un control ListBox."""
        if self.owner.DataSource:
            raise RuntimeError("Cannot modify Items collection when DataSource is set.")
            
        self._items.append(item)
        if hasattr(self.owner, '_tk_widget') and self.owner._tk_widget:
            self.owner._tk_widget.insert(tk.END, item)
        return len(self._items) - 1

    def AddRange(self, items):
        """Agrega una matriz de elementos a la lista de elementos de ListBox."""
        if self.owner.DataSource:
            raise RuntimeError("Cannot modify Items collection when DataSource is set.")
            
        for item in items:
            self.Add(item)

    def Clear(self):
        """Quita todos los elementos de la colección."""
        if self.owner.DataSource:
            raise RuntimeError("Cannot modify Items collection when DataSource is set.")
            
        self._items.clear()
        if hasattr(self.owner, '_tk_widget') and self.owner._tk_widget:
            self.owner._tk_widget.delete(0, tk.END)

    def Contains(self, item):
        """Determina si el elemento especificado está ubicado en la colección."""
        return item in self._items

    def CopyTo(self, dest, index):
        """Copia toda la colección en una matriz de objetos existente."""
        for i, item in enumerate(self._items):
            if index + i < len(dest):
                dest[index + i] = item
            else:
                # If dest is a list, we can append
                if isinstance(dest, list):
                    dest.append(item)

    def IndexOf(self, item):
        """Devuelve el índice del elemento especificado en la colección."""
        try:
            return self._items.index(item)
        except ValueError:
            return -1

    def Insert(self, index, item):
        """Inserta un elemento en el cuadro de lista en el índice especificado."""
        if self.owner.DataSource:
            raise RuntimeError("Cannot modify Items collection when DataSource is set.")
            
        self._items.insert(index, item)
        if hasattr(self.owner, '_tk_widget') and self.owner._tk_widget:
            self.owner._tk_widget.insert(index, item)

    def Remove(self, item):
        """Quita el objeto especificado de la colección."""
        if self.owner.DataSource:
            raise RuntimeError("Cannot modify Items collection when DataSource is set.")
            
        if item in self._items:
            index = self._items.index(item)
            self._items.remove(item)
            if hasattr(self.owner, '_tk_widget') and self.owner._tk_widget:
                self.owner._tk_widget.delete(index)

    def RemoveAt(self, index):
        """Quita el elemento en el índice especificado de la colección."""
        if self.owner.DataSource:
            raise RuntimeError("Cannot modify Items collection when DataSource is set.")
            
        if 0 <= index < len(self._items):
            del self._items[index]
            if hasattr(self.owner, '_tk_widget') and self.owner._tk_widget:
                self.owner._tk_widget.delete(index)

    def __len__(self):
        return len(self._items)
    
    def __iter__(self):
        return iter(self._items)
    
    def __contains__(self, item):
        return item in self._items
        
    # Python list compatibility
    def append(self, item):
        self.Add(item)
        
    def clear(self):
        self.Clear()
        
    def insert(self, index, item):
        self.Insert(index, item)
        
    def remove(self, item):
        self.Remove(item)
        
    def index(self, item):
        return self.IndexOf(item)


class ListBoxSelectedObjectCollection:
    """Collection of selected items in a ListBox."""
    def __init__(self, owner):
        self.owner = owner

    def __getitem__(self, index):
        indices = self.owner.SelectedIndices
        if 0 <= index < len(indices):
            return self.owner.Items[indices[index]]
        raise IndexError("Index out of range")

    def __len__(self):
        return self.owner.SelectedIndices.Count

    def __iter__(self):
        for i in self.owner.SelectedIndices:
            yield self.owner.Items[i]

    def Contains(self, item):
        return self.owner.Items.Contains(item) and self.owner.GetSelected(self.owner.Items.IndexOf(item))

    def IndexOf(self, item):
        if not self.Contains(item): return -1
        for i, selected in enumerate(self):
            if selected == item:
                return i
        return -1
        
    @property
    def Count(self):
        return len(self)
        
    def CopyTo(self, dest, index):
        for i, item in enumerate(self):
            dest[index + i] = item
            
    def Clear(self):
        self.owner.ClearSelected()
        
    def Add(self, item):
        raise NotImplementedError("Cannot add directly to SelectedObjectCollection")
        
    def Remove(self, item):
        if self.Contains(item):
            self.owner.SetSelected(self.owner.Items.IndexOf(item), False)

class ListBoxSelectedIndexCollection:
    """Collection of selected indices in a ListBox."""
    def __init__(self, owner):
        self.owner = owner
        
    def __getitem__(self, index):
        sel = self.owner._tk_widget.curselection()
        return sel[index]

    def __len__(self):
        return len(self.owner._tk_widget.curselection())

    def __iter__(self):
        return iter(self.owner._tk_widget.curselection())
        
    def Contains(self, index):
        return index in self.owner._tk_widget.curselection()
        
    def IndexOf(self, index):
        sel = self.owner._tk_widget.curselection()
        try:
            return sel.index(index)
        except ValueError:
            return -1
            
    @property
    def Count(self):
        return len(self)
        
    def CopyTo(self, dest, index):
        for i, val in enumerate(self):
            dest[index + i] = val
            
    def Add(self, index):
        self.owner.SetSelected(index, True)
        
    def Remove(self, index):
        self.owner.SetSelected(index, False)
        
    def Clear(self):
        self.owner.ClearSelected()


class ListBox(ControlBase):
    """Represents a ListBox."""
    
    def __init__(self, master_form, props=None):
        """Initializes a ListBox.

        Args:
            master_form: The parent form or container
            props: Optional dictionary with initial properties
        """
        # Default values
        defaults = {
            'Left': 10,
            'Top': 170,
            'Width': 200,
            'Height': 100,
            'Name': '',
            'Items': None,
            'DataSource': None,
            'DisplayMember': '',
            'ValueMember': '',
            'SelectedIndex': -1,
            'SelectionMode': SelectionMode.One,
            'TopIndex': 0,
            'IntegralHeight': True,
            'MultiColumn': False,
            'ScrollAlwaysVisible': False,
            'HorizontalScrollbar': False,
            'HorizontalExtent': 0,
            'Sorted': False,
            'Enabled': True,
            'Font': None,
            'ForeColor': None,
            'BackColor': None,
            'UseTabStops': True,
            'UseCustomTabOffsets': False
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Window", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Window")
        
        # Resolve the Tkinter widget and store the parent container
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Store the parent container for auto-registration
        self._parent_container = parent_container
        
        self.Name = defaults['Name']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        
        self.Items = ListBoxObjectCollection(self)
        
        self._data_source = defaults['DataSource']
        self._display_member = defaults['DisplayMember']
        self._value_member = defaults['ValueMember']
        self._selection_mode = defaults['SelectionMode']
        self._top_index = defaults['TopIndex']
        self._integral_height = defaults['IntegralHeight']
        self._multi_column = defaults['MultiColumn']
        self._scroll_always_visible = defaults['ScrollAlwaysVisible']
        self._horizontal_scrollbar = defaults['HorizontalScrollbar']
        self._horizontal_extent = defaults['HorizontalExtent']
        self._sorted = defaults['Sorted']
        self._use_tab_stops = defaults['UseTabStops']
        self._use_custom_tab_offsets = defaults['UseCustomTabOffsets']
        
        self.Enabled = defaults['Enabled']
        self.Font = defaults['Font']
        self.ForeColor = defaults['ForeColor']
        self.BackColor = defaults['BackColor']
        
        # Collections
        self._selected_indices = ListBoxSelectedIndexCollection(self)
        self._selected_items = ListBoxSelectedObjectCollection(self)
        
        # Events
        self.SelectedIndexChanged = lambda sender, e: None
        self.SelectedValueChanged = lambda sender, e: None
        self.Click = lambda sender, e: None
        self.DoubleClick = lambda sender, e: None
        self.DrawItem = lambda sender, e: None
        self.MeasureItem = lambda sender, e: None
        
        # Internal
        self._updating = False
        
        # Create the Tkinter widget
        self._tk_widget = tk.Listbox(self.master)
        
        # Set selectmode
        selectmode_map = {
            SelectionMode.One: 'browse',
            SelectionMode.MultiSimple: 'multiple',
            SelectionMode.MultiExtended: 'extended',
            SelectionMode.None_: 'single'
        }
        self._tk_widget.config(selectmode=selectmode_map.get(self._selection_mode, 'browse'))
        
        # Populate
        if defaults['Items']:
            self.Items.AddRange(defaults['Items'])
            
        if self._data_source and self._display_member:
            self._populate_from_datasource()
            
        # Apply Font, ForeColor, BackColor, Enabled
        config = {}
        if self.Font:
            config['font'] = self.Font
        if self.ForeColor:
            config['fg'] = self.ForeColor
        if self.BackColor:
            config['bg'] = self.BackColor
        if not self.Enabled:
            config['state'] = 'disabled'
        if config:
            self._tk_widget.config(**config)
            
        # Scrollbars (Basic implementation - placeholder for full frame support)
        if self._scroll_always_visible:
            vscroll = tk.Scrollbar(self.master, command=self._tk_widget.yview)
            self._tk_widget.config(yscrollcommand=vscroll.set)
            vscroll.place(x=self.Left+self.Width-15, y=self.Top, height=self.Height)
            if self.MultiColumn:  # For multi-column, add horizontal scroll
                hscroll = tk.Scrollbar(self.master, orient='horizontal', command=self._tk_widget.xview)
                self._tk_widget.config(xscrollcommand=hscroll.set)
                hscroll.place(x=self.Left, y=self.Top+self.Height-15, width=self.Width)
             
        self._place_control(self.Width, self.Height)
        
        # Apply Dock and Anchor if they were specified in props
        if 'Dock' in defaults and defaults['Dock']:
            self.Dock = defaults['Dock']
        if 'Anchor' in defaults and defaults['Anchor']:
            self.Anchor = defaults['Anchor']
        
        # Bind events
        self._tk_widget.bind('<<ListboxSelect>>', self._on_selected_index_changed)
        self._tk_widget.bind('<Button-1>', self._on_click)
        self._tk_widget.bind('<Double-Button-1>', self._on_double_click)
        self._tk_widget.bind('<FocusIn>', self._on_enter)
        self._tk_widget.bind('<FocusOut>', self._on_leave)
        self._tk_widget.bind('<Key>', self._on_key_down)
        
        if self._sorted:
            self._sort_items()
            
        if defaults['SelectedIndex'] >= 0:
            self.SelectedIndex = defaults['SelectedIndex']
            
        # Auto-register with the parent container if necessary
        self._auto_register_with_parent()

    @property
    def DataSource(self):
        return self._data_source

    @DataSource.setter
    def DataSource(self, value):
        if self._data_source != value:
            self._data_source = value
            self._populate_from_datasource()
            self.DataSourceChanged(self, None)

    @property
    def DisplayMember(self):
        return self._display_member

    @DisplayMember.setter
    def DisplayMember(self, value):
        if self._display_member != value:
            self._display_member = value
            self._populate_from_datasource()
            self.DisplayMemberChanged(self, None)

    @property
    def ValueMember(self):
        return self._value_member

    @ValueMember.setter
    def ValueMember(self, value):
        if self._value_member != value:
            self._value_member = value
            self.ValueMemberChanged(self, None)

    def _populate_from_datasource(self):
        if self._data_source:
            self.Items.Clear()
            # Assuming DataSource is a list of objects
            for item in self._data_source:
                if self._display_member and hasattr(item, self._display_member):
                    self.Items.Add(getattr(item, self._display_member))
                else:
                    self.Items.Add(str(item))

    @property
    def SelectedIndex(self):
        """Gets or sets the zero-based index of the currently selected item."""
        if self.SelectedIndices.Count > 0:
            return self.SelectedIndices[0]
        return -1

    @SelectedIndex.setter
    def SelectedIndex(self, value):
        self.ClearSelected()
        if value != -1:
            self.SetSelected(value, True)

    @property
    def SelectedIndices(self):
        """Gets a collection that contains the zero-based indices of all currently selected items."""
        return self._selected_indices

    @property
    def SelectedItem(self):
        """Gets or sets the currently selected item."""
        if self.SelectedIndex != -1:
            return self.Items[self.SelectedIndex]
        return None

    @SelectedItem.setter
    def SelectedItem(self, value):
        index = self.Items.IndexOf(value)
        if index != -1:
            self.SelectedIndex = index
        else:
            self.SelectedIndex = -1

    @property
    def SelectedItems(self):
        """Gets a collection containing the currently selected items."""
        return self._selected_items

    @property
    def SelectedValue(self):
        """Gets or sets the value of the member property specified by the ValueMember property."""
        if self.SelectedIndex != -1 and self._data_source and self._value_member:
            item = self._data_source[self.SelectedIndex]
            if hasattr(item, self._value_member):
                return getattr(item, self._value_member)
        return None
        
    @SelectedValue.setter
    def SelectedValue(self, value):
        if self._data_source and self._value_member:
            for i, item in enumerate(self._data_source):
                if hasattr(item, self._value_member) and getattr(item, self._value_member) == value:
                    self.SelectedIndex = i
                    return
        self.SelectedIndex = -1

    @property
    def SelectionMode(self):
        return self._selection_mode

    @SelectionMode.setter
    def SelectionMode(self, value):
        self._selection_mode = value
        selectmode_map = {
            SelectionMode.One: 'browse',
            SelectionMode.MultiSimple: 'multiple',
            SelectionMode.MultiExtended: 'extended',
            SelectionMode.None_: 'single'
        }
        self._tk_widget.config(selectmode=selectmode_map.get(value, 'browse'))

    @property
    def Sorted(self):
        return self._sorted

    @Sorted.setter
    def Sorted(self, value):
        if self._sorted != value:
            self._sorted = value
            if self._sorted:
                self._sort_items()

    def _sort_items(self):
        # This is a bit destructive as it reloads the listbox
        # We need to get all items, sort them, and put them back
        items = list(self.Items)
        items.sort(key=lambda x: str(x).lower())
        self.Items.Clear()
        self.Items.AddRange(items)

    @property
    def TopIndex(self):
        return self._top_index

    @TopIndex.setter
    def TopIndex(self, value):
        self._top_index = value
        self._tk_widget.yview(value)

    @property
    def MultiColumn(self):
        return self._multi_column
        
    @MultiColumn.setter
    def MultiColumn(self, value):
        self._multi_column = value
        # Not fully supported in standard tk.Listbox

    @property
    def HorizontalScrollbar(self):
        return self._horizontal_scrollbar
        
    @HorizontalScrollbar.setter
    def HorizontalScrollbar(self, value):
        self._horizontal_scrollbar = value
        # Requires frame implementation

    @property
    def HorizontalExtent(self):
        return self._horizontal_extent
        
    @HorizontalExtent.setter
    def HorizontalExtent(self, value):
        self._horizontal_extent = value
        # Used for horizontal scrolling calculation

    def BeginUpdate(self):
        """Prevents the control from drawing until the EndUpdate method is called."""
        self._updating = True

    def EndUpdate(self):
        """Resumes drawing of the list box control after drawing is suspended by the BeginUpdate method."""
        self._updating = False
        self._tk_widget.update_idletasks()

    def FindString(self, s, start_index=-1):
        """Finds the first item in the ListBox that starts with the specified string."""
        s = s.lower()
        count = self.Items.Count
        for i in range(start_index + 1, count):
            if str(self.Items[i]).lower().startswith(s):
                return i
        # Wrap around
        if start_index != -1:
            for i in range(0, start_index + 1):
                if str(self.Items[i]).lower().startswith(s):
                    return i
        return -1

    def FindStringExact(self, s, start_index=-1):
        """Finds the first item in the ListBox that exactly matches the specified string."""
        s = s.lower()
        count = self.Items.Count
        for i in range(start_index + 1, count):
            if str(self.Items[i]).lower() == s:
                return i
        if start_index != -1:
            for i in range(0, start_index + 1):
                if str(self.Items[i]).lower() == s:
                    return i
        return -1

    def GetSelected(self, index):
        """Returns a value indicating whether the specified item is selected."""
        return self._tk_widget.selection_includes(index)

    def SetSelected(self, index, value):
        """Selects or clears the selection for the specified item."""
        if value:
            self._tk_widget.selection_set(index)
        else:
            self._tk_widget.selection_clear(index)

    def ClearSelected(self):
        """Unselects all items in the ListBox."""
        self._tk_widget.selection_clear(0, tk.END)

    def GetItemHeight(self, index):
        """Returns the height of an item in the ListBox."""
        # Approximation
        return 15 

    def GetItemRectangle(self, index):
        """Returns the bounding rectangle for an item in the ListBox."""
        bbox = self._tk_widget.bbox(index)
        if bbox:
            return (bbox[0], bbox[1], bbox[2], bbox[3])
        return (0,0,0,0)

    def _on_selected_index_changed(self, event=None):
        self.SelectedIndexChanged(self, None)
        self.SelectedValueChanged(self, None)

    def _on_click(self, event):
        self.Click(self, None)

    def _on_double_click(self, event):
        self.DoubleClick(self, None)

    def _on_enter(self, event):
        self.Enter(self, None)

    def _on_leave(self, event):
        self.Leave(self, None)

    def _on_key_down(self, event):
        self.KeyDown(self, event.keysym)


class CheckedListBoxObjectCollection(ListBoxObjectCollection):
    """Collection of items for CheckedListBox."""
    def __init__(self, owner):
        super().__init__(owner)

    def Add(self, item, is_checked=False):
        """Adds an item to the list of items for a CheckedListBox."""
        if self.owner.DataSource:
            raise RuntimeError("Cannot modify Items collection when DataSource is set.")
            
        self._items.append(item)
        self.owner._add_item_to_ui(item, is_checked)
        return len(self._items) - 1

    def Clear(self):
        """Removes all items from the collection."""
        if self.owner.DataSource:
            raise RuntimeError("Cannot modify Items collection when DataSource is set.")
            
        self._items.clear()
        self.owner._clear_items_ui()

    def Remove(self, item):
        """Removes the specified object from the collection."""
        if self.owner.DataSource:
            raise RuntimeError("Cannot modify Items collection when DataSource is set.")
            
        if item in self._items:
            index = self._items.index(item)
            self.RemoveAt(index)

    def RemoveAt(self, index):
        """Removes the item at the specified index within the collection."""
        if self.owner.DataSource:
            raise RuntimeError("Cannot modify Items collection when DataSource is set.")
            
        if 0 <= index < len(self._items):
            del self._items[index]
            self.owner._remove_item_from_ui(index)

    def __setitem__(self, index, value):
        """Gets or sets the item at the specified index within the collection."""
        if self.owner.DataSource:
            raise RuntimeError("Cannot modify Items collection when DataSource is set.")
            
        self._items[index] = value
        # Update UI label text
        if 0 <= index < len(self.owner._widgets):
            _, _, lbl = self.owner._widgets[index]
            lbl.config(text=str(value))

    # Inherited methods from ListBoxObjectCollection that need no override:
    # Count, IsReadOnly, __getitem__, Contains, CopyTo, IndexOf, __len__, __iter__
    
    # Methods that need override because base implementation uses _tk_widget as Listbox
    def Insert(self, index, item):
        """Inserts an item into the list box at the specified index."""
        if self.owner.DataSource:
            raise RuntimeError("Cannot modify Items collection when DataSource is set.")
            
        self._items.insert(index, item)
        # Rebuild UI is expensive but necessary for correct ordering in this implementation
        # Or implement _insert_item_to_ui
        self.owner._rebuild_ui()

    def AddRange(self, items):
        """Adds an array of items to the list of items for a ListBox."""
        if self.owner.DataSource:
            raise RuntimeError("Cannot modify Items collection when DataSource is set.")
            
        for item in items:
            self.Add(item)


class CheckedIndexCollection:
    """Collection of checked indices."""
    def __init__(self, owner):
        self.owner = owner
    
    @property
    def Count(self):
        """Gets the number of checked items."""
        return len(self)

    @property
    def IsReadOnly(self):
        """Gets a value indicating whether the collection is read-only."""
        return True

    def __getitem__(self, index):
        """Gets the index of a checked item in the CheckedListBox control."""
        indices = [i for i, var in enumerate(self.owner._vars) if var.get() != 0]
        return indices[index]

    def __len__(self):
        return len([i for i, var in enumerate(self.owner._vars) if var.get() != 0])
    
    def __iter__(self):
        """Returns an enumerator that can be used to iterate through the CheckedIndices collection."""
        return iter([i for i, var in enumerate(self.owner._vars) if var.get() != 0])
    
    def Contains(self, index):
        """Determines whether the specified index is located in the collection."""
        if 0 <= index < len(self.owner._vars):
            return self.owner._vars[index].get() != 0
        return False

    def IndexOf(self, index):
        """Returns an index into the collection of checked indexes."""
        checked_indices = [i for i, var in enumerate(self.owner._vars) if var.get() != 0]
        try:
            return checked_indices.index(index)
        except ValueError:
            return -1

    def CopyTo(self, dest, index):
        """Copies the entire collection into an existing array at a specified location within the array."""
        checked_indices = [i for i, var in enumerate(self.owner._vars) if var.get() != 0]
        for i, val in enumerate(checked_indices):
            if index + i < len(dest):
                dest[index + i] = val

    def __contains__(self, index):
        return self.Contains(index)


class CheckedItemCollection:
    """Collection of checked items."""
    def __init__(self, owner):
        self.owner = owner
    
    @property
    def Count(self):
        return len(self)

    @property
    def IsReadOnly(self):
        return True

    def __getitem__(self, index):
        items = [self.owner.Items[i] for i, var in enumerate(self.owner._vars) if var.get() != 0]
        return items[index]

    def __len__(self):
        return len([self.owner.Items[i] for i, var in enumerate(self.owner._vars) if var.get() != 0])

    def __iter__(self):
        return iter([self.owner.Items[i] for i, var in enumerate(self.owner._vars) if var.get() != 0])
    
    def Contains(self, item):
        try:
            idx = self.owner.Items.index(item)
            return self.owner.GetItemCheckState(idx) != 0
        except ValueError:
            return False

    def IndexOf(self, item):
        if not self.Contains(item):
            return -1
        checked_items = [self.owner.Items[i] for i, var in enumerate(self.owner._vars) if var.get() != 0]
        try:
            return checked_items.index(item)
        except ValueError:
            return -1

    def CopyTo(self, dest, index):
        checked_items = [self.owner.Items[i] for i, var in enumerate(self.owner._vars) if var.get() != 0]
        for i, val in enumerate(checked_items):
            if index + i < len(dest):
                dest[index + i] = val
    
    def __contains__(self, item):
        return self.Contains(item)


class CheckedListBox(ControlBase):
    """Represents a CheckedListBox (list with checkboxes)."""
    
    def __init__(self, master_form, props=None):
        """Initializes a CheckedListBox.

        Args:
            master_form: The parent form or container
            props: Optional dictionary with initial properties
        """
        # Default values
        defaults = {
            'Left': 10,
            'Top': 200,
            'Width': 200,
            'Height': 100,
            'Name': '',
            'Items': None,
            'DataSource': None,
            'DisplayMember': '',
            'ValueMember': '',
            'SelectionMode': SelectionMode.One,
            'CheckOnClick': False,
            'ThreeDCheckBoxes': True,
            'Enabled': True,
            'Visible': True,
            'Font': None,
            'ForeColor': None,
            'BackColor': 'white',
            'UseTabStops': True,
            'UseCustomTabOffsets': False
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Window", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Window")
        
        # Resolve the Tkinter widget and store the parent container
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Save the parent container for auto-registration
        self._parent_container = parent_container
        
        self.Name = defaults['Name']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        
        self.DataSource = defaults['DataSource']
        self.DisplayMember = defaults['DisplayMember']
        self.ValueMember = defaults['ValueMember']
        self.SelectionMode = defaults['SelectionMode']
        self.CheckOnClick = defaults['CheckOnClick']
        self.ThreeDCheckBoxes = defaults['ThreeDCheckBoxes']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.Font = defaults['Font']
        self.ForeColor = defaults['ForeColor']
        self.BackColor = defaults['BackColor']
        
        self._use_tab_stops = defaults['UseTabStops']
        self._use_custom_tab_offsets = defaults['UseCustomTabOffsets']
        self._custom_tab_offsets = []
        
        # Collections
        self.Items = CheckedListBoxObjectCollection(self)
        self.CheckedItems = CheckedItemCollection(self)
        self.CheckedIndices = CheckedIndexCollection(self)
        
        # Internal state
        self._vars = [] # List of IntVar (0=Unchecked, 1=Checked, 2=Indeterminate)
        self._widgets = [] # List of (Frame, Checkbutton, Label) tuples
        self._selected_index = -1
        
        # VB events (callbacks)
        self.ItemCheck = lambda item_event=None: None # item_event: {'Index': i, 'NewValue': val, 'CurrentValue': val}
        self.SelectedIndexChanged = lambda sender=None, e=None: None
        self.SelectedValueChanged = lambda sender=None, e=None: None
        self.Click = lambda sender=None, e=None: None
        self.DoubleClick = lambda sender=None, e=None: None
        
        # Create container Frame (holds Canvas + Scrollbar)
        self._container_frame = tk.Frame(self.master, width=self.Width, height=self.Height, bg=self.BackColor)
        self._tk_widget = self._container_frame
        
        # Create Scrollbar
        self._scrollbar = tk.Scrollbar(self._container_frame, orient="vertical")
        
        # Create Canvas
        self._canvas = tk.Canvas(self._container_frame, bg=self.BackColor, highlightthickness=0, yscrollcommand=self._scrollbar.set)
        self._scrollbar.config(command=self._canvas.yview)
        
        # Create Frame inside Canvas
        self._scrollable_frame = tk.Frame(self._canvas, bg=self.BackColor)
        
        # Bind configuration for scrolling
        self._scrollable_frame.bind(
            "<Configure>",
            lambda e: self._canvas.configure(
                scrollregion=self._canvas.bbox("all")
            )
        )
        
        self._canvas_window = self._canvas.create_window((0, 0), window=self._scrollable_frame, anchor="nw")
        
        # Bind canvas resize to adjust frame width
        self._canvas.bind('<Configure>', self._on_canvas_configure)
        
        self._canvas.pack(side="left", fill="both", expand=True)
        self._scrollbar.pack(side="right", fill="y")
        
        # Populate initial items
        initial_items = defaults['Items'] or []
        if self.DataSource and self.DisplayMember:
            initial_items = [getattr(item, self.DisplayMember) for item in self.DataSource]
        
        for item in initial_items:
            self.Items.Add(item)
            
        # Place control
        if self.Visible:
            self._place_control(self.Width, self.Height)
            self._container_frame.pack_propagate(False)
        else:
            self._container_frame.place_forget()
            
        # Apply Dock and Anchor
        if 'Dock' in defaults and defaults['Dock']:
            self.Dock = defaults['Dock']
        if 'Anchor' in defaults and defaults['Anchor']:
            self.Anchor = defaults['Anchor']
        
        self._auto_register_with_parent()

    def _rebuild_ui(self):
        """Rebuilds the entire UI from Items collection."""
        # Save states
        old_vars = [v.get() for v in self._vars]
        self._clear_items_ui()
        
        # Re-add all
        for i, item in enumerate(self.Items):
            # Try to preserve state if index matches
            state = old_vars[i] if i < len(old_vars) else 0
            self._add_item_to_ui(item, state)

    def _on_canvas_configure(self, event):
        """Adjusts the inner frame width to match the canvas."""
        self._canvas.itemconfig(self._canvas_window, width=event.width)

    def _add_item_to_ui(self, item, is_checked=False):
        """Adds an item to the UI.
        
        Args:
            item: The item to add.
            is_checked: Boolean or int (0, 1, 2).
        """
        index = len(self._vars)
        
        # Row Frame
        row_frame = tk.Frame(self._scrollable_frame, bg=self.BackColor)
        row_frame.pack(fill='x', expand=True)
        
        # Variable
        val = 0
        if isinstance(is_checked, bool):
            val = 1 if is_checked else 0
        elif isinstance(is_checked, int):
            val = is_checked
            
        var = tk.IntVar(value=val)
        self._vars.append(var)
        
        # Trace for ItemCheck event
        var.trace('w', lambda *args, idx=index: self._on_item_check_internal(idx))
        
        # Checkbox
        relief = 'raised' if self.ThreeDCheckBoxes else 'flat'
        # Tkinter Checkbutton doesn't support 3-state visual natively without tristateimage or theme support.
        # We will use standard behavior: 0=unchecked, 1=checked. 
        # If value is 2 (Indeterminate), it might show as checked or unchecked depending on implementation.
        # To properly support Indeterminate visual, we would need a custom widget or images.
        # For now, we map 2 to Checked visual but keep internal state as 2.
        # Or we can use 'tristatevalue' if available in ttk, but we are using tk.Checkbutton.
        # Let's just use standard Checkbutton.
        chk = tk.Checkbutton(row_frame, variable=var, bg=self.BackColor, activebackground=self.BackColor, relief=relief)
        chk.pack(side='left')
        
        lbl = tk.Label(row_frame, text=str(item), bg=self.BackColor, anchor='w')
        if self.Font:
            lbl.config(font=self.Font)
        if self.ForeColor:
            lbl.config(fg=self.ForeColor)
        
        lbl.pack(side='left', fill='x', expand=True)
        
        # Bindings
        lbl.bind('<Button-1>', lambda e, idx=index: self._on_item_click(idx))
        chk.bind('<Button-1>', lambda e, idx=index: self._on_check_click(idx))
        
        self._widgets.append((row_frame, chk, lbl))

    def _clear_items_ui(self):
        """Clears all items from UI."""
        for frame, chk, lbl in self._widgets:
            frame.destroy()
        self._widgets.clear()
        self._vars.clear()
        self._selected_index = -1

    def _remove_item_from_ui(self, index):
        """Removes an item from UI."""
        # Rebuild is safer to keep indices in sync
        self._rebuild_ui()

    def _on_item_click(self, index):
        """Handles click on item label."""
        self.SelectedIndex = index
        if self.CheckOnClick:
            # Toggle check
            current = self._vars[index].get()
            # Cycle: 0 -> 1 -> 0 (Indeterminate is only set by code)
            new_val = 1 if current == 0 else 0
            self.SetItemCheckState(index, new_val)
        self.Click()

    def _on_check_click(self, index):
        """Handles click on checkbox."""
        self.SelectedIndex = index
        # Check state change is handled by variable trace or default behavior
        self.Click()

    def _on_item_check_internal(self, index):
        """Internal handler for variable change."""
        if 0 <= index < len(self._vars):
            new_val = self._vars[index].get()
            # Fire ItemCheck event
            # Note: In WinForms ItemCheck fires BEFORE change. Here we fire AFTER.
            # Close enough for Python wrapper.
            # CurrentValue is tricky because we already changed.
            # We assume toggle behavior for CurrentValue estimation.
            current_val = 0 if new_val != 0 else 1 # Guess
            
            # Map int to CheckState enum if possible, but passing int is fine
            self.ItemCheck({'Index': index, 'NewValue': new_val, 'CurrentValue': current_val})

    def GetItemChecked(self, index):
        """Gets whether the item at the specified index is checked."""
        if 0 <= index < len(self._vars):
            return self._vars[index].get() != 0
        return False

    def SetItemChecked(self, index, value):
        """Sets the checked state of an item."""
        if 0 <= index < len(self._vars):
            val = 1 if value else 0
            self._vars[index].set(val)

    def GetItemCheckState(self, index):
        """Gets the check state (0=Unchecked, 1=Checked, 2=Indeterminate)."""
        if 0 <= index < len(self._vars):
            return self._vars[index].get()
        return 0

    def SetItemCheckState(self, index, value):
        """Sets the check state."""
        if 0 <= index < len(self._vars):
            self._vars[index].set(value)

    @property
    def SelectedIndex(self):
        return self._selected_index

    @SelectedIndex.setter
    def SelectedIndex(self, value):
        if self.SelectionMode == SelectionMode.None_:
            return
        if self._selected_index != value:
            # Deselect old
            if 0 <= self._selected_index < len(self._widgets):
                _, _, lbl = self._widgets[self._selected_index]
                lbl.config(bg=self.BackColor, fg=self.ForeColor or 'black')
            
            self._selected_index = value
            
            # Select new
            if 0 <= self._selected_index < len(self._widgets):
                _, _, lbl = self._widgets[self._selected_index]
                lbl.config(bg='#0078D7', fg='white') # System highlight color approx
                
                # Ensure visible
                # self._canvas.yview_moveto(...) # Complex to calculate
            
            self.SelectedIndexChanged()
            self.SelectedValueChanged()

    @property
    def SelectedItem(self):
        if 0 <= self._selected_index < len(self.Items):
            return self.Items[self._selected_index]
        return None

    @SelectedItem.setter
    def SelectedItem(self, value):
        try:
            idx = self.Items.index(value)
            self.SelectedIndex = idx
        except ValueError:
            pass
            
    @property
    def UseTabStops(self):
        return self._use_tab_stops
        
    @UseTabStops.setter
    def UseTabStops(self, value):
        self._use_tab_stops = value
        
    @property
    def UseCustomTabOffsets(self):
        return self._use_custom_tab_offsets
        
    @UseCustomTabOffsets.setter
    def UseCustomTabOffsets(self, value):
        self._use_custom_tab_offsets = value
        
    @property
    def CustomTabOffsets(self):
        return self._custom_tab_offsets
        
    @property
    def SelectionMode(self):
        return self._selection_mode
        
    @SelectionMode.setter
    def SelectionMode(self, value):
        if value not in [SelectionMode.One, SelectionMode.None_]:
            raise ValueError("SelectionMode must be SelectionMode.One or SelectionMode.None_ for CheckedListBox")
        self._selection_mode = value
        if value == SelectionMode.None_:
            self.SelectedIndex = -1


class FlowLayoutPanel(Panel):
    """
    El control FlowLayoutPanel organiza su contenido en una dirección de flujo horizontal o vertical.
    Su contenido puede ajustarse desde una fila a la siguiente o desde una columna a la siguiente.
    Como alternativa, su contenido se puede recortar en lugar de encapsularse.

    Puede especificar la dirección de flujo estableciendo el valor de la propiedad FlowDirection.
    El FlowLayoutPanel control invierte correctamente su dirección de flujo en diseños de derecha a izquierda (RTL).
    También puede especificar si el contenido del FlowLayoutPanel control se ajusta o recorta estableciendo el valor de la WrapContents propiedad.

    Cualquier control Windows Forms, incluidas otras instancias de FlowLayoutPanel, puede ser un elemento secundario del FlowLayoutPanel control.
    Con esta funcionalidad, puede construir diseños sofisticados que se adapten a las dimensiones del formulario en tiempo de ejecución.

    Los comportamientos de acoplamiento y delimitación de los controles secundarios difieren de los comportamientos de otros controles contenedor.
    El acoplamiento y la delimitación están relacionados con el control mayor en la dirección del flujo.
    """
    
    def __init__(self, master_form, props=None):
        """Inicializa un FlowLayoutPanel.
        
        Args:
            master_form: El formulario o contenedor padre
            props: Diccionario opcional con propiedades iniciales
        """
        # Valores por defecto específicos de FlowLayoutPanel
        defaults = {
            'Left': 10,
            'Top': 10,
            'Width': 400,
            'Height': 300,
            'Name': '',
            'Text': '',
            'FlowDirection': FlowDirection.LeftToRight,  # 'LeftToRight', 'RightToLeft', 'TopDown', 'BottomUp'
            'WrapContents': True,
            'Padding': (0, 0, 0, 0),  # left, top, right, bottom
            'AutoScroll': False,
            'BorderStyle': BorderStyle.FixedSingle,
            'BackColor': 'SystemButtonFace',
            'Enabled': True,
            'Visible': True
        }
        
        if props:
            defaults.update(props)
        
        # Inicializar como Panel
        super().__init__(master_form, defaults)
        
        # Propiedades específicas de FlowLayoutPanel
        self.FlowDirection = defaults['FlowDirection']
        self.WrapContents = defaults['WrapContents']
        
        # Override AddControl para aplicar el layout automático
        self._original_add_control = super().AddControl

        # Override Resize event to update layout
        self.Resize = self._on_resize_internal
        
    def _on_resize_internal(self):
        """Internal handler for resize event."""
        self._apply_flow_layout()

    def AddControl(self, control):
        """Añade un control al FlowLayoutPanel y aplica el layout automático.
        
        Args:
            control: Control a añadir
        """
        # Añadir usando el método del padre
        self._original_add_control(control)
        
        # Aplicar layout automático
        self._apply_flow_layout()
    
    def RemoveControl(self, control):
        """Quita un control del FlowLayoutPanel y reorganiza el layout.
        
        Args:
            control: Control a quitar
        """
        super().RemoveControl(control)
        self._apply_flow_layout()
    
    def _apply_flow_layout(self):
        """Aplica el layout automático según FlowDirection y WrapContents."""
        if not self.Controls:
            return
        
        # Obtener padding
        padding = self.Padding
        if isinstance(padding, tuple) and len(padding) == 4:
            pad_left, pad_top, pad_right, pad_bottom = padding
        elif isinstance(padding, tuple) and len(padding) == 2:
            pad_left = pad_right = padding[0]
            pad_top = pad_bottom = padding[1]
        else:
            pad_left = pad_right = pad_top = pad_bottom = 0
        
        # Área disponible
        available_width = self.Width - pad_left - pad_right
        available_height = self.Height - pad_top - pad_bottom
        
        # Posición inicial
        current_x = pad_left
        current_y = pad_top
        if self.FlowDirection == 'RightToLeft':
             current_x = self.Width - pad_right
        elif self.FlowDirection == 'BottomUp':
             current_y = self.Height - pad_bottom
             
        max_row_height = 0
        max_col_width = 0
        
        for control in self.Controls:
            if not hasattr(control, 'Width') or not hasattr(control, 'Height'):
                continue
            
            if not hasattr(control, '_visible') or control._visible:
                control_width = control.Width
                control_height = control.Height
                
                # Get margins
                margin = getattr(control, 'Margin', (3, 3, 3, 3))
                if isinstance(margin, int): margin = (margin, margin, margin, margin)
                m_left, m_top, m_right, m_bottom = margin
                
                full_width = m_left + control_width + m_right
                full_height = m_top + control_height + m_bottom
                
                if self.FlowDirection == 'LeftToRight':
                    # Flujo horizontal (izquierda a derecha)
                    
                    # Check wrap
                    if self.WrapContents and current_x + full_width > available_width + pad_left and current_x > pad_left:
                         current_x = pad_left
                         current_y += max_row_height
                         max_row_height = 0

                    control.Left = current_x + m_left
                    control.Top = current_y + m_top
                    control._place_control(control_width, control_height)
                    
                    current_x += full_width
                    max_row_height = max(max_row_height, full_height)
                    
                    if getattr(control, '_flow_break', False):
                        current_x = pad_left
                        current_y += max_row_height
                        max_row_height = 0
                
                elif self.FlowDirection == 'RightToLeft':
                    # Flujo horizontal (derecha a izquierda)
                    if self.WrapContents and current_x - full_width < pad_left:
                        # Nueva fila
                        current_x = self.Width - pad_right
                        current_y += max_row_height
                        max_row_height = 0
                    
                    control.Left = current_x - m_right - control_width
                    control.Top = current_y + m_top
                    control._place_control(control_width, control_height)
                    
                    current_x -= full_width
                    max_row_height = max(max_row_height, full_height)

                    if getattr(control, '_flow_break', False):
                        current_x = self.Width - pad_right
                        current_y += max_row_height
                        max_row_height = 0
                
                elif self.FlowDirection == 'TopDown':
                    # Flujo vertical (arriba a abajo)
                    if self.WrapContents and current_y + full_height > available_height + pad_top:
                        # Nueva columna
                        current_y = pad_top
                        current_x += max_col_width
                        max_col_width = 0
                    
                    control.Left = current_x + m_left
                    control.Top = current_y + m_top
                    control._place_control(control_width, control_height)
                    
                    current_y += full_height
                    max_col_width = max(max_col_width, full_width)

                    if getattr(control, '_flow_break', False):
                        current_y = pad_top
                        current_x += max_col_width
                        max_col_width = 0
                
                elif self.FlowDirection == 'BottomUp':
                    # Flujo vertical (abajo a arriba)
                    if self.WrapContents and current_y - full_height < pad_top:
                        # Nueva columna
                        current_y = self.Height - pad_bottom
                        current_x += max_col_width
                        max_col_width = 0
                    
                    control.Left = current_x + m_left
                    control.Top = current_y - m_bottom - control_height
                    control._place_control(control_width, control_height)
                    
                    current_y -= full_height
                    max_col_width = max(max_col_width, full_width)

                    if getattr(control, '_flow_break', False):
                        current_y = self.Height - pad_bottom
                        current_x += max_col_width
                        max_col_width = 0

        # Update scroll region if AutoScroll is enabled
        if self.AutoScroll and hasattr(self, '_update_scroll_region'):
            self._update_scroll_region()
    
    def set_FlowDirection(self, direction):
        """Establece la dirección del flujo y reorganiza los controles.
        
        Args:
            direction: 'LeftToRight', 'RightToLeft', 'TopDown', o 'BottomUp'
        """
        self.FlowDirection = direction
        self._apply_flow_layout()
    
    def set_WrapContents(self, wrap):
        """Establece si los controles deben ajustarse a nuevas líneas/columnas.
        
        Args:
            wrap: True para ajustar, False para recortar
        """
        self.WrapContents = wrap
        self._apply_flow_layout()

    def SetFlowBreak(self, control, value):
        """Sets the value of the flow-break setting for the control."""
        control._flow_break = value
        self._apply_flow_layout()

    def GetFlowBreak(self, control):
        """Returns the value of the flow-break setting for the control."""
        return getattr(control, '_flow_break', False)


class TableLayoutPanel(Panel):
    """
    El control TableLayoutPanel organiza su contenido en una cuadrícula. Como el diseño se realiza en tiempo de diseño y en tiempo de ejecución, puede cambiar dinámicamente cuando cambie el entorno de la aplicación. Esto proporciona a los controles del panel la capacidad de ajustar el tamaño proporcionalmente para poder responder a cambios como el ajuste de tamaño del control primario o el cambio de longitud del texto debido a la localización.

    Cualquier control de Windows Forms puede ser un control secundario del control TableLayoutPanel, incluidas otras instancias de TableLayoutPanel. Esto le permite construir diseños sofisticados que se adapten a los cambios en tiempo de ejecución.

    El control TableLayoutPanel puede expandirse para acomodar nuevos controles cuando se agreguen, dependiendo del valor de las propiedades RowCount, ColumnCount y GrowStyle. Establecer las propiedades RowCount o ColumnCount en un valor de 0 especifica que el TableLayoutPanel se desenlazará en la dirección correspondiente.

    También puede controlar la dirección de expansión (horizontal o vertical) cuando el control TableLayoutPanel se llene de controles secundarios. De forma predeterminada, el control TableLayoutPanel se expande hacia abajo agregando filas.

    Si quiere que el comportamiento de las filas y columnas sea diferente del predeterminado, puede controlar las propiedades de las filas y columnas mediante las propiedades RowStyles y ColumnStyles. Puede establecer las propiedades de las filas o columnas individualmente.

    El control TableLayoutPanel agrega las siguientes propiedades a sus controles secundarios: Cell, Column, Row, ColumnSpan y RowSpan.

    Puede combinar las celdas del control TableLayoutPanel estableciendo las propiedades ColumnSpan o RowSpan de un control secundario.

    Nota:
    Para establecer las Cellpropiedades , Column, Row, ColumnSpany RowSpan en tiempo de ejecución, use los SetCellPositionmétodos , SetColumnSetRow, , SetColumnSpany SetRowSpan .
    Para leer las Cellpropiedades , Column, Row, ColumnSpany RowSpan en tiempo de ejecución, use los GetCellPositionmétodos , GetColumnGetRow, , GetColumnSpany GetRowSpan .

    El comportamiento de anclaje de los controles secundarios de TableLayoutPanel difiere del de otros controles de contenedor. Si el valor de la propiedad del Anchor control secundario se establece Left en o Right, el control se colocará en el borde izquierdo o derecho de la celda, a una distancia que sea la suma de la propiedad del Margin control y la propiedad del Padding panel.
    """
    
    def __init__(self, master_form, props=None):
        """Inicializa un TableLayoutPanel.
        
        Args:
            master_form: El formulario o contenedor padre
            props: Diccionario opcional con propiedades iniciales
        """
        # Valores por defecto específicos de TableLayoutPanel
        defaults = {
            'Left': 10,
            'Top': 10,
            'Width': 600,
            'Height': 400,
            'Name': '',
            'Text': '',
            'RowCount': 2,
            'ColumnCount': 2,
            'RowStyles': None,  # Lista de tuplas (SizeType, Value)
            'ColumnStyles': None,  # Lista de tuplas (SizeType, Value)
            'CellBorderStyle': TableLayoutPanelCellBorderStyle.Single,
            'Padding': (0, 0, 0, 0),
            'BorderStyle': BorderStyle.FixedSingle,
            'BackColor': 'SystemButtonFace',
            'GrowStyle': TableLayoutPanelGrowStyle.AddRows,
            'Enabled': True,
            'Visible': True
        }
        
        if props:
            defaults.update(props)
        
        # Inicializar como Panel
        super().__init__(master_form, defaults)
        
        # Propiedades específicas de TableLayoutPanel
        self.RowCount = defaults['RowCount']
        self.ColumnCount = defaults['ColumnCount']
        self.GrowStyle = defaults['GrowStyle']
        self.CellBorderStyle = defaults['CellBorderStyle']
        
        # Estilos por defecto (porcentajes iguales)
        if defaults['RowStyles']:
            self.RowStyles = defaults['RowStyles']
        else:
            percent = 100.0 / max(1, self.RowCount)
            self.RowStyles = [(SizeType.Percent, percent) for _ in range(self.RowCount)]
        
        if defaults['ColumnStyles']:
            self.ColumnStyles = defaults['ColumnStyles']
        else:
            percent = 100.0 / max(1, self.ColumnCount)
            self.ColumnStyles = [(SizeType.Percent, percent) for _ in range(self.ColumnCount)]
        
        # Matriz de celdas (row, col) -> control
        self._cell_controls = {}
        
        # Override AddControl para posicionar en celdas
        self._original_add_control = super().AddControl
        self._next_cell = (0, 0)  # Próxima celda disponible

        # Override Resize event to update layout
        self.Resize = self._on_resize_internal
        
    def _on_resize_internal(self):
        """Internal handler for resize event."""
        self._apply_table_layout()
    
    def AddControl(self, control, column=None, row=None):
        """Añade un control al TableLayoutPanel en la celda especificada.
        
        Args:
            control: Control a añadir
            column: Columna donde colocar el control (None para siguiente disponible)
            row: Fila donde colocar el control (None para siguiente disponible)
        """
        # Disable standard ControlBase layout logic for this child
        # We want TableLayoutPanel to fully control the positioning
        control._on_container_resize = lambda e=None: None
        control._initialize_anchor_dock = lambda: None
        # Redirect _apply_dock to our layout engine
        control._apply_dock = self._apply_table_layout
        
        # Determinar celda
        if column is None or row is None:
            row, column = self._next_cell
            self._advance_next_cell()
        
        # Validar celda
        if row >= self.RowCount or column >= self.ColumnCount:
            if self.GrowStyle == 'AddRows':
                self.RowCount = row + 1
                percent = 100.0 / self.RowCount
                self.RowStyles = [('Percent', percent) for _ in range(self.RowCount)]
            elif self.GrowStyle == 'AddColumns':
                self.ColumnCount = column + 1
                percent = 100.0 / self.ColumnCount
                self.ColumnStyles = [('Percent', percent) for _ in range(self.ColumnCount)]
            else:  # FixedSize
                # If fixed size, we might need to expand anyway if user explicitly asks for it?
                # For now, raise error or just expand if it's out of bounds
                pass
        
        # Remove from any existing cell (to avoid duplicates if added multiple times)
        for cell, ctrl in list(self._cell_controls.items()):
            if ctrl == control:
                del self._cell_controls[cell]
                break

        # Añadir usando el método del padre
        self._original_add_control(control)
        
        # Guardar en la matriz de celdas
        self._cell_controls[(row, column)] = control
        
        # Aplicar layout automático
        self._apply_table_layout()
    
    def RemoveControl(self, control):
        """Quita un control del TableLayoutPanel y reorganiza el layout.
        
        Args:
            control: Control a quitar
        """
        # Eliminar de la matriz de celdas
        for cell, ctrl in list(self._cell_controls.items()):
            if ctrl == control:
                del self._cell_controls[cell]
                break
        
        super().RemoveControl(control)
        self._apply_table_layout()
    
    def SetCellPosition(self, control, column, row):
        """Establece la posición de un control en una celda específica.
        
        Args:
            control: Control a posicionar
            column: Columna destino
            row: Fila destino
        """
        # Eliminar de celda anterior
        for cell, ctrl in list(self._cell_controls.items()):
            if ctrl == control:
                del self._cell_controls[cell]
                break
        
        # Añadir a nueva celda
        self._cell_controls[(row, column)] = control
        self._apply_table_layout()
    
    def GetCellPosition(self, control):
        """Obtiene la posición de celda de un control.
        
        Args:
            control: Control a buscar
            
        Returns:
            Tupla (row, column) o None si no se encuentra
        """
        for cell, ctrl in self._cell_controls.items():
            if ctrl == control:
                return cell
        return None

    def SetColumn(self, control, column):
        """Sets the column position of the specified child control."""
        pos = self.GetCellPosition(control)
        if pos:
            self.SetCellPosition(control, column, pos[0])
        else:
            # If not in grid yet, assume row 0 or find next?
            # For now, assume row 0 if not found
            self.SetCellPosition(control, column, 0)

    def GetColumn(self, control):
        """Returns the column position of the specified child control."""
        pos = self.GetCellPosition(control)
        return pos[1] if pos else -1

    def SetRow(self, control, row):
        """Sets the row position of the specified child control."""
        pos = self.GetCellPosition(control)
        if pos:
            self.SetCellPosition(control, pos[1], row)
        else:
            self.SetCellPosition(control, 0, row)

    def GetRow(self, control):
        """Returns the row position of the specified child control."""
        pos = self.GetCellPosition(control)
        return pos[0] if pos else -1

    def SetRowSpan(self, control, value):
        """Sets the number of rows that the control spans."""
        control._row_span = value
        self._apply_table_layout()

    def GetRowSpan(self, control):
        return getattr(control, '_row_span', 1)

    def SetColumnSpan(self, control, value):
        """Sets the number of columns that the control spans."""
        control._column_span = value
        self._apply_table_layout()

    def GetColumnSpan(self, control):
        return getattr(control, '_column_span', 1)
    
    def _advance_next_cell(self):
        """Avanza la próxima celda disponible."""
        row, col = self._next_cell
        col += 1
        if col >= self.ColumnCount:
            col = 0
            row += 1
        self._next_cell = (row, col)
    
    def _apply_table_layout(self):
        """Aplica el layout automático según las filas y columnas definidas."""
        if not self._cell_controls:
            return
        
        # Obtener padding
        padding = self.Padding
        if isinstance(padding, tuple) and len(padding) == 4:
            pad_left, pad_top, pad_right, pad_bottom = padding
        elif isinstance(padding, tuple) and len(padding) == 2:
            pad_left = pad_right = padding[0]
            pad_top = pad_bottom = padding[1]
        else:
            pad_left = pad_right = pad_top = pad_bottom = 0
        
        # Área disponible
        available_width = self.Width - pad_left - pad_right
        available_height = self.Height - pad_top - pad_bottom
        
        # Calcular tamaños de columnas
        column_widths = self._calculate_sizes(self.ColumnStyles, available_width, 'width')
        
        # Calcular tamaños de filas
        row_heights = self._calculate_sizes(self.RowStyles, available_height, 'height')
        
        # Calcular posiciones de inicio de cada columna y fila
        column_positions = [pad_left]
        for width in column_widths[:-1]:
            column_positions.append(column_positions[-1] + width)
        
        row_positions = [pad_top]
        for height in row_heights[:-1]:
            row_positions.append(row_positions[-1] + height)
        
        # Posicionar controles en sus celdas
        for (row, col), control in self._cell_controls.items():
            if row >= len(row_heights) or col >= len(column_widths):
                continue
            
            # Skip if control is not visible
            if not getattr(control, '_visible', True):
                continue

            row_span = getattr(control, '_row_span', 1)
            col_span = getattr(control, '_column_span', 1)
            
            cell_x = column_positions[col]
            cell_y = row_positions[row]
            
            # Calculate total width/height including spans
            cell_width = 0
            for i in range(col_span):
                if col + i < len(column_widths):
                    cell_width += column_widths[col + i]
            
            cell_height = 0
            for i in range(row_span):
                if row + i < len(row_heights):
                    cell_height += row_heights[row + i]
            
            # Aplicar márgenes de celda usando control.Margin
            margin = getattr(control, 'Margin', (3, 3, 3, 3))
            if isinstance(margin, int): margin = (margin, margin, margin, margin)
            m_left, m_top, m_right, m_bottom = margin
            
            # Determine final position and size based on Dock and Anchor
            final_x = cell_x + m_left
            final_y = cell_y + m_top
            final_w = cell_width - (m_left + m_right)
            final_h = cell_height - (m_top + m_bottom)
            
            dock = getattr(control, 'Dock', 'None')
            anchor = getattr(control, 'Anchor', ['Top', 'Left'])
            
            if dock == 'Fill':
                # Fill the cell (minus margins)
                pass # final_x, final_y, final_w, final_h are already correct for Fill
            elif dock == 'None':
                # Handle Anchor
                # Default size is control.Width/Height unless anchored to stretch
                
                ctrl_w = getattr(control, 'Width', 0)
                ctrl_h = getattr(control, 'Height', 0)
                
                # Horizontal Anchor
                if 'Left' in anchor and 'Right' in anchor:
                    # Stretch horizontally
                    pass # final_w is already stretched
                elif 'Left' in anchor:
                    # Align Left
                    final_w = ctrl_w
                elif 'Right' in anchor:
                    # Align Right
                    final_x = cell_x + cell_width - m_right - ctrl_w
                    final_w = ctrl_w
                else:
                    # Center Horizontally (None or Top/Bottom only)
                    final_x = cell_x + (cell_width - ctrl_w) // 2
                    final_w = ctrl_w
                
                # Vertical Anchor
                if 'Top' in anchor and 'Bottom' in anchor:
                    # Stretch vertically
                    pass # final_h is already stretched
                elif 'Top' in anchor:
                    # Align Top
                    final_h = ctrl_h
                elif 'Bottom' in anchor:
                    # Align Bottom
                    final_y = cell_y + cell_height - m_bottom - ctrl_h
                    final_h = ctrl_h
                else:
                    # Center Vertically
                    final_y = cell_y + (cell_height - ctrl_h) // 2
                    final_h = ctrl_h

            # Update control properties
            control.Left = int(final_x)
            control.Top = int(final_y)
            control.Width = int(max(0, final_w))
            control.Height = int(max(0, final_h))
            
            # Reposicionar el control
            if hasattr(control, '_place_control'):
                control._place_control(control.Width, control.Height)
    
    def _calculate_sizes(self, styles, available_space, dimension):
        """Calcula los tamaños según los estilos definidos.
        
        Args:
            styles: Lista de tuplas (SizeType, Value)
            available_space: Espacio total disponible
            dimension: 'width' o 'height'
            
        Returns:
            Lista de tamaños calculados
        """
        count = len(styles)
        sizes = [0] * count
        remaining_space = available_space
        remaining_percent = 100.0
        autosize_indices = []
        
        # Primera pasada: tamaños absolutos y porcentajes
        for i, (size_type, value) in enumerate(styles):
            if size_type == 'Absolute':
                sizes[i] = value
                remaining_space -= value
            elif size_type == 'Percent':
                # Calculamos después
                pass
            elif size_type == 'AutoSize':
                autosize_indices.append(i)
        
        # Segunda pasada: AutoSize (buscar contenido más grande)
        for i in autosize_indices:
            max_size = 0
            for (row, col), control in self._cell_controls.items():
                if (dimension == 'width' and col == i) or (dimension == 'height' and row == i):
                    if hasattr(control, 'Width' if dimension == 'width' else 'Height'):
                        # Use preferred size if available, else current size
                        # For AutoSize, we ideally want the "natural" size of the control
                        # But here we use Width/Height as a proxy
                        size = control.Width if dimension == 'width' else control.Height
                        
                        # Add margins
                        margin = getattr(control, 'Margin', (3, 3, 3, 3))
                        if isinstance(margin, int): margin = (margin, margin, margin, margin)
                        m_left, m_top, m_right, m_bottom = margin
                        
                        if dimension == 'width':
                            size += m_left + m_right
                        else:
                            size += m_top + m_bottom
                            
                        max_size = max(max_size, size)
            
            sizes[i] = max_size
            remaining_space -= sizes[i]
        
        # Tercera pasada: porcentajes del espacio restante
        # Normalize percentages if they exceed 100? Or just use as weights?
        # .NET treats them as weights if total > 100, or absolute % if < 100.
        # Simplified: treat as weights of remaining space
        
        total_percent = sum(val for type, val in styles if type == 'Percent')
        
        if total_percent > 0:
            for i, (size_type, value) in enumerate(styles):
                if size_type == 'Percent':
                    # Distribute remaining space proportionally
                    sizes[i] = (value / total_percent) * max(0, remaining_space)
        
        return sizes
    
    def set_RowCount(self, count):
        """Establece el número de filas y reorganiza el layout.
        
        Args:
            count: Número de filas
        """
        self.RowCount = count
        percent = 100.0 / max(1, count)
        self.RowStyles = [('Percent', percent) for _ in range(count)]
        self._apply_table_layout()
    
    def set_ColumnCount(self, count):
        """Establece el número de columnas y reorganiza el layout.
        
        Args:
            count: Número de columnas
        """
        self.ColumnCount = count
        percent = 100.0 / max(1, count)
        self.ColumnStyles = [('Percent', percent) for _ in range(count)]
        self._apply_table_layout()
    
    def set_RowStyles(self, styles):
        """Establece los estilos de las filas y reorganiza el layout.
        
        Args:
            styles: Lista de tuplas (SizeType, Value)
        """
        self.RowStyles = styles
        self._apply_table_layout()
    

class SplitterPanel(Panel):
    """
    Represents a panel in a SplitContainer.
    
    SplitterPanel is a member of its associated SplitContainer rather than being a member 
    of the underlying form. At design time, SplitterPanel is accessible through the 
    Panel1 or Panel2 properties of SplitContainer.
    """
    def __init__(self, owner, props=None):
        """Initializes a SplitterPanel."""
        # Remove irrelevant properties from props if present
        if props:
            # These properties are not relevant for SplitterPanel as it is managed by SplitContainer
            for prop in ['Dock', 'Anchor', 'Location', 'Size', 'TabIndex', 'TabStop']:
                if prop in props:
                    del props[prop]
            
        super().__init__(owner, props)
        
        # Explicitly set irrelevant properties to defaults/None to avoid side effects
        self._dock = 'None'
        self._anchor = 'None'

    def _place_control(self, width=None, height=None):
        # SplitterPanel is managed by the SplitContainer (PanedWindow), 
        # so we override placement to do nothing.
        pass
        
    @property
    def Width(self):
        """Gets the width of the SplitterPanel."""
        if self._tk_widget:
            return self._tk_widget.winfo_width()
        return self._width

    @Width.setter
    def Width(self, value):
        """Sets the width of the SplitterPanel."""
        # Width is controlled by SplitContainer, but we store the value
        self._width = value

    @property
    def Height(self):
        """Gets the height of the SplitterPanel."""
        if self._tk_widget:
            return self._tk_widget.winfo_height()
        return self._height

    @Height.setter
    def Height(self, value):
        """Sets the height of the SplitterPanel."""
        # Height is controlled by SplitContainer, but we store the value
        self._height = value


class SplitContainer(ControlBase):
    """
    Represents a container composed of two panels separated by a movable splitter.
    
    Use the SplitContainer control to divide the display area of a container (e.g., Form)
    and allow the user to resize the controls added to the SplitContainer panels.
    
    Properties:
    - Orientation: Vertical (default, panels left/right) or Horizontal (panels top/bottom).
    - SplitterDistance: Location of the splitter in pixels.
    - FixedPanel: Determines which panel remains fixed size during resizing (None, Panel1, Panel2).
    - IsSplitterFixed: If True, the splitter cannot be moved by the user.
    - Panel1, Panel2: The two panels managed by the container.
    """
    def __init__(self, master_form, props=None):
        defaults = {
            'Orientation': Orientation.Vertical,
            'SplitterDistance': 100,
            'SplitterWidth': 4,
            'SplitterIncrement': 1,
            'FixedPanel': FixedPanel.None_,
            'IsSplitterFixed': False,
            'Panel1Collapsed': False,
            'Panel2Collapsed': False,
            'Panel1MinSize': 25,
            'Panel2MinSize': 25,
            'BorderStyle': BorderStyle.None_,
            'Left': 0,
            'Top': 0,
            'Width': 300,
            'Height': 300,
            'Name': '',
            'Dock': None,
            'Text': '' # Irrelevant
        }
        
        if props:
            defaults.update(props)
            
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Propagate _root
        if hasattr(master_form, '_root'):
            self._root = master_form._root
        else:
            self._root = None
        
        self._parent_container = parent_container
        self.Name = defaults['Name']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self._orientation = defaults['Orientation']
        self._splitter_distance = defaults['SplitterDistance']
        self._splitter_width = defaults['SplitterWidth']
        self._splitter_increment = defaults['SplitterIncrement']
        self._fixed_panel = defaults['FixedPanel']
        self._is_splitter_fixed = defaults['IsSplitterFixed']
        self._panel1_collapsed = defaults['Panel1Collapsed']
        self._panel2_collapsed = defaults['Panel2Collapsed']
        self._panel1_min_size = defaults['Panel1MinSize']
        self._panel2_min_size = defaults['Panel2MinSize']
        self._border_style = defaults['BorderStyle']
        
        # Events
        self.SplitterMoved = lambda sender, e: None
        self.SplitterMoving = lambda sender, e: None
        
        # Create PanedWindow
        # WinForms Vertical = Panels Left/Right = Tkinter HORIZONTAL
        orient = tk.HORIZONTAL if self._orientation == Orientation.Vertical else tk.VERTICAL
        
        self._tk_widget = tk.PanedWindow(
            self.master,
            orient=orient,
            sashwidth=self._splitter_width,
            bg='lightgray',
            bd=0,
            sashrelief='raised'
        )
        
        # Apply BorderStyle
        self._apply_border_style()
        
        # Create Panels
        self.Panel1 = SplitterPanel(self, {'Name': 'Panel1'})
        self.Panel2 = SplitterPanel(self, {'Name': 'Panel2'})
        
        # Add panels to Controls collection
        self.Controls = [self.Panel1, self.Panel2]
        
        # Add panels to PanedWindow
        self._add_panels()
        
        # Bind events
        self._tk_widget.bind('<ButtonRelease-1>', self._on_sash_release)
        self._tk_widget.bind('<B1-Motion>', self._on_sash_move)
        
        # Initial placement
        if defaults['Dock']:
            self.Dock = defaults['Dock']
        else:
            self._place_control(self.Width, self.Height)
            
        self._auto_register_with_parent()
        
        # Defer setting splitter distance until mapped
        self._tk_widget.bind('<Map>', self._on_map)

    def _apply_border_style(self):
        if self._border_style == BorderStyle.FixedSingle:
            self._tk_widget.config(bd=1, relief='solid')
        elif self._border_style == BorderStyle.Fixed3D:
            self._tk_widget.config(bd=2, relief='sunken')
        else: # None
            self._tk_widget.config(bd=0, relief='flat')

    def _add_panels(self):
        # Configure stretch based on FixedPanel
        p1_stretch = 'always'
        p2_stretch = 'always'
        
        if self._fixed_panel == FixedPanel.Panel1:
            p1_stretch = 'never'
        elif self._fixed_panel == FixedPanel.Panel2:
            p2_stretch = 'never'
            
        if not self._panel1_collapsed:
            self._tk_widget.add(self.Panel1._tk_widget, minsize=self._panel1_min_size, stretch=p1_stretch)
        if not self._panel2_collapsed:
            self._tk_widget.add(self.Panel2._tk_widget, minsize=self._panel2_min_size, stretch=p2_stretch)

    def _on_map(self, event):
        if self._splitter_distance > 0:
            self.SplitterDistance = self._splitter_distance
        self._tk_widget.unbind('<Map>')

    def _on_sash_move(self, event):
        if self._is_splitter_fixed:
            return "break"
        self.SplitterMoving(self, event)

    def _on_sash_release(self, event):
        self.SplitterMoved(self, event)
        # Update internal distance
        try:
            if self.Orientation == Orientation.Vertical:
                self._splitter_distance = self._tk_widget.sash_coord(0)[0]
            else:
                self._splitter_distance = self._tk_widget.sash_coord(0)[1]
        except:
            pass

    @property
    def Orientation(self): return self._orientation
    @Orientation.setter
    def Orientation(self, value):
        self._orientation = value
        orient = tk.HORIZONTAL if value == Orientation.Vertical else tk.VERTICAL
        self._tk_widget.config(orient=orient)

    @property
    def SplitterDistance(self): return self._splitter_distance
    @SplitterDistance.setter
    def SplitterDistance(self, value):
        self._splitter_distance = value
        try:
            if self.Orientation == Orientation.Vertical:
                self._tk_widget.sash_place(0, value, 0)
            else:
                self._tk_widget.sash_place(0, 0, value)
        except:
            pass

    @property
    def SplitterWidth(self): return self._splitter_width
    @SplitterWidth.setter
    def SplitterWidth(self, value):
        self._splitter_width = value
        self._tk_widget.config(sashwidth=value)

    @property
    def BorderStyle(self): return self._border_style
    @BorderStyle.setter
    def BorderStyle(self, value):
        self._border_style = value
        self._apply_border_style()

    @property
    def SplitterIncrement(self): return self._splitter_increment
    @SplitterIncrement.setter
    def SplitterIncrement(self, value):
        self._splitter_increment = value

    # Irrelevant properties overrides
    @property
    def Text(self): return ""
    @Text.setter
    def Text(self, value): pass
    
    @property
    def Padding(self): return (0,0,0,0)
    @Padding.setter
    def Padding(self, value): pass
    
    @property
    def AutoScroll(self): return False
    @AutoScroll.setter
    def AutoScroll(self, value): pass

    @property
    def FixedPanel(self): return self._fixed_panel
    @FixedPanel.setter
    def FixedPanel(self, value):
        self._fixed_panel = value
        p1_stretch = 'always'
        p2_stretch = 'always'
        
        if self._fixed_panel == FixedPanel.Panel1:
            p1_stretch = 'never'
        elif self._fixed_panel == FixedPanel.Panel2:
            p2_stretch = 'never'
            
        try:
            if not self._panel1_collapsed:
                self._tk_widget.paneconfigure(self.Panel1._tk_widget, stretch=p1_stretch)
            if not self._panel2_collapsed:
                self._tk_widget.paneconfigure(self.Panel2._tk_widget, stretch=p2_stretch)
        except:
            pass 

    @property
    def IsSplitterFixed(self): return self._is_splitter_fixed
    @IsSplitterFixed.setter
    def IsSplitterFixed(self, value):
        self._is_splitter_fixed = value

    @property
    def Panel1Collapsed(self): return self._panel1_collapsed
    @Panel1Collapsed.setter
    def Panel1Collapsed(self, value):
        self._panel1_collapsed = value
        if value:
            self._tk_widget.forget(self.Panel1._tk_widget)
        else:
            self._tk_widget.forget(self.Panel2._tk_widget)
            self._add_panels()

    @property
    def Panel2Collapsed(self): return self._panel2_collapsed
    @Panel2Collapsed.setter
    def Panel2Collapsed(self, value):
        self._panel2_collapsed = value
        if value:
            self._tk_widget.forget(self.Panel2._tk_widget)
        else:
            self._tk_widget.add(self.Panel2._tk_widget)


class StatusBar(ControlBase):
    """
    Windows Forms status bar control.
    """
    def __init__(self, master_form, props=None):
        defaults = {
            'Text': "Ready",
            'Left': 0,
            'Top': 570,
            'Width': 800,
            'Height': 25,
            'ShowPanels': False,
            'SizingGrip': True,
            'BorderStyle': "Fixed3D",
            'Name': "",
            'Dock': None,
            'Margin': (0, 0, 0, 0)
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Status", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Status")
        
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        self._parent_container = parent_container
        initial_dock = defaults.get('Dock', None)
        
        self.Name = defaults['Name']
        self._text = defaults['Text']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self._show_panels = defaults['ShowPanels']
        self.SizingGrip = defaults['SizingGrip']
        self.BorderStyle = defaults['BorderStyle']
        self.Margin = defaults['Margin']
        self.BackColor = 'SystemButtonFace'
        self.ForeColor = 'black'
        self.Font = ('Segoe UI', 9)
        self._background_image = defaults.get('BackgroundImage', None)
        self._background_image_layout = defaults.get('BackgroundImageLayout', 'Tile')
        
        # Panel collection
        self.Panels = StatusBarPanelCollection(self)
        
        self._master_form = master_form
        
        # Events
        self.PanelClick = lambda sender, panel: None
        self.DrawItem = lambda sender, e: None
        
        relief_map = {
            'None': 'flat',
            'Fixed3D': 'ridge',
            'FixedSingle': 'solid'
        }
        
        self._tk_widget = tk.Frame(
            self.master,
            relief=relief_map.get(self.BorderStyle, 'ridge'),
            borderwidth=1 if self.BorderStyle != 'None' else 0,
            bg=self.BackColor,
            height=self.Height
        )
        
        self._content_frame = tk.Frame(self._tk_widget, bg=self.BackColor)
        self._content_frame.pack(side='left', fill='both', expand=True)
        
        self._text_label = None
        
        if self.SizingGrip:
            self._grip_canvas = tk.Canvas(
                self._tk_widget,
                width=15,
                height=self.Height,
                bg=self.BackColor,
                highlightthickness=0
            )
            self._grip_canvas.pack(side='right', fill='y')
            self._draw_sizing_grip()
        
        self._update_display()
        
        if initial_dock and initial_dock != 'None':
            self.Dock = initial_dock
        else:
            if hasattr(self, '_visible') and self._visible:
                self._place_control(self.Width, self.Height)

        self._auto_register_with_parent()
    
    @property
    def ShowPanels(self): return self._show_panels
    @ShowPanels.setter
    def ShowPanels(self, value):
        self._show_panels = value
        self._update_display()

    @property
    def Text(self): return self._text
    @Text.setter
    def Text(self, value):
        self._text = value
        if self._text_label: self._text_label.config(text=value)

    @property
    def BackgroundImage(self): return self._background_image
    @BackgroundImage.setter
    def BackgroundImage(self, value):
        self._background_image = value

    @property
    def BackgroundImageLayout(self): return self._background_image_layout
    @BackgroundImageLayout.setter
    def BackgroundImageLayout(self, value):
        self._background_image_layout = value
    
    def AddPanel(self, panel):
        """Adds a panel to the panel collection (Legacy support)."""
        self.Panels.Add(panel)
    
    def RemovePanel(self, panel):
        """Removes a panel from the collection (Legacy support)."""
        self.Panels.Remove(panel)
    
    def _update_display(self):
        """Updates the display according to ShowPanels."""
        for widget in self._content_frame.winfo_children():
            widget.destroy()
        
        if self.ShowPanels and len(self.Panels) > 0:
            self._display_panels()
        else:
            self._text_label = tk.Label(
                self._content_frame,
                text=self._text,
                bg=self.BackColor,
                fg=self.ForeColor,
                font=self.Font,
                anchor='w',
                padx=5
            )
            self._text_label.pack(side='left', fill='both', expand=True)
    
    def _display_panels(self):
        """Displays the panels in the StatusBar."""
        for panel in self.Panels:
            widget = panel._create_widget(self._content_frame)
            
            pack_opts = {'side': 'left', 'fill': 'y', 'padx': 0}
            
            if panel.AutoSize == 'Spring':
                pack_opts['expand'] = True
                pack_opts['fill'] = 'both'
            elif panel.AutoSize == 'Contents':
                pass
            else:
                pass
                
            widget.pack(**pack_opts)

    def _draw_sizing_grip(self):
        """Draws the sizing grip dots."""
        w, h = 15, self.Height
        for i in range(3):
            for j in range(i + 1):
                x = w - (j * 4) - 3
                y = h - (i * 4) - 3
                self._grip_canvas.create_rectangle(x, y, x+1, y+1, fill='gray', outline='gray')
                self._grip_canvas.create_rectangle(x+1, y+1, x+2, y+2, fill='white', outline='white')


class StatusBarPanelCollection:
    """Collection of StatusBarPanel objects."""
    def __init__(self, owner):
        self._owner = owner
        self._items = []

    @property
    def Count(self):
        """Gets the number of items in the collection."""
        return len(self._items)

    @property
    def IsReadOnly(self):
        """Gets a value indicating whether this collection is read-only."""
        return False

    def Add(self, value):
        """Adds a panel to the collection."""
        if isinstance(value, str):
            panel = StatusBarPanel()
            panel.Text = value
            value = panel
        
        if not isinstance(value, StatusBarPanel):
            raise TypeError("Value must be a StatusBarPanel or string")
            
        self._items.append(value)
        value._parent_statusbar = self._owner
        if self._owner.ShowPanels:
            self._owner._update_display()
        return self._items.index(value)

    def AddRange(self, values):
        """Adds a range of panels."""
        for v in values:
            self.Add(v)

    def Clear(self):
        """Removes all panels."""
        self._items.clear()
        if self._owner.ShowPanels:
            self._owner._update_display()

    def Contains(self, item):
        """Determines whether the specified panel is located within the collection."""
        return item in self._items

    def ContainsKey(self, key):
        """Determines whether the collection contains a StatusBarPanel with the specified key."""
        return any(item.Name == key for item in self._items)

    def IndexOf(self, item):
        """Returns the index within the collection of the specified panel."""
        try:
            return self._items.index(item)
        except ValueError:
            return -1

    def IndexOfKey(self, key):
        """Returns the index of the first occurrence of a StatusBarPanel with the specified key."""
        for i, item in enumerate(self._items):
            if item.Name == key:
                return i
        return -1

    def Insert(self, index, value):
        """Inserts the specified StatusBarPanel into the collection at the specified index."""
        if not isinstance(value, StatusBarPanel):
            raise TypeError("Value must be a StatusBarPanel")
        
        self._items.insert(index, value)
        value._parent_statusbar = self._owner
        if self._owner.ShowPanels:
            self._owner._update_display()

    def Remove(self, value):
        """Removes a specific panel."""
        if value in self._items:
            self._items.remove(value)
            value._parent_statusbar = None
            if self._owner.ShowPanels:
                self._owner._update_display()

    def RemoveAt(self, index):
        """Removes the panel at the specified index."""
        if 0 <= index < len(self._items):
            panel = self._items.pop(index)
            panel._parent_statusbar = None
            if self._owner.ShowPanels:
                self._owner._update_display()

    def RemoveByKey(self, key):
        """Removes the StatusBarPanel with the specified key from the collection."""
        index = self.IndexOfKey(key)
        if index != -1:
            self.RemoveAt(index)

    def __getitem__(self, index):
        """Gets the StatusBarPanel at the specified index or with the specified key."""
        if isinstance(index, str):
            idx = self.IndexOfKey(index)
            if idx != -1:
                return self._items[idx]
            raise KeyError(f"Panel with key '{index}' not found")
        return self._items[index]
        
    def __setitem__(self, index, value):
        """Sets the StatusBarPanel at the specified index."""
        if not isinstance(value, StatusBarPanel):
            raise TypeError("Value must be a StatusBarPanel")
        
        # If index is string, find the numeric index
        if isinstance(index, str):
            idx = self.IndexOfKey(index)
            if idx != -1:
                index = idx
            else:
                # If key not found, we can't set it (unlike dict where we'd add it)
                # Standard List behavior for setitem is to replace existing
                raise KeyError(f"Panel with key '{index}' not found")

        self._items[index] = value
        value._parent_statusbar = self._owner
        if self._owner.ShowPanels:
            self._owner._update_display()

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)


class StatusBarPanel:
    """
    Represents an individual panel within a StatusBar.
    
    Usage - Option 1: panel = StatusBarPanel(); panel.Text = "Ready"; panel.Width = 150
    Usage - Option 2: panel = StatusBarPanel({'Text': 'Ready', 'Width': 150})
    """
    
    def __init__(self, props=None):
        self._text = ""
        self._width = 100
        self._auto_size = "None"  # 'None', 'Spring', 'Contents'
        self._icon = None
        self._tooltip_text = ""
        self._border_style = "Sunken"  # 'Raised', 'Sunken', 'None'
        self._style = "Text"  # 'Text', 'OwnerDraw'
        self._min_width = 10
        self._alignment = "Left"  # 'Left', 'Center', 'Right'
        self._tag = None
        self._name = ""
        
        # Internal references
        self._parent_statusbar = None
        self._frame = None
        self._label = None
        self._icon_label = None
        
        # Events
        self.Click = lambda sender=None, e=None: None
        self.DoubleClick = lambda sender=None, e=None: None
        self.Disposed = lambda sender=None, e=None: None
        
        if props:
            if isinstance(props, dict):
                self._apply_props(props)
            elif isinstance(props, str):
                self.Text = props

    def _apply_props(self, props):
        if 'Text' in props: self.Text = props['Text']
        if 'Width' in props: self.Width = props['Width']
        if 'AutoSize' in props: self.AutoSize = props['AutoSize']
        if 'Icon' in props: self.Icon = props['Icon']
        if 'ToolTipText' in props: self.ToolTipText = props['ToolTipText']
        if 'BorderStyle' in props: self.BorderStyle = props['BorderStyle']
        if 'Bevel' in props: self.BorderStyle = props['Bevel'] # Alias
        if 'Style' in props: self.Style = props['Style']
        if 'Alignment' in props: self.Alignment = props['Alignment']
        if 'MinWidth' in props: self.MinWidth = props['MinWidth']
        if 'Tag' in props: self.Tag = props['Tag']
        if 'Name' in props: self.Name = props['Name']

    @property
    def Parent(self):
        """Gets the control StatusBar that hosts the status bar panel."""
        return self._parent_statusbar

    @property
    def Text(self): return self._text
    @Text.setter
    def Text(self, value):
        self._text = value
        if self._label: self._label.config(text=value)
        if self._auto_size == 'Contents' and self._parent_statusbar:
            self._parent_statusbar._update_display()
    
    @property
    def Width(self): return self._width
    @Width.setter
    def Width(self, value):
        self._width = value
        if self._parent_statusbar: self._parent_statusbar._update_display()

    @property
    def AutoSize(self): return self._auto_size
    @AutoSize.setter
    def AutoSize(self, value):
        self._auto_size = value
        if self._parent_statusbar: self._parent_statusbar._update_display()

    @property
    def Icon(self): return self._icon
    @Icon.setter
    def Icon(self, value):
        self._icon = value
        if self._parent_statusbar: self._parent_statusbar._update_display()

    @property
    def ToolTipText(self): return self._tooltip_text
    @ToolTipText.setter
    def ToolTipText(self, value):
        self._tooltip_text = value
        # Tooltip update logic would go here if we kept a reference to the tooltip object

    @property
    def BorderStyle(self): return self._border_style
    @BorderStyle.setter
    def BorderStyle(self, value):
        self._border_style = value
        if self._parent_statusbar: self._parent_statusbar._update_display()

    @property
    def Style(self): return self._style
    @Style.setter
    def Style(self, value): self._style = value

    @property
    def Alignment(self): return self._alignment
    @Alignment.setter
    def Alignment(self, value):
        self._alignment = value
        if self._parent_statusbar: self._parent_statusbar._update_display()

    @property
    def MinWidth(self): return self._min_width
    @MinWidth.setter
    def MinWidth(self, value): self._min_width = value

    @property
    def Tag(self): return self._tag
    @Tag.setter
    def Tag(self, value): self._tag = value

    @property
    def Name(self): return self._name
    @Name.setter
    def Name(self, value): self._name = value

    def BeginInit(self):
        """Begins the initialization of a StatusBarPanel."""
        pass

    def EndInit(self):
        """Ends the initialization of a StatusBarPanel."""
        pass

    def Dispose(self):
        """Releases all resources used by the Component."""
        if self._frame:
            self._frame.destroy()
            self._frame = None
        self.Disposed(self, None)

    def ToString(self):
        """Retrieves a string that contains information about the panel."""
        return f"StatusBarPanel: {{Text={self.Text}}}"

    def _create_widget(self, parent_frame):
        """Creates the tkinter widget for this panel."""
        # Panel container frame
        relief_map = {
            'Raised': 'raised',
            'Sunken': 'sunken',
            'None': 'flat'
        }
        
        # Calculate width if fixed
        frame_kwargs = {
            'relief': relief_map.get(self.BorderStyle, 'sunken'),
            'borderwidth': 1 if self.BorderStyle != 'None' else 0,
            'bg': parent_frame.cget('bg')
        }
        
        if self.AutoSize == 'None':
            frame_kwargs['width'] = max(self.Width, self.MinWidth)
            
        self._frame = tk.Frame(parent_frame, **frame_kwargs)
        
        # Label for the icon (if it exists)
        if self.Icon:
            self._icon_label = tk.Label(self._frame, image=self.Icon, bg=self._frame.cget('bg'))
            self._icon_label.pack(side='left', padx=2)
        
        # Label for the text
        anchor_map = {
            'Left': 'w',
            'Center': 'center',
            'Right': 'e'
        }
        
        self._label = tk.Label(
            self._frame,
            text=self._text,
            anchor=anchor_map.get(self.Alignment, 'w'),
            bg=self._frame.cget('bg')
        )
        self._label.pack(side='left', fill='both', expand=True, padx=2)
        
        # Bind events
        self._frame.bind('<Button-1>', self._on_click)
        self._frame.bind('<Double-Button-1>', lambda e: self.DoubleClick())
        self._label.bind('<Button-1>', self._on_click)
        self._label.bind('<Double-Button-1>', lambda e: self.DoubleClick())
        
        # Tooltip
        if self.ToolTipText:
            self._create_tooltip(self._frame, self.ToolTipText)
            self._create_tooltip(self._label, self.ToolTipText)
        
        # If AutoSize is 'None', disable propagation to respect fixed width
        if self.AutoSize == 'None':
            self._frame.pack_propagate(False)
        
        return self._frame
    
    def _on_click(self, event=None):
        self.Click()
        if self._parent_statusbar and hasattr(self._parent_statusbar, 'PanelClick'):
            self._parent_statusbar.PanelClick(self._parent_statusbar, self)
    
    def _create_tooltip(self, widget, text):
        """Creates a simple tooltip for the widget."""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=text, background="lightyellow", 
                           relief="solid", borderwidth=1, padx=5, pady=2)
            label.pack()
            widget._tooltip = tooltip
        
        def hide_tooltip(event):
            if hasattr(widget, '_tooltip'):
                widget._tooltip.destroy()
                delattr(widget, '_tooltip')
        
        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)


class ImageList:
    """
    Represents an ImageList to manage images with VB.NET-like properties.

    Usage - Option 1: imgList = ImageList(); imgList.ImageSize = (32, 32)
    Usage - Option 2: imgList = ImageList({'ImageSize': (32, 32), 'Name': 'icons'})
    """
    
    class ImageCollection:
        """Represents the collection of images in an ImageList."""
        def __init__(self, owner):
            self._owner = owner
            
        def Add(self, image, key=None):
            """Add an image to the list. If key is None, use a numeric index."""
            return self._owner._add_image(image, key)
            
        def RemoveByKey(self, key):
            """Remove an image by key."""
            self._owner._remove_image(key)
            
        def RemoveAt(self, index):
            """Remove an image by index."""
            self._owner._remove_image(index)
            
        def Clear(self):
            """Clear all images."""
            self._owner._clear_images()
            
        def __getitem__(self, key):
            """Get an image by index or key."""
            return self._owner.GetImage(key)
            
        def __len__(self):
            """Return the number of images."""
            return self._owner.Count()
            
        def __iter__(self):
            """Iterate over images."""
            # This iterates over values (images) to be consistent with a collection of images
            # Note: The internal storage is a dict, so order is insertion order in modern Python
            return iter(self._owner._images.values())

    def __init__(self, props=None):
        defaults = {
            'Name': "",
            'ImageSize': (16, 16),
            'ColorDepth': 32,
            'TransparentColor': None,
            'ImageStream': None,
            'Tag': None
        }
        
        if props:
            defaults.update(props)
        
        self.Name = defaults['Name']  # Unique identifier
        self._images = {}  # Dictionary of images (key: index or name, value: PhotoImage)
        self._image_size = defaults['ImageSize']  # (width, height) in pixels
        self.ColorDepth = defaults['ColorDepth']  # Color depth (8, 16, 24, 32 bits)
        self.TransparentColor = defaults['TransparentColor']  # Transparent color
        self.ImageStream = defaults['ImageStream']  # For serialization (placeholder)
        self.Tag = defaults['Tag']  # Custom object
        self._next_index = 0  # For auto-assigning indices
        
        # Initialize the Images collection property
        self._images_collection = self.ImageCollection(self)
        
        # VB-style events
        self.CollectionChanged = lambda: None
        self.Disposed = lambda sender, e: None
        self.RecreateHandle = lambda sender, e: None
        
    @property
    def Images(self):
        """Gets the ImageList.ImageCollection for this image list."""
        return self._images_collection
        
    @property
    def ImageSize(self):
        """Gets or sets the size of the images in the image list."""
        return self._image_size
        
    @ImageSize.setter
    def ImageSize(self, value):
        if self._image_size != value:
            self._image_size = value
            # In .NET, changing ImageSize recreates the handle and clears images
            # We will simulate this behavior or just warn
            # For now, we just trigger the event
            self.RecreateHandle(self, None)
            
    @property
    def Handle(self):
        """Gets the handle of the image list object."""
        # Return the memory address as a fake handle
        return id(self)
        
    @property
    def HandleCreated(self):
        """Gets a value indicating whether the underlying Win32 handle has been created."""
        return True

    def _add_image(self, image, key=None):
        """Internal method to add image."""
        if key is None:
            key = self._next_index
            self._next_index += 1
        
        # TODO: Resize image to self.ImageSize if possible
        # Without PIL, resizing is limited. We assume the user provides correct size
        # or we use the image as is.
        
        self._images[key] = image
        self.CollectionChanged()
        return key

    def _remove_image(self, key):
        """Internal method to remove image."""
        if key in self._images:
            del self._images[key]
            self.CollectionChanged()
            
    def _clear_images(self):
        """Internal method to clear images."""
        self._images.clear()
        self._next_index = 0
        self.CollectionChanged()

    def Add(self, image, key=None):
        """Add an image to the list. If key is None, use a numeric index.
        DEPRECATED: Use Images.Add() instead.
        """
        return self._add_image(image, key)
    
    def GetImage(self, key):
        """Get an image by key (index or name)."""
        return self._images.get(key, None)
    
    def Remove(self, key):
        """Remove an image by key.
        DEPRECATED: Use Images.RemoveByKey() or Images.RemoveAt() instead.
        """
        self._remove_image(key)
    
    def Clear(self):
        """Clear all images.
        DEPRECATED: Use Images.Clear() instead.
        """
        self._clear_images()
    
    def Count(self):
        """Return the number of images."""
        return len(self._images)
        
    def Draw(self, graphics, x, y, index=None, width=None, height=None):
        """
        Draws the image indicated by the given index on the specified Graphics (Canvas).
        
        Args:
            graphics: The target object (usually a tk.Canvas or object with create_image)
            x: X coordinate
            y: Y coordinate
            index: The index or key of the image to draw.
            width: Optional width (ignored if no resizing support)
            height: Optional height (ignored if no resizing support)
        """
        if index is None:
            return
            
        image = self.GetImage(index)
        if image:
            if hasattr(graphics, 'create_image'):
                # It's a Canvas
                graphics.create_image(x, y, image=image, anchor='nw')
            elif hasattr(graphics, 'create_image_on_surface'):
                # Custom wrapper?
                pass
    
    def Dispose(self):
        """Dispose ImageList resources."""
        self.Disposed(self, None)
    
    def ToString(self):
        """Returns a string that represents the current ImageList."""
        return f"ImageList {{ Name = '{self.Name}', ImageSize = {self.ImageSize}, Count = {self.Count()} }}"


class ListViewItem:
    """
    Represents an item in a ListView.
    
    Usage - Option 1: item = ListViewItem(); item.Text = "Item1"
    Usage - Option 2: item = ListViewItem({'Text': 'Item1', 'SubItems': ['SubItem1', 'SubItem2']})
    """
    
    def __init__(self, props=None, **kwargs):
        # Support dictionary-based init for compatibility
        if isinstance(props, dict):
            kwargs.update(props)
        elif isinstance(props, str):
            kwargs['Text'] = props
            
        self._text = kwargs.get('Text', "")
        self._subitems = kwargs.get('SubItems', []) or []
        self._image_index = kwargs.get('ImageIndex', -1)
        self._image_key = kwargs.get('ImageKey', "")
        self._tag = kwargs.get('Tag', None)
        self._back_color = kwargs.get('BackColor', None)
        self._fore_color = kwargs.get('ForeColor', None)
        self._font = kwargs.get('Font', None)
        self._checked = kwargs.get('Checked', False)
        self._focused = kwargs.get('Focused', False)
        self._selected = kwargs.get('Selected', False)
        self._group = kwargs.get('Group', None)
        self._indent_count = kwargs.get('IndentCount', 0)
        self._state_image_index = kwargs.get('StateImageIndex', -1)
        self._tool_tip_text = kwargs.get('ToolTipText', "")
        self._use_item_style_for_subitems = kwargs.get('UseItemStyleForSubItems', True)
        self._name = kwargs.get('Name', "")
        
        # Internal references
        self._list_view = None
        self._index = -1
        self._id = None # Tkinter Item ID
        
    @property
    def Text(self):
        """Gets or sets the text of the item."""
        return self._text

    @Text.setter
    def Text(self, value):
        self._text = value
        # TODO: Update UI if attached to ListView

    @property
    def SubItems(self):
        """Gets a collection containing all subitems of the item."""
        return self._subitems

    @SubItems.setter
    def SubItems(self, value):
        self._subitems = value

    @property
    def ImageIndex(self):
        """Gets or sets the index of the image that is displayed for the item."""
        return self._image_index

    @ImageIndex.setter
    def ImageIndex(self, value):
        self._image_index = value

    @property
    def ImageKey(self):
        """Gets or sets the key for the image that is displayed for the item."""
        return self._image_key

    @ImageKey.setter
    def ImageKey(self, value):
        self._image_key = value

    @property
    def Tag(self):
        """Gets or sets an object that contains data to associate with the item."""
        return self._tag

    @Tag.setter
    def Tag(self, value):
        self._tag = value

    @property
    def BackColor(self):
        """Gets or sets the background color of the item's text."""
        return self._back_color

    @BackColor.setter
    def BackColor(self, value):
        self._back_color = value

    @property
    def ForeColor(self):
        """Gets or sets the foreground color of the item's text."""
        return self._fore_color

    @ForeColor.setter
    def ForeColor(self, value):
        self._fore_color = value

    @property
    def Font(self):
        """Gets or sets the font of the text displayed by the item."""
        return self._font

    @Font.setter
    def Font(self, value):
        self._font = value

    @property
    def Checked(self):
        """Gets or sets a value indicating whether the item is checked."""
        return self._checked

    @Checked.setter
    def Checked(self, value):
        self._checked = value

    @property
    def Focused(self):
        """Gets or sets a value indicating whether the item has focus within the ListView control."""
        return self._focused

    @Focused.setter
    def Focused(self, value):
        self._focused = value

    @property
    def Selected(self):
        """Gets or sets a value indicating whether the item is selected."""
        return self._selected

    @Selected.setter
    def Selected(self, value):
        self._selected = value
        if self._list_view:
            # TODO: Update selection in ListView
            pass

    @property
    def Group(self):
        """Gets or sets the group to which the item is assigned."""
        return self._group

    @Group.setter
    def Group(self, value):
        self._group = value

    @property
    def IndentCount(self):
        """Gets or sets the number of small image widths by which to indent the ListViewItem."""
        return self._indent_count

    @IndentCount.setter
    def IndentCount(self, value):
        self._indent_count = value

    @property
    def Index(self):
        """Gets the zero-based index of the item within the ListView control."""
        if self._list_view:
            try:
                return self._list_view.Items.index(self)
            except ValueError:
                return -1
        return -1

    @property
    def ListView(self):
        """Gets the ListView control that contains the item."""
        return self._list_view

    @property
    def Name(self):
        """Gets or sets the name associated with this ListViewItem."""
        return self._name

    @Name.setter
    def Name(self, value):
        self._name = value

    @property
    def Position(self):
        """Gets or sets the position of the upper-left corner of the ListViewItem."""
        # Placeholder: In standard ListView (Details), position is automatic.
        # In Icon view, it might be relevant.
        return Point(0, 0)

    @Position.setter
    def Position(self, value):
        pass

    @property
    def StateImageIndex(self):
        """Gets or sets the index of the state image."""
        return self._state_image_index

    @StateImageIndex.setter
    def StateImageIndex(self, value):
        self._state_image_index = value

    @property
    def ToolTipText(self):
        """Gets or sets the text shown when the mouse pointer rests on the ListViewItem."""
        return self._tool_tip_text

    @ToolTipText.setter
    def ToolTipText(self, value):
        self._tool_tip_text = value

    @property
    def UseItemStyleForSubItems(self):
        """Gets or sets a value indicating whether the item style is used for subitems."""
        return self._use_item_style_for_subitems

    @UseItemStyleForSubItems.setter
    def UseItemStyleForSubItems(self, value):
        self._use_item_style_for_subitems = value

    @property
    def ImageList(self):
        """Gets the ImageList that contains the image displayed with the item."""
        if self._list_view:
            return self._list_view.LargeImageList if self._list_view.View == View.LargeIcon else self._list_view.SmallImageList
        return None

    @property
    def Bounds(self):
        """Gets the bounding rectangle of the item, including subitems."""
        # Placeholder
        return Rectangle(0, 0, 0, 0)

    def BeginEdit(self):
        """Places the item text into edit mode."""
        pass

    def Clone(self):
        """Creates an identical copy of the item."""
        new_item = ListViewItem()
        new_item.Text = self.Text
        new_item.SubItems = list(self.SubItems)
        new_item.ImageIndex = self.ImageIndex
        new_item.ImageKey = self.ImageKey
        new_item.Tag = self.Tag
        new_item.BackColor = self.BackColor
        new_item.ForeColor = self.ForeColor
        new_item.Font = self.Font
        new_item.Checked = self.Checked
        new_item.Group = self.Group
        new_item.IndentCount = self.IndentCount
        new_item.StateImageIndex = self.StateImageIndex
        new_item.ToolTipText = self.ToolTipText
        new_item.UseItemStyleForSubItems = self.UseItemStyleForSubItems
        new_item.Name = self.Name
        return new_item

    def EnsureVisible(self):
        """Ensures that the item is visible within the control."""
        if self._list_view and self._list_view._tk_widget:
            # Treeview see method
            # We need the item ID in the treeview. 
            # Currently ListView implementation doesn't store ID in ListViewItem easily accessible.
            # Assuming ListView manages mapping or we find it.
            pass

    def Remove(self):
        """Removes the item from its associated ListView control."""
        if self._list_view:
            self._list_view.Items.remove(self)
            # Trigger UI update in ListView
            # self._list_view._remove_item_from_ui(self) # Hypothetical method
            self._list_view = None

    def ToString(self):
        """Returns a string that represents the current object."""
        return f"ListViewItem: {{Text={self.Text}}}"


class ColumnHeader:
    """
    Represents a column header in a ListView.
    
    Usage - Option 1: col = ColumnHeader(); col.Text = "Column"; col.Width = 150
    Usage - Option 2: col = ColumnHeader({'Text': 'Column', 'Width': 150})
    """
    
    def __init__(self, props=None, **kwargs):
        # Support dictionary-based init
        if isinstance(props, dict):
            kwargs.update(props)
        
        self._text = kwargs.get('Text', "")
        self._width = kwargs.get('Width', 60)
        self._text_align = kwargs.get('TextAlign', HorizontalAlignment.Left)
        self._image_index = kwargs.get('ImageIndex', -1)
        self._image_key = kwargs.get('ImageKey', "")
        self._name = kwargs.get('Name', "")
        self._tag = kwargs.get('Tag', None)
        self._display_index = kwargs.get('DisplayIndex', -1)
        
        self._list_view = None # Reference to parent ListView
        
        # Events
        self.Disposed = lambda sender, e: None

    @property
    def Text(self):
        """Gets or sets the text displayed in the column header."""
        return self._text

    @Text.setter
    def Text(self, value): 
        self._text = value
        # TODO: Update UI if attached to ListView

    @property
    def Width(self):
        """Gets or sets the width of the column."""
        return self._width

    @Width.setter
    def Width(self, value): 
        self._width = value
        # TODO: Update UI if attached to ListView

    @property
    def TextAlign(self):
        """Gets or sets the horizontal alignment of the text displayed in the ColumnHeader."""
        return self._text_align

    @TextAlign.setter
    def TextAlign(self, value): 
        self._text_align = value
        # TODO: Update UI if attached to ListView

    @property
    def ImageIndex(self):
        """Gets or sets the index of the image displayed in the ColumnHeader."""
        return self._image_index

    @ImageIndex.setter
    def ImageIndex(self, value):
        self._image_index = value

    @property
    def ImageKey(self):
        """Gets or sets the key of the image displayed in the ColumnHeader."""
        return self._image_key

    @ImageKey.setter
    def ImageKey(self, value):
        self._image_key = value

    @property
    def Name(self):
        """Gets or sets the name of the ColumnHeader."""
        return self._name

    @Name.setter
    def Name(self, value):
        self._name = value

    @property
    def Tag(self):
        """Gets or sets an object that contains data to associate with the ColumnHeader."""
        return self._tag

    @Tag.setter
    def Tag(self, value):
        self._tag = value

    @property
    def DisplayIndex(self):
        """Gets or sets the display order of the column relative to the currently displayed columns."""
        return self._display_index

    @DisplayIndex.setter
    def DisplayIndex(self, value):
        self._display_index = value

    @property
    def ListView(self):
        """Gets the ListView control the ColumnHeader is located in."""
        return self._list_view
    
    @property
    def Index(self):
        """Gets the location of the ColumnHeader within the ListView.ColumnHeaderCollection of the ListView control."""
        if self._list_view:
            try:
                return self._list_view.Columns.index(self)
            except ValueError:
                return -1
        return -1

    @property
    def ImageList(self):
        """Gets the ImageList that contains the image displayed with the ColumnHeader."""
        if self._list_view:
            return self._list_view.SmallImageList
        return None

    def AutoResize(self, style):
        """Resizes the width of the column as indicated by the resize style."""
        pass # Placeholder

    def Clone(self):
        """Creates an identical copy of the current ColumnHeader that is not attached to any list view control."""
        new_col = ColumnHeader()
        new_col.Text = self.Text
        new_col.Width = self.Width
        new_col.TextAlign = self.TextAlign
        new_col.ImageIndex = self.ImageIndex
        new_col.ImageKey = self.ImageKey
        new_col.Name = self.Name
        new_col.Tag = self.Tag
        return new_col

    def Dispose(self):
        """Releases all resources used by the Component."""
        self.Disposed(self, None)

    def ToString(self):
        """Returns a String that represents the current Object."""
        return f"ColumnHeader: Text: {self.Text}"


class ImageLayout(Enum):
    None_ = 0
    Tile = 1
    Center = 2
    Stretch = 3
    Zoom = 4


class RightToLeft(Enum):
    No = 0
    Yes = 1
    Inherit = 2


class BorderStyle(Enum):
    None_ = 0
    FixedSingle = 1
    Fixed3D = 2


class Activation(Enum):
    Standard = 0
    OneClick = 1
    TwoClick = 2


class ListViewAlignment(Enum):
    Default = 0
    Top = 1
    Left = 2
    SnapToGrid = 3


class ListViewHitTestLocations(Enum):
    None_ = 1
    Image = 2
    Label = 4
    StateImage = 8


class ListViewItemCollection:
    """Represents the collection of items in a ListView control."""
    def __init__(self, owner):
        self._owner = owner
        self._items = []

    def Add(self, item):
        """Adds an item to the collection."""
        if isinstance(item, str):
            item = ListViewItem(Text=item)
        
        if not isinstance(item, ListViewItem):
            raise TypeError("Item must be a ListViewItem or string")
            
        self._items.append(item)
        item._list_view = self._owner
        item._index = len(self._items) - 1
        
        # Add to UI
        if self._owner and self._owner._tk_widget:
            self._owner._add_item_to_ui(item)
            
        return item

    def AddRange(self, items):
        """Adds an array of items to the collection."""
        for item in items:
            self.Add(item)

    def Clear(self):
        """Removes all items from the collection."""
        self._items.clear()
        if self._owner and self._owner._tk_widget:
            # Clear UI
            for item in self._owner._tk_widget.get_children():
                self._owner._tk_widget.delete(item)

    def Contains(self, item):
        """Determines whether the specified item is located in the collection."""
        return item in self._items

    def ContainsKey(self, key):
        """Determines whether the collection contains an item with the specified key."""
        return any(item.Name == key for item in self._items)

    def IndexOf(self, item):
        """Returns the index within the collection of the specified item."""
        try:
            return self._items.index(item)
        except ValueError:
            return -1

    def IndexOfKey(self, key):
        """Returns the index of the first occurrence of an item with the specified key."""
        for i, item in enumerate(self._items):
            if item.Name == key:
                return i
        return -1

    def Insert(self, index, item):
        """Inserts an item into the collection at the specified index."""
        if isinstance(item, str):
            item = ListViewItem(Text=item)
            
        self._items.insert(index, item)
        item._list_view = self._owner
        
        # Re-index items
        for i, it in enumerate(self._items):
            it._index = i
            
        # Update UI
        if self._owner and self._owner._tk_widget:
             self._owner._insert_item_to_ui(index, item)

    def Remove(self, item):
        """Removes the specified item from the collection."""
        if item in self._items:
            self._items.remove(item)
            if self._owner and self._owner._tk_widget and item._id:
                self._owner._tk_widget.delete(item._id)
            
            # Re-index
            for i, it in enumerate(self._items):
                it._index = i

    def RemoveAt(self, index):
        """Removes the item at the specified index."""
        if 0 <= index < len(self._items):
            item = self._items[index]
            self.Remove(item)

    def RemoveByKey(self, key):
        """Removes the item with the specified key."""
        index = self.IndexOfKey(key)
        if index != -1:
            self.RemoveAt(index)

    def __getitem__(self, index):
        if isinstance(index, str):
            idx = self.IndexOfKey(index)
            if idx != -1:
                return self._items[idx]
            raise KeyError(f"Item with key '{index}' not found")
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)


class ColumnHeaderCollection:
    """Represents the collection of column headers in a ListView control."""
    def __init__(self, owner):
        self._owner = owner
        self._items = []

    def Add(self, text, width=60, text_align=HorizontalAlignment.Left):
        """Adds a column header to the collection."""
        col = ColumnHeader()
        col.Text = text
        col.Width = width
        col.TextAlign = text_align
        return self.AddColumn(col)

    def AddColumn(self, column):
        """Adds a ColumnHeader to the collection."""
        self._items.append(column)
        column._list_view = self._owner
        
        # Update UI
        if self._owner and self._owner._tk_widget:
            self._owner._update_columns()
            
        return column

    def Clear(self):
        """Removes all columns from the collection."""
        self._items.clear()
        if self._owner:
            self._owner._update_columns()

    def Contains(self, column):
        return column in self._items

    def IndexOf(self, column):
        try:
            return self._items.index(column)
        except ValueError:
            return -1

    def Remove(self, column):
        if column in self._items:
            self._items.remove(column)
            if self._owner:
                self._owner._update_columns()

    def RemoveAt(self, index):
        if 0 <= index < len(self._items):
            self._items.pop(index)
            if self._owner:
                self._owner._update_columns()

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)


class ListViewHitTestInfo:
    def __init__(self, item, location):
        self.Item = item
        self.Location = location


class ListView(ControlBase):
    """
    Represents a ListView with VB.NET properties.
    """
    
    def __init__(self, master_form, props=None):
        defaults = {
            'Columns': None,
            'Left': 10,
            'Top': 280,
            'Width': 300,
            'Height': 150,
            'Name': "",
            'Items': None,
            'View': View.Details,
            'SmallImageList': None,
            'LargeImageList': None,
            'FullRowSelect': True,
            'MultiSelect': True,
            'CheckBoxes': False,
            'GridLines': False,
            'HeaderStyle': ColumnHeaderStyle.Clickable,
            'Sorting': SortOrder.None_,
            'Enabled': True,
            'Visible': True,
            'Tag': None
        }
        
        if props:
            defaults.update(props)
        
        # Resolve Tkinter widget and save parent container
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Set ControlBase properties
        self.Name = defaults['Name']
        self.Enabled = defaults['Enabled']
        self.Visible = defaults['Visible']
        self.Tag = defaults['Tag']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        
        # Save parent container for auto-registration
        self._parent_container = parent_container
        
        # Collections
        self._items = ListViewItemCollection(self)
        self._columns = ColumnHeaderCollection(self)
        
        # Properties
        self._view = defaults['View']
        self._small_image_list = defaults['SmallImageList']
        self._large_image_list = defaults['LargeImageList']
        self._full_row_select = defaults['FullRowSelect']
        self._multi_select = defaults['MultiSelect']
        self._check_boxes = defaults['CheckBoxes']
        self._grid_lines = defaults['GridLines']
        self._header_style = defaults['HeaderStyle']
        self._sorting = defaults['Sorting']
        self._activation = Activation.Standard
        self._alignment = ListViewAlignment.Top
        self._allow_column_reorder = False
        self._auto_arrange = True
        self._background_image = None
        self._background_image_layout = ImageLayout.Tile
        self._background_image_tiled = False
        self._focused_item = None
        self._groups = [] # Placeholder
        self._hide_selection = True
        self._hot_tracking = False
        self._hover_selection = False
        self._insertion_mark = None # Placeholder
        self._label_edit = False
        self._label_wrap = True
        self._list_view_item_sorter = None
        self._owner_draw = False
        self._scrollable = True
        self._show_groups = False
        self._show_item_tool_tips = False
        self._tile_size = Size(0, 0)
        self._top_item = None
        self._use_compatible_state_image_behavior = True
        self._virtual_list_size = 0
        self._virtual_mode = False
        
        # Events
        self.SelectedIndexChanged = lambda sender=None, e=None: None
        self.ItemSelectionChanged = lambda sender=None, e=None: None
        self.DoubleClick = lambda sender=None, e=None: None
        self.Click = lambda sender=None, e=None: None
        self.ItemCheck = lambda sender, e: None
        self.AfterCheck = lambda sender, e: None
        self.ColumnClick = lambda sender, e: None
        self.MouseClick = lambda sender, e: None
        self.Enter = lambda: None
        self.Leave = lambda: None
        self.KeyDown = lambda sender=None, e=None: None
        self.KeyPress = lambda sender=None, e=None: None
        self.DrawItem = lambda sender=None, e=None: None
        self.DrawSubItem = lambda sender, e: None
        self.DrawColumnHeader = lambda sender, e: None
        self.AfterLabelEdit = lambda sender, e: None
        self.BeforeLabelEdit = lambda sender, e: None
        self.CacheVirtualItems = lambda sender, e: None
        self.RetrieveVirtualItem = lambda sender, e: None
        self.SearchForVirtualItem = lambda sender, e: None
        self.ItemActivate = lambda sender, e: None
        self.ItemDrag = lambda sender, e: None
        self.ItemMouseHover = lambda sender, e: None
        self.VirtualItemsSelectionRangeChanged = lambda sender, e: None
        
        # Initialize Widget
        show = 'headings' if self._view == View.Details else 'tree'
        selectmode = 'extended' if self._multi_select else 'browse'
        self._tk_widget = ttk.Treeview(self.master, show=show, selectmode=selectmode, height=10)
        
        # Initial Columns
        if defaults['Columns']:
            for col in defaults['Columns']:
                self._columns.AddColumn(col)
        else:
            # Add default column if none provided, to show something
            self._columns.Add("ColumnHeader")
            
        # Initial Items
        if defaults['Items']:
            for item in defaults['Items']:
                self._items.Add(item)
        
        self._update_styles()
        self._place_control(self.Width, self.Height)
        
        # Bind events
        self._bind_common_events()
        self._tk_widget.bind('<<TreeviewSelect>>', self._on_selection_changed)
        self._tk_widget.bind('<Key>', self._on_key_down)
        self._tk_widget.bind('<KeyPress>', self._on_key_press)
        self._tk_widget.bind('<Double-1>', self._on_double_click)
        self._tk_widget.bind('<Button-1>', self._on_click)
        
        # Apply Dock and Anchor if specified in props
        if 'Dock' in defaults and defaults['Dock']:
            self.Dock = defaults['Dock']
        if 'Anchor' in defaults and defaults['Anchor']:
            self.Anchor = defaults['Anchor']
        
        # Auto-register with parent container if necessary
        self._auto_register_with_parent()

    @property
    def Items(self):
        return self._items

    @Items.setter
    def Items(self, value):
        self._items.Clear()
        if value:
            self._items.AddRange(value)

    @property
    def Columns(self):
        return self._columns

    @Columns.setter
    def Columns(self, value):
        self._columns.Clear()
        if value:
            for col in value:
                self._columns.AddColumn(col)

    @property
    def View(self):
        return self._view

    @View.setter
    def View(self, value):
        self._view = value
        show = 'headings' if value == View.Details else 'tree'
        if self._tk_widget:
            self._tk_widget.config(show=show)

    @property
    def SelectedItems(self):
        """Gets the collection of selected items."""
        selections = self._tk_widget.selection()
        selected_items = []
        for sel in selections:
            # Find item by ID
            for item in self._items:
                if item._id == sel:
                    selected_items.append(item)
                    break
        return selected_items

    @property
    def SelectedIndices(self):
        """Gets the collection of selected indices."""
        selections = self._tk_widget.selection()
        indices = []
        for sel in selections:
            for i, item in enumerate(self._items):
                if item._id == sel:
                    indices.append(i)
                    break
        return indices

    @property
    def CheckedItems(self):
        """Gets the collection of checked items."""
        return [item for item in self._items if item.Checked]

    @property
    def CheckedIndices(self):
        """Gets the collection of checked indices."""
        return [i for i, item in enumerate(self._items) if item.Checked]

    @property
    def FocusedItem(self):
        return self._focused_item

    @property
    def FullRowSelect(self):
        return self._full_row_select

    @FullRowSelect.setter
    def FullRowSelect(self, value):
        self._full_row_select = value
        # Treeview always does full row select visually in most themes

    @property
    def GridLines(self):
        return self._grid_lines

    @GridLines.setter
    def GridLines(self, value):
        self._grid_lines = value
        self._update_styles()

    @property
    def MultiSelect(self):
        return self._multi_select

    @MultiSelect.setter
    def MultiSelect(self, value):
        self._multi_select = value
        selectmode = 'extended' if value else 'browse'
        if self._tk_widget:
            self._tk_widget.config(selectmode=selectmode)

    @property
    def CheckBoxes(self):
        return self._check_boxes

    @CheckBoxes.setter
    def CheckBoxes(self, value):
        self._check_boxes = value
        # Not natively supported in Treeview without custom drawing or images

    @property
    def HeaderStyle(self):
        return self._header_style

    @HeaderStyle.setter
    def HeaderStyle(self, value):
        self._header_style = value
        if self._tk_widget:
            if value == ColumnHeaderStyle.None_:
                self._tk_widget.config(show='')
            else:
                self._tk_widget.config(show='headings')

    @property
    def Sorting(self):
        return self._sorting

    @Sorting.setter
    def Sorting(self, value):
        self._sorting = value
        if value != SortOrder.None_:
            self.Sort()

    @property
    def SmallImageList(self):
        return self._small_image_list

    @SmallImageList.setter
    def SmallImageList(self, value):
        self._small_image_list = value

    @property
    def LargeImageList(self):
        return self._large_image_list

    @LargeImageList.setter
    def LargeImageList(self, value):
        self._large_image_list = value

    @property
    def Activation(self): return self._activation
    @Activation.setter
    def Activation(self, value): self._activation = value

    @property
    def Alignment(self): return self._alignment
    @Alignment.setter
    def Alignment(self, value): self._alignment = value

    @property
    def AllowColumnReorder(self): return self._allow_column_reorder
    @AllowColumnReorder.setter
    def AllowColumnReorder(self, value): self._allow_column_reorder = value

    @property
    def AutoArrange(self): return self._auto_arrange
    @AutoArrange.setter
    def AutoArrange(self, value): self._auto_arrange = value

    @property
    def BackgroundImage(self): return self._background_image
    @BackgroundImage.setter
    def BackgroundImage(self, value): self._background_image = value

    @property
    def BackgroundImageLayout(self): return self._background_image_layout
    @BackgroundImageLayout.setter
    def BackgroundImageLayout(self, value): self._background_image_layout = value

    @property
    def BackgroundImageTiled(self): return self._background_image_tiled
    @BackgroundImageTiled.setter
    def BackgroundImageTiled(self, value): self._background_image_tiled = value

    @property
    def Groups(self): return self._groups

    @property
    def HideSelection(self): return self._hide_selection
    @HideSelection.setter
    def HideSelection(self, value): self._hide_selection = value

    @property
    def HotTracking(self): return self._hot_tracking
    @HotTracking.setter
    def HotTracking(self, value): self._hot_tracking = value

    @property
    def HoverSelection(self): return self._hover_selection
    @HoverSelection.setter
    def HoverSelection(self, value): self._hover_selection = value

    @property
    def InsertionMark(self): return self._insertion_mark

    @property
    def LabelEdit(self): return self._label_edit
    @LabelEdit.setter
    def LabelEdit(self, value): self._label_edit = value

    @property
    def LabelWrap(self): return self._label_wrap
    @LabelWrap.setter
    def LabelWrap(self, value): self._label_wrap = value

    @property
    def ListViewItemSorter(self): return self._list_view_item_sorter
    @ListViewItemSorter.setter
    def ListViewItemSorter(self, value): self._list_view_item_sorter = value

    @property
    def OwnerDraw(self): return self._owner_draw
    @OwnerDraw.setter
    def OwnerDraw(self, value): self._owner_draw = value

    @property
    def Scrollable(self): return self._scrollable
    @Scrollable.setter
    def Scrollable(self, value): self._scrollable = value

    @property
    def ShowGroups(self): return self._show_groups
    @ShowGroups.setter
    def ShowGroups(self, value): self._show_groups = value

    @property
    def ShowItemToolTips(self): return self._show_item_tool_tips
    @ShowItemToolTips.setter
    def ShowItemToolTips(self, value): self._show_item_tool_tips = value

    @property
    def TileSize(self): return self._tile_size
    @TileSize.setter
    def TileSize(self, value): self._tile_size = value

    @property
    def TopItem(self): return self._top_item
    @TopItem.setter
    def TopItem(self, value): 
        self._top_item = value
        if value:
            self.EnsureVisible(value.Index)

    @property
    def UseCompatibleStateImageBehavior(self): return self._use_compatible_state_image_behavior
    @UseCompatibleStateImageBehavior.setter
    def UseCompatibleStateImageBehavior(self, value): self._use_compatible_state_image_behavior = value

    @property
    def VirtualListSize(self): return self._virtual_list_size
    @VirtualListSize.setter
    def VirtualListSize(self, value): self._virtual_list_size = value

    @property
    def VirtualMode(self): return self._virtual_mode
    @VirtualMode.setter
    def VirtualMode(self, value): self._virtual_mode = value

    def AddItem(self, item):
        """Adds a ListViewItem to the ListView. (Legacy support)"""
        self._items.Add(item)

    def GetSelectedItem(self):
        """Gets the first selected item. (Legacy support)"""
        items = self.SelectedItems
        return items[0] if items else None

    def set_View(self, view):
        """Sets the ListView view. (Legacy support)"""
        self.View = view

    def set_Sorting(self, sorting):
        """Sets the sorting type. (Legacy support)"""
        self.Sorting = sorting

    def ArrangeIcons(self, value=None):
        """Organizes icons."""
        pass

    def AutoResizeColumn(self, column_index, style):
        """Resizes the width of the column."""
        pass

    def AutoResizeColumns(self, style):
        """Resizes the width of the columns."""
        pass

    def BeginUpdate(self):
        """Prevents the control from drawing until EndUpdate is called."""
        pass

    def EndUpdate(self):
        """Resumes drawing."""
        pass

    def Clear(self):
        """Removes all items and columns."""
        self._items.Clear()
        self._columns.Clear()

    def EnsureVisible(self, index):
        """Ensures that the item at the specified index is visible."""
        if 0 <= index < len(self._items):
            item = self._items[index]
            if item._id:
                self._tk_widget.see(item._id)

    def FindItemWithText(self, text, include_subitems=False, start_index=0, is_prefix_search=True):
        """Finds the first ListViewItem that begins with the specified text value."""
        for i in range(start_index, len(self._items)):
            item = self._items[i]
            if is_prefix_search:
                if item.Text.startswith(text):
                    return item
                if include_subitems:
                    for sub in item.SubItems:
                        if sub.startswith(text):
                            return item
            else:
                if item.Text == text:
                    return item
                if include_subitems:
                    for sub in item.SubItems:
                        if sub == text:
                            return item
        return None

    def FindNearestItem(self, search_direction, x, y):
        """Finds the nearest item."""
        return None # Not supported in Treeview

    def GetItemAt(self, x, y):
        """Retrieves the item at the specified location."""
        item_id = self._tk_widget.identify_row(y)
        if item_id:
            for item in self._items:
                if item._id == item_id:
                    return item
        return None

    def GetItemRect(self, index):
        """Retrieves the bounding rectangle for an item."""
        if 0 <= index < len(self._items):
            item = self._items[index]
            if item._id:
                bbox = self._tk_widget.bbox(item._id)
                if bbox:
                    return Rectangle(bbox[0], bbox[1], bbox[2], bbox[3])
        return Rectangle(0, 0, 0, 0)

    def HitTest(self, x, y):
        """Provides item information given a point."""
        item = self.GetItemAt(x, y)
        return ListViewHitTestInfo(item, ListViewHitTestLocations.None_ if not item else ListViewHitTestLocations.Image) # Simplified

    def RedrawItems(self, start_index, end_index, invalidate_only):
        """Redraws items."""
        pass

    def Sort(self):
        """Sorts the items."""
        if self.Sorting != SortOrder.None_:
            reverse = self.Sorting == SortOrder.Descending
            # Sort internal list
            self._items._items.sort(key=lambda x: x.Text, reverse=reverse)
            # Refresh UI
            self._refresh_items()

    def _add_item_to_ui(self, item):
        values = item.SubItems
        item._id = self._tk_widget.insert('', 'end', text=item.Text, values=values)

    def _insert_item_to_ui(self, index, item):
        values = item.SubItems
        item._id = self._tk_widget.insert('', index, text=item.Text, values=values)

    def _update_columns(self):
        self._tk_widget['columns'] = [str(i) for i in range(len(self._columns))]
        
        anchor_map = {
            HorizontalAlignment.Left: 'w',
            HorizontalAlignment.Right: 'e',
            HorizontalAlignment.Center: 'center'
        }
        
        for i, col in enumerate(self._columns):
            self._tk_widget.heading(str(i), text=col.Text, command=lambda c=i: self._on_column_click(c))
            anchor = anchor_map.get(col.TextAlign, 'w')
            self._tk_widget.column(str(i), width=col.Width, anchor=anchor)

    def _refresh_items(self):
        # Clear all
        for item in self._tk_widget.get_children():
            self._tk_widget.delete(item)
        # Re-add
        for item in self._items:
            self._add_item_to_ui(item)

    def _update_styles(self):
        style = ttk.Style()
        if self.GridLines:
            style.configure("Treeview", rowheight=25) # Placeholder

    def _on_selection_changed(self, event):
        self.SelectedIndexChanged()
        selected = self.SelectedItems
        for item in selected:
            self.ItemSelectionChanged(self, {'Item': item, 'Selected': True})

    def _on_column_click(self, column_index):
        self.ColumnClick(self, {'Column': self._columns[column_index]})

    def _on_key_down(self, event):
        self.KeyDown(self, {'KeyCode': event.keysym, 'Modifiers': event.state})

    def _on_key_press(self, event):
        self.KeyPress(self, {'KeyChar': event.char})

    def _on_double_click(self, event):
        self.DoubleClick()
        self.MouseDoubleClick(self, {'Button': 'Left', 'Clicks': 2, 'X': event.x, 'Y': event.y})

    def _on_click(self, event):
        self.Click()
        self.MouseClick(self, {'Button': 'Left', 'Clicks': 1, 'X': event.x, 'Y': event.y})
        item = self.GetItemAt(event.x, event.y)
        if item:
            self._focused_item = item
            if self.Activation == Activation.OneClick:
                self.ItemActivate(self, {'Item': item})


class TreeNodeCollection:
    """Collection of TreeNodes."""
    def __init__(self, owner):
        self.owner = owner  # TreeNode or TreeView
        self._list = []

    @property
    def Count(self):
        """Gets the total number of TreeNode objects in the collection."""
        return len(self._list)

    @property
    def IsReadOnly(self):
        """Gets a value indicating whether the collection is read-only."""
        return False

    def Add(self, *args):
        """Adds a new node to the collection."""
        node = None
        
        # Add(TreeNode)
        if len(args) == 1 and isinstance(args[0], TreeNode):
            node = args[0]
        
        # Add(String text)
        elif len(args) == 1 and isinstance(args[0], str):
            node = TreeNode(args[0])

        # Add(String key, String text)
        elif len(args) == 2:
            node = TreeNode(args[1])
            node.Name = args[0]

        # Add(String key, String text, Int32 imageIndex)
        elif len(args) == 3 and isinstance(args[2], int):
            node = TreeNode(args[1])
            node.Name = args[0]
            node.ImageIndex = args[2]

        # Add(String key, String text, String imageKey)
        elif len(args) == 3 and isinstance(args[2], str):
            node = TreeNode(args[1])
            node.Name = args[0]
            node.ImageKey = args[2]

        # Add(String key, String text, Int32 imageIndex, Int32 selectedImageIndex)
        elif len(args) == 4 and isinstance(args[2], int) and isinstance(args[3], int):
            node = TreeNode(args[1])
            node.Name = args[0]
            node.ImageIndex = args[2]
            node.SelectedImageIndex = args[3]

        # Add(String key, String text, String imageKey, String selectedImageKey)
        elif len(args) == 4 and isinstance(args[2], str) and isinstance(args[3], str):
            node = TreeNode(args[1])
            node.Name = args[0]
            node.ImageKey = args[2]
            node.SelectedImageKey = args[3]
            
        if node:
            return self._add_node(node)
        else:
            raise ValueError("Invalid arguments for Add")

    def _add_node(self, node):
        self._list.append(node)
        self._set_parent_and_update_ui(node)
        return node

    def AddRange(self, nodes):
        """Adds an array of previously created tree nodes to the collection."""
        for node in nodes:
            self.Add(node)

    def Clear(self):
        """Removes all nodes."""
        # Create a copy to iterate safely
        for node in list(self._list):
            self.Remove(node)

    def Contains(self, node):
        """Determines whether the specified tree node is a member of the collection."""
        return node in self._list

    def ContainsKey(self, key):
        """Determines whether the collection contains a tree node with the specified key."""
        for node in self._list:
            if node.Name == key:
                return True
        return False

    def CopyTo(self, array, index):
        """Copies the entire collection into an existing array at a specified location within the array."""
        for i, node in enumerate(self._list):
            if index + i < len(array):
                array[index + i] = node

    def Find(self, key, search_all_children):
        """Finds the tree nodes with specified key, optionally searching subnodes."""
        found = []
        for node in self._list:
            if node.Name == key:
                found.append(node)
            if search_all_children:
                found.extend(node.Nodes.Find(key, True))
        return found

    def IndexOf(self, node):
        """Returns the index of the specified node in the collection."""
        try:
            return self._list.index(node)
        except ValueError:
            return -1

    def IndexOfKey(self, key):
        """Returns the index of the first occurrence of a tree node with the specified key."""
        for i, node in enumerate(self._list):
            if node.Name == key:
                return i
        return -1

    def Insert(self, index, *args):
        """Inserts a tree node into the collection at the specified location."""
        node = None
        
        # Insert(Int32, TreeNode)
        if len(args) == 1 and isinstance(args[0], TreeNode):
            node = args[0]
            
        # Insert(Int32, String text)
        elif len(args) == 1 and isinstance(args[0], str):
            node = TreeNode(args[0])

        # Insert(Int32, String key, String text)
        elif len(args) == 2:
            node = TreeNode(args[1])
            node.Name = args[0]

        # Insert(Int32, String key, String text, Int32 imageIndex)
        elif len(args) == 3 and isinstance(args[2], int):
            node = TreeNode(args[1])
            node.Name = args[0]
            node.ImageIndex = args[2]

        # Insert(Int32, String key, String text, String imageKey)
        elif len(args) == 3 and isinstance(args[2], str):
            node = TreeNode(args[1])
            node.Name = args[0]
            node.ImageKey = args[2]

        # Insert(Int32, String key, String text, Int32 imageIndex, Int32 selectedImageIndex)
        elif len(args) == 4 and isinstance(args[2], int) and isinstance(args[3], int):
            node = TreeNode(args[1])
            node.Name = args[0]
            node.ImageIndex = args[2]
            node.SelectedImageIndex = args[3]

        # Insert(Int32, String key, String text, String imageKey, String selectedImageKey)
        elif len(args) == 4 and isinstance(args[2], str) and isinstance(args[3], str):
            node = TreeNode(args[1])
            node.Name = args[0]
            node.ImageKey = args[2]
            node.SelectedImageKey = args[3]
            
        if node:
            self._list.insert(index, node)
            self._set_parent_and_update_ui(node, index)
            return node
        else:
            raise ValueError("Invalid arguments for Insert")

    def Remove(self, node):
        """Removes a node from the collection."""
        if node in self._list:
            self._list.remove(node)
            if node.TreeView:
                node.TreeView._remove_node_from_ui(node)
                node.TreeView = None

    def RemoveAt(self, index):
        """Removes the tree node at the specified index from the collection."""
        if 0 <= index < len(self._list):
            node = self._list[index]
            self.Remove(node)

    def RemoveByKey(self, key):
        """Removes the tree node with the specified key from the collection."""
        node = self[key]
        if node:
            self.Remove(node)

    def _set_parent_and_update_ui(self, node, insert_index=None):
        # Set parent references
        if isinstance(self.owner, TreeNode):
            node.Parent = self.owner
            tree_view = self.owner.TreeView
        else: # Owner is TreeView
            node.Parent = None
            tree_view = self.owner
            
        # If attached to a TreeView, update UI
        if tree_view:
            node.TreeView = tree_view
            if insert_index is not None:
                # For insert, we need to handle UI insertion at specific index
                # Tkinter insert supports index
                tree_view._insert_node_to_ui(node, self.owner, insert_index)
            else:
                tree_view._add_node_to_ui(node, self.owner)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._list[key]
        if isinstance(key, str):
            for node in self._list:
                if node.Name == key:
                    return node
        return None

    def __setitem__(self, index, value):
        if isinstance(index, int) and isinstance(value, TreeNode):
            old_node = self._list[index]
            self.Remove(old_node)
            self.Insert(index, value)

    def __len__(self):
        return len(self._list)

    def __iter__(self):
        return iter(self._list)


class TreeNode:
    """
    Represents a node in a TreeView.
    """
    
    def __init__(self, text="", **kwargs):
        # Support dictionary-based init for compatibility
        if isinstance(text, dict):
            kwargs.update(text)
            text = kwargs.get('Text', "")
        
        self._text = text
        self._image_index = kwargs.get('ImageIndex', -1)
        self._selected_image_index = kwargs.get('SelectedImageIndex', -1)
        self._image_key = kwargs.get('ImageKey', "")
        self._selected_image_key = kwargs.get('SelectedImageKey', "")
        self._state_image_index = kwargs.get('StateImageIndex', -1)
        self._state_image_key = kwargs.get('StateImageKey', "")
        self._tag = kwargs.get('Tag', None)
        self._name = kwargs.get('Name', "")
        self._tool_tip_text = kwargs.get('ToolTipText', "")
        self._checked = kwargs.get('Checked', False)
        self._back_color = kwargs.get('BackColor', None)
        self._fore_color = kwargs.get('ForeColor', None)
        self._node_font = kwargs.get('NodeFont', None)
        self._context_menu_strip = kwargs.get('ContextMenuStrip', None)
        
        self.TreeView = None
        self.Parent = None
        self._id = None  # Tkinter Item ID
        
        self.Nodes = TreeNodeCollection(self)
        
        # Add initial children if provided
        initial_nodes = kwargs.get('Nodes', [])
        if initial_nodes:
            for node in initial_nodes:
                self.Nodes.Add(node)

    @property
    def Text(self):
        return self._text

    @Text.setter
    def Text(self, value):
        self._text = value
        if self.TreeView and self._id:
            self.TreeView._tk_widget.item(self._id, text=value)

    @property
    def Name(self): return self._name
    @Name.setter
    def Name(self, value): self._name = value

    @property
    def Tag(self): return self._tag
    @Tag.setter
    def Tag(self, value): self._tag = value

    @property
    def ImageIndex(self): return self._image_index
    @ImageIndex.setter
    def ImageIndex(self, value): self._image_index = value

    @property
    def SelectedImageIndex(self): return self._selected_image_index
    @SelectedImageIndex.setter
    def SelectedImageIndex(self, value): self._selected_image_index = value

    @property
    def ImageKey(self): return self._image_key
    @ImageKey.setter
    def ImageKey(self, value): self._image_key = value

    @property
    def SelectedImageKey(self): return self._selected_image_key
    @SelectedImageKey.setter
    def SelectedImageKey(self, value): self._selected_image_key = value

    @property
    def StateImageIndex(self): return self._state_image_index
    @StateImageIndex.setter
    def StateImageIndex(self, value): self._state_image_index = value

    @property
    def StateImageKey(self): return self._state_image_key
    @StateImageKey.setter
    def StateImageKey(self, value): self._state_image_key = value

    @property
    def ToolTipText(self): return self._tool_tip_text
    @ToolTipText.setter
    def ToolTipText(self, value): self._tool_tip_text = value

    @property
    def Checked(self): return self._checked
    @Checked.setter
    def Checked(self, value): self._checked = value

    @property
    def BackColor(self): return self._back_color
    @BackColor.setter
    def BackColor(self, value): self._back_color = value

    @property
    def ForeColor(self): return self._fore_color
    @ForeColor.setter
    def ForeColor(self, value): self._fore_color = value

    @property
    def NodeFont(self): return self._node_font
    @NodeFont.setter
    def NodeFont(self, value): self._node_font = value

    @property
    def ContextMenuStrip(self): return self._context_menu_strip
    @ContextMenuStrip.setter
    def ContextMenuStrip(self, value): self._context_menu_strip = value

    @property
    def FullPath(self):
        """Gets the full path of the node."""
        path = [self.Text]
        current = self.Parent
        while current:
            path.insert(0, current.Text)
            current = current.Parent
        separator = self.TreeView.PathSeparator if self.TreeView else "\\"
        return separator.join(path)

    @property
    def Level(self):
        """Gets the zero-based depth of the tree node in the TreeView control."""
        level = 0
        current = self.Parent
        while current:
            level += 1
            current = current.Parent
        return level

    @property
    def Index(self):
        """Gets the position of the tree node in the tree node collection."""
        if self.Parent:
            return self.Parent.Nodes.IndexOf(self)
        elif self.TreeView:
            return self.TreeView.Nodes.IndexOf(self)
        return -1

    @property
    def FirstNode(self):
        """Gets the first child tree node in the tree node collection."""
        if len(self.Nodes) > 0:
            return self.Nodes[0]
        return None

    @property
    def LastNode(self):
        """Gets the last child tree node."""
        if len(self.Nodes) > 0:
            return self.Nodes[len(self.Nodes) - 1]
        return None

    @property
    def NextNode(self):
        """Gets the next sibling tree node."""
        parent_nodes = self.Parent.Nodes if self.Parent else (self.TreeView.Nodes if self.TreeView else None)
        if parent_nodes:
            index = self.Index
            if index != -1 and index < len(parent_nodes) - 1:
                return parent_nodes[index + 1]
        return None

    @property
    def PrevNode(self):
        """Gets the previous sibling tree node."""
        parent_nodes = self.Parent.Nodes if self.Parent else (self.TreeView.Nodes if self.TreeView else None)
        if parent_nodes:
            index = self.Index
            if index > 0:
                return parent_nodes[index - 1]
        return None

    @property
    def IsExpanded(self):
        """Gets whether the node is expanded."""
        if self.TreeView and self._id:
            return self.TreeView._tk_widget.item(self._id, 'open')
        return False

    @property
    def IsSelected(self):
        """Gets whether the node is selected."""
        if self.TreeView and self._id:
            return self.TreeView.SelectedNode == self
        return False

    @property
    def IsVisible(self):
        """Gets a value indicating whether the tree node is visible or partially visible."""
        # In Tkinter, if parent is open, it's visible (mostly)
        current = self.Parent
        while current:
            if not current.IsExpanded:
                return False
            current = current.Parent
        return True

    @property
    def IsEditing(self):
        """Gets a value indicating whether the tree node is in an editable state."""
        return False # Not implemented

    @property
    def Bounds(self):
        """Gets the bounds of the tree node."""
        if self.TreeView and self._id:
            bbox = self.TreeView._tk_widget.bbox(self._id)
            if bbox:
                return Rectangle(bbox[0], bbox[1], bbox[2], bbox[3])
        return Rectangle(0, 0, 0, 0)

    @property
    def Handle(self):
        """Gets the handle of the tree node."""
        return self._id

    def BeginEdit(self):
        """Initiates the editing of the tree node label."""
        pass

    def EndEdit(self, cancel):
        """Ends the editing of the tree node label."""
        pass

    def Clone(self):
        """Copies the tree node and the entire subtree rooted at this tree node."""
        new_node = TreeNode()
        new_node.Text = self.Text
        new_node.Name = self.Name
        new_node.Tag = self.Tag
        new_node.ImageIndex = self.ImageIndex
        new_node.SelectedImageIndex = self.SelectedImageIndex
        new_node.ImageKey = self.ImageKey
        new_node.SelectedImageKey = self.SelectedImageKey
        new_node.StateImageIndex = self.StateImageIndex
        new_node.StateImageKey = self.StateImageKey
        new_node.ToolTipText = self.ToolTipText
        new_node.Checked = self.Checked
        new_node.BackColor = self.BackColor
        new_node.ForeColor = self.ForeColor
        new_node.NodeFont = self.NodeFont
        
        for child in self.Nodes:
            new_node.Nodes.Add(child.Clone())
            
        return new_node

    def Expand(self):
        """Expands the node."""
        if self.TreeView and self._id:
            self.TreeView._tk_widget.item(self._id, open=True)
            # Trigger BeforeExpand/AfterExpand? (Tkinter handles this via events usually)

    def ExpandAll(self):
        """Expands all the child tree nodes."""
        self.Expand()
        for child in self.Nodes:
            child.ExpandAll()

    def Collapse(self, ignoreChildren=False):
        """Collapses the node."""
        if self.TreeView and self._id:
            self.TreeView._tk_widget.item(self._id, open=False)
            if not ignoreChildren:
                for child in self.Nodes:
                    child.Collapse()

    def Toggle(self):
        """Toggles the node expansion state."""
        if self.IsExpanded:
            self.Collapse()
        else:
            self.Expand()

    def EnsureVisible(self):
        """Ensures the node is visible, expanding parents if necessary."""
        if self.TreeView and self._id:
            self.TreeView._tk_widget.see(self._id)
            
    def Remove(self):
        """Removes the current node from the TreeView."""
        if self.Parent:
            self.Parent.Nodes.Remove(self)
        elif self.TreeView:
            self.TreeView.Nodes.Remove(self)
            
    def GetNodeCount(self, includeSubTrees):
        """Returns the number of child tree nodes."""
        count = len(self.Nodes)
        if includeSubTrees:
            for child in self.Nodes:
                count += child.GetNodeCount(True)
        return count

    def ToString(self):
        """Returns a string that represents the current object."""
        return f"TreeNode: {self.Text}"


class TreeViewDrawMode(Enum):
    Normal = 0
    OwnerDrawText = 1
    OwnerDrawAll = 2


class TreeView(ControlBase):
    """
    Represents a TreeView with VB.NET properties.
    """
    
    def __init__(self, master_form, props=None):
        defaults = {
            'Left': 10,
            'Top': 10,
            'Width': 200,
            'Height': 200,
            'Name': "",
            'Nodes': None,
            'ImageList': None,
            'ImageIndex': -1,
            'SelectedImageIndex': -1,
            'FullRowSelect': False,
            'CheckBoxes': False,
            'ShowLines': True,
            'ShowPlusMinus': True,
            'ShowRootLines': True,
            'PathSeparator': "\\",
            'LabelEdit': False,
            'Font': None,
            'ForeColor': None,
            'BackColor': None,
            'BackgroundImage': None,
            'BackgroundImageLayout': ImageLayout.Tile,
            'BorderStyle': BorderStyle.Fixed3D,
            'DrawMode': TreeViewDrawMode.Normal,
            'HideSelection': True,
            'HotTracking': False,
            'ImageKey': "",
            'SelectedImageKey': "",
            'Indent': 19,
            'ItemHeight': -1,
            'LineColor': None, # Color.Black
            'RightToLeft': RightToLeft.No,
            'RightToLeftLayout': False,
            'Scrollable': True,
            'ShowNodeToolTips': False,
            'Sorted': False,
            'StateImageList': None,
            'VisibleCount': 0 # Read-only usually
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Window", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Window")
        
        # Resolve Tkinter widget and save parent container
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Save parent container for auto-registration
        self._parent_container = parent_container
        
        self.Name = defaults['Name']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        
        self._node_map = {} # Map Tkinter IID -> TreeNode
        self.Nodes = TreeNodeCollection(self) # Root nodes
        
        self.ImageList = defaults['ImageList']
        self.ImageIndex = defaults['ImageIndex']
        self.SelectedImageIndex = defaults['SelectedImageIndex']
        self.FullRowSelect = defaults['FullRowSelect']
        self.CheckBoxes = defaults['CheckBoxes']
        self.ShowLines = defaults['ShowLines']
        self.ShowPlusMinus = defaults['ShowPlusMinus']
        self.ShowRootLines = defaults['ShowRootLines']
        self.PathSeparator = defaults['PathSeparator']
        self.LabelEdit = defaults['LabelEdit']
        self.Font = defaults['Font']
        self.ForeColor = defaults['ForeColor']
        self.BackColor = defaults['BackColor']
        
        # New Properties
        self.BackgroundImage = defaults['BackgroundImage']
        self.BackgroundImageLayout = defaults['BackgroundImageLayout']
        self.BorderStyle = defaults['BorderStyle']
        self.DrawMode = defaults['DrawMode']
        self.HideSelection = defaults['HideSelection']
        self.HotTracking = defaults['HotTracking']
        self.ImageKey = defaults['ImageKey']
        self.SelectedImageKey = defaults['SelectedImageKey']
        self.Indent = defaults['Indent']
        self.ItemHeight = defaults['ItemHeight']
        self.LineColor = defaults['LineColor']
        self.RightToLeft = defaults['RightToLeft']
        self.RightToLeftLayout = defaults['RightToLeftLayout']
        self.Scrollable = defaults['Scrollable']
        self.ShowNodeToolTips = defaults['ShowNodeToolTips']
        self.Sorted = defaults['Sorted']
        self.StateImageList = defaults['StateImageList']
        self.TreeViewNodeSorter = None
        
        # VB Events
        self.AfterSelect = lambda sender, e: None
        self.BeforeSelect = lambda sender, e: None
        self.AfterCheck = lambda sender, e: None
        self.BeforeCheck = lambda sender, e: None
        self.AfterExpand = lambda sender, e: None
        self.BeforeExpand = lambda sender, e: None
        self.AfterCollapse = lambda sender, e: None
        self.BeforeCollapse = lambda sender, e: None
        self.NodeMouseClick = lambda sender, e: None
        self.NodeMouseDoubleClick = lambda sender, e: None
        self.AfterLabelEdit = lambda sender, e: None
        self.BeforeLabelEdit = lambda sender, e: None
        self.DrawNode = lambda sender, e: None
        self.ItemDrag = lambda sender, e: None
        self.NodeMouseHover = lambda sender, e: None
        
        # Create Tkinter widget (Treeview)
        self._tk_widget = ttk.Treeview(self.master, show='tree')
        
        # Apply configurations
        style = ttk.Style()
        if self.Font:
            style.configure('Treeview', font=self.Font)
        if self.ForeColor:
            style.configure('Treeview', foreground=self.ForeColor)
        if self.BackColor:
            style.configure('Treeview', background=self.BackColor)
            style.configure('Treeview', fieldbackground=self.BackColor)
        
        self._place_control(self.Width, self.Height)
        
        # Bind events
        self._tk_widget.bind('<<TreeviewSelect>>', self._on_after_select)
        self._tk_widget.bind('<<TreeviewOpen>>', self._on_after_expand)
        self._tk_widget.bind('<<TreeviewClose>>', self._on_after_collapse)
        self._tk_widget.bind('<Button-1>', self._on_node_mouse_click)
        self._tk_widget.bind('<Double-1>', self._on_node_mouse_double_click)
        
        # Add initial nodes if provided in defaults
        initial_nodes = defaults['Nodes']
        if initial_nodes:
            for node in initial_nodes:
                self.Nodes.Add(node)
        
        # Auto-register with parent container if necessary
        self._auto_register_with_parent()
    
    @property
    def TopNode(self):
        """Gets the first fully visible tree node in the tree view control."""
        # Tkinter doesn't expose this directly easily, returning first node for now
        if len(self.Nodes) > 0:
            return self.Nodes[0]
        return None

    @property
    def VisibleCount(self):
        """Gets the number of tree nodes that can be fully visible in the tree view control."""
        # Estimate based on height and font?
        return 10 # Placeholder

    @property
    def SelectedNode(self):
        """Gets or sets the selected node."""
        selection = self._tk_widget.selection()
        if selection:
            return self._node_map.get(selection[0])
        return None
    
    @SelectedNode.setter
    def SelectedNode(self, node):
        if node and node.TreeView == self and node._id:
            self._tk_widget.selection_set(node._id)
            self._tk_widget.see(node._id)
        elif node is None:
            if self._tk_widget.selection():
                self._tk_widget.selection_remove(self._tk_widget.selection())

    def BeginUpdate(self):
        """Disables any redrawing of the tree view."""
        pass

    def EndUpdate(self):
        """Enables the redrawing of the tree view."""
        pass

    def GetNodeAt(self, x, y):
        """Gets the node at the specified coordinates."""
        item_id = self._tk_widget.identify_row(y)
        return self._node_map.get(item_id)

    def GetNodeCount(self, includeSubTrees):
        """Retrieves the number of tree nodes, optionally including those in all subtrees."""
        count = len(self.Nodes)
        if includeSubTrees:
            for node in self.Nodes:
                count += node.GetNodeCount(True)
        return count

    def HitTest(self, x, y):
        """Provides node information given x and y coordinates."""
        node = self.GetNodeAt(x, y)
        # Return simplified info
        return {'Node': node, 'Location': 'Label' if node else 'None'}

    def Sort(self):
        """Sorts the items in the TreeView control."""
        # Basic sort by text
        self._sort_nodes(self.Nodes)
        
    def _sort_nodes(self, nodes):
        # This would require re-ordering in UI which is complex in Tkinter without clearing/re-adding
        # For now, just a placeholder or we could implement a simple sort
        pass

    def ExpandAll(self):
        """Expands all nodes."""
        for node in self.Nodes:
            node.Expand()
            self._expand_recursive(node)
            
    def _expand_recursive(self, node):
        for child in node.Nodes:
            child.Expand()
            self._expand_recursive(child)

    def CollapseAll(self):
        """Collapses all nodes."""
        for node in self.Nodes:
            node.Collapse()
            # No need to recurse for collapse usually, but good for state consistency
            self._collapse_recursive(node)

    def _collapse_recursive(self, node):
        for child in node.Nodes:
            child.Collapse()
            self._collapse_recursive(child)

    def _add_node_to_ui(self, node, parent_owner):
        """Internal method to add a node to the Tkinter widget."""
        parent_id = ''
        if isinstance(parent_owner, TreeNode):
            parent_id = parent_owner._id
            
        # Insert into Tkinter
        node._id = self._tk_widget.insert(parent_id, 'end', text=node.Text, open=False)
        self._node_map[node._id] = node
        
        # Recursively add children
        for child in node.Nodes:
            child.TreeView = self
            child.Parent = node
            self._add_node_to_ui(child, node)

    def _insert_node_to_ui(self, node, parent_owner, index):
        """Internal method to insert a node to the Tkinter widget at a specific index."""
        parent_id = ''
        if isinstance(parent_owner, TreeNode):
            parent_id = parent_owner._id
            
        # Insert into Tkinter at specific index
        node._id = self._tk_widget.insert(parent_id, index, text=node.Text, open=False)
        self._node_map[node._id] = node
        
        # Recursively add children
        for child in node.Nodes:
            child.TreeView = self
            child.Parent = node
            self._add_node_to_ui(child, node)

    def _remove_node_from_ui(self, node):
        """Internal method to remove a node from the Tkinter widget."""
        if node._id:
            # Remove from map (including children)
            self._remove_from_map_recursive(node)
            self._tk_widget.delete(node._id)
            node._id = None

    def _remove_from_map_recursive(self, node):
        if node._id in self._node_map:
            del self._node_map[node._id]
        for child in node.Nodes:
            self._remove_from_map_recursive(child)

    def _on_after_select(self, event):
        """Handler for AfterSelect event."""
        node = self.SelectedNode
        if node:
            self.AfterSelect(self, {'Node': node, 'Action': TreeViewAction.ByMouse})
    
    def _on_after_expand(self, event):
        """Handler for AfterExpand event."""
        # Tkinter doesn't give the item in event easily for Open/Close, use focus or selection
        # But for Open/Close, the item might not be selected.
        # We can try to find which item changed state? 
        # Actually, Tkinter 8.6 sends the item id in the event detail or we can query.
        # A common workaround is using focus() or selection() but it's not guaranteed.
        # However, for '<<TreeviewOpen>>', the focused item is usually the one expanded.
        item_id = self._tk_widget.focus()
        node = self._node_map.get(item_id)
        if node:
            self.AfterExpand(self, {'Node': node})
    
    def _on_after_collapse(self, event):
        """Handler for AfterCollapse event."""
        item_id = self._tk_widget.focus()
        node = self._node_map.get(item_id)
        if node:
            self.AfterCollapse(self, {'Node': node})
    
    def _on_node_mouse_click(self, event):
        """Handler for NodeMouseClick event."""
        item_id = self._tk_widget.identify_row(event.y)
        node = self._node_map.get(item_id)
        if node:
            self.NodeMouseClick(self, {'Node': node, 'Button': event.num, 'X': event.x, 'Y': event.y})
    
    def _on_node_mouse_double_click(self, event):
        """Handler for NodeMouseDoubleClick event."""
        item_id = self._tk_widget.identify_row(event.y)
        node = self._node_map.get(item_id)
        if node:
            self.NodeMouseDoubleClick(self, {'Node': node, 'Button': event.num, 'X': event.x, 'Y': event.y})
    
    def _find_node_by_id(self, item_id):
        """Finds TreeNode by item_id."""
        return self._node_map.get(item_id)


class TreeViewAction(Enum):
    Unknown = 0
    ByKeyboard = 1
    ByMouse = 2
    Collapse = 3
    Expand = 4


class DataColumn:
    """Represents the schema of a column in a DataTable."""
    def __init__(self, column_name, data_type=str, caption=None):
        self.ColumnName = column_name
        self.DataType = data_type
        self.Caption = caption or column_name


class DataColumnCollection:
    """Represents a collection of DataColumn objects for a DataTable."""
    def __init__(self, table):
        self.table = table
        self._columns = []

    def Add(self, column_name, data_type=str):
        col = DataColumn(column_name, data_type)
        self._columns.append(col)
        return col
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return self._columns[key]
        for col in self._columns:
            if col.ColumnName == key:
                return col
        return None

    def __iter__(self):
        return iter(self._columns)
    
    def __len__(self):
        return len(self._columns)


class DataRow:
    """Represents a row of data in a DataTable."""
    def __init__(self, table, data=None):
        self.Table = table
        self._data = data if data is not None else {}

    def __getitem__(self, key):
        # Access by column name or index
        if isinstance(key, int):
            col_name = self.Table.Columns[key].ColumnName
            return self._data.get(col_name)
        return self._data.get(key)

    def __setitem__(self, key, value):
        if isinstance(key, int):
            col_name = self.Table.Columns[key].ColumnName
            self._data[col_name] = value
        else:
            self._data[key] = value


class DataRowCollection:
    """Represents a collection of rows for a DataTable."""
    def __init__(self, table):
        self.table = table
        self._rows = []

    def Add(self, *values):
        data = {}
        # Handle list/tuple passed as single arg
        if len(values) == 1 and isinstance(values[0], (list, tuple)):
            vals = values[0]
            for i, col in enumerate(self.table.Columns):
                if i < len(vals):
                    data[col.ColumnName] = vals[i]
        # Handle dict passed as single arg
        elif len(values) == 1 and isinstance(values[0], dict):
            data = values[0]
        # Handle individual args
        else:
            for i, col in enumerate(self.table.Columns):
                if i < len(values):
                    data[col.ColumnName] = values[i]
        
        row = DataRow(self.table, data)
        self._rows.append(row)
        return row

    def Clear(self):
        self._rows.clear()

    def __getitem__(self, index):
        return self._rows[index]

    def __iter__(self):
        return iter(self._rows)

    def __len__(self):
        return len(self._rows)


class DataTable:
    """Represents one table of in-memory data."""
    def __init__(self, table_name="Table1"):
        self.TableName = table_name
        self.Columns = DataColumnCollection(self)
        self.Rows = DataRowCollection(self)

    def NewRow(self):
        return DataRow(self)


class DataSet:
    """Represents an in-memory cache of data."""
    def __init__(self, data_set_name="NewDataSet"):
        self.DataSetName = data_set_name
        self.Tables = []


class DataGridViewCell:
    """Represents a cell in a DataGridView."""
    def __init__(self, value=None):
        self.Value = value
        self.Tag = None
        self.Style = None
        self.ToolTipText = ""
        self.RowIndex = -1
        self.ColumnIndex = -1
        self.OwningRow = None
        self.OwningColumn = None


class DataGridViewRow:
    """Represents a row in a DataGridView."""
    def __init__(self):
        self.Cells = []
        self.Tag = None
        self.Index = -1
        self.DataGridView = None
        self.Height = 22
        self.Visible = True
        self.Selected = False
        self._data_bound_item = None # For data binding

    @property
    def DataBoundItem(self):
        return self._data_bound_item

    def CreateCells(self, data_grid_view, values=None):
        """Creates cells based on the columns of the DataGridView."""
        self.DataGridView = data_grid_view
        self.Cells = []
        for col in data_grid_view.Columns:
            cell = DataGridViewCell()
            cell.OwningColumn = col
            cell.OwningRow = self
            self.Cells.append(cell)
        
        if values:
            for i, val in enumerate(values):
                if i < len(self.Cells):
                    self.Cells[i].Value = val


class DataGridViewRowCollection:
    """Collection of DataGridViewRows."""
    def __init__(self, owner):
        self.owner = owner # DataGridView
        self._list = []

    def Add(self, *values):
        """Adds a new row to the collection."""
        row = DataGridViewRow()
        
        # Handle different input types
        if len(values) == 1 and isinstance(values[0], DataGridViewRow):
            row = values[0]
        elif len(values) == 1 and isinstance(values[0], (list, tuple)):
             row.CreateCells(self.owner, values[0])
        elif len(values) > 0:
             row.CreateCells(self.owner, values)
        else:
             row.CreateCells(self.owner) # Empty row

        self._list.append(row)
        row.Index = len(self._list) - 1
        row.DataGridView = self.owner
        
        # Update UI
        self.owner._add_row_to_ui(row)
        return row.Index

    def Clear(self):
        """Removes all rows."""
        self._list.clear()
        self.owner._clear_rows_ui()

    def __getitem__(self, index):
        return self._list[index]

    def __len__(self):
        return len(self._list)
    
    def __iter__(self):
        return iter(self._list)


class DataGridViewColumnCollection:
    """Collection of DataGridViewColumns."""
    def __init__(self, owner):
        self.owner = owner
        self._list = []

    def Add(self, column_or_name, header_text=None):
        """Adds a column."""
        if isinstance(column_or_name, DataGridViewColumn):
            col = column_or_name
        else:
            col = DataGridViewColumn(Name=column_or_name, HeaderText=header_text or column_or_name)
            
        self._list.append(col)
        col.Index = len(self._list) - 1
        col.DataGridView = self.owner
        
        # Update UI if columns are already generated
        self.owner._apply_columns()
        return col.Index

    def Clear(self):
        self._list.clear()
        self.owner._apply_columns()

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._list[key]
        elif isinstance(key, str):
            for col in self._list:
                if col.Name == key:
                    return col
            return None
        return None

    def __len__(self):
        return len(self._list)

    def __iter__(self):
        return iter(self._list)


class DataGridViewColumn:
    """
    Represents a column in DataGridView.
    
    Usage - Option 1: col = DataGridViewColumn(); col.Name = "col1"; col.HeaderText = "Column 1"
    Usage - Option 2: col = DataGridViewColumn({'Name': 'col1', 'HeaderText': 'Column 1', 'Width': 150})
    """
    
    def __init__(self, props=None, **kwargs):
        defaults = {
            'Name': "",
            'HeaderText': "",
            'DataPropertyName': "",
            'Width': 100,
            'Visible': True,
            'ReadOnly': False
        }
        
        if props:
            defaults.update(props)
        if kwargs:
            defaults.update(kwargs)
        
        self.Name = defaults['Name']
        self.HeaderText = defaults['HeaderText']
        self.DataPropertyName = defaults['DataPropertyName']
        self.Width = defaults['Width']
        self.Visible = defaults['Visible']
        self.ReadOnly = defaults['ReadOnly']
        self.DisplayIndex = 0
        self.DefaultCellStyle = {}
        self.SortMode = "Automatic"
        self.ValueType = str
        self.CellTemplate = None
        self.Frozen = False
        self.AutoSizeMode = "None"
        self.DataGridView = None
        self.Index = -1


class DataGridView(ControlBase):
    """
    Represents a DataGridView with VB.NET properties.
    
    Usage - Option 1 (property assignment):
        grid = DataGridView(form)
        grid.Left = 10
        grid.Top = 10
        grid.Width = 500
        grid.Height = 300
        grid.DataSource = data_list
    
    Usage - Option 2 (dictionary):
        grid = DataGridView(form, {'Left': 10, 'Top': 10, 'Width': 500, 'DataSource': data_list})
    """
    
    def __init__(self, master_form, props=None):
        defaults = {
            'Left': 10,
            'Top': 10,
            'Width': 400,
            'Height': 200,
            'Name': "",
            'DataSource': None,
            'Columns': None,
            'AllowUserToAddRows': False,
            'AllowUserToDeleteRows': False,
            'AllowUserToResizeColumns': True,
            'ReadOnly': False,
            'SelectionMode': DataGridViewSelectionMode.FullRowSelect,
            'DefaultCellStyle': None,
            'AutoGenerateColumns': True,
            'AlternatingRowsDefaultCellStyle': None,
            'RowHeadersVisible': True,
            'ColumnHeadersVisible': True,
            'Dock': None,
            'Anchor': None
        }
        
        if props:
            defaults.update(props)
        
        # Resolve Tkinter widget and save parent container
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Save parent container for auto-registration
        self._parent_container = parent_container
        
        self.Name = defaults['Name']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        
        self._columns = DataGridViewColumnCollection(self)
        self._rows = DataGridViewRowCollection(self)
        self._datasource = None
        
        # Initial Columns from props
        if defaults['Columns']:
            for col in defaults['Columns']:
                if isinstance(col, str):
                    self._columns.Add(col, col)
                else:
                    self._columns.Add(col)

        self._allow_user_to_add_rows = defaults['AllowUserToAddRows']
        self._allow_user_to_delete_rows = defaults['AllowUserToDeleteRows']
        self.AllowUserToResizeColumns = defaults['AllowUserToResizeColumns']
        self._readonly = defaults['ReadOnly']
        self._selection_mode = defaults['SelectionMode']  # 'FullRowSelect', 'CellSelect', etc.
        self.DefaultCellStyle = defaults['DefaultCellStyle'] or {}
        self.AutoGenerateColumns = defaults['AutoGenerateColumns']
        self.AlternatingRowsDefaultCellStyle = defaults['AlternatingRowsDefaultCellStyle'] or {}
        self.RowHeadersVisible = defaults['RowHeadersVisible']
        self._column_headers_visible = defaults['ColumnHeadersVisible']
        
        # VB Events
        self.CellClick = lambda sender, e: None
        self.CellContentClick = lambda sender, e: None
        self.SelectionChanged = lambda sender, e: None
        self.UserAddedRow = lambda sender, e: None
        self.UserDeletedRow = lambda sender, e: None
        
        show = 'headings' if self._column_headers_visible else 'tree'
        selectmode = 'browse' if self._selection_mode == DataGridViewSelectionMode.FullRowSelect else 'extended'
        self._tk_widget = ttk.Treeview(self.master, show=show, selectmode=selectmode, height=10)
        
        # Configure columns and datasource
        self.DataSource = defaults['DataSource']
        
        self._place_control(self.Width, self.Height)
        
        # Bind events
        self._bind_common_events()
        self._tk_widget.bind('<<TreeviewSelect>>', self._on_selection_changed)
        self._tk_widget.bind('<Button-1>', self._on_click)
        self._tk_widget.bind('<Double-1>', self._on_double_click)
        
        # Apply Dock and Anchor if specified in props
        if 'Dock' in defaults and defaults['Dock']:
            self.Dock = defaults['Dock']
        if 'Anchor' in defaults and defaults['Anchor']:
            self.Anchor = defaults['Anchor']
        
        # Auto-register with parent container if necessary
        self._auto_register_with_parent()
    
    @property
    def Columns(self):
        return self._columns
        
    @property
    def Rows(self):
        return self._rows

    @property
    def DataSource(self):
        return self._datasource

    @DataSource.setter
    def DataSource(self, value):
        self._datasource = value
        self.Rows.Clear()
        self.Columns.Clear()
        
        if value:
            if self.AutoGenerateColumns:
                self._generate_columns_from_datasource()
            self._populate_from_datasource()

    @property
    def AllowUserToAddRows(self):
        return self._allow_user_to_add_rows

    @AllowUserToAddRows.setter
    def AllowUserToAddRows(self, value):
        self._allow_user_to_add_rows = value

    @property
    def AllowUserToDeleteRows(self):
        return self._allow_user_to_delete_rows

    @AllowUserToDeleteRows.setter
    def AllowUserToDeleteRows(self, value):
        self._allow_user_to_delete_rows = value

    @property
    def ReadOnly(self):
        return self._readonly

    @ReadOnly.setter
    def ReadOnly(self, value):
        self._readonly = value

    @property
    def ColumnHeadersVisible(self):
        return self._column_headers_visible

    @ColumnHeadersVisible.setter
    def ColumnHeadersVisible(self, value):
        self._column_headers_visible = value
        show = 'headings' if value else 'tree'
        self._tk_widget.config(show=show)

    @property
    def SelectionMode(self):
        return self._selection_mode

    @SelectionMode.setter
    def SelectionMode(self, value):
        self._selection_mode = value
        selectmode = 'browse' if value == DataGridViewSelectionMode.FullRowSelect else 'extended'
        self._tk_widget.config(selectmode=selectmode)

    @property
    def CurrentRow(self):
        """Gets the row containing the current cell."""
        selection = self._tk_widget.selection()
        if selection:
            try:
                index = self._tk_widget.index(selection[0])
                if 0 <= index < len(self.Rows):
                    return self.Rows[index]
            except:
                pass
        return None

    @property
    def SelectedRows(self):
        """Gets the collection of selected rows."""
        selected = []
        for item_id in self._tk_widget.selection():
            try:
                index = self._tk_widget.index(item_id)
                if 0 <= index < len(self.Rows):
                    selected.append(self.Rows[index])
            except:
                pass
        return selected

    def _generate_columns_from_datasource(self):
        """Automatically generates columns from DataSource."""
        if isinstance(self.DataSource, list) and self.DataSource:
            sample = self.DataSource[0]
            if isinstance(sample, dict):
                for key in sample.keys():
                    self.Columns.Add(key, key) # Name, HeaderText
                    self.Columns[key].DataPropertyName = key
            else:
                # Try to get attributes from object
                for key in dir(sample):
                    if not key.startswith('_') and not callable(getattr(sample, key)):
                        self.Columns.Add(key, key)
                        self.Columns[key].DataPropertyName = key
        elif isinstance(self.DataSource, DataTable):
            for col in self.DataSource.Columns:
                self.Columns.Add(col.ColumnName, col.Caption)
                self.Columns[col.ColumnName].DataPropertyName = col.ColumnName
        elif isinstance(self.DataSource, DataSet):
            if self.DataSource.Tables:
                table = self.DataSource.Tables[0]
                for col in table.Columns:
                    self.Columns.Add(col.ColumnName, col.Caption)
                    self.Columns[col.ColumnName].DataPropertyName = col.ColumnName

    def _apply_columns(self):
        """Applies columns to Treeview."""
        col_ids = [col.Name for col in self.Columns if col.Visible]
        self._tk_widget.config(columns=col_ids)
        for col in self.Columns:
            if col.Visible:
                self._tk_widget.heading(col.Name, text=col.HeaderText)
                self._tk_widget.column(col.Name, width=col.Width)
    
    def _populate_from_datasource(self):
        """Populates rows from DataSource."""
        source = self.DataSource
        
        # Handle DataSet (use first table)
        if isinstance(source, DataSet):
            if source.Tables:
                source = source.Tables[0]
            else:
                return

        # Handle DataTable
        if isinstance(source, DataTable):
            for row in source.Rows:
                values = []
                for col in self.Columns:
                    if col.Visible:
                        val = row[col.DataPropertyName] if col.DataPropertyName else None
                        values.append(str(val) if val is not None else "")
                
                self.Rows.Add(values)
                self.Rows[len(self.Rows)-1]._data_bound_item = row
            return

        # Handle List
        if isinstance(source, list):
            for item in source:
                values = []
                if isinstance(item, dict):
                    for col in self.Columns:
                        if col.Visible:
                            values.append(item.get(col.DataPropertyName, ''))
                else:
                    for col in self.Columns:
                        if col.Visible:
                            val = getattr(item, col.DataPropertyName, '')
                            values.append(val)
                
                self.Rows.Add(values)
                self.Rows[len(self.Rows)-1]._data_bound_item = item

    def _add_row_to_ui(self, row):
        """Internal method to add a row to Tkinter widget."""
        values = [cell.Value for cell in row.Cells]
        self._tk_widget.insert('', 'end', values=values)

    def _clear_rows_ui(self):
        """Internal method to clear rows from Tkinter widget."""
        for i in self._tk_widget.get_children():
            self._tk_widget.delete(i)

    def _on_selection_changed(self, event):
        """Handler for SelectionChanged."""
        self.SelectionChanged(self, {})

    def _on_click(self, event):
        """Handler for Click/CellClick."""
        item_id = self._tk_widget.identify_row(event.y)
        col_id = self._tk_widget.identify_column(event.x)
        
        if item_id and col_id:
            # Convert col_id '#1' to index
            col_index = int(col_id.replace('#', '')) - 1
            row_index = self._tk_widget.index(item_id)
            
            if 0 <= row_index < len(self.Rows) and 0 <= col_index < len(self.Columns):
                self.CellClick(self, {'RowIndex': row_index, 'ColumnIndex': col_index})

    def _on_double_click(self, event):
        pass


class ToolStripItem:
    """Base class for items in a ToolStrip or StatusStrip."""
    def __init__(self):
        self._text = ""
        self._image = None
        self._visible = True
        self._enabled = True
        self._alignment = "Left"  # 'Left', 'Right'
        self._spring = False
        self._tag = None
        self._name = ""
        self._width = None  # Auto
        self._back_color = None
        self._fore_color = None
        self._font = None
        self._tooltip_text = ""
        
        self._owner = None
        self._widget = None
        
        self.Click = lambda sender, e: None

    @property
    def Text(self): return self._text
    @Text.setter
    def Text(self, value):
        self._text = value
        self._update_widget()

    @property
    def Image(self): return self._image
    @Image.setter
    def Image(self, value):
        self._image = value
        self._update_widget()

    @property
    def Visible(self): return self._visible
    @Visible.setter
    def Visible(self, value):
        self._visible = value
        if self._owner: self._owner._update_layout()

    @property
    def Enabled(self): return self._enabled
    @Enabled.setter
    def Enabled(self, value):
        self._enabled = value
        self._update_widget()

    @property
    def Alignment(self): return self._alignment
    @Alignment.setter
    def Alignment(self, value):
        self._alignment = value
        if self._owner: self._owner._update_layout()

    @property
    def Spring(self): return self._spring
    @Spring.setter
    def Spring(self, value):
        self._spring = value
        if self._owner: self._owner._update_layout()

    @property
    def Tag(self): return self._tag
    @Tag.setter
    def Tag(self, value): self._tag = value

    @property
    def Name(self): return self._name
    @Name.setter
    def Name(self, value): self._name = value

    def _create_widget(self, parent):
        """Creates the widget. Must be overridden."""
        pass

    def _update_widget(self):
        """Updates the widget properties."""
        pass

    def _add_to_menu(self, menu):
        """Adds this item to a tk.Menu."""
        pass


class ToolStripButton(ToolStripItem):
    """Represents a selectable button in a ToolStrip."""
    def __init__(self, text="", image=None, onClick=None, name=""):
        super().__init__()
        self.Text = text
        self.Image = image
        self.Name = name
        if onClick:
            self.Click = onClick
        self._display_style = "ImageAndText" # None, Text, Image, ImageAndText
        self._checked = False
        self._check_on_click = False
        
    @property
    def Checked(self): return self._checked
    @Checked.setter
    def Checked(self, value):
        self._checked = value
        self._update_widget()
        
    @property
    def CheckOnClick(self): return self._check_on_click
    @CheckOnClick.setter
    def CheckOnClick(self, value): self._check_on_click = value

    @property
    def DisplayStyle(self): return self._display_style
    @DisplayStyle.setter
    def DisplayStyle(self, value):
        self._display_style = value
        self._update_widget()

    def _create_widget(self, parent):
        self._widget = tk.Button(
            parent,
            text=self.Text,
            relief='flat',
            bg=parent.cget('bg'),
            bd=0,
            padx=4,
            pady=2,
            compound='left'
        )
        if self.Image:
            self._widget.config(image=self.Image)
            
        self._widget.bind('<Button-1>', self._on_click)
        self._widget.bind('<Enter>', self._on_mouse_enter)
        self._widget.bind('<Leave>', self._on_mouse_leave)
        
        self._update_widget()
        return self._widget

    def _on_click(self, event):
        if self.CheckOnClick:
            self.Checked = not self.Checked
        self.Click(self, event)

    def _on_mouse_enter(self, event):
        if self.Enabled:
            self._widget.config(relief='raised', bg='#e5f1fb') # Light blue hover

    def _on_mouse_leave(self, event):
        if self.Enabled and not self.Checked:
            self._widget.config(relief='flat', bg=self._owner._tk_widget.cget('bg') if self._owner else 'SystemButtonFace')
        elif self.Checked:
             self._widget.config(relief='sunken', bg='#cce8ff') # Checked state

    def _update_widget(self):
        if self._widget:
            # Handle DisplayStyle
            if self.DisplayStyle == "Text":
                self._widget.config(text=self.Text, image='')
            elif self.DisplayStyle == "Image":
                self._widget.config(text='', image=self.Image if self.Image else '')
            elif self.DisplayStyle == "ImageAndText":
                self._widget.config(text=self.Text, image=self.Image if self.Image else '')
            
            # Handle Checked state visual
            if self.Checked:
                self._widget.config(relief='sunken', bg='#cce8ff')
            else:
                self._widget.config(relief='flat', bg=self._owner._tk_widget.cget('bg') if self._owner else 'SystemButtonFace')

    def _add_to_menu(self, menu):
        # ToolStripButton in a menu acts like a command
        menu.add_command(label=self.Text, command=lambda: self._on_click(None), 
                         image=self.Image if self.Image else '',
                         compound='left')


class ToolStripLabel(ToolStripItem):
    """Represents a label in a ToolStrip."""
    def __init__(self, text="", image=None, isLink=False):
        super().__init__()
        self.Text = text
        self.Image = image
        self._is_link = isLink
        
    @property
    def IsLink(self): return self._is_link
    @IsLink.setter
    def IsLink(self, value):
        self._is_link = value
        self._update_widget()

    def _create_widget(self, parent):
        self._widget = tk.Label(
            parent,
            text=self.Text,
            bg=parent.cget('bg'),
            compound='left'
        )
        if self.Image:
            self._widget.config(image=self.Image)
            
        self._widget.bind('<Button-1>', lambda e: self.Click(self, e))
        self._update_widget()
        return self._widget

    def _update_widget(self):
        if self._widget:
            self._widget.config(text=self.Text)
            if self.Image: self._widget.config(image=self.Image)
            
            if self.IsLink:
                self._widget.config(fg='blue', cursor='hand2')
                try:
                    from tkinter import font
                    f = font.Font(font=self._widget.cget("font"))
                    f.configure(underline=True)
                    self._widget.config(font=f)
                except: pass
            else:
                self._widget.config(fg='black', cursor='')


class ToolStripSeparator(ToolStripItem):
    """Represents a separator in a ToolStrip."""
    def _create_widget(self, parent):
        self._widget = ttk.Separator(parent, orient='vertical')
        return self._widget

    def _add_to_menu(self, menu):
        menu.add_separator()


class ToolStripStatusLabel(ToolStripItem):
    """Represents a label in a StatusStrip."""
    def __init__(self, text=""):
        super().__init__()
        self.Text = text
        self._border_sides = "None"  # 'None', 'All', 'Bottom', 'Top', 'Left', 'Right'
        self._border_style = "Flat"  # 'Flat', 'Raised', 'Sunken', 'Etched', 'Bump', 'Adjust'
        
    @property
    def BorderSides(self): return self._border_sides
    @BorderSides.setter
    def BorderSides(self, value):
        self._border_sides = value
        self._update_widget()

    @property
    def BorderStyle(self): return self._border_style
    @BorderStyle.setter
    def BorderStyle(self, value):
        self._border_style = value
        self._update_widget()

    def _create_widget(self, parent):
        relief = 'flat'
        if self.BorderStyle == 'Sunken': relief = 'sunken'
        elif self.BorderStyle == 'Raised': relief = 'raised'
        
        bd = 1 if self.BorderStyle != 'Flat' else 0
        
        self._widget = tk.Label(
            parent,
            text=self.Text,
            relief=relief,
            borderwidth=bd,
            bg=parent.cget('bg')
        )
        if self.Image:
            self._widget.config(image=self.Image, compound='left')
            
        self._widget.bind('<Button-1>', lambda e: self.Click(self, e))
        return self._widget

    def _update_widget(self):
        if self._widget:
            self._widget.config(text=self.Text)
            if self.Image: self._widget.config(image=self.Image)

class ToolStripMenuItem(ToolStripItem):
    """Represents a selectable option displayed on a MenuStrip or ContextMenuStrip."""
    def __init__(self, text="", image=None, onClick=None, name=""):
        super().__init__()
        self.Text = text
        self.Image = image
        self.Name = name
        if onClick:
            self.Click = onClick
        
        self.DropDownItems = ToolStripItemCollection(self)
        self._shortcut_keys = None
        self._checked = False
        self._check_on_click = False
        self._shortcut_key_display_string = ""
        
    @property
    def Checked(self): return self._checked
    @Checked.setter
    def Checked(self, value):
        self._checked = value
        self._update_widget()
        
    @property
    def CheckOnClick(self): return self._check_on_click
    @CheckOnClick.setter
    def CheckOnClick(self, value): self._check_on_click = value

    @property
    def ShortcutKeys(self): return self._shortcut_keys
    @ShortcutKeys.setter
    def ShortcutKeys(self, value): self._shortcut_keys = value

    @property
    def ShortcutKeyDisplayString(self): return self._shortcut_key_display_string
    @ShortcutKeyDisplayString.setter
    def ShortcutKeyDisplayString(self, value): self._shortcut_key_display_string = value

    @property
    def HasDropDownItems(self):
        return len(self.DropDownItems) > 0

    def _create_widget(self, parent):
        # When on a MenuStrip, it looks like a label/button
        self._widget = tk.Label(
            parent,
            text=self.Text,
            bg=parent.cget('bg'),
            padx=5,
            pady=2,
            compound='left'
        )
        if self.Image:
            self._widget.config(image=self.Image)
            
        self._widget.bind('<Button-1>', self._on_click)
        self._widget.bind('<Enter>', self._on_mouse_enter)
        self._widget.bind('<Leave>', self._on_mouse_leave)
        
        self._update_widget()
        return self._widget

    def _on_click(self, event):
        if len(self.DropDownItems) > 0:
            self.ShowDropDown()
        else:
            if self.CheckOnClick:
                self.Checked = not self.Checked
            self.Click(self, event)

    def _on_mouse_enter(self, event):
        if self.Enabled:
            self._widget.config(bg='#cce8ff') # Light blue hover

    def _on_mouse_leave(self, event):
        if self.Enabled:
            self._widget.config(bg=self._owner._tk_widget.cget('bg') if self._owner else 'SystemButtonFace')

    def _update_widget(self):
        if self._widget:
            self._widget.config(text=self.Text)
            if self.Image: self._widget.config(image=self.Image)

    def ShowDropDown(self):
        if not self._widget: return
        
        menu = tk.Menu(self._widget, tearoff=0)
        for item in self.DropDownItems:
            item._add_to_menu(menu)
        
        x = self._widget.winfo_rootx()
        y = self._widget.winfo_rooty() + self._widget.winfo_height()
        menu.post(x, y)

    def _add_to_menu(self, menu):
        # Add self to a parent menu
        if len(self.DropDownItems) > 0:
            sub_menu = tk.Menu(menu, tearoff=0)
            for item in self.DropDownItems:
                item._add_to_menu(sub_menu)
            menu.add_cascade(label=self.Text, menu=sub_menu, image=self.Image if self.Image else '')
        else:
            # Checkbutton or command
            if self.CheckOnClick or self.Checked:
                 # We use a variable to set initial state
                 var = tk.BooleanVar(value=self.Checked)
                 menu.add_checkbutton(label=self.Text, command=lambda: self._menu_click(), 
                                      variable=var,
                                      image=self.Image if self.Image else '',
                                      compound='left')
                 # Keep reference to var to avoid garbage collection? 
                 # Actually menu keeps it? No, usually we need to keep it.
                 # But since menu is modal (post), maybe it's fine?
                 # Let's store it in self temporarily
                 self._temp_var = var
            else:
                menu.add_command(label=self.Text, command=lambda: self._menu_click(), 
                                 image=self.Image if self.Image else '',
                                 compound='left')

    def _menu_click(self):
        if self.CheckOnClick:
            self.Checked = not self.Checked
        self.Click(self, None)

class ToolStripProgressBar(ToolStripItem):
    """Represents a progress bar in a StatusStrip."""
    def __init__(self):
        super().__init__()
        self._value = 0
        self._maximum = 100
        self._style = "Blocks"  # 'Blocks', 'Continuous', 'Marquee'
        self._width = 100

    @property
    def Value(self): return self._value
    @Value.setter
    def Value(self, value):
        self._value = value
        self._update_widget()

    @property
    def Maximum(self): return self._maximum
    @Maximum.setter
    def Maximum(self, value):
        self._maximum = value
        self._update_widget()

    def _create_widget(self, parent):
        try:
            import tkinter.ttk as ttk
            self._widget = ttk.Progressbar(parent, maximum=self.Maximum, value=self.Value, length=self._width)
        except ImportError:
            self._widget = tk.Label(parent, text=f"Progress: {self.Value}%")
        
        self._widget.bind('<Button-1>', lambda e: self.Click(self, e))
        return self._widget

    def _update_widget(self):
        if self._widget:
            try:
                self._widget['value'] = self.Value
                self._widget['maximum'] = self.Maximum
            except:
                pass

class ToolStripItemCollection:
    def __init__(self, owner):
        self._owner = owner
        self._items = []

    def Add(self, item):
        if isinstance(item, str):
            # If owner is StatusStrip, create StatusLabel, otherwise ToolStripButton
            owner_type = type(self._owner).__name__
            if owner_type == 'StatusStrip':
                item = ToolStripStatusLabel(item)
            elif owner_type == 'MenuStrip' or owner_type == 'ToolStripMenuItem':
                item = ToolStripMenuItem(item)
            else:
                item = ToolStripButton(item)
                
        self._items.append(item)
        item._owner = self._owner
        # Only update layout if owner is a control (ToolStrip/StatusStrip/MenuStrip)
        # If owner is ToolStripMenuItem, we don't need to update layout of the item itself, 
        # but maybe the parent menu if it was open? For now, we check if _update_layout exists.
        if hasattr(self._owner, '_update_layout'):
            self._owner._update_layout()
        return item

    def AddRange(self, items):
        for item in items: self.Add(item)

    def Clear(self):
        self._items.clear()
        if hasattr(self._owner, '_update_layout'):
            self._owner._update_layout()

    def Remove(self, item):
        if item in self._items:
            self._items.remove(item)
            item._owner = None
            if hasattr(self._owner, '_update_layout'):
                self._owner._update_layout()

    def __getitem__(self, index): return self._items[index]
    def __len__(self): return len(self._items)
    def __iter__(self): return iter(self._items)


class ToolStrip(ControlBase):
    """
    Represents a toolbar that can contain buttons, labels, etc.
    """
    def __init__(self, master_form, props=None):
        defaults = {
            'Dock': 'Top',
            'GripStyle': 'Visible',
            'Height': 25,
            'Name': '',
            'Text': '',
            'Left': 0,
            'Top': 0,
            'Width': 300
        }
        if props: defaults.update(props)
        
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        self.Name = defaults['Name']
        self.Dock = defaults['Dock']
        self.Height = defaults['Height']
        self.Width = defaults['Width']
        
        self._items = ToolStripItemCollection(self)
        
        self._tk_widget = tk.Frame(
            self.master,
            bg='#f0f0f0', # System color usually
            height=self.Height
        )
        self._tk_widget.pack_propagate(False) # Maintain height
        
        # Initial placement
        if self.Dock:
            self._place_control()
        else:
            self._place_control(self.Width, self.Height)
            
        self._auto_register_with_parent()

    @property
    def Items(self): return self._items

    def _update_layout(self):
        # Re-pack all items
        for widget in self._tk_widget.winfo_children():
            widget.pack_forget()
            
        for item in self.Items:
            if item.Visible:
                if not item._widget:
                    item._create_widget(self._tk_widget)
                
                # Pack logic
                fill = 'none'
                expand = False
                padx = 2
                
                if isinstance(item, ToolStripSeparator):
                    fill = 'y'
                    padx = 6
                
                if item.Alignment == 'Right':
                    side = 'right'
                else:
                    side = 'left'
                    
                item._widget.pack(side=side, fill=fill, padx=padx, pady=2)


class MenuStrip(ToolStrip):
    """
    Represents a menu strip control.
    """
    def __init__(self, master_form, props=None):
        defaults = {
            'Dock': 'Top',
            'GripStyle': 'Hidden',
            'Height': 24,
            'Name': '',
            'Text': '',
            'Left': 0,
            'Top': 0,
            'Width': 300
        }
        if props: defaults.update(props)
        
        super().__init__(master_form, defaults)
        
        # MenuStrip specific styling
        # We might want to ensure it looks like a menu bar
        # But ToolStrip defaults are mostly fine, except maybe background color or border
        # self._tk_widget.config(bg='#f0f0f0') 

class StatusStrip(ControlBase):
    """
    Represents a Windows Status Strip control.
    """
    def __init__(self, master_form, props=None):
        defaults = {
            'Text': "",
            'Left': 0,
            'Top': 0,
            'Width': 300,
            'Height': 22,
            'Dock': 'Bottom',
            'SizingGrip': True,
            'ShowItemToolTips': True,
            'Name': ""
        }
        
        if props:
            defaults.update(props)
            
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        self._parent_container = parent_container
        self.Name = defaults['Name']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Dock = defaults['Dock']
        self.SizingGrip = defaults['SizingGrip']
        self.ShowItemToolTips = defaults['ShowItemToolTips']
        self.BackColor = 'SystemButtonFace'
        
        self.Items = ToolStripItemCollection(self)
        
        self._tk_widget = tk.Frame(
            self.master,
            bg=self.BackColor,
            height=self.Height,
            relief='flat'
        )
        
        # Left and Right frames for alignment
        self._left_frame = tk.Frame(self._tk_widget, bg=self.BackColor)
        self._left_frame.pack(side='left', fill='both', expand=True)
        
        self._right_frame = tk.Frame(self._tk_widget, bg=self.BackColor)
        self._right_frame.pack(side='right', fill='y')
        
        if self.SizingGrip:
            self._grip_canvas = tk.Canvas(
                self._tk_widget,
                width=12,
                height=self.Height,
                bg=self.BackColor,
                highlightthickness=0
            )
            self._grip_canvas.pack(side='right', fill='y')
            self._draw_sizing_grip()

        self._update_layout()
        
        if self.Dock and self.Dock != 'None':
            pass
        else:
             if hasattr(self, '_visible') and self._visible:
                self._place_control(self.Width, self.Height)

        self._auto_register_with_parent()

    def _update_layout(self):
        # Clear existing widgets
        for w in self._left_frame.winfo_children(): w.destroy()
        for w in self._right_frame.winfo_children(): w.destroy()
        
        # Separate items by alignment
        left_items = [i for i in self.Items if i.Alignment == 'Left']
        right_items = [i for i in self.Items if i.Alignment == 'Right']
        
        # Pack Left items
        for item in left_items:
            if not item.Visible: continue
            w = item._create_widget(self._left_frame)
            pack_opts = {'side': 'left', 'padx': 2, 'fill': 'y'}
            if item.Spring:
                pack_opts['expand'] = True
                pack_opts['fill'] = 'both'
            w.pack(**pack_opts)
            
        # Pack Right items
        for item in right_items:
            if not item.Visible: continue
            w = item._create_widget(self._right_frame)
            w.pack(side='left', padx=2, fill='y')

    def _draw_sizing_grip(self):
        canvas = self._grip_canvas
        h = self.Height
        for i in range(3):
            x = 9 - i * 4
            canvas.create_line(x, h-3, x+3, h-6, fill='gray', width=1)
            canvas.create_line(x+1, h-3, x+4, h-6, fill='white', width=1)


class TrackBar(ControlBase):
    """
    Represents a standard Windows track bar (slider).
    """
    def __init__(self, master_form, props=None):
        defaults = {
            'Minimum': 0,
            'Maximum': 10,
            'Value': 0,
            'Orientation': Orientation.Horizontal,
            'TickFrequency': 1,
            'SmallChange': 1,
            'LargeChange': 5,
            'TickStyle': TickStyle.BottomRight,
            'Left': 0, 'Top': 0, 'Width': 100, 'Height': 45,
            'Name': '', 'Enabled': True, 'Visible': True
        }
        if props: defaults.update(props)
        
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        self._parent_container = parent_container
        self.Name = defaults['Name']
        self._minimum = defaults['Minimum']
        self._maximum = defaults['Maximum']
        self._value = defaults['Value']
        self._orientation = defaults['Orientation']
        self._tick_frequency = defaults['TickFrequency']
        self._small_change = defaults['SmallChange']
        self._large_change = defaults['LargeChange']
        
        # Events
        self.Scroll = lambda sender, e: None
        self.ValueChanged = lambda sender, e: None
        
        orient = tk.HORIZONTAL if self._orientation == Orientation.Horizontal else tk.VERTICAL
        
        self._tk_widget = tk.Scale(
            self.master,
            from_=self._minimum,
            to=self._maximum,
            orient=orient,
            resolution=self._small_change,
            tickinterval=self._tick_frequency if defaults['TickStyle'] != TickStyle.None_ else 0,
            showvalue=0, 
            command=self._on_scroll
        )
        self._tk_widget.set(self._value)
        
        self._apply_visual_config()
        self._auto_register_with_parent()

    def _on_scroll(self, value):
        new_val = float(value)
        if self._value != new_val:
            self._value = new_val
            self.Scroll(self, None)
            self.ValueChanged(self, None)

    @property
    def Value(self):
        return int(self._tk_widget.get())
    
    @Value.setter
    def Value(self, val):
        self._tk_widget.set(val)
        self._value = val
        
    @property
    def Minimum(self):
        return self._minimum
        
    @Minimum.setter
    def Minimum(self, val):
        self._minimum = val
        self._tk_widget.config(from_=val)

    @property
    def Maximum(self):
        return self._maximum
        
    @Maximum.setter
    def Maximum(self, val):
        self._maximum = val
        self._tk_widget.config(to=val)
        
    @property
    def SmallChange(self):
        return self._small_change
        
    @SmallChange.setter
    def SmallChange(self, val):
        self._small_change = val
        self._tk_widget.config(resolution=val)


class MenuItem:
    """Represents an individual item that is displayed within a MainMenu or ContextMenu."""
    def __init__(self, text="", onClick=None, shortcut=None):
        self.Text = text
        self.Click = onClick if onClick else lambda sender, e: None
        self.MenuItems = [] # Sub items
        self.Checked = False
        self.Enabled = True
        self.Visible = True
        self.Shortcut = shortcut # e.g. "Ctrl+O"
        self.RadioCheck = False
        
    def PerformClick(self):
        if self.Enabled:
            self.Click(self, None)

class MainMenu:
    """Represents the menu structure of a form."""
    def __init__(self, items=None):
        self.MenuItems = items if items else []
        
    def GetForm(self):
        return None


class ToolStripTextBox(ToolStripItem):
    """Represents a text box in a ToolStrip or ContextMenuStrip."""
    def __init__(self, name=None):
        super().__init__()
        self.Name = name
        self.Text = ""
        # Not fully implemented for ContextMenu yet

class ToolStripComboBox(ToolStripItem):
    """Represents a combo box in a ToolStrip or ContextMenuStrip."""
    def __init__(self, name=None):
        super().__init__()
        self.Name = name
        self.Items = []
        # Not fully implemented for ContextMenu yet

class ContextMenuStrip:
    """Represents a shortcut menu."""
    def __init__(self, container=None):
        self.Items = []
        self.Name = None
        self.Tag = None
        self.Opening = lambda sender, e: None
        self.Closing = lambda sender, e: None
        self.Opened = lambda sender, e: None
        self.Closed = lambda sender, e: None
        
        # Internal Tkinter menu
        self._tk_menu = None
        self._target_control = None
        
    @property
    def SourceControl(self):
        """Gets the last control that caused this ContextMenuStrip to be displayed."""
        return self._target_control

    def Show(self, control, position=None):
        """Displays the shortcut menu at the specified position."""
        if not control or not control._tk_widget:
            return
            
        self._target_control = control
        
        # Create menu if needed
        self._rebuild_menu(control._tk_widget)
        
        # Trigger Opening event
        cancel_args = type('CancelEventArgs', (), {'Cancel': False})()
        self.Opening(self, cancel_args)
        if cancel_args.Cancel:
            return
            
        # Calculate position
        x, y = 0, 0
        if position:
            # Position is relative to control
            # Convert to screen coordinates
            try:
                x = control._tk_widget.winfo_rootx() + position.X
                y = control._tk_widget.winfo_rooty() + position.Y
            except:
                x = position.X
                y = position.Y
        else:
            # Default to mouse position
            x = control._tk_widget.winfo_pointerx()
            y = control._tk_widget.winfo_pointery()
            
        try:
            self._tk_menu.tk_popup(x, y)
            self.Opened(self, None)
        finally:
            pass

    def Close(self):
        """Closes the shortcut menu."""
        if self._tk_menu:
            self._tk_menu.unpost()
            self.Closed(self, None)

    def _rebuild_menu(self, master):
        """Rebuilds the Tkinter menu from Items."""
        if self._tk_menu:
            try:
                self._tk_menu.destroy()
            except:
                pass
            
        self._tk_menu = tk.Menu(master, tearoff=0)
        self._build_items(self._tk_menu, self.Items)
        
    def _build_items(self, menu, items):
        for item in items:
            if not item.Visible:
                continue
                
            if isinstance(item, ToolStripSeparator):
                menu.add_separator()
            elif isinstance(item, ToolStripMenuItem):
                if item.HasDropDownItems:
                    submenu = tk.Menu(menu, tearoff=0)
                    self._build_items(submenu, item.DropDownItems)
                    menu.add_cascade(label=item.Text, menu=submenu)
                else:
                    # Handle Checked
                    if item.Checked:
                        menu.add_checkbutton(label=item.Text, 
                                             command=lambda i=item: self._on_item_click(i),
                                             variable=tk.BooleanVar(value=True))
                    else:
                        menu.add_command(label=item.Text, 
                                         command=lambda i=item: self._on_item_click(i))
                                         
    def _on_item_click(self, item):
        if item.CheckOnClick:
            item.Checked = not item.Checked
        item.PerformClick()
        # Context menu usually closes on click


class Application:
    """
    Provides static methods and properties to manage an application.
    """
    @staticmethod
    def Run(main_form):
        """Begins running a standard application message loop on the current thread."""
        if hasattr(main_form, 'Show'):
            main_form.Show()
        
        # If main_form is a Form, it has a _root (tk.Tk or Toplevel)
        if hasattr(main_form, '_root'):
            main_form._root.mainloop()
        elif hasattr(main_form, '_tk_widget'):
             main_form._tk_widget.mainloop()
             
    @staticmethod
    def Exit():
        """Informs all message pumps that they must terminate."""
        import sys
        sys.exit()


class ErrorProvider:
    """
    Provides a user interface for indicating that a control on a form has an error associated with it.
    """
    def __init__(self, container_control=None):
        self.ContainerControl = container_control
        self.BlinkStyle = 'BlinkIfDifferentError' # 'BlinkIfDifferentError', 'AlwaysBlink', 'NeverBlink'
        self.BlinkRate = 250
        self._errors = {} # Map control -> error_message
        self._icons = {} # Map control -> icon_label
        self.Tag = None

    @property
    def Tag(self):
        """Gets or sets the object that contains data about the control."""
        return self._tag

    @Tag.setter
    def Tag(self, value):
        self._tag = value
        
    def SetError(self, control, value):
        """Sets the error description string for the specified control."""
        if not value:
            # Clear error
            if control in self._errors:
                del self._errors[control]
                if control in self._icons:
                    self._icons[control].destroy()
                    del self._icons[control]
        else:
            self._errors[control] = value
            self._show_error_icon(control, value)
            
    def GetError(self, control):
        return self._errors.get(control, "")
        
    def _show_error_icon(self, control, message):
        if control in self._icons:
            self._icons[control].destroy()
            
        # Create a small label with an exclamation mark or icon
        # Position it to the right of the control
        if hasattr(control, '_tk_widget'):
            widget = control._tk_widget
            parent = widget.master
            
            # We need to place it relative to the control. 
            # Since controls use place(), we can get their x, y, width
            x = control.Left + control.Width
            y = control.Top + (control.Height // 2) - 8
            
            # Ensure parent is a widget where we can place things
            try:
                icon = tk.Label(parent, text="!", fg="white", bg="red", font=("Arial", 8, "bold"), width=2)
                icon.place(x=x, y=y)
                
                # Tooltip for the error
                ToolTip(icon, {'Text': message, 'BgColor': '#ffcccc', 'FgColor': 'red'})
                
                self._icons[control] = icon
                
                # Blink logic if needed
                if self.BlinkStyle != 'NeverBlink':
                    self._blink(icon, 0)
            except:
                pass

    def _blink(self, icon, count):
        if not icon.winfo_exists(): return
        if count >= 6: # Blink 3 times
            icon.config(bg="red", fg="white")
            return
            
        current_bg = icon.cget("bg")
        new_bg = "white" if current_bg == "red" else "red"
        new_fg = "red" if current_bg == "red" else "white"
        
        icon.config(bg=new_bg, fg=new_fg)
        icon.after(self.BlinkRate, lambda: self._blink(icon, count + 1))

    def Clear(self):
        for icon in self._icons.values():
            icon.destroy()
        self._icons.clear()
        self._errors.clear()


############# Controls for Date-Time #############

class MonthCalendar(ControlBase):
    """
    Represents a MonthCalendar control (wraps tkcalendar.Calendar).
    """
    
    def __init__(self, master_form, props=None):
        # Internal state
        self._calendar = None
        self._styles = {}
        self._selection_start = datetime.now().date()
        self._selection_end = datetime.now().date()
        self._min_date = None
        self._max_date = None
        self._show_week_numbers = False
        self._first_day_of_week = Day.Default
        self._bolded_dates = []
        
        # Events
        self.DateChanged = lambda sender=None, e=None: None
        self.DateSelected = lambda sender=None, e=None: None
        self.MouseUp = lambda sender=None, e=None: None
        self.DoubleClick = lambda sender=None, e=None: None
        
        defaults = {
            'Left': 10, 'Top': 10, 'Width': 220, 'Height': 200, 'Name': "",
            'SelectionStart': datetime.now().date(),
            'SelectionEnd': datetime.now().date(),
            'MinDate': None,
            'MaxDate': None,
            'ShowWeekNumbers': False,
            'FirstDayOfWeek': Day.Default,
            # Styles
            'TitleBackColor': None, 'TitleForeColor': None, 'TrailingForeColor': None,
            'BackColor': None, 'ForeColor': None,
            'Locale': None,
            'HeadersBackground': None, 'HeadersForeground': None,
            'SelectBackground': None, 'SelectForeground': None,
            'WeekendBackground': None, 'WeekendForeground': None,
            'OtherMonthBackground': None, 'OtherMonthForeground': None,
            'OtherMonthWeekendBackground': None, 'OtherMonthWeekendForeground': None,
            'TooltipBackground': None, 'TooltipForeground': None,
            'TooltipAlpha': None, 'TooltipDelay': None
        }
        
        if props:
            defaults.update(props)
            
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        self._parent_container = parent_container
        
        self.Name = defaults['Name']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        
        self._selection_start = defaults['SelectionStart']
        self._selection_end = defaults['SelectionEnd']
        self._min_date = defaults['MinDate']
        self._max_date = defaults['MaxDate']
        self._show_week_numbers = defaults['ShowWeekNumbers']
        self._first_day_of_week = defaults['FirstDayOfWeek']
        
        # Store styles
        self._styles['background'] = defaults.get('BackColor')
        self._styles['foreground'] = defaults.get('ForeColor')
        self._styles['headersbackground'] = defaults.get('TitleBackColor') or defaults.get('HeadersBackground')
        self._styles['headersforeground'] = defaults.get('TitleForeColor') or defaults.get('HeadersForeground')
        self._styles['othermonthforeground'] = defaults.get('TrailingForeColor') or defaults.get('OtherMonthForeground')
        
        # Direct styles
        for key in ['Locale', 'SelectBackground', 'SelectForeground', 
                   'WeekendBackground', 'WeekendForeground', 'OtherMonthBackground', 
                   'OtherMonthWeekendBackground', 'OtherMonthWeekendForeground',
                   'TooltipBackground', 'TooltipForeground', 'TooltipAlpha', 'TooltipDelay']:
             if defaults.get(key) is not None:
                 self._styles[key.lower()] = defaults[key]

        self._create_control()
        self._auto_register_with_parent()

    def _create_control(self):
        if install_library("tkcalendar"):
            try:
                from tkcalendar import Calendar
                options = {
                    'selectmode': 'day',
                    'year': self._selection_start.year,
                    'month': self._selection_start.month,
                    'day': self._selection_start.day,
                    'mindate': self._min_date,
                    'maxdate': self._max_date,
                    'showweeknumbers': self._show_week_numbers
                }
                
                if self._first_day_of_week == Day.Sunday:
                    options['firstweekday'] = 'sunday'
                elif self._first_day_of_week == Day.Monday:
                    options['firstweekday'] = 'monday'
                
                valid_styles = {k: v for k, v in self._styles.items() if v is not None}
                options.update(valid_styles)
                
                self._calendar = Calendar(self.master, **options)
                self._tk_widget = self._calendar
                
                self._calendar.bind('<<CalendarSelected>>', self._on_date_changed)
                self._calendar.bind('<ButtonRelease-1>', self._on_mouse_up)
                self._calendar.bind('<Double-1>', self._on_double_click)
                
            except ImportError:
                self._create_fallback()
        else:
            self._create_fallback()
            
        self._place_control(self.Width, self.Height)

    def _create_fallback(self):
        self._tk_widget = tk.Label(self.master, text="Install tkcalendar", bg='white', relief='sunken')
        
    def _on_date_changed(self, event):
        try:
            selected_date = self._calendar.selection_get()
            self._selection_start = selected_date
            self._selection_end = selected_date
            
            self.DateChanged(self, {'Start': selected_date, 'End': selected_date})
            self.DateSelected(self, {'Start': selected_date, 'End': selected_date})
        except:
            pass

    def _on_mouse_up(self, event):
        self.MouseUp(self, {'Button': event.num, 'X': event.x, 'Y': event.y})
        
    def _on_double_click(self, event):
        self.DoubleClick()

    def _update_style(self, option, value):
        self._styles[option] = value
        if self._calendar:
            try:
                self._calendar.configure(**{option: value})
            except Exception as e:
                print(f"Error updating style {option}: {e}")

    def AddBoldedDate(self, date):
        """Adds a date to be displayed in bold."""
        if self._calendar:
            self._calendar.calevent_create(date, 'bold', 'bold')
            # Configure tag if not already configured (or re-configure)
            # Note: font handling might need improvement to merge with existing font
            self._calendar.tag_config('bold', background='#e0e0e0') 
            self._bolded_dates.append(date)

    def RemoveBoldedDate(self, date):
        """Removes a bolded date."""
        # tkcalendar doesn't easily support removing specific events by date without ID
        pass 

    def RemoveAllBoldedDates(self):
        """Removes all bolded dates."""
        if self._calendar:
            self._calendar.calevent_remove('all', 'bold')
            self._bolded_dates.clear()

    def SetDate(self, date):
        """Sets the selected date."""
        self.SelectionStart = date

    # Properties
    @property
    def SelectionStart(self): return self._selection_start
    @SelectionStart.setter
    def SelectionStart(self, value):
        self._selection_start = value
        if self._calendar:
            self._calendar.selection_set(value)

    @property
    def SelectionEnd(self): return self._selection_end
    @SelectionEnd.setter
    def SelectionEnd(self, value):
        self._selection_end = value
        # tkcalendar only supports single date in 'day' mode
        if self._calendar:
            self._calendar.selection_set(value)

    @property
    def SelectionRange(self): return (self._selection_start, self._selection_end)
    @SelectionRange.setter
    def SelectionRange(self, value):
        if value and len(value) >= 1:
            self.SelectionStart = value[0]
            # Ignore end for now as we are single select

    @property
    def MinDate(self): return self._min_date
    @MinDate.setter
    def MinDate(self, value):
        self._min_date = value
        if self._calendar: 
            try:
                self._calendar.configure(mindate=value)
            except Exception as e:
                print(f"Error setting MinDate: {e}")

    @property
    def MaxDate(self): return self._max_date
    @MaxDate.setter
    def MaxDate(self, value):
        self._max_date = value
        if self._calendar: 
            try:
                self._calendar.configure(maxdate=value)
            except Exception as e:
                print(f"Error setting MaxDate: {e}")

    @property
    def ShowWeekNumbers(self): return self._show_week_numbers
    @ShowWeekNumbers.setter
    def ShowWeekNumbers(self, value):
        self._show_week_numbers = value
        if self._calendar: self._calendar.configure(showweeknumbers=value)

    @property
    def FirstDayOfWeek(self): return self._first_day_of_week
    @FirstDayOfWeek.setter
    def FirstDayOfWeek(self, value):
        self._first_day_of_week = value
        val = 'sunday' if value == Day.Sunday else 'monday'
        if self._calendar: self._calendar.configure(firstweekday=val)

    # Styles
    @property
    def TitleBackColor(self): return self._styles.get('headersbackground')
    @TitleBackColor.setter
    def TitleBackColor(self, value): self._update_style('headersbackground', value)

    @property
    def TitleForeColor(self): return self._styles.get('headersforeground')
    @TitleForeColor.setter
    def TitleForeColor(self, value): self._update_style('headersforeground', value)

    @property
    def TrailingForeColor(self): return self._styles.get('othermonthforeground')
    @TrailingForeColor.setter
    def TrailingForeColor(self, value): self._update_style('othermonthforeground', value)

    @property
    def BackColor(self): return self._styles.get('background')
    @BackColor.setter
    def BackColor(self, value): self._update_style('background', value)

    @property
    def ForeColor(self): return self._styles.get('foreground')
    @ForeColor.setter
    def ForeColor(self, value): self._update_style('foreground', value)

    # Direct tkcalendar styles
    @property
    def Locale(self): return self._styles.get('locale')
    @Locale.setter
    def Locale(self, value): self._update_style('locale', value)

    @property
    def HeadersBackground(self): return self._styles.get('headersbackground')
    @HeadersBackground.setter
    def HeadersBackground(self, value): self._update_style('headersbackground', value)

    @property
    def HeadersForeground(self): return self._styles.get('headersforeground')
    @HeadersForeground.setter
    def HeadersForeground(self, value): self._update_style('headersforeground', value)

    @property
    def SelectBackground(self): return self._styles.get('selectbackground')
    @SelectBackground.setter
    def SelectBackground(self, value): self._update_style('selectbackground', value)

    @property
    def SelectForeground(self): return self._styles.get('selectforeground')
    @SelectForeground.setter
    def SelectForeground(self, value): self._update_style('selectforeground', value)

    @property
    def WeekendBackground(self): return self._styles.get('weekendbackground')
    @WeekendBackground.setter
    def WeekendBackground(self, value): self._update_style('weekendbackground', value)

    @property
    def WeekendForeground(self): return self._styles.get('weekendforeground')
    @WeekendForeground.setter
    def WeekendForeground(self, value): self._update_style('weekendforeground', value)

    @property
    def OtherMonthBackground(self): return self._styles.get('othermonthbackground')
    @OtherMonthBackground.setter
    def OtherMonthBackground(self, value): self._update_style('othermonthbackground', value)

    @property
    def OtherMonthForeground(self): return self._styles.get('othermonthforeground')
    @OtherMonthForeground.setter
    def OtherMonthForeground(self, value): self._update_style('othermonthforeground', value)

    @property
    def OtherMonthWeekendBackground(self): return self._styles.get('othermonthwebackground')
    @OtherMonthWeekendBackground.setter
    def OtherMonthWeekendBackground(self, value): self._update_style('othermonthwebackground', value)

    @property
    def OtherMonthWeekendForeground(self): return self._styles.get('othermonthweforeground')
    @OtherMonthWeekendForeground.setter
    def OtherMonthWeekendForeground(self, value): self._update_style('othermonthweforeground', value)


class DatePicker(ControlBase):
    """
    Represents a Windows Forms-style date picker control.
    Wraps tkcalendar.DateEntry to provide a rich date selection experience.
    """
    
    # Default constants
    MinDateTime = datetime(1753, 1, 1)
    MaxDateTime = datetime(9998, 12, 31)

    def __init__(self, master_form, props=None):
        # Initialize internal state
        self._date_entry = None
        self._chk = None
        self._chk_var = None
        self._value = datetime.now()
        self._format = DatePickerFormat.USFormat
        self._custom_format = ""
        self._min_date = self.MinDateTime
        self._max_date = self.MaxDateTime
        self._show_check_box = False
        self._checked = True
        
        # Style and Config storage
        self._styles = {}
        
        # Events
        self.ValueChanged = lambda sender, e: None
        self.FormatChanged = lambda sender, e: None
        self.CheckedChanged = lambda sender, e: None

        # Default properties
        defaults = {
            'Left': 10, 'Top': 10, 'Width': 150, 'Height': 25, 'Name': "",
            'Value': datetime.now(),
            'Format': DatePickerFormat.USFormat,
            'CustomFormat': "",
            'MinDate': self.MinDateTime,
            'MaxDate': self.MaxDateTime,
            'ShowCheckBox': False,
            'Checked': True,
            'Enabled': True,
            # WinForms / tkcalendar styles
            'CalendarMonthBackground': None,
            'CalendarTitleBackColor': None,
            'CalendarTitleForeColor': None,
            'CalendarTrailingForeColor': None,
            'Locale': None,
            'FirstWeekday': None,
            'ShowWeekNumbers': False,
            'HeadersBackground': None,
            'HeadersForeground': None,
            'SelectBackground': None,
            'SelectForeground': None,
            'WeekendBackground': None,
            'WeekendForeground': None,
            'OtherMonthBackground': None,
            'OtherMonthForeground': None,
            'OtherMonthWeekendBackground': None,
            'OtherMonthWeekendForeground': None,
            'TooltipBackground': None,
            'TooltipForeground': None,
            'TooltipAlpha': None,
            'TooltipDelay': None
        }
        
        if props:
            defaults.update(props)

        # Initialize ControlBase
        master_widget, parent_container = _resolve_master_widget(master_form)
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        self._parent_container = parent_container
        self.Name = defaults['Name']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        
        # Apply core properties
        self._value = defaults['Value'] or datetime.now()
        self._format = defaults['Format']
        self._custom_format = defaults['CustomFormat']
        self._min_date = defaults['MinDate'] or self.MinDateTime
        self._max_date = defaults['MaxDate'] or self.MaxDateTime
        self._show_check_box = defaults['ShowCheckBox']
        self._checked = defaults['Checked']
        
        # Store styles
        self._styles['background'] = defaults.get('CalendarMonthBackground')
        self._styles['headersbackground'] = defaults.get('CalendarTitleBackColor') or defaults.get('HeadersBackground')
        self._styles['headersforeground'] = defaults.get('CalendarTitleForeColor') or defaults.get('HeadersForeground')
        self._styles['othermonthforeground'] = defaults.get('CalendarTrailingForeColor') or defaults.get('OtherMonthForeground')
        
        # Store other styles directly
        for key in ['Locale', 'FirstWeekday', 'ShowWeekNumbers', 'SelectBackground', 'SelectForeground', 
                   'WeekendBackground', 'WeekendForeground', 'OtherMonthBackground', 
                   'OtherMonthWeekendBackground', 'OtherMonthWeekendForeground',
                   'TooltipBackground', 'TooltipForeground', 'TooltipAlpha', 'TooltipDelay']:
             if defaults.get(key) is not None:
                 opt = key.lower()
                 if key == 'FirstWeekday':
                     val = defaults[key]
                     self._styles[opt] = 'sunday' if val == Day.Sunday else 'monday'
                 else:
                     self._styles[opt] = defaults[key]

        # Create the control
        self._create_control()
        
        # Apply initial state
        self._update_display()
        
        # Auto-register
        self._auto_register_with_parent()

    def _create_control(self):
        self._frame = tk.Frame(self.master)
        self._tk_widget = self._frame
        
        if self._show_check_box:
            self._chk_var = tk.IntVar(value=1 if self._checked else 0)
            self._chk = tk.Checkbutton(self._frame, variable=self._chk_var, command=self._on_checked_changed)
            self._chk.pack(side='left')
            
        if install_library("tkcalendar"):
            try:
                from tkcalendar import DateEntry
                
                # Prepare options
                options = {
                    'width': 12,
                    'year': self._value.year,
                    'month': self._value.month,
                    'day': self._value.day,
                    'mindate': self._min_date,
                    'maxdate': self._max_date,
                }
                
                # Add styles
                valid_styles = {k: v for k, v in self._styles.items() if v is not None}
                options.update(valid_styles)
                
                self._date_entry = DateEntry(self._frame, **options)
                self._date_entry.pack(side='left', fill='both', expand=True)
                
                self._date_entry.bind("<<DateEntrySelected>>", self._on_date_changed)
                self._date_entry.bind("<FocusOut>", self._on_date_changed)
                self._date_entry.bind("<Return>", self._on_date_changed)
                
            except ImportError:
                self._create_fallback()
        else:
            self._create_fallback()
            
        self._place_control(self.Width, self.Height)

    def _create_fallback(self):
        self._date_entry = tk.Entry(self._frame)
        self._date_entry.insert(0, "Install tkcalendar")
        self._date_entry.config(state='disabled')
        self._date_entry.pack(side='left', fill='both', expand=True)

    def _update_display(self):
        if not self._date_entry or isinstance(self._date_entry, tk.Entry):
            return
            
        try:
            # Determine pattern
            if self._format == DatePickerFormat.Custom:
                pattern = self._custom_format
            elif isinstance(self._format, DatePickerFormat):
                pattern = self._format.value
            else:
                pattern = str(self._format)
                
            # Configure pattern first
            self._date_entry.configure(date_pattern=pattern)
            
            # Set date
            self._date_entry.set_date(self._value.date())
            
            # Update state
            if self._show_check_box:
                state = 'normal' if self._checked else 'disabled'
                self._date_entry.config(state=state)
                
        except Exception:
            pass

    def _on_date_changed(self, event):
        try:
            val = self._date_entry.get_date()
            current_time = self._value.time()
            new_value = datetime.combine(val, current_time)
            
            if new_value != self._value:
                self.Value = new_value
        except:
            pass

    def _on_checked_changed(self):
        self._checked = bool(self._chk_var.get())
        self._update_display()
        self.CheckedChanged(self, {'Checked': self._checked})

    def _update_style(self, option, value):
        self._styles[option] = value
        if self._date_entry and hasattr(self._date_entry, 'configure'):
            try:
                self._date_entry.configure(**{option: value})
            except:
                pass

    # Properties
    @property
    def Value(self): return self._value
    @Value.setter
    def Value(self, value):
        if value < self._min_date: value = self._min_date
        if value > self._max_date: value = self._max_date
        old = self._value
        self._value = value
        self._update_display()
        if old != value: self.ValueChanged(self, {'OldValue': old, 'NewValue': value})

    @property
    def MinDate(self): return self._min_date
    @MinDate.setter
    def MinDate(self, value):
        self._min_date = value
        if self._date_entry and hasattr(self._date_entry, 'configure'):
            self._date_entry.configure(mindate=value)

    @property
    def MaxDate(self): return self._max_date
    @MaxDate.setter
    def MaxDate(self, value):
        self._max_date = value
        if self._date_entry and hasattr(self._date_entry, 'configure'):
            self._date_entry.configure(maxdate=value)

    @property
    def Format(self): return self._format
    @Format.setter
    def Format(self, value):
        old = self._format
        self._format = value
        self._update_display()
        if old != value: self.FormatChanged(self, {'OldFormat': old, 'NewFormat': value})

    @property
    def CustomFormat(self): return self._custom_format
    @CustomFormat.setter
    def CustomFormat(self, value):
        self._custom_format = value
        if self._format == DatePickerFormat.Custom:
            self._update_display()

    @property
    def ShowCheckBox(self): return self._show_check_box
    @ShowCheckBox.setter
    def ShowCheckBox(self, value):
        self._show_check_box = value
        if self._chk:
            if value: self._chk.pack(side='left', before=self._date_entry)
            else: self._chk.pack_forget()
        elif value:
            self._chk_var = tk.IntVar(value=1 if self._checked else 0)
            self._chk = tk.Checkbutton(self._frame, variable=self._chk_var, command=self._on_checked_changed)
            self._chk.pack(side='left', before=self._date_entry)

    @property
    def Checked(self): return self._checked
    @Checked.setter
    def Checked(self, value):
        self._checked = value
        if self._chk_var: self._chk_var.set(1 if value else 0)
        self._update_display()
        self.CheckedChanged(self, {'Checked': value})

    # Style Properties
    @property
    def CalendarMonthBackground(self): return self._styles.get('background')
    @CalendarMonthBackground.setter
    def CalendarMonthBackground(self, value): self._update_style('background', value)

    @property
    def CalendarTitleBackColor(self): return self._styles.get('headersbackground')
    @CalendarTitleBackColor.setter
    def CalendarTitleBackColor(self, value): self._update_style('headersbackground', value)

    @property
    def CalendarTitleForeColor(self): return self._styles.get('headersforeground')
    @CalendarTitleForeColor.setter
    def CalendarTitleForeColor(self, value): self._update_style('headersforeground', value)

    @property
    def CalendarTrailingForeColor(self): return self._styles.get('othermonthforeground')
    @CalendarTrailingForeColor.setter
    def CalendarTrailingForeColor(self, value): self._update_style('othermonthforeground', value)

    # tkcalendar direct properties
    @property
    def Locale(self): return self._styles.get('locale')
    @Locale.setter
    def Locale(self, value): self._update_style('locale', value)

    @property
    def FirstWeekday(self): return self._styles.get('firstweekday')
    @FirstWeekday.setter
    def FirstWeekday(self, value):
        val = 'sunday' if value == Day.Sunday else 'monday'
        self._update_style('firstweekday', val)

    @property
    def ShowWeekNumbers(self): return self._styles.get('showweeknumbers')
    @ShowWeekNumbers.setter
    def ShowWeekNumbers(self, value): self._update_style('showweeknumbers', value)

    @property
    def HeadersBackground(self): return self._styles.get('headersbackground')
    @HeadersBackground.setter
    def HeadersBackground(self, value): self._update_style('headersbackground', value)

    @property
    def HeadersForeground(self): return self._styles.get('headersforeground')
    @HeadersForeground.setter
    def HeadersForeground(self, value): self._update_style('headersforeground', value)

    @property
    def SelectBackground(self): return self._styles.get('selectbackground')
    @SelectBackground.setter
    def SelectBackground(self, value): self._update_style('selectbackground', value)

    @property
    def SelectForeground(self): return self._styles.get('selectforeground')
    @SelectForeground.setter
    def SelectForeground(self, value): self._update_style('selectforeground', value)

    @property
    def WeekendBackground(self): return self._styles.get('weekendbackground')
    @WeekendBackground.setter
    def WeekendBackground(self, value): self._update_style('weekendbackground', value)

    @property
    def WeekendForeground(self): return self._styles.get('weekendforeground')
    @WeekendForeground.setter
    def WeekendForeground(self, value): self._update_style('weekendforeground', value)

    @property
    def OtherMonthBackground(self): return self._styles.get('othermonthbackground')
    @OtherMonthBackground.setter
    def OtherMonthBackground(self, value): self._update_style('othermonthbackground', value)

    @property
    def OtherMonthForeground(self): return self._styles.get('othermonthforeground')
    @OtherMonthForeground.setter
    def OtherMonthForeground(self, value): self._update_style('othermonthforeground', value)

    @property
    def OtherMonthWeekendBackground(self): return self._styles.get('othermonthwebackground')
    @OtherMonthWeekendBackground.setter
    def OtherMonthWeekendBackground(self, value): self._update_style('othermonthwebackground', value)

    @property
    def OtherMonthWeekendForeground(self): return self._styles.get('othermonthweforeground')
    @OtherMonthWeekendForeground.setter
    def OtherMonthWeekendForeground(self, value): self._update_style('othermonthweforeground', value)

    @property
    def TooltipBackground(self): return self._styles.get('tooltipbackground')
    @TooltipBackground.setter
    def TooltipBackground(self, value): self._update_style('tooltipbackground', value)

    @property
    def TooltipForeground(self): return self._styles.get('tooltipforeground')
    @TooltipForeground.setter
    def TooltipForeground(self, value): self._update_style('tooltipforeground', value)

    @property
    def TooltipAlpha(self): return self._styles.get('tooltipalpha')
    @TooltipAlpha.setter
    def TooltipAlpha(self, value): self._update_style('tooltipalpha', value)

    @property
    def TooltipDelay(self): return self._styles.get('tooltipdelay')
    @TooltipDelay.setter
    def TooltipDelay(self, value): self._update_style('tooltipdelay', value)
    
    @CustomFormat.setter
    def CustomFormat(self, value):
        old_custom = getattr(self, '_custom_format', None)
        self._custom_format = value
        self._update_display()
        if old_custom != value:
            self.FormatChanged(self, {'OldCustomFormat': old_custom, 'NewCustomFormat': value})

    @property
    def Checked(self):
        return self._checked
    
    @Checked.setter
    def Checked(self, value):
        if self._checked != value:
            self._checked = value
            self._chk_var.set(1 if value else 0)
            self._update_display()
            self.CheckedChanged(self, {'Checked': value})

