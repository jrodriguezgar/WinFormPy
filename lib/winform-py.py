# =============================================================
# Module: winform-py.py
# Author: Vibe coding by DatamanEdge 
# Date: 2025-12-05
# Version: 1.0.3
# Description: 
# WinFormPy is a complete Python library designed to
# bridge the gap between the graphical user interface (GUI) 
# development paradigm of Visual Basic (VB.NET / WinForms) 
# and Python's standard toolkit, Tkinter.
# This tool allows developers with 
# VB experience to leverage their existing knowledge to create 
# cross-platform desktop applications in Python, minimizing the 
# learning curve of Tkinter's specific conventions.
# =============================================================


import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import os
import winsound
from datetime import date, datetime
import importlib.util
import sys

# Importar utilidades de winform-py_tools
try:
    spec = importlib.util.spec_from_file_location("winform_py_tools", 
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "winform-py_tools.py"))
    winform_py_tools = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(winform_py_tools)
    from winform_py_tools import css_to_tkinter_config, apply_css_to_widget
except:
    # Fallback si no se puede importar
    def css_to_tkinter_config(css_string, current_widget=None):
        return {}
    def apply_css_to_widget(widget, css_string):
        pass

# =======================================================================
# MÓDULO PRINCIPAL: winformpy.py
# =======================================================================

class SystemColors:
    """Colores del sistema Windows Forms."""
    Control = "#F0F0F0"  # Color de fondo de controles
    ControlText = "#000000"  # Color de texto de controles
    Window = "#FFFFFF"  # Color de fondo de ventanas
    WindowText = "#000000"  # Color de texto de ventanas
    Highlight = "#0078D7"  # Color de resaltado/selección
    HighlightText = "#FFFFFF"  # Color de texto resaltado
    GrayText = "#6D6D6D"  # Color de texto deshabilitado
    ButtonFace = "#F0F0F0"  # Color de fondo de botones
    ButtonText = "#000000"  # Color de texto de botones
    ActiveCaption = "#0078D7"  # Color de barra de título activa
    InactiveCaption = "#BFBFBF"  # Color de barra de título inactiva
    ActiveBorder = "#B4B4B4"  # Color de borde activo
    InactiveBorder = "#F4F4F4"  # Color de borde inactivo
    AppWorkspace = "#ABABAB"  # Color de fondo de área de trabajo MDI
    Desktop = "#000000"  # Color de fondo del escritorio
    MenuBar = "#F0F0F0"  # Color de fondo de barra de menú
    Menu = "#F0F0F0"  # Color de fondo de menú
    MenuText = "#000000"  # Color de texto de menú
    Info = "#FFFFE1"  # Color de fondo de tooltip
    InfoText = "#000000"  # Color de texto de tooltip


class SystemFonts:
    """Fuentes del sistema Windows Forms."""
    DefaultFont = ("Segoe UI", 9)  # Fuente predeterminada del sistema
    MessageBoxFont = ("Segoe UI", 9)  # Fuente de MessageBox
    CaptionFont = ("Segoe UI", 9)  # Fuente de barra de título
    SmallCaptionFont = ("Segoe UI", 8)  # Fuente de barra de título pequeña
    MenuFont = ("Segoe UI", 9)  # Fuente de menús
    StatusFont = ("Segoe UI", 9)  # Fuente de barra de estado
    IconTitleFont = ("Segoe UI", 9)  # Fuente de títulos de iconos
    DialogFont = ("Segoe UI", 9)  # Fuente de diálogos


class SystemStyles:
    """Clase para gestionar estilos del sistema y permitir personalización global.
    
    Uso:
        # Usar estilos del sistema (por defecto)
        button = Button(form, {'UseSystemStyles': True})
        
        # O establecer estilos globales personalizados
        SystemStyles.SetGlobalFont(("Arial", 10))
        SystemStyles.SetGlobalColors(BackColor="#FFFFFF", ForeColor="#000000")
    """
    
    # Configuración global (None = usar valores del sistema)
    _global_font = None
    _global_back_color = None
    _global_fore_color = None
    _use_system_styles_by_default = True
    
    @staticmethod
    def SetGlobalFont(font):
        """Establece una fuente global para todos los controles nuevos.
        
        Args:
            font: Tupla (nombre_fuente, tamaño) o None para usar fuente del sistema
        """
        SystemStyles._global_font = font
    
    @staticmethod
    def SetGlobalColors(BackColor=None, ForeColor=None):
        """Establece colores globales para todos los controles nuevos.
        
        Args:
            BackColor: Color de fondo o None para usar color del sistema
            ForeColor: Color de texto o None para usar color del sistema
        """
        if BackColor is not None:
            SystemStyles._global_back_color = BackColor
        if ForeColor is not None:
            SystemStyles._global_fore_color = ForeColor
    
    @staticmethod
    def SetUseSystemStylesByDefault(value):
        """Establece si usar estilos del sistema por defecto.
        
        Args:
            value: True para usar estilos del sistema, False para usar None
        """
        SystemStyles._use_system_styles_by_default = value
    
    @staticmethod
    def GetDefaultFont(control_type="Control"):
        """Obtiene la fuente predeterminada según configuración.
        
        Args:
            control_type: Tipo de control ("Control", "Menu", "Status", etc.)
        
        Returns:
            Fuente a usar o None si no se debe aplicar
        """
        # Prioridad: global > sistema > None
        if SystemStyles._global_font is not None:
            return SystemStyles._global_font
        
        if SystemStyles._use_system_styles_by_default:
            if control_type == "Menu":
                return SystemFonts.MenuFont
            elif control_type == "Status":
                return SystemFonts.StatusFont
            elif control_type == "Dialog":
                return SystemFonts.DialogFont
            else:
                return SystemFonts.DefaultFont
        
        return None
    
    @staticmethod
    def GetDefaultBackColor(control_type="Control"):
        """Obtiene el color de fondo predeterminado según configuración.
        
        Args:
            control_type: Tipo de control ("Control", "Window", "Button", etc.)
        
        Returns:
            Color a usar o None si no se debe aplicar
        """
        # Prioridad: global > sistema > None
        if SystemStyles._global_back_color is not None:
            return SystemStyles._global_back_color
        
        if SystemStyles._use_system_styles_by_default:
            if control_type == "Window":
                return SystemColors.Window
            elif control_type == "Button":
                return SystemColors.ButtonFace
            else:
                return SystemColors.Control
        
        return None
    
    @staticmethod
    def GetDefaultForeColor(control_type="Control"):
        """Obtiene el color de texto predeterminado según configuración.
        
        Args:
            control_type: Tipo de control ("Control", "Window", "Button", etc.)
        
        Returns:
            Color a usar o None si no se debe aplicar
        """
        # Prioridad: global > sistema > None
        if SystemStyles._global_fore_color is not None:
            return SystemStyles._global_fore_color
        
        if SystemStyles._use_system_styles_by_default:
            if control_type == "Window":
                return SystemColors.WindowText
            elif control_type == "Button":
                return SystemColors.ButtonText
            else:
                return SystemColors.ControlText
        
        return None
    
    @staticmethod
    def ApplyToDefaults(defaults, control_type="Control", use_system_styles=None):
        """Aplica estilos del sistema a un diccionario de defaults si está habilitado.
        
        Args:
            defaults: Diccionario de valores por defecto
            control_type: Tipo de control para determinar estilos apropiados
            use_system_styles: True/False para forzar, None para usar configuración global
        
        Returns:
            Diccionario defaults modificado
        """
        # Determinar si aplicar estilos del sistema
        apply = use_system_styles if use_system_styles is not None else SystemStyles._use_system_styles_by_default
        
        if not apply:
            return defaults
        
        # Aplicar solo si el valor es None en defaults
        if 'Font' in defaults and defaults['Font'] is None:
            defaults['Font'] = SystemStyles.GetDefaultFont(control_type)
        
        if 'BackColor' in defaults and defaults['BackColor'] is None:
            defaults['BackColor'] = SystemStyles.GetDefaultBackColor(control_type)
        
        if 'ForeColor' in defaults and defaults['ForeColor'] is None:
            defaults['ForeColor'] = SystemStyles.GetDefaultForeColor(control_type)
        
        return defaults


class ToolTip:
    """
    Clase para crear tooltips (información contextual al pasar el ratón).
    
    Uso - Opción 1: tooltip = ToolTip(widget); tooltip.Text = "Help text"
    Uso - Opción 2: tooltip = ToolTip(widget, {'Text': 'Help text', 'Delay': 1000, 'BgColor': 'yellow'})
    Uso - Opción 3: tooltip = ToolTip(widget, {'UseSystemStyles': True})  # Usa colores del sistema
    """
    
    def __init__(self, widget, props=None):
        """Inicializa un ToolTip para un widget.
        
        Args:
            widget: Widget de tkinter al que se asocia el tooltip
            props: Diccionario opcional con propiedades (Text, Delay, BgColor, FgColor, BorderColor, BorderWidth, Font)
                   Use {'UseSystemStyles': True} para aplicar estilos del sistema automáticamente
        """
        defaults = {
            'Text': "",
            'Delay': 500,
            'BgColor': None,
            'FgColor': None,
            'BorderColor': "black",
            'BorderWidth': 1,
            'Font': None
        }
        
        if props:
            # Extraer UseSystemStyles antes de actualizar defaults
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            # Aplicar estilos del sistema si está habilitado (usar colores de Info)
            if use_system_styles:
                if defaults['BgColor'] is None:
                    defaults['BgColor'] = SystemColors.Info
                if defaults['FgColor'] is None:
                    defaults['FgColor'] = SystemColors.InfoText
                if defaults['Font'] is None:
                    defaults['Font'] = SystemFonts.DefaultFont
            # Aliases para compatibilidad
            if 'text' in props:
                defaults['Text'] = props['text']
            if 'bg' in props:
                defaults['BgColor'] = props['bg']
            if 'fg' in props:
                defaults['FgColor'] = props['fg']
            if 'delay' in props:
                defaults['Delay'] = props['delay']
            if 'bordercolor' in props:
                defaults['BorderColor'] = props['bordercolor']
            if 'borderwidth' in props:
                defaults['BorderWidth'] = props['borderwidth']
            if 'font' in props:
                defaults['Font'] = props['font']
        
        # Aplicar valores por defecto si aún son None
        if defaults['BgColor'] is None:
            defaults['BgColor'] = "lightyellow"
        if defaults['FgColor'] is None:
            defaults['FgColor'] = "black"
        if defaults['Font'] is None:
            defaults['Font'] = ("Segoe UI", 9)
        
        self.widget = widget
        self.text = defaults['Text']
        self.delay = defaults['Delay']
        self.bg = defaults['BgColor']
        self.fg = defaults['FgColor']
        self.bordercolor = defaults['BorderColor']
        self.borderwidth = defaults['BorderWidth']
        self.font = defaults['Font']
        
        self._tooltip_window = None
        self._scheduled_id = None
        
        # Bind eventos
        self.widget.bind('<Enter>', self._on_enter)
        self.widget.bind('<Leave>', self._on_leave)
        self.widget.bind('<Motion>', self._on_motion)
    
    def _on_enter(self, event):
        """Maneja el evento de entrada del ratón."""
        self._schedule_tooltip(event)
    
    def _on_leave(self, event):
        """Maneja el evento de salida del ratón."""
        self._cancel_tooltip()
        self._hide_tooltip()
    
    def _on_motion(self, event):
        """Maneja el movimiento del ratón."""
        if self._tooltip_window:
            # Actualizar posición del tooltip
            x = event.x_root + 15
            y = event.y_root + 10
            self._tooltip_window.wm_geometry(f"+{x}+{y}")
    
    def _schedule_tooltip(self, event):
        """Programa la aparición del tooltip después del delay."""
        self._cancel_tooltip()
        if self.text:
            self._scheduled_id = self.widget.after(
                self.delay, 
                lambda: self._show_tooltip(event)
            )
    
    def _cancel_tooltip(self):
        """Cancela la aparición programada del tooltip."""
        if self._scheduled_id:
            self.widget.after_cancel(self._scheduled_id)
            self._scheduled_id = None
    
    def _show_tooltip(self, event):
        """Muestra el tooltip."""
        if self._tooltip_window or not self.text:
            return
        
        x = event.x_root + 15
        y = event.y_root + 10
        
        self._tooltip_window = tk.Toplevel(self.widget)
        self._tooltip_window.wm_overrideredirect(True)
        self._tooltip_window.wm_geometry(f"+{x}+{y}")
        
        # Crear label con el texto
        label = tk.Label(
            self._tooltip_window,
            text=self.text,
            background=self.bg,
            foreground=self.fg,
            relief="solid",
            borderwidth=self.borderwidth,
            font=self.font,
            padx=5,
            pady=2,
            justify='left'
        )
        label.pack()
        
        # Configurar borde
        if self.bordercolor != self.bg:
            label.config(highlightbackground=self.bordercolor, highlightthickness=self.borderwidth)
    
    def _hide_tooltip(self):
        """Oculta el tooltip."""
        if self._tooltip_window:
            self._tooltip_window.destroy()
            self._tooltip_window = None
    
    def update_text(self, new_text):
        """Actualiza el texto del tooltip."""
        self.text = new_text
        if self._tooltip_window:
            # Si está visible, ocultarlo y volver a mostrarlo con el nuevo texto
            self._hide_tooltip()


