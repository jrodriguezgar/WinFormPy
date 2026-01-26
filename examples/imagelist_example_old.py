"""
ImageList Example - WinFormPy

This example demonstrates the ImageList component:
- Creating an ImageList
- Understanding ImageList properties (ImageSize, ColorDepth)
- How ImageList would work with controls (conceptual)

NOTE: This is a conceptual example. ImageList is designed to work with
ListView, TreeView, and other controls that support image indices.
For this example, we demonstrate the ImageList API and properties.
"""

import sys
from pathlib import Path

# Add parent directory to path to import winformpy without installation
sys.path.insert(0, str(Path(__file__).parent.parent))

from winformpy import (
    Application, Form, ImageList, ListView, Button, Label, 
    Panel, DockStyle, Font, FontStyle, ListViewItem, MessageBox
)

try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class ImageListForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "ImageList Demo"
        self.Width = 700
        self.Height = 500
        self.StartPosition = "CenterScreen"
        
        self.ApplyLayout()
        
        # Header
        header = Panel(self, {
            'Left': 0,
            'Top': 0,
            'Width': 700,
            'Height': 60,
            'BackColor': '#2c3e50'
        })
        
        Label(header, {
            'Text': 'ImageList Component',
            'Font': Font('Segoe UI', 14, FontStyle.Bold),
            'ForeColor': 'white',
            'BackColor': '#2c3e50',
            'Left': 20,
            'Top': 12,
            'AutoSize': True
        })
        
        Label(header, {
            'Text': 'Centralized image management for controls',
            'ForeColor': '#ecf0f1',
            'BackColor': '#2c3e50',
            'Left': 20,
            'Top': 38,
            'AutoSize': True
        })
        
        # Info panel
        info_panel = Panel(self, {
            'Left': 20,
            'Top': 80,
            'Width': 660,
            'Height': 180,
            'BackColor': '#ecf0f1',
            'BorderStyle': 'FixedSingle'
        })
        
        Label(info_panel, {
            'Text': 'What is ImageList?',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 15,
            'Top': 10,
            'AutoSize': True
        })
        
        info_text = """ImageList is a component that stores a collection of images that can be used by 
other controls like ListView, TreeView, TabControl, ToolStrip, etc.

Key Features:
• Centralized image storage - Load images once, use in multiple controls
• Consistent sizing - All images resized to ImageSize property
• Index-based or key-based access - Reference images by number or name
• Memory efficient - Shared across controls

Common Properties:
• ImageSize - Size of images (e.g., 16x16, 32x32, 48x48)
• ColorDepth - Color depth in bits (8, 16, 24, 32)
• Images - Collection to add/remove images"""
        
        Label(info_panel, {
            'Text': info_text,
            'Left': 15,
            'Top': 35,
            'Width': 630,
            'Height': 135,
            'Font': Font('Segoe UI', 9)
        })
        
        # Create ImageList demo
        demo_panel = Panel(self, {
            'Left': 20,
            'Top': 275,
            'Width': 660,
            'Height': 150,
            'BackColor': 'white',
            'BorderStyle': 'FixedSingle'
        })
        
        Label(demo_panel, {
            'Text': 'ImageList Demo:',
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'Left': 15,
            'Top': 15,
            'AutoSize': True
        })
        
        # Create ImageList
        self.image_list = ImageList({
            'ImageSize': (16, 16),
            'Name': 'DemoIcons'
        })
        
        # Status label
        self.status_label = Label(demo_panel, {
            'Text': 'ImageList created with ImageSize: (16, 16)',
            'Left': 15,
            'Top': 45,
            'Width': 630,
            'Height': 60,
            'ForeColor': '#27ae60',
            'Font': Font('Segoe UI', 9)
        })
        
        # Buttons
        Button(demo_panel, {
            'Text': 'Show ImageList Info',
            'Left': 15,
            'Top': 110,
            'Width': 150,
            'Height': 30
        }).Click = self._show_info
        
        Button(demo_panel, {
            'Text': 'Try Add Image (PIL)',
            'Left': 175,
            'Top': 110,
            'Width': 150,
            'Height': 30
        }).Click = self._try_add_image
        
        # Close button
        Button(self, {
            'Text': 'Close',
            'Left': 580,
            'Top': 440,
            'Width': 100,
            'Height': 30
        }).Click = lambda s, e: self.Close()
    
    def _show_info(self, sender, e):
        """Show ImageList information"""
        info = []
        info.append(f"Name: {self.image_list.Name}")
        info.append(f"ImageSize: {self.image_list.ImageSize}")
        info.append(f"ColorDepth: {self.image_list.ColorDepth}")
        info.append(f"Image Count: {len(self.image_list.Images)}")
        info.append("")
        info.append("ImageList is ready to be used with:")
        info.append("  • ListView (SmallImageList, LargeImageList)")
        info.append("  • TreeView (ImageList property)")
        info.append("  • TabControl (ImageList property)")
        info.append("  • ToolStrip and other controls")
        
        MessageBox.Show('\n'.join(info), 'ImageList Information', 'OK', 'Information')
    
    def _try_add_image(self, sender, e):
        """Try to add an image to ImageList"""
        if not PIL_AVAILABLE:
            MessageBox.Show(
                'PIL (Pillow) is not installed.\n\n'
                'To use ImageList with real images, install Pillow:\n'
                'pip install Pillow\n\n'
                'Then you can add images with:\n'
                'image = Image.open("icon.png")\n'
                'image_list.Images.Add(image, "icon_name")',
                'PIL Required',
                'OK',
                'Warning'
            )
            return
        
        # Create a simple test image
        img = Image.new('RGB', (16, 16), '#3498db')
        draw = ImageDraw.Draw(img)
        draw.rectangle([4, 4, 12, 12], fill='#e74c3c')
        
        self.image_list.Images.Add(img, 'test_icon')
        
        self.status_label.Text = (
            f'✓ Image added successfully!\n'
            f'ImageList now contains {len(self.image_list.Images)} image(s)\n'
            f'Access by key: image_list.Images["test_icon"]'
        )
        self.status_label.ForeColor = '#27ae60'
            return handler
        
        btn.Click = make_handler(text)


