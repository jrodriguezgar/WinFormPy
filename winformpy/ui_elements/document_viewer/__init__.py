"""
Document Viewer UI Elements

This module provides components for previewing various document formats:
- PDF documents
- Word documents (.docx, .doc)
- Excel spreadsheets (.xlsx, .xls)
- PowerPoint presentations (.pptx, .ppt)
- Text files (.txt, .md, .log)
- Images (as document pages)
"""

from .document_viewer_panel import DocumentViewerPanel
from .document_viewer_ui import DocumentViewerForm, DocumentViewerDialog
from .document_backend import DocumentBackend, PDFBackend, WordBackend, ImageBackend

__all__ = [
    'DocumentViewerPanel',
    'DocumentViewerForm',
    'DocumentViewerDialog',
    'DocumentBackend',
    'PDFBackend',
    'WordBackend',
    'ImageBackend'
]