class ControlBase:
    """Clase base para todos los controles de WinFormPy."""
    
    def __init__(self, master_tk_widget, Left=0, Top=0):
        # El widget de Tkinter real (e.g., tk.Button, tk.Label)
        self._tk_widget = None 
        # Referencia al widget contenedor (la Form o UserControl)
        self.master = master_tk_widget 
        
        # Propiedades de posición tipo VB (Backing fields)
        self._left = Left
        self._top = Top
        self._width = None
        self._height = None
        
        # Propiedad MousePointer (cursor del mouse)
        self.MousePointer = "arrow"
        
        # Nuevas propiedades VB
        self.Enabled = True
        self.BackColor = None
        self.BorderStyle = None  # e.g., 'flat', 'raised', 'sunken', 'ridge', 'groove'
        self.BackgroundImage = None
        self.Font = None
        self.FontColor = None
        self.ForeColor = None
        
        # AutoSize properties
        self._autosize = False
        self.MinimumSize = None  # (width, height) or None
        self.MaximumSize = None  # (width, height) or None
        self._original_size = None  # Para AutoSizeMode.GrowOnly
        
        # Anchor and Dock properties
        self._anchor = ['Top', 'Left']  # Default: Top, Left
        self._dock = 'None'  # None, Top, Bottom, Left, Right, Fill
        self._initial_distance = {}  # Almacena distancias iniciales a los bordes
        self._container_size = None  # Tamaño inicial del contenedor
        
        # ToolTip
        self._tooltip_text = ""
        self._tooltip_instance = None
        
        # Eventos comunes VB (callbacks)
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

    @property
    def Left(self):
        return self._left

    @Left.setter
    def Left(self, value):
        self._left = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._place_control(self.Width, self.Height)

    @property
    def Top(self):
        return self._top

    @Top.setter
    def Top(self, value):
        self._top = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._place_control(self.Width, self.Height)

    @property
    def Width(self):
        return self._width

    @Width.setter
    def Width(self, value):
        self._width = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._place_control(self.Width, self.Height)

    @property
    def Height(self):
        return self._height

    @Height.setter
    def Height(self, value):
        self._height = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._place_control(self.Width, self.Height)

    @property
    def Location(self):
        return (self._left, self._top)

    @Location.setter
    def Location(self, value):
        if isinstance(value, (tuple, list)) and len(value) >= 2:
            self._left = value[0]
            self._top = value[1]
            if hasattr(self, '_tk_widget') and self._tk_widget:
                self._place_control(self.Width, self.Height)

    @property
    def Size(self):
        return (self._width, self._height)

    @Size.setter
    def Size(self, value):
        if isinstance(value, (tuple, list)) and len(value) >= 2:
            self._width = value[0]
            self._height = value[1]
            if hasattr(self, '_tk_widget') and self._tk_widget:
                self._place_control(self.Width, self.Height)
        
    @property
    def AutoSize(self):
        """Obtiene o establece si el control se redimensiona automáticamente."""
        return self._autosize

    @AutoSize.setter
    def AutoSize(self, value):
        self._autosize = value
        if value and hasattr(self, '_apply_autosize'):
            self._apply_autosize()
            # Si el control es visible, reposicionar
            if hasattr(self, 'Visible') and self.Visible and hasattr(self, '_place_control'):
                if hasattr(self, 'Width') and hasattr(self, 'Height'):
                    self._place_control(self.Width, self.Height)

    @property
    def Font(self):
        """Obtiene o establece la fuente del control."""
        return getattr(self, '_font', None)

    @Font.setter
    def Font(self, value):
        """Obtiene o establece la fuente del control."""
        self._font = value
        if self._tk_widget:
            self._apply_visual_config()
            if self.AutoSize:
                self._apply_autosize()
                # Si el control es visible, reposicionar
                if hasattr(self, 'Visible') and self.Visible and hasattr(self, '_place_control'):
                    if hasattr(self, 'Width') and hasattr(self, 'Height'):
                        self._place_control(self.Width, self.Height)

    @property
    def BackColor(self):
        """Obtiene o establece el color de fondo del control."""
        return self._backcolor

    @BackColor.setter
    def BackColor(self, value):
        """Establece el color de fondo del control."""
        self._backcolor = value
        if self._tk_widget:
            self._apply_visual_config()

    @property
    def ForeColor(self):
        """Obtiene o establece el color de texto del control."""
        return self._forecolor

    @ForeColor.setter
    def ForeColor(self, value):
        """Establece el color de texto del control."""
        self._forecolor = value
        if self._tk_widget:
            self._apply_visual_config()

    @property
    def Enabled(self):
        """Obtiene o establece si el control está habilitado."""
        return self._enabled

    @Enabled.setter
    def Enabled(self, value):
        """Establece si el control está habilitado."""
        self._enabled = value
        if self._tk_widget:
            self._apply_visual_config()

    @property
    def BorderStyle(self):
        """Obtiene o establece el estilo del borde del control."""
        return self._borderstyle

    @BorderStyle.setter
    def BorderStyle(self, value):
        """Establece el estilo del borde del control."""
        self._borderstyle = value
        if self._tk_widget:
            self._apply_visual_config()

    def _place_control(self, width=None, height=None):
        """Usa el gestor de geometría 'place' para posicionar el control."""
        if self._tk_widget:
            # Posicionar inicialmente
            place_args = {
                'x': self.Left,
                'y': self.Top,
                'in_': self.master
            }
            if width is not None:
                place_args['width'] = width
            if height is not None:
                place_args['height'] = height
                
            self._tk_widget.place(**place_args)
            
            # Vincular eventos de redimensionamiento una sola vez
            if not hasattr(self, '_anchor_dock_initialized'):
                self._anchor_dock_initialized = True
                # Esperar a que la ventana esté completamente renderizada
                self.master.after(100, self._initialize_anchor_dock)
            
            # Notificar al padre si es un contenedor WinFormPy
            if hasattr(self.master, '_control_wrapper'):
                parent = self.master._control_wrapper
                if hasattr(parent, '_apply_autosize_panel') and getattr(parent, 'AutoSize', False):
                    parent._apply_autosize_panel()
            
            # Establecer el cursor
            self._tk_widget.config(cursor=self.MousePointer)
            
            # Aplicar configuración visual
            self._apply_visual_config()

    def _bind_common_events(self):
        """Binds common events to the widget."""
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
        """Handler for MouseDown event."""
        self.MouseDown(event.num, event.x, event.y)

    def _on_mouse_up(self, event):
        """Handler for MouseUp event."""
        self.MouseUp(event.num, event.x, event.y)

    def _on_mouse_enter(self, event):
        """Handler for MouseEnter event."""
        self.MouseEnter()

    def _on_mouse_leave(self, event):
        """Handler for MouseLeave event."""
        self.MouseLeave()

    def _on_enter(self, event):
        """Handler for Enter (GotFocus) event."""
        self.Enter()

    def _on_leave(self, event):
        """Handler for Leave (LostFocus) event."""
        self.Leave()

    def _on_key_down(self, event):
        """Handler for KeyDown event."""
        self.KeyDown(event.keysym)

    def _on_click(self, event):
        """Handler for Click event."""
        self.Click()

    def _on_double_click(self, event):
        """Handler for DoubleClick event."""
        self.DoubleClick()

    def _on_paint(self, event):
        """Handler for Paint and Resize events."""
        self.Paint()
        self.Resize()

    def _on_key_press(self, event):
        """Handler for KeyPress event."""
        self.KeyPress(event.char)

    def _on_key_up(self, event):
        """Handler for KeyUp event."""
        self.KeyUp(event.keysym)

    def apply_css(self, css_string):
        """Aplica estilos CSS al control usando la utilidad de winform-py_tools."""
        apply_css_to_widget(self._tk_widget, css_string)

    def get_Parent(self):
        """Obtiene el control padre (contenedor) de este control.
        
        Returns:
            El control padre si existe, None en caso contrario.
        """
        # Buscar el control padre recorriendo el master hasta encontrar un control
        # que tenga la lista de Controls (Panel, Form, TabPage, etc.)
        parent = None
        current_master = self.master
        
        # Buscar en la jerarquía de widgets Tkinter hasta encontrar un contenedor
        while current_master is not None:
            # Verificar si hay un objeto wrapper que contenga este widget
            if hasattr(current_master, '_control_wrapper'):
                parent = current_master._control_wrapper
                break
            # Intentar obtener el master del widget actual
            try:
                current_master = current_master.master
            except AttributeError:
                break
        
        return parent
    
    @property
    def Visible(self):
        """Obtiene el estado de visibilidad efectiva del control.
        
        Un control solo es visible si su propiedad Visible está en True
        Y todos sus contenedores padre también están visibles.
        """
        return self.get_Visible()

    @Visible.setter
    def Visible(self, value):
        """Establece el estado de visibilidad del control."""
        self.set_Visible(value)

    def get_Visible(self):
        """Obtiene el estado de visibilidad efectiva del control.
        
        Implementa la jerarquía de visibilidad de Windows Forms:
        - Un control solo es visible si su propia propiedad _visible es True
        - Y todos sus contenedores padre también tienen _visible = True
        
        Returns:
            True si el control y todos sus padres están visibles, False en caso contrario.
        """
        # Verificar la propiedad _visible propia
        if not getattr(self, '_visible', True):
            return False
        
        # Verificar la visibilidad de todos los padres en la jerarquía
        parent = self.get_Parent()
        while parent is not None:
            if not getattr(parent, '_visible', True):
                return False
            # Subir al siguiente nivel de la jerarquía
            parent = parent.get_Parent() if hasattr(parent, 'get_Parent') else None
        
        return True

    def set_Visible(self, value):
        """Establece el estado de visibilidad del control.
        
        Implementa la jerarquía de visibilidad de Windows Forms:
        - Establece la propiedad _visible del control
        - Si el control es un contenedor (Panel, etc.), propaga el cambio a sus hijos
        - Solo muestra u oculta físicamente el widget si la visibilidad efectiva cambia
        
        Args:
            value: True para hacer visible, False para ocultar
        """
        old_visible = getattr(self, '_visible', True)
        self._visible = value
        
        # Determinar si el control debe mostrarse u ocultarse físicamente
        # Solo mostrar si value es True Y todos los padres también son visibles
        should_be_visible = value
        if value:
            # Verificar visibilidad de padres
            parent = self.get_Parent()
            while parent is not None:
                if not getattr(parent, '_visible', True):
                    should_be_visible = False
                    break
                parent = parent.get_Parent() if hasattr(parent, 'get_Parent') else None
        
        # Aplicar visibilidad física al widget
        if hasattr(self, '_tk_widget') and self._tk_widget:
            if should_be_visible:
                # Mostrar el control usando place con su posición y tamaño actuales
                if hasattr(self, 'Width') and hasattr(self, 'Height'):
                    self._place_control(self.Width, self.Height)
                else:
                    self._tk_widget.place(x=self.Left, y=self.Top)
            else:
                # Ocultar el control
                self._tk_widget.place_forget()
        
        # Si es un contenedor con controles hijos, propagar el cambio
        if hasattr(self, 'Controls'):
            for control in self.Controls:
                if hasattr(control, '_visible'):
                    # Solo actualizar la visibilidad física si el hijo tiene _visible = True
                    if control._visible:
                        if should_be_visible:
                            # El contenedor se hace visible, mostrar hijos visibles
                            if hasattr(control, '_place_control'):
                                if hasattr(control, 'Width') and hasattr(control, 'Height'):
                                    control._place_control(control.Width, control.Height)
                                else:
                                    control._place_control()
                        else:
                            # El contenedor se oculta, ocultar todos los hijos
                            if hasattr(control, '_tk_widget') and control._tk_widget:
                                control._tk_widget.place_forget()
                    # Si el hijo está propagando cambios a sus propios hijos (ej. Panel dentro de Panel)
                    if hasattr(control, 'set_Visible') and old_visible != value:
                        # Re-evaluar la visibilidad del hijo para que propague a sus hijos
                        control_visible = control._visible
                        control.set_Visible(control_visible)
    
    @property
    def ToolTipText(self):
        """Obtiene el texto del tooltip."""
        return self._tooltip_text
    
    @ToolTipText.setter
    def ToolTipText(self, value):
        """Establece el texto del tooltip."""
        self._tooltip_text = value
        
        # Crear o actualizar el tooltip
        if self._tk_widget:
            if value and value.strip():
                if self._tooltip_instance:
                    # Actualizar texto existente
                    self._tooltip_instance.update_text(value)
                else:
                    # Crear nuevo tooltip
                    self._tooltip_instance = ToolTip(self._tk_widget, value)
            else:
                # Remover tooltip si el texto está vacío
                if self._tooltip_instance:
                    self._tooltip_instance._hide_tooltip()
                    self._tooltip_instance = None
    
    def _initialize_anchor_dock(self):
        """Inicializa Anchor o Dock después de que el contenedor está listo."""
        if self._dock != 'None':
            # Aplicar Dock
            self._apply_dock()
            # Vincular redimensionamiento para Dock
            self.master.bind('<Configure>', self._on_dock_resize, add='+')
        elif self._anchor:
            # Calcular distancias iniciales para Anchor
            self._calculate_initial_distances()
            # Vincular redimensionamiento para Anchor
            self.master.bind('<Configure>', self._on_container_resize, add='+')
            # También vincular al evento de mapeo para cuando la ventana se muestra
            self.master.bind('<Map>', lambda e: self._calculate_initial_distances(), add='+')
    
    def _calculate_initial_distances(self):
        """Calcula las distancias iniciales del control a los bordes del contenedor."""
        self.master.update_idletasks()
        container_width = self.master.winfo_width()
        container_height = self.master.winfo_height()
        
        # Si el contenedor aún no tiene tamaño válido, reintentar
        if container_width <= 1 or container_height <= 1:
            self.master.after(50, self._calculate_initial_distances)
            return
        
        # Obtener la posición actual real del widget
        self._tk_widget.update_idletasks()
        
        # Calcular coordenadas relativas a self.master (el contenedor lógico)
        # Esto es necesario porque el widget Tkinter puede tener un padre diferente (ej. _root)
        # pero estar posicionado visualmente dentro de self.master usando place(in_=...)
        if self._tk_widget.master != self.master:
            try:
                actual_x = self._tk_widget.winfo_rootx() - self.master.winfo_rootx()
                actual_y = self._tk_widget.winfo_rooty() - self.master.winfo_rooty()
            except:
                # Fallback si hay error (ej. widget no mapeado)
                actual_x = self._tk_widget.winfo_x()
                actual_y = self._tk_widget.winfo_y()
        else:
            actual_x = self._tk_widget.winfo_x()
            actual_y = self._tk_widget.winfo_y()
            
        actual_width = self._tk_widget.winfo_width()
        actual_height = self._tk_widget.winfo_height()
        
        # Si el widget no ha sido posicionado aún, usar los valores de propiedades
        if actual_x == 0 and actual_y == 0 and actual_width <= 1:
            actual_x = self.Left
            actual_y = self.Top
            actual_width = self.Width
            actual_height = self.Height
        else:
            # Actualizar las propiedades con los valores reales
            self.Left = actual_x
            self.Top = actual_y
            self.Width = actual_width
            self.Height = actual_height
        
        self._container_size = (container_width, container_height)
        self._initial_distance = {
            'left': actual_x,
            'top': actual_y,
            'right': container_width - (actual_x + actual_width),
            'bottom': container_height - (actual_y + actual_height)
        }
    
    def _on_container_resize(self, event=None):
        """Maneja el redimensionamiento del contenedor para aplicar Anchor."""
        if not self._tk_widget or self._dock != 'None':
            return
        
        # Filtrar eventos: solo procesar si el evento es del master o no hay evento
        # (llamadas directas sin evento también se procesan)
        if event and hasattr(event, 'widget'):
            # Solo procesar si el widget del evento es el master o un ancestro
            if event.widget != self.master and not self._is_ancestor(event.widget, self.master):
                return
        
        # Obtener nuevo tamaño del contenedor
        new_width = self.master.winfo_width()
        new_height = self.master.winfo_height()
        
        # Ignorar eventos de contenedores sin tamaño válido
        if new_width <= 1 or new_height <= 1:
            return
        
        # Si no hay distancias iniciales, calcularlas
        if not self._initial_distance or not self._container_size:
            self._calculate_initial_distances()
            return
        
        # Aplicar Anchor
        new_left = self.Left
        new_top = self.Top
        new_width_ctrl = self.Width
        new_height_ctrl = self.Height
        
        # Anchor Left: mantener distancia izquierda
        if 'Left' in self._anchor:
            new_left = self._initial_distance['left']
        
        # Anchor Right: mantener distancia derecha
        if 'Right' in self._anchor:
            if 'Left' in self._anchor:
                # Anclado a ambos lados: estirar horizontalmente
                new_width_ctrl = new_width - self._initial_distance['left'] - self._initial_distance['right']
            else:
                # Solo Right: mover el control
                new_left = new_width - self._initial_distance['right'] - self.Width
        
        # Anchor Top: mantener distancia superior
        if 'Top' in self._anchor:
            new_top = self._initial_distance['top']
        
        # Anchor Bottom: mantener distancia inferior
        if 'Bottom' in self._anchor:
            if 'Top' in self._anchor:
                # Anclado arriba y abajo: estirar verticalmente
                new_height_ctrl = new_height - self._initial_distance['top'] - self._initial_distance['bottom']
            else:
                # Solo Bottom: mover el control
                new_top = new_height - self._initial_distance['bottom'] - self.Height
        
        # Actualizar posición y tamaño
        self.Left = int(new_left)
        self.Top = int(new_top)
        self.Width = int(new_width_ctrl)
        self.Height = int(new_height_ctrl)
        
        # Reposicionar con el nuevo tamaño
        self._tk_widget.place(x=self.Left, y=self.Top, width=self.Width, height=self.Height)
        
        # Actualizar tamaño del contenedor
        self._container_size = (new_width, new_height)
    
    def _apply_dock(self):
        """Aplica la propiedad Dock al control."""
        if not self._tk_widget or self._dock == 'None':
            return
        
        self.master.update_idletasks()
        container_width = self.master.winfo_width()
        container_height = self.master.winfo_height()
        
        # Si el contenedor aún no tiene tamaño válido, reintentar
        if container_width <= 1 or container_height <= 1:
            self.master.after(50, self._apply_dock)
            return
        
        if self._dock == 'Top':
            self.Left = 0
            self.Top = 0
            self.Width = container_width
            self._tk_widget.place(x=0, y=0, width=container_width, height=self.Height)
        elif self._dock == 'Bottom':
            self.Left = 0
            self.Top = container_height - self.Height
            self.Width = container_width
            self._tk_widget.place(x=0, y=self.Top, width=container_width, height=self.Height)
        elif self._dock == 'Left':
            self.Left = 0
            self.Top = 0
            self.Height = container_height
            self._tk_widget.place(x=0, y=0, width=self.Width, height=container_height)
        elif self._dock == 'Right':
            self.Left = container_width - self.Width
            self.Top = 0
            self.Height = container_height
            self._tk_widget.place(x=self.Left, y=0, width=self.Width, height=container_height)
        elif self._dock == 'Fill':
            self.Left = 0
            self.Top = 0
            self.Width = container_width
            self.Height = container_height
            self._tk_widget.place(x=0, y=0, width=container_width, height=container_height)
    
    def _on_dock_resize(self, event=None):
        """Maneja el redimensionamiento del contenedor para aplicar Dock."""
        if not self._tk_widget or self._dock == 'None':
            return
        
        # Filtrar eventos: solo procesar si es del master o no hay evento
        if event and hasattr(event, 'widget'):
            if event.widget != self.master and not self._is_ancestor(event.widget, self.master):
                return
        
        self._apply_dock()
    
    def _is_ancestor(self, widget, potential_ancestor):
        """Verifica si widget es un ancestro de potential_ancestor."""
        try:
            current = potential_ancestor
            while current:
                if current == widget:
                    return True
                current = current.master if hasattr(current, 'master') else None
            return False
        except:
            return False
    
    @property
    def Anchor(self):
        """Obtiene la configuración de anclaje del control.
        
        Returns:
            Lista de strings con los bordes anclados: ['Top', 'Left', 'Bottom', 'Right']
        """
        return self._anchor.copy()
    
    @Anchor.setter
    def Anchor(self, value):
        """Establece la configuración de anclaje del control.
        
        Args:
            value: Lista de strings o string separado por comas con los bordes a anclar.
                   Valores válidos: 'Top', 'Bottom', 'Left', 'Right'
                   Ejemplos: ['Top', 'Left'], 'Top,Left', ['Top', 'Bottom', 'Left', 'Right']
        """
        # Limpiar Dock si se establece Anchor
        if self._dock != 'None':
            self._dock = 'None'
            if hasattr(self, '_dock_resize_bound'):
                delattr(self, '_dock_resize_bound')
        
        # Convertir string a lista si es necesario
        if isinstance(value, str):
            value = [v.strip() for v in value.split(',')]
        
        # Validar valores
        valid_anchors = ['Top', 'Bottom', 'Left', 'Right']
        self._anchor = [v for v in value if v in valid_anchors]
        
        # Recalcular distancias iniciales
        if hasattr(self, 'Width') and hasattr(self, 'Height'):
            self._calculate_initial_distances()
    
    @property
    def Dock(self):
        """Obtiene la configuración de acoplamiento del control.
        
        Returns:
            String con el lado acoplado: 'None', 'Top', 'Bottom', 'Left', 'Right', 'Fill'
        """
        return self._dock
    
    @Dock.setter
    def Dock(self, value):
        """Establece la configuración de acoplamiento del control.
        
        Args:
            value: String con el lado al que acoplar el control.
                   Valores válidos: 'None', 'Top', 'Bottom', 'Left', 'Right', 'Fill'
        """
        # Limpiar Anchor si se establece Dock
        if value != 'None':
            self._anchor = []
            self._initial_distance = {}
            if hasattr(self, '_resize_bound'):
                delattr(self, '_resize_bound')
        
        # Validar valor
        valid_docks = ['None', 'Top', 'Bottom', 'Left', 'Right', 'Fill']
        if value in valid_docks:
            self._dock = value
            # Aplicar dock inmediatamente si el widget ya existe
            if self._tk_widget and value != 'None':
                self._apply_dock()
    
    def _apply_autosize(self):
        """Aplica el redimensionamiento automático basado en el contenido.
        
        Este método calcula el tamaño necesario para mostrar todo el contenido
        del control y ajusta Width y Height respetando MinimumSize y MaximumSize.
        
        Debe ser sobrescrito por controles específicos que necesiten
        comportamiento personalizado de AutoSize.
        """
        if not self.AutoSize or not self._tk_widget:
            return
        
        # Forzar actualización del widget para obtener dimensiones correctas
        self._tk_widget.update_idletasks()
        
        # Obtener tamaño requerido del widget
        required_width = self._tk_widget.winfo_reqwidth()
        required_height = self._tk_widget.winfo_reqheight()
        
        # Aplicar restricciones de MinimumSize
        if self.MinimumSize:
            min_width, min_height = self.MinimumSize
            required_width = max(required_width, min_width)
            required_height = max(required_height, min_height)
        
        # Aplicar restricciones de MaximumSize
        if self.MaximumSize:
            max_width, max_height = self.MaximumSize
            if max_width > 0:
                required_width = min(required_width, max_width)
            if max_height > 0:
                required_height = min(required_height, max_height)
        
        # Actualizar dimensiones
        self.Width = required_width
        self.Height = required_height

    def _apply_visual_config(self):
        """Aplica la configuración visual común a todos los controles.
        
        Este método configura las propiedades visuales básicas como colores,
        fuente, estado habilitado, etc. Puede ser sobrescrito por controles
        específicos que necesiten configuraciones adicionales.
        """
        if not self._tk_widget:
            return
        
        config = {}
        
        # Aplicar colores
        if self.BackColor is not None:
            config['bg'] = self.BackColor
        if self.ForeColor is not None:
            config['fg'] = self.ForeColor
        
        # Aplicar fuente
        if self.Font is not None:
            config['font'] = self.Font
        
        # Aplicar estado habilitado/deshabilitado
        if not self.Enabled:
            config['state'] = 'disabled'
        else:
            config['state'] = 'normal'
        
        # Aplicar borde/relieve
        if self.BorderStyle is not None:
            relief_map = {
                'None': 'flat', 'Fixed3D': 'ridge', 'FixedSingle': 'solid',
                'flat': 'flat', 'groove': 'groove', 'raised': 'raised',
                'ridge': 'ridge', 'solid': 'solid', 'sunken': 'sunken'
            }
            config['relief'] = relief_map.get(self.BorderStyle, 'flat')
        
        # Aplicar imagen de fondo
        if self.BackgroundImage is not None:
            config['image'] = self.BackgroundImage
        
        # Aplicar configuración al widget
        if config:
            try:
                self._tk_widget.config(**config)
            except tk.TclError:
                # Algunos widgets no soportan todas las opciones
                # Intentar aplicar opciones una por una
                for key, value in config.items():
                    try:
                        self._tk_widget.config(**{key: value})
                    except tk.TclError:
                        pass  # Ignorar opciones no soportadas

class Button(ControlBase):
    """Representa un botón (CommandButton en VB6, Button en VB.NET)."""
    
    def __init__(self, master_form, props=None):
        """Inicializa un Button.
        
        Args:
            master_form: El formulario o contenedor padre
            props: Diccionario opcional con propiedades iniciales
                   Ejemplo: {'Text': 'Click', 'Left': 10, 'Top': 20, 'BackColor': 'blue'}
                   Use {'UseSystemStyles': True} para aplicar estilos del sistema automáticamente
        """
        # Valores por defecto
        defaults = {
            'Left': 10,
            'Top': 10,
            'Width': 100,
            'Height': 30,
            'Name': '',
            'Text': 'Button',
            'Enabled': True,
            'Visible': True,
            'DialogResult': None,
            'Font': None,
            'ForeColor': None,
            'BackColor': None,
            'FlatStyle': 'Standard',
            'Image': None,
            'ImageAlign': 'left',
            'TextImageRelation': 'left',
            'UseCompatibleTextRendering': False,
            'AutoSize': False,
            'MinimumSize': None,
            'MaximumSize': None,
            'ToolTipText': ''
        }
        
        # Combinar valores por defecto con props proporcionadas
        if props:
            # Extraer UseSystemStyles antes de actualizar defaults
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            # Aplicar estilos del sistema si está habilitado
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Button", use_system_styles=True)
        else:
            # Aplicar estilos del sistema según configuración global
            SystemStyles.ApplyToDefaults(defaults, control_type="Button")
        
        # Inicializar ControlBase con posición
        super().__init__(master_form._root, defaults['Left'], defaults['Top'])
        
        # Establecer propiedades básicas
        self.Name = defaults['Name']
        self._text_value = defaults['Text']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.DialogResult = defaults['DialogResult']
        self.Font = defaults['Font']
        self.ForeColor = defaults['ForeColor']
        self.BackColor = defaults['BackColor']
        self._flatstyle = defaults['FlatStyle']
        self.Image = defaults['Image']
        self.ImageAlign = defaults['ImageAlign']
        self.TextImageRelation = defaults['TextImageRelation']
        self.UseCompatibleTextRendering = defaults['UseCompatibleTextRendering']
        self.AutoSize = defaults['AutoSize']
        self.MinimumSize = defaults['MinimumSize']
        self.MaximumSize = defaults['MaximumSize']
        
        # Location como tupla
        self.Location = (self.Left, self.Top)
        
        # Crear el widget Tkinter
        self._tk_widget = tk.Button(
            self.master, 
            text=self._text_value, 
            command=self._handle_click_event
        )
        
        # Aplicar configuraciones visuales
        self._apply_visual_config()
        
        # Establecer tooltip
        if defaults['ToolTipText']:
            self.ToolTipText = defaults['ToolTipText']
        
        # Bind common events
        self._bind_common_events()
        
        # Unbind Button-1 because tk.Button uses command for clicks
        # This prevents double firing of the Click event
        if self._tk_widget:
            self._tk_widget.unbind('<Button-1>')
        
        # Posicionar si visible
        if self.Visible:
            if self.AutoSize:
                self._apply_autosize()
            self._place_control(self.Width, self.Height)
        else:
            self._tk_widget.place_forget()
    
    def _apply_visual_config(self):
        """Aplica la configuración visual al widget."""
        # Call base method first
        super()._apply_visual_config()
        
        # Apply Button-specific configurations
        config = {}
        if self.Image:
            config['image'] = self.Image
        if self.TextImageRelation:
            config['compound'] = self.TextImageRelation
        # Map FlatStyle to relief
        relief_map = {'Standard': 'raised', 'Flat': 'flat', 'Popup': 'ridge', 'System': 'raised'}
        config['relief'] = relief_map.get(self._flatstyle, 'raised')
        
        if config:
            try:
                self._tk_widget.config(**config)
            except tk.TclError:
                pass  # Ignore unsupported options

    def _handle_click_event(self):
        """Función intermediaria para ejecutar el método Click asignado."""
        self.Click()

    def set_Enabled(self, enabled):
        """Establece si el botón está habilitado."""
        self.Enabled = enabled
        self._tk_widget.config(state='normal' if enabled else 'disabled')

    @property
    def Text(self):
        """Property getter para Text en Button."""
        return self._text_value
    
    @Text.setter
    def Text(self, value):
        """Property setter para Text en Button."""
        self._text_value = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._tk_widget.config(text=value)
            # Aplicar AutoSize si está habilitado
            if self.AutoSize:
                self._apply_autosize()
                # Reposicionar con nuevo tamaño
                if self.Visible:
                    self._place_control(self.Width, self.Height)
    
    @property
    def FlatStyle(self):
        """Property getter para FlatStyle."""
        return self._flatstyle
    
    @FlatStyle.setter
    def FlatStyle(self, value):
        """Property setter para FlatStyle."""
        self._flatstyle = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            relief_map = {'Standard': 'raised', 'Flat': 'flat', 'Popup': 'ridge', 'System': 'raised'}
            self._tk_widget.config(relief=relief_map.get(value, 'raised'))

class Label(ControlBase):
    """Representa una etiqueta de texto."""
    
    def __init__(self, master_form, props=None):
        """Inicializa un Label.
        
        Args:
            master_form: El formulario o contenedor padre
            props: Diccionario opcional con propiedades iniciales
                   Use {'UseSystemStyles': True} para aplicar estilos del sistema automáticamente
        """
        # Valores por defecto
        defaults = {
            'Left': 10,
            'Top': 50,
            'Width': None,
            'Height': None,
            'Name': '',
            'Text': 'Label',
            'Enabled': True,
            'Visible': True,
            'Font': None,
            'ForeColor': None,
            'BackColor': None,
            'BorderStyle': None,
            'TextAlign': 'left',
            'AutoSize': True,
            'MinimumSize': None,
            'MaximumSize': None,
            'UseMnemonic': False,
            'Padding': (0, 0),
            'Margin': (0, 0),
            'ToolTipText': ''
        }
        
        if props:
            # Extraer UseSystemStyles antes de actualizar defaults
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            # Aplicar estilos del sistema si está habilitado
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Control", use_system_styles=True)
        else:
            # Aplicar estilos del sistema según configuración global
            SystemStyles.ApplyToDefaults(defaults, control_type="Control")
        
        # Resolve master widget
        master_widget = getattr(master_form, '_root', getattr(master_form, '_tk_widget', getattr(master_form, '_frame', master_form)))
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Propiedades VB
        self.Name = defaults['Name']
        self._text_value = defaults['Text']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.Font = defaults['Font']
        self.ForeColor = defaults['ForeColor']
        self.BackColor = defaults['BackColor']
        self.BorderStyle = defaults['BorderStyle']
        self.TextAlign = defaults['TextAlign']
        self.AutoSize = defaults['AutoSize']
        self.MinimumSize = defaults['MinimumSize']
        self.MaximumSize = defaults['MaximumSize']
        self.UseMnemonic = defaults['UseMnemonic']
        self.Padding = defaults['Padding']
        self.Margin = defaults['Margin']
        
        # Eventos VB
        self.TextChanged = lambda: None
        
        # Procesar UseMnemonic
        display_text = self._text_value
        underline = -1
        if self.UseMnemonic and '&' in self._text_value:
            idx = self._text_value.find('&')
            if idx + 1 < len(self._text_value):
                underline = idx
                display_text = self._text_value[:idx] + self._text_value[idx+1:]
        
        # Crear el widget Tkinter
        self._tk_widget = tk.Label(self.master, text=display_text, underline=underline)
        
        # Aplicar propiedades
        if self.ForeColor:
            self._tk_widget.config(fg=self.ForeColor)
        if self.BackColor:
            self._tk_widget.config(bg=self.BackColor)
        if self.BorderStyle:
            # Mapear BorderStyle de VB.NET a tkinter
            relief_map = {
                'None': 'flat', 'Fixed3D': 'ridge', 'FixedSingle': 'solid',
                'flat': 'flat', 'groove': 'groove', 'raised': 'raised',
                'ridge': 'ridge', 'solid': 'solid', 'sunken': 'sunken'
            }
            self._tk_widget.config(relief=relief_map.get(self.BorderStyle, 'flat'))
        if self.Font:
            self._tk_widget.config(font=self.Font)
        
        # Alineación
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
        
        # Establecer tooltip
        if defaults['ToolTipText']:
            self.ToolTipText = defaults['ToolTipText']
        
        # Bind events
        self._bind_common_events()
        self._tk_widget.bind('<Button-1>', self._on_click)
        self._tk_widget.bind('<Double-Button-1>', self._on_double_click)
        self._tk_widget.bind('<Configure>', self._on_paint)  # Placeholder for Paint
        
        # AutoSize: ajustar tamaño automáticamente según contenido
        if self.AutoSize:
            self._apply_autosize()
            self._place_control(self.Width, self.Height)
        else:
            # Tamaño fijo
            if self.Width is None or self.Height is None:
                # Si no se especifica tamaño, usar auto
                self._place_control()
            else:
                self._place_control(self.Width, self.Height)

    def _on_click(self, event):
        """Handler for Click event."""
        self.Click()

    def _on_double_click(self, event):
        """Handler for DoubleClick event."""
        self.DoubleClick()

    def _on_paint(self, event):
        """Handler for Paint event (placeholder)."""
        self.Paint()

    def set_Text(self, new_text):
        """Método set para actualizar el texto en tiempo de ejecución."""
        self._text_value = new_text
        self._tk_widget.config(text=new_text)
        self.TextChanged()
        
        # Aplicar AutoSize si está habilitado
        if self.AutoSize:
            self._apply_autosize()
            # Reposicionar con nuevo tamaño
            if self.Visible:
                self._place_control(self.Width, self.Height)
    
    @property
    def Text(self):
        """Property getter para Text en Label."""
        return self._text_value
    
    @Text.setter
    def Text(self, value):
        """Property setter para Text en Label."""
        self.set_Text(value)
        
