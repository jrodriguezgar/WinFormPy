# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-04-22

WinUI 3 module, MAUI object model refactor, 11 UI elements, 8 application templates, 40+ examples, themes, and comprehensive documentation.

### Pre-release audit (2026-04-21)

#### Fixed

- **21 undefined name bugs (F821)**: Added missing imports (`os`, `Application`, `Native`) and fixed typos (`tNative` → `Native` ×3) across 7 files
- **Lambda capture bug**: Fixed late-binding closure in `PictureBox` async error handler (`lambda: self.Error(self, e)` → `lambda err=e: self.Error(self, err)`)
- **116 bare `except:` clauses**: Replaced with `except Exception:` across 9 source files
- **Version mismatch**: Aligned all module version headers to `1.0.4` (was 1.0.6, 2.3.0, 1.0.2, 1.0.0)
- **Duplicate imports**: Removed duplicate `tkfont`, `datetime`, `WORD`, `FLAT`, `ARC` imports
- **Duplicate dict key**: Removed duplicate `highlight_text` in `winforms_theme.py`
- **CI workflow**: Fixed `formulite` → `winformpy` references in `.github/workflows/ci.yml`
- **README.md**: Fixed 5 broken links, removed duplicate Quick Start section, corrected Python badge (3.7+ → 3.10+), updated Project Structure tree, fixed Roadmap

#### Added

- `tests/test_core.py` — 49 tests for EventArgs, Color, Size, Point, Rectangle, FontStyle, and 15 enum types
- `tests/test_themes.py` — 11 tests for WinForms and WinUI 3 theme configuration
- `tests/conftest.py` — Shared pytest fixtures
- `CONTRIBUTING.md` — Contribution guidelines
- `CODE_OF_CONDUCT.md` — Contributor Covenant v2.1
- `CHANGELOG.md` — Full release history from git log

#### Changed

- `pyproject.toml` — Added classifiers, project-urls, authors, optional-dependencies, ruff/pytest configuration
- `llms.txt` — Updated project structure with tests, community files, and lint commands

#### Removed

- `winformpy/ui_elements/document_viewer/document_backend_old.py` — Dead code with syntax error (444 lines)
- `winformpy.egg-info/` — Build artifacts removed from version control

---

### `34a2de3` — Abstraction violations fixed and MAUI object model (2026-02-19)

Refactor UI elements to eliminate abstraction layer violations; expand MAUI object model with richer page/shell support.

**18 files changed** | +2,600 −1,032 lines

#### Changed

- `winformpy/mauipy.py` — Refactor MAUI Shell/Pages with expanded object model
- `winformpy/winformpy.py` — Extend core controls with additional properties and methods
- `winformpy/winformpy_tools.py` — Improve tool utilities
- `winformpy/winui3.py` — Refine WinUI 3 controls
- `winformpy/winformpy_extended.py` — Clean up extended controls
- `winformpy/mdipy.py` — Minor MDI adjustments

#### Fixed

- Remove abstraction violations in `chat_panel.py`, `console_ui.py`, `data_grid_panel.py`, `document_viewer_panel.py`, `master_detail_panel.py`, `record_form_panel.py`, `web_browser_ui.py`, `word_processor_panel.py`
- Update module READMEs (`EXTENDED_README.md`, `README.md`, `TOOLS_README.md`, `WINUI3_README.md`)

---

### `ab20186` — llms.txt added (2026-02-09)

Add LLM-friendly project summary for AI-assisted development.

**1 file changed** | +303 lines

#### Added

- `llms.txt` — Machine-readable project description with public API surface (+303 lines)

---

### `2db9832` — WinUI 3 added (2026-02-09)

Add WinUI 3 Fluent Design theme engine, expand module READMEs, and restructure root README.

**18 files changed** | +2,760 −2,208 lines

#### Added

- `winformpy/themes/winforms_theme.py` — Classic WinForms color/font defaults (+190 lines)
- `winformpy/themes/winui3_theme.py` — WinUI 3 Fluent Design theme (+212 lines)
- `winformpy/README.md` — Core module API reference (+130 lines)
- `winformpy/EXTENDED_README.md` — Extended controls documentation (+24 lines)
- `winformpy/TOOLS_README.md` — Tools module documentation (+35 lines)
- `winformpy/WINUI3_README.md` — WinUI 3 module documentation (+37 lines)
- `winformpy/templates/README.md` — Templates index (+23 lines)
- `examples/README.md` — Examples index (+37 lines)

#### Changed

