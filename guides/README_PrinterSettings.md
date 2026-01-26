# PrinterSettings Class

`PrinterSettings` is a class in WinFormPy that specifies information about how a document is printed, including the printer that prints it. This mirrors the functionality of `System.Drawing.Printing.PrinterSettings` from .NET Windows Forms.

## Table of Contents

- [Overview](#overview)
- [Class Features](#class-features)
- [Properties](#properties)
- [Static Methods](#static-methods)
- [Instance Methods](#instance-methods)
- [Usage Examples](#usage-examples)
- [Integration with Dialogs](#integration-with-dialogs)
- [Dictionary Support](#dictionary-support)

## Overview

The `PrinterSettings` class provides a comprehensive way to manage printer configurations in your WinFormPy applications. It supports:

- ✅ Accessing installed printers
- ✅ Getting/setting printer properties
- ✅ Validating printer availability
- ✅ Dictionary serialization/deserialization
- ✅ Integration with `PrintDialog` and `PageSetupDialog`
- ✅ Cloning settings

## Class Features

### Key Capabilities

1. **Printer Discovery** - Enumerate all installed printers on the system
2. **Settings Management** - Configure print options (copies, duplex, color, etc.)
3. **Validation** - Check if a printer exists and is available
4. **Persistence** - Convert to/from dictionaries for saving to JSON, databases, etc.
5. **Integration** - Works seamlessly with `PrintDialog` and `PageSetupDialog`

## Properties

All properties are read/write unless marked otherwise.

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `PrinterName` | str | Default printer | Name of the printer to use |
| `Copies` | int | 1 | Number of copies to print |
| `Duplex` | str | "Simplex" | Duplex mode: "Simplex", "Vertical", "Horizontal" |
| `Collate` | bool | False | Whether to collate copies |
| `FromPage` | int | 1 | Starting page number when printing a range |
| `ToPage` | int | 9999 | Ending page number when printing a range |
| `PrintToFile` | bool | False | Whether to print to a file instead of printer |
| `Color` | bool | True | True for color printing, False for grayscale |
| `PrintRange` | str | "AllPages" | "AllPages", "Selection", "CurrentPage", "SomePages" |
| `PaperSource` | str | "AutomaticFeed" | Paper source tray |
| `PaperSize` | str | "A4" | Paper size (e.g., "Letter", "A4", "Legal") |
| `Landscape` | bool | False | True for landscape orientation, False for portrait |
| `IsDefaultPrinter` | bool | (Read-only) | True if this is the default printer |
| `IsValid` | bool | (Read-only) | True if the printer exists on the system |
| `CanDuplex` | bool | (Read-only) | True if printer supports duplex printing |
| `SupportsColor` | bool | (Read-only) | True if printer supports color printing |

## Static Methods

### `GetInstalledPrinters()`

Returns a list of names of all printers installed on the computer.

```python
from winformpy.winformpy import PrinterSettings

printers = PrinterSettings.GetInstalledPrinters()
for printer in printers:
    print(printer)

# Output example:
# Microsoft Print to PDF
# Microsoft XPS Document Writer
# HP LaserJet Pro
```

**Requires:** `pywin32` package for Windows (`pip install pywin32`)  
**Fallback:** If `pywin32` not available, returns common Windows printers

### `GetDefaultPrinterName()`

Gets the name of the default printer.

```python
default_printer = PrinterSettings.GetDefaultPrinterName()
print(f"Default printer: {default_printer}")

# Output: Default printer: Microsoft Print to PDF
```

## Instance Methods

### `__init__(settings_dict=None)`

Constructor. Can optionally initialize from a dictionary.

```python
# Create with defaults
ps = PrinterSettings()

# Create from dictionary
settings = {
    'PrinterName': 'Microsoft Print to PDF',
    'Copies': 2,
    'Color': False
}
ps = PrinterSettings(settings)
```

### `from_dict(settings_dict)`

Load settings from a dictionary.

```python
ps = PrinterSettings()
ps.from_dict({
    'PrinterName': 'HP LaserJet',
    'Copies': 5,
    'Duplex': 'Vertical',
    'Collate': True
})
```

### `to_dict()`

Convert settings to a dictionary. Returns all properties as a dictionary.

```python
ps = PrinterSettings()
ps.Copies = 3
ps.Duplex = 'Horizontal'

settings_dict = ps.to_dict()
# Result: {'PrinterName': '...', 'Copies': 3, 'Duplex': 'Horizontal', ...}

# Save to JSON
import json
with open('printer_config.json', 'w') as f:
    json.dump(settings_dict, f)
```

### `Clone()`

Creates an independent copy of the PrinterSettings.

```python
original = PrinterSettings()
original.Copies = 10

clone = original.Clone()
clone.Copies = 99

print(original.Copies)  # 10
print(clone.Copies)     # 99
```

## Usage Examples

### Basic Usage

```python
from winformpy.winformpy import PrinterSettings

# Create settings
ps = PrinterSettings()
ps.PrinterName = "Microsoft Print to PDF"
ps.Copies = 3
ps.Duplex = "Vertical"
ps.Color = False
ps.Landscape = True

print(f"Printing to: {ps.PrinterName}")
print(f"Copies: {ps.Copies}")
print(f"Valid: {ps.IsValid}")
```

### Validate Printer Availability

```python
ps = PrinterSettings()
ps.PrinterName = "My Fancy Printer"

if ps.IsValid:
    print("Printer is available")
else:
    print("Printer not found!")
    print("Available printers:")
    for printer in PrinterSettings.GetInstalledPrinters():
        print(f"  - {printer}")
```

### Select Default Printer

```python
ps = PrinterSettings()
# Already initialized with default printer

if ps.IsDefaultPrinter:
    print(f"{ps.PrinterName} is the default printer")
```

## Integration with Dialogs

### Using with PrintDialog

```python
from winformpy.winformpy import PrintDialog, PrinterSettings

# Create settings
printer_settings = PrinterSettings()
printer_settings.Copies = 5
printer_settings.Duplex = "Vertical"

# Use with PrintDialog
dialog = PrintDialog()
dialog.PrinterSettings = printer_settings
dialog.AllowSomePages = True

if dialog.ShowDialog() == 'OK':
    # Get updated settings from dialog
    updated_settings = dialog.PrinterSettings
    print(f"Selected printer: {updated_settings.PrinterName}")
    print(f"Copies: {updated_settings.Copies}")
```

### Using with PageSetupDialog

```python
from winformpy.winformpy import PageSetupDialog, PrinterSettings

printer_settings = PrinterSettings()
printer_settings.PaperSize = "A4"
printer_settings.Landscape = True

dialog = PageSetupDialog()
dialog.PrinterSettings = printer_settings

if dialog.ShowDialog() == 'OK':
    updated_settings = dialog.PrinterSettings
    print(f"Paper size: {updated_settings.PaperSize}")
    print(f"Landscape: {updated_settings.Landscape}")
```

## Dictionary Support

### Save to Configuration File

```python
import json
from winformpy.winformpy import PrinterSettings

# Configure settings
ps = PrinterSettings()
ps.PrinterName = "HP LaserJet"
ps.Copies = 2
ps.Duplex = "Vertical"
ps.Color = True

# Save to JSON
config = {
    'printer': ps.to_dict(),
    'app_name': 'My Application'
}

with open('config.json', 'w') as f:
    json.dump(config, f, indent=2)
```

### Load from Configuration File

```python
import json
from winformpy.winformpy import PrinterSettings

# Load from JSON
with open('config.json', 'r') as f:
    config = json.load(f)

# Restore settings
ps = PrinterSettings(config['printer'])

print(f"Loaded printer: {ps.PrinterName}")
print(f"Copies: {ps.Copies}")
```

### Document Viewer Integration

```python
from winformpy.ui_elements.document_viewer import DocumentViewerPanel

# Create viewer
viewer = DocumentViewerPanel(parent_form)

# Get PrinterSettings object (automatic conversion)
ps = viewer.printer_settings_obj

# Modify settings
ps.Copies = 5
ps.Duplex = "Horizontal"

# Or use dictionary interface (legacy support)
settings_dict = viewer.get_printer_settings()
settings_dict['Copies'] = 10
viewer.set_printer_settings(settings_dict)
```

## Best Practices

1. **Validate Printer Names** - Always check `IsValid` before printing
   ```python
   if ps.IsValid:
       # OK to print
   else:
       # Show error or select different printer
   ```

2. **Use Dictionary Format for Persistence** - Save/load from JSON or database
   ```python
   # Save
   config = ps.to_dict()
   save_to_database(config)
   
   # Load
   config = load_from_database()
   ps = PrinterSettings(config)
   ```

3. **Clone for Comparison** - Create copies when comparing settings
   ```python
   original = PrinterSettings()
   modified = original.Clone()
   modified.Copies = 99
   # original unchanged
   ```

4. **Check Default Printer** - Use default when user hasn't selected
   ```python
   ps = PrinterSettings()  # Uses default
   if not ps.IsDefaultPrinter:
       ps.PrinterName = PrinterSettings.GetDefaultPrinterName()
   ```

5. **Integrate with Dialogs** - Let users configure via UI
   ```python
   dialog = PrintDialog()
   dialog.PrinterSettings = my_settings
   if dialog.ShowDialog() == 'OK':
       my_settings = dialog.PrinterSettings
   ```

## Complete Example

See [examples/printersettings_example.py](../examples/printersettings_example.py) for a complete working example demonstrating all features.

## Dependencies

- **Optional:** `pywin32` - For real printer enumeration on Windows
  ```bash
  pip install pywin32
  ```
  
  If not installed, falls back to common printer names.

## See Also

- [PrintDialog](../winformpy/winformpy.py) - Dialog for selecting print options
- [PageSetupDialog](../winformpy/winformpy.py) - Dialog for page layout settings
- [Document Viewer Panel](../winformpy/ui_elements/document_viewer/README.md) - Integrated document viewer with printing
