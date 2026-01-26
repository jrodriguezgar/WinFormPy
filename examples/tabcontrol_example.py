"""
TabControl Example - WinFormPy

This example demonstrates comprehensive TabControl and TabPage functionality:
- Creating tabs programmatically
- Adding/removing tabs dynamically
- Tab appearance customization
- Different tab alignments
- Switching between tabs
- Tab events (SelectedIndexChanged)
- Content in each tab
- Multiple TabControls
"""

from winformpy import (
    Application, Form, Label, Button, TextBox, Panel, TabControl, TabPage,
    ListBox, CheckBox, RadioButton, ProgressBar, TrackBar,
    MessageBox, DockStyle, Font, FontStyle, Color
)


class TabControlForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "TabControl Demo"
        self.Width = 1100
        self.Height = 750
        self.StartPosition = "CenterScreen"
        
        # Counter for dynamic tabs
        self.tab_counter = 1
        
        # Apply layout before adding controls
        self.ApplyLayout()
        
        self._init_header()
        self._init_main_tabcontrol()
        self._init_controls_panel()
        self._init_footer()
    
    def _init_header(self):
        """Initialize header panel"""
        header = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 60,
            'BackColor': '#2c3e50'
        })
        
        title = Label(header, {
            'Text': 'TabControl & TabPage Examples',
            'Font': Font('Segoe UI', 16, FontStyle.Bold),
            'ForeColor': 'white',
            'Left': 20,
            'Top': 15,
            'AutoSize': True
        })
    
    def _init_main_tabcontrol(self):
        """Initialize main TabControl with various examples"""
        main_panel = Panel(self, {
            'Dock': DockStyle.Fill,
            'BackColor': '#ecf0f1'
        })
        
        # Main TabControl
        self.tab_main = TabControl(main_panel, {
            'Dock': DockStyle.Fill,
            'Padding': (10, 10)
        })
        self.tab_main.SelectedIndexChanged = self._on_tab_changed
        
        # Tab 1: Basic Controls
        self._create_basic_controls_tab()
        
        # Tab 2: Data Entry
        self._create_data_entry_tab()
        
        # Tab 3: Nested TabControl
        self._create_nested_tabs_tab()
        
        # Tab 4: Dynamic Content
        self._create_dynamic_content_tab()
        
        # Tab 5: Alignment Examples
        self._create_alignment_tab()
    
    def _create_basic_controls_tab(self):
        """Create tab with basic controls"""
        tab = TabPage(self.tab_main, {
            'Text': 'Basic Controls',
            'BackColor': 'white'
        })
        
        # Title
        Label(tab, {
            'Text': 'Common WinFormPy Controls',
            'Font': Font('Segoe UI', 12, FontStyle.Bold),
            'Left': 20,
            'Top': 20,
            'AutoSize': True
        })
        
        # Buttons
        y = 60
        Label(tab, {
            'Text': 'Buttons:',
            'Left': 20,
            'Top': y,
            'Width': 100
        })
        
        Button(tab, {
            'Text': 'Primary',
            'Left': 130,
            'Top': y,
            'Width': 100
        })
        
        Button(tab, {
            'Text': 'Secondary',
            'Left': 240,
            'Top': y,
            'Width': 100
        })
        
        # TextBox
        y += 50
        Label(tab, {
            'Text': 'TextBox:',
            'Left': 20,
            'Top': y,
            'Width': 100
        })
        
        TextBox(tab, {
            'Text': 'Sample text...',
            'Left': 130,
            'Top': y,
            'Width': 250
        })
        
        # CheckBoxes
        y += 50
        Label(tab, {
            'Text': 'CheckBoxes:',
            'Left': 20,
            'Top': y,
            'Width': 100
        })
        
        CheckBox(tab, {
            'Text': 'Option 1',
            'Left': 130,
            'Top': y,
            'Checked': True,
            'AutoSize': True
        })
        
        CheckBox(tab, {
            'Text': 'Option 2',
            'Left': 240,
            'Top': y,
            'AutoSize': True
        })
        
        # RadioButtons
        y += 50
        Label(tab, {
            'Text': 'RadioButtons:',
            'Left': 20,
            'Top': y,
            'Width': 100
        })
        
        RadioButton(tab, {
            'Text': 'Choice A',
            'Left': 130,
            'Top': y,
            'Checked': True,
            'AutoSize': True
        })
        
        RadioButton(tab, {
            'Text': 'Choice B',
            'Left': 240,
            'Top': y,
            'AutoSize': True
        })
        
        # ProgressBar
        y += 50
        Label(tab, {
            'Text': 'ProgressBar:',
            'Left': 20,
            'Top': y,
            'Width': 100
        })
        
        ProgressBar(tab, {
            'Left': 130,
            'Top': y,
            'Width': 300,
            'Value': 60
        })
        
        # TrackBar
        y += 50
        Label(tab, {
            'Text': 'TrackBar:',
            'Left': 20,
            'Top': y,
            'Width': 100
        })
        
        TrackBar(tab, {
            'Left': 130,
            'Top': y,
            'Width': 300,
            'Value': 5,
            'Minimum': 0,
            'Maximum': 10
        })
    
    def _create_data_entry_tab(self):
        """Create tab with data entry form"""
        tab = TabPage(self.tab_main, {
            'Text': 'Data Entry',
            'BackColor': '#f8f9fa'
        })
        
        # Title
        Label(tab, {
            'Text': 'Sample Data Entry Form',
            'Font': Font('Segoe UI', 12, FontStyle.Bold),
            'Left': 20,
            'Top': 20,
            'AutoSize': True
        })
        
        # Form fields
        y = 60
        fields = [
            ('Name:', 'name'),
            ('Email:', 'email'),
            ('Phone:', 'phone'),
            ('Address:', 'address')
        ]
        
        for label_text, field_name in fields:
            Label(tab, {
                'Text': label_text,
                'Left': 20,
                'Top': y,
                'Width': 80
            })
            
            TextBox(tab, {
                'Left': 110,
                'Top': y,
                'Width': 300
            })
            
            y += 40
        
        # Comments
        Label(tab, {
            'Text': 'Comments:',
            'Left': 20,
            'Top': y,
            'Width': 80
        })
        
        TextBox(tab, {
            'Multiline': True,
            'Left': 110,
            'Top': y,
            'Width': 500,
            'Height': 100,
            'ScrollBars': 'Vertical'
        })
        
        # Submit button
        y += 120
        Button(tab, {
            'Text': 'Submit',
            'Left': 110,
            'Top': y,
            'Width': 100,
            'Height': 35
        })
        
        Button(tab, {
            'Text': 'Clear',
            'Left': 220,
            'Top': y,
            'Width': 100,
            'Height': 35
        })
    
    def _create_nested_tabs_tab(self):
        """Create tab with nested TabControl"""
        tab = TabPage(self.tab_main, {
            'Text': 'Nested Tabs',
            'BackColor': 'white'
        })
        
        # Title
        Label(tab, {
            'Text': 'TabControl Inside TabPage',
            'Font': Font('Segoe UI', 12, FontStyle.Bold),
            'Left': 20,
            'Top': 20,
            'AutoSize': True
        })
        
        # Nested TabControl
        nested_tab = TabControl(tab, {
            'Left': 20,
            'Top': 60,
            'Width': 700,
            'Height': 400
        })
        
        # Nested tab pages
        for i in range(1, 4):
            nested_page = TabPage(nested_tab, {
                'Text': f'Sub-Tab {i}',
                'BackColor': '#ecf0f1'
            })
            
            Label(nested_page, {
                'Text': f'This is content for Sub-Tab {i}',
                'Font': Font('Segoe UI', 11),
                'Left': 20,
                'Top': 20,
                'AutoSize': True
            })
            
            ListBox(nested_page, {
                'Left': 20,
                'Top': 60,
                'Width': 300,
                'Height': 200
            }).Items.extend([f'Item {j}' for j in range(1, 11)])
    
    def _create_dynamic_content_tab(self):
        """Create tab with dynamic content"""
        tab = TabPage(self.tab_main, {
            'Text': 'Dynamic Content',
            'BackColor': '#f8f9fa'
        })
        
        # Title
        Label(tab, {
            'Text': 'Dynamically Updated Content',
            'Font': Font('Segoe UI', 12, FontStyle.Bold),
            'Left': 20,
            'Top': 20,
            'AutoSize': True
        })
        
        # Content area
        self.dynamic_content_panel = Panel(tab, {
            'Left': 20,
            'Top': 60,
            'Width': 700,
            'Height': 350,
            'BackColor': 'white',
            'BorderStyle': 'FixedSingle'
        })
        
        # Initial content
        Label(self.dynamic_content_panel, {
            'Text': 'Click buttons below to change content',
            'Left': 250,
            'Top': 150,
            'Width': 200,
            'ForeColor': '#999999'
        })
        
        # Buttons to change content
        y = 430
        btn_content1 = Button(tab, {
            'Text': 'Show List',
            'Left': 20,
            'Top': y,
            'Width': 120
        })
        btn_content1.Click = self._show_dynamic_list
        
        btn_content2 = Button(tab, {
            'Text': 'Show Form',
            'Left': 150,
            'Top': y,
            'Width': 120
        })
        btn_content2.Click = self._show_dynamic_form
        
        btn_content3 = Button(tab, {
            'Text': 'Show Message',
            'Left': 280,
            'Top': y,
            'Width': 120
        })
        btn_content3.Click = self._show_dynamic_message
    
    def _create_alignment_tab(self):
        """Create tab showing different tab alignments"""
        tab = TabPage(self.tab_main, {
            'Text': 'Alignment',
            'BackColor': 'white'
        })
        
        # Title
        Label(tab, {
            'Text': 'TabControl with Different Alignments',
            'Font': Font('Segoe UI', 12, FontStyle.Bold),
            'Left': 20,
            'Top': 20,
            'AutoSize': True
        })
        
        # Left-aligned tabs
        Label(tab, {
            'Text': 'Left Alignment:',
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'Left': 20,
            'Top': 60,
            'AutoSize': True
        })
        
        tab_left = TabControl(tab, {
            'Left': 20,
            'Top': 90,
            'Width': 300,
            'Height': 200,
            'Alignment': 'Left',
            'SizeMode': 'Fixed',
            'ItemSize': (100, 25)
        })
        
        for i in range(1, 4):
            TabPage(tab_left, {
                'Text': f'Tab {i}',
                'BackColor': '#ecf0f1'
            })
        
        # Right-aligned tabs
        Label(tab, {
            'Text': 'Right Alignment:',
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'Left': 340,
            'Top': 60,
            'AutoSize': True
        })
        
        tab_right = TabControl(tab, {
            'Left': 340,
            'Top': 90,
            'Width': 300,
            'Height': 200,
            'Alignment': 'Right',
            'SizeMode': 'Fixed',
            'ItemSize': (100, 25)
        })
        
        for i in range(1, 4):
            TabPage(tab_right, {
                'Text': f'Tab {i}',
                'BackColor': '#ecf0f1'
            })
        
        # Bottom-aligned tabs
        Label(tab, {
            'Text': 'Bottom Alignment:',
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'Left': 20,
            'Top': 310,
            'AutoSize': True
        })
        
        tab_bottom = TabControl(tab, {
            'Left': 20,
            'Top': 340,
            'Width': 620,
            'Height': 150,
            'Alignment': 'Bottom'
        })
        
        for i in range(1, 5):
            TabPage(tab_bottom, {
                'Text': f'Tab {i}',
                'BackColor': '#ecf0f1'
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
            'Text': 'Tab Controls',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'ForeColor': 'white',
            'Left': 20,
            'Top': 20,
            'AutoSize': True
        })
        
        # Current tab info
        Label(panel, {
            'Text': 'Current Tab:',
            'ForeColor': 'white',
            'Left': 20,
            'Top': 60,
            'Width': 180
        })
        
        self.lbl_current_tab = Label(panel, {
            'Text': 'Basic Controls',
            'Font': Font('Segoe UI', 9, FontStyle.Bold),
            'ForeColor': '#3498db',
            'Left': 20,
            'Top': 85,
            'Width': 180
        })
        
        # Add tab button
        btn_add = Button(panel, {
            'Text': 'Add New Tab',
            'Left': 20,
            'Top': 130,
            'Width': 180,
            'Height': 35
        })
        btn_add.Click = self._add_new_tab
        
        # Remove tab button
        btn_remove = Button(panel, {
            'Text': 'Remove Current Tab',
            'Left': 20,
            'Top': 175,
            'Width': 180,
            'Height': 35
        })
        btn_remove.Click = self._remove_current_tab
        
        # Go to first tab
        btn_first = Button(panel, {
            'Text': 'First Tab',
            'Left': 20,
            'Top': 230,
            'Width': 85,
            'Height': 30
        })
        btn_first.Click = lambda s, e: self._goto_tab(0)
        
        # Go to last tab
        btn_last = Button(panel, {
            'Text': 'Last Tab',
            'Left': 115,
            'Top': 230,
            'Width': 85,
            'Height': 30
        })
        btn_last.Click = lambda s, e: self._goto_tab(self.tab_main.TabCount - 1)
        
        # Tab count
        self.lbl_tab_count = Label(panel, {
            'Text': f'Total Tabs: {self.tab_main.TabCount}',
            'ForeColor': 'white',
            'Left': 20,
            'Top': 280,
            'Width': 180
        })
    
    def _init_footer(self):
        """Initialize footer panel"""
        footer = Panel(self, {
            'Dock': DockStyle.Bottom,
            'Height': 50,
            'BackColor': '#ecf0f1'
        })
        
        btn_close = Button(footer, {
            'Text': 'Close',
            'Left': 850,
            'Top': 10,
            'Width': 100,
            'Height': 30
        })
        btn_close.Click = lambda s, e: self.Close()
    
    def _on_tab_changed(self, sender, e):
        """Handle tab selection change"""
        if self.tab_main.SelectedIndex >= 0:
            current_tab = self.tab_main.TabPages[self.tab_main.SelectedIndex]
            self.lbl_current_tab.Text = current_tab.Text
    
    def _add_new_tab(self, sender, e):
        """Add a new tab dynamically"""
        new_tab = TabPage(self.tab_main, {
            'Text': f'New Tab {self.tab_counter}',
            'BackColor': 'white'
        })
        
        Label(new_tab, {
            'Text': f'This is dynamically created Tab {self.tab_counter}',
            'Font': Font('Segoe UI', 11),
            'Left': 20,
            'Top': 20,
            'AutoSize': True
        })
        
        Button(new_tab, {
            'Text': 'Click Me!',
            'Left': 20,
            'Top': 60,
            'Width': 120
        })
        
        self.tab_counter += 1
        self.lbl_tab_count.Text = f'Total Tabs: {self.tab_main.TabCount}'
        
        # Select the new tab
        self.tab_main.SelectedIndex = self.tab_main.TabCount - 1
    
    def _remove_current_tab(self, sender, e):
        """Remove the currently selected tab"""
        if self.tab_main.TabCount <= 1:
            MessageBox.Show('Cannot remove the last tab!', 'Warning', 'OK', 'Warning')
            return
        
        current_index = self.tab_main.SelectedIndex
        if current_index >= 0:
            current_tab = self.tab_main.TabPages[current_index]
            self.tab_main.TabPages.Remove(current_tab)
            self.lbl_tab_count.Text = f'Total Tabs: {self.tab_main.TabCount}'
    
    def _goto_tab(self, index):
        """Go to specific tab by index"""
        if 0 <= index < self.tab_main.TabCount:
            self.tab_main.SelectedIndex = index
    
    def _show_dynamic_list(self, sender, e):
        """Show a list in dynamic content area"""
        self.dynamic_content_panel.Controls.clear()
        
        Label(self.dynamic_content_panel, {
            'Text': 'Dynamic List Content',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 20,
            'Top': 20,
            'AutoSize': True
        })
        
        listbox = ListBox(self.dynamic_content_panel, {
            'Left': 20,
            'Top': 60,
            'Width': 300,
            'Height': 250
        })
        listbox.Items.extend([f'Dynamic Item {i}' for i in range(1, 21)])
    
    def _show_dynamic_form(self, sender, e):
        """Show a form in dynamic content area"""
        self.dynamic_content_panel.Controls.clear()
        
        Label(self.dynamic_content_panel, {
            'Text': 'Dynamic Form Content',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'Left': 20,
            'Top': 20,
            'AutoSize': True
        })
        
        y = 60
        for field in ['Username', 'Password', 'Confirm']:
            Label(self.dynamic_content_panel, {
                'Text': f'{field}:',
                'Left': 20,
                'Top': y,
                'Width': 100
            })
            
            TextBox(self.dynamic_content_panel, {
                'Left': 130,
                'Top': y,
                'Width': 200,
                'PasswordChar': '*' if 'Password' in field else ''
            })
            
            y += 40
        
        Button(self.dynamic_content_panel, {
            'Text': 'Submit',
            'Left': 130,
            'Top': y + 20,
            'Width': 100
        })
    
    def _show_dynamic_message(self, sender, e):
        """Show a message in dynamic content area"""
        self.dynamic_content_panel.Controls.clear()
        
        Label(self.dynamic_content_panel, {
            'Text': 'Dynamic Message Content',
            'Font': Font('Segoe UI', 14, FontStyle.Bold),
            'ForeColor': '#27ae60',
            'Left': 180,
            'Top': 120,
            'Width': 350,
            'Height': 100,
            'TextAlign': 'MiddleCenter'
        })


def main():
    form = TabControlForm()
    Application.Run(form)


if __name__ == '__main__':
    main()
