# WinFormPy Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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