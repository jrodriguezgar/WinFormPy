
# =============================================================
# Module: winform_py.py
# Author: Vibe coding by DatamanEdge 
# Date: 2025-11-29
# Version: 1.0.0
# Description: Complete library mapping Windows Forms/(VB) syntax and objects to Tkinter.
# =============================================================

import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import os
import winsound
from datetime import date, datetime

# =======================================================================
# MAIN MODULE: winformpy.py
# =======================================================================

class ControlBase:
    # Base class for all WinFormPy controls.
    
    def __init__(self, master_tk_widget, Left=0, Top=0):
        # The actual Tkinter widget (e.g., tk.Button, tk.Label)
        self._tk_widget = None 
        # Reference to the container widget (the Form or UserControl)
        self.master = master_tk_widget 
        
        # VB-style position properties
        self.Left = Left
        self.Top = Top
        
        # MousePointer property (mouse cursor)
        self.MousePointer = "arrow"
        
        # New VB properties
        self.Enabled = True
        self.BackColor = None
        self.BorderStyle = None  # e.g., 'flat', 'raised', 'sunken', 'ridge', 'groove'
        self.BackgroundImage = None
        self.Font = None
        self.FontColor = None
        
        # Common VB events (callbacks)
        self.MouseDown = lambda button, x, y: None
        self.MouseUp = lambda button, x, y: None
        self.MouseEnter = lambda: None
        self.MouseLeave = lambda: None
        self.Enter = lambda: None  # GotFocus
        self.Leave = lambda: None  # LostFocus
        self.KeyDown = lambda key: None
        self.Click = lambda: None
        self.DoubleClick = lambda: None
        self.Paint = lambda: None
        self.Resize = lambda: None
        self.KeyPress = lambda char: None
        self.KeyUp = lambda key: None
        
    def _place_control(self, width=None, height=None):
        # Uses the 'place' geometry manager to position the control.
        if self._tk_widget:
            place_args = {
                'x': self.Left,
                'y': self.Top,
                'in_': self.master  # Ensure it's positioned relative to the current container
            }
            if width is not None:
                place_args['width'] = width
            if height is not None:
                place_args['height'] = height
                
            self._tk_widget.place(**place_args)
            # Set the cursor
            self._tk_widget.config(cursor=self.MousePointer)
            # Apply VB properties
            config = {}
            if self.BackColor is not None:
                config['bg'] = self.BackColor
            if self.BorderStyle is not None:
                config['relief'] = self.BorderStyle
            if self.BackgroundImage is not None:
                config['image'] = self.BackgroundImage
            if self.Font is not None:
                config['font'] = self.Font
            if self.FontColor is not None:
                config['fg'] = self.FontColor
            if not self.Enabled:
                config['state'] = 'disabled'
            if config:
                self._tk_widget.config(**config)

    def _bind_common_events(self):
        # Binds common events to the widget.
        if self._tk_widget:
            self._tk_widget.bind('<Button-1>', self._on_click)
            self._tk_widget.bind('<ButtonPress>', self._on_mouse_down)
            self._tk_widget.bind('<ButtonRelease>', self._on_mouse_up)
            self._tk_widget.bind('<Enter>', self._on_mouse_enter)
            self._tk_widget.bind('<Leave>', self._on_mouse_leave)
            self._tk_widget.bind('<FocusIn>', self._on_enter)
            self._tk_widget.bind('<FocusOut>', self._on_leave)
            self._tk_widget.bind('<Key>', self._on_key_down)
            self._tk_widget.bind('<Double-Button-1>', self._on_double_click)
            self._tk_widget.bind('<Configure>', self._on_paint)
            self._tk_widget.bind('<KeyPress>', self._on_key_press)
            self._tk_widget.bind('<KeyRelease>', self._on_key_up)

    def _on_mouse_down(self, event):
        # Handler for MouseDown event.
        self.MouseDown(event.num, event.x, event.y)

    def _on_mouse_up(self, event):
        # Handler for MouseUp event.
        self.MouseUp(event.num, event.x, event.y)

    def _on_mouse_enter(self, event):
        # Handler for MouseEnter event.
        self.MouseEnter()

    def _on_mouse_leave(self, event):
        # Handler for MouseLeave event.
        self.MouseLeave()

    def _on_enter(self, event):
        # Handler for Enter (GotFocus) event.
        self.Enter()

    def _on_leave(self, event):
        # Handler for Leave (LostFocus) event.
        self.Leave()

    def _on_key_down(self, event):
        # Handler for KeyDown event.
        self.KeyDown(event.keysym)

    def _on_click(self, event):
        # Handler for Click event.
        self.Click()

    def _on_double_click(self, event):
        # Handler for DoubleClick event.
        self.DoubleClick()

    def _on_paint(self, event):
        # Handler for Paint and Resize events.
        self.Paint()
        self.Resize()

    def _on_key_press(self, event):
        # Handler for KeyPress event.
        self.KeyPress(event.char)

    def _on_key_up(self, event):
        # Handler for KeyUp event.
        self.KeyUp(event.keysym)

    def apply_css(self, css_string):
        # Applies CSS styles to the control.
        styles = {}
        for rule in css_string.split(';'):
            if ':' in rule:
                key, value = rule.split(':', 1)
                styles[key.strip()] = value.strip()
        
        config = {}
        if 'color' in styles:
            config['fg'] = styles['color']
        if 'background-color' in styles:
            config['bg'] = styles['background-color']
        if 'font-size' in styles:
            # Assume font is tuple, update size
            current_font = self._tk_widget.cget('font') or ('TkDefaultFont', 10)
            if isinstance(current_font, str):
                config['font'] = (current_font, int(styles['font-size']))
            else:
                config['font'] = (current_font[0], int(styles['font-size']))
        if 'width' in styles:
            config['width'] = int(styles['width'])
        if 'height' in styles:
            config['height'] = int(styles['height'])
        
        if config:
            self._tk_widget.config(**config)

class Button(ControlBase):
    # Represents a button (CommandButton in VB6, Button in VB.NET).
    
    def __init__(self, master_form, Text="Button", Left=10, Top=10, Width=100, Height=30, Name="", Enabled=True, Visible=True, DialogResult=None, Font=None, ForeColor=None, BackColor=None, FlatStyle="Standard", Image=None, ImageAlign="left", TextImageRelation="left", UseCompatibleTextRendering=False):
        super().__init__(master_form._root, Left, Top)
        
        # VB-style properties
        self.Name = Name
        self.Text = Text
        self.Width = Width
        self.Height = Height
        self.Enabled = Enabled
        self.Visible = Visible
        self.DialogResult = DialogResult
        self.Font = Font
        self.ForeColor = ForeColor
        self.BackColor = BackColor
        self.FlatStyle = FlatStyle
        self.Image = Image
        self.ImageAlign = ImageAlign
        self.TextImageRelation = TextImageRelation
        self.UseCompatibleTextRendering = UseCompatibleTextRendering

        # Location as a tuple
        self.Location = (Left, Top)

        # Create the Tkinter widget
        self._tk_widget = tk.Button(
            self.master, 
            text=self.Text, 
            command=self._handle_click_event
        )

        # Apply configurations
        config = {}
        if self.Font:
            config['font'] = self.Font
        if self.ForeColor:
            config['fg'] = self.ForeColor
        if self.BackColor:
            config['bg'] = self.BackColor
        if self.Image:
            config['image'] = self.Image
        if self.TextImageRelation:
            config['compound'] = self.TextImageRelation
        # Map FlatStyle to relief
        relief_map = {'Standard': 'raised', 'Flat': 'flat', 'Popup': 'ridge', 'System': 'raised'}
        config['relief'] = relief_map.get(self.FlatStyle, 'raised')
        if self.Enabled:
            config['state'] = 'normal'
        else:
            config['state'] = 'disabled'

        if config:
            self._tk_widget.config(**config)

        # Bind common events
        self._bind_common_events()

        # Position if visible
        if self.Visible:
            self._place_control(self.Width, self.Height)
        else:
            self._tk_widget.place_forget()

    def _handle_click_event(self):
        # Intermediate function to execute the assigned Click method.
        self.Click()

    def set_Enabled(self, enabled):
        # Sets whether the button is enabled.
        self.Enabled = enabled
        self._tk_widget.config(state='normal' if enabled else 'disabled')

    def set_Visible(self, visible):
        # Sets the visibility of the button.
        self.Visible = visible
        if visible:
            self._place_control(self.Width, self.Height)
        else:
            self._tk_widget.place_forget()

class Label(ControlBase):
    # Represents a text label.
    
    def __init__(self, master_form, Text="Label", Left=10, Top=50, Name="", Enabled=True, Visible=True, Font=None, ForeColor=None, BackColor=None, BorderStyle=None, TextAlign="left", AutoSize=True, UseMnemonic=False, Padding=(0,0), Margin=(0,0)):
        # Resolve master widget
        master_widget = getattr(master_form, '_root', getattr(master_form, '_tk_widget', getattr(master_form, '_frame', master_form)))
        super().__init__(master_widget, Left, Top)

        # VB-style properties
        self.Name = Name
        self.Text = Text
        self.Enabled = Enabled
        self.Visible = Visible
        self.Font = Font
        self.ForeColor = ForeColor
        self.BackColor = BackColor
        self.BorderStyle = BorderStyle
        self.TextAlign = TextAlign  # 'left', 'center', 'right', or combinations like 'nw', 'center', etc.
        self.AutoSize = AutoSize
        self.UseMnemonic = UseMnemonic
        self.Padding = Padding  # (padx, pady)
        self.Margin = Margin  # Not directly used in Tkinter

        # VB events
        self.TextChanged = lambda: None
        
        # Process UseMnemonic
        display_text = self.Text
        underline = -1
        if self.UseMnemonic and '&' in self.Text:
            idx = self.Text.find('&')
            if idx + 1 < len(self.Text):
                underline = idx
                display_text = self.Text[:idx] + self.Text[idx+1:]
        
        # Create the Tkinter widget
        self._tk_widget = tk.Label(self.master, text=display_text, underline=underline)
        
        # Apply properties
        if self.ForeColor:
            self._tk_widget.config(fg=self.ForeColor)
        if self.BackColor:
            self._tk_widget.config(bg=self.BackColor)
        if self.BorderStyle:
            self._tk_widget.config(relief=self.BorderStyle)
        if self.Font:
            self._tk_widget.config(font=self.Font)
        
        # Alignment
        if self.TextAlign == 'left':
            self._tk_widget.config(anchor='w', justify='left')
        elif self.TextAlign == 'center':
            self._tk_widget.config(anchor='center', justify='center')
        elif self.TextAlign == 'right':
            self._tk_widget.config(anchor='e', justify='right')
        else:
            self._tk_widget.config(anchor=self.TextAlign)
        
        # Padding
        padx, pady = self.Padding
        self._tk_widget.config(padx=padx, pady=pady)
        
        # Enabled/Visible
        if not self.Enabled:
            self._tk_widget.config(state='disabled')
        if not self.Visible:
            self._tk_widget.place_forget()
        
        # Bind events
        self._bind_common_events()
        self._tk_widget.bind('<Button-1>', self._on_click)
        self._tk_widget.bind('<Double-Button-1>', self._on_double_click)
        self._tk_widget.bind('<Configure>', self._on_paint)  # Placeholder for Paint
        
        # AutoSize: if True, do not set width/height
        if self.AutoSize:
            self._place_control()  # Without width/height
        else:
            self._place_control(width=100, height=25)  # Default values

    def _on_click(self, event):
        # Handler for Click event.
        self.Click()

    def _on_double_click(self, event):
        # Handler for DoubleClick event.
        self.DoubleClick()

    def _on_paint(self, event):
        # Handler for Paint event (placeholder).
        self.Paint()

    def set_Text(self, new_text):
        # Set method to update the text at runtime.
        self.Text = new_text
        self._tk_widget.config(text=new_text)
        self.TextChanged()
        