class TextBox(ControlBase):
    """Representa una caja de texto simple."""
    
    def __init__(self, master_form, props=None):
        """Inicializa un TextBox.
        
        Args:
            master_form: El formulario o contenedor padre
            props: Diccionario opcional con propiedades iniciales
                   Use {'UseSystemStyles': True} para aplicar estilos del sistema automáticamente
        """
        # Valores por defecto
        defaults = {
            'Left': 10,
            'Top': 80,
            'Width': 200,
            'Height': 25,
            'Name': '',
            'Text': '',
            'Enabled': True,
            'Visible': True,
            'ReadOnly': False,
            'Multiline': False,
            'ScrollBars': None,
            'PasswordChar': '',
            'UseSystemPasswordChar': False,
            'MaxLength': 0,
            'TextAlign': 'left',
            'WordWrap': True,
            'AcceptsReturn': True,
            'AutoSize': False,
            'MinimumSize': None,
            'MaximumSize': None,
            'BackColor': None,
            'ForeColor': None,
            'Font': None
        }
        
        if props:
            # Extraer UseSystemStyles antes de actualizar defaults
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            # Aplicar estilos del sistema si está habilitado
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Window", use_system_styles=True)
        else:
            # Aplicar estilos del sistema según configuración global
            SystemStyles.ApplyToDefaults(defaults, control_type="Window")
        
        super().__init__(master_form._root, defaults['Left'], defaults['Top'])
        
        # Propiedades VB
        self.Name = defaults['Name']
        self._text_value = defaults['Text']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.ReadOnly = defaults['ReadOnly']
        self.Multiline = defaults['Multiline']
        self.ScrollBars = defaults['ScrollBars']
        self.PasswordChar = defaults['PasswordChar']
        self.UseSystemPasswordChar = defaults['UseSystemPasswordChar']
        self.MaxLength = defaults['MaxLength']
        self.TextAlign = defaults['TextAlign']
        self.WordWrap = defaults['WordWrap']
        self.AcceptsReturn = defaults['AcceptsReturn']
        self.AutoSize = defaults['AutoSize']
        self.MinimumSize = defaults['MinimumSize']
        self.MaximumSize = defaults['MaximumSize']
        self.BackColor = defaults['BackColor']
        self.ForeColor = defaults['ForeColor']
        self.Font = defaults['Font']
        
        # Eventos VB (callbacks)
        self.TextChanged = lambda: None
        self.MouseMove = lambda x, y: None
        
        # Crear el widget Tkinter
        if self.Multiline:
            self._tk_widget = tk.Text(self.master, height=self.Height//15, wrap='word' if self.WordWrap else 'none')
            if self.ScrollBars in ['vertical', 'both']:
                vscroll = tk.Scrollbar(self.master, command=self._tk_widget.yview)
                self._tk_widget.config(yscrollcommand=vscroll.set)
                vscroll.place(x=self.Left+self.Width-15, y=self.Top, height=self.Height)
            if self.ScrollBars in ['horizontal', 'both']:
                hscroll = tk.Scrollbar(self.master, orient='horizontal', command=self._tk_widget.xview)
                self._tk_widget.config(xscrollcommand=hscroll.set)
                hscroll.place(x=self.Left, y=self.Top+self.Height-15, width=self.Width)
            self._tk_widget.insert('1.0', self._text_value)
            if self.ReadOnly:
                self._tk_widget.config(state='disabled')
            
            # Bind events for Text widget
            self._tk_widget.bind('<<Modified>>', self._on_text_changed)
            self._tk_widget.bind('<KeyRelease>', self._on_key_up)
            self._tk_widget.bind('<Button-1>', self._on_click)
            self._tk_widget.bind('<Double-Button-1>', self._on_double_click)
            self._tk_widget.bind('<Motion>', self._on_mouse_move)
        else:
            self._text_var = tk.StringVar(value=self._text_value)
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
        
        # Aplicar configuraciones de estilo
        config = {}
        if self.BackColor:
            config['bg'] = self.BackColor
        if self.ForeColor:
            config['fg'] = self.ForeColor
        if self.Font:
            config['font'] = self.Font
        if config:
            try:
                self._tk_widget.config(**config)
            except tk.TclError:
                pass  # Algunos widgets no soportan todas las opciones
        
        # Aplicar alineación
        if self.TextAlign == 'center':
            self._tk_widget.config(justify='center')
        elif self.TextAlign == 'right':
            self._tk_widget.config(justify='right')
        
        # Aplicar Enabled/Visible
        if not self.Enabled:
            self._tk_widget.config(state='disabled')
        if not self.Visible:
            self._tk_widget.place_forget()
        
        if self.AutoSize:
            self._apply_autosize_textbox()
            
        self._place_control(self.Width, self.Height if not self.Multiline else self.Height)

    def _on_text_changed(self, event=None):
        """Handler for TextChanged event (Text widget)."""
        self.TextChanged()
        # Reset modified flag
        self._tk_widget.edit_modified(False)

    def _on_text_changed_entry(self, *args):
        """Handler for TextChanged event (Entry widget)."""
        self.TextChanged()

    def _on_mouse_move(self, event):
        """Handler for MouseMove event."""
        self.MouseMove(event.x, event.y)

    def _validate_length(self, new_text):
        return len(new_text) <= self.MaxLength

    def get_Text(self):
        """Obtiene el texto del TextBox."""
        if self.Multiline:
            return self._tk_widget.get('1.0', 'end-1c')
        else:
            return self._text_var.get()

    def set_Text(self, new_text):
        """Establece el texto del TextBox."""
        self._text_value = new_text
        if self.Multiline:
            self._tk_widget.delete('1.0', 'end')
            self._tk_widget.insert('1.0', new_text)
        else:
            self._text_var.set(new_text)
        # Aplicar AutoSize si está habilitado
        if self.AutoSize:
            self._apply_autosize_textbox()
    
    def _apply_autosize_textbox(self):
        """Aplica AutoSize específico para TextBox.
        
        - Para TextBox de una línea: Solo ajusta altura según la fuente
        - Para TextBox multilínea: Ajusta altura para mostrar todo el texto
        """
        if not self.AutoSize or not self._tk_widget:
            return
        
        self._tk_widget.update_idletasks()
        
        if self.Multiline:
            # Para multilínea, ajustar altura según número de líneas
            num_lines = int(self._tk_widget.index('end-1c').split('.')[0])
            # Estimar altura por línea (aproximadamente 20-25 píxeles por línea)
            line_height = 22
            required_height = num_lines * line_height + 10  # +10 para padding
            
            # Mantener ancho, solo ajustar altura
            self.Height = required_height
        else:
            # Para una línea, solo ajustar altura según fuente
            required_height = self._tk_widget.winfo_reqheight()
            self.Height = required_height
        
        # Aplicar restricciones de MinimumSize
        if self.MinimumSize:
            _, min_height = self.MinimumSize
            self.Height = max(self.Height, min_height)
        
        # Aplicar restricciones de MaximumSize
        if self.MaximumSize:
            _, max_height = self.MaximumSize
            if max_height > 0:
                self.Height = min(self.Height, max_height)
        
        # Reposicionar con nuevo tamaño
        if self.Visible:
            self._place_control(self.Width, self.Height)
    
    @property
    def Text(self):
        """Property getter para Text."""
        return self.get_Text()
    
    @Text.setter
    def Text(self, value):
        """Property setter para Text que llama a set_Text()."""
        self.set_Text(value)

class ComboBox(ControlBase):
    """Representa un ComboBox (desplegable)."""
    
    def __init__(self, master_form, props=None):
        """Inicializa un ComboBox.
        
        Args:
            master_form: El formulario o contenedor padre
            props: Diccionario opcional con propiedades iniciales
                   Use {'UseSystemStyles': True} para aplicar estilos del sistema automáticamente
        """
        # Valores por defecto
        defaults = {
            'Left': 10,
            'Top': 110,
            'Width': 200,
            'Name': '',
            'Items': None,
            'DataSource': None,
            'DisplayMember': '',
            'ValueMember': '',
            'SelectedItem': None,
            'SelectedValue': None,
            'SelectedIndex': -1,
            'Text': '',
            'DropDownStyle': 'readonly',
            'DroppedDown': False,
            'MaxDropDownItems': 10,
            'MaxLength': 0,
            'Enabled': True,
            'Visible': True,
            'Font': None,
            'ForeColor': None,
            'BackColor': None
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Control", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Control")
        
        super().__init__(master_form._root, defaults['Left'], defaults['Top'])
        
        # Propiedades VB
        self.Name = defaults['Name']
        self.Items = defaults['Items'] or []
        self.DataSource = defaults['DataSource']
        self.DisplayMember = defaults['DisplayMember']
        self.ValueMember = defaults['ValueMember']
        self.SelectedItem = defaults['SelectedItem']
        self.SelectedValue = defaults['SelectedValue']
        self.SelectedIndex = defaults['SelectedIndex']
        self._text_value = defaults['Text']
        self.DropDownStyle = defaults['DropDownStyle']
        self.DroppedDown = defaults['DroppedDown']
        self.MaxDropDownItems = defaults['MaxDropDownItems']
        self.MaxLength = defaults['MaxLength']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.Font = defaults['Font']
        self.ForeColor = defaults['ForeColor']
        self.BackColor = defaults['BackColor']
        
        # Eventos VB (callbacks)
        self.SelectedIndexChanged = lambda: None
        self.SelectionChangeCommitted = lambda: None
        self.TextChanged = lambda: None
        self.DropDown = lambda: None
        self.DropDownClosed = lambda: None
        self.Validating = lambda: None
        self.DrawItem = lambda index, graphics, bounds, state: None  # Placeholder
        
        self.Width = defaults['Width']
        self.Height = 25  # Fixed height for ComboBox
        
        # Si DataSource, poblar Items
        if self.DataSource:
            self._populate_from_datasource()
        
        self._selected_var = tk.StringVar(value=self.Text)
        
        # Crear el widget Tkinter
        self._tk_widget = ttk.Combobox(self.master, textvariable=self._selected_var, values=self.Items, state=self.DropDownStyle)
        self._tk_widget.config(height=self.MaxDropDownItems)
        if self.MaxLength > 0:
            vcmd = (self.master.register(self._validate_length), '%P')
            self._tk_widget.config(validate='key', validatecommand=vcmd)
        
        # Aplicar estilos
        config = {}
        if self.Font:
            config['font'] = self.Font
        if self.BackColor:
            config['background'] = self.BackColor
        if self.ForeColor:
            config['foreground'] = self.ForeColor
        if config:
            try:
                self._tk_widget.config(**config)
            except tk.TclError:
                pass  # ttk.Combobox no soporta todas las opciones
        
        # Aplicar Enabled/Visible
        if not self.Enabled:
            self._tk_widget.config(state='disabled')
        if not self.Visible:
            self._tk_widget.place_forget()
        
        self._place_control(self.Width, 25) # Altura fija
        
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
        """Pobla Items desde DataSource usando DisplayMember."""
        if self.DataSource and self.DisplayMember:
            self.Items = [getattr(item, self.DisplayMember) for item in self.DataSource]

    def _validate_length(self, new_text):
        return len(new_text) <= self.MaxLength

    def get_SelectedItem(self):
        """Obtiene el elemento seleccionado."""
        idx = self._tk_widget.current()
        if idx >= 0:
            return self.Items[idx]
        return None

    def set_SelectedItem(self, item):
        """Establece el elemento seleccionado."""
        try:
            idx = self.Items.index(item)
            self._tk_widget.current(idx)
        except ValueError:
            pass

    def get_SelectedValue(self):
        """Obtiene el valor del ValueMember del elemento seleccionado."""
        if self.DataSource and self.ValueMember and self.get_SelectedItem():
            idx = self._tk_widget.current()
            if idx >= 0:
                return getattr(self.DataSource[idx], self.ValueMember)
        return self.get_SelectedItem()

    def get_SelectedIndex(self):
        """Obtiene el índice del elemento seleccionado."""
        return self._tk_widget.current()

    def set_SelectedIndex(self, index):
        """Establece el índice seleccionado."""
        if 0 <= index < len(self.Items):
            self._tk_widget.current(index)

    def _on_selected_index_changed(self, event=None):
        """Handler for SelectedIndexChanged event."""
        self.SelectedIndexChanged()
        self.SelectionChangeCommitted()

    def _on_text_changed(self, *args):
        """Handler for TextChanged event."""
        self.TextChanged()

    def _on_enter(self, event):
        """Handler for Enter (GotFocus) event."""
        self.Enter()

    def _on_leave(self, event):
        """Handler for Leave (LostFocus) event."""
        self.Leave()
        self.Validating()

    def _on_key_down(self, event):
        """Handler for KeyDown event."""
        self.KeyDown(event.keysym)

    def _on_key_press(self, event):
        """Handler for KeyPress event."""
        self.KeyPress(event.char)
    
    @property
    def Text(self):
        """Property getter para Text en ComboBox."""
        if hasattr(self, '_tk_widget') and self._tk_widget:
            return self._tk_widget.get()
        return self._text_value
    
    @Text.setter
    def Text(self, value):
        """Property setter para Text en ComboBox."""
        self._text_value = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._tk_widget.set(value)

class ListBoxObjectCollection:
    """Colección de elementos para ListBox."""
    def __init__(self, owner):
        self.owner = owner
        self._items = []

    def Add(self, item):
        self._items.append(item)
        if hasattr(self.owner, '_tk_widget') and self.owner._tk_widget:
            self.owner._tk_widget.insert(tk.END, item)
        return len(self._items) - 1

    def Clear(self):
        self._items.clear()
        if hasattr(self.owner, '_tk_widget') and self.owner._tk_widget:
            self.owner._tk_widget.delete(0, tk.END)

    def Remove(self, item):
        if item in self._items:
            index = self._items.index(item)
            self._items.remove(item)
            if hasattr(self.owner, '_tk_widget') and self.owner._tk_widget:
                self.owner._tk_widget.delete(index)

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)
    
    def __iter__(self):
        return iter(self._items)
    
    def append(self, item):
        """Compatibility with list."""
        self.Add(item)

class ListBox(ControlBase):
    """Representa un ListBox."""
    
    def __init__(self, master_form, props=None):
        """Inicializa un ListBox.
        
        Args:
            master_form: El formulario o contenedor padre
            props: Diccionario opcional con propiedades iniciales
        """
        # Valores por defecto
        defaults = {
            'Left': 10,
            'Top': 170,
            'Width': 200,
            'Height': 100,
            'Name': '',
            'Items': None,
            'DataSource': None,
            'DisplayMember': '',
            'ValueMember': '',
            'SelectedIndex': -1,
            'SelectionMode': 'One',
            'TopIndex': 0,
            'IntegralHeight': True,
            'MultiColumn': False,
            'ScrollAlwaysVisible': False,
            'Enabled': True,
            'Font': None,
            'ForeColor': None,
            'BackColor': None
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Window", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Window")
        
        super().__init__(master_form._root, defaults['Left'], defaults['Top'])
        
        self.Name = defaults['Name']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Items = ListBoxObjectCollection(self)
        if defaults['Items']:
            for item in defaults['Items']:
                self.Items.Add(item)
                
        self.DataSource = defaults['DataSource']
        self.DisplayMember = defaults['DisplayMember']
        self.ValueMember = defaults['ValueMember']
        self.SelectedIndex = defaults['SelectedIndex']
        self.SelectionMode = defaults['SelectionMode']
        self.TopIndex = defaults['TopIndex']
        self.IntegralHeight = defaults['IntegralHeight']
        self.MultiColumn = defaults['MultiColumn']
        self.ScrollAlwaysVisible = defaults['ScrollAlwaysVisible']
        self.Enabled = defaults['Enabled']
        self.Font = defaults['Font']
        self.ForeColor = defaults['ForeColor']
        self.BackColor = defaults['BackColor']
        
        # Eventos VB (callbacks)
        self.SelectedIndexChanged = lambda: None
        self.SelectedValueChanged = lambda: None
        self.Format = lambda item: None  # placeholder
        self.DrawItem = lambda index, graphics, bounds, state: None  # placeholder
        
        # If DataSource, populate Items
        if self.DataSource and self.DisplayMember:
            self.Items.Clear()
            for item in self.DataSource:
                self.Items.Add(getattr(item, self.DisplayMember))
        
        # Crear el widget Tkinter
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
            vscroll.place(x=self.Left+self.Width-15, y=self.Top, height=self.Height)
            if self.MultiColumn:  # For multi-column, add horizontal scroll
                hscroll = tk.Scrollbar(self.master, orient='horizontal', command=self._tk_widget.xview)
                self._tk_widget.config(xscrollcommand=hscroll.set)
                hscroll.place(x=self.Left, y=self.Top+self.Height-15, width=self.Width)
        
        # Apply Font, ForeColor, BackColor, Enabled
        config = {}
        if self.Font:
            config['font'] = self.Font
        if self.ForeColor:
            config['fg'] = self.ForeColor
        if self.BackColor:
            config['bg'] = self.BackColor
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
        """Obtiene el elemento seleccionado."""
        selection = self._tk_widget.curselection()
        if selection:
            return self._tk_widget.get(selection[0])
        return None

    def get_SelectedIndex(self):
        """Obtiene el índice del elemento seleccionado."""
        selection = self._tk_widget.curselection()
        return selection[0] if selection else -1

    def set_SelectedIndex(self, index):
        """Establece el índice seleccionado."""
        if 0 <= index < self._tk_widget.size():
            self._tk_widget.selection_set(index)

    def get_SelectedItems(self):
        """Obtiene la lista de elementos seleccionados."""
        selections = self._tk_widget.curselection()
        return [self._tk_widget.get(i) for i in selections]

    def get_SelectedIndices(self):
        """Obtiene la lista de índices seleccionados."""
        return list(self._tk_widget.curselection())

    def get_SelectedValue(self):
        """Obtiene el valor del ValueMember del elemento seleccionado."""
        if self.DataSource and self.ValueMember:
            idx = self.get_SelectedIndex()
            if idx >= 0:
                return getattr(self.DataSource[idx], self.ValueMember)
        return self.get_SelectedItem()

    def set_TopIndex(self, index):
        """Establece el índice del primer elemento visible."""
        self.TopIndex = index
        self._tk_widget.yview(index)
    
    def _on_selected_index_changed(self, event=None):
        """Handler for SelectedIndexChanged event."""
        self.SelectedIndexChanged()
        self.SelectedValueChanged()

    @property
    def SelectedItem(self):
        """Obtiene el elemento seleccionado."""
        return self.get_SelectedItem()

    @property
    def SelectedIndex(self):
        """Obtiene o establece el índice seleccionado."""
        return self.get_SelectedIndex()

    @SelectedIndex.setter
    def SelectedIndex(self, value):
        self.set_SelectedIndex(value)

    @property
    def SelectedItems(self):
        """Obtiene los elementos seleccionados."""
        return self.get_SelectedItems()

    @property
    def SelectedIndices(self):
        """Obtiene los índices seleccionados."""
        return self.get_SelectedIndices()

    @property
    def SelectedValue(self):
        """Obtiene el valor seleccionado."""
        return self.get_SelectedValue()

class CheckBox(ControlBase):
    """Representa un CheckBox."""
    
    def __init__(self, master_form, props=None):
        """Inicializa un CheckBox.
        
        Args:
            master_form: El formulario o contenedor padre
            props: Diccionario opcional con propiedades iniciales
        """
        # Valores por defecto
        defaults = {
            'Left': 10,
            'Top': 140,
            'Width': 100,
            'Height': 25,
            'Name': '',
            'Text': 'CheckBox',
            'Checked': False,
            'CheckState': 0,
            'ThreeState': False,
            'Enabled': True,
            'Visible': True,
            'Font': None,
            'ForeColor': None,
            'BackColor': None,
            'TextAlign': 'w',
            'Appearance': 'Normal',
            'AutoSize': False
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Control", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Control")
        
        super().__init__(master_form._root, defaults['Left'], defaults['Top'])
        
        self.Name = defaults['Name']
        self._text_value = defaults['Text']
        self._checked_value = defaults['Checked']
        self._checkstate_value = defaults['CheckState']
        self.ThreeState = defaults['ThreeState']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.Font = defaults['Font']
        self.ForeColor = defaults['ForeColor']
        self.BackColor = defaults['BackColor']
        self.TextAlign = defaults['TextAlign']
        self.Appearance = defaults['Appearance']
        self.AutoSize = defaults['AutoSize']
        
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        
        self.Location = (self.Left, self.Top)
        
        # Variable based on ThreeState
        if self.ThreeState:
            self._state_var = tk.IntVar(value=self._checkstate_value)
        else:
            self._state_var = tk.BooleanVar(value=self._checked_value)
        
        # Eventos VB
        self.CheckedChanged = lambda: None
        self.CheckStateChanged = lambda: None

        # Crear el widget Tkinter
        self._tk_widget = tk.Checkbutton(self.master, text=self._text_value, variable=self._state_var, command=self._on_check_click)
        
        # Aplicar configuraciones
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
        
        # Posicionar si visible
        if self.Visible:
            if self.AutoSize:
                self._apply_autosize()
            self._place_control(self.Width, self.Height)
        else:
            self._tk_widget.place_forget()

    def _on_check_click(self):
        """Maneja el clic en el checkbox."""
        self.CheckedChanged()
        self.CheckStateChanged()

    def get_Checked(self):
        """Obtiene si está marcado (booleano)."""
        return bool(self._state_var.get())

    def set_Checked(self, value):
        """Establece si está marcado."""
        self._checked_value = value
        self._state_var.set(value)

    def get_CheckState(self):
        """Obtiene el estado de la casilla (0=Unchecked, 1=Checked, 2=Indeterminate)."""
        return self._state_var.get()

    def set_CheckState(self, value):
        """Establece el estado de la casilla."""
        self._checkstate_value = value
        self._state_var.set(value)
    
    @property
    def Checked(self):
        """Property getter para Checked."""
        return self.get_Checked()
    
    @Checked.setter
    def Checked(self, value):
        """Property setter para Checked que llama a set_Checked()."""
        self.set_Checked(value)
    
    @property
    def Text(self):
        """Property getter para Text en CheckBox."""
        return self._text_value
    
    @Text.setter
    def Text(self, value):
        """Property setter para Text en CheckBox."""
        self._text_value = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._tk_widget.config(text=value)
            
            # Aplicar AutoSize si está habilitado
            if self.AutoSize:
                self._apply_autosize()
                # Reposicionar con nuevo tamaño
                if self.Visible:
                    self._place_control(self.Width, self.Height)

