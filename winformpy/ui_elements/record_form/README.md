# Record Form UI Element

A reusable UI component for displaying and editing individual record details with auto-generated input fields and pluggable backend architecture.

## Overview

The Record Form element provides:

- **RecordFormPanel**: Embeddable panel that auto-generates fields based on column definitions
- **RecordFormDialog**: Standalone dialog form for viewing/editing records
- **RecordFormBackend**: Abstract base class for CRUD operations (insert, update, delete)
- **InMemoryRecordBackend**: In-memory backend implementation for testing and demos

## Features

- Auto-generates input fields from ColumnDefinition metadata
- Supports multiple data types (String, Integer, Currency, Boolean, Date, etc.)
- Read-only, edit, and insert modes
- Built-in CRUD action buttons (Insert, Update, Delete, Cancel)
- **Pluggable backend architecture** for any data source
- Value change events for real-time validation
- Responsive layout that adjusts to container size
- Dynamic field visibility (show/hide fields at runtime)
- Backend hooks for before/after operations

## Quick Start

### Using RecordFormPanel with Backend (Recommended)

```python
from winformpy.ui_elements.record_form import (
    RecordFormPanel, RecordFormBackend, InMemoryRecordBackend, RecordFormMode
)
from winformpy.ui_elements.data_grid import ColumnDefinition, DataType

# Define columns
columns = [
    ColumnDefinition("id", "ID", DataType.INTEGER, width=60, visible=False),
    ColumnDefinition("name", "Name", DataType.STRING),
    ColumnDefinition("email", "Email", DataType.STRING),
    ColumnDefinition("salary", "Salary", DataType.CURRENCY),
    ColumnDefinition("active", "Active", DataType.BOOLEAN),
]

# Create backend with initial data
backend = InMemoryRecordBackend(records=[
    {'id': 1, 'name': 'John', 'email': 'john@example.com', 'salary': 50000, 'active': True},
    {'id': 2, 'name': 'Jane', 'email': 'jane@example.com', 'salary': 60000, 'active': True},
])

# Create panel with CRUD buttons
panel = RecordFormPanel(parent, props={
    'Dock': DockStyle.Fill,
    'Columns': columns,
    'Record': backend.get_records()[0],
    'Backend': backend,
    'ShowInsertButton': True,
    'ShowUpdateButton': True,
    'ShowDeleteButton': True,
    'ShowCancelButton': True
})

# Handle events
panel.RecordInserted = lambda s, e: print(f"Inserted: {e['record']}")
panel.RecordUpdated = lambda s, e: print(f"Updated: {e['record']}")
panel.RecordDeleted = lambda s, e: print(f"Deleted: {e['record']}")
panel.ValidationFailed = lambda s, e: print(f"Errors: {e['errors']}")
```

### Using RecordFormPanel without Backend (Manual CRUD)

```python
from winformpy.ui_elements.record_form import RecordFormPanel
from winformpy.ui_elements.data_grid import ColumnDefinition, DataType

# Define columns
columns = [
    ColumnDefinition("name", "Name", DataType.STRING),
    ColumnDefinition("email", "Email", DataType.STRING),
    ColumnDefinition("salary", "Salary", DataType.CURRENCY),
    ColumnDefinition("active", "Active", DataType.BOOLEAN),
]

# Create panel without backend
panel = RecordFormPanel(parent, props={
    'Dock': DockStyle.Fill,
    'Columns': columns,
    'Record': {'name': 'John', 'email': 'john@example.com', 'salary': 50000, 'active': True},
    'ReadOnly': False,
    'ShowActionButtons': True  # Shows Save/Cancel buttons
})

# Handle manual save
panel.SaveClick = lambda s, e: save_to_database(e['values'])
panel.CancelClick = lambda s, e: cancel_edit()
panel.ValueChanged = lambda s, e: validate_field(e['field'])
```

### Using RecordFormDialog (Standalone Dialog)

```python
from winformpy.ui_elements.record_form import RecordFormDialog
from winformpy.winformpy import DialogResult

# Show edit dialog
dialog = RecordFormDialog(
    columns=columns,
    record=record,
    title="Edit Customer",
    readonly=False
)

if dialog.ShowDialog() == DialogResult.OK:
    updated_values = dialog.get_values()
    save_to_database(updated_values)
```

## Backend Architecture

### RecordFormBackend (Abstract Base Class)