class TextBox(ControlBase):
    # Represents a simple text box.
    
    def __init__(self, master_form, Text="", Left=10, Top=80, Width=200, Height=25, Name="", Enabled=True, Visible=True, ReadOnly=False, Multiline=False, ScrollBars=None, PasswordChar="", UseSystemPasswordChar=False, MaxLength=0, TextAlign="left", WordWrap=True, AcceptsReturn=True):
        super().__init__(master_form._root, Left, Top)
        
        # VB Properties
        self.Name = Name
        self.Text = Text
        self.Enabled = Enabled
        self.Visible = Visible
        self.ReadOnly = ReadOnly
        self.Multiline = Multiline
        self.ScrollBars = ScrollBars  # 'none', 'horizontal', 'vertical', 'both'
        self.PasswordChar = PasswordChar
        self.UseSystemPasswordChar = UseSystemPasswordChar
        self.MaxLength = MaxLength
        self.TextAlign = TextAlign  # 'left', 'center', 'right'
        self.WordWrap = WordWrap
        self.AcceptsReturn = AcceptsReturn
        
        # VB Events (callbacks)
        self.TextChanged = lambda: None
        self.MouseMove = lambda x, y: None
        
        # Create the Tkinter widget
        if self.Multiline:
            self._tk_widget = tk.Text(self.master, height=Height//15, wrap='word' if self.WordWrap else 'none')
            if self.ScrollBars in ['vertical', 'both']:
                vscroll = tk.Scrollbar(self.master, command=self._tk_widget.yview)
                self._tk_widget.config(yscrollcommand=vscroll.set)
                vscroll.place(x=Left+Width-15, y=Top, height=Height)
            if self.ScrollBars in ['horizontal', 'both']:
                hscroll = tk.Scrollbar(self.master, orient='horizontal', command=self._tk_widget.xview)
                self._tk_widget.config(xscrollcommand=hscroll.set)
                hscroll.place(x=Left, y=Top+Height-15, width=Width)
            self._tk_widget.insert('1.0', self.Text)
            if self.ReadOnly:
                self._tk_widget.config(state='disabled')
            
            # Bind events for Text widget
            self._tk_widget.bind('<<Modified>>', self._on_text_changed)
            self._tk_widget.bind('<KeyRelease>', self._on_key_up)
            self._tk_widget.bind('<Button-1>', self._on_click)
            self._tk_widget.bind('<Double-Button-1>', self._on_double_click)
            self._tk_widget.bind('<Motion>', self._on_mouse_move)
        else:
            self._text_var = tk.StringVar(value=Text)
            self._tk_widget = tk.Entry(self.master, textvariable=self._text_var)
            if self.PasswordChar:
                self._tk_widget.config(show=self.PasswordChar)
            elif self.UseSystemPasswordChar:
                self._tk_widget.config(show='*')
            if self.ReadOnly:
                self._tk_widget.config(state='readonly')
            if self.MaxLength > 0:
                vcmd = (self.master.register(self._validate_length), '%P')
                self._tk_widget.config(validate='key', validatecommand=vcmd)
            
            # Bind events for Entry widget
            self._text_var.trace('w', self._on_text_changed_entry)
            self._tk_widget.bind('<KeyRelease>', self._on_key_up)
            self._tk_widget.bind('<Button-1>', self._on_click)
            self._tk_widget.bind('<Double-Button-1>', self._on_double_click)
            self._tk_widget.bind('<Motion>', self._on_mouse_move)
        
        self._bind_common_events()
        
        # Apply alignment
        if self.TextAlign == 'center':
            self._tk_widget.config(justify='center')
        elif self.TextAlign == 'right':
            self._tk_widget.config(justify='right')
        
        # Apply Enabled/Visible
        if not self.Enabled:
            self._tk_widget.config(state='disabled')
        if not self.Visible:
            self._tk_widget.place_forget()
        
        self._place_control(Width, Height if not self.Multiline else Height)

    def _on_text_changed(self, event=None):
        # Handler for TextChanged event (Text widget).
        self.TextChanged()
        # Reset modified flag
        self._tk_widget.edit_modified(False)

    def _on_text_changed_entry(self, *args):
        # Handler for TextChanged event (Entry widget).
        self.TextChanged()

    def _on_mouse_move(self, event):
        # Handler for MouseMove event.
        self.MouseMove(event.x, event.y)

    def _validate_length(self, new_text):
        return len(new_text) <= self.MaxLength

    def get_Text(self):
        # Gets the text from the TextBox.
        if self.Multiline:
            return self._tk_widget.get('1.0', 'end-1c')
        else:
            return self._text_var.get()

    def set_Text(self, new_text):
        # Sets the text of the TextBox.
        if self.Multiline:
            self._tk_widget.delete('1.0', 'end')
            self._tk_widget.insert('1.0', new_text)
        else:
            self._text_var.set(new_text)

class ComboBox(ControlBase):
    # Represents a ComboBox (dropdown).
    
    def __init__(self, master_form, Items=None, Left=10, Top=110, Width=200, Name="", DataSource=None, DisplayMember="", ValueMember="", SelectedItem=None, SelectedValue=None, SelectedIndex=-1, Text="", DropDownStyle="readonly", DroppedDown=False, MaxDropDownItems=10, MaxLength=0, Enabled=True, Visible=True):
        super().__init__(master_form._root, Left, Top)
        
        # VB Properties
        self.Name = Name
        self.Items = Items or []
        self.DataSource = DataSource
        self.DisplayMember = DisplayMember
        self.ValueMember = ValueMember
        self.SelectedItem = SelectedItem
        self.SelectedValue = SelectedValue
        self.SelectedIndex = SelectedIndex
        self.Text = Text
        self.DropDownStyle = DropDownStyle  # 'readonly', 'normal'
        self.DroppedDown = DroppedDown
        self.MaxDropDownItems = MaxDropDownItems
        self.MaxLength = MaxLength
        self.Enabled = Enabled
        self.Visible = Visible
        
        # VB Events (callbacks)
        self.SelectedIndexChanged = lambda: None
        self.SelectionChangeCommitted = lambda: None
        self.TextChanged = lambda: None
        self.DropDown = lambda: None
        self.DropDownClosed = lambda: None
        self.Validating = lambda: None
        self.DrawItem = lambda index, graphics, bounds, state: None  # Placeholder
        
        self.Width = Width
        self.Height = 25  # Fixed height for ComboBox
        
        # If DataSource, populate Items
        if self.DataSource:
            self._populate_from_datasource()
        
        self._selected_var = tk.StringVar(value=self.Text)
        
        # Create the Tkinter widget
        self._tk_widget = ttk.Combobox(self.master, textvariable=self._selected_var, values=self.Items, state=self.DropDownStyle)
        self._tk_widget.config(height=self.MaxDropDownItems)
        if self.MaxLength > 0:
            vcmd = (self.master.register(self._validate_length), '%P')
            self._tk_widget.config(validate='key', validatecommand=vcmd)
        
        # Apply Enabled/Visible
        if not self.Enabled:
            self._tk_widget.config(state='disabled')
        if not self.Visible:
            self._tk_widget.place_forget()
        
        self._place_control(self.Width, 25) # Fixed height
        
        # Bind events
        self._tk_widget.bind('<<ComboboxSelected>>', self._on_selected_index_changed)
        if self.DropDownStyle != 'readonly':
            self._selected_var.trace('w', self._on_text_changed)
        self._tk_widget.bind('<FocusIn>', self._on_enter)
        self._tk_widget.bind('<FocusOut>', self._on_leave)
        self._tk_widget.bind('<Key>', self._on_key_down)
        self._tk_widget.bind('<KeyPress>', self._on_key_press)
        
        # Set initial selection
        if self.SelectedIndex >= 0 and self.SelectedIndex < len(self.Items):
            self._tk_widget.current(self.SelectedIndex)
        elif self.SelectedItem:
            try:
                idx = self.Items.index(self.SelectedItem)
                self._tk_widget.current(idx)
            except ValueError:
                pass

    def _populate_from_datasource(self):
        # Populates Items from DataSource using DisplayMember.
        if self.DataSource and self.DisplayMember:
            self.Items = [getattr(item, self.DisplayMember) for item in self.DataSource]

    def _validate_length(self, new_text):
        return len(new_text) <= self.MaxLength

    def get_SelectedItem(self):
        # Gets the selected item.
        idx = self._tk_widget.current()
        if idx >= 0:
            return self.Items[idx]
        return None

    def set_SelectedItem(self, item):
        # Sets the selected item.
        try:
            idx = self.Items.index(item)
            self._tk_widget.current(idx)
        except ValueError:
            pass

    def get_SelectedValue(self):
        # Gets the value of the ValueMember of the selected item.
        if self.DataSource and self.ValueMember and self.get_SelectedItem():
            idx = self._tk_widget.current()
            if idx >= 0:
                return getattr(self.DataSource[idx], self.ValueMember)
        return self.get_SelectedItem()

    def get_SelectedIndex(self):
        # Gets the index of the selected item.
        return self._tk_widget.current()

    def set_SelectedIndex(self, index):
        # Sets the selected index.
        if 0 <= index < len(self.Items):
            self._tk_widget.current(index)

    def _on_selected_index_changed(self, event=None):
        # Handler for SelectedIndexChanged event.
        self.SelectedIndexChanged()
        self.SelectionChangeCommitted()

    def _on_text_changed(self, *args):
        # Handler for TextChanged event.
        self.TextChanged()

    def _on_enter(self, event):
        # Handler for Enter (GotFocus) event.
        self.Enter()

    def _on_leave(self, event):
        # Handler for Leave (LostFocus) event.
        self.Leave()
        self.Validating()

    def _on_key_down(self, event):
        """Handler for KeyDown event."""
        self.KeyDown(event.keysym)

    def _on_key_press(self, event):
        """Handler for KeyPress event."""
        self.KeyPress(event.char)

class ListBox(ControlBase):
    # Represents a ListBox.
    
    def __init__(self, master_form, Items=None, Left=10, Top=170, Width=200, Height=100, Name="", DataSource=None, DisplayMember="", ValueMember="", SelectedIndex=-1, SelectionMode="One", TopIndex=0, IntegralHeight=True, MultiColumn=False, ScrollAlwaysVisible=False, Enabled=True, Font=None, ForeColor=None):
        super().__init__(master_form._root, Left, Top)
        
        self.Name = Name
        self.Width = Width
        self.Height = Height
        self.Items = Items or []
        self.DataSource = DataSource
        self.DisplayMember = DisplayMember
        self.ValueMember = ValueMember
        self.SelectedIndex = SelectedIndex
        self.SelectionMode = SelectionMode
        self.TopIndex = TopIndex
        self.IntegralHeight = IntegralHeight
        self.MultiColumn = MultiColumn
        self.ScrollAlwaysVisible = ScrollAlwaysVisible
        self.Enabled = Enabled
        self.Font = Font
        self.ForeColor = ForeColor
        
        # VB Events (callbacks)
        self.SelectedIndexChanged = lambda: None
        self.SelectedValueChanged = lambda: None
        self.Format = lambda item: None  # placeholder
        self.DrawItem = lambda index, graphics, bounds, state: None  # placeholder
        
        # If DataSource, populate Items
        if self.DataSource and self.DisplayMember:
            self.Items = [getattr(item, self.DisplayMember) for item in self.DataSource]
        
        # Create the Tkinter widget
        self._tk_widget = tk.Listbox(self.master)
        
        # Set selectmode
        selectmode_map = {'One': 'browse', 'MultiSimple': 'multiple', 'MultiExtended': 'extended', 'None': 'single'}
        self._tk_widget.config(selectmode=selectmode_map.get(self.SelectionMode, 'browse'))
        
        # Add items
        for item in self.Items:
            self._tk_widget.insert(tk.END, item)
        
        # Scrollbars if ScrollAlwaysVisible
        if self.ScrollAlwaysVisible:
            vscroll = tk.Scrollbar(self.master, command=self._tk_widget.yview)
            self._tk_widget.config(yscrollcommand=vscroll.set)
            vscroll.place(x=Left+Width-15, y=Top, height=Height)
            if self.MultiColumn:  # For multi-column, add horizontal scroll
                hscroll = tk.Scrollbar(self.master, orient='horizontal', command=self._tk_widget.xview)
                self._tk_widget.config(xscrollcommand=hscroll.set)
                hscroll.place(x=Left, y=Top+Height-15, width=Width)
        
        # Apply Font, ForeColor, Enabled
        config = {}
        if self.Font:
            config['font'] = self.Font
        if self.ForeColor:
            config['fg'] = self.ForeColor
        if not self.Enabled:
            config['state'] = 'disabled'
        if config:
            self._tk_widget.config(**config)
        
        # Set TopIndex
        if self.TopIndex > 0:
            self._tk_widget.yview(self.TopIndex)
        
        # Set SelectedIndex
        if self.SelectedIndex >= 0:
            self.set_SelectedIndex(self.SelectedIndex)
        
        self._place_control(self.Width, self.Height)
        
        # Bind events
        self._tk_widget.bind('<<ListboxSelect>>', self._on_selected_index_changed)
        self._tk_widget.bind('<Button-1>', self._on_click)
        self._tk_widget.bind('<Double-Button-1>', self._on_double_click)
        self._tk_widget.bind('<FocusIn>', self._on_enter)
        self._tk_widget.bind('<FocusOut>', self._on_leave)
        self._tk_widget.bind('<Key>', self._on_key_down)

    def get_SelectedItem(self):
        # Gets the selected item.
        selection = self._tk_widget.curselection()
        if selection:
            return self._tk_widget.get(selection[0])
        return None

    def get_SelectedIndex(self):
        # Gets the index of the selected item.
        selection = self._tk_widget.curselection()
        return selection[0] if selection else -1

    def set_SelectedIndex(self, index):
        # Sets the selected index.
        if 0 <= index < self._tk_widget.size():
            self._tk_widget.selection_set(index)

    def get_SelectedItems(self):
        # Gets the list of selected items.
        selections = self._tk_widget.curselection()
        return [self._tk_widget.get(i) for i in selections]

    def get_SelectedIndices(self):
        # Gets the list of selected indices.
        return list(self._tk_widget.curselection())

    def get_SelectedValue(self):
        # Gets the ValueMember value of the selected item.
        if self.DataSource and self.ValueMember:
            idx = self.get_SelectedIndex()
            if idx >= 0:
                return getattr(self.DataSource[idx], self.ValueMember)
        return self.get_SelectedItem()

    def set_TopIndex(self, index):
        # Sets the index of the first visible item.
        self.TopIndex = index
        self._tk_widget.yview(index)
    
    def _on_selected_index_changed(self, event=None):
        # Handler for SelectedIndexChanged event.
        self.SelectedIndexChanged()
        self.SelectedValueChanged()

class CheckBox(ControlBase):
    # Represents a CheckBox.
    
    def __init__(self, master_form, Text="CheckBox", Left=10, Top=140, Name="", Checked=False, CheckState=0, ThreeState=False, Enabled=True, Visible=True, Font=None, ForeColor=None, BackColor=None, TextAlign="w", Appearance="Normal"):
        super().__init__(master_form._root, Left, Top)
        
        self.Name = Name
        self.Text = Text
        self.Checked = Checked
        self.CheckState = CheckState
        self.ThreeState = ThreeState
        self.Enabled = Enabled
        self.Visible = Visible
        self.Font = Font
        self.ForeColor = ForeColor
        self.BackColor = BackColor
        self.TextAlign = TextAlign
        self.Appearance = Appearance
        
        self.Location = (Left, Top)
        
        # Variable based on ThreeState
        if self.ThreeState:
            self._state_var = tk.IntVar(value=self.CheckState)
        else:
            self._state_var = tk.BooleanVar(value=self.Checked)
        
        # Create the Tkinter widget
        self._tk_widget = tk.Checkbutton(self.master, text=self.Text, variable=self._state_var)
        
        # Apply configurations
        config = {}
        if self.Font:
            config['font'] = self.Font
        if self.ForeColor:
            config['fg'] = self.ForeColor
        if self.BackColor:
            config['bg'] = self.BackColor
        if self.TextAlign:
            config['anchor'] = self.TextAlign
        if self.Appearance == "Button":
            config['indicatoron'] = 0
        if not self.Enabled:
            config['state'] = 'disabled'
        if config:
            self._tk_widget.config(**config)
        
        # Position if visible
        if self.Visible:
            self._place_control()
        else:
            self._tk_widget.place_forget()

    def get_Checked(self):
        # Gets whether it is checked (boolean).
        return bool(self._state_var.get())

    def set_Checked(self, value):
        # Sets whether it is checked.
        self.Checked = value
        self._state_var.set(value)

    def get_CheckState(self):
        # Gets the checkbox state (0=Unchecked, 1=Checked, 2=Indeterminate).
        return self._state_var.get()

    def set_CheckState(self, value):
        # Sets the checkbox state.
        self.CheckState = value
        self._state_var.set(value)

class CheckedListBox(ControlBase):
    # Represents a CheckedListBox (list with checkboxes).
    
    def __init__(self, master_form, Items=None, Left=10, Top=200, Width=200, Height=100, Name="", DataSource=None, DisplayMember="", ValueMember="", SelectedItems=None, SelectionMode="One", CheckOnClick=True, ThreeDCheckBoxes=True, Enabled=True, Visible=True, Font=None, ForeColor=None, BackColor=None):
        super().__init__(master_form._root, Left, Top)
        
        self.Name = Name
        self.Width = Width
        self.Height = Height
        self.Items = Items or []
        self.DataSource = DataSource
        self.DisplayMember = DisplayMember
        self.ValueMember = ValueMember
        self.SelectedItems = SelectedItems or []
        self.SelectionMode = SelectionMode
        self.CheckOnClick = CheckOnClick
        self.ThreeDCheckBoxes = ThreeDCheckBoxes
        self.Enabled = Enabled
        self.Visible = Visible
        self.Font = Font
        self.ForeColor = ForeColor
        self.BackColor = BackColor
        
        # VB Events (callbacks)
        self.ItemCheck = lambda item, new_value: None
        self.SelectedIndexChanged = lambda: None
        self.SelectedValueChanged = lambda: None
        self.Format = lambda item: None
        
        self.Location = (Left, Top)
        
        # If DataSource, populate Items
        if self.DataSource and self.DisplayMember:
            self.Items = [getattr(item, self.DisplayMember) for item in self.DataSource]
        
        # Create a Frame to contain the Checkbuttons
        self._frame = tk.Frame(self.master, width=self.Width, height=self.Height)
        self._tk_widget = self._frame
        
        self._checks = []
        self._vars = []
        relief = 'raised' if self.ThreeDCheckBoxes else 'flat'
        for item in self.Items:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self._frame, text=item, variable=var, anchor='w', relief=relief)
            if self.Font:
                chk.config(font=self.Font)
            if self.ForeColor:
                chk.config(fg=self.ForeColor)
            if self.BackColor:
                chk.config(bg=self.BackColor)
            if not self.Enabled:
                chk.config(state='disabled')
            chk.pack(fill='x')
            self._checks.append(chk)
            self._vars.append(var)
        
        # Bind events to checkbuttons
        for i, chk in enumerate(self._checks):
            chk.bind('<Button-1>', self._on_click)
            chk.bind('<Double-Button-1>', self._on_double_click)
            chk.bind('<FocusIn>', self._on_enter)
            chk.bind('<FocusOut>', self._on_leave)
            chk.bind('<Key>', lambda e, idx=i: self._on_key_down_wrapper(e, idx))
            # For ItemCheck, use trace
            self._vars[i].trace('w', lambda *args, idx=i: self._on_item_check(idx))
        
        # Position if visible
        if self.Visible:
            self._place_control(self.Width, self.Height)
        else:
            self._frame.place_forget()

    def get_CheckedItems(self):
        # Gets the list of checked items.
        return [self.Items[i] for i, var in enumerate(self._vars) if var.get()]

    def get_CheckedIndices(self):
        # Gets the list of checked indices.
        return [i for i, var in enumerate(self._vars) if var.get()]

    def set_Checked(self, index, value):
        # Sets whether an item is checked.
        self.ItemCheck(index, value)
        if 0 <= index < len(self._vars):
            self._vars[index].set(value)

    def get_SelectedItems(self):
        # Gets the list of selected items (same as checked for simplicity).
        return self.get_CheckedItems()

    def get_SelectedIndices(self):
        # Gets the list of selected indices.
        return self.get_CheckedIndices()
    
    def _on_item_check(self, index):
        # Handler for ItemCheck event.
        self.ItemCheck(index, self._vars[index].get())
    
    def _on_selected_index_changed(self, event=None):
        # Handler for SelectedIndexChanged event.
        self.SelectedIndexChanged()
        self.SelectedValueChanged()

