"""
Dialogs Example

This example demonstrates all available dialog controls in WinFormPy:

- ColorDialog (color selection)
- FontDialog (font selection)
- OpenFileDialog (file opening)
- SaveFileDialog (file saving)
- PageSetupDialog (page setup for printing)
- PrintDialog (printer selection)
- PrintPreviewDialog (print preview)
- MessageBox (message display)
- InputBox (text input)
- Font and Color classes (programmatic usage)
"""

from winformpy import (
    Form, Button, Label, Panel, TextBox,
    ColorDialog, FontDialog, OpenFileDialog, SaveFileDialog,
    PageSetupDialog, PrintDialog, PrintPreviewDialog,
    MessageBox, InputBox,
    DialogResult, Application,
    Font, Color, FontStyle, DockStyle
)



def main():
    # =========================================================================
    # Create main form
    # =========================================================================
    form = Form({
        'Text': 'Dialogs Example',
        'Width': 800,
        'Height': 600,
        'StartPosition': 'CenterScreen'
    })
    form.ApplyLayout()
    
    # =========================================================================
    # Title Panel
    # =========================================================================
    title_panel = Panel(form, {
        'Dock': DockStyle.Top,
        'Height': 50,
        'BackColor': '#0078D4'
    })
    
    title_label = Label(title_panel, {
        'Text': 'All Dialogs Demo',
        'Left': 20,
        'Top': 12,
        'AutoSize': True,
        'Font': Font('Segoe UI', 16, FontStyle.Bold),
        'ForeColor': '#FFFFFF',
        'BackColor': '#0078D4'
    })
    
    # =========================================================================
    # Main content panel
    # =========================================================================
    content_panel = Panel(form, {
        'Dock': DockStyle.Fill,
        'BackColor': '#FFFFFF',
        'Padding': 10
    })
    
    # Info label
    lbl_info = Label(content_panel, {
        'Text': 'Click buttons to test dialogs.',
        'Top': 10,
        'Left': 10,
        'AutoSize': True
    })
    
    # Result TextBox
    txt_result = TextBox(content_panel, {
        'Multiline': True,
        'ScrollBars': 'Vertical',
        'Top': 40,
        'Left': 10,
        'Width': 460,
        'Height': 100
    })
    
    def log(msg):
        """Add message to result textbox."""
        current = txt_result.Text
        txt_result.Text = current + msg + '\r\n'
    
    # =========================================================================
    # Dialog Instances
    # =========================================================================
    color_dialog = ColorDialog()
    font_dialog = FontDialog()
    open_file_dialog = OpenFileDialog()
    save_file_dialog = SaveFileDialog()
    page_setup_dialog = PageSetupDialog()
    print_dialog = PrintDialog()
    print_preview_dialog = PrintPreviewDialog()
    
    # =========================================================================
    # Row 1: Common Dialogs
    # =========================================================================
    y_start = 160
    y_step = 40
    
    btn_color = Button(content_panel, {
        'Text': 'Color Dialog',
        'Top': y_start,
        'Left': 10
    })
    
    btn_font = Button(content_panel, {
        'Text': 'Font Dialog',
        'Top': y_start,
        'Left': 120
    })
    
    btn_open = Button(content_panel, {
        'Text': 'Open File',
        'Top': y_start,
        'Left': 230
    })
    
    btn_save = Button(content_panel, {
        'Text': 'Save File',
        'Top': y_start,
        'Left': 340
    })
    
    # =========================================================================
    # Row 2: Print Dialogs
    # =========================================================================
    y_start += y_step
    
    btn_page_setup = Button(content_panel, {
        'Text': 'Page Setup',
        'Top': y_start,
        'Left': 10
    })
    
    btn_print = Button(content_panel, {
        'Text': 'Print Dialog',
        'Top': y_start,
        'Left': 120
    })
    
    btn_preview = Button(content_panel, {
        'Text': 'Print Preview',
        'Top': y_start,
        'Left': 230
    })
    
    # =========================================================================
    # Row 3: MessageBox & InputBox
    # =========================================================================
    y_start += y_step
    
    btn_msgbox = Button(content_panel, {
        'Text': 'MessageBox',
        'Top': y_start,
        'Left': 10
    })
    
    btn_inputbox = Button(content_panel, {
        'Text': 'InputBox',
        'Top': y_start,
        'Left': 120
    })
    
    btn_test_classes = Button(content_panel, {
        'Text': 'Test Font/Color Classes',
        'Top': y_start,
        'Left': 230,
        'Width': 140
    })
    
    # =========================================================================
    # Event Handlers
    # =========================================================================
    
    def on_color_click(sender=None, e=None):
        if color_dialog.ShowDialog() == DialogResult.OK:
            color = color_dialog.Color
            log(f'Color Selected: {color} (R={color.R}, G={color.G}, B={color.B})')
            form.BackColor = color
        else:
            log('Color Dialog Cancelled')
    
    def on_font_click(sender=None, e=None):
        if font_dialog.ShowDialog(form) == DialogResult.OK:
            font = font_dialog.Font
            style_info = []
            if font.Bold: style_info.append('Bold')
            if font.Italic: style_info.append('Italic')
            if font.Underline: style_info.append('Underline')
            if font.Strikeout: style_info.append('Strikeout')
            style_str = ' | '.join(style_info) if style_info else 'Regular'
            log(f'Font Selected: {font.Name}, {font.Size}pt, Style: {style_str}')
            lbl_info.Font = font
        else:
            log('Font Dialog Cancelled')
    
    def on_open_click(sender=None, e=None):
        open_file_dialog.Filter = 'Text Files|*.txt|All Files|*.*'
        open_file_dialog.Title = 'Select a Text File'
        if open_file_dialog.ShowDialog():
            log(f'File Opened: {open_file_dialog.FileName}')
        else:
            log('Open File Cancelled')
    
    def on_save_click(sender=None, e=None):
        save_file_dialog.Filter = 'Text Files|*.txt|All Files|*.*'
        save_file_dialog.Title = 'Save Text File'
        if save_file_dialog.ShowDialog():
            log(f'File Saved: {save_file_dialog.FileName}')
        else:
            log('Save File Cancelled')
    
    def on_page_setup_click(sender=None, e=None):
        if page_setup_dialog.ShowDialog() == DialogResult.OK:
            log(f'Page Setup OK: {page_setup_dialog.PaperSize}, {page_setup_dialog.Orientation}, Margins: {page_setup_dialog.Margins}')
        else:
            log('Page Setup Cancelled')
    
    def on_print_click(sender=None, e=None):
        if print_dialog.ShowDialog() == DialogResult.OK:
            log(f'Print Dialog OK: Printer={print_dialog.PrinterName}, Copies={print_dialog.Copies}')
        else:
            log('Print Dialog Cancelled')
    
    def on_preview_click(sender=None, e=None):
        if print_preview_dialog.ShowDialog() == DialogResult.OK:
            log('Print Preview OK')
        else:
            log('Print Preview Cancelled')
    
    def on_msgbox_click(sender=None, e=None):
        result = MessageBox.Show(
            'This is a test message box.\nDo you want to continue?',
            'MessageBox Test',
            'YesNoCancel',
            'Question'
        )
        log(f'MessageBox Result: {result}')
    
    def on_inputbox_click(sender=None, e=None):
        result = InputBox.Show(
            'Please enter your name:',
            'InputBox Test',
            'User'
        )
        if result:
            log(f'InputBox Result: {result}')
        else:
            log('InputBox Cancelled or Empty')
    
    def on_test_classes_click(sender=None, e=None):
        """Demonstrate programmatic use of Font, Color, and FontStyle classes."""
        log('\n=== Testing Font & Color Classes ===')
        
        # Test Color class
        log('\n--- Color Examples ---')
        color1 = Color(Color.Red)
        log(f'Color(Color.Red): {color1} (R={color1.R}, G={color1.G}, B={color1.B})')
        
        color2 = Color.FromRgb(100, 150, 200)
        log(f'Color.FromRgb(100,150,200): {color2} (R={color2.R}, G={color2.G}, B={color2.B})')
        
        color3 = Color.FromHex('#FF8800')
        log(f"Color.FromHex('#FF8800'): {color3} (R={color3.R}, G={color3.G}, B={color3.B})")
        
        color4 = Color.FromName('blue')
        log(f"Color.FromName('blue'): {color4} (R={color4.R}, G={color4.G}, B={color4.B})")
        
        # Test Font class
        log('\n--- Font Examples ---')
        font1 = Font('Arial', 12, FontStyle.Bold)
        log(f"Font('Arial', 12, Bold): {font1}")
        
        font2 = Font('Courier New', 10, FontStyle.Bold | FontStyle.Italic)
        log(f'Font with Bold|Italic: {font2}')
        
        font3 = Font.FromSystemFont('Default')
        log(f'System Font: {font3}')
        
        # Apply to label temporarily
        lbl_info.Font = font2
        lbl_info.ForeColor = color3
        log('\nLabel updated with custom font and color!')
    
    # =========================================================================
    # Bind Events
    # =========================================================================
    btn_color.Click = on_color_click
    btn_font.Click = on_font_click
    btn_open.Click = on_open_click
    btn_save.Click = on_save_click
    btn_page_setup.Click = on_page_setup_click
    btn_print.Click = on_print_click
    btn_preview.Click = on_preview_click
    btn_msgbox.Click = on_msgbox_click
    btn_inputbox.Click = on_inputbox_click
    btn_test_classes.Click = on_test_classes_click
    
    # =========================================================================
    # Show the form
    # =========================================================================
    Application.Run(form)


if __name__ == '__main__':
    main()