class CheckedListBox(ControlBase):
    """Representa un CheckedListBox (lista con checkboxes)."""
    
    def __init__(self, master_form, props=None):
        """Inicializa un CheckedListBox.
        
        Args:
            master_form: El formulario o contenedor padre
            props: Diccionario opcional con propiedades iniciales
        """
        # Valores por defecto
        defaults = {
            'Left': 10,
            'Top': 200,
            'Width': 200,
            'Height': 100,
            'Name': '',
            'Items': None,
            'DataSource': None,
            'DisplayMember': '',
            'ValueMember': '',
            'SelectedItems': None,
            'SelectionMode': 'One',
            'CheckOnClick': True,
            'ThreeDCheckBoxes': True,
            'Enabled': True,
            'Visible': True,
            'Font': None,
            'ForeColor': None,
            'BackColor': None
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Window", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Window")
        
        super().__init__(master_form._root, defaults['Left'], defaults['Top'])
        
        self.Name = defaults['Name']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Items = defaults['Items'] or []
        self.DataSource = defaults['DataSource']
        self.DisplayMember = defaults['DisplayMember']
        self.ValueMember = defaults['ValueMember']
        self.SelectedItems = defaults['SelectedItems'] or []
        self.SelectionMode = defaults['SelectionMode']
        self.CheckOnClick = defaults['CheckOnClick']
        self.ThreeDCheckBoxes = defaults['ThreeDCheckBoxes']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.Font = defaults['Font']
        self.ForeColor = defaults['ForeColor']
        self.BackColor = defaults['BackColor']
        
        # Eventos VB (callbacks)
        self.ItemCheck = lambda item, new_value: None
        self.SelectedIndexChanged = lambda: None
        self.SelectedValueChanged = lambda: None
        self.Format = lambda item: None
        
        self.Location = (self.Left, self.Top)
        
        # If DataSource, populate Items
        if self.DataSource and self.DisplayMember:
            self.Items = [getattr(item, self.DisplayMember) for item in self.DataSource]
        
        # Crear un Frame para contener los Checkbuttons
        self._frame = tk.Frame(self.master, width=self.Width, height=self.Height)
        self._tk_widget = self._frame
        
        # Configurar frame
        if self.BackColor:
            self._frame.config(bg=self.BackColor)
        
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
        
        # Posicionar si visible
        if self.Visible:
            self._place_control(self.Width, self.Height)
            # Asegurar que el frame no se encoja
            self._frame.pack_propagate(False)
        else:
            self._frame.place_forget()

    def get_CheckedItems(self):
        """Obtiene la lista de elementos marcados."""
        return [self.Items[i] for i, var in enumerate(self._vars) if var.get()]

    def get_CheckedIndices(self):
        """Obtiene la lista de índices marcados."""
        return [i for i, var in enumerate(self._vars) if var.get()]

    def set_Checked(self, index, value):
        """Establece si un elemento está marcado."""
        self.ItemCheck(index, value)
        if 0 <= index < len(self._vars):
            self._vars[index].set(value)

    def get_SelectedItems(self):
        """Obtiene la lista de elementos seleccionados (igual a marcados para simplicidad)."""
        return self.get_CheckedItems()

    def get_SelectedIndices(self):
        """Obtiene la lista de índices seleccionados."""
        return self.get_CheckedIndices()
    
    def _on_item_check(self, index):
        """Handler for ItemCheck event."""
        self.ItemCheck(index, self._vars[index].get())
    
    def _on_selected_index_changed(self, event=None):
        """Handler for SelectedIndexChanged event."""
        self.SelectedIndexChanged()
        self.SelectedValueChanged()

class Panel(ControlBase):
    """Representa un Panel (contenedor)."""
    
    def __init__(self, master_form, props=None):
        """Inicializa un Panel.
        
        Args:
            master_form: El formulario o contenedor padre
            props: Diccionario opcional con propiedades iniciales
        """
        # Valores por defecto
        defaults = {
            'Left': 0,
            'Top': 0,
            'Width': 200,
            'Height': 100,
            'Name': '',
            'Text': '',
            'Enabled': True,
            'Visible': True,
            'BackColor': 'lightgray',
            'ForeColor': None,
            'BackgroundImage': None,
            'BorderStyle': 'flat',
            'AutoScroll': False,
            'AutoScrollOffset': (0, 0),
            'Dock': None,
            'Padding': (0, 0),
            'AutoSize': False,
            'AutoSizeMode': 'GrowOnly',
            'MinimumSize': None,
            'MaximumSize': None
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Control", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Control")
        
        # Resolve master widget
        master_widget = getattr(master_form, '_root', getattr(master_form, '_tk_widget', getattr(master_form, '_frame', master_form)))
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        self.Name = defaults['Name']
        self._text = defaults['Text']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.BackColor = defaults['BackColor']
        self.ForeColor = defaults['ForeColor']
        self.BackgroundImage = defaults['BackgroundImage']
        self.BorderStyle = defaults['BorderStyle']
        self.AutoScroll = defaults['AutoScroll']
        self.AutoScrollOffset = defaults['AutoScrollOffset']
        self.Dock = defaults['Dock']
        self._padding = defaults['Padding']
        self.AutoSize = defaults['AutoSize']
        self.AutoSizeMode = defaults['AutoSizeMode']
        self.MinimumSize = defaults['MinimumSize']
        self.MaximumSize = defaults['MaximumSize']
        self._original_size = (defaults['Width'], defaults['Height'])
        
        self.Location = (self.Left, self.Top)
        
        # Crear el widget Tkinter (Frame o LabelFrame según haya título)
        padx, pady = self.Padding
        
        # Mapear BorderStyle de VB.NET a tkinter
        relief_map = {
            'None': 'flat',
            'Fixed3D': 'ridge',
            'FixedSingle': 'solid',
            'flat': 'flat',
            'groove': 'groove',
            'raised': 'raised',
            'ridge': 'ridge',
            'solid': 'solid',
            'sunken': 'sunken'
        }
        
        config = {
            'width': self.Width,
            'height': self.Height,
            'bg': self.BackColor,
            'relief': relief_map.get(self.BorderStyle, 'flat'),
            'padx': padx,
            'pady': pady
        }
        
        # Si BorderStyle es 'FixedSingle' o 'solid', añadir borde
        if self.BorderStyle in ['FixedSingle', 'solid']:
            config['borderwidth'] = 1
        elif self.BorderStyle != 'None' and self.BorderStyle != 'flat':
            config['borderwidth'] = 2
        else:
            config['borderwidth'] = 0
        
        # Crear widget principal (Frame o LabelFrame)
        if self._text:
            config['text'] = self._text
            if self.BackgroundImage:
                config['image'] = self.BackgroundImage
            self._tk_widget = tk.LabelFrame(self.master, **config)
        else:
            if self.BackgroundImage:
                config['image'] = self.BackgroundImage
            self._tk_widget = tk.Frame(self.master, **config)
        
        # Asegurar que el frame no se encoja
        self._tk_widget.pack_propagate(False)
        self._tk_widget.grid_propagate(False)
        
        # Si AutoScroll está activado, crear estructura con Canvas y Scrollbars
        if self.AutoScroll:
            # Canvas para contenido desplazable
            self._canvas = tk.Canvas(
                self._tk_widget,
                bg=self.BackColor,
                highlightthickness=0
            )
            
            # Scrollbars
            self._v_scrollbar = tk.Scrollbar(
                self._tk_widget,
                orient='vertical',
                command=self._canvas.yview
            )
            self._h_scrollbar = tk.Scrollbar(
                self._tk_widget,
                orient='horizontal',
                command=self._canvas.xview
            )
            
            # Configurar canvas con scrollbars
            self._canvas.configure(
                yscrollcommand=self._v_scrollbar.set,
                xscrollcommand=self._h_scrollbar.set
            )
            
            # Frame interno que contendrá los controles
            self._scroll_frame = tk.Frame(self._canvas, bg=self.BackColor)
            self._canvas_window = self._canvas.create_window(
                (0, 0),
                window=self._scroll_frame,
                anchor='nw'
            )
            
            # Posicionar scrollbars y canvas
            self._v_scrollbar.pack(side='right', fill='y')
            self._h_scrollbar.pack(side='bottom', fill='x')
            self._canvas.pack(side='left', fill='both', expand=True)
            
            # Actualizar región desplazable cuando cambia el tamaño
            self._scroll_frame.bind('<Configure>', self._on_scroll_frame_configure)
            self._canvas.bind('<Configure>', self._on_canvas_configure)
            
            # Soporte para rueda del ratón
            self._canvas.bind('<Enter>', self._bind_mousewheel)
            self._canvas.bind('<Leave>', self._unbind_mousewheel)
            
            # El contenedor para controles será el scroll_frame
            self._container = self._scroll_frame
        else:
            # Sin AutoScroll, el contenedor es el widget principal
            self._container = self._tk_widget
        
        # Add _root for container functionality
        self._root = master_form._root
        
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
        
        # Lista de controles dentro del panel
        self.Controls = []
        
        # Eventos VB
        self.ControlAdded = lambda control: None
        self.ControlRemoved = lambda control: None

    def AddControl(self, control):
        """Añade un control al Panel con posiciones relativas.
        
        Implementa la jerarquía de visibilidad de Windows Forms:
        - El control se añade al Panel (se convierte en su padre)
        - El control solo será visible si su propia propiedad Visible es True
          Y el Panel (y todos sus padres) también están visibles
        """
        self.Controls.append(control)
        # Cambiar el master del control al contenedor apropiado (scroll_frame o widget principal)
        control.master = self._container
        
        # Registrar este Panel como wrapper del contenedor para la jerarquía de padres
        if not hasattr(self._container, '_control_wrapper'):
            self._container._control_wrapper = self
        
        # Heredar propiedades del contenedor
        if hasattr(control, 'Enabled'):
            control.Enabled = self.Enabled
            if hasattr(control, '_tk_widget'):
                try:
                    control._tk_widget.config(state='normal' if self.Enabled else 'disabled')
                except tk.TclError:
                    pass  # Algunos widgets no soportan state
        
        # Aplicar jerarquía de visibilidad:
        # El control solo se muestra si su _visible es True Y el Panel está visible
        if hasattr(control, '_visible'):
            control_should_be_visible = control._visible and self.get_Visible()
            if control_should_be_visible:
                # Mostrar el control
                control._place_control()
            else:
                # Ocultar el control
                if hasattr(control, '_tk_widget') and control._tk_widget:
                    control._tk_widget.place_forget()
        else:
            # Si el control no tiene _visible, usar comportamiento por defecto
            if self.get_Visible():
                control._place_control()
        
        # Actualizar región de scroll si AutoScroll está activado
        if self.AutoScroll and hasattr(self, '_scroll_frame'):
            self._scroll_frame.update_idletasks()
            self._canvas.configure(scrollregion=self._canvas.bbox('all'))
        
        # Aplicar AutoSize si está habilitado
        if self.AutoSize:
            self._apply_autosize_panel()
        
        self.ControlAdded(control)

    def set_Enabled(self, enabled):
        """Establece si el panel está habilitado y propaga a los controles."""
        self.Enabled = enabled
        for control in self.Controls:
            if hasattr(control, 'Enabled'):
                control.Enabled = enabled
                if hasattr(control, '_tk_widget'):
                    control._tk_widget.config(state='normal' if enabled else 'disabled')
    
    def set_Visible(self, value):
        """Establece la visibilidad del panel y la propaga a sus controles.
        
        Implementa la jerarquía de visibilidad de Windows Forms:
        - Cuando el Panel se oculta (Visible = False), automáticamente oculta
          todos sus controles hijos, sin importar su propiedad Visible individual
        - Cuando el Panel se hace visible (Visible = True), solo muestra los
          controles hijos cuya propiedad Visible individual sea True
        """
        # Usar la implementación base que maneja la jerarquía completa
        # Esto propagará automáticamente a todos los hijos
        super().set_Visible(value)

    def RemoveControl(self, control):
        """Quita un control del Panel."""
        if control in self.Controls:
            self.Controls.remove(control)
            self.ControlRemoved(control)
            # Aplicar AutoSize si está habilitado
            if self.AutoSize:
                self._apply_autosize_panel()
    
    def _apply_autosize_panel(self):
        """Aplica AutoSize específico para Panel.
        
        El Panel se redimensiona para abarcar todos sus controles hijos,
        respetando AutoSizeMode:
        - GrowOnly: Crece pero no se encoge por debajo del tamaño original
        - GrowAndShrink: Se ajusta exactamente al contenido
        """
        if not self.AutoSize or not self.Controls:
            return
        
        # Calcular el área necesaria para contener todos los controles
        max_right = 0
        max_bottom = 0
        
        for control in self.Controls:
            if hasattr(control, 'Left') and hasattr(control, 'Top'):
                control_right = control.Left + getattr(control, 'Width', 0)
                control_bottom = control.Top + getattr(control, 'Height', 0)
                max_right = max(max_right, control_right)
                max_bottom = max(max_bottom, control_bottom)
        
        # Agregar padding
        padx, pady = self.Padding
        required_width = max_right + padx * 2
        required_height = max_bottom + pady * 2
        
        # Aplicar AutoSizeMode
        if self.AutoSizeMode == 'GrowOnly':
            # No encoger por debajo del tamaño original
            original_width, original_height = self._original_size
            required_width = max(required_width, original_width)
            required_height = max(required_height, original_height)
        # GrowAndShrink: usar tamaño calculado tal cual
        
        # Aplicar restricciones de MinimumSize
        if self.MinimumSize:
            min_width, min_height = self.MinimumSize
            required_width = max(required_width, min_width)
            required_height = max(required_height, min_height)
        
        # Aplicar restricciones de MaximumSize
        if self.MaximumSize:
            max_width, max_height = self.MaximumSize
            if max_width > 0:
                required_width = min(required_width, max_width)
            if max_height > 0:
                required_height = min(required_height, max_height)
        
        # Actualizar dimensiones
        self.Width = required_width
        self.Height = required_height
        
        # Reposicionar con nuevo tamaño
        if self.Visible:
            self._place_control(self.Width, self.Height)

    @property
    def Padding(self):
        """Obtiene el padding interno del Panel."""
        return self._padding

    @Padding.setter
    def Padding(self, value):
        """Establece el padding interno del Panel."""
        self._padding = value
        if self._tk_widget:
            padx, pady = value
            self._tk_widget.config(padx=padx, pady=pady)
            if self.AutoSize:
                self._apply_autosize_panel()

    @property
    def Text(self):
        """Obtiene el título del Panel."""
        return self._text
    
    @Text.setter
    def Text(self, value):
        """Establece el título del Panel."""
        self._text = value
        if self._tk_widget:
            # Si el widget actual es un Frame y se quiere agregar texto,
            # necesitamos recrear como LabelFrame
            if isinstance(self._tk_widget, tk.Frame) and not isinstance(self._tk_widget, tk.LabelFrame) and value:
                self._recreate_widget_as_labelframe()
            # Si ya es LabelFrame, simplemente actualizar el texto
            elif isinstance(self._tk_widget, tk.LabelFrame):
                self._tk_widget.config(text=value)
    
    def _recreate_widget_as_labelframe(self):
        """Recrea el widget como LabelFrame cuando se agrega texto a un Frame existente."""
        # Guardar configuración actual
        old_widget = self._tk_widget
        old_place_info = old_widget.place_info()
        
        # Crear nuevo LabelFrame con la misma configuración
        padx, pady = self.Padding
        
        # Mapear BorderStyle de VB.NET a tkinter
        relief_map = {
            'None': 'flat', 'Fixed3D': 'ridge', 'FixedSingle': 'solid',
            'flat': 'flat', 'groove': 'groove', 'raised': 'raised',
            'ridge': 'ridge', 'solid': 'solid', 'sunken': 'sunken'
        }
        
        config = {
            'text': self._text,
            'width': self.Width,
            'height': self.Height,
            'bg': self.BackColor,
            'relief': relief_map.get(self.BorderStyle, 'flat'),
            'padx': padx,
            'pady': pady
        }
        if self.BackgroundImage:
            config['image'] = self.BackgroundImage
        
        new_widget = tk.LabelFrame(self.master, **config)
        
        # Mover todos los controles hijos al nuevo widget
        for control in self.Controls:
            control.master = new_widget
            if hasattr(control, '_tk_widget'):
                control._tk_widget.place_forget()
        
        # Reemplazar el widget
        old_widget.destroy()
        self._tk_widget = new_widget
        
        # Reposicionar el nuevo widget
        if old_place_info:
            self._tk_widget.place(**old_place_info)
        else:
            self._place_control(self.Width, self.Height)
        
        # Reposicionar controles hijos
        for control in self.Controls:
            if hasattr(control, '_place_control'):
                control._place_control()
        
        # Re-bind eventos
        self._tk_widget.bind('<Configure>', self._on_paint)
        self._tk_widget.bind('<Button-1>', self._on_click)
        self._tk_widget.bind('<Double-Button-1>', self._on_double_click)
        self._tk_widget.bind('<Enter>', self._on_mouse_enter)
        self._tk_widget.bind('<Leave>', self._on_mouse_leave)
        self._tk_widget.bind('<ButtonPress>', self._on_mouse_down)
        self._tk_widget.bind('<ButtonRelease>', self._on_mouse_up)

    def _on_paint(self, event):
        """Handler for Paint and Resize events."""
        self.Paint()
        self.Resize()
    
    def _on_scroll_frame_configure(self, event):
        """Actualiza la región de scroll cuando cambia el contenido."""
        if hasattr(self, '_canvas'):
            self._canvas.configure(scrollregion=self._canvas.bbox('all'))
    
    def _on_canvas_configure(self, event):
        """Ajusta el ancho del frame interno al ancho del canvas."""
        if hasattr(self, '_canvas') and hasattr(self, '_canvas_window'):
            canvas_width = event.width
            self._canvas.itemconfig(self._canvas_window, width=canvas_width)
    
    def _bind_mousewheel(self, event):
        """Habilita el scroll con la rueda del ratón."""
        if hasattr(self, '_canvas'):
            # Windows y MacOS
            self._canvas.bind_all('<MouseWheel>', self._on_mousewheel)
            # Linux
            self._canvas.bind_all('<Button-4>', self._on_mousewheel)
            self._canvas.bind_all('<Button-5>', self._on_mousewheel)
    
    def _unbind_mousewheel(self, event):
        """Deshabilita el scroll con la rueda del ratón."""
        if hasattr(self, '_canvas'):
            self._canvas.unbind_all('<MouseWheel>')
            self._canvas.unbind_all('<Button-4>')
            self._canvas.unbind_all('<Button-5>')
    
    def _on_mousewheel(self, event):
        """Maneja el scroll con la rueda del ratón."""
        if hasattr(self, '_canvas'):
            # Windows y MacOS
            if event.num == 5 or event.delta < 0:
                self._canvas.yview_scroll(1, 'units')
            elif event.num == 4 or event.delta > 0:
                self._canvas.yview_scroll(-1, 'units')


