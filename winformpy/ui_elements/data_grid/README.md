# DataGrid UI Element

A data grid component for displaying tabular data with pagination, sorting, search, and selection capabilities. Follows the architecture-agnostic backend pattern.

> **📦 Component Structure**: This module provides:
> - `DataGridPanel` - Embeddable panel for any Form/Panel
> - `DataGridForm` - Standalone form that **uses DataGridPanel internally** (access via `.grid` property)

## Quick Demo

Run the built-in demos to see the component in action:

```bash
# Embeddable panel demo (200 employee records)
python winformpy/ui_elements/data_grid/data_grid_panel.py

# Standalone form demo with multiple dialogs
python winformpy/ui_elements/data_grid/data_grid_ui.py
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    DataGridPanel                         │
│                  (Visual Component)                      │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Toolbar: Search | Page Size                     │    │
│  ├─────────────────────────────────────────────────┤    │
│  │  Headers: ID ▲ | Name | Email | Dept | Salary   │    │
│  ├─────────────────────────────────────────────────┤    │
│  │  Row 1: 1 | John Smith | john@... | Eng | $85K  │    │
│  │  Row 2: 2 | Jane Doe   | jane@... | HR  | $72K  │    │
│  │  ...                                             │    │
│  ├─────────────────────────────────────────────────┤    │
│  │  Pagination: Showing 1-20 of 200 | ◀ Page 1 ▶   │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   DataGridManager                        │
│                   (Service Layer)                        │
│  - Manages state (page, sort, search, selection)        │
│  - Coordinates UI and Backend                            │
│  - Fires events (DataLoaded, SelectionChanged, etc.)    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                 DataGridBackend (ABC)                    │
│              (Your Implementation)                       │
│  - get_columns() → List[ColumnDefinition]               │
│  - fetch_data(request) → DataResponse                    │
│  - format_value(value, column) → str                     │
└─────────────────────────────────────────────────────────┘
                          │
         ┌────────────────┴────────────────┐
         ▼                                  ▼
┌─────────────────┐               ┌─────────────────┐
│  SQLiteBackend  │               │   APIBackend    │
│  PostgresBackend│               │   CSVBackend    │
│  MySQLBackend   │               │   ExcelBackend  │
└─────────────────┘               └─────────────────┘
```

## Features

- **Sortable Columns**: Click headers to sort ascending/descending
- **Search**: Filter records by text across searchable columns
- **Pagination**: Navigate pages with configurable page size (10/20/50/100)
- **Row Selection**: Single and multi-select (Ctrl+Click)
- **Data Formatting**: Automatic formatting for different data types
- **External Backend**: Connect to any data source

## Data Types

| DataType | Description | Default Format |
|----------|-------------|----------------|
| `STRING` | Text values | As-is |
| `INTEGER` | Whole numbers | `1,234` |
| `FLOAT` | Decimal numbers | `1,234.56` |
| `CURRENCY` | Money values | `$1,234.56` |
| `DATE` | Date only | `2024-01-15` |
| `DATETIME` | Date and time | `2024-01-15 14:30` |
| `BOOLEAN` | True/False | `Yes` / `No` |
| `PERCENTAGE` | Percentages | `85.5%` |

## Basic Usage

```python
from winformpy.winformpy import Form, DockStyle
from winformpy.ui_elements.data_grid import (
    DataGridPanel, DataGridManager, DataGridBackend,
    ColumnDefinition, DataRequest, DataResponse, PageInfo, DataType
)

# 1. Implement your backend
class MyDatabaseBackend(DataGridBackend):
    def __init__(self, connection):
        self.conn = connection
    
    def get_columns(self):
        return [
            ColumnDefinition("id", "ID", DataType.INTEGER, width=60),
            ColumnDefinition("name", "Name", DataType.STRING, width=200),
            ColumnDefinition("price", "Price", DataType.CURRENCY, width=100),
        ]
    
    def fetch_data(self, request):
        # Build SQL query with pagination, sorting, filtering
        # Execute query and return DataResponse
        ...

# 2. Create manager with backend
backend = MyDatabaseBackend(db_connection)
manager = DataGridManager(backend)

# 3. Create panel
form = Form()
form.ApplyLayout()

grid = DataGridPanel(form, props={'Dock': DockStyle.Fill}, manager=manager)

# 4. Handle events
grid.RowDoubleClick = lambda s, e: edit_record(e['record'])

# 5. Load data
manager.refresh()

form.ShowDialog()
```

## Customizing with Sub-Properties

DataGridPanel supports sub-properties for configuring internal elements:

