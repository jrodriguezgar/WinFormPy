"""
ListBox and CheckedListBox Example

This example demonstrates the use of ListBox and CheckedListBox controls
with various features including:

- Adding, removing, and clearing items
- Selection modes (single, multiple, extended)
- Data binding with DataSource
- CheckedListBox with checkboxes
- Events: SelectedIndexChanged, ItemCheck
- Getting selected and checked items
"""

from winformpy import (
    Form, Panel, Button, Label, TextBox, GroupBox,
    ListBox, CheckedListBox, SelectionMode,
    DockStyle, AnchorStyles, Font, FontStyle,
    MessageBox, MessageBoxButtons, MessageBoxIcon, DialogResult
)


def main():
    # =========================================================================
    # Create main form
    # =========================================================================
    form = Form({
        'Text': 'ListBox & CheckedListBox Example',
        'Width': 900,
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
        'Text': 'ListBox & CheckedListBox Demo',
        'Left': 20,
        'Top': 12,
        'AutoSize': True,
        'Font': Font('Segoe UI', 16, FontStyle.Bold),
        'ForeColor': '#FFFFFF',
        'BackColor': '#0078D4'
    })
    
    # =========================================================================
    # Main content panel
    # =========================================================================
    content_panel = Panel(form, {
        'Dock': DockStyle.Fill,
        'Padding': 10
    })
    
    # =========================================================================
    # LEFT SIDE: ListBox Section
    # =========================================================================
    listbox_group = GroupBox(content_panel, {
        'Text': 'ListBox Control',
        'Left': 20,
        'Top': 20,
        'Width': 400,
        'Height': 520,
        'Anchor': AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Bottom
    })
    
    # ListBox
    listbox = ListBox(listbox_group, {
        'Left': 15,
        'Top': 30,
        'Width': 250,
        'Height': 200,
        'SelectionMode': SelectionMode.MultiExtended,  # Ctrl+Click, Shift+Click
        'Items': [
            'Python',
            'JavaScript', 
            'TypeScript',
            'C#',
            'Java',
            'Go',
            'Rust',
            'C++',
            'Ruby',
            'Swift'
        ]
    })
    
    # Selection info label
    selection_label = Label(listbox_group, {
        'Text': 'Selected: (none)',
        'Left': 15,
        'Top': 240,
        'Width': 370,
        'Height': 40,
        'AutoSize': False
    })
    
    # TextBox for adding items
    add_textbox = TextBox(listbox_group, {
        'Left': 15,
        'Top': 290,
        'Width': 200,
        'PlaceholderText': 'Enter new item...'
    })
    
    # Buttons for ListBox operations
    btn_add = Button(listbox_group, {
        'Text': 'Add Item',
        'Left': 225,
        'Top': 288,
        'Width': 80
    })
    
    btn_remove = Button(listbox_group, {
        'Text': 'Remove Selected',
        'Left': 15,
        'Top': 330,
        'Width': 120
    })
    
    btn_clear = Button(listbox_group, {
        'Text': 'Clear All',
        'Left': 145,
        'Top': 330,
        'Width': 80
    })
    
    btn_sort = Button(listbox_group, {
        'Text': 'Sort',
        'Left': 235,
        'Top': 330,
        'Width': 70
    })
    
    # Selection mode options
    mode_label = Label(listbox_group, {
        'Text': 'Selection Mode:',
        'Left': 15,
        'Top': 375,
        'AutoSize': True
    })
    
    btn_mode_single = Button(listbox_group, {
        'Text': 'Single',
        'Left': 15,
        'Top': 400,
        'Width': 70
    })
    
    btn_mode_multi = Button(listbox_group, {
        'Text': 'Multi',
        'Left': 95,
        'Top': 400,
        'Width': 70
    })
    
    btn_mode_extended = Button(listbox_group, {
        'Text': 'Extended',
        'Left': 175,
        'Top': 400,
        'Width': 80
    })
    
    # Info section
    info_label = Label(listbox_group, {
        'Text': 'ℹ️ Extended mode: Ctrl+Click for multiple, Shift+Click for range',
        'Left': 15,
        'Top': 440,
        'Width': 370,
        'ForeColor': '#666666',
        'AutoSize': False
    })
    
    count_label = Label(listbox_group, {
        'Text': 'Total items: 10',
        'Left': 15,
        'Top': 470,
        'AutoSize': True
    })
    
    # =========================================================================
    # RIGHT SIDE: CheckedListBox Section
    # =========================================================================
    checkedlistbox_group = GroupBox(content_panel, {
        'Text': 'CheckedListBox Control',
        'Left': 440,
        'Top': 20,
        'Width': 400,
        'Height': 520,
        'Anchor': AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right | AnchorStyles.Bottom
    })
    
    # CheckedListBox
    checkedlistbox = CheckedListBox(checkedlistbox_group, {
        'Left': 15,
        'Top': 30,
        'Width': 250,
        'Height': 200,
        'CheckOnClick': True,  # Toggle check on item click
        'Items': [
            '📧 Email notifications',
            '📱 SMS notifications',
            '🔔 Push notifications',
            '📰 Newsletter subscription',
            '🎉 Event reminders',
            '📊 Weekly reports',
            '🔐 Security alerts',
            '💳 Payment confirmations'
        ]
    })
    
    # Set some items as initially checked
    checkedlistbox.SetItemChecked(0, True)  # Email notifications
    checkedlistbox.SetItemChecked(6, True)  # Security alerts
    checkedlistbox.SetItemChecked(7, True)  # Payment confirmations
    
    # Checked items info
    checked_label = Label(checkedlistbox_group, {
        'Text': 'Checked: 3 items',
        'Left': 15,
        'Top': 240,
        'Width': 370,
        'Height': 60,
        'AutoSize': False
    })
    
    # TextBox for adding items
    add_checked_textbox = TextBox(checkedlistbox_group, {
        'Left': 15,
        'Top': 310,
        'Width': 200,
        'PlaceholderText': 'Enter new option...'
    })
    
    # Buttons for CheckedListBox operations
    btn_add_checked = Button(checkedlistbox_group, {
        'Text': 'Add Option',
        'Left': 225,
        'Top': 308,
        'Width': 90
    })
    
    btn_check_all = Button(checkedlistbox_group, {
        'Text': 'Check All',
        'Left': 15,
        'Top': 350,
        'Width': 90
    })
    
    btn_uncheck_all = Button(checkedlistbox_group, {
        'Text': 'Uncheck All',
        'Left': 115,
        'Top': 350,
        'Width': 100
    })
    
    btn_invert = Button(checkedlistbox_group, {
        'Text': 'Invert',
        'Left': 225,
        'Top': 350,
        'Width': 70
    })
    
    btn_get_checked = Button(checkedlistbox_group, {
        'Text': 'Show Checked Items',
        'Left': 15,
        'Top': 395,
        'Width': 150
    })
    
    btn_clear_checked = Button(checkedlistbox_group, {
        'Text': 'Clear All',
        'Left': 175,
        'Top': 395,
        'Width': 80
    })
    
    # Statistics
    stats_label = Label(checkedlistbox_group, {
        'Text': 'Total: 8 | Checked: 3 | Unchecked: 5',
        'Left': 15,
        'Top': 440,
        'Width': 370,
        'AutoSize': False
    })
    
    # CheckOnClick option
    btn_toggle_click_check = Button(checkedlistbox_group, {
        'Text': 'Toggle CheckOnClick (ON)',
        'Left': 15,
        'Top': 470,
        'Width': 180
    })
    
    # =========================================================================
    # Helper functions
    # =========================================================================
    
    def update_count_label():
        count_label.Text = f'Total items: {listbox.Items.Count}'
    
    def update_selection_label():
        selected = listbox.SelectedItems
        if selected:
            if len(selected) > 3:
                text = f'Selected: {", ".join(str(s) for s in selected[:3])}... ({len(selected)} total)'
            else:
                text = f'Selected: {", ".join(str(s) for s in selected)}'
        else:
            text = 'Selected: (none)'
        selection_label.Text = text
    
    def update_checked_stats():
        total = len(checkedlistbox.Items)
        checked = len(checkedlistbox.CheckedItems)
        unchecked = total - checked
        stats_label.Text = f'Total: {total} | Checked: {checked} | Unchecked: {unchecked}'
        
        # Update checked label
        if checked > 0:
            items = [str(item) for item in checkedlistbox.CheckedItems]
            if len(items) > 2:
                checked_label.Text = f'Checked: {items[0]}, {items[1]}... ({checked} total)'
            else:
                checked_label.Text = f'Checked: {", ".join(items)}'
        else:
            checked_label.Text = 'Checked: (none)'
    
    # =========================================================================
    # ListBox Event Handlers
    # =========================================================================
    
    def on_listbox_selection_changed(sender, e):
        update_selection_label()
    
    def on_add_item(sender, e):
        text = add_textbox.Text.strip()
        if text:
            listbox.Items.Add(text)
            add_textbox.Text = ''
            update_count_label()
        else:
            MessageBox.Show('Please enter an item name.', 'Input Required',
                          MessageBoxButtons.OK, MessageBoxIcon.Warning)
    
    def on_remove_selected(sender, e):
        indices = list(listbox.SelectedIndices)
        if not indices:
            MessageBox.Show('Please select items to remove.', 'No Selection',
                          MessageBoxButtons.OK, MessageBoxIcon.Information)
            return
        # Remove from highest index to lowest to avoid index shifting
        for idx in sorted(indices, reverse=True):
            listbox.Items.RemoveAt(idx)
        update_count_label()
        update_selection_label()
    
    def on_clear_all(sender, e):
        if listbox.Items.Count == 0:
            return
        result = MessageBox.Show('Clear all items?', 'Confirm',
                                MessageBoxButtons.YesNo, MessageBoxIcon.Question)
        if result == DialogResult.Yes:
            listbox.Items.Clear()
            update_count_label()
            update_selection_label()
    
    def on_sort(sender, e):
        # Get items, sort, clear and re-add
        items = list(listbox.Items)
        items.sort(key=lambda x: str(x).lower())
        listbox.Items.Clear()
        for item in items:
            listbox.Items.Add(item)
        update_count_label()
    
    def on_mode_single(sender, e):
        listbox.SelectionMode = SelectionMode.One
        info_label.Text = 'ℹ️ Single mode: Only one item can be selected'
    
    def on_mode_multi(sender, e):
        listbox.SelectionMode = SelectionMode.MultiSimple
        info_label.Text = 'ℹ️ Multi mode: Click to toggle selection'
    
    def on_mode_extended(sender, e):
        listbox.SelectionMode = SelectionMode.MultiExtended
        info_label.Text = 'ℹ️ Extended mode: Ctrl+Click for multiple, Shift+Click for range'
    
    # =========================================================================
    # CheckedListBox Event Handlers
    # =========================================================================
    
    def on_item_check(item_event):
        # item_event = {'Index': i, 'NewValue': val, 'CurrentValue': val}
        update_checked_stats()
    
    def on_checked_selection_changed(sender, e):
        idx = checkedlistbox.SelectedIndex
        if idx >= 0:
            item = checkedlistbox.Items[idx]
            is_checked = checkedlistbox.GetItemChecked(idx)
            # You could update a detail view here
    
    def on_add_checked_item(sender, e):
        text = add_checked_textbox.Text.strip()
        if text:
            checkedlistbox.Items.Add(text)
            add_checked_textbox.Text = ''
            update_checked_stats()
        else:
            MessageBox.Show('Please enter an option name.', 'Input Required',
                          MessageBoxButtons.OK, MessageBoxIcon.Warning)
    
    def on_check_all(sender, e):
        for i in range(len(checkedlistbox.Items)):
            checkedlistbox.SetItemChecked(i, True)
        update_checked_stats()
    
    def on_uncheck_all(sender, e):
        for i in range(len(checkedlistbox.Items)):
            checkedlistbox.SetItemChecked(i, False)
        update_checked_stats()
    
    def on_invert_checks(sender, e):
        for i in range(len(checkedlistbox.Items)):
            current = checkedlistbox.GetItemChecked(i)
            checkedlistbox.SetItemChecked(i, not current)
        update_checked_stats()
    
    def on_get_checked(sender, e):
        checked_items = list(checkedlistbox.CheckedItems)
        if checked_items:
            msg = 'Checked items:\n\n' + '\n'.join(f'• {item}' for item in checked_items)
        else:
            msg = 'No items are checked.'
        MessageBox.Show(msg, 'Checked Items', MessageBoxButtons.OK, MessageBoxIcon.Information)
    
    def on_clear_checked_list(sender, e):
        if len(checkedlistbox.Items) == 0:
            return
        result = MessageBox.Show('Clear all options?', 'Confirm',
                                MessageBoxButtons.YesNo, MessageBoxIcon.Question)
        if result == DialogResult.Yes:
            checkedlistbox.Items.Clear()
            update_checked_stats()
    
    def on_toggle_click_check(sender, e):
        checkedlistbox.CheckOnClick = not checkedlistbox.CheckOnClick
        state = 'ON' if checkedlistbox.CheckOnClick else 'OFF'
        btn_toggle_click_check.Text = f'Toggle CheckOnClick ({state})'
    
    # =========================================================================
    # Bind Events
    # =========================================================================
    
    # ListBox events
    listbox.SelectedIndexChanged = on_listbox_selection_changed
    btn_add.Click = on_add_item
    btn_remove.Click = on_remove_selected
    btn_clear.Click = on_clear_all
    btn_sort.Click = on_sort
    btn_mode_single.Click = on_mode_single
    btn_mode_multi.Click = on_mode_multi
    btn_mode_extended.Click = on_mode_extended
    
    # CheckedListBox events
    checkedlistbox.ItemCheck = on_item_check
    checkedlistbox.SelectedIndexChanged = on_checked_selection_changed
    btn_add_checked.Click = on_add_checked_item
    btn_check_all.Click = on_check_all
    btn_uncheck_all.Click = on_uncheck_all
    btn_invert.Click = on_invert_checks
    btn_get_checked.Click = on_get_checked
    btn_clear_checked.Click = on_clear_checked_list
    btn_toggle_click_check.Click = on_toggle_click_check
    
    # Initialize stats
    update_checked_stats()
    
    # =========================================================================
    # Show the form
    # =========================================================================
    form.ShowDialog()


if __name__ == '__main__':
    main()
