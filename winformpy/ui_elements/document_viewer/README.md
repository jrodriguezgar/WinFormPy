# Document Viewer UI Element

A comprehensive document viewer component for WinFormPy that supports multiple document formats including PDF, Word, images, and text files. Features a modern Windows 11-style toolbar with integrated settings management.

## Features

- **Document Operations**:
  - Printer Setup dialog (printer, driver, port, paper, quality)
  - Page Setup dialog (margins, orientation, paper size)
  - Print dialog (copies, page range, collation)
  - Print configuration with page range and copies

- **Navigation**:
  - Next/Previous page buttons
  - Jump to first/last page
  - Go to specific page
  - Page counter display with current/total pages

- **Viewing Options**:
  - Zoom in/out (25% - 200%)
  - Fit to width
  - Custom zoom levels
  - Scrollable view for large documents

- **Settings Management**:
  - Integrated Settings panel (toggle with button)
  - Real-time display of printer, page, and print settings
  - Persistent storage of all configurations
  - Visual feedback for active settings

- **Additional Features**:
  - Text extraction from pages
  - Document information display
  - Integrated toolbar with button groups
  - Customizable toolbar visibility
  - Modern Windows 11-style UI design
  - Menu bar with shortcuts (in UI form)
  - Status bar with document info
  - Keyboard shortcuts support

## Installation

### Required Dependencies

For full functionality, install the following libraries:

```bash
# For PDF support
pip install PyMuPDF

# For Word document support
pip install python-docx

# Image support (included with PIL/Pillow)
pip install Pillow
```

**Note**: The viewer will work with any format whose backend library is installed. If a library is missing, only that format will be unsupported.

## Components

### 1. DocumentViewerPanel

A reusable panel component that can be embedded in your forms.

```python
from winformpy.ui_elements.document_viewer import DocumentViewerPanel

# Create panel
panel = DocumentViewerPanel(parent_form)
panel.Dock = DockStyle.Fill

# Load document
panel.load_document('report.pdf')

# Events
panel.PageChanged = lambda s, e: print(f"Page: {e['page']}")
panel.DocumentLoaded = lambda s, e: print(f"Loaded: {e['file_path']}")
```

### 2. DocumentViewerForm

Standalone form with full menu bar and functionality.

```python
from winformpy.ui_elements.document_viewer import DocumentViewerForm

# Create viewer
viewer = DocumentViewerForm()
viewer.Show()

# Or open specific file
viewer = DocumentViewerForm()
viewer.open_document('document.pdf')
viewer.Show()
```

### 3. DocumentViewerDialog

Modal dialog for viewing documents.

```python
from winformpy.ui_elements.document_viewer import DocumentViewerDialog

# Show as modal dialog
dialog = DocumentViewerDialog(parent_form, 'report.pdf', 'View Report')
dialog.ShowDialog()
```

## Backends

The viewer uses a backend system to support different document formats:

### PDFBackend

For PDF documents using PyMuPDF (fitz).

```python
from winformpy.ui_elements.document_viewer import PDFBackend, DocumentViewerPanel

backend = PDFBackend()
panel = DocumentViewerPanel(parent_form, backend=backend)
panel.load_document('report.pdf')
```

### WordBackend

For Word documents using python-docx.

```python
from winformpy.ui_elements.document_viewer import WordBackend

backend = WordBackend()
panel = DocumentViewerPanel(parent_form, backend=backend)
panel.load_document('document.docx')
```

### ImageBackend

For image files.

```python
from winformpy.ui_elements.document_viewer import ImageBackend

backend = ImageBackend()
panel = DocumentViewerPanel(parent_form, backend=backend)
panel.load_document('diagram.png')
```

### TextBackend

For text files.

```python
from winformpy.ui_elements.document_viewer.document_backend import TextBackend

backend = TextBackend(lines_per_page=50)
panel = DocumentViewerPanel(parent_form, backend=backend)
panel.load_document('readme.txt')
```

## API Reference

### DocumentViewerPanel Methods

| Method | Description |
|--------|-------------|
| `load_document(file_path, backend=None)` | Load a document file |
| `next_page()` | Navigate to next page |
| `previous_page()` | Navigate to previous page |
| `go_to_first_page()` | Jump to first page |
| `go_to_last_page()` | Jump to last page |
| `go_to_page(page_number)` | Go to specific page (0-based) |
| `zoom_in()` | Increase zoom by 25% |
| `zoom_out()` | Decrease zoom by 25% |
| `set_zoom(zoom_percent)` | Set specific zoom level |
| `fit_to_width()` | Fit document to panel width |
| `get_current_page_text()` | Extract text from current page |
| `get_document_info()` | Get document metadata |
| `close_document()` | Close current document |
| `get_page_setup_settings()` | Get copy of page setup settings dictionary |
| `get_print_settings()` | Get copy of print settings dictionary |
| `set_page_setup_settings(settings)` | Update page setup settings from dictionary |
| `set_print_settings(settings)` | Update print settings from dictionary |

