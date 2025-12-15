import sys
import os

# Add the parent directory to sys.path to import winformpy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from winformpy.winformpy import (
    Form, Button, Label, Panel, TextBox,
    ColorDialog, FontDialog, OpenFileDialog, SaveFileDialog,
    PageSetupDialog, PrintDialog, PrintPreviewDialog,
    MessageBox, InputBox,
    DialogResult, Application,
    Font, Color, FontStyle
)

class AllDialogsExampleForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "All Dialogs Example"
        self.Width = 800
        self.Height = 600  # Increased height for more buttons
        self.StartPosition = "CenterScreen"
        
        # --- UI Setup ---
        self.lblInfo = Label(self)
        self.lblInfo.Text = "Click buttons to test dialogs."
        self.lblInfo.Top = 10
        self.lblInfo.Left = 10
        self.lblInfo.AutoSize = True
        
        self.txtResult = TextBox(self, {'Multiline': True, 'ScrollBars': 'Vertical'})
        self.txtResult.Top = 40
        self.txtResult.Left = 10
        self.txtResult.Width = 460
        self.txtResult.Height = 100
        
        # Buttons
        y_start = 160
        y_step = 40
        
        # Row 1: Common Dialogs
        self.btnColor = Button(self)
        self.btnColor.Text = "Color Dialog"
        self.btnColor.Top = y_start
        self.btnColor.Left = 10
        self.btnColor.Click = self.btnColor_Click
        
        self.btnFont = Button(self)
        self.btnFont.Text = "Font Dialog"
        self.btnFont.Top = y_start
        self.btnFont.Left = 120
        self.btnFont.Click = self.btnFont_Click
        
        self.btnOpen = Button(self)
        self.btnOpen.Text = "Open File"
        self.btnOpen.Top = y_start
        self.btnOpen.Left = 230
        self.btnOpen.Click = self.btnOpen_Click
        
        self.btnSave = Button(self)
        self.btnSave.Text = "Save File"
        self.btnSave.Top = y_start
        self.btnSave.Left = 340
        self.btnSave.Click = self.btnSave_Click
        
        y_start += y_step
        
        # Row 2: Print Dialogs
        self.btnPageSetup = Button(self)
        self.btnPageSetup.Text = "Page Setup"
        self.btnPageSetup.Top = y_start
        self.btnPageSetup.Left = 10
        self.btnPageSetup.Click = self.btnPageSetup_Click
        
        self.btnPrint = Button(self)
        self.btnPrint.Text = "Print Dialog"
        self.btnPrint.Top = y_start
        self.btnPrint.Left = 120
        self.btnPrint.Click = self.btnPrint_Click
        
        self.btnPreview = Button(self)
        self.btnPreview.Text = "Print Preview"
        self.btnPreview.Top = y_start
        self.btnPreview.Left = 230
        self.btnPreview.Click = self.btnPreview_Click
        
        y_start += y_step

        # Row 3: MessageBox & InputBox
        self.btnMsgBox = Button(self)
        self.btnMsgBox.Text = "MessageBox"
        self.btnMsgBox.Top = y_start
        self.btnMsgBox.Left = 10
        self.btnMsgBox.Click = self.btnMsgBox_Click

        self.btnInputBox = Button(self)
        self.btnInputBox.Text = "InputBox"
        self.btnInputBox.Top = y_start
        self.btnInputBox.Left = 120
        self.btnInputBox.Click = self.btnInputBox_Click
        
        self.btnTestClasses = Button(self)
        self.btnTestClasses.Text = "Test Font/Color Classes"
        self.btnTestClasses.Top = y_start
        self.btnTestClasses.Left = 230
        self.btnTestClasses.Width = 140
        self.btnTestClasses.Click = self.btnTestClasses_Click
        
        # Dialog Instances
        self.colorDialog = ColorDialog()
        self.fontDialog = FontDialog()
        self.openFileDialog = OpenFileDialog()
        self.saveFileDialog = SaveFileDialog()
        self.pageSetupDialog = PageSetupDialog()
        self.printDialog = PrintDialog()
        self.printPreviewDialog = PrintPreviewDialog()

    def log(self, msg):
        current = self.txtResult.Text
        self.txtResult.Text = current + msg + "\r\n"

    def btnColor_Click(self, sender=None, e=None):
        if self.colorDialog.ShowDialog() == DialogResult.OK:
            color = self.colorDialog.Color
            self.log(f"Color Selected: {color} (R={color.R}, G={color.G}, B={color.B})")
            self.BackColor = color
        else:
            self.log("Color Dialog Cancelled")

    def btnFont_Click(self, sender=None, e=None):
        if self.fontDialog.ShowDialog(self) == DialogResult.OK:
            font = self.fontDialog.Font
            style_info = []
            if font.Bold: style_info.append("Bold")
            if font.Italic: style_info.append("Italic")
            if font.Underline: style_info.append("Underline")
            if font.Strikeout: style_info.append("Strikeout")
            style_str = " | ".join(style_info) if style_info else "Regular"
            self.log(f"Font Selected: {font.Name}, {font.Size}pt, Style: {style_str}")
            self.lblInfo.Font = font
        else:
            self.log("Font Dialog Cancelled")

    def btnOpen_Click(self, sender=None, e=None):
        self.openFileDialog.Filter = "Text Files|*.txt|All Files|*.*"
        self.openFileDialog.Title = "Select a Text File"
        if self.openFileDialog.ShowDialog():
            self.log(f"File Opened: {self.openFileDialog.FileName}")
        else:
            self.log("Open File Cancelled")

    def btnSave_Click(self, sender=None, e=None):
        self.saveFileDialog.Filter = "Text Files|*.txt|All Files|*.*"
        self.saveFileDialog.Title = "Save Text File"
        if self.saveFileDialog.ShowDialog():
            self.log(f"File Saved: {self.saveFileDialog.FileName}")
        else:
            self.log("Save File Cancelled")

    def btnPageSetup_Click(self, sender=None, e=None):
        if self.pageSetupDialog.ShowDialog() == DialogResult.OK:
            self.log(f"Page Setup OK: {self.pageSetupDialog.PaperSize}, {self.pageSetupDialog.Orientation}, Margins: {self.pageSetupDialog.Margins}")
        else:
            self.log("Page Setup Cancelled")

    def btnPrint_Click(self, sender=None, e=None):
        if self.printDialog.ShowDialog() == DialogResult.OK:
            self.log(f"Print Dialog OK: Printer={self.printDialog.PrinterName}, Copies={self.printDialog.Copies}")
        else:
            self.log("Print Dialog Cancelled")

    def btnPreview_Click(self, sender=None, e=None):
        if self.printPreviewDialog.ShowDialog() == DialogResult.OK:
            self.log("Print Preview OK")
        else:
            self.log("Print Preview Cancelled")

    def btnMsgBox_Click(self, sender=None, e=None):
        result = MessageBox.Show(
            "This is a test message box.\nDo you want to continue?",
            "MessageBox Test",
            "YesNoCancel",
            "Question"
        )
        self.log(f"MessageBox Result: {result}")

    def btnInputBox_Click(self, sender=None, e=None):
        result = InputBox.Show(
            "Please enter your name:",
            "InputBox Test",
            "User"
        )
        if result:
            self.log(f"InputBox Result: {result}")
        else:
            self.log("InputBox Cancelled or Empty")

    def btnTestClasses_Click(self, sender=None, e=None):
        """Demonstrate programmatic use of Font, Color, and FontStyle classes."""
        self.log("\n=== Testing Font & Color Classes ===")
        
        # Test Color class
        self.log("\n--- Color Examples ---")
        color1 = Color(Color.Red)
        self.log(f"Color(Color.Red): {color1} (R={color1.R}, G={color1.G}, B={color1.B})")
        
        color2 = Color.FromRgb(100, 150, 200)
        self.log(f"Color.FromRgb(100,150,200): {color2} (R={color2.R}, G={color2.G}, B={color2.B})")
        
        color3 = Color.FromHex("#FF8800")
        self.log(f"Color.FromHex('#FF8800'): {color3} (R={color3.R}, G={color3.G}, B={color3.B})")
        
        color4 = Color.FromName("blue")
        self.log(f"Color.FromName('blue'): {color4} (R={color4.R}, G={color4.G}, B={color4.B})")
        
        # Test Font class
        self.log("\n--- Font Examples ---")
        font1 = Font("Arial", 12, FontStyle.Bold)
        self.log(f"Font('Arial', 12, Bold): {font1}")
        
        font2 = Font("Courier New", 10, FontStyle.Bold | FontStyle.Italic)
        self.log(f"Font with Bold|Italic: {font2}")
        
        font3 = Font.FromSystemFont("Default")
        self.log(f"System Font: {font3}")
        
        # Apply to label temporarily
        self.lblInfo.Font = font2
        self.lblInfo.ForeColor = color3
        self.log("\nLabel updated with custom font and color!")

if __name__ == "__main__":
    form = AllDialogsExampleForm()
    Application.Run(form)
