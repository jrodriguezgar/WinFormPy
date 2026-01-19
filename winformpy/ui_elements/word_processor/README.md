# Word Processor UI Element

A complete word processor component for WinFormPy, built on the enhanced `RichTextBox` control following Windows Forms standards.

## Overview

The Word Processor UI Element provides a full-featured text editor with:

- **Rich Text Editing**: Bold, Italic, Underline, Strikethrough
- **Font Control**: Font family and size selection
- **Color Options**: Text color and highlight color
- **Text Alignment**: Left, Center, Right
- **Find & Replace**: Search and replace functionality
- **Status Bar**: Word count, character count, line count, cursor position
- **File Operations**: New, Open, Save, Save As (RTF and Plain Text)
- **RTF Support**: Full RTF format read/write

## Components

### WordProcessorPanel

The main editing component that can be embedded in any form or panel.

```python
from winformpy.ui_elements.word_processor import WordProcessorPanel
from winformpy import RichTextBoxStreamType

# Create word processor panel
processor = WordProcessorPanel(form, {
    'Dock': DockStyle.Fill,
    'ShowToolbar': True,
    'ShowStatusBar': True,
    'DefaultFont': 'Segoe UI',
    'DefaultFontSize': 11
})

# Access text content
plain_text = processor.Text        # Plain text (Windows Forms standard)
rtf_content = processor.Rtf        # RTF format (Windows Forms standard)

# Set content
processor.Text = "Hello World"
processor.Rtf = r"{\rtf1\ansi Hello \b World\b0}"

# File operations with RTF support
processor.Open("document.rtf")                                    # Auto-detect
processor.Open("document.rtf", RichTextBoxStreamType.RichText)    # Force RTF
processor.SaveAs("output.rtf", RichTextBoxStreamType.RichText)    # Save as RTF
```

### WordProcessorForm (WordUI)

A complete WordPad-style word processor application with full menu bar, quick access toolbar, and extended status bar.

**Features:**
- **Full Menu Bar**: File, Edit, Insert, Format, View, Help
- **Quick Access Toolbar**: New, Open, Save, Undo, Redo, Print, Find
- **Extended Status Bar**: Zoom control (50%-500%), Word Wrap indicator
- **Recent Files**: Tracks up to 10 recently opened files
- **Insert Date/Time**: Multiple date/time formats
- **View Toggles**: Toolbar, Format Bar, Status Bar, Word Wrap visibility

```python
from winformpy.ui_elements.word_processor import WordProcessorForm
from winformpy import Application

# Create and run WordUI application
form = WordProcessorForm()
Application.Run(form)

# Or with custom properties
form = WordProcessorForm({
    'Text': 'My Document Editor',
    'Width': 1200,
    'Height': 900
})
Application.Run(form)
```

## Windows Forms Standard Properties

### Text Properties (following .NET RichTextBox)

| Property         | Type | Description                                             |
| ---------------- | ---- | ------------------------------------------------------- |
| `Text`         | str  | Gets/sets document plain text (no formatting)           |
| `Rtf`          | str  | Gets/sets document in RTF format with colors/formatting |
| `SelectedText` | str  | Gets/sets selected plain text                           |
| `SelectedRtf`  | str  | Gets/sets selected text in RTF format                   |

### Document Properties

| Property          | Type        | Description                        |
| ----------------- | ----------- | ---------------------------------- |
| `FilePath`      | str         | Gets the current file path         |
| `DocumentTitle` | str         | Gets the document title            |
| `IsModified`    | bool        | Gets/sets the modified state       |
| `ReadOnly`      | bool        | Gets/sets read-only mode           |
| `Editor`        | RichTextBox | Gets the underlying editor control |

### Statistics Properties

| Property           | Type | Description              |
| ------------------ | ---- | ------------------------ |
| `WordCount`      | int  | Gets the word count      |
| `CharacterCount` | int  | Gets the character count |
| `LineCount`      | int  | Gets the line count      |

### Configuration Properties

