"""
Master-Detail Demo - Shows different layout configurations

This example demonstrates:
- Customer Orders (DataGrid master, vertical layout)
- Category Products (ListView master, horizontal layout)
- Customer Orders (DataGrid master, horizontal layout)
"""

import sys
import os

# Add project root to path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy.winformpy import Form, DockStyle, Application
from winformpy.ui_elements.master_detail.master_detail_panel import MasterDetailPanel
from winformpy.ui_elements.master_detail.master_detail_manager import MasterDetailManager
from winformpy.ui_elements.master_detail.master_detail_ui import CustomerOrdersBackend, CategoryProductsBackend


def run_demo():
    """Run master-detail demos."""
    print("=" * 60)
    print("Master-Detail Form Demo")
    print("=" * 60)
    print("\nSelect demo:")
    print("  1. Customer Orders - DataGrid master, vertical layout")
    print("  2. Category Products - ListView master, horizontal layout")
    print("  3. Customer Orders - DataGrid master, horizontal layout")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        # Customer Orders - DataGrid master, vertical layout
        backend = CustomerOrdersBackend()
        manager = MasterDetailManager(backend)
        
        form = Form()
        form.Text = "Customer Orders - Vertical Layout"
        form.Width = 1000
        form.Height = 800
        form.StartPosition = 'CenterScreen'
        form.ApplyLayout()
        
        panel = MasterDetailPanel(form, props={
            'Dock': DockStyle.Fill,
            'Orientation': 'vertical',
            'MasterHeight': 300,
        }, manager=manager)
        
        manager.refresh_master()
        Application.Run(form)
    
    elif choice == '2':
        # Category Products - ListView master
        backend = CategoryProductsBackend()
        manager = MasterDetailManager(backend)
        
        form = Form()
        form.Text = "Category Products - Master-Detail Demo"
        form.Width = 1000
        form.Height = 600
        form.StartPosition = 'CenterScreen'
        form.ApplyLayout()
        
        panel = MasterDetailPanel(form, props={
            'Dock': DockStyle.Fill,
            'Orientation': 'horizontal',
            'MasterWidth': 250,
        }, manager=manager)
        
        from winformpy.ui_elements.master_detail.master_detail_backend import MasterItem
        
        def on_category_changed(sender, args):
            item = args.get('master_record', {})
            if item:
                text = item.text if isinstance(item, MasterItem) else item.get('text', 'Unknown')
                form.Text = f"Products in: {text}"
        
        panel.MasterSelectionChanged = on_category_changed
        
        manager.refresh_master()
        Application.Run(form)
    
    elif choice == '3':
        # Customer Orders - DataGrid master, horizontal layout
        backend = CustomerOrdersBackend()
        manager = MasterDetailManager(backend)
        
        form = Form()
        form.Text = "Customer Orders - Master-Detail Demo"
        form.Width = 1200
        form.Height = 700
        form.StartPosition = 'CenterScreen'
        form.ApplyLayout()
        
        panel = MasterDetailPanel(form, props={
            'Dock': DockStyle.Fill,
            'Orientation': 'horizontal',
            'MasterWidth': 450,
        }, manager=manager)
        
        def on_master_changed(sender, args):
            customer = args.get('master_record', {})
            if customer:
                form.Text = f"Orders for: {customer.get('name', 'Unknown')}"
        
        def on_detail_double_click(sender, args):
            order = args.get('record', {})
            if order:
                MessageBox.Show(
                    f"Order #{order.get('order_id')}\n"
                    f"Product: {order.get('product')}\n"
                    f"Amount: ${order.get('amount', 0):,.2f}\n"
                    f"Status: {order.get('status')}",
                    "Order Details"
                )
        
        panel.MasterSelectionChanged = on_master_changed
        panel.DetailRowDoubleClick = on_detail_double_click
        
        manager.refresh_master()
        Application.Run(form)
    
    else:
        print("Invalid choice")


if __name__ == "__main__":
    run_demo()