```python
from winformpy import Form, DockStyle, Font, FontStyle
from winformpy.ui_elements.data_grid import DataGridPanel, DataGridManager

form = Form({'Text': 'Custom Grid', 'Width': 1000, 'Height': 700})
form.ApplyLayout()

# Configure internal elements with sub-properties
grid = DataGridPanel(form, props={
    'Dock': DockStyle.Fill,
    
    # Configure toolbar at the top
    'Toolbar': {
        'Height': 50,
        'BackColor': '#E0E0E0'
    },
    
    # Configure column headers
    'Header': {
        'Height': 40,
        'BackColor': '#0078D4',
        'ForeColor': '#FFFFFF'
    },
    
    # Configure data rows
    'Rows': {
        'Height': 35,
        'BackColor': '#FFFFFF',
        'AlternateBackColor': '#F9F9F9',
        'ForeColor': '#000000',
        'HoverColor': '#E3F2FD',
        'SelectedColor': '#BBDEFB'
    },
    
    # Configure pagination bar
    'Pagination': {
        'Height': 40,
        'BackColor': '#F5F5F5'
    },
    
    # Configure search input
    'SearchBox': {
        'Width': 250,
        'PlaceholderText': 'Type to search...'
    }
}, manager=my_manager)
```

### Available Sub-Properties

| Sub-Property | Keys | Description |
|--------------|------|-------------|
| `Toolbar` | `Height`, `BackColor` | Top toolbar with search and page size |
| `Header` | `Height`, `BackColor`, `ForeColor` | Column header row |
| `Rows` | `Height`, `BackColor`, `AlternateBackColor`, `ForeColor`, `HoverColor`, `SelectedColor` | Data rows |
| `Pagination` | `Height`, `BackColor` | Bottom pagination bar |
| `SearchBox` | `Width`, `PlaceholderText` | Search input in toolbar |

## Column Definition

```python
from winformpy.ui_elements.data_grid import ColumnDefinition, DataType

columns = [
    ColumnDefinition(
        name="employee_id",       # Field name in data
        header="Employee ID",     # Display header
        data_type=DataType.INTEGER,
        width=80,                 # Pixels
        sortable=True,
        searchable=False,         # Exclude from search
        visible=True,
        format_string=None,       # Custom format (optional)
        align="right"             # left, center, right
    ),
    ColumnDefinition("name", "Full Name", DataType.STRING, width=200),
    ColumnDefinition("salary", "Salary", DataType.CURRENCY, width=100, align="right"),
    ColumnDefinition("hire_date", "Hired", DataType.DATE, width=100, 
                     format_string="%d/%m/%Y"),  # Custom date format
]
```

## Backend Implementation Examples

### SQLite Backend

```python
import sqlite3
from winformpy.ui_elements.data_grid import (
    DataGridBackend, ColumnDefinition, DataRequest, DataResponse, 
    PageInfo, DataType, SortOrder
)

class SQLiteBackend(DataGridBackend):
    def __init__(self, db_path: str, table: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.table = table
        self._columns = self._introspect_columns()
    
    def _introspect_columns(self):
        cursor = self.conn.execute(f"PRAGMA table_info({self.table})")
        columns = []
        for row in cursor:
            col_name = row['name']
            col_type = row['type'].upper()
            
            # Map SQLite types to DataType
            if 'INT' in col_type:
                data_type = DataType.INTEGER
            elif 'REAL' in col_type or 'FLOAT' in col_type:
                data_type = DataType.FLOAT
            elif 'DATE' in col_type:
                data_type = DataType.DATE
            else:
                data_type = DataType.STRING
            
            columns.append(ColumnDefinition(col_name, col_name.title(), data_type))
        return columns
    
    def get_columns(self):
        return self._columns
    
    def fetch_data(self, request):
        # Build query
        query = f"SELECT * FROM {self.table}"
        params = []
        
        # Search
        if request.search_text:
            searchable = [c.name for c in self._columns if c.searchable]
            conditions = [f"{col} LIKE ?" for col in searchable]
            query += f" WHERE ({' OR '.join(conditions)})"
            params = [f"%{request.search_text}%"] * len(searchable)
        
        # Sort
        if request.sort_column and request.sort_order != SortOrder.NONE:
            order = "ASC" if request.sort_order == SortOrder.ASCENDING else "DESC"
            query += f" ORDER BY {request.sort_column} {order}"
        
        # Count total
        count_query = query.replace("SELECT *", "SELECT COUNT(*)")
        total = self.conn.execute(count_query, params).fetchone()[0]
        
        # Pagination
        offset = (request.page - 1) * request.page_size
        query += f" LIMIT {request.page_size} OFFSET {offset}"
        
        # Execute
        cursor = self.conn.execute(query, params)
        records = [dict(row) for row in cursor]
        
        total_pages = max(1, (total + request.page_size - 1) // request.page_size)
        
        return DataResponse(
            records=records,
            page_info=PageInfo(
                current_page=request.page,
                page_size=request.page_size,
                total_records=total,
                total_pages=total_pages
            )
        )
```

