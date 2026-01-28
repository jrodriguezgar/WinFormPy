"""
TabControl Example - WinFormPy

This example demonstrates TabControl and TabPage functionality:
- Creating tabs programmatically
- Adding/removing tabs dynamically
- Switching between tabs
- Tab events (SelectedIndexChanged)
- Different content in each tab
"""

from winformpy import (
    Application, Form, Label, Button, TextBox, Panel, TabControl, TabPage,
    ListBox, MessageBox, DockStyle, Font, FontStyle
)


class TabControlForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "TabControl Demo"
        self.Width = 800
        self.Height = 600
        self.StartPosition = "CenterScreen"
        
        # Counter for dynamic tabs
        self.tab_counter = 1
        
        # Apply layout before adding controls
        self.ApplyLayout()
        
        self._init_main_tabcontrol()
        self._init_controls_panel()
    
    def _init_main_tabcontrol(self):
        """Initialize main TabControl"""
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
        
        # Tab 1: Welcome
        self._create_welcome_tab()
        
        # Tab 2: Form
        self._create_form_tab()
        
        # Tab 3: List
        self._create_list_tab()
        
        # Tab 4: Nested Tabs
        self._create_nested_tabs_tab()
    
    def _create_welcome_tab(self):
        """Create welcome tab"""
        tab = TabPage(self.tab_main, {
            'Text': 'Welcome',
            'BackColor': 'white'
        })
        
        Label(tab, {
            'Text': 'TabControl Example',
            'Font': Font('Segoe UI', 16, FontStyle.Bold),
            'Left': 50,
            'Top': 50,
            'AutoSize': True
        })
        
        Label(tab, {
            'Text': 'This example demonstrates basic TabControl functionality.',
            'Left': 50,
            'Top': 100,
            'Width': 400,
            'Height': 60
        })
        
        Button(tab, {
            'Text': 'Click Me!',
            'Left': 50,
            'Top': 170,
            'Width': 120,
            'Height': 35
        }).Click = lambda s, e: MessageBox.Show('Hello from Tab 1!', 'Info')
    
    def _create_form_tab(self):
        """Create form tab"""
        tab = TabPage(self.tab_main, {
            'Text': 'Form',
            'BackColor': '#f8f9fa'
        })
        
        Label(tab, {
            'Text': 'Simple Form',
            'Font': Font('Segoe UI', 12, FontStyle.Bold),
            'Left': 50,
            'Top': 30,
            'AutoSize': True
        })
        
        y = 70
        for field in ['Name', 'Email', 'Phone']:
            Label(tab, {
                'Text': f'{field}:',
                'Left': 50,
                'Top': y,
                'Width': 80
            })
            
            TextBox(tab, {
                'Left': 140,
                'Top': y - 3,
                'Width': 250
            })
            
            y += 45
        
        Button(tab, {
            'Text': 'Submit',
            'Left': 140,
            'Top': y + 20,
            'Width': 100,
            'Height': 35
        })
    
    def _create_list_tab(self):
        """Create list tab"""
        tab = TabPage(self.tab_main, {
            'Text': 'List',
            'BackColor': 'white'
        })
        
        Label(tab, {
            'Text': 'Items List',
            'Font': Font('Segoe UI', 12, FontStyle.Bold),
            'Left': 50,
            'Top': 30,
            'AutoSize': True
        })
        
        listbox = ListBox(tab, {
            'Left': 50,
            'Top': 70,
            'Width': 300,
            'Height': 250
        })
        listbox.Items.extend([f'Item {i}' for i in range(1, 16)])
    
    def _create_nested_tabs_tab(self):
        """Create tab with nested TabControl"""
        tab = TabPage(self.tab_main, {
            'Text': 'Nested Tabs',
            'BackColor': 'white'
        })
        
        Label(tab, {
            'Text': 'TabControl Inside TabPage',
            'Font': Font('Segoe UI', 12, FontStyle.Bold),
            'Left': 50,
            'Top': 20,
            'AutoSize': True
        })
        
        # Nested TabControl
        nested_tab = TabControl(tab, {
            'Left': 50,
            'Top': 60,
            'Width': 450,
            'Height': 300
        })
        
        # Sub-tab 1
        sub_tab1 = TabPage(nested_tab, {
            'Text': 'Settings',
            'BackColor': '#f8f9fa'
        })
        
        Label(sub_tab1, {
            'Text': 'Configuration Options',
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'Left': 20,
            'Top': 20,
            'AutoSize': True
        })
        
        for i, option in enumerate(['Enable notifications', 'Auto-save', 'Dark mode']):
            Label(sub_tab1, {
                'Text': option,
                'Left': 20,
                'Top': 60 + (i * 30),
                'Width': 200
            })
        
        # Sub-tab 2
        sub_tab2 = TabPage(nested_tab, {
            'Text': 'Info',
            'BackColor': '#ecf0f1'
        })
        
        Label(sub_tab2, {
            'Text': 'Application Information',
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'Left': 20,
            'Top': 20,
            'AutoSize': True
        })
        
        info_list = ListBox(sub_tab2, {
            'Left': 20,
            'Top': 60,
            'Width': 250,
            'Height': 150
        })
        info_list.Items.extend(['Version: 1.0', 'Build: 2026.01', 'Platform: Windows'])
    
    def _init_controls_panel(self):
        """Initialize control panel"""
        panel = Panel(self, {
            'Dock': DockStyle.Right,
            'Width': 200,
            'BackColor': '#34495e'
        })
        
        Label(panel, {
            'Text': 'Tab Controls',
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'ForeColor': 'white',
            'BackColor': '#34495e',
            'Left': 15,
            'Top': 20,
            'AutoSize': True
        })
        
        self.lbl_current_tab = Label(panel, {
            'Text': 'Current: Welcome',
            'ForeColor': '#3498db',
            'BackColor': '#34495e',
            'Left': 15,
            'Top': 60,
            'Width': 170
        })
        
        self.lbl_tab_count = Label(panel, {
            'Text': f'Total: {self.tab_main.TabCount}',
            'ForeColor': 'white',
            'BackColor': '#34495e',
            'Left': 15,
            'Top': 90,
            'Width': 170
        })
        
        Button(panel, {
            'Text': 'Add New Tab',
            'Left': 15,
            'Top': 130,
            'Width': 170,
            'Height': 35
        }).Click = self._add_new_tab
        
        Button(panel, {
            'Text': 'Remove Tab',
            'Left': 15,
            'Top': 175,
            'Width': 170,
            'Height': 35
        }).Click = self._remove_current_tab
        
        Button(panel, {
            'Text': 'First',
            'Left': 15,
            'Top': 230,
            'Width': 80,
            'Height': 30
        }).Click = lambda s, e: self._goto_tab(0)
        
        Button(panel, {
            'Text': 'Last',
            'Left': 105,
            'Top': 230,
            'Width': 80,
            'Height': 30
        }).Click = lambda s, e: self._goto_tab(self.tab_main.TabCount - 1)
    
    def _on_tab_changed(self, sender, e):
        """Handle tab selection change"""
        if self.tab_main.SelectedIndex >= 0:
            current_tab = self.tab_main.TabPages[self.tab_main.SelectedIndex]
            self.lbl_current_tab.Text = f'Current: {current_tab.Text}'
    
    def _add_new_tab(self, sender, e):
        """Add a new tab dynamically"""
        tab_text = f'Tab {self.tab_counter}'
        new_tab = TabPage(self.tab_main, {
            'Text': tab_text,
            'BackColor': 'white'
        })
        
        Label(new_tab, {
            'Text': f'Dynamically created {tab_text}',
            'Font': Font('Segoe UI', 11),
            'Left': 50,
            'Top': 50,
            'AutoSize': True
        })
        
        btn = Button(new_tab, {
            'Text': 'Test Button',
            'Left': 50,
            'Top': 100,
            'Width': 120,
            'Height': 35
        })
        btn.Click = lambda s, e, t=tab_text: MessageBox.Show(f'{t} button clicked!', 'Info')
        
        self.tab_counter += 1
        self.lbl_tab_count.Text = f'Total: {self.tab_main.TabCount}'
        self.tab_main.SelectedIndex = self.tab_main.TabCount - 1
    
    def _remove_current_tab(self, sender, e):
        """Remove the currently selected tab"""
        if self.tab_main.TabCount <= 1:
            MessageBox.Show('Cannot remove the last tab!', 'Warning')
            return
        
        current_index = self.tab_main.SelectedIndex
        if current_index >= 0:
            current_tab = self.tab_main.TabPages[current_index]
            self.tab_main.RemoveTab(current_tab)
            self.lbl_tab_count.Text = f'Total: {self.tab_main.TabCount}'
    
    def _goto_tab(self, index):
        """Go to specific tab by index"""
        if 0 <= index < self.tab_main.TabCount:
            self.tab_main.SelectedIndex = index


def main():
    form = TabControlForm()
    Application.Run(form)


if __name__ == '__main__':
    main()
