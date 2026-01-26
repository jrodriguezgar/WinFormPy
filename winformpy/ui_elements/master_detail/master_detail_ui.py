"""
Master-Detail UI - Standalone forms for Master-Detail display.

This module provides:
1. MasterDetailForm - A ready-to-use form with MasterDetailPanel + status bar
2. Demo functions replicating master_detail_panel examples

Example usage:
    from master_detail_ui import MasterDetailForm
    
    backend = MyBackend()
    form = MasterDetailForm(backend, title="My Data")
    form.refresh()
    Application.Run(form)
"""

import sys
import os
import random
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from winformpy.winformpy import (
    Form, Panel, Label, Button, Application,
    DockStyle, AnchorStyles, Font, FontStyle, DialogResult
)
from typing import Any, List, Dict, Optional, Callable

# Handle imports for both module and direct execution
try:
    from ..data_grid.data_grid_backend import (
        DataRequest, DataResponse, ColumnDefinition, DataType, PageInfo
    )
    from .master_detail_backend import (
        MasterDetailBackend, MasterType, MasterItem, MasterListResponse
    )
    from .master_detail_manager import MasterDetailManager
    from .master_detail_panel import MasterDetailPanel
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data_grid'))
    from data_grid_backend import (
        DataRequest, DataResponse, ColumnDefinition, DataType, PageInfo
    )
    from master_detail_backend import (
        MasterDetailBackend, MasterType, MasterItem, MasterListResponse
    )
    from master_detail_manager import MasterDetailManager
    from master_detail_panel import MasterDetailPanel


# =============================================================================
# MasterDetailForm - Standalone Form with Status Bar
# =============================================================================

