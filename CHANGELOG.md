# WinFormPy Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2025-12-05

## Major Changes

### 1. System Styles Framework
**New Classes Added:**
- `SystemColors`: Provides Windows Forms system color constants
- `SystemFonts`: Provides Windows Forms system font definitions  
- `SystemStyles`: Manages global styling and theming

**Key Features:**
- Predefined color palette matching Windows system colors
- Standard system fonts for consistent typography
- Global styling system with `SetGlobalFont()` and `SetGlobalColors()` methods
- Automatic application of system-appropriate styles to controls

### 2. Enhanced Control Initialization
**Modified Classes:** All control classes (Button, Label, TextBox, ComboBox, ListBox, CheckBox, Panel, etc.)

**Changes:**
- Added support for `UseSystemStyles` parameter in props dictionary
- Automatic application of system styles by default
- Improved props-based initialization with style application
- Better separation of style application logic

**Example Usage:**
```python
# Traditional approach (still supported)
button = Button(form)
button.Text = "Click me"

# New props-based with system styles
button = Button(form, {'Text': 'Click me', 'UseSystemStyles': True})

# Global styling
SystemStyles.SetGlobalFont(("Arial", 10))
SystemStyles.SetGlobalColors(BackColor="#FFFFFF", ForeColor="#000000")
```

### 3. ListBox Enhancements
**New Class:** `ListBoxObjectCollection`

**Changes:**
- Replaced simple list with dedicated collection class
- Added `Add()`, `Clear()`, `Remove()` methods
- Improved DataSource compatibility
- Better item management with automatic widget updates

**Benefits:**
- More VB.NET-like API for item manipulation
- Automatic synchronization between collection and UI
- Enhanced data binding capabilities

### 4. Event System Improvements
**CheckBox Class:**
- Added `CheckedChanged` and `CheckStateChanged` events
- Automatic event firing on state changes
- Better integration with VB.NET event patterns

**RadioButton Class:**
- Enhanced group handling with shared `StringVar` instances
- Proper mutual exclusion within named groups
- Support for both string group names and explicit StringVar objects

### 5. Dialog Enhancements
**MessageBox and InputBox:**
- Added `modal` parameter for proper modal dialog behavior
- Improved dialog parenting for better window management
- Enhanced cross-platform compatibility

**Form Class:**
- Added `ShowDialog()` method for modal form display
- Better support for dialog-based workflows

### 6. Visual Property Enhancements
**TabPage Class:**
- Added `BackColor`, `ForeColor`, `Font` properties
- Proper property setters for visual customization
- Inheritance of visual properties to child controls

**Panel Class:**
- Enhanced `Padding` property with proper getters/setters
- Improved border styling with `BorderStyle` support
- Better AutoSize behavior with padding calculations

**StatusBar Class:**
- Added `ShowPanels` property for display mode switching
- Improved panel layout with consistent padding
- Enhanced AutoSize handling for panels

## Technical Implementation Details

### SystemStyles.ApplyToDefaults()
**Location:** Applied in all control `__init__` methods

**Function:**
```python
@staticmethod
def ApplyToDefaults(defaults, control_type="Control", use_system_styles=None):
    """Applies system styles to control defaults based on configuration."""
    if use_system_styles or (use_system_styles is None and SystemStyles._use_system_styles_by_default):
        # Apply system colors based on control type
        if control_type == "Window":
            defaults.setdefault('BackColor', SystemColors.Window)
            defaults.setdefault('ForeColor', SystemColors.WindowText)
        elif control_type == "Control":
            defaults.setdefault('BackColor', SystemColors.Control)
            defaults.setdefault('ForeColor', SystemColors.ControlText)
        # ... additional control types
        
        # Apply global font if set
        if SystemStyles._global_font:
            defaults.setdefault('Font', SystemStyles._global_font)
        
        # Apply global colors if set
        if SystemStyles._global_back_color:
            defaults['BackColor'] = SystemStyles._global_back_color
        if SystemStyles._global_fore_color:
            defaults['ForeColor'] = SystemStyles._global_fore_color
```

### ListBoxObjectCollection Implementation
**Key Methods:**
- `Add(item)`: Adds item and updates UI automatically
- `Clear()`: Removes all items and clears UI
- `Remove(item)`: Removes specific item and updates UI
- List-like behavior with `__getitem__`, `__len__`, `__iter__`

### Modal Dialog Implementation
**MessageBox.Show() Enhancement:**
```python
def Show(text, caption="Message", buttons="OK", icon=None, defaultButton=None, options=None, modal=True):
    parent_widget = tk._default_root if modal else None
    # Use parent_widget in all messagebox calls for proper modal behavior
```

## Migration Guide

### For Existing Code
- **No breaking changes**: All existing code continues to work unchanged
- **Optional enhancements**: Use `UseSystemStyles: True` in props for better visual consistency
- **Global styling**: Call `SystemStyles.SetGlobalFont()` and `SystemStyles.SetGlobalColors()` for app-wide theming