class Panel(ControlBase):
    # Represents a Panel (container).
    
    def __init__(self, master_form, Left=0, Top=0, Width=200, Height=100, Name="", Enabled=True, Visible=True, BackColor='lightgray', BackgroundImage=None, BorderStyle='flat', AutoScroll=False, AutoScrollOffset=(0,0), Dock=None, Anchor=None, Padding=(0,0)):
        # Resolve master widget
        master_widget = getattr(master_form, '_root', getattr(master_form, '_tk_widget', getattr(master_form, '_frame', master_form)))
        super().__init__(master_widget, Left, Top)
        
        self.Name = Name
        self.Width = Width
        self.Height = Height
        self.Enabled = Enabled
        self.Visible = Visible
        self.BackColor = BackColor
        self.BackgroundImage = BackgroundImage
        self.BorderStyle = BorderStyle
        self.AutoScroll = AutoScroll
        self.AutoScrollOffset = AutoScrollOffset
        self.Dock = Dock
        self.Anchor = Anchor
        self.Padding = Padding
        
        self.Location = (Left, Top)
        
        # Create the Tkinter widget (Frame)
        padx, pady = self.Padding
        config = {
            'width': self.Width,
            'height': self.Height,
            'bg': self.BackColor,
            'relief': self.BorderStyle,
            'padx': padx,
            'pady': pady
        }
        if self.BackgroundImage:
            config['image'] = self.BackgroundImage
        self._tk_widget = tk.Frame(self.master, **config)
        
        if self.Visible:
            self._place_control(self.Width, self.Height)
        else:
            self._tk_widget.place_forget()
        
        # Bind events
        self._tk_widget.bind('<Configure>', self._on_paint)
        self._tk_widget.bind('<Button-1>', self._on_click)
        self._tk_widget.bind('<Double-Button-1>', self._on_double_click)
        self._tk_widget.bind('<Enter>', self._on_mouse_enter)
        self._tk_widget.bind('<Leave>', self._on_mouse_leave)
        self._tk_widget.bind('<ButtonPress>', self._on_mouse_down)
        self._tk_widget.bind('<ButtonRelease>', self._on_mouse_up)
        
        # List of controls inside the panel
        self.Controls = []
        
        # VB Events
        self.ControlAdded = lambda control: None
        self.ControlRemoved = lambda control: None

    def AddControl(self, control):
        # Adds a control to the Panel.
        self.Controls.append(control)
        # Change the control's master to the panel
        control.master = self._tk_widget
        control._place_control()
        # Apply the panel's Enabled property to the control
        if hasattr(control, 'Enabled'):
            control.Enabled = self.Enabled
            if hasattr(control, '_tk_widget'):
                control._tk_widget.config(state='normal' if self.Enabled else 'disabled')
        self.ControlAdded(control)

    def set_Enabled(self, enabled):
        # Sets whether the panel is enabled and propagates to controls.
        self.Enabled = enabled
        for control in self.Controls:
            if hasattr(control, 'Enabled'):
                control.Enabled = enabled
                if hasattr(control, '_tk_widget'):
                    control._tk_widget.config(state='normal' if enabled else 'disabled')

    def RemoveControl(self, control):
        # Removes a control from the Panel.
        if control in self.Controls:
            self.Controls.remove(control)
            self.ControlRemoved(control)

    def _on_paint(self, event):
        # Handler for Paint and Resize events.
        self.Paint()
        self.Resize()


class FileDialog:
    # Base class for file dialogs.
    
    def __init__(self):
        self.FileName = ""
        self.FileNames = []
        self.Filter = ""
        self.FilterIndex = 1
        self.InitialDirectory = ""
        self.Title = ""
        self.DefaultExt = ""
        self.AddExtension = True
        self.CheckFileExists = True
        self.CheckPathExists = True
        self.RestoreDirectory = False
        self.ValidateNames = True
        self.ShowHelp = False
        
        # VB Events
        self.FileOk = lambda sender, e: None
        self.HelpRequest = lambda sender, hlpevent: None
        self.Disposed = lambda sender, e: None
    
    def _parse_filter(self):
        # Parse the Filter string into filetypes for Tkinter.
        if not self.Filter:
            return [("All files", "*.*")]
        # Simple parsing: "Description|*.ext|Description2|*.ext2"
        parts = self.Filter.split('|')
        filetypes = []
        for i in range(0, len(parts), 2):
            if i+1 < len(parts):
                filetypes.append((parts[i], parts[i+1]))
        return filetypes
    
    def __del__(self):
        # Destructor to trigger Disposed event.
        self.Disposed(self, None)


class OpenFileDialog(FileDialog):
    # Represents an OpenFileDialog.
    
    def __init__(self):
        super().__init__()
        self.Multiselect = False
        self.ReadOnlyChecked = False
        self.ShowReadOnly = False
        self.SafeFileName = ""
    
    def ShowDialog(self):
        # Shows the dialog and returns the selected file.
        from tkinter import filedialog
        if self.Multiselect:
            files = filedialog.askopenfilenames(
                initialdir=self.InitialDirectory or None,
                title=self.Title or None,
                filetypes=self._parse_filter(),
                defaultextension=self.DefaultExt if self.AddExtension else None
            )
            self.FileNames = list(files)
            self.FileName = self.FileNames[0] if self.FileNames else ""
            self.SafeFileName = os.path.basename(self.FileName) if self.FileName else ""
        else:
            self.FileName = filedialog.askopenfilename(
                initialdir=self.InitialDirectory or None,
                title=self.Title or None,
                filetypes=self._parse_filter(),
                defaultextension=self.DefaultExt if self.AddExtension else None
            )
            self.FileNames = [self.FileName] if self.FileName else []
            self.SafeFileName = os.path.basename(self.FileName) if self.FileName else ""
        
        # Trigger FileOk event
        self.FileOk(self, None)
        
        return self.FileName


class SaveFileDialog(FileDialog):
    # Represents a SaveFileDialog.
    
    def __init__(self):
        super().__init__()
        self.OverwritePrompt = True
        self.CreatePrompt = False
    
    def ShowDialog(self):
        # Shows the dialog and returns the selected file.
        from tkinter import filedialog
        self.FileName = filedialog.asksaveasfilename(
            initialdir=self.InitialDirectory or None,
            title=self.Title or None,
            filetypes=self._parse_filter(),
            defaultextension=self.DefaultExt if self.AddExtension else None
        )
        self.FileNames = [self.FileName] if self.FileName else []
        
        # Trigger FileOk event
        self.FileOk(self, None)
        
        return self.FileName


class PrintDialog:
    # Represents a PrintDialog with main VB.NET properties.
    
    def __init__(self):
        self.Document = None  # The PrintDocument object to be printed
        self.PrinterSettings = None  # Selected printer settings
        self.AllowCurrentPage = False  # Enables "Current Page" option
        self.AllowSelection = False  # Enables "Selection" option
        self.AllowPrintToFile = False  # Displays "Print to File" checkbox
        self.AllowSomePages = False  # Enables "Pages" option
        self.ShowHelp = False  # Displays Help button
        self.ShowNetwork = False  # Allows access to network printers
        self.UseEXDialog = True  # Uses modern dialog (default True)
        self.PrintToFile = False  # Set by the user if "Print to File" is checked
        self.PrinterName = ""  # Name of the selected printer
    
    def ShowDialog(self):
        # Shows the simulated print dialog and returns the result.
        from tkinter import messagebox
        
        # Build message based on enabled options
        options = []
        if self.AllowCurrentPage:
            options.append("Current Page")
        if self.AllowSelection:
            options.append("Selection")
        if self.AllowSomePages:
            options.append("Pages")
        if self.AllowPrintToFile:
            options.append("Print to file")

        message = "Available print options:\n" + "\n".join(options) if options else "Print document"
        if self.ShowHelp:
            message += "\n\nPress OK to print or Cancel to cancel."
        
        result = messagebox.askyesno("Print Dialog", message)
        
        # Simulate configuration based on result
        if result:
            self.PrintToFile = self.AllowPrintToFile  # Simulado
            self.PrinterName = "Default Printer"  # Simulado
        
        return result