- `winformpy/winui3.py` — Major expansion of WinUI 3 controls (TextBlock, ToggleSwitch, InfoBar, NavigationView)
- `winformpy/mauipy.py` — Expand MAUI module with richer navigation
- `winformpy/mdipy.py` — Enhance MDI window management
- `README.md` — Restructure root README to link module docs
- `examples/winui3_example.py` — Rewrite WinUI 3 example
- `guides/README_WinUI3.md` — Streamline WinUI 3 guide

---

### `6209f02` — New .gitignore (2026-02-05)

Update ignore rules.

**1 file changed** | +11 lines

#### Changed

- `.gitignore` — Add additional ignore patterns

---

### `6e60d8c` — View login, mask and DatePickerBox (2026-01-28)

Add DatePickerBox control, enhance login panel with visual modes, improve document viewer backend.

**8 files changed** | +1,573 −52 lines

#### Added

- `examples/datepickerbox_example.py` — DatePickerBox example (+309 lines)
- `winformpy/winformpy_extended.py` — Add `DatePickerBox` control with calendar dropdown (+841 lines)

#### Changed

- `winformpy/mauipy.py` — Add page lifecycle methods
- `winformpy/ui_elements/document_viewer/document_backend.py` — Improve document loading
- `winformpy/ui_elements/login/login_panel.py` — Add visual modes and enhanced layout
- `winformpy/winformpy.py` — Add MaskedTextBox enhancements

---

### `29d0eee` — More examples (2026-01-28)

Add WinUI 3 example, professional form example, .NET 2.0 controls example; add WinUI 3 module and guide.

**23 files changed** | +5,977 −4,375 lines

#### Added

- `winformpy/winui3.py` — WinUI 3 Fluent Design controls module (+1,071 lines)
- `examples/winui3_example.py` — WinUI 3 controls example (+643 lines)
- `examples/dotnet2_controls_example.py` — .NET 2.0 controls example (+607 lines)
- `examples/imagelist_comprehensive_example.py` — Comprehensive ImageList example (+694 lines)
- `examples/professional_form_example.py` — Professional form layout example (+734 lines)
- `guides/README_WinUI3.md` — WinUI 3 guide (+521 lines)

#### Changed

- `winformpy/winformpy.py` — Expand core controls (+615 lines)
- `winformpy/winformpy_extended.py` — Reorganize extended controls
- Refactor examples: `scrollbars`, `splitcontainer`, `tabcontrol`, `treeview`, `picturebox`, `trackbar`

#### Removed

- `IMAGELIST_TODO.md` — Remove completed TODO
- `examples/imagelist_example.py`, `examples/imagelist_example_old.py` — Replace with comprehensive version
- `examples/menustrip_example.py`, `examples/statusstrip_example.py`, `examples/toolstrip_example.py` — Consolidate into other examples

---

### `29cefb0` — Styles, documentation updates and new examples (2026-01-26)

Major documentation and examples expansion; add Document Viewer UI element; extend controls.

**81 files changed** | +21,035 −4,725 lines

#### Added

- `winformpy/ui_elements/document_viewer/` — Document Viewer UI element: `document_backend.py`, `document_viewer_panel.py`, `document_viewer_ui.py`, `README.md` (+2,459 lines)
- 25+ new example scripts: `chat_example.py`, `console_example.py`, `contextmenu_example.py`, `data_grid_crud_example.py`, `datagridview_example.py`, `datetimepicker_example.py`, `db_connection_example.py`, `document_viewer_example.py`, `email_example.py`, `listbox_checkedlistbox_example.py`, `listview_example.py`, `login_example.py`, `master_detail_example.py`, `monthcalendar_example.py`, `picturebox_example.py`, `printersettings_example.py`, `record_form_example.py`, `richtextbox_example.py`, `scrollbars_example.py`, `splitcontainer_example.py`, `statusbar_example.py`, `tabcontrol_example.py`, `trackbar_example.py`, `treeview_example.py`, `web_browser_example.py`, `word_processor_example.py`
- `guides/README_PrinterSettings.md` — PrinterSettings guide (+370 lines)
- `winformpy/winformpy_extended.py` — Add `ConsoleTextBox` and `ExtendedLabel` (+772 lines)

#### Changed

- Rewrite and expand existing examples for new package structure
- Update UI element READMEs and `README.md`
- Enhance `winformpy/winformpy.py` with new controls and properties (+1,850 lines)
- Expand `guides/README_Dock_Anchor.md` and `guides/README_winformpy_extended.md`