### DocumentViewerPanel Properties

| Property | Type | Description |
|----------|------|-------------|
| `ShowToolbar` | bool | Show/hide entire toolbar (default: True) |
| `ShowDocumentButtons` | bool | Show/hide document operation buttons (Printer, Page, Print) |
| `ShowNavigationButtons` | bool | Show/hide navigation buttons (First, Prev, Next, Last) |
| `ShowZoomButtons` | bool | Show/hide zoom buttons (Zoom In, Zoom Out) |
| `ShowViewButtons` | bool | Show/hide view buttons (Fit, Text, Settings) |
| `ShowSettingsPanel` | bool | Show/hide settings panel (toggle programmatically or via button) |
| `PrinterSettings` | PrinterSettings | Printer configuration object (from winformpy) |
| `page_setup_settings` | dict | Dictionary with page setup configuration (read/write) |
| `print_settings` | dict | Dictionary with print configuration (read/write) |

### Settings Management

**PrinterSettings Object:**

The viewer uses a `PrinterSettings` object from WinFormPy core library:

```python
# Direct property access
viewer.PrinterSettings.PrinterName = "Microsoft Print to PDF"
viewer.PrinterSettings.Copies = 5
viewer.PrinterSettings.Color = False  # Grayscale
viewer.PrinterSettings.Duplex = "Vertical"
viewer.PrinterSettings.Landscape = True
viewer.PrinterSettings.PaperSize = "A4"

# Validation
if viewer.PrinterSettings.IsValid:
    print("Printer exists")
if viewer.PrinterSettings.IsDefaultPrinter:
    print("Using default printer")

# Save/load as dictionary
settings_dict = viewer.PrinterSettings.to_dict()
viewer.PrinterSettings.from_dict(settings_dict)
```

For complete PrinterSettings documentation, see [PrinterSettings Guide](../../../guides/README_PrinterSettings.md).

**page_setup_settings** dictionary contains:
- `paper_size`: Paper size (e.g., 'Letter', 'A4') (default: 'Letter')
- `orientation`: 'Portrait' or 'Landscape' (default: 'Portrait')
- `margin_left`: Left margin in inches (default: 1.0)
- `margin_right`: Right margin in inches (default: 1.0)
- `margin_top`: Top margin in inches (default: 1.0)
- `margin_bottom`: Bottom margin in inches (default: 1.0)

**print_settings** contains:
- `printer_name`: Name of the printer (default: 'Default Printer')
- `document_name`: Document name for printing (default: '')
- `copies`: Number of copies (default: 1)
- `print_range`: 'All', 'Selection', or 'Pages' (default: 'All')
- `from_page`: Starting page number (default: 1)
- `to_page`: Ending page number (default: 1)
- `collate`: Boolean for collation (default: True)

### Events

| Event | Description | Event Data |
|-------|-------------|------------|
| `PageChanged` | Fired when page changes | `{'page': int}` |
| `DocumentLoaded` | Fired when document loads | `{'file_path': str}` |
| `ZoomChanged` | Fired when zoom changes | `{'zoom': int}` |

## Complete Example

