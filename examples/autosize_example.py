"""
AutoSize Comprehensive Demo

This example demonstrates AutoSize behavior with various controls and containers:

- Basic controls (Label, Button, CheckBox, TextBox)
- Container controls (GroupBox, Panel)
- TabControl with dynamic TabPages
- AutoSizeMode options: GrowAndShrink vs GrowOnly
"""

from winformpy import (
    Form, Label, Button, CheckBox, RadioButton, TextBox, GroupBox,
    Panel, TabControl, TabPage,
    DockStyle, AnchorStyles, AutoSizeMode, Color, Font, FontStyle,
    ContentAlignment
)



def main():
    # =========================================================================
    # Create main form
    # =========================================================================
    form = Form({
        'Text': 'AutoSize Comprehensive Demo',
        'Width': 1000,
        'Height': 750,
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
        'Text': 'AutoSize Comprehensive Demo',
        'Left': 20,
        'Top': 12,
        'AutoSize': True,
        'Font': Font('Segoe UI', 16, FontStyle.Bold),
        'ForeColor': '#FFFFFF',
        'BackColor': '#0078D4'
    })
    
    # =========================================================================
    # TabControl - Main content
    # =========================================================================
    tabs = TabControl(form, {
        'Dock': DockStyle.Fill,
        'Alignment': 'Left'
    })
    
    # =========================================================================
    # Tab 1: Basic Controls
    # =========================================================================
    tab_basic = TabPage(tabs, {'Text': 'Basic Controls'})
    tabs.AddTab(tab_basic)
    
    # Banner
    banner_basic = Label(tab_basic, {
        'Text': 'BASIC CONTROLS AUTOSIZE: Toggle AutoSize on/off and change text to see how Label, Button, CheckBox, and TextBox adjust their size automatically. Basic controls always use GrowAndShrink mode.',
        'Dock': DockStyle.Top,
        'Height': 50,
        'BackColor': '#2C2C2C',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9, FontStyle.Bold),
        'TextAlign': ContentAlignment.MiddleLeft,
        'Padding': (15, 10, 15, 10)
    })
    
    # Control Panel (Left)
    panel_controls_basic = Panel(tab_basic, {
        'Dock': DockStyle.Left,
        'Width': 250,
        'BackColor': '#F5F5F5',
        'AutoScroll': True
    })
    
    # Demo Area (Right - Fill)
    panel_demo = Panel(tab_basic, {
        'Dock': DockStyle.Fill,
        'BackColor': '#FFFFFF'
    })
    
    lbl_instr = Label(panel_controls_basic, {
        'Text': 'Control Properties:',
        'Top': 10,
        'Left': 10,
        'Font': Font('Segoe UI', 10, FontStyle.Bold),
        'AutoSize': True
    })
    
    # AutoSize Toggle
    chk_autosize = CheckBox(panel_controls_basic, {
        'Text': 'AutoSize Enabled',
        'Top': 40,
        'Left': 10,
        'Checked': False,
        'AutoSize': True
    })
    
    # Text Input
    Label(panel_controls_basic, {
        'Text': 'Text Content:',
        'Top': 70,
        'Left': 10,
        'AutoSize': True
    })
    
    txt_content = TextBox(panel_controls_basic, {
        'Top': 90,
        'Left': 10,
        'Width': 220,
        'Text': 'AutoSize Me!'
    })
    
    # Info note
    Label(panel_controls_basic, {
        'Text': 'Note: Basic controls always\nuse GrowAndShrink behavior\nwhen AutoSize is enabled.',
        'Top': 120,
        'Left': 10,
        'AutoSize': True,
        'ForeColor': '#808080',
        'Font': Font('Segoe UI', 8, FontStyle.Italic)
    })
    
    # Target Selection
    Label(panel_controls_basic, {
        'Text': 'Select Target:',
        'Top': 190,
        'Left': 10,
        'AutoSize': True
    })
    
    rb_label = RadioButton(panel_controls_basic, {
        'Text': 'Label',
        'Top': 210,
        'Left': 10,
        'Checked': True,
        'AutoSize': True
    })
    
    rb_button = RadioButton(panel_controls_basic, {
        'Text': 'Button',
        'Top': 235,
        'Left': 10,
        'AutoSize': True
    })
    
    rb_checkbox = RadioButton(panel_controls_basic, {
        'Text': 'CheckBox',
        'Top': 260,
        'Left': 10,
        'AutoSize': True
    })
    
    rb_textbox = RadioButton(panel_controls_basic, {
        'Text': 'TextBox (Multiline)',
        'Top': 285,
        'Left': 10,
        'AutoSize': True
    })
    
    # Info Label
    lbl_info = Label(panel_controls_basic, {
        'Text': 'Size: 0, 0',
        'Top': 320,
        'Left': 10,
        'AutoSize': True,
        'ForeColor': '#0078D4'
    })
    
    # Demo Controls
    demo_label = Label(panel_demo, {
        'Text': 'AutoSize Me!',
        'Left': 50,
        'Top': 50,
        'BackColor': '#FFFFE0',
        'BorderStyle': 'solid',
        'AutoSize': False,
        'Width': 200,
        'Height': 30
    })
    
    demo_button = Button(panel_demo, {
        'Text': 'AutoSize Me!',
        'Left': 50,
        'Top': 50,
        'AutoSize': False,
        'Visible': False,
        'Width': 200,
        'Height': 30
    })
    
    demo_checkbox = CheckBox(panel_demo, {
        'Text': 'AutoSize Me!',
        'Left': 50,
        'Top': 50,
        'AutoSize': False,
        'Visible': False,
        'Width': 200,
        'Height': 30
    })
    
    demo_textbox = TextBox(panel_demo, {
        'Text': 'AutoSize Me!',
        'Left': 50,
        'Top': 50,
        'Multiline': True,
        'AutoSize': False,
        'Visible': False,
        'BackColor': '#F0F8FF',
        'Width': 200,
        'Height': 80
    })
    
    # Store current control reference
    current_control = [demo_label]  # Using list to allow modification in nested function
    
    def update_info():
        """Update size information display."""
        current_control[0].Invalidate()
        w = current_control[0].Width
        h = current_control[0].Height
        lbl_info.Text = f'Size: {w}, {h}'
    
    def on_apply_changes(sender, e):
        """Apply text and AutoSize changes to the current control."""
        # Hide all first
        demo_label.Visible = False
        demo_button.Visible = False
        demo_checkbox.Visible = False
        demo_textbox.Visible = False
        
        # Determine which control is selected
        if rb_label.Checked:
            current_control[0] = demo_label
        elif rb_button.Checked:
            current_control[0] = demo_button
        elif rb_checkbox.Checked:
            current_control[0] = demo_checkbox
        elif rb_textbox.Checked:
            current_control[0] = demo_textbox
        
        # Show the selected control
        current_control[0].Visible = True
        
        # Get AutoSize state from checkbox
        autosize_enabled = chk_autosize.Checked
        current_control[0].AutoSize = autosize_enabled
        
        # Set fixed size if AutoSize is disabled
        if not current_control[0].AutoSize:
            if isinstance(current_control[0], TextBox):
                current_control[0].Width = 200
                current_control[0].Height = 80
            else:
                current_control[0].Width = 200
                current_control[0].Height = 30
        
        # Set the new text
        current_control[0].Text = txt_content.Text
        
        update_info()
    
    # Apply Changes Button
    btn_apply = Button(panel_controls_basic, {
        'Text': 'Apply Changes',
        'Top': 360,
        'Left': 10,
        'Width': 220
    })
    btn_apply.Click = on_apply_changes
    
    update_info()
    
    # =========================================================================
    # Tab 2: GroupBox AutoSize
    # =========================================================================
    tab_groupbox = TabPage(tabs, {'Text': 'GroupBox AutoSize'})
    tabs.AddTab(tab_groupbox)
    
    # Banner
    banner_groupbox = Label(tab_groupbox, {
        'Text': 'GROUPBOX AUTOSIZE MODES: Add/remove controls dynamically to see AutoSize behavior. GrowOnly mode only grows (never shrinks). GrowAndShrink mode adjusts to fit content (grows and shrinks).',
        'Dock': DockStyle.Top,
        'Height': 50,
        'BackColor': '#2C2C2C',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9, FontStyle.Bold),
        'TextAlign': ContentAlignment.MiddleLeft,
        'Padding': (15, 10, 15, 10)
    })
    
    # Title
    Label(tab_groupbox, {
        'Text': 'GroupBox AutoSize Demo - Add/Remove controls dynamically',
        'Top': 60,
        'Left': 10,
        'Font': Font('Segoe UI', 11, FontStyle.Bold),
        'AutoSize': True,
        'ForeColor': '#003D5B'
    })
    
    # Control Panel
    panel_controls_grp = Panel(tab_groupbox, {
        'Top': 100,
        'Left': 10,
        'Width': 200,
        'Height': 200,
        'BackColor': '#F5F5F5',
        'BorderStyle': 'solid'
    })
    
    Label(panel_controls_grp, {
        'Text': 'Controls:',
        'Top': 10,
        'Left': 10,
        'AutoSize': True,
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })
    
    # GroupBox Demo Area
    grp_auto = GroupBox(tab_groupbox, {
        'Text': 'AutoSize GroupBox (GrowAndShrink)',
        'Left': 230,
        'Top': 100,
        'AutoSize': True,
        'AutoSizeMode': AutoSizeMode.GrowAndShrink,
        'BackColor': '#FFFFE0',
        'Padding': (10, 25, 10, 10)
    })
    
    # Add initial control
    Label(grp_auto, {
        'Text': 'Initial content in GroupBox',
        'Top': 30,
        'Left': 10,
        'AutoSize': True
    })
    
    # Info Label
    lbl_groupbox_info = Label(tab_groupbox, {
        'Text': 'GroupBox Size: 0 x 0',
        'Top': 320,
        'Left': 10,
        'AutoSize': True,
        'ForeColor': '#0078D4',
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })
    
    # Fixed Size GroupBox for comparison
    grp_fixed = GroupBox(tab_groupbox, {
        'Text': 'Fixed Size GroupBox (AutoSize=False)',
        'Left': 550,
        'Top': 100,
        'Width': 250,
        'Height': 150,
        'AutoSize': False,
        'BackColor': '#E0FFFF',
        'Padding': (10, 25, 10, 10)
    })
    
    Label(grp_fixed, {
        'Text': 'This GroupBox has fixed size\nand won\'t grow with content',
        'Top': 25,
        'Left': 10,
        'AutoSize': True
    })
    
    grp_auto_counter = [0]  # Using list to allow modification
    
    def update_groupbox_info():
        """Update GroupBox size information."""
        grp_auto.Invalidate()
        grp_fixed.Invalidate()
        
        w_auto = grp_auto.Width
        h_auto = grp_auto.Height
        count_auto = len(grp_auto.Controls)
        
        w_fixed = grp_fixed.Width
        h_fixed = grp_fixed.Height
        count_fixed = len(grp_fixed.Controls)
        
        lbl_groupbox_info.Text = (
            f'AutoSize: {w_auto}x{h_auto} ({count_auto} controls) | '
            f'Fixed: {w_fixed}x{h_fixed} ({count_fixed} controls)'
        )
    
    def add_to_groupbox(control_type):
        """Add a control to both GroupBoxes for comparison."""
        grp_auto_counter[0] += 1
        
        # Add to both GroupBoxes to show the difference
        for grp in [grp_auto, grp_fixed]:
            # Calculate position based on number of controls already in this GroupBox
            num_controls = len(grp.Controls)
            y_pos = 30 + (num_controls * 30)
            
            # Create control based on type
            if control_type == 'button':
                ctrl = Button(grp, {
                    'Text': f'Button {grp_auto_counter[0]}',
                    'AutoSize': True
                })
            elif control_type == 'label':
                ctrl = Label(grp, {
                    'Text': f'Label {grp_auto_counter[0]} - Dynamic',
                    'AutoSize': True
                })
            elif control_type == 'checkbox':
                ctrl = CheckBox(grp, {
                    'Text': f'CheckBox {grp_auto_counter[0]}',
                    'AutoSize': True
                })
            
            # Set position after auto-registration
            ctrl.Top = y_pos
            ctrl.Left = 10
        
        update_groupbox_info()
    
    def remove_from_groupbox(sender, e):
        """Remove last control from both GroupBoxes."""
        # Remove from both GroupBoxes
        for grp in [grp_auto, grp_fixed]:
            if len(grp.Controls) > 1:  # Keep at least one
                last_control = grp.Controls[-1]
                grp.RemoveControl(last_control)
        update_groupbox_info()
    
    def clear_groupbox(sender, e):
        """Clear all controls from both GroupBoxes."""
        # Remove all controls from both GroupBoxes
        for grp in [grp_auto, grp_fixed]:
            while len(grp.Controls) > 0:
                grp.RemoveControl(grp.Controls[-1])
            
            # Add back initial control
            lbl = Label(grp, {
                'Text': 'Initial content in GroupBox',
                'Top': 30,
                'Left': 10,
                'AutoSize': True
            })
        
        grp_auto_counter[0] = 0
        update_groupbox_info()
    
    # Buttons for GroupBox operations
    btn_add_button = Button(panel_controls_grp, {
        'Text': 'Add Button',
        'Top': 35,
        'Left': 10,
        'Width': 180
    })
    btn_add_button.Click = lambda s, e: add_to_groupbox('button')
    
    btn_add_label = Button(panel_controls_grp, {
        'Text': 'Add Label',
        'Top': 65,
        'Left': 10,
        'Width': 180
    })
    btn_add_label.Click = lambda s, e: add_to_groupbox('label')
    
    btn_add_checkbox = Button(panel_controls_grp, {
        'Text': 'Add CheckBox',
        'Top': 95,
        'Left': 10,
        'Width': 180
    })
    btn_add_checkbox.Click = lambda s, e: add_to_groupbox('checkbox')
    
    btn_remove = Button(panel_controls_grp, {
        'Text': 'Remove Last',
        'Top': 125,
        'Left': 10,
        'Width': 180
    })
    btn_remove.Click = remove_from_groupbox
    
    btn_clear = Button(panel_controls_grp, {
        'Text': 'Clear All',
        'Top': 155,
        'Left': 10,
        'Width': 180
    })
    btn_clear.Click = clear_groupbox
    
    update_groupbox_info()
    
    # =========================================================================
    # Tab 3: Panel AutoSize
    # =========================================================================
    tab_panel = TabPage(tabs, {'Text': 'Panel AutoSize'})
    tabs.AddTab(tab_panel)
    
    # Banner
    banner_panel = Label(tab_panel, {
        'Text': 'PANEL AUTOSIZE COMPARISON: Compare three panels with different AutoSize settings. GrowAndShrink adjusts to content size. GrowOnly grows but never shrinks. Fixed Size has AutoSize disabled.',
        'Dock': DockStyle.Top,
        'Height': 50,
        'BackColor': '#2C2C2C',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9, FontStyle.Bold),
        'TextAlign': ContentAlignment.MiddleLeft,
        'Padding': (15, 10, 15, 10)
    })
    
    # Title
    Label(tab_panel, {
        'Text': 'Panel AutoSize Demo - Compare AutoSize modes',
        'Top': 60,
        'Left': 10,
        'Font': Font('Segoe UI', 11, FontStyle.Bold),
        'AutoSize': True,
        'ForeColor': '#003D5B'
    })
    
    # Control Panel
    panel_controls_panel = Panel(tab_panel, {
        'Top': 90,
        'Left': 10,
        'Width': 180,
        'Height': 150,
        'BackColor': '#F5F5F5',
        'BorderStyle': 'solid'
    })
    
    Label(panel_controls_panel, {
        'Text': 'Add controls:',
        'Top': 10,
        'Left': 10,
        'AutoSize': True,
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })
    
    # Panel 1: GrowAndShrink
    Label(tab_panel, {
        'Text': 'Panel - AutoSizeMode.GrowAndShrink',
        'Top': 250,
        'Left': 10,
        'AutoSize': True,
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })
    
    panel_grow_shrink = Panel(tab_panel, {
        'Top': 270,
        'Left': 10,
        'AutoSize': True,
        'AutoSizeMode': AutoSizeMode.GrowAndShrink,
        'BackColor': '#90EE90',
        'BorderStyle': 'solid',
        'Padding': (5, 5, 5, 5)
    })
    
    # Panel 2: GrowOnly
    Label(tab_panel, {
        'Text': 'Panel - AutoSizeMode.GrowOnly',
        'Top': 250,
        'Left': 250,
        'AutoSize': True,
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })
    
    panel_grow_only = Panel(tab_panel, {
        'Top': 270,
        'Left': 250,
        'AutoSize': True,
        'AutoSizeMode': AutoSizeMode.GrowOnly,
        'BackColor': '#F08080',
        'BorderStyle': 'solid',
        'Padding': (5, 5, 5, 5)
    })
    
    # Panel 3: Fixed Size (no AutoSize)
    Label(tab_panel, {
        'Text': 'Panel - Fixed Size (AutoSize=False)',
        'Top': 250,
        'Left': 490,
        'AutoSize': True,
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })
    
    panel_fixed = Panel(tab_panel, {
        'Top': 270,
        'Left': 490,
        'Width': 200,
        'Height': 100,
        'AutoSize': False,
        'BackColor': '#ADD8E6',
        'BorderStyle': 'solid',
        'Padding': (5, 5, 5, 5)
    })
    
    # Info Labels
    lbl_panel_info1 = Label(tab_panel, {
        'Top': 370,
        'Left': 10,
        'AutoSize': True,
        'ForeColor': '#006400'
    })
    
    lbl_panel_info2 = Label(tab_panel, {
        'Top': 370,
        'Left': 250,
        'AutoSize': True,
        'ForeColor': '#8B0000'
    })
    
    lbl_panel_info3 = Label(tab_panel, {
        'Top': 370,
        'Left': 490,
        'AutoSize': True,
        'ForeColor': '#00008B'
    })
    
    panel_counter = [0]
    
    def update_panel_info():
        """Update panel size information."""
        # Force layout update before reading dimensions
        panel_grow_shrink.Invalidate()
        panel_grow_only.Invalidate()
        panel_fixed.Invalidate()
        
        lbl_panel_info1.Text = (
            f'Size: {panel_grow_shrink.Width}x{panel_grow_shrink.Height}\n'
            f'Grows and shrinks'
        )
        lbl_panel_info2.Text = (
            f'Size: {panel_grow_only.Width}x{panel_grow_only.Height}\n'
            f'Grows only, doesn\'t shrink'
        )
        lbl_panel_info3.Text = (
            f'Size: {panel_fixed.Width}x{panel_fixed.Height}\n'
            f'Fixed size (may clip)'
        )
    
    def add_to_panels(sender, e):
        """Add controls to all three panels."""
        panel_counter[0] += 1
        y_pos = 5 + (len(panel_grow_shrink.Controls) * 30)
        
        for panel in [panel_grow_shrink, panel_grow_only, panel_fixed]:
            btn = Button(panel, {
                'Text': f'Btn {panel_counter[0]}',
                'Top': y_pos,
                'Left': 5,
                'AutoSize': True
            })
        
        update_panel_info()
    
    def clear_panels(sender, e):
        """Clear all panels."""
        # Remove controls properly using RemoveControl
        while len(panel_grow_shrink.Controls) > 0:
            panel_grow_shrink.RemoveControl(panel_grow_shrink.Controls[-1])
        
        while len(panel_grow_only.Controls) > 0:
            panel_grow_only.RemoveControl(panel_grow_only.Controls[-1])
        
        while len(panel_fixed.Controls) > 0:
            panel_fixed.RemoveControl(panel_fixed.Controls[-1])
        
        panel_counter[0] = 0
        update_panel_info()
    
    btn_add_panel = Button(panel_controls_panel, {
        'Text': 'Add Button',
        'Top': 35,
        'Left': 10,
        'Width': 160
    })
    btn_add_panel.Click = add_to_panels
    
    btn_clear_panels = Button(panel_controls_panel, {
        'Text': 'Clear All',
        'Top': 65,
        'Left': 10,
        'Width': 160
    })
    btn_clear_panels.Click = clear_panels
    
    update_panel_info()
    
    # =========================================================================
    # Tab 4: TabControl Demo
    # =========================================================================
    tab_tabs = TabPage(tabs, {'Text': 'TabControl Demo'})
    tabs.AddTab(tab_tabs)
    
    # Banner
    banner_tabs = Label(tab_tabs, {
        'Text': 'DYNAMIC TABCONTROL: Add and remove TabPages dynamically. Each new tab contains sample content with an AutoSize GroupBox demonstrating container behavior within tabs.',
        'Dock': DockStyle.Top,
        'Height': 50,
        'BackColor': '#2C2C2C',
        'ForeColor': '#FFFFFF',
        'Font': Font('Segoe UI', 9, FontStyle.Bold),
        'TextAlign': ContentAlignment.MiddleLeft,
        'Padding': (15, 10, 15, 10)
    })
    
    # Title
    Label(tab_tabs, {
        'Text': 'Dynamic TabControl - Add/Remove TabPages',
        'Top': 60,
        'Left': 10,
        'Font': Font('Segoe UI', 11, FontStyle.Bold),
        'AutoSize': True,
        'ForeColor': '#003D5B'
    })
    
    # Dynamic TabControl
    demo_tabcontrol = TabControl(tab_tabs, {
        'Top': 130,
        'Left': 10,
        'Width': 600,
        'Height': 350
    })
    
    # Info
    lbl_tabs_info = Label(tab_tabs, {
        'Top': 490,
        'Left': 10,
        'AutoSize': True,
        'ForeColor': '#0078D4',
        'Font': Font('Segoe UI', 9, FontStyle.Bold)
    })
    
    tab_counter = [0]
    
    def add_tabpage(sender, e):
        """Add a new TabPage to the demo TabControl."""
        tab_counter[0] += 1
        
        new_tab = TabPage(demo_tabcontrol, {
            'Text': f'Tab {tab_counter[0]}'
        })
        demo_tabcontrol.AddTab(new_tab)
        
        # Add some content to the new tab
        Label(new_tab, {
            'Text': f'Content of Tab {tab_counter[0]}',
            'Top': 20,
            'Left': 20,
            'Font': Font('Segoe UI', 10, FontStyle.Bold),
            'AutoSize': True
        })
        
        # Add a GroupBox with AutoSize in the tab
        grp = GroupBox(new_tab, {
            'Text': 'AutoSize GroupBox in Tab',
            'Top': 60,
            'Left': 20,
            'AutoSize': True,
            'AutoSizeMode': AutoSizeMode.GrowAndShrink,
            'BackColor': '#F0FFF0'
        })
        
        for i in range(3):
            CheckBox(grp, {
                'Text': f'Option {i+1}',
                'Top': 25 + (i * 25),
                'Left': 10,
                'AutoSize': True
            })
        
        update_tabs_info()
    
    def remove_tabpage(sender, e):
        """Remove the last TabPage from demo TabControl."""
        if len(demo_tabcontrol.TabPages) > 1:
            last_tab = demo_tabcontrol.TabPages[-1]
            demo_tabcontrol.RemoveTab(last_tab)
            update_tabs_info()
    
    def update_tabs_info():
        """Update TabControl information."""
        count = len(demo_tabcontrol.TabPages)
        lbl_tabs_info.Text = f'TabControl has {count} TabPages'
    
    # Control Panel
    btn_add_tab = Button(tab_tabs, {
        'Text': 'Add TabPage',
        'Top': 95,
        'Left': 10,
        'Width': 120
    })
    btn_add_tab.Click = add_tabpage
    
    btn_remove_tab = Button(tab_tabs, {
        'Text': 'Remove Last Tab',
        'Top': 95,
        'Left': 140,
        'Width': 130
    })
    btn_remove_tab.Click = remove_tabpage
    
    # Add initial tab
    add_tabpage(None, None)
    
    # =========================================================================
    # Show the form
    # =========================================================================
    form.ShowDialog()


if __name__ == '__main__':
    main()

