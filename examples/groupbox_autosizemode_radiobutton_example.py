"""
Ejemplo de GroupBox con AutoSize y RadioButtons.
Demuestra cómo el GroupBox se ajusta automáticamente al añadir opciones.
"""

import sys
import os

# Add module path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from winformpy.py file
import importlib.util
spec = importlib.util.spec_from_file_location("winformpy", 
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib", "winformpy.py"))
wfp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wfp)

# Alias para controles
Form = wfp.Form
GroupBox = wfp.GroupBox
RadioButton = wfp.RadioButton
Button = wfp.Button
Label = wfp.Label

# Crear formulario principal
form = Form({
    'Text': 'Ejemplo AutoSizeMode con RadioButtons',
    'Width': 500,
    'Height': 450
})

# -----------------------------------------------------------------------------
# GroupBox 1: GrowAndShrink (Se ajusta exactamente al contenido)
# -----------------------------------------------------------------------------
gb_shrink = GroupBox(form, {
    'Text': 'Modo: GrowAndShrink',
    'Left': 20,
    'Top': 20,
    'AutoSize': True,
    'AutoSizeMode': 'GrowAndShrink',
    'BackColor': '#e6f7ff'  # Azul claro
})

# Añadir algunos RadioButtons iniciales
rb1 = RadioButton(gb_shrink, {
    'Text': 'Opción A',
    'Left': 15,
    'Top': 25,
    'Width': 100,
    'Checked': True
})
# gb_shrink.AddControl(rb1) <-- ELIMINADO: Ya se registra automáticamente

rb2 = RadioButton(gb_shrink, {
    'Text': 'Opción B',
    'Left': 15,
    'Top': 55,
    'Width': 100
})
# gb_shrink.AddControl(rb2) <-- ELIMINADO: Ya se registra automáticamente

# -----------------------------------------------------------------------------
# GroupBox 2: GrowOnly (Crece pero no se encoge más allá de su tamaño original)
# -----------------------------------------------------------------------------
gb_grow = GroupBox(form, {
    'Text': 'Modo: GrowOnly (Min 200x60)',
    'Left': 250,
    'Top': 20,
    'Width': 200,
    'Height': 60,  # Altura inicial reducida para ver el efecto antes
    'AutoSize': True,
    'AutoSizeMode': 'GrowOnly',
    'BackColor': '#f6ffed'  # Verde claro
})

rb3 = RadioButton(gb_grow, {
    'Text': 'Opción 1',
    'Left': 15,
    'Top': 25,
    'Width': 100,
    'Checked': True
})
# gb_grow.AddControl(rb3) <-- ELIMINADO: Ya se registra automáticamente

# -----------------------------------------------------------------------------
# Controles para modificar dinámicamente
# -----------------------------------------------------------------------------
lbl_info = Label(form, {
    'Text': 'Añade o quita opciones para ver cómo se comportan los GroupBox:',
    'Left': 20,
    'Top': 250,
    'Width': 450,
    'AutoSize': True
})

lbl_size_shrink = Label(form, {
    'Text': 'Size: 0x0',
    'Left': 20,
    'Top': 270,
    'Width': 150,
    'ForeColor': 'blue'
})

lbl_size_grow = Label(form, {
    'Text': 'Size: 0x0',
    'Left': 250,
    'Top': 270,
    'Width': 150,
    'ForeColor': 'green'
})

def adjust_layout():
    """Ajusta la posición de los controles inferiores para evitar solapamiento."""
    # Forzar actualización de geometría para asegurar que Width/Height son correctos
    form._root.update_idletasks()
    
    # Actualizar etiquetas de tamaño
    lbl_size_shrink.Text = f"Size: {gb_shrink.Width}x{gb_shrink.Height}"
    lbl_size_grow.Text = f"Size: {gb_grow.Width}x{gb_grow.Height}"
    
    # --- AJUSTE HORIZONTAL ---
    # Si el GroupBox izquierdo crece mucho, empujar el derecho
    min_x_right = gb_shrink.Left + gb_shrink.Width + 20
    new_x_right = max(250, min_x_right)
    
    # Actualizar propiedades Left (sin forzar visual todavía)
    gb_grow.Left = new_x_right
    lbl_size_grow.Left = new_x_right
    btn_add_grow_v.Left = new_x_right
    btn_add_grow_h.Left = new_x_right
    btn_remove_grow.Left = new_x_right
    
    # --- AJUSTE VERTICAL ---
    # Calcular la posición Y más baja de los GroupBox
    bottom_shrink = gb_shrink.Top + gb_shrink.Height
    bottom_grow = gb_grow.Top + gb_grow.Height
    max_bottom = max(bottom_shrink, bottom_grow)
    
    # Margen de separación
    margin = 20
    start_y = max(250, max_bottom + margin)
    
    # Actualizar propiedades Top
    lbl_info.Top = start_y
    lbl_size_shrink.Top = start_y + 25
    lbl_size_grow.Top = start_y + 25
    
    btn_add_shrink_v.Top = start_y + 55
    btn_add_shrink_h.Top = start_y + 90
    btn_remove_shrink.Top = start_y + 125
    
    btn_add_grow_v.Top = start_y + 55
    btn_add_grow_h.Top = start_y + 90
    btn_remove_grow.Top = start_y + 125
    
    # --- FORZAR ACTUALIZACIÓN VISUAL (WORKAROUND) ---
    # Aplicar .place() explícitamente para todos los controles móviles
    # Esto asegura que tanto el movimiento horizontal como el vertical se apliquen visualmente
    controls_to_update = [
        gb_grow,
        lbl_info,
        lbl_size_shrink, lbl_size_grow,
        btn_add_shrink_v, btn_add_shrink_h, btn_remove_shrink,
        btn_add_grow_v, btn_add_grow_h, btn_remove_grow
    ]
    
    for c in controls_to_update:
        if hasattr(c, '_tk_widget'):
            c._tk_widget.place(x=c.Left, y=c.Top)

    # Ajustar ancho/alto del formulario
    required_width = new_x_right + gb_grow.Width + 40
    required_height = btn_remove_grow.Top + btn_remove_grow.Height + 40
    
    resize_needed = False
    if form.Width < required_width:
        form.Width = required_width
        resize_needed = True
    if form.Height < required_height:
        form.Height = required_height
        resize_needed = True
        
    if resize_needed:
        form._root.geometry(f"{form.Width}x{form.Height}")
    
    # Forzar repintado
    form._root.update()