### REST API Backend

```python
import requests
from winformpy.ui_elements.data_grid import (
    DataGridBackend, ColumnDefinition, DataRequest, DataResponse, 
    PageInfo, DataType, SortOrder
)

class APIBackend(DataGridBackend):
    def __init__(self, base_url: str, endpoint: str, columns: list):
        self.base_url = base_url
        self.endpoint = endpoint
        self._columns = columns
    
    def get_columns(self):
        return self._columns
    
    def fetch_data(self, request):
        params = {
            'page': request.page,
            'limit': request.page_size,
        }
        
        if request.search_text:
            params['search'] = request.search_text
        
        if request.sort_column:
            params['sort'] = request.sort_column
            params['order'] = 'asc' if request.sort_order == SortOrder.ASCENDING else 'desc'
        
        response = requests.get(f"{self.base_url}/{self.endpoint}", params=params)
        data = response.json()
        
        return DataResponse(
            records=data['items'],
            page_info=PageInfo(
                current_page=data['page'],
                page_size=data['limit'],
                total_records=data['total'],
                total_pages=data['total_pages']
            )
        )
```

## Manager Events

```python
manager = DataGridManager(backend)

# Data loaded successfully
manager.DataLoaded = lambda sender, args: print(f"Loaded {len(args['records'])} records")

# Error loading data
manager.DataLoadError = lambda sender, args: show_error(args['message'])

# Selection changed
manager.SelectionChanged = lambda sender, args: update_toolbar(args['selected_records'])

# Page changed
manager.PageChanged = lambda sender, args: print(f"Now on page {args['page']}")

# Sort changed
manager.SortChanged = lambda sender, args: print(f"Sorted by {args['column']}")

# Search changed
manager.SearchChanged = lambda sender, args: print(f"Searching: {args['search_text']}")
```

## Panel Events

```python
grid = DataGridPanel(form, manager=manager)

# Row clicked
grid.RowClick = lambda sender, args: select_record(args['record'])

# Row double-clicked
grid.RowDoubleClick = lambda sender, args: edit_record(args['record'])

# Selection changed
grid.SelectionChanged = lambda sender, args: update_status(args['selected_records'])

# Data loaded
grid.DataLoaded = lambda sender, args: print("Grid refreshed")

# Load error
grid.DataLoadError = lambda sender, args: show_error(args['message'])
```

## Manager Operations

```python
# Refresh data
manager.refresh()

# Search
manager.search("John")
manager.clear_search()

# Pagination
manager.next_page()
manager.previous_page()
manager.first_page()
manager.last_page()
manager.go_to_page(5)

# Sorting
manager.sort("name")  # Toggle sort on column

# Selection
manager.select_record(0)              # Select first row
manager.select_record(1, multi=True)  # Add to selection
manager.select_all()
manager.clear_selection()

# Filters
manager.set_filter("department", "Engineering")
manager.clear_filter("department")
manager.clear_all_filters()

# Properties
print(f"Page {manager.current_page} of {manager.page_info.total_pages}")
print(f"Selected: {len(manager.selected_records)} records")
```

## Column Visibility

DataGridPanel provides methods to show/hide columns dynamically.
All methods accept a single column name or a list of column names:

```python
# Hide a single column
grid.hide_column("internal_id")

# Hide multiple columns at once
grid.hide_column(["internal_id", "created_at", "updated_at"])

# Show columns
grid.show_column("internal_id")
grid.show_column(["internal_id", "notes"])

# Set visibility explicitly
grid.set_column_visibility("notes", False)
grid.set_column_visibility(["id", "name"], True)

# Check visibility
if grid.get_column_visibility("email"):
    print("Email column is visible")

# Get all visible/hidden columns
visible = grid.get_visible_columns()  # ['id', 'name', 'email']
hidden = grid.get_hidden_columns()    # ['internal_id', 'notes']
```

## Integration with RecordFormPanel

DataGridPanel can be linked to a RecordFormPanel to create master-detail views. When a row is selected in the grid, the detail panel automatically updates with the selected record.

### DetailPanel Property

Set the `DetailPanel` property to link a RecordFormPanel:

