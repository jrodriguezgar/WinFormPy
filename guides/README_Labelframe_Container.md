# Container Architecture in WinFormPy

## Introduction

This document details the internal implementation of the main containers (`GroupBox` and `Panel`) in `winformpy`, explaining how Tkinter widgets (`LabelFrame` and `Frame`) are used to emulate Windows Forms behavior, including borders, titles, padding, and autosize.

## 1. GroupBox (LabelFrame)

The `GroupBox` is implemented using Tkinter's `tk.LabelFrame` widget, which provides native support for a title integrated into the border and internal padding.

### Internal Structure

```python
LabelFrame (self._tk_widget)
│   ├─ text: "GroupBox Title"
│   ├─ padx: Calculated from Padding (internal)
│   ├─ pady: Calculated from Padding (internal)
│   ├─ relief: 'groove', 'flat', etc. (according to FlatStyle)
│   └─ borderwidth: 2 (or 1 for Flat)
│
└── Frame (self._container)
    │   ├─ Position: place(x=0, y=0, relwidth=1, relheight=1)
    │   └─ bg: Inherited from parent
    │
    └── Child Controls (Buttons, Labels, etc.)
```

### Padding and Border Handling

* **Padding:** WinForms `Padding` properties are directly mapped to `padx` and `pady` of the `LabelFrame`. This creates an automatic internal margin around the `_container`.
* **Content:** The internal `_container` occupies all available space *within* the padding of the `LabelFrame` (`relwidth=1`, `relheight=1`).
* **Coordinates:** Child controls are positioned relative to the `_container`. Visually, this means that `Left=0, Top=0` for a child is offset by the border and padding of the `GroupBox`.

### AutoSize in GroupBox

The `AutoSize` logic in `GroupBox` is complex due to the need to accommodate the title and borders:

1. **Content Calculation:** All child controls are iterated to find `max_right` and `max_bottom`.
2. **Title Metrics:** `tkinter.font` is used to measure the exact width and height of the title text.
3. **Dimension Calculation:**
   * `Width` = Maximum between (Content width + Padding) and (Title width + Margin).
   * **Critical Adjustment:** An `extra_right_padding` (currently 30px) is added to compensate for the space occupied by the `LabelFrame` border curve on the right side, preventing controls from being cut off.
   * `Height` = Content height + Padding + Title height.

## 2. Panel (Frame)

The `Panel` is implemented using `tk.Frame`. Unlike `GroupBox`, it has no integrated title and handles borders differently.

### Internal Structure

```python
Frame (self._tk_widget)
│   ├─ relief: 'flat', 'solid', 'groove' (according to BorderStyle)
│   └─ borderwidth: 0 or 3 (for visibility)
│
└── Frame (self._container)
    │   ├─ Position: place(x=bw, y=bw, width=-2*bw, height=-2*bw)
    │   └─ bg: BackColor
    │
    └── Child Controls
```

### Border and Padding Handling

* **Borders:** If `BorderStyle` is not `None`, the `Panel` manually adjusts the position of the internal `_container`. It offsets `x` and `y` by the border width (`borderwidth`) and reduces its size so it does not overlap with the outer `Frame`'s border.
* **Padding:** In the standard `Panel` (manual layout), `Padding` does not automatically affect child positions (unless `Dock` is used). However, `AutoSize` does take it into account.

### AutoSize in Panel

The `AutoSize` of the `Panel` adds the space occupied by children plus the configured `Padding` and border width:

* `Width` = `max_right` (children) + `Padding.Horizontal` + `BorderWidth` * 2
* `Height` = `max_bottom` (children) + `Padding.Vertical` + `BorderWidth` * 2

## 3. Key Differences

| Feature               | GroupBox                                  | Panel                                               |
| :-------------------- | :---------------------------------------- | :-------------------------------------------------- |
| **Base Widget** | `tk.LabelFrame`                         | `tk.Frame`                                        |
| **Title**       | Integrated into the border                | Not natively supported                              |
| **Padding**     | Automatic via Tkinter's `padx`/`pady` | Calculated in AutoSize logic                        |
| **Borders**     | Managed by `LabelFrame`                 | Managed by `_container` offset                    |
| **Scroll**      | Not native                                | Supports `AutoScroll` (via `ScrollableControl`) |

## 4. Implementation Considerations

* **Update IdleTasks:** Both `GroupBox` and `Panel` force `update_idletasks()` before calculating `AutoSize` to ensure Tkinter returns the real dimensions (`winfo_reqwidth`) of children.
* **Anchor Compatibility:** When resized by `AutoSize`, both controls adjust their position (`Left`/`Top`) if anchored to the right or bottom, to maintain the illusion of growing towards the left/up. Arquitectura de Contenedores en WinFormPy
