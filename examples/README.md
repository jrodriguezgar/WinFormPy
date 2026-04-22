# WinFormPy Examples

This directory contains standalone examples demonstrating various features of the library.

## Getting Started
Run any example using `uv run` or standard `python`:
```bash
uv run examples/basic_controls_example.py
```

## Catalog

### Core functionality
- `basic_controls_example.py`: Button, Label, TextBox.
- `more_controls_example.py`: LinkLabel, DomainUpDown, NumericUpDown, RichTextBox.
- `dotnet2_controls_example.py`: MenuStrip, ContextMenuStrip, ToolStrip, StatusStrip (.NET 2.0 replacements).
- `contextmenu_example.py`: ContextMenuStrip with submenus, separators, checked items, and dynamic updates.
- `dialogs_example.py`: ColorDialog, FontDialog, OpenFileDialog, SaveFileDialog, PrintDialog, MessageBox, InputBox.
- `tooltip_example.py`: ToolTip on Button, Label, TextBox, CheckBox with dynamic updates.

### Layout
- `layouts_example.py`: FlowLayoutPanel and TableLayoutPanel.
- `layout_manager_example.py`: LayoutManager with vertical, horizontal, flow, and wrap distributions.
- `stackpane_itemscontrol_example.py`: StackPane and ItemsControl containers.
- `dock_anchor_example.py`: Responsive layouts using Dock/Anchor.
- `autosize_example.py`: Dynamic sizing behaviors.
- `scrollbars_example.py`: HScrollBar and VScrollBar with RGB color mixer and custom ranges.
- `splitcontainer_example.py`: SplitContainer with orientation, collapse/expand, lock, and resize.
- `hierarchical_visibility_example.py`: Child control visibility depending on parent container hierarchy.

### Data controls
- `datagridview_example.py`: Tabular data management.
- `data_grid_crud_example.py`: DataGrid CRUD operations with pagination, sorting, search, and RecordFormPanel.
- `master_detail_example.py`: Master-detail layouts with DataGrid and ListView in different configurations.
- `treeview_example.py`: Hierarchical nodes.
- `listview_example.py`: Icons and multi-column lists.
- `listbox_checkedlistbox_example.py`: ListBox and CheckedListBox with selection modes, data binding, and events.
- `imagelist_comprehensive_example.py`: ImageList with ListView, TreeView, TabControl, and Button integration.

### Input controls
- `richtextbox_example.py`: Formatted text and RTF.
- `maskedtextbox_example.py`: MaskedTextBox with various mask formats and validation scenarios.
- `datepickerbox_example.py`: DatePickerBox with date formats, calendar dropdown, and min/max validation.
- `datetimepicker_example.py`: DatePicker with formats, custom format strings, and range validation.
- `monthcalendar_example.py`: MonthCalendar with bold dates, week numbers, and color customization.
- `trackbar_example.py`: TrackBar with horizontal/vertical orientation, tick marks, and real-world use cases.

### Container controls
- `groupbox_autosizemode_radiobutton_example.py`: GroupBox AutoSizeMode (GrowAndShrink vs GrowOnly) with RadioButtons.
- `tabcontrol_example.py`: TabControl with dynamic add/remove tabs and SelectedIndexChanged events.
- `statusbar_example.py`: StatusBar with multi-panel, icons, progress, clock, and click events.
- `picturebox_example.py`: PictureBox with SizeMode options, image manipulation, and programmatic images.

### Specialized UI
- `chat_example.py`: Modern chat interface.
- `console_example.py`: Log terminal.
- `web_browser_example.py`: Browser with tabs.
- `db_connection_example.py`: Database connection manager.
- `word_processor_example.py`: RTF Editor (WordPad style).
- `document_viewer_example.py`: Document viewer for PDF, Word, images, and text with zoom and navigation.
- `email_example.py`: Email client with folder navigation, message list, composition, and search.
- `printersettings_example.py`: PrinterSettings with PrintDialog and PageSetupDialog integration.

### Modern UI
- `winui3_example.py`: WinUI 3 controls showcase.
- `login_example.py`: Authentication flows.
- `record_form_example.py`: Auto-generated CRUD forms.
- `professional_form_example.py`: Professional form with strict Dock/Anchor layout, validation, and typed controls.

### Extended library
- `winformpy_extended_example.py`: ExtendedLabel from winformpy_extended module.

For full application boilerplates, see the `winformpy/templates/` folder.