| Property            | Default    | Description                  |
| ------------------- | ---------- | ---------------------------- |
| `ShowToolbar`     | True       | Show/hide formatting toolbar |
| `ShowStatusBar`   | True       | Show/hide status bar         |
| `ShowFindBar`     | False      | Show/hide find bar on start  |
| `DefaultFont`     | 'Segoe UI' | Default font family          |
| `DefaultFontSize` | 11         | Default font size            |
| `EditorBackColor` | '#FFFFFF'  | Editor background color      |
| `EditorForeColor` | '#000000'  | Editor text color            |

## Enums

### RichTextBoxStreamType

Specifies the format for file operations:

```python
from winformpy import RichTextBoxStreamType

# Available values:
RichTextBoxStreamType.RichText          # RTF format
RichTextBoxStreamType.PlainText         # Plain text
RichTextBoxStreamType.RichNoOleObjs     # RTF without OLE objects
RichTextBoxStreamType.TextTextOleObjs   # Plain text with OLE text
RichTextBoxStreamType.UnicodePlainText  # Unicode plain text
```

### RichTextBoxFinds

Specifies search options for the `Find` method:

```python
from winformpy import RichTextBoxFinds

# Available values (can be combined with |):
RichTextBoxFinds.None_         # Default search
RichTextBoxFinds.WholeWord     # Match whole words only
RichTextBoxFinds.MatchCase     # Case-sensitive search
RichTextBoxFinds.NoHighlight   # Don't highlight found text
RichTextBoxFinds.Reverse       # Search backwards
```

## Events

| Event                | Description                         |
| -------------------- | ----------------------------------- |
| `DocumentChanged`  | Fired when document content changes |
| `DocumentSaved`    | Fired when document is saved        |
| `DocumentOpened`   | Fired when a document is opened     |
| `SelectionChanged` | Fired when text selection changes   |
| `ModifiedChanged`  | Fired when modified state changes   |

## Methods

### Document Operations

```python
# Create new document
processor.New()

# Open a file (auto-detects format from extension)
processor.Open("document.rtf")

# Open with explicit format
processor.Open("document.rtf", RichTextBoxStreamType.RichText)
processor.Open("document.txt", RichTextBoxStreamType.PlainText)

# Save current document
processor.Save()

# Save with new name (auto-detects format from extension)
processor.SaveAs("output.rtf")

# Save with explicit format
processor.SaveAs("output.rtf", RichTextBoxStreamType.RichText)
```

### Text Operations

```python
# Write text
processor.Write("Hello ", '#FF0000')
processor.WriteLine("World!", '#0000FF')

# Append text
processor.AppendText("More text")

# Clear document
processor.Clear()
```

### Clipboard Operations

```python
processor.Cut()
processor.Copy()
processor.Paste()
processor.SelectAll()
processor.Undo()
processor.Redo()
```

## RichTextBox Properties (Windows Forms Standard)

The underlying `RichTextBox` control follows Windows Forms conventions:

### Text Properties

```python
rtb = processor.Editor

# Plain text (Windows Forms standard)
text = rtb.Text

# RTF format (Windows Forms standard)
rtf = rtb.Rtf
rtb.Rtf = r"{\rtf1\ansi Hello \b Bold\b0}"

# Selection
selected = rtb.SelectedText
selected_rtf = rtb.SelectedRtf
```

### Selection Properties

```python
# Selection position and length
rtb.SelectionStart = 10
rtb.SelectionLength = 5

# Selection formatting
rtb.SelectionBold = True
rtb.SelectionItalic = True
rtb.SelectionUnderline = True
rtb.SelectionStrikethrough = True
rtb.SelectionColor = '#FF0000'
rtb.SelectionBackColor = '#FFFF00'
rtb.SelectionFont = Font('Arial', 14)
rtb.SelectionAlignment = 'center'
```

### Find Method (Windows Forms Standard)

```python
# Simple find
pos = rtb.Find("search text", 0)

# Find with options
pos = rtb.Find("Word", 0, RichTextBoxFinds.WholeWord | RichTextBoxFinds.MatchCase)

# Find backwards
pos = rtb.Find("text", 100, RichTextBoxFinds.Reverse)

# Find and Replace
count = rtb.FindAndReplace("old", "new", replace_all=True)
```