---

### `14821d7` — Masked CRUD in-line (2026-01-21)

Add masked editing support to DataGrid inline CRUD.

**3 files changed** | +714 −56 lines

#### Added

- `winformpy/ui_elements/data_grid/data_grid_panel.py` — Masked column types for inline editing (+552 lines)
- `winformpy/ui_elements/data_grid/README.md` — Document masked CRUD features (+129 lines)

#### Changed

- `winformpy/winformpy.py` — Extend MaskedTextBox integration (+89 lines)

---

### `3b511f4` — DataGrid CRUD in-line (2026-01-21)

Add inline create/read/update/delete to DataGrid panel.

**4 files changed** | +1,050 −6 lines

#### Added

- `winformpy/ui_elements/data_grid/data_grid_panel.py` — Inline CRUD operations (+671 lines)
- `winformpy/ui_elements/data_grid/data_grid_backend.py` — CRUD backend methods (+81 lines)
- `winformpy/ui_elements/data_grid/README.md` — CRUD documentation (+291 lines)

---

### `70c5123` — New UI elements (2026-01-21)

Add DataGrid, Login, MasterDetail, RecordForm UI elements; add UI elements README index.

**50 files changed** | +14,230 −445 lines

#### Added

- `winformpy/ui_elements/data_grid/` — DataGrid UI element: `data_grid_backend.py`, `data_grid_manager.py`, `data_grid_panel.py`, `data_grid_ui.py`, `README.md` (+3,468 lines)
- `winformpy/ui_elements/login/` — Login UI element: `login_backend.py`, `login_manager.py`, `login_panel.py`, `login_ui.py`, `README.md` (+2,379 lines)
- `winformpy/ui_elements/master_detail/` — MasterDetail UI element: `master_detail_backend.py`, `master_detail_manager.py`, `master_detail_panel.py`, `master_detail_ui.py`, `README.md` (+3,023 lines)
- `winformpy/ui_elements/record_form/` — RecordForm UI element: `record_form_backend.py`, `record_form_panel.py`, `record_form_ui.py`, `README.md` (+3,474 lines)
- `winformpy/ui_elements/README.md` — UI elements index (+866 lines)

#### Changed

- `winformpy/winformpy.py` — Add new controls and properties (+372 lines)
- Expand Chat UI element with manager layer
- Rename `email_primitives.py` → `email_backend.py`
- Update existing UI elements READMEs

---

### `0fdfb54` — New UI elements (2026-01-19)

Add Console, Email Client, Word Processor UI elements; expand core controls.

**29 files changed** | +11,711 −691 lines

#### Added

- `winformpy/ui_elements/console/` — Console UI element: `console_io.py`, `console_panel.py`, `console_ui.py`, `README.md` (+2,585 lines)
- `winformpy/ui_elements/email_client/` — Email Client UI element: `email_manager.py`, `email_panel.py`, `email_primitives.py`, `email_ui.py`, `README.md` (+3,191 lines)
- `winformpy/ui_elements/word_processor/` — Word Processor UI element: `word_processor_panel.py`, `word_processor_primitives.py`, `word_processor_ui.py`, `README.md` (+3,508 lines)
- `examples/word_processor_example.py` — Word Processor example (+649 lines)

#### Changed

- `winformpy/winformpy.py` — Major core controls expansion (+1,513 lines)
- Update Chat and WebBrowser UI elements
- Reorganize Studio template

#### Removed

- `test_dock.py` — Remove test file
- Move examples from `examples/ui_elements/` to root `examples/`

---

### `72130a3` — Templates, controls and documentation (2026-01-19)

Add 7 application templates, Chat and WebBrowser UI elements, expand core controls.

**35 files changed** | +10,125 −223 lines

#### Added

- `winformpy/templates/studio_template.py` — IDE-style template (+552 lines)
- `winformpy/templates/explorer_template.py` — File explorer template (+651 lines)
- `winformpy/templates/browser_template.py` — Web browser template (+399 lines)
- `winformpy/templates/navigation_pane_template.py` — Navigation pane template (+192 lines)
- `winformpy/templates/navigation_rail_template.py` — Navigation rail template (+196 lines)
- `winformpy/templates/winui3_template.py` — WinUI 3 gallery template (+619 lines)
- `winformpy/ui_elements/chat/` — Chat UI element: `chat_manager.py`, `chat_panel.py`, `chat_ui.py`, `README.md` (+1,908 lines)
- `winformpy/ui_elements/web_browser/` — WebBrowser UI element: `web_browser_panel.py`, `web_browser_ui.py`, `browser_data.json`, `README.md` (+2,521 lines)
- `examples/chat_example.py` — Chat example (+27 lines)