class MasterDetailForm(Form):
    """
    Standalone form containing a MasterDetailPanel with status bar.
    
    Use this when you need a complete master-detail window with
    title bar and status bar showing selection info.
    
    Example:
        backend = CustomerOrdersBackend()
        form = MasterDetailForm(backend, title="Customer Orders")
        form.DetailRowDoubleClick = lambda s, e: edit_order(e['record'])
        form.refresh()
        Application.Run(form)
    """
    
    def __init__(self, backend: MasterDetailBackend = None,
                 manager: MasterDetailManager = None,
                 title: str = "Master-Detail View",
                 width: int = 1200,
                 height: int = 700,
                 orientation: str = 'horizontal',
                 master_size: int = None):
        """
        Initialize the MasterDetailForm.
        
        Args:
            backend: Optional MasterDetailBackend for data source.
            manager: Optional pre-configured MasterDetailManager.
            title: Window title.
            width: Form width in pixels.
            height: Form height in pixels.
            orientation: 'horizontal' (side-by-side) or 'vertical' (top-bottom)
            master_size: Width (horizontal) or height (vertical) of master panel.
        """
        super().__init__({
            'Text': title,
            'Width': width,
            'Height': height,
            'StartPosition': 'CenterScreen'
        })
        self.ApplyLayout()
        
        # Setup manager
        if manager:
            self._manager = manager
        elif backend:
            self._manager = MasterDetailManager(backend)
        else:
            raise ValueError("Either 'backend' or 'manager' must be provided")
        
        self._orientation = orientation
        self._master_size = master_size
        
        # External events (forwarded from panel)
        self.MasterSelectionChanged: Callable[[object, Dict], None] = lambda s, e: None
        self.MasterRowClick: Callable[[object, Dict], None] = lambda s, e: None
        self.MasterRowDoubleClick: Callable[[object, Dict], None] = lambda s, e: None
        self.DetailRowClick: Callable[[object, Dict], None] = lambda s, e: None
        self.DetailRowDoubleClick: Callable[[object, Dict], None] = lambda s, e: None
        self.DetailSelectionChanged: Callable[[object, Dict], None] = lambda s, e: None
        
        # Build UI
        self._build_ui()
    
    def _build_ui(self):
        """Build the form UI."""
        # Status bar at bottom
        self._status_bar = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': 40,
            'BackColor': '#F0F0F0',
        })
        
        self._status_label = Label(self._status_bar, {
            'Dock': DockStyle.Left,
            'Width': 400,
            'Text': 'Ready',
            'Font': Font('Segoe UI', 9),
            'Padding': (10, 10, 10, 10),
        })
        
        self._close_btn = Button(self._status_bar, {
            'Text': 'Close',
            'Width': 80,
            'Height': 28,
            'Anchor': AnchorStyles.Top | AnchorStyles.Right,
        })
        self._close_btn.Left = self._status_bar.Width - 90
        self._close_btn.Top = 6
        self._close_btn.Click = lambda s, e: self.Close()
        
        # Build panel props
        panel_props = {
            'Dock': DockStyle.Fill,
            'Orientation': self._orientation,
        }
        
        if self._master_size:
            if self._orientation == 'horizontal':
                panel_props['MasterWidth'] = self._master_size
            else:
                panel_props['MasterHeight'] = self._master_size
        
        # Main panel
        self._panel = MasterDetailPanel(self, props=panel_props, manager=self._manager)
        
        # Forward events
        self._panel.MasterSelectionChanged = self._on_master_selection_changed
        self._panel.MasterRowClick = lambda s, e: self.MasterRowClick(s, e)
        self._panel.MasterRowDoubleClick = lambda s, e: self.MasterRowDoubleClick(s, e)
        self._panel.DetailRowClick = lambda s, e: self.DetailRowClick(s, e)
        self._panel.DetailRowDoubleClick = lambda s, e: self.DetailRowDoubleClick(s, e)
        self._panel.DetailSelectionChanged = lambda s, e: self.DetailSelectionChanged(s, e)
    
    def _on_master_selection_changed(self, sender, event_args):
        """Handle master selection change."""
        master_id = event_args.get('master_id')
        record = event_args.get('master_record')
        
        if master_id is not None:
            if record:
                # Try to get a display name from record
                if isinstance(record, MasterItem):
                    name = record.text
                elif isinstance(record, dict):
                    name = (record.get('name') or record.get('Name') or
                            record.get('title') or record.get('Title') or
                            record.get('text') or str(master_id))
                else:
                    name = str(master_id)
                self._status_label.Text = f"Selected: {name}"
            else:
                self._status_label.Text = f"Selected ID: {master_id}"
        else:
            self._status_label.Text = "Ready"
        
        # Forward event
        self.MasterSelectionChanged(sender, event_args)
    
    @property
    def manager(self) -> MasterDetailManager:
        """Get the MasterDetailManager instance."""
        return self._manager
    
    @property
    def panel(self) -> MasterDetailPanel:
        """Get the MasterDetailPanel."""
        return self._panel
    
    @property
    def master_grid(self):
        """Get the master DataGridPanel (if using grid mode)."""
        return self._panel.master_grid
    
    @property
    def detail_grid(self):
        """Get the detail DataGridPanel."""
        return self._panel.detail_grid
    
    def refresh(self):
        """Refresh all data."""
        self._manager.refresh_master()


# =============================================================================
# Demo Backends (same as master_detail_panel.py)
# =============================================================================

