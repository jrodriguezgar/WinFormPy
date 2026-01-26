"""
Console Demo - Terminal with full command handler

This example demonstrates:
- Command processing (help, clear, time, echo, etc.)
- Theme switching
- Font customization
- Colored output
- Command history
- Prompt customization
"""

import sys
import os
from datetime import datetime

# Add project root to path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy.winformpy import Application
from winformpy.ui_elements.console.console_ui import ConsoleForm


def main():
    """Run console demo with full command handler."""
    
    # Create console form
    form = ConsoleForm(
        title="WinFormPy Console - Full Demo",
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


if __name__ == "__main__":
    main()
