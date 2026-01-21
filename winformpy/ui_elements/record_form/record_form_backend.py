"""
Record Form Backend - Abstract base class for record form backends.

This module defines the contract that all record form backends must implement.
The backend is responsible for CRUD operations on individual records.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable
from enum import Enum


class RecordFormMode(Enum):
    """Mode of the record form."""
    VIEW = "view"           # Read-only viewing
    EDIT = "edit"           # Editing existing record
    INSERT = "insert"       # Creating new record


@dataclass
class RecordResponse:
    """Response from a backend operation."""
    success: bool = True
    record: Dict[str, Any] = field(default_factory=dict)
    error_message: str = ""
    validation_errors: Dict[str, str] = field(default_factory=dict)


@dataclass
class ValidationResult:
    """Result of field validation."""
    is_valid: bool = True
    errors: Dict[str, str] = field(default_factory=dict)  # field_name -> error_message


class RecordFormBackend(ABC):
    """
    Abstract base class for RecordFormPanel backends.
    
    Implement this class to connect the RecordFormPanel to any data source:
    - SQL databases (SQLite, PostgreSQL, MySQL, etc.)
    - REST APIs
    - In-memory collections
    - File-based storage
    
    Example:
        class SQLiteRecordBackend(RecordFormBackend):
            def __init__(self, connection, table_name):
                self.conn = connection
                self.table = table_name
            
            def insert(self, record: Dict[str, Any]) -> RecordResponse:
                # Execute INSERT SQL
                ...
            
            def update(self, record: Dict[str, Any]) -> RecordResponse:
                # Execute UPDATE SQL
                ...
            
            def delete(self, record: Dict[str, Any]) -> RecordResponse:
                # Execute DELETE SQL
                ...
    """
    
    def __init__(self):
        """Initialize the backend."""
        # Callbacks for UI notification
        self.on_insert_complete: Callable[[RecordResponse], None] = lambda r: None
        self.on_update_complete: Callable[[RecordResponse], None] = lambda r: None
        self.on_delete_complete: Callable[[RecordResponse], None] = lambda r: None
        self.on_validation_error: Callable[[ValidationResult], None] = lambda r: None
    
    @abstractmethod
    def insert(self, record: Dict[str, Any]) -> RecordResponse:
        """
        Insert a new record.
        
        Args:
            record: Dictionary with field names and values.
            
        Returns:
            RecordResponse with success status and the inserted record (with generated IDs).
        """
        pass
    
    @abstractmethod
    def update(self, record: Dict[str, Any]) -> RecordResponse:
        """
        Update an existing record.
        
        Args:
            record: Dictionary with field names and values (must include primary key).
            
        Returns:
            RecordResponse with success status and the updated record.
        """
        pass
    
    @abstractmethod
    def delete(self, record: Dict[str, Any]) -> RecordResponse:
        """
        Delete an existing record.
        
        Args:
            record: Dictionary with field names and values (must include primary key).
            
        Returns:
            RecordResponse with success status.
        """
        pass
    
    def validate(self, record: Dict[str, Any], mode: RecordFormMode = RecordFormMode.EDIT) -> ValidationResult:
        """
        Validate a record before insert/update.
        
        Override this to implement custom validation logic.
        
        Args:
            record: Dictionary with field names and values.
            mode: The current form mode (insert/edit).
            
        Returns:
            ValidationResult indicating if the record is valid.
        """
        return ValidationResult(is_valid=True, errors={})
    
    def get_default_values(self) -> Dict[str, Any]:
        """
        Get default values for a new record.
        
        Override this to provide initial values for insert mode.
        
        Returns:
            Dictionary with default field values.
        """
        return {}
    
    def get_primary_key_field(self) -> str:
        """
        Get the name of the primary key field.
        
        Override this if your records use a different primary key field.
        
        Returns:
            Name of the primary key field (default: 'id').
        """
        return 'id'
    
    def before_insert(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hook called before insert operation.
        
        Override this to modify the record before insertion.
        
        Args:
            record: The record to be inserted.
            
        Returns:
            Modified record.
        """
        return record
    
    def before_update(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hook called before update operation.
        
        Override this to modify the record before update.
        
        Args:
            record: The record to be updated.
            
        Returns:
            Modified record.
        """
        return record
    
    def before_delete(self, record: Dict[str, Any]) -> bool:
        """
        Hook called before delete operation.
        
        Override this to add confirmation or validation before delete.
        
        Args:
            record: The record to be deleted.
            
        Returns:
            True to proceed with delete, False to cancel.
        """
        return True


class InMemoryRecordBackend(RecordFormBackend):
    """
    Simple in-memory backend for testing and demos.
    
    Stores records in a list and provides basic CRUD operations.
    
    Example:
        backend = InMemoryRecordBackend()
        backend.set_records([
            {'id': 1, 'name': 'John', 'email': 'john@example.com'},
            {'id': 2, 'name': 'Jane', 'email': 'jane@example.com'}
        ])
        
        panel = RecordFormPanel(form, props={
            'Backend': backend,
            'ShowInsertButton': True,
            'ShowUpdateButton': True,
            'ShowDeleteButton': True
        })
    """
    
    def __init__(self, records: List[Dict[str, Any]] = None, primary_key: str = 'id'):
        """
        Initialize the in-memory backend.
        
        Args:
            records: Optional initial list of records.
            primary_key: Name of the primary key field.
        """
        super().__init__()
        self._records: List[Dict[str, Any]] = records or []
        self._primary_key = primary_key
        self._next_id = 1
        
        # Calculate next ID
        if self._records:
            max_id = max((r.get(self._primary_key, 0) for r in self._records), default=0)
            if isinstance(max_id, int):
                self._next_id = max_id + 1
    
    def set_records(self, records: List[Dict[str, Any]]):
        """Set the records list."""
        self._records = records
        if self._records:
            max_id = max((r.get(self._primary_key, 0) for r in self._records), default=0)
            if isinstance(max_id, int):
                self._next_id = max_id + 1
    
    def get_records(self) -> List[Dict[str, Any]]:
        """Get all records."""
        return self._records.copy()
    
    def get_primary_key_field(self) -> str:
        return self._primary_key
    
    def insert(self, record: Dict[str, Any]) -> RecordResponse:
        """Insert a new record."""
        try:
            # Apply before hook
            record = self.before_insert(record)
            
            # Validate
            validation = self.validate(record, RecordFormMode.INSERT)
            if not validation.is_valid:
                self.on_validation_error(validation)
                return RecordResponse(
                    success=False,
                    error_message="Validation failed",
                    validation_errors=validation.errors
                )
            
            # Generate ID if not provided
            new_record = record.copy()
            if self._primary_key not in new_record or not new_record[self._primary_key]:
                new_record[self._primary_key] = self._next_id
                self._next_id += 1
            
            self._records.append(new_record)
            
            response = RecordResponse(success=True, record=new_record)
            self.on_insert_complete(response)
            return response
            
        except Exception as e:
            return RecordResponse(success=False, error_message=str(e))
    
    def update(self, record: Dict[str, Any]) -> RecordResponse:
        """Update an existing record."""
        try:
            # Apply before hook
            record = self.before_update(record)
            
            # Validate
            validation = self.validate(record, RecordFormMode.EDIT)
            if not validation.is_valid:
                self.on_validation_error(validation)
                return RecordResponse(
                    success=False,
                    error_message="Validation failed",
                    validation_errors=validation.errors
                )
            
            # Find and update
            pk_value = record.get(self._primary_key)
            for i, r in enumerate(self._records):
                if r.get(self._primary_key) == pk_value:
                    self._records[i] = record.copy()
                    response = RecordResponse(success=True, record=self._records[i])
                    self.on_update_complete(response)
                    return response
            
            return RecordResponse(success=False, error_message=f"Record with {self._primary_key}={pk_value} not found")
            
        except Exception as e:
            return RecordResponse(success=False, error_message=str(e))
    
    def delete(self, record: Dict[str, Any]) -> RecordResponse:
        """Delete an existing record."""
        try:
            # Apply before hook
            if not self.before_delete(record):
                return RecordResponse(success=False, error_message="Delete cancelled")
            
            pk_value = record.get(self._primary_key)
            for i, r in enumerate(self._records):
                if r.get(self._primary_key) == pk_value:
                    deleted = self._records.pop(i)
                    response = RecordResponse(success=True, record=deleted)
                    self.on_delete_complete(response)
                    return response
            
            return RecordResponse(success=False, error_message=f"Record with {self._primary_key}={pk_value} not found")
            
        except Exception as e:
            return RecordResponse(success=False, error_message=str(e))
    
    def get_default_values(self) -> Dict[str, Any]:
        """Get default values for a new record."""
        return {self._primary_key: None}


def create_record_backend(backend_type: str = "memory", **kwargs) -> RecordFormBackend:
    """
    Factory function to create a record backend.
    
    Args:
        backend_type: Type of backend ("memory", or custom implementations).
        **kwargs: Backend-specific arguments.
        
    Returns:
        A RecordFormBackend instance.
    """
    if backend_type == "memory":
        return InMemoryRecordBackend(**kwargs)
    else:
        raise ValueError(f"Unknown backend type: {backend_type}")
