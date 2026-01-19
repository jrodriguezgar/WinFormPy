"""
Word Processor Example - Demonstrates the enhanced RichTextBox and WordProcessorPanel.

This example shows:
1. Using the WordProcessorPanel as an embeddable component
2. Using RichTextBox directly with Write/WriteLine methods
3. Text formatting and color options
4. Document operations

Run this example:
    python word_processor_example.py
"""

import sys
import os

# Add project root to path for imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy import (
    Form, Panel, Button, Label, RichTextBox, TabControl, TabPage, TextBox,
    DockStyle, AnchorStyles, Font, FontStyle, Color, MessageBox
)
from winformpy.ui_elements.word_processor import WordProcessorPanel, WordProcessorForm


def create_richtextbox_demo():
    """Create a form demonstrating RichTextBox features."""
    form = Form({
        'Text': 'RichTextBox Demo - Enhanced Features',
        'Width': 900,
        'Height': 700,
        'BackColor': '#F0F0F0'
    })
    form.ApplyLayout()
    
    # Create tab control - FILL goes LAST on form, but tabs has no siblings so OK
    tabs = TabControl(form, {
        'Dock': DockStyle.Fill
    })
    
    # =========================================================================
    # Tab 1: Write Methods Demo
    # =========================================================================
    tab_write = TabPage(tabs, {'Text': 'Write Methods'})
    
    # IMPORTANT: Create DockStyle.Top controls FIRST, then Fill LAST
    
    # Toolbar (Top - created first)
    toolbar1 = Panel(tab_write, {
        'Dock': DockStyle.Top,
        'Height': 45,
        'BackColor': '#E8E8E8'
    })
    
    # Toolbar buttons - created inside toolbar
    btn_write_demo = Button(toolbar1, {
        'Text': 'Demo Write Methods',
        'Left': 10,
        'Top': 8,
        'Width': 140,
        'Height': 28,
        'BackColor': '#4CAF50',
        'ForeColor': '#FFFFFF'
    })
    
    btn_clear = Button(toolbar1, {
        'Text': 'Clear',
        'Left': 160,
        'Top': 8,
        'Width': 80,
        'Height': 28
    })
    
    btn_add_log = Button(toolbar1, {
        'Text': 'Add Log Entry',
        'Left': 250,
        'Top': 8,
        'Width': 100,
        'Height': 28
    })
    
    # RichTextBox for write demo (Fill - created LAST)
    rtb_write = RichTextBox(tab_write, {
        'Dock': DockStyle.Fill,
        'BackColor': '#1E1E1E',
        'ForeColor': '#CCCCCC',
        'Font': Font('Consolas', 11),
        'MaxLines': 500
    })
    
    # Event handlers
    def demo_write_methods():
        rtb_write.Clear()
        rtb_write.WriteLine("=== RichTextBox Write Methods Demo ===", '#00BFFF')
        rtb_write.WriteLine()
        
        rtb_write.WriteLine("1. Basic Write Methods:", '#FFFF00')
        rtb_write.Write("   Write() adds text ")
        rtb_write.Write("without ", '#FF6B6B')
        rtb_write.WriteLine("a newline")
        rtb_write.WriteLine("   WriteLine() adds text with a newline", '#00FF00')
        rtb_write.WriteLine()
        
        rtb_write.WriteLine("2. Colored Write Methods:", '#FFFF00')
        rtb_write.WriteInfo("   WriteInfo() - Information message")
        rtb_write.WriteSuccess("   WriteSuccess() - Success message")
        rtb_write.WriteWarning("   WriteWarning() - Warning message")
        rtb_write.WriteError("   WriteError() - Error message")
        rtb_write.WriteLine()
        
        rtb_write.WriteLine("3. Custom Colors:", '#FFFF00')
        colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#9400D3']
        rtb_write.Write("   ")
        for i, color in enumerate(colors):
            rtb_write.Write(f"Color{i+1} ", color)
        rtb_write.WriteLine()
        rtb_write.WriteLine()
        
        rtb_write.WriteLine("4. Mixed Content:", '#FFFF00')
        rtb_write.Write("   Status: ")
        rtb_write.Write("[", '#808080')
        rtb_write.Write("RUNNING", '#00FF00')
        rtb_write.Write("]", '#808080')
        rtb_write.Write(" | Memory: ")
        rtb_write.Write("256 MB", '#00BFFF')
        rtb_write.Write(" | CPU: ")
        rtb_write.WriteLine("45%", '#FFD93D')
        rtb_write.WriteLine()
        
        rtb_write.WriteLine("=== Demo Complete ===", '#00BFFF')
    
    btn_write_demo.Click = lambda s, e: demo_write_methods()
    btn_clear.Click = lambda s, e: rtb_write.Clear()
    
    log_counter = [0]
    def add_log_entry():
        log_counter[0] += 1
        import datetime
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        rtb_write.Write(f"[{timestamp}] ", '#808080')
        rtb_write.WriteLine(f"Log entry #{log_counter[0]}", '#CCCCCC')
    
    btn_add_log.Click = lambda s, e: add_log_entry()
    
    # =========================================================================
    # Tab 2: Formatting Demo
    # =========================================================================
    tab_format = TabPage(tabs, {'Text': 'Text Formatting'})
    
    # Toolbar (Top - created first)
    toolbar2 = Panel(tab_format, {
        'Dock': DockStyle.Top,
        'Height': 45,
        'BackColor': '#E8E8E8'
    })
    
    # Formatting buttons inside toolbar
    btn_bold = Button(toolbar2, {
        'Text': 'B',
        'Left': 10,
        'Top': 8,
        'Width': 32,
        'Height': 28,
        'Font': Font('Segoe UI', 10, FontStyle.Bold)
    })
    
    btn_italic = Button(toolbar2, {
        'Text': 'I',
        'Left': 45,
        'Top': 8,
        'Width': 32,
        'Height': 28,
        'Font': Font('Segoe UI', 10, FontStyle.Italic)
    })
    
    btn_underline = Button(toolbar2, {
        'Text': 'U',
        'Left': 80,
        'Top': 8,
        'Width': 32,
        'Height': 28
    })
    
    btn_strike = Button(toolbar2, {
        'Text': 'S',
        'Left': 115,
        'Top': 8,
        'Width': 32,
        'Height': 28
    })
    
    # Color buttons
    color_index = [0]
    colors = ['#FF0000', '#00FF00', '#0000FF', '#FF00FF', '#00FFFF', '#000000']
    
    btn_text_color = Button(toolbar2, {
        'Text': 'A',
        'Left': 160,
        'Top': 8,
        'Width': 32,
        'Height': 28,
        'ForeColor': '#FF0000',
        'Font': Font('Segoe UI', 10, FontStyle.Bold)
    })
    
    bg_index = [0]
    bg_colors = ['#FFFF00', '#00FFFF', '#FF00FF', '#90EE90', '#FFB6C1', '#FFFFFF']
    
    btn_bg_color = Button(toolbar2, {
        'Text': '⬜',
        'Left': 195,
        'Top': 8,
        'Width': 32,
        'Height': 28,
        'BackColor': '#FFFF00'
    })
    
    # RichTextBox for formatting (Fill - created LAST)
    rtb_format = RichTextBox(tab_format, {
        'Dock': DockStyle.Fill,
        'BackColor': '#FFFFFF',
        'ForeColor': '#000000',
        'Font': Font('Segoe UI', 12)
    })
    
    # Add sample text
    rtb_format.Text = """Welcome to the RichTextBox Formatting Demo!

Select some text and use the buttons above to apply formatting.

Features:
- Bold (Ctrl+B)
- Italic (Ctrl+I)
- Underline (Ctrl+U)
- Strikethrough
- Text Color
- Background Color
- Font Selection

Try selecting different portions of this text and applying various formats.
You can also mix and match formats - text can be bold AND italic at the same time!

Keyboard Shortcuts:
Ctrl+B = Bold
Ctrl+I = Italic
Ctrl+U = Underline
Ctrl+A = Select All
Ctrl+Z = Undo
Ctrl+Y = Redo
"""
    
    # Event handlers for formatting
    btn_bold.Click = lambda s, e: setattr(rtb_format, 'SelectionBold', not rtb_format.SelectionBold)
    btn_italic.Click = lambda s, e: setattr(rtb_format, 'SelectionItalic', not rtb_format.SelectionItalic)
    btn_underline.Click = lambda s, e: setattr(rtb_format, 'SelectionUnderline', not rtb_format.SelectionUnderline)
    btn_strike.Click = lambda s, e: setattr(rtb_format, 'SelectionStrikethrough', not rtb_format.SelectionStrikethrough)
    
    def cycle_text_color():
        color_index[0] = (color_index[0] + 1) % len(colors)
        color = colors[color_index[0]]
        rtb_format.SelectionColor = color
        btn_text_color.ForeColor = color
    
    btn_text_color.Click = lambda s, e: cycle_text_color()
    
    def cycle_bg_color():
        bg_index[0] = (bg_index[0] + 1) % len(bg_colors)
        color = bg_colors[bg_index[0]]
        rtb_format.SelectionBackColor = color
        btn_bg_color.BackColor = color
    
    btn_bg_color.Click = lambda s, e: cycle_bg_color()
    
    # =========================================================================
    # Tab 3: Find & Replace Demo
    # =========================================================================
    tab_find = TabPage(tabs, {'Text': 'Find & Replace'})
    
    # Toolbar (Top - created first)
    toolbar3 = Panel(tab_find, {
        'Dock': DockStyle.Top,
        'Height': 80,
        'BackColor': '#E8E8E8'
    })
    
    # Find controls inside toolbar
    lbl_find = Label(toolbar3, {
        'Text': 'Find:',
        'Left': 10,
        'Top': 12,
        'Width': 40,
        'BackColor': '#E8E8E8'
    })
    
    txt_find = TextBox(toolbar3, {
        'Text': 'quick',
        'Left': 55,
        'Top': 8,
        'Width': 150,
        'Height': 24
    })
    
    btn_find_next = Button(toolbar3, {
        'Text': 'Find Next',
        'Left': 215,
        'Top': 7,
        'Width': 80,
        'Height': 26
    })
    
    btn_find_prev = Button(toolbar3, {
        'Text': 'Find Prev',
        'Left': 300,
        'Top': 7,
        'Width': 80,
        'Height': 26
    })
    
    # Replace controls
    lbl_replace = Label(toolbar3, {
        'Text': 'Replace:',
        'Left': 10,
        'Top': 47,
        'Width': 55,
        'BackColor': '#E8E8E8'
    })
    
    txt_replace = TextBox(toolbar3, {
        'Text': 'fast',
        'Left': 55,
        'Top': 43,
        'Width': 150,
        'Height': 24
    })
    
    btn_replace = Button(toolbar3, {
        'Text': 'Replace',
        'Left': 215,
        'Top': 42,
        'Width': 80,
        'Height': 26
    })
    
    btn_replace_all = Button(toolbar3, {
        'Text': 'Replace All',
        'Left': 300,
        'Top': 42,
        'Width': 80,
        'Height': 26
    })
    
    # RichTextBox for find demo (Fill - created LAST)
    rtb_find = RichTextBox(tab_find, {
        'Dock': DockStyle.Fill,
        'BackColor': '#FFFFFF',
        'ForeColor': '#000000',
        'Font': Font('Consolas', 11)
    })
    
    # Add sample text
    rtb_find.Text = """The quick brown fox jumps over the lazy dog.
The quick brown fox jumps over the lazy dog.
The quick brown fox jumps over the lazy dog.

Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.

The quick brown fox jumps over the lazy dog.
The quick brown fox jumps over the lazy dog.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia.
"""
    
    # Event handlers for find/replace
    btn_find_next.Click = lambda s, e: rtb_find.FindNext(txt_find.Text)
    btn_find_prev.Click = lambda s, e: rtb_find.FindNext(txt_find.Text, search_up=True)
    btn_replace.Click = lambda s, e: rtb_find.FindAndReplace(txt_find.Text, txt_replace.Text, replace_all=False)
    
    def replace_all():
        count = rtb_find.FindAndReplace(txt_find.Text, txt_replace.Text, replace_all=True)
        MessageBox.Show(f"Replaced {count} occurrences.", "Replace All", "OK", "Information")
    
    btn_replace_all.Click = lambda s, e: replace_all()
    
    # =========================================================================
    # Tab 4: Word Processor Panel Demo
    # =========================================================================
    tab_wp = TabPage(tabs, {'Text': 'Word Processor Panel'})
    
    # WordProcessorPanel handles its own dock order internally
    wp_panel = WordProcessorPanel(tab_wp, {
        'Dock': DockStyle.Fill,
        'ShowToolbar': True,
        'ShowStatusBar': True,
        'DefaultFont': 'Georgia',
        'DefaultFontSize': 12
    })
    
    # Add sample content
    wp_panel.Text = """Welcome to the Word Processor Panel!

This is a complete word processor component that you can embed in your applications.

Features:
• Formatting toolbar with Bold, Italic, Underline
• Font family and size selection
• Text color and highlight color
• Text alignment options
• Find and Replace (Ctrl+F)
• Word count and character count
• Line and column position tracking

Try editing this text and using the formatting toolbar above.

You can also use keyboard shortcuts:
Ctrl+B = Bold
Ctrl+I = Italic
Ctrl+U = Underline
Ctrl+S = Save
Ctrl+F = Find
"""
    
    # =========================================================================
    # Tab 5: Raw Text / RTF Demo
    # =========================================================================
    tab_raw = TabPage(tabs, {'Text': 'Raw Text & RTF'})
    
    # Top panel for source editor
    top_panel = Panel(tab_raw, {
        'Dock': DockStyle.Top,
        'Height': 250,
        'BackColor': '#F0F0F0'
    })
    
    # Label for source
    lbl_source = Label(top_panel, {
        'Text': 'Source (write colored text here):',
        'Left': 10,
        'Top': 5,
        'AutoSize': True,
        'BackColor': '#F0F0F0'
    })
    
    # Source RichTextBox
    rtb_source = RichTextBox(top_panel, {
        'Left': 10,
        'Top': 25,
        'Width': 400,
        'Height': 180,
        'BackColor': '#1E1E1E',
        'ForeColor': '#CCCCCC',
        'Font': Font('Consolas', 10)
    })
    
    # Buttons panel
    btn_get_text = Button(top_panel, {
        'Text': 'Get Text',
        'Left': 420,
        'Top': 25,
        'Width': 120,
        'Height': 28
    })
    
    btn_get_selected = Button(top_panel, {
        'Text': 'Get SelectedText',
        'Left': 420,
        'Top': 58,
        'Width': 120,
        'Height': 28
    })
    
    btn_get_rtf = Button(top_panel, {
        'Text': 'Get Rtf',
        'Left': 420,
        'Top': 91,
        'Width': 120,
        'Height': 28
    })
    
    btn_get_selected_rtf = Button(top_panel, {
        'Text': 'Get SelectedRtf',
        'Left': 420,
        'Top': 124,
        'Width': 120,
        'Height': 28
    })
    
    btn_get_line = Button(top_panel, {
        'Text': 'GetLineText(0)',
        'Left': 420,
        'Top': 157,
        'Width': 120,
        'Height': 28
    })
    
    btn_add_sample = Button(top_panel, {
        'Text': 'Add Sample',
        'Left': 420,
        'Top': 190,
        'Width': 120,
        'Height': 28
    })
    
    # Bottom panel for output
    bottom_panel = Panel(tab_raw, {
        'Dock': DockStyle.Fill,
        'BackColor': '#E8E8E8'
    })
    
    lbl_output = Label(bottom_panel, {
        'Text': 'Output:',
        'Left': 10,
        'Top': 5,
        'AutoSize': True,
        'BackColor': '#E8E8E8'
    })
    
    # Output RichTextBox (for displaying results)
    rtb_output = RichTextBox(bottom_panel, {
        'Left': 10,
        'Top': 25,
        'Width': 860,
        'Height': 200,
        'BackColor': '#FFFFFF',
        'ForeColor': '#000000',
        'Font': Font('Consolas', 9),
        'Anchor': AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right | AnchorStyles.Bottom
    })
    
    # Event handlers for raw text buttons
    def add_sample_colors():
        rtb_source.Clear()
        rtb_source.WriteLine("=== Colored Text Sample ===", '#00BFFF')
        rtb_source.WriteLine()
        rtb_source.WriteError("This is an error message")
        rtb_source.WriteWarning("This is a warning message")
        rtb_source.WriteSuccess("This is a success message")
        rtb_source.WriteInfo("This is an info message")
        rtb_source.WriteLine("This is normal text")
        rtb_source.Write("Mixed: ", '#FFFFFF')
        rtb_source.Write("Red ", '#FF0000')
        rtb_source.Write("Green ", '#00FF00')
        rtb_source.WriteLine("Blue", '#0000FF')
    
    btn_add_sample.Click = lambda s, e: add_sample_colors()
    
    def show_text():
        """Demo: Text property (plain text without formatting)"""
        rtb_output.Clear()
        rtb_output.WriteLine("=== .Text Property ===", '#0066CC')
        rtb_output.WriteLine("Gets the plain text content (Windows Forms standard)")
        rtb_output.WriteLine()
        text = rtb_source.Text
        rtb_output.WriteLine(repr(text))
    
    btn_get_text.Click = lambda s, e: show_text()
    
    def show_selected_text():
        """Demo: SelectedText property"""
        rtb_output.Clear()
        rtb_output.WriteLine("=== .SelectedText Property ===", '#0066CC')
        rtb_output.WriteLine("Gets the currently selected plain text")
        rtb_output.WriteLine()
        selected = rtb_source.SelectedText
        if selected:
            rtb_output.WriteLine(repr(selected))
        else:
            rtb_output.WriteWarning("No text selected. Select some text first!")
    
    btn_get_selected.Click = lambda s, e: show_selected_text()
    
    def show_rtf():
        """Demo: Rtf property (RTF format with colors)"""
        rtb_output.Clear()
        rtb_output.WriteLine("=== .Rtf Property ===", '#0066CC')
        rtb_output.WriteLine("Gets the text in RTF format with color table")
        rtb_output.WriteLine()
        rtf = rtb_source.Rtf
        # Show first 1000 chars
        if len(rtf) > 1000:
            rtb_output.WriteLine(rtf[:1000])
            rtb_output.WriteLine(f"\n... truncated ({len(rtf)} total chars)", '#999999')
        else:
            rtb_output.WriteLine(rtf)
    
    btn_get_rtf.Click = lambda s, e: show_rtf()
    
    def show_selected_rtf():
        """Demo: SelectedRtf property"""
        rtb_output.Clear()
        rtb_output.WriteLine("=== .SelectedRtf Property ===", '#0066CC')
        rtb_output.WriteLine("Gets the RTF of the current selection")
        rtb_output.WriteLine()
        selected_rtf = rtb_source.SelectedRtf
        if selected_rtf and len(selected_rtf) > 20:
            rtb_output.WriteLine(selected_rtf)
        else:
            rtb_output.WriteWarning("No text selected. Select some text first!")
    
    btn_get_selected_rtf.Click = lambda s, e: show_selected_rtf()
    
    def show_line():
        """Demo: GetLineText method"""
        rtb_output.Clear()
        rtb_output.WriteLine("=== GetLineText(0) ===", '#0066CC')
        rtb_output.WriteLine("Gets the text of line 0 (first line)")
        rtb_output.WriteLine()
        line = rtb_source.GetLineText(0)
        rtb_output.WriteLine(repr(line))
        rtb_output.WriteLine()
        rtb_output.WriteLine("Other useful properties:", '#0066CC')
        rtb_output.WriteLine(f"  LineCount: {rtb_source.LineCount}", '#666666')
        rtb_output.WriteLine(f"  TextLength: {rtb_source.TextLength}", '#666666')
        rtb_output.WriteLine(f"  SelectionStart: {rtb_source.SelectionStart}", '#666666')
        rtb_output.WriteLine(f"  SelectionLength: {rtb_source.SelectionLength}", '#666666')
    
    btn_get_line.Click = lambda s, e: show_line()
    
    # Add initial sample
    add_sample_colors()
    
    # Run demo on first tab
    demo_write_methods()
    
    return form


def main():
    """Main entry point for the example."""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--full':
        # Run full word processor application
        form = WordProcessorForm()
    else:
        # Run demo form
        form = create_richtextbox_demo()
    
    form.Show()


if __name__ == '__main__':
    main()