#### Changed

- `winformpy/winformpy.py` — Expand controls: MonthCalendar, DateTimePicker, ListView, RichTextBox, SplitContainer (+1,590 lines)
- `winformpy/winformpy_extended.py` — Extend FlowLayoutPanel, TableLayoutPanel (+513 lines)
- Update `guides/README_winformpy_extended.md`
- Relocate MAUI and MDI templates to `winformpy/templates/`

---

### `d6f70df` — More events (2026-01-16)

Expand event system across core controls and MAUI module.

**5 files changed** | +630 −318 lines

#### Changed

- `winformpy/winformpy.py` — Add SelectedIndexChanged, CellClick, Scroll, and other events (+545 lines)
- `winformpy/mauipy.py` — Add navigation and lifecycle events (+341 lines)
- `README.md` — Document new events (+46 lines)
- `guides/README_MAUI.md` — Update MAUI event documentation

---

### `5b89847` — Fix MDI and MAUI plus updates (2026-01-15)

Expand MDI/MAUI modules; add DB Connection UI element; extend core library.

**18 files changed** | +10,218 −1,831 lines

#### Added

- `winformpy/ui_elements/db_connection/` — DB Connection UI element: `db_connection_manager.py`, `db_connection_panel.py`, `db_connection_ui.py`, `README.md` (+1,966 lines)
- `examples/winformpy_extended_example.py` — Extended controls example (+104 lines)
- `guides/README_winformpy_extended.md` — Extended controls guide (+58 lines)

#### Changed

- `winformpy/mauipy.py` — Major expansion: Shell navigation, ContentPage, TabbedPage, FlyoutPage (+6,086 lines)
- `winformpy/mdipy.py` — Enhance MDI with cascade/tile/arrange, menu integration (+799 lines)
- `winformpy/winformpy.py` — Add new controls and properties (+773 lines)
- `winformpy/winformpy_extended.py` — Extend with additional controls (+97 lines)
- `README.md` — Major README expansion (+973 lines)
- `guides/README_MAUI.md` — Expand MAUI guide (+312 lines)

---

### Workspace-only changes (not yet committed)

#### Added

- `examples/stackpane_itemscontrol_example.py` — StackPane and ItemsControl example (workspace)

#### Fixed

- Fix 21 undefined name references (bugs) across 6 files:
  - Fix `tNative` → `Native` in `mauipy.py` (3 instances)
  - Add missing `import os` in `document_viewer/document_backend.py`
  - Add missing `Application` import in `console_ui.py` and `email_ui.py`
  - Add missing `Native` import and replace `tk.` references in `web_browser_ui.py`
  - Fix lambda variable capture (`e` → `err=e`) in `winformpy.py` PictureBox async loader
- Fix duplicate dict key `highlight_text` in `winforms_theme.py`
- Remove duplicate imports in `winformpy.py` (`tkinter.font`, `datetime`)
- Remove duplicate imports in `mauipy.py` (`WORD`, `FLAT`, `ARC`)
- Fix broken documentation link to `TOOLS_README.md` in root `README.md`
- Fix broken example link `imagelist_example.py` → `imagelist_comprehensive_example.py`
- Fix broken example link `menustrip_example.py` → `contextmenu_example.py`
- Remove dead references to non-existent `guides/README_Lazy_Import.md`
- Remove duplicate Quick Start section in root `README.md`
- Clean up ~8,700 trailing whitespace violations across all Python files

---

## [1.0.4] — 2025-12-15

Complete package redesign from single-file library to modular Python package with extended layout controls, tools module, guides, and LayoutManager enhancements.

---

### `202e351` — Enhance LayoutManager with fixed wrapping and autosize, fix Dock detection bug (2025-12-16)

Fix wrapping logic in AutoLayoutManager; add layout examples.

**8 files changed** | +3,028 −2,419 lines

#### Added

- `examples/layout_manager_example.py` — LayoutManager example (+269 lines)
- `examples/layouts_example.py` — Layouts example (+185 lines)
- `guides/README_winformpy_tools.md` — Tools guide (moved from winformpy/) (+192 lines)

#### Changed

- `winformpy/winformpy.py` — Refactor core controls layout logic
- `winformpy/winformpy_tools.py` — Fix AutoLayoutManager wrapping and autosize (+274 lines)

#### Fixed

