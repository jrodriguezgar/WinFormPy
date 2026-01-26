"""
TreeView Example - Comprehensive TreeView Control Demonstration

This example demonstrates the TreeView control in WinFormPy with:
1. Hierarchical node structure
2. Node expansion and collapse
3. Node selection and navigation
4. Adding and removing nodes dynamically
5. Node images with ImageList
6. Context menu for nodes
7. Search functionality
8. Node manipulation (edit, delete, move)

FEATURES DEMONSTRATED:
- TreeNode creation and management
- Parent-child relationships
- Node expansion/collapse
- Node selection events
- Dynamic node addition/removal
- ImageList integration
- Context menu
- Node search and filtering
"""

from winformpy.winformpy import (
    Application, Form, TreeView, TreeNode, Panel, Button, Label,
    TextBox, DockStyle, Font, FontStyle, MessageBox, ImageList,
    ContextMenuStrip, ToolStripMenuItem, SplitContainer
)
from winformpy.winformpy_extended import PhotoImage


class TreeViewExampleForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "WinFormPy TreeView Example"
        self.Width = 1100
        self.Height = 750
        self.StartPosition = "CenterScreen"
        self.ApplyLayout()
        
        # Initialize components
        self._create_top_panel()
        self._create_split_container()
        self._create_bottom_panel()
        
        # Populate sample data
        self._populate_sample_tree()
    
    def _create_top_panel(self):
        """Create top title panel."""
        top_panel = Panel(self, {
            'Height': 70,
            'BackColor': '#0078D4'
        })
        top_panel.Dock = DockStyle.Top
        
        Label(top_panel, {
            'Text': 'TREEVIEW CONTROL DEMONSTRATION',
            'Left': 20,
            'Top': 12,
            'AutoSize': True,
            'Font': Font('Segoe UI', 16, FontStyle.Bold),
            'ForeColor': '#FFFFFF',
            'BackColor': '#0078D4'
        })
        
        Label(top_panel, {
            'Text': 'Explore hierarchical data with TreeView - expand, collapse, and navigate nodes',
            'Left': 20,
            'Top': 42,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9),
            'ForeColor': '#E0E0E0',
            'BackColor': '#0078D4'
        })
    
    def _create_split_container(self):
        """Create split container with TreeView and details panel."""
        self.split_container = SplitContainer(self, {
            'Orientation': 'Vertical',
            'SplitterDistance': 350,
            'BackColor': '#CCCCCC'
        })
        self.split_container.Dock = DockStyle.Fill
        
        # Left panel - TreeView
        self._create_treeview_panel()
        
        # Right panel - Details and controls
        self._create_details_panel()
    
    def _create_treeview_panel(self):
        """Create TreeView panel."""
        tree_panel = Panel(self.split_container.Panel1, {
            'BackColor': '#F5F5F5'
        })
        tree_panel.Dock = DockStyle.Fill
        
        # Search panel
        search_panel = Panel(tree_panel, {
            'Height': 50,
            'BackColor': '#E0E0E0',
            'BorderStyle': 'FixedSingle'
        })
        search_panel.Dock = DockStyle.Top
        
        Label(search_panel, {
            'Text': 'Search:',
            'Left': 10,
            'Top': 15,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9, FontStyle.Bold),
            'BackColor': '#E0E0E0'
        })
        
        self.txt_search = TextBox(search_panel, {
            'Left': 70,
            'Top': 12,
            'Width': 200
        })
        
        btn_search = Button(search_panel, {
            'Text': 'Find',
            'Left': 280,
            'Top': 10,
            'Width': 50,
            'Height': 26
        })
        btn_search.Click = self._on_search_node
        
        # TreeView
        self.treeview = TreeView(tree_panel, {
            'BackColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9),
            'ShowLines': True,
            'ShowPlusMinus': True,
            'ShowRootLines': True,
            'FullRowSelect': True
        })
        self.treeview.Dock = DockStyle.Fill
        
        # Bind events
        self.treeview.AfterSelect = self._on_node_selected
        self.treeview.NodeMouseDoubleClick = self._on_node_double_click
        
        # Create context menu
        self._create_context_menu()
    
    def _create_context_menu(self):
        """Create context menu for TreeView nodes."""
        context_menu = ContextMenuStrip()
        
        menu_add_child = ToolStripMenuItem("Add Child Node")
        menu_add_child.Click = lambda s, e: self._on_add_child_node()
        context_menu.Items.Add(menu_add_child)
        
        menu_add_sibling = ToolStripMenuItem("Add Sibling Node")
        menu_add_sibling.Click = lambda s, e: self._on_add_sibling_node()
        context_menu.Items.Add(menu_add_sibling)
        
        context_menu.Items.Add(ToolStripMenuItem("-"))  # Separator
        
        menu_rename = ToolStripMenuItem("Rename Node")
        menu_rename.Click = lambda s, e: self._on_rename_node()
        context_menu.Items.Add(menu_rename)
        
        menu_delete = ToolStripMenuItem("Delete Node")
        menu_delete.Click = lambda s, e: self._on_delete_node()
        context_menu.Items.Add(menu_delete)
        
        context_menu.Items.Add(ToolStripMenuItem("-"))  # Separator
        
        menu_expand_all = ToolStripMenuItem("Expand All")
        menu_expand_all.Click = lambda s, e: self.treeview.ExpandAll()
        context_menu.Items.Add(menu_expand_all)
        
        menu_collapse_all = ToolStripMenuItem("Collapse All")
        menu_collapse_all.Click = lambda s, e: self.treeview.CollapseAll()
        context_menu.Items.Add(menu_collapse_all)
        
        self.treeview.ContextMenuStrip = context_menu
    
    def _create_details_panel(self):
        """Create details panel with node information and controls."""
        details_panel = Panel(self.split_container.Panel2, {
            'BackColor': '#FFFFFF'
        })
        details_panel.Dock = DockStyle.Fill
        
        # Title
        Label(details_panel, {
            'Text': 'Node Details & Operations',
            'Left': 20,
            'Top': 20,
            'AutoSize': True,
            'Font': Font('Segoe UI', 12, FontStyle.Bold),
            'ForeColor': '#0078D4'
        })
        
        # Selected node info
        Label(details_panel, {
            'Text': 'Selected Node:',
            'Left': 20,
            'Top': 60,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        
        self.lbl_selected_node = Label(details_panel, {
            'Text': 'None',
            'Left': 140,
            'Top': 60,
            'Width': 500,
            'AutoSize': False,
            'Font': Font('Segoe UI', 9),
            'ForeColor': '#333333'
        })
        
        Label(details_panel, {
            'Text': 'Full Path:',
            'Left': 20,
            'Top': 85,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        
        self.lbl_node_path = Label(details_panel, {
            'Text': '',
            'Left': 140,
            'Top': 85,
            'Width': 500,
            'AutoSize': False,
            'Font': Font('Segoe UI', 9),
            'ForeColor': '#666666'
        })
        
        Label(details_panel, {
            'Text': 'Level:',
            'Left': 20,
            'Top': 110,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        
        self.lbl_node_level = Label(details_panel, {
            'Text': '',
            'Left': 140,
            'Top': 110,
            'Width': 200,
            'AutoSize': False,
            'Font': Font('Segoe UI', 9)
        })
        
        Label(details_panel, {
            'Text': 'Children:',
            'Left': 20,
            'Top': 135,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        
        self.lbl_node_children = Label(details_panel, {
            'Text': '',
            'Left': 140,
            'Top': 135,
            'Width': 200,
            'AutoSize': False,
            'Font': Font('Segoe UI', 9)
        })
        
        # Operations section
        Label(details_panel, {
            'Text': 'Node Operations:',
            'Left': 20,
            'Top': 180,
            'AutoSize': True,
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'ForeColor': '#0078D4'
        })
        
        # Add buttons
        btn_add_root = Button(details_panel, {
            'Text': '➕ Add Root Node',
            'Left': 20,
            'Top': 210,
            'Width': 180,
            'Height': 35,
            'BackColor': '#2ECC71',
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        btn_add_root.Click = self._on_add_root_node
        
        btn_add_child = Button(details_panel, {
            'Text': '➕ Add Child Node',
            'Left': 210,
            'Top': 210,
            'Width': 180,
            'Height': 35,
            'BackColor': '#3498DB',
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        btn_add_child.Click = lambda s, e: self._on_add_child_node()
        
        btn_delete = Button(details_panel, {
            'Text': '➖ Delete Node',
            'Left': 400,
            'Top': 210,
            'Width': 180,
            'Height': 35,
            'BackColor': '#E74C3C',
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        btn_delete.Click = lambda s, e: self._on_delete_node()
        
        # Expansion controls
        btn_expand = Button(details_panel, {
            'Text': '⬇️ Expand All',
            'Left': 20,
            'Top': 260,
            'Width': 140,
            'Height': 30
        })
        btn_expand.Click = lambda s, e: self.treeview.ExpandAll()
        
        btn_collapse = Button(details_panel, {
            'Text': '⬆️ Collapse All',
            'Left': 170,
            'Top': 260,
            'Width': 140,
            'Height': 30
        })
        btn_collapse.Click = lambda s, e: self.treeview.CollapseAll()
        
        # Statistics
        Label(details_panel, {
            'Text': 'Tree Statistics:',
            'Left': 20,
            'Top': 320,
            'AutoSize': True,
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'ForeColor': '#0078D4'
        })
        
        self.lbl_stats = Label(details_panel, {
            'Text': 'Total Nodes: 0\nRoot Nodes: 0\nMax Depth: 0',
            'Left': 20,
            'Top': 350,
            'Width': 300,
            'Height': 80,
            'Font': Font('Segoe UI', 9),
            'ForeColor': '#666666'
        })
        
        # Update stats button
        btn_update_stats = Button(details_panel, {
            'Text': '🔄 Update Statistics',
            'Left': 20,
            'Top': 440,
            'Width': 160,
            'Height': 30,
            'BackColor': '#95A5A6',
            'ForeColor': '#FFFFFF'
        })
        btn_update_stats.Click = self._on_update_statistics
    
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
            'Font': Font('Segoe UI', 9),
            'BackColor': '#34495E'
        })
    
    def _populate_sample_tree(self):
        """Populate TreeView with sample organizational data."""
        # Company root
        root = TreeNode("TechCorp International", 0)
        self.treeview.Nodes.Add(root)
        
        # Departments
        engineering = TreeNode("Engineering Department", 1)
        root.Nodes.Add(engineering)
        
        # Engineering teams
        frontend = TreeNode("Frontend Team", 2)
        engineering.Nodes.Add(frontend)
        frontend.Nodes.Add(TreeNode("John Smith - Senior Developer", 3))
        frontend.Nodes.Add(TreeNode("Sarah Johnson - Developer", 3))
        frontend.Nodes.Add(TreeNode("Mike Chen - Junior Developer", 3))
        
        backend = TreeNode("Backend Team", 2)
        engineering.Nodes.Add(backend)
        backend.Nodes.Add(TreeNode("David Wilson - Tech Lead", 3))
        backend.Nodes.Add(TreeNode("Lisa Anderson - Senior Developer", 3))
        backend.Nodes.Add(TreeNode("Robert Taylor - Developer", 3))
        
        devops = TreeNode("DevOps Team", 2)
        engineering.Nodes.Add(devops)
        devops.Nodes.Add(TreeNode("Thomas Lopez - DevOps Lead", 3))
        devops.Nodes.Add(TreeNode("Jennifer Martinez - DevOps Engineer", 3))
        
        # Sales Department
        sales = TreeNode("Sales Department", 1)
        root.Nodes.Add(sales)
        
        sales_us = TreeNode("US Sales", 2)
        sales.Nodes.Add(sales_us)
        sales_us.Nodes.Add(TreeNode("James Garcia - Sales Manager", 3))
        sales_us.Nodes.Add(TreeNode("Mary Rodriguez - Account Executive", 3))
        
        sales_eu = TreeNode("EU Sales", 2)
        sales.Nodes.Add(sales_eu)
        sales_eu.Nodes.Add(TreeNode("William Lee - Regional Manager", 3))
        sales_eu.Nodes.Add(TreeNode("Patricia Hernandez - Sales Rep", 3))
        
        # HR Department
        hr = TreeNode("Human Resources", 1)
        root.Nodes.Add(hr)
        hr.Nodes.Add(TreeNode("Linda Gonzalez - HR Manager", 3))
        hr.Nodes.Add(TreeNode("Charles Wilson - HR Specialist", 3))
        hr.Nodes.Add(TreeNode("Emily Davis - Recruiter", 3))
        
        # Finance Department
        finance = TreeNode("Finance Department", 1)
        root.Nodes.Add(finance)
        finance.Nodes.Add(TreeNode("Richard Brown - CFO", 3))
        finance.Nodes.Add(TreeNode("Barbara Moore - Accountant", 3))
        finance.Nodes.Add(TreeNode("Daniel Clark - Financial Analyst", 3))
        
        # Expand root by default
        root.Expand()
        
        self._update_statistics()
    
    def _on_node_selected(self, sender, e):
        """Handle node selection."""
        selected_node = self.treeview.SelectedNode
        if selected_node:
            self.lbl_selected_node.Text = selected_node.Text
            self.lbl_node_path.Text = selected_node.FullPath
            self.lbl_node_level.Text = f"Level {selected_node.Level}"
            self.lbl_node_children.Text = f"{len(selected_node.Nodes)} child node(s)"
            self.lbl_status.Text = f"Selected: {selected_node.Text}"
        else:
            self.lbl_selected_node.Text = "None"
            self.lbl_node_path.Text = ""
            self.lbl_node_level.Text = ""
            self.lbl_node_children.Text = ""
            self.lbl_status.Text = "No node selected"
    
    def _on_node_double_click(self, sender, e):
        """Handle node double-click."""
        selected_node = self.treeview.SelectedNode
        if selected_node:
            if selected_node.IsExpanded:
                selected_node.Collapse()
            else:
                selected_node.Expand()
    
    def _on_add_root_node(self, sender, e):
        """Add a new root node."""
        node_name = f"New Department {len(self.treeview.Nodes) + 1}"
        new_node = TreeNode(node_name, 1)
        self.treeview.Nodes.Add(new_node)
        self.treeview.SelectedNode = new_node
        self._update_statistics()
        MessageBox.Show(f"Added root node: {node_name}", "Add Root Node")
    
    def _on_add_child_node(self):
        """Add a child node to selected node."""
        selected_node = self.treeview.SelectedNode
        if not selected_node:
            MessageBox.Show("Please select a parent node first", "Add Child Node")
            return
        
        node_name = f"New Item {len(selected_node.Nodes) + 1}"
        new_node = TreeNode(node_name, 3)
        selected_node.Nodes.Add(new_node)
        selected_node.Expand()
        self._update_statistics()
        MessageBox.Show(f"Added child node: {node_name}", "Add Child Node")
    
    def _on_add_sibling_node(self):
        """Add a sibling node to selected node."""
        selected_node = self.treeview.SelectedNode
        if not selected_node:
            MessageBox.Show("Please select a node first", "Add Sibling Node")
            return
        
        parent = selected_node.Parent
        node_name = f"Sibling {selected_node.Index + 2}"
        new_node = TreeNode(node_name, selected_node.ImageIndex)
        
        if parent:
            parent.Nodes.Add(new_node)
        else:
            self.treeview.Nodes.Add(new_node)
        
        self._update_statistics()
        MessageBox.Show(f"Added sibling node: {node_name}", "Add Sibling Node")
    
    def _on_rename_node(self):
        """Rename selected node."""
        selected_node = self.treeview.SelectedNode
        if not selected_node:
            MessageBox.Show("Please select a node to rename", "Rename Node")
            return
        
        # In a real app, show an input dialog
        MessageBox.Show("Rename functionality would show an input dialog here", "Rename Node")
    
    def _on_delete_node(self):
        """Delete selected node."""
        selected_node = self.treeview.SelectedNode
        if not selected_node:
            MessageBox.Show("Please select a node to delete", "Delete Node")
            return
        
        node_name = selected_node.Text
        selected_node.Remove()
        self._update_statistics()
        self.lbl_status.Text = f"Deleted: {node_name}"
    
    def _on_search_node(self, sender, e):
        """Search for nodes containing search text."""
        search_text = self.txt_search.Text.strip().lower()
        if not search_text:
            MessageBox.Show("Please enter search text", "Search")
            return
        
        found_nodes = self._search_nodes_recursive(self.treeview.Nodes, search_text)
        
        if found_nodes:
            # Select and expand to first found node
            first_node = found_nodes[0]
            self.treeview.SelectedNode = first_node
            
            # Expand parent nodes
            parent = first_node.Parent
            while parent:
                parent.Expand()
                parent = parent.Parent
            
            MessageBox.Show(f"Found {len(found_nodes)} matching node(s)", "Search Results")
        else:
            MessageBox.Show("No matching nodes found", "Search Results")
    
    def _search_nodes_recursive(self, nodes, search_text):
        """Recursively search for nodes containing text."""
        found = []
        for node in nodes:
            if search_text in node.Text.lower():
                found.append(node)
            found.extend(self._search_nodes_recursive(node.Nodes, search_text))
        return found
    
    def _on_update_statistics(self, sender=None, e=None):
        """Update tree statistics."""
        self._update_statistics()
        MessageBox.Show("Statistics updated", "Update Statistics")
    
    def _update_statistics(self):
        """Calculate and display tree statistics."""
        total_nodes = self._count_all_nodes(self.treeview.Nodes)
        root_count = len(self.treeview.Nodes)
        max_depth = self._get_max_depth(self.treeview.Nodes, 0)
        
        self.lbl_stats.Text = f"Total Nodes: {total_nodes}\nRoot Nodes: {root_count}\nMax Depth: {max_depth}"
    
    def _count_all_nodes(self, nodes):
        """Recursively count all nodes."""
        count = len(nodes)
        for node in nodes:
            count += self._count_all_nodes(node.Nodes)
        return count
    
    def _get_max_depth(self, nodes, current_depth):
        """Recursively get maximum depth."""
        if not nodes:
            return current_depth
        max_d = current_depth
        for node in nodes:
            depth = self._get_max_depth(node.Nodes, current_depth + 1)
            max_d = max(max_d, depth)
        return max_d


def main():
    """Application entry point."""
    app = TreeViewExampleForm()
    Application.Run(app)


if __name__ == '__main__':
    main()
