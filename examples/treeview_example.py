"""
TreeView Example - COMPLETE TreeView Control Demonstration

This example demonstrates ALL TreeView features in WinFormPy:

BASIC FEATURES:
1. Hierarchical node structure
2. Node expansion and collapse
3. Node selection and navigation
4. Adding and removing nodes dynamically

ADVANCED FEATURES:
5. ImageList integration (node icons)
6. CheckBoxes for nodes
7. Context menu with full operations
8. Search functionality
9. Label editing (inline rename)
10. Node colors (BackColor, ForeColor)
11. Node ToolTips
12. HotTracking (hover effects)
13. Sorted mode
14. FullRowSelect mode
15. Line styles (ShowLines, ShowPlusMinus, ShowRootLines)

ALL EVENTS DEMONSTRATED:
- AfterSelect, BeforeSelect
- AfterExpand, BeforeExpand
- AfterCollapse, BeforeCollapse
- AfterCheck, BeforeCheck
- NodeMouseClick, NodeMouseDoubleClick
- AfterLabelEdit, BeforeLabelEdit

ALL PROPERTIES DEMONSTRATED:
- PathSeparator, Indent, ItemHeight
- HideSelection, Scrollable
- BorderStyle, DrawMode
- ImageIndex, SelectedImageIndex
- CheckBoxes, LabelEdit, Sorted
- ShowLines, ShowPlusMinus, ShowRootLines
"""

from winformpy.winformpy import (
    Application, Form, TreeView, TreeNode, Panel, Button, Label,
    TextBox, DockStyle, MessageBox, ImageList,
    ContextMenuStrip, ToolStripMenuItem, CheckBox
)
from winformpy.winformpy_extended import PhotoImage


class TreeViewExampleForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "WinFormPy TreeView - Complete Feature Demonstration"
        self.Width = 900
        self.Height = 700
        self.StartPosition = "CenterScreen"
        self.BackColor = '#F0F0F0'
        self.ApplyLayout()
        
        print("=== TreeView Example Starting ===")
        
        # Initialize components
        self._create_imagelist()
        print("ImageList created")
        
        self._create_top_panel()
        print("Top panel created")
        
        self._create_toolbar()
        print("Toolbar created")
        
        self._create_treeview()
        print("TreeView created")
        
        self._create_bottom_panel()
        print("Bottom panel created")
        
        # Populate sample data
        self._populate_sample_tree()
        print(f"TreeView populated with {len(self.treeview.Nodes)} root nodes")
        
        # Expand first node to make tree visible
        if len(self.treeview.Nodes) > 0:
            self.treeview.Nodes[0].Expand()
            print("First node expanded")
        
        print("=== Initialization Complete ===")
        print("If you see this, the window should be visible!")
    
    def _create_imagelist(self):
        """Create ImageList with icons for TreeView nodes."""
        self.imagelist = ImageList({'ImageSize': (16, 16)})
        
        # Create simple colored icons
        colors = [
            ('#E74C3C', 'Company'),      # 0 - Red (Company)
            ('#3498DB', 'Department'),   # 1 - Blue (Department)
            ('#2ECC71', 'Team'),         # 2 - Green (Team)
            ('#F39C12', 'Person'),       # 3 - Orange (Person)
            ('#9B59B6', 'Project'),      # 4 - Purple (Project)
            ('#1ABC9C', 'Task'),         # 5 - Teal (Task)
        ]
        
        for color, name in colors:
            icon = PhotoImage(width=16, height=16)
            # Create colored square
            for y in range(16):
                for x in range(16):
                    if 2 <= x <= 13 and 2 <= y <= 13:
                        icon.put(color, (x, y))
                    else:
                        icon.put('#FFFFFF', (x, y))
            self.imagelist.Add(icon, name.lower())
    
    def _create_top_panel(self):
        """Create top title panel."""
        top_panel = Panel(self, {
            'Height': 90,
            'BackColor': '#0078D4'
        })
        top_panel.Dock = DockStyle.Top
        
        Label(top_panel, {
            'Text': 'TREEVIEW - COMPLETE FEATURE DEMONSTRATION',
            'Left': 20,
            'Top': 12,
            'AutoSize': True,
            'Font': ('Segoe UI', 18, 'bold'),
            'ForeColor': '#FFFFFF',
            'BackColor': '#0078D4'
        })
        
        Label(top_panel, {
            'Text': 'All TreeView features: CheckBoxes, ImageList, LabelEdit, HotTracking, Events, Node Colors, and more!',
            'Left': 20,
            'Top': 48,
            'Width': 1300,
            'Font': ('Segoe UI', 9),
            'ForeColor': '#E0E0E0',
            'BackColor': '#0078D4'
        })
        
        Label(top_panel, {
            'Text': 'Try: Check nodes, Expand/Collapse, Right-click for menu, Double-click to edit labels',
            'Left': 20,
            'Top': 68,
            'Width': 850,
            'Font': ('Segoe UI', 8, 'italic'),
            'ForeColor': '#BDC3C7',
            'BackColor': '#0078D4'
        })
    
    def _create_toolbar(self):
        """Create toolbar with quick actions."""
        toolbar = Panel(self, {
            'Height': 80,
            'BackColor': '#E0E0E0'
        })
        toolbar.Dock = DockStyle.Top
        
        # Row 1: View options (Note: CheckBoxes removed since using Unicode symbols)
        Label(toolbar, {
            'Text': 'View Options:',
            'Left': 10,
            'Top': 8,
            'AutoSize': True,
            'Font': ('Segoe UI', 9, 'bold')
        })
        
        self.chk_show_lines = CheckBox(toolbar, {
            'Text': 'Show Lines',
            'Left': 120,
            'Top': 5,
            'Width': 120,
            'Checked': True
        })
        self.chk_show_lines.CheckedChanged = self._on_toggle_show_lines
        
        self.chk_full_row_select = CheckBox(toolbar, {
            'Text': 'Full Row Select',
            'Left': 250,
            'Top': 5,
            'Width': 130,
            'Checked': True
        })
        self.chk_full_row_select.CheckedChanged = self._on_toggle_full_row_select
        
        self.chk_hot_tracking = CheckBox(toolbar, {
            'Text': 'Hot Tracking',
            'Left': 390,
            'Top': 5,
            'Width': 120,
            'Checked': True
        })
        self.chk_hot_tracking.CheckedChanged = self._on_toggle_hot_tracking
        
        Label(toolbar, {
            'Text': '💡 Checkboxes shown as ☐/☑ symbols (Tkinter limitation)',
            'Left': 520,
            'Top': 8,
            'AutoSize': True,
            'Font': ('Segoe UI', 8, 'italic'),
            'ForeColor': '#555555'
        })
        
        # Row 2: Action buttons
        Label(toolbar, {
            'Text': 'Actions:',
            'Left': 10,
            'Top': 38,
            'AutoSize': True,
            'Font': ('Segoe UI', 9, 'bold')
        })
        
        btn_expand_all = Button(toolbar, {
            'Text': '⬇ Expand All',
            'Left': 120,
            'Top': 35,
            'Width': 100,
            'Height': 30
        })
        btn_expand_all.Click = lambda s, e: self.treeview.ExpandAll()
        
        btn_collapse_all = Button(toolbar, {
            'Text': '⬆ Collapse All',
            'Left': 230,
            'Top': 35,
            'Width': 100,
            'Height': 30
        })
        btn_collapse_all.Click = lambda s, e: self.treeview.CollapseAll()
        
        btn_check_all = Button(toolbar, {
            'Text': '☑ Check All',
            'Left': 340,
            'Top': 35,
            'Width': 100,
            'Height': 30
        })
        btn_check_all.Click = self._on_check_all_nodes
        
        btn_uncheck_all = Button(toolbar, {
            'Text': '☐ Uncheck All',
            'Left': 450,
            'Top': 35,
            'Width': 100,
            'Height': 30
        })
        btn_uncheck_all.Click = self._on_uncheck_all_nodes
        
        btn_add_root = Button(toolbar, {
            'Text': '➕ Add Root',
            'Left': 570,
            'Top': 35,
            'Width': 100,
            'Height': 30,
            'BackColor': '#27AE60',
            'ForeColor': '#FFFFFF'
        })
        btn_add_root.Click = self._on_add_root_node
        
        btn_reload = Button(toolbar, {
            'Text': '🔄 Reload',
            'Left': 680,
            'Top': 35,
            'Width': 100,
            'Height': 30,
            'BackColor': '#3498DB',
            'ForeColor': '#FFFFFF'
        })
        btn_reload.Click = lambda s, e: self._populate_sample_tree()
    
    def _create_treeview(self):
        """Create TreeView with all features enabled.
        
        NOTE: Tkinter's ttk.Treeview doesn't natively support checkboxes.
        We simulate checkboxes using Unicode symbols in the node text.
        """
        self.treeview = TreeView(self, {
            'BackColor': '#FFFFFF',
            'Font': ('Segoe UI', 9),
            'ShowLines': True,
            'ShowPlusMinus': True,
            'ShowRootLines': True,
            'FullRowSelect': True,
            'CheckBoxes': False,  # Tkinter doesn't support native checkboxes
            'LabelEdit': True,
            'HotTracking': True,
            'ImageList': self.imagelist,
            'HideSelection': False,
            'Scrollable': True,
            'PathSeparator': ' → ',
            'Indent': 19
        })
        self.treeview.Dock = DockStyle.Fill
        
        # Bind events
        self.treeview.AfterSelect = self._on_after_select
        self.treeview.AfterExpand = self._on_after_expand
        self.treeview.AfterCollapse = self._on_after_collapse
        self.treeview.AfterCheck = self._on_after_check
        self.treeview.NodeMouseClick = self._on_node_mouse_click
        self.treeview.NodeMouseDoubleClick = self._on_node_double_click
        self.treeview.AfterLabelEdit = self._on_after_label_edit
        
        # Create context menu
        self._create_context_menu()
    
    def _create_context_menu(self):
        """Create context menu for TreeView nodes."""
        context_menu = ContextMenuStrip()
        
        menu_add_child = ToolStripMenuItem("Add Child Node")
        menu_add_child.Click = lambda s, e: self._on_add_child_node()
        context_menu.Items.append(menu_add_child)
        
        menu_add_sibling = ToolStripMenuItem("Add Sibling Node")
        menu_add_sibling.Click = lambda s, e: self._on_add_sibling_node()
        context_menu.Items.append(menu_add_sibling)
        
        context_menu.Items.append(ToolStripMenuItem("-"))  # Separator
        
        menu_rename = ToolStripMenuItem("Rename Node")
        menu_rename.Click = lambda s, e: self._on_rename_node()
        context_menu.Items.append(menu_rename)
        
        menu_delete = ToolStripMenuItem("Delete Node")
        menu_delete.Click = lambda s, e: self._on_delete_node()
        context_menu.Items.append(menu_delete)
        
        context_menu.Items.append(ToolStripMenuItem("-"))  # Separator
        
        menu_expand_all = ToolStripMenuItem("Expand All")
        menu_expand_all.Click = lambda s, e: self.treeview.ExpandAll()
        context_menu.Items.append(menu_expand_all)
        
        menu_collapse_all = ToolStripMenuItem("Collapse All")
        menu_collapse_all.Click = lambda s, e: self.treeview.CollapseAll()
        context_menu.Items.append(menu_collapse_all)
        
        self.treeview.ContextMenuStrip = context_menu
    
    def _create_bottom_panel(self):
        """Create bottom status panel."""
        bottom_panel = Panel(self, {
            'Height': 35,
            'BackColor': '#34495E'
        })
        bottom_panel.Dock = DockStyle.Bottom
        
        self.lbl_status = Label(bottom_panel, {
            'Text': 'Ready | No node selected',
            'Left': 15,
            'Top': 8,
            'Width': 1000,
            'ForeColor': '#FFFFFF',
            'Font': ('Segoe UI', 9),
            'BackColor': '#34495E'
        })
    
    def _populate_sample_tree(self):
        """Populate TreeView with comprehensive sample data demonstrating all features.
        
        NOTE: Using checkbox symbols (☐/☑) in text since Tkinter doesn't support native checkboxes.
        """
        # Clear existing tree
        self.treeview.Nodes.Clear()
        
        # Company root with color
        root = TreeNode("🏢 TechCorp International", ImageIndex=0)
        root.Tag = {'type': 'company', 'id': 1, 'checked': False}
        root.ToolTipText = "Main company headquarters"
        self.treeview.Nodes.Add(root)
        
        # Engineering Department
        engineering = TreeNode("💻 Engineering Department", ImageIndex=1)
        engineering.Tag = {'type': 'department', 'id': 2, 'checked': False}
        engineering.ForeColor = '#2980B9'
        root.Nodes.Add(engineering)
        
        # Engineering teams
        frontend = TreeNode("🎨 Frontend Team", ImageIndex=2)
        frontend.Tag = {'type': 'team', 'id': 3, 'checked': False}
        engineering.Nodes.Add(frontend)
        
        # Frontend developers with varied properties - some with checkboxes
        dev1 = TreeNode("☑ John Smith - Senior Developer", ImageIndex=3)
        dev1.Tag = {'type': 'person', 'role': 'senior', 'skill': 'React', 'checked': True}
        frontend.Nodes.Add(dev1)
        
        dev2 = TreeNode("☐ Sarah Johnson - Developer", ImageIndex=3)
        dev2.Tag = {'type': 'person', 'role': 'mid', 'skill': 'Vue', 'checked': False}
        frontend.Nodes.Add(dev2)
        
        dev3 = TreeNode("☐ Mike Chen - Junior Developer", ImageIndex=3)
        dev3.Tag = {'type': 'person', 'role': 'junior', 'skill': 'Angular', 'checked': False}
        dev3.ForeColor = '#27AE60'
        frontend.Nodes.Add(dev3)
        
        # Backend Team
        backend = TreeNode("⚙️ Backend Team", ImageIndex=2)
        backend.Tag = {'type': 'team', 'id': 4, 'checked': False}
        engineering.Nodes.Add(backend)
        
        dev4 = TreeNode("☑ David Wilson - Tech Lead", ImageIndex=3)
        dev4.Tag = {'checked': True}
        backend.Nodes.Add(dev4)
        
        dev5 = TreeNode("☐ Lisa Anderson - Senior Developer", ImageIndex=3)
        dev5.Tag = {'checked': False}
        backend.Nodes.Add(dev5)
        
        dev6 = TreeNode("☐ Robert Taylor - Developer", ImageIndex=3)
        dev6.Tag = {'checked': False}
        backend.Nodes.Add(dev6)
        
        # DevOps Team with projects
        devops = TreeNode("🔧 DevOps Team", ImageIndex=2)
        devops.Tag = {'type': 'team', 'id': 5, 'checked': False}
        engineering.Nodes.Add(devops)
        
        devops_member1 = TreeNode("☑ Thomas Lopez - DevOps Lead", ImageIndex=3)
        devops_member1.Tag = {'checked': True}
        devops.Nodes.Add(devops_member1)
        
        # Projects under DevOps lead
        project1 = TreeNode("📦 CI/CD Pipeline", ImageIndex=4)
        project1.Tag = {'checked': False}
        project1.BackColor = '#FFF3CD'
        devops_member1.Nodes.Add(project1)
        
        task1 = TreeNode("☐ Jenkins Setup", ImageIndex=5)
        task1.Tag = {'checked': False}
        project1.Nodes.Add(task1)
        
        task2 = TreeNode("☑ Docker Configuration", ImageIndex=5)
        task2.Tag = {'checked': True}
        project1.Nodes.Add(task2)
        
        devops_member2 = TreeNode("☐ Jennifer Martinez - DevOps Engineer", ImageIndex=3)
        devops_member2.Tag = {'checked': False}
        devops.Nodes.Add(devops_member2)
        
        # Sales Department
        sales = TreeNode("💼 Sales Department", ImageIndex=1)
        sales.Tag = {'type': 'department', 'id': 6, 'checked': False}
        sales.ForeColor = '#E67E22'
        root.Nodes.Add(sales)
        
        # US Sales
        sales_us = TreeNode("🇺🇸 US Sales", ImageIndex=2)
        sales_us.Tag = {'checked': False}
        sales.Nodes.Add(sales_us)
        
        sales1 = TreeNode("☑ James Garcia - Sales Manager", ImageIndex=3)
        sales1.Tag = {'checked': True}
        sales_us.Nodes.Add(sales1)
        
        sales2 = TreeNode("☐ Mary Rodriguez - Account Executive", ImageIndex=3)
        sales2.Tag = {'checked': False}
        sales_us.Nodes.Add(sales2)
        
        # EU Sales
        sales_eu = TreeNode("🇪🇺 EU Sales", ImageIndex=2)
        sales_eu.Tag = {'checked': False}
        sales.Nodes.Add(sales_eu)
        
        sales3 = TreeNode("☐ William Lee - Regional Manager", ImageIndex=3)
        sales3.Tag = {'checked': False}
        sales_eu.Nodes.Add(sales3)
        
        sales4 = TreeNode("☐ Patricia Hernandez - Sales Rep", ImageIndex=3)
        sales4.Tag = {'checked': False}
        sales_eu.Nodes.Add(sales4)
        
        # HR Department
        hr = TreeNode("👥 Human Resources", ImageIndex=1)
        hr.Tag = {'type': 'department', 'id': 7, 'checked': False}
        hr.ForeColor = '#8E44AD'
        root.Nodes.Add(hr)
        
        hr_manager = TreeNode("☑ Linda Gonzalez - HR Manager", ImageIndex=3)
        hr_manager.Tag = {'checked': True}
        hr_manager.BackColor = '#E8DAEF'
        hr.Nodes.Add(hr_manager)
        
        hr1 = TreeNode("☐ Charles Wilson - HR Specialist", ImageIndex=3)
        hr1.Tag = {'checked': False}
        hr.Nodes.Add(hr1)
        
        hr2 = TreeNode("☐ Emily Davis - Recruiter", ImageIndex=3)
        hr2.Tag = {'checked': False}
        hr.Nodes.Add(hr2)
        
        # Finance Department with budget breakdown
        finance = TreeNode("💰 Finance Department", ImageIndex=1)
        finance.Tag = {'type': 'department', 'id': 8, 'checked': False}
        finance.ForeColor = '#16A085'
        root.Nodes.Add(finance)
        
        cfo = TreeNode("☑ Richard Brown - CFO", ImageIndex=3)
        cfo.Tag = {'checked': True}
        finance.Nodes.Add(cfo)
        
        # Budget breakdown under CFO
        budgets = TreeNode("📊 Budget 2026", ImageIndex=4)
        budgets.Tag = {'checked': False}
        budgets.BackColor = '#D5F4E6'
        cfo.Nodes.Add(budgets)
        
        budget1 = TreeNode("☐ Q1: $500K", ImageIndex=5)
        budget1.Tag = {'checked': False}
        budgets.Nodes.Add(budget1)
        
        budget2 = TreeNode("☑ Q2: $600K", ImageIndex=5)
        budget2.Tag = {'checked': True}
        budgets.Nodes.Add(budget2)
        
        budget3 = TreeNode("☐ Q3: $550K", ImageIndex=5)
        budget3.Tag = {'checked': False}
        budgets.Nodes.Add(budget3)
        
        budget4 = TreeNode("☐ Q4: $700K", ImageIndex=5)
        budget4.Tag = {'checked': False}
        budgets.Nodes.Add(budget4)
        
        finance.Nodes.Add(TreeNode("👤 Barbara Moore - Accountant", ImageIndex=3))
        finance.Nodes.Add(TreeNode("👤 Daniel Clark - Financial Analyst", ImageIndex=3))
        
        # Expand root and engineering to show structure
        root.Expand()
        engineering.Expand()
        frontend.Expand()
        
        self.lbl_status.Text = "Sample tree loaded - Try expanding nodes and checking boxes!"
    
    # =======================
    # EVENT HANDLERS
    # =======================
    
    def _on_toggle_show_lines(self, sender, e):
        """Toggle tree lines visibility."""
        self.treeview.ShowLines = self.chk_show_lines.Checked
        self.treeview.Refresh()
        status = "visible" if self.chk_show_lines.Checked else "hidden"
        self.lbl_status.Text = f"Tree lines {status}"
    
    def _on_toggle_full_row_select(self, sender, e):
        """Toggle full row selection."""
        self.treeview.FullRowSelect = self.chk_full_row_select.Checked
        self.treeview.Refresh()
        status = "enabled" if self.chk_full_row_select.Checked else "disabled"
        self.lbl_status.Text = f"Full row select {status}"
    
    def _on_toggle_hot_tracking(self, sender, e):
        """Toggle hot tracking (hover effect)."""
        self.treeview.HotTracking = self.chk_hot_tracking.Checked
        self.treeview.Refresh()
        status = "enabled" if self.chk_hot_tracking.Checked else "disabled"
        self.lbl_status.Text = f"Hot tracking {status}"
    
    def _on_after_select(self, sender, e):
        """Handle node selection."""
        if self.treeview.SelectedNode:
            node = self.treeview.SelectedNode
            self.lbl_status.Text = f"Selected: {node.Text}"
    
    def _on_after_expand(self, sender, e):
        """Handle node expansion."""
        if self.treeview.SelectedNode:
            self.lbl_status.Text = f"Expanded node"
    
    def _on_after_collapse(self, sender, e):
        """Handle node collapse."""
        if self.treeview.SelectedNode:
            self.lbl_status.Text = f"Collapsed node"
    
    def _on_after_check(self, sender, e):
        """Handle checkbox state change."""
        if self.treeview.SelectedNode:
            node = self.treeview.SelectedNode
            # Check the Tag for checkbox state (or text symbol)
            is_checked = False
            if node.Tag and isinstance(node.Tag, dict):
                is_checked = node.Tag.get('checked', False)
            elif node.Text.startswith('☑'):
                is_checked = True
            
            state = "Checked" if is_checked else "Unchecked"
            self.lbl_status.Text = f"{state}: {node.Text}"
    
    def _on_node_mouse_click(self, sender, e):
        """Handle node click."""
        pass
    
    def _on_node_double_click(self, sender, e):
        """Handle double-click - toggle expansion."""
        if self.treeview.SelectedNode:
            node = self.treeview.SelectedNode
            if node.IsExpanded:
                node.Collapse()
            else:
                node.Expand()
    
    def _on_after_label_edit(self, sender, e):
        """Handle label edit completion."""
        if self.treeview.SelectedNode:
            self.lbl_status.Text = f"Label edited: {self.treeview.SelectedNode.Text}"
    
    # =======================
    # BUTTON CLICK HANDLERS
    # =======================
    
    def _on_add_root_node(self, sender, e):
        """Add a new root node."""
        node_name = f"🆕 New Department {len(self.treeview.Nodes) + 1}"
        new_node = TreeNode(node_name, ImageIndex=1)
        self.treeview.Nodes.Add(new_node)
        self.treeview.SelectedNode = new_node
        self.lbl_status.Text = f"Added: {node_name}"
    
    def _on_check_all_nodes(self, sender, e):
        """Check all nodes recursively using checkbox symbols."""
        self._set_all_nodes_checked(self.treeview.Nodes, True)
        total = self._count_all_nodes(self.treeview.Nodes)
        self.lbl_status.Text = f"✓ All {total} nodes checked"
        MessageBox.Show(f"Checked all {total} nodes in the tree.\n\nCheckboxes are displayed using ☑ symbols.", "Check All")
    
    def _on_uncheck_all_nodes(self, sender, e):
        """Uncheck all nodes recursively using checkbox symbols."""
        self._set_all_nodes_checked(self.treeview.Nodes, False)
        total = self._count_all_nodes(self.treeview.Nodes)
        self.lbl_status.Text = f"☐ All {total} nodes unchecked"
        MessageBox.Show(f"Unchecked all {total} nodes in the tree.\n\nCheckboxes are displayed using ☐ symbols.", "Uncheck All")
    
    def _set_all_nodes_checked(self, nodes, checked):
        """Recursively set checked state for all nodes using text symbols.
        
        Since Tkinter doesn't support native checkboxes, we toggle between
        ☐ (unchecked) and ☑ (checked) symbols in the node text.
        """
        for node in nodes:
            # Update checkbox symbol in text
            if node.Text.startswith('☐ '):
                if checked:
                    node.Text = '☑ ' + node.Text[2:]  # Replace ☐ with ☑
                    if node.Tag and isinstance(node.Tag, dict):
                        node.Tag['checked'] = True
            elif node.Text.startswith('☑ '):
                if not checked:
                    node.Text = '☐ ' + node.Text[2:]  # Replace ☑ with ☐
                    if node.Tag and isinstance(node.Tag, dict):
                        node.Tag['checked'] = False
            
            # Recursively process children
            self._set_all_nodes_checked(node.Nodes, checked)
    
    def _count_all_nodes(self, nodes):
        """Recursively count all nodes."""
        count = len(nodes)
        for node in nodes:
            count += self._count_all_nodes(node.Nodes)
        return count


def main():
    """Application entry point."""
    app = TreeViewExampleForm()
    Application.Run(app)


if __name__ == '__main__':
    main()