class PictureBox(ControlBase):
    # Represents a PictureBox to display images with VB.NET properties.
    
    def __init__(self, master_form, Image=None, Left=10, Top=10, Width=100, Height=100, Name="", ImageLocation="", SizeMode="Normal", BorderStyle=None, Enabled=True, Visible=True, BackColor=None, ErrorImage=None, InitialImage=None, WaitOnLoad=False):
        super().__init__(master_form._root, Left, Top)
        
        self.Name = Name
        self.Width = Width
        self.Height = Height
        self.Image = Image
        self.ImageLocation = ImageLocation
        self.SizeMode = SizeMode  # 'Normal', 'StretchImage', 'AutoSize', 'CenterImage', 'Zoom'
        self.BorderStyle = BorderStyle  # 'None', 'FixedSingle', 'Fixed3D'
        self.Enabled = Enabled
        self.Visible = Visible
        self.BackColor = BackColor
        self.ErrorImage = ErrorImage
        self.InitialImage = InitialImage
        self.WaitOnLoad = WaitOnLoad
        
        # VB Events
        self.LoadCompleted = lambda sender, e: None
        self.LoadProgressChanged = lambda sender, e: None
        self.Error = lambda sender, e: None
        
        # Create the Tkinter widget (Label with image)
        self._tk_widget = tk.Label(self.master, image=self.Image)
        
        # Apply properties
        self._apply_properties()
        
        # Load image from ImageLocation if specified
        if self.ImageLocation:
            self._load_image_from_location()
        
        self._place_control(self.Width, self.Height)
        
        # Bind events
        self._tk_widget.bind('<Button-1>', self._on_click)
        self._tk_widget.bind('<Double-Button-1>', self._on_double_click)
        self._tk_widget.bind('<Configure>', self._on_paint)
        self._tk_widget.bind('<Enter>', self._on_mouse_enter)
        self._tk_widget.bind('<Leave>', self._on_mouse_leave)
        self._tk_widget.bind('<ButtonPress>', self._on_mouse_down)
        self._tk_widget.bind('<ButtonRelease>', self._on_mouse_up)
    
    def _apply_properties(self):
        # Applies properties to the Tkinter widget.
        config = {}
        if self.Image:
            config['image'] = self.Image
        if self.BackColor:
            config['bg'] = self.BackColor
        if self.BorderStyle == 'FixedSingle':
            config['relief'] = 'solid'
        elif self.BorderStyle == 'Fixed3D':
            config['relief'] = 'raised'
        else:
            config['relief'] = 'flat'
        if not self.Enabled:
            config['state'] = 'disabled'
        if config:
            self._tk_widget.config(**config)
        
        # SizeMode mapping (simplified)
        if self.SizeMode == 'StretchImage':
            # Tkinter Label doesn't stretch, use compound or custom
            pass  # Placeholder
        elif self.SizeMode == 'AutoSize':
            # Adjust size to image
            if self.Image:
                self.Width = self.Image.width()
                self.Height = self.Image.height()
        elif self.SizeMode == 'CenterImage':
            self._tk_widget.config(anchor='center')
        elif self.SizeMode == 'Zoom':
            # Placeholder for zoom
            pass
    
    def _load_image_from_location(self):
        # Loads the image from ImageLocation.
        try:
            # Try PIL first for better format support
            try:
                from PIL import Image, ImageTk
                use_pil = True
            except ImportError:
                use_pil = False
            
            if use_pil:
                if self.WaitOnLoad:
                    # Synchronous load
                    img = Image.open(self.ImageLocation)
                    self.Image = ImageTk.PhotoImage(img)
                    self._tk_widget.config(image=self.Image)
                    self.LoadCompleted(self, None)
                else:
                    # Asynchronous load (simplified)
                    if self.InitialImage:
                        self._tk_widget.config(image=self.InitialImage)
                    # In real implementation, use threading
                    img = Image.open(self.ImageLocation)
                    self.Image = ImageTk.PhotoImage(img)
                    self._tk_widget.config(image=self.Image)
                    self.LoadCompleted(self, None)
            else:
                # Fallback to Tkinter PhotoImage (limited formats)
                self.Image = tk.PhotoImage(file=self.ImageLocation)
                self._tk_widget.config(image=self.Image)
                self.LoadCompleted(self, None)
        except Exception as e:
            if self.ErrorImage:
                self._tk_widget.config(image=self.ErrorImage)
            self.Error(self, e)
    
    def set_Image(self, image):
        # Sets the image.
        self.Image = image
        self._tk_widget.config(image=image)
        self._apply_properties()
    
    def set_ImageLocation(self, location):
        # Sets the image location and loads it.
        self.ImageLocation = location
        self._load_image_from_location()
    
    def set_SizeMode(self, mode):
        # Sets the size mode.
        self.SizeMode = mode
        self._apply_properties()
    
    def set_BorderStyle(self, style):
        # Sets the border style.
        self.BorderStyle = style
        self._apply_properties()
    
    def set_Enabled(self, enabled):
        # Sets whether it is enabled.
        self.Enabled = enabled
        self._tk_widget.config(state='normal' if enabled else 'disabled')
    
    def set_Visible(self, visible):
        # Sets the visibility.
        self.Visible = visible
        if visible:
            self._place_control(self.Width, self.Height)
        else:
            self._tk_widget.place_forget()
    
    def _on_click(self, event):
        # Handler for Click event.
        self.Click()
    
    def _on_double_click(self, event):
        # Handler for DoubleClick event.
        self.DoubleClick()
    
    def _on_paint(self, event):
        # Handler for Paint and Resize events.
        self.Paint()
        self.Resize()


class ImageList:
    # Represents an ImageList to manage images with VB.NET properties.
    
    def __init__(self, Name="", ImageSize=(16, 16), ColorDepth=32, TransparentColor=None, ImageStream=None):
        self.Name = Name  # Unique identifier
        self.Images = {}  # Dictionary of images (key: index or name, value: PhotoImage)
        self.ImageSize = ImageSize  # (width, height) in pixels
        self.ColorDepth = ColorDepth  # Color depth (8, 16, 24, 32 bits)
        self.TransparentColor = TransparentColor  # Transparent color
        self.ImageStream = ImageStream  # For serialization (placeholder)
        self._next_index = 0  # For automatic index assignment
        
        # VB Events
        self.CollectionChanged = lambda: None
        self.Disposed = lambda sender, e: None
    
    def Add(self, image, key=None):
        # Adds an image to the list. If key is None, uses a numeric index.
        if key is None:
            key = self._next_index
            self._next_index += 1
        self.Images[key] = image
        self.CollectionChanged()
    
    def GetImage(self, key):
        # Gets an image by key (index or name).
        return self.Images.get(key, None)
    
    def Remove(self, key):
        # Removes an image by key.
        if key in self.Images:
            del self.Images[key]
            self.CollectionChanged()
    
    def Clear(self):
        # Clears all images.
        self.Images.clear()
        self._next_index = 0
        self.CollectionChanged()
    
    def Count(self):
        # Returns the number of images.
        return len(self.Images)
    
    def Dispose(self):
        # Releases the resources of the ImageList.
        self.Disposed(self, None)


class DialogResult:
    # Represents the return values of a dialog (DialogResult).
    
    OK = "OK"
    Cancel = "Cancel"
    Yes = "Yes"
    No = "No"
    Abort = "Abort"
    Retry = "Retry"
    Ignore = "Ignore"


class MessageBox:
    # Represents a MessageBox for messages with VB.NET parameters.
    
    @staticmethod
    def Show(text, caption="Message", buttons="OK", icon=None, defaultButton=None, options=None):
        # Shows a message and returns the result.
        # Parameters:
        # - text: The main message.
        # - caption: The title.
        # - buttons: 'OK', 'OKCancel', 'YesNo', 'YesNoCancel', 'RetryCancel', 'AbortRetryIgnore'
        # - icon: 'Information', 'Warning', 'Error', 'Question', 'None'
        # - defaultButton: 'Button1', 'Button2', 'Button3' (not implemented in Tkinter)
        # - options: 'RightAlign', 'RtlReading', etc. (partially supported)
        # Map icon to messagebox function
        icon_map = {
            'Information': 'info',
            'Warning': 'warning',
            'Error': 'error',
            'Question': 'question',
            'None': 'info'
        }
        msg_type = icon_map.get(icon, 'info')
        
        # Adjust text for options
        display_text = text
        if options and 'RightAlign' in options:
            # Simulate right align (placeholder)
            display_text = text  # Tkinter doesn't support easily
        
        # Map buttons to Tkinter functions
        if buttons == "OK":
            if msg_type == 'warning':
                messagebox.showwarning(caption, display_text)
            elif msg_type == 'error':
                messagebox.showerror(caption, display_text)
            else:
                messagebox.showinfo(caption, display_text)
            return DialogResult.OK
        elif buttons == "OKCancel":
            return DialogResult.OK if messagebox.askokcancel(caption, display_text) else DialogResult.Cancel
        elif buttons == "YesNo":
            if msg_type == 'question':
                return DialogResult.Yes if messagebox.askyesno(caption, display_text) else DialogResult.No
            else:
                return DialogResult.Yes if messagebox.askyesno(caption, display_text) else DialogResult.No
        elif buttons == "YesNoCancel":
            result = messagebox.askyesnocancel(caption, display_text)
            if result is True:
                return DialogResult.Yes
            elif result is False:
                return DialogResult.No
            else:
                return DialogResult.Cancel
        elif buttons == "RetryCancel":
            return DialogResult.Retry if messagebox.askretrycancel(caption, display_text) else DialogResult.Cancel
        elif buttons == "AbortRetryIgnore":
            # Tkinter no tiene AbortRetryIgnore, simular con YesNoCancel o custom
            result = messagebox.askyesnocancel(caption, f"{display_text}\n\nAbort = Yes, Retry = No, Ignore = Cancel")
            if result is True:
                return DialogResult.Abort
            elif result is False:
                return DialogResult.Retry
            else:
                return DialogResult.Ignore
        # Default
        messagebox.showinfo(caption, display_text)
        return DialogResult.OK
    

class InputBox:
    # Represents an InputBox for text input with VB.NET parameters.
    
    @staticmethod
    def Show(prompt, title="Input", defaultResponse="", xpos=None, ypos=None):
        # Shows an input dialog and returns the text.
        # Parameters:
        # - prompt: The main message.
        # - title: The title.
        # - defaultResponse: Default value in the text box.
        # - xpos: X position (not implemented in Tkinter simpledialog).
        # - ypos: Y position (not implemented in Tkinter simpledialog).
        from tkinter import simpledialog
        result = simpledialog.askstring(title, prompt, initialvalue=defaultResponse)
        return result if result is not None else ""


class MaskedFormat:
    # Class for formatting text with masks.
    
    @staticmethod
    def Format(value, mask):
           # Applies a mask to the value (simple placeholder).
        # Basic implementation, e.g., for numbers
        if mask == "9999":
            return str(value).zfill(4)
        return str(value)


class MaskedTextBox(TextBox):
    # Represents a MaskedTextBox with mask validation and VB.NET properties.
    
    def __init__(self, master_form, Mask="", Text="", Left=10, Top=80, Width=200, Name="", PromptChar='_', HidePromptOnLeave=False, PasswordChar=None, UseSystemPasswordChar=False, BeepOnError=False, CutCopyMaskFormat='IncludeLiterals', InsertKeyMode='Insert', AllowPromptAsInput=False, FormatProvider=None):
        super().__init__(master_form, Text, Left, Top, Width, Name=Name)
        
        # VB Properties
        self.Mask = Mask
        self.PromptChar = PromptChar
        self.HidePromptOnLeave = HidePromptOnLeave
        self.PasswordChar = PasswordChar
        self.UseSystemPasswordChar = UseSystemPasswordChar
        self.BeepOnError = BeepOnError
        self.CutCopyMaskFormat = CutCopyMaskFormat  # 'IncludeLiterals', 'ExcludePromptAndLiterals', etc.
        self.InsertKeyMode = InsertKeyMode  # 'Insert', 'Overwrite'
        self.AllowPromptAsInput = AllowPromptAsInput
        self.FormatProvider = FormatProvider  # Placeholder para cultura
        
        # Specific events for MaskedTextBox
        self.MaskInputRejected = lambda sender, e: None
        self.TypeValidationCompleted = lambda sender, e: None
        
        # Apply PasswordChar if specified
        if self.PasswordChar:
            self._tk_widget.config(show=self.PasswordChar)
        elif self.UseSystemPasswordChar:
            self._tk_widget.config(show='*')
        
        # Configure validation
        vcmd = (self.master.register(self._validate), '%P')
        self._tk_widget.config(validate='key', validatecommand=vcmd)
        
        # Bind focus events for HidePromptOnLeave
        self._tk_widget.bind('<FocusIn>', self._on_focus_in)
        self._tk_widget.bind('<FocusOut>', self._on_focus_out)
        
        # Inicializar display text con prompts
        self._update_display_text()
    
    def _validate(self, new_text):
        # Validates the text according to the mask.
        if not self.Mask:
            return True
        
        # Permitir PromptChar si AllowPromptAsInput
        if self.AllowPromptAsInput and new_text == self.PromptChar:
            return True
        
        # Basic mask validation implementation
        # 9: optional digit, 0: required digit, L: required letter, ?: optional letter, A: required alphanumeric, etc.
        # Simplificado para ejemplos comunes
        valid = False
        if self.Mask == "9999":  # 4 optional digits
            cleaned = new_text.replace(self.PromptChar, '')
            valid = cleaned.isdigit() and len(cleaned) <= 4
        elif self.Mask == "(999) 999-9999":  # Phone
            # Allow digits, parentheses, hyphens, spaces, and prompts
            cleaned = new_text.replace('(', '').replace(')', '').replace('-', '').replace(' ', '').replace(self.PromptChar, '')
            valid = cleaned.isdigit() and len(cleaned) <= 10
        elif self.Mask == "00/00/0000":  # Fecha
            cleaned = new_text.replace('/', '').replace(self.PromptChar, '')
            valid = cleaned.isdigit() and len(cleaned) <= 8
        else:
            # General basic validation: length does not exceed mask
            valid = len(new_text) <= len(self.Mask)
        
        if not valid:
            self.MaskInputRejected(self, None)
            if self.BeepOnError:
                winsound.Beep(800, 200)  # Beep de error
        
        return valid
    
    def _on_focus_in(self, event):
        # Handles the focus-in event.
        if self.HidePromptOnLeave:
            self._update_display_text()
    
    def _on_focus_out(self, event):
        # Handles the focus-out event.
        if self.HidePromptOnLeave:
            # Ocultar prompts
            current = self._tk_widget.get()
            cleaned = current.replace(self.PromptChar, '')
            self._tk_widget.delete(0, 'end')
            self._tk_widget.insert(0, cleaned)
        # Trigger TypeValidationCompleted if mask is completed
        if self.MaskCompleted:
            self.TypeValidationCompleted(self, None)
    
    def _update_display_text(self):
        # Updates the displayed text with prompts.
        if not self.Mask:
            return
        # Generar texto con prompts (simplificado)
        display = ''
        for char in self.Mask:
            if char in '09L?A':
                display += self.PromptChar
            else:
                display += char
        if not self._tk_widget.get():
            self._tk_widget.insert(0, display)
    
    @property
    def MaskFull(self):
        # Read-only property: True if all required and optional positions are filled.
        if not self.Mask:
            return True
        current = self._tk_widget.get()
        # Contar posiciones requeridas (0, L, A) vs opcionales (9, ?, etc.)
        required_positions = sum(1 for char in self.Mask if char in '0LA')
        filled_required = sum(1 for i, char in enumerate(self.Mask) if char in '0LA' and i < len(current) and current[i] != self.PromptChar)
        return filled_required >= required_positions
    
    @property
    def MaskCompleted(self):
        # Read-only property: True if all required positions are filled.
        if not self.Mask:
            return True
        current = self._tk_widget.get()
        required_positions = sum(1 for char in self.Mask if char in '0LA')
        filled_required = sum(1 for i, char in enumerate(self.Mask) if char in '0LA' and i < len(current) and current[i] != self.PromptChar)
        return filled_required == required_positions
    
    def get_Text(self):
        # Gets the text without prompts.
        text = self._tk_widget.get()
        return text.replace(self.PromptChar, '')
    
    def set_Text(self, new_text):
        # Sets the text and updates the display.
        self.Text = new_text
        self._tk_widget.delete(0, 'end')
        self._tk_widget.insert(0, new_text)
        self._update_display_text()


