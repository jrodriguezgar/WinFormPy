"""
Word Processor Demo - WordPad-style editor

This example demonstrates:
- Rich text editing (Bold, Italic, Underline, Strikethrough)
- Font and color selection
- Text alignment
- File operations (New, Open, Save, Save As, Print)
- Find and Replace
- Insert Date/Time
- Zoom control
- Status bar with word count
"""

import sys
import os

# Add project root to path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy.winformpy import Application
from winformpy.ui_elements.word_processor.word_processor_ui import WordProcessorForm


def main():
    """Run word processor demo."""
    print("=" * 60)
    print("  WORD PROCESSOR DEMO")
    print("=" * 60)
    print("\nFeatures:")
    print("  • Rich text formatting (Bold, Italic, Underline, etc.)")
    print("  • Font family and size selection")
    print("  • Text and background colors")
    print("  • Text alignment (Left, Center, Right)")
    print("  • File operations (Open, Save, Print)")
    print("  • Find and Replace")
    print("  • Insert Date/Time")
    print("  • Zoom control (50% - 200%)")
    print("  • Word count and cursor position")
    print("  • Recent files tracking")
    print()
    print("Starting word processor...")
    
    form = WordProcessorForm()
    Application.Run(form)


if __name__ == "__main__":
    main()