The `RecordFormBackend` class defines the contract for CRUD operations:

```python
from winformpy.ui_elements.record_form import RecordFormBackend, RecordResponse, ValidationResult

class MySQLRecordBackend(RecordFormBackend):
    """Custom backend for MySQL database."""
    
    def __init__(self, connection, table_name):
        super().__init__()
        self.conn = connection
        self.table = table_name
    
    def insert(self, record: dict) -> RecordResponse:
        # Execute INSERT SQL
        cursor = self.conn.cursor()
        # ... SQL execution ...
        return RecordResponse(success=True, record=inserted_record)
    
    def update(self, record: dict) -> RecordResponse:
        # Execute UPDATE SQL
        return RecordResponse(success=True, record=updated_record)
    
    def delete(self, record: dict) -> RecordResponse:
        # Execute DELETE SQL
        return RecordResponse(success=True, record=deleted_record)
    
    def validate(self, record: dict, mode) -> ValidationResult:
        # Custom validation
        errors = {}
        if not record.get('email'):
            errors['email'] = "Email is required"
        return ValidationResult(is_valid=len(errors) == 0, errors=errors)
```

### Backend Callbacks

The backend provides callbacks for operation completion:

```python
backend = InMemoryRecordBackend()

# Set callbacks
backend.on_insert_complete = lambda response: print(f"Inserted: {response.record}")
backend.on_update_complete = lambda response: print(f"Updated: {response.record}")
backend.on_delete_complete = lambda response: print(f"Deleted: {response.record}")
backend.on_validation_error = lambda result: print(f"Errors: {result.errors}")
```

### Backend Hooks

Override hooks for custom behavior:

```python
class CustomBackend(RecordFormBackend):
    def before_insert(self, record):
        # Add timestamp
        record['created_at'] = datetime.now()
        return record
    
    def before_update(self, record):
        # Add modification timestamp
        record['updated_at'] = datetime.now()
        return record
    
    def before_delete(self, record):
        # Show confirmation (return False to cancel)
        return messagebox.askyesno("Confirm", "Delete this record?")
    
    def get_default_values(self):
        # Default values for new records
        return {'status': 'active', 'created_by': 'admin'}
```

### InMemoryRecordBackend

Built-in backend for testing and demos:

```python
from winformpy.ui_elements.record_form import InMemoryRecordBackend

# Create with initial records
backend = InMemoryRecordBackend(records=[
    {'id': 1, 'name': 'John'},
    {'id': 2, 'name': 'Jane'}
], primary_key='id')

# Or set records later
backend = InMemoryRecordBackend()
backend.set_records(my_records)

# Get all records
records = backend.get_records()
```

### Factory Function

```python
from winformpy.ui_elements.record_form import create_record_backend

# Create in-memory backend
backend = create_record_backend("memory", records=my_records, primary_key='id')
```

## Form Modes

The `RecordFormMode` enum defines three modes:

| Mode | Description |
|------|-------------|
| `VIEW` | Read-only viewing of a record |
| `EDIT` | Editing an existing record |
| `INSERT` | Creating a new record |

```python
from winformpy.ui_elements.record_form import RecordFormMode

# Switch to insert mode (clears fields, shows Insert button)
panel.new_record()

# Switch to edit mode (shows Update button)
panel.edit_record()

# Switch to view mode (read-only)
panel.view_record()

# Check current mode
if panel.Mode == RecordFormMode.INSERT:
    print("Creating new record")
```

## RecordFormPanel Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Columns` | List[ColumnDefinition] | [] | Column definitions for input fields |
| `Record` | Dict[str, Any] | {} | Current record data |
| `ReadOnly` | bool | False | If True, all fields are read-only |
| `Backend` | RecordFormBackend | None | Backend for CRUD operations |
| `Mode` | RecordFormMode | VIEW | Current form mode |
| `ShowActionButtons` | bool | False | Show Save/Cancel buttons (legacy) |
| `ShowInsertButton` | bool | True* | Show Insert/New button |
| `ShowUpdateButton` | bool | True* | Show Update/Save button |
| `ShowDeleteButton` | bool | True* | Show Delete button |
| `ShowCancelButton` | bool | True* | Show Cancel/Close button |
| `FieldSpacing` | int | 40 | Vertical spacing between fields |
| `LabelWidth` | int | 150 | Width of field labels |
| `ContentPadding` | int | 20 | Internal padding |