```python
from winformpy.winformpy import Form, Panel, DockStyle
from winformpy.ui_elements.data_grid import DataGridPanel, DataGridManager
from winformpy.ui_elements.record_form import RecordFormPanel, InMemoryRecordBackend

form = Form({'Text': 'Master-Detail View', 'Width': 1280, 'Height': 700})
form.ApplyLayout()

# Right panel for detail view (create first for proper docking)
right_panel = Panel(form, {'Dock': DockStyle.Right, 'Width': 350})

# Create RecordFormPanel in right panel
record_backend = InMemoryRecordBackend(
    fields=['id', 'name', 'email', 'department'],
    id_field='id'
)

detail = RecordFormPanel(right_panel, {
    'Dock': DockStyle.Fill,
    'Backend': record_backend,
    'Fields': [
        {'name': 'id', 'label': 'ID', 'readonly': True},
        {'name': 'name', 'label': 'Name'},
        {'name': 'email', 'label': 'Email'},
        {'name': 'department', 'label': 'Department'},
    ],
    'ShowInsertButton': False,  # Disable create/delete for detail view
    'ShowDeleteButton': False,
})

# Left panel for grid (Dock.Fill should be last)
left_panel = Panel(form, {'Dock': DockStyle.Fill})

# Create grid
grid_backend = MyDatabaseBackend(connection)
manager = DataGridManager(grid_backend)

grid = DataGridPanel(left_panel, {'Dock': DockStyle.Fill}, manager=manager)

# Link detail panel to grid - automatic updates on selection
grid.DetailPanel = detail

# Load data
manager.refresh()

form.ShowDialog()
```

### How It Works

1. When `DetailPanel` is set, the grid listens for selection changes
2. On selection, it calls `detail_panel.load_record(selected_record)`
3. When selection is cleared, it calls `detail_panel.clear()`
4. The RecordFormPanel displays and allows editing the selected record

### Custom Double-Click Handling

You can combine `DetailPanel` with custom double-click actions:

```python
# DetailPanel handles single-click selection
grid.DetailPanel = detail

# Double-click opens a full dialog for advanced editing
def on_double_click(sender, args):
    record = args['record']
    dialog = RecordFormDialog(columns, record, title="Edit Record")
    if dialog.ShowDialog() == DialogResult.OK:
        # Save changes
        backend.update(dialog.get_values())
        manager.refresh()

grid.RowDoubleClick = on_double_click
```

### Read-Only Detail View

For display-only detail panels, make all fields readonly:

```python
detail = RecordFormPanel(right_panel, {
    'Backend': backend,
    'Fields': [
        {'name': 'id', 'label': 'ID', 'readonly': True},
        {'name': 'name', 'label': 'Name', 'readonly': True},
        # All fields readonly = display only
    ],
    'ShowInsertButton': False,
    'ShowUpdateButton': False,
    'ShowDeleteButton': False,
})
```

## Running the Demo

The module includes interactive demos with simulated employee records:

```bash
python winformpy/ui_elements/data_grid/data_grid_panel.py
```

### Demo Options

1. **Basic DataGrid with events** - 200 employee records with full pagination, sorting, search, and selection. Demonstrates event handling.

2. **DataGrid + RecordFormPanel integration** - Master-detail view with 50 records. Click a row to see details in the right panel. Demonstrates `DetailPanel` property.

Demo features:
- Randomly generated employee records (all data types)
- Full pagination (20 records per page)
- Column sorting (click headers)
- Text search (name, email, department)
- Row selection (single and multi-select)

## Standalone Forms (data_grid_ui.py)

### DataGridForm

A complete standalone window with a data grid:

```python
from winformpy.ui_elements.data_grid import DataGridForm

backend = MyDatabaseBackend(connection)
form = DataGridForm(backend, title="Customer List", width=1024, height=700)
form.RowDoubleClick = lambda s, e: edit_record(e['record'])
form.refresh()
form.ShowDialog()
```

### DataGridPickerForm

A picker dialog for selecting records:

```python
from winformpy.ui_elements.data_grid import DataGridPickerForm, DialogResult

picker = DataGridPickerForm(backend, title="Select Customer", multi_select=False)

if picker.ShowDialog() == DialogResult.OK:
    selected = picker.selected_record
    print(f"Selected: {selected['name']}")
```

### RecordFormDialog

A form for viewing/editing a single record. This component is now in the `record_form` module:

