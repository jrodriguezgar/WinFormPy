"""
Console I/O Layer - Abstract communication interface for ConsolePanel.

This module provides the communication layer that separates the console UI
from the command processing logic. It enables different backends:
- Local command processing (default)
- Subprocess execution (shell commands)
- Remote connections (SSH, API, WebSocket)
- Custom handlers

Architecture:
    ┌─────────────────┐
    │   ConsoleForm   │  UI Layer (presentation)
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  ConsolePanel   │  Widget Layer (visual console)
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │   ConsoleIO     │  I/O Layer (abstract interface)
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  Implementation │  Backend Layer (LocalIO, SubprocessIO, etc.)
    └─────────────────┘
"""

from abc import ABC, abstractmethod
from typing import Callable, Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import threading
import queue


class OutputType(Enum):
    """Type of output message."""
    NORMAL = 'normal'
    ERROR = 'error'
    WARNING = 'warning'
    SUCCESS = 'success'
    INFO = 'info'
    SYSTEM = 'system'


@dataclass
class OutputMessage:
    """
    Represents an output message from the I/O layer.
    
    Attributes:
        text: The message text
        output_type: Type of message (normal, error, warning, etc.)
        color: Optional custom color override
        timestamp: When the message was created
        metadata: Optional additional data
    """
    text: str
    output_type: OutputType = OutputType.NORMAL
    color: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class InputCommand:
    """
    Represents an input command to the I/O layer.
    
    Attributes:
        command: The command string
        timestamp: When the command was received
        metadata: Optional additional data (e.g., working directory, env vars)
    """
    command: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ConsoleIOBase(ABC):
    """
    Abstract base class for console I/O implementations.
    
    Subclass this to create custom backends for the console.
    
    Example:
        class MyCustomIO(ConsoleIOBase):
            def send_command(self, command):
                # Process command
                self.on_output(OutputMessage("Result", OutputType.NORMAL))
            
            def connect(self):
                self.on_output(OutputMessage("Connected!", OutputType.SUCCESS))
    """
    
    def __init__(self):
        """Initialize the I/O layer."""
        self._connected = False
        self._command_history: List[str] = []
        
        # Callbacks - set by ConsolePanel
        self.on_output: Callable[[OutputMessage], None] = lambda msg: None
        self.on_connected: Callable[[], None] = lambda: None
        self.on_disconnected: Callable[[], None] = lambda: None
        self.on_error: Callable[[str], None] = lambda err: None
    
    @property
    def is_connected(self) -> bool:
        """Returns True if the I/O layer is connected and ready."""
        return self._connected
    
    @property
    def command_history(self) -> List[str]:
        """Returns the command history."""
        return list(self._command_history)
    
    @abstractmethod
    def send_command(self, command: InputCommand) -> None:
        """
        Send a command to be processed.
        
        Args:
            command: The InputCommand to process
        """
        pass
    
    @abstractmethod
    def connect(self) -> bool:
        """
        Connect/initialize the I/O layer.
        
        Returns:
            True if connection successful
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect/cleanup the I/O layer."""
        pass
    
    def write(self, text: str, output_type: OutputType = OutputType.NORMAL, 
              color: Optional[str] = None) -> None:
        """
        Convenience method to send output.
        
        Args:
            text: Text to output
            output_type: Type of output
            color: Optional color override
        """
        msg = OutputMessage(text, output_type, color)
        self.on_output(msg)
    
    def write_line(self, text: str = '', output_type: OutputType = OutputType.NORMAL,
                   color: Optional[str] = None) -> None:
        """
        Convenience method to send output with newline.
        
        Args:
            text: Text to output
            output_type: Type of output
            color: Optional color override
        """
        self.write(text + '\n', output_type, color)
    
    def write_error(self, text: str) -> None:
        """Write an error message."""
        self.write_line(text, OutputType.ERROR)
    
    def write_warning(self, text: str) -> None:
        """Write a warning message."""
        self.write_line(text, OutputType.WARNING)
    
    def write_success(self, text: str) -> None:
        """Write a success message."""
        self.write_line(text, OutputType.SUCCESS)
    
    def write_info(self, text: str) -> None:
        """Write an info message."""
        self.write_line(text, OutputType.INFO)
    
    def _add_to_history(self, command: str) -> None:
        """Add a command to history if not duplicate."""
        if command.strip():
            if not self._command_history or self._command_history[-1] != command:
                self._command_history.append(command)


