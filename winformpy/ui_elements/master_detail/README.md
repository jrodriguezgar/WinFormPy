# Master-Detail UI Element

A flexible master-detail component where selecting a master record displays related detail records.

## 📦 Component Structure

| Component | Type | Description |
|-----------|------|-------------|
| `MasterDetailPanel` | Embeddable Panel | Two containers: Master (DataGrid/ListView) + Detail (DataGrid) |
| `MasterDetailForm` | Standalone Form | Ready-to-use window |

## Features

- **Two Container Layout**: Master container + Detail container
- **Configurable Master View**: DataGrid or ListView (via `MasterType` property)
- **DataGrid Detail View**: Full DataGridPanel with search, sort, pagination
- **Automatic Refresh**: Detail updates when master selection changes
- **Flexible Layout**: Horizontal (side-by-side) or vertical (top-bottom)
- **Sub-Properties**: Fine-grained styling for all internal elements
- **Event Forwarding**: All grid events accessible from parent

## Quick Start

### Using MasterDetailForm (Standalone)

```python
from winformpy.ui_elements.master_detail import MasterDetailForm, MasterDetailBackend

# Create your backend
backend = CustomerOrdersBackend()

# Create and show form
form = MasterDetailForm(
    backend,
    title="Customer Orders",
    orientation='horizontal',
    master_size=350
)
form.DetailRowDoubleClick = lambda s, e: edit_order(e['record'])
form.Show()
```

### Using MasterDetailPanel (Embeddable)

```python
from winformpy.winformpy import Form, DockStyle
from winformpy.ui_elements.master_detail import MasterDetailPanel, MasterDetailManager

backend = CustomerOrdersBackend()
manager = MasterDetailManager(backend)

form = Form({'Text': 'My App', 'Width': 1200, 'Height': 700})
form.ApplyLayout()

panel = MasterDetailPanel(form, props={
    'Dock': DockStyle.Fill,
    'Orientation': 'horizontal',     # 'horizontal' or 'vertical'
    'MasterType': MasterType.DATA_GRID,  # or MasterType.LIST_VIEW
    'MasterWidth': 400,
}, manager=manager)

panel.MasterSelectionChanged = lambda s, e: print(f"Selected: {e['master_id']}")
panel.DetailRowDoubleClick = lambda s, e: edit_record(e['record'])

form.Show()
```

## Quick Demo

Run built-in demos from the command line:

```bash
# DataGrid as master (Customer → Orders)
python -m winformpy.ui_elements.master_detail.master_detail_ui --demo grid

# ListView as master (Category → Products)  
python -m winformpy.ui_elements.master_detail.master_detail_ui --demo list

# Vertical layout
python -m winformpy.ui_elements.master_detail.master_detail_ui --demo vertical
```

## Architecture

```
MasterDetailBackend (ABC)     # Your data source contract
        ↓ implements
YourCustomBackend             # Your implementation
        ↓ used by
MasterDetailManager           # State & data flow management
        ↓ used by
MasterDetailPanel             # UI component (master + detail grids)
        ↓ optional wrapper
MasterDetailForm              # Standalone window
```

## Implementing a Backend

```python
from winformpy.ui_elements.master_detail import (
    MasterDetailBackend, MasterType
)
from winformpy.ui_elements.data_grid import (
    ColumnDefinition, DataType, DataRequest, DataResponse, PageInfo
)

class CustomerOrdersBackend(MasterDetailBackend):
    """Example: Customers as master, Orders as detail."""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    # === Master Configuration ===
    
    def get_master_type(self) -> MasterType:
        return MasterType.DATA_GRID  # or MasterType.LIST_VIEW
    
    def get_master_title(self) -> str:
        return 'Customers'
    
    def get_master_columns(self) -> list:
        return [
            ColumnDefinition('id', 'ID', DataType.INTEGER, width=60),
            ColumnDefinition('name', 'Customer', DataType.STRING, width=200),
            ColumnDefinition('city', 'City', DataType.STRING, width=120),
        ]
    
    def fetch_master_data(self, request: DataRequest) -> DataResponse:
        # Query customers with pagination, search, sort
        query = "SELECT * FROM customers"
        
        if request.search_text:
            query += f" WHERE name LIKE '%{request.search_text}%'"
        
        if request.sort_column:
            query += f" ORDER BY {request.sort_column} {request.sort_order}"
        
        # Add pagination
        offset = (request.page - 1) * request.page_size
        query += f" LIMIT {request.page_size} OFFSET {offset}"
        
        records = self.db.execute(query)
        total = self.db.execute("SELECT COUNT(*) FROM customers")[0][0]
        
        return DataResponse(
            records=records,
            page_info=PageInfo(
                current_page=request.page,
                page_size=request.page_size,
                total_records=total
            )
        )
    
    def get_master_id_field(self) -> str:
        return 'id'  # Field used to identify master records
    
    # === Detail Configuration ===
    
    def get_detail_title(self) -> str:
        return 'Orders'
    
    def get_detail_columns(self) -> list:
        return [
            ColumnDefinition('order_id', 'Order #', DataType.INTEGER, width=80),
            ColumnDefinition('date', 'Date', DataType.DATE, width=100),
            ColumnDefinition('product', 'Product', DataType.STRING, width=150),
            ColumnDefinition('total', 'Total', DataType.CURRENCY, width=100),
        ]
    
    def fetch_detail_data(self, master_id, request: DataRequest) -> DataResponse:
        # Query orders for the selected customer
        query = f"SELECT * FROM orders WHERE customer_id = {master_id}"
        
        if request.search_text:
            query += f" AND product LIKE '%{request.search_text}%'"
        
        records = self.db.execute(query)
        
        return DataResponse(
            records=records,
            page_info=PageInfo(
                current_page=1,
                total_records=len(records)
            )
        )
```

