"""
Word Processor UI Element for WinFormPy.

Provides a complete word processor component with formatting toolbar,
RichTextBox editor, and status bar.

Architecture:
    - **Primitives Layer** (`word_processor_primitives.py`): Low-level text and file operations
    - **UI Layer** (`word_processor_panel.py`, `word_processor_ui.py`): Visual components
"""

from .word_processor_primitives import (
    WordProcessorPrimitives,
    FileFormat,
    TextAlignment,
    TextStyle,
    SearchOptions,
    TextRange,
    TextFormat,
    SearchResult,
    DocumentInfo,
    TextStatistics
)

from .word_processor_panel import WordProcessorPanel
from .word_processor_ui import WordProcessorForm

__all__ = [
    # Primitives
    'WordProcessorPrimitives',
    'FileFormat',
    'TextAlignment',
    'TextStyle',
    'SearchOptions',
    'TextRange',
    'TextFormat',
    'SearchResult',
    'DocumentInfo',
    'TextStatistics',
    
    # UI
    'WordProcessorPanel',
    'WordProcessorForm'
]
