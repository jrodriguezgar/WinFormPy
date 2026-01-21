"""
Master-Detail UI Element

Provides a master-detail view component with two containers:
- Master: Can be a DataGrid or ListView (configurable via MasterType property)
- Detail: Always a DataGrid showing related records

Layout options:
- Orientation: 'horizontal' (side-by-side) or 'vertical' (top-bottom)

Components:
- MasterDetailBackend: Abstract base class for data sources
- MasterDetailManager: Service layer for state management
- MasterDetailPanel: Embeddable UI component
- MasterDetailForm: Standalone window

Demo Backends:
- DemoMasterDetailBackend: Customer → Orders (DataGrid master)
- DemoListViewBackend: Category → Products (ListView master)

Usage:
    from winformpy.ui_elements.master_detail import (
        MasterDetailPanel, MasterDetailForm, MasterDetailBackend,
        MasterDetailManager, MasterType
    )
    
    # Horizontal layout with DataGrid master
    panel = MasterDetailPanel(form, props={
        'Orientation': 'horizontal',
        'MasterType': MasterType.DATA_GRID,
        'MasterWidth': 350,
    }, manager=manager)
    
    # Vertical layout with ListView master
    panel = MasterDetailPanel(form, props={
        'Orientation': 'vertical',
        'MasterType': MasterType.LIST_VIEW,
        'MasterHeight': 200,
    }, manager=manager)
"""

from .master_detail_backend import (
    MasterDetailBackend,
    MasterType,
    MasterItem,
    MasterListResponse,
    DemoMasterDetailBackend,
    DemoListViewBackend,
)
from .master_detail_manager import MasterDetailManager
from .master_detail_panel import MasterDetailPanel
from .master_detail_ui import (
    MasterDetailForm,
    run_demo_grid_master,
    run_demo_list_master,
    run_demo_vertical,
)

__all__ = [
    # Backend
    'MasterDetailBackend',
    'MasterType',
    'MasterItem',
    'MasterListResponse',
    'DemoMasterDetailBackend',
    'DemoListViewBackend',
    # Manager
    'MasterDetailManager',
    # Panel
    'MasterDetailPanel',
    # Form
    'MasterDetailForm',
    # Demo functions
    'run_demo_grid_master',
    'run_demo_list_master',
    'run_demo_vertical',
]
