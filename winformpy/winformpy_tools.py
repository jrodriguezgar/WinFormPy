"""
WinFormPy Tools - Utilities for Windows Forms in Python

This module contains utility functions for working with Windows Forms controls.
"""

import tkinter as tk
import tkinter.font as tkFont
from typing import Dict, List, Tuple, Optional, Union
import ctypes


class FontManager:
    """
    Class for managing system fonts and font utilities.
    
    Provides methods to retrieve system fonts, specific fonts, and available fonts.
    """
    
    @staticmethod
    def get_system_fonts() -> Dict[str, Tuple[str, ...]]:
        """
        Get a dictionary with Windows system fonts.

        Returns:
            Dictionary with system fonts:
            {
                'default': ('Segoe UI', 9),
                'menu': ('Segoe UI', 9),
                'message': ('Segoe UI', 9),
                'status': ('Segoe UI', 9),
                'caption': ('Segoe UI', 9, 'bold'),
                'icon': ('Segoe UI', 9),
                'tooltip': ('Segoe UI', 9)
            }
        """
        try:
            # Create a temporary window to get system fonts
            root = tk._default_root
            if root is None:
                root = tk.Tk()
                root.withdraw()
                temp_root = True
            else:
                temp_root = False

            # Get system fonts
            default_font = tkFont.nametofont("TkDefaultFont")
            text_font = tkFont.nametofont("TkTextFont")
            fixed_font = tkFont.nametofont("TkFixedFont")
            menu_font = tkFont.nametofont("TkMenuFont")
            heading_font = tkFont.nametofont("TkHeadingFont")
            caption_font = tkFont.nametofont("TkCaptionFont")
            small_caption_font = tkFont.nametofont("TkSmallCaptionFont")
            icon_font = tkFont.nametofont("TkIconFont")
            tooltip_font = tkFont.nametofont("TkTooltipFont")

            fonts = {
                'default': (default_font.actual('family'), default_font.actual('size')),
                'text': (text_font.actual('family'), text_font.actual('size')),
                'fixed': (fixed_font.actual('family'), fixed_font.actual('size')),
                'menu': (menu_font.actual('family'), menu_font.actual('size')),
                'heading': (heading_font.actual('family'), heading_font.actual('size')),
                'caption': (caption_font.actual('family'), caption_font.actual('size'), 'bold'),
                'small_caption': (small_caption_font.actual('family'), small_caption_font.actual('size')),
                'icon': (icon_font.actual('family'), icon_font.actual('size')),
                'tooltip': (tooltip_font.actual('family'), tooltip_font.actual('size')),
                'status': (default_font.actual('family'), default_font.actual('size')),
                'message': (default_font.actual('family'), default_font.actual('size'))
            }

            if temp_root:
                root.destroy()

            return fonts
        except Exception:
            # If it fails, return default Windows fonts
            return {
                'default': ('Segoe UI', 9),
                'text': ('Segoe UI', 9),
                'fixed': ('Consolas', 9),
                'menu': ('Segoe UI', 9),
                'heading': ('Segoe UI', 9, 'bold'),
                'caption': ('Segoe UI', 9, 'bold'),
                'small_caption': ('Segoe UI', 8),
                'icon': ('Segoe UI', 9),
                'tooltip': ('Segoe UI', 9),
                'status': ('Segoe UI', 9),
                'message': ('Segoe UI', 9)
            }

    @staticmethod
    def get_system_font(font_type: str = 'default') -> Tuple[str, ...]:
        """
        Get a specific system font.

        Args:
            font_type: Font type ('default', 'menu', 'status', 'caption', 'tooltip', etc.)

        Returns:
            Tuple with the font (family, size) or (family, size, style)

        Examples:
            >>> font = FontManager.get_system_font('default')
            ('Segoe UI', 9)

            >>> font = FontManager.get_system_font('caption')
            ('Segoe UI', 9, 'bold')
        """
        fonts = FontManager.get_system_fonts()
        return fonts.get(font_type, fonts['default'])

    @staticmethod
    def get_all_available_fonts() -> List[str]:
        """
        Get the list of all available fonts on the system.

        Returns:
            Sorted list of available font names

        Example:
            >>> fonts = FontManager.get_all_available_fonts()
            ['Arial', 'Calibri', 'Consolas', 'Courier New', 'Segoe UI', ...]
        """
        try:
            root = tk._default_root
            if root is None:
                root = tk.Tk()
                root.withdraw()
                temp_root = True
            else:
                temp_root = False

            font_families = sorted(tkFont.families())

            if temp_root:
                root.destroy()

            return font_families
        except Exception:
            # Basic list of common Windows fonts
            return [
                'Arial', 'Arial Black', 'Calibri', 'Cambria', 'Candara',
                'Comic Sans MS', 'Consolas', 'Constantia', 'Corbel', 'Courier New',
                'Georgia', 'Impact', 'Lucida Console', 'Lucida Sans Unicode',
                'Microsoft Sans Serif', 'Segoe UI', 'Tahoma', 'Times New Roman',
                'Trebuchet MS', 'Verdana'
            ]


