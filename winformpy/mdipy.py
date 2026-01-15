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
        # Use the MDIChild color constant for consistent styling
        bg_color = MDIChild.MDI_CLIENT_COLOR

        self._mdi_client = tk.Frame(self._root, bg=bg_color, relief="sunken", bd=2)
        self._mdi_client.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Bind resize to update children constraints
        self._mdi_client.bind('<Configure>', self._on_client_resize, add='+')
        
    def _on_client_resize(self, event):
        """Update children when MDI client area resizes."""
        for child in self.MdiChildren:
            if hasattr(child, '_constrain_to_parent'):
                child._constrain_to_parent()
        
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
        children = [c for c in self.MdiChildren if c.WindowState == FormWindowState.Normal]
        if not children:
            return
            
        # Get MDI client area dimensions
        try:
            self._mdi_client.update_idletasks()
            client_w = self._mdi_client.winfo_width()
            client_h = self._mdi_client.winfo_height()
        except tk.TclError:
            return
        
        if value == 0: # Cascade
            x = 10
            y = 10
            step = 30
            # Default size for cascaded windows
            w = max(200, client_w - 100)
            h = max(150, client_h - 100)
            
            for child in children:
                child._set_position(x, y)
                child._set_size(w, h)
                child.Activate()
                x += step
                y += step
                # Wrap around if needed
                if x + 100 > client_w or y + 50 > client_h:
                    x = 10
                    y = 10
                    
        elif value == 1: # TileHorizontal
            # Stack vertically (full width, stacked vertically)
            count = len(children)
            if count == 0: return
            
            h = client_h // count
            y = 0
            x = 0
            w = client_w
            
            for child in children:
                child._set_position(x, y)
                child._set_size(w, h)
                y += h
                    
        elif value == 2: # TileVertical
            # Stack horizontally (side by side)
            count = len(children)
            if count == 0: return
            
            w = client_w // count
            x = 0
            y = 0
            h = client_h
            
            for child in children:
                child._set_position(x, y)
                child._set_size(w, h)
                x += w