class Line:
    """
    Representa una línea (System.Windows.Shapes.Line de WPF/UWP) dibujada en un Canvas.
    
    Uso - Opción 1 (asignación de propiedades):
        line = Line(form)
        line.X1 = 10
        line.Y1 = 10
        line.X2 = 200
        line.Y2 = 100
        line.Stroke = "blue"
        line.StrokeThickness = 2
    
    Uso - Opción 2 (diccionario):
        line = Line(form, {'X1': 10, 'Y1': 10, 'X2': 200, 'Y2': 100, 'Stroke': 'blue'})
    """
    
    def __init__(self, master_form, props=None):
        defaults = {
            'X1': 0,
            'Y1': 0,
            'X2': 100,
            'Y2': 100,
            'Name': "",
            'Stroke': "black",
            'StrokeThickness': 1,
            'StrokeDashArray': None,
            'Visible': True,
            'Tag': None
        }
        
        if props:
            defaults.update(props)
        
        # Resolver el canvas o widget master
        if hasattr(master_form, '_canvas'):
            self._canvas = master_form._canvas
        elif hasattr(master_form, '_tk_widget') and isinstance(master_form._tk_widget, tk.Canvas):
            self._canvas = master_form._tk_widget
        elif isinstance(master_form, tk.Canvas):
            self._canvas = master_form
        else:
            # Si no hay canvas, crear uno
            master_widget = getattr(master_form, '_root', getattr(master_form, '_tk_widget', getattr(master_form, '_frame', master_form)))
            self._canvas = tk.Canvas(master_widget, bg='white')
            self._canvas.pack(fill='both', expand=True)
        
        # Propiedades WPF/UWP
        self.Name = defaults['Name']
        self.X1 = defaults['X1']
        self.Y1 = defaults['Y1']
        self.X2 = defaults['X2']
        self.Y2 = defaults['Y2']
        self.Stroke = defaults['Stroke']
        self.StrokeThickness = defaults['StrokeThickness']
        self.StrokeDashArray = defaults['StrokeDashArray']  # Lista como [5, 2, 3, 2] para patrón de guiones
        self._visible = defaults['Visible']
        self.Tag = defaults['Tag']
        
        # Eventos UIElement (WPF/UWP)
        self.MouseEnter = lambda sender, e: None
        self.MouseLeave = lambda sender, e: None
        self.MouseLeftButtonDown = lambda sender, e: None
        self.MouseLeftButtonUp = lambda sender, e: None
        self.MouseMove = lambda sender, e: None
        self.MouseRightButtonDown = lambda sender, e: None
        self.MouseRightButtonUp = lambda sender, e: None
        self.ManipulationStarted = lambda sender, e: None
        self.ManipulationDelta = lambda sender, e: None
        self.ManipulationCompleted = lambda sender, e: None
        
        # Dibujar la línea
        self._line_id = None
        self._draw()
        
        # Bind eventos si la línea es visible
        if self.Visible:
            self._bind_events()
    
    @property
    def Visible(self):
        """Obtiene la visibilidad de la línea."""
        return self._visible
    
    @Visible.setter
    def Visible(self, value):
        """Establece la visibilidad de la línea."""
        self.set_Visible(value)
    
    def _draw(self):
        """Dibuja o actualiza la línea en el canvas."""
        if self._line_id:
            # Actualizar línea existente
            self._canvas.coords(self._line_id, self.X1, self.Y1, self.X2, self.Y2)
            self._canvas.itemconfig(self._line_id, 
                                   fill=self.Stroke, 
                                   width=self.StrokeThickness,
                                   dash=self._convert_dash_array())
        else:
            # Crear nueva línea
            self._line_id = self._canvas.create_line(
                self.X1, self.Y1, self.X2, self.Y2,
                fill=self.Stroke,
                width=self.StrokeThickness,
                dash=self._convert_dash_array(),
                tags=self.Name if self.Name else None
            )
        
        # Aplicar visibilidad
        if self.Visible:
            self._canvas.itemconfig(self._line_id, state='normal')
        else:
            self._canvas.itemconfig(self._line_id, state='hidden')
    
    def _convert_dash_array(self):
        """Convierte StrokeDashArray a formato tkinter."""
        if self.StrokeDashArray:
            # Tkinter usa tupla de enteros para dash
            return tuple(int(x) for x in self.StrokeDashArray)
        return None
    
    def _bind_events(self):
        """Vincula eventos del mouse a la línea."""
        if self._line_id:
            self._canvas.tag_bind(self._line_id, '<Enter>', self._on_mouse_enter)
            self._canvas.tag_bind(self._line_id, '<Leave>', self._on_mouse_leave)
            self._canvas.tag_bind(self._line_id, '<Button-1>', self._on_mouse_left_down)
            self._canvas.tag_bind(self._line_id, '<ButtonRelease-1>', self._on_mouse_left_up)
            self._canvas.tag_bind(self._line_id, '<Motion>', self._on_mouse_move)
            self._canvas.tag_bind(self._line_id, '<Button-3>', self._on_mouse_right_down)
            self._canvas.tag_bind(self._line_id, '<ButtonRelease-3>', self._on_mouse_right_up)
    
    def _on_mouse_enter(self, event):
        """Handler para MouseEnter."""
        self.MouseEnter(self, event)
    
    def _on_mouse_leave(self, event):
        """Handler para MouseLeave."""
        self.MouseLeave(self, event)
    
    def _on_mouse_left_down(self, event):
        """Handler para MouseLeftButtonDown."""
        self.MouseLeftButtonDown(self, event)
        # Simulación básica de ManipulationStarted
        self.ManipulationStarted(self, event)
    
    def _on_mouse_left_up(self, event):
        """Handler para MouseLeftButtonUp."""
        self.MouseLeftButtonUp(self, event)
        # Simulación básica de ManipulationCompleted
        self.ManipulationCompleted(self, event)
    
    def _on_mouse_move(self, event):
        """Handler para MouseMove."""
        self.MouseMove(self, event)
        # Simulación básica de ManipulationDelta
        self.ManipulationDelta(self, event)
    
    def _on_mouse_right_down(self, event):
        """Handler para MouseRightButtonDown."""
        self.MouseRightButtonDown(self, event)
    
    def _on_mouse_right_up(self, event):
        """Handler para MouseRightButtonUp."""
        self.MouseRightButtonUp(self, event)
    
    # Properties con getters/setters
    
    def set_X1(self, value):
        """Establece la coordenada X del punto inicial."""
        self.X1 = value
        self._draw()
    
    def set_Y1(self, value):
        """Establece la coordenada Y del punto inicial."""
        self.Y1 = value
        self._draw()
    
    def set_X2(self, value):
        """Establece la coordenada X del punto final."""
        self.X2 = value
        self._draw()
    
    def set_Y2(self, value):
        """Establece la coordenada Y del punto final."""
        self.Y2 = value
        self._draw()
    
    def set_Stroke(self, value):
        """Establece el color de la línea."""
        self.Stroke = value
        if self._line_id:
            self._canvas.itemconfig(self._line_id, fill=value)
    
    def set_StrokeThickness(self, value):
        """Establece el grosor de la línea."""
        self.StrokeThickness = value
        if self._line_id:
            self._canvas.itemconfig(self._line_id, width=value)
    
    def set_StrokeDashArray(self, value):
        """Establece el patrón de guiones de la línea.
        
        Parámetro:
        - value: Lista de números [dash, space, dash, space, ...]
                Ejemplo: [5, 2] = 5px línea, 2px espacio
                         [5, 2, 1, 2] = 5px línea, 2px espacio, 1px línea, 2px espacio
        """
        self.StrokeDashArray = value
        if self._line_id:
            self._canvas.itemconfig(self._line_id, dash=self._convert_dash_array())
    
    def set_Visible(self, value):
        """Establece la visibilidad de la línea."""
        self._visible = value
        self._draw()
    
    def Delete(self):
        """Elimina la línea del canvas."""
        if self._line_id:
            self._canvas.delete(self._line_id)
            self._line_id = None
    
    def BringToFront(self):
        """Trae la línea al frente (encima de otros elementos)."""
        if self._line_id:
            self._canvas.tag_raise(self._line_id)
    
    def SendToBack(self):
        """Envía la línea al fondo (detrás de otros elementos)."""
        if self._line_id:
            self._canvas.tag_lower(self._line_id)


class FileDialog:
    """Clase base para diálogos de archivos."""
    
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
        
        # Eventos VB
        self.FileOk = lambda sender, e: None
        self.HelpRequest = lambda sender, hlpevent: None
        self.Disposed = lambda sender, e: None
    
    def _parse_filter(self):
        """Parse the Filter string into filetypes for Tkinter."""
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
        """Destructor to trigger Disposed event."""
        self.Disposed(self, None)


class OpenFileDialog(FileDialog):
    """Representa un OpenFileDialog."""
    
    def __init__(self):
        super().__init__()
        self.Multiselect = False
        self.ReadOnlyChecked = False
        self.ShowReadOnly = False
        self.SafeFileName = ""
    
    def ShowDialog(self):
        """Muestra el diálogo y devuelve el archivo seleccionado."""
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
    """Representa un SaveFileDialog."""
    
    def __init__(self):
        super().__init__()
        self.OverwritePrompt = True
        self.CreatePrompt = False
    
    def ShowDialog(self):
        """Muestra el diálogo y devuelve el archivo seleccionado."""
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
    """Representa un PrintDialog con propiedades principales de VB.NET."""
    
    def __init__(self):
        self.Document = None  # El objeto PrintDocument que se va a imprimir
        self.PrinterSettings = None  # Configuraciones de impresora seleccionadas
        self.AllowCurrentPage = False  # Habilita opción "Página actual"
        self.AllowSelection = False  # Habilita opción "Selección"
        self.AllowPrintToFile = False  # Muestra casilla "Imprimir a archivo"
        self.AllowSomePages = False  # Habilita opción "Páginas"
        self.ShowHelp = False  # Muestra botón de Ayuda
        self.ShowNetwork = False  # Permite acceso a impresoras de red
        self.UseEXDialog = True  # Usa diálogo moderno (por defecto True)
        self.PrintToFile = False  # Establecido por el usuario si marca "Imprimir a archivo"
        self.PrinterName = ""  # Nombre de la impresora seleccionada
    
    def ShowDialog(self):
        """Muestra el diálogo de impresión simulado y devuelve el resultado."""
        from tkinter import messagebox
        
        # Construir mensaje basado en las opciones habilitadas
        options = []
        if self.AllowCurrentPage:
            options.append("Página actual")
        if self.AllowSelection:
            options.append("Selección")
        if self.AllowSomePages:
            options.append("Páginas")
        if self.AllowPrintToFile:
            options.append("Imprimir a archivo")
        
        message = "Opciones de impresión disponibles:\n" + "\n".join(options) if options else "Imprimir documento"
        if self.ShowHelp:
            message += "\n\nPresione OK para imprimir o Cancelar para cancelar."
        
        result = messagebox.askyesno("Print Dialog", message)
        
        # Simular configuración basada en resultado
        if result:
            self.PrintToFile = self.AllowPrintToFile  # Simulado
            self.PrinterName = "Default Printer"  # Simulado
        
        return result


class PictureBox(ControlBase):
    """
    Representa un PictureBox para mostrar imágenes con propiedades VB.NET.
    
    Uso - Opción 1 (asignación de propiedades):
        picture = PictureBox(form)
        picture.Left = 10
        picture.Top = 10
        picture.Width = 200
        picture.Height = 200
        picture.ImageLocation = "path/to/image.png"
        picture.SizeMode = "Zoom"
    
    Uso - Opción 2 (diccionario):
        picture = PictureBox(form, {
            'Left': 10, 'Top': 10, 'Width': 200, 'Height': 200,
            'ImageLocation': 'path/to/image.png', 'SizeMode': 'Zoom'
        })
    """
    
    def __init__(self, master_form, props=None):
        # Valores por defecto
        defaults = {
            'Image': None,
            'Left': 10,
            'Top': 10,
            'Width': 100,
            'Height': 100,
            'Name': "",
            'ImageLocation': "",
            'SizeMode': "Normal",
            'BorderStyle': None,
            'Enabled': True,
            'Visible': True,
            'BackColor': None,
            'ErrorImage': None,
            'InitialImage': None,
            'WaitOnLoad': False
        }
        
        # Merge con props si existe
        if props:
            defaults.update(props)
        
        super().__init__(master_form._root, defaults['Left'], defaults['Top'])
        
        # Asignar todas las propiedades
        self.Name = defaults['Name']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Image = defaults['Image']
        self.ImageLocation = defaults['ImageLocation']
        self.SizeMode = defaults['SizeMode']  # 'Normal', 'StretchImage', 'AutoSize', 'CenterImage', 'Zoom'
        self.BorderStyle = defaults['BorderStyle']  # 'None', 'FixedSingle', 'Fixed3D'
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.BackColor = defaults['BackColor']
        self.ErrorImage = defaults['ErrorImage']
        self.InitialImage = defaults['InitialImage']
        self.WaitOnLoad = defaults['WaitOnLoad']
        
        # Eventos VB
        self.LoadCompleted = lambda sender, e: None
        self.LoadProgressChanged = lambda sender, e: None
        self.Error = lambda sender, e: None
        
        # Crear el widget Tkinter (Label con imagen)
        self._tk_widget = tk.Label(self.master, image=self.Image)
        
        # Aplicar propiedades
        self._apply_properties()
        
        # Cargar imagen desde ImageLocation si especificada
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
        """Aplica las propiedades al widget Tkinter."""
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
        """Carga la imagen desde ImageLocation."""
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
        """Establece la imagen."""
        self.Image = image
        self._tk_widget.config(image=image)
        self._apply_properties()
    
    def set_ImageLocation(self, location):
        """Establece la ubicación de la imagen y la carga."""
        self.ImageLocation = location
        self._load_image_from_location()
    
    def set_SizeMode(self, mode):
        """Establece el modo de tamaño."""
        self.SizeMode = mode
        self._apply_properties()
    
    def set_BorderStyle(self, style):
        """Establece el estilo del borde."""
        self.BorderStyle = style
        self._apply_properties()
    
    def set_Enabled(self, enabled):
        """Establece si está habilitado."""
        self.Enabled = enabled
        self._tk_widget.config(state='normal' if enabled else 'disabled')
    
    def _on_click(self, event):
        """Handler for Click event."""
        self.Click()
    
    def _on_double_click(self, event):
        """Handler for DoubleClick event."""
        self.DoubleClick()
    
    def _on_paint(self, event):
        """Handler for Paint and Resize events."""
        self.Paint()
        self.Resize()


class ImageList:
    """
    Representa una ImageList para gestionar imágenes con propiedades VB.NET.
    
    Uso - Opción 1: imgList = ImageList(); imgList.ImageSize = (32, 32)
    Uso - Opción 2: imgList = ImageList({'ImageSize': (32, 32), 'Name': 'icons'})
    """
    
    def __init__(self, props=None):
        defaults = {
            'Name': "",
            'ImageSize': (16, 16),
            'ColorDepth': 32,
            'TransparentColor': None,
            'ImageStream': None
        }
        
        if props:
            defaults.update(props)
        
        self.Name = defaults['Name']  # Identificador único
        self.Images = {}  # Diccionario de imágenes (clave: índice o nombre, valor: PhotoImage)
        self.ImageSize = defaults['ImageSize']  # (ancho, alto) en píxeles
        self.ColorDepth = defaults['ColorDepth']  # Profundidad de color (8, 16, 24, 32 bits)
        self.TransparentColor = defaults['TransparentColor']  # Color transparente
        self.ImageStream = defaults['ImageStream']  # Para serialización (placeholder)
        self._next_index = 0  # Para asignar índices automáticamente
        
        # Eventos VB
        self.CollectionChanged = lambda: None
        self.Disposed = lambda sender, e: None
    
    def Add(self, image, key=None):
        """Añade una imagen a la lista. Si key es None, usa un índice numérico."""
        if key is None:
            key = self._next_index
            self._next_index += 1
        self.Images[key] = image
        self.CollectionChanged()
    
    def GetImage(self, key):
        """Obtiene una imagen por clave (índice o nombre)."""
        return self.Images.get(key, None)
    
    def Remove(self, key):
        """Elimina una imagen por clave."""
        if key in self.Images:
            del self.Images[key]
            self.CollectionChanged()
    
    def Clear(self):
        """Limpia todas las imágenes."""
        self.Images.clear()
        self._next_index = 0
        self.CollectionChanged()
    
    def Count(self):
        """Devuelve el número de imágenes."""
        return len(self.Images)
    
    def Dispose(self):
        """Libera los recursos del ImageList."""
        self.Disposed(self, None)


class DialogResult:
    """Representa los valores de retorno de un diálogo (DialogResult)."""
    
    OK = "OK"
    Cancel = "Cancel"
    Yes = "Yes"
    No = "No"
    Abort = "Abort"
    Retry = "Retry"
    Ignore = "Ignore"


class MessageBox:
    """Representa un MessageBox para mensajes con parámetros VB.NET."""
    
    @staticmethod
    def Show(
        text,
        caption="Message",
        buttons="OK",
        icon=None,
        defaultButton=None,
        options=None,
        modal=True
    ):
        """Muestra un mensaje y devuelve el resultado.
        
        Parámetros:
        - text: El mensaje principal.
        - caption: El título.
        - buttons: 'OK', 'OKCancel', 'YesNo', 'YesNoCancel', 'RetryCancel', 'AbortRetryIgnore'
        - icon: 'Information', 'Warning', 'Error', 'Question', 'None'
        - defaultButton: 'Button1', 'Button2', 'Button3' (no implementado en Tkinter)
        - options: 'RightAlign', 'RtlReading', etc. (parcialmente soportado)
        """
        # Determine parent widget for modal dialogs
        parent_widget = tk._default_root if modal else None

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
                messagebox.showwarning(caption, display_text, parent=parent_widget)
            elif msg_type == 'error':
                messagebox.showerror(caption, display_text, parent=parent_widget)
            else:
                messagebox.showinfo(caption, display_text, parent=parent_widget)
            return DialogResult.OK
        elif buttons == "OKCancel":
            return DialogResult.OK if messagebox.askokcancel(caption, display_text, parent=parent_widget) else DialogResult.Cancel
        elif buttons == "YesNo":
            if msg_type == 'question':
                return DialogResult.Yes if messagebox.askyesno(caption, display_text, parent=parent_widget) else DialogResult.No
            else:
                return DialogResult.Yes if messagebox.askyesno(caption, display_text, parent=parent_widget) else DialogResult.No
        elif buttons == "YesNoCancel":
            result = messagebox.askyesnocancel(caption, display_text, parent=parent_widget)
            if result is True:
                return DialogResult.Yes
            elif result is False:
                return DialogResult.No
            else:
                return DialogResult.Cancel
        elif buttons == "RetryCancel":
            return DialogResult.Retry if messagebox.askretrycancel(caption, display_text, parent=parent_widget) else DialogResult.Cancel
        elif buttons == "AbortRetryIgnore":
            # Tkinter no tiene AbortRetryIgnore, simular con YesNoCancel o custom
            result = messagebox.askyesnocancel(
                caption,
                f"{display_text}\n\nAbort = Yes, Retry = No, Ignore = Cancel",
                parent=parent_widget
            )
            if result is True:
                return DialogResult.Abort
            elif result is False:
                return DialogResult.Retry
            else:
                return DialogResult.Ignore
        # Default
        messagebox.showinfo(caption, display_text, parent=parent_widget)
        return DialogResult.OK
    

class InputBox:
    """Representa un InputBox para entrada de texto con parámetros VB.NET."""
    
    @staticmethod
    def Show(prompt, title="Input", defaultResponse="", xpos=None, ypos=None, modal=True):
        """Muestra un diálogo de entrada y devuelve el texto.
        
        Parámetros:
        - prompt: El mensaje principal.
        - title: El título.
        - defaultResponse: Valor por defecto en el cuadro de texto.
        - xpos: Posición X (no implementado en Tkinter simpledialog).
        - ypos: Posición Y (no implementado en Tkinter simpledialog).
        """
        from tkinter import simpledialog
        parent_widget = tk._default_root if modal else None
        result = simpledialog.askstring(title, prompt, initialvalue=defaultResponse, parent=parent_widget)
        return result if result is not None else ""


class MaskedFormat:
    """Clase para formatear texto con máscaras."""
    
    @staticmethod
    def Format(value, mask):
        """Aplica una máscara al valor (placeholder simple)."""
        # Implementación básica, e.g., para números
        if mask == "9999":
            return str(value).zfill(4)
        return str(value)


class MaskedTextBox(TextBox):
    """
    Representa un MaskedTextBox con validación de máscara y propiedades VB.NET.
    
    Uso - Opción 1 (asignación de propiedades):
        mtb = MaskedTextBox(form)
        mtb.Mask = "(999) 000-0000"
        mtb.Left = 10
        mtb.Top = 80
    
    Uso - Opción 2 (diccionario):
        mtb = MaskedTextBox(form, {'Mask': '(999) 000-0000', 'Left': 10, 'Top': 80})
    """
    
    def __init__(self, master_form, props=None):
        defaults = {
            'Mask': "",
            'Text': "",
            'Left': 10,
            'Top': 80,
            'Width': 200,
            'Name': "",
            'PromptChar': '_',
            'HidePromptOnLeave': False,
            'PasswordChar': None,
            'UseSystemPasswordChar': False,
            'BeepOnError': False,
            'CutCopyMaskFormat': 'IncludeLiterals',
            'InsertKeyMode': 'Insert',
            'AllowPromptAsInput': False,
            'FormatProvider': None
        }
        
        if props:
            defaults.update(props)
        
        # Llamar al constructor padre con los parámetros necesarios
        super().__init__(master_form, {'Text': defaults['Text'], 'Left': defaults['Left'], 'Top': defaults['Top'], 'Width': defaults['Width'], 'Name': defaults['Name']})
        
        # Propiedades VB específicas
        self.Mask = defaults['Mask']
        self.PromptChar = defaults['PromptChar']
        self.HidePromptOnLeave = defaults['HidePromptOnLeave']
        self.PasswordChar = defaults['PasswordChar']
        self.UseSystemPasswordChar = defaults['UseSystemPasswordChar']
        self.BeepOnError = defaults['BeepOnError']
        self.CutCopyMaskFormat = defaults['CutCopyMaskFormat']  # 'IncludeLiterals', 'ExcludePromptAndLiterals', etc.
        self.InsertKeyMode = defaults['InsertKeyMode']  # 'Insert', 'Overwrite'
        self.AllowPromptAsInput = defaults['AllowPromptAsInput']
        self.FormatProvider = defaults['FormatProvider']  # Placeholder para cultura
        
        # Eventos específicos de MaskedTextBox
        self.MaskInputRejected = lambda sender, e: None
        self.TypeValidationCompleted = lambda sender, e: None
        
        # Aplicar PasswordChar si especificado
        if self.PasswordChar:
            self._tk_widget.config(show=self.PasswordChar)
        elif self.UseSystemPasswordChar:
            self._tk_widget.config(show='*')
        
        # Configurar validación
        vcmd = (self.master.register(self._validate), '%P')
        self._tk_widget.config(validate='key', validatecommand=vcmd)
        
        # Bind focus events for HidePromptOnLeave
        self._tk_widget.bind('<FocusIn>', self._on_focus_in)
        self._tk_widget.bind('<FocusOut>', self._on_focus_out)
        
        # Inicializar display text con prompts
        self._update_display_text()
    
    def _validate(self, new_text):
        """Valida el texto según la máscara."""
        if not self.Mask:
            return True
        
        # Permitir PromptChar si AllowPromptAsInput
        if self.AllowPromptAsInput and new_text == self.PromptChar:
            return True
        
        # Implementación básica de validación de máscara
        # 9: dígito opcional, 0: dígito requerido, L: letra requerida, ?: letra opcional, A: alfanumérico requerido, etc.
        # Simplificado para ejemplos comunes
        valid = False
        if self.Mask == "9999":  # 4 dígitos opcionales
            cleaned = new_text.replace(self.PromptChar, '')
            valid = cleaned.isdigit() and len(cleaned) <= 4
        elif self.Mask == "(999) 999-9999":  # Teléfono
            # Permitir dígitos, paréntesis, guiones, espacios y prompts
            cleaned = new_text.replace('(', '').replace(')', '').replace('-', '').replace(' ', '').replace(self.PromptChar, '')
            valid = cleaned.isdigit() and len(cleaned) <= 10
        elif self.Mask == "00/00/0000":  # Fecha
            cleaned = new_text.replace('/', '').replace(self.PromptChar, '')
            valid = cleaned.isdigit() and len(cleaned) <= 8
        else:
            # Validación general básica: longitud no exceda la máscara
            valid = len(new_text) <= len(self.Mask)
        
        if not valid:
            self.MaskInputRejected(self, None)
            if self.BeepOnError:
                winsound.Beep(800, 200)  # Beep de error
        
        return valid
    
    def _on_focus_in(self, event):
        """Maneja el evento de foco entrante."""
        if self.HidePromptOnLeave:
            self._update_display_text()
    
    def _on_focus_out(self, event):
        """Maneja el evento de foco saliente."""
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
        """Actualiza el texto mostrado con prompts."""
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
        """Propiedad de solo lectura: True si todas las posiciones requeridas y opcionales están llenas."""
        if not self.Mask:
            return True
        current = self._tk_widget.get()
        # Contar posiciones requeridas (0, L, A) vs opcionales (9, ?, etc.)
        required_positions = sum(1 for char in self.Mask if char in '0LA')
        filled_required = sum(1 for i, char in enumerate(self.Mask) if char in '0LA' and i < len(current) and current[i] != self.PromptChar)
        return filled_required >= required_positions
    
    @property
    def MaskCompleted(self):
        """Propiedad de solo lectura: True si todas las posiciones requeridas están llenas."""
        if not self.Mask:
            return True
        current = self._tk_widget.get()
        required_positions = sum(1 for char in self.Mask if char in '0LA')
        filled_required = sum(1 for i, char in enumerate(self.Mask) if char in '0LA' and i < len(current) and current[i] != self.PromptChar)
        return filled_required == required_positions
    
    def get_Text(self):
        """Obtiene el texto sin prompts."""
        text = self._tk_widget.get()
        return text.replace(self.PromptChar, '')
    
    def set_Text(self, new_text):
        """Establece el texto y actualiza display."""
        self._text_value = new_text
        self._tk_widget.delete(0, 'end')
        self._tk_widget.insert(0, new_text)
        self._update_display_text()