- Dock detection bug in LayoutManager

#### Removed

- `winformpy/README_winformpy_tools.md` — Move to `guides/`

---

### `413f7d2` — Update README.md (2025-12-15)

Rewrite project README for new package structure.

**1 file changed** | +107 −96 lines

#### Changed

- `README.md` — Update installation, usage, and API overview

---

### `685fcdd` — Redesign (2025-12-15)

Major restructuring: move from `lib/winform_py.py` single-file to `winformpy/` package with separate modules for MAUI, MDI, extended controls, and tools.

**43 files changed** | +27,341 −4,343 lines

#### Added

- `winformpy/winformpy.py` — Core library: Forms, Controls, Dialogs, Enums (+19,798 lines)
- `winformpy/mauipy.py` — MAUI-style Shell/ContentPage navigation (+899 lines)
- `winformpy/mdipy.py` — MDI Parent/Child window management (+404 lines)
- `winformpy/winformpy_extended.py` — FlowLayoutPanel, TableLayoutPanel stubs (+8 lines)
- `winformpy/winformpy_tools.py` — CSSManager, FontManager, ColorManager, AutoLayoutManager (+617 lines)
- `winformpy/__init__.py` — Package init (+3 lines)
- `winformpy/README_winformpy_tools.md` — Tools documentation (+74 lines)
- New examples: `dock_anchor`, `dialogs`, `maskedtextbox`, `maui`, `mdi`, `containers`, `more_controls`, `groupbox_autosizemode_radiobutton`, `autolayout_nested`
- New guides: `README_Autosize.md`, `README_MAUI.md`, `README_MDI.md`, `README_MaskedTextBox.md`, `README_Naming.md`, `README_Windows_Forms_Layout_Emulation.md`

#### Changed

- Restructure all examples for new `winformpy` package imports
- Update guides: `README_Container_Best_Practice.md`, `README_Dock_Anchor.md`, `README_GroupBox.md`, `README_Labelframe_Container.md`

#### Removed

- `lib/winform-py.py` — Replace with `winformpy/` package
- `lib/winform-py_tools.py` — Replace with `winformpy/winformpy_tools.py`
- `CHANGELOG.md` — Remove old CHANGELOG (to be rewritten)
- `examples/all_system_styles_example.py`, `examples/css_set_controls_example.py`, `examples/system_fonts_colors_example.py`, `examples/anchor_dock_example.py`
- `guides/README_Autosize_Pack_Vs_Place.md`, `guides/README_Statusbar_Guide.md`, `guides/README_extended_layouts.md`
- `.python-version`, `uv.lock`

---

### `28625ac` — Extended layout and tools (2025-12-03)

Add `.gitignore`, documentation guides, restructure examples; remove old `lib/` source files.

**20 files changed** | +3,110 −8,222 lines

#### Added

- `.gitignore` — Git ignore rules (+206 lines)
- `guides/README_Autosize_Pack_Vs_Place.md` — AutoSize guide (+243 lines)
- `guides/README_Container_Best_Practice.md` — Container best practices (+267 lines)
- `guides/README_Dock_Anchor.md` — Dock/Anchor guide (+347 lines)
- `guides/README_GroupBox.md` — GroupBox guide (+300 lines)
- `guides/README_Labelframe_Container.md` — Labelframe guide (+697 lines)
- `guides/README_Statusbar_Guide.md` — StatusBar guide (+393 lines)
- `guides/README_extended_layouts.md` — Extended layouts guide (+361 lines)

#### Changed

- `CHANGELOG.md` — Add v1.0.4 release notes
- `README.md` — Update for extended layouts
- Refactor all examples for new imports

#### Removed

- `lib/winform-py.py` — Remove old single-file library (−6,568 lines)
- `lib/winform-py_tools.py` — Remove old tools file (−528 lines)

---

### `04ebbab` — Extended layout and tools (2025-12-03)

Version bump in `pyproject.toml`.

**1 file changed** | +2 −2 lines

#### Changed

- `pyproject.toml` — Update version to 1.0.4 and description

---

## [1.0.3] — 2025-12-01

System Styles framework, ListBox collection class, enhanced events, modal dialogs, and visual property improvements.

---

### `bd023d3` — Objects improvements and style management (2025-12-01)

Add SystemColors/SystemFonts/SystemStyles, ListBoxObjectCollection, modal dialogs, and 8 example scripts.

**15 files changed** | +4,919 −98 lines

#### Added

