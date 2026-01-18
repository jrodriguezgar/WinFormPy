"""
Database Connection Management Module.

This module provides a layered architecture for managing database connections:

Architecture:
    ┌─────────────────────────────────────┐
    │  Visual Layer (same level)          │
    │  - DBConnectionUI (Form window)     │
    │  - DBConnectionPanel (Panel embed)  │
    └─────────────┬───────────────────────┘
                  │ uses
    ┌─────────────▼───────────────────────┐
    │  DBConnectionManager (Service)      │
    └─────────────┬───────────────────────┘
                  │ delegates to
    ┌─────────────▼───────────────────────┐
    │  Storage Backend (⚠️ EXTERNAL)      │
    │  NOT part of this project           │
    └─────────────────────────────────────┘

The storage backend must be provided externally and implement:

Required methods (CRUD for connection parameters file):
    - save(name, data) -> str ('created' | 'updated')
    - read(name) -> dict | None
    - read_all() -> dict
    - delete(name) -> bool
    - list_names() -> list[str]

Optional method (for connectivity testing):
    - test_connection(conn_data) -> tuple[bool, str]

Example:
    >>> from winformpy.ui_elements.db_connection import (
    ...     DBConnectionManager, DBConnectionUI
    ... )
    >>> 
    >>> # Backend provided externally
    >>> backend = MyExternalBackend()
    >>> manager = DBConnectionManager(backend)
    >>> 
    >>> # Option 1: Standalone Form window
    >>> ui = DBConnectionUI(manager)
    >>> ui.show_dialog()
    >>> 
    >>> # Option 2: Embeddable Panel
    >>> panel = DBConnectionPanel(parent_window, manager)
"""

from .db_connection_manager import DBConnectionManager
from .db_connection_ui import DBConnectionUI
from .db_connection_panel import DBConnectionPanel

__all__ = [
    'DBConnectionManager',
    'DBConnectionUI',
    'DBConnectionPanel'
]
