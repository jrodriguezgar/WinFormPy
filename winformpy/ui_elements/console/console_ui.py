"""
ConsoleForm - A complete terminal-style console window.

Provides a standalone form with a console panel and toolbar for customization.
"""

import sys
import os

# Add project root to path for imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..', '..', '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy.winformpy import (
    Form, Panel, Label, Button, ComboBox, ListBox,
    DockStyle, AnchorStyles, Color, ColorDialog, DialogResult,
    Font, FontStyle, FlatStyle, ControlBase
)
from winformpy.ui_elements.console.console_panel import ConsolePanel
import tkinter.font as tkfont


class ConsoleForm(Form):
    """
    A complete console window with toolbar for customization.
    
    Features:
    - Embedded ConsolePanel
    - Font family selector
    - Font size selector
    - Color customization (foreground and background)
    - Theme presets
    - Clear button
    - Visual command panel with quick action buttons
    
    Example:
        from winformpy import Application
        from winformpy.ui_elements.console import ConsoleForm
        
        console = ConsoleForm(title="My Terminal", width=800, height=600)
        
        def handle_command(sender, cmd):
            if cmd == "help":
                console.console.WriteLine("Available commands: help, clear, exit")
            elif cmd == "clear":
                console.console.Clear()
            elif cmd == "exit":
                console.Close()
            else:
                console.console.WriteLine(f"Unknown command: {cmd}")
        
        console.console.CommandReceived = handle_command
        console.console.WriteLine("Welcome! Type 'help' for commands.")
        
        Application.Run(console)
    """
    
    def __init__(self, title="Console", width=800, height=600, theme='dark', 
                 show_command_panel=True, **kwargs):
        """
        Initialize the ConsoleForm.
        
        Args:
            title: Window title
            width: Window width
            height: Window height
            theme: Initial theme ('dark', 'light', 'matrix', 'retro', 'blue', 'powershell', 'ubuntu')
            show_command_panel: Show the visual command panel on the right (default: True)
            **kwargs: Additional Form properties
        """
        super().__init__({
            'Text': title,
            'Width': width,
            'Height': height,
            'BackColor': '#2D2D2D',
            **kwargs
        })
        
        self._current_theme = theme
        self._show_command_panel = show_command_panel
        
        # Apply layout before adding controls
        self.ApplyLayout()
        
        # Build the UI
        self._create_toolbar()
        if show_command_panel:
            self._create_command_panel()
        self._create_console(theme)
        
        # Welcome message
        self.console.WriteLine(f"Console initialized - Theme: {theme}")
        self.console.WriteLine("Type commands below or use the toolbar to customize.")
        if show_command_panel:
            self.console.WriteLine("Use the command panel on the right for quick actions.")
        self.console.WriteLine("")
    
    def _create_toolbar(self):
        """Create the toolbar with customization options."""
        self._toolbar = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 40,
            'BackColor': '#3C3C3C',
            'BorderStyle': 'None'
        })
        
        # Get available fonts
        available_fonts = self._get_monospace_fonts()
        
        # Font family label and combo
        self._lbl_font = Label(self._toolbar, {
            'Text': 'Font:',
            'ForeColor': '#CCCCCC',
            'BackColor': '#3C3C3C',
            'Left': 10,
            'Top': 10,
            'AutoSize': True
        })
        
        self._cmb_font = ComboBox(self._toolbar, {
            'Left': 50,
            'Top': 7,
            'Width': 150,
            'Height': 25
        })
        for font_name in available_fonts:
            self._cmb_font.Items.Add(font_name)
        self._cmb_font.SelectedIndex = available_fonts.index('Consolas') if 'Consolas' in available_fonts else 0
        self._cmb_font.SelectedIndexChanged = lambda s, e: self._on_font_changed()
        
        # Font size label and combo
        self._lbl_size = Label(self._toolbar, {
            'Text': 'Size:',
            'ForeColor': '#CCCCCC',
            'BackColor': '#3C3C3C',
            'Left': 210,
            'Top': 10,
            'AutoSize': True
        })
        
        self._cmb_size = ComboBox(self._toolbar, {
            'Left': 250,
            'Top': 7,
            'Width': 60,
            'Height': 25
        })
        for size in [8, 9, 10, 11, 12, 14, 16, 18, 20, 24]:
            self._cmb_size.Items.Add(str(size))
        self._cmb_size.SelectedIndex = 3  # Default to 11
        self._cmb_size.SelectedIndexChanged = lambda s, e: self._on_size_changed()
        
        # Theme label and combo
        self._lbl_theme = Label(self._toolbar, {
            'Text': 'Theme:',
            'ForeColor': '#CCCCCC',
            'BackColor': '#3C3C3C',
            'Left': 320,
            'Top': 10,
            'AutoSize': True
        })
        
        self._cmb_theme = ComboBox(self._toolbar, {
            'Left': 370,
            'Top': 7,
            'Width': 100,
            'Height': 25
        })
        themes = ['dark', 'light', 'matrix', 'retro', 'blue', 'powershell', 'ubuntu']
        for theme in themes:
            self._cmb_theme.Items.Add(theme)
        self._cmb_theme.SelectedIndex = themes.index(self._current_theme) if self._current_theme in themes else 0
        self._cmb_theme.SelectedIndexChanged = lambda s, e: self._on_theme_changed()
        
        # Background color button
        self._btn_bg = Button(self._toolbar, {
            'Text': '🎨 Back',
            'Left': 480,
            'Top': 7,
            'Width': 70,
            'Height': 26,
            'FlatStyle': FlatStyle.Flat
        })
        self._btn_bg.Click = lambda s, e: self._pick_bg_color()
        
        # Foreground color button
        self._btn_fg = Button(self._toolbar, {
            'Text': '🎨 Fore',
            'Left': 555,
            'Top': 7,
            'Width': 70,
            'Height': 26,
            'FlatStyle': FlatStyle.Flat
        })
        self._btn_fg.Click = lambda s, e: self._pick_fg_color()
        
        # Clear button
        self._btn_clear = Button(self._toolbar, {
            'Text': '🗑️ Clear',
            'Left': 630,
            'Top': 7,
            'Width': 70,
            'Height': 26,
            'FlatStyle': FlatStyle.Flat
        })
        self._btn_clear.Click = lambda s, e: self.console.Clear()
        
        # Toggle sidebar button
        self._btn_toggle_sidebar = Button(self._toolbar, {
            'Text': '◀ Panel',
            'Left': 705,
            'Top': 7,
            'Width': 70,
            'Height': 26,
            'FlatStyle': FlatStyle.Flat
        })
        self._btn_toggle_sidebar.Click = lambda s, e: self.ToggleCommandPanel()
    
    def _create_command_panel(self):
        """Create the visual command panel on the right side with command list and execute button."""
        self._command_panel = Panel(self, {
            'Dock': DockStyle.Right,
            'Width': 160,
            'BackColor': '#2D2D2D',
            'BorderStyle': 'None'
        })
        self._command_panel_visible = True
        
        # Panel title - Commands
        self._cmd_title = Label(self._command_panel, {
            'Text': '⚡ Commands',
            'ForeColor': '#FFFFFF',
            'BackColor': '#2D2D2D',
            'Font': Font('Segoe UI', 9, FontStyle.Bold),
            'Left': 10,
            'Top': 8,
            'AutoSize': True
        })
        
        # Command list
        self._command_list = ListBox(self._command_panel, {
            'Left': 10,
            'Top': 32,
            'Width': 140,
            'Height': 180,
            'BackColor': '#1E1E1E',
            'ForeColor': '#CCCCCC'
        })
        
        # Add commands to the list
        commands = [
            'help',
            'clear',
            'time',
            'demo',
            'history',
            'clearhistory',
            'info',
            'exit'
        ]
        for cmd in commands:
            self._command_list.Items.Add(cmd)
        self._command_list.SelectedIndex = 0
        
        # Execute button
        self._btn_execute = Button(self._command_panel, {
            'Text': '▶ Execute',
            'Left': 10,
            'Top': 218,
            'Width': 140,
            'Height': 30,
            'FlatStyle': FlatStyle.Flat,
            'BackColor': '#2E7D32'
        })
        self._btn_execute.Click = lambda s, e: self._on_execute_command()
        
        # Double-click on list to execute (using WinFormPy event)
        self._command_list.DoubleClick = lambda s, e: self._on_execute_command()
        
        # Separator
        sep_label = Label(self._command_panel, {
            'Text': '─' * 20,
            'ForeColor': '#555555',
            'BackColor': '#2D2D2D',
            'Left': 10,
            'Top': 255,
            'AutoSize': True
        })
        
        # Theme section title
        theme_title = Label(self._command_panel, {
            'Text': '🎭 Themes',
            'ForeColor': '#FFFFFF',
            'BackColor': '#2D2D2D',
            'Font': Font('Segoe UI', 9, FontStyle.Bold),
            'Left': 10,
            'Top': 275,
            'AutoSize': True
        })
        
        # Theme list
        self._theme_list = ListBox(self._command_panel, {
            'Left': 10,
            'Top': 298,
            'Width': 140,
            'Height': 130,
            'BackColor': '#1E1E1E',
            'ForeColor': '#CCCCCC'
        })
        
        # Add themes to the list
        themes = [
            'dark',
            'light',
            'matrix',
            'retro',
            'blue',
            'powershell',
            'ubuntu'
        ]
        for theme in themes:
            self._theme_list.Items.Add(theme)
        self._theme_list.SelectedIndex = 0
        
        # Apply theme button
        self._btn_apply_theme = Button(self._command_panel, {
            'Text': '🎨 Apply Theme',
            'Left': 10,
            'Top': 433,
            'Width': 140,
            'Height': 28,
            'FlatStyle': FlatStyle.Flat,
            'BackColor': '#1565C0'
        })
        self._btn_apply_theme.Click = lambda s, e: self._on_apply_theme()
        
        # Double-click on theme list to apply (using WinFormPy event)
        self._theme_list.DoubleClick = lambda s, e: self._on_apply_theme()
        
        # Separator
        sep_label2 = Label(self._command_panel, {
            'Text': '─' * 20,
            'ForeColor': '#555555',
            'BackColor': '#2D2D2D',
            'Left': 10,
            'Top': 468,
            'AutoSize': True
        })
        
        # Exit button at bottom
        self._btn_exit = Button(self._command_panel, {
            'Text': '🚪 Exit',
            'Left': 10,
            'Top': 490,
            'Width': 140,
            'Height': 28,
            'FlatStyle': FlatStyle.Flat,
            'BackColor': '#8B0000'
        })
        self._btn_exit.Click = lambda s, e: self.Close()
    
    def _on_execute_command(self):
        """Execute the selected command from the list."""
        if hasattr(self, '_command_list'):
            selected = self._command_list.SelectedItem
            if selected:
                self.console.ExecuteCommand(selected)
    
    def _on_apply_theme(self):
        """Apply the selected theme from the list."""
        if hasattr(self, '_theme_list'):
            selected = self._theme_list.SelectedItem
            if selected:
                self._apply_quick_theme(selected)
    
    def ToggleCommandPanel(self):
        """Toggle the visibility of the command panel."""
        if not hasattr(self, '_command_panel'):
            return
        
        if self._command_panel_visible:
            # Hide the panel using WinFormPy Visible property
            self._command_panel.Visible = False
            self._command_panel_visible = False
            self._btn_toggle_sidebar.Text = '▶ Panel'
            
            # Use InvokeAsync to allow event loop to process, then refresh
            self.InvokeAsync(self._delayed_refresh, 10)
        else:
            # Show the panel using WinFormPy Visible property
            self._command_panel.Visible = True
            self._command_panel_visible = True
            self._btn_toggle_sidebar.Text = '◀ Panel'
            
            # Position the panel using WinFormPy properties
            form_width = self.Width
            form_height = self.Height
            toolbar_height = 40
            panel_width = getattr(self, '_command_panel_width', 160)
            panel_height = form_height - toolbar_height
            
            self._command_panel.Left = form_width - panel_width
            self._command_panel.Top = toolbar_height
            self._command_panel.Width = panel_width
            self._command_panel.Height = panel_height
            
            # Use InvokeAsync to allow event loop to process, then refresh
            self.InvokeAsync(self._delayed_refresh, 10)
    
    def _delayed_refresh(self):
        """Delayed refresh to allow geometry to settle."""
        self.Refresh()
        self._refresh_layout()
        self.Refresh()
    
    def ShowCommandPanel(self):
        """Show the command panel."""
        if hasattr(self, '_command_panel') and not self._command_panel_visible:
            self.ToggleCommandPanel()
    
    def HideCommandPanel(self):
        """Hide the command panel."""
        if hasattr(self, '_command_panel') and self._command_panel_visible:
            self.ToggleCommandPanel()
    
    def _refresh_layout(self):
        """Force a layout refresh to resize all controls properly."""
        # Refresh to process pending geometry changes
        self.Refresh()
        
        # Force recalculation of all docked controls in this Form
        # This is needed because changing Visible on a docked control
        # doesn't automatically trigger a layout recalculation
        if hasattr(self, '_root') and self._root:
            ControlBase._layout_docked_children(self._root)
        
        self.Refresh()
        
        # Trigger console panel layout to properly resize internal components
        if hasattr(self, 'console') and self.console:
            if hasattr(self.console, 'PerformLayout'):
                self.console.PerformLayout()
        
        self.Refresh()

    def _apply_quick_theme(self, theme):
        """Apply a theme from the quick theme buttons."""
        self.console.SetTheme(theme)
        self.console.WriteSuccess(f"Theme changed to: {theme}")
        # Update the theme combo box
        themes = ['dark', 'light', 'matrix', 'retro', 'blue', 'powershell', 'ubuntu']
        if theme in themes:
            self._cmb_theme.SelectedIndex = themes.index(theme)
            self._current_theme = theme

    def _create_console(self, theme):
        """Create the console panel."""
        self.console = ConsolePanel(self, {
            'Dock': DockStyle.Fill
        })
        self.console.SetTheme(theme)
    
    def _get_monospace_fonts(self):
        """Get a list of available monospace fonts."""
        # Common monospace fonts to look for
        preferred = [
            'Consolas', 'Cascadia Code', 'Cascadia Mono',
            'Fira Code', 'Source Code Pro', 'JetBrains Mono',
            'Monaco', 'Menlo', 'Ubuntu Mono', 'DejaVu Sans Mono',
            'Courier New', 'Courier', 'Lucida Console'
        ]
        
        try:
            all_fonts = list(tkfont.families())
            available = [f for f in preferred if f in all_fonts]
            
            # Add other monospace fonts from system
            for font_name in all_fonts:
                if font_name not in available:
                    if any(x in font_name.lower() for x in ['mono', 'code', 'console', 'courier', 'terminal']):
                        available.append(font_name)
            
            return available if available else ['TkFixedFont']
        except:
            return ['Consolas', 'Courier New']
    
    def _on_font_changed(self):
        """Handle font family change."""
        selected = self._cmb_font.Text
        if selected:
            self.console.FontFamily = selected
    
    def _on_size_changed(self):
        """Handle font size change."""
        selected = self._cmb_size.Text
        if selected:
            try:
                self.console.FontSize = int(selected)
            except ValueError:
                pass
    
    def _on_theme_changed(self):
        """Handle theme change."""
        selected = self._cmb_theme.Text
        if selected:
            self.console.SetTheme(selected)
            self._current_theme = selected
    
    def _pick_bg_color(self):
        """Open color picker for background color."""
        dialog = ColorDialog()
        dialog.Color = Color(self.console.ConsoleBackColor)
        if dialog.ShowDialog(self) == DialogResult.OK:
            self.console.ConsoleBackColor = str(dialog.Color)
    
    def _pick_fg_color(self):
        """Open color picker for foreground color."""
        dialog = ColorDialog()
        dialog.Color = Color(self.console.ForeColor)
        if dialog.ShowDialog(self) == DialogResult.OK:
            self.console.ForeColor = str(dialog.Color)