- `SystemColors` class — Windows Forms system color constants
- `SystemFonts` class — Windows Forms system font definitions
- `SystemStyles` class — Global styling with `SetGlobalFont()` and `SetGlobalColors()`
- `ListBoxObjectCollection` class — VB.NET-like item management (`Add()`, `Clear()`, `Remove()`)
- `ShowDialog()` method on Form for modal display
- CheckBox events: `CheckedChanged`, `CheckStateChanged`
- RadioButton enhanced group handling with shared `StringVar`
- Modal dialog support in `MessageBox` and `InputBox` (`modal` parameter)
- TabPage visual properties: `BackColor`, `ForeColor`, `Font`
- `lib/winform-py_tools.py` — CSSManager, FontManager utilities (+528 lines)
- `pyproject.toml` — Project metadata (+7 lines)
- Examples: `all_system_styles`, `anchor_dock`, `autosize`, `basic_controls`, `css_set_controls`, `hierarchical_visibility`, `system_fonts_colors`, `tooltip`

#### Changed

- All controls support `UseSystemStyles` in props
- Panel `Padding` property with proper getters/setters
- StatusBar `ShowPanels` property
- Rename `lib/winform_py.py` → `lib/winform-py.py`

---

## [1.0.2] — 2025-12-01

Props-based initialization, enhanced AutoSize with constraints, and improved property management.

---

### `881421e` — Release version 1.0.2 (2025-12-01)

Add props dictionary initialization pattern, enhanced AutoSize, and property setters.

**3 files changed** | +1,286 −486 lines

#### Added

- Props-based initialization for all controls (`Button(form, {'Text': 'Click', 'Left': 10})`)
- `Parent` and `ToolTipText` properties with getters/setters
- Comprehensive `@property` decorators for `Text`, `Visible`, and key properties

#### Changed

- `ControlBase` extended with parent notification for AutoSize
- All controls updated for both traditional and props-based setup

#### Fixed

- AutoSize behavior with proper MinimumSize/MaximumSize constraints
- Tooltip management and property synchronization

---

## [1.0.1] — 2025-12-01

ToolTip, Line, StatusBar controls, AutoSize support, and CSS styling utilities.

---

### `34d572d` — Release version 1.0.1 (2025-12-01)

Add ToolTip, Line, StatusBar classes; AutoSize properties; CSS-to-Tkinter utilities.

**3 files changed** | +2,352 −546 lines

#### Added

- `ToolTip` class — Contextual tooltips with customizable text, delay, colors, fonts, positioning
- `Line` class — Canvas line drawing (WPF/UWP-style) with stroke, dash, and events
- `StatusBarPanel` class — Individual status bar panel
- `StatusBar` class — Multi-panel status bar at form bottom
- `AutoSize`, `MinimumSize`, `MaximumSize` properties in `ControlBase`
- CSS-to-Tkinter utilities: `css_to_tkinter_config()`, `apply_css_to_widget()`

#### Changed

- `ControlBase` extended with AutoSize and built-in tooltip management
- Improved event binding and handling across controls

---

## [1.0.0] — 2025-11-29

Initial release of WinFormPy — complete mapping of Windows Forms/VB.NET syntax to Tkinter.

---

### `253dcbb` — Add comprehensive README and initial WinFormPy library (2025-12-01)

Initial library implementation with full control set.

**2 files changed** | +3,385 lines

#### Added

- `lib/winform_py.py` — Complete WinFormPy library (+3,083 lines)
- Core controls: Button, Label, TextBox, ComboBox, ListBox, CheckBox, CheckedListBox, Panel
- Dialog classes: FileDialog, OpenFileDialog, SaveFileDialog, PrintDialog, MessageBox, InputBox
- Advanced controls: PictureBox, ImageList, DataGridView, TreeView, TabControl, ProgressBar
- Utility classes: SendKeys, Timer, Screen, Point, Size, Rectangle
- Form management with VB-style properties and events

---

### `6436972` — Initial commit (2025-11-29)

Repository initialization.

**3 files changed** | +25 lines

#### Added

- `LICENSE` — MIT License
- `README.md` — Initial README
- `.gitattributes` — Git attributes

---

[1.1.0]: https://github.com/jrodriguezgar/WinFormPy/compare/v1.0.4...v1.1.0
[1.0.4]: https://github.com/jrodriguezgar/WinFormPy/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/jrodriguezgar/WinFormPy/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/jrodriguezgar/WinFormPy/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/jrodriguezgar/WinFormPy/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/jrodriguezgar/WinFormPy/releases/tag/v1.0.0
