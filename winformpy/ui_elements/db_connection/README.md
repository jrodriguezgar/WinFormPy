# 📁 Database Connection Manager

## 📖 Overview

**Database Connection Manager** is a modular system for visual management of database connections (SQL and NoSQL) in Windows applications. It provides a clean layered architecture that separates business logic from visual presentation.

### 🎯 Purpose

- **Centralized Management**: Manage multiple database connections in one place
- **Automatic Validation**: Validate configurations before saving
- **Visual Interface**: Graphical forms for connection management
- **Clean Architecture**: Well-defined separation of responsibilities

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│  Visual Layer (same level)                          │
│  - DBConnectionUI (Standalone Form window)          │
│  - DBConnectionPanel (Embeddable Panel)             │
│    → Receive DBConnectionManager as dependency      │
└─────────────────────┬───────────────────────────────┘
                      │ delegates operations
┌─────────────────────▼───────────────────────────────┐
│  Service Layer                                      │
│  - DBConnectionManager                              │
│    → Validates data and delegates CRUD to backend   │
│    → Receives Storage Backend as dependency         │
└─────────────────────┬───────────────────────────────┘
                      │ delegates CRUD
┌─────────────────────▼───────────────────────────────┐
│  ⚠️ EXTERNAL (not part of this project)             │
│  Storage Backend                                    │
│    → Must be provided externally                    │
│    → Manages connection parameters file             │
└─────────────────────────────────────────────────────┘
```

**⚠️ IMPORTANT**: The Storage Backend is **NOT part of this project**. It must be provided externally.

---

## 📋 Storage Backend Contract (External)

The external backend must implement CRUD methods for managing the connection parameters file:

```python
class StorageBackend:
    """Required interface for the Storage Backend (external)."""
  
    # === Required CRUD Methods ===
  
    def save(self, name: str, data: dict) -> str:
        """
        Save or update a connection.
      
        Returns:
            str: 'created' if new, 'updated' if already existed
        """
        pass
  
    def read(self, name: str) -> dict | None:
        """Read a specific connection. Returns dict or None if not found."""
        pass
  
    def read_all(self) -> dict:
        """Read all connections. Returns {name: config, ...}"""
        pass
  
    def delete(self, name: str) -> bool:
        """Delete a connection. Returns True if deleted."""
        pass
  
    def list_names(self) -> list[str]:
        """Get list of connection names."""
        pass
  
    # === OPTIONAL Method for Connectivity Testing ===
  
    def test_connection(self, conn_data: dict) -> tuple[bool, str]:
        """
        Test connectivity to a database.
      
        ⚠️ IMPORTANT: This method is OPTIONAL.
        If not implemented, DBConnectionManager will show
        'Connection test not available'.
      
        Args:
            conn_data: Dictionary with connection parameters
                       (type, host, port, database, user, password, schema)
      
        Returns:
            tuple[bool, str]: (success, descriptive message)
        """
        pass
```

### ⚠️ Note on Connectivity Testing

The **"Test Connection"** feature requires the backend to implement `test_connection()`. If not implemented:

- Manager returns: `(False, "Connection test not available. Backend does not implement test_connection().")`
- UI displays a message indicating the test is not available

**This is by design**: The backend is responsible for actual connectivity since only it knows the drivers and libraries needed for each database type.

---

## 🗂️ Project Components

| Component                     | Type             | Purpose                                     |
| ----------------------------- | ---------------- | ------------------------------------------- |
| **DBConnectionUI**      | Visual Form      | Standalone window for connection management |
| **DBConnectionPanel**   | Embeddable Panel | Visual component to integrate in other apps |
| **DBConnectionManager** | Service          | Validation and CRUD operation delegation    |

---

## 🚀 Quick Start

### Using Visual Interface (Form)

```python
from winformpy.ui_elements.db_connection import (
    DBConnectionManager,
    DBConnectionUI
)

# External backend (NOT part of this project)
backend = MyExternalBackend()

