# =============================================================
# Module: winformpy_extended.py
# Author: DatamanEdge
# Date: 2025-12-08
# Version: 1.0.1
# Description: 
# WinFormPy Extension for custom controls and advanced layout management.
# =============================================================

import tkinter as tk
import tkinter.ttk as ttk
try:
    from winformpy import Label, AnchorStyles, ContentAlignment, TabControl, TabAlignment
except ImportError:
    try:
        from .winformpy import Label, AnchorStyles, ContentAlignment, TabControl, TabAlignment
    except ImportError:
        # Fallback if running directly or path issues
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from winformpy import Label, AnchorStyles, ContentAlignment, TabControl, TabAlignment

class ExtendedLabel(Label):
    """
    Extended Label control that supports multiline text with dynamic wrapping
    and alignment.
    
    Features:
    - Dynamic Wrapping: Text wraps to fit the control's width automatically.
    - AutoSize=False by default: Control size determines text layout.
    - Resizing: Updates wrapping when control is resized (e.g. via Anchors).
    - TextAlign: Supports dynamic alignment updates.
    """
    def __init__(self, master_form, props=None):
        if props is None:
            props = {}
            
        # Ensure AutoSize is False so we control the size
        # "autosize no sea al texto si no del texto al tamaño del control"
        if 'AutoSize' not in props:
            props['AutoSize'] = False
            
        super().__init__(master_form, props)
        
        # Bind the resize event to update text wrapping with add='+' to keep base class bindings
        self._tk_widget.bind('<Configure>', self._update_wrapping, add="+")
        
        # Initial wrap update
        self._tk_widget.after(10, self._update_wrapping)
        
    def _update_wrapping(self, event=None):
        """Updates the wraplength of the label to match its current width."""
        if self._tk_widget:
            # Set wraplength to the current width of the widget
            # Subtract a small padding to ensure it fits comfortably
            # event.width is available on resize, otherwise use winfo_width
            width = event.width if event else self._tk_widget.winfo_width()
            
            # Only update if width is valid and changed
            if width > 10:
                # Subtract padding (padx * 2) if set, but simple subtraction works for now
                # We subtract a bit more to avoid jitter at the edge
                self._tk_widget.config(wraplength=width - 8)

    @property
    def TextAlign(self):
        """Gets or sets the alignment of the text in the label."""
        return getattr(self, '_text_align', ContentAlignment.TopLeft)

    @TextAlign.setter
    def TextAlign(self, value):
        self._text_align = value
        if self._tk_widget:
            # Alignment maps
            anchor_map = {
                ContentAlignment.TopLeft: 'nw', ContentAlignment.TopCenter: 'n', ContentAlignment.TopRight: 'ne',
                ContentAlignment.MiddleLeft: 'w', ContentAlignment.MiddleCenter: 'center', ContentAlignment.MiddleRight: 'e',
                ContentAlignment.BottomLeft: 'sw', ContentAlignment.BottomCenter: 's', ContentAlignment.BottomRight: 'se',
                # String fallbacks
                'TopLeft': 'nw', 'TopCenter': 'n', 'TopRight': 'ne',
                'MiddleLeft': 'w', 'MiddleCenter': 'center', 'MiddleRight': 'e',
                'BottomLeft': 'sw', 'BottomCenter': 's', 'BottomRight': 'se',
                'left': 'w', 'center': 'center', 'right': 'e'
            }
            
            justify_map = {
                ContentAlignment.TopLeft: 'left', ContentAlignment.TopCenter: 'center', ContentAlignment.TopRight: 'right',
                ContentAlignment.MiddleLeft: 'left', ContentAlignment.MiddleCenter: 'center', ContentAlignment.MiddleRight: 'right',
                ContentAlignment.BottomLeft: 'left', ContentAlignment.BottomCenter: 'center', ContentAlignment.BottomRight: 'right',
                 # String fallbacks
                'TopLeft': 'left', 'TopCenter': 'center', 'TopRight': 'right',
                'MiddleLeft': 'left', 'MiddleCenter': 'center', 'MiddleRight': 'right',
                'BottomLeft': 'left', 'BottomCenter': 'center', 'BottomRight': 'right',
                'left': 'left', 'center': 'center', 'right': 'right'
            }
            
            self._tk_widget.config(
                anchor=anchor_map.get(value, 'w'),
                justify=justify_map.get(value, 'left')
            )


