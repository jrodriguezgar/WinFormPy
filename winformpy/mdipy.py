import tkinter as tk
from .winformpy import Form, ControlBase, FormWindowState, Size, MenuItem, FormStartPosition, ToolStripMenuItem

class MDIParent(Form):
    """
    Represents a Multiple Document Interface (MDI) parent form.
    """
    def __init__(self, props=None):
        super().__init__(props)
        self.IsMdiContainer = True
        self._mdi_children = []
        self._mdi_window_list_item = None
        self._active_mdi_child = None
        self._menu = None # Store parent menu
        
        # Optional: Create a background frame (MDI Client area)
        bg_color = "SystemAppWorkspace"
        try:
            self._root.winfo_rgb(bg_color)
        except tk.TclError:
            bg_color = "gray50"

        self._mdi_client = tk.Frame(self._root, bg=bg_color)
        self._mdi_client.pack(fill="both", expand=True)
        self._mdi_client.lower()
        
    @property
    def Menu(self):
        return self._menu
        
    @Menu.setter
    def Menu(self, value):
        self._menu = value
        self._update_main_menu()

    def _update_main_menu(self):
        # Determine which menu to show
        target_menu = self._menu
        if self._active_mdi_child and self._active_mdi_child.Menu:
            target_menu = self._active_mdi_child.Menu
            
        if not target_menu:
            self._root.config(menu="")
            return

        # Create new menubar
        menubar = tk.Menu(self._root)
        
        # Build menu items
        # Support both MenuStrip (Items) and MainMenu (MenuItems)
        items = []
        if hasattr(target_menu, 'MenuItems'):
            items = target_menu.MenuItems
        elif hasattr(target_menu, 'Items'):
            items = target_menu.Items
            
        for item in items:
            self._build_menu(menubar, item)
        
        self._root.config(menu=menubar)

    @property
    def MdiChildren(self):
        """Gets the array of forms that are children of this MDI parent form."""
        # Filter out closed forms
        self._mdi_children = [c for c in self._mdi_children if c._root and c._root.winfo_exists()]
        return self._mdi_children

    @property
    def MdiWindowListItem(self):
        """Gets or sets the MenuItem that displays a list of MDI child forms."""
        return self._mdi_window_list_item

    @MdiWindowListItem.setter
    def MdiWindowListItem(self, value):
        self._mdi_window_list_item = value
        self._update_window_list_menu()

    @property
    def ActiveMdiChild(self):
        """Gets the currently active MDI child window."""
        return self._active_mdi_child

    def _register_child(self, child):
        if child not in self._mdi_children:
            self._mdi_children.append(child)
            self._update_window_list_menu()
            self._activate_child(child)

    def _unregister_child(self, child):
        if child in self._mdi_children:
            self._mdi_children.remove(child)
            if self._active_mdi_child == child:
                self._active_mdi_child = None
                # Try to activate another child
                valid_children = self.MdiChildren
                if valid_children:
                    self._activate_child(valid_children[-1])
                else:
                    self._update_main_menu()
            self._update_window_list_menu()

    def _update_window_list_menu(self):
        """Updates the MdiWindowListItem menu with the list of open child windows."""
        if not self._mdi_window_list_item:
            return
            
        # Clear previous window items
        if not hasattr(self, '_window_menu_items'):
            self._window_menu_items = []

        # Remove old items from the menu item list
        # Note: This assumes we can modify the list directly.
        # If MdiWindowListItem is a ToolStripMenuItem, it has DropDownItems.
        # If it is a MenuItem, it has MenuItems.
        
        target_list = None
        if hasattr(self._mdi_window_list_item, 'MenuItems'):
            target_list = self._mdi_window_list_item.MenuItems
        elif hasattr(self._mdi_window_list_item, 'DropDownItems'):
            target_list = self._mdi_window_list_item.DropDownItems
            
        if target_list is None:
            return

        for item in self._window_menu_items:
            if item in target_list:
                if hasattr(target_list, 'Remove'):
                    target_list.Remove(item)
                else:
                    target_list.remove(item)
        self._window_menu_items.clear()
        
        # Add separator if needed
        if target_list and self.MdiChildren:
             # Check if last item is separator?
             pass

        # Add items for each child
        for i, child in enumerate(self.MdiChildren):
            text = f"{i+1} {child.Text}"
            # Create menu item
            if hasattr(target_list, 'Add'): # ToolStripItemCollection
                item = ToolStripMenuItem(text)
                item.Click = lambda s, e, c=child: self._activate_child(c)
            else: # List (MenuItem)
                item = MenuItem(text, lambda s, e, c=child: self._activate_child(c))
            
            # Check if active
            if child == self.ActiveMdiChild:
                item.Checked = True
            
            # Add to list
            if hasattr(target_list, 'Add'): # ToolStripItemCollection
                target_list.Add(item)
            else: # List
                target_list.append(item)
                
            self._window_menu_items.append(item)
            
        # Force menu redraw
        self._update_main_menu()

    def _activate_child(self, child):
        """Activates the specified child window."""
        if child in self.MdiChildren:
            # Bring to front
            try:
                child._root.lift()
                child._root.focus_force()
            except tk.TclError:
                pass
                
            self._active_mdi_child = child
            self._update_main_menu()
            self._update_window_list_menu()

    def _build_menu(self, parent_menu, item):
        # Override to support both MenuItem and ToolStripMenuItem
        if not getattr(item, 'Visible', True):
            return
            
        text = getattr(item, 'Text', '')
        enabled = getattr(item, 'Enabled', True)
        
        # Check for subitems
        subitems = []
        if hasattr(item, 'MenuItems'):
            subitems = item.MenuItems
        elif hasattr(item, 'DropDownItems'):
            subitems = item.DropDownItems
            
        if subitems:
            # Submenu
            submenu = tk.Menu(parent_menu, tearoff=0)
            parent_menu.add_cascade(label=text, menu=submenu)
            for subitem in subitems:
                self._build_menu(submenu, subitem)
        else:
            # Command
            if text == "-":
                parent_menu.add_separator()
            else:
                state = "normal" if enabled else "disabled"
                
                # Handle click
                def on_click():
                    if hasattr(item, 'PerformClick'):
                        item.PerformClick()
                    elif hasattr(item, 'Click') and callable(item.Click):
                        item.Click(item, None)
                    elif hasattr(item, 'OnClick'): # MenuItem style
                        item.OnClick()
                        
                parent_menu.add_command(
                    label=text,
                    state=state,
                    command=on_click
                )

    def LayoutMdi(self, value):
        """Arranges the multiple-document interface (MDI) child forms within the MDI parent form.
        
        Args:
            value: LayoutMdi value. 
                   0 = Cascade
                   1 = TileHorizontal
                   2 = TileVertical
                   3 = ArrangeIcons (Not implemented)
        """
        children = self.MdiChildren
        if not children:
            return
            
        # Get parent geometry (screen coordinates)
        try:
            parent_x = self._root.winfo_rootx()
            parent_y = self._root.winfo_rooty()
            parent_w = self._root.winfo_width()
            parent_h = self._root.winfo_height()
        except tk.TclError:
            return
        
        offset_y = 0 
        offset_x = 0
        
        if value == 0: # Cascade
            x = parent_x + offset_x + 20
            y = parent_y + offset_y + 20
            step = 30
            for child in children:
                if child.WindowState == FormWindowState.Normal:
                    child.SetDesktopLocation(x, y)
                    child.Activate()
                    child._root.lift()
                    x += step
                    y += step
                    
        elif value == 1: # TileHorizontal
            # Stack vertically (Horizontal Tiling means full width, stacked vertically)
            normal_children = [c for c in children if c.WindowState == FormWindowState.Normal]
            count = len(normal_children)
            if count == 0: return
            
            h = parent_h // count
            y = parent_y
            x = parent_x
            w = parent_w
            
            for child in normal_children:
                child.SetDesktopLocation(x, y)
                child.Size = Size(w, h)
                y += h
                    
        elif value == 2: # TileVertical
            # Stack horizontally
            normal_children = [c for c in children if c.WindowState == FormWindowState.Normal]
            count = len(normal_children)
            if count == 0: return
            
            w = parent_w // count
            x = parent_x
            y = parent_y
            h = parent_h
            
            for child in normal_children:
                child.SetDesktopLocation(x, y)
                child.Size = Size(w, h)
                x += w