### File Operations (Windows Forms Standard)

```python
# Load file (auto-detects from extension)
rtb.LoadFile("document.rtf")

# Load with explicit format
rtb.LoadFile("document.rtf", RichTextBoxStreamType.RichText)

# Save file
rtb.SaveFile("output.rtf", RichTextBoxStreamType.RichText)
rtb.SaveFile("output.txt", RichTextBoxStreamType.PlainText)
```

### Line and Character Properties

```python
lines = rtb.Lines           # Get as array
rtb.Lines = ['Line 1', 'Line 2']  # Set from array
count = rtb.LineCount       # Get line count
length = rtb.TextLength     # Get character count

# Position methods
line = rtb.GetLineFromCharIndex(50)    # Get line number from char index
pos = rtb.GetPositionFromCharIndex(50) # Get x,y position
idx = rtb.GetFirstCharIndexFromLine(5) # Get char index from line number
text = rtb.GetLineText(3)              # Get text of line 3
```

### Navigation

```python
rtb.ScrollToEnd()
rtb.ScrollToStart()
rtb.ScrollToLine(10)
rtb.ScrollToCaret()
rtb.GoToLine(5)
```

## Keyboard Shortcuts

### File Operations

| Shortcut       | Action        |
| -------------- | ------------- |
| Ctrl+N         | New document  |
| Ctrl+O         | Open document |
| Ctrl+S         | Save document |
| Ctrl+Shift+S   | Save As       |
| Ctrl+P         | Print         |

### Edit Operations

| Shortcut | Action                |
| -------- | --------------------- |
| Ctrl+Z   | Undo                  |
| Ctrl+Y   | Redo                  |
| Ctrl+X   | Cut                   |
| Ctrl+C   | Copy                  |
| Ctrl+V   | Paste                 |
| Ctrl+A   | Select all            |
| Ctrl+F   | Show find bar         |
| Ctrl+H   | Show find/replace bar |
| F3       | Find next             |
| F5       | Insert Date/Time      |
| Del      | Delete selected       |

### Format Operations

| Shortcut | Action           |
| -------- | ---------------- |
| Ctrl+B   | Toggle bold      |
| Ctrl+I   | Toggle italic    |
| Ctrl+U   | Toggle underline |
| Ctrl+L   | Align left       |
| Ctrl+E   | Center           |
| Ctrl+R   | Align right      |

### View Operations

| Shortcut | Action   |
| -------- | -------- |
| Ctrl++   | Zoom in  |
| Ctrl+-   | Zoom out |

### Help

| Shortcut | Action         |
| -------- | -------------- |
| F1       | Help topics    |
| Escape   | Close find bar |

## Example Usage

### Basic Word Processor with RTF Support

```python
from winformpy import Form, DockStyle, RichTextBoxStreamType
from winformpy.ui_elements.word_processor import WordProcessorPanel

# Create form
form = Form({'Text': 'My Word Processor', 'Width': 1024, 'Height': 768})
form.ApplyLayout()

# Add word processor
processor = WordProcessorPanel(form, {
    'Dock': DockStyle.Fill,
    'DefaultFont': 'Calibri',
    'DefaultFontSize': 12
})

# Handle save event
def on_save(sender, e):
    print(f"Document saved: {processor.FilePath}")
    print(f"RTF content length: {len(processor.Rtf)}")

processor.DocumentSaved = on_save

# Open RTF file
processor.Open("document.rtf", RichTextBoxStreamType.RichText)

form.Show()
```

### Get RTF Content

```python
# Get plain text
plain_text = processor.Text

# Get RTF with formatting
rtf_content = processor.Rtf

# Get selected text RTF
selected_rtf = processor.SelectedRtf

# Save as RTF
processor.SaveAs("output.rtf", RichTextBoxStreamType.RichText)
```

### Log Viewer with RichTextBox

