"""
DataGrid UI Elements

This package provides components for displaying tabular data with
pagination, sorting, search, and selection capabilities.

Components:
- DataGridBackend: Abstract base class for data sources
- DataGridManager: Service layer handling state and operations
- DataGridPanel: Visual grid component
- DataGridForm: Standalone form with grid
- DataGridPickerForm: Record selector dialog

Note: RecordFormDialog (formerly RecordDetailForm) is in the record_form module.
      Import it from: winformpy.ui_elements.record_form

Enums and Data Classes:
- DataType: Column data types (STRING, INTEGER, FLOAT, CURRENCY, etc.)
- SortOrder: Sort directions (ASCENDING, DESCENDING, NONE)
- ColumnDefinition: Column configuration
- DataRequest: Request parameters for fetching data
- DataResponse: Response with records and pagination info
- PageInfo: Pagination information
"""

from .data_grid_backend import (
    DataGridBackend,
    DataType,
    SortOrder,
    ColumnDefinition,
    PageInfo,
    DataRequest,
    DataResponse,
)

from .data_grid_manager import DataGridManager

from .data_grid_panel import DataGridPanel

from .data_grid_ui import (
    DataGridForm,
    DataGridPickerForm,
)

__all__ = [
    # Backend
    'DataGridBackend',
    'DataType',
    'SortOrder',
    'ColumnDefinition',
    'PageInfo',
    'DataRequest',
    'DataResponse',
    # Manager
    'DataGridManager',
    # Panel
    'DataGridPanel',
    # UI Forms
    'DataGridForm',
    'DataGridPickerForm',
]