```python
from winformpy.ui_elements.record_form import RecordFormDialog
from winformpy.winformpy import DialogResult

columns = backend.get_columns()
record = get_current_record()

# View mode (readonly)
detail = RecordFormDialog(columns, record, title="View Customer", readonly=True)
detail.ShowDialog()

# Edit mode
edit_form = RecordFormDialog(columns, record, title="Edit Customer", readonly=False)
if edit_form.ShowDialog() == DialogResult.OK:
    updated_values = edit_form.get_values()
    save_to_database(updated_values)
```

## Visibility Properties

Control which elements are visible in the toolbar and pagination bar:

### Toolbar/Pagination Visibility

| Property | Default | Description |
|----------|---------|-------------|
| `ShowToolbar` | `True` | Show/hide the entire top toolbar |
| `ShowPagination` | `True` | Show/hide the entire bottom pagination bar |
| `ShowActionButtons` | `False` | Show/hide OK/Cancel buttons (picker mode) |

### Toolbar Element Visibility

| Property | Default | Description |
|----------|---------|-------------|
| `ShowSearch` | `True` | Show/hide all search controls (🔍 icon, text box, "Search" and "Clear" buttons) |
| `ShowCaseSensitive` | `True` | Show/hide the "Aa" case-sensitive checkbox |
| `ShowExactMatch` | `True` | Show/hide the "Exact" match checkbox |
| `ShowPageSizeControl` | `True` | Show/hide the rows/page size controls |

### Pagination Element Visibility

| Property | Default | Description |
|----------|---------|-------------|
| `ShowRecordInfo` | `True` | Show/hide "Showing X - Y of Z records" label |
| `ShowRecordNavigation` | `True` | Show/hide all navigation buttons (⏮ ◀ ▶ ⏭) and "Page X of Y" label |

### Action Buttons (Picker Mode)

Enable `ShowActionButtons` to add OK/Cancel buttons for record selection:

```python
grid = DataGridPanel(form, props={
    'Dock': DockStyle.Fill,
    'ShowActionButtons': True  # Shows OK/Cancel buttons
}, manager=manager)

# Handle button clicks
grid.OkClick = lambda s, e: print(f"Selected: {e['selected_records']}")
grid.CancelClick = lambda s, e: print("Cancelled")

# Access selected records directly
selected = grid.selected_records
indices = grid.selected_indices
```

### Example: Minimal Grid (No Toolbars)

```python
grid = DataGridPanel(form, props={
    'Dock': DockStyle.Fill,
    'ShowToolbar': False,
    'ShowPagination': False
}, manager=manager)
```

### Example: Simplified Search (No Checkboxes)

```python
grid = DataGridPanel(form, props={
    'Dock': DockStyle.Fill,
    'ShowCaseSensitive': False,
    'ShowExactMatch': False,
    'ShowPageSizeControl': False
}, manager=manager)
```

### Example: Read-Only Grid (No Search)

```python
grid = DataGridPanel(form, props={
    'Dock': DockStyle.Fill,
    'ShowSearch': False
}, manager=manager)
```

### Dynamic Visibility

You can also toggle visibility at runtime:

```python
# Toggle toolbar visibility
grid.ShowToolbar = False  # Hide
grid.ShowToolbar = True   # Show

# Toggle pagination visibility
grid.ShowPagination = False
```

## Inline CRUD (Edit in Row)

DataGridPanel supports inline CRUD operations, allowing users to create, edit, and delete records directly in the grid rows.

### Enabling CRUD

```python
from winformpy.ui_elements.data_grid import DataGridPanel, DataGridManager, SelectionMode

grid = DataGridPanel(form, props={
    'Dock': DockStyle.Fill,
    'AllowEdit': True,           # Enable inline editing
    'AllowAdd': True,            # Show ➕ Add button in toolbar
    'AllowDelete': True,         # Show 🗑️ delete button per row
    'ShowActionColumn': True,    # Show Actions column with edit/delete buttons
    'ActionColumnWidth': 80      # Width of actions column (default: 100)
}, manager=manager)
```

### CRUD Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `AllowEdit` | `bool` | `False` | Enable inline editing (✏️ button per row) |
| `AllowAdd` | `bool` | `False` | Show ➕ Add button in toolbar for new records |
| `AllowDelete` | `bool` | `False` | Enable row deletion (🗑️ button per row) |
| `ShowActionColumn` | `bool` | `False` | Show the Actions column with Edit/Delete buttons |
| `ActionColumnWidth` | `int` | `100` | Width of the Actions column in pixels |
| `DateFormat` | `str` | `'system'` | Date format for editing: `'ISO'`, `'EU'`, `'US'`, or `'system'` |
| `TimeFormat` | `str` | `'24h'` | Time format: `'24h'` or `'12h'` |

