"""
StatusBar Example

This example demonstrates various uses of the StatusBar control:

- Simple text status
- Multi-panel status bar
- Panel types: Text, AutoSize, Spring
- Icons in panels
- Dynamic updates
- Progress indication
- Clock/Timer display
- Click events on panels
- Tooltips on panels
"""

import time
import threading
from winformpy import (
    Form, Panel, Button, Label, TextBox, GroupBox, ProgressBar,
    StatusBar, StatusBarPanel,
    DockStyle, AnchorStyles, Font, FontStyle,
    MessageBox, MessageBoxButtons, MessageBoxIcon, DialogResult
)


def main():
    # =========================================================================
    # Create main form
    # =========================================================================
    form = Form({
        'Text': 'StatusBar Examples',
        'Width': 920,
        'Height': 650,
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
        'Text': 'StatusBar Demo - Multiple Use Cases',
        'Left': 20,
        'Top': 12,
        'AutoSize': True,
        'Font': Font('Segoe UI', 16, FontStyle.Bold),
        'ForeColor': '#FFFFFF',
        'BackColor': '#0078D4'
    })
    
    # =========================================================================
    # StatusBar with multiple panels
    # =========================================================================
    statusbar = StatusBar(form, {
        'Dock': DockStyle.Bottom,
        'ShowPanels': True,
        'SizingGrip': True
    })
    
    # Panel 1: Status message (Spring - takes available space)
    panel_status = StatusBarPanel({
        'Text': '✅ Ready',
        'AutoSize': 'Spring',  # Takes remaining space
        'Alignment': 'Left',
        'ToolTipText': 'Application status'
    })
    
    # Panel 2: Document info
    panel_doc = StatusBarPanel({
        'Text': '📄 No document',
        'Width': 150,
        'AutoSize': 'Contents',
        'Alignment': 'Center',
        'ToolTipText': 'Current document'
    })
    
    # Panel 3: Line/Column position
    panel_position = StatusBarPanel({
        'Text': 'Ln 1, Col 1',
        'Width': 100,
        'Alignment': 'Center',
        'ToolTipText': 'Cursor position'
    })
    
    # Panel 4: Encoding
    panel_encoding = StatusBarPanel({
        'Text': 'UTF-8',
        'Width': 70,
        'Alignment': 'Center',
        'ToolTipText': 'File encoding'
    })
    
    # Panel 5: Clock
    panel_clock = StatusBarPanel({
        'Text': '🕐 00:00:00',
        'Width': 100,
        'Alignment': 'Right',
        'ToolTipText': 'Current time'
    })
    
    # Add panels to statusbar
    statusbar.Panels.Add(panel_status)
    statusbar.Panels.Add(panel_doc)
    statusbar.Panels.Add(panel_position)
    statusbar.Panels.Add(panel_encoding)
    statusbar.Panels.Add(panel_clock)
    
    # =========================================================================
    # Main content panel
    # =========================================================================
    content_panel = Panel(form, {
        'Dock': DockStyle.Fill,
        'Padding': 10
    })
    
    # =========================================================================
    # LEFT: Status Controls
    # =========================================================================
    status_group = GroupBox(content_panel, {
        'Text': 'Status Message',
        'Left': 20,
        'Top': 20,
        'Width': 430,
        'Height': 180
    })
    
    Label(status_group, {
        'Text': 'Set status message:',
        'Left': 15,
        'Top': 30,
        'AutoSize': True
    })
    
    txt_status = TextBox(status_group, {
        'Text': 'Ready',
        'Left': 15,
        'Top': 55,
        'Width': 280
    })
    
    btn_set_status = Button(status_group, {
        'Text': 'Set',
        'Left': 305,
        'Top': 53,
        'Width': 70
    })
    
    # Preset status buttons
    btn_ready = Button(status_group, {
        'Text': '✅ Ready',
        'Left': 15,
        'Top': 95,
        'Width': 90
    })
    
    btn_loading = Button(status_group, {
        'Text': '⏳ Loading...',
        'Left': 115,
        'Top': 95,
        'Width': 100
    })
    
    btn_error = Button(status_group, {
        'Text': '❌ Error',
        'Left': 225,
        'Top': 95,
        'Width': 80
    })
    
    btn_success = Button(status_group, {
        'Text': '✓ Success',
        'Left': 315,
        'Top': 95,
        'Width': 80
    })
    
    btn_warning = Button(status_group, {
        'Text': '⚠️ Warning',
        'Left': 15,
        'Top': 135,
        'Width': 100
    })
    
    btn_info = Button(status_group, {
        'Text': 'ℹ️ Info',
        'Left': 125,
        'Top': 135,
        'Width': 80
    })
    
    btn_saving = Button(status_group, {
        'Text': '💾 Saving...',
        'Left': 215,
        'Top': 135,
        'Width': 90
    })
    
    btn_connected = Button(status_group, {
        'Text': '🔗 Connected',
        'Left': 315,
        'Top': 135,
        'Width': 100
    })
    
    # =========================================================================
    # RIGHT: Document Simulation
    # =========================================================================
    doc_group = GroupBox(content_panel, {
        'Text': 'Document Simulation',
        'Left': 460,
        'Top': 20,
        'Width': 410,
        'Height': 210
    })
    
    Label(doc_group, {
        'Text': 'Document name:',
        'Left': 15,
        'Top': 30,
        'AutoSize': True
    })
    
    txt_docname = TextBox(doc_group, {
        'Text': 'Untitled.txt',
        'Left': 15,
        'Top': 55,
        'Width': 200
    })
    
    btn_open_doc = Button(doc_group, {
        'Text': 'Open',
        'Left': 225,
        'Top': 53,
        'Width': 70
    })
    
    btn_close_doc = Button(doc_group, {
        'Text': 'Close',
        'Left': 305,
        'Top': 53,
        'Width': 70
    })
    
    Label(doc_group, {
        'Text': 'Simulate cursor position:',
        'Left': 15,
        'Top': 95,
        'AutoSize': True
    })
    
    txt_line = TextBox(doc_group, {
        'Text': '1',
        'Left': 15,
        'Top': 120,
        'Width': 60
    })
    
    Label(doc_group, {
        'Text': 'Line',
        'Left': 80,
        'Top': 123,
        'AutoSize': True
    })
    
    txt_col = TextBox(doc_group, {
        'Text': '1',
        'Left': 120,
        'Top': 120,
        'Width': 60
    })
    
    Label(doc_group, {
        'Text': 'Column',
        'Left': 185,
        'Top': 123,
        'AutoSize': True
    })
    
    btn_update_pos = Button(doc_group, {
        'Text': 'Update Position',
        'Left': 260,
        'Top': 118,
        'Width': 120
    })
    
    # Encoding buttons
    btn_utf8 = Button(doc_group, {
        'Text': 'UTF-8',
        'Left': 15,
        'Top': 160,
        'Width': 70
    })
    
    btn_ascii = Button(doc_group, {
        'Text': 'ASCII',
        'Left': 95,
        'Top': 160,
        'Width': 70
    })
    
    btn_utf16 = Button(doc_group, {
        'Text': 'UTF-16',
        'Left': 175,
        'Top': 160,
        'Width': 70
    })
    
    btn_latin1 = Button(doc_group, {
        'Text': 'Latin-1',
        'Left': 255,
        'Top': 160,
        'Width': 70
    })
    
    # =========================================================================
    # BOTTOM LEFT: Progress Simulation
    # =========================================================================
    progress_group = GroupBox(content_panel, {
        'Text': 'Progress Simulation',
        'Left': 20,
        'Top': 220,
        'Width': 430,
        'Height': 150
    })
    
    btn_start_progress = Button(progress_group, {
        'Text': 'Start Task (5s)',
        'Left': 15,
        'Top': 30,
        'Width': 120
    })
    
    btn_quick_task = Button(progress_group, {
        'Text': 'Quick Task (1s)',
        'Left': 145,
        'Top': 30,
        'Width': 120
    })
    
    btn_simulate_download = Button(progress_group, {
        'Text': 'Simulate Download',
        'Left': 275,
        'Top': 30,
        'Width': 130
    })
    
    progress_label = Label(progress_group, {
        'Text': 'Progress: 0%',
        'Left': 15,
        'Top': 75,
        'Width': 370,
        'AutoSize': False
    })
    
    progress_bar = ProgressBar(progress_group, {
        'Left': 15,
        'Top': 100,
        'Width': 370,
        'Height': 25,
        'Minimum': 0,
        'Maximum': 100,
        'Value': 0
    })
    
    # =========================================================================
    # BOTTOM RIGHT: StatusBar Options
    # =========================================================================
    options_group = GroupBox(content_panel, {
        'Text': 'StatusBar Options',
        'Left': 460,
        'Top': 250,
        'Width': 410,
        'Height': 150
    })
    
    btn_show_panels = Button(options_group, {
        'Text': 'Show Panels',
        'Left': 15,
        'Top': 30,
        'Width': 110
    })
    
    btn_simple_mode = Button(options_group, {
        'Text': 'Simple Mode',
        'Left': 135,
        'Top': 30,
        'Width': 110
    })
    
    btn_toggle_grip = Button(options_group, {
        'Text': 'Toggle Grip',
        'Left': 255,
        'Top': 30,
        'Width': 110
    })
    
    btn_add_panel = Button(options_group, {
        'Text': 'Add Panel',
        'Left': 15,
        'Top': 70,
        'Width': 110
    })
    
    btn_remove_panel = Button(options_group, {
        'Text': 'Remove Last',
        'Left': 135,
        'Top': 70,
        'Width': 110
    })
    
    btn_clear_panels = Button(options_group, {
        'Text': 'Clear All',
        'Left': 255,
        'Top': 70,
        'Width': 110
    })
    
    panel_counter = [0]  # Counter for added panels
    
    info_label = Label(options_group, {
        'Text': f'Panels: {len(statusbar.Panels)} | ShowPanels: {statusbar.ShowPanels}',
        'Left': 15,
        'Top': 115,
        'Width': 370,
        'AutoSize': False
    })
    
    # =========================================================================
    # Clock update (using after)
    # =========================================================================
    clock_running = [True]
    
    def update_clock():
        if clock_running[0]:
            current_time = time.strftime('%H:%M:%S')
            panel_clock.Text = f'🕐 {current_time}'
            form._root.after(1000, update_clock)
    
    # Start clock after form is shown
    form._root.after(100, update_clock)
    
    # =========================================================================
    # Event Handlers
    # =========================================================================
    
    def update_info():
        info_label.Text = f'Panels: {len(statusbar.Panels)} | ShowPanels: {statusbar.ShowPanels}'
    
    def on_set_status(sender, e):
        panel_status.Text = txt_status.Text
    
    def on_ready(sender, e):
        panel_status.Text = '✅ Ready'
        txt_status.Text = 'Ready'
    
    def on_loading(sender, e):
        panel_status.Text = '⏳ Loading...'
        txt_status.Text = 'Loading...'
    
    def on_error(sender, e):
        panel_status.Text = '❌ Error occurred'
        txt_status.Text = 'Error occurred'
    
    def on_success(sender, e):
        panel_status.Text = '✓ Operation completed successfully'
        txt_status.Text = 'Operation completed successfully'
    
    def on_warning(sender, e):
        panel_status.Text = '⚠️ Warning: Check settings'
        txt_status.Text = 'Warning: Check settings'
    
    def on_info(sender, e):
        panel_status.Text = 'ℹ️ Information message'
        txt_status.Text = 'Information message'
    
    def on_saving(sender, e):
        panel_status.Text = '💾 Saving document...'
        txt_status.Text = 'Saving document...'
    
    def on_connected(sender, e):
        panel_status.Text = '🔗 Connected to server'
        txt_status.Text = 'Connected to server'
    
    def on_open_doc(sender, e):
        name = txt_docname.Text.strip()
        if name:
            panel_doc.Text = f'📄 {name}'
            panel_status.Text = f'✅ Opened: {name}'
        else:
            MessageBox.Show('Enter a document name', 'Error', 
                          MessageBoxButtons.OK, MessageBoxIcon.Warning)
    
    def on_close_doc(sender, e):
        panel_doc.Text = '📄 No document'
        panel_position.Text = 'Ln 1, Col 1'
        panel_status.Text = '✅ Document closed'
    
    def on_update_pos(sender, e):
        try:
            line = int(txt_line.Text)
            col = int(txt_col.Text)
            panel_position.Text = f'Ln {line}, Col {col}'
        except ValueError:
            MessageBox.Show('Enter valid numbers', 'Error',
                          MessageBoxButtons.OK, MessageBoxIcon.Warning)
    
    def on_utf8(sender, e):
        panel_encoding.Text = 'UTF-8'
    
    def on_ascii(sender, e):
        panel_encoding.Text = 'ASCII'
    
    def on_utf16(sender, e):
        panel_encoding.Text = 'UTF-16'
    
    def on_latin1(sender, e):
        panel_encoding.Text = 'Latin-1'
    
    def run_progress(duration, message):
        """Run a progress simulation"""
        steps = 20
        delay = duration / steps
        
        for i in range(steps + 1):
            progress = int((i / steps) * 100)
            progress_bar.Value = progress
            progress_label.Text = f'{message}: {progress}%'
            panel_status.Text = f'⏳ {message}: {progress}%'
            form._root.update()
            time.sleep(delay)
        
        panel_status.Text = f'✅ {message} completed!'
        progress_label.Text = 'Progress: Complete!'
    
    def on_start_progress(sender, e):
        run_progress(5, 'Processing')
    
    def on_quick_task(sender, e):
        run_progress(1, 'Quick task')
    
    def on_simulate_download(sender, e):
        run_progress(3, 'Downloading file')
    
    def on_show_panels(sender, e):
        statusbar.ShowPanels = True
        update_info()
    
    def on_simple_mode(sender, e):
        statusbar.ShowPanels = False
        statusbar.Text = 'Simple mode - No panels visible'
        update_info()
    
    def on_toggle_grip(sender, e):
        # Toggle sizing grip visibility would require recreating the widget
        MessageBox.Show(
            'SizingGrip is typically set at design time.\n'
            'Current value: ' + str(statusbar.SizingGrip),
            'Sizing Grip',
            MessageBoxButtons.OK,
            MessageBoxIcon.Information
        )
    
    def on_add_panel(sender, e):
        panel_counter[0] += 1
        new_panel = StatusBarPanel({
            'Text': f'Panel #{panel_counter[0]}',
            'Width': 100,
            'Alignment': 'Center'
        })
        statusbar.Panels.Add(new_panel)
        update_info()
        panel_status.Text = f'✅ Added panel #{panel_counter[0]}'
    
    def on_remove_panel(sender, e):
        if len(statusbar.Panels) > 1:
            last_panel = statusbar.Panels[-1]
            statusbar.Panels.Remove(last_panel)
            update_info()
            panel_status.Text = '✅ Removed last panel'
        else:
            MessageBox.Show('Cannot remove the last panel', 'Info',
                          MessageBoxButtons.OK, MessageBoxIcon.Information)
    
    def on_clear_panels(sender, e):
        result = MessageBox.Show(
            'Clear all panels? This will remove all status information.',
            'Confirm',
            MessageBoxButtons.YesNo,
            MessageBoxIcon.Question
        )
        if result == DialogResult.Yes:
            statusbar.Panels.Clear()
            update_info()
    
    def on_panel_click(sender, panel):
        """Handle panel click events"""
        MessageBox.Show(
            f'You clicked on: {panel.Text}',
            'Panel Click',
            MessageBoxButtons.OK,
            MessageBoxIcon.Information
        )
    
    # =========================================================================
    # Bind Events
    # =========================================================================
    btn_set_status.Click = on_set_status
    btn_ready.Click = on_ready
    btn_loading.Click = on_loading
    btn_error.Click = on_error
    btn_success.Click = on_success
    btn_warning.Click = on_warning
    btn_info.Click = on_info
    btn_saving.Click = on_saving
    btn_connected.Click = on_connected
    
    btn_open_doc.Click = on_open_doc
    btn_close_doc.Click = on_close_doc
    btn_update_pos.Click = on_update_pos
    
    btn_utf8.Click = on_utf8
    btn_ascii.Click = on_ascii
    btn_utf16.Click = on_utf16
    btn_latin1.Click = on_latin1
    
    btn_start_progress.Click = on_start_progress
    btn_quick_task.Click = on_quick_task
    btn_simulate_download.Click = on_simulate_download
    
    btn_show_panels.Click = on_show_panels
    btn_simple_mode.Click = on_simple_mode
    btn_toggle_grip.Click = on_toggle_grip
    btn_add_panel.Click = on_add_panel
    btn_remove_panel.Click = on_remove_panel
    btn_clear_panels.Click = on_clear_panels
    
    statusbar.PanelClick = on_panel_click
    
    # =========================================================================
    # Form close handler
    # =========================================================================
    def on_form_closing(sender, e):
        clock_running[0] = False
    
    form.FormClosing = on_form_closing
    
    # =========================================================================
    # Show the form
    # =========================================================================
    form.ShowDialog()


if __name__ == '__main__':
    main()
