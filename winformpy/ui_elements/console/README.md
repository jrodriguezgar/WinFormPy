# 🖥️ Console UI Module

A terminal-style console interface component for WinFormPy applications with a pluggable I/O layer architecture.

> ⚠️ **Architecture-agnostic**: This component uses a **pluggable I/O layer**. You provide the command processing backend (local handlers, shell execution, remote API, etc.).

> **📦 Component Structure**: This module provides:
> - `ConsolePanel` - Embeddable panel for any Form/Panel
> - `ConsoleForm` - Standalone form that **uses ConsolePanel internally** (access via `.console` property)

## Quick Demo

Run the built-in demo to see the component in action:

```bash
# Embeddable console panel demo
python winformpy/ui_elements/console/console_panel.py
```

## 📖 Overview

This module provides a customizable console/terminal component with:

### Core Features
- ✅ Terminal-style text output area
- ✅ Command input with Enter to submit
- ✅ Command history (Up/Down arrows)
- ✅ Customizable font (family, size, style)
- ✅ Customizable colors (foreground and background)
- ✅ Multiple color output methods (Write, WriteError, WriteWarning, etc.)
- ✅ Predefined themes (dark, light, matrix, retro, blue, powershell, ubuntu)
- ✅ Maximum line buffer management
- ✅ **Pluggable I/O layer** for different command processing backends

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│  ConsoleForm (Complete Form)                        │
│  - Toolbar with font/size/theme selectors           │
│  - Color picker buttons                             │
│  - Toggle command panel                             │
├─────────────────────────────────────────────────────┤
│  ConsolePanel (Embeddable Panel)                    │
│  - Scrollable output area                           │
│  - Command input with prompt                        │
│  - Command history support                          │
│  - Color-coded output methods                       │
├─────────────────────────────────────────────────────┤
│  ConsoleIO (I/O Layer - Pluggable)                  │
│  - LocalConsoleIO (command handlers)                │
│  - SubprocessConsoleIO (shell execution)            │
│  - CallbackConsoleIO (simple callback)              │
│  - Custom implementations                           │
└─────────────────────────────────────────────────────┘
```

---

## 📦 Components

| Component | Type | Description |
|-----------|------|-------------|
| `ConsoleForm` | Form | Complete terminal window with toolbar |
| `ConsolePanel` | Panel | Embeddable console widget |
| `ConsoleIOBackend` | ABC | Abstract base for I/O implementations |
| `LocalConsoleIO` | I/O | Local command processing with decorators |
| `SubprocessConsoleIO` | I/O | Execute shell commands |
| `CallbackConsoleIO` | I/O | Simple callback-based processing |

---

## 🚀 Quick Start

### Option 1: Legacy Callback Style (Simple)

```python
from winformpy import Form, Application, DockStyle
from winformpy.ui_elements.console import ConsolePanel

form = Form({'Text': 'Console', 'Width': 800, 'Height': 600})
form.ApplyLayout()

console = ConsolePanel(form, {'Dock': DockStyle.Fill})

# Handle commands with callback
def handle_command(sender, command):
    if command == "help":
        console.WriteLine("Commands: help, clear, exit")
    elif command == "clear":
        console.Clear()
    elif command == "exit":
        form.Close()
    else:
        console.WriteWarning(f"Unknown: {command}")

console.CommandReceived = handle_command
console.WriteLine("Type 'help' for commands.")

Application.Run(form)
```

### Option 2: I/O Layer with Decorators (Recommended)

```python
from winformpy import Form, Application, DockStyle
from winformpy.ui_elements.console import ConsolePanel, LocalConsoleIO

form = Form({'Text': 'Console', 'Width': 800, 'Height': 600})
form.ApplyLayout()

# Create I/O layer
io = LocalConsoleIO()

# Create console with I/O layer
console = ConsolePanel(form, {
    'Dock': DockStyle.Fill,
    'ConsoleIO': io
})

# Register commands with decorators
@io.command('help', aliases=['?', 'h'])
```

### Customizing with Sub-Properties

ConsolePanel supports sub-properties for fine-tuning internal WinFormPy controls:

```python
from winformpy import Form, Application, DockStyle, Font, FontStyle
from winformpy.ui_elements.console import ConsolePanel

form = Form({'Text': 'Custom Console', 'Width': 800, 'Height': 600})
form.ApplyLayout()

console = ConsolePanel(form, {
    'Dock': DockStyle.Fill,
    'BackColor': '#1E1E1E',
    'ForeColor': '#CCCCCC',
    'FontFamily': 'Consolas',
    'FontSize': 12,
    'Prompt': '>>> ',
    
    # Sub-properties for internal controls
    'OutputArea': {
        'BackColor': '#0C0C0C',
        'ForeColor': '#00FF00',
        'Padding': 12,
        'MaxLines': 2000,
        'SelectionBackColor': '#3A3A3A'
    },
    'InputArea': {
        'Height': 35,
        'BackColor': '#1A1A1A'
    },
    'PromptLabel': {
        'ForeColor': '#FFFF00',
        'Font': Font('Consolas', 12, FontStyle.Bold)
    },
    'InputBox': {
        'BackColor': '#1A1A1A',
        'ForeColor': '#FFFFFF'
    }
})

