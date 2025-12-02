"""
Example of using system fonts and colors functions in winformpy_tools
"""

import sys
import os
import importlib.util

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lib_dir = os.path.join(parent_dir, "lib")
sys.path.insert(0, parent_dir)

# Import winformpy.py
module_path = os.path.join(lib_dir, "winformpy.py")
spec = importlib.util.spec_from_file_location("winform_py", module_path)
winform_py = importlib.util.module_from_spec(spec)
spec.loader.exec_module(winform_py)

# Import winformpy_tools.py
tools_path = os.path.join(lib_dir, "winformpy_tools.py")
spec_tools = importlib.util.spec_from_file_location("winform_py_tools", tools_path)
winform_py_tools = importlib.util.module_from_spec(spec_tools)
spec_tools.loader.exec_module(winform_py_tools)

# Extract classes/functions
Form = winform_py.Form
Label = winform_py.Label
Button = winform_py.Button
TextBox = winform_py.TextBox
Panel = winform_py.Panel
ListBox = winform_py.ListBox
MessageBox = winform_py.MessageBox

FontManager = winform_py_tools.FontManager
ColorManager = winform_py_tools.ColorManager


def main():
    # Create main form
    form = Form()
    form.Text = "Demo: System Fonts and Colors"
    form.Width = 700
    form.Height = 600
    form.StartPosition = "CenterScreen"
    
    # ===== SECTION 1: System fonts information =====
    lbl_title1 = Label(form, {
        'Text': '📝 System Fonts:',
        'Left': 20,
        'Top': 20,
        'Width': 300,
        'Font': ('Segoe UI', 11, 'bold')
    })
    
    # Get all system fonts
    system_fonts = FontManager.get_system_fonts()
    
    y_pos = 50
    for font_name, font_tuple in system_fonts.items():
        lbl = Label(form, {
            'Text': f'{font_name}: {font_tuple}',
            'Left': 30,
            'Top': y_pos,
            'Width': 300,
            'Font': font_tuple  # Apply the system font
        })
        y_pos += 25
    
    # ===== SECTION 2: System colors =====
    lbl_title2 = Label(form, {
        'Text': '🎨 System Colors:',
        'Left': 350,
        'Top': 20,
        'Width': 300,
        'Font': ('Segoe UI', 11, 'bold')
    })
    
    # Get all system colors
    system_colors = ColorManager.get_system_colors()
    
    y_pos = 50
    for color_name, color_value in system_colors.items():
        # Panel with the color
        panel = Panel(form, {
            'Left': 360,
            'Top': y_pos,
            'Width': 30,
            'Height': 20,
            'BackColor': color_value
        })
        
        # Label with the color name
        lbl = Label(form, {
            'Text': f'{color_name}: {color_value}',
            'Left': 400,
            'Top': y_pos,
            'Width': 250,
            'Font': FontManager.get_system_font('default')
        })
        y_pos += 25
    
    # ===== SECTION 3: Practical example =====
    lbl_title3 = Label(form, {
        'Text': '✨ Practical Application:',
        'Left': 20,
        'Top': 360,
        'Width': 660,
        'Font': ('Segoe UI', 11, 'bold')
    })
    
    # TextBox with system font
    txt = TextBox(form, {
        'Left': 20,
        'Top': 390,
        'Width': 300,
        'Font': FontManager.get_system_font('text'),
        'BackColor': ColorManager.get_system_color('window'),
        'ForeColor': ColorManager.get_system_color('text')
    })
    txt.Text = "TextBox with system fonts"
    
    # Button with system colors
    btn1 = Button(form, {
        'Text': 'Button with system colors',
        'Left': 340,
        'Top': 390,
        'Width': 200,
        'Font': FontManager.get_system_font('default'),
        'BackColor': ColorManager.get_system_color('button')
    })
    
    def show_colors_info():
        bg = ColorManager.get_system_color('button')
        fg = ColorManager.get_system_color('text')
        MessageBox.Show(f"This button uses system colors:\nBackground: {bg}\nText: {fg}", "Color Information")
        
    btn1.Click = show_colors_info
    
    # ListBox with all available fonts
    lbl_fonts = Label(form, {
        'Text': 'All available fonts:',
        'Left': 20,
        'Top': 430,
        'Width': 300,
        'Font': FontManager.get_system_font('default')
    })
    
    lst_fonts = ListBox(form, {
        'Left': 20,
        'Top': 455,
        'Width': 300,
        'Height': 100,
        'Font': FontManager.get_system_font('fixed')
    })
    
    # Fill the ListBox with available fonts
    all_fonts = FontManager.get_all_available_fonts()
    for font_name in all_fonts[:20]:  # Show only the first 20
        lst_fonts.Items.Add(font_name)
    
    # Informational label
    lbl_info = Label(form, {
        'Text': f'Total available fonts: {len(all_fonts)}',
        'Left': 340,
        'Top': 455,
        'Width': 300,
        'Font': FontManager.get_system_font('small_caption'),
        'ForeColor': ColorManager.get_system_color('gray_text')
    })
    
    # Button to change TextBox font
    def change_font():
        selected = lst_fonts.SelectedItem
        if selected:
            txt.Font = (selected, 10)
    
    btn2 = Button(form, {
        'Text': 'Apply selected font',
        'Left': 340,
        'Top': 485,
        'Width': 200,
        'Font': FontManager.get_system_font('default')
    })
    btn2.Click = change_font
    
    # Additional information
    lbl_note = Label(form, {
        'Text': '💡 Use FontManager and ColorManager to get system values',
        'Left': 20,
        'Top': 525,
        'Width': 660,
        'Font': FontManager.get_system_font('tooltip'),
        'BackColor': ColorManager.get_system_color('info'),
        'ForeColor': ColorManager.get_system_color('info_text')
    })
    
    form.ShowDialog()


if __name__ == "__main__":
    main()
