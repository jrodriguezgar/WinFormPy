# WinFormPyLayout: Windows Forms Layout Emulation Specification

This specification details the required implementation for a Python library that accurately emulates the core layout management system of Windows Forms controls. The goal is to achieve behavior faithful to the interaction of `Padding`, `Margin`, `AutoSize`, `Dock`, and `Anchor`, as well as the functionality of specialized containers.

---

## 1. Core Positioning and Spacing Properties

These fundamental properties apply to **all controls** and define their location, dimensions, and internal/external spacing.

| Property | Type | Behavior | Key Interaction |
| :--- | :--- | :--- | :--- |
| **`Location`** | (x, y) | Defines the position of the top-left corner (relative to the parent). | Disregarded if the control is `Docked` or managed by an advanced layout container. |
| **`Size`** | (Width, Height) | Defines the dimensions of the control. | Acts as the minimum size if `AutoSizeMode` is `GrowOnly`. |
| **`MinimumSize`** / **`MaximumSize`** | (Width, Height) | Restricts the minimum and maximum dimensions the control can achieve. | Always respected, regardless of `AutoSize` or `Dock` settings. |

### 1.1. Spacing (Padding and Margin)

Spacing is crucial for precise placement and is defined in four directions (Left, Top, Right, Bottom).

| Property | Application | Behavior | Interaction Rule |
| :--- | :--- | :--- | :--- |
| **`Margin`** | **External** Space | Maintains a minimum distance from adjacent controls. The designer uses "Snaplines" based on this property. | The effective distance between neighbors is guided by the sum of their margins. |
| **`Padding`** | **Internal** Space | Separates the control's content (e.g., text) from its own borders. | The distance between a child control and its parent container is: $$\text{Distance} = \text{Child.Margin} + \text{Parent.Padding}$$ |



---

## 2. Automatic Sizing and Positioning

These properties allow controls to adapt dynamically to form or container resizing.

### 2.1. AutoSize Property (Automatic Sizing)

* **Definition:** If `True`, the control automatically sizes itself to fit its content, respecting its `Padding`.
* **Size Calculation:** The preferred size (`PreferredSize`) is calculated based on:
    $$Width = (\text{Content Width}) + (\text{Padding.Left}) + (\text{Padding.Right})$$
    $$Height = (\text{Content Height}) + (\text{Padding.Top}) + (\text{Padding.Bottom})$$
* **Clipping:** If `AutoSize=False` and the content exceeds the control's `Size`, the content must be **clipped**.

### 2.2. AutoSize and Anchor Interaction

* **Anchor Property (Anchoring):** Pins a control to one or more container edges.
* **Behavior:** When the container is resized, the control maintains a fixed distance from the anchored edges.
* **Growth Direction (with `AutoSize=True`):** The control must expand in the direction **opposite** to the anchored sides.
    * *Example:* If `Anchor = Right, Bottom`, the control grows towards the **Left** and **Top**.



### 2.3. AutoSizeMode Property (For Container Controls)

| Value | Behavior | Size Restriction |
| :--- | :--- | :--- |
| **`GrowOnly` (Default)** | The container grows to fit its content but **will not shrink** to a size smaller than its initial `Size`. | `Size` acts as the minimum size constraint. |
| **`GrowAndShrink`** | The container sizes itself **exactly** to the required bounding box of its children. | The control cannot be manually resized; its dimensions are dynamically locked to its content. |

### 2.4. Dock Property (Docking)

* **Definition:** Aligns a control to a specific side of the container (`Top`, `Bottom`, `Left`, `Right`, `Fill`).
* **Sizing Effect:**
    * **`Top`/`Bottom`:** `Width` is automatically adjusted; `Height` is respected.
    * **`Left`/`Right`:** `Height` is automatically adjusted; `Width` is respected.
* **Z-order:** The drawing order is critical. Docked controls are distributed sequentially: a control docked first consumes available space, reducing the area for subsequent docked controls.



---

## 3. Specialized Layout Containers

These controls feature an internal layout engine that automatically manages the `Location` and `Size` of their child controls, overriding the children's manual positioning properties.

| Container | Layout Mechanism | Flow/Scroll Behavior |
| :--- | :--- | :--- |
| **`Form` / `Panel` / `GroupBox`** | Basic manual layout respecting `Location`, `Dock`, and `Anchor`. | `Panel` supports scroll bars (`AutoScroll=True`) if content exceeds bounds. `GroupBox` is primarily for visual grouping. |
| **`FlowLayoutPanel`** | Arranges controls in a **linear sequence** (horizontal or vertical), governed by `FlowDirection`. | Supports **wrapping** (`WrapContents`) or clipping content. Child controls may use the `FlowBreak=True` property to force a line/column break. |
| **`TableLayoutPanel`** | Organizes controls in a **grid** (rows and columns) with dynamic sizing capabilities. | Allows **proportional** dimensioning. Child controls receive special properties (`RowSpan`, `ColumnSpan`) to span multiple cells. |
| **`SplitContainer`** | A composite control with two panels separated by a movable **splitter** bar. | Users can dynamically resize the space between the two panels at runtime. |
| **`TabControl`** | A container for multiple pages (`TabPage`). | Only the visible (active) page renders its internal layout. Controls on hidden pages do not affect the layout of the main container. |