class TabPage:
    """
    Representa una página de pestaña para TabControl con propiedades VB.NET.
    
    Uso - Opción 1: page = TabPage(); page.Text = "Mi Pestaña"; page.Name = "tabPage1"
    Uso - Opción 2: page = TabPage({'Text': 'Mi Pestaña', 'Name': 'tabPage1'})
    Uso - Opción 3: page = TabPage({'Text': 'Mi Pestaña', 'UseSystemStyles': True})
    """
    
    def __init__(self, props=None):
        defaults = {
            'Text': "TabPage",
            'Name': "",
            'Enabled': True,
            'Visible': True,
            'ImageIndex': -1,
            'ImageKey': "",
            'ToolTipText': "",
            'UseVisualStyleBackColor': True,
            'Padding': (3, 3),
            'BackColor': None,
            'ForeColor': None,
            'Font': None
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Control", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Control")
        
        self.Name = defaults['Name'] or defaults['Text']  # Usar Text si Name vacío
        self._text_value = defaults['Text']  # Atributo interno para almacenar el texto
        self.Parent = None  # Asignado por TabControl
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']  # Placeholder, ttk.Notebook maneja visibilidad automáticamente
        self.ImageIndex = defaults['ImageIndex']
        self.ImageKey = defaults['ImageKey']
        self.ToolTipText = defaults['ToolTipText']  # Placeholder, Tkinter no tiene tooltips nativos
        self.UseVisualStyleBackColor = defaults['UseVisualStyleBackColor']  # Placeholder
        self.Padding = defaults['Padding']  # (padx, pady)
        self.BackColor = defaults['BackColor']
        self.ForeColor = defaults['ForeColor']
        self.Font = defaults['Font']
        
        # Crear el frame con padding
        padx, pady = self.Padding
        self._frame = tk.Frame(padx=padx, pady=pady)
        
        # Aplicar colores al frame
        if self.BackColor:
            self._frame.config(bg=self.BackColor)
        
        self.Controls = []

        # Eventos VB
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

    def get_Parent(self):
        """Obtiene el control padre del TabPage.
        
        El padre de un TabPage es el TabControl que lo contiene.
        
        Returns:
            El TabControl padre si existe, None en caso contrario.
        """
        return getattr(self, 'Parent', None)
    
    def AddControl(self, control):
        """Añade un control a la TabPage con posiciones relativas.
        
        Implementa la jerarquía de visibilidad de Windows Forms:
        - El control se añade al TabPage (se convierte en su padre)
        - El control solo será visible si su propia propiedad Visible es True
          Y el TabPage (y todos sus padres) también están visibles
        """
        self.Controls.append(control)
        control.master = self._frame
        
        # Registrar este TabPage como wrapper del frame para la jerarquía de padres
        if not hasattr(self._frame, '_control_wrapper'):
            self._frame._control_wrapper = self
        
        # Heredar propiedades del contenedor
        if hasattr(control, 'Enabled'):
            control.Enabled = self.Enabled
            if hasattr(control, '_tk_widget'):
                try:
                    control._tk_widget.config(state='normal' if self.Enabled else 'disabled')
                except tk.TclError:
                    pass
        
        # Aplicar jerarquía de visibilidad:
        # El control solo se muestra si su _visible es True Y el TabPage está visible
        if hasattr(control, '_visible'):
            # Calcular visibilidad efectiva del TabPage
            tabpage_visible = getattr(self, '_visible', True)
            if hasattr(self, 'Parent') and self.Parent:
                # Si el TabPage tiene un Parent (TabControl), verificar su visibilidad
                parent_visible = getattr(self.Parent, '_visible', True)
                tabpage_visible = tabpage_visible and parent_visible
            
            control_should_be_visible = control._visible and tabpage_visible
            if control_should_be_visible:
                # Mostrar el control
                control._place_control()
            else:
                # Ocultar el control
                if hasattr(control, '_tk_widget') and control._tk_widget:
                    control._tk_widget.place_forget()
        else:
            # Si el control no tiene _visible, usar comportamiento por defecto
            control._place_control()
        
        self.ControlAdded(control)

    def _on_configure(self, event):
        """Handler for Paint and Resize events."""
        self.Paint()
        self.Resize()

    def RemoveControl(self, control):
        """Quita un control de la TabPage."""
        if control in self.Controls:
            self.Controls.remove(control)
            self.ControlRemoved(control)
    
    @property
    def Text(self):
        """Property getter para Text en TabPage."""
        return self._text_value
    
    @Text.setter
    def Text(self, value):
        """Property setter para Text en TabPage."""
        self._text_value = value
        # TabPage text se actualiza vía TabControl.AddTab()
    
    def set_BackColor(self, color):
        """Establece el color de fondo del TabPage."""
        self.BackColor = color
        if hasattr(self, '_frame'):
            self._frame.config(bg=color)
    
    def set_ForeColor(self, color):
        """Establece el color de texto del TabPage."""
        self.ForeColor = color
        # No aplica directamente al frame, pero se hereda a controles hijos
    
    def set_Font(self, font):
        """Establece la fuente del TabPage."""
        self.Font = font
        # No aplica directamente al frame, pero se hereda a controles hijos


class TabControl(ControlBase):
    """
    Representa un TabControl con pestañas.
    
    Uso - Opción 1 (asignación de propiedades):
        tab = TabControl(form)
        tab.Left = 10
        tab.Top = 10
        tab.Width = 400
        tab.Height = 300
    
    Uso - Opción 2 (diccionario):
        tab = TabControl(form, {'Left': 10, 'Top': 10, 'Width': 400, 'Height': 300})
    """
    
    def __init__(self, master_form, props=None):
        # Valores por defecto
        defaults = {
            'Left': 10,
            'Top': 10,
            'Width': 300,
            'Height': 200,
            'Name': "",
            'TabPages': None,
            'SelectedIndex': 0,
            'ImageList': None,
            'Appearance': "Normal",
            'Alignment': "Top",
            'Multiline': False,
            'SizeMode': "Normal",
            'Enabled': True,
            'Visible': True,
            'Padding': (0, 0),
            'HotTrack': False
        }
        
        # Merge con props si existe
        if props:
            defaults.update(props)
        
        # Resolve master widget
        master_widget = getattr(master_form, '_root', getattr(master_form, '_tk_widget', getattr(master_form, '_frame', master_form)))
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Asignar propiedades
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        
        # Store master_form for container access
        self.master_form = master_form
        
        # Propiedades VB
        self.Name = defaults['Name']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self.TabPages = defaults['TabPages'] or []
        self.SelectedIndex = defaults['SelectedIndex']
        self.ImageList = defaults['ImageList']
        self.Appearance = defaults['Appearance']  # 'Normal', 'Buttons', 'FlatButtons' - placeholder
        self.Alignment = defaults['Alignment']  # 'Top', 'Bottom', 'Left', 'Right'
        self.Multiline = defaults['Multiline']
        self.SizeMode = defaults['SizeMode']  # 'Normal', 'Fixed', 'FillToRight' - placeholder
        self.Padding = defaults['Padding']  # (padx, pady)
        self.HotTrack = defaults['HotTrack']  # Placeholder
        
        # Eventos VB
        self.SelectedIndexChanged = lambda: None
        self.Selecting = lambda sender, e: None
        self.Selected = lambda sender, e: None
        self.Deselecting = lambda sender, e: None
        self.Deselected = lambda sender, e: None
        self.DrawItem = lambda sender, e: None
        self.ControlAdded = lambda control: None
        self.ControlRemoved = lambda control: None
        
        # Crear el widget Tkinter (Notebook)
        self._tk_widget = ttk.Notebook(self.master)
        
        # Aplicar configuraciones
        config = {}
        padx, pady = self.Padding
        config['padding'] = (padx, pady)
        if config:
            self._tk_widget.config(**config)
        
        self._place_control(self.Width, self.Height)
        
        # Track selected tab for events
        self._last_selected = self.SelectedIndex
        self._tk_widget.bind('<<NotebookTabChanged>>', self._on_tab_changed)
        
        # Añadir TabPages iniciales si existen
        for tab in self.TabPages:
            self.AddTab(tab)
        
        # Establecer SelectedIndex inicial
        if self.TabPages and 0 <= self.SelectedIndex < len(self.TabPages):
            self._tk_widget.select(self.SelectedIndex)

    def AddTab(self, tab_page):
        """Añade una TabPage al TabControl."""
        self.TabPages.append(tab_page)
        tab_page.Parent = self  # Asignar Parent
        tab_page._root = self.master_form._root  # Asignar _root para compatibilidad con controles hijos
        self._tk_widget.add(tab_page._frame, text=tab_page.Text)
        # Aplicar imagen si ImageList y ImageIndex/ImageKey
        if self.ImageList and hasattr(tab_page, 'ImageIndex') and tab_page.ImageIndex >= 0:
            # Placeholder: ttk.Notebook no soporta imágenes fácilmente, usar compound o custom
            pass
        self.ControlAdded(tab_page)

    def RemoveTab(self, tab_page):
        """Quita una TabPage del TabControl."""
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
        """Obtiene la TabPage seleccionada."""
        if self.TabPages and 0 <= self.SelectedIndex < len(self.TabPages):
            return self.TabPages[self.SelectedIndex]
        return None

    @SelectedTab.setter
    def SelectedTab(self, tab_page):
        """Establece la TabPage seleccionada."""
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
        """Obtiene el índice de la pestaña seleccionada."""
        try:
            return self._tk_widget.index(self._tk_widget.select())
        except:
            return -1

    def set_SelectedIndex(self, index):
        """Establece el índice de la pestaña seleccionada."""
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
    """Representa un RadioButton."""
    
    _group_vars = {}  # Class variable to store shared StringVars by group name
    
    def __init__(self, master_form, props=None):
        """Inicializa un RadioButton.
        
        Args:
            master_form: El formulario o contenedor padre
            props: Diccionario opcional con propiedades iniciales
        """
        # Valores por defecto
        defaults = {
            'Left': 10,
            'Top': 140,
            'Width': 100,
            'Height': 25,
            'Name': '',
            'Text': 'Radio',
            'Group': None,
            'Checked': False,
            'Enabled': True,
            'Visible': True,
            'Font': None,
            'ForeColor': None,
            'BackColor': None,
            'TextAlign': 'w',
            'Appearance': 'Normal',
            'AutoSize': False
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Control", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Control")
        
        # Resolve master widget
        master_widget = getattr(master_form, '_root', getattr(master_form, '_tk_widget', getattr(master_form, '_frame', master_form)))
        super().__init__(master_widget, defaults['Left'], defaults['Top'])
        
        # Propiedades VB
        self.Name = defaults['Name']
        self.Enabled = defaults['Enabled']
        self._visible = defaults['Visible']
        self._text_value = defaults['Text']
        
        # Handle Group: if string, use shared StringVar; if StringVar, use it; else create new
        if isinstance(defaults['Group'], str):
            group_name = defaults['Group']
            if group_name not in RadioButton._group_vars:
                RadioButton._group_vars[group_name] = tk.StringVar()
            self.Group = RadioButton._group_vars[group_name]
        elif isinstance(defaults['Group'], tk.StringVar):
            self.Group = defaults['Group']
        else:
            self.Group = tk.StringVar()
        
        self._checked_value = defaults['Checked']
        self.Font = defaults['Font']
        self.ForeColor = defaults['ForeColor']
        self.BackColor = defaults['BackColor']
        self.TextAlign = defaults['TextAlign']
        self.Appearance = defaults['Appearance']
        self.AutoSize = defaults['AutoSize']
        
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        
        # Crear el widget Tkinter
        self._tk_widget = tk.Radiobutton(self.master, text=self._text_value, variable=self.Group, value=self._text_value)
        
        # Aplicar configuraciones
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
        
        if self.AutoSize:
            self._apply_autosize()
            
        self._place_control(self.Width, self.Height)
        
        # Bind common events
        self._bind_common_events()
        
        # Establecer Checked inicial
        if self._checked_value:
            self.Group.set(self._text_value)
        
        # Bind CheckedChanged
        self.Group.trace('w', self._on_checked_changed)

    def get_Checked(self):
        """Verifica si está seleccionado."""
        return self.Group.get() == self._text_value

    def set_Checked(self, value):
        """Establece si está seleccionado."""
        self._checked_value = value
        if value:
            self.Group.set(self._text_value)

    def _on_checked_changed(self, *args):
        """Handler for CheckedChanged event."""
        old_checked = self._checked_value
        self._checked_value = self.get_Checked()
        if old_checked != self._checked_value:
            # Solo llamar a CheckedChanged si está definido
            if hasattr(self, 'CheckedChanged') and callable(self.CheckedChanged):
                self.CheckedChanged()
    
    @property
    def Checked(self):
        """Property getter para Checked."""
        return self.get_Checked()
    
    @Checked.setter
    def Checked(self, value):
        """Property setter para Checked."""
        self.set_Checked(value)
    
    @property
    def Text(self):
        """Property getter para Text en RadioButton."""
        return self._text_value
    
    @Text.setter
    def Text(self, value):
        """Property setter para Text en RadioButton."""
        self._text_value = value
        if hasattr(self, '_tk_widget') and self._tk_widget:
            self._tk_widget.config(text=value)
            # Actualizar el valor del radio button si es necesario
            if hasattr(self, 'Group'):
                self._tk_widget.config(value=value)
            
            # Aplicar AutoSize si está habilitado
            if self.AutoSize:
                self._apply_autosize()
                # Reposicionar con nuevo tamaño
                if self.Visible:
                    self._place_control(self.Width, self.Height)


class ProgressBar(ControlBase):
    """Representa una ProgressBar."""
    
    def __init__(self, master_form, props=None):
        """Inicializa un ProgressBar.
        
        Args:
            master_form: El formulario o contenedor padre
            props: Diccionario opcional con propiedades iniciales
        """
        # Valores por defecto
        defaults = {
            'Left': 10,
            'Top': 10,
            'Width': 200,
            'Height': 20,
            'Minimum': 0,
            'Maximum': 100,
            'Value': 0,
            'Style': 'Blocks'
        }
        
        if props:
            defaults.update(props)
        
        super().__init__(master_form._root, defaults['Left'], defaults['Top'])
        
        self.Minimum = defaults['Minimum']
        self.Maximum = defaults['Maximum']
        self.Value = defaults['Value']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Style = defaults['Style']  # 'Blocks', 'Continuous', 'Marquee'
        
        # Eventos VB
        self.ValueChanged = lambda: None
        self.StyleChanged = lambda: None
        
        # Determinar mode basado en Style
        mode = 'indeterminate' if self.Style == 'Marquee' else 'determinate'
        
        # Crear el widget Tkinter
        self._tk_widget = ttk.Progressbar(self.master, orient='horizontal', length=self.Width, mode=mode)
        self._tk_widget['maximum'] = self.Maximum
        self._tk_widget['value'] = self.Value
        self._place_control(self.Width, self.Height)
        
        # Bind common events
        self._bind_common_events()
        
        # Iniciar animación si Marquee
        if self.Style == 'Marquee':
            self._tk_widget.start()

    def set_Value(self, value):
        """Establece el valor de la barra."""
        self.Value = value
        self._tk_widget['value'] = value
        self.ValueChanged()

    def set_Style(self, style):
        """Establece el estilo de la barra."""
        self.Style = style
        mode = 'indeterminate' if style == 'Marquee' else 'determinate'
        self._tk_widget.config(mode=mode)
        if style == 'Marquee':
            self._tk_widget.start()
        else:
            self._tk_widget.stop()
        self.StyleChanged()


class ListViewItem:
    """
    Representa un elemento en un ListView.
    
    Uso - Opción 1: item = ListViewItem(); item.Text = "Item1"
    Uso - Opción 2: item = ListViewItem({'Text': 'Item1', 'SubItems': ['SubItem1', 'SubItem2']})
    """
    
    def __init__(self, props=None):
        defaults = {
            'Text': "",
            'SubItems': None,
            'ImageIndex': -1,
            'ImageKey': "",
            'Tag': None
        }
        
        if props:
            defaults.update(props)
        
        self.Text = defaults['Text']
        self.SubItems = defaults['SubItems'] or []  # Lista de subelementos para columnas adicionales
        self.ImageIndex = defaults['ImageIndex']
        self.ImageKey = defaults['ImageKey']
        self.Tag = defaults['Tag']  # Objeto personalizado


class ColumnHeader:
    """
    Representa un encabezado de columna en un ListView.
    
    Uso - Opción 1: col = ColumnHeader(); col.Text = "Columna"; col.Width = 150
    Uso - Opción 2: col = ColumnHeader({'Text': 'Columna', 'Width': 150})
    """
    
    def __init__(self, props=None):
        defaults = {
            'Text': "",
            'Width': 100,
            'TextAlign': "left",
            'ImageIndex': -1
        }
        
        if props:
            defaults.update(props)
        
        self.Text = defaults['Text']
        self.Width = defaults['Width']
        self.TextAlign = defaults['TextAlign']  # 'left', 'center', 'right'
        self.ImageIndex = defaults['ImageIndex']


class ListView(ControlBase):
    """
    Representa un ListView con propiedades VB.NET.
    
    Uso - Opción 1 (asignación de propiedades):
        lv = ListView(form)
        lv.Left = 10
        lv.Top = 10
        lv.Width = 400
        lv.Height = 200
        lv.View = "Details"
    
    Uso - Opción 2 (diccionario):
        lv = ListView(form, {'Left': 10, 'Top': 10, 'Width': 400, 'Height': 200, 'View': 'Details'})
    """
    
    def __init__(self, master_form, props=None):
        defaults = {
            'Columns': None,
            'Left': 10,
            'Top': 280,
            'Width': 300,
            'Height': 150,
            'Name': "",
            'Items': None,
            'View': "Details",
            'SmallImageList': None,
            'LargeImageList': None,
            'FullRowSelect': True,
            'MultiSelect': True,
            'CheckBoxes': False,
            'GridLines': False,
            'HeaderStyle': "Clickable",
            'Sorting': "None",
            'Enabled': True,
            'Visible': True
        }
        
        if props:
            defaults.update(props)
        
        super().__init__(master_form._root, defaults['Left'], defaults['Top'], Name=defaults['Name'], Enabled=defaults['Enabled'], Visible=defaults['Visible'])
        
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Items = defaults['Items'] or []  # Lista de ListViewItem
        self.View = defaults['View']  # 'LargeIcon', 'SmallIcon', 'List', 'Details', 'Tile'
        self.Columns = defaults['Columns'] or [ColumnHeader()]
        self.SmallImageList = defaults['SmallImageList']
        self.LargeImageList = defaults['LargeImageList']
        self.FullRowSelect = defaults['FullRowSelect']
        self.MultiSelect = defaults['MultiSelect']
        self.CheckBoxes = defaults['CheckBoxes']
        self.GridLines = defaults['GridLines']
        self.HeaderStyle = defaults['HeaderStyle']  # 'Clickable', 'Nonclickable', 'None'
        self.Sorting = defaults['Sorting']  # 'Ascending', 'Descending', 'None'
        
        # Eventos VB
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
        
        # Aplicar estilos
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
        
        # Añadir items iniciales
        for item in self.Items:
            self.AddItem(item)

    @property
    def SelectedItems(self):
        """Obtiene la colección de elementos seleccionados."""
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
        """Añade un ListViewItem al ListView."""
        if isinstance(item, ListViewItem):
            values = [item.Text] + item.SubItems
            self._tk_widget.insert('', 'end', text=item.Text, values=item.SubItems)
            self.Items.append(item)
        else:
            raise TypeError("AddItem expects a ListViewItem object")

    def GetSelectedItem(self):
        """Obtiene el primer elemento seleccionado."""
        selection = self._tk_widget.selection()
        if selection:
            item_data = self._tk_widget.item(selection[0])
            return ListViewItem(Text=item_data.get('text', ''), SubItems=item_data.get('values', []))
        return None

    def set_View(self, view):
        """Establece la vista del ListView."""
        self.View = view
        # Reconfigurar widget (placeholder: limited support)
        show = 'headings' if view == 'Details' else 'tree'
        self._tk_widget.config(show=show)

    def set_Sorting(self, sorting):
        """Establece el tipo de ordenación."""
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
        """Handler for SelectedIndexChanged and ItemSelectionChanged."""
        self.SelectedIndexChanged()
        selected = self._tk_widget.selection()
        for item in selected:
            self.ItemSelectionChanged(self, {'Item': item, 'Selected': True})

    def _on_column_click(self, column):
        """Handler for ColumnClick."""
        self.ColumnClick(self, {'Column': column})

    def _on_key_down(self, event):
        """Handler for KeyDown."""
        self.KeyDown(self, {'KeyCode': event.keysym, 'Modifiers': event.state})

    def _on_key_press(self, event):
        """Handler for KeyPress."""
        self.KeyPress(self, {'KeyChar': event.char})

class DataGridViewColumn:
    """
    Representa una columna en DataGridView.
    
    Uso - Opción 1: col = DataGridViewColumn(); col.Name = "col1"; col.HeaderText = "Columna 1"
    Uso - Opción 2: col = DataGridViewColumn({'Name': 'col1', 'HeaderText': 'Columna 1', 'Width': 150})
    """
    
    def __init__(self, props=None):
        defaults = {
            'Name': "",
            'HeaderText': "",
            'DataPropertyName': "",
            'Width': 100,
            'Visible': True,
            'ReadOnly': False
        }
        
        if props:
            defaults.update(props)
        
        self.Name = defaults['Name']
        self.HeaderText = defaults['HeaderText']
        self.DataPropertyName = defaults['DataPropertyName']
        self.Width = defaults['Width']
        self.Visible = defaults['Visible']
        self.ReadOnly = defaults['ReadOnly']
        self.DisplayIndex = 0
        self.DefaultCellStyle = {}
        self.SortMode = "Automatic"
        self.ValueType = str
        self.CellTemplate = None
        self.Frozen = False
        self.AutoSizeMode = "None"


