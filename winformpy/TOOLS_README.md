# WinFormPy Tools

Utility module providing advanced tools for layout, styling, and system integration.

## Module: `winformpy_tools.py`

### Tools Reference

| Tool | Description |
| --- | --- |
| **FontManager** | System font discovery and retrieval |
| **ColorManager** | Native Windows system color access |
| **CSSManager** | Apply CSS-like styles to WinFormPy controls |
| **LayoutManager** | Automatic control distribution (Flow, Stack, Grid) |

### 1. FontManager
Manage and retrieve system fonts.
```python
from winformpy.winformpy_tools import FontManager

fonts = FontManager.get_all_available_fonts()
default = FontManager.get_system_font('default')
```

### 2. ColorManager
Access native Windows system colors.
```python
from winformpy.winformpy_tools import ColorManager

win_bg = ColorManager.get_system_color('window')
```

### 3. CSSManager
Apply styles to controls using CSS syntax. Internally integrated with `winformpy.py` via `css_to_tkinter_config` and `apply_css_to_widget`.
```python
from winformpy.winformpy_tools import CSSManager

CSSManager.apply_css_to_winform_control(btn, "background-color: blue; color: white; font-size: 14px;")
```

### 4. LayoutManager
Automatic distribution of controls (Flow, Stack, Grid).
```python
from winformpy.winformpy_tools import LayoutManager

layout = LayoutManager(panel, margin=10)
layout.add_control(btn1)
layout.add_control(btn2)
```

### Integration with Core

The CSS utilities (`css_to_tkinter_config`, `apply_css_to_widget`) are automatically imported by `winformpy.py` at module level, enabling CSS-style property application on any `ControlBase`-derived control.