class CustomerOrdersBackend(MasterDetailBackend):
    """Demo backend showing customers (master) and their orders (detail)."""
    
    def __init__(self):
        """Generate sample customer and order data."""
        self._customers = self._generate_customers(15)
        self._orders = self._generate_orders()
    
    def _generate_customers(self, count: int) -> list:
        """Generate sample customer data."""
        first_names = ["John", "Jane", "Robert", "Emily", "Michael", "Sarah", 
                      "David", "Lisa", "James", "Maria", "William", "Anna",
                      "Richard", "Jennifer", "Thomas"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
                     "Miller", "Davis", "Rodriguez", "Martinez", "Anderson", "Taylor"]
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
                 "Philadelphia", "San Antonio", "San Diego", "Dallas", "Austin"]
        
        customers = []
        for i in range(1, count + 1):
            first = random.choice(first_names)
            last = random.choice(last_names)
            customers.append({
                'id': i,
                'name': f"{first} {last}",
                'email': f"{first.lower()}.{last.lower()}@email.com",
                'city': random.choice(cities),
                'total_orders': 0,
                'total_spent': 0.0,
            })
        return customers
    
    def _generate_orders(self) -> list:
        """Generate sample orders for each customer."""
        products = ["Widget Pro", "Gadget X", "Tool Kit", "Component A", 
                   "Module B", "System C", "Device D", "Unit E"]
        statuses = ["Completed", "Processing", "Shipped", "Pending", "Delivered"]
        
        orders = []
        order_id = 1000
        
        for customer in self._customers:
            num_orders = random.randint(2, 8)
            customer_total = 0.0
            
            for _ in range(num_orders):
                amount = round(random.uniform(25.0, 500.0), 2)
                customer_total += amount
                
                orders.append({
                    'order_id': order_id,
                    'customer_id': customer['id'],
                    'product': random.choice(products),
                    'amount': amount,
                    'quantity': random.randint(1, 10),
                    'date': datetime.now() - timedelta(days=random.randint(1, 365)),
                    'status': random.choice(statuses),
                })
                order_id += 1
            
            customer['total_orders'] = num_orders
            customer['total_spent'] = round(customer_total, 2)
        
        return orders
    
    def get_master_type(self) -> MasterType:
        return MasterType.DATA_GRID
    
    def get_master_title(self) -> str:
        return "Customers"
    
    def get_master_id_field(self) -> str:
        return 'id'
    
    def get_master_columns(self) -> list:
        return [
            ColumnDefinition('id', 'ID', DataType.INTEGER, width=50, align='right'),
            ColumnDefinition('name', 'Customer Name', DataType.STRING, width=180),
            ColumnDefinition('city', 'City', DataType.STRING, width=120),
            ColumnDefinition('total_orders', 'Orders', DataType.INTEGER, width=70, align='right'),
            ColumnDefinition('total_spent', 'Total Spent', DataType.CURRENCY, width=100, align='right'),
        ]
    
    def fetch_master_data(self, request: DataRequest) -> DataResponse:
        filtered = self._customers.copy()
        
        if request.search_text:
            search = request.search_text.lower()
            filtered = [c for c in filtered if 
                       search in c['name'].lower() or 
                       search in c['city'].lower() or
                       search in c['email'].lower()]
        
        if request.sort_column:
            reverse = request.sort_order.value == 'desc'
            filtered.sort(
                key=lambda x: (x.get(request.sort_column) is None, x.get(request.sort_column)),
                reverse=reverse
            )
        
        total = len(filtered)
        total_pages = max(1, (total + request.page_size - 1) // request.page_size)
        current_page = min(request.page, total_pages)
        
        start = (current_page - 1) * request.page_size
        end = start + request.page_size
        
        return DataResponse(
            records=filtered[start:end],
            page_info=PageInfo(
                current_page=current_page,
                page_size=request.page_size,
                total_records=total,
                total_pages=total_pages
            ),
            columns=self.get_master_columns()
        )
    
    def get_detail_title(self) -> str:
        return "Orders"
    
    def get_detail_columns(self) -> list:
        return [
            ColumnDefinition('order_id', 'Order #', DataType.INTEGER, width=80, align='right'),
            ColumnDefinition('product', 'Product', DataType.STRING, width=150),
            ColumnDefinition('quantity', 'Qty', DataType.INTEGER, width=50, align='right'),
            ColumnDefinition('amount', 'Amount', DataType.CURRENCY, width=100, align='right'),
            ColumnDefinition('date', 'Date', DataType.DATE, width=100, align='center'),
            ColumnDefinition('status', 'Status', DataType.STRING, width=100),
        ]
    
    def fetch_detail_data(self, master_id, request: DataRequest) -> DataResponse:
        filtered = [o for o in self._orders if o['customer_id'] == master_id]
        
        if request.search_text:
            search = request.search_text.lower()
            filtered = [o for o in filtered if 
                       search in o['product'].lower() or
                       search in o['status'].lower()]
        
        if request.sort_column:
            reverse = request.sort_order.value == 'desc'
            filtered.sort(
                key=lambda x: (x.get(request.sort_column) is None, x.get(request.sort_column)),
                reverse=reverse
            )
        
        total = len(filtered)
        total_pages = max(1, (total + request.page_size - 1) // request.page_size)
        current_page = min(request.page, total_pages)
        
        start = (current_page - 1) * request.page_size
        end = start + request.page_size
        
        return DataResponse(
            records=filtered[start:end],
            page_info=PageInfo(
                current_page=current_page,
                page_size=request.page_size,
                total_records=total,
                total_pages=total_pages
            ),
            columns=self.get_detail_columns()
        )


class CategoryProductsBackend(MasterDetailBackend):
    """Demo backend using ListView for master (categories) and Grid for detail (products)."""
    
    def __init__(self):
        self._categories = [
            {'id': 1, 'name': 'Electronics', 'icon': '💻'},
            {'id': 2, 'name': 'Clothing', 'icon': '👕'},
            {'id': 3, 'name': 'Books', 'icon': '📚'},
            {'id': 4, 'name': 'Home & Garden', 'icon': '🏠'},
            {'id': 5, 'name': 'Sports', 'icon': '⚽'},
        ]
        self._products = self._generate_products()
    
    def _generate_products(self) -> list:
        products_by_category = {
            1: [("Laptop Pro", 1299.99), ("Smartphone X", 899.99), ("Tablet Air", 649.99),
                ("Wireless Earbuds", 199.99), ("Smart Watch", 349.99)],
            2: [("T-Shirt Basic", 19.99), ("Jeans Classic", 59.99), ("Jacket Winter", 129.99),
                ("Sneakers Sport", 89.99), ("Hat Summer", 24.99)],
            3: [("Python Guide", 49.99), ("Data Science", 59.99), ("Web Development", 44.99),
                ("Machine Learning", 69.99), ("Clean Code", 39.99)],
            4: [("Garden Tools Set", 79.99), ("Plant Pot Large", 29.99), ("LED Lights", 49.99),
                ("Furniture Polish", 12.99), ("Outdoor Chair", 149.99)],
            5: [("Football Pro", 39.99), ("Tennis Racket", 89.99), ("Yoga Mat", 29.99),
                ("Running Shoes", 119.99), ("Weights Set", 199.99)],
        }
        
        products = []
        prod_id = 1
        for cat_id, items in products_by_category.items():
            for name, price in items:
                products.append({
                    'id': prod_id,
                    'category_id': cat_id,
                    'name': name,
                    'price': price,
                    'stock': random.randint(0, 100),
                    'rating': round(random.uniform(3.5, 5.0), 1),
                })
                prod_id += 1
        return products
    
    def get_master_type(self) -> MasterType:
        return MasterType.LIST_VIEW
    
    def get_master_title(self) -> str:
        return "Categories"
    
    def fetch_master_list(self) -> MasterListResponse:
        items = [
            MasterItem(
                id=cat['id'],
                text=f"{cat['icon']} {cat['name']}",
                data=cat
            )
            for cat in self._categories
        ]
        return MasterListResponse(items=items)
    
    def get_detail_title(self) -> str:
        return "Products"
    
    def get_detail_columns(self) -> list:
        return [
            ColumnDefinition('id', 'ID', DataType.INTEGER, width=50, align='right'),
            ColumnDefinition('name', 'Product Name', DataType.STRING, width=180),
            ColumnDefinition('price', 'Price', DataType.CURRENCY, width=100, align='right'),
            ColumnDefinition('stock', 'In Stock', DataType.INTEGER, width=80, align='right'),
            ColumnDefinition('rating', 'Rating', DataType.FLOAT, width=70, align='center'),
        ]
    
    def fetch_detail_data(self, master_id, request: DataRequest) -> DataResponse:
        filtered = [p for p in self._products if p['category_id'] == master_id]
        
        if request.search_text:
            search = request.search_text.lower()
            filtered = [p for p in filtered if search in p['name'].lower()]
        
        if request.sort_column:
            reverse = request.sort_order.value == 'desc'
            filtered.sort(
                key=lambda x: (x.get(request.sort_column) is None, x.get(request.sort_column)),
                reverse=reverse
            )
        
        return DataResponse(
            records=filtered,
            page_info=PageInfo(
                current_page=1,
                page_size=len(filtered) or 1,
                total_records=len(filtered),
                total_pages=1
            ),
            columns=self.get_detail_columns()
        )


# =============================================================================
# Demo Functions
# =============================================================================

def run_demo():
    """Run the Master-Detail UI demo."""
    print("=" * 60)
    print("Master-Detail UI Demo")
def run_demo():
    """Run simple demo."""
    backend = CustomerOrdersBackend()
    form = MasterDetailForm(backend=backend)
    form.Show()
    Application.Run(form)


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    run_demo()
