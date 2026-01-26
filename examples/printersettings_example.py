"""
PrinterSettings Example - Demonstrates the use of PrinterSettings class

This example shows:
1. Getting installed printers
2. Creating and initializing PrinterSettings from dictionary
3. Using PrinterSettings with PrintDialog and PageSetupDialog
4. Converting PrinterSettings to/from dictionary
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from winformpy.winformpy import (
    Form, Panel, Button, Label, TextBox, ListBox,
    PrinterSettings, PrintDialog, PageSetupDialog,
    DockStyle, AnchorStyles
)


class PrinterSettingsExampleForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "PrinterSettings Example"
        self.Width = 700
        self.Height = 500
        self.ApplyLayout()
        
        # Initialize PrinterSettings
        self.printer_settings = PrinterSettings()
        
        # OR initialize from dictionary
        # settings_dict = {
        #     'PrinterName': 'Microsoft Print to PDF',
        #     'Copies': 2,
        #     'Duplex': 'Vertical',
        #     'Color': True
        # }
        # self.printer_settings = PrinterSettings(settings_dict)
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the user interface."""
        
        # Top panel - Buttons
        panel_top = Panel(self, {'Dock': DockStyle.Top, 'Height': 100})
        
        btn_show_printers = Button(panel_top, {
            'Text': 'Show Installed Printers',
            'Left': 10,
            'Top': 10,
            'Width': 180
        })
        btn_show_printers.Click = lambda s, e: self._show_installed_printers()
        
        btn_print_dialog = Button(panel_top, {
            'Text': 'Open Print Dialog',
            'Left': 200,
            'Top': 10,
            'Width': 150
        })
        btn_print_dialog.Click = lambda s, e: self._open_print_dialog()
        
        btn_page_setup = Button(panel_top, {
            'Text': 'Open Page Setup',
            'Left': 360,
            'Top': 10,
            'Width': 150
        })
        btn_page_setup.Click = lambda s, e: self._open_page_setup()
        
        btn_to_dict = Button(panel_top, {
            'Text': 'Settings to Dict',
            'Left': 520,
            'Top': 10,
            'Width': 150
        })
        btn_to_dict.Click = lambda s, e: self._settings_to_dict()
        
        btn_from_dict = Button(panel_top, {
            'Text': 'Load from Dict',
            'Left': 10,
            'Top': 50,
            'Width': 150
        })
        btn_from_dict.Click = lambda s, e: self._settings_from_dict()
        
        btn_check_valid = Button(panel_top, {
            'Text': 'Check Validity',
            'Left': 170,
            'Top': 50,
            'Width': 150
        })
        btn_check_valid.Click = lambda s, e: self._check_validity()
        
        btn_is_default = Button(panel_top, {
            'Text': 'Is Default Printer?',
            'Left': 330,
            'Top': 50,
            'Width': 150
        })
        btn_is_default.Click = lambda s, e: self._check_default()
        
        btn_clone = Button(panel_top, {
            'Text': 'Clone Settings',
            'Left': 490,
            'Top': 50,
            'Width': 150
        })
        btn_clone.Click = lambda s, e: self._clone_settings()
        
        # Bottom panel - Output display
        panel_bottom = Panel(self, {'Dock': DockStyle.Fill})
        
        Label(panel_bottom, {
            'Text': 'Current PrinterSettings:',
            'Left': 10,
            'Top': 10,
            'Width': 200
        })
        
        self.txt_output = TextBox(panel_bottom, {
            'Multiline': True,
            'ScrollBars': 'Vertical',
            'Left': 10,
            'Top': 35,
            'Width': 660,
            'Height': 300
        })
        
        # Initial display
        self._update_display()
    
    def _show_installed_printers(self):
        """Show all installed printers."""
        printers = PrinterSettings.GetInstalledPrinters()
        default = PrinterSettings.GetDefaultPrinterName()
        
        output = "Installed Printers:\n"
        output += "=" * 50 + "\n\n"
        for i, printer in enumerate(printers, 1):
            marker = " (DEFAULT)" if printer == default else ""
            output += f"{i}. {printer}{marker}\n"
        
        output += "\n" + "=" * 50 + "\n"
        output += f"Total: {len(printers)} printer(s)\n"
        output += f"Default: {default}\n"
        
        self.txt_output.Text = output
    
    def _open_print_dialog(self):
        """Open PrintDialog with current settings."""
        dialog = PrintDialog()
        dialog.PrinterSettings = self.printer_settings
        dialog.AllowSomePages = True
        dialog.AllowSelection = True
        
        result = dialog.ShowDialog(self)
        
        if result == 'OK':
            # Get updated settings from dialog
            self.printer_settings = dialog.PrinterSettings
            self._update_display()
            self.txt_output.Text += "\n\n✓ Print Dialog OK - Settings updated"
        else:
            self.txt_output.Text += "\n\n✗ Print Dialog Cancelled"
    
    def _open_page_setup(self):
        """Open PageSetupDialog with current settings."""
        dialog = PageSetupDialog()
        dialog.PrinterSettings = self.printer_settings
        
        result = dialog.ShowDialog(self)
        
        if result == 'OK':
            self.printer_settings = dialog.PrinterSettings
            self._update_display()
            self.txt_output.Text += "\n\n✓ Page Setup OK - Settings updated"
        else:
            self.txt_output.Text += "\n\n✗ Page Setup Cancelled"
    
    def _settings_to_dict(self):
        """Convert PrinterSettings to dictionary."""
        settings_dict = self.printer_settings.to_dict()
        
        output = "PrinterSettings as Dictionary:\n"
        output += "=" * 50 + "\n\n"
        for key, value in settings_dict.items():
            output += f"{key}: {value}\n"
        
        output += "\n" + "=" * 50 + "\n"
        output += "You can save this dictionary to JSON, database, etc.\n"
        
        self.txt_output.Text = output
    
    def _settings_from_dict(self):
        """Load PrinterSettings from a dictionary."""
        # Example dictionary - simulating loaded from config/database
        settings_dict = {
            'PrinterName': 'Microsoft XPS Document Writer',
            'Copies': 3,
            'Duplex': 'Vertical',
            'Collate': True,
            'Color': False,
            'FromPage': 1,
            'ToPage': 10,
            'PrintRange': 'SomePages',
            'PaperSize': 'A4',
            'Landscape': True
        }
        
        self.printer_settings.from_dict(settings_dict)
        
        self._update_display()
        self.txt_output.Text += "\n\n✓ Settings loaded from dictionary"
    
    def _check_validity(self):
        """Check if current printer is valid."""
        is_valid = self.printer_settings.IsValid
        printer_name = self.printer_settings.PrinterName
        
        output = "Printer Validity Check:\n"
        output += "=" * 50 + "\n\n"
        output += f"Printer Name: {printer_name}\n"
        output += f"Is Valid: {is_valid}\n\n"
        
        if is_valid:
            output += "✓ This printer exists on the system"
        else:
            output += "✗ This printer does NOT exist on the system"
            output += "\n\nAvailable printers:\n"
            for printer in PrinterSettings.GetInstalledPrinters():
                output += f"  - {printer}\n"
        
        self.txt_output.Text = output
    
    def _check_default(self):
        """Check if current printer is the default printer."""
        is_default = self.printer_settings.IsDefaultPrinter
        printer_name = self.printer_settings.PrinterName
        default_name = PrinterSettings.GetDefaultPrinterName()
        
        output = "Default Printer Check:\n"
        output += "=" * 50 + "\n\n"
        output += f"Current Printer: {printer_name}\n"
        output += f"Default Printer: {default_name}\n"
        output += f"Is Default: {is_default}\n\n"
        
        if is_default:
            output += "✓ This is the default printer"
        else:
            output += "✗ This is NOT the default printer"
        
        self.txt_output.Text = output
    
    def _clone_settings(self):
        """Clone the current settings."""
        cloned = self.printer_settings.Clone()
        
        output = "PrinterSettings Cloned:\n"
        output += "=" * 50 + "\n\n"
        output += f"Original Printer: {self.printer_settings.PrinterName}\n"
        output += f"Cloned Printer: {cloned.PrinterName}\n"
        output += f"Are Different Objects: {cloned is not self.printer_settings}\n\n"
        
        # Modify clone
        cloned.Copies = 999
        
        output += f"After modifying clone to 999 copies:\n"
        output += f"Original Copies: {self.printer_settings.Copies}\n"
        output += f"Cloned Copies: {cloned.Copies}\n\n"
        output += "✓ Clone is independent of original"
        
        self.txt_output.Text = output
    
    def _update_display(self):
        """Update the display with current settings."""
        ps = self.printer_settings
        
        output = "Current PrinterSettings:\n"
        output += "=" * 50 + "\n\n"
        output += f"Printer Name: {ps.PrinterName}\n"
        output += f"Copies: {ps.Copies}\n"
        output += f"Duplex: {ps.Duplex}\n"
        output += f"Collate: {ps.Collate}\n"
        output += f"Color: {ps.Color}\n"
        output += f"Print Range: {ps.PrintRange}\n"
        output += f"From Page: {ps.FromPage}\n"
        output += f"To Page: {ps.ToPage}\n"
        output += f"Print to File: {ps.PrintToFile}\n"
        output += f"Paper Size: {ps.PaperSize}\n"
        output += f"Landscape: {ps.Landscape}\n"
        output += f"Paper Source: {ps.PaperSource}\n"
        output += "\n" + "=" * 50 + "\n"
        output += f"Is Valid: {ps.IsValid}\n"
        output += f"Is Default Printer: {ps.IsDefaultPrinter}\n"
        output += f"Can Duplex: {ps.CanDuplex}\n"
        output += f"Supports Color: {ps.SupportsColor}\n"
        
        self.txt_output.Text = output


if __name__ == "__main__":
    form = PrinterSettingsExampleForm()
    form.Show()
