"""
Module: db_connection_manager.py
Description: Service layer for database connection parameter management.
Manages connection configurations by delegating storage operations to a backend.
The backend must implement the same CRUD interface as this manager.
"""

from typing import Dict, List, Optional, Any, Tuple


class DBConnectionManager:
    """
    Service layer for database connection management.
    
    This class provides CRUD operations for connection parameters and delegates
    actual storage to a backend. The backend must implement the same methods:
    save(), read(), read_all(), delete(), list_names().
    
    Responsibilities:
    - Validation of connection parameters
    - Testing database connectivity
    - Delegating storage operations to the backend
    """
    
    # SQL Databases
    SUPPORTED_DB_TYPES = [
        'oracle', 'mysql', 'postgresql', 'sqlite', 'sqlserver', 'access',
        # NoSQL Databases
        'mongodb', 'cassandra', 'neo4j', 'elasticsearch', 'redis'
    ]
    
    def __init__(self, storage_backend, global_manager=None):
        """
        Initializes the connection manager.
        
        Args:
            storage_backend: Backend implementing CRUD methods:
                           - save(name, data) -> str
                           - read(name) -> dict | None
                           - read_all() -> dict
                           - delete(name) -> bool
                           - list_names() -> list
            global_manager: Optional instance of ConnectionManager for shared connections.
        """
        self.backend = storage_backend
        self.global_manager = global_manager
    
    # ===== CRUD OPERATIONS (delegated to backend) =====
    
    def save(self, name: str, connection_data: Dict[str, Any]) -> str:
        """
        Saves or updates a connection.
        Validates data before delegating to backend.
        
        Args:
            name: Connection name (cannot be empty or start with 'GLOBAL:')
            connection_data: Dictionary with connection parameters
            
        Returns:
            str: 'created' or 'updated'
            
        Raises:
            ValueError: If validation fails
        """
        if name and name.startswith("GLOBAL:"):
            raise ValueError("Directly saving changes to global connections is not allowed.")

        if not name or not name.strip():
            raise ValueError("Connection name cannot be empty.")
        
        if 'type' not in connection_data:
            raise ValueError("Database type is mandatory.")
        
        conn_type = connection_data['type'].lower()
        if conn_type not in self.SUPPORTED_DB_TYPES:
            raise ValueError(f"Unsupported database type: {conn_type}")
        
        # Validate connection data structure
        is_valid, error_msg = self.validate_connection_data(connection_data)
        if not is_valid:
            raise ValueError(f"Invalid connection data: {error_msg}")
        
        # Delegate to backend
        return self.backend.save(name, connection_data)
    
    def read(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Reads a specific connection.
        Supports 'GLOBAL:' prefix for library-managed connections.
        
        Args:
            name: Connection name
            
        Returns:
            dict with connection parameters, or None if not found
        """
        if name.startswith("GLOBAL:") and self.global_manager:
            real_name = name[7:]
            config = self.global_manager.get_connection(real_name)
            if config:
                # Map library CFG fields to UI expected fields
                return {
                    'type': config.get('db_type', 'oracle').lower(),
                    'host': config.get('host', 'localhost'),
                    'port': config.get('port', ''),
                    'database': config.get('database', ''),
                    'service_name': config.get('database', config.get('service_name', '')),
                    'user': config.get('user', ''),
                    'password': config.get('pwd', ''),
                    'schema': config.get('schema', ''),
                    'is_global': True
                }
        
        # Delegate to backend
        return self.backend.read(name)
    
    def read_all(self) -> Dict[str, Any]:
        """
        Reads all local connections.
        
        Returns:
            dict: All connections {name: config}
        """
        return self.backend.read_all()
    
    def delete(self, name: str) -> bool:
        """
        Deletes a local connection.
        Global connections are read-only.
        
        Args:
            name: Connection name to delete
            
        Returns:
            bool: True if deleted, False otherwise
        """
        if name.startswith("GLOBAL:"):
            return False
        
        return self.backend.delete(name)
    
    def exists(self, name: str) -> bool:
        """
        Checks if a local or global connection exists.
        
        Args:
            name: Connection name to check
            
        Returns:
            bool: True if exists
        """
        if name.startswith("GLOBAL:"):
            return self.read(name) is not None
        
        return name in self.backend.list_names()
    
    def list_names(self) -> List[str]:
        """
        Gets the list of all connection names.
        Includes both local and global connections.
        
        Returns:
            list: Connection names
        """
        names = self.backend.list_names()
        
        if self.global_manager:
            # Aggregate names from connector library
            for name, conn in self.global_manager._connections.items():
                if conn.get('connector') == 'db' or 'db_type' in conn:
                    global_name = f"GLOBAL:{conn.get('name', name)}"
                    if global_name not in names:
                        names.append(global_name)
        return names
    
    def test_connection(self, name: str = None, connection_data: Dict[str, Any] = None) -> Tuple[bool, str]:
        """
        Tests the database connection.
        
        Delegates to backend.test_connection() if the backend implements it.
        Otherwise returns an error indicating test is not available.
        
        Args:
            name: Connection name to test (reads config from backend)
            connection_data: Direct connection config to test
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        # Resolve connection data
        if name and name.startswith("GLOBAL:"):
            connection_data = self.read(name)
            name = None

        if name:
            conn_data = self.read(name)
            if not conn_data:
                return False, f"Connection '{name}' not found."
        elif connection_data:
            conn_data = connection_data
        else:
            raise ValueError("Must provide 'name' or 'connection_data'.")
        
        # Validation
        is_valid, error_msg = self.validate_connection_data(conn_data)
        if not is_valid:
            return False, f"Invalid data: {error_msg}"
        
        # Delegate to backend if it implements test_connection
        if hasattr(self.backend, 'test_connection') and callable(self.backend.test_connection):
            try:
                return self.backend.test_connection(conn_data)
            except Exception as e:
                return False, f"Connection test failed: {str(e)}"
        
        # Backend does not implement test_connection
        return False, "Connection test not available. Backend does not implement test_connection()."

    # Note: Connection testing is delegated to the backend.
    # The backend must implement test_connection(conn_data) -> Tuple[bool, str]
    # if connectivity testing is required.
    
    def validate_connection_data(self, connection_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validates connection data structure.
        
        Args:
            connection_data: Data to validate.
            
        Returns:
            Tuple (is_valid, error_message)
        """
        if 'type' not in connection_data:
            return False, "Missing 'type' field"
        
        db_type = connection_data['type'].lower()
        
        if db_type not in self.SUPPORTED_DB_TYPES:
            return False, f"Unsupported type: '{db_type}'"
        
        # Validation by type
        # SQL Databases
        if db_type == 'oracle':
            if not connection_data.get('host'):
                return False, "Oracle requires 'host'."
            if not connection_data.get('service_name') and not connection_data.get('database'):
                return False, "Oracle requires 'service_name' or 'database' (SID)."
        
        elif db_type in ['mysql', 'postgresql', 'sqlserver']:
            if not connection_data.get('host'):
                return False, f"{db_type} requires 'host'."
            if not connection_data.get('database'):
                return False, f"{db_type} requires 'database' name."
        
        elif db_type in ['sqlite', 'access']:
            if not connection_data.get('database'):
                return False, f"{db_type} requires 'database' path."
        
        # NoSQL Databases
        elif db_type == 'mongodb':
            if not connection_data.get('host'):
                return False, "MongoDB requires 'host'."
            if not connection_data.get('database'):
                return False, "MongoDB requires 'database' name."
        
        elif db_type == 'cassandra':
            if not connection_data.get('host'):
                return False, "Cassandra requires 'host'."
            if not connection_data.get('keyspace'):
                return False, "Cassandra requires 'keyspace'."
        
        elif db_type == 'neo4j':
            if not connection_data.get('host'):
                return False, "Neo4j requires 'host'."
            if not connection_data.get('database'):
                return False, "Neo4j requires 'database' name."
        
        elif db_type == 'elasticsearch':
            if not connection_data.get('host'):
                return False, "Elasticsearch requires 'host'."
        
        elif db_type == 'redis':
            if not connection_data.get('host'):
                return False, "Redis requires 'host'."
        
        return True, ""

