# 🧩 UI Elements

Pre-built, **architecture-agnostic**, embeddable UI components for WinFormPy applications.

## 📖 Overview

UI Elements are complete, ready-to-use components that can be embedded in your applications. Each element follows a consistent architecture that **separates visual presentation from business logic and external operations**.

**Key Principle**: Components are **completely decoupled** from specific backend implementations. You can use them with any storage system, API, or service of your choice.

## 🏗️ Architecture Pattern

All UI Elements follow the same layered architecture:

```
┌─────────────────────────────────────────────────────┐
│  UI Layer (Panel / Form)                            │
│    → Visual components and user interaction         │
│    → Receives Manager as dependency                 │
├─────────────────────────────────────────────────────┤
│  Service Layer (Manager)                            │
│    → Business logic and state management            │
│    → Validates data and handles events              │
│    → Delegates operations to backend                │
├─────────────────────────────────────────────────────┤
│  ⚠️ EXTERNAL (not part of this project)             │
│  Backend Implementation                             │
│    → Must be provided by the application            │
│    → Connects to external services/APIs             │
└─────────────────────────────────────────────────────┘
```

**⚠️ IMPORTANT**: Backend implementations are **NOT part of WinFormPy**. They must be provided externally by your application.

---

## 🎨 Sub-Properties System

UI Elements support **sub-properties** for deep customization of internal elements. This allows you to configure colors, sizes, fonts and other properties of the internal components.

### How It Works

When creating a UI Element, you can pass sub-property dictionaries in the `props` parameter:

```python
panel = SomePanel(form, props={
    # Regular Panel properties
    'Dock': DockStyle.Fill,
    'BackColor': '#FFFFFF',
    
    # Sub-properties for internal elements
    'Toolbar': {'Height': 50, 'BackColor': '#E0E0E0'},
    'Header': {'ForeColor': '#333', 'Font': Font('Segoe UI', 12)},
    'Button': {'BackColor': '#0078D4', 'ForeColor': '#FFF'}
})
```

### Available Sub-Properties by Component

| Component | Sub-Properties |
|-----------|----------------|
| **DataGridPanel** | `Toolbar`, `Header`, `Rows`, `Pagination`, `SearchBox` + Visibility props (see below) |
| **ChatPanel** | `InputArea`, `SendButton`, `MessageArea`, `UserBubble`, `AssistantBubble` |
| **LoginPanel** | `Title`, `Subtitle`, `Inputs`, `Button`, `Links` |
| **MasterDetailPanel** | `MasterPanel`, `MasterGrid`, `MasterList`, `DetailPanel`, `DetailGrid` |
| **RecordFormPanel** | `ShowActionButtons`, `FieldSpacing`, `LabelWidth`, `ContentPadding` |
| **WordProcessorPanel** | `Toolbar`, `ToolbarButton`, `Editor`, `StatusBar`, `FindBar` |
| **ConsolePanel** | `OutputArea`, `InputArea`, `PromptLabel`, `InputBox` |
| **WebBrowserPanel** | Uses flat props: `ShowNavigationBar`, `ShowStatusBar`, `HomeUrl` |

### DataGridPanel Visibility Properties

DataGridPanel supports additional boolean properties to show/hide individual elements:

**Toolbar visibility:**
- `ShowToolbar`, `ShowSearch`
- `ShowCaseSensitive`, `ShowExactMatch`, `ShowPageSizeControl`

**Pagination visibility:**
- `ShowPagination`, `ShowRecordInfo`, `ShowRecordNavigation`

**Action buttons (picker mode):**
- `ShowActionButtons` - Show OK/Cancel buttons at bottom
- Events: `OkClick`, `CancelClick`
- Properties: `selected_records`, `selected_indices`

See each component's README for detailed sub-property documentation.

---

## � Component Structure

> **IMPORTANT**: Each UI Element module follows a **Panel + Form pattern**:
> 
> - **Panel** (e.g., `ChatPanel`, `DataGridPanel`): Embeddable component that can be placed in any Form or Panel
> - **Form/UI** (e.g., `ChatUI`, `DataGridForm`): Standalone form that **uses the Panel internally**
>
> When using a Form/UI class, the Panel is created and managed automatically. You can access it via properties like `.chat_panel`, `.grid`, `.Editor`, etc.