### Input Masks and Locale

When editing DATE and DATETIME columns, the grid uses **MaskedTextBox** with locale-aware masks:

#### Date Format Options

| DateFormat | Pattern | Example | Used in |
|------------|---------|---------|---------|
| `'ISO'` | `YYYY-MM-DD` | `2024-01-15` | International standard, Asian countries |
| `'EU'` | `DD/MM/YYYY` | `15/01/2024` | Spain, France, Germany, UK, Australia, Latin America |
| `'US'` | `MM/DD/YYYY` | `01/15/2024` | United States |
| `'system'` | Auto-detect | Depends on OS locale | **Default** |

#### Time Format Options

| TimeFormat | Pattern | Example |
|------------|---------|---------|
| `'24h'` | `HH:MM` | `14:30` |
| `'12h'` | `HH:MM AM/PM` | `02:30 PM` |

#### Example: Explicit Format

```python
# Spanish format (DD/MM/YYYY)
grid = DataGridPanel(form, props={
    'Dock': DockStyle.Fill,
    'AllowEdit': True,
    'ShowActionColumn': True,
    'DateFormat': 'EU',          # Force European format
    'TimeFormat': '24h'
}, manager=manager)
```

#### Example: Full Locale Configuration

```python
# Spanish locale with Euro currency
grid = DataGridPanel(form, props={
    'Dock': DockStyle.Fill,
    'AllowEdit': True,
    'ShowActionColumn': True,
    'DateFormat': 'EU',          # DD/MM/YYYY
    'TimeFormat': '24h',
    'NumberFormat': 'EU',        # 1.234,56 (dot thousands, comma decimal)
    'CurrencySymbol': '€',       # Euro symbol
    'CurrencyPosition': 'after'  # 100 € (symbol after number)
}, manager=manager)
```

#### Example: Auto-detect from System

```python
# Let the system decide based on OS locale
grid = DataGridPanel(form, props={
    'Dock': DockStyle.Fill,
    'AllowEdit': True,
    'ShowActionColumn': True,
    'DateFormat': 'system',      # Auto-detect (default)
    'NumberFormat': 'system',    # Auto-detect (default)
    'CurrencySymbol': 'system',  # Auto-detect (default)
}, manager=manager)
```

#### System Locale Detection

When using `'system'`, the grid auto-detects settings based on OS locale:

| Locale | Date Format | Number Format | Currency |
|--------|-------------|---------------|----------|
| `es_ES` | `'EU'` (DD/MM/YYYY) | `1.234,56` | `100 €` |
| `fr_FR` | `'EU'` (DD/MM/YYYY) | `1.234,56` | `100 €` |
| `de_DE` | `'EU'` (DD/MM/YYYY) | `1.234,56` | `100 €` |
| `en_GB` | `'EU'` (DD/MM/YYYY) | `1,234.56` | `£100` |
| `en_US` | `'US'` (MM/DD/YYYY) | `1,234.56` | `$100` |
| `ja_JP`, `zh_CN` | `'ISO'` (YYYY-MM-DD) | `1,234.56` | `¥100` |

#### Number Format Options

| NumberFormat | Thousands | Decimal | Example |
|--------------|-----------|---------|---------|
| `'US'` | `,` | `.` | `1,234.56` |
| `'EU'` | `.` | `,` | `1.234,56` |
| `'system'` | Auto | Auto | Depends on locale |

#### Currency Options

| Property | Values | Description |
|----------|--------|-------------|
| `CurrencySymbol` | `'$'`, `'€'`, `'£'`, `'¥'`, `'system'` | Currency symbol to use |
| `CurrencyPosition` | `'before'`, `'after'`, `'system'` | Symbol position: `$100` vs `100 €` |

#### Display Format Examples

| DataType | US Format | EU Format (es_ES) |
|----------|-----------|-------------------|
| `INTEGER` | `1,234` | `1.234` |
| `FLOAT` | `1,234.56` | `1.234,56` |
| `CURRENCY` | `$1,234.56` | `1.234,56 €` |
| `PERCENTAGE` | `85.5%` | `85,5%` |
| `DATE` | `01/15/2024` | `15/01/2024` |

#### Edit Mode Format

When editing, numeric fields are formatted according to locale settings:

| DataType | US Edit | EU Edit | Notes |
|----------|---------|---------|-------|
| `INTEGER` | `1234` | `1234` | No thousands separator in edit |
| `FLOAT` | `1234.56` | `1234,56` | Decimal separator follows locale |
| `CURRENCY` | `1234.56` | `1234,56` | Symbol removed for editing |
| `PERCENTAGE` | `85.5` | `85,5` | % removed for editing |
| `DATE` | `01/15/2024` | `15/01/2024` | MaskedTextBox with locale mask |

