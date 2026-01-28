"""
ImageList Comprehensive Example - Complete demonstration of ImageList functionality

DESCRIPTION:
    Demonstrates ALL ImageList features in WinFormPy:
    - Creating ImageList with different sizes
    - Adding images from files and PIL
    - Using ImageKey and ImageIndex
    - Integration with ListView (SmallImageList, LargeImageList)
    - Integration with TreeView (normal and selected icons)
    - Integration with TabControl (tab icons)
    - Integration with Button (button icons)
    - Managing images (Add, Clear, Count)

DEPENDENCIES:
    Optional:
    - PIL/Pillow: For creating test images dynamically
      Install: pip install pillow

LAZY IMPORT PATTERN:
    PIL is imported only when needed (inside functions that use it).
    The example will still run without PIL, but some features will be limited.

USAGE:
    python examples/imagelist_comprehensive_example.py

AUTHOR: WinFormPy
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from winformpy.winformpy import (
    Form, Panel, Label, Button, ListView, TreeView, TabControl, TabPage,
    ImageList, DockStyle, AnchorStyles, Font, FontStyle, View,
    ListViewItem, TreeNode, MessageBox, TextImageRelation
)

# Detect PIL availability without importing
try:
    import importlib.util
    PIL_AVAILABLE = importlib.util.find_spec('PIL') is not None
except (ImportError, AttributeError):
    PIL_AVAILABLE = False


def create_colored_image(color_name, color_hex, size=(32, 32)):
    """
    Create a test image with PIL.
    
    Args:
        color_name: Name to display on image
        color_hex: Background color
        size: Image size tuple
        
    Returns:
        PIL.Image or None if PIL not available
    """
    if not PIL_AVAILABLE:
        return None
    
    # Lazy import: only import PIL when actually needed
    from PIL import Image, ImageDraw, ImageFont
    
    img = Image.new('RGB', size, color=color_hex)
    draw = ImageDraw.Draw(img)
    
    # Draw border
    draw.rectangle([0, 0, size[0]-1, size[1]-1], outline='white', width=2)
    
    # Add text if size is big enough
    if size[0] >= 32:
        try:
            font = ImageFont.truetype("arial.ttf", 10)
        except:
            font = ImageFont.load_default()
        
        # Draw text centered
        text = color_name[:3].upper()
        draw.text((size[0]//2, size[1]//2), text, fill='white', anchor='mm', font=font)
    
    return img


class ImageListDemoForm(Form):
    """Main form demonstrating all ImageList features"""
    
    def __init__(self):
        super().__init__()
        
        self.Text = "ImageList - Complete Functionality Demo"
        self.Width = 1200
        self.Height = 850
        self.ApplyLayout()
        
        # Create UI first
        self._create_header()
        self._create_status_panel()
        
        # Then create ImageLists (which updates status)
        self._create_image_lists()
        
        # Finally create tab control with ImageLists
        self._create_tab_control()
    
    def _create_image_lists(self):
        """Create ImageLists with test images"""
        
        # Small icons (16x16) for TreeView and small ListView
        self.small_imagelist = ImageList({'ImageSize': (16, 16)})
        
        # Medium icons (32x32) for buttons and tabs
        self.medium_imagelist = ImageList({'ImageSize': (32, 32)})
        
        # Large icons (64x64) for large ListView
        self.large_imagelist = ImageList({'ImageSize': (64, 64)})
        
        # Define test colors
        colors = [
            ('Red', '#e74c3c'),
            ('Blue', '#3498db'),
            ('Green', '#2ecc71'),
            ('Orange', '#f39c12'),
            ('Purple', '#9b59b6'),
            ('Teal', '#1abc9c'),
            ('Yellow', '#f1c40f'),
            ('Pink', '#e91e63'),
        ]
        
        # Add images to all ImageLists
        for name, color_hex in colors:
            # Small icons (16x16)
            img_small = create_colored_image(name, color_hex, (16, 16))
            if img_small:
                self.small_imagelist.Add(img_small, name.lower())
            
            # Medium icons (32x32)
            img_medium = create_colored_image(name, color_hex, (32, 32))
            if img_medium:
                self.medium_imagelist.Add(img_medium, name.lower())
            
            # Large icons (64x64)
            img_large = create_colored_image(name, color_hex, (64, 64))
            if img_large:
                self.large_imagelist.Add(img_large, name.lower())
        
        # Update status
        self._update_imagelist_status()
    
    def _create_header(self):
        """Create header panel"""
        header = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 80,
            'BackColor': '#2c3e50'
        })
        
        title = Label(header, {
            'Text': 'ImageList - Complete Functionality Demo',
            'Font': Font('Segoe UI', 16, FontStyle.Bold),
            'ForeColor': 'white',
            'BackColor': '#2c3e50',
            'Left': 20,
            'Top': 15,
            'AutoSize': True
        })
        
        subtitle = Label(header, {
            'Text': 'Demonstrating all ImageList features: ListView, TreeView, TabControl, Button integration',
            'Font': Font('Segoe UI', 10),
            'ForeColor': '#bdc3c7',
            'BackColor': '#2c3e50',
            'Left': 20,
            'Top': 50,
            'AutoSize': True
        })
    
    def _create_tab_control(self):
        """Create tab control with different demos"""
        self.tab_control = TabControl(self, {
            'Dock': DockStyle.Fill,
            'ImageList': self.medium_imagelist  # Tabs will use medium icons
        })
        
        # Tab 1: ListView Demo
        tab1 = TabPage(self.tab_control, {
            'Text': 'ListView',
            'ImageKey': 'blue'  # Tab icon
        })
        self._create_listview_demo(tab1)
        
        # Tab 2: TreeView Demo
        tab2 = TabPage(self.tab_control, {
            'Text': 'TreeView',
            'ImageKey': 'green'  # Tab icon
        })
        self._create_treeview_demo(tab2)
        
        # Tab 3: Button Demo
        tab3 = TabPage(self.tab_control, {
            'Text': 'Buttons',
            'ImageKey': 'orange'  # Tab icon
        })
        self._create_button_demo(tab3)
        
        # Tab 4: Management Demo
        tab4 = TabPage(self.tab_control, {
            'Text': 'Management',
            'ImageKey': 'purple'  # Tab icon
        })
        self._create_management_demo(tab4)
    
    def _create_listview_demo(self, parent):
        """Create ListView demonstration"""
        info_panel = Panel(parent, {
            'Dock': DockStyle.Top,
            'Height': 30,
            'BackColor': '#ecf0f1'
        })
        
        info = Label(info_panel, {
            'Text': 'ListView with SmallImageList (16x16) and LargeImageList (64x64)',
            'Left': 10,
            'Top': 7,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9),
            'ForeColor': '#2c3e50'
        })
        
        # View selector
        view_panel = Panel(parent, {
            'Dock': DockStyle.Top,
            'Height': 40
        })
        
        Label(view_panel, {
            'Text': 'View:',
            'Left': 10,
            'Top': 10,
            'AutoSize': True
        })
        
        btn_details = Button(view_panel, {
            'Text': 'Details (16x16)',
            'Left': 60,
            'Top': 5,
            'Width': 120,
            'Height': 30
        })
        btn_details.Click = lambda s, e: self._change_view(View.Details)
        
        btn_list = Button(view_panel, {
            'Text': 'List (16x16)',
            'Left': 190,
            'Top': 5,
            'Width': 120,
            'Height': 30
        })
        btn_list.Click = lambda s, e: self._change_view(View.List)
        
        btn_large = Button(view_panel, {
            'Text': 'Large Icons (64x64)',
            'Left': 320,
            'Top': 5,
            'Width': 140,
            'Height': 30
        })
        btn_large.Click = lambda s, e: self._change_view(View.LargeIcon)
        
        btn_small = Button(view_panel, {
            'Text': 'Small Icons (16x16)',
            'Left': 470,
            'Top': 5,
            'Width': 140,
            'Height': 30
        })
        btn_small.Click = lambda s, e: self._change_view(View.SmallIcon)
        
        # ListView
        self.listview = ListView(parent, {
            'Dock': DockStyle.Fill,
            'SmallImageList': self.small_imagelist,  # 16x16 icons
            'LargeImageList': self.large_imagelist,  # 64x64 icons
            'View': View.Details,
            'FullRowSelect': True,
            'GridLines': True
        })
        
        # Add columns
        self.listview.Columns.Add('Color', 200)
        self.listview.Columns.Add('Type', 150)
        self.listview.Columns.Add('Usage', 300)
        
        # Add items with icons (using ImageKey)
        items_data = [
            ('red', 'Red', 'Primary', 'Error messages, warnings'),
            ('blue', 'Blue', 'Primary', 'Information, links'),
            ('green', 'Green', 'Secondary', 'Success, confirmation'),
            ('orange', 'Orange', 'Accent', 'Warnings, highlights'),
            ('purple', 'Purple', 'Accent', 'Special features'),
            ('teal', 'Teal', 'Secondary', 'Neutral actions'),
            ('yellow', 'Yellow', 'Accent', 'Caution, attention'),
            ('pink', 'Pink', 'Accent', 'Decorative'),
        ]
        
        for icon_key, color, type_, usage in items_data:
            item = ListViewItem()
            item.Text = color  # First column
            item.SubItems = [type_, usage]  # Additional columns
            item.ImageKey = icon_key  # Set icon by key
            self.listview.Items.Add(item)
    
    def _create_treeview_demo(self, parent):
        """Create TreeView demonstration"""
        # Info panel at top
        info_panel = Panel(parent, {
            'Dock': DockStyle.Top,
            'Height': 30,
            'BackColor': '#ecf0f1'
        })
        
        info = Label(info_panel, {
            'Text': 'TreeView with ImageList - Different icons for normal and selected states',
            'Left': 10,
            'Top': 7,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9),
            'ForeColor': '#2c3e50'
        })
        
        # TreeView - positioned below info panel with explicit coordinates
        self.treeview = TreeView(parent, {
            'Left': 0,
            'Top': 30,  # Starts right after the 30px info panel
            'Width': 1170,  # Full width of tab
            'Height': 650,  # Enough height to show all nodes
            'ImageList': self.small_imagelist,
            'ShowLines': True,
            'ShowPlusMinus': True
        })
        
        # Add root nodes with icons
        colors_node = TreeNode('Color Categories')
        colors_node.ImageKey = 'blue'
        colors_node.SelectedImageKey = 'teal'
        self.treeview.Nodes.Add(colors_node)
        
        # Primary colors
        primary = TreeNode('Primary Colors')
        primary.ImageKey = 'purple'
        primary.SelectedImageKey = 'pink'
        colors_node.Nodes.Add(primary)
        
        red_node = TreeNode('Red')
        red_node.ImageKey = 'red'
        red_node.SelectedImageKey = 'orange'
        primary.Nodes.Add(red_node)
        
        blue_node = TreeNode('Blue')
        blue_node.ImageKey = 'blue'
        blue_node.SelectedImageKey = 'teal'
        primary.Nodes.Add(blue_node)
        
        # Secondary colors
        secondary = TreeNode('Secondary Colors')
        secondary.ImageKey = 'green'
        secondary.SelectedImageKey = 'teal'
        colors_node.Nodes.Add(secondary)
        
        green_node = TreeNode('Green')
        green_node.ImageKey = 'green'
        green_node.SelectedImageKey = 'teal'
        secondary.Nodes.Add(green_node)
        
        orange_node = TreeNode('Orange')
        orange_node.ImageKey = 'orange'
        orange_node.SelectedImageKey = 'yellow'
        secondary.Nodes.Add(orange_node)
        
        purple_node = TreeNode('Purple')
        purple_node.ImageKey = 'purple'
        purple_node.SelectedImageKey = 'pink'
        secondary.Nodes.Add(purple_node)
        
        # Expand nodes to show hierarchy
        colors_node.Expand()
        primary.Expand()
        secondary.Expand()
    
    def _create_button_demo(self, parent):
        """Create Button demonstration"""
        info_panel = Panel(parent, {
            'Dock': DockStyle.Top,
            'Height': 30,
            'BackColor': '#ecf0f1'
        })
        
        info = Label(info_panel, {
            'Text': 'Buttons with ImageList icons (32x32)',
            'Left': 10,
            'Top': 7,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9),
            'ForeColor': '#2c3e50'
        })
        
        # Container for buttons
        button_panel = Panel(parent, {
            'Dock': DockStyle.Fill,
            'BackColor': 'white'
        })
        
        # Create buttons with icons
        buttons_data = [
            ('red', 'Delete', 50, 50),
            ('blue', 'Information', 200, 50),
            ('green', 'Save', 350, 50),
            ('orange', 'Warning', 500, 50),
            ('purple', 'Settings', 50, 120),
            ('teal', 'Refresh', 200, 120),
            ('yellow', 'Caution', 350, 120),
            ('pink', 'Favorite', 500, 120),
        ]
        
        for icon_key, text, left, top in buttons_data:
            btn = Button(button_panel, {
                'Text': text,
                'Left': left,
                'Top': top,
                'Width': 130,
                'Height': 50,
                'ImageList': self.medium_imagelist,
                'ImageKey': icon_key,  # Icon from ImageList
                'TextImageRelation': TextImageRelation.ImageBeforeText
            })
            
            # Add click handler
            btn.Click = lambda s, e, t=text: MessageBox.Show(
                f'Clicked: {t}',
                'Button Click',
                'OK',
                'Information'
            )
        
        # Instructions
        Label(button_panel, {
            'Text': 'Click any button to see the ImageKey being used',
            'Left': 50,
            'Top': 200,
            'Font': Font('Segoe UI', 9, FontStyle.Italic),
            'ForeColor': '#7f8c8d',
            'AutoSize': True
        })
    
    def _create_management_demo(self, parent):
        """Create ImageList management demonstration"""
        info_panel = Panel(parent, {
            'Dock': DockStyle.Top,
            'Height': 30,
            'BackColor': '#ecf0f1'
        })
        
        info = Label(info_panel, {
            'Text': 'ImageList Management - Add, Clear, Count',
            'Left': 10,
            'Top': 7,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9),
            'ForeColor': '#2c3e50'
        })
        
        # Controls panel
        controls = Panel(parent, {
            'Dock': DockStyle.Top,
            'Height': 120,
            'BackColor': '#f8f9fa'
        })
        
        # Title
        Label(controls, {
            'Text': 'Image Management:',
            'Left': 20,
            'Top': 10,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9, FontStyle.Bold),
            'ForeColor': '#2c3e50'
        })
        
        btn_add = Button(controls, {
            'Text': 'Add Random Image',
            'Left': 20,
            'Top': 35,
            'Width': 150,
            'Height': 30,
            'BackColor': '#28a745',
            'ForeColor': 'white'
        })
        btn_add.Click = self._add_random_image
        
        btn_clear = Button(controls, {
            'Text': 'Clear & Recreate',
            'Left': 190,
            'Top': 35,
            'Width': 150,
            'Height': 30,
            'BackColor': '#dc3545',
            'ForeColor': 'white'
        })
        btn_clear.Click = self._clear_images
        
        btn_refresh = Button(controls, {
            'Text': 'Refresh Display',
            'Left': 360,
            'Top': 35,
            'Width': 150,
            'Height': 30,
            'BackColor': '#007bff',
            'ForeColor': 'white'
        })
        btn_refresh.Click = lambda s, e: self._update_imagelist_status()
        
        # Status display
        self.status_label = Label(controls, {
            'Text': 'ImageList status will appear here',
            'Left': 20,
            'Top': 75,
            'Width': 700,
            'Height': 35,
            'Font': Font('Segoe UI', 9),
            'ForeColor': '#2c3e50',
            'BackColor': '#f8f9fa'
        })
        
        # ListView to show ImageList contents
        self.management_listview = ListView(parent, {
            'Dock': DockStyle.Fill,
            'SmallImageList': self.small_imagelist,
            'View': View.Details,
            'FullRowSelect': True,
            'GridLines': True
        })
        
        self.management_listview.Columns.Add('Index', 80)
        self.management_listview.Columns.Add('ImageKey', 200)
        self.management_listview.Columns.Add('Size', 100)
        self.management_listview.Columns.Add('ImageList', 150)
    
    def _create_status_panel(self):
        """Create status panel"""
        status = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': 40,
            'BackColor': '#34495e'
        })
        
        self.imagelist_status = Label(status, {
            'Text': '',
            'Left': 20,
            'Top': 10,
            'Width': 1100,
            'Height': 20,
            'Font': Font('Segoe UI', 9),
            'ForeColor': 'white',
            'BackColor': '#34495e'
        })
    
    def _change_view(self, view):
        """Change ListView view mode"""
        self.listview.View = view
        # Force refresh to update display
        if hasattr(self.listview, '_refresh_items'):
            self.listview._refresh_items()
    
    def _add_random_image(self, sender, e):
        """Add a random image to ImageList"""
        if not PIL_AVAILABLE:
            MessageBox.Show(
                'PIL/Pillow is required to create images.',
                'PIL Not Available',
                'OK',
                'Warning'
            )
            return
        
        import random
        colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#f1c40f', '#e91e63']
        color = random.choice(colors)
        
        # Add to all three ImageLists
        key = f'random_{self.small_imagelist.Count()}'
        
        success_count = 0
        
        img_small = create_colored_image('New', color, (16, 16))
        if img_small:
            self.small_imagelist.Add(img_small, key)
            success_count += 1
        
        img_medium = create_colored_image('New', color, (32, 32))
        if img_medium:
            self.medium_imagelist.Add(img_medium, key)
            success_count += 1
        
        img_large = create_colored_image('New', color, (64, 64))
        if img_large:
            self.large_imagelist.Add(img_large, key)
            success_count += 1
        
        if success_count > 0:
            self._update_imagelist_status()
    
    def _clear_images(self, sender, e):
        """Clear all images from ImageList"""
        result = MessageBox.Show(
            'This will clear all images and recreate the default set. Continue?',
            'Confirm Clear',
            'YesNo',
            'Question'
        )
        
        if result == 'Yes':
            # Clear and recreate
            self._create_image_lists()
            self._update_imagelist_status()
            
            MessageBox.Show(
                'ImageLists cleared and recreated',
                'Cleared',
                'OK',
                'Information'
            )
    
    def _update_imagelist_status(self):
        """Update status display"""
        small_count = self.small_imagelist.Count()
        medium_count = self.medium_imagelist.Count()
        large_count = self.large_imagelist.Count()
        
        self.imagelist_status.Text = (
            f'ImageLists: Small (16x16) = {small_count} images | '
            f'Medium (32x32) = {medium_count} images | '
            f'Large (64x64) = {large_count} images'
        )
        
        # Update management ListView if exists
        if hasattr(self, 'management_listview') and hasattr(self, 'status_label'):
            self.management_listview.Items.Clear()
            
            # Iterate over all keys in the ImageList
            for key in self.small_imagelist._images.keys():
                item = ListViewItem()
                item.Text = str(key)
                item.SubItems = [
                    f'Image {key}',
                    '16x16',
                    'Small ImageList'
                ]
                item.ImageKey = str(key)
                self.management_listview.Items.Add(item)
            
            self.status_label.Text = (
                f'Total images in Small ImageList: {small_count} | '
                f'Medium: {medium_count} | Large: {large_count}'
            )


def main():
    """Run the ImageList comprehensive demo."""
    print("=" * 70)
    print("  IMAGELIST COMPREHENSIVE DEMO")
    print("=" * 70)
    print()
    
    if not PIL_AVAILABLE:
        print("⚠️  WARNING: PIL/Pillow is not installed")
        print("\nSome features will be limited without PIL.")
        print("\nTo install PIL, run:")
        print("  pip install pillow")
        print()
        
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
        print()
    
    form = ImageListDemoForm()
    form.Show()


if __name__ == '__main__':
    main()