### For New Code
- **Recommended**: Use props-based initialization with `UseSystemStyles: True`
- **Modal dialogs**: Use `modal=True` parameter in MessageBox/InputBox calls
- **ListBox items**: Use `listBox.Items.Add(item)` instead of direct list manipulation
- **RadioButton groups**: Use string group names for automatic group management

## Performance Considerations
- System styles are applied once during control initialization
- Global style changes require control recreation for full effect
- Modal dialogs use proper parenting for better performance
- ListBox collection operations are optimized for UI synchronization

## Compatibility
- **Python**: 3.7+ (unchanged)
- **Tkinter**: Standard library (unchanged)
- **Platforms**: Windows, macOS, Linux (unchanged)
- **Backwards Compatible**: Yes, all existing APIs preserved

## Testing Recommendations
- Test control initialization with and without `UseSystemStyles`
- Verify modal dialog behavior across platforms
- Test RadioButton group functionality with multiple groups
- Validate ListBox item operations and DataSource binding
- Check global styling application and inheritance

## [1.0.2] - 2025-12-03

### Added
- **Props-based Initialization**: New initialization pattern for all controls using `props` dictionary parameter. Allows both traditional property assignment and dictionary-based setup for cleaner code.
  - Example: `Button(form, {'Text': 'Click', 'Left': 10, 'Top': 20, 'BackColor': 'blue'})`
- **Enhanced AutoSize Implementation**: Improved `_apply_autosize` method with better size calculation, MinimumSize/MaximumSize constraints, and parent notification for container resizing.
- **New Properties**: Added `Parent`, `ToolTipText` properties with proper getters/setters for better control hierarchy and tooltip management.
- **Property Setters**: Comprehensive `@property` decorators for Text, Visible, and other key properties across all controls.
- **Advanced Event Handling**: Enhanced event binding with better separation of concerns and improved callback management.

### Enhanced
- **ControlBase Class**: Extended with parent notification system for AutoSize, improved tooltip integration, and enhanced property management.
- **All Controls**: Updated initialization to support both traditional and props-based setup, with better default value handling.
- **Documentation**: More detailed Spanish docstrings and usage examples for all classes and methods.

### Changed
- **Initialization Pattern**: All control constructors now accept optional `props` parameter for dictionary-based configuration.
- **Property Management**: Improved consistency in property getters/setters across the library.
- **Code Organization**: Better separation of initialization logic and property setting.

### Fixed
- Improved AutoSize behavior with proper size constraints and parent container updates.
- Enhanced tooltip management and property synchronization.

## [1.0.1] - 2025-12-01

### Added
- **ToolTip Class**: New class for creating contextual tooltips that appear on mouse hover. Supports customizable text, delay, colors, fonts, and positioning.
- **Line Class**: New class for drawing lines on Canvas widgets, inspired by WPF/UWP System.Windows.Shapes.Line. Includes properties for coordinates, stroke color, thickness, dash patterns, and mouse/touch events.
- **StatusBarPanel Class**: New class representing individual panels within a status bar.
- **StatusBar Class**: New class for creating status bars with multiple panels at the bottom of forms.
- **AutoSize Support**: Enhanced ControlBase with AutoSize, MinimumSize, MaximumSize, and related properties for automatic control resizing based on content.
- **Integrated ToolTip Support**: Controls can now have tooltips associated directly through ControlBase properties (_tooltip_text, _tooltip_instance).
- **CSS Utilities**: Added support for CSS-to-Tkinter configuration functions (css_to_tkinter_config, apply_css_to_widget) for advanced styling.

### Enhanced
- **ControlBase Class**: Extended with AutoSize functionality and built-in tooltip management for better usability and VB.NET compatibility.
- **Event Handling**: Improved event binding and handling across controls, including simulation of touch/manipulation events in Line class.

### Fixed
- Minor improvements in event handling and property management.

### Changed
- Updated version number to 1.0.1.
- Enhanced documentation and comments for better maintainability.

## [1.0.0] - 2025-11-29

### Added
- Initial release of WinFormPy library.
- Complete mapping of Windows Forms/VB.NET syntax to Tkinter.
- Core controls: Button, Label, TextBox, ComboBox, ListBox, CheckBox, CheckedListBox, Panel, etc.
- Dialog classes: FileDialog, OpenFileDialog, SaveFileDialog, PrintDialog, MessageBox, InputBox.
- Advanced controls: PictureBox, ImageList, DataGridView, TreeView, TabControl, ProgressBar, etc.
- Utility classes: SendKeys, Timer, Screen, Point, Size, Rectangle.
- Form management: Form, MDIParent, MDIChild.
- VB-style properties and events for all controls.

### Technical Details
- Built on Python 3.7+ with Tkinter.
- Cross-platform desktop application development.
- VB.NET developer-friendly API.