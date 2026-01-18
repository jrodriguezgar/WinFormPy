"""
AutoSize Comprehensive Demo
============================
Demonstrates AutoSize behavior with various controls and containers:
- Basic controls (Label, Button, CheckBox, TextBox)
- Container controls (GroupBox, Panel)
- Layout panels (FlowLayoutPanel, TableLayoutPanel)
- TabControl with dynamic TabPages
"""
import sys
import os

# Add the parent directory to sys.path to allow importing winformpy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from winformpy.winformpy import (
    Form, Label, Button, CheckBox, RadioButton, TextBox, GroupBox, ComboBox,
    Panel, TabControl, TabPage,
    DockStyle, AnchorStyles, AutoSizeMode, Color, Font, FontStyle, MessageBox,
    ContentAlignment
)

class AutoSizeDemoForm(Form):
    def __init__(self):
        super().__init__()
        self.Text = "WinFormPy AutoSize Comprehensive Demo"
        self.Width = 1000
        self.Height = 750
        self.StartPosition = "CenterScreen"

        # Main TabControl
        self.tabs = TabControl(self)
        self.tabs.Dock = DockStyle.Fill
        self.tabs.Alignment = "Left"
        
        # --- Tab 1: Basic Controls ---
        self.tab_basic = TabPage(self.tabs)
        self.tab_basic.Text = "Basic Controls"
        self.tabs.AddTab(self.tab_basic)
        self._init_basic_tab()

        # --- Tab 2: GroupBox Demo ---
        self.tab_groupbox = TabPage(self.tabs)
        self.tab_groupbox.Text = "GroupBox AutoSize"
        self.tabs.AddTab(self.tab_groupbox)
        self._init_groupbox_tab()

        # --- Tab 3: Panel Demo ---
        self.tab_panel = TabPage(self.tabs)
        self.tab_panel.Text = "Panel AutoSize"
        self.tabs.AddTab(self.tab_panel)
        self._init_panel_tab()

        # --- Tab 5: TabControl Dynamic ---
        self.tab_tabs = TabPage(self.tabs)
        self.tab_tabs.Text = "TabControl Demo"
        self.tabs.AddTab(self.tab_tabs)
        self._init_tabs_tab()

    def _init_basic_tab(self):
        """Initialize the Basic Controls tab."""
        # 1. Explanation banner (Top)
        lbl_banner = Label(self.tab_basic)
        lbl_banner.Text = "BASIC CONTROLS AUTOSIZE: Toggle AutoSize on/off and change text to see how Label, Button, CheckBox, and TextBox adjust their size automatically. Basic controls always use GrowAndShrink mode."
        lbl_banner.Dock = DockStyle.Top
        lbl_banner.Height = 50
        lbl_banner.BackColor = Color.Black
        lbl_banner.ForeColor = Color.White
        lbl_banner.Font = Font("Segoe UI", 9, FontStyle.Bold)
        lbl_banner.TextAlign = ContentAlignment.MiddleLeft
        lbl_banner.Padding = (15, 10, 15, 10)

        # 2. Control Panel (Left)
        panel_controls = Panel(self.tab_basic)
        panel_controls.Dock = DockStyle.Left
        panel_controls.Width = 250
        panel_controls.BackColor = Color.WhiteSmoke
        panel_controls.AutoScroll = True

        # 3. Demo Area (Right - Fill)
        self.panel_demo = Panel(self.tab_basic)
        self.panel_demo.Dock = DockStyle.Fill
        self.panel_demo.BackColor = Color.White
        
        lbl_instr = Label(panel_controls)
        lbl_instr.Text = "Control Properties:"
        lbl_instr.Top = 10
        lbl_instr.Left = 10
        lbl_instr.Font = Font("Segoe UI", 10, FontStyle.Bold)
        lbl_instr.AutoSize = True

        # AutoSize Toggle - Create FIRST to define initial state
        self.chk_autosize = CheckBox(panel_controls)
        self.chk_autosize.Text = "AutoSize Enabled"
        self.chk_autosize.Top = 40
        self.chk_autosize.Left = 10
        self.chk_autosize.Checked = False  # Start with AutoSize disabled
        self.chk_autosize.AutoSize = True

        # Text Input
        Label(panel_controls, props={"Text": "Text Content:", "Top": 70, "Left": 10, "AutoSize": True})
        self.txt_content = TextBox(panel_controls)
        self.txt_content.Top = 90
        self.txt_content.Left = 10
        self.txt_content.Width = 220
        self.txt_content.Text = "AutoSize Me!"

        # Info note
        lbl_note = Label(panel_controls)
        lbl_note.Text = "Note: Basic controls always\nuse GrowAndShrink behavior\nwhen AutoSize is enabled."
        lbl_note.Top = 120
        lbl_note.Left = 10
        lbl_note.AutoSize = True
        lbl_note.ForeColor = Color.Gray
        lbl_note.Font = Font("Segoe UI", 8, FontStyle.Italic)

        # Target Selection
        Label(panel_controls, props={"Text": "Select Target:", "Top": 190, "Left": 10, "AutoSize": True})
        
        self.rb_label = RadioButton(panel_controls)
        self.rb_label.Text = "Label"
        self.rb_label.Top = 210
        self.rb_label.Left = 10
        self.rb_label.Checked = True
        self.rb_label.AutoSize = True

        self.rb_button = RadioButton(panel_controls)
        self.rb_button.Text = "Button"
        self.rb_button.Top = 235
        self.rb_button.Left = 10
        self.rb_button.AutoSize = True

        self.rb_checkbox = RadioButton(panel_controls)
        self.rb_checkbox.Text = "CheckBox"
        self.rb_checkbox.Top = 260
        self.rb_checkbox.Left = 10
        self.rb_checkbox.AutoSize = True
        
        self.rb_textbox = RadioButton(panel_controls)
        self.rb_textbox.Text = "TextBox (Multiline)"
        self.rb_textbox.Top = 285
        self.rb_textbox.Left = 10
        self.rb_textbox.AutoSize = True

        # Info Label
        self.lbl_info = Label(panel_controls)
        self.lbl_info.Text = "Size: 0, 0"
        self.lbl_info.Top = 320
        self.lbl_info.Left = 10
        self.lbl_info.AutoSize = True
        self.lbl_info.ForeColor = Color.Blue
        
        # Apply Changes Button (at the end)
        btn_apply = Button(panel_controls)
        btn_apply.Text = "Apply Changes"
        btn_apply.Top = 360
        btn_apply.Left = 10
        btn_apply.Width = 220
        btn_apply.Click = self._on_apply_changes

        # Create Demo Controls - Use checkbox state for initial AutoSize value
        autosize_initial = self.chk_autosize.Checked
        
        self.demo_label = Label(self.panel_demo)
        self.demo_label.Text = "AutoSize Me!"
        self.demo_label.Left = 50
        self.demo_label.Top = 50
        self.demo_label.BackColor = Color.LightYellow
        self.demo_label.BorderStyle = "solid" # Visual aid
        self.demo_label.AutoSize = autosize_initial
        if not autosize_initial:
            self.demo_label.Width = 200
            self.demo_label.Height = 30

        self.demo_button = Button(self.panel_demo)
        self.demo_button.Text = "AutoSize Me!"
        self.demo_button.Left = 50
        self.demo_button.Top = 50
        self.demo_button.AutoSize = autosize_initial
        self.demo_button.Visible = False
        if not autosize_initial:
            self.demo_button.Width = 200
            self.demo_button.Height = 30

        self.demo_checkbox = CheckBox(self.panel_demo)
        self.demo_checkbox.Text = "AutoSize Me!"
        self.demo_checkbox.Left = 50
        self.demo_checkbox.Top = 50
        self.demo_checkbox.AutoSize = autosize_initial
        self.demo_checkbox.Visible = False
        if not autosize_initial:
            self.demo_checkbox.Width = 200
            self.demo_checkbox.Height = 30
        
        self.demo_textbox = TextBox(self.panel_demo)
        self.demo_textbox.Text = "AutoSize Me!"
        self.demo_textbox.Left = 50
        self.demo_textbox.Top = 50
        self.demo_textbox.Multiline = True
        self.demo_textbox.AutoSize = autosize_initial
        self.demo_textbox.Visible = False
        self.demo_textbox.BackColor = Color.AliceBlue
        if not autosize_initial:
            self.demo_textbox.Width = 200
            self.demo_textbox.Height = 80

        self.current_control = self.demo_label
        self._update_info()

    def _init_groupbox_tab(self):
        """Initialize the GroupBox AutoSize tab."""
        # Explanation banner
        lbl_banner = Label(self.tab_groupbox)
        lbl_banner.Text = "GROUPBOX AUTOSIZE MODES: Add/remove controls dynamically to see AutoSize behavior. GrowOnly mode only grows (never shrinks). GrowAndShrink mode adjusts to fit content (grows and shrinks)."
        lbl_banner.Dock = DockStyle.Top
        lbl_banner.Height = 50
        lbl_banner.BackColor = Color.Black
        lbl_banner.ForeColor = Color.White
        lbl_banner.Font = Font("Segoe UI", 9, FontStyle.Bold)
        lbl_banner.TextAlign = ContentAlignment.MiddleLeft
        lbl_banner.Padding = (15, 10, 15, 10)
        
        # Title
        lbl_title = Label(self.tab_groupbox)
        lbl_title.Text = "GroupBox AutoSize Demo - Add/Remove controls dynamically"
        lbl_title.Top = 60
        lbl_title.Left = 10
        lbl_title.Font = Font("Segoe UI", 11, FontStyle.Bold)
        lbl_title.AutoSize = True
        lbl_title.ForeColor = Color.DarkBlue

        # Control Panel
        panel_controls = Panel(self.tab_groupbox)
        panel_controls.Top = 100
        panel_controls.Left = 10
        panel_controls.Width = 200
        panel_controls.Height = 200
        panel_controls.BackColor = Color.WhiteSmoke
        panel_controls.BorderStyle = "solid"

        Label(panel_controls, props={
            "Text": "Controls:", 
            "Top": 10, 
            "Left": 10, 
            "AutoSize": True,
            "Font": ("Segoe UI", 9, "bold")
        })

        btn_add_button = Button(panel_controls)
        btn_add_button.Text = "Add Button"
        btn_add_button.Top = 35
        btn_add_button.Left = 10
        btn_add_button.Width = 180
        btn_add_button.Click = lambda s, e: self._add_to_groupbox("button")

        btn_add_label = Button(panel_controls)
        btn_add_label.Text = "Add Label"
        btn_add_label.Top = 65
        btn_add_label.Left = 10
        btn_add_label.Width = 180
        btn_add_label.Click = lambda s, e: self._add_to_groupbox("label")

        btn_add_checkbox = Button(panel_controls)
        btn_add_checkbox.Text = "Add CheckBox"
        btn_add_checkbox.Top = 95
        btn_add_checkbox.Left = 10
        btn_add_checkbox.Width = 180
        btn_add_checkbox.Click = lambda s, e: self._add_to_groupbox("checkbox")

        btn_remove = Button(panel_controls)
        btn_remove.Text = "Remove Last"
        btn_remove.Top = 125
        btn_remove.Left = 10
        btn_remove.Width = 180
        btn_remove.Click = lambda s, e: self._remove_from_groupbox()

        btn_clear = Button(panel_controls)
        btn_clear.Text = "Clear All"
        btn_clear.Top = 155
        btn_clear.Left = 10
        btn_clear.Width = 180
        btn_clear.Click = lambda s, e: self._clear_groupbox()

        # GroupBox Demo Area
        self.grp_auto = GroupBox(self.tab_groupbox)
        self.grp_auto.Text = "AutoSize GroupBox (GrowAndShrink)"
        self.grp_auto.Left = 230
        self.grp_auto.Top = 100
        self.grp_auto.AutoSize = True
        self.grp_auto.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.grp_auto.BackColor = Color.LightYellow
        self.grp_auto.Padding = (10, 25, 10, 10)
        
        # Add initial control
        lbl_initial = Label(self.grp_auto)
        lbl_initial.Text = "Initial content in GroupBox"
        lbl_initial.Top = 30
        lbl_initial.Left = 10
        lbl_initial.AutoSize = True

        # Info Label
        self.lbl_groupbox_info = Label(self.tab_groupbox)
        self.lbl_groupbox_info.Text = "GroupBox Size: 0 x 0"
        self.lbl_groupbox_info.Top = 320
        self.lbl_groupbox_info.Left = 10
        self.lbl_groupbox_info.AutoSize = True
        self.lbl_groupbox_info.ForeColor = Color.Blue
        self.lbl_groupbox_info.Font = Font("Segoe UI", 9, FontStyle.Bold)

        # Fixed Size GroupBox for comparison
        self.grp_fixed = GroupBox(self.tab_groupbox)
        self.grp_fixed.Text = "Fixed Size GroupBox (AutoSize=False)"
        self.grp_fixed.Left = 550
        self.grp_fixed.Top = 100
        self.grp_fixed.Width = 250
        self.grp_fixed.Height = 150
        self.grp_fixed.AutoSize = False
        self.grp_fixed.BackColor = Color.LightCyan
        self.grp_fixed.Padding = (10, 25, 10, 10)

        lbl_fixed = Label(self.grp_fixed)
        lbl_fixed.Text = "This GroupBox has fixed size\nand won't grow with content"
        lbl_fixed.Top = 25
        lbl_fixed.Left = 10
        lbl_fixed.AutoSize = True

        self.grp_auto_counter = 0
        self._update_groupbox_info()

    def _add_to_groupbox(self, control_type):
        """Add a control to both GroupBoxes for comparison."""
        self.grp_auto_counter += 1
        
        # Add to both GroupBoxes to show the difference
        for grp in [self.grp_auto, self.grp_fixed]:
            # Calculate position based on number of controls already in this GroupBox
            num_controls = len(grp.Controls)
            y_pos = 30 + (num_controls * 30)
            
            # Create control based on type
            if control_type == "button":
                ctrl = Button(grp, props={
                    "Text": f"Button {self.grp_auto_counter}",
                    "AutoSize": True
                })
            elif control_type == "label":
                ctrl = Label(grp, props={
                    "Text": f"Label {self.grp_auto_counter} - Dynamic",
                    "AutoSize": True
                })
            elif control_type == "checkbox":
                ctrl = CheckBox(grp, props={
                    "Text": f"CheckBox {self.grp_auto_counter}",
                    "AutoSize": True
                })
            
            # Set position after auto-registration
            ctrl.Top = y_pos
            ctrl.Left = 10
        
        self._update_groupbox_info()

    def _remove_from_groupbox(self):
        """Remove last control from both GroupBoxes."""
        # Remove from both GroupBoxes
        for grp in [self.grp_auto, self.grp_fixed]:
            if len(grp.Controls) > 1:  # Keep at least one
                last_control = grp.Controls[-1]
                grp.RemoveControl(last_control)
        self._update_groupbox_info()

    def _clear_groupbox(self):
        """Clear all controls from both GroupBoxes."""
        # Remove all controls from both GroupBoxes
        for grp in [self.grp_auto, self.grp_fixed]:
            while len(grp.Controls) > 0:
                grp.RemoveControl(grp.Controls[-1])
            
            # Add back initial control
            lbl = Label(grp)
            lbl.Text = "Initial content in GroupBox"
            lbl.Top = 30
            lbl.Left = 10
            lbl.AutoSize = True
        
        self.grp_auto_counter = 0
        self._update_groupbox_info()

    def _update_groupbox_info(self):
        """Update GroupBox size information."""
        self.grp_auto.Invalidate()
        self.grp_fixed.Invalidate()
        
        w_auto = self.grp_auto.Width
        h_auto = self.grp_auto.Height
        count_auto = len(self.grp_auto.Controls)
        
        w_fixed = self.grp_fixed.Width
        h_fixed = self.grp_fixed.Height
        count_fixed = len(self.grp_fixed.Controls)
        
        self.lbl_groupbox_info.Text = (
            f"AutoSize: {w_auto}x{h_auto} ({count_auto} controls) | "
            f"Fixed: {w_fixed}x{h_fixed} ({count_fixed} controls)"
        )

    def _init_panel_tab(self):
        """Initialize the Panel AutoSize tab."""
        # Explanation banner
        lbl_banner = Label(self.tab_panel)
        lbl_banner.Text = "PANEL AUTOSIZE COMPARISON: Compare three panels with different AutoSize settings. GrowAndShrink adjusts to content size. GrowOnly grows but never shrinks. Fixed Size has AutoSize disabled."
        lbl_banner.Dock = DockStyle.Top
        lbl_banner.Height = 50
        lbl_banner.BackColor = Color.Black
        lbl_banner.ForeColor = Color.White
        lbl_banner.Font = Font("Segoe UI", 9, FontStyle.Bold)
        lbl_banner.TextAlign = ContentAlignment.MiddleLeft
        lbl_banner.Padding = (15, 10, 15, 10)
        
        # Title
        lbl_title = Label(self.tab_panel)
        lbl_title.Text = "Panel AutoSize Demo - Compare AutoSize modes"
        lbl_title.Top = 60
        lbl_title.Left = 10
        lbl_title.Font = Font("Segoe UI", 11, FontStyle.Bold)
        lbl_title.AutoSize = True
        lbl_title.ForeColor = Color.DarkBlue

        # Control Panel
        panel_controls = Panel(self.tab_panel)
        panel_controls.Top = 90
        panel_controls.Left = 10
        panel_controls.Width = 180
        panel_controls.Height = 150
        panel_controls.BackColor = Color.WhiteSmoke
        panel_controls.BorderStyle = "solid"

        Label(panel_controls, props={
            "Text": "Add controls:", 
            "Top": 10, 
            "Left": 10, 
            "AutoSize": True,
            "Font": ("Segoe UI", 9, "bold")
        })

        btn_add_panel = Button(panel_controls)
        btn_add_panel.Text = "Add Button"
        btn_add_panel.Top = 35
        btn_add_panel.Left = 10
        btn_add_panel.Width = 160
        btn_add_panel.Click = lambda s, e: self._add_to_panels()

        btn_clear_panels = Button(panel_controls)
        btn_clear_panels.Text = "Clear All"
        btn_clear_panels.Top = 65
        btn_clear_panels.Left = 10
        btn_clear_panels.Width = 160
        btn_clear_panels.Click = lambda s, e: self._clear_panels()

        # Panel 1: GrowAndShrink
        Label(self.tab_panel, props={
            "Text": "Panel - AutoSizeMode.GrowAndShrink", 
            "Top": 250, 
            "Left": 10, 
            "AutoSize": True,
            "Font": ("Segoe UI", 9, "bold")
        })

        self.panel_grow_shrink = Panel(self.tab_panel)
        self.panel_grow_shrink.Top = 270
        self.panel_grow_shrink.Left = 10
        self.panel_grow_shrink.AutoSize = True
        self.panel_grow_shrink.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.panel_grow_shrink.BackColor = Color.LightGreen
        self.panel_grow_shrink.BorderStyle = "solid"
        self.panel_grow_shrink.Padding = (5, 5, 5, 5)

        # Panel 2: GrowOnly
        Label(self.tab_panel, props={
            "Text": "Panel - AutoSizeMode.GrowOnly", 
            "Top": 250, 
            "Left": 250, 
            "AutoSize": True,
            "Font": ("Segoe UI", 9, "bold")
        })

        self.panel_grow_only = Panel(self.tab_panel)
        self.panel_grow_only.Top = 270
        self.panel_grow_only.Left = 250
        self.panel_grow_only.AutoSize = True
        self.panel_grow_only.AutoSizeMode = AutoSizeMode.GrowOnly
        self.panel_grow_only.BackColor = Color.LightCoral
        self.panel_grow_only.BorderStyle = "solid"
        self.panel_grow_only.Padding = (5, 5, 5, 5)

        # Panel 3: Fixed Size (no AutoSize)
        Label(self.tab_panel, props={
            "Text": "Panel - Fixed Size (AutoSize=False)", 
            "Top": 250, 
            "Left": 490, 
            "AutoSize": True,
            "Font": ("Segoe UI", 9, "bold")
        })

        self.panel_fixed = Panel(self.tab_panel)
        self.panel_fixed.Top = 270
        self.panel_fixed.Left = 490
        self.panel_fixed.Width = 200
        self.panel_fixed.Height = 100
        self.panel_fixed.AutoSize = False
        self.panel_fixed.BackColor = Color.LightBlue
        self.panel_fixed.BorderStyle = "solid"
        self.panel_fixed.Padding = (5, 5, 5, 5)

        # Info Labels
        self.lbl_panel_info1 = Label(self.tab_panel)
        self.lbl_panel_info1.Top = 370
        self.lbl_panel_info1.Left = 10
        self.lbl_panel_info1.AutoSize = True
        self.lbl_panel_info1.ForeColor = Color.DarkGreen

        self.lbl_panel_info2 = Label(self.tab_panel)
        self.lbl_panel_info2.Top = 370
        self.lbl_panel_info2.Left = 250
        self.lbl_panel_info2.AutoSize = True
        self.lbl_panel_info2.ForeColor = Color.DarkRed

        self.lbl_panel_info3 = Label(self.tab_panel)
        self.lbl_panel_info3.Top = 370
        self.lbl_panel_info3.Left = 490
        self.lbl_panel_info3.AutoSize = True
        self.lbl_panel_info3.ForeColor = Color.DarkBlue

        self.panel_counter = 0
        self._update_panel_info()

    def _add_to_panels(self):
        """Add controls to all three panels."""
        self.panel_counter += 1
        y_pos = 5 + (len(self.panel_grow_shrink.Controls) * 30)
        
        for panel in [self.panel_grow_shrink, self.panel_grow_only, self.panel_fixed]:
            btn = Button(panel)
            btn.Text = f"Btn {self.panel_counter}"
            btn.Top = y_pos
            btn.Left = 5
            btn.AutoSize = True
        
        self._update_panel_info()

    def _clear_panels(self):
        """Clear all panels."""
        # Remove controls properly using RemoveControl
        while len(self.panel_grow_shrink.Controls) > 0:
            self.panel_grow_shrink.RemoveControl(self.panel_grow_shrink.Controls[-1])
        
        while len(self.panel_grow_only.Controls) > 0:
            self.panel_grow_only.RemoveControl(self.panel_grow_only.Controls[-1])
        
        while len(self.panel_fixed.Controls) > 0:
            self.panel_fixed.RemoveControl(self.panel_fixed.Controls[-1])
        
        self.panel_counter = 0
        self._update_panel_info()

    def _update_panel_info(self):
        """Update panel size information."""
        # Force layout update before reading dimensions
        self.panel_grow_shrink.Invalidate()
        self.panel_grow_only.Invalidate()
        self.panel_fixed.Invalidate()
        
        self.lbl_panel_info1.Text = (
            f"Size: {self.panel_grow_shrink.Width}x{self.panel_grow_shrink.Height}\n"
            f"Grows and shrinks"
        )
        self.lbl_panel_info2.Text = (
            f"Size: {self.panel_grow_only.Width}x{self.panel_grow_only.Height}\n"
            f"Grows only, doesn't shrink"
        )
        self.lbl_panel_info3.Text = (
            f"Size: {self.panel_fixed.Width}x{self.panel_fixed.Height}\n"
            f"Fixed size (may clip)"
        )

    def _init_tabs_tab(self):
        """Initialize the TabControl demo tab."""
        # Explanation banner
        lbl_banner = Label(self.tab_tabs)
        lbl_banner.Text = "DYNAMIC TABCONTROL: Add and remove TabPages dynamically. Each new tab contains sample content with an AutoSize GroupBox demonstrating container behavior within tabs."
        lbl_banner.Dock = DockStyle.Top
        lbl_banner.Height = 50
        lbl_banner.BackColor = Color.Black
        lbl_banner.ForeColor = Color.White
        lbl_banner.Font = Font("Segoe UI", 9, FontStyle.Bold)
        lbl_banner.TextAlign = ContentAlignment.MiddleLeft
        lbl_banner.Padding = (15, 10, 15, 10)
        
        # Title
        lbl_title = Label(self.tab_tabs)
        lbl_title.Text = "Dynamic TabControl - Add/Remove TabPages"
        lbl_title.Top = 60
        lbl_title.Left = 10
        lbl_title.Font = Font("Segoe UI", 11, FontStyle.Bold)
        lbl_title.AutoSize = True
        lbl_title.ForeColor = Color.DarkBlue

        # Control Panel
        btn_add_tab = Button(self.tab_tabs)
        btn_add_tab.Text = "Add TabPage"
        btn_add_tab.Top = 95
        btn_add_tab.Left = 10
        btn_add_tab.Width = 120
        btn_add_tab.Click = lambda s, e: self._add_tabpage()

        btn_remove_tab = Button(self.tab_tabs)
        btn_remove_tab.Text = "Remove Last Tab"
        btn_remove_tab.Top = 95
        btn_remove_tab.Left = 140
        btn_remove_tab.Width = 130
        btn_remove_tab.Click = lambda s, e: self._remove_tabpage()

        # Dynamic TabControl
        self.demo_tabcontrol = TabControl(self.tab_tabs)
        self.demo_tabcontrol.Top = 130
        self.demo_tabcontrol.Left = 10
        self.demo_tabcontrol.Width = 600
        self.demo_tabcontrol.Height = 350

        # Info
        self.lbl_tabs_info = Label(self.tab_tabs)
        self.lbl_tabs_info.Top = 440
        self.lbl_tabs_info.Left = 10
        self.lbl_tabs_info.AutoSize = True
        self.lbl_tabs_info.ForeColor = Color.Blue
        self.lbl_tabs_info.Font = Font("Segoe UI", 9, FontStyle.Bold)

        # Add initial tab
        self.tab_counter = 0
        self._add_tabpage()

    def _add_tabpage(self):
        """Add a new TabPage to the demo TabControl."""
        self.tab_counter += 1
        
        new_tab = TabPage(self.demo_tabcontrol)
        new_tab.Text = f"Tab {self.tab_counter}"
        self.demo_tabcontrol.AddTab(new_tab)
        
        # Add some content to the new tab
        lbl = Label(new_tab)
        lbl.Text = f"Content of Tab {self.tab_counter}"
        lbl.Top = 20
        lbl.Left = 20
        lbl.Font = Font("Segoe UI", 10, FontStyle.Bold)
        lbl.AutoSize = True
        
        # Add a GroupBox with AutoSize in the tab
        grp = GroupBox(new_tab)
        grp.Text = "AutoSize GroupBox in Tab"
        grp.Top = 60
        grp.Left = 20
        grp.AutoSize = True
        grp.AutoSizeMode = AutoSizeMode.GrowAndShrink
        grp.BackColor = Color.Honeydew
        
        for i in range(3):
            chk = CheckBox(grp)
            chk.Text = f"Option {i+1}"
            chk.Top = 25 + (i * 25)
            chk.Left = 10
            chk.AutoSize = True
        
        self._update_tabs_info()

    def _remove_tabpage(self):
        """Remove the last TabPage from demo TabControl."""
        if len(self.demo_tabcontrol.TabPages) > 1:
            last_tab = self.demo_tabcontrol.TabPages[-1]
            self.demo_tabcontrol.RemoveTab(last_tab)
            self._update_tabs_info()

    def _update_tabs_info(self):
        """Update TabControl information."""
        count = len(self.demo_tabcontrol.TabPages)
        self.lbl_tabs_info.Text = f"TabControl has {count} TabPages"

    def _on_apply_changes(self, sender, e):
        """Apply text and AutoSize changes to the current control."""
        # Hide all first
        self.demo_label.Visible = False
        self.demo_button.Visible = False
        self.demo_checkbox.Visible = False
        self.demo_textbox.Visible = False

        # Determine which control is selected
        if self.rb_label.Checked:
            self.current_control = self.demo_label
        elif self.rb_button.Checked:
            self.current_control = self.demo_button
        elif self.rb_checkbox.Checked:
            self.current_control = self.demo_checkbox
        elif self.rb_textbox.Checked:
            self.current_control = self.demo_textbox
        
        # Show the selected control
        self.current_control.Visible = True
        
        # Get AutoSize state from checkbox
        autosize_enabled = self.chk_autosize.Checked
        self.current_control.AutoSize = autosize_enabled
        
        # Set fixed size if AutoSize is disabled
        if not self.current_control.AutoSize:
            if isinstance(self.current_control, TextBox):
                self.current_control.Width = 200
                self.current_control.Height = 80
            else:
                self.current_control.Width = 200
                self.current_control.Height = 30
        
        # Set the new text
        self.current_control.Text = self.txt_content.Text

        self._update_info()

    def _update_info(self):
        """Update size information display."""
        # Force layout update before reading dimensions
        self.current_control.Invalidate()
        
        w = self.current_control.Width
        h = self.current_control.Height
        self.lbl_info.Text = f"Size: {w}, {h}"

if __name__ == "__main__":
    form = AutoSizeDemoForm()
    form.Show()

