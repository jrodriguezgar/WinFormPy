# WinFormPy Extended Controls

Advanced controls and enhanced versions of core components for complex UI scenarios.

## Module: `winformpy_extended.py`

### 1. ExtendedLabel
Label with automatic text wrapping and alignment.
- Handles paragraphs of text that need to fit within a specific width.
- Responds to window resizing.

### 2. ConsoleTextBox
Multi-colored text control optimized for logs and terminals.
- `WriteError`, `WriteWarning`, `WriteSuccess`, `WriteInfo`.
- Auto-scroll and MaxLines management.

### 3. PhotoImage Wrapper
Manage images without importing Tkinter directly.
- Scaling (subsample/zoom).
- Pixel-level manipulation.
- Base64 support.

### 4. Legacy WinUI Aliases
Compatibility layer for projects using older `WinUI*` prefixes.