def create_info_tab(tab_control, image_list):
    """Create Info tab showing ImageList properties."""
    tab = TabPage(tab_control, {'Text': 'ImageList Info'})
    
    # Title
    title_panel = Panel(tab, {
        'Height': 70,
        'BackColor': '#F0F0F0'
    })
    title_panel.Dock = DockStyle.Top
    
    Label(title_panel, {
        'Text': 'ImageList Properties',
        'Font': Font('Segoe UI', 12, FontStyle.Bold),
        'Top': 15,
        'Left': 20,
        'AutoSize': True,
        'ForeColor': '#0078D4',
        'BackColor': '#F0F0F0'
    })
    
    Label(title_panel, {
        'Text': 'Information about the ImageList object',
        'Top': 42,
        'Left': 20,
        'AutoSize': True,
        'ForeColor': '#666666',
        'BackColor': '#F0F0F0',
        'Font': Font('Segoe UI', 9)
    })
    
    # Info panel
    info_panel = Panel(tab, {
        'BackColor': '#FFFFFF',
        'Padding': (30, 30, 30, 30)
    })
    info_panel.Dock = DockStyle.Fill
    
    info_text = f"""ImageList Properties:
    
Name: {image_list.Name}
Image Size: {image_list.ImageSize}
Image Count: {image_list.Count()}
Color Depth: {image_list.ColorDepth} bits
Handle: {image_list.Handle}
Handle Created: {image_list.HandleCreated}

Usage:

1. Creating an ImageList:
   image_list = ImageList({{'ImageSize': (16, 16), 'Name': 'myIcons'}})

2. Adding images:
   image_list.Images.Add(my_photo_image, 'icon1')
   image_list.Images.Add(my_photo_image)  # Auto-indexed as 0, 1, 2...

3. Using with controls:
   listview.SmallImageList = image_list
   treeview.ImageList = image_list
   
4. Accessing images:
   image = image_list.GetImage(0)  # By index
   image = image_list.GetImage('icon1')  # By key
   
5. Collection operations:
   count = len(image_list.Images)
   image_list.Images.Clear()
   image_list.Images.RemoveByKey('icon1')
   image_list.Images.RemoveAt(0)
"""
    
    Label(info_panel, {
        'Text': info_text,
        'Left': 0,
        'Top': 0,
        'Width': 800,
        'Height': 500,
        'Font': Font('Consolas', 9),
        'ForeColor': '#333333',
        'BackColor': '#FFFFFF',
        'TextAlign': 'TopLeft'
    })