\* These buttons default to `True` when `Backend` is provided, otherwise `False`.

## Customizing with Sub-Properties

RecordFormPanel supports sub-properties for configuring internal elements:

| Sub-Property | Applies To | Common Options |
|--------------|------------|----------------|
| `ContentPanel` | Content area | `BackColor`, `Padding` |
| `ActionPanel` | Action buttons area | `Height`, `BackColor` |
| `Labels` | Field labels | `Font`, `ForeColor` |
| `Inputs` | Input fields | `Font`, `Height`, `BackColor` |
| `Buttons` | Action buttons | `Font`, `Width`, `Height` |

### Example with Sub-Properties

```python
panel = RecordFormPanel(parent, props={
    'Dock': DockStyle.Fill,
    'Columns': columns,
    'Backend': backend,
    # Sub-properties for internal elements
    'ContentPanel': {
        'BackColor': '#FAFAFA'
    },
    'ActionPanel': {
        'Height': 70,
        'BackColor': '#F0F0F0'
    },
    'Labels': {
        'Font': Font('Segoe UI', 11, FontStyle.Bold),
        'ForeColor': '#333333'
    },
    'Inputs': {
        'Height': 32,
        'Font': Font('Segoe UI', 11),
        'BackColor': '#FFFFFF'
    },
    'Buttons': {
        'Width': 100,
        'Height': 36,
        'Font': Font('Segoe UI', 10)
    }
})
```

## RecordFormPanel Events

### CRUD Events (with Backend)

| Event | Args | Description |
|-------|------|-------------|
| `InsertClick` | `{'values': dict}` | Fired when Insert button clicked |
| `UpdateClick` | `{'values': dict}` | Fired when Update button clicked |
| `DeleteClick` | `{'record': dict}` | Fired when Delete button clicked |
| `RecordInserted` | `{'record': dict, 'response': RecordResponse}` | Fired after successful insert |
| `RecordUpdated` | `{'record': dict, 'response': RecordResponse}` | Fired after successful update |
| `RecordDeleted` | `{'record': dict, 'response': RecordResponse}` | Fired after successful delete |
| `ValidationFailed` | `{'errors': dict}` | Fired when validation fails |

### Legacy Events (without Backend)

| Event | Args | Description |
|-------|------|-------------|
| `SaveClick` | `{'values': dict}` | Fired when Save button clicked |
| `CancelClick` | `{}` | Fired when Cancel button clicked |
| `ValueChanged` | `{'field': str, 'values': dict}` | Fired when any field changes |

## RecordFormPanel Methods

| Method | Description |
|--------|-------------|
| `get_values()` | Get all field values as dictionary |
| `set_values(record)` | Set all field values from dictionary |
| `load_record(record)` | Alias for `set_values()` - for DataGridPanel integration |
| `clear()` | Clear all field values |
| `new_record()` | Switch to INSERT mode with empty/default fields |
| `edit_record()` | Switch to EDIT mode |
| `view_record()` | Switch to VIEW mode (read-only) |
| `set_field_value(name, value)` | Set a specific field value |
| `get_field_value(name)` | Get a specific field value |
| `hide_field(name)` | Hide field(s) - accepts str or list |
| `show_field(name)` | Show field(s) - accepts str or list |
| `set_field_visibility(name, visible)` | Set visibility - accepts str or list |
| `get_field_visibility(name)` | Get field visibility state |
| `get_visible_fields()` | Get list of visible field names |
| `get_hidden_fields()` | Get list of hidden field names |

## Field Visibility

RecordFormPanel allows dynamic show/hide of fields. Methods accept a single field name or a list:

```python
# Hide a single field
panel.hide_field("password")

# Hide multiple fields at once
panel.hide_field(["password", "secret_key", "internal_id"])

# Show fields
panel.show_field("email")
panel.show_field(["phone", "address"])

# Set visibility explicitly
panel.set_field_visibility("notes", False)
panel.set_field_visibility(["id", "name"], True)

# Check visibility state
if panel.get_field_visibility("email"):
    print("Email field is visible")

# Get all visible/hidden fields
visible = panel.get_visible_fields()  # ['name', 'email', 'phone']
hidden = panel.get_hidden_fields()    # ['password', 'internal_id']
```

## Data Type Support

The panel automatically creates appropriate widgets based on `DataType`:

