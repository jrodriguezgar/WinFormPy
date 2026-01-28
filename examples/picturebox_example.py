"""
PictureBox Example - WinFormPy

This example demonstrates PictureBox control functionality:
- Loading images from files
- Different SizeMode options (Normal, StretchImage, AutoSize, CenterImage, Zoom)
- Image manipulation (rotation, flip)
- Creating images programmatically
- Click events on images
- Image borders and styling

DEPENDENCIES:
• winformpy (required)
• PIL/Pillow (optional but recommended) - Install with: pip install Pillow

LAZY IMPORT PATTERN:
PIL is only imported when actually needed for image creation/manipulation.
The example will run without PIL but with limited functionality.
"""

from winformpy import (
    Application, Form, Label, Button, PictureBox, Panel, ComboBox,
    OpenFileDialog, MessageBox, DockStyle, Font, FontStyle, PictureBoxSizeMode
)
import os

# Check PIL availability without importing (lazy import pattern)
try:
    import importlib.util
    PIL_AVAILABLE = importlib.util.find_spec('PIL') is not None
except (ImportError, AttributeError):
    PIL_AVAILABLE = False


class PictureBoxForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "PictureBox Demo"
        self.Width = 1200
        self.Height = 800
        self.StartPosition = "CenterScreen"
        
        # Current image path
        self.current_image_path = None
        self.current_image = None
        
        # Store original PictureBox size for restoring after AutoSize
        self.original_pic_width = 800
        self.original_pic_height = 500
        
        # Apply layout before adding controls
        self.ApplyLayout()
        
        self._init_header()
        self._init_main_content()
        self._init_controls_panel()
        self._init_footer()
        
        # Create a default image
        self._create_default_image()
    
    def _init_header(self):
        """Initialize header panel"""
        header = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 60,
            'BackColor': '#2c3e50'
        })
        
        title = Label(header, {
            'Text': 'PictureBox Control Examples',
            'Font': Font('Segoe UI', 16, FontStyle.Bold),
            'ForeColor': 'white',
            'BackColor': '#2c3e50',
            'Left': 20,
            'Top': 15,
            'AutoSize': True
        })
    
    def _init_main_content(self):
        """Initialize main content area with PictureBoxes"""
        content = Panel(self, {
            'Dock': DockStyle.Fill,
            'BackColor': '#ecf0f1'
        })
        
        # Title
        Label(content, {
            'Text': 'Image Viewer - Change SizeMode to see different display options',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 20,
            'Top': 20,
            'Width': 800,
            'AutoSize': False
        })
        
        # Main large PictureBox
        self.pic_main = PictureBox(content, {
            'Left': 20,
            'Top': 60,
            'Width': 800,
            'Height': 500,
            'BorderStyle': 'Fixed3D',
            'BackColor': '#ffffff',
            'SizeMode': PictureBoxSizeMode.Normal
        })
        
        # Image info
        self.lbl_image_info = Label(content, {
            'Text': 'No image loaded\nSizeMode: Normal',
            'Left': 20,
            'Top': 580,
            'Width': 800,
            'Height': 100,
            'BorderStyle': 'FixedSingle',
            'BackColor': 'white',
            'Font': Font('Segoe UI', 9),
            'Padding': (10, 10, 10, 10)
        })
    
    def _init_controls_panel(self):
        """Initialize control panel"""
        panel = Panel(self, {
            'Dock': DockStyle.Right,
            'Width': 220,
            'BackColor': '#34495e'
        })
        
        # Title
        Label(panel, {
            'Text': 'Image Controls',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'ForeColor': 'white',
            'BackColor': '#34495e',
            'Left': 20,
            'Top': 20,
            'AutoSize': True
        })
        
        # Load image button
        btn_load = Button(panel, {
            'Text': 'Load Image...',
            'Left': 20,
            'Top': 60,
            'Width': 180,
            'Height': 35
        })
        btn_load.Click = self._load_image
        
        # Create sample button
        btn_create = Button(panel, {
            'Text': 'Create Sample',
            'Left': 20,
            'Top': 105,
            'Width': 180,
            'Height': 35
        })
        btn_create.Click = self._create_sample_image
        
        # Rotate buttons
        Label(panel, {
            'Text': 'Rotation:',
            'ForeColor': 'white',
            'BackColor': '#34495e',
            'Left': 20,
            'Top': 160,
            'AutoSize': True
        })
        
        btn_rotate_left = Button(panel, {
            'Text': '↶ 90°',
            'Left': 20,
            'Top': 185,
            'Width': 85,
            'Height': 30
        })
        btn_rotate_left.Click = lambda s, e: self._rotate_image(-90)
        
        btn_rotate_right = Button(panel, {
            'Text': '↷ 90°',
            'Left': 115,
            'Top': 185,
            'Width': 85,
            'Height': 30
        })
        btn_rotate_right.Click = lambda s, e: self._rotate_image(90)
        
        # Flip buttons
        Label(panel, {
            'Text': 'Flip:',
            'ForeColor': 'white',
            'BackColor': '#34495e',
            'Left': 20,
            'Top': 235,
            'AutoSize': True
        })
        
        btn_flip_h = Button(panel, {
            'Text': 'Horizontal',
            'Left': 20,
            'Top': 260,
            'Width': 85,
            'Height': 30
        })
        btn_flip_h.Click = lambda s, e: self._flip_image('horizontal')
        
        btn_flip_v = Button(panel, {
            'Text': 'Vertical',
            'Left': 115,
            'Top': 260,
            'Width': 85,
            'Height': 30
        })
        btn_flip_v.Click = lambda s, e: self._flip_image('vertical')
        
        # Clear button
        btn_clear = Button(panel, {
            'Text': 'Clear Image',
            'Left': 20,
            'Top': 320,
            'Width': 180,
            'Height': 35
        })
        btn_clear.Click = self._clear_image
        
        # SizeMode selector for main image
        Label(panel, {
            'Text': 'Main SizeMode:',
            'ForeColor': 'white',
            'BackColor': '#34495e',
            'Left': 20,
            'Top': 380,
            'AutoSize': True
        })
        
        self.combo_sizemode = ComboBox(panel, {
            'Left': 20,
            'Top': 405,
            'Width': 180,
            'DropDownStyle': 'DropDownList'
        })
        self.combo_sizemode.Items.extend(['Normal', 'StretchImage', 'AutoSize', 'CenterImage', 'Zoom'])
        self.combo_sizemode.SelectedIndex = 0  # Normal
        self.combo_sizemode.SelectedIndexChanged = self._change_main_sizemode
    
    def _init_footer(self):
        """Initialize footer panel"""
        footer = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': 50,
            'BackColor': '#ecf0f1'
        })
        
        Label(footer, {
            'Text': 'Use the "Main SizeMode" dropdown to see how different modes display the image',
            'Left': 20,
            'Top': 15,
            'Width': 600,
            'ForeColor': '#666666'
        })
        
        btn_close = Button(footer, {
            'Text': 'Close',
            'Left': 1050,
            'Top': 10,
            'Width': 100,
            'Height': 30
        })
        btn_close.Click = lambda s, e: self.Close()
    
    def _create_default_image(self):
        """Create a default placeholder image"""
        if not PIL_AVAILABLE:
            MessageBox.Show("PIL/Pillow is required to create images.", "PIL Not Available", "OK", "Warning")
            return
        
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a smaller image (300x200) to demonstrate SizeMode differences
        # The PictureBox is 640x140, so this smaller image will show the modes clearly
        img = Image.new('RGB', (300, 200), color='#3498db')
        draw = ImageDraw.Draw(img)
        
        # Draw some shapes
        draw.rectangle([30, 30, 270, 170], outline='white', width=3)
        draw.ellipse([75, 60, 225, 140], fill='#e74c3c', outline='white', width=2)
        
        # Add text
        try:
            # Try to use a nice font
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        text = "WinFormPy\nDemo"
        draw.text((150, 100), text, fill='white', anchor='mm', font=font, align='center')
        
        # Save to temp file
        temp_path = os.path.join(os.path.expanduser('~'), 'temp_picturebox_demo.png')
        img.save(temp_path)
        
        # Load into all PictureBoxes
        self._load_image_from_path(temp_path)
        
        self.lbl_image_info.Text = (
            "Default Sample Image\n"
            f"Size: {img.width}x{img.height}\n"
            "Format: PNG\n"
            "Mode: RGB\n"
            f"SizeMode: {self.combo_sizemode.SelectedItem}"
        )
    
    def _load_image(self, sender, e):
        """Load image from file"""
        dialog = OpenFileDialog()
        dialog.Filter = "Image Files|*.png;*.jpg;*.jpeg;*.gif;*.bmp|All Files|*.*"
        dialog.Title = "Select an Image"
        
        if dialog.ShowDialog() == 'OK':
            self._load_image_from_path(dialog.FileName)
    
    def _load_image_from_path(self, path):
        """Load image from specified path"""
        try:
            if PIL_AVAILABLE:
                from PIL import Image
                # Load with PIL to get info
                self.current_image = Image.open(path)
                self.current_image_path = path
            
            # Load into main PictureBox
            self.pic_main.Load(path)
            
            # Update info
            if PIL_AVAILABLE and self.current_image:
                self.lbl_image_info.Text = (
                    f"Filename: {os.path.basename(path)}\n"
                    f"Size: {self.current_image.width}x{self.current_image.height}\n"
                    f"Format: {self.current_image.format}\n"
                    f"Mode: {self.current_image.mode}\n"
                    f"SizeMode: {self.combo_sizemode.SelectedItem}"
                )
            else:
                self.lbl_image_info.Text = f"Filename: {os.path.basename(path)}\nSizeMode: {self.combo_sizemode.SelectedItem}"
            
        except Exception as ex:
            MessageBox.Show(f'Error loading image: {str(ex)}', 'Error', 'OK', 'Error')
    
    def _create_sample_image(self, sender, e):
        """Create a new sample image"""
        if not PIL_AVAILABLE:
            MessageBox.Show('PIL/Pillow is required to create images.', 'PIL Not Available', 'OK', 'Warning')
            return
        
        from PIL import Image, ImageDraw, ImageFont
        import random
        
        # Create random colored image - smaller size to show SizeMode differences
        colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
        bg_color = random.choice(colors)
        
        img = Image.new('RGB', (350, 250), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Draw random shapes
        for _ in range(5):
            x1 = random.randint(0, 280)
            y1 = random.randint(0, 180)
            x2 = x1 + random.randint(40, 100)
            y2 = y1 + random.randint(40, 100)
            
            shape_type = random.choice(['rect', 'ellipse'])
            color = random.choice(colors)
            
            if shape_type == 'rect':
                draw.rectangle([x1, y1, x2, y2], fill=color, outline='white', width=2)
            else:
                draw.ellipse([x1, y1, x2, y2], fill=color, outline='white', width=2)
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except:
            font = ImageFont.load_default()
        
        draw.text((250, 200), "Sample Image", fill='white', anchor='mm', font=font)
        
        # Save and load
        temp_path = os.path.join(os.path.expanduser('~'), 'temp_sample.png')
        img.save(temp_path)
        self._load_image_from_path(temp_path)
    
    def _rotate_image(self, degrees):
        """Rotate the current image"""
        if self.current_image is None:
            MessageBox.Show('No image loaded', 'Info', 'OK', 'Information')
            return
        
        if not PIL_AVAILABLE:
            MessageBox.Show('PIL/Pillow is required for image rotation.', 'PIL Not Available', 'OK', 'Warning')
            return
        
        try:
            # Rotate the image
            rotated = self.current_image.rotate(-degrees, expand=True)
            
            # Save to temp file
            temp_path = os.path.join(os.path.expanduser('~'), 'temp_rotated.png')
            rotated.save(temp_path)
            
            # Reload
            self._load_image_from_path(temp_path)
            
        except Exception as ex:
            MessageBox.Show(f'Error rotating image: {str(ex)}', 'Error', 'OK', 'Error')
    
    def _flip_image(self, direction):
        """Flip the current image"""
        if self.current_image is None:
            MessageBox.Show('No image loaded', 'Info', 'OK', 'Information')
            return
        
        if not PIL_AVAILABLE:
            MessageBox.Show('PIL/Pillow is required for image flipping.', 'PIL Not Available', 'OK', 'Warning')
            return
        
        try:
            from PIL import Image
            # Flip the image
            if direction == 'horizontal':
                flipped = self.current_image.transpose(Image.FLIP_LEFT_RIGHT)
            else:
                flipped = self.current_image.transpose(Image.FLIP_TOP_BOTTOM)
            
            # Save to temp file
            temp_path = os.path.join(os.path.expanduser('~'), 'temp_flipped.png')
            flipped.save(temp_path)
            
            # Reload
            self._load_image_from_path(temp_path)
            
        except Exception as ex:
            MessageBox.Show(f'Error flipping image: {str(ex)}', 'Error', 'OK', 'Error')
    
    def _clear_image(self, sender, e):
        """Clear all images"""
        self.pic_main.Image = None
        
        self.current_image = None
        self.current_image_path = None
        
        self.lbl_image_info.Text = 'No image loaded'
    
    def _change_main_sizemode(self, sender, e):
        """Change SizeMode of main PictureBox"""
        selected = self.combo_sizemode.SelectedItem
        if selected:
            # Convert string to PictureBoxSizeMode enum
            size_mode_map = {
                'Normal': PictureBoxSizeMode.Normal,
                'StretchImage': PictureBoxSizeMode.StretchImage,
                'AutoSize': PictureBoxSizeMode.AutoSize,
                'CenterImage': PictureBoxSizeMode.CenterImage,
                'Zoom': PictureBoxSizeMode.Zoom
            }
            
            size_mode = size_mode_map.get(selected)
            if size_mode:
                # Restore original size if changing from AutoSize to another mode
                if selected != 'AutoSize':
                    self.pic_main.Width = self.original_pic_width
                    self.pic_main.Height = self.original_pic_height
                    self.pic_main._place_control(self.original_pic_width, self.original_pic_height)
                
                # Use the set_SizeMode method to properly update the control
                self.pic_main.set_SizeMode(size_mode)
                
                # Reload current image to show the effect of the new SizeMode
                if self.current_image_path and os.path.exists(self.current_image_path):
                    self.pic_main.Load(self.current_image_path)
                
                # Update info label to show current mode
                current_info = self.lbl_image_info.Text
                if '\nSizeMode:' in current_info:
                    # Replace existing SizeMode line
                    lines = current_info.split('\n')
                    lines = [line for line in lines if not line.startswith('SizeMode:')]
                    lines.append(f'SizeMode: {selected}')
                    self.lbl_image_info.Text = '\n'.join(lines)
                else:
                    # Add SizeMode info
                    self.lbl_image_info.Text = f'{current_info}\nSizeMode: {selected}'
                
                # Refresh the PictureBox to apply the new SizeMode
                if hasattr(self.pic_main, 'Refresh'):
                    self.pic_main.Refresh()


def main():
    form = PictureBoxForm()
    Application.Run(form)


if __name__ == '__main__':
    main()
