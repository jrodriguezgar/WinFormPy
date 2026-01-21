"""
DataGrid Manager - Service layer for DataGrid operations.

This module provides the business logic layer between the UI and the backend.
"""

from typing import Any, List, Dict, Optional, Callable

# Handle imports for both module and direct execution
try:
    from .data_grid_backend import (
        DataGridBackend, DataRequest, DataResponse, 
        ColumnDefinition, PageInfo, SortOrder, DataType
    )
except ImportError:
    from data_grid_backend import (
        DataGridBackend, DataRequest, DataResponse, 
        ColumnDefinition, PageInfo, SortOrder, DataType
    )


class DataGridManager:
    """
    Manager class that handles data grid operations and state.
    
    This class:
    - Manages current page, sort, and filter state
    - Coordinates between UI and backend
    - Fires events for data changes
    - Handles selection state
    """
    
    def __init__(self, backend: DataGridBackend = None):
        """
        Initialize the DataGridManager.
        
        Args:
            backend: Optional DataGridBackend implementation.
        """
        self._backend = backend
        
        # State
        self._current_page = 1
        self._page_size = 20
        self._search_text = ""
        self._case_sensitive = False
        self._exact_match = False
        self._sort_column: str = None
        self._sort_order = SortOrder.NONE
        self._filters: Dict[str, Any] = {}
        self._selected_records: List[Dict[str, Any]] = []
        self._selected_indices: List[int] = []
        
        # Cached data
        self._columns: List[ColumnDefinition] = []
        self._records: List[Dict[str, Any]] = []
        self._page_info = PageInfo()
        
        # Events
        self.DataLoaded: Callable[[object, Dict], None] = lambda s, e: None
        self.DataLoadError: Callable[[object, Dict], None] = lambda s, e: None
        self.SelectionChanged: Callable[[object, Dict], None] = lambda s, e: None
        self.PageChanged: Callable[[object, Dict], None] = lambda s, e: None
        self.SortChanged: Callable[[object, Dict], None] = lambda s, e: None
        self.SearchChanged: Callable[[object, Dict], None] = lambda s, e: None
    
    @property
    def backend(self) -> DataGridBackend:
        """Get the current backend."""
        return self._backend
    
    @backend.setter
    def backend(self, value: DataGridBackend):
        """Set a new backend and refresh data."""
        self._backend = value
        self._reset_state()
        if value:
            self._load_columns()
    
    @property
    def columns(self) -> List[ColumnDefinition]:
        """Get the current column definitions."""
        return self._columns
    
    @property
    def records(self) -> List[Dict[str, Any]]:
        """Get the current page of records."""
        return self._records
    
    @property
    def page_info(self) -> PageInfo:
        """Get the current page information."""
        return self._page_info
    
    @property
    def current_page(self) -> int:
        """Get the current page number."""
        return self._current_page
    
    @property
    def page_size(self) -> int:
        """Get the current page size."""
        return self._page_size
    
    @page_size.setter
    def page_size(self, value: int):
        """Set the page size and refresh data."""
        if value != self._page_size and value > 0:
            self._page_size = value
            self._current_page = 1
            self.refresh()
    
    @property
    def search_text(self) -> str:
        """Get the current search text."""
        return self._search_text
    
    @property
    def case_sensitive(self) -> bool:
        """Get whether search is case-sensitive."""
        return self._case_sensitive
    
    @case_sensitive.setter
    def case_sensitive(self, value: bool):
        """Set whether search is case-sensitive."""
        self._case_sensitive = value
    
    @property
    def exact_match(self) -> bool:
        """Get whether search requires exact match."""
        return self._exact_match
    
    @exact_match.setter
    def exact_match(self, value: bool):
        """Set whether search requires exact match."""
        self._exact_match = value
    
    @property
    def sort_column(self) -> str:
        """Get the current sort column."""
        return self._sort_column
    
    @property
    def sort_order(self) -> SortOrder:
        """Get the current sort order."""
        return self._sort_order
    
    @property
    def selected_records(self) -> List[Dict[str, Any]]:
        """Get the currently selected records."""
        return self._selected_records
    
    @property
    def selected_indices(self) -> List[int]:
        """Get the indices of selected records."""
        return self._selected_indices
    
    @property
    def has_previous_page(self) -> bool:
        """Check if there is a previous page."""
        return self._current_page > 1
    
    @property
    def has_next_page(self) -> bool:
        """Check if there is a next page."""
        return self._current_page < self._page_info.total_pages
    
    def _reset_state(self):
        """Reset all state to initial values."""
        self._current_page = 1
        self._search_text = ""
        self._sort_column = None
        self._sort_order = SortOrder.NONE
        self._filters = {}
        self._selected_records = []
        self._selected_indices = []
        self._columns = []
        self._records = []
        self._page_info = PageInfo()
    
    def _load_columns(self):
        """Load column definitions from backend."""
        if self._backend:
            self._columns = self._backend.get_columns()
    
    def _create_request(self) -> DataRequest:
        """Create a data request from current state."""
        return DataRequest(
            page=self._current_page,
            page_size=self._page_size,
            search_text=self._search_text,
            case_sensitive=self._case_sensitive,
            exact_match=self._exact_match,
            sort_column=self._sort_column,
            sort_order=self._sort_order,
            filters=self._filters.copy()
        )
    
    def refresh(self):
        """Refresh data from the backend."""
        if not self._backend:
            return
        
        try:
            request = self._create_request()
            response = self._backend.fetch_data(request)
            
            if response.success:
                self._records = response.records
                self._page_info = response.page_info
                
                if response.columns:
                    self._columns = response.columns
                
                self.DataLoaded(self, {
                    'records': self._records,
                    'page_info': self._page_info,
                    'columns': self._columns
                })
            else:
                self.DataLoadError(self, {'message': response.error_message})
                
        except Exception as e:
            self.DataLoadError(self, {'message': str(e)})
    
    def search(self, text: str, case_sensitive: bool = None, exact_match: bool = None):
        """
        Search records with the given text.
        
        Args:
            text: Search text to filter records.
            case_sensitive: Whether search is case-sensitive. If None, uses current setting.
            exact_match: Whether search requires exact match. If None, uses current setting.
        """
        self._search_text = text
        if case_sensitive is not None:
            self._case_sensitive = case_sensitive
        if exact_match is not None:
            self._exact_match = exact_match
        self._current_page = 1
        self._selected_records = []
        self._selected_indices = []
        
        self.SearchChanged(self, {
            'search_text': text,
            'case_sensitive': self._case_sensitive,
            'exact_match': self._exact_match
        })
        self.refresh()
    
    def clear_search(self):
        """Clear the current search."""
        self.search("")
    
    def sort(self, column_name: str):
        """
        Sort by the specified column.
        
        Toggles between ascending, descending, and no sort.
        
        Args:
            column_name: Name of the column to sort by.
        """
        if self._sort_column == column_name:
            # Toggle sort order
            if self._sort_order == SortOrder.ASCENDING:
                self._sort_order = SortOrder.DESCENDING
            elif self._sort_order == SortOrder.DESCENDING:
                self._sort_order = SortOrder.NONE
                self._sort_column = None
            else:
                self._sort_order = SortOrder.ASCENDING
        else:
            self._sort_column = column_name
            self._sort_order = SortOrder.ASCENDING
        
        self.SortChanged(self, {
            'column': self._sort_column,
            'order': self._sort_order
        })
        self.refresh()
    
    def go_to_page(self, page: int):
        """
        Go to a specific page.
        
        Args:
            page: Page number (1-based).
        """
        if page < 1:
            page = 1
        elif page > self._page_info.total_pages:
            page = self._page_info.total_pages
        
        if page != self._current_page and page >= 1:
            self._current_page = page
            self._selected_records = []
            self._selected_indices = []
            
            self.PageChanged(self, {'page': page})
            self.refresh()
    
    def next_page(self):
        """Go to the next page."""
        if self.has_next_page:
            self.go_to_page(self._current_page + 1)
    
    def previous_page(self):
        """Go to the previous page."""
        if self.has_previous_page:
            self.go_to_page(self._current_page - 1)
    
    def first_page(self):
        """Go to the first page."""
        self.go_to_page(1)
    
    def last_page(self):
        """Go to the last page."""
        self.go_to_page(self._page_info.total_pages)
    
    def select_record(self, index: int, multi_select: bool = False):
        """
        Select a record by index.
        
        Args:
            index: Index of the record to select.
            multi_select: If True, add to selection; if False, replace selection.
        """
        if index < 0 or index >= len(self._records):
            return
        
        record = self._records[index]
        
        if multi_select:
            if index in self._selected_indices:
                self._selected_indices.remove(index)
                self._selected_records.remove(record)
            else:
                self._selected_indices.append(index)
                self._selected_records.append(record)
        else:
            self._selected_indices = [index]
            self._selected_records = [record]
        
        # Track last selected index for range selection
        self._last_selected_index = index
        
        self.SelectionChanged(self, {
            'selected_records': self._selected_records,
            'selected_indices': self._selected_indices
        })
    
    def select_range(self, end_index: int):
        """
        Select a range of records from the last selected index to end_index.
        Used for Shift+Click selection.
        
        Args:
            end_index: End index of the range to select.
        """
        if end_index < 0 or end_index >= len(self._records):
            return
        
        # Get start index (last selected or 0)
        start_index = getattr(self, '_last_selected_index', 0)
        
        # Determine range (handle both directions)
        if start_index <= end_index:
            indices = list(range(start_index, end_index + 1))
        else:
            indices = list(range(end_index, start_index + 1))
        
        # Select all records in range
        self._selected_indices = indices
        self._selected_records = [self._records[i] for i in indices]
        
        self.SelectionChanged(self, {
            'selected_records': self._selected_records,
            'selected_indices': self._selected_indices
        })
    
    def select_all(self):
        """Select all records on the current page."""
        self._selected_indices = list(range(len(self._records)))
        self._selected_records = self._records.copy()
        
        self.SelectionChanged(self, {
            'selected_records': self._selected_records,
            'selected_indices': self._selected_indices
        })
    
    def clear_selection(self):
        """Clear all selections."""
        self._selected_indices = []
        self._selected_records = []
        
        self.SelectionChanged(self, {
            'selected_records': [],
            'selected_indices': []
        })
    
    def set_filter(self, column_name: str, value: Any):
        """
        Set a filter on a column.
        
        Args:
            column_name: Name of the column to filter.
            value: Filter value.
        """
        self._filters[column_name] = value
        self._current_page = 1
        self.refresh()
    
    def clear_filter(self, column_name: str):
        """
        Clear a filter on a column.
        
        Args:
            column_name: Name of the column to clear filter from.
        """
        if column_name in self._filters:
            del self._filters[column_name]
            self._current_page = 1
            self.refresh()
    
    def clear_all_filters(self):
        """Clear all filters."""
        self._filters = {}
        self._current_page = 1
        self.refresh()
    
    def get_formatted_value(self, record: Dict[str, Any], column_name: str) -> str:
        """
        Get a formatted value for display.
        
        Args:
            record: The record dictionary.
            column_name: The column name.
            
        Returns:
            Formatted string value.
        """
        if not self._backend:
            return str(record.get(column_name, ""))
        
        column = next((c for c in self._columns if c.name == column_name), None)
        if column:
            return self._backend.format_value(record.get(column_name), column)
        return str(record.get(column_name, ""))
