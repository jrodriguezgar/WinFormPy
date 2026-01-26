"""
PictureBox Example - WinFormPy

This example demonstrates PictureBox control functionality:
- Loading images from files
- Different SizeMode options (Normal, StretchImage, AutoSize, CenterImage, Zoom)
- Image manipulation (rotation, flip)
- Creating images programmatically
- Click events on images
- Image borders and styling
"""

from winformpy import (
    Application, Form, Label, Button, PictureBox, Panel, ComboBox,
    OpenFileDialog, MessageBox, DockStyle, Font, FontStyle
)
from PIL import Image, ImageDraw, ImageFont
import os


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
        
        # Different SizeMode examples
        y = 20
        size_modes = [
            ('Normal', 'Normal'),
            ('StretchImage', 'StretchImage'),
            ('AutoSize', 'AutoSize'),
            ('CenterImage', 'CenterImage'),
            ('Zoom', 'Zoom')
        ]
        
        x = 20
        for mode_name, mode_value in size_modes:
            # Label
            Label(content, {
                'Text': mode_name,
                'Font': Font('Segoe UI', 10, FontStyle.Bold),
                'Left': x,
                'Top': y,
                'Width': 200,
                'TextAlign': 'MiddleCenter'
            })
            
            # PictureBox
            picbox = PictureBox(content, {
                'Left': x,
                'Top': y + 30,
                'Width': 200,
                'Height': 200,
                'BorderStyle': 'FixedSingle',
                'BackColor': 'white',
                'SizeMode': mode_value
            })
            picbox.Click = lambda s, e, m=mode_name: self._on_picturebox_click(m)
            
            # Store reference based on mode
            if mode_name == 'Normal':
                self.pic_normal = picbox
            elif mode_name == 'StretchImage':
                self.pic_stretch = picbox
            elif mode_name == 'AutoSize':
                self.pic_autosize = picbox
            elif mode_name == 'CenterImage':
                self.pic_center = picbox
            elif mode_name == 'Zoom':
                self.pic_zoom = picbox
            
            x += 220
            
            # Move to second row after 3 items
            if mode_name == 'AutoSize':
                x = 20
                y = 260
        
        # Main large PictureBox
        Label(content, {
            'Text': 'Main Image Viewer',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 20,
            'Top': 500,
            'AutoSize': True
        })
        
        self.pic_main = PictureBox(content, {
            'Left': 20,
            'Top': 530,
            'Width': 640,
            'Height': 140,
            'BorderStyle': 'Fixed3D',
            'BackColor': '#f8f9fa',
            'SizeMode': 'Zoom'
        })
        
        # Image info
        self.lbl_image_info = Label(content, {
            'Text': 'No image loaded',
            'Left': 680,
            'Top': 530,
            'Width': 280,
            'Height': 140,
            'BorderStyle': 'FixedSingle',
            'BackColor': 'white',
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
        self.combo_sizemode.SelectedIndex = 4  # Zoom
        self.combo_sizemode.SelectedIndexChanged = self._change_main_sizemode
    
    def _init_footer(self):
        """Initialize footer panel"""
        footer = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': 50,
            'BackColor': '#ecf0f1'
        })
        
        Label(footer, {
            'Text': 'Click on any PictureBox to see which mode it uses',
            'Left': 20,
            'Top': 15,
            'Width': 400,
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
        # Create a simple colored image with text
        img = Image.new('RGB', (400, 300), color='#3498db')
        draw = ImageDraw.Draw(img)
        
        # Draw some shapes
        draw.rectangle([50, 50, 350, 250], outline='white', width=3)
        draw.ellipse([100, 100, 300, 200], fill='#e74c3c', outline='white', width=2)
        
        # Add text
        try:
            # Try to use a nice font
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        text = "WinFormPy\nPictureBox\nDemo"
        draw.text((200, 120), text, fill='white', anchor='mm', font=font, align='center')
        
        # Save to temp file
        temp_path = os.path.join(os.path.expanduser('~'), 'temp_picturebox_demo.png')
        img.save(temp_path)
        
        # Load into all PictureBoxes
        self._load_image_from_path(temp_path)
        
        self.lbl_image_info.Text = (
            "Default Sample Image\n"
            f"Size: {img.width}x{img.height}\n"
            "Format: PNG\n"
            "Mode: RGB"
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
            # Load with PIL to get info
            self.current_image = Image.open(path)
            self.current_image_path = path
            
            # Load into all PictureBoxes
            self.pic_normal.Load(path)
            self.pic_stretch.Load(path)
            self.pic_autosize.Load(path)
            self.pic_center.Load(path)
            self.pic_zoom.Load(path)
            self.pic_main.Load(path)
            
            # Update info
            self.lbl_image_info.Text = (
                f"Filename: {os.path.basename(path)}\n"
                f"Size: {self.current_image.width}x{self.current_image.height}\n"
                f"Format: {self.current_image.format}\n"
                f"Mode: {self.current_image.mode}"
            )
            
        except Exception as ex:
            MessageBox.Show(f'Error loading image: {str(ex)}', 'Error', 'OK', 'Error')
    
    def _create_sample_image(self, sender, e):
        """Create a new sample image"""
        import random
        
        # Create random colored image
        colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
        bg_color = random.choice(colors)
        
        img = Image.new('RGB', (500, 400), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Draw random shapes
        for _ in range(5):
            x1 = random.randint(0, 400)
            y1 = random.randint(0, 300)
            x2 = x1 + random.randint(50, 150)
            y2 = y1 + random.randint(50, 150)
            
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
        
        try:
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
        self.pic_normal.Image = None
        self.pic_stretch.Image = None
        self.pic_autosize.Image = None
        self.pic_center.Image = None
        self.pic_zoom.Image = None
        self.pic_main.Image = None
        
        self.current_image = None
        self.current_image_path = None
        
        self.lbl_image_info.Text = 'No image loaded'
    
    def _change_main_sizemode(self, sender, e):
        """Change SizeMode of main PictureBox"""
        selected = self.combo_sizemode.SelectedItem
        if selected:
            self.pic_main.SizeMode = selected
    
    def _on_picturebox_click(self, mode_name):
        """Handle PictureBox click"""
        MessageBox.Show(
            f'This PictureBox uses SizeMode: {mode_name}\n\n'
            f'Click "Load Image..." to load your own image and see how different SizeModes display it.',
            'SizeMode Info',
            'OK',
            'Information'
        )


def main():
    form = PictureBoxForm()
    Application.Run(form)


if __name__ == '__main__':
    main()