| DataType | Widget | Notes |
|----------|--------|-------|
| STRING | TextBox | Standard text input |
| INTEGER | TextBox | Converts to int on get_values() |
| FLOAT | TextBox | Converts to float on get_values() |
| CURRENCY | TextBox | Formats with commas, strips symbols |
| PERCENTAGE | TextBox | Formats with %, strips symbol |
| BOOLEAN | CheckBox | Checked/unchecked |
| DATE | TextBox | Formats as YYYY-MM-DD |
| DATETIME | TextBox | Formats as YYYY-MM-DD HH:MM |

## Integration with DataGrid

RecordFormPanel works seamlessly with DataGrid's column definitions:

```python
from winformpy.ui_elements.data_grid import DataGridPanel, DataGridBackend
from winformpy.ui_elements.record_form import RecordFormPanel

# Get columns from backend
backend = MyDatabaseBackend()
columns = backend.get_columns()

# Use same columns in form panel
form_panel = RecordFormPanel(parent, props={
    'Columns': columns,
    'Record': selected_record,
    'ShowActionButtons': True
})
```

## Master-Detail Pattern with Backend

```python
from winformpy.ui_elements.record_form import RecordFormPanel, InMemoryRecordBackend

# Create shared backend
backend = InMemoryRecordBackend(records=employee_list, primary_key='id')

# Left: List of records
list_panel = Panel(left, {'Dock': DockStyle.Fill})

# Right: Form panel with CRUD
form_panel = RecordFormPanel(right_panel, props={
    'Dock': DockStyle.Fill,
    'Columns': columns,
    'Backend': backend,
    'ShowInsertButton': True,
    'ShowUpdateButton': True,
    'ShowDeleteButton': True,
    'ShowCancelButton': True
})

# Update list after changes
def refresh_list():
    # Rebuild list from backend
    for record in backend.get_records():
        # Create list item button...
        pass

form_panel.RecordInserted = lambda s, e: refresh_list()
form_panel.RecordUpdated = lambda s, e: refresh_list()
form_panel.RecordDeleted = lambda s, e: refresh_list()

# Load record when selected
def on_select(record):
    form_panel.Record = record
    form_panel.edit_record()
```

## Master-Detail Pattern (Legacy)

```python
# Left: DataGrid with records
grid = DataGridPanel(left_panel, props={'Dock': DockStyle.Fill})

# Right: Form panel for selected record
form_panel = RecordFormPanel(right_panel, props={
    'Dock': DockStyle.Fill,
    'Columns': columns,
    'ReadOnly': True
})

# Update form when selection changes
def on_selection(sender, args):
    record = args.get('record')
    if record:
        form_panel.Record = record

grid.RowClick = on_selection
```

## DataGridPanel.DetailPanel Integration

The easiest way to create a master-detail view is to use `DataGridPanel.DetailPanel`. When set, the grid automatically updates the form panel when a row is selected.

```python
from winformpy.winformpy import Form, Panel, DockStyle
from winformpy.ui_elements.data_grid import DataGridPanel, DataGridManager
from winformpy.ui_elements.record_form import RecordFormPanel, InMemoryRecordBackend

form = Form({'Text': 'Master-Detail View', 'Width': 1280, 'Height': 700})
form.ApplyLayout()

# Right panel for detail view (create first for proper docking)
right_panel = Panel(form, {'Dock': DockStyle.Right, 'Width': 350})

# Create RecordFormPanel
backend = InMemoryRecordBackend(fields=['id', 'name', 'email'], id_field='id')
detail = RecordFormPanel(right_panel, {
    'Dock': DockStyle.Fill,
    'Backend': backend,
    'Fields': [
        {'name': 'id', 'label': 'ID', 'readonly': True},
        {'name': 'name', 'label': 'Name'},
        {'name': 'email', 'label': 'Email'},
    ],
})

# Left panel for grid
left_panel = Panel(form, {'Dock': DockStyle.Fill})
grid = DataGridPanel(left_panel, {'Dock': DockStyle.Fill}, manager=my_manager)

# Link form panel to grid - automatic updates on selection
grid.DetailPanel = detail

manager.refresh()
form.ShowDialog()
```

### How It Works

1. When `grid.DetailPanel = form_panel` is set, the grid tracks selection changes
2. On row selection, it calls `form_panel.load_record(selected_record)`
3. When selection is cleared, it calls `form_panel.clear()`
4. The `load_record()` method is an alias for `set_values()` - both work identically

### Running the Integration Demo