class TabPage:
    # Represents a tab page for TabControl with VB.NET properties.
    
    def __init__(self, Text="TabPage", Name="", Enabled=True, Visible=True, ImageIndex=-1, ImageKey="", ToolTipText="", UseVisualStyleBackColor=True, Padding=(3,3)):
        self.Name = Name or Text  # Use Text if Name is empty
        self.Text = Text
        self.Parent = None  # Asignado por TabControl
        self.Enabled = Enabled
        self.Visible = Visible  # Placeholder, ttk.Notebook handles visibility automatically
        self.ImageIndex = ImageIndex
        self.ImageKey = ImageKey
        self.ToolTipText = ToolTipText  # Placeholder, Tkinter no tiene tooltips nativos
        self.UseVisualStyleBackColor = UseVisualStyleBackColor  # Placeholder
        self.Padding = Padding  # (padx, pady)
        
        # Create the frame with padding
        padx, pady = self.Padding
        self._frame = tk.Frame(padx=padx, pady=pady)
        self.Controls = []

        # VB Events
        self.Enter = lambda: None
        self.Leave = lambda: None
        self.Paint = lambda: None
        self.ControlAdded = lambda control: None
        self.ControlRemoved = lambda control: None
        self.Resize = lambda: None
        self.ChangeUICues = lambda sender, e: None

        # Bind events
        self._frame.bind('<Configure>', self._on_configure)
        self._frame.bind('<FocusIn>', lambda e: self.ChangeUICues(self, e))
        self._frame.bind('<FocusOut>', lambda e: self.ChangeUICues(self, e))

    def AddControl(self, control):
        # Adds a control to the TabPage.
        self.Controls.append(control)
        control.master = self._frame
        control._place_control()
        # Apply TabPage's Enabled to the control
        if hasattr(control, 'Enabled'):
            control.Enabled = self.Enabled
            if hasattr(control, '_tk_widget'):
                control._tk_widget.config(state='normal' if self.Enabled else 'disabled')
        self.ControlAdded(control)

    def _on_configure(self, event):
        # Handler for Paint and Resize events.
        self.Paint()
        self.Resize()

    def RemoveControl(self, control):
        # Removes a control from the TabPage.
        if control in self.Controls:
            self.Controls.remove(control)
            self.ControlRemoved(control)


class TabControl(ControlBase):
    # Represents a TabControl with tabs.
    
    def __init__(self, master_form, Left=10, Top=10, Width=300, Height=200, Name="", TabPages=None, SelectedIndex=0, ImageList=None, Appearance="Normal", Alignment="Top", Multiline=False, SizeMode="Normal", Enabled=True, Visible=True, Padding=(0,0), HotTrack=False):
        # Resolve master widget
        master_widget = getattr(master_form, '_root', getattr(master_form, '_tk_widget', getattr(master_form, '_frame', master_form)))
        super().__init__(master_widget, Left, Top)
        
        self.Width = Width
        self.Height = Height
        
        # VB Properties
        self.Name = Name
        self.Enabled = Enabled
        self.Visible = Visible
        self.TabPages = TabPages or []
        self.SelectedIndex = SelectedIndex
        self.ImageList = ImageList
        self.Appearance = Appearance  # 'Normal', 'Buttons', 'FlatButtons' - placeholder
        self.Alignment = Alignment  # 'Top', 'Bottom', 'Left', 'Right'
        self.Multiline = Multiline
        self.SizeMode = SizeMode  # 'Normal', 'Fixed', 'FillToRight' - placeholder
        self.Padding = Padding  # (padx, pady)
        self.HotTrack = HotTrack  # Placeholder
        
        # VB Events
        self.SelectedIndexChanged = lambda: None
        self.Selecting = lambda sender, e: None
        self.Selected = lambda sender, e: None
        self.Deselecting = lambda sender, e: None
        self.Deselected = lambda sender, e: None
        self.DrawItem = lambda sender, e: None
        self.ControlAdded = lambda control: None
        self.ControlRemoved = lambda control: None
        
        # Create the Tkinter widget (Notebook)
        self._tk_widget = ttk.Notebook(self.master)
        
        # Apply configurations
        config = {}
        padx, pady = self.Padding
        config['padding'] = (padx, pady)
        if config:
            self._tk_widget.config(**config)
        
        self._place_control(self.Width, self.Height)
        
        # Track selected tab for events
        self._last_selected = self.SelectedIndex
        self._tk_widget.bind('<<NotebookTabChanged>>', self._on_tab_changed)
        
        # Add initial TabPages if they exist
        for tab in self.TabPages:
            self.AddTab(tab)
        
        # Establecer SelectedIndex inicial
        if self.TabPages and 0 <= self.SelectedIndex < len(self.TabPages):
            self._tk_widget.select(self.SelectedIndex)

    def AddTab(self, tab_page):
        # Adds a TabPage to the TabControl.
        self.TabPages.append(tab_page)
        tab_page.Parent = self  # Asignar Parent
        self._tk_widget.add(tab_page._frame, text=tab_page.Text)
        # Apply image if ImageList and ImageIndex/ImageKey
        if self.ImageList and hasattr(tab_page, 'ImageIndex') and tab_page.ImageIndex >= 0:
            # Placeholder: ttk.Notebook does not easily support images, use compound or custom
            pass
        self.ControlAdded(tab_page)

    def RemoveTab(self, tab_page):
        # Removes a TabPage from the TabControl.
        if tab_page in self.TabPages:
            index = self.TabPages.index(tab_page)
            self.TabPages.remove(tab_page)
            self._tk_widget.forget(tab_page._frame)
            self.ControlRemoved(tab_page)
            # If it was selected, select another or none
            if self.get_SelectedIndex() == index:
                if self.TabPages:
                    self.set_SelectedIndex(0)
                else:
                    self._last_selected = -1

    @property
    def SelectedTab(self):
        # Gets the selected TabPage.
        if self.TabPages and 0 <= self.SelectedIndex < len(self.TabPages):
            return self.TabPages[self.SelectedIndex]
        return None

    @SelectedTab.setter
    def SelectedTab(self, tab_page):
            # Sets the selected TabPage.
        if tab_page in self.TabPages:
            old_index = self.get_SelectedIndex()
            new_index = self.TabPages.index(tab_page)
            if old_index != new_index:
                # Trigger Selecting and Deselecting
                self.Selecting(self, {'TabPage': tab_page, 'TabPageIndex': new_index, 'Cancel': False})
                if old_index >= 0:
                    self.Deselecting(self, {'TabPage': self.TabPages[old_index], 'TabPageIndex': old_index, 'Cancel': False})
                # Proceed
                if old_index >= 0:
                    self.TabPages[old_index].Leave()
                    self.Deselected(self, {'TabPage': self.TabPages[old_index], 'TabPageIndex': old_index})
                self.SelectedIndex = new_index
                self._tk_widget.select(new_index)
                tab_page.Enter()
                self.Selected(self, {'TabPage': tab_page, 'TabPageIndex': new_index})
                self.SelectedIndexChanged()
                self._last_selected = new_index

    def get_SelectedIndex(self):
            # Gets the index of the selected tab.
        try:
            return self._tk_widget.index(self._tk_widget.select())
        except:
            return -1

    def set_SelectedIndex(self, index):
            # Sets the index of the selected tab.
        if 0 <= index < len(self.TabPages):
            old_index = self.get_SelectedIndex()
            if old_index != index:
                # Trigger Selecting and Deselecting
                self.Selecting(self, {'TabPage': self.TabPages[index], 'TabPageIndex': index, 'Cancel': False})
                if old_index >= 0:
                    self.Deselecting(self, {'TabPage': self.TabPages[old_index], 'TabPageIndex': old_index, 'Cancel': False})
                # Proceed
                if old_index >= 0:
                    self.TabPages[old_index].Leave()
                    self.Deselected(self, {'TabPage': self.TabPages[old_index], 'TabPageIndex': old_index})
                self.SelectedIndex = index
                self._tk_widget.select(index)
                self.TabPages[index].Enter()
                self.Selected(self, {'TabPage': self.TabPages[index], 'TabPageIndex': index})
                self.SelectedIndexChanged()
                self._last_selected = index

    def _on_tab_changed(self, event):
        """Handler for tab selection changes."""
        new_index = self.get_SelectedIndex()
        if new_index != self._last_selected:
            # Trigger Selecting and Deselecting
            if new_index >= 0:
                self.Selecting(self, {'TabPage': self.TabPages[new_index], 'TabPageIndex': new_index, 'Cancel': False})
            if self._last_selected >= 0:
                self.Deselecting(self, {'TabPage': self.TabPages[self._last_selected], 'TabPageIndex': self._last_selected, 'Cancel': False})
            # Proceed
            if self._last_selected >= 0:
                self.TabPages[self._last_selected].Leave()
                self.Deselected(self, {'TabPage': self.TabPages[self._last_selected], 'TabPageIndex': self._last_selected})
            self._last_selected = new_index
            if new_index >= 0:
                self.TabPages[new_index].Enter()
                self.Selected(self, {'TabPage': self.TabPages[new_index], 'TabPageIndex': new_index})
            self.SelectedIndexChanged()


class RadioButton(ControlBase):
    # Represents a RadioButton.
    
    def __init__(self, master_form, Text="Radio", Group=None, Left=10, Top=140, Name="", Checked=False, Enabled=True, Visible=True, Font=None, ForeColor=None, BackColor=None, TextAlign="w", Appearance="Normal"):
        # Resolve master widget
        master_widget = getattr(master_form, '_root', getattr(master_form, '_tk_widget', getattr(master_form, '_frame', master_form)))
        super().__init__(master_widget, Left, Top)
        
        # VB Properties
        self.Name = Name
        self.Enabled = Enabled
        self.Visible = Visible
        self.Text = Text
        self.Group = Group or tk.StringVar()
        self.Checked = Checked
        self.Font = Font
        self.ForeColor = ForeColor
        self.BackColor = BackColor
        self.TextAlign = TextAlign  # 'w' (left), 'e' (right), etc.
        self.Appearance = Appearance  # 'Normal', 'Button'
        
        # VB Events
        self.CheckedChanged = lambda: None
        
        # Create the Tkinter widget
        self._tk_widget = tk.Radiobutton(self.master, text=self.Text, variable=self.Group, value=self.Text)
        
        # Apply configurations
        config = {}
        if self.Font:
            config['font'] = self.Font
        if self.ForeColor:
            config['fg'] = self.ForeColor
        if self.BackColor:
            config['bg'] = self.BackColor
        if self.TextAlign:
            config['anchor'] = self.TextAlign
       
        if self.Appearance == "Button":
            config['indicatoron'] = 0
        if not self.Enabled:
            config['state'] = 'disabled'
        if config:
            self._tk_widget.config(**config)
        
        self._place_control()
        
        # Bind common events
        self._bind_common_events()
        
        # Establecer Checked inicial
        if self.Checked:
            self.Group.set(self.Text)
        
        # Bind CheckedChanged
        self.Group.trace('w', self._on_checked_changed)

    def get_Checked(self):
        # Checks if it is selected.
        return self.Group.get() == self.Text

    def set_Checked(self, value):
        # Sets whether it is selected.
        self.Checked = value
        if value:
            self.Group.set(self.Text)

    def _on_checked_changed(self, *args):
        # Handler for CheckedChanged event.
        old_checked = self.Checked
        self.Checked = self.get_Checked()
        if old_checked != self.Checked:
            self.CheckedChanged()