## ListView Master Backend

For a simpler list-based master:

```python
from winformpy.ui_elements.master_detail import (
    MasterDetailBackend, MasterType, MasterItem, MasterListResponse
)

class CategoryProductsBackend(MasterDetailBackend):
    """Categories as ListView, Products as DataGrid."""
    
    def get_master_type(self) -> MasterType:
        return MasterType.LIST_VIEW
    
    def get_master_title(self) -> str:
        return 'Categories'
    
    def fetch_master_list(self) -> MasterListResponse:
        items = [
            MasterItem(id=1, text='Electronics', icon='📱'),
            MasterItem(id=2, text='Clothing', icon='👕'),
            MasterItem(id=3, text='Books', icon='📚'),
        ]
        return MasterListResponse(items=items)
    
    # Detail methods same as above...
```

## Sub-Properties

Customize internal elements with sub-properties:

```python
panel = MasterDetailPanel(form, props={
    'Dock': DockStyle.Fill,
    'Orientation': 'horizontal',
    'MasterWidth': 350,
    
    # Master panel container
    'MasterPanel': {
        'BackColor': '#F5F5F5',
    },
    
    # Master DataGrid (when using MasterType.DATA_GRID)
    'MasterGrid': {
        'Header': {'BackColor': '#E0E0E0', 'Height': 45},
        'Rows': {'Height': 38},
        'Pagination': {'Height': 40},
    },
    
    # Master ListView (when using MasterType.LIST_VIEW)
    'MasterList': {
        'BackColor': '#FFFFFF',
    },
    
    # Detail panel container
    'DetailPanel': {
        'BackColor': '#FFFFFF',
    },
    
    # Detail DataGrid
    'DetailGrid': {
        'Toolbar': {'Height': 50},
        'Header': {'Height': 42, 'BackColor': '#333', 'ForeColor': '#FFF'},
        'Rows': {'Height': 40, 'AlternateBackColor': '#FAFAFA'},
        'SearchBox': {'Width': 280},
    },
}, manager=manager)
```

## Events

### Master Events

| Event | Args | Description |
|-------|------|-------------|
| `MasterSelectionChanged` | `{'master_id': Any, 'master_record': dict}` | Selection changed |
| `MasterRowClick` | Standard grid args | Row clicked (grid mode) |
| `MasterRowDoubleClick` | Standard grid args | Row double-clicked (grid mode) |

### Detail Events

| Event | Args | Description |
|-------|------|-------------|
| `DetailRowClick` | Standard grid args | Row clicked |
| `DetailRowDoubleClick` | Standard grid args | Row double-clicked |
| `DetailSelectionChanged` | Standard grid args | Selection changed |

## Methods

| Method | Description |
|--------|-------------|
| `refresh_master()` | Refresh master view data |
| `refresh_detail()` | Refresh detail grid data |
| `refresh()` | Refresh both master and detail |
| `select_master_by_id(id)` | Programmatically select a master record |
| `clear_selection()` | Clear all selections |

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `manager` | MasterDetailManager | The manager instance |
| `master_grid` | DataGridPanel | Master grid (if MasterType.DATA_GRID) |
| `master_listbox` | ListBox | Master listbox (if MasterType.LIST_VIEW) |
| `detail_grid` | DataGridPanel | Detail grid (always present) |
| `master_type` | MasterType | Current master view type |
| `selected_master_id` | Any | Currently selected master ID |
| `selected_master_record` | dict | Currently selected master record |
| `orientation` | str | Layout orientation ('horizontal' or 'vertical') |

## Layout Options

### Orientation

| Value | Description | Size Property |
|-------|-------------|---------------|
| `horizontal` | Side-by-side (master left, detail right) | `MasterWidth` |
| `vertical` | Top-bottom (master top, detail bottom) | `MasterHeight` |

### MasterType

| Value | Description | Props Key |
|-------|-------------|-------|
| `MasterType.DATA_GRID` | DataGrid with columns | `MasterGrid` |
| `MasterType.LIST_VIEW` | Simple list with items | `MasterList` |

## Demo Backends

The module includes demo backends for testing:

```python
from winformpy.ui_elements.master_detail import (
    DemoMasterDetailBackend,  # Customer → Orders (grid)
    DemoListViewBackend,       # Category → Products (list)
)

# Use directly
form = MasterDetailForm(DemoMasterDetailBackend())
form.Show()
```

## Files

| File | Description |
|------|-------------|
| `master_detail_backend.py` | Backend contracts and demo implementations |
| `master_detail_manager.py` | State and data flow management |
| `master_detail_panel.py` | Main embeddable UI component |
| `master_detail_ui.py` | Standalone forms and demos |
| `__init__.py` | Public exports |