class ColorManager:
    """
    Class for managing system colors and color utilities.
    
    Provides methods to retrieve system colors and specific colors.
    """
    
    @staticmethod
    def get_system_colors() -> Dict[str, str]:
        """
        Get Windows system colors using Windows API.

        Returns:
            Dictionary with system colors in hexadecimal format:
            {
                'control': '#F0F0F0',
                'window': '#FFFFFF',
                'text': '#000000',
                'button': '#F0F0F0',
                'highlight': '#0078D7',
                ...
            }
        """
        try:
            # Windows system color indices
            COLOR_BTNFACE = 15
            COLOR_WINDOW = 5
            COLOR_WINDOWTEXT = 8
            COLOR_HIGHLIGHT = 13
            COLOR_HIGHLIGHTTEXT = 14
            COLOR_INFOBK = 24
            COLOR_INFOTEXT = 23
            COLOR_ACTIVECAPTION = 2
            COLOR_INACTIVECAPTION = 3
            COLOR_MENU = 4
            COLOR_MENUTEXT = 7
            COLOR_GRAYTEXT = 17
            COLOR_WINDOWFRAME = 6

            def rgb_to_hex(colorref: int) -> str:
                """Convert Windows COLORREF (0x00BBGGRR) to hex #RRGGBB."""
                r = colorref & 0xFF
                g = (colorref >> 8) & 0xFF
                b = (colorref >> 16) & 0xFF
                return f'#{r:02X}{g:02X}{b:02X}'

            colors = {
                'control': rgb_to_hex(ctypes.windll.user32.GetSysColor(COLOR_BTNFACE)),
                'window': rgb_to_hex(ctypes.windll.user32.GetSysColor(COLOR_WINDOW)),
                'text': rgb_to_hex(ctypes.windll.user32.GetSysColor(COLOR_WINDOWTEXT)),
                'button': rgb_to_hex(ctypes.windll.user32.GetSysColor(COLOR_BTNFACE)),
                'highlight': rgb_to_hex(ctypes.windll.user32.GetSysColor(COLOR_HIGHLIGHT)),
                'highlight_text': rgb_to_hex(ctypes.windll.user32.GetSysColor(COLOR_HIGHLIGHTTEXT)),
                'info': rgb_to_hex(ctypes.windll.user32.GetSysColor(COLOR_INFOBK)),
                'info_text': rgb_to_hex(ctypes.windll.user32.GetSysColor(COLOR_INFOTEXT)),
                'active': rgb_to_hex(ctypes.windll.user32.GetSysColor(COLOR_ACTIVECAPTION)),
                'inactive': rgb_to_hex(ctypes.windll.user32.GetSysColor(COLOR_INACTIVECAPTION)),
                'menu': rgb_to_hex(ctypes.windll.user32.GetSysColor(COLOR_MENU)),
                'menu_text': rgb_to_hex(ctypes.windll.user32.GetSysColor(COLOR_MENUTEXT)),
                'gray_text': rgb_to_hex(ctypes.windll.user32.GetSysColor(COLOR_GRAYTEXT)),
                'border': rgb_to_hex(ctypes.windll.user32.GetSysColor(COLOR_WINDOWFRAME))
            }

            return colors
        except Exception:
            # Fallback to default Windows colors if API call fails
            return {
                'control': '#F0F0F0',
                'window': '#FFFFFF',
                'text': '#000000',
                'button': '#F0F0F0',
                'highlight': '#0078D7',
                'highlight_text': '#FFFFFF',
                'info': '#FFFFE1',
                'info_text': '#000000',
                'active': '#E5F3FF',
                'inactive': '#F0F0F0',
                'menu': '#F0F0F0',
                'menu_text': '#000000',
                'gray_text': '#6D6D6D',
                'border': '#ADADAD'
            }

    @staticmethod
    def get_system_color(color_type: str = 'control') -> str:
        """
        Get a specific system color.

        Args:
            color_type: Color type ('control', 'window', 'text', 'button', 'highlight', etc.)

        Returns:
            String with the color in hexadecimal format

        Examples:
            >>> color = ColorManager.get_system_color('control')
            '#F0F0F0'

            >>> color = ColorManager.get_system_color('highlight')
            '#0078D7'
        """
        colors = ColorManager.get_system_colors()
        return colors.get(color_type, colors['control'])


