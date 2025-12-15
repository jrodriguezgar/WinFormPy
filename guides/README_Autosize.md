# AutoSize - Current Implementation in WinFormPy

## Implemented Approach

WinFormPy uses **exclusively `place()`** for control positioning, maintaining full compatibility with the Windows Forms absolute coordinate model (Left, Top, Width, Height).

### Why not use pack()?

Although Tkinter's `pack()` calculates sizes automatically, **it is not compatible with Windows Forms**:

- Windows Forms uses absolute coordinates (Left, Top) for all controls
- `pack()` does not allow positioning controls at specific coordinates
- It would require a fundamental change incompatible with the Windows Forms API

## Implemented Solution

WinFormPy implements **AutoSize based on control properties** using `place()` with manual size calculation. This is the only way to maintain Windows Forms compatibility while keeping absolute positioning.

## AutoSize Architecture

### Class Hierarchy

1. **ControlBase** (line 2397-2720): Defines the base infrastructure

   - `AutoSize` property (getter/setter)
   - `AutoSizeMode` property (GrowOnly vs GrowAndShrink)
   - `_apply_autosize()` base method (line 3750)
   - `_apply_autosize_anchor_adjustment()` to adjust position with Anchor
2. **Basic Controls** (Button, Label, CheckBox, RadioButton):

   - **Always use GrowAndShrink internally** (not configurable)
   - Property `AutoSizeMode` overridden to always return `GrowAndShrink`
   - Behavior conforming to Windows Forms
3. **Containers** (Panel, GroupBox, UserControl):

   - Implement specialized `_apply_autosize()`
   - Calculate size based on child controls
   - AutoSizeMode configurable (GrowOnly by default)

### Main Properties

```python
# In ControlBase (line 2640-2707)
@property
def AutoSize(self):
     """Gets or sets whether the control resizes automatically."""
     return self._autosize

@AutoSize.setter
def AutoSize(self, value):
     # When disabling: saves current size as _original_size
     if not value and self._autosize:
          self._original_size = (self.Width, self.Height)
   
     # When enabling with GrowAndShrink: resets _original_size
     elif value and not self._autosize:
          if self.AutoSizeMode == AutoSizeMode.GrowAndShrink:
                self._original_size = None
   
     self._autosize = value
     if value:
          self._apply_autosize()

@property
def AutoSizeMode(self):
     """Gets or sets the mode by which the control automatically resizes itself."""
     return self._autosizemode

@AutoSizeMode.setter
def AutoSizeMode(self, value):
     self._autosizemode = value
     if self.AutoSize:
          self._apply_autosize()
```

## _apply_autosize() Method - Simple Controls

### Standard Sequence (line 3750-3810)

For simple controls (Button, Label, etc.):

```python
def _apply_autosize(self):
     """Applies automatic resizing based on content.
   
     Standard AutoSize sequence for all controls:
     1. Verify AutoSize is enabled
     2. Force geometry update (update_idletasks)
     3. Get required size from widget
     4. Apply AutoSizeMode (GrowOnly vs GrowAndShrink)
     5. Apply MinimumSize/MaximumSize restrictions
     6. Adjust position if anchored Right/Bottom
     7. Update Width/Height properties
     8. Reposition/resize visually (always, visible or not)
     9. Notify parent container
     """
     if not self.AutoSize or not self._tk_widget:
          return
   
     # 1. Force widget update to get correct dimensions
     self._tk_widget.update_idletasks()
   
     # 2. Get required size from Tkinter widget
     required_width = self._tk_widget.winfo_reqwidth()
     required_height = self._tk_widget.winfo_reqheight()
   
     # 3. Apply AutoSizeMode logic
     if self.AutoSizeMode == AutoSizeMode.GrowOnly and self._original_size:
          orig_w, orig_h = self._original_size
          required_width = max(required_width, orig_w)
          required_height = max(required_height, orig_h)
   
     # 4. Apply MinimumSize restrictions
     if self.MinimumSize:
          min_width, min_height = self.MinimumSize
          required_width = max(required_width, min_width)
          required_height = max(required_height, min_height)
   
     # 5. Apply MaximumSize restrictions
     if self.MaximumSize:
          max_width, max_height = self.MaximumSize
          if max_width > 0:
                required_width = min(required_width, max_width)
          if max_height > 0:
                required_height = min(required_height, max_height)
   
     # 6. Adjust position if Anchored to Right/Bottom
     self._apply_autosize_anchor_adjustment(required_width, required_height)

     # 7. Update dimensions
     self.Width = required_width
     self.Height = required_height
   
     # 8. Reposition with the new size (always, visible or not)
     if hasattr(self, '_place_control'):
          self._place_control(required_width, required_height)
   
     # 9. Notify parent container that this control's size changed
     self._notify_parent_layout_changed()
```