| Module | Panel (Embeddable) | Form/UI (Standalone) | Access Property |
|--------|-------------------|---------------------|-----------------|
| Chat | `ChatPanel` | `ChatUI` | `.chat_panel` |
| Console | `ConsolePanel` | `ConsoleForm` | `.console` |
| Data Grid | `DataGridPanel` | `DataGridForm` | `.grid` |
| Login | `LoginPanel` | `LoginForm` | Direct methods |
| Master-Detail | `MasterDetailPanel` | `MasterDetailForm` | `.panel` |
| Record Form | `RecordFormPanel` | `RecordFormDialog` | `.panel` |
| Web Browser | `WebBrowserPanel` | `WebBrowserUI` | `.CurrentTab` |
| Word Processor | `WordProcessorPanel` | `WordProcessorForm` | `.Editor` |

---

## 📦 Available Components

| Component | Description | Backend Required |
|-----------|-------------|------------------|
| [Chat](#-chat) | Messenger-style chat interface | `ChatBackend` |
| [Console](#-console) | Terminal/console emulator | `ConsoleIOBackend` |
| [Data Grid](#-data-grid) | Tabular data with pagination | `DataGridBackend` |
| [DB Connection](#-db-connection) | Database connection manager | `StorageBackend` |
| [Email Client](#-email-client) | Complete email client | `EmailBackend` |
| [Login](#-login) | Authentication with password change | `LoginBackend` |
| [Master-Detail](#-master-detail) | Master-detail data relationship view | `MasterDetailBackend` |
| [Record Form](#-record-form) | Auto-generated record edit form | None (uses ColumnDefinition) |
| [Web Browser](#-web-browser) | Embedded web browser | None (uses tkinterweb) |
| [Word Processor](#-word-processor) | Rich text editor | None (local) |

---

## 💬 Chat

Messenger-style chat interface with modern features.

### Features
- Message bubbles with avatars and timestamps
- Typing indicators and read receipts
- Emoji picker and search
- Context menu (copy, reply, delete)
- Pluggable backend for AI/API integration

### Quick Start

```python
from winformpy import Form, Application
from winformpy.ui_elements.chat import ChatPanel, ChatManager, ChatBackend

# Create your backend (EXTERNAL - not part of WinFormPy)
class MyChatBackend(ChatBackend):
    def send_message(self, text, context=None):
        # Connect to your AI/chat service
        return "Response from service"

# Use with ChatPanel
backend = MyChatBackend()
manager = ChatManager(backend=backend)

form = Form({'Text': 'Chat', 'Width': 600, 'Height': 700})
form.ApplyLayout()
chat = ChatPanel(form, manager=manager)

Application.Run(form)
```

### Components
| Class | Type | Description |
|-------|------|-------------|
| `ChatUI` | Form | Complete chat window |
| `ChatPanel` | Panel | Embeddable chat component |
| `ChatManager` | Service | Message history and state |
| `ChatBackend` | ABC | Base class for backends |

📚 [Full Documentation](chat/README.md)

---

## 🖥️ Console

Terminal-style console with pluggable I/O layer.

### Features
- Command input with history (Up/Down arrows)
- Colored output (error, warning, success, info)
- Multiple themes (dark, light, matrix, powershell, etc.)
- Pluggable I/O backends

### Quick Start

```python
from winformpy import Form, Application, DockStyle
from winformpy.ui_elements.console import ConsolePanel, LocalConsoleIO

form = Form({'Text': 'Console', 'Width': 800, 'Height': 600})
form.ApplyLayout()

# Create I/O layer with commands
io = LocalConsoleIO()

@io.command('hello')
def hello_cmd(args):
    io.write_success("Hello, World!")

@io.command('echo')
def echo_cmd(args):
    io.write_line(args)

console = ConsolePanel(form, {'Dock': DockStyle.Fill})
console.set_io(io)
io.connect()

Application.Run(form)
```

### Components
| Class | Type | Description |
|-------|------|-------------|
| `ConsoleForm` | Form | Complete terminal window |
| `ConsolePanel` | Panel | Embeddable console |
| `LocalConsoleIO` | I/O | Local command handlers |
| `SubprocessConsoleIO` | I/O | Shell command execution |
| `CallbackConsoleIO` | I/O | Simple callback-based I/O |

📚 [Full Documentation](console/README.md)

---

## � Data Grid

Tabular data display with pagination, sorting, search, and selection.

### Features
- Sortable columns (click headers to toggle)
- Text search across searchable columns
- Pagination with configurable page sizes (10/20/50/100)
- Row selection (single and multi-select with Ctrl+Click)
- Automatic data formatting (currency, dates, percentages, etc.)
- External backend for any data source

### Quick Start

```python
from winformpy import Form, Application, DockStyle
from winformpy.ui_elements.data_grid import (
    DataGridPanel, DataGridManager, DataGridBackend,
    ColumnDefinition, DataRequest, DataResponse, PageInfo, DataType
)

# Create your backend (EXTERNAL - not part of WinFormPy)
class MyDatabaseBackend(DataGridBackend):
    def get_columns(self):
        return [
            ColumnDefinition("id", "ID", DataType.INTEGER, width=60),
            ColumnDefinition("name", "Name", DataType.STRING, width=200),
            ColumnDefinition("salary", "Salary", DataType.CURRENCY, width=100),
        ]
    
    def fetch_data(self, request):
        # Fetch from your database with pagination
        # Return DataResponse with records and PageInfo
        ...

# Use with DataGridPanel
backend = MyDatabaseBackend()
manager = DataGridManager(backend)

form = Form({'Text': 'Data Grid', 'Width': 1024, 'Height': 700})
form.ApplyLayout()

grid = DataGridPanel(form, props={'Dock': DockStyle.Fill}, manager=manager)
grid.RowDoubleClick = lambda s, e: edit_record(e['record'])

manager.refresh()  # Load initial data

Application.Run(form)
```

### Components
| Class | Type | Description |
|-------|------|-------------|
| `DataGridPanel` | Panel | Embeddable data grid component |
| `DataGridManager` | Manager | State and operations handler |
| `DataGridBackend` | ABC | Backend interface (implement this) |
| `ColumnDefinition` | Data | Column configuration |
| `DataType` | Enum | Data types (STRING, INTEGER, CURRENCY, etc.) |
| `SortOrder` | Enum | Sort directions |
| `DataRequest` | Data | Request parameters |
| `DataResponse` | Data | Response with records |
| `PageInfo` | Data | Pagination information |

### Column Visibility Methods
| Method | Description |
|--------|-------------|
| `hide_column(name)` | Hide column(s) - accepts str or list |
| `show_column(name)` | Show column(s) - accepts str or list |
| `get_visible_columns()` | Get list of visible column names |
| `get_hidden_columns()` | Get list of hidden column names |

📚 [Full Documentation](data_grid/README.md)

---

## �🗄️ DB Connection

Visual manager for database connection parameters.

### Features
- Support for SQL and NoSQL databases
- Connection testing
- Visual forms for configuration
- CRUD operations delegated to backend

### Quick Start

```python
from winformpy import Form, Application, DockStyle
from winformpy.ui_elements.db_connection import DBConnectionPanel, DBConnectionManager

# Your storage backend (EXTERNAL - not part of WinFormPy)
class MyStorageBackend:
    def save(self, name, data): ...
    def read(self, name): ...
    def read_all(self): ...
    def delete(self, name): ...
    def list_names(self): ...

backend = MyStorageBackend()
manager = DBConnectionManager(backend)

form = Form({'Text': 'Connections', 'Width': 800, 'Height': 600})
form.ApplyLayout()
panel = DBConnectionPanel(form, manager, {'Dock': DockStyle.Fill})

Application.Run(form)
```

### Components
| Class | Type | Description |
|-------|------|-------------|
| `DBConnectionUI` | Form | Standalone connection manager |
| `DBConnectionPanel` | Panel | Embeddable component |
| `DBConnectionManager` | Service | Validation and CRUD delegation |

📚 [Full Documentation](db_connection/README.md)

---

## 📧 Email Client

Complete email client with three-layer architecture.

### Features
- Folder tree, message list, reading pane
- Compose, reply, forward
- Message threading and search
- Background synchronization

### Quick Start

```python
from winformpy.ui_elements.email_client import EmailForm, EmailAccount, EmailBackend

# Your IMAP backend (EXTERNAL - not part of WinFormPy)
class MyIMAPBackend(EmailBackend):
    def connect(self):
        import imaplib
        self._imap = imaplib.IMAP4_SSL(...)
        return True
    
    def get_message_list(self, folder, start, limit):
        # Implementation
        pass

account = EmailAccount(
    email="user@example.com",
    incoming_server="imap.example.com",
    incoming_port=993
)

backend = MyIMAPBackend(account)
form = EmailForm()
form.Manager.primitives = backend
form.Connect()
form.Show()
```

### Components
| Class | Type | Description |
|-------|------|-------------|
| `EmailForm` | Form | Complete email client |
| `EmailPanel` | Panel | Embeddable email component |
| `EmailManager` | Service | Business logic and events |
| `EmailBackend` | Base | Override for IMAP/SMTP |

📚 [Full Documentation](email_client/README.md)

---

## 🔐 Login

Authentication component with login and password change functionality.

### Features
- Username/password login form
- Password change with strength indicator
- Password reset request
- Remember me option
- Modern, responsive design
- Pluggable authentication backend

### Quick Start

```python
from winformpy.ui_elements.login import LoginForm, LoginBackend, AuthResult, PasswordChangeResult

# Create your backend (EXTERNAL - not part of WinFormPy)
class MyAuthBackend(LoginBackend):
    def authenticate(self, username, password):
        if self._check_credentials(username, password):
            return AuthResult(success=True, username=username, display_name="User")
        return AuthResult(success=False, error="Invalid credentials")
    
    def change_password(self, username, old_password, new_password):
        if self._update_password(username, old_password, new_password):
            return PasswordChangeResult(success=True)
        return PasswordChangeResult(success=False, error="Failed to change password")

# Use with LoginForm
backend = MyAuthBackend()
login = LoginForm(backend=backend)

if login.ShowDialog():
    user = login.authenticated_user
    print(f"Welcome, {user.display_name}!")
```

### Components
| Class | Type | Description |
|-------|------|-------------|
| `LoginForm` | Form | Standalone login dialog |
| `LoginPanel` | Panel | Embeddable login component |
| `ChangePasswordForm` | Form | Password change dialog |
| `LoginManager` | Service | State and event management |
| `LoginBackend` | ABC | Base class for backends |

📚 [Full Documentation](login/README.md)

---

## 🔗 Master-Detail

Master-detail view with automatic detail refresh on master selection.

### Features
- Dual master view types: DataGrid or ListView
- Full detail DataGrid with search, sort, pagination
- Automatic refresh when master selection changes
- Horizontal or vertical layout
- Sub-properties for styling internal elements

### Quick Start

```python
from winformpy import Form, Application, DockStyle
from winformpy.ui_elements.master_detail import (
    MasterDetailForm, MasterDetailBackend, MasterType
)
from winformpy.ui_elements.data_grid import ColumnDefinition, DataType, DataRequest, DataResponse, PageInfo

# Create your backend (EXTERNAL - not part of WinFormPy)
class CustomerOrdersBackend(MasterDetailBackend):
    def get_master_type(self):
        return MasterType.DATA_GRID
    
    def get_master_columns(self):
        return [
            ColumnDefinition('id', 'ID', DataType.INTEGER, width=60),
            ColumnDefinition('name', 'Customer', DataType.STRING, width=200),
        ]
    
    def fetch_master_data(self, request):
        # Fetch customers from your database
        return DataResponse(records=[...], page_info=PageInfo(...))
    
    def get_detail_columns(self):
        return [
            ColumnDefinition('order_id', 'Order #', DataType.INTEGER, width=80),
            ColumnDefinition('total', 'Total', DataType.CURRENCY, width=100),
        ]
    
    def fetch_detail_data(self, master_id, request):
        # Fetch orders for the selected customer
        return DataResponse(records=[...], page_info=PageInfo(...))

# Use with MasterDetailForm
backend = CustomerOrdersBackend()
form = MasterDetailForm(
    backend,
    title="Customer Orders",
    orientation='horizontal',
    master_size=350
)
form.DetailRowDoubleClick = lambda s, e: edit_order(e['record'])
form.Show()
```

### Components
| Class | Type | Description |
|-------|------|-------------|
| `MasterDetailForm` | Form | Standalone master-detail window |
| `MasterDetailPanel` | Panel | Embeddable master-detail component |
| `MasterDetailManager` | Service | State and data flow management |
| `MasterDetailBackend` | ABC | Base class for backends |

### Demo Backends
| Backend | Description |
|---------|-------------|
| `DemoMasterDetailBackend` | Customer → Orders (DataGrid master) |
| `DemoListViewBackend` | Category → Products (ListView master) |

📚 [Full Documentation](master_detail/README.md)

---

## 📝 Record Form

Auto-generated forms for viewing and editing individual records.

### Features
- Auto-generates input fields from ColumnDefinition metadata
- Supports multiple data types (String, Integer, Currency, Boolean, Date, etc.)
- Read-only and edit modes
- Built-in Save/Cancel action buttons (optional)
- Value change events for real-time validation
- Responsive layout that adjusts to container size
- Dynamic field visibility (show/hide fields at runtime)

### Quick Start

```python
from winformpy import Form, Application, DockStyle, DialogResult
from winformpy.ui_elements.record_form import RecordFormPanel, RecordFormDialog
from winformpy.ui_elements.data_grid import ColumnDefinition, DataType

# Define columns (reuse from DataGrid if available)
columns = [
    ColumnDefinition("name", "Name", DataType.STRING),
    ColumnDefinition("email", "Email", DataType.STRING),
    ColumnDefinition("salary", "Salary", DataType.CURRENCY),
    ColumnDefinition("active", "Active", DataType.BOOLEAN),
]

# Sample record
record = {
    "name": "John Doe",
    "email": "john@example.com",
    "salary": 75000.00,
    "active": True
}

# Option 1: Use RecordFormDialog (standalone dialog)
form = RecordFormDialog(columns, record, title="Edit Employee")
if form.ShowDialog() == DialogResult.OK:
    updated = form.get_values()
    save_to_database(updated)

# Option 2: Use RecordFormPanel (embeddable)
form = Form({'Text': 'Employee Details', 'Width': 500, 'Height': 400})
form.ApplyLayout()

panel = RecordFormPanel(form, props={
    'Dock': DockStyle.Fill,
    'Columns': columns,
    'Record': record,
    'ShowActionButtons': True
})
panel.SaveClick = lambda s, e: save_record(e['values'])

Application.Run(form)
```

### Components
| Class | Type | Description |
|-------|------|-------------|
| `RecordFormDialog` | Form | Standalone edit/view dialog |
| `RecordFormPanel` | Panel | Embeddable record editor |

### Properties
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Columns` | List | [] | Column definitions for fields |
| `Record` | Dict | {} | Current record data |
| `ReadOnly` | bool | False | Read-only mode |
| `ShowActionButtons` | bool | False | Show Save/Cancel buttons |
| `FieldSpacing` | int | 40 | Vertical spacing between fields |
| `LabelWidth` | int | 150 | Width of field labels |

### Events
| Event | Args | Description |
|-------|------|-------------|
| `SaveClick` | `{'values': dict}` | Fired when Save clicked |
| `CancelClick` | `{}` | Fired when Cancel clicked |
| `ValueChanged` | `{'field': str, 'values': dict}` | Fired when any field changes |

### Methods
| Method | Description |
|--------|-------------|
| `get_values()` | Get all field values as dictionary |
| `set_values(record)` | Set all field values from dictionary |
| `hide_field(name)` | Hide field(s) - accepts str or list |
| `show_field(name)` | Show field(s) - accepts str or list |
| `get_visible_fields()` | Get list of visible field names |
| `get_hidden_fields()` | Get list of hidden field names |

📚 [Full Documentation](record_form/README.md)

---

## 🌐 Web Browser

Embedded web browser using tkinterweb.

### Features
- Navigation controls (back, forward, refresh, home)
- Address bar with URL entry
- Bookmark management
- Tab support (optional)

### Quick Start

```python
from winformpy import Form, Application, DockStyle
from winformpy.ui_elements.web_browser import WebBrowserPanel

form = Form({'Text': 'Browser', 'Width': 1024, 'Height': 768})
form.ApplyLayout()

browser = WebBrowserPanel(form, {'Dock': DockStyle.Fill})
browser.Navigate("https://www.python.org")

Application.Run(form)
```

### Components
| Class | Type | Description |
|-------|------|-------------|
| `WebBrowserPanel` | Panel | Embeddable browser |

📚 [Full Documentation](web_browser/README.md)

---

## 📝 Word Processor

Rich text editor with formatting toolbar.

### Features
- Bold, italic, underline formatting
- Font family and size selection
- Text alignment
- Find and replace
- File operations (new, open, save)

### Quick Start

```python
from winformpy import Form, Application, DockStyle
from winformpy.ui_elements.word_processor import WordProcessorPanel

form = Form({'Text': 'Editor', 'Width': 900, 'Height': 700})
form.ApplyLayout()

editor = WordProcessorPanel(form, {'Dock': DockStyle.Fill})

Application.Run(form)
```

### Components
| Class | Type | Description |
|-------|------|-------------|
| `WordProcessorPanel` | Panel | Embeddable rich text editor |

📚 [Full Documentation](word_processor/README.md)

---

## 🔧 Creating Custom Backends

### Chat Backend Example

```python
from winformpy.ui_elements.chat import ChatBackend

class OpenAIChatBackend(ChatBackend):
    def __init__(self, api_key):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
    
    def send_message(self, text, context=None):
        messages = [{"role": "user", "content": text}]
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        return response.choices[0].message.content
```

### Email Backend Example

```python
from winformpy.ui_elements.email_client import EmailBackend

class IMAPBackend(EmailBackend):
    def connect(self):
        import imaplib
        self._imap = imaplib.IMAP4_SSL(
            self._account.incoming_server,
            self._account.incoming_port
        )
        self._imap.login(
            self._account.incoming_username,
            self._account.incoming_password
        )
        self._connected = True
        return True
```

### Login Backend Example

```python
from winformpy.ui_elements.login import LoginBackend, AuthResult, PasswordChangeResult

class DatabaseLoginBackend(LoginBackend):
    def __init__(self, db):
        self.db = db
    
    def authenticate(self, username, password):
        user = self.db.get_user(username)
        if user and verify_hash(password, user.password_hash):
            return AuthResult(
                success=True,
                user_id=str(user.id),
                username=user.username,
                display_name=user.full_name
            )
        return AuthResult(success=False, error="Invalid credentials")
    
    def change_password(self, username, old_password, new_password):
        auth = self.authenticate(username, old_password)
        if not auth.success:
            return PasswordChangeResult(success=False, error="Current password is incorrect")
        
        self.db.update_password(username, hash_password(new_password))
        return PasswordChangeResult(success=True)
```

### Storage Backend Example

```python
import json

class JSONStorageBackend:
    def __init__(self, filepath):
        self.filepath = filepath
    
    def save(self, name, data):
        all_data = self.read_all()
        existed = name in all_data
        all_data[name] = data
        with open(self.filepath, 'w') as f:
            json.dump(all_data, f)
        return 'updated' if existed else 'created'
    
    def read(self, name):
        return self.read_all().get(name)
    
    def read_all(self):
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def delete(self, name):
        all_data = self.read_all()
        if name in all_data:
            del all_data[name]
            with open(self.filepath, 'w') as f:
                json.dump(all_data, f)
            return True
        return False
    
    def list_names(self):
        return list(self.read_all().keys())
```

---

## 📁 Directory Structure

```
ui_elements/
├── README.md              ← You are here
├── __init__.py
├── chat/
│   ├── __init__.py
│   ├── chat_manager.py    # ChatManager, ChatBackend
│   ├── chat_panel.py      # ChatPanel
│   ├── chat_ui.py         # ChatUI/ChatForm
│   └── README.md
├── console/
│   ├── __init__.py
│   ├── console_io.py      # I/O layer classes
│   ├── console_panel.py   # ConsolePanel
│   ├── console_ui.py      # ConsoleForm
│   └── README.md
├── data_grid/
│   ├── __init__.py
│   ├── data_grid_backend.py  # DataGridBackend, ColumnDefinition, etc.
│   ├── data_grid_manager.py  # DataGridManager
│   ├── data_grid_panel.py    # DataGridPanel
│   ├── data_grid_ui.py       # DataGridForm, DataGridPickerForm
│   └── README.md
├── db_connection/
│   ├── __init__.py
│   ├── db_connection_manager.py
│   ├── db_connection_panel.py
│   ├── db_connection_ui.py
│   └── README.md
├── email_client/
│   ├── __init__.py
│   ├── email_backend.py
│   ├── email_manager.py
│   ├── email_panel.py
│   ├── email_ui.py
│   └── README.md
├── login/
│   ├── __init__.py
│   ├── login_backend.py   # LoginBackend, AuthResult, etc.
│   ├── login_manager.py   # LoginManager
│   ├── login_panel.py     # LoginPanel
│   ├── login_ui.py        # LoginForm, ChangePasswordForm
│   └── README.md
├── record_form/
│   ├── __init__.py
│   ├── record_form_panel.py  # RecordFormPanel
│   ├── record_form_ui.py     # RecordFormDialog
│   └── README.md
├── web_browser/
│   ├── __init__.py
│   ├── web_browser_panel.py
│   ├── web_browser_ui.py
│   └── README.md
└── word_processor/
    ├── __init__.py
    ├── word_processor_panel.py
    ├── word_processor_primitives.py
    ├── word_processor_ui.py
    └── README.md
```

---

## 🔗 Related Documentation

- [WinFormPy Main Documentation](../../README.md)
- [Dock & Anchor Guide](../../guides/README_Dock_Anchor.md)
- [Container Best Practices](../../guides/README_Container_Best_Practice.md)
