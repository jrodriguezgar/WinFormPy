"""
DataGrid Backend - Abstract base class for data grid backends.

This module defines the contract that all data grid backends must implement.
The backend is responsible for fetching data, filtering, and pagination.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Dict, Optional, Callable


class DataType(Enum):
    """Supported data types for column formatting."""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    CURRENCY = "currency"
    DATE = "date"
    DATETIME = "datetime"
    BOOLEAN = "boolean"
    PERCENTAGE = "percentage"


class SortOrder(Enum):
    """Sort order for columns."""
    NONE = "none"
    ASCENDING = "asc"
    DESCENDING = "desc"


@dataclass
class ColumnDefinition:
    """Definition of a column in the data grid."""
    name: str                          # Internal field name
    header: str                        # Display header text
    data_type: DataType = DataType.STRING
    width: int = 100                   # Column width in pixels
    sortable: bool = True              # Whether column can be sorted
    searchable: bool = True            # Whether column is included in search
    visible: bool = True               # Whether column is visible
    format_string: str = None          # Custom format string (e.g., "{:.2f}", "%Y-%m-%d")
    align: str = "left"                # Text alignment: left, center, right


@dataclass
class PageInfo:
    """Information about the current page of data."""
    current_page: int = 1
    page_size: int = 20
    total_records: int = 0
    total_pages: int = 0
    
    @property
    def start_record(self) -> int:
        """Get the 1-based index of the first record on this page."""
        return ((self.current_page - 1) * self.page_size) + 1
    
    @property
    def end_record(self) -> int:
        """Get the 1-based index of the last record on this page."""
        return min(self.current_page * self.page_size, self.total_records)


@dataclass
class DataRequest:
    """Request parameters for fetching data."""
    page: int = 1
    page_size: int = 20
    search_text: str = ""
    case_sensitive: bool = False  # Whether search is case-sensitive
    exact_match: bool = False  # Whether search requires exact match
    sort_column: str = None
    sort_order: SortOrder = SortOrder.NONE
    filters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DataResponse:
    """Response from the backend containing data and metadata."""
    records: List[Dict[str, Any]]
    page_info: PageInfo
    columns: List[ColumnDefinition] = field(default_factory=list)
    success: bool = True
    error_message: str = ""


class DataGridBackend(ABC):
    """
    Abstract base class for DataGrid backends.
    
    Implement this class to connect the DataGrid to any data source:
    - SQL databases (SQLite, PostgreSQL, MySQL, etc.)
    - REST APIs
    - CSV/Excel files
    - In-memory collections
    - NoSQL databases
    
    Example:
        class SQLiteBackend(DataGridBackend):
            def __init__(self, connection, table_name):
                self.conn = connection
                self.table = table_name
            
            def get_columns(self) -> List[ColumnDefinition]:
                # Return column definitions from table schema
                ...
            
            def fetch_data(self, request: DataRequest) -> DataResponse:
                # Execute SQL query with pagination and filtering
                ...
    """
    
    @abstractmethod
    def get_columns(self) -> List[ColumnDefinition]:
        """
        Get the column definitions for the data grid.
        
        Returns:
            List of ColumnDefinition objects describing each column.
        """
        pass
    
    @abstractmethod
    def fetch_data(self, request: DataRequest) -> DataResponse:
        """
        Fetch data from the backend with pagination, sorting, and filtering.
        
        Args:
            request: DataRequest containing page, search, sort parameters.
            
        Returns:
            DataResponse containing records and pagination info.
        """
        pass
    
    def get_total_count(self, search_text: str = "", filters: Dict[str, Any] = None) -> int:
        """
        Get the total number of records matching the criteria.
        
        Override this for optimized count queries.
        
        Args:
            search_text: Optional search text to filter records.
            filters: Optional additional filters.
            
        Returns:
            Total number of matching records.
        """
        # Default implementation - subclasses should override for efficiency
        request = DataRequest(page=1, page_size=1000000, search_text=search_text, filters=filters or {})
        response = self.fetch_data(request)
        return len(response.records)
    
    def format_value(self, value: Any, column: ColumnDefinition) -> str:
        """
        Format a value according to its column definition.
        
        Args:
            value: The raw value to format.
            column: The column definition with type and format info.
            
        Returns:
            Formatted string representation of the value.
        """
        if value is None:
            return ""
        
        try:
            if column.data_type == DataType.STRING:
                return str(value)
            
            elif column.data_type == DataType.INTEGER:
                if column.format_string:
                    return column.format_string.format(int(value))
                return f"{int(value):,}"
            
            elif column.data_type == DataType.FLOAT:
                if column.format_string:
                    return column.format_string.format(float(value))
                return f"{float(value):,.2f}"
            
            elif column.data_type == DataType.CURRENCY:
                if column.format_string:
                    return column.format_string.format(float(value))
                return f"${float(value):,.2f}"
            
            elif column.data_type == DataType.PERCENTAGE:
                if column.format_string:
                    return column.format_string.format(float(value))
                return f"{float(value):.1f}%"
            
            elif column.data_type == DataType.DATE:
                if column.format_string:
                    return value.strftime(column.format_string)
                return value.strftime("%Y-%m-%d") if hasattr(value, 'strftime') else str(value)
            
            elif column.data_type == DataType.DATETIME:
                if column.format_string:
                    return value.strftime(column.format_string)
                return value.strftime("%Y-%m-%d %H:%M") if hasattr(value, 'strftime') else str(value)
            
            elif column.data_type == DataType.BOOLEAN:
                return "Yes" if value else "No"
            
            else:
                return str(value)
                
        except (ValueError, TypeError, AttributeError):
            return str(value)
    
    def export_data(self, request: DataRequest, format: str = "csv") -> bytes:
        """
        Export data in the specified format.
        
        Override this for custom export functionality.
        
        Args:
            request: DataRequest (page_size should be large for full export).
            format: Export format ("csv", "json", "excel").
            
        Returns:
            Bytes of the exported data.
        """
        raise NotImplementedError("Export not implemented in this backend")
    
    def refresh(self) -> None:
        """
        Refresh any cached data.
        
        Override this if your backend caches data.
        """
        pass
    
    # =========================================================================
    # CRUD Operations (Override in subclasses for data modification support)
    # =========================================================================
    
    def supports_crud(self) -> bool:
        """
        Check if this backend supports CRUD operations.
        
        Returns:
            True if create, update, delete operations are supported.
        """
        return False
    
    def get_primary_key(self) -> str:
        """
        Get the primary key column name.
        
        Returns:
            Name of the primary key column, or None if not applicable.
        """
        return None
    
    def create_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new record in the data source.
        
        Args:
            record: Dictionary with field values for the new record.
            
        Returns:
            The created record (including any auto-generated fields like ID).
            
        Raises:
            NotImplementedError: If CRUD is not supported.
        """
        raise NotImplementedError("Create not implemented in this backend")
    
    def update_record(self, primary_key_value: Any, changes: Dict[str, Any]) -> bool:
        """
        Update an existing record in the data source.
        
        Args:
            primary_key_value: Value of the primary key for the record to update.
            changes: Dictionary with field names and new values.
            
        Returns:
            True if update was successful, False otherwise.
            
        Raises:
            NotImplementedError: If CRUD is not supported.
        """
        raise NotImplementedError("Update not implemented in this backend")
    
    def delete_record(self, primary_key_value: Any) -> bool:
        """
        Delete a record from the data source.
        
        Args:
            primary_key_value: Value of the primary key for the record to delete.
            
        Returns:
            True if delete was successful, False otherwise.
            
        Raises:
            NotImplementedError: If CRUD is not supported.
        """
        raise NotImplementedError("Delete not implemented in this backend")
    
    def validate_record(self, record: Dict[str, Any], is_new: bool = False) -> tuple[bool, str]:
        """
        Validate a record before creating or updating.
        
        Args:
            record: Dictionary with field values to validate.
            is_new: True if this is a new record, False if updating.
            
        Returns:
            Tuple of (is_valid, error_message). If valid, error_message is empty.
        """
        return True, ""