class ProgressBar(ControlBase):
    # Represents a ProgressBar.
    
    def __init__(self, master_form, Minimum=0, Maximum=100, Value=0, Left=10, Top=10, Width=200, Height=20, Style="Blocks"):
        super().__init__(master_form._root, Left, Top)
        
        self.Minimum = Minimum
        self.Maximum = Maximum
        self.Value = Value
        self.Style = Style  # 'Blocks', 'Continuous', 'Marquee'
        
        # VB Events
        self.ValueChanged = lambda: None
        self.StyleChanged = lambda: None
        
        # Determinar mode basado en Style
        mode = 'indeterminate' if self.Style == 'Marquee' else 'determinate'
        
        # Create the Tkinter widget
        self._tk_widget = ttk.Progressbar(self.master, orient='horizontal', length=Width, mode=mode)
        self._tk_widget['maximum'] = self.Maximum
        self._tk_widget['value'] = self.Value
        self._place_control(Width, Height)
        
        # Bind common events
        self._bind_common_events()
        
        # Start animation if Marquee
        if self.Style == 'Marquee':
            self._tk_widget.start()

    def set_Value(self, value):
        # Sets the value of the bar.
        self.Value = value
        self._tk_widget['value'] = value
        self.ValueChanged()

    def set_Style(self, style):
        # Sets the style of the bar.
        self.Style = style
        mode = 'indeterminate' if style == 'Marquee' else 'determinate'
        self._tk_widget.config(mode=mode)
        if style == 'Marquee':
            self._tk_widget.start()
        else:
            self._tk_widget.stop()
        self.StyleChanged()


class ListViewItem:
    # Represents an item in a ListView.
    
    def __init__(self, Text="", SubItems=None, ImageIndex=-1, ImageKey="", Tag=None):
        self.Text = Text
        self.SubItems = SubItems or []  # List of subitems for additional columns
        self.ImageIndex = ImageIndex
        self.ImageKey = ImageKey
        self.Tag = Tag  # Custom object


class ColumnHeader:
    # Represents a column header in a ListView.
    
    def __init__(self, Text="", Width=100, TextAlign="left", ImageIndex=-1):
        self.Text = Text
        self.Width = Width
        self.TextAlign = TextAlign  # 'left', 'center', 'right'
        self.ImageIndex = ImageIndex


class ListView(ControlBase):
    # Represents a ListView with VB.NET properties.
    
    def __init__(self, master_form, Columns=None, Left=10, Top=280, Width=300, Height=150, Name="", Items=None, View="Details", SmallImageList=None, LargeImageList=None, FullRowSelect=True, MultiSelect=True, CheckBoxes=False, GridLines=False, HeaderStyle="Clickable", Sorting="None", Enabled=True, Visible=True):
        super().__init__(master_form._root, Left, Top, Name=Name, Enabled=Enabled, Visible=Visible)
        
        self.Width = Width
        self.Height = Height
        self.Items = Items or []  # Lista de ListViewItem
        self.View = View  # 'LargeIcon', 'SmallIcon', 'List', 'Details', 'Tile'
        self.Columns = Columns or [ColumnHeader("Column1")]
        self.SmallImageList = SmallImageList
        self.LargeImageList = LargeImageList
        self.FullRowSelect = FullRowSelect
        self.MultiSelect = MultiSelect
        self.CheckBoxes = CheckBoxes
        self.GridLines = GridLines
        self.HeaderStyle = HeaderStyle  # 'Clickable', 'Nonclickable', 'None'
        self.Sorting = Sorting  # 'Ascending', 'Descending', 'None'
        
        # VB Events
        self.SelectedIndexChanged = lambda: None
        self.ItemSelectionChanged = lambda sender, e: None
        self.DoubleClick = lambda: None
        self.Click = lambda: None
        self.ItemCheck = lambda sender, e: None
        self.AfterCheck = lambda sender, e: None
        self.ColumnClick = lambda sender, e: None
        self.MouseClick = lambda sender, e: None
        self.Enter = lambda: None
        self.Leave = lambda: None
        self.KeyDown = lambda sender, e: None
        self.KeyPress = lambda sender, e: None
        self.DrawItem = lambda sender, e: None
        self.DrawSubItem = lambda sender, e: None
        self.DrawColumnHeader = lambda sender, e: None
        show = 'headings' if self.View == 'Details' else 'tree'
        selectmode = 'extended' if self.MultiSelect else 'browse'
        self._tk_widget = ttk.Treeview(self.master, columns=[col.Text for col in self.Columns], show=show, selectmode=selectmode, height=10)
        
        # Configurar columnas
        for i, col in enumerate(self.Columns):
            self._tk_widget.heading(i, text=col.Text)
            self._tk_widget.column(i, width=col.Width, anchor=col.TextAlign)
        
        # Apply styles
        style = ttk.Style()
        if self.GridLines:
            style.configure("Treeview", rowheight=25)  # Placeholder for gridlines
        if self.HeaderStyle == 'None':
            self._tk_widget.config(show='')  # Hide headings
        elif self.HeaderStyle == 'Nonclickable':
            # Placeholder: disable clicking
            pass
        
        self._place_control(self.Width, self.Height)
        
        # Bind events
        self._bind_common_events()
        self._tk_widget.bind('<<TreeviewSelect>>', self._on_selection_changed)
        # For ColumnClick
        for i in range(len(self.Columns)):
            self._tk_widget.heading(i, command=lambda col=i: self._on_column_click(col))
        # For KeyDown/KeyPress
        self._tk_widget.bind('<Key>', self._on_key_down)
        self._tk_widget.bind('<KeyPress>', self._on_key_press)
        # For ItemCheck/AfterCheck, placeholder if CheckBoxes
        if self.CheckBoxes:
            # Placeholder: Treeview doesn't have checkboxes, need custom implementation
            pass
        
        # Add initial items
        for item in self.Items:
            self.AddItem(item)

    @property
    def SelectedItems(self):
            # Gets the collection of selected items.
        selections = self._tk_widget.selection()
        selected_items = []
        for sel in selections:
            item_data = self._tk_widget.item(sel)
            # Map back to ListViewItem (simplified)
            text = item_data.get('text', '')
            values = item_data.get('values', [])
            selected_items.append(ListViewItem(Text=text, SubItems=values))
        return selected_items

    def AddItem(self, item):
            # Adds a ListViewItem to the ListView.
        if isinstance(item, ListViewItem):
            values = [item.Text] + item.SubItems
            self._tk_widget.insert('', 'end', text=item.Text, values=item.SubItems)
            self.Items.append(item)
        else:
            raise TypeError("AddItem expects a ListViewItem object")

    def GetSelectedItem(self):
            # Gets the first selected item.
        selection = self._tk_widget.selection()
        if selection:
            item_data = self._tk_widget.item(selection[0])
            return ListViewItem(Text=item_data.get('text', ''), SubItems=item_data.get('values', []))
        return None

    def set_View(self, view):
            # Sets the view of the ListView.
        self.View = view
        # Reconfigurar widget (placeholder: limited support)
        show = 'headings' if view == 'Details' else 'tree'
        self._tk_widget.config(show=show)

    def set_Sorting(self, sorting):
            # Sets the sorting type.
        self.Sorting = sorting
        # Implement sorting logic (placeholder)
        if sorting != 'None':
            # Sort items based on Text or first column
            reverse = sorting == 'Descending'
            self.Items.sort(key=lambda x: x.Text, reverse=reverse)
            # Rebuild treeview
            for i in self._tk_widget.get_children():
                self._tk_widget.delete(i)
            for item in self.Items:
                self.AddItem(item)

    def _on_selection_changed(self, event):
           # Handler for SelectedIndexChanged and ItemSelectionChanged.
        self.SelectedIndexChanged()
        selected = self._tk_widget.selection()
        for item in selected:
            self.ItemSelectionChanged(self, {'Item': item, 'Selected': True})

    def _on_column_click(self, column):
           # Handler for ColumnClick.
        self.ColumnClick(self, {'Column': column})

    def _on_key_down(self, event):
           # Handler for KeyDown.
        self.KeyDown(self, {'KeyCode': event.keysym, 'Modifiers': event.state})

    def _on_key_press(self, event):
           # Handler for KeyPress.
        self.KeyPress(self, {'KeyChar': event.char})

class DataGridViewColumn:
    # Represents a column in DataGridView.
    
    def __init__(self, Name="", HeaderText="", DataPropertyName="", Width=100, Visible=True, ReadOnly=False):
        self.Name = Name
        self.HeaderText = HeaderText
        self.DataPropertyName = DataPropertyName
        self.Width = Width
        self.Visible = Visible
        self.ReadOnly = ReadOnly
        self.DisplayIndex = 0
        self.DefaultCellStyle = {}
        self.SortMode = "Automatic"
        self.ValueType = str
        self.CellTemplate = None
        self.Frozen = False
        self.AutoSizeMode = "None"


class DataGridView(ControlBase):
    # Represents a DataGridView with VB.NET properties.
    
    def __init__(self, master_form, Left=10, Top=10, Width=400, Height=200, Name="", DataSource=None, Columns=None, AllowUserToAddRows=False, AllowUserToDeleteRows=False, AllowUserToResizeColumns=True, ReadOnly=False, SelectionMode="FullRowSelect", DefaultCellStyle=None, AutoGenerateColumns=True, AlternatingRowsDefaultCellStyle=None, RowHeadersVisible=True, ColumnHeadersVisible=True, Dock=None, Anchor=None):
        super().__init__(master_form._root, Left, Top)
        self.Name = Name
        
        self.Width = Width
        self.Height = Height
        self.DataSource = DataSource
        # Convert columns if they are strings
        self.Columns = []
        if Columns:
            for col in Columns:
                if isinstance(col, str):
                    self.Columns.append(DataGridViewColumn(Name=col, HeaderText=col, DataPropertyName=col))
                else:
                    self.Columns.append(col)
        self.AllowUserToAddRows = AllowUserToAddRows
        self.AllowUserToDeleteRows = AllowUserToDeleteRows
        self.AllowUserToResizeColumns = AllowUserToResizeColumns
        self.ReadOnly = ReadOnly
        self.SelectionMode = SelectionMode  # 'FullRowSelect', 'CellSelect', etc.
        self.DefaultCellStyle = DefaultCellStyle or {}
        self.AutoGenerateColumns = AutoGenerateColumns
        self.AlternatingRowsDefaultCellStyle = AlternatingRowsDefaultCellStyle or {}
        self.RowHeadersVisible = RowHeadersVisible
        self.ColumnHeadersVisible = ColumnHeadersVisible
        self.Dock = Dock
        self.Anchor = Anchor
        
        self.Rows = []
        
        # VB Events
        self.ColumnHeaderMouseClick = lambda sender, e: None
        self.ColumnStateChanged = lambda sender, e: None
        self.ColumnWidthChanged = lambda sender, e: None
        self.ColumnDisplayIndexChanged = lambda sender, e: None
        self.ColumnAdded = lambda sender, e: None
        self.ColumnRemoved = lambda sender, e: None
        show = 'headings' if self.ColumnHeadersVisible else 'tree'
        selectmode = 'browse' if self.SelectionMode == 'FullRowSelect' else 'extended'
        self._tk_widget = ttk.Treeview(self.master, show=show, selectmode=selectmode, height=10)
        
        # Configure columns
        if self.DataSource and self.AutoGenerateColumns and not self.Columns:
            self._generate_columns_from_datasource()
        
        self._apply_columns()
        
        # Populate from DataSource
        if self.DataSource:
            self._populate_from_datasource()
        
        self._place_control(self.Width, self.Height)
        
        # Apply styles (placeholders)
        self._apply_styles()
        
        # Bind events
        self._bind_common_events()
        # For ColumnHeaderMouseClick, placeholder: Treeview headings not easily bindable
        # For other events, placeholders
    
    def _generate_columns_from_datasource(self):
           # Automatically generates columns from DataSource.
        if isinstance(self.DataSource, list) and self.DataSource:
            sample = self.DataSource[0]
            if isinstance(sample, dict):
                for key in sample.keys():
                    self.Columns.append(DataGridViewColumn(Name=key, HeaderText=key, DataPropertyName=key))
    
    def _apply_columns(self):
           # Applies columns to the Treeview.
        col_ids = [col.Name for col in self.Columns if col.Visible]
        self._tk_widget.config(columns=col_ids)
        for col in self.Columns:
            if col.Visible:
                self._tk_widget.heading(col.Name, text=col.HeaderText)
                self._tk_widget.column(col.Name, width=col.Width)
    
    def _populate_from_datasource(self):
           # Populates rows from DataSource.
        for item in self.DataSource:
            if isinstance(item, dict):
                values = [item.get(col.DataPropertyName, '') for col in self.Columns if col.Visible]
                self._tk_widget.insert('', 'end', values=values)
                self.Rows.append(item)
    
    def _apply_styles(self):
           # Applies styles (placeholder).
        # Placeholder for DefaultCellStyle, AlternatingRowsDefaultCellStyle
        pass
    
    def AddRow(self, values):
           # Adds a row to the DataGridView.
        if isinstance(values, dict):
            self._tk_widget.insert('', 'end', values=[values.get(col.DataPropertyName, '') for col in self.Columns if col.Visible])
            self.Rows.append(values)
        elif isinstance(values, (list, tuple)):
            # Create a dict for internal storage based on column DataPropertyNames
            row_dict = {}
            visible_cols = [col for col in self.Columns if col.Visible]
            for i, val in enumerate(values):
                if i < len(visible_cols):
                    row_dict[visible_cols[i].DataPropertyName] = val
            
            self._tk_widget.insert('', 'end', values=values)
            self.Rows.append(row_dict)
        else:
            raise TypeError("AddRow expects a dict or list/tuple")
    
    def set_DataSource(self, datasource):
           # Sets the data source and updates the view.
        self.DataSource = datasource
        # Clear and repopulate
        for i in self._tk_widget.get_children():
            self._tk_widget.delete(i)
        self.Rows = []
        if self.AutoGenerateColumns and not self.Columns:
            self._generate_columns_from_datasource()
        self._apply_columns()
        if datasource:
            self._populate_from_datasource()