```python
from winformpy import Form, Panel, Button, DockStyle, Application
from winformpy.ui_elements.document_viewer import DocumentViewerPanel

class MyDocumentForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "My Document Viewer"
        self.Width = 1024
        self.Height = 768
        
        self.ApplyLayout()
        
        # Add viewer panel
        self.viewer = DocumentViewerPanel(self, {
            'Dock': DockStyle.Fill
        })
        
        # Optional: Customize toolbar visibility
        # self.viewer.ShowDocumentButtons = False  # Hide Printer, Page and Print
        # self.viewer.ShowZoomButtons = False      # Hide zoom controls
        # self.viewer.ShowViewButtons = False      # Hide Fit, Text, Settings
        # self.viewer.ShowToolbar = False          # Hide entire toolbar
        
        # Optional: Show settings panel programmatically
        # self.viewer.ShowSettingsPanel = True  # Display settings on the right
        
        # Optional: Access and modify printer settings via PrinterSettings object
        # self.viewer.PrinterSettings.Color = False  # Set to grayscale
        # self.viewer.PrinterSettings.Copies = 5
        # self.viewer.PrinterSettings.Duplex = "Vertical"
        
        # Or save/load settings as dictionary
        # settings_dict = self.viewer.PrinterSettings.to_dict()
        # self.viewer.PrinterSettings.from_dict(settings_dict)
        
        # page_setup = self.viewer.get_page_setup_settings()
        # page_setup['orientation'] = 'Landscape'
        # self.viewer.set_page_setup_settings(page_setup)
        
        # print_settings = self.viewer.get_print_settings()
        # print_settings['copies'] = 2
        # self.viewer.set_print_settings(print_settings)
        
        # Connect events
        
        # Optional: Access settings programmatically
        # page_setup = self.viewer.get_page_setup_settings()
        # print_settings = self.viewer.get_print_settings()
        
        # self.viewer.ShowDocumentButtons = False  # Hide Page Setup and Print
        # self.viewer.ShowZoomButtons = False      # Hide zoom controls
        # self.viewer.ShowToolbar = False          # Hide entire toolbar
        
        # Connect events
        self.viewer.PageChanged = self.on_page_changed
        self.viewer.DocumentLoaded = self.on_document_loaded
        
        # Add custom toolbar (for Open button, etc.)
        toolbar = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 40
        })
        
        btn_open = Button(toolbar, {
            'Text': 'Open PDF',
            'Left': 10,
            'Top': 5,
            'Width': 100
        })
        btn_open.Click = lambda s, e: self.viewer.load_document('sample.pdf')
    
    def on_page_changed(self, sender, e):
        print(f"Now viewing page {e['page'] + 1}")
    
    def on_document_loaded(self, sender, e):
        print(f"Loaded: {e['file_path']}")

# Run
form = MyDocumentForm()
Application.Run(form)
```

## Custom Backend

You can create custom backends for other document types:

```python
from winformpy.ui_elements.document_viewer.document_backend import DocumentBackend
from PIL import Image

class MyCustomBackend(DocumentBackend):
    def load_document(self, file_path: str) -> bool:
        # Load your custom format
        return True
    
    def get_page_count(self) -> int:
        return self.page_count
    
    def render_page(self, page_number: int, width=None, height=None) -> Image.Image:
        # Render page as PIL Image
        img = Image.new('RGB', (600, 800), 'white')
        return img
    
    def get_page_text(self, page_number: int) -> str:
        # Extract text
        return "Page text"
```

## UI Design Guidelines

The Document Viewer follows Windows 11 design principles:

- **Toolbar**: Light gray background (#f3f3f3), 45px height
- **Buttons**: White background (#ffffff), dark text (#333333), 1px border, 28px height
- **Labels**: Medium gray text (#555555), Segoe UI 9pt font
- **Separators**: Light gray (#cccccc) vertical bars (│)
- **Status Bar**: Matches toolbar color, 28px height, bordered
- **Settings Panel**: Very light gray (#fafafa), 300px width when visible
- **Active States**: Pressed buttons use light gray (#e0e0e0)

### Button Sizes and Spacing

- Document buttons: 75-90px width
- Navigation buttons: 38px width (compact)
- Zoom buttons: 45px width
- View buttons: 65-80px width
- Spacing between buttons: 5-7px
- Group separators: ~15-20px spacing

## Best Practices

1. **Loading Documents**: Always check the return value of `load_document()` and handle failures gracefully
2. **Settings Management**: Use the getter/setter methods rather than directly modifying dictionaries
3. **Toolbar Customization**: Hide button groups that aren't needed for your use case
4. **Settings Panel**: Use the integrated button rather than external controls for consistency
5. **Events**: Connect to PageChanged, DocumentLoaded, and ZoomChanged for state synchronization
6. **Backend Selection**: Let the panel auto-detect backends, or specify one for better control

## Notes

- Auto-detection of document format is based on file extension
- Missing backend libraries will result in an error message when trying to open unsupported formats
- Large documents may take time to render; consider adding loading indicators
- Text extraction quality depends on the document format and backend
- Word documents are rendered as text-based images (simplified rendering)

## Troubleshooting

### "PyMuPDF not found"
```bash
pip install PyMuPDF
```

### "python-docx not found"
```bash
pip install python-docx
```

### "Failed to render page"
- Check that the file is not corrupted
- Ensure the backend library is properly installed
- Try a different zoom level or page