class MDIChild(Form):
    """
    Represents a Multiple Document Interface (MDI) child form.
    """
    def __init__(self, props=None, mdi_parent=None):
        super().__init__(props)
        self._mdi_parent = mdi_parent
        self.ConstrainToParent = True
        
        # If parent provided, register
        if self._mdi_parent:
            self.MdiParent = self._mdi_parent

        # Bind events
        self._root.bind('<FocusIn>', self._on_focus_in, add='+')
        self._root.bind('<Configure>', self._on_configure, add='+')
        
        # Hook into FormClosed
        original_closed = self.FormClosed
        self.FormClosed = lambda: (self._on_closed(), original_closed() if original_closed else None)

    @property
    def MdiParent(self):
        return self._mdi_parent

    @MdiParent.setter
    def MdiParent(self, value):
        self._mdi_parent = value
        if value:
            # Make transient to parent (always on top of parent)
            try:
                self._root.transient(value._root)
            except tk.TclError:
                pass
            
            # Register with parent
            value._register_child(self)
            
            # Set start position to CenterParent if not manual
            if self.StartPosition == FormStartPosition.WindowsDefaultLocation:
                 self.StartPosition = FormStartPosition.CenterParent

    def _on_focus_in(self, event):
        if self.MdiParent and event.widget == self._root:
            if self.MdiParent.ActiveMdiChild != self:
                self.MdiParent._activate_child(self)

    def _on_closed(self):
        if self.MdiParent:
            self.MdiParent._unregister_child(self)

    def _on_configure(self, event):
        """Constrains the child window to the parent's area."""
        if not self.MdiParent or not self.MdiParent._root.winfo_exists(): 
            return
        
        if not self.ConstrainToParent:
            return
        
        # Only handle if it's this window moving
        if event.widget != self._root: return
        
        # Avoid infinite loop
        if getattr(self, '_is_adjusting', False): return

        try:
            # Get parent bounds (Content area)
            p_x = self.MdiParent._root.winfo_rootx()
            p_y = self.MdiParent._root.winfo_rooty()
            p_w = self.MdiParent._root.winfo_width()
            p_h = self.MdiParent._root.winfo_height()
            
            # Get my bounds
            x = self._root.winfo_x()
            y = self._root.winfo_y()
            w = self._root.winfo_width()
            h = self._root.winfo_height()
            
            # Calculate limits
            # Allow title bar (approx 30px) to stay within parent vertically
            # Allow at least 50px horizontally
            
            new_x = x
            new_y = y
            changed = False
            
            # Constrain X
            # If left edge is too far right
            if x > p_x + p_w - 50:
                new_x = p_x + p_w - 50
                changed = True
            # If right edge is too far left
            elif x + w < p_x + 50:
                new_x = p_x + 50 - w
                changed = True
                
            # Constrain Y
            # If top is above parent top
            if y < p_y:
                new_y = p_y
                changed = True
            # If top is below parent bottom
            elif y > p_y + p_h - 30:
                new_y = p_y + p_h - 30
                changed = True
                
            if changed:
                self._is_adjusting = True
                self._root.geometry(f"+{int(new_x)}+{int(new_y)}")
                self.Invalidate()
                self._is_adjusting = False
                
        except tk.TclError:
            pass
