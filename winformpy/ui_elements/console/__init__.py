"""
Console UI Element Module

Provides a terminal-style console component with customizable font, colors,
and a pluggable I/O layer for different command processing backends.

Architecture:
    ┌─────────────────┐
    │   ConsoleForm   │  UI Layer (complete console window)
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  ConsolePanel   │  Widget Layer (embeddable console)
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │   ConsoleIO     │  I/O Layer (pluggable backend)
    └─────────────────┘

I/O Implementations:
    - LocalConsoleIO: Local command handlers with decorators
    - SubprocessConsoleIO: Execute shell commands
    - CallbackConsoleIO: Simple callback-based processing
"""

from .console_panel import ConsolePanel
from .console_ui import ConsoleForm
from .console_io import (
    # Base classes
    ConsoleIOBackend,
    
    # Implementations
    LocalConsoleIO,
    SubprocessConsoleIO,
    CallbackConsoleIO,
    
    # Data classes
    OutputMessage,
    InputCommand,
    OutputType,
    
    # Factory
    create_console_io
)

__all__ = [
    # UI Components
    'ConsolePanel',
    'ConsoleForm',
    
    # I/O Layer
    'ConsoleIOBackend',
    'LocalConsoleIO',
    'SubprocessConsoleIO',
    'CallbackConsoleIO',
    
    # Data types
    'OutputMessage',
    'InputCommand',
    'OutputType',
    
    # Factory
    'create_console_io'
]