# Example usage
if __name__ == '__main__':
    from winformpy.winformpy import Application
    from datetime import datetime
    
    # Create console form
    form = ConsoleForm(
        title="WinFormPy Console",
        width=900,
        height=600,
        theme='dark'
    )
    
    # Command handler with full implementation
    def handle_command(sender, command):
        cmd = command.strip().lower()
        args = command.strip().split(' ', 1)
        
        if cmd == 'help':
            form.console.WriteLine("")
            form.console.WriteInfo("━" * 45)
            form.console.WriteInfo("  Available Commands")
            form.console.WriteInfo("━" * 45)
            form.console.WriteLine("")
            form.console.WriteLine("  help              - Show this help message")
            form.console.WriteLine("  clear             - Clear the console")
            form.console.WriteLine("  time              - Show current date and time")
            form.console.WriteLine("  echo <text>       - Echo the text back")
            form.console.WriteLine("  theme <name>      - Change theme")
            form.console.WriteLine("                      (dark, light, matrix, retro,")
            form.console.WriteLine("                       blue, powershell, ubuntu)")
            form.console.WriteLine("  font <name>       - Change font family")
            form.console.WriteLine("  size <n>          - Change font size (6-48)")
            form.console.WriteLine("  prompt <text>     - Change the command prompt")
            form.console.WriteLine("  timestamp [on|off]- Toggle timestamp display")
            form.console.WriteLine("  demo              - Show color output demo")
            form.console.WriteLine("  history           - Show command history")
            form.console.WriteLine("  clearhistory      - Clear command history")
            form.console.WriteLine("  info              - Show console info")
            form.console.WriteLine("  exit              - Close the console")
            form.console.WriteLine("")
        
        elif cmd == 'clear':
            form.console.Clear()
        
        elif cmd == 'time':
            now = datetime.now()
            form.console.WriteSuccess(f"📅 Date: {now.strftime('%Y-%m-%d')}")
            form.console.WriteSuccess(f"⏰ Time: {now.strftime('%H:%M:%S')}")
        
        elif args[0].lower() == 'echo' and len(args) > 1:
            form.console.WriteLine(args[1])
        
        elif args[0].lower() == 'theme':
            if len(args) > 1:
                theme = args[1].lower()
                themes = ['dark', 'light', 'matrix', 'retro', 'blue', 'powershell', 'ubuntu']
                if theme in themes:
                    form.console.SetTheme(theme)
                    form.console.WriteSuccess(f"Theme changed to: {theme}")
                else:
                    form.console.WriteError(f"Unknown theme: {theme}")
                    form.console.WriteLine(f"Available themes: {', '.join(themes)}")
            else:
                form.console.WriteWarning("Usage: theme <name>")
                form.console.WriteLine("Available: dark, light, matrix, retro, blue, powershell, ubuntu")
        
        elif args[0].lower() == 'font':
            if len(args) > 1:
                font_name = args[1]
                form.console.FontFamily = font_name
                form.console.WriteSuccess(f"Font changed to: {font_name}")
            else:
                form.console.WriteWarning("Usage: font <name>")
                form.console.WriteLine(f"Current font: {form.console.FontFamily}")
        
        elif args[0].lower() == 'size':
            if len(args) > 1:
                try:
                    size = int(args[1])
                    if 6 <= size <= 48:
                        form.console.FontSize = size
                        form.console.WriteSuccess(f"Font size changed to: {size}")
                    else:
                        form.console.WriteError("Size must be between 6 and 48")
                except ValueError:
                    form.console.WriteError("Invalid size. Use a number (6-48).")
            else:
                form.console.WriteWarning("Usage: size <number>")
                form.console.WriteLine(f"Current size: {form.console.FontSize}")
        
        elif args[0].lower() == 'prompt':
            if len(args) > 1:
                new_prompt = args[1] + ' '
                form.console.Prompt = new_prompt
                form.console.WriteSuccess(f"Prompt changed to: '{new_prompt}'")
            else:
                form.console.WriteWarning("Usage: prompt <text>")
                form.console.WriteLine(f"Current prompt: '{form.console.Prompt}'")
        
        elif args[0].lower() == 'timestamp':
            if len(args) > 1:
                if args[1].lower() == 'on':
                    form.console.ShowTimestamp = True
                    form.console.WriteSuccess("Timestamps enabled")
                elif args[1].lower() == 'off':
                    form.console.ShowTimestamp = False
                    form.console.WriteSuccess("Timestamps disabled")
                else:
                    form.console.WriteWarning("Usage: timestamp [on|off]")
            else:
                # Toggle
                form.console.ShowTimestamp = not form.console.ShowTimestamp
                status = "enabled" if form.console.ShowTimestamp else "disabled"
                form.console.WriteSuccess(f"Timestamps {status}")
        
        elif cmd == 'demo':
            form.console.WriteLine("")
            form.console.WriteLine("Color Output Demo:")
            form.console.WriteLine("─" * 35)
            form.console.Write("  Write():        ")
            form.console.WriteLine("Normal text output")
            form.console.Write("  WriteError():   ")
            form.console.WriteError("Error messages in red")
            form.console.Write("  WriteWarning(): ")
            form.console.WriteWarning("Warnings in yellow")
            form.console.Write("  WriteSuccess(): ")
            form.console.WriteSuccess("Success messages in green")
            form.console.Write("  WriteInfo():    ")
            form.console.WriteInfo("Info messages in cyan")
            form.console.WriteLine("")
            form.console.WriteLine("Custom Colors:")
            form.console.WriteLine("─" * 35)
            form.console.WriteLine("  Purple text", '#9B59B6')
            form.console.WriteLine("  Orange text", '#E67E22')
            form.console.WriteLine("  Pink text", '#FF69B4')
            form.console.WriteLine("  Teal text", '#1ABC9C')
            form.console.WriteLine("")
        
        elif cmd == 'history':
            history = form.console.CommandHistory
            if history:
                form.console.WriteInfo(f"Command History ({len(history)} commands):")
                for i, h_cmd in enumerate(history, 1):
                    form.console.WriteLine(f"  {i:3}. {h_cmd}")
                form.console.WriteLine("")
                form.console.WriteLine("TIP: Use Up/Down arrows to navigate history")
            else:
                form.console.WriteLine("No command history yet.")
        
        elif cmd == 'clearhistory':
            form.console.ClearHistory()
            form.console.WriteSuccess("Command history cleared")
        
        elif cmd == 'info':
            form.console.WriteInfo("Console Information:")
            form.console.WriteLine(f"  Font Family:  {form.console.FontFamily}")
            form.console.WriteLine(f"  Font Size:    {form.console.FontSize}")
            form.console.WriteLine(f"  Back Color:   {form.console.ConsoleBackColor}")
            form.console.WriteLine(f"  Fore Color:   {form.console.ForeColor}")
            form.console.WriteLine(f"  Prompt:       '{form.console.Prompt}'")
            form.console.WriteLine(f"  Timestamps:   {'On' if form.console.ShowTimestamp else 'Off'}")
            form.console.WriteLine(f"  Max Lines:    {form.console.MaxLines}")
            form.console.WriteLine(f"  History:      {len(form.console.CommandHistory)} commands")
        
        elif cmd == 'exit':
            form.Close()
        
        elif cmd:
            form.console.WriteWarning(f"Unknown command: {command}")
            form.console.WriteLine("Type 'help' for available commands.")
    
    form.console.CommandReceived = handle_command
    
    # Welcome banner
    form.console.Clear()
    form.console.WriteSuccess("╔══════════════════════════════════════════════════╗")
    form.console.WriteSuccess("║                                                  ║")
    form.console.WriteSuccess("║        Welcome to WinFormPy Console!             ║")
    form.console.WriteSuccess("║                                                  ║")
    form.console.WriteSuccess("╚══════════════════════════════════════════════════╝")
    form.console.WriteLine("")
    form.console.WriteLine("  A terminal-style console with customizable appearance.")
    form.console.WriteLine("")
    form.console.WriteInfo("  💡 TIP: Use the toolbar to change font, size, and theme.")
    form.console.WriteInfo("  💡 TIP: Use Up/Down arrows to navigate command history.")
    form.console.WriteLine("")
    form.console.WriteLine("  Type 'help' for available commands.")
    form.console.WriteLine("  Type 'demo' to see color output examples.")
    form.console.WriteLine("")
    
    Application.Run(form)