class CSSManager:
    """
    Class for managing CSS parsing and conversion to Tkinter configurations.
    
    Provides methods to parse CSS strings and apply them to Tkinter widgets.
    """
    
    @staticmethod
    def parse_css_string(css_string: str) -> Dict[str, str]:
        """
        Parse a CSS string and return a dictionary with the styles.

        Args:
            css_string: String with CSS styles (e.g., "color: blue; font-size: 12")

        Returns:
            Dictionary with parsed styles
        """
        styles = {}
        for rule in css_string.split(';'):
            if ':' in rule:
                key, value = rule.split(':', 1)
                styles[key.strip()] = value.strip()
        return styles

    @staticmethod
    def css_to_winform_props(css_string: str) -> Dict[str, Union[str, int, Tuple]]:
        """
        Convert a CSS string to WinFormPy control properties dictionary.

        Args:
            css_string: String with CSS styles

        Returns:
            Dictionary with WinFormPy properties (e.g., 'BackColor', 'ForeColor', 'Font', 'Width', etc.)
        """
        styles = CSSManager.parse_css_string(css_string)
        props = {}

        # Mapping CSS properties to WinFormPy properties
        if 'color' in styles:
            props['ForeColor'] = styles['color']

        if 'background-color' in styles:
            props['BackColor'] = styles['background-color']

        # Font handling
        font_family = None
        font_size = None
        font_weight = None

        if 'font-family' in styles:
            font_family = styles['font-family']

        if 'font-size' in styles:
            # Remove 'px' if present
            size_str = styles['font-size'].replace('px', '')
            try:
                font_size = int(size_str)
            except ValueError:
                font_size = 9  # default

        if 'font-weight' in styles and styles['font-weight'] == 'bold':
            font_weight = 'bold'

        # Build Font tuple if any font property is set
        if font_family or font_size or font_weight:
            # Default values
            family = font_family or 'Segoe UI'
            size = font_size or 9
            weight = font_weight or ''
            props['Font'] = (family, size) if not weight else (family, size, weight)

        if 'width' in styles:
            width_str = styles['width'].replace('px', '')
            try:
                props['Width'] = int(width_str)
            except ValueError:
                pass

        if 'height' in styles:
            height_str = styles['height'].replace('px', '')
            try:
                props['Height'] = int(height_str)
            except ValueError:
                pass

        # Position properties (extended CSS support)
        if 'left' in styles:
            left_str = styles['left'].replace('px', '')
            try:
                props['Left'] = int(left_str)
            except ValueError:
                pass

        if 'top' in styles:
            top_str = styles['top'].replace('px', '')
            try:
                props['Top'] = int(top_str)
            except ValueError:
                pass

        if 'position' in styles and styles['position'] == 'absolute':
            # Enable absolute positioning
            pass  # WinFormPy uses Left/Top by default

        # Border style
        if 'border' in styles or 'border-style' in styles:
            border_map = {
                'solid': 'solid',
                'none': 'flat',
                'dotted': 'groove',
                'dashed': 'ridge'
            }
            border_style = styles.get('border-style', styles.get('border', 'solid').split()[0])
            props['BorderStyle'] = border_map.get(border_style, 'flat')

        if 'border-width' in styles:
            border_width_str = styles['border-width'].replace('px', '')
            try:
                props['BorderWidth'] = int(border_width_str)
            except ValueError:
                pass

        # Padding (simplified)
        if 'padding' in styles:
            padding_str = styles['padding'].replace('px', '')
            try:
                padding = int(padding_str)
                # WinFormPy doesn't have direct padding, but we can set it if needed
                # For now, just store it
                props['_Padding'] = padding
            except ValueError:
                pass

        return props

    @staticmethod
    def apply_css_to_widget(widget: tk.Widget, css_string: str) -> None:
        """
        Apply CSS styles directly to a Tkinter widget.

        Args:
            widget: Tkinter widget
            css_string: String with CSS styles
        """
        config = CSSManager.css_to_tkinter_config(css_string, widget)
        if config:
            widget.config(**config)

    @staticmethod
    def apply_css_to_winform_control(control, css_string: str) -> None:
        """
        Apply CSS styles to a WinFormPy control by setting its properties.

        Args:
            control: WinFormPy control instance
            css_string: String with CSS styles
        """
        props = CSSManager.css_to_winform_props(css_string)
        for prop_name, prop_value in props.items():
            if hasattr(control, prop_name):
                setattr(control, prop_name, prop_value)