# Create layers
manager = DBConnectionManager(backend)
ui = DBConnectionUI(manager)

# Show visual interface
ui.show_dialog()
```

### Embeddable Visual Panel

```python
from winformpy.winformpy import Form, DockStyle
from winformpy.ui_elements.db_connection import (
    DBConnectionManager,
    DBConnectionPanel
)

# Create main window
form = Form({'Text': "My App", 'Width': 900, 'Height': 700})
form.ApplyLayout()  # IMPORTANT: Call before adding child controls

# External backend (NOT part of this project)
backend = MyExternalBackend()

# Create layers
manager = DBConnectionManager(backend)
panel = DBConnectionPanel(form, manager, {'Dock': DockStyle.Fill})

form.Run()
```

### Included Demo

```bash
# DBConnectionUI demo (Standalone Form)
python -m winformpy.ui_elements.db_connection.db_connection_ui

# DBConnectionPanel demo (Embeddable Panel)
python -m winformpy.ui_elements.db_connection.db_connection_panel
```

Demos include a sample backend for demonstration purposes.

---

## 📚 Backend Example (External)

This example shows how to implement a complete backend that:

- Stores connections in a JSON file
- Implements connectivity testing for SQLite and PostgreSQL

```python
import json
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple


class JSONStorageBackend:
    """
    Backend that stores connections in a JSON file.
    Includes connectivity testing for SQLite and PostgreSQL.
    """
  
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._ensure_file_exists()
  
    def _ensure_file_exists(self):
        if not self.file_path.exists():
            self.file_path.write_text("{}", encoding='utf-8')
  
    def _read_all_raw(self) -> Dict[str, Any]:
        return json.loads(self.file_path.read_text(encoding='utf-8'))
  
    def _write_all_raw(self, data: Dict[str, Any]):
        self.file_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
  
    # === Required CRUD Methods ===
  
    def save(self, name: str, data: Dict[str, Any]) -> str:
        all_data = self._read_all_raw()
        action = 'updated' if name in all_data else 'created'
        all_data[name] = data
        self._write_all_raw(all_data)
        return action
  
    def read(self, name: str) -> Optional[Dict[str, Any]]:
        return self._read_all_raw().get(name)
  
    def read_all(self) -> Dict[str, Any]:
        return self._read_all_raw()
  
    def delete(self, name: str) -> bool:
        all_data = self._read_all_raw()
        if name not in all_data:
            return False
        del all_data[name]
        self._write_all_raw(all_data)
        return True
  
    def list_names(self) -> List[str]:
        return list(self._read_all_raw().keys())
  
    # === OPTIONAL: Connectivity Testing ===
  
    def test_connection(self, conn_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Test real connectivity to SQLite and PostgreSQL.
        This method is OPTIONAL.
        """
        db_type = conn_data.get('type', '').lower()
      
        if db_type == 'sqlite':
            return self._test_sqlite(conn_data)
        elif db_type == 'postgresql':
            return self._test_postgresql(conn_data)
        else:
            return False, f"Test not implemented for '{db_type}'."
  
    def _test_sqlite(self, conn_data: dict) -> Tuple[bool, str]:
        """SQLite connectivity test."""
        database = conn_data.get('database', '')
      
        if not database:
            return False, "SQLite: Database path required."
      
        try:
            conn = sqlite3.connect(database)
            cursor = conn.cursor()
            cursor.execute("SELECT sqlite_version();")
            version = cursor.fetchone()[0]
            conn.close()
            return True, f"SQLite {version}: Connected to '{database}'."
        except sqlite3.Error as e:
            return False, f"SQLite error: {e}"
        except Exception as e:
            return False, f"Error: {e}"
  
    def _test_postgresql(self, conn_data: dict) -> Tuple[bool, str]:
        """PostgreSQL connectivity test."""
        try:
            import psycopg2
        except ImportError:
            return False, "PostgreSQL: Install 'psycopg2' (pip install psycopg2-binary)."
      
        host = conn_data.get('host', 'localhost')
        port = conn_data.get('port', '5432')
        database = conn_data.get('database', '')
        user = conn_data.get('user', '')
        password = conn_data.get('password', '')
      
        if not all([host, database, user]):
            return False, "PostgreSQL: host, database and user are required."
      
        try:
            conn = psycopg2.connect(
                host=host,
                port=int(port),
                dbname=database,
                user=user,
                password=password,
                connect_timeout=5
            )
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0].split(',')[0]
            conn.close()
            return True, f"{version}: Connected to {host}:{port}/{database}."
        except psycopg2.Error as e:
            return False, f"PostgreSQL error: {e}"
        except Exception as e:
            return False, f"Error: {e}"


# === Usage ===
from winformpy.ui_elements.db_connection import (
    DBConnectionManager,
    DBConnectionUI
)

backend = JSONStorageBackend("connections.json")
manager = DBConnectionManager(backend)
ui = DBConnectionUI(manager)
ui.show_dialog()
```

---

## 🔌 Supported Databases

**SQL**: Oracle, MySQL, PostgreSQL, SQL Server, SQLite, MS Access
**NoSQL**: MongoDB, Cassandra, Neo4j, Elasticsearch, Redis

### Default Ports

| Type | Port | Required Fields |
|------|------|-----------------|
| `oracle` | 1521 | host, service_name, user, password |
| `mysql` | 3306 | host, database, user, password |
| `postgresql` | 5432 | host, database, user, password, schema |
| `sqlserver` | 1433 | host, database, user, password |
| `sqlite` | N/A | database (file path) |
| `access` | N/A | database (file path) |
| `mongodb` | 27017 | host, database |
| `cassandra` | 9042 | host, keyspace |
| `neo4j` | 7687 | host, database, user, password |
| `elasticsearch` | 9200 | host |
| `redis` | 6379 | host |

---

## 📋 API Reference

### DBConnectionManager

Service layer that validates data and delegates CRUD to backend.

```python
from winformpy.ui_elements.db_connection import DBConnectionManager

manager = DBConnectionManager(backend)
```

| Method | Parameters | Description | Returns |
|--------|------------|-------------|---------|
| `save()` | `name: str, data: dict` | Save/update connection | `'created'` or `'updated'` |
| `read()` | `name: str` | Read a connection | `dict` or `None` |
| `read_all()` | — | Read all connections | `dict` |
| `delete()` | `name: str` | Delete a connection | `bool` |
| `list_names()` | — | List connection names | `list[str]` |
| `test_connection()` | `name: str = None, data: dict = None` | Test connectivity | `tuple[bool, str]` |
| `validate_connection_data()` | `data: dict` | Validate connection structure | `tuple[bool, str]` |

### DBConnectionUI

Standalone Form window for visual connection management.

```python
from winformpy.ui_elements.db_connection import DBConnectionUI

ui = DBConnectionUI(manager)
ui.show_dialog()
```

### DBConnectionPanel

Embeddable panel for integration in other windows.

```python
from winformpy.ui_elements.db_connection import DBConnectionPanel

panel = DBConnectionPanel(parent, manager, props)
config = panel.get_config()  # Get selected connection
```

---

## 📁 Module Files

| File | Description |
|------|-------------|
| `__init__.py` | Module exports |
| `db_connection_manager.py` | DBConnectionManager service layer |
| `db_connection_panel.py` | DBConnectionPanel embeddable component |
| `db_connection_ui.py` | DBConnectionUI standalone form |

---

## ✅ Architecture Benefits

- **External and flexible backend**: Implement only what you need
- **Optional connectivity testing**: Don't need it? Don't implement it
- **Unchanged UI code**: `DBConnectionUI` and `DBConnectionPanel` work the same with any backend
- **Isolated business logic**: `DBConnectionManager` only validates and delegates