```python
from winformpy import Form, RichTextBox, DockStyle

form = Form({'Text': 'Log Viewer', 'Width': 800, 'Height': 600})
form.ApplyLayout()

log = RichTextBox(form, {
    'Dock': DockStyle.Fill,
    'BackColor': '#1E1E1E',
    'ForeColor': '#CCCCCC',
    'ReadOnly': True,
    'MaxLines': 1000
})

# Add log entries with colors
log.WriteInfo("Application started")
log.WriteSuccess("Connection established")
log.WriteWarning("Cache miss - using fallback")
log.WriteError("Failed to load config")
log.WriteLine("Normal message")

# Get RTF for export
rtf_log = log.Rtf

form.Show()
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        UI Layer                                  │
│    WordProcessorPanel (embeddable) / WordProcessorForm (full)   │
│                                                                  │
│  ┌─────────────┐  ┌─────────────────────────────────────────┐  │
│  │  Toolbar    │  │              RichTextBox                 │  │
│  │  [B][I][U]  │  │            (Editor Area)                 │  │
│  │  Font/Size  │  │                                          │  │
│  └─────────────┘  └─────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Primitives Layer                               │
│                 WordProcessorPrimitives                          │
│                                                                  │
│  • File I/O (load, save)       • Undo/Redo management           │
│  • Text operations             • Search/Replace                  │
│  • Line operations             • Text statistics                 │
│  • Format operations           • Document info                   │
└─────────────────────────────────────────────────────────────────┘
```

## Files

| File | Description |
|------|-------------|
| `word_processor_primitives.py` | Low-level text and file operations |
| `word_processor_panel.py` | Embeddable word processor component |
| `word_processor_ui.py` | Standalone WordUI form |
| `__init__.py` | Package exports |
| `README.md` | Documentation |

## Primitives Layer

The primitives layer provides low-level text operations that can be used independently or by the UI components.

### WordProcessorPrimitives

```python
from winformpy.ui_elements.word_processor import (
    WordProcessorPrimitives, FileFormat, SearchOptions
)

# Create primitives instance
primitives = WordProcessorPrimitives()

# File operations
primitives.load_file("document.txt")
primitives.save_file("output.txt", FileFormat.PLAIN_TEXT)

# Text operations
primitives.insert_text("Hello ", 0)
primitives.append_text("World!")
text = primitives.get_text(0, 6)  # "Hello "

# Search and replace
result = primitives.find("World")
if result:
    print(f"Found at position {result.start}")

count = primitives.replace_all("old", "new")
print(f"Replaced {count} occurrences")

# Undo/Redo
if primitives.can_undo():
    primitives.undo()

# Statistics
stats = primitives.get_statistics()
print(f"Words: {stats.word_count}, Lines: {stats.line_count}")
```

### Data Classes

```python
from winformpy.ui_elements.word_processor import (
    TextRange, TextFormat, SearchResult, DocumentInfo, TextStatistics
)

# TextRange - Represents a text range
range_ = TextRange(start=0, end=10, text="Hello World")
print(range_.length)  # 10

# DocumentInfo - Document metadata
info = DocumentInfo(
    file_path="/path/to/file.txt",
    title="My Document",
    is_modified=False
)

# TextStatistics - Text analysis
stats = TextStatistics(
    word_count=100,
    character_count=500,
    line_count=10
)
```

### Enums

```python
from winformpy.ui_elements.word_processor import (
    FileFormat, TextAlignment, TextStyle, SearchOptions
)

# FileFormat
FileFormat.PLAIN_TEXT   # Plain text (.txt)
FileFormat.RICH_TEXT    # Rich text (.rtf)
FileFormat.HTML         # HTML format
FileFormat.AUTO         # Auto-detect from extension

# TextAlignment
TextAlignment.LEFT
TextAlignment.CENTER
TextAlignment.RIGHT
TextAlignment.JUSTIFY

# TextStyle (can be combined with |)
TextStyle.BOLD | TextStyle.ITALIC | TextStyle.UNDERLINE

# SearchOptions (can be combined with |)
SearchOptions.MATCH_CASE | SearchOptions.WHOLE_WORD
SearchOptions.REGEX
SearchOptions.REVERSE
```

---

## UI Layer

### WordProcessorForm (WordUI)