class TreeNode:
    # Represents a node in a TreeView.
    
    def __init__(self, Text="", ImageIndex=-1, SelectedImageIndex=-1, Tag=None, Nodes=None):
        self.Text = Text
        self.ImageIndex = ImageIndex
        self.SelectedImageIndex = SelectedImageIndex
        self.Tag = Tag
        self.Nodes = Nodes or []  # List of child TreeNodes
        self.Parent = None  # Assigned by TreeView
        self.TreeView = None  # Reference to TreeView
    
    @property
    def FullPath(self):
        # Gets the full path of the node.
        path = [self.Text]
        current = self.Parent
        while current:
            path.insert(0, current.Text)
            current = current.Parent
        return self.TreeView.PathSeparator.join(path) if self.TreeView else self.Text


class TreeView(ControlBase):
    # Represents a TreeView with VB.NET properties.
    
    def __init__(self, master_form, Left=10, Top=10, Width=200, Height=200, Name="", Nodes=None, ImageList=None, ImageIndex=-1, SelectedImageIndex=-1, FullRowSelect=False, CheckBoxes=False, ShowLines=True, ShowPlusMinus=True, ShowRootLines=True, PathSeparator="\\", LabelEdit=False, Font=None, ForeColor=None, BackColor=None):
        super().__init__(master_form._root, Left, Top)
        
        self.Name = Name
        
        self.Width = Width
        self.Height = Height
        self.Nodes = Nodes or []  # List of root TreeNodes
        self.ImageList = ImageList
        self.ImageIndex = ImageIndex
        self.SelectedImageIndex = SelectedImageIndex
        self.FullRowSelect = FullRowSelect
        self.CheckBoxes = CheckBoxes
        self.ShowLines = ShowLines
        self.ShowPlusMinus = ShowPlusMinus
        self.ShowRootLines = ShowRootLines
        self.PathSeparator = PathSeparator
        self.LabelEdit = LabelEdit
        self.Font = Font
        self.ForeColor = ForeColor
        self.BackColor = BackColor
        
        # VB Events
        self.AfterSelect = lambda sender, e: None
        self.BeforeSelect = lambda sender, e: None
        self.AfterCheck = lambda sender, e: None
        self.BeforeCheck = lambda sender, e: None
        self.AfterExpand = lambda sender, e: None
        self.BeforeExpand = lambda sender, e: None
        self.AfterCollapse = lambda sender, e: None
        self.BeforeCollapse = lambda sender, e: None
        self.NodeMouseClick = lambda sender, e: None
        self.NodeMouseDoubleClick = lambda sender, e: None
        self.AfterLabelEdit = lambda sender, e: None
        self.BeforeLabelEdit = lambda sender, e: None
        
        # Create the Tkinter widget (Treeview)
        self._tk_widget = ttk.Treeview(self.master, show='tree')
        
        # Apply configurations
        style = ttk.Style()
        if self.ShowLines:
            # Placeholder: ttk.Treeview shows lines by default
            pass
        if not self.ShowPlusMinus:
            # Placeholder: hide expanders
            pass
        if self.CheckBoxes:
            # Placeholder: add checkboxes (requires custom)
            pass
        if self.FullRowSelect:
            # Placeholder: full row select
            pass
        if self.Font:
            style.configure('Treeview', font=self.Font)
        if self.ForeColor:
            style.configure('Treeview', foreground=self.ForeColor)
        if self.BackColor:
            style.configure('Treeview', background=self.BackColor)
        
        self._place_control(Width, Height)
        
        # Bind events
        self._tk_widget.bind('<<TreeviewSelect>>', self._on_after_select)
        self._tk_widget.bind('<<TreeviewOpen>>', self._on_after_expand)
        self._tk_widget.bind('<<TreeviewClose>>', self._on_after_collapse)
        self._tk_widget.bind('<Button-1>', self._on_node_mouse_click)
        self._tk_widget.bind('<Double-1>', self._on_node_mouse_double_click)
        # For BeforeSelect, BeforeExpand, BeforeCollapse, BeforeCheck, BeforeLabelEdit: placeholders, Tkinter doesn't support before events directly
        # For AfterCheck, AfterLabelEdit: placeholders, Treeview doesn't have built-in checkboxes or label editing
        
        # Add initial nodes
        for node in self.Nodes:
            self.AddNode(node)
    
    @property
    def SelectedNode(self):
        # Gets the selected node.
        selection = self._tk_widget.selection()
        if selection:
            # Map back to TreeNode (simplified)
            item_text = self._tk_widget.item(selection[0], 'text')
            # Find in Nodes (placeholder)
            return TreeNode(Text=item_text)
        return None
    
    def AddNode(self, node, parent=''):
        # Adds a TreeNode to the TreeView.
        if isinstance(node, TreeNode):
            item_id = self._tk_widget.insert(parent, 'end', text=node.Text)
            node.TreeView = self
            if parent:
                parent_node = self._find_node_by_id(parent)
                if parent_node:
                    parent_node.Nodes.append(node)
                    node.Parent = parent_node
            else:
                self.Nodes.append(node)
            # Recursively add children
            for child in node.Nodes:
                self.AddNode(child, item_id)
            return item_id
        else:
            raise TypeError("AddNode expects a TreeNode object")
    
    def _on_after_select(self, event):
           # Handler for AfterSelect event.
        selected = self._tk_widget.selection()
        if selected:
            node = self._find_node_by_id(selected[0])
            self.AfterSelect(self, {'Node': node, 'Action': 'Unknown'})
    
    def _on_after_expand(self, event):
           # Handler for AfterExpand event.
        item = self._tk_widget.focus()
        if item:
            node = self._find_node_by_id(item)
            self.AfterExpand(self, {'Node': node})
    
    def _on_after_collapse(self, event):
           # Handler for AfterCollapse event.
        item = self._tk_widget.focus()
        if item:
            node = self._find_node_by_id(item)
            self.AfterCollapse(self, {'Node': node})
    
    def _on_node_mouse_click(self, event):
           # Handler for NodeMouseClick event.
        item = self._tk_widget.identify_row(event.y)
        if item:
            node = self._find_node_by_id(item)
            self.NodeMouseClick(self, {'Node': node, 'Button': event.num, 'X': event.x, 'Y': event.y})
    
    def _on_node_mouse_double_click(self, event):
           # Handler for NodeMouseDoubleClick event.
        item = self._tk_widget.identify_row(event.y)
        if item:
            node = self._find_node_by_id(item)
            self.NodeMouseDoubleClick(self, {'Node': node, 'Button': event.num, 'X': event.x, 'Y': event.y})
    
    def _find_node_by_id(self, item_id):
        # Finds the TreeNode by item_id (placeholder).
        # Simplified: not implemented fully
        return None


class MonthCalendar(ControlBase):
    # Represents a MonthCalendar with VB.NET properties.
    
    def __init__(self, master_form, Left=10, Top=10, Width=200, Height=200, Name="", SelectionRange=None, SelectionStart=None, SelectionEnd=None, MaxSelectionCount=7, MinDate=None, MaxDate=None, TodayDate=None, ShowToday=True, ShowTodayCircle=True, ShowWeekNumbers=False, CalendarDimensions=(1,1), FirstDayOfWeek="Sunday", BoldedDates=None, AnnuallyBoldedDates=None, MonthlyBoldedDates=None):
        super().__init__(master_form._root, Left, Top)
        
        self.Name = Name
        
        self.Width = Width
        self.Height = Height
        self.SelectionRange = SelectionRange or (SelectionStart, SelectionEnd)
        self.SelectionStart = SelectionStart
        self.SelectionEnd = SelectionEnd
        self.MaxSelectionCount = MaxSelectionCount
        self.MinDate = MinDate
        self.MaxDate = MaxDate
        self.TodayDate = TodayDate or str(date.today())
        self.ShowToday = ShowToday
        self.ShowTodayCircle = ShowTodayCircle
        self.ShowWeekNumbers = ShowWeekNumbers
        self.CalendarDimensions = CalendarDimensions
        self.FirstDayOfWeek = FirstDayOfWeek
        self.BoldedDates = BoldedDates or []
        self.AnnuallyBoldedDates = AnnuallyBoldedDates or []
        self.MonthlyBoldedDates = MonthlyBoldedDates or []
        
        # VB Events
        self.DateChanged = lambda sender, e: None
        self.DateSelected = lambda sender, e: None
        self.DayHeaderClick = lambda sender, e: None
        self.MouseUp = lambda sender, e: None
        self.RightToLeftLayoutChanged = lambda sender, e: None
        self.DoubleClick = lambda: None
        self.Paint = lambda: None
        self.BoldedDatesChanged = lambda sender, e: None
        
        # Placeholder: use tkcalendar if available, else Label
        try:
            from tkcalendar import Calendar
            self._tk_widget = Calendar(self.master, selectmode='day', year=int(self.TodayDate[:4]), month=int(self.TodayDate[5:7]), day=int(self.TodayDate[8:]))
        except ImportError:
            self._tk_widget = tk.Label(self.master, text="MonthCalendar Placeholder\nInstall tkcalendar for full functionality")
        
        self._place_control(Width, Height)
        
        # Bind events
        if hasattr(self._tk_widget, 'bind'):
            self._tk_widget.bind('<<CalendarSelected>>', self._on_date_changed)
            self._tk_widget.bind('<ButtonRelease-1>', self._on_mouse_up)
            self._tk_widget.bind('<Double-1>', self._on_double_click)
            # For DayHeaderClick, RightToLeftLayoutChanged, Paint, BoldedDatesChanged: placeholders
    
    def _on_date_changed(self, event):
        # Handler for DateChanged and DateSelected events.
        selected_date = self._tk_widget.get_date()
        self.DateChanged(self, {'Start': selected_date, 'End': selected_date})
        self.DateSelected(self, {'Start': selected_date, 'End': selected_date})
    
    def _on_mouse_up(self, event):
        # Handler for MouseUp event.
        self.MouseUp(self, {'Button': event.num, 'X': event.x, 'Y': event.y})
    
    def _on_double_click(self, event):
        # Handler for DoubleClick event.
        self.DoubleClick()


