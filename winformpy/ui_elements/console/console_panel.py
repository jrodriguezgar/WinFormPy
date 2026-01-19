"""
ConsolePanel - A terminal-style console component for WinFormPy.

Provides a text-based console interface with customizable font, colors,
and command history support. Features a pluggable I/O layer for different
command processing backends.

Architecture:
    ┌─────────────────┐
    │  ConsolePanel   │  Widget Layer (visual console)
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │   ConsoleIO     │  I/O Layer (pluggable backend)
    └─────────────────┘

This component uses WinFormPy controls exclusively:
- ConsoleTextBox: For multi-color text output with scrollbar
- TextBox: For command input
- Panel, Label: For layout and prompts
"""

import sys
import os

# Add project root to path for imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..', '..', '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy.winformpy import (
    Panel, Label, TextBox, ConsoleTextBox,
    DockStyle, AnchorStyles, Color,
    Font, FontStyle, ScrollBars
)
from winformpy.ui_elements.console.console_io import (
    ConsoleIOBase, LocalConsoleIO, OutputMessage, OutputType, InputCommand,
    create_console_io
)
from datetime import datetime
from typing import Optional, Callable


class ConsolePanel(Panel):
    """
    A terminal-style console panel with customizable appearance.
    
    Features:
    - Customizable font (family, size, style)
    - Customizable foreground and background colors
    - Command input with history (up/down arrows)
    - Read-only output area with scrolling
    - Pluggable I/O layer for command processing
    - Write, WriteLine, and Clear methods
    - Command handler callback (legacy) or I/O layer
    - Prompt customization
    
    Example (Legacy callback style):
        console = ConsolePanel(form, {
            'Dock': DockStyle.Fill,
            'BackColor': '#1E1E1E',
            'ForeColor': '#00FF00',
            'FontFamily': 'Consolas',
            'FontSize': 11
        })
        
        console.CommandReceived = lambda sender, cmd: console.WriteLine(f"You typed: {cmd}")
        console.WriteLine("Welcome to the console!")
    
    Example (I/O layer style):
        from winformpy.ui_elements.console import LocalConsoleIO
        
        # Create I/O layer with commands
        io = LocalConsoleIO()
        
        @io.command('hello')
        def hello_cmd(args):
            io.write_success(f"Hello {args or 'World'}!")
        
        # Create console with I/O layer
        console = ConsolePanel(form, {
            'Dock': DockStyle.Fill,
            'ConsoleIO': io
        })
        
        io.connect()
    """
    
    # Default console colors (dark theme)
    DEFAULT_BACK_COLOR = '#1E1E1E'
    DEFAULT_FORE_COLOR = '#CCCCCC'
    DEFAULT_FONT_FAMILY = 'Consolas'
    DEFAULT_FONT_SIZE = 11
    DEFAULT_PROMPT = '> '
    
    # Color mapping for OutputType
    OUTPUT_COLORS = {
        OutputType.NORMAL: None,  # Uses ForeColor
        OutputType.ERROR: '#FF6B6B',
        OutputType.WARNING: '#FFD93D',
        OutputType.SUCCESS: '#6BCB77',
        OutputType.INFO: '#4D96FF',
        OutputType.SYSTEM: '#808080'
    }
    
    def __init__(self, parent, props=None):
        """
        Initialize the ConsolePanel.
        
        Args:
            parent: The parent form or container
            props: Optional dictionary with properties:
                - BackColor: Background color (default: '#1E1E1E')
                - ForeColor: Text color (default: '#CCCCCC')
                - FontFamily: Font family name (default: 'Consolas')
                - FontSize: Font size in points (default: 11)
                - FontStyle: Font style (default: FontStyle.Regular)
                - Prompt: Command prompt string (default: '> ')
                - ShowTimestamp: Show timestamp on each line (default: False)
                - MaxLines: Maximum lines to keep in buffer (default: 1000)
                - ReadOnly: If True, hide command input (default: False)
                - ConsoleIO: Optional ConsoleIOBase instance for I/O layer
        """
        # Extract console-specific properties before calling parent
        defaults = {
            'Width': 600,
            'Height': 400,
            'BackColor': self.DEFAULT_BACK_COLOR,
            'ForeColor': self.DEFAULT_FORE_COLOR,
            'FontFamily': self.DEFAULT_FONT_FAMILY,
            'FontSize': self.DEFAULT_FONT_SIZE,
            'FontStyle': FontStyle.Regular,
            'Prompt': self.DEFAULT_PROMPT,
            'ShowTimestamp': False,
            'MaxLines': 1000,
            'ReadOnly': False,
            'BorderStyle': 'None',
            'ConsoleIO': None
        }
        
        if props:
            defaults.update(props)
        
        # Store console-specific properties
        self._font_family = defaults.pop('FontFamily')
        self._font_size = defaults.pop('FontSize')
        self._font_style = defaults.pop('FontStyle')
        self._fore_color = defaults.get('ForeColor', self.DEFAULT_FORE_COLOR)
        self._back_color = defaults.get('BackColor', self.DEFAULT_BACK_COLOR)
        self._prompt = defaults.pop('Prompt')
        self._show_timestamp = defaults.pop('ShowTimestamp')
        self._max_lines = defaults.pop('MaxLines')
        self._read_only = defaults.pop('ReadOnly')
        
        # I/O Layer
        self._console_io: Optional[ConsoleIOBase] = defaults.pop('ConsoleIO')
        self._use_io_layer = self._console_io is not None
        
        # Command history (used when not using I/O layer)
        self._command_history = []
        self._history_index = -1
        self._current_input = ''
        
        # Initialize parent Panel
        super().__init__(parent, defaults)
        
        # Events (legacy callback style)
        self.CommandReceived: Callable = lambda sender, command: None
        self.OutputWritten: Callable = lambda sender, text: None
        
        # Create the console font
        self._console_font = Font(self._font_family, self._font_size, self._font_style)
        
        # Build the UI
        self._create_ui()
        
        # Connect I/O layer if provided
        if self._console_io:
            self._connect_io_layer()
    
    def _connect_io_layer(self) -> None:
        """Connect the I/O layer callbacks to the console."""
        if not self._console_io:
            return
        
        # Set output callback
        self._console_io.on_output = self._handle_io_output
        
        # Set error callback
        self._console_io.on_error = lambda err: self.WriteError(err)
    
    def _handle_io_output(self, message: OutputMessage) -> None:
        """Handle output from the I/O layer."""
        # Determine color
        color = message.color
        if not color and message.output_type in self.OUTPUT_COLORS:
            color = self.OUTPUT_COLORS[message.output_type]
        
        # Write to console
        self.Write(message.text, color)
    
    def _create_ui(self):
        """Create the console UI components using WinFormPy controls."""
        # Output area - ConsoleTextBox with scrollbar and multi-color support
        self._output_text = ConsoleTextBox(self, {
            'Dock': DockStyle.Fill,
            'BackColor': self._back_color,
            'ForeColor': self._fore_color,
            'Font': self._console_font,
            'ReadOnly': True,
            'WordWrap': True,
            'ShowScrollBar': True,
            'MaxLines': self._max_lines,
            'BorderWidth': 0,
            'Padding': 8,
            'SelectionBackColor': '#264F78'
        })
        
        # Input area (only if not read-only)
        if not self._read_only:
            self._input_panel = Panel(self, {
                'Dock': DockStyle.Bottom,
                'Height': 30,
                'BackColor': self._back_color,
                'BorderStyle': 'None'
            })
            
            # Prompt label
            self._prompt_label = Label(self._input_panel, {
                'Text': self._prompt,
                'Font': self._console_font,
                'ForeColor': self._fore_color,
                'BackColor': self._back_color,
                'Left': 8,
                'Top': 5,
                'AutoSize': True
            })
            
            # Calculate prompt width
            prompt_width = len(self._prompt) * (self._font_size - 2) + 10
            
            # Input TextBox
            self._input_entry = TextBox(self._input_panel, {
                'Left': prompt_width,
                'Top': 4,
                'Width': 500,  # Will be adjusted by anchor
                'Height': 22,
                'BackColor': self._back_color,
                'ForeColor': self._fore_color,
                'Font': self._console_font,
                'BorderStyle': 'None'
            })
            
            # Bind key events using WinFormPy BindKey
            self._input_entry.BindKey('<Return>', self._on_command_enter)
            self._input_entry.BindKey('<Up>', self._on_history_up)
            self._input_entry.BindKey('<Down>', self._on_history_down)
            self._input_entry.BindKey('<Escape>', self._on_escape)
            
            # Set focus to input
            self._input_entry.Focus()
    
    def PerformLayout(self):
        """Force layout recalculation for all internal widgets."""
        # Refresh to get updated geometry
        self.Refresh()
        
        # ConsoleTextBox has its own PerformLayout
        if hasattr(self, '_output_text') and self._output_text:
            if hasattr(self._output_text, 'PerformLayout'):
                self._output_text.PerformLayout()
        
        self.Refresh()
    
    # =========================================================================
    # Properties
    # =========================================================================
    
    @property
    def FontFamily(self):
        """Gets the font family name."""
        return self._font_family
    
    @FontFamily.setter
    def FontFamily(self, value):
        """Sets the font family name and updates the console."""
        self._font_family = value
        self._update_font()
    
    @property
    def FontSize(self):
        """Gets the font size in points."""
        return self._font_size
    
    @FontSize.setter
    def FontSize(self, value):
        """Sets the font size and updates the console."""
        self._font_size = value
        self._update_font()
    
    @property
    def ConsoleFontStyle(self):
        """Gets the font style."""
        return self._font_style
    
    @ConsoleFontStyle.setter
    def ConsoleFontStyle(self, value):
        """Sets the font style and updates the console."""
        self._font_style = value
        self._update_font()
    
    @property
    def ForeColor(self):
        """Gets the text foreground color."""
        return self._fore_color
    
    @ForeColor.setter
    def ForeColor(self, value):
        """Sets the text foreground color."""
        self._fore_color = value
        self._update_colors()
    
    @property
    def ConsoleBackColor(self):
        """Gets the console background color."""
        return self._back_color
    
    @ConsoleBackColor.setter
    def ConsoleBackColor(self, value):
        """Sets the console background color."""
        self._back_color = value
        self._update_colors()
    
    @property
    def Prompt(self):
        """Gets the command prompt string."""
        return self._prompt
    
    @Prompt.setter
    def Prompt(self, value):
        """Sets the command prompt string."""
        self._prompt = value
        if hasattr(self, '_prompt_label'):
            self._prompt_label.Text = value
    
    @property
    def ShowTimestamp(self):
        """Gets whether timestamps are shown."""
        return self._show_timestamp
    
    @ShowTimestamp.setter
    def ShowTimestamp(self, value):
        """Sets whether timestamps are shown."""
        self._show_timestamp = value
    
    @property
    def MaxLines(self):
        """Gets the maximum number of lines to keep."""
        return self._max_lines
    
    @MaxLines.setter
    def MaxLines(self, value):
        """Sets the maximum number of lines to keep."""
        self._max_lines = value
        self._trim_output()
    
    @property
    def CommandHistory(self):
        """Gets the command history list (read-only)."""
        return self._get_history()
    
    @property
    def Text(self):
        """Gets all text in the output area."""
        return self._output_text.Text
    
    @property
    def ConsoleIO(self) -> Optional[ConsoleIOBase]:
        """Gets the current I/O layer."""
        return self._console_io
    
    @ConsoleIO.setter
    def ConsoleIO(self, value: Optional[ConsoleIOBase]) -> None:
        """Sets the I/O layer."""
        # Disconnect old I/O layer
        if self._console_io and self._console_io.is_connected:
            self._console_io.disconnect()
        
        self._console_io = value
        self._use_io_layer = value is not None
        
        # Connect new I/O layer
        if value:
            self._connect_io_layer()
    
    @property
    def IsIOLayerConnected(self) -> bool:
        """Returns True if I/O layer is connected."""
        return self._console_io is not None and self._console_io.is_connected
    
    # =========================================================================
    # Methods
    # =========================================================================
    
    def Write(self, text, color=None):
        """
        Write text to the console without a newline.
        
        Args:
            text: The text to write
            color: Optional color for this text (default: ForeColor)
        """
        # Use ConsoleTextBox.Write which handles colors and read-only state
        self._output_text.Write(text, color)
        
        # Fire event
        self.OutputWritten(self, text)
    
    def WriteLine(self, text='', color=None):
        """
        Write text to the console with a newline.
        
        Args:
            text: The text to write
            color: Optional color for this text (default: ForeColor)
        """
        if self._show_timestamp:
            timestamp = datetime.now().strftime('[%H:%M:%S] ')
            self.Write(timestamp, '#808080')
        
        self.Write(text + '\n', color)
    
    def WriteError(self, text):
        """
        Write error text to the console (in red).
        
        Args:
            text: The error text to write
        """
        self.WriteLine(text, '#FF6B6B')
    
    def WriteWarning(self, text):
        """
        Write warning text to the console (in yellow).
        
        Args:
            text: The warning text to write
        """
        self.WriteLine(text, '#FFD93D')
    
    def WriteSuccess(self, text):
        """
        Write success text to the console (in green).
        
        Args:
            text: The success text to write
        """
        self.WriteLine(text, '#6BCB77')
    
    def WriteInfo(self, text):
        """
        Write info text to the console (in cyan).
        
        Args:
            text: The info text to write
        """
        self.WriteLine(text, '#4D96FF')
    
    def Clear(self):
        """Clear all text from the console."""
        self._output_text.Clear()
    
    def ClearHistory(self):
        """Clear the command history."""
        self._command_history.clear()
        self._history_index = -1
    
    def Focus(self):
        """Set focus to the command input."""
        if hasattr(self, '_input_entry') and self._input_entry:
            self._input_entry.Focus()
    
    def ExecuteCommand(self, command):
        """
        Execute a command programmatically.
        
        Args:
            command: The command string to execute
        """
        self._process_command(command)
    
    def SetTheme(self, theme_name):
        """
        Apply a predefined theme.
        
        Args:
            theme_name: Theme name ('dark', 'light', 'matrix', 'retro', 'blue')
        """
        themes = {
            'dark': {
                'BackColor': '#1E1E1E',
                'ForeColor': '#CCCCCC'
            },
            'light': {
                'BackColor': '#FFFFFF',
                'ForeColor': '#333333'
            },
            'matrix': {
                'BackColor': '#0D0208',
                'ForeColor': '#00FF41'
            },
            'retro': {
                'BackColor': '#000000',
                'ForeColor': '#FFA500'
            },
            'blue': {
                'BackColor': '#012456',
                'ForeColor': '#EEEDF0'
            },
            'powershell': {
                'BackColor': '#012456',
                'ForeColor': '#EEEDF0'
            },
            'ubuntu': {
                'BackColor': '#300A24',
                'ForeColor': '#FFFFFF'
            }
        }
        
        if theme_name.lower() in themes:
            theme = themes[theme_name.lower()]
            self.ConsoleBackColor = theme['BackColor']
            self.ForeColor = theme['ForeColor']
    
    # =========================================================================
    # Private Methods
    # =========================================================================
    
    def _update_font(self):
        """Update the font on all console widgets."""
        self._console_font = Font(self._font_family, self._font_size, self._font_style)
        
        # Update ConsoleTextBox font
        if hasattr(self, '_output_text') and self._output_text:
            self._output_text.Font = self._console_font
        
        # Update TextBox font
        if hasattr(self, '_input_entry') and self._input_entry:
            self._input_entry.Font = self._console_font
        
        # Update Label font
        if hasattr(self, '_prompt_label') and self._prompt_label:
            self._prompt_label.Font = self._console_font
    
    def _update_colors(self):
        """Update colors on all console widgets."""
        # Update ConsoleTextBox colors
        if hasattr(self, '_output_text') and self._output_text:
            self._output_text.BackColor = self._back_color
            self._output_text.ForeColor = self._fore_color
        
        # Update TextBox colors
        if hasattr(self, '_input_entry') and self._input_entry:
            self._input_entry.BackColor = self._back_color
            self._input_entry.ForeColor = self._fore_color
        
        # Update Label colors
        if hasattr(self, '_prompt_label') and self._prompt_label:
            self._prompt_label.ForeColor = self._fore_color
            self._prompt_label.BackColor = self._back_color
        
        # Update Panel colors
        if hasattr(self, '_input_panel') and self._input_panel:
            self._input_panel.BackColor = self._back_color
    
    def _trim_output(self):
        """Trim output to MaxLines if exceeded.
        
        Note: ConsoleTextBox handles this automatically via MaxLines property.
        This method is kept for backwards compatibility.
        """
        pass  # ConsoleTextBox handles trimming internally
    
    def _process_command(self, command):
        """Process a command entered by the user."""
        # Echo the command
        self.Write(self._prompt, '#808080')
        self.WriteLine(command)
        
        if self._use_io_layer and self._console_io:
            # Use I/O layer for command processing
            input_cmd = InputCommand(command)
            self._console_io.send_command(input_cmd)
        else:
            # Legacy callback style
            # Add to history if not empty and different from last
            if command.strip():
                if not self._command_history or self._command_history[-1] != command:
                    self._command_history.append(command)
                self._history_index = len(self._command_history)
            
            # Fire the command event
            self.CommandReceived(self, command)
    
    def _on_command_enter(self, event):
        """Handle Enter key press in the input field."""
        command = self._input_entry.Text
        self._input_entry.Text = ''
        self._process_command(command)
        return 'break'
    
    def _get_history(self) -> list:
        """Get command history from I/O layer or local."""
        if self._use_io_layer and self._console_io:
            return self._console_io.command_history
        return self._command_history
    
    def _on_history_up(self, event):
        """Navigate up in command history."""
        history = self._get_history()
        if history and self._history_index > 0:
            if self._history_index == len(history):
                self._current_input = self._input_entry.Text
            self._history_index -= 1
            self._input_entry.Text = history[self._history_index]
        return 'break'
    
    def _on_history_down(self, event):
        """Navigate down in command history."""
        history = self._get_history()
        if self._history_index < len(history) - 1:
            self._history_index += 1
            self._input_entry.Text = history[self._history_index]
        elif self._history_index == len(history) - 1:
            self._history_index = len(history)
            self._input_entry.Text = self._current_input
        return 'break'
    
    def _on_escape(self, event):
        """Handle Escape key - clear input."""
        self._input_entry.Text = ''
        history = self._get_history()
        self._history_index = len(history)
        return 'break'