# Vincular evento Resize para ajuste automático
gb_shrink.Resize = adjust_layout
gb_grow.Resize = adjust_layout

def add_shrink_vertical():
    # Buscar el control más abajo
    max_bottom = 0
    for c in gb_shrink.Controls:
        if hasattr(c, 'Top') and hasattr(c, 'Height'):
            max_bottom = max(max_bottom, c.Top + c.Height)
    
    if max_bottom == 0: max_bottom = 10 # Padding inicial
    
    count = len([c for c in gb_shrink.Controls if isinstance(c, RadioButton)])
    new_rb = RadioButton(gb_shrink, {
        'Text': f'V-{count+1}',
        'Left': 15,
        'Top': max_bottom + 5,
        'Width': 80
    })
    adjust_layout()

def add_shrink_horizontal():
    # Buscar el control más a la derecha
    max_right = 0
    for c in gb_shrink.Controls:
        # Asegurar que usamos valores actualizados
        if hasattr(c, '_tk_widget'):
            c._tk_widget.update_idletasks()
            
        if hasattr(c, 'Left') and hasattr(c, 'Width'):
            max_right = max(max_right, c.Left + c.Width)
            
    if max_right == 0: max_right = 10
    
    count = len([c for c in gb_shrink.Controls if isinstance(c, RadioButton)])
    new_rb = RadioButton(gb_shrink, {
        'Text': f'H-{count+1}',
        'Left': max_right + 5,
        'Top': 25, # Fila superior
        'Width': 80
    })
    adjust_layout()

def remove_option_shrink():
    radios = [c for c in gb_shrink.Controls if isinstance(c, RadioButton)]
    if radios:
        last_radio = radios[-1]
        gb_shrink.RemoveControl(last_radio)
    adjust_layout()

btn_add_shrink_v = Button(form, {
    'Text': 'Añadir 1 (V)',
    'Left': 20,
    'Top': 280,
    'Width': 150
})
btn_add_shrink_v.Click = add_shrink_vertical

btn_add_shrink_h = Button(form, {
    'Text': 'Añadir 1 (H)',
    'Left': 20,
    'Top': 315,
    'Width': 150
})
btn_add_shrink_h.Click = add_shrink_horizontal

btn_remove_shrink = Button(form, {
    'Text': 'Quitar Último (-)',
    'Left': 20,
    'Top': 350,
    'Width': 150
})
btn_remove_shrink.Click = remove_option_shrink

def add_grow_vertical():
    # Buscar el control más abajo
    max_bottom = 0
    for c in gb_grow.Controls:
        if hasattr(c, 'Top') and hasattr(c, 'Height'):
            max_bottom = max(max_bottom, c.Top + c.Height)
            
    if max_bottom == 0: max_bottom = 10
    
    count = len([c for c in gb_grow.Controls if isinstance(c, RadioButton)])
    new_rb = RadioButton(gb_grow, {
        'Text': f'V-{count+1}',
        'Left': 15,
        'Top': max_bottom + 5,
        'Width': 80
    })
    
    adjust_layout()

def add_grow_horizontal():
    # Buscar el control más a la derecha
    max_right = 0
    for c in gb_grow.Controls:
        # Asegurar que usamos valores actualizados
        if hasattr(c, '_tk_widget'):
            c._tk_widget.update_idletasks()
            
        if hasattr(c, 'Left') and hasattr(c, 'Width'):
            max_right = max(max_right, c.Left + c.Width)
            
    if max_right == 0: max_right = 10
    
    count = len([c for c in gb_grow.Controls if isinstance(c, RadioButton)])
    new_rb = RadioButton(gb_grow, {
        'Text': f'H-{count+1}',
        'Left': max_right + 5,
        'Top': 25,
        'Width': 80
    })
    adjust_layout()

def remove_option_grow():
    radios = [c for c in gb_grow.Controls if isinstance(c, RadioButton)]
    if radios:
        last_radio = radios[-1]
        gb_grow.RemoveControl(last_radio)
    adjust_layout()

btn_add_grow_v = Button(form, {
    'Text': 'Añadir 2 (V)',
    'Left': 250,
    'Top': 280,
    'Width': 150
})
btn_add_grow_v.Click = add_grow_vertical

btn_add_grow_h = Button(form, {
    'Text': 'Añadir 2 (H)',
    'Left': 250,
    'Top': 315,
    'Width': 150
})
btn_add_grow_h.Click = add_grow_horizontal

btn_remove_grow = Button(form, {
    'Text': 'Quitar Último (-)',
    'Left': 250,
    'Top': 350,
    'Width': 150
})
btn_remove_grow.Click = remove_option_grow

# Mostrar formulario
print("Iniciando ejemplo...")
print(f"Tamaño inicial GrowAndShrink: {gb_shrink.Width}x{gb_shrink.Height}")
print(f"Tamaño inicial GrowOnly: {gb_grow.Width}x{gb_grow.Height}")

# Ajustar diseño inicial
adjust_layout()

form.Show()