Application.Run(form)
```

#### Available Sub-Properties

| Sub-Property | Keys | Description |
|--------------|------|-------------|
| `OutputArea` | `BackColor`, `ForeColor`, `Padding`, `MaxLines`, `SelectionBackColor` | Main output ConsoleTextBox |
| `InputArea` | `Height`, `BackColor` | Input panel at bottom |
| `PromptLabel` | `ForeColor`, `BackColor`, `Font` | Prompt label (e.g., ">>> ") |
| `InputBox` | `BackColor`, `ForeColor`, `Font` | Command input TextBox |

---

## 🔌 I/O Layer Architecture (continued)

```python
@io.command('help', aliases=['?', 'h'])
def help_cmd(args):
    io.write_info("Commands: help, clear, exit")

@io.command('clear', aliases=['cls'])
def clear_cmd(args):
    console.Clear()

@io.command('exit', aliases=['quit', 'q'])
def exit_cmd(args):
    form.Close()

# Connect and run
io.connect()
console.WriteLine("Type 'help' for commands.")

Application.Run(form)
```

### Option 3: Subprocess Shell

```python
from winformpy import Form, Application, DockStyle
from winformpy.ui_elements.console import ConsolePanel, SubprocessConsoleIO

form = Form({'Text': 'PowerShell', 'Width': 900, 'Height': 600})
form.ApplyLayout()

# Create subprocess I/O for PowerShell
io = SubprocessConsoleIO(shell='powershell')

console = ConsolePanel(form, {
    'Dock': DockStyle.Fill,
    'BackColor': '#012456',
    'ForeColor': '#EEEDF0',
    'Prompt': 'PS> ',
    'ConsoleIO': io
})

io.connect()
console.WriteInfo("PowerShell subprocess - enter any command")

Application.Run(form)
```

---

## 🔌 I/O Layer Architecture

### ConsoleIOBackend (Abstract Base)

All I/O implementations inherit from `ConsoleIOBackend`:

```python
from winformpy.ui_elements.console import ConsoleIOBackend, OutputMessage, OutputType

class MyCustomIO(ConsoleIOBackend):
    def send_command(self, command):
        # Process command
        self.write_success(f"Executed: {command.command}")
    
    def connect(self) -> bool:
        self._connected = True
        self.on_connected()
        return True
    
    def disconnect(self):
        self._connected = False
        self.on_disconnected()
```

### LocalConsoleIO

Command processing with Python handlers:

```python
io = LocalConsoleIO()

# Register with decorator
@io.command('greet', aliases=['hello', 'hi'])
def greet(args):
    name = args or 'World'
    io.write_success(f"Hello, {name}!")

# Register manually
def calc(args):
    try:
        result = eval(args)
        io.write_line(f"= {result}")
    except:
        io.write_error("Invalid expression")

io.register_command('calc', calc, aliases=['c', 'eval'])

# Default handler for unknown commands
io.set_default_handler(lambda cmd, args: io.write_warning(f"Unknown: {cmd}"))
```

### SubprocessConsoleIO

Execute shell commands:

```python
# PowerShell
io = SubprocessConsoleIO(shell='powershell')

# Bash (Linux/Mac)
io = SubprocessConsoleIO(shell='bash')

# CMD
io = SubprocessConsoleIO(shell='cmd', working_dir='C:\\Projects')
```

### CallbackConsoleIO

Simple callback for custom processing:

```python
def my_processor(command):
    # Return string for output, or None
    return f"You typed: {command}"

io = CallbackConsoleIO(my_processor)
```

---

## 📊 Data Classes

### OutputMessage

Represents output from the I/O layer:

```python
@dataclass
class OutputMessage:
    text: str                           # Message text
    output_type: OutputType             # Type (NORMAL, ERROR, etc.)
    color: Optional[str] = None         # Color override
    timestamp: datetime                 # When created
    metadata: Dict[str, Any]           # Additional data
```

### InputCommand

Represents input to the I/O layer:

```python
@dataclass
class InputCommand:
    command: str                        # Command string
    timestamp: datetime                 # When received
    metadata: Dict[str, Any]           # Additional data (cwd, env, etc.)
```

### OutputType

```python
class OutputType(Enum):
    NORMAL = 'normal'      # Default color
    ERROR = 'error'        # Red
    WARNING = 'warning'    # Yellow
    SUCCESS = 'success'    # Green
    INFO = 'info'          # Cyan
    SYSTEM = 'system'      # Gray
