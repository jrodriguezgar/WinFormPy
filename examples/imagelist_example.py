"""
ImageList Example - WinFormPy

This example demonstrates the ImageList component - a centralized image storage
mechanism used by controls like ListView, TreeView, TabControl, and ToolStrip.

WHAT THIS DEMONSTRATES:
• Creating an ImageList
• Understanding ImageList properties (ImageSize, ColorDepth, Name)
• How ImageList serves as a shared image repository
• ImageList API (Add, Remove, Access by index/key)

NOTE: ImageList works best with PIL (Pillow) installed for image handling.
      Install with: pip install Pillow
"""

import sys
from pathlib import Path

# Add parent directory to path to import winformpy without installation
sys.path.insert(0, str(Path(__file__).parent.parent))

from winformpy import (
    Application, Form, ImageList, Button, Label, 
    Panel, Font, FontStyle, MessageBox
)

try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class ImageListDemoForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "ImageList Component Demo"
        self.Width = 750
        self.Height = 550
        self.StartPosition = "CenterScreen"
        
        self.ApplyLayout()
        
        # Header
        header = Panel(self, {
            'Left': 0,
            'Top': 0,
            'Width': 750,
            'Height': 70,
            'BackColor': '#2c3e50'
        })
        
        Label(header, {
            'Text': 'ImageList Component',
            'Font': Font('Segoe UI', 16, FontStyle.Bold),
            'ForeColor': 'white',
            'BackColor': '#2c3e50',
            'Left': 20,
            'Top': 12,
            'AutoSize': True
        })
        
        Label(header, {
            'Text': 'Centralized image management for Windows Forms controls',
            'ForeColor': '#ecf0f1',
            'BackColor': '#2c3e50',
            'Left': 20,
            'Top': 45,
            'AutoSize': True,
            'Font': Font('Segoe UI', 9)
        })
        
        # Main content area
        content = Panel(self, {
            'Left': 20,
            'Top': 90,
            'Width': 710,
            'Height': 400,
            'BackColor': '#ecf0f1',
            'BorderStyle': 'FixedSingle'
        })
        
        # Info section
        Label(content, {
            'Text': 'What is ImageList?',
            'Font': Font('Segoe UI', 12, FontStyle.Bold),
            'Left': 20,
            'Top': 20,
            'AutoSize': True
        })
        
        info_text = """ImageList is a component that stores a collection of images for use by controls.

Key Features:
  • Centralized Storage - Load images once, use across multiple controls
  • Consistent Sizing - All images resized to ImageSize property
  • Efficient Memory - Images shared across controls, not duplicated
  • Flexible Access - Reference by numeric index or string key
  
Common Uses:
  • ListView icons (SmallImageList, LargeImageList properties)
  • TreeView node icons (ImageList property)
  • TabControl tab icons (ImageList property)
  • ToolStrip button icons (ImageList property)
  • Button images (via ImageIndex/ImageKey)"""
        
        Label(content, {
            'Text': info_text,
            'Left': 20,
            'Top': 50,
            'Width': 670,
            'Height': 180,
            'Font': Font('Segoe UI', 9)
        })
        
        # Demo section
        Label(content, {
            'Text': 'ImageList Demo:',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 20,
            'Top': 245,
            'AutoSize': True
        })
        
        # Create ImageList
        self.image_list = ImageList({
            'ImageSize': (24, 24),
            'ColorDepth': 32,
            'Name': 'DemoIcons'
        })
        
        # Status display
        self.status_label = Label(content, {
            'Text': f'ImageList created: Name="{self.image_list.Name}", Size={self.image_list.ImageSize}, Images=0',
            'Left': 20,
            'Top': 275,
            'Width': 670,
            'Height': 60,
            'ForeColor': '#27ae60',
            'Font': Font('Segoe UI', 9, FontStyle.Bold)
        })
        
        # Action buttons
        Button(content, {
            'Text': '📊 Show Properties',
            'Left': 20,
            'Top': 350,
            'Width': 150,
            'Height': 35,
            'Font': Font('Segoe UI', 10)
        }).Click = self._show_properties
        
        Button(content, {
            'Text': '➕ Add Test Image',
            'Left': 190,
            'Top': 350,
            'Width': 150,
            'Height': 35,
            'Font': Font('Segoe UI', 10)
        }).Click = self._add_test_image
        
        Button(content, {
            'Text': '📋 Usage Examples',
            'Left': 360,
            'Top': 350,
            'Width': 150,
            'Height': 35,
            'Font': Font('Segoe UI', 10)
        }).Click = self._show_usage
        
        Button(content, {
            'Text': '🗑️ Clear Images',
            'Left': 530,
            'Top': 350,
            'Width': 150,
            'Height': 35,
            'Font': Font('Segoe UI', 10)
        }).Click = self._clear_images
        
        # Close button
        Button(self, {
            'Text': 'Close',
            'Left': 630,
            'Top': 502,
            'Width': 100,
            'Height': 32
        }).Click = lambda s, e: self.Close()
    
    def _show_properties(self, sender, e):
        """Display ImageList properties"""
        info = []
        info.append("=== ImageList Properties ===\n")
        info.append(f"Name: {self.image_list.Name}")
        info.append(f"Image Size: {self.image_list.ImageSize[0]} x {self.image_list.ImageSize[1]} pixels")
        info.append(f"Color Depth: {self.image_list.ColorDepth} bits")
        info.append(f"Image Count: {len(self.image_list.Images)}")
        info.append(f"Handle Created: {self.image_list.HandleCreated}")
        info.append(f"\nTransparent Color: {self.image_list.TransparentColor if self.image_list.TransparentColor else 'None'}")
        
        MessageBox.Show('\n'.join(info), 'ImageList Properties', 'OK', 'Information')
    
    def _add_test_image(self, sender, e):
        """Add a test image to the ImageList"""
        if not PIL_AVAILABLE:
            MessageBox.Show(
                'PIL (Pillow) is required to create and add images.\n\n'
                'Install with:\n'
                '  pip install Pillow\n\n'
                'Then you can add images:\n'
                '  img = Image.open("icon.png")\n'
                '  image_list.Images.Add(img, "my_icon")',
                'PIL Required',
                'OK',
                'Warning'
            )
            return
        
        # Create a simple colored square
        colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
        color = colors[len(self.image_list.Images) % len(colors)]
        
        img = Image.new('RGB', (24, 24), color)
        draw = ImageDraw.Draw(img)
        # Draw a border
        draw.rectangle([2, 2, 21, 21], outline='white', width=2)
        
        # Add to ImageList
        key = f'icon_{len(self.image_list.Images)}'
        self.image_list.Images.Add(img, key)
        
        count = len(self.image_list.Images)
        self.status_label.Text = (
            f'✓ Image added successfully!\n'
            f'ImageList now contains {count} image(s)\n'
            f'Last added: key="{key}", color={color}'
        )
    
    def _show_usage(self, sender, e):
        """Show usage examples"""
        examples = """=== ImageList Usage Examples ===

1. CREATE ImageList:
   image_list = ImageList({
       'ImageSize': (16, 16),
       'Name': 'MyIcons'
   })

2. ADD IMAGES:
   # By index (automatic)
   image_list.Images.Add(my_image)
   
   # By key (named)
   image_list.Images.Add(my_image, 'save_icon')

3. USE WITH LISTVIEW:
   listview.SmallImageList = image_list
   item = ListViewItem('Document')
   item.ImageIndex = 0  # or
   item.ImageKey = 'save_icon'

4. USE WITH TREEVIEW:
   treeview.ImageList = image_list
   node = TreeNode('Folder')
   node.ImageIndex = 0
   node.SelectedImageIndex = 1

5. USE WITH TABCONTROL:
   tabcontrol.ImageList = image_list
   tab.ImageIndex = 0

6. ACCESS IMAGES:
   img = image_list.Images[0]      # By index
   img = image_list.Images['key']  # By key
"""
        MessageBox.Show(examples, 'ImageList Usage', 'OK', 'Information')
    
    def _clear_images(self, sender, e):
        """Clear all images from ImageList"""
        if len(self.image_list.Images) == 0:
            MessageBox.Show('ImageList is already empty', 'Clear Images', 'OK', 'Information')
            return
        
        count = len(self.image_list.Images)
        self.image_list.Images.Clear()
        
        self.status_label.Text = f'All {count} image(s) removed from ImageList\nImageList is now empty'
        self.status_label.ForeColor = '#e67e22'


def main():
    form = ImageListDemoForm()
    Application.Run(form)


if __name__ == '__main__':
    main()