class LocalConsoleIO(ConsoleIOBase):
    """
    Local command processing I/O layer.
    
    This is the default I/O layer that processes commands locally
    using registered command handlers.
    
    Example:
        io = LocalConsoleIO()
        
        @io.command('hello')
        def hello_cmd(args):
            io.write_success("Hello, World!")
        
        @io.command('echo')
        def echo_cmd(args):
            io.write_line(args)
        
        io.connect()
        io.send_command(InputCommand("hello"))
    """
    
    def __init__(self):
        """Initialize the local I/O layer."""
        super().__init__()
        self._commands: Dict[str, Callable[[str], None]] = {}
        self._default_handler: Optional[Callable[[str, str], None]] = None
    
    def register_command(self, name: str, handler: Callable[[str], None], 
                         aliases: Optional[List[str]] = None) -> None:
        """
        Register a command handler.
        
        Args:
            name: Command name (case-insensitive)
            handler: Function that takes args string and processes command
            aliases: Optional list of alternative names
        """
        self._commands[name.lower()] = handler
        if aliases:
            for alias in aliases:
                self._commands[alias.lower()] = handler
    
    def command(self, name: str, aliases: Optional[List[str]] = None):
        """
        Decorator to register a command handler.
        
        Args:
            name: Command name
            aliases: Optional alternative names
        
        Example:
            @io.command('greet', aliases=['hello', 'hi'])
            def greet(args):
                io.write_success(f"Hello {args or 'World'}!")
        """
        def decorator(func: Callable[[str], None]):
            self.register_command(name, func, aliases)
            return func
        return decorator
    
    def set_default_handler(self, handler: Callable[[str, str], None]) -> None:
        """
        Set the default handler for unknown commands.
        
        Args:
            handler: Function that takes (command_name, args) for unknown commands
        """
        self._default_handler = handler
    
    def send_command(self, command: InputCommand) -> None:
        """Process a command locally."""
        self._add_to_history(command.command)
        
        # Parse command and args
        parts = command.command.strip().split(' ', 1)
        cmd_name = parts[0].lower() if parts else ''
        args = parts[1] if len(parts) > 1 else ''
        
        if not cmd_name:
            return
        
        # Find and execute handler
        if cmd_name in self._commands:
            try:
                self._commands[cmd_name](args)
            except Exception as e:
                self.write_error(f"Error executing '{cmd_name}': {str(e)}")
        elif self._default_handler:
            self._default_handler(cmd_name, args)
        else:
            self.write_warning(f"Unknown command: {cmd_name}")
            self.write_line("Type 'help' for available commands.")
    
    def connect(self) -> bool:
        """Initialize the local I/O layer."""
        self._connected = True
        self.on_connected()
        return True
    
    def disconnect(self) -> None:
        """Cleanup the local I/O layer."""
        self._connected = False
        self.on_disconnected()
    
    def get_commands(self) -> List[str]:
        """Get list of registered command names."""
        return sorted(set(self._commands.keys()))