def parse_css_string(css_string: str) -> Dict[str, str]:
    """Deprecated: Use CSSManager.parse_css_string() instead."""
    return CSSManager.parse_css_string(css_string)


def css_to_tkinter_config(css_string: str, current_widget: Optional[tk.Widget] = None) -> Dict[str, Union[str, int, Tuple]]:
    """Deprecated: Use CSSManager.css_to_tkinter_config() instead."""
    return CSSManager.css_to_tkinter_config(css_string, current_widget)


def apply_css_to_widget(widget: tk.Widget, css_string: str) -> None:
    """Deprecated: Use CSSManager.apply_css_to_widget() instead."""
    CSSManager.apply_css_to_widget(widget, css_string)


def css_to_winform_props(css_string: str) -> Dict[str, Union[str, int, Tuple]]:
    """Deprecated: Use CSSManager.css_to_winform_props() instead."""
    return CSSManager.css_to_winform_props(css_string)


def apply_css_to_winform_control(control, css_string: str) -> None:
    """Deprecated: Use CSSManager.apply_css_to_winform_control() instead."""
    CSSManager.apply_css_to_winform_control(control, css_string)


from enum import Enum, auto

class LayoutManager:
    """
    Class for automatically distributing controls in a container (like a Panel).
    
    Supports vertical (top to bottom), horizontal (left to right), and flow layouts.
    Starts positioning from the top-left corner (0, 0) or padding offset.
    """
    
    class StartPosition(Enum):
        TopLeft = 0

    class Distribution(Enum):
        UpDown = 0    # Vertical Top to Bottom
        LeftRight = 2 # Horizontal Left to Right

    class Alignment(Enum):
        Up = 0
        Down = 1
        Left = 2
        Right = 3
        Center = 4

    class LayoutType(Enum):
        FlowLayout = 0
        Autosize = 1
        Dock = 2
        Anchor = 3
        TableLayout = 4

    def __init__(self, container, margin: int = 0, padding: int = 0, autosize_container: bool = False, wrap_count: int = None):
        """
        Initialize the LayoutManager.
        
        Args:
            container: The container control (e.g., Panel) where controls will be placed.
            margin: Space between controls in pixels (default 0).
            padding: Space from container borders (default 0).
            autosize_container: If True, the container will automatically resize to fit controls.
            wrap_count: Number of items per row/column before wrapping. If None, wraps based on container size (Automatic).
        """
        self.container = container
        self.margin = margin
        self.padding = padding
        self.wrap_count = wrap_count
        self.start_position = self.StartPosition.TopLeft
        self.distribution = self.Distribution.UpDown
        self.alignment = self.Alignment.Left
        self.layout_type = self.LayoutType.FlowLayout
        
        # Enable AutoSize on container if requested
        if autosize_container and hasattr(self.container, 'AutoSize'):
            self.container.AutoSize = True
        
        self.max_width = 0
        self.max_height = 0
        self.controls = []  # Track managed controls
        self.current_row_height = 0  # Track max height in current row for flow layout
        self.current_col_width = 0   # Track max width in current column for flow layout
        self.reset()
    
    def add_control(self, control):
        """
        Add a control to the container and position it automatically.
        
        Args:
            control: The control to add and position.
        """
        # Track the control
        self.controls.append(control)
        
        # Only position if visible
        if hasattr(control, 'Visible') and not control.Visible:
            return

        # Ignore controls with Dock or Anchor set (if not None/Default)
        # WinFormPy controls usually have Dock='None' (or DockStyle.None_) by default.
        if hasattr(control, 'Dock'):
            dock = control.Dock
            # Check if Dock is effectively "None"
            is_docked = False
            if dock:
                # If it's an Enum member (truthy), check if it's None_ (value 0)
                if hasattr(dock, 'value') and dock.value == 0:
                    is_docked = False
                elif str(dock) == 'None':
                    is_docked = False
                else:
                    is_docked = True
            
            if is_docked:
                return
        
        # Calculate position
        self._position_control(control)
        
        # Apply AutoSize if enabled
        self._apply_autosize()
    
    def _position_control(self, control):
        # Ensure integer coordinates
        x = int(self.current_x)
        y = int(self.current_y)
        
        container_width = self.container.Width
        container_height = self.container.Height
        
        # Get control dimensions (default to 0 if None for AutoSize controls)
        control_width = control.Width if control.Width is not None else 0
        control_height = control.Height if control.Height is not None else 0
        
        # Handle Flow Layout Wrapping
        if self.layout_type == self.LayoutType.FlowLayout:
            should_wrap = False
            
            # Check wrap based on count (Fixed)
            if self.wrap_count is not None and self.wrap_count > 0:
                if self.current_line_item_count >= self.wrap_count:
                    should_wrap = True
            else:
                # Check wrap based on size (Automatic)
                if self.distribution == self.Distribution.LeftRight:
                    if x + control_width > container_width - self.padding and x > self.start_x:
                        should_wrap = True
                elif self.distribution == self.Distribution.UpDown:
                    if y + control_height > container_height - self.padding and y > self.start_y:
                        should_wrap = True

            if should_wrap:
                if self.distribution == self.Distribution.LeftRight:
                    # Wrap to next line
                    x = self.start_x
                    y += self.current_row_height + self.margin
                    self.current_x = x
                    self.current_y = y
                    self.current_row_height = 0 # Reset row height for new row
                    self.current_col_width = 0 # Reset col width for new column (if needed)
                    self.current_line_item_count = 0
                elif self.distribution == self.Distribution.UpDown:
                    # Wrap to next column
                    y = self.start_y
                    x += self.current_col_width + self.margin
                    self.current_x = x
                    self.current_y = y
                    self.current_col_width = 0 # Reset col width for new column
                    self.current_row_height = 0 # Reset row height for new row
                    self.current_line_item_count = 0

        # Set the position of the control
        final_x = x
        final_y = y
        
        control.Left = final_x
        control.Top = final_y
        
        # Track maximum dimensions for AutoSize
        control_right = final_x + control_width
        control_bottom = final_y + control_height
        self.current_col_width = max(self.current_col_width, control_width)
            
        if control_right > self.max_width:
            self.max_width = control_right
        if control_bottom > self.max_height:
            self.max_height = control_bottom
        
        # Update the current position based on distribution
        if self.distribution == self.Distribution.UpDown:
            self.current_y += control_height + self.margin
            # Alignment handling (Cross-axis)
            if self.alignment == self.Alignment.Right:
                 control.Left = container_width - self.padding - control_width
            elif self.alignment == self.Alignment.Center:
                 control.Left = (container_width - control_width) // 2
            # Default Left: already set
            
        elif self.distribution == self.Distribution.LeftRight:
            self.current_x += control_width + self.margin
            self.current_row_height = max(self.current_row_height, control_height)
            # Alignment handling (Cross-axis - Vertical)
            # This is tricky for FlowLayout as it depends on row height.
            # For simple LeftRight without flow (single row), we can align.
            if self.alignment == self.Alignment.Down:
                 # Align to bottom of container? Or bottom of row?
                 # Let's assume bottom of container for now if not flow?
                 pass
        
        self.current_line_item_count += 1

    def _apply_autosize(self):
        """Apply AutoSize to container if enabled."""
        if hasattr(self.container, 'AutoSize') and self.container.AutoSize:
            new_width = self.max_width + self.padding
            new_height = self.max_height + self.padding
            
            # Apply size constraints if defined
            if hasattr(self.container, 'MinimumSize') and self.container.MinimumSize:
                min_w, min_h = self.container.MinimumSize
                new_width = max(new_width, min_w)
                new_height = max(new_height, min_h)
            
            if hasattr(self.container, 'MaximumSize') and self.container.MaximumSize:
                max_w, max_h = self.container.MaximumSize
                new_width = min(new_width, max_w)
                new_height = min(new_height, max_h)
            
            # Update container size
            self.container.Width = new_width
            self.container.Height = new_height
            
            # Update tkinter widget size
            if hasattr(self.container, '_tk_widget'):
                self.container._tk_widget.config(width=new_width, height=new_height)
    
    def reset(self):
        """
        Reset the layout position based on StartPosition.
        """
        self.max_width = 0
        self.max_height = 0
        self.current_col_width = 0
        self.current_row_height = 0
        self.current_line_item_count = 0
        
        # Ensure container has valid dimensions
        w = self.container.Width if hasattr(self.container, 'Width') else 0
        h = self.container.Height if hasattr(self.container, 'Height') else 0
        
        # If dimensions are 0 or 1 (uninitialized), try to get from tk widget
        if (w <= 1 or h <= 1) and hasattr(self.container, '_tk_widget'):
            try:
                self.container._tk_widget.update_idletasks()
                w = self.container._tk_widget.winfo_width()
                h = self.container._tk_widget.winfo_height()
            except Exception:
                pass
        
        p = self.padding
        
        # Determine start coordinates
        if self.start_position == self.StartPosition.TopLeft:
            self.current_x = p
            self.current_y = p
            
        self.start_x = self.current_x 
        self.start_y = self.current_y
    
    def arrange_all(self, controls=None):
        """
        Arrange all controls in the list automatically.
        
        Args:
            controls: Optional list of controls to arrange. If None, uses internal list.
        """
        if controls:
            self.controls = controls
            
        self.reset()
        # We need to clear controls list if we are re-adding them via add_control logic
        # But add_control appends. So we should iterate and call _position_control directly?
        # Or just reset controls list and re-add?
        
        # Better: iterate existing controls and re-position
        controls_to_arrange = list(self.controls)
        self.controls = [] # Clear to avoid duplication when calling add_control
        
        for control in controls_to_arrange:
            self.add_control(control)
    
    def recalculate_layout(self):
        """
        Recalculate the layout for all managed controls.
        """
        self.arrange_all()

# Alias for backward compatibility
AutoLayoutManager = LayoutManager