def main():
    """Application entry point."""
    # Create main form
    form = Form({
        'Text': 'WinFormPy ImageList Example',
        'Width': 950,
        'Height': 720,
        'StartPosition': 'CenterScreen'
    })
    form.ApplyLayout()
    
    # Top panel
    top_panel = Panel(form, {
        'Height': 60,
        'BackColor': '#0078D4'
    })
    top_panel.Dock = DockStyle.Top
    
    Label(top_panel, {
        'Text': 'IMAGELIST DEMONSTRATION',
        'Left': 20,
        'Top': 10,
        'AutoSize': True,
        'Font': Font('Segoe UI', 16, FontStyle.Bold),
        'ForeColor': '#FFFFFF',
        'BackColor': '#0078D4'
    })
    
    Label(top_panel, {
        'Text': 'Managing and displaying images with ImageList',
        'Left': 20,
        'Top': 38,
        'AutoSize': True,
        'Font': Font('Segoe UI', 9),
        'ForeColor': '#E0E0E0',
        'BackColor': '#0078D4'
    })
    
    # Bottom panel
    bottom_panel = Panel(form, {
        'Height': 35,
        'BackColor': '#34495E'
    })
    bottom_panel.Dock = DockStyle.Bottom
    
    Label(bottom_panel, {
        'Text': '⚡ ImageList - Centralized image management for controls',
        'Left': 15,
        'Top': 8,
        'AutoSize': True,
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9),
        'BackColor': '#34495E'
    })
    
    # Create sample images (if PIL available)
    sample_images = create_sample_images()
    
    # Create ImageList
    image_list = ImageList({
        'ImageSize': (16, 16),
        'Name': 'MainIcons'
    })
    
    # Add images to ImageList if PIL is available
    if sample_images:
        for img in sample_images:
            image_list.Images.Add(img)
        
        Label(top_panel, {
            'Text': f'✓ {len(sample_images)} images loaded in ImageList',
            'Left': 550,
            'Top': 25,
            'AutoSize': True,
            'Font': Font('Segoe UI', 8),
            'ForeColor': '#A0FFA0',
            'BackColor': '#0078D4'
        })
    else:
        Label(top_panel, {
            'Text': '⚠ PIL not available - using emojis as placeholders',
            'Left': 550,
            'Top': 25,
            'AutoSize': True,
            'Font': Font('Segoe UI', 8),
            'ForeColor': '#FFFF00',
            'BackColor': '#0078D4'
        })
    
    # Main panel with TabControl
    main_panel = Panel(form, {
        'BackColor': '#F5F5F5'
    })
    main_panel.Dock = DockStyle.Fill
    
    # TabControl
    tabs = TabControl(main_panel, {
        'Dock': DockStyle.Fill,
        'Font': Font('Segoe UI', 9)
    })
    
    # Create tabs
    create_listview_tab(tabs, image_list)
    create_treeview_tab(tabs, image_list)
    create_buttons_tab(tabs, image_list)
    create_info_tab(tabs, image_list)
    
    # Run application
    Application.Run(form)


if __name__ == '__main__':
    main()
