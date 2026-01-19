"""
Word Processor Primitives - Low-level text and file operations.

This module provides the primitive operations for word processing:
- File I/O operations (load, save RTF/plain text)
- Text formatting operations
- Search and replace operations
- Clipboard operations
- Text analysis (word count, etc.)

Architecture:
    WordProcessorPrimitives (this module)
        ↓ used by
    WordProcessorManager (business logic) [optional]
        ↓ used by
    WordProcessorPanel/WordProcessorForm (UI)

Note: This is an abstraction layer that wraps low-level text operations.
The UI components can use these primitives directly or through a manager.
"""

import os
import re
from enum import Enum, Flag, auto
from typing import List, Optional, Tuple, Dict, Any
from dataclasses import dataclass, field


# =============================================================================
# Enums
# =============================================================================

class FileFormat(Enum):
    """Supported file formats."""
    PLAIN_TEXT = "txt"
    RICH_TEXT = "rtf"
    HTML = "html"
    AUTO = "auto"  # Detect from extension


class TextAlignment(Enum):
    """Text alignment options."""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"


class TextStyle(Flag):
    """Text style flags."""
    NONE = 0
    BOLD = auto()
    ITALIC = auto()
    UNDERLINE = auto()
    STRIKETHROUGH = auto()


class SearchOptions(Flag):
    """Search option flags."""
    NONE = 0
    MATCH_CASE = auto()
    WHOLE_WORD = auto()
    REGEX = auto()
    REVERSE = auto()


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class TextRange:
    """Represents a range of text."""
    start: int
    end: int
    text: str = ""
    
    @property
    def length(self) -> int:
        return self.end - self.start


@dataclass
class TextFormat:
    """Represents text formatting."""
    font_family: str = "Segoe UI"
    font_size: float = 11.0
    style: TextStyle = TextStyle.NONE
    alignment: TextAlignment = TextAlignment.LEFT
    fore_color: str = "#000000"
    back_color: str = "#FFFFFF"
    
    @property
    def is_bold(self) -> bool:
        return TextStyle.BOLD in self.style
    
    @property
    def is_italic(self) -> bool:
        return TextStyle.ITALIC in self.style
    
    @property
    def is_underline(self) -> bool:
        return TextStyle.UNDERLINE in self.style


@dataclass
class SearchResult:
    """Represents a search result."""
    start: int
    end: int
    text: str
    line_number: int = 0
    line_text: str = ""


@dataclass
class DocumentInfo:
    """Information about a document."""
    file_path: Optional[str] = None
    file_format: FileFormat = FileFormat.PLAIN_TEXT
    encoding: str = "utf-8"
    is_modified: bool = False
    created_date: Optional[str] = None
    modified_date: Optional[str] = None
    title: str = "Untitled"
    author: str = ""
    
    @property
    def file_name(self) -> str:
        if self.file_path:
            return os.path.basename(self.file_path)
        return self.title
    
    @property
    def extension(self) -> str:
        if self.file_path:
            _, ext = os.path.splitext(self.file_path)
            return ext.lower()
        return ".txt"


@dataclass
class TextStatistics:
    """Text statistics."""
    character_count: int = 0
    character_count_no_spaces: int = 0
    word_count: int = 0
    line_count: int = 0
    paragraph_count: int = 0
    sentence_count: int = 0
    
    def __str__(self) -> str:
        return (f"Words: {self.word_count}, "
                f"Characters: {self.character_count}, "
                f"Lines: {self.line_count}")


# =============================================================================
# Primitive Operations
# =============================================================================