class MDIChild:
    """
    Represents a Multiple Document Interface (MDI) child form.
    
    MDI children are embedded frames within the MDI parent's client area,
    not separate Toplevel windows. This follows the Windows Forms standard.
    """
    
    # Title bar height
    TITLE_BAR_HEIGHT = 24
    # Border width
    BORDER_WIDTH = 3
    # Button size
    BUTTON_SIZE = 18
    # Window colors (shared style)
    ACTIVE_BORDER_COLOR = "#0078D7"
    ACTIVE_TITLE_BG = "#0078D7"
    ACTIVE_TITLE_FG = "white"
    INACTIVE_BORDER_COLOR = "#AAAAAA"
    INACTIVE_TITLE_BG = "#AAAAAA"
    INACTIVE_TITLE_FG = "#333333"
    CONTENT_BG = "#F0F0F0"
    BUTTON_HOVER_COLOR = "#1C97EA"
    CLOSE_HOVER_COLOR = "#E81123"
    # MDI Client area color (matching Windows style)
    MDI_CLIENT_COLOR = "#5A5A5A"
    
    def __init__(self, props=None, mdi_parent=None):
        self._mdi_parent = None
        self._window_state = FormWindowState.Normal
        self._text = "MDI Child"
        self._width = 300
        self._height = 200
        self._left = 20
        self._top = 20
        self._menu = None
        self._visible = True
        self._enabled = True
        self._controls = []
        
        # Saved position/size for restore from maximized/minimized
        self._saved_bounds = None
        
        # Drag state
        self._drag_data = {'x': 0, 'y': 0, 'dragging': False}
        self._resize_data = {'edge': None, 'start_x': 0, 'start_y': 0, 'start_w': 0, 'start_h': 0}
        
        # Frame references
        self._outer_frame = None
        self._title_bar = None
        self._title_label = None
        self._content_frame = None
        self._btn_minimize = None
        self._btn_maximize = None
        self._btn_close = None
        
        # Apply props
        if props:
            for key, value in props.items():
                if hasattr(self, key):
                    setattr(self, key, value)
        
        # Set parent if provided
        if mdi_parent:
            self.MdiParent = mdi_parent

    def _create_window(self):
        """Creates the MDI child window frame inside the parent's client area."""
        if not self._mdi_parent:
            return
            
        parent_client = self._mdi_parent._mdi_client
        
        # Main outer frame (with border for resizing)
        self._outer_frame = tk.Frame(
            parent_client,
            bg=self.ACTIVE_BORDER_COLOR,
            relief="raised",
            bd=0
        )
        self._outer_frame.place(x=self._left, y=self._top, width=self._width, height=self._height)
        
        # Inner container (inside the border)
        inner = tk.Frame(self._outer_frame, bg=self.CONTENT_BG)
        inner.place(x=self.BORDER_WIDTH, y=self.BORDER_WIDTH, 
                    width=self._width - 2*self.BORDER_WIDTH, 
                    height=self._height - 2*self.BORDER_WIDTH)
        
        # Title bar
        self._title_bar = tk.Frame(inner, bg=self.ACTIVE_TITLE_BG, height=self.TITLE_BAR_HEIGHT)
        self._title_bar.pack(fill="x", side="top")
        self._title_bar.pack_propagate(False)
        
        # Title label
        self._title_label = tk.Label(
            self._title_bar, 
            text=self._text, 
            bg=self.ACTIVE_TITLE_BG, 
            fg=self.ACTIVE_TITLE_FG,
            font=("Segoe UI", 9),
            anchor="w",
            padx=5
        )
        self._title_label.pack(side="left", fill="x", expand=True)
        
        # Window buttons frame
        btn_frame = tk.Frame(self._title_bar, bg=self.ACTIVE_TITLE_BG)
        btn_frame.pack(side="right")
        
        # Minimize button
        self._btn_minimize = tk.Label(
            btn_frame, text="−", bg=self.ACTIVE_TITLE_BG, fg=self.ACTIVE_TITLE_FG,
            font=("Segoe UI", 10), width=3, cursor="hand2"
        )
        self._btn_minimize.pack(side="left")
        self._btn_minimize.bind('<Button-1>', lambda e: self._minimize())
        self._btn_minimize.bind('<Enter>', lambda e: self._btn_minimize.config(bg=self.BUTTON_HOVER_COLOR))
        self._btn_minimize.bind('<Leave>', lambda e: self._btn_minimize.config(bg=self.ACTIVE_TITLE_BG))
        
        # Maximize button
        self._btn_maximize = tk.Label(
            btn_frame, text="□", bg=self.ACTIVE_TITLE_BG, fg=self.ACTIVE_TITLE_FG,
            font=("Segoe UI", 10), width=3, cursor="hand2"
        )
        self._btn_maximize.pack(side="left")
        self._btn_maximize.bind('<Button-1>', lambda e: self._toggle_maximize())
        self._btn_maximize.bind('<Enter>', lambda e: self._btn_maximize.config(bg=self.BUTTON_HOVER_COLOR))
        self._btn_maximize.bind('<Leave>', lambda e: self._btn_maximize.config(bg=self.ACTIVE_TITLE_BG))
        
        # Close button
        self._btn_close = tk.Label(
            btn_frame, text="×", bg=self.ACTIVE_TITLE_BG, fg=self.ACTIVE_TITLE_FG,
            font=("Segoe UI", 12, "bold"), width=3, cursor="hand2"
        )
        self._btn_close.pack(side="left")
        self._btn_close.bind('<Button-1>', lambda e: self.Close())
        self._btn_close.bind('<Enter>', lambda e: self._btn_close.config(bg=self.CLOSE_HOVER_COLOR))
        self._btn_close.bind('<Leave>', lambda e: self._btn_close.config(bg=self.ACTIVE_TITLE_BG))
        
        # Content frame (where controls go)
        self._content_frame = tk.Frame(inner, bg=self.CONTENT_BG)
        self._content_frame.pack(fill="both", expand=True)
        
        # For compatibility - _root points to content frame
        self._root = self._content_frame
        self._tk_widget = self._content_frame
        
        # Bind drag events for title bar
        self._title_bar.bind('<Button-1>', self._start_drag)
        self._title_bar.bind('<B1-Motion>', self._on_drag)
        self._title_bar.bind('<ButtonRelease-1>', self._stop_drag)
        self._title_label.bind('<Button-1>', self._start_drag)
        self._title_label.bind('<B1-Motion>', self._on_drag)
        self._title_label.bind('<ButtonRelease-1>', self._stop_drag)
        self._title_bar.bind('<Double-Button-1>', lambda e: self._toggle_maximize())
        self._title_label.bind('<Double-Button-1>', lambda e: self._toggle_maximize())
        
        # Bind resize events on outer frame edges
        self._outer_frame.bind('<Button-1>', self._start_resize)
        self._outer_frame.bind('<B1-Motion>', self._on_resize)
        self._outer_frame.bind('<ButtonRelease-1>', self._stop_resize)
        self._outer_frame.bind('<Motion>', self._update_resize_cursor)
        
        # Focus binding
        self._outer_frame.bind('<Button-1>', self._on_click, add='+')
        inner.bind('<Button-1>', self._on_click, add='+')
        self._content_frame.bind('<Button-1>', self._on_click, add='+')
        
    def _on_click(self, event):
        """Handle click to activate window."""
        self.Activate()
        
    def _start_drag(self, event):
        """Start dragging the window."""
        if self._window_state == FormWindowState.Maximized:
            return
        self._drag_data['dragging'] = True
        self._drag_data['x'] = event.x_root
        self._drag_data['y'] = event.y_root
        self.Activate()
        
    def _on_drag(self, event):
        """Handle window dragging."""
        if not self._drag_data['dragging'] or self._window_state == FormWindowState.Maximized:
            return
            
        dx = event.x_root - self._drag_data['x']
        dy = event.y_root - self._drag_data['y']
        
        self._left += dx
        self._top += dy
        
        self._constrain_to_parent()
        self._outer_frame.place(x=self._left, y=self._top)
        
        self._drag_data['x'] = event.x_root
        self._drag_data['y'] = event.y_root
        
    def _stop_drag(self, event):
        """Stop dragging."""
        self._drag_data['dragging'] = False
        
    def _update_resize_cursor(self, event):
        """Update cursor based on position for resize."""
        if self._window_state == FormWindowState.Maximized:
            self._outer_frame.config(cursor="")
            return
            
        x, y = event.x, event.y
        w = self._outer_frame.winfo_width()
        h = self._outer_frame.winfo_height()
        b = self.BORDER_WIDTH + 2
        
        # Determine edge
        edge = None
        if x < b and y < b:
            edge = 'nw'
            cursor = 'size_nw_se'
        elif x > w - b and y < b:
            edge = 'ne'
            cursor = 'size_ne_sw'
        elif x < b and y > h - b:
            edge = 'sw'
            cursor = 'size_ne_sw'
        elif x > w - b and y > h - b:
            edge = 'se'
            cursor = 'size_nw_se'
        elif x < b:
            edge = 'w'
            cursor = 'size_we'
        elif x > w - b:
            edge = 'e'
            cursor = 'size_we'
        elif y < b:
            edge = 'n'
            cursor = 'size_ns'
        elif y > h - b:
            edge = 's'
            cursor = 'size_ns'
        else:
            cursor = ''
            
        self._outer_frame.config(cursor=cursor)
        
    def _start_resize(self, event):
        """Start resizing."""
        if self._window_state == FormWindowState.Maximized:
            return
            
        x, y = event.x, event.y
        w = self._outer_frame.winfo_width()
        h = self._outer_frame.winfo_height()
        b = self.BORDER_WIDTH + 2
        
        # Determine edge
        edge = None
        if x < b and y < b:
            edge = 'nw'
        elif x > w - b and y < b:
            edge = 'ne'
        elif x < b and y > h - b:
            edge = 'sw'
        elif x > w - b and y > h - b:
            edge = 'se'
        elif x < b:
            edge = 'w'
        elif x > w - b:
            edge = 'e'
        elif y < b:
            edge = 'n'
        elif y > h - b:
            edge = 's'
            
        if edge:
            self._resize_data['edge'] = edge
            self._resize_data['start_x'] = event.x_root
            self._resize_data['start_y'] = event.y_root
            self._resize_data['start_w'] = self._width
            self._resize_data['start_h'] = self._height
            self._resize_data['start_left'] = self._left
            self._resize_data['start_top'] = self._top
            self.Activate()
            
    def _on_resize(self, event):
        """Handle resizing."""
        edge = self._resize_data.get('edge')
        if not edge:
            return
            
        dx = event.x_root - self._resize_data['start_x']
        dy = event.y_root - self._resize_data['start_y']
        
        min_w = 150
        min_h = 100
        
        new_w = self._resize_data['start_w']
        new_h = self._resize_data['start_h']
        new_x = self._resize_data['start_left']
        new_y = self._resize_data['start_top']
        
        if 'e' in edge:
            new_w = max(min_w, self._resize_data['start_w'] + dx)
        if 'w' in edge:
            new_w = max(min_w, self._resize_data['start_w'] - dx)
            if new_w > min_w:
                new_x = self._resize_data['start_left'] + dx
        if 's' in edge:
            new_h = max(min_h, self._resize_data['start_h'] + dy)
        if 'n' in edge:
            new_h = max(min_h, self._resize_data['start_h'] - dy)
            if new_h > min_h:
                new_y = self._resize_data['start_top'] + dy
                
        self._width = new_w
        self._height = new_h
        self._left = new_x
        self._top = new_y
        
        self._constrain_to_parent()
        self._update_geometry()
        
    def _stop_resize(self, event):
        """Stop resizing."""
        self._resize_data['edge'] = None
        
    def _update_geometry(self):
        """Update the window geometry."""
        if not self._outer_frame:
            return
        self._outer_frame.place(x=self._left, y=self._top, width=self._width, height=self._height)
        
        # Update inner frame
        inner = self._outer_frame.winfo_children()[0] if self._outer_frame.winfo_children() else None
        if inner:
            inner.place(x=self.BORDER_WIDTH, y=self.BORDER_WIDTH,
                       width=self._width - 2*self.BORDER_WIDTH,
                       height=self._height - 2*self.BORDER_WIDTH)
    
    def _set_position(self, x, y):
        """Set position within parent."""
        self._left = x
        self._top = y
        if self._outer_frame:
            self._outer_frame.place(x=x, y=y)
            
    def _set_size(self, w, h):
        """Set size."""
        self._width = w
        self._height = h
        self._update_geometry()
        
    def _constrain_to_parent(self):
        """Constrain window position to stay within MDI client area."""
        if not self._mdi_parent or not self._outer_frame:
            return
            
        try:
            client_w = self._mdi_parent._mdi_client.winfo_width()
            client_h = self._mdi_parent._mdi_client.winfo_height()
        except tk.TclError:
            return
            
        # Ensure at least 50px visible horizontally and title bar visible vertically
        min_visible = 50
        
        # Constrain left edge (can't go too far right)
        if self._left > client_w - min_visible:
            self._left = client_w - min_visible
        # Can't go too far left
        if self._left + self._width < min_visible:
            self._left = min_visible - self._width
        # Can't go above
        if self._top < 0:
            self._top = 0
        # Can't go too far down (keep title bar visible)
        if self._top > client_h - self.TITLE_BAR_HEIGHT:
            self._top = client_h - self.TITLE_BAR_HEIGHT
            
    def _minimize(self):
        """Minimize the window."""
        if self._window_state != FormWindowState.Minimized:
            self._saved_bounds = (self._left, self._top, self._width, self._height)
            self._window_state = FormWindowState.Minimized
            # Hide the window (in a real implementation, show as icon in bottom)
            if self._outer_frame:
                self._outer_frame.place_forget()
                
    def _toggle_maximize(self):
        """Toggle between maximized and normal."""
        if self._window_state == FormWindowState.Maximized:
            self._restore()
        else:
            self._maximize()
            
    def _maximize(self):
        """Maximize the window to fill MDI client area."""
        if self._window_state != FormWindowState.Maximized:
            self._saved_bounds = (self._left, self._top, self._width, self._height)
            self._window_state = FormWindowState.Maximized
            
            try:
                client_w = self._mdi_parent._mdi_client.winfo_width()
                client_h = self._mdi_parent._mdi_client.winfo_height()
            except tk.TclError:
                return
                
            self._left = 0
            self._top = 0
            self._width = client_w
            self._height = client_h
            self._update_geometry()
            self._btn_maximize.config(text="❐")
            
    def _restore(self):
        """Restore window to previous size."""
        if self._saved_bounds:
            self._left, self._top, self._width, self._height = self._saved_bounds
            self._saved_bounds = None
        self._window_state = FormWindowState.Normal
        self._update_geometry()
        if self._outer_frame:
            self._outer_frame.place(x=self._left, y=self._top, width=self._width, height=self._height)
        self._btn_maximize.config(text="□")
        
    def _set_active_style(self, active):
        """Set window style based on active state."""
        if active:
            color = "#0078D7"
        else:
            color = "#AAAAAA"
            
        if self._outer_frame:
            self._outer_frame.config(bg=color)
        if self._title_bar:
            self._title_bar.config(bg=color)
        if self._title_label:
            self._title_label.config(bg=color)
        if self._btn_minimize:
            self._btn_minimize.config(bg=color)
        if self._btn_maximize:
            self._btn_maximize.config(bg=color)
        if self._btn_close:
            self._btn_close.config(bg=color)
            
    # Public API to match Form interface
    @property
    def Text(self):
        return self._text
        
    @Text.setter
    def Text(self, value):
        self._text = value
        if self._title_label:
            self._title_label.config(text=value)
        if self._mdi_parent:
            self._mdi_parent._update_window_list_menu()
            
    @property
    def Width(self):
        return self._width
        
    @Width.setter
    def Width(self, value):
        self._width = value
        self._update_geometry()
        
    @property
    def Height(self):
        return self._height
        
    @Height.setter
    def Height(self, value):
        self._height = value
        self._update_geometry()
        
    @property
    def Left(self):
        return self._left
        
    @Left.setter
    def Left(self, value):
        self._left = value
        if self._outer_frame:
            self._outer_frame.place(x=value)
            
    @property
    def Top(self):
        return self._top
        
    @Top.setter
    def Top(self, value):
        self._top = value
        if self._outer_frame:
            self._outer_frame.place(y=value)
            
    @property
    def Size(self):
        return Size(self._width, self._height)
        
    @Size.setter
    def Size(self, value):
        if isinstance(value, Size):
            self._width = value.Width
            self._height = value.Height
        elif isinstance(value, tuple):
            self._width, self._height = value
        self._update_geometry()
        
    @property
    def Location(self):
        return (self._left, self._top)
        
    @Location.setter
    def Location(self, value):
        self._left, self._top = value
        if self._outer_frame:
            self._outer_frame.place(x=self._left, y=self._top)
            
    @property
    def WindowState(self):
        return self._window_state
        
    @WindowState.setter
    def WindowState(self, value):
        if value == FormWindowState.Maximized:
            self._maximize()
        elif value == FormWindowState.Minimized:
            self._minimize()
        else:
            self._restore()
            
    @property
    def MdiParent(self):
        return self._mdi_parent

    @MdiParent.setter
    def MdiParent(self, value):
        self._mdi_parent = value
        if value:
            self._create_window()
            value._register_child(self)
            
    @property
    def Menu(self):
        return self._menu
        
    @Menu.setter
    def Menu(self, value):
        self._menu = value
        if self._mdi_parent and self._mdi_parent.ActiveMdiChild == self:
            self._mdi_parent._update_main_menu()
            
    @property
    def Visible(self):
        return self._visible
        
    @Visible.setter
    def Visible(self, value):
        self._visible = value
        if self._outer_frame:
            if value:
                self._outer_frame.place(x=self._left, y=self._top, width=self._width, height=self._height)
            else:
                self._outer_frame.place_forget()
                
    @property
    def Enabled(self):
        return self._enabled
        
    @Enabled.setter
    def Enabled(self, value):
        self._enabled = value
            
    @property
    def Controls(self):
        """Returns the list of controls in this MDI child."""
        return self._controls
        
    def Show(self):
        """Show the MDI child window."""
        self.Visible = True
        self.Activate()
        
    def Hide(self):
        """Hide the MDI child window."""
        self.Visible = False
        
    def Close(self):
        """Close the MDI child window."""
        if self._mdi_parent:
            self._mdi_parent._unregister_child(self)
        if self._outer_frame:
            self._outer_frame.destroy()
            self._outer_frame = None
            
    def Activate(self):
        """Activate this MDI child window."""
        if self._mdi_parent:
            # Deactivate other children
            for child in self._mdi_parent.MdiChildren:
                if child != self:
                    child._set_active_style(False)
            # Activate this one
            self._set_active_style(True)
            if self._outer_frame:
                self._outer_frame.lift()
            self._mdi_parent._activate_child(self)
            
    def AddControl(self, control):
        """Add a control to this MDI child."""
        self._controls.append(control)
        
    def RemoveControl(self, control):
        """Remove a control from this MDI child."""
        if control in self._controls:
            self._controls.remove(control)
            
    def SetDesktopLocation(self, x, y):
        """Set location (for compatibility with LayoutMdi)."""
        self._left = x
        self._top = y
        if self._outer_frame:
            self._outer_frame.place(x=x, y=y)
            
    def Invalidate(self):
        """Force redraw."""
        if self._outer_frame:
            self._outer_frame.update_idletasks()