```

---

## 🎨 Themes

| Theme | Background | Foreground |
|-------|------------|------------|
| `dark` | #1E1E1E | #CCCCCC |
| `light` | #FFFFFF | #333333 |
| `matrix` | #0D0208 | #00FF41 |
| `retro` | #000000 | #FFA500 |
| `blue` | #012456 | #EEEDF0 |
| `powershell` | #012456 | #EEEDF0 |
| `ubuntu` | #300A24 | #FFFFFF |

```python
console.SetTheme('matrix')
```

---

## 📝 ConsolePanel Properties

| Property | Type | Description |
|----------|------|-------------|
| `FontFamily` | str | Font family name |
| `FontSize` | int | Font size in points |
| `ConsoleFontStyle` | FontStyle | Font style |
| `ForeColor` | str | Text color |
| `ConsoleBackColor` | str | Background color |
| `Prompt` | str | Command prompt string |
| `ShowTimestamp` | bool | Show timestamp on lines |
| `MaxLines` | int | Maximum lines in buffer |
| `CommandHistory` | list | Read-only command history |
| `ConsoleIO` | ConsoleIOBackend | Current I/O layer |
| `IsIOLayerConnected` | bool | I/O layer connection status |

---

## 📝 ConsolePanel Methods

### Output Methods

| Method | Description |
|--------|-------------|
| `Write(text, color=None)` | Write text without newline |
| `WriteLine(text='', color=None)` | Write text with newline |
| `WriteError(text)` | Write in red |
| `WriteWarning(text)` | Write in yellow |
| `WriteSuccess(text)` | Write in green |
| `WriteInfo(text)` | Write in cyan |
| `Clear()` | Clear all output |

### Control Methods

| Method | Description |
|--------|-------------|
| `Focus()` | Focus the command input |
| `ExecuteCommand(cmd)` | Execute a command |
| `SetTheme(name)` | Apply a predefined theme |
| `ClearHistory()` | Clear command history |
| `PerformLayout()` | Force layout recalculation |

---

## 🔗 API Consistency with RichTextBox

The `ConsolePanel` output methods are designed to be consistent with WinFormPy's `RichTextBox` control. This provides a familiar API for text output across different components:

| Console Method | RichTextBox Method | Description |
|----------------|-------------------|-------------|
| `Write(text, color)` | `Write(text, color)` | Write text without newline |
| `WriteLine(text, color)` | `WriteLine(text, color)` | Write text with newline |
| `WriteError(text)` | `WriteError(text)` | Write in red |
| `WriteWarning(text)` | `WriteWarning(text)` | Write in yellow |
| `WriteSuccess(text)` | `WriteSuccess(text)` | Write in green |
| `WriteInfo(text)` | `WriteInfo(text)` | Write in cyan |
| `Clear()` | `Clear()` | Clear all text |
| `Text` (property) | `Text` (property) | Get all text content |

This consistency allows for easy migration of code between console-style and rich text editor components.

> **See Also**: For full-featured rich text editing with RTF support, see `RichTextBox` and `WordProcessorPanel` in the main WinFormPy documentation.

| Event | Args | Description |
|-------|------|-------------|
| `CommandReceived` | (sender, command: str) | Fired when user submits (legacy) |
| `OutputWritten` | (sender, text: str) | Fired when text is written |

---

## 💡 Example: Custom I/O for API

```python
from winformpy.ui_elements.console import ConsoleIOBackend, InputCommand
import requests

class APIConsoleIO(ConsoleIOBackend):
    def __init__(self, api_url):
        super().__init__()
        self.api_url = api_url
    
    def send_command(self, command: InputCommand):
        self._add_to_history(command.command)
        
        try:
            response = requests.post(
                f"{self.api_url}/execute",
                json={'command': command.command}
            )
            
            if response.ok:
                self.write_line(response.json().get('output', ''))
            else:
                self.write_error(f"API Error: {response.status_code}")
        
        except Exception as e:
            self.write_error(f"Connection error: {e}")
    
    def connect(self) -> bool:
        try:
            response = requests.get(f"{self.api_url}/health")
            self._connected = response.ok
            if self._connected:
                self.write_success("Connected to API")
                self.on_connected()
            return self._connected
        except:
            self.write_error("Failed to connect")
            return False
    
    def disconnect(self):
        self._connected = False
        self.on_disconnected()

# Usage
io = APIConsoleIO("https://api.example.com")
console = ConsolePanel(form, {'ConsoleIO': io})
io.connect()
```

---

## 🔧 Running Examples

```bash
# Legacy callback style
python -m winformpy.ui_elements.console.console_panel

# I/O layer with decorators
python -m winformpy.ui_elements.console.console_panel --io

# PowerShell subprocess
python -m winformpy.ui_elements.console.console_panel --shell
```

---

## 📁 Files

| File | Description |
|------|-------------|
| `__init__.py` | Module exports |
| `console_io.py` | I/O layer interfaces and implementations |
| `console_panel.py` | ConsolePanel widget |
| `console_ui.py` | ConsoleForm complete window |
| `README.md` | This documentation |