```bash
# Interactive demo with multiple integration examples
python winformpy/ui_elements/data_grid/data_grid_panel.py
```

## Data Classes

### RecordResponse

Response from backend operations:

```python
from dataclasses import dataclass

@dataclass
class RecordResponse:
    success: bool = True
    record: Dict[str, Any] = field(default_factory=dict)
    error_message: str = ""
    validation_errors: Dict[str, str] = field(default_factory=dict)
```

### ValidationResult

Result from validation:

```python
@dataclass
class ValidationResult:
    is_valid: bool = True
    errors: Dict[str, str] = field(default_factory=dict)  # field_name -> error_message
```

## Styling

Customize colors via the COLORS dictionary:

```python
RecordFormPanel.COLORS = {
    'background': '#FFFFFF',
    'text': '#1A1A1A',
    'text_secondary': '#666666',
    'primary': '#0078D4',
    'border': '#E0E0E0',
    'input_bg': '#FFFFFF',
    'button_bg': '#F0F0F0',
}
```

## Backwards Compatibility

For backwards compatibility, the old names are still available as aliases:

```python
# These are equivalent:
from winformpy.ui_elements.record_form import RecordFormPanel
from winformpy.ui_elements.record_form import RecordDetailPanel  # alias

from winformpy.ui_elements.record_form import RecordFormDialog
from winformpy.ui_elements.record_form import RecordDetailForm   # alias
```

## File Structure

```
record_form/
├── __init__.py              # Package exports
├── record_form_backend.py   # Abstract backend + InMemoryRecordBackend
├── record_form_panel.py     # Embeddable panel component
├── record_form_ui.py        # Standalone dialog forms
└── README.md                # This documentation
```

## Complete Example

```python
from winformpy.winformpy import Form, Panel, Button, Label, DockStyle
from winformpy.ui_elements.record_form import (
    RecordFormPanel, InMemoryRecordBackend, RecordFormMode
)
from winformpy.ui_elements.data_grid import ColumnDefinition, DataType

# Column definitions
columns = [
    ColumnDefinition("id", "ID", DataType.INTEGER, width=60),
    ColumnDefinition("name", "Name", DataType.STRING, width=150),
    ColumnDefinition("email", "Email", DataType.STRING, width=200),
    ColumnDefinition("department", "Department", DataType.STRING, width=120),
    ColumnDefinition("salary", "Salary", DataType.CURRENCY, width=100),
    ColumnDefinition("active", "Active", DataType.BOOLEAN, width=80),
]

# Backend with sample data
backend = InMemoryRecordBackend(records=[
    {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 
     'department': 'Engineering', 'salary': 75000, 'active': True},
    {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com',
     'department': 'Marketing', 'salary': 65000, 'active': True},
], primary_key='id')

# Create form
form = Form({'Text': 'Employee Manager', 'Width': 900, 'Height': 600})
form.ApplyLayout()

# Left panel - Employee list
left_panel = Panel(form, {'Dock': DockStyle.Left, 'Width': 250})

# New Employee button
new_btn = Button(left_panel, {
    'Text': '+ New Employee', 
    'Dock': DockStyle.Top, 
    'Height': 40
})

# Right panel - Form
right_panel = Panel(form, {'Dock': DockStyle.Fill})

form_panel = RecordFormPanel(right_panel, props={
    'Dock': DockStyle.Fill,
    'Columns': columns,
    'Backend': backend,
    'ShowInsertButton': True,
    'ShowUpdateButton': True,
    'ShowDeleteButton': True,
    'ShowCancelButton': True
})

# Event handlers
def create_employee_list():
    # Clear existing buttons (except first)
    for widget in left_panel._tk_widget.winfo_children()[1:]:
        widget.destroy()
    
    for emp in backend.get_records():
        btn = Button(left_panel, {
            'Text': emp['name'],
            'Dock': DockStyle.Top,
            'Height': 35
        })
        btn.Click = lambda s, e, r=emp: select_employee(r)

def select_employee(record):
    form_panel.Record = record
    form_panel.edit_record()

def on_new_click(sender, e):
    form_panel.new_record()

new_btn.Click = on_new_click
form_panel.RecordInserted = lambda s, e: create_employee_list()
form_panel.RecordUpdated = lambda s, e: create_employee_list()
form_panel.RecordDeleted = lambda s, e: create_employee_list()

# Initialize
create_employee_list()
form.Show()
```