# =============================================================================
# Example Usage
# =============================================================================

if __name__ == '__main__':
    from winformpy.winformpy import Form, Application, DockStyle
    import sys
    
    # Check for command line args to select example
    use_io_layer = '--io' in sys.argv or '-i' in sys.argv
    use_subprocess = '--shell' in sys.argv or '-s' in sys.argv
    
    # Create main form
    form = Form({
        'Text': 'Console Panel Example' + (' (I/O Layer)' if use_io_layer else ' (Subprocess)' if use_subprocess else ' (Legacy)'),
        'Width': 900,
        'Height': 600,
        'BackColor': '#2D2D2D'
    })
    form.ApplyLayout()
    
    if use_subprocess:
        # =================================================================
        # Example: Subprocess I/O Layer (execute shell commands)
        # =================================================================
        from winformpy.ui_elements.console.console_io import SubprocessConsoleIO
        
        io = SubprocessConsoleIO(shell='powershell')
        
        console = ConsolePanel(form, {
            'Dock': DockStyle.Fill,
            'FontFamily': 'Cascadia Code',
            'FontSize': 11,
            'BackColor': '#012456',
            'ForeColor': '#EEEDF0',
            'Prompt': 'PS> ',
            'ConsoleIO': io
        })
        
        io.connect()
        console.WriteInfo("PowerShell subprocess console")
        console.WriteLine("Enter any PowerShell command to execute.")
        console.WriteLine("")
        
    elif use_io_layer:
        # =================================================================
        # Example: Local I/O Layer with command decorators
        # =================================================================
        from winformpy.ui_elements.console.console_io import LocalConsoleIO
        
        # Create I/O layer
        io = LocalConsoleIO()
        
        # Create console with I/O layer
        console = ConsolePanel(form, {
            'Dock': DockStyle.Fill,
            'FontFamily': 'Consolas',
            'FontSize': 12,
            'BackColor': '#1E1E1E',
            'ForeColor': '#CCCCCC',
            'Prompt': '> ',
            'ConsoleIO': io
        })
        
        # Register commands using decorators
        @io.command('help', aliases=['?', 'h'])
        def help_cmd(args):
            io.write_line("")
            io.write_info("━" * 40)
            io.write_info("  Available Commands (I/O Layer)")
            io.write_info("━" * 40)
            io.write_line("")
            io.write_line("  help, ?, h    - Show this help message")
            io.write_line("  clear, cls    - Clear the console")
            io.write_line("  time          - Show current date and time")
            io.write_line("  echo <text>   - Echo the text back")
            io.write_line("  theme <name>  - Change theme")
            io.write_line("  demo          - Show color demo")
            io.write_line("  commands      - List registered commands")
            io.write_line("  exit, quit    - Close the console")
            io.write_line("")
        
        @io.command('clear', aliases=['cls'])
        def clear_cmd(args):
            console.Clear()
        
        @io.command('time')
        def time_cmd(args):
            now = datetime.now()
            io.write_success(f"📅 Date: {now.strftime('%Y-%m-%d')}")
            io.write_success(f"⏰ Time: {now.strftime('%H:%M:%S')}")
        
        @io.command('echo')
        def echo_cmd(args):
            io.write_line(args or '')
        
        @io.command('theme')
        def theme_cmd(args):
            themes = ['dark', 'light', 'matrix', 'retro', 'blue', 'powershell', 'ubuntu']
            if args and args.lower() in themes:
                console.SetTheme(args.lower())
                io.write_success(f"Theme changed to: {args}")
            else:
                io.write_error(f"Unknown theme: {args}" if args else "Please specify a theme")
                io.write_line(f"Available: {', '.join(themes)}")
        
        @io.command('demo')
        def demo_cmd(args):
            io.write_line("")
            io.write_line("Color Output Demo:")
            io.write_line("─" * 30)
            io.write_line("Normal text output")
            io.write_error("Error messages appear in red")
            io.write_warning("Warnings appear in yellow")
            io.write_success("Success messages in green")
            io.write_info("Info messages appear in cyan")
            io.write_line("")
        
        @io.command('commands')
        def commands_cmd(args):
            cmds = io.get_commands()
            io.write_info(f"Registered commands ({len(cmds)}):")
            io.write_line(", ".join(cmds))
        
        @io.command('exit', aliases=['quit', 'q'])
        def exit_cmd(args):
            form.Close()
        
        # Connect I/O layer
        io.connect()
        
        # Welcome message
        console.WriteSuccess("╔══════════════════════════════════════════════════╗")
        console.WriteSuccess("║     Console with I/O Layer Architecture          ║")
        console.WriteSuccess("╚══════════════════════════════════════════════════╝")
        console.WriteLine("")
        console.WriteInfo("  Commands registered via @io.command() decorator")
        console.WriteLine("")
        console.WriteLine("  Type 'help' for available commands.")
        console.WriteLine("")
        
    else:
        # =================================================================
        # Example: Legacy callback style (backwards compatible)
        # =================================================================
        console = ConsolePanel(form, {
            'Dock': DockStyle.Fill,
            'FontFamily': 'Consolas',
            'FontSize': 12,
            'BackColor': '#1E1E1E',
            'ForeColor': '#CCCCCC',
            'Prompt': '> ',
            'ShowTimestamp': False
        })
        
        # Command handler (legacy callback style)
        def handle_command(sender, command):
            cmd = command.strip().lower()
            args = command.strip().split(' ', 1)
            
            if cmd == 'help':
                console.WriteLine("")
                console.WriteInfo("━" * 40)
                console.WriteInfo("  Available Commands (Legacy)")
                console.WriteInfo("━" * 40)
                console.WriteLine("")
                console.WriteLine("  help          - Show this help message")
                console.WriteLine("  clear         - Clear the console")
                console.WriteLine("  time          - Show current date and time")
                console.WriteLine("  echo <text>   - Echo the text back")
                console.WriteLine("  theme <name>  - Change theme")
                console.WriteLine("  demo          - Show color demo")
                console.WriteLine("  history       - Show command history")
                console.WriteLine("  exit          - Close the console")
                console.WriteLine("")
            
            elif cmd == 'clear':
                console.Clear()
            
            elif cmd == 'time':
                now = datetime.now()
                console.WriteSuccess(f"📅 Date: {now.strftime('%Y-%m-%d')}")
                console.WriteSuccess(f"⏰ Time: {now.strftime('%H:%M:%S')}")
            
            elif args[0].lower() == 'echo' and len(args) > 1:
                console.WriteLine(args[1])
            
            elif args[0].lower() == 'theme' and len(args) > 1:
                theme = args[1].lower()
                themes = ['dark', 'light', 'matrix', 'retro', 'blue', 'powershell', 'ubuntu']
                if theme in themes:
                    console.SetTheme(theme)
                    console.WriteSuccess(f"Theme changed to: {theme}")
                else:
                    console.WriteError(f"Unknown theme: {theme}")
                    console.WriteLine(f"Available: {', '.join(themes)}")
            
            elif cmd == 'demo':
                console.WriteLine("")
                console.WriteLine("Color Output Demo:")
                console.WriteLine("─" * 30)
                console.WriteLine("Normal text output")
                console.WriteError("Error messages appear in red")
                console.WriteWarning("Warnings appear in yellow")
                console.WriteSuccess("Success messages in green")
                console.WriteInfo("Info messages appear in cyan")
                console.WriteLine("")
            
            elif cmd == 'history':
                history = console.CommandHistory
                if history:
                    console.WriteInfo("Command History:")
                    for i, cmd in enumerate(history, 1):
                        console.WriteLine(f"  {i}. {cmd}")
                else:
                    console.WriteLine("No command history.")
            
            elif cmd == 'exit':
                form.Close()
            
            elif cmd:
                console.WriteWarning(f"Unknown command: {command}")
                console.WriteLine("Type 'help' for available commands.")
        
        # Set command handler
        console.CommandReceived = handle_command
        
        # Welcome banner
        console.WriteSuccess("╔══════════════════════════════════════════════════╗")
        console.WriteSuccess("║        Welcome to WinFormPy Console!             ║")
        console.WriteSuccess("╚══════════════════════════════════════════════════╝")
        console.WriteLine("")
        console.WriteLine("  Legacy callback style (CommandReceived event)")
        console.WriteLine("")
        console.WriteInfo("  💡 Run with --io for I/O Layer example")
        console.WriteInfo("  💡 Run with --shell for PowerShell subprocess")
        console.WriteLine("")
        console.WriteLine("  Type 'help' for available commands.")
        console.WriteLine("")
    
    # Run the application
    Application.Run(form)