class DataGridView(ControlBase):
    """
    Representa un DataGridView con propiedades VB.NET.
    
    Uso - Opción 1 (asignación de propiedades):
        grid = DataGridView(form)
        grid.Left = 10
        grid.Top = 10
        grid.Width = 500
        grid.Height = 300
        grid.DataSource = data_list
    
    Uso - Opción 2 (diccionario):
        grid = DataGridView(form, {'Left': 10, 'Top': 10, 'Width': 500, 'DataSource': data_list})
    """
    
    def __init__(self, master_form, props=None):
        defaults = {
            'Left': 10,
            'Top': 10,
            'Width': 400,
            'Height': 200,
            'Name': "",
            'DataSource': None,
            'Columns': None,
            'AllowUserToAddRows': False,
            'AllowUserToDeleteRows': False,
            'AllowUserToResizeColumns': True,
            'ReadOnly': False,
            'SelectionMode': "FullRowSelect",
            'DefaultCellStyle': None,
            'AutoGenerateColumns': True,
            'AlternatingRowsDefaultCellStyle': None,
            'RowHeadersVisible': True,
            'ColumnHeadersVisible': True,
            'Dock': None,
            'Anchor': None
        }
        
        if props:
            defaults.update(props)
        
        super().__init__(master_form._root, defaults['Left'], defaults['Top'])
        self.Name = defaults['Name']
        
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.DataSource = defaults['DataSource']
        # Convertir columnas si son strings
        self.Columns = []
        if defaults['Columns']:
            for col in defaults['Columns']:
                if isinstance(col, str):
                    self.Columns.append(DataGridViewColumn({'Name': col, 'HeaderText': col, 'DataPropertyName': col}))
                else:
                    self.Columns.append(col)
        self.AllowUserToAddRows = defaults['AllowUserToAddRows']
        self.AllowUserToDeleteRows = defaults['AllowUserToDeleteRows']
        self.AllowUserToResizeColumns = defaults['AllowUserToResizeColumns']
        self.ReadOnly = defaults['ReadOnly']
        self.SelectionMode = defaults['SelectionMode']  # 'FullRowSelect', 'CellSelect', etc.
        self.DefaultCellStyle = defaults['DefaultCellStyle'] or {}
        self.AutoGenerateColumns = defaults['AutoGenerateColumns']
        self.AlternatingRowsDefaultCellStyle = defaults['AlternatingRowsDefaultCellStyle'] or {}
        self.RowHeadersVisible = defaults['RowHeadersVisible']
        self.ColumnHeadersVisible = defaults['ColumnHeadersVisible']
        self.Dock = defaults['Dock']
        self.Anchor = defaults['Anchor']
        
        self.Rows = []
        
        # Eventos VB
        self.ColumnHeaderMouseClick = lambda sender, e: None
        self.ColumnStateChanged = lambda sender, e: None
        self.ColumnWidthChanged = lambda sender, e: None
        self.ColumnDisplayIndexChanged = lambda sender, e: None
        self.ColumnAdded = lambda sender, e: None
        self.ColumnRemoved = lambda sender, e: None
        show = 'headings' if self.ColumnHeadersVisible else 'tree'
        selectmode = 'browse' if self.SelectionMode == 'FullRowSelect' else 'extended'
        self._tk_widget = ttk.Treeview(self.master, show=show, selectmode=selectmode, height=10)
        
        # Configurar columnas
        if self.DataSource and self.AutoGenerateColumns and not self.Columns:
            self._generate_columns_from_datasource()
        
        self._apply_columns()
        
        # Poblar desde DataSource
        if self.DataSource:
            self._populate_from_datasource()
        
        self._place_control(self.Width, self.Height)
        
        # Aplicar estilos (placeholders)
        self._apply_styles()
        
        # Bind events
        self._bind_common_events()
        # For ColumnHeaderMouseClick, placeholder: Treeview headings not easily bindable
        # For other events, placeholders
    
    def _generate_columns_from_datasource(self):
        """Genera columnas automáticamente desde DataSource."""
        if isinstance(self.DataSource, list) and self.DataSource:
            sample = self.DataSource[0]
            if isinstance(sample, dict):
                for key in sample.keys():
                    self.Columns.append(DataGridViewColumn(Name=key, HeaderText=key, DataPropertyName=key))
    
    def _apply_columns(self):
        """Aplica las columnas al Treeview."""
        col_ids = [col.Name for col in self.Columns if col.Visible]
        self._tk_widget.config(columns=col_ids)
        for col in self.Columns:
            if col.Visible:
                self._tk_widget.heading(col.Name, text=col.HeaderText)
                self._tk_widget.column(col.Name, width=col.Width)
    
    def _populate_from_datasource(self):
        """Pobla las filas desde DataSource."""
        for item in self.DataSource:
            if isinstance(item, dict):
                values = [item.get(col.DataPropertyName, '') for col in self.Columns if col.Visible]
                self._tk_widget.insert('', 'end', values=values)
                self.Rows.append(item)
    
    def _apply_styles(self):
        """Aplica estilos (placeholder)."""
        # Placeholder for DefaultCellStyle, AlternatingRowsDefaultCellStyle
        pass
    
    def AddRow(self, values):
        """Añade una fila al DataGridView."""
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
        """Establece la fuente de datos y actualiza la vista."""
        self.DataSource = datasource
        # Limpiar y repoblar
        for i in self._tk_widget.get_children():
            self._tk_widget.delete(i)
        self.Rows = []
        if self.AutoGenerateColumns and not self.Columns:
            self._generate_columns_from_datasource()
        self._apply_columns()
        if datasource:
            self._populate_from_datasource()


class TreeNode:
    """
    Representa un nodo en un TreeView.
    
    Uso - Opción 1: node = TreeNode(); node.Text = "Nodo1"; node.Tag = data
    Uso - Opción 2: node = TreeNode({'Text': 'Nodo1', 'Tag': data, 'Nodes': [child1, child2]})
    """
    
    def __init__(self, props=None):
        defaults = {
            'Text': "",
            'ImageIndex': -1,
            'SelectedImageIndex': -1,
            'Tag': None,
            'Nodes': None
        }
        
        if props:
            defaults.update(props)
        
        self.Text = defaults['Text']
        self.ImageIndex = defaults['ImageIndex']
        self.SelectedImageIndex = defaults['SelectedImageIndex']
        self.Tag = defaults['Tag']
        self.Nodes = defaults['Nodes'] or []  # Lista de TreeNode hijos
        self.Parent = None  # Asignado por TreeView
        self.TreeView = None  # Referencia al TreeView
    
    @property
    def FullPath(self):
        """Obtiene la ruta completa del nodo."""
        path = [self.Text]
        current = self.Parent
        while current:
            path.insert(0, current.Text)
            current = current.Parent
        return self.TreeView.PathSeparator.join(path) if self.TreeView else self.Text


class TreeView(ControlBase):
    """
    Representa un TreeView con propiedades VB.NET.
    
    Uso - Opción 1 (asignación de propiedades):
        tree = TreeView(form)
        tree.Left = 10
        tree.Top = 10
        tree.Width = 250
        tree.Height = 300
        tree.ShowLines = True
    
    Uso - Opción 2 (diccionario):
        tree = TreeView(form, {'Left': 10, 'Top': 10, 'Width': 250, 'Height': 300})
    """
    
    def __init__(self, master_form, props=None):
        defaults = {
            'Left': 10,
            'Top': 10,
            'Width': 200,
            'Height': 200,
            'Name': "",
            'Nodes': None,
            'ImageList': None,
            'ImageIndex': -1,
            'SelectedImageIndex': -1,
            'FullRowSelect': False,
            'CheckBoxes': False,
            'ShowLines': True,
            'ShowPlusMinus': True,
            'ShowRootLines': True,
            'PathSeparator': "\\",
            'LabelEdit': False,
            'Font': None,
            'ForeColor': None,
            'BackColor': None
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Window", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Window")
        
        super().__init__(master_form._root, defaults['Left'], defaults['Top'])
        
        self.Name = defaults['Name']
        
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Nodes = defaults['Nodes'] or []  # Lista de TreeNode raíz
        self.ImageList = defaults['ImageList']
        self.ImageIndex = defaults['ImageIndex']
        self.SelectedImageIndex = defaults['SelectedImageIndex']
        self.FullRowSelect = defaults['FullRowSelect']
        self.CheckBoxes = defaults['CheckBoxes']
        self.ShowLines = defaults['ShowLines']
        self.ShowPlusMinus = defaults['ShowPlusMinus']
        self.ShowRootLines = defaults['ShowRootLines']
        self.PathSeparator = defaults['PathSeparator']
        self.LabelEdit = defaults['LabelEdit']
        self.Font = defaults['Font']
        self.ForeColor = defaults['ForeColor']
        self.BackColor = defaults['BackColor']
        
        # Eventos VB
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
        
        # Crear el widget Tkinter (Treeview)
        self._tk_widget = ttk.Treeview(self.master, show='tree')
        
        # Aplicar configuraciones
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
        
        self._place_control(self.Width, self.Height)
        
        # Bind events
        self._tk_widget.bind('<<TreeviewSelect>>', self._on_after_select)
        self._tk_widget.bind('<<TreeviewOpen>>', self._on_after_expand)
        self._tk_widget.bind('<<TreeviewClose>>', self._on_after_collapse)
        self._tk_widget.bind('<Button-1>', self._on_node_mouse_click)
        self._tk_widget.bind('<Double-1>', self._on_node_mouse_double_click)
        # For BeforeSelect, BeforeExpand, BeforeCollapse, BeforeCheck, BeforeLabelEdit: placeholders, Tkinter doesn't support before events directly
        # For AfterCheck, AfterLabelEdit: placeholders, Treeview doesn't have built-in checkboxes or label editing
        
        # Añadir nodos iniciales
        for node in self.Nodes:
            self.AddNode(node)
    
    @property
    def SelectedNode(self):
        """Obtiene el nodo seleccionado."""
        selection = self._tk_widget.selection()
        if selection:
            # Map back to TreeNode (simplified)
            item_text = self._tk_widget.item(selection[0], 'text')
            # Find in Nodes (placeholder)
            return TreeNode(Text=item_text)
        return None
    
    def AddNode(self, node, parent=''):
        """Añade un TreeNode al TreeView."""
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
        """Handler for AfterSelect event."""
        selected = self._tk_widget.selection()
        if selected:
            node = self._find_node_by_id(selected[0])
            self.AfterSelect(self, {'Node': node, 'Action': 'Unknown'})
    
    def _on_after_expand(self, event):
        """Handler for AfterExpand event."""
        item = self._tk_widget.focus()
        if item:
            node = self._find_node_by_id(item)
            self.AfterExpand(self, {'Node': node})
    
    def _on_after_collapse(self, event):
        """Handler for AfterCollapse event."""
        item = self._tk_widget.focus()
        if item:
            node = self._find_node_by_id(item)
            self.AfterCollapse(self, {'Node': node})
    
    def _on_node_mouse_click(self, event):
        """Handler for NodeMouseClick event."""
        item = self._tk_widget.identify_row(event.y)
        if item:
            node = self._find_node_by_id(item)
            self.NodeMouseClick(self, {'Node': node, 'Button': event.num, 'X': event.x, 'Y': event.y})
    
    def _on_node_mouse_double_click(self, event):
        """Handler for NodeMouseDoubleClick event."""
        item = self._tk_widget.identify_row(event.y)
        if item:
            node = self._find_node_by_id(item)
            self.NodeMouseDoubleClick(self, {'Node': node, 'Button': event.num, 'X': event.x, 'Y': event.y})
    
    def _find_node_by_id(self, item_id):
        """Encuentra el TreeNode por item_id (placeholder)."""
        # Simplified: not implemented fully
        return None


class MonthCalendar(ControlBase):
    """
    Representa un MonthCalendar con propiedades VB.NET.
    
    Uso - Opción 1 (asignación de propiedades):
        cal = MonthCalendar(form)
        cal.Left = 10
        cal.Top = 10
        cal.Width = 220
        cal.ShowWeekNumbers = True
    
    Uso - Opción 2 (diccionario):
        cal = MonthCalendar(form, {'Left': 10, 'Top': 10, 'ShowWeekNumbers': True})
    """
    
    def __init__(self, master_form, props=None):
        defaults = {
            'Left': 10,
            'Top': 10,
            'Width': 200,
            'Height': 200,
            'Name': "",
            'SelectionRange': None,
            'SelectionStart': None,
            'SelectionEnd': None,
            'MaxSelectionCount': 7,
            'MinDate': None,
            'MaxDate': None,
            'TodayDate': None,
            'ShowToday': True,
            'ShowTodayCircle': True,
            'ShowWeekNumbers': False,
            'CalendarDimensions': (1, 1),
            'FirstDayOfWeek': "Sunday",
            'BoldedDates': None,
            'AnnuallyBoldedDates': None,
            'MonthlyBoldedDates': None
        }
        
        if props:
            defaults.update(props)
        
        super().__init__(master_form._root, defaults['Left'], defaults['Top'])
        
        self.Name = defaults['Name']
        
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.SelectionRange = defaults['SelectionRange'] or (defaults['SelectionStart'], defaults['SelectionEnd'])
        self.SelectionStart = defaults['SelectionStart']
        self.SelectionEnd = defaults['SelectionEnd']
        self.MaxSelectionCount = defaults['MaxSelectionCount']
        self.MinDate = defaults['MinDate']
        self.MaxDate = defaults['MaxDate']
        self.TodayDate = defaults['TodayDate'] or str(date.today())
        self.ShowToday = defaults['ShowToday']
        self.ShowTodayCircle = defaults['ShowTodayCircle']
        self.ShowWeekNumbers = defaults['ShowWeekNumbers']
        self.CalendarDimensions = defaults['CalendarDimensions']
        self.FirstDayOfWeek = defaults['FirstDayOfWeek']
        self.BoldedDates = defaults['BoldedDates'] or []
        self.AnnuallyBoldedDates = defaults['AnnuallyBoldedDates'] or []
        self.MonthlyBoldedDates = defaults['MonthlyBoldedDates'] or []
        
        # Eventos VB
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
        
        self._place_control(self.Width, self.Height)
        
        # Bind events
        if hasattr(self._tk_widget, 'bind'):
            self._tk_widget.bind('<<CalendarSelected>>', self._on_date_changed)
            self._tk_widget.bind('<ButtonRelease-1>', self._on_mouse_up)
            self._tk_widget.bind('<Double-1>', self._on_double_click)
            # For DayHeaderClick, RightToLeftLayoutChanged, Paint, BoldedDatesChanged: placeholders
    
    def _on_date_changed(self, event):
        """Handler for DateChanged and DateSelected events."""
        selected_date = self._tk_widget.get_date()
        self.DateChanged(self, {'Start': selected_date, 'End': selected_date})
        self.DateSelected(self, {'Start': selected_date, 'End': selected_date})
    
    def _on_mouse_up(self, event):
        """Handler for MouseUp event."""
        self.MouseUp(self, {'Button': event.num, 'X': event.x, 'Y': event.y})
    
    def _on_double_click(self, event):
        """Handler for DoubleClick event."""
        self.DoubleClick()


