"""
Master-Detail Backend - Abstract base classes for Master-Detail data sources.

This module defines the contracts that external backends must implement
to provide data for the Master-Detail component.

Architecture:
    MasterDetailBackend (ABC)
        ↓ implemented by
    YourCustomBackend (your code)
        ↓ used by
    MasterDetailManager
        ↓ used by
    MasterDetailPanel
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum

import sys
import os
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..', '..', '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Import from data_grid for column definitions and data types
try:
    from winformpy.ui_elements.data_grid.data_grid_backend import (
        ColumnDefinition, DataType, DataRequest, DataResponse, PageInfo
    )
except ImportError:
    from ..data_grid.data_grid_backend import (
        ColumnDefinition, DataType, DataRequest, DataResponse, PageInfo
    )


class MasterType(Enum):
    """Type of control to use for the master view."""
    DATA_GRID = "data_grid"
    LIST_VIEW = "list_view"


@dataclass
class MasterItem:
    """
    Represents a single item in the master list.
    
    Used when MasterType is LIST_VIEW.
    
    Attributes:
        id: Unique identifier for the item
        text: Display text for the item
        icon: Optional icon identifier
        data: Optional additional data dictionary
    """
    id: Any
    text: str
    icon: str = None
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MasterListResponse:
    """
    Response containing master list items.
    
    Used when MasterType is LIST_VIEW.
    """
    items: List[MasterItem]
    total_count: int = 0
    
    def __post_init__(self):
        if self.total_count == 0:
            self.total_count = len(self.items)


class MasterDetailBackend(ABC):
    """
    Abstract base class for Master-Detail data backends.
    
    Implement this class to connect the Master-Detail panel to your data source.
    The backend must provide both master and detail data.
    
    Example:
        class CustomerOrdersBackend(MasterDetailBackend):
            def get_master_type(self):
                return MasterType.DATA_GRID
            
            def get_master_columns(self):
                return [
                    ColumnDefinition('id', 'ID', DataType.INTEGER, width=60),
                    ColumnDefinition('name', 'Customer Name', DataType.STRING, width=200),
                ]
            
            def fetch_master_data(self, request):
                # Fetch customers from database
                ...
            
            def get_detail_columns(self):
                return [
                    ColumnDefinition('order_id', 'Order #', DataType.INTEGER, width=80),
                    ColumnDefinition('date', 'Date', DataType.DATE, width=100),
                    ColumnDefinition('total', 'Total', DataType.CURRENCY, width=100),
                ]
            
            def fetch_detail_data(self, master_id, request):
                # Fetch orders for the selected customer
                ...
    """
    
    # =========================================================================
    # Master Configuration
    # =========================================================================
    
    @abstractmethod
    def get_master_type(self) -> MasterType:
        """
        Return the type of control to use for the master view.
        
        Returns:
            MasterType.DATA_GRID or MasterType.LIST_VIEW
        """
        pass
    
    def get_master_columns(self) -> List[ColumnDefinition]:
        """
        Return column definitions for the master grid.
        
        Only required when get_master_type() returns MasterType.DATA_GRID.
        
        Returns:
            List of ColumnDefinition objects
        """
        return []
    
    def fetch_master_data(self, request: DataRequest) -> DataResponse:
        """
        Fetch data for the master grid.
        
        Only required when get_master_type() returns MasterType.DATA_GRID.
        
        Args:
            request: DataRequest with pagination, sorting, filtering
            
        Returns:
            DataResponse with records and page info
        """
        return DataResponse(records=[], page_info=PageInfo())
    
    def fetch_master_list(self) -> MasterListResponse:
        """
        Fetch items for the master list view.
        
        Only required when get_master_type() returns MasterType.LIST_VIEW.
        
        Returns:
            MasterListResponse with list items
        """
        return MasterListResponse(items=[])
    
    def get_master_id_field(self) -> str:
        """
        Return the field name that contains the master record ID.
        
        Used to link master selection to detail data.
        Default is 'id'.
        
        Returns:
            Field name string
        """
        return 'id'
    
    def get_master_title(self) -> str:
        """
        Return the title for the master panel.
        
        Returns:
            Title string (default: 'Master')
        """
        return 'Master'
    
    # =========================================================================
    # Detail Configuration
    # =========================================================================
    
    @abstractmethod
    def get_detail_columns(self) -> List[ColumnDefinition]:
        """
        Return column definitions for the detail grid.
        
        Returns:
            List of ColumnDefinition objects
        """
        pass
    
    @abstractmethod
    def fetch_detail_data(self, master_id: Any, request: DataRequest) -> DataResponse:
        """
        Fetch detail data for the selected master record.
        
        Args:
            master_id: The ID of the selected master record
            request: DataRequest with pagination, sorting, filtering
            
        Returns:
            DataResponse with detail records and page info
        """
        pass
    
    def get_detail_title(self) -> str:
        """
        Return the title for the detail panel.
        
        Returns:
            Title string (default: 'Details')
        """
        return 'Details'
    
    # =========================================================================
    # Formatting
    # =========================================================================
    
    def format_master_value(self, value: Any, column: ColumnDefinition) -> str:
        """
        Format a value for display in the master grid.
        
        Override this method for custom formatting.
        
        Args:
            value: The raw value
            column: The column definition
            
        Returns:
            Formatted string
        """
        return self._default_format(value, column)
    
    def format_detail_value(self, value: Any, column: ColumnDefinition) -> str:
        """
        Format a value for display in the detail grid.
        
        Override this method for custom formatting.
        
        Args:
            value: The raw value
            column: The column definition
            
        Returns:
            Formatted string
        """
        return self._default_format(value, column)
    
    def _default_format(self, value: Any, column: ColumnDefinition) -> str:
        """Default formatting based on data type."""
        if value is None:
            return ''
        
        if column.format_string:
            try:
                return column.format_string.format(value)
            except (ValueError, KeyError):
                pass
        
        if column.data_type == DataType.CURRENCY:
            try:
                return f"${float(value):,.2f}"
            except (ValueError, TypeError):
                return str(value)
        elif column.data_type == DataType.PERCENTAGE:
            try:
                return f"{float(value):.1f}%"
            except (ValueError, TypeError):
                return str(value)
        elif column.data_type == DataType.INTEGER:
            try:
                return f"{int(value):,}"
            except (ValueError, TypeError):
                return str(value)
        elif column.data_type == DataType.FLOAT:
            try:
                return f"{float(value):,.2f}"
            except (ValueError, TypeError):
                return str(value)
        elif column.data_type == DataType.BOOLEAN:
            return 'Yes' if value else 'No'
        
        return str(value)


# =============================================================================
# Example Backend for Demo/Testing
# =============================================================================

class DemoMasterDetailBackend(MasterDetailBackend):
    """
    Demo backend with sample customer/orders data.
    
    Useful for testing and demonstration.
    """
    
    def __init__(self):
        # Sample customers
        self._customers = [
            {'id': 1, 'name': 'Acme Corporation', 'city': 'New York', 'country': 'USA'},
            {'id': 2, 'name': 'Global Industries', 'city': 'London', 'country': 'UK'},
            {'id': 3, 'name': 'Tech Solutions', 'city': 'San Francisco', 'country': 'USA'},
            {'id': 4, 'name': 'Euro Partners', 'city': 'Berlin', 'country': 'Germany'},
            {'id': 5, 'name': 'Asian Traders', 'city': 'Tokyo', 'country': 'Japan'},
        ]
        
        # Sample orders (keyed by customer_id)
        self._orders = {
            1: [
                {'order_id': 1001, 'date': '2025-01-15', 'product': 'Widget A', 'quantity': 100, 'total': 2500.00},
                {'order_id': 1002, 'date': '2025-01-18', 'product': 'Widget B', 'quantity': 50, 'total': 1750.00},
                {'order_id': 1003, 'date': '2025-01-20', 'product': 'Gadget X', 'quantity': 25, 'total': 3125.00},
            ],
            2: [
                {'order_id': 2001, 'date': '2025-01-10', 'product': 'Service Plan', 'quantity': 1, 'total': 5000.00},
                {'order_id': 2002, 'date': '2025-01-22', 'product': 'Widget A', 'quantity': 200, 'total': 4800.00},
            ],
            3: [
                {'order_id': 3001, 'date': '2025-01-05', 'product': 'Software License', 'quantity': 10, 'total': 9990.00},
            ],
            4: [
                {'order_id': 4001, 'date': '2025-01-12', 'product': 'Widget C', 'quantity': 75, 'total': 2250.00},
                {'order_id': 4002, 'date': '2025-01-14', 'product': 'Widget A', 'quantity': 30, 'total': 720.00},
                {'order_id': 4003, 'date': '2025-01-16', 'product': 'Gadget Y', 'quantity': 15, 'total': 1875.00},
                {'order_id': 4004, 'date': '2025-01-19', 'product': 'Service Plan', 'quantity': 2, 'total': 10000.00},
            ],
            5: [],  # No orders yet
        }
    
    def get_master_type(self) -> MasterType:
        return MasterType.DATA_GRID
    
    def get_master_title(self) -> str:
        return 'Customers'
    
    def get_master_columns(self) -> List[ColumnDefinition]:
        return [
            ColumnDefinition('id', 'ID', DataType.INTEGER, width=60),
            ColumnDefinition('name', 'Company Name', DataType.STRING, width=200),
            ColumnDefinition('city', 'City', DataType.STRING, width=120),
            ColumnDefinition('country', 'Country', DataType.STRING, width=100),
        ]
    
    def fetch_master_data(self, request: DataRequest) -> DataResponse:
        records = self._customers.copy()
        
        # Apply search
        if request.search_text:
            search = request.search_text.lower()
            records = [r for r in records if 
                      search in r['name'].lower() or
                      search in r['city'].lower() or
                      search in r['country'].lower()]
        
        # Apply sorting
        if request.sort_column:
            reverse = (hasattr(request.sort_order, 'value') and request.sort_order.value == 'desc') or request.sort_order == 'desc'
            records.sort(key=lambda x: x.get(request.sort_column, ''), reverse=reverse)
        
        total = len(records)
        
        # Apply pagination
        start = (request.page - 1) * request.page_size
        end = start + request.page_size
        records = records[start:end]
        
        return DataResponse(
            records=records,
            page_info=PageInfo(
                current_page=request.page,
                page_size=request.page_size,
                total_records=total,
                total_pages=(total + request.page_size - 1) // request.page_size
            )
        )
    
    def get_detail_title(self) -> str:
        return 'Orders'
    
    def get_detail_columns(self) -> List[ColumnDefinition]:
        return [
            ColumnDefinition('order_id', 'Order #', DataType.INTEGER, width=80),
            ColumnDefinition('date', 'Date', DataType.DATE, width=100),
            ColumnDefinition('product', 'Product', DataType.STRING, width=150),
            ColumnDefinition('quantity', 'Qty', DataType.INTEGER, width=60, align='right'),
            ColumnDefinition('total', 'Total', DataType.CURRENCY, width=100, align='right'),
        ]
    
    def fetch_detail_data(self, master_id: Any, request: DataRequest) -> DataResponse:
        if master_id is None:
            return DataResponse(records=[], page_info=PageInfo())
        
        records = self._orders.get(master_id, []).copy()
        
        # Apply search
        if request.search_text:
            search = request.search_text.lower()
            records = [r for r in records if 
                      search in r['product'].lower() or
                      search in str(r['order_id'])]
        
        # Apply sorting
        if request.sort_column:
            reverse = (hasattr(request.sort_order, 'value') and request.sort_order.value == 'desc') or request.sort_order == 'desc'
            records.sort(key=lambda x: x.get(request.sort_column, ''), reverse=reverse)
        
        total = len(records)
        
        # Apply pagination
        start = (request.page - 1) * request.page_size
        end = start + request.page_size
        records = records[start:end]
        
        return DataResponse(
            records=records,
            page_info=PageInfo(
                current_page=request.page,
                page_size=request.page_size,
                total_records=total,
                total_pages=max(1, (total + request.page_size - 1) // request.page_size)
            )
        )


class DemoListViewBackend(MasterDetailBackend):
    """
    Demo backend using ListView for master.
    
    Shows categories with products as details.
    """
    
    def __init__(self):
        self._categories = [
            MasterItem(id=1, text='Electronics', icon='📱'),
            MasterItem(id=2, text='Clothing', icon='👕'),
            MasterItem(id=3, text='Books', icon='📚'),
            MasterItem(id=4, text='Home & Garden', icon='🏠'),
            MasterItem(id=5, text='Sports', icon='⚽'),
        ]
        
        self._products = {
            1: [
                {'id': 101, 'name': 'Smartphone', 'price': 699.99, 'stock': 50},
                {'id': 102, 'name': 'Laptop', 'price': 1299.99, 'stock': 25},
                {'id': 103, 'name': 'Tablet', 'price': 449.99, 'stock': 40},
                {'id': 104, 'name': 'Headphones', 'price': 199.99, 'stock': 100},
            ],
            2: [
                {'id': 201, 'name': 'T-Shirt', 'price': 29.99, 'stock': 200},
                {'id': 202, 'name': 'Jeans', 'price': 59.99, 'stock': 150},
                {'id': 203, 'name': 'Jacket', 'price': 149.99, 'stock': 75},
            ],
            3: [
                {'id': 301, 'name': 'Python Programming', 'price': 49.99, 'stock': 30},
                {'id': 302, 'name': 'Data Science Handbook', 'price': 39.99, 'stock': 45},
            ],
            4: [
                {'id': 401, 'name': 'Garden Tools Set', 'price': 79.99, 'stock': 60},
                {'id': 402, 'name': 'Indoor Plant', 'price': 24.99, 'stock': 80},
                {'id': 403, 'name': 'Outdoor Furniture', 'price': 299.99, 'stock': 20},
            ],
            5: [
                {'id': 501, 'name': 'Soccer Ball', 'price': 29.99, 'stock': 100},
                {'id': 502, 'name': 'Tennis Racket', 'price': 89.99, 'stock': 35},
                {'id': 503, 'name': 'Running Shoes', 'price': 119.99, 'stock': 50},
                {'id': 504, 'name': 'Yoga Mat', 'price': 34.99, 'stock': 75},
            ],
        }
    
    def get_master_type(self) -> MasterType:
        return MasterType.LIST_VIEW
    
    def get_master_title(self) -> str:
        return 'Categories'
    
    def fetch_master_list(self) -> MasterListResponse:
        return MasterListResponse(items=self._categories)
    
    def get_detail_title(self) -> str:
        return 'Products'
    
    def get_detail_columns(self) -> List[ColumnDefinition]:
        return [
            ColumnDefinition('id', 'ID', DataType.INTEGER, width=60),
            ColumnDefinition('name', 'Product Name', DataType.STRING, width=200),
            ColumnDefinition('price', 'Price', DataType.CURRENCY, width=100, align='right'),
            ColumnDefinition('stock', 'In Stock', DataType.INTEGER, width=80, align='right'),
        ]
    
    def fetch_detail_data(self, master_id: Any, request: DataRequest) -> DataResponse:
        if master_id is None:
            return DataResponse(records=[], page_info=PageInfo())
        
        records = self._products.get(master_id, []).copy()
        
        # Apply search
        if request.search_text:
            search = request.search_text.lower()
            records = [r for r in records if search in r['name'].lower()]
        
        total = len(records)
        
        return DataResponse(
            records=records,
            page_info=PageInfo(
                current_page=1,
                page_size=total or 1,
                total_records=total,
                total_pages=1
            )
        )