class DateTimePicker(ControlBase):
    # Represents a DateTimePicker with VB.NET properties.
    
    def __init__(self, master_form, Left=10, Top=10, Width=150, Height=25, Name="", Value=None, Format="Long", CustomFormat="", MinDate=None, MaxDate=None, ShowUpDown=False, ShowCheckBox=False, CalendarForeColor=None, TitleBackColor=None):
        super().__init__(master_form._root, Left, Top)
        
        self.Name = Name
        
        self.Width = Width
        self.Height = Height
        self._value = Value or datetime.now()
        self._format = Format
        self._custom_format = CustomFormat
        self.MinDate = MinDate
        self.MaxDate = MaxDate
        self.ShowUpDown = ShowUpDown
        self.ShowCheckBox = ShowCheckBox
        self.CalendarForeColor = CalendarForeColor
        self.TitleBackColor = TitleBackColor
        
        # VB Events
        self.ValueChanged = lambda sender, e: None
        self.FormatChanged = lambda sender, e: None
        self.DropDown = lambda sender, e: None
        self.CloseUp = lambda sender, e: None
        self.CheckedChanged = lambda sender, e: None
        
        # Placeholder: use Entry with button for calendar
        self._frame = tk.Frame(self.master)
        self._entry = tk.Entry(self._frame, width=Width//10)
        self._button = tk.Button(self._frame, text="...", command=self._open_calendar)
        self._entry.pack(side='left')
        self._button.pack(side='left')
        self._tk_widget = self._frame
        
        # Set initial value
        self._update_display()
        
        self._place_control(Width, Height)
        
        # Bind events
        self._button.bind('<Button-1>', self._on_drop_down)
        # For CloseUp, trigger after _open_calendar
        # For CheckedChanged, placeholder if ShowCheckBox
    
    def _update_display(self):
        # Updates the display according to Format.
        if self._format == "Long":
            display = self._value.strftime("%A, %B %d, %Y")
        elif self._format == "Short":
            display = self._value.strftime("%m/%d/%Y")
        elif self._format == "Time":
            display = self._value.strftime("%I:%M %p")
        elif self._format == "Custom" and self._custom_format:
            display = self._value.strftime(self._custom_format)
        else:
            display = str(self._value)
        self._entry.delete(0, 'end')
        self._entry.insert(0, display)
    
    def _open_calendar(self):
        # Opens a calendar to select a date (simple placeholder).
        # Placeholder: simple date selection
        from tkinter import simpledialog
        date_str = simpledialog.askstring("Select Date", "Enter date (YYYY-MM-DD):", initialvalue=self._value.strftime("%Y-%m-%d"))
        if date_str:
            try:
                old_value = self._value
                self._value = datetime.strptime(date_str, "%Y-%m-%d")
                self._update_display()
                if old_value != self._value:
                    self.ValueChanged(self, {'OldValue': old_value, 'NewValue': self._value})
                self.CloseUp(self, {})
            except ValueError:
                pass
        else:
            self.CloseUp(self, {})
    
    def _on_drop_down(self, event):
           # Handler for DropDown event.
        self.DropDown(self, {})
    
    @property
    def Value(self):
        return self._value
    
    @Value.setter
    def Value(self, value):
        old_value = getattr(self, '_value', None)
        self._value = value
        self._update_display()
        if old_value != value:
            self.ValueChanged(self, {'OldValue': old_value, 'NewValue': value})
    
    @property
    def Format(self):
        return self._format
    
    @Format.setter
    def Format(self, value):
        old_format = getattr(self, '_format', None)
        self._format = value
        self._update_display()
        if old_format != value:
            self.FormatChanged(self, {'OldFormat': old_format, 'NewFormat': value})
    
    @property
    def CustomFormat(self):
        return self._custom_format
    
    @CustomFormat.setter
    def CustomFormat(self, value):
        old_custom = getattr(self, '_custom_format', None)
        self._custom_format = value
        self._update_display()
        if old_custom != value:
            self.FormatChanged(self, {'OldCustomFormat': old_custom, 'NewCustomFormat': value})


class Rectangle:
    # Represents a rectangle with coordinates and dimensions.
    
    def __init__(self, x=0, y=0, width=0, height=0):
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height


class classproperty:
    # Descriptor for class properties.
    
    def __init__(self, fget):
        self.fget = fget
    
    def __get__(self, obj, cls=None):
        return self.fget(cls)


class Screen:
    # Represents the screen (Screen).
    
    def __init__(self, root=None):
        self._root = root or tk.Tk()  # Create a dummy root if none provided
    
    @property
    def Width(self):
        # Width of the screen.
        return self._root.winfo_screenwidth()
    
    @property
    def Height(self):
        # Height of the screen.
        return self._root.winfo_screenheight()
    
    @property
    def Bounds(self):
        # Bounds of the screen.
        return Rectangle(0, 0, self.Width, self.Height)
    
    @property
    def WorkingArea(self):
        # Working area of the screen.
        # Placeholder: assuming full screen for now
        return Rectangle(0, 0, self.Width, self.Height)
    
    @property
    def DeviceName(self):
        # Device name of the screen.
        return "Primary Screen"
    
    @property
    def BitsPerPixel(self):
        # Bits per pixel of the screen.
        # Placeholder: assuming 32-bit
        return 32
    
    @classproperty
    def PrimaryScreen(cls):
        # Primary screen.
        return Screen()
    
    @classproperty
    def AllScreens(cls):
        # All screens.
        return [Screen()]
    
    # System events (placeholders, since Tkinter does not directly support display configuration change events)
    DisplaySettingsChanging = lambda sender, e: None  # Occurs before the display configuration changes
    DisplaySettingsChanged = lambda sender, e: None   # Occurs after the display configuration has changed


class Point:
    # Represents a point with X and Y coordinates.
    
    def __init__(self, x=0, y=0):
        self.X = x
        self.Y = y


class Size:
    # Represents a size with width and height.
    
    def __init__(self, width=0, height=0):
        self.Width = width
        self.Height = height


class Form:
    # Represents the main window (Form).
    
    def __init__(self, Title="WinFormPy Application", Width=500, Height=300, Name=""):
        self._root = tk.Tk()
        
        # Main VB Properties
        self.Name = Name or "Form1"
        self.Text = Title
        self.Width = Width
        self.Height = Height
        self.Size = Size(Width, Height)
        self.Location = Point(0, 0)
        self.StartPosition = "WindowsDefaultLocation"  # 'CenterScreen', 'WindowsDefaultLocation', 'Manual', etc.
        self.FormBorderStyle = "Sizable"  # 'Sizable', 'FixedSingle', 'FixedDialog', 'None'
        self.MaximizeBox = True
        self.MinimizeBox = True
        self.ControlBox = True
        self.ShowIcon = True
        self.Icon = None
        self.BackColor = None
        self.Opacity = 1.0
        self.WindowState = "Normal"  # 'Normal', 'Minimized', 'Maximized'
        self.Enabled = True
        self.Visible = True
        self.TopMost = False
        self.IsMdiContainer = False
        self.CancelButton = None
        self.AcceptButton = None
        
        # Internal list to keep a reference to all controls
        self.Controls = [] 
        
        # Additional Properties
        self.BackgroundImage = None
        self.Font = None
        self.FontColor = None 
        
        # VB Events for forms (inspired by ControlBase)
        self.Load = lambda: None  # Initialization, before showing the form
        self.FormClosing = lambda sender, e: None  # Antes de cerrarse, permite cancelar
        self.FormClosed = lambda: None  # After closing
        self.Activated = lambda: None  # Cuando el formulario se activa
        self.Deactivate = lambda: None  # Cuando el formulario pierde el foco
        self.Resize = lambda: None  # Al redimensionar
        self.Move = lambda: None  # On move (placeholder)

    def Show(self):
        # Starts the main loop.
        # Apply VB properties
        self._root.title(self.Text)
        
        # Size and Location
        width = self.Size.Width
        height = self.Size.Height
        x = self.Location.X
        y = self.Location.Y
        
        if self.StartPosition == "CenterScreen":
            screen_width = self._root.winfo_screenwidth()
            screen_height = self._root.winfo_screenheight()
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
        elif self.StartPosition == "WindowsDefaultLocation":
            # Tkinter default
            pass
        # For Manual, use Location
        
        self._root.geometry(f"{width}x{height}+{x}+{y}")
        
        # FormBorderStyle
        if self.FormBorderStyle == "FixedSingle":
            self._root.resizable(False, False)
        elif self.FormBorderStyle == "None":
            self._root.overrideredirect(True)
        # Sizable is default
        
        # WindowState
        if self.WindowState == "Maximized":
            self._root.state('zoomed')
        elif self.WindowState == "Minimized":
            self._root.iconify()
        
        # Opacity
        self._root.attributes('-alpha', self.Opacity)
        
        # TopMost
        self._root.attributes('-topmost', self.TopMost)
        
        # Icon
        if self.Icon and self.ShowIcon:
            self._root.iconphoto(True, self.Icon)
        
        # Visible
        if not self.Visible:
            self._root.withdraw()
        
        # BackColor
        config = {}
        if self.BackColor is not None:
            config['bg'] = self.BackColor
        if self.BackgroundImage is not None:
            config['image'] = self.BackgroundImage
        if config:
            self._root.config(**config)
        
        # Bind CancelButton and AcceptButton
        if self.CancelButton:
            self._root.bind('<Escape>', lambda e: self.CancelButton._tk_widget.invoke())
        if self.AcceptButton:
            self._root.bind('<Return>', lambda e: self.AcceptButton._tk_widget.invoke())
        
        # Bind form events
        self._root.protocol("WM_DELETE_WINDOW", self._close)
        self._root.bind('<FocusIn>', lambda e: self.Activated())
        self._root.bind('<FocusOut>', lambda e: self.Deactivate())
        self._root.bind('<Configure>', lambda e: self.Resize())
        # Move placeholder
        
        # Trigger Load event
        self.Load()
        
        self._root.mainloop()
        
    def _close(self):
        # Handles the closing of the form.
        e = {'Cancel': False}
        self.FormClosing(self, e)
        if not e['Cancel']:
            self._root.destroy()
            self.FormClosed()
    
    def Close(self):
        # Closes the form.
        self._close()

    def AddControl(self, control):
        # Adds a control to the Form and positions it.
        self.Controls.append(control)
        control._place_control() # Posiciona el control base

class MDIParent(Form):
    # Represents the MDI parent form.
    
    def __init__(self, Title="MDI Parent", Width=800, Height=600):
        super().__init__(Title, Width, Height)
        
        self.IsMdiContainer = True  # Configura como contenedor MDI
        self.MDIChildren = []
        self.MainMenuStrip = None  # Placeholder para MenuStrip principal
        
        # Specific events for MDIParent
        self.MdiChildActivate = lambda sender, e: None  # Occurs when an MDI child form gets or loses focus, or is maximized/minimized
        self.ControlAdded = lambda control: None  # Occurs when a new control/child form is added
        self.ControlRemoved = lambda control: None  # Occurs when a child form is closed or removed
    
    @property
    def ActiveMdiChild(self):
        # Gets the active MDI child form.
        # Placeholder: returns the last added or None
        return self.MDIChildren[-1] if self.MDIChildren else None
    
    @property
    def MdiChildren(self):
        # Gets the array of MDI child forms.
        return self.MDIChildren
    
    def AddMDIChild(self, child):
        # Adds an MDI child.
        self.MDIChildren.append(child)
        child.MdiParent = self  # Asignar el MDIParent
        child._frame.pack(in_=self._root, fill='both', expand=True)
        # Bind para MdiChildActivate
        child._frame.bind('<FocusIn>', lambda e: self.MdiChildActivate(self, {'Child': child, 'Action': 'Activated'}))
        child._frame.bind('<FocusOut>', lambda e: self.MdiChildActivate(self, {'Child': child, 'Action': 'Deactivated'}))
        self.ControlAdded(child)
    
    def RemoveMDIChild(self, child):
        # Removes an MDI child.
        if child in self.MDIChildren:
            self.MDIChildren.remove(child)
            child._frame.pack_forget()
            self.ControlRemoved(child)
    
    def LayoutMdi(self, layout):
        # Arranges the MDI child forms.
        # layout: 'Cascade', 'TileHorizontal', 'TileVertical', 'ArrangeIcons'
        # Placeholder: basic implementation not available in Tkinter
        # En VB.NET, organiza las ventanas hijas
        pass


class MDIChild:
    # Represents an MDI child form.
    
    def __init__(self, title="Child"):
        self.Title = title
        self.Text = title  # Alias for Title
        self.MdiParent = None  # Assign the MDIParent
        self.IsMdiChild = True  # Indicates that it is an MDI child form
        self.ControlBox = True
        self.MinimizeBox = True
        self.MaximizeBox = True
        self.ShowInTaskbar = False
        self.WindowState = "Normal"  # 'Normal', 'Minimized', 'Maximized'
        self.MainMenuStrip = None  # Placeholder for MenuStrip
        
        self._frame = tk.Frame()
        self.Controls = []
        
        # Main events of MDIChild
        self.Load = lambda: None  # Initialization, before being visible
        self.FormClosing = lambda sender, e: None  # Before closing, allows cancel
        self.FormClosed = lambda: None  # After closing
        self.Activated = lambda: None  # When activated within the MDIParent
        self.Deactivate = lambda: None  # When it loses focus
        self.Resize = lambda: None  # On resize
        self.Move = lambda: None  # On move (placeholder, no title bar in Tkinter)

        # Bind events
        self._frame.bind('<FocusIn>', lambda e: self.Activated())
        self._frame.bind('<FocusOut>', lambda e: self.Deactivate())
        self._frame.bind('<Configure>', lambda e: self.Resize())
        # Move placeholder: no direct bind for move in Tkinter Frame
    
    def Show(self):
        # Shows the MDI child form (placeholder).
        # In the current implementation, it is shown via AddMDIChild of the parent
        self.Load()  # Trigger Load event
    
    def Close(self):
        # Closes the MDI child form.
        # Trigger FormClosing, allow cancel
        e = {'Cancel': False}
        self.FormClosing(self, e)
        if not e['Cancel']:
            # Proceed to close
            if self.MdiParent:
                self.MdiParent.RemoveMDIChild(self)
            self.FormClosed()  # Trigger FormClosed
    
    def AddControl(self, control):
        # Adds a control to the MDI child.
        self.Controls.append(control)
        control.master = self._frame
        control._place_control()


class SendKeys:
    # Class to send keystrokes and key combinations to the active process.
    
    @staticmethod
    def _parse_keys(keys):
        # Parses the keys string to handle special codes.
        parsed = []
        i = 0
        while i < len(keys):
            if keys[i] == '{':
                j = keys.find('}', i)
                if j > i:
                    inside = keys[i+1:j]
                    if ' ' in inside:
                        key, count = inside.split()
                        count = int(count)
                        for _ in range(count):
                            if key.lower() == 'enter':
                                parsed.append('\n')
                            elif key.lower() == 'tab':
                                parsed.append('\t')
                            elif key.lower() == 'esc':
                                parsed.append('\x1b')
                            # Add more if needed
                    else:
                        if inside.lower() == 'enter':
                            parsed.append('\n')
                        elif inside.lower() == 'tab':
                            parsed.append('\t')
                        elif inside.lower() == 'esc':
                            parsed.append('\x1b')
                        elif inside.startswith('f') and inside[1:].isdigit():
                            # F keys, placeholder
                            pass
                        else:
                            parsed.append(inside)
                    i = j + 1
                else:
                    parsed.append('{')
                    i += 1
            elif keys[i] == '~':
                parsed.append('\n')
                i += 1
            else:
                parsed.append(keys[i])
                i += 1
        return ''.join(parsed)
    
    @staticmethod
    def Send(keys):
        # Sends the keystrokes immediately.
        parsed_keys = SendKeys._parse_keys(keys)
        focused = tk.focus_get()
        if focused and hasattr(focused, 'insert'):
            focused.insert(tk.END, parsed_keys)
    
    @staticmethod
    def SendWait(keys):
        # Sends the keystrokes and waits for them to be processed.
        # In Tkinter, it is synchronous, so same as Send
        SendKeys.Send(keys)


class Timer:
    # Represents a Timer for timed events.
    
    def __init__(self, root, interval=1000, Name="", Enabled=False, Tag=None, Modifiers="Private"):
        self._root = root
        self.Name = Name
        self.Interval = interval
        self._enabled = False  # Initialize _enabled before property setter usage
        self.Enabled = Enabled
        self.Tag = Tag  # Custom object
        self.Modifiers = Modifiers  # 'Public', 'Private', etc. (placeholder)
        self.Tick = lambda: None
        self._job = None
        
        # Start if Enabled
        if self.Enabled:
            self.Start()

    @property
    def Enabled(self):
        return self._enabled

    @Enabled.setter
    def Enabled(self, value):
        if value and not self._enabled:
            self.Start()
        elif not value and self._enabled:
            self.Stop()
        self._enabled = value

    def Start(self):
        # Starts the timer.
        if not self._enabled:
            self._enabled = True
            self._schedule()

    def Stop(self):
        # Stops the timer.
        self._enabled = False
        if self._job:
            self._root.after_cancel(self._job)

    def _schedule(self):
        # Schedules the next tick.
        if self._enabled:
            self.Tick()
            self._job = self._root.after(self.Interval, self._schedule)