class DateTimePicker(ControlBase):
    """
    Representa un DateTimePicker con propiedades VB.NET.
    
    Uso - Opción 1 (asignación de propiedades):
        dtp = DateTimePicker(form)
        dtp.Left = 10
        dtp.Top = 10
        dtp.Width = 200
        dtp.Format = "Short"
    
    Uso - Opción 2 (diccionario):
        dtp = DateTimePicker(form, {'Left': 10, 'Top': 10, 'Format': 'Short'})
    """
    
    def __init__(self, master_form, props=None):
        defaults = {
            'Left': 10,
            'Top': 10,
            'Width': 150,
            'Height': 25,
            'Name': "",
            'Value': None,
            'Format': "Long",
            'CustomFormat': "",
            'MinDate': None,
            'MaxDate': None,
            'ShowUpDown': False,
            'ShowCheckBox': False,
            'CalendarForeColor': None,
            'TitleBackColor': None
        }
        
        if props:
            defaults.update(props)
        
        super().__init__(master_form._root, defaults['Left'], defaults['Top'])
        
        self.Name = defaults['Name']
        
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self._value = defaults['Value'] or datetime.now()
        self._format = defaults['Format']
        self._custom_format = defaults['CustomFormat']
        self.MinDate = defaults['MinDate']
        self.MaxDate = defaults['MaxDate']
        self.ShowUpDown = defaults['ShowUpDown']
        self.ShowCheckBox = defaults['ShowCheckBox']
        self.CalendarForeColor = defaults['CalendarForeColor']
        self.TitleBackColor = defaults['TitleBackColor']
        
        # Eventos VB
        self.ValueChanged = lambda sender, e: None
        self.FormatChanged = lambda sender, e: None
        self.DropDown = lambda sender, e: None
        self.CloseUp = lambda sender, e: None
        self.CheckedChanged = lambda sender, e: None
        
        # Placeholder: use Entry with button for calendar
        self._frame = tk.Frame(self.master)
        self._entry = tk.Entry(self._frame, width=self.Width//10)
        self._button = tk.Button(self._frame, text="...", command=self._open_calendar)
        self._entry.pack(side='left')
        self._button.pack(side='left')
        self._tk_widget = self._frame
        
        # Set initial value
        self._update_display()
        
        self._place_control(self.Width, self.Height)
        
        # Bind events
        self._button.bind('<Button-1>', self._on_drop_down)
        # For CloseUp, trigger after _open_calendar
        # For CheckedChanged, placeholder if ShowCheckBox
    
    def _update_display(self):
        """Actualiza el display según Format."""
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
        """Abre un calendario para seleccionar fecha (placeholder)."""
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
        """Handler for DropDown event."""
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
    """Representa un rectángulo con coordenadas y dimensiones."""
    
    def __init__(self, x=0, y=0, width=0, height=0):
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height


class classproperty:
    """Descriptor for class properties."""
    
    def __init__(self, fget):
        self.fget = fget
    
    def __get__(self, obj, cls=None):
        return self.fget(cls)


class Screen:
    """Representa la pantalla (Screen)."""
    
    def __init__(self, root=None):
        self._root = root or tk.Tk()  # Create a dummy root if none provided
    
    @property
    def Width(self):
        """Ancho de la pantalla."""
        return self._root.winfo_screenwidth()
    
    @property
    def Height(self):
        """Alto de la pantalla."""
        return self._root.winfo_screenheight()
    
    @property
    def Bounds(self):
        """Límites de la pantalla."""
        return Rectangle(0, 0, self.Width, self.Height)
    
    @property
    def WorkingArea(self):
        """Área de trabajo de la pantalla."""
        # Placeholder: assuming full screen for now
        return Rectangle(0, 0, self.Width, self.Height)
    
    @property
    def DeviceName(self):
        """Nombre del dispositivo de la pantalla."""
        return "Primary Screen"
    
    @property
    def BitsPerPixel(self):
        """Bits por píxel de la pantalla."""
        # Placeholder: assuming 32-bit
        return 32
    
    @classproperty
    def PrimaryScreen(cls):
        """Pantalla primaria."""
        return Screen()
    
    @classproperty
    def AllScreens(cls):
        """Todas las pantallas."""
        return [Screen()]
    
    # Eventos del sistema (placeholders, ya que Tkinter no soporta eventos de cambio de configuración de pantalla directamente)
    DisplaySettingsChanging = lambda sender, e: None  # Se produce antes de que la configuración de la pantalla cambie
    DisplaySettingsChanged = lambda sender, e: None   # Se produce después de que la configuración de la pantalla ha cambiado


class Point:
    """Representa un punto con coordenadas X e Y."""
    
    def __init__(self, x=0, y=0):
        self.X = x
        self.Y = y


class Size:
    """Representa un tamaño con ancho y alto."""
    
    def __init__(self, width=0, height=0):
        self.Width = width
        self.Height = height


class Form:
    """
    Representa la ventana principal (Form).
    
    Uso - Opción 1: form = Form(); form.Text = "Mi App"; form.Width = 800
    Uso - Opción 2: form = Form({'Text': 'Mi App', 'Width': 800, 'Height': 600})
    """
    
    def __init__(self, props=None):
        defaults = {
            'Title': "WinFormPy Application",
            'Width': 500,
            'Height': 300,
            'Name': "",
            'AutoScroll': False
        }
        
        if props:
            defaults.update(props)
            # Alias: Text es equivalente a Title
            if 'Text' in props:
                defaults['Title'] = props['Text']
        
        self._root = tk.Tk()
        
        # Propiedades VB principales
        self.Name = defaults['Name'] or "Form1"
        self._text_value = defaults['Title']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.Size = Size(self.Width, self.Height)
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
        self.AutoScroll = defaults['AutoScroll']
        
        # Lista interna para mantener una referencia a todos los controles
        self.Controls = [] 
        
        # Propiedades adicionales
        self.BackgroundImage = None
        self.Font = None
        self.FontColor = None
        
        # Si AutoScroll está activado, crear estructura con Canvas y Scrollbars
        if self.AutoScroll:
            # Frame principal que contendrá el canvas y scrollbars
            self._main_frame = tk.Frame(self._root)
            self._main_frame.pack(fill='both', expand=True)
            
            # Canvas para contenido desplazable
            self._canvas = tk.Canvas(
                self._main_frame,
                highlightthickness=0
            )
            
            # Scrollbars
            self._v_scrollbar = tk.Scrollbar(
                self._main_frame,
                orient='vertical',
                command=self._canvas.yview
            )
            self._h_scrollbar = tk.Scrollbar(
                self._main_frame,
                orient='horizontal',
                command=self._canvas.xview
            )
            
            # Configurar canvas con scrollbars
            self._canvas.configure(
                yscrollcommand=self._v_scrollbar.set,
                xscrollcommand=self._h_scrollbar.set
            )
            
            # Frame interno que contendrá los controles
            self._scroll_frame = tk.Frame(self._canvas)
            self._canvas_window = self._canvas.create_window(
                (0, 0),
                window=self._scroll_frame,
                anchor='nw'
            )
            
            # Posicionar scrollbars y canvas
            self._v_scrollbar.pack(side='right', fill='y')
            self._h_scrollbar.pack(side='bottom', fill='x')
            self._canvas.pack(side='left', fill='both', expand=True)
            
            # Actualizar región desplazable cuando cambia el tamaño
            self._scroll_frame.bind('<Configure>', self._on_form_scroll_frame_configure)
            self._canvas.bind('<Configure>', self._on_form_canvas_configure)
            
            # Soporte para rueda del ratón
            self._canvas.bind('<Enter>', self._bind_form_mousewheel)
            self._canvas.bind('<Leave>', self._unbind_form_mousewheel)
            
            # El contenedor para controles será el scroll_frame
            self._container = self._scroll_frame
        else:
            # Sin AutoScroll, el contenedor es el root
            self._container = self._root 
        
        # Eventos VB para formularios (inspirado en ControlBase)
        self.Load = lambda: None  # Inicialización, antes de mostrar el formulario
        self.FormClosing = lambda sender, e: None  # Antes de cerrarse, permite cancelar
        self.FormClosed = lambda: None  # Después de cerrarse
        self.Activated = lambda: None  # Cuando el formulario se activa
        self.Deactivate = lambda: None  # Cuando el formulario pierde el foco
        self.Resize = lambda: None  # Al redimensionar
        self.Move = lambda: None  # Al mover (placeholder)
        self.ControlAdded = lambda control: None  # Cuando se añade un control
        self.ControlRemoved = lambda control: None  # Cuando se elimina un control 

    @property
    def Text(self):
        """Obtiene el título del formulario."""
        return self._text_value

    @Text.setter
    def Text(self, value):
        """Establece el título del formulario."""
        self._text_value = value
        if hasattr(self, '_root') and self._root:
            self._root.title(value)

    def Show(self):
        """Inicia el bucle principal."""
        # Aplicar propiedades VB
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

    def ShowDialog(self):
        """Muestra el formulario como un diálogo modal."""
        self.Show()
        
    def _close(self):
        """Maneja el cierre del formulario."""
        e = {'Cancel': False}
        self.FormClosing(self, e)
        if not e['Cancel']:
            self._root.destroy()
            self.FormClosed()
    
    def Close(self):
        """Cierra el formulario."""
        self._close()

    def ForceUpdate(self):
        """Procesa eventos pendientes de la GUI y refresca la ventana."""
        if hasattr(self, '_root') and self._root:
            try:
                self._root.update_idletasks()
                self._root.update()
            except tk.TclError:
                pass

    def get_Parent(self):
        """Obtiene el control padre del Form.
        
        Para el Form principal, normalmente no hay padre (retorna None).
        
        Returns:
            None para Form principal.
        """
        return None
    
    def AddControl(self, control):
        """Añade un control a la Form con posiciones relativas.
        
        Implementa la jerarquía de visibilidad de Windows Forms:
        - El control se añade a la Form (se convierte en su padre)
        - El control solo será visible si su propia propiedad Visible es True
        """
        self.Controls.append(control)
        
        # Configurar el contenedor del control (usar _container si hay AutoScroll)
        control.master = self._container if hasattr(self, '_container') else self._root
        
        # Registrar este Form como wrapper del contenedor para la jerarquía de padres
        if not hasattr(control.master, '_control_wrapper'):
            control.master._control_wrapper = self
        
        # Reposicionar el control en el nuevo contenedor
        control._place_control()
        
        # Heredar propiedades del contenedor
        if hasattr(control, 'Enabled') and hasattr(self, 'Enabled'):
            control.Enabled = self.Enabled
            if hasattr(control, '_tk_widget'):
                try:
                    control._tk_widget.config(state='normal' if self.Enabled else 'disabled')
                except tk.TclError:
                    pass
        
        # Actualizar región de scroll si AutoScroll está activado
        if self.AutoScroll and hasattr(self, '_scroll_frame'):
            self._scroll_frame.update_idletasks()
            self._canvas.configure(scrollregion=self._canvas.bbox('all'))
        
        # Invocar evento ControlAdded
        self.ControlAdded(control)
    
    def RemoveControl(self, control):
        """Elimina un control de la Form."""
        if control in self.Controls:
            self.Controls.remove(control)
            self.ControlRemoved(control)
    
    def _on_form_scroll_frame_configure(self, event):
        """Actualiza la región de scroll cuando cambia el contenido del Form."""
        if hasattr(self, '_canvas'):
            self._canvas.configure(scrollregion=self._canvas.bbox('all'))
    
    def _on_form_canvas_configure(self, event):
        """Ajusta el ancho del frame interno al ancho del canvas."""
        if hasattr(self, '_canvas') and hasattr(self, '_canvas_window'):
            canvas_width = event.width
            self._canvas.itemconfig(self._canvas_window, width=canvas_width)
    
    def _bind_form_mousewheel(self, event):
        """Habilita el scroll con la rueda del ratón en el Form."""
        if hasattr(self, '_canvas'):
            # Windows y MacOS
            self._canvas.bind_all('<MouseWheel>', self._on_form_mousewheel)
            # Linux
            self._canvas.bind_all('<Button-4>', self._on_form_mousewheel)
            self._canvas.bind_all('<Button-5>', self._on_form_mousewheel)
    
    def _unbind_form_mousewheel(self, event):
        """Deshabilita el scroll con la rueda del ratón en el Form."""
        if hasattr(self, '_canvas'):
            self._canvas.unbind_all('<MouseWheel>')
            self._canvas.unbind_all('<Button-4>')
            self._canvas.unbind_all('<Button-5>')
    
    def _on_form_mousewheel(self, event):
        """Maneja el scroll con la rueda del ratón en el Form."""
        if hasattr(self, '_canvas'):
            # Windows y MacOS
            if event.num == 5 or event.delta < 0:
                self._canvas.yview_scroll(1, 'units')
            elif event.num == 4 or event.delta > 0:
                self._canvas.yview_scroll(-1, 'units')

class MDIParent(Form):
    """
    Representa el formulario padre MDI.
    
    Uso - Opción 1: parent = MDIParent(); parent.Text = "MDI App"; parent.Width = 1024
    Uso - Opción 2: parent = MDIParent({'Text': 'MDI App', 'Width': 1024, 'Height': 768})
    """
    
    def __init__(self, props=None):
        defaults = {
            'Title': "MDI Parent",
            'Width': 800,
            'Height': 600
        }
        
        if props:
            defaults.update(props)
            # Alias: Text es equivalente a Title
            if 'Text' in props:
                defaults['Title'] = props['Text']
        
        super().__init__(defaults)
        
        self.IsMdiContainer = True  # Configura como contenedor MDI
        self.MDIChildren = []
        self.MainMenuStrip = None  # Placeholder para MenuStrip principal
        
        # Eventos específicos de MDIParent
        self.MdiChildActivate = lambda sender, e: None  # Se produce cuando un formulario hijo MDI obtiene o pierde el foco, o se maximiza/minimiza
        self.ControlAdded = lambda control: None  # Se produce cuando se añade un nuevo control/formulario hijo
        self.ControlRemoved = lambda control: None  # Se produce cuando se cierra o elimina un formulario hijo
    
    @property
    def ActiveMdiChild(self):
        """Obtiene el formulario hijo MDI activo."""
        # Placeholder: devuelve el último añadido o None
        return self.MDIChildren[-1] if self.MDIChildren else None
    
    @property
    def MdiChildren(self):
        """Obtiene la matriz de formularios hijos MDI."""
        return self.MDIChildren
    
    def AddMDIChild(self, child):
        """Añade un hijo MDI."""
        self.MDIChildren.append(child)
        child.MdiParent = self  # Asignar el MDIParent
        child._frame.pack(in_=self._root, fill='both', expand=True)
        # Bind para MdiChildActivate
        child._frame.bind('<FocusIn>', lambda e: self.MdiChildActivate(self, {'Child': child, 'Action': 'Activated'}))
        child._frame.bind('<FocusOut>', lambda e: self.MdiChildActivate(self, {'Child': child, 'Action': 'Deactivated'}))
        self.ControlAdded(child)
    
    def RemoveMDIChild(self, child):
        """Quita un hijo MDI."""
        if child in self.MDIChildren:
            self.MDIChildren.remove(child)
            child._frame.pack_forget()
            self.ControlRemoved(child)
    
    def LayoutMdi(self, layout):
        """Organiza los formularios hijos MDI.
        
        layout: 'Cascade', 'TileHorizontal', 'TileVertical', 'ArrangeIcons'
        """
        # Placeholder: implementación básica no disponible en Tkinter
        # En VB.NET, organiza las ventanas hijas
        pass


class StatusBarPanel:
    """
    Representa un panel individual dentro de un StatusBar.
    
    Uso - Opción 1: panel = StatusBarPanel(); panel.Text = "Ready"; panel.Width = 150
    Uso - Opción 2: panel = StatusBarPanel({'Text': 'Ready', 'Width': 150})
    """
    
    def __init__(self, props=None):
        defaults = {
            'Text': "",
            'Width': 100,
            'AutoSize': "None",
            'Icon': None,
            'ToolTipText': "",
            'Bevel': "Sunken",
            'Style': "Text"
        }
        
        if props:
            defaults.update(props)
        
        self._text = defaults['Text']
        self.Width = defaults['Width']
        self.AutoSize = defaults['AutoSize']  # 'None', 'Spring', 'Contents'
        self.Icon = defaults['Icon']
        self.ToolTipText = defaults['ToolTipText']
        self.Bevel = defaults['Bevel']  # 'Raised', 'Sunken', 'None'
        self.Style = defaults['Style']  # 'Text', 'OwnerDraw'
        self.MinWidth = 10
        self.Alignment = "Left"  # 'Left', 'Center', 'Right'
        self.BorderStyle = "Sunken"
        
        # Referencias internas
        self._parent_statusbar = None
        self._frame = None
        self._label = None
        self._icon_label = None
        
        # Eventos
        self.Click = lambda: None
        self.DoubleClick = lambda: None
    
    @property
    def Text(self):
        """Obtiene el texto del panel."""
        return self._text
    
    @Text.setter
    def Text(self, value):
        """Establece el texto del panel."""
        self._text = value
        if self._label:
            self._label.config(text=value)
    
    def _create_widget(self, parent_frame):
        """Crea el widget tkinter para este panel."""
        # Frame contenedor del panel
        relief_map = {
            'Raised': 'raised',
            'Sunken': 'sunken',
            'None': 'flat'
        }
        
        self._frame = tk.Frame(
            parent_frame,
            relief=relief_map.get(self.Bevel, 'sunken'),
            borderwidth=2,
            width=self.Width
        )
        
        # Label para el icono (si existe)
        if self.Icon:
            self._icon_label = tk.Label(self._frame, image=self.Icon)
            self._icon_label.pack(side='left', padx=2)
        
        # Label para el texto
        anchor_map = {
            'Left': 'w',
            'Center': 'center',
            'Right': 'e'
        }
        
        self._label = tk.Label(
            self._frame,
            text=self._text,
            anchor=anchor_map.get(self.Alignment, 'w')
        )
        self._label.pack(side='left', fill='both', expand=True, padx=2)
        
        # Bind eventos
        self._frame.bind('<Button-1>', lambda e: self.Click())
        self._frame.bind('<Double-Button-1>', lambda e: self.DoubleClick())
        self._label.bind('<Button-1>', lambda e: self.Click())
        self._label.bind('<Double-Button-1>', lambda e: self.DoubleClick())
        
        # Tooltip
        if self.ToolTipText:
            self._create_tooltip(self._frame, self.ToolTipText)
            self._create_tooltip(self._label, self.ToolTipText)
        
        # Si AutoSize es 'None', desactivar propagación para respetar el ancho fijo
        if self.AutoSize == 'None':
            self._frame.pack_propagate(False)
        
        return self._frame
    
    def _create_tooltip(self, widget, text):
        """Crea un tooltip simple para el widget."""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=text, background="lightyellow", 
                           relief="solid", borderwidth=1, padx=5, pady=2)
            label.pack()
            widget._tooltip = tooltip
        
        def hide_tooltip(event):
            if hasattr(widget, '_tooltip'):
                widget._tooltip.destroy()
                delattr(widget, '_tooltip')
        
        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)


class StatusBar(ControlBase):
    """
    Control de barra de estado de Windows Forms.
    
    Uso - Opción 1 (asignación de propiedades):
        sb = StatusBar(form)
        sb.Text = "Ready"
        sb.Width = 800
        sb.ShowPanels = False
    
    Uso - Opción 2 (diccionario):
        sb = StatusBar(form, {'Text': 'Ready', 'Width': 800, 'ShowPanels': False})
    """
    
    def __init__(self, master_form, props=None):
        defaults = {
            'Text': "Ready",
            'Left': 0,
            'Top': 570,
            'Width': 800,
            'Height': 25,
            'ShowPanels': False,
            'SizingGrip': True,
            'BorderStyle': "Fixed3D",
            'Name': ""
        }
        
        if props:
            use_system_styles = props.pop('UseSystemStyles', None)
            defaults.update(props)
            if use_system_styles:
                SystemStyles.ApplyToDefaults(defaults, control_type="Status", use_system_styles=True)
        else:
            SystemStyles.ApplyToDefaults(defaults, control_type="Status")
        
        super().__init__(master_form._root, defaults['Left'], defaults['Top'])
        
        # Propiedades básicas
        self.Name = defaults['Name']
        self._text = defaults['Text']
        self.Width = defaults['Width']
        self.Height = defaults['Height']
        self.ShowPanels = defaults['ShowPanels']
        self.SizingGrip = defaults['SizingGrip']
        self.BorderStyle = defaults['BorderStyle']
        self.BackColor = 'SystemButtonFace'
        self.ForeColor = 'black'
        self.Font = ('Segoe UI', 9)
        
        # Colección de paneles
        self.Panels = []
        
        # Referencias internas
        self._master_form = master_form
        
        # Eventos
        self.PanelClick = lambda sender, panel: None
        self.DrawItem = lambda sender, e: None
        
        # Crear widget principal
        relief_map = {
            'None': 'flat',
            'Fixed3D': 'ridge',
            'FixedSingle': 'solid'
        }
        
        self._tk_widget = tk.Frame(
            self.master,
            relief=relief_map.get(self.BorderStyle, 'ridge'),
            borderwidth=1 if self.BorderStyle != 'None' else 0,
            bg=self.BackColor,
            height=self.Height
        )
        
        # Frame contenedor para paneles o texto simple
        self._content_frame = tk.Frame(self._tk_widget, bg=self.BackColor)
        self._content_frame.pack(side='left', fill='both', expand=True)
        
        # Label para texto simple (cuando ShowPanels = False)
        self._text_label = tk.Label(
            self._content_frame,
            text=self._text,
            bg=self.BackColor,
            fg=self.ForeColor,
            font=self.Font,
            anchor='w',
            padx=5
        )
        
        # Grip de redimensionamiento
        if self.SizingGrip:
            self._grip_canvas = tk.Canvas(
                self._tk_widget,
                width=15,
                height=self.Height,
                bg=self.BackColor,
                highlightthickness=0
            )
            self._grip_canvas.pack(side='right')
            self._draw_sizing_grip()
        
        # Mostrar el contenido apropiado
        self._update_display()
        
        # Posicionar el control
        if hasattr(self, '_visible') and self._visible:
            self._place_control(self.Width, self.Height)
    
    @property
    def ShowPanels(self):
        """Indica si se muestran los paneles o el texto simple."""
        return getattr(self, '_show_panels', False)

    @ShowPanels.setter
    def ShowPanels(self, value):
        self._show_panels = value
        if hasattr(self, '_content_frame'):
            self._update_display()

    @property
    def Text(self):
        """Obtiene el texto de la barra de estado."""
        return self._text
    
    @Text.setter
    def Text(self, value):
        """Establece el texto de la barra de estado."""
        self._text = value
        if self._text_label:
            self._text_label.config(text=value)
    
    def AddPanel(self, panel):
        """Añade un panel a la colección de paneles.
        
        Args:
            panel: Objeto StatusBarPanel a añadir
        """
        self.Panels.append(panel)
        panel._parent_statusbar = self
        if self.ShowPanels:
            self._update_display()
    
    def RemovePanel(self, panel):
        """Elimina un panel de la colección.
        
        Args:
            panel: Objeto StatusBarPanel a eliminar
        """
        if panel in self.Panels:
            self.Panels.remove(panel)
            if self.ShowPanels:
                self._update_display()
    
    def _update_display(self):
        """Actualiza la visualización según ShowPanels."""
        # Limpiar contenido anterior
        for widget in self._content_frame.winfo_children():
            widget.destroy()
        
        if self.ShowPanels and self.Panels:
            # Mostrar paneles
            self._display_panels()
        else:
            # Mostrar texto simple
            self._text_label = tk.Label(
                self._content_frame,
                text=self._text,
                bg=self.BackColor,
                fg=self.ForeColor,
                font=self.Font,
                anchor='w',
                padx=5
            )
            self._text_label.pack(side='left', fill='both', expand=True)
    
    def _display_panels(self):
        """Muestra los paneles en el StatusBar."""
        total_width = self.Width - (15 if self.SizingGrip else 0)
        
        # Calcular anchos según AutoSize
        spring_panels = [p for p in self.Panels if p.AutoSize == 'Spring']
        fixed_panels = [p for p in self.Panels if p.AutoSize != 'Spring']
        
        # Ancho usado por paneles fijos
        fixed_width = sum(p.Width for p in fixed_panels)
        
        # Ancho disponible para paneles Spring
        available_width = total_width - fixed_width
        spring_width = available_width // len(spring_panels) if spring_panels else 0
        
        for index, panel in enumerate(self.Panels):
            panel_widget = panel._create_widget(self._content_frame)
            
            # Configurar ancho según AutoSize
            if panel.AutoSize == 'Spring':
                panel_widget.config(width=spring_width)
                panel_widget.pack(side='left', fill='both', expand=True, padx=2, pady=2)
            elif panel.AutoSize == 'Contents':
                panel_widget.pack(side='left', fill='y', padx=2, pady=2)
            else:  # 'None'
                panel_widget.config(width=panel.Width)
                panel_widget.pack(side='left', fill='y', padx=2, pady=2)
            
            # Bind evento PanelClick
            panel_widget.bind('<Button-1>', lambda e, p=panel: self._on_panel_click(p))

            # Añadir una línea delimitadora para resaltar la división entre paneles
            if index < len(self.Panels) - 1:
                separator = tk.Frame(self._content_frame, width=1, bg=SystemColors.ActiveBorder)
                separator.pack(side='left', fill='y', pady=4)
    
    def _on_panel_click(self, panel):
        """Maneja el clic en un panel."""
        self.PanelClick(self, panel)
        panel.Click()
    
    def _draw_sizing_grip(self):
        """Dibuja el grip de redimensionamiento."""
        canvas = self._grip_canvas
        h = self.Height
        
        # Dibujar líneas diagonales (estilo Windows)
        for i in range(3):
            x = 12 - i * 4
            canvas.create_line(x, h-3, x+3, h-6, fill='gray', width=1)
            canvas.create_line(x+1, h-3, x+4, h-6, fill='white', width=1)
    
    def Dock(self, side='bottom'):
        """Ancla el StatusBar a un lado del formulario.
        
        Args:
            side: 'bottom', 'top', 'left', 'right'
        """
        self._tk_widget.pack_forget()
        if side == 'bottom':
            self._tk_widget.pack(side='bottom', fill='x')
        elif side == 'top':
            self._tk_widget.pack(side='top', fill='x')
        elif side == 'left':
            self._tk_widget.pack(side='left', fill='y')
        elif side == 'right':
            self._tk_widget.pack(side='right', fill='y')


class MDIChild:
    """
    Representa un formulario hijo MDI.
    
    Uso - Opción 1: child = MDIChild(); child.Title = "Child Window"
    Uso - Opción 2: child = MDIChild({'Title': 'Child Window', 'WindowState': 'Maximized'})
    """
    
    def __init__(self, props=None):
        defaults = {
            'Title': "Child",
            'MdiParent': None,
            'ControlBox': True,
            'MinimizeBox': True,
            'MaximizeBox': True,
            'ShowInTaskbar': False,
            'WindowState': "Normal"
        }
        
        if props:
            defaults.update(props)
            # Alias: Text es equivalente a Title
            if 'Text' in props:
                defaults['Title'] = props['Text']
        
        self.Title = defaults['Title']
        self._text_value = defaults['Title']  # Alias para Title
        self.MdiParent = defaults['MdiParent']  # Asignar el MDIParent
        self.IsMdiChild = True  # Indica que es un formulario hijo MDI
        self.ControlBox = defaults['ControlBox']
        self.MinimizeBox = defaults['MinimizeBox']
        self.MaximizeBox = defaults['MaximizeBox']
        self.ShowInTaskbar = defaults['ShowInTaskbar']
        self.WindowState = defaults['WindowState']  # 'Normal', 'Minimized', 'Maximized'
        self.MainMenuStrip = None  # Placeholder para MenuStrip
        
        self._frame = tk.Frame()
        self.Controls = []
        
        # Eventos principales de MDIChild
        self.Load = lambda: None  # Inicialización, antes de ser visible
        self.FormClosing = lambda sender, e: None  # Antes de cerrarse, permite cancelar
        self.FormClosed = lambda: None  # Después de cerrarse
        self.Activated = lambda: None  # Cuando se activa dentro del MDIParent
        self.Deactivate = lambda: None  # Cuando pierde el foco
        self.Resize = lambda: None  # Al redimensionar
        self.Move = lambda: None  # Al mover (placeholder, sin barra de título en Tkinter) 

        # Bind events
        self._frame.bind('<FocusIn>', lambda e: self.Activated())
        self._frame.bind('<FocusOut>', lambda e: self.Deactivate())
        self._frame.bind('<Configure>', lambda e: self.Resize())
        # Move placeholder: no direct bind for move in Tkinter Frame
    
    @property
    def Text(self):
        """Obtiene el título del formulario hijo MDI."""
        return self._text_value

    @Text.setter
    def Text(self, value):
        """Establece el título del formulario hijo MDI."""
        self._text_value = value
        self.Title = value  # Mantener sincronizado con Title
    
    def Show(self):
        """Muestra el formulario hijo MDI (placeholder)."""
        # En la implementación actual, se muestra mediante AddMDIChild del padre
        self.Load()  # Trigger Load event
    
    def Close(self):
        """Cierra el formulario hijo MDI."""
        # Trigger FormClosing, allow cancel
        e = {'Cancel': False}
        self.FormClosing(self, e)
        if not e['Cancel']:
            # Proceed to close
            if self.MdiParent:
                self.MdiParent.RemoveMDIChild(self)
            self.FormClosed()  # Trigger FormClosed
    
    def get_Parent(self):
        """Obtiene el control padre del MdiChildForm.
        
        El padre de un MdiChildForm es el MdiParent (Form principal).
        
        Returns:
            El MdiParent si existe, None en caso contrario.
        """
        return getattr(self, 'MdiParent', None)
    
    def AddControl(self, control):
        """Añade un control al hijo MDI.
        
        Implementa la jerarquía de visibilidad de Windows Forms:
        - El control se añade al MdiChildForm (se convierte en su padre)
        - El control solo será visible si su propia propiedad Visible es True
          Y el MdiChildForm está visible
        """
        self.Controls.append(control)
        control.master = self._frame
        
        # Registrar este MdiChildForm como wrapper del frame para la jerarquía de padres
        if not hasattr(self._frame, '_control_wrapper'):
            self._frame._control_wrapper = self
        
        control._place_control()


class SendKeys:
    """Clase para enviar pulsaciones de teclas y combinaciones de teclas al proceso activo."""
    
    @staticmethod
    def _parse_keys(keys):
        """Parse the keys string to handle special codes."""
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
        """Envía las pulsaciones de teclas inmediatamente."""
        parsed_keys = SendKeys._parse_keys(keys)
        focused = tk.focus_get()
        if focused and hasattr(focused, 'insert'):
            focused.insert(tk.END, parsed_keys)
    
    @staticmethod
    def SendWait(keys):
        """Envía las pulsaciones de teclas y espera a que se procesen."""
        # En Tkinter, es sincrónico, así que igual que Send
        SendKeys.Send(keys)


class Timer:
    """
    Representa un Timer para eventos temporizados.
    
    Uso - Opción 1: timer = Timer(root); timer.Interval = 2000; timer.Enabled = True
    Uso - Opción 2: timer = Timer(root, {'Interval': 2000, 'Enabled': True})
    """
    
    def __init__(self, root, props=None):
        defaults = {
            'interval': 1000,
            'Name': "",
            'Enabled': False,
            'Tag': None,
            'Modifiers': "Private"
        }
        
        if props:
            defaults.update(props)
            # Alias: Interval (mayúscula) también es válido
            if 'Interval' in props:
                defaults['interval'] = props['Interval']
        
        self._root = root
        self.Name = defaults['Name']
        self.Interval = defaults['interval']
        self._enabled = False  # Initialize _enabled before property setter usage
        self.Enabled = defaults['Enabled']
        self.Tag = defaults['Tag']  # Objeto personalizado
        self.Modifiers = defaults['Modifiers']  # 'Public', 'Private', etc. (placeholder)
        self.Tick = lambda: None
        self._job = None
        
        # Iniciar si Enabled
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
        """Inicia el timer."""
        if not self._enabled:
            self._enabled = True
            self._schedule()

    def Stop(self):
        """Detiene el timer."""
        self._enabled = False
        if self._job:
            self._root.after_cancel(self._job)

    def _schedule(self):
        """Programa el siguiente tick."""
        if self._enabled:
            self.Tick()
            self._job = self._root.after(self.Interval, self._schedule)

