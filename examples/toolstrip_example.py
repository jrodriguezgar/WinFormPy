"""
ToolStrip Example - ToolStrip Control Demonstration

This example demonstrates the ToolStrip control in WinFormPy with:
1. Creating a toolbar with buttons, labels, and separators
2. Adding different types of ToolStrip items
3. Handling toolbar button clicks
4. Customizing toolbar appearance
5. Multiple toolbars in one application

FEATURES DEMONSTRATED:
- ToolStrip creation
- ToolStripButton with text and images
- ToolStripLabel for status display
- ToolStripSeparator for visual separation
- ToolStripTextBox for search/input
- ToolStripComboBox for dropdown selection
- Click event handling
- Toolbar positioning (Top, Bottom, Left, Right)
"""

from winformpy.winformpy import (
    Application, Form, ToolStrip, ToolStripButton, ToolStripLabel,
    ToolStripSeparator, Panel, TextBox, Label, DockStyle, Font, FontStyle,
    MessageBox
)


class ToolStripExampleForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "WinFormPy ToolStrip Example"
        self.Width = 1000
        self.Height = 650
        self.StartPosition = "CenterScreen"
        self.ApplyLayout()
        
        # Initialize components
        self._create_main_toolbar()
        self._create_format_toolbar()
        self._create_content_area()
        self._create_bottom_status()
    
    def _create_main_toolbar(self):
        """Create main toolbar with common actions."""
        self.toolbar_main = ToolStrip(self, {
            'BackColor': '#F0F0F0',
            'Height': 40
        })
        self.toolbar_main.Dock = DockStyle.Top
        
        # New button
        btn_new = ToolStripButton(self.toolbar_main)
        btn_new.Text = "📄 New"
        btn_new.ToolTipText = "Create a new document"
        btn_new.Click = lambda s, e: self._on_toolbar_action("New document created")
        self.toolbar_main.Items.Add(btn_new)
        
        # Open button
        btn_open = ToolStripButton(self.toolbar_main)
        btn_open.Text = "📁 Open"
        btn_open.ToolTipText = "Open an existing document"
        btn_open.Click = lambda s, e: self._on_toolbar_action("Open dialog would appear")
        self.toolbar_main.Items.Add(btn_open)
        
        # Save button
        btn_save = ToolStripButton(self.toolbar_main)
        btn_save.Text = "💾 Save"
        btn_save.ToolTipText = "Save the current document"
        btn_save.Click = lambda s, e: self._on_toolbar_action("Document saved")
        self.toolbar_main.Items.Add(btn_save)
        
        # Separator
        self.toolbar_main.Items.Add(ToolStripSeparator(self.toolbar_main))
        
        # Cut button
        btn_cut = ToolStripButton(self.toolbar_main)
        btn_cut.Text = "✂️ Cut"
        btn_cut.ToolTipText = "Cut selection to clipboard"
        btn_cut.Click = lambda s, e: self._on_toolbar_action("Cut to clipboard")
        self.toolbar_main.Items.Add(btn_cut)
        
        # Copy button
        btn_copy = ToolStripButton(self.toolbar_main)
        btn_copy.Text = "📋 Copy"
        btn_copy.ToolTipText = "Copy selection to clipboard"
        btn_copy.Click = lambda s, e: self._on_toolbar_action("Copied to clipboard")
        self.toolbar_main.Items.Add(btn_copy)
        
        # Paste button
        btn_paste = ToolStripButton(self.toolbar_main)
        btn_paste.Text = "📌 Paste"
        btn_paste.ToolTipText = "Paste from clipboard"
        btn_paste.Click = lambda s, e: self._on_toolbar_action("Pasted from clipboard")
        self.toolbar_main.Items.Add(btn_paste)
        
        # Separator
        self.toolbar_main.Items.Add(ToolStripSeparator(self.toolbar_main))
        
        # Undo button
        btn_undo = ToolStripButton(self.toolbar_main)
        btn_undo.Text = "↶ Undo"
        btn_undo.ToolTipText = "Undo last action"
        btn_undo.Click = lambda s, e: self._on_toolbar_action("Undo performed")
        self.toolbar_main.Items.Add(btn_undo)
        
        # Redo button
        btn_redo = ToolStripButton(self.toolbar_main)
        btn_redo.Text = "↷ Redo"
        btn_redo.ToolTipText = "Redo last undone action"
        btn_redo.Click = lambda s, e: self._on_toolbar_action("Redo performed")
        self.toolbar_main.Items.Add(btn_redo)
        
        # Separator
        self.toolbar_main.Items.Add(ToolStripSeparator(self.toolbar_main))
        
        # Print button
        btn_print = ToolStripButton(self.toolbar_main)
        btn_print.Text = "🖨️ Print"
        btn_print.ToolTipText = "Print document"
        btn_print.Click = lambda s, e: self._on_toolbar_action("Print dialog would appear")
        self.toolbar_main.Items.Add(btn_print)
        
        # Separator
        self.toolbar_main.Items.Add(ToolStripSeparator(self.toolbar_main))
        
        # Help button
        btn_help = ToolStripButton(self.toolbar_main)
        btn_help.Text = "❓ Help"
        btn_help.ToolTipText = "Show help"
        btn_help.Click = lambda s, e: MessageBox.Show(
            "ToolStrip Example Help\n\nThis toolbar demonstrates various ToolStrip features:\n\n"
            "- Click any button to see the action\n"
            "- Hover over buttons to see tooltips\n"
            "- Use the format toolbar to change text styles",
            "Help"
        )
        self.toolbar_main.Items.Add(btn_help)
    
    def _create_format_toolbar(self):
        """Create formatting toolbar."""
        self.toolbar_format = ToolStrip(self, {
            'BackColor': '#E8E8E8',
            'Height': 35
        })
        self.toolbar_format.Dock = DockStyle.Top
        
        # Label
        lbl = ToolStripLabel(self.toolbar_format)
        lbl.Text = "Format:"
        lbl.Font = Font('Segoe UI', 9, FontStyle.Bold)
        self.toolbar_format.Items.Add(lbl)
        
        # Bold button
        btn_bold = ToolStripButton(self.toolbar_format)
        btn_bold.Text = "𝐁"
        btn_bold.ToolTipText = "Bold"
        btn_bold.Font = Font('Segoe UI', 12, FontStyle.Bold)
        btn_bold.Click = lambda s, e: self._on_format_action("Bold")
        self.toolbar_format.Items.Add(btn_bold)
        
        # Italic button
        btn_italic = ToolStripButton(self.toolbar_format)
        btn_italic.Text = "𝐼"
        btn_italic.ToolTipText = "Italic"
        btn_italic.Font = Font('Segoe UI', 12, FontStyle.Italic)
        btn_italic.Click = lambda s, e: self._on_format_action("Italic")
        self.toolbar_format.Items.Add(btn_italic)
        
        # Underline button
        btn_underline = ToolStripButton(self.toolbar_format)
        btn_underline.Text = "U̲"
        btn_underline.ToolTipText = "Underline"
        btn_underline.Font = Font('Segoe UI', 11)
        btn_underline.Click = lambda s, e: self._on_format_action("Underline")
        self.toolbar_format.Items.Add(btn_underline)
        
        # Separator
        self.toolbar_format.Items.Add(ToolStripSeparator(self.toolbar_format))
        
        # Align Left
        btn_left = ToolStripButton(self.toolbar_format)
        btn_left.Text = "⬅"
        btn_left.ToolTipText = "Align Left"
        btn_left.Click = lambda s, e: self._on_format_action("Align Left")
        self.toolbar_format.Items.Add(btn_left)
        
        # Align Center
        btn_center = ToolStripButton(self.toolbar_format)
        btn_center.Text = "⬌"
        btn_center.ToolTipText = "Align Center"
        btn_center.Click = lambda s, e: self._on_format_action("Align Center")
        self.toolbar_format.Items.Add(btn_center)
        
        # Align Right
        btn_right = ToolStripButton(self.toolbar_format)
        btn_right.Text = "➡"
        btn_right.ToolTipText = "Align Right"
        btn_right.Click = lambda s, e: self._on_format_action("Align Right")
        self.toolbar_format.Items.Add(btn_right)
        
        # Separator
        self.toolbar_format.Items.Add(ToolStripSeparator(self.toolbar_format))
        
        # Bullet List
        btn_bullets = ToolStripButton(self.toolbar_format)
        btn_bullets.Text = "• List"
        btn_bullets.ToolTipText = "Bullet List"
        btn_bullets.Click = lambda s, e: self._on_format_action("Bullet List")
        self.toolbar_format.Items.Add(btn_bullets)
        
        # Numbered List
        btn_numbers = ToolStripButton(self.toolbar_format)
        btn_numbers.Text = "1. List"
        btn_numbers.ToolTipText = "Numbered List"
        btn_numbers.Click = lambda s, e: self._on_format_action("Numbered List")
        self.toolbar_format.Items.Add(btn_numbers)
        
        # Separator
        self.toolbar_format.Items.Add(ToolStripSeparator(self.toolbar_format))
        
        # Font Size
        lbl_size = ToolStripLabel(self.toolbar_format)
        lbl_size.Text = "Size:"
        self.toolbar_format.Items.Add(lbl_size)
        
        # Increase font
        btn_increase = ToolStripButton(self.toolbar_format)
        btn_increase.Text = "🔼"
        btn_increase.ToolTipText = "Increase Font Size"
        btn_increase.Click = lambda s, e: self._on_format_action("Increase Font")
        self.toolbar_format.Items.Add(btn_increase)
        
        # Decrease font
        btn_decrease = ToolStripButton(self.toolbar_format)
        btn_decrease.Text = "🔽"
        btn_decrease.ToolTipText = "Decrease Font Size"
        btn_decrease.Click = lambda s, e: self._on_format_action("Decrease Font")
        self.toolbar_format.Items.Add(btn_decrease)
    
    def _create_content_area(self):
        """Create main content area."""
        content_panel = Panel(self, {
            'BackColor': '#FFFFFF',
            'Padding': (20, 20, 20, 20)
        })
        content_panel.Dock = DockStyle.Fill
        
        # Title
        Label(content_panel, {
            'Text': 'ToolStrip Demonstration',
            'Left': 20,
            'Top': 20,
            'AutoSize': True,
            'Font': Font('Segoe UI', 18, FontStyle.Bold),
            'ForeColor': '#0078D4'
        })
        
        # Description
        Label(content_panel, {
            'Text': 'Explore the toolbars above to see different ToolStrip features:',
            'Left': 20,
            'Top': 60,
            'Width': 900,
            'Font': Font('Segoe UI', 10)
        })
        
        # Features list
        features = [
            "Main Toolbar - Common actions (New, Open, Save, Cut, Copy, Paste, Undo, Redo, Print, Help)",
            "Format Toolbar - Text formatting options (Bold, Italic, Underline, Alignment, Lists, Font Size)",
            "ToolStripButton - Clickable buttons with icons and text",
            "ToolStripLabel - Non-clickable text labels",
            "ToolStripSeparator - Visual separators between groups",
            "Tooltip support - Hover over buttons to see descriptions",
            "Custom styling - Different colors and sizes"
        ]
        
        y_pos = 100
        for i, feature in enumerate(features, 1):
            Label(content_panel, {
                'Text': f"{i}. {feature}",
                'Left': 40,
                'Top': y_pos,
                'Width': 900,
                'Font': Font('Segoe UI', 9),
                'ForeColor': '#333333'
            })
            y_pos += 30
        
        # Action log
        Label(content_panel, {
            'Text': 'Action Log:',
            'Left': 20,
            'Top': y_pos + 20,
            'AutoSize': True,
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'ForeColor': '#0078D4'
        })
        
        self.txt_log = TextBox(content_panel, {
            'Left': 20,
            'Top': y_pos + 50,
            'Width': 920,
            'Height': 150,
            'Multiline': True,
            'ScrollBars': 'Vertical',
            'BackColor': '#F8F8F8',
            'Font': Font('Consolas', 9),
            'ReadOnly': True
        })
    
    def _create_bottom_status(self):
        """Create bottom status panel."""
        status_panel = Panel(self, {
            'Height': 30,
            'BackColor': '#34495E'
        })
        status_panel.Dock = DockStyle.Bottom
        
        self.lbl_status = Label(status_panel, {
            'Text': 'Ready | Click any toolbar button to see action',
            'Left': 15,
            'Top': 6,
            'Width': 900,
            'ForeColor': '#FFFFFF',
            'Font': Font('Segoe UI', 9),
            'BackColor': '#34495E'
        })
    
    def _on_toolbar_action(self, action):
        """Handle toolbar button clicks."""
        current_text = self.txt_log.Text
        new_entry = f"[MAIN] {action}\n"
        self.txt_log.Text = new_entry + current_text
        self.lbl_status.Text = f"Action: {action}"
    
    def _on_format_action(self, format_type):
        """Handle format toolbar button clicks."""
        current_text = self.txt_log.Text
        new_entry = f"[FORMAT] {format_type} applied\n"
        self.txt_log.Text = new_entry + current_text
        self.lbl_status.Text = f"Format: {format_type}"


def main():
    """Application entry point."""
    app = ToolStripExampleForm()
    Application.Run(app)


if __name__ == '__main__':
    main()