### Anchor Adjustment

```python
def _apply_autosize_anchor_adjustment(self, required_width, required_height):
     """Adjusts Left/Top if anchored Right/Bottom during AutoSize."""
     if not hasattr(self, '_anchor'): 
          return
   
     # If anchored Right (and not Left), grow to the left
     if AnchorStyles.Right in self._anchor and AnchorStyles.Left not in self._anchor:
          current_width = self.Width if self.Width is not None else required_width
          delta_w = required_width - current_width
          if delta_w != 0:
                self.Left -= delta_w
              
     # If anchored Bottom (and not Top), grow to the top
     if AnchorStyles.Bottom in self._anchor and AnchorStyles.Top not in self._anchor:
          current_height = self.Height if self.Height is not None else required_height
          delta_h = required_height - current_height
          if delta_h != 0:
                self.Top -= delta_h
```

## _apply_autosize() Method - Containers

### For UserControl, Panel, GroupBox (line 4366-4476)

Containers calculate their size based on the Left/Top/Width/Height properties of their child controls:

```python
def _apply_autosize(self):
     """Applies AutoSize logic to containers (UserControl/Panel/GroupBox).
   
     Resizes to encompass all child controls, respecting AutoSizeMode:
     - GrowOnly: Grows but does not shrink below the original size
     - GrowAndShrink: Adjusts exactly to the content
   
     Uses control properties directly (NOT widget geometry).
     """
     if not self.AutoSize or not hasattr(self, 'Controls') or not self.Controls:
          return
   
     # Prevent recursion: if already applying AutoSize, return
     if getattr(self, '_applying_autosize', False):
          return
   
     self._applying_autosize = True
   
     try:
          # Force Tkinter geometry update
          container = self._container if hasattr(self, '_container') else self._tk_widget
          if container:
                container.update_idletasks()
              
          # Get border width
          border_width = 0
          try:
                border_width = int(self._tk_widget.cget('borderwidth'))
          except:
                pass
        
          # Calculate required area based on child control PROPERTIES
          max_right = 0
          max_bottom = 0
        
          for control in self.Controls:
                # Use control's Left/Top/Width/Height properties directly
                if hasattr(control, 'Left') and hasattr(control, 'Top'):
                     x = control.Left
                     y = control.Top
                     width = getattr(control, 'Width', 0)
                     height = getattr(control, 'Height', 0)
                   
                     control_right = x + width
                     control_bottom = y + height
                     max_right = max(max_right, control_right)
                     max_bottom = max(max_bottom, control_bottom)
        
          # Add padding
          padding = self.Padding
          if len(padding) == 4:
                pad_left, pad_top, pad_right, pad_bottom = padding
                padx = (pad_left + pad_right) // 2
                pady = (pad_top + pad_bottom) // 2
          else:
                padx, pady = padding
              
          # Calculate required size including padding AND border
          required_width = max_right + padx * 2 + border_width * 2
          required_height = max_bottom + pady * 2 + border_width * 2
        
          # Apply AutoSizeMode
          if self.AutoSizeMode == AutoSizeMode.GrowOnly:
                if not hasattr(self, '_original_size'):
                     self._original_size = (0, 0)
                original_width, original_height = self._original_size
                required_width = max(required_width, original_width)
                required_height = max(required_height, original_height)
                # Update _original_size to the new maximum
                self._original_size = (required_width, required_height)
        
          # Apply MinimumSize/MaximumSize constraints
          if self.MinimumSize:
                min_width, min_height = self.MinimumSize
                required_width = max(required_width, min_width)
                required_height = max(required_height, min_height)
        
          if self.MaximumSize:
                max_width, max_height = self.MaximumSize
                if max_width > 0:
                     required_width = min(required_width, max_width)
                if max_height > 0:
                     required_height = min(required_height, max_height)
        
          # Update dimensions only if changed
          if self.Width != required_width or self.Height != required_height:
                # Adjust position if Anchored to Right/Bottom
                if hasattr(self, '_apply_autosize_anchor_adjustment'):
                     self._apply_autosize_anchor_adjustment(required_width, required_height)
              
                # Update dimensions
                self.Width = required_width
                self.Height = required_height
              
                # Force update of the widget size
                self._tk_widget.config(width=self.Width, height=self.Height)
                self._place_control(self.Width, self.Height)
              
                # Notify parent container
                self._notify_parent_layout_changed()
     finally:
          self._applying_autosize = False
```

