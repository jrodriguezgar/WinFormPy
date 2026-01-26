"""
RecordForm Demo - Shows different modes and use cases

This example demonstrates:
- Edit mode (modify existing records)
- View mode (read-only display)
- New record mode (empty form)
- Multiple records in sequence
"""

import sys
import os

# Add project root to path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

sys.path.insert(0, os.path.join(_project_root, 'winformpy', 'ui_elements', 'data_grid'))

from winformpy.winformpy import Application, DialogResult
from winformpy.ui_elements.record_form.record_form_ui import RecordFormDialog
from data_grid_backend import ColumnDefinition, DataType


def main():
    """Run RecordForm demos."""
    print("=" * 60)
    print("RecordFormDialog Demo")
    print("=" * 60)
    print("\nSelect demo:")
    print("  1. Edit mode (can modify values)")
    print("  2. View mode (read-only)")
    print("  3. New record (empty form)")
    print("  4. Multiple records in sequence")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    # Sample columns
    columns = [
        ColumnDefinition("id", "ID", DataType.INTEGER, width=60),
        ColumnDefinition("name", "Full Name", DataType.STRING, width=200),
        ColumnDefinition("email", "Email Address", DataType.STRING, width=250),
        ColumnDefinition("department", "Department", DataType.STRING, width=150),
        ColumnDefinition("salary", "Annual Salary", DataType.CURRENCY, width=120),
        ColumnDefinition("hire_date", "Hire Date", DataType.DATE, width=100),
        ColumnDefinition("active", "Active", DataType.BOOLEAN, width=70),
    ]
    
    # Sample records
    employees = [
        {"id": 1, "name": "Jane Smith", "email": "jane@company.com", "department": "Engineering", "salary": 95000.00, "hire_date": "2020-03-15", "active": True},
        {"id": 2, "name": "Bob Wilson", "email": "bob@company.com", "department": "Marketing", "salary": 75000.00, "hire_date": "2019-08-22", "active": True},
        {"id": 3, "name": "Alice Brown", "email": "alice@company.com", "department": "Sales", "salary": 65000.00, "hire_date": "2021-01-10", "active": False},
    ]
    
    if choice == "1":
        # Demo 1: Edit mode
        print("\n--- Edit Mode Demo ---")
        
        dialog = RecordFormDialog(
            columns=columns,
            record=employees[0],
            title="Edit Employee",
            readonly=False
        )
        
        result = dialog.ShowDialog()
        
        if result == DialogResult.OK:
            values = dialog.get_values()
            print("\nSaved values:")
            for key, value in values.items():
                print(f"  {key}: {value}")
        else:
            print("\nCancelled")
    
    elif choice == "2":
        # Demo 2: View mode
        print("\n--- View Mode Demo ---")
        
        dialog = RecordFormDialog(
            columns=columns,
            record=employees[0],
            title="Employee Details",
            readonly=True
        )
        
        dialog.ShowDialog()
        print("\nDialog closed")
    
    elif choice == "3":
        # Demo 3: New record (empty form)
        print("\n--- New Record Demo ---")
        
        dialog = RecordFormDialog(
            columns=columns,
            record={},  # Empty record
            title="New Employee",
            readonly=False
        )
        
        result = dialog.ShowDialog()
        
        if result == DialogResult.OK:
            values = dialog.get_values()
            print("\nNew record values:")
            for key, value in values.items():
                print(f"  {key}: {value}")
        else:
            print("\nCancelled - no record created")
    
    elif choice == "4":
        # Demo 4: Multiple records in sequence
        print("\n--- Multiple Records Demo ---")
        
        for i, emp in enumerate(employees):
            print(f"\nEditing employee {i+1} of {len(employees)}: {emp['name']}")
            
            dialog = RecordFormDialog(
                columns=columns,
                record=emp,
                title=f"Edit Employee ({i+1}/{len(employees)})",
                readonly=False
            )
            
            result = dialog.ShowDialog()
            
            if result == DialogResult.OK:
                values = dialog.get_values()
                print(f"  Saved: {values.get('name')} - ${values.get('salary'):,.2f}")
            else:
                print(f"  Skipped: {emp['name']}")
        
        print("\nAll employees processed")
    
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