class WordProcessorPrimitives:
    """
    Low-level word processor operations.
    
    This class provides primitive operations that can be used directly
    by UI components or through a manager layer.
    
    All methods are designed to work with plain text content.
    Subclasses can override for specific text widget implementations.
    """
    
    def __init__(self):
        """Initialize the primitives."""
        self._content = ""
        self._document_info = DocumentInfo()
        self._undo_stack: List[str] = []
        self._redo_stack: List[str] = []
        self._max_undo = 100
    
    # =========================================================================
    # Properties
    # =========================================================================
    
    @property
    def content(self) -> str:
        """Get the current content."""
        return self._content
    
    @content.setter
    def content(self, value: str):
        """Set the content."""
        self._push_undo()
        self._content = value
    
    @property
    def document_info(self) -> DocumentInfo:
        """Get document information."""
        return self._document_info
    
    # =========================================================================
    # File Operations
    # =========================================================================
    
    def new_document(self) -> bool:
        """
        Create a new empty document.
        
        Returns:
            bool: True if successful
        """
        self._push_undo()
        self._content = ""
        self._document_info = DocumentInfo()
        self._undo_stack.clear()
        self._redo_stack.clear()
        return True
    
    def load_file(self, file_path: str, 
                  format_: FileFormat = FileFormat.AUTO,
                  encoding: str = "utf-8") -> bool:
        """
        Load a document from file.
        
        Args:
            file_path: Path to the file
            format_: File format (AUTO detects from extension)
            encoding: Text encoding for plain text files
            
        Returns:
            bool: True if loaded successfully
        """
        if not os.path.exists(file_path):
            return False
        
        try:
            # Detect format from extension if AUTO
            if format_ == FileFormat.AUTO:
                format_ = self._detect_format(file_path)
            
            # Read file content
            if format_ == FileFormat.PLAIN_TEXT:
                with open(file_path, 'r', encoding=encoding) as f:
                    self._content = f.read()
            elif format_ == FileFormat.RICH_TEXT:
                # RTF needs special handling - for now read as binary
                with open(file_path, 'rb') as f:
                    # This would need RTF parsing
                    self._content = f.read().decode('latin-1', errors='ignore')
            else:
                with open(file_path, 'r', encoding=encoding) as f:
                    self._content = f.read()
            
            # Update document info
            self._document_info.file_path = file_path
            self._document_info.file_format = format_
            self._document_info.encoding = encoding
            self._document_info.is_modified = False
            self._document_info.title = os.path.basename(file_path)
            
            # Clear undo/redo
            self._undo_stack.clear()
            self._redo_stack.clear()
            
            return True
        except Exception:
            return False
    
    def save_file(self, file_path: str = None,
                  format_: FileFormat = FileFormat.AUTO,
                  encoding: str = "utf-8") -> bool:
        """
        Save the document to file.
        
        Args:
            file_path: Path to save to (uses current if None)
            format_: File format
            encoding: Text encoding
            
        Returns:
            bool: True if saved successfully
        """
        # Use current path if none provided
        if file_path is None:
            file_path = self._document_info.file_path
        
        if not file_path:
            return False
        
        try:
            # Detect format from extension if AUTO
            if format_ == FileFormat.AUTO:
                format_ = self._detect_format(file_path)
            
            # Write content
            if format_ == FileFormat.PLAIN_TEXT:
                with open(file_path, 'w', encoding=encoding) as f:
                    f.write(self._content)
            elif format_ == FileFormat.RICH_TEXT:
                # RTF would need special handling
                # For now, save as plain text with RTF extension
                with open(file_path, 'w', encoding=encoding) as f:
                    f.write(self._content)
            else:
                with open(file_path, 'w', encoding=encoding) as f:
                    f.write(self._content)
            
            # Update document info
            self._document_info.file_path = file_path
            self._document_info.file_format = format_
            self._document_info.is_modified = False
            self._document_info.title = os.path.basename(file_path)
            
            return True
        except Exception:
            return False
    
    def _detect_format(self, file_path: str) -> FileFormat:
        """Detect file format from extension."""
        _, ext = os.path.splitext(file_path.lower())
        
        if ext == '.rtf':
            return FileFormat.RICH_TEXT
        elif ext in ['.html', '.htm']:
            return FileFormat.HTML
        else:
            return FileFormat.PLAIN_TEXT
    
    # =========================================================================
    # Text Operations
    # =========================================================================
    
    def get_text(self, start: int = None, end: int = None) -> str:
        """
        Get text in a range.
        
        Args:
            start: Start position (0 if None)
            end: End position (end of content if None)
            
        Returns:
            Text in the range
        """
        start = start or 0
        end = end if end is not None else len(self._content)
        return self._content[start:end]
    
    def set_text(self, text: str, start: int = None, end: int = None) -> bool:
        """
        Set text in a range (replace).
        
        Args:
            text: Text to insert
            start: Start position
            end: End position
            
        Returns:
            bool: True if successful
        """
        self._push_undo()
        
        start = start or 0
        end = end if end is not None else len(self._content)
        
        self._content = self._content[:start] + text + self._content[end:]
        self._document_info.is_modified = True
        return True
    
    def insert_text(self, text: str, position: int) -> bool:
        """
        Insert text at position.
        
        Args:
            text: Text to insert
            position: Insert position
            
        Returns:
            bool: True if successful
        """
        return self.set_text(text, position, position)
    
    def delete_text(self, start: int, end: int) -> bool:
        """
        Delete text in range.
        
        Args:
            start: Start position
            end: End position
            
        Returns:
            bool: True if successful
        """
        return self.set_text("", start, end)
    
    def append_text(self, text: str) -> bool:
        """
        Append text at the end.
        
        Args:
            text: Text to append
            
        Returns:
            bool: True if successful
        """
        return self.insert_text(text, len(self._content))
    
    def clear(self) -> bool:
        """
        Clear all content.
        
        Returns:
            bool: True if successful
        """
        return self.set_text("", 0, len(self._content))
    
    # =========================================================================
    # Search Operations
    # =========================================================================
    
    def find(self, search_text: str, start: int = 0,
             options: SearchOptions = SearchOptions.NONE) -> Optional[SearchResult]:
        """
        Find text in content.
        
        Args:
            search_text: Text to find
            start: Start position
            options: Search options
            
        Returns:
            SearchResult or None if not found
        """
        if not search_text:
            return None
        
        content = self._content
        
        # Case sensitivity
        if SearchOptions.MATCH_CASE not in options:
            content = content.lower()
            search_text = search_text.lower()
        
        # Regex search
        if SearchOptions.REGEX in options:
            try:
                flags = 0 if SearchOptions.MATCH_CASE in options else re.IGNORECASE
                pattern = re.compile(search_text, flags)
                
                match = pattern.search(self._content, start)
                if match:
                    return SearchResult(
                        start=match.start(),
                        end=match.end(),
                        text=match.group(),
                        line_number=self._get_line_number(match.start())
                    )
            except re.error:
                return None
        else:
            # Simple search
            pos = content.find(search_text, start)
            if pos != -1:
                end_pos = pos + len(search_text)
                return SearchResult(
                    start=pos,
                    end=end_pos,
                    text=self._content[pos:end_pos],
                    line_number=self._get_line_number(pos)
                )
        
        return None
    
    def find_all(self, search_text: str,
                 options: SearchOptions = SearchOptions.NONE) -> List[SearchResult]:
        """
        Find all occurrences of text.
        
        Args:
            search_text: Text to find
            options: Search options
            
        Returns:
            List of SearchResult objects
        """
        results = []
        start = 0
        
        while True:
            result = self.find(search_text, start, options)
            if result is None:
                break
            results.append(result)
            start = result.end
        
        return results
    
    def replace(self, search_text: str, replace_text: str,
                start: int = 0,
                options: SearchOptions = SearchOptions.NONE) -> bool:
        """
        Replace first occurrence of text.
        
        Args:
            search_text: Text to find
            replace_text: Replacement text
            start: Start position
            options: Search options
            
        Returns:
            bool: True if replaced
        """
        result = self.find(search_text, start, options)
        if result:
            self.set_text(replace_text, result.start, result.end)
            return True
        return False
    
    def replace_all(self, search_text: str, replace_text: str,
                    options: SearchOptions = SearchOptions.NONE) -> int:
        """
        Replace all occurrences of text.
        
        Args:
            search_text: Text to find
            replace_text: Replacement text
            options: Search options
            
        Returns:
            int: Number of replacements made
        """
        count = 0
        
        if SearchOptions.REGEX in options:
            try:
                flags = 0 if SearchOptions.MATCH_CASE in options else re.IGNORECASE
                self._push_undo()
                self._content, count = re.subn(
                    search_text, replace_text, self._content, flags=flags
                )
                if count > 0:
                    self._document_info.is_modified = True
            except re.error:
                pass
        else:
            # Simple replace all
            self._push_undo()
            if SearchOptions.MATCH_CASE in options:
                new_content = self._content.replace(search_text, replace_text)
            else:
                # Case-insensitive replace
                pattern = re.compile(re.escape(search_text), re.IGNORECASE)
                new_content = pattern.sub(replace_text, self._content)
            
            count = self._content.count(search_text) if SearchOptions.MATCH_CASE in options else len(
                re.findall(re.escape(search_text), self._content, re.IGNORECASE)
            )
            
            if new_content != self._content:
                self._content = new_content
                self._document_info.is_modified = True
        
        return count
    
    def _get_line_number(self, position: int) -> int:
        """Get line number for a position."""
        return self._content[:position].count('\n') + 1
    
    # =========================================================================
    # Undo/Redo
    # =========================================================================
    
    def _push_undo(self):
        """Push current state to undo stack."""
        if len(self._undo_stack) >= self._max_undo:
            self._undo_stack.pop(0)
        self._undo_stack.append(self._content)
        self._redo_stack.clear()
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return len(self._undo_stack) > 0
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return len(self._redo_stack) > 0
    
    def undo(self) -> bool:
        """
        Undo last operation.
        
        Returns:
            bool: True if undone
        """
        if not self.can_undo():
            return False
        
        self._redo_stack.append(self._content)
        self._content = self._undo_stack.pop()
        return True
    
    def redo(self) -> bool:
        """
        Redo last undone operation.
        
        Returns:
            bool: True if redone
        """
        if not self.can_redo():
            return False
        
        self._undo_stack.append(self._content)
        self._content = self._redo_stack.pop()
        return True
    
    # =========================================================================
    # Text Analysis
    # =========================================================================
    
    def get_statistics(self) -> TextStatistics:
        """
        Get text statistics.
        
        Returns:
            TextStatistics object
        """
        content = self._content
        
        stats = TextStatistics()
        stats.character_count = len(content)
        stats.character_count_no_spaces = len(content.replace(' ', '').replace('\n', '').replace('\t', ''))
        stats.word_count = len(content.split()) if content.strip() else 0
        stats.line_count = content.count('\n') + 1 if content else 0
        stats.paragraph_count = len([p for p in content.split('\n\n') if p.strip()])
        stats.sentence_count = len(re.findall(r'[.!?]+', content))
        
        return stats
    
    def get_word_count(self) -> int:
        """Get word count."""
        return self.get_statistics().word_count
    
    def get_line_count(self) -> int:
        """Get line count."""
        return self.get_statistics().line_count
    
    def get_char_count(self, include_spaces: bool = True) -> int:
        """Get character count."""
        stats = self.get_statistics()
        return stats.character_count if include_spaces else stats.character_count_no_spaces
    
    # =========================================================================
    # Line Operations
    # =========================================================================
    
    def get_line(self, line_number: int) -> Optional[str]:
        """
        Get a specific line.
        
        Args:
            line_number: 1-based line number
            
        Returns:
            Line text or None if invalid
        """
        lines = self._content.split('\n')
        if 1 <= line_number <= len(lines):
            return lines[line_number - 1]
        return None
    
    def get_lines(self) -> List[str]:
        """Get all lines as a list."""
        return self._content.split('\n')
    
    def get_line_range(self, line_number: int) -> Optional[TextRange]:
        """
        Get the character range for a line.
        
        Args:
            line_number: 1-based line number
            
        Returns:
            TextRange or None if invalid
        """
        lines = self._content.split('\n')
        if not (1 <= line_number <= len(lines)):
            return None
        
        start = sum(len(lines[i]) + 1 for i in range(line_number - 1))
        end = start + len(lines[line_number - 1])
        
        return TextRange(start, end, lines[line_number - 1])
    
    def get_current_line(self, position: int) -> int:
        """
        Get line number at position.
        
        Args:
            position: Character position
            
        Returns:
            1-based line number
        """
        return self._get_line_number(position)
    
    def get_current_column(self, position: int) -> int:
        """
        Get column at position.
        
        Args:
            position: Character position
            
        Returns:
            1-based column number
        """
        line_start = self._content.rfind('\n', 0, position) + 1
        return position - line_start + 1
    
    # =========================================================================
    # Formatting Operations (Abstract - UI dependent)
    # =========================================================================
    
    def apply_bold(self, start: int, end: int) -> bool:
        """
        Apply bold formatting to range.
        Note: This is a placeholder. Actual implementation depends on the text widget.
        
        Args:
            start: Start position
            end: End position
            
        Returns:
            bool: True if applied
        """
        # Placeholder - actual formatting is widget-dependent
        return True
    
    def apply_italic(self, start: int, end: int) -> bool:
        """Apply italic formatting to range."""
        return True
    
    def apply_underline(self, start: int, end: int) -> bool:
        """Apply underline formatting to range."""
        return True
    
    def apply_font(self, start: int, end: int, font_family: str, font_size: float) -> bool:
        """Apply font to range."""
        return True
    
    def apply_color(self, start: int, end: int, color: str) -> bool:
        """Apply text color to range."""
        return True
    
    def apply_background(self, start: int, end: int, color: str) -> bool:
        """Apply background color to range."""
        return True
    
    def apply_alignment(self, alignment: TextAlignment) -> bool:
        """Apply text alignment."""
        return True
    
    def get_format_at(self, position: int) -> TextFormat:
        """
        Get formatting at position.
        
        Args:
            position: Character position
            
        Returns:
            TextFormat at position
        """
        # Return default format - actual implementation is widget-dependent
        return TextFormat()
