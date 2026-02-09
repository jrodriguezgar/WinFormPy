# WinFormPy Tools

Utility module providing advanced tools for layout, styling, and system integration.

## Module: `winformpy_tools.py`

### 1. FontManager
Manage and retrieve system fonts.
```python
from winformpy_tools import FontManager
fonts = FontManager.get_all_available_fonts()
default = FontManager.get_system_font('default')
```

### 2. ColorManager
Access native Windows system colors.
```python
from winformpy_tools import ColorManager
win_bg = ColorManager.get_system_color('window')
```

### 3. CSSManager
Apply styles to controls using CSS syntax.
```python
from winformpy_tools import CSSManager
CSSManager.apply_css_to_winform_control(btn, "background-color: blue; color: white;")
```

### 4. LayoutManager
Automatic distribution of controls (Flow, Stack, Grid).
```python
layout = LayoutManager(panel, margin=10)
layout.add_control(btn1)
layout.add_control(btn2)
```
