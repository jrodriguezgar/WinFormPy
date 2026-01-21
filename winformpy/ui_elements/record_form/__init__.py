"""
Record Form UI Element

Provides embeddable panels and standalone forms for displaying
and editing individual record details with auto-generated fields.
Supports pluggable backend architecture for CRUD operations.
"""

from .record_form_panel import RecordFormPanel
from .record_form_ui import RecordFormDialog
from .record_form_backend import (
    RecordFormBackend,
    RecordFormMode,
    RecordResponse,
    ValidationResult,
    InMemoryRecordBackend,
    create_record_backend
)

# Backwards compatibility aliases
RecordDetailPanel = RecordFormPanel
RecordDetailForm = RecordFormDialog

__all__ = [
    # Main components
    'RecordFormPanel',
    'RecordFormDialog',
    # Backend architecture
    'RecordFormBackend',
    'RecordFormMode',
    'RecordResponse',
    'ValidationResult',
    'InMemoryRecordBackend',
    'create_record_backend',
    # Backwards compatibility
    'RecordDetailPanel',
    'RecordDetailForm',
]