**Important**: The grid automatically:
1. **Displays** values with full locale formatting (thousands, currency symbol, %)
2. **Edits** values in simplified locale format (decimal separator only, no symbols)
3. **Parses** values using the configured locale when saving

#### Widget Types by DataType

| DataType | Edit Widget | Mask |
|----------|-------------|------|
| `BOOLEAN` | CheckBox | (none) |
| `DATE` | MaskedTextBox | `0000-00-00` / `00/00/0000` |
| `DATETIME` | MaskedTextBox | `0000-00-00 00:00` / `00/00/0000 00:00` |
| `STRING`, `INTEGER`, `FLOAT`, `CURRENCY`, `PERCENTAGE` | TextBox | (none) |

### CRUD Events

```python
# Record created (after successful insert)
grid.RecordCreated = lambda s, e: print(f"Created: {e['record']}")

# Record updated (after successful update)
grid.RecordUpdated = lambda s, e: print(f"Updated: {e['record']}")

# Record deleted (after successful delete)
grid.RecordDeleted = lambda s, e: print(f"Deleted: {e['record']}")

# Edit started (row entered edit mode)
grid.EditStarted = lambda s, e: print(f"Editing row {e['index']}")

# Edit cancelled
grid.EditCancelled = lambda s, e: print(f"Edit cancelled for row {e['index']}")
```

### CRUD Methods

```python
# Start editing a specific row
grid.BeginEdit(index=2)      # Edit row at index 2
grid.BeginEdit()             # Edit selected row

# Start adding a new row
grid.BeginAdd()              # Adds empty row in edit mode

# Save current edit
success = grid.SaveEdit()    # Returns True if saved successfully

# Cancel current edit
grid.CancelEdit()            # Restores original values

# Delete a record
grid.DeleteRecord(index=3)   # Delete row at index 3
grid.DeleteRecord()          # Delete selected row

# Check edit state
if grid.IsEditing:
    print(f"Currently editing row {grid.EditingRowIndex}")
```

### Visual Behavior

When CRUD is enabled:

1. **Normal Mode**:
   - Each row shows ✏️ (edit) and 🗑️ (delete) buttons in the Actions column
   - Toolbar shows ➕ button for adding new records

2. **Edit Mode** (when editing a row):
   - Cell values become editable TextBox/CheckBox widgets
   - Actions column shows ✓ (save) and ✗ (cancel) buttons
   - Row background changes to light yellow

3. **Add Mode** (when adding new record):
   - New row appears at the bottom with empty fields
   - Each field shows placeholder text with column header
   - Same ✓/✗ buttons for save/cancel

### Implementing a CRUD Backend

Your backend must implement CRUD methods:

```python
from winformpy.ui_elements.data_grid import DataGridBackend

class MyCrudBackend(DataGridBackend):
    def __init__(self, data):
        self._data = data
        self._next_id = max(r['id'] for r in data) + 1
    
    # Required: Indicate CRUD support
    def supports_crud(self) -> bool:
        return True
    
    # Required: Primary key field name
    def get_primary_key(self) -> str:
        return "id"
    
    # Create new record
    def create_record(self, record: dict) -> dict:
        new_record = record.copy()
        new_record['id'] = self._next_id
        self._next_id += 1
        self._data.append(new_record)
        return new_record
    
    # Update existing record
    def update_record(self, pk_value, changes: dict) -> bool:
        for i, r in enumerate(self._data):
            if r['id'] == pk_value:
                self._data[i].update(changes)
                return True
        return False
    
    # Delete record
    def delete_record(self, pk_value) -> bool:
        for i, r in enumerate(self._data):
            if r['id'] == pk_value:
                self._data.pop(i)
                return True
        return False
    
    # Optional: Validation before save
    def validate_record(self, record: dict, is_new: bool = False) -> tuple:
        if not record.get('name'):
            return False, "Name is required"
        return True, ""
    
    # ... also implement get_columns() and fetch_data()
```

### Complete CRUD Example