**Key difference with simple controls:**

- Simple controls use Tkinter's `winfo_reqwidth()` / `winfo_reqheight()`
- Containers calculate based on children's `Left/Top/Width/Height` properties
- Protection against recursion with `_applying_autosize` flag

## AutoSizeMode: GrowOnly vs GrowAndShrink

### GrowAndShrink

- Adjusts size exactly to content (grows and shrinks)
- Resets `_original_size` to `None` when AutoSize is activated
- Used by default in basic controls (Button, Label, CheckBox, RadioButton)
- Overridden in basic controls to always force this mode

### GrowOnly

- Only grows, never shrinks below the reached size
- Maintains `_original_size` as reference of the maximum size reached
- Used by default in containers (Panel, GroupBox)
- Updates `_original_size` to the new maximum each time it grows

## Important Features

### 1. Parent Notification

```python
def _notify_parent_layout_changed(self):
     """Notify parent container that this control's size changed."""
     if self.master and hasattr(self.master, '_control_wrapper'):
          parent = self.master._control_wrapper
          if not getattr(parent, '_applying_autosize', False):
                if hasattr(parent, '_apply_autosize_panel'):
                     parent._apply_autosize_panel()
                elif hasattr(parent, '_apply_autosize'):
                     parent._apply_autosize()
```

When a control changes size, it notifies its parent container to update its own size if it has AutoSize enabled.

### 2. Recursion Protection

```python
if getattr(self, '_applying_autosize', False):
     return

self._applying_autosize = True
try:
     # ... calculations ...
finally:
     self._applying_autosize = False
```

Avoids infinite loops when nested containers have AutoSize.

### 3. Update Idletasks

```python
self._tk_widget.update_idletasks()
```

Forces Tkinter to calculate pending geometries before reading sizes. **Critical** to get correct measurements.

### 4. Basic Controls vs Containers

**Basic Controls** (Button, Label, CheckBox, RadioButton):

```python
@property
def AutoSizeMode(self):
     """Basic controls always use GrowAndShrink mode."""
     return AutoSizeMode.GrowAndShrink

@AutoSizeMode.setter
def AutoSizeMode(self, value):
     """AutoSizeMode is not configurable for basic controls."""
     pass  # Ignore any attempts to change it
```

**Containers** (Panel, GroupBox):

```python
# In __init__
self._autosizemode = AutoSizeMode.GrowOnly  # Configurable
```

## Use Cases

### 1. Button with AutoSize

```python
button = Button(form)
button.Text = "Click Me"
button.AutoSize = True  # Adjusts to text automatically
button.Text = "Click Me Now!"  # Re-adjusts to new text
```

### 2. GroupBox with AutoSize GrowOnly

```python
groupbox = GroupBox(form)
groupbox.AutoSize = True
groupbox.AutoSizeMode = AutoSizeMode.GrowOnly  # Default
# Add controls - groupbox grows
# Remove controls - groupbox does NOT shrink
```

### 3. Panel with AutoSize GrowAndShrink

```python
panel = Panel(form)
panel.AutoSize = True
panel.AutoSizeMode = AutoSizeMode.GrowAndShrink
# Add controls - panel grows
# Remove controls - panel shrinks
```

## Limitations and Considerations

1. **Uses place() exclusively**: Maintains Windows Forms compatibility but requires manual calculation
2. **Update idletasks required**: Without this, measurements may be incorrect
3. **Controlled recursion**: `_applying_autosize` flag prevents infinite loops
4. **Based on properties**: Containers calculate from children's properties, not from Tkinter geometry
5. **Cascading notification**: Changes propagate upwards in the container hierarchy

## Conclusion

The current AutoSize implementation in WinFormPy:

- ✅ Maintains full Windows Forms compatibility
- ✅ Supports absolute coordinates (Left/Top)
- ✅ Correctly implements GrowOnly and GrowAndShrink
- ✅ Integration with Anchor, MinimumSize, MaximumSize
- ✅ Protection against recursion in nested containers
- ⚠️ Requires manual calculation (inherent to place())
- ⚠️ Requires explicit calls to update_idletasks()

This is the **viable solution** to maintain compatibility with the Windows Forms model without compromising positioning capabilities. AutoSize - Implementación Actual en WinFormPy