class SubprocessConsoleIO(ConsoleIOBase):
    """
    Subprocess-based I/O layer for executing shell commands.
    
    Executes commands in a subprocess and streams output back
    to the console.
    
    Example:
        io = SubprocessConsoleIO(shell='powershell')
        io.connect()
        io.send_command(InputCommand("dir"))
    """
    
    def __init__(self, shell: str = 'cmd', working_dir: Optional[str] = None):
        """
        Initialize subprocess I/O.
        
        Args:
            shell: Shell to use ('cmd', 'powershell', 'bash')
            working_dir: Working directory for commands
        """
        super().__init__()
        self._shell = shell
        self._working_dir = working_dir
        self._process = None
        self._output_queue: queue.Queue = queue.Queue()
        self._reader_thread: Optional[threading.Thread] = None
    
    def send_command(self, command: InputCommand) -> None:
        """Execute command in subprocess."""
        import subprocess
        
        self._add_to_history(command.command)
        
        try:
            # Build command based on shell
            if self._shell == 'powershell':
                full_cmd = ['powershell', '-Command', command.command]
            elif self._shell == 'bash':
                full_cmd = ['bash', '-c', command.command]
            else:
                full_cmd = ['cmd', '/c', command.command]
            
            # Execute
            result = subprocess.run(
                full_cmd,
                capture_output=True,
                text=True,
                cwd=self._working_dir or command.metadata.get('cwd'),
                timeout=30
            )
            
            # Output stdout
            if result.stdout:
                for line in result.stdout.splitlines():
                    self.write_line(line)
            
            # Output stderr as error
            if result.stderr:
                for line in result.stderr.splitlines():
                    self.write_error(line)
            
            # Show return code if non-zero
            if result.returncode != 0:
                self.write_warning(f"Exit code: {result.returncode}")
                
        except subprocess.TimeoutExpired:
            self.write_error("Command timed out after 30 seconds")
        except FileNotFoundError:
            self.write_error(f"Shell not found: {self._shell}")
        except Exception as e:
            self.write_error(f"Error: {str(e)}")
    
    def connect(self) -> bool:
        """Initialize subprocess I/O."""
        self._connected = True
        self.write_info(f"Shell: {self._shell}")
        if self._working_dir:
            self.write_info(f"Working directory: {self._working_dir}")
        self.on_connected()
        return True
    
    def disconnect(self) -> None:
        """Cleanup subprocess I/O."""
        self._connected = False
        self.on_disconnected()


class CallbackConsoleIO(ConsoleIOBase):
    """
    Simple callback-based I/O layer.
    
    Allows setting a single callback function to handle all commands.
    Useful for simple integrations.
    
    Example:
        def my_handler(command):
            if command == 'hello':
                return "Hello, World!"
            return f"You said: {command}"
        
        io = CallbackConsoleIO(my_handler)
        io.connect()
    """
    
    def __init__(self, handler: Optional[Callable[[str], Optional[str]]] = None):
        """
        Initialize callback I/O.
        
        Args:
            handler: Callback function that receives command and optionally returns response
        """
        super().__init__()
        self._handler = handler
    
    def set_handler(self, handler: Callable[[str], Optional[str]]) -> None:
        """Set the command handler callback."""
        self._handler = handler
    
    def send_command(self, command: InputCommand) -> None:
        """Process command through callback."""
        self._add_to_history(command.command)
        
        if self._handler:
            try:
                result = self._handler(command.command)
                if result is not None:
                    self.write_line(str(result))
            except Exception as e:
                self.write_error(f"Error: {str(e)}")
        else:
            self.write_warning("No handler configured")
    
    def connect(self) -> bool:
        """Initialize callback I/O."""
        self._connected = True
        self.on_connected()
        return True
    
    def disconnect(self) -> None:
        """Cleanup callback I/O."""
        self._connected = False
        self.on_disconnected()


# =============================================================================
# Factory function
# =============================================================================

def create_console_io(io_type: str = 'local', **kwargs) -> ConsoleIOBase:
    """
    Factory function to create I/O layer instances.
    
    Args:
        io_type: Type of I/O ('local', 'subprocess', 'callback')
        **kwargs: Additional arguments for the I/O class
    
    Returns:
        ConsoleIOBase instance
    
    Example:
        io = create_console_io('subprocess', shell='powershell')
        io = create_console_io('local')
    """
    io_types = {
        'local': LocalConsoleIO,
        'subprocess': SubprocessConsoleIO,
        'callback': CallbackConsoleIO
    }
    
    if io_type not in io_types:
        raise ValueError(f"Unknown I/O type: {io_type}. Available: {list(io_types.keys())}")
    
    return io_types[io_type](**kwargs)
