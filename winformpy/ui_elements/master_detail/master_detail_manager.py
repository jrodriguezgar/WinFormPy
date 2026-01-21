"""
Master-Detail Manager - Service layer for Master-Detail operations.

This module manages the state and data flow between master and detail grids.
"""

from typing import Any, Optional, Callable

import sys
import os

# Handle imports for both module and direct execution
try:
    from ..data_grid.data_grid_backend import DataRequest, DataResponse, PageInfo
    from .master_detail_backend import MasterDetailBackend, MasterType, MasterListResponse
except ImportError:
    # Direct execution - add paths
    _current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(_current_dir, '..', 'data_grid'))
    from data_grid_backend import DataRequest, DataResponse, PageInfo
    from master_detail_backend import MasterDetailBackend, MasterType, MasterListResponse


class MasterDetailManager:
    """
    Manages the state and data flow for the Master-Detail component.
    
    This manager:
    - Fetches data from the backend
    - Maintains selection state
    - Coordinates master selection → detail refresh
    - Provides formatted values
    
    Example:
        backend = CustomerOrdersBackend()
        manager = MasterDetailManager(backend)
        
        # Get master columns
        columns = manager.get_master_columns()
        
        # Fetch master data
        request = DataRequest(page=1, page_size=20)
        response = manager.fetch_master_data(request)
        
        # Select a master record
        manager.set_selected_master_id(1)
        
        # Fetch detail data
        detail_response = manager.fetch_detail_data(request)
    """
    
    def __init__(self, backend: MasterDetailBackend):
        """
        Initialize the manager with a backend.
        
        Args:
            backend: Implementation of MasterDetailBackend
        """
        self._backend = backend
        self._selected_master_id: Any = None
        self._selected_master_record: dict = None
        
        # Callbacks
        self._on_master_selection_changed: Callable[[Any], None] = None
        self._on_detail_data_changed: Callable[[], None] = None
        self._on_master_data_changed: Callable[[], None] = None
    
    # =========================================================================
    # Properties
    # =========================================================================
    
    @property
    def backend(self) -> MasterDetailBackend:
        """Get the backend instance."""
        return self._backend
    
    @property
    def selected_master_id(self) -> Any:
        """Get the currently selected master ID."""
        return self._selected_master_id
    
    @property
    def selected_master_record(self) -> dict:
        """Get the currently selected master record."""
        return self._selected_master_record
    
    @property
    def on_master_selection_changed(self) -> Callable[[Any], None]:
        """Get/set callback for master selection changes."""
        return self._on_master_selection_changed
    
    @on_master_selection_changed.setter
    def on_master_selection_changed(self, callback: Callable[[Any], None]):
        self._on_master_selection_changed = callback
    
    @property
    def on_detail_data_changed(self) -> Callable[[], None]:
        """Get/set callback for detail data changes."""
        return self._on_detail_data_changed
    
    @on_detail_data_changed.setter
    def on_detail_data_changed(self, callback: Callable[[], None]):
        self._on_detail_data_changed = callback

    @property
    def on_master_data_changed(self) -> Callable[[], None]:
        """Get/set callback for master data changes."""
        return self._on_master_data_changed

    @on_master_data_changed.setter
    def on_master_data_changed(self, callback: Callable[[], None]):
        self._on_master_data_changed = callback

    # =========================================================================
    # Master Methods
    # =========================================================================

    def get_master_type(self) -> MasterType:
        """Get the type of master view (DataGrid or ListView)."""
        return self._backend.get_master_type()
    
    def get_master_title(self) -> str:
        """Get the title for the master panel."""
        return self._backend.get_master_title()
    
    def get_master_columns(self):
        """Get column definitions for the master grid."""
        return self._backend.get_master_columns()
    
    def get_master_id_field(self) -> str:
        """Get the field name for the master ID."""
        return self._backend.get_master_id_field()
    
    def fetch_master_data(self, request: DataRequest) -> DataResponse:
        """
        Fetch data for the master grid.
        
        Args:
            request: DataRequest with pagination, sorting, filtering
            
        Returns:
            DataResponse with records and page info
        """
        return self._backend.fetch_master_data(request)
    
    def fetch_master_list(self) -> MasterListResponse:
        """
        Fetch items for the master list view.
        
        Returns:
            MasterListResponse with list items
        """
        return self._backend.fetch_master_list()
    
    def format_master_value(self, value: Any, column) -> str:
        """Format a value for display in the master grid."""
        return self._backend.format_master_value(value, column)
    
    def set_selected_master_id(self, master_id: Any, record: dict = None):
        """
        Set the selected master record.
        
        This will trigger detail data refresh.
        
        Args:
            master_id: The ID of the selected master record
            record: The full master record (optional)
        """
        old_id = self._selected_master_id
        self._selected_master_id = master_id
        self._selected_master_record = record
        
        if old_id != master_id:
            if self._on_master_selection_changed:
                self._on_master_selection_changed(master_id)
    
    def clear_master_selection(self):
        """Clear the master selection."""
        self.set_selected_master_id(None, None)
    
    # =========================================================================
    # Detail Methods
    # =========================================================================
    
    def get_detail_title(self) -> str:
        """Get the title for the detail panel."""
        return self._backend.get_detail_title()
    
    def get_detail_columns(self):
        """Get column definitions for the detail grid."""
        return self._backend.get_detail_columns()
    
    def fetch_detail_data(self, request: DataRequest) -> DataResponse:
        """
        Fetch detail data for the currently selected master record.
        
        Args:
            request: DataRequest with pagination, sorting, filtering
            
        Returns:
            DataResponse with detail records and page info
        """
        if self._selected_master_id is None:
            return DataResponse(records=[], page_info=PageInfo())
        
        return self._backend.fetch_detail_data(self._selected_master_id, request)
    
    def format_detail_value(self, value: Any, column) -> str:
        """Format a value for display in the detail grid."""
        return self._backend.format_detail_value(value, column)
    
    # =========================================================================
    # Refresh
    # =========================================================================
    
    def refresh_detail(self):
        """Notify that detail data should be refreshed."""
        if self._on_detail_data_changed:
            self._on_detail_data_changed()

    def refresh_master(self):
        """Notify that master data should be refreshed."""
        if self._on_master_data_changed:
            self._on_master_data_changed()