```python
from winformpy.winformpy import Form, DockStyle
from winformpy.ui_elements.data_grid import (
    DataGridPanel, DataGridManager, DataGridBackend,
    ColumnDefinition, DataRequest, DataResponse, PageInfo, DataType, SortOrder
)

class ProductBackend(DataGridBackend):
    """In-memory backend with CRUD support."""
    
    def __init__(self):
        self._next_id = 4
        self._data = [
            {"id": 1, "name": "Laptop", "price": 999.99, "stock": 50},
            {"id": 2, "name": "Mouse", "price": 29.99, "stock": 200},
            {"id": 3, "name": "Keyboard", "price": 79.99, "stock": 150},
        ]
        self._columns = [
            ColumnDefinition("id", "ID", DataType.INTEGER, width=60),
            ColumnDefinition("name", "Product", DataType.STRING, width=180),
            ColumnDefinition("price", "Price", DataType.CURRENCY, width=100),
            ColumnDefinition("stock", "Stock", DataType.INTEGER, width=80),
        ]
    
    def get_columns(self):
        return self._columns
    
    def fetch_data(self, request: DataRequest) -> DataResponse:
        # Simple fetch (add sorting/filtering as needed)
        return DataResponse(
            records=self._data.copy(),
            page_info=PageInfo(1, len(self._data), len(self._data), 1)
        )
    
    def supports_crud(self) -> bool:
        return True
    
    def get_primary_key(self) -> str:
        return "id"
    
    def create_record(self, record):
        new_record = record.copy()
        new_record["id"] = self._next_id
        self._next_id += 1
        # Convert types
        new_record["price"] = float(new_record.get("price", 0))
        new_record["stock"] = int(new_record.get("stock", 0))
        self._data.append(new_record)
        return new_record
    
    def update_record(self, pk_value, changes):
        for i, r in enumerate(self._data):
            if r["id"] == pk_value:
                changes["price"] = float(changes.get("price", r["price"]))
                changes["stock"] = int(changes.get("stock", r["stock"]))
                self._data[i].update(changes)
                return True
        return False
    
    def delete_record(self, pk_value):
        for i, r in enumerate(self._data):
            if r["id"] == pk_value:
                self._data.pop(i)
                return True
        return False


# Create application
form = Form({'Text': 'Product Inventory', 'Width': 800, 'Height': 500})
form.ApplyLayout()

backend = ProductBackend()
manager = DataGridManager(backend)

grid = DataGridPanel(form, props={
    'Dock': DockStyle.Fill,
    'AllowEdit': True,
    'AllowAdd': True,
    'AllowDelete': True,
    'ShowActionColumn': True,
    'ActionColumnWidth': 80
}, manager=manager)

# Event handlers
grid.RecordCreated = lambda s, e: print(f"✅ Created: {e['record']['name']}")
grid.RecordUpdated = lambda s, e: print(f"✅ Updated: {e['record']['name']}")
grid.RecordDeleted = lambda s, e: print(f"🗑️ Deleted: {e['record']['name']}")

manager.refresh()
form.ShowDialog()
```

### Running the CRUD Demo

```bash
python winformpy/ui_elements/data_grid/data_grid_panel.py
# Select option 2: CRUD Inline DataGrid
```

## Selection Modes

Control how rows can be selected using the `SelectionMode` property:

```python
from winformpy.ui_elements.data_grid import DataGridPanel, SelectionMode

# No selection allowed
grid = DataGridPanel(form, props={
    'SelectionMode': SelectionMode.NONE
}, manager=manager)

# Single row selection only (default behavior before multi-select)
grid = DataGridPanel(form, props={
    'SelectionMode': SelectionMode.SINGLE
}, manager=manager)

# Multiple selection with Ctrl+Click and Shift+Click (default)
grid = DataGridPanel(form, props={
    'SelectionMode': SelectionMode.MULTIPLE
}, manager=manager)
```

### SelectionMode Values

| Mode | Description |
|------|-------------|
| `NONE` | No selection - clicking rows only fires `RowClick` event |
| `SINGLE` | Only one row can be selected at a time |
| `MULTIPLE` | Multiple rows with Ctrl+Click (toggle) and Shift+Click (range) |

### Selection Properties and Methods

```python
# Get selected records
records = grid.selected_records      # List of record dictionaries
indices = grid.selected_indices      # List of row indices
record = grid.selected_record        # First selected record (convenience)

# Selection methods
grid.SelectAll()                     # Select all visible rows
grid.ClearSelection()                # Clear all selections
grid.SelectRecord(5)                 # Select row at index 5
grid.ToggleRecordSelection(5)        # Toggle selection of row 5
```

## File Structure

```
data_grid/
├── __init__.py           # Package exports
├── data_grid_backend.py  # Backend ABC and data classes
├── data_grid_manager.py  # Service layer
├── data_grid_panel.py    # Visual component (embeddable)
├── data_grid_ui.py       # Standalone forms and dialogs
└── README.md             # This file
```
