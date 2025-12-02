# LabelFrame en Contenedores winform-py

## Introducción

Este documento explica cómo funciona el uso de `LabelFrame` de Tkinter en los contenedores de winform-py (Panel y GroupBox), específicamente la interacción entre el padding del LabelFrame (`padx`/`pady`) y el posicionamiento de controles internos usando coordenadas relativas (`relwidth`/`relheight`).

## Conceptos Fundamentales

### LabelFrame de Tkinter

`LabelFrame` es un widget de Tkinter que combina:
- Un **Frame** (contenedor) con borde
- Un **Label** (título) integrado en el borde superior
- **Padding interno** configurable (`padx`, `pady`)

### Ventajas sobre Frame + Label separados

| Aspecto | Frame + Label | LabelFrame |
|---------|---------------|------------|
| Título | Posicionamiento manual | Automático, integrado en borde |
| Padding | Cálculo manual de espacios | Automático con padx/pady |
| Consistencia | Requiere ajustes manuales | Estándar de Tkinter |
| Código | Más líneas, más complejo | Más simple y mantenible |

## Arquitectura de Contenedores

### GroupBox

```python
LabelFrame (widget principal)
│   ├─ text: "Título del GroupBox"
│   ├─ padx: 10  # Padding horizontal
│   ├─ pady: 20  # Padding vertical
│   ├─ relief: 'groove'
│   └─ borderwidth: 2
│
└── Frame (_container)
    │   ├─ posición: place(x=0, y=0, relwidth=1, relheight=1)
    │   └─ bg: color heredado
    │
    └── Controles hijos
        ├─ Button (Left=10, Top=10)
        ├─ Label (Left=10, Top=50)
        └─ TextBox (Left=10, Top=80)
```

### Panel (con título)

```python
LabelFrame (widget principal)
│   ├─ text: "Título del Panel"
│   ├─ padx: 0-10
│   ├─ pady: 0-10
│   ├─ relief: configurable ('flat', 'groove', etc.)
│   └─ borderwidth: configurable
│
└── Frame (_container)
    │   ├─ posición: place(x=0, y=0, relwidth=1, relheight=1)
    │   └─ bg: color heredado
    │
    └── Controles hijos
```

### Panel (sin título)

```python
Frame (widget principal)
│   ├─ padx: configurable
│   ├─ pady: configurable
│   ├─ relief: configurable
│   └─ borderwidth: configurable
│
└── _container = _tk_widget (mismo widget)
    └── Controles hijos
```

## Funcionamiento del Padding

### padx y pady en LabelFrame

Cuando configuras `padx` y `pady` en un LabelFrame:

```python
labelframe = tk.LabelFrame(parent, text="Título", padx=10, pady=20)
```

Tkinter **automáticamente** crea un espacio interno:
- **padx**: Espacio horizontal a izquierda y derecha (10px cada lado = 20px total)
- **pady**: Espacio vertical arriba y abajo (20px cada lado = 40px total)

### Interacción con relwidth/relheight

Cuando colocas un widget hijo con coordenadas relativas:

```python
container = tk.Frame(labelframe, bg="lightblue")
container.place(x=0, y=0, relwidth=1, relheight=1)
```

**Comportamiento de Tkinter:**
1. `relwidth=1` significa "100% del ancho **disponible**"
2. El ancho disponible = ancho total del LabelFrame - (2 × padx) - borde
3. `relheight=1` significa "100% del alto **disponible**"
4. El alto disponible = alto total del LabelFrame - (2 × pady) - borde - espacio del título

**Resultado:**
- El `container` **respeta automáticamente** el padding del LabelFrame
- No necesitas calcular `width=-2*padx` manualmente
- El área de contenido está perfectamente centrada

## Ejemplo Práctico

### Código de Prueba

```python
import tkinter as tk

root = tk.Tk()

# LabelFrame con padding
lf = tk.LabelFrame(
    root,
    text="Ejemplo con Padding",
    padx=10,      # 10px de margen horizontal
    pady=20,      # 20px de margen vertical
    relief="groove",
    borderwidth=2,
    bg="yellow"
)
lf.pack(padx=20, pady=20, fill="both", expand=True)

# Container interno con relwidth=1, relheight=1
container = tk.Frame(lf, bg="lightblue")
container.place(x=0, y=0, relwidth=1, relheight=1)

# Control en (0,0) del container
label = tk.Label(container, text="(0,0)", bg="red", fg="white")
label.place(x=0, y=0)

root.mainloop()
```

### Resultado Visual

```
┌─────── Ejemplo con Padding ────────┐
│ ↕ pady=20                          │
│ ┌──────────────────────────────┐ ↔ │
│ │  (0,0)                       │   │ padx=10
│ │  [Container Lightblue]       │   │
│ │                              │   │
│ └──────────────────────────────┘   │
│ ↕ pady=20                          │
└────────────────────────────────────┘
```

El label "(0,0)" está:
- A 10px del borde izquierdo (por padx)
- A 20px del borde superior (por pady + altura del título)
- Las coordenadas (0,0) son relativas al container, no al LabelFrame

## Implementación en winform-py

### GroupBox - Código

```python
class GroupBox(ControlBase):
    def __init__(self, master_form, props=None):
        # ... configuración inicial ...
        
        # Obtener padding
        padding = self._padding
        if isinstance(padding, tuple) and len(padding) == 4:
            padx_left, pady_top, padx_right, pady_bottom = padding
            padx = (padx_left + padx_right) // 2
            pady = (pady_top + pady_bottom) // 2
        elif isinstance(padding, tuple) and len(padding) == 2:
            padx, pady = padding
        else:
            padx, pady = 10, 20  # Valores por defecto
        
        # Crear LabelFrame principal
        self._tk_widget = tk.LabelFrame(
            self.master,
            text=self._text,
            width=self.Width,
            height=self.Height,
            relief='groove',
            borderwidth=2,
            bg=self.BackColor,
            fg=self.ForeColor,
            font=self.Font,
            padx=padx,    # ← Padding horizontal
            pady=pady     # ← Padding vertical
        )
        
        # Crear container interno
        self._container = tk.Frame(
            self._tk_widget,
            bg=self.BackColor,
            highlightthickness=0
        )
        
        # ¡CLAVE! Usar relwidth=1, relheight=1 para respetar padding
        self._container.place(x=0, y=0, relwidth=1, relheight=1)
        self._container.pack_propagate(False)
        self._container.grid_propagate(False)
```

### Panel - Código

```python
class Panel(ControlBase):
    def __init__(self, master_form, props=None):
        # ... configuración inicial ...
        
        # Crear LabelFrame si tiene título
        if self._text:
            self._tk_widget = tk.LabelFrame(
                self.master,
                text=self._text,
                width=self.Width,
                height=self.Height,
                padx=padx,
                pady=pady,
                # ... otras configuraciones ...
            )
            
            # Si NO tiene AutoScroll, crear container interno
            if not self.AutoScroll:
                self._container = tk.Frame(
                    self._tk_widget,
                    bg=self.BackColor,
                    highlightthickness=0
                )
                # Usar relwidth=1, relheight=1
                self._container.place(x=0, y=0, relwidth=1, relheight=1)
                self._container.pack_propagate(False)
                self._container.grid_propagate(False)
        else:
            # Frame simple sin título
            self._tk_widget = tk.Frame(...)
            self._container = self._tk_widget
```

## Beneficios del Enfoque

### 1. Simplicidad
- No necesitas calcular manualmente la altura del título
- No necesitas ajustar coordenadas para compensar bordes
- Tkinter gestiona todo automáticamente

### 2. Precisión
```python
# ANTES (Frame + Label manual):
# - Calcular title_height = 18px (aproximado)
# - Posicionar _container en y = title_height + 3
# - Ajustar width con -6px para compensar bordes

# AHORA (LabelFrame):
# - place(x=0, y=0, relwidth=1, relheight=1)
# - Tkinter calcula todo automáticamente
```

### 3. Mantenibilidad
- Si cambias el padding, todo se ajusta automáticamente
- Si cambias el tamaño del GroupBox, el container se redimensiona
- No hay "números mágicos" en el código

### 4. Consistencia con Tkinter
- Uso estándar de LabelFrame
- Comportamiento predecible
- Documentación de Tkinter aplicable directamente

## Posicionamiento de Controles Hijos

### Coordenadas Absolutas

Cuando creas un control en un GroupBox/Panel:

```python
groupbox = GroupBox(form, {'Text': 'Opciones', 'Padding': (10, 20)})

button = Button(groupbox, {
    'Left': 0,    # Posición relativa al _container
    'Top': 0,     # No relativa al LabelFrame
    'Width': 100
})
groupbox.AddControl(button)
```

**Resultado:**
- Button aparece en (0, 0) del **_container**
- El _container está a (padx, pady + título) del LabelFrame
- Efecto visual: Button con margen automático

### Ejemplo Visual

```
GroupBox con Padding (10, 20)
┌───── Título ─────────────────┐
│ ↕ 20px                       │
│ ┌─────────────────────────┐  │
│ │ ┌──────┐                │  │
│ │ │Button│ ← (0,0) del    │ ↔│ 10px
│ │ └──────┘   container    │  │
│ │                         │  │
│ └─────────────────────────┘  │
│ ↕ 20px                       │
└──────────────────────────────┘
       ↔ 10px
```

## AutoSize y LabelFrame

El cálculo de AutoSize se simplifica con LabelFrame:

### Código Anterior (Frame + Label)

```python
# Calcular altura del título manualmente
title_label = self._title_label
title_height = title_label.winfo_reqheight()  # ~18-20px

# Agregar espacios y bordes
border_padding = 3
required_width = max_right + padx * 2 + border_padding * 2
required_height = max_bottom + pady * 2 + title_height + border_padding * 2
```

### Código Actual (LabelFrame)

```python
# LabelFrame gestiona título y bordes automáticamente
# Solo necesitamos calcular el contenido + padding

required_width = max_right + padx * 2
required_height = max_bottom + pady * 2

# Tkinter añade automáticamente:
# - Espacio del título
# - Bordes (borderwidth)
# - Ajustes internos
```

## Casos de Uso

### 1. GroupBox Estándar

```python
groupbox = GroupBox(form, {
    'Text': 'Configuración',
    'Left': 10,
    'Top': 10,
    'Width': 200,
    'Height': 150,
    'Padding': (10, 20),  # padx=10, pady=20
    'BackColor': '#f0f0f0'
})

label = Label(groupbox, {'Text': 'Nombre:', 'Left': 0, 'Top': 0})
textbox = TextBox(groupbox, {'Left': 70, 'Top': 0, 'Width': 100})
button = Button(groupbox, {'Text': 'OK', 'Left': 0, 'Top': 30})

groupbox.AddControl(label)
groupbox.AddControl(textbox)
groupbox.AddControl(button)
```

**Resultado:** Controles con margen uniforme de 10px (izq/der) y 20px (arriba/abajo)

### 2. Panel con Título y AutoSize

```python
panel = Panel(form, {
    'Text': 'Resultados',
    'Left': 10,
    'Top': 10,
    'Padding': (5, 10),
    'AutoSize': True,
    'AutoSizeMode': 'GrowAndShrink'
})

# Panel se redimensiona automáticamente al contenido + padding
```

### 3. Padding Asimétrico

```python
groupbox = GroupBox(form, {
    'Text': 'Detalles',
    'Padding': (5, 10, 15, 20)  # left, top, right, bottom
    # Se convierte a padx=(5+15)/2=10, pady=(10+20)/2=15
})
```

## Características No Implementadas y Mejoras

### ✅ Implementado

1. ✓ LabelFrame en GroupBox
2. ✓ LabelFrame en Panel (con título)
3. ✓ Container interno con relwidth/relheight
4. ✓ Padding automático
5. ✓ AutoSize con LabelFrame
6. ✓ Manejo de padding asimétrico (4 valores)

### ⚠️ Pendientes de Implementación

#### 1. **Font dinámico para título**

**Problema actual:**
```python
self._tk_widget = tk.LabelFrame(
    font=self.Font if self.Font else ('TkDefaultFont', 9)  # Font fijo
)
```

**Mejora propuesta:**
```python
@property
def Font(self):
    return self._font

@Font.setter
def Font(self, value):
    self._font = value
    if self._tk_widget and isinstance(self._tk_widget, tk.LabelFrame):
        self._tk_widget.config(font=value)
```

#### 2. **ForeColor dinámico para título**

**Problema actual:**
```python
fg=self.ForeColor if self.ForeColor else 'black'  # Color fijo al crear
```

**Mejora propuesta:**
```python
@property
def ForeColor(self):
    return self._forecolor

@ForeColor.setter
def ForeColor(self, value):
    self._forecolor = value
    if self._tk_widget and isinstance(self._tk_widget, tk.LabelFrame):
        self._tk_widget.config(fg=value)
```

#### 3. **LabelAnchor** (posición del título)

En Tkinter, LabelFrame soporta `labelanchor` para posicionar el título:

**Valores posibles:**
- `'n'`, `'ne'`, `'e'`, `'se'`, `'s'`, `'sw'`, `'w'`, `'nw'`

**Implementación sugerida:**
```python
class GroupBox(ControlBase):
    def __init__(self, master_form, props=None):
        defaults = {
            # ... propiedades existentes ...
            'LabelAnchor': 'nw',  # Por defecto: noroeste (arriba-izquierda)
        }
        
        self._tk_widget = tk.LabelFrame(
            # ... configuración existente ...
            labelanchor=defaults['LabelAnchor']
        )
```

#### 4. **BorderStyle para GroupBox**

**Actualmente:** GroupBox tiene `relief='groove'` fijo

**Mejora propuesta:**
```python
defaults = {
    # ... propiedades existentes ...
    'BorderStyle': 'groove',  # Permitir otros valores
}

relief_map = {
    'None': 'flat',
    'Fixed3D': 'groove',
    'FixedSingle': 'solid',
    'flat': 'flat',
    'groove': 'groove',
    'raised': 'raised',
    'ridge': 'ridge',
    'solid': 'solid',
    'sunken': 'sunken'
}

self._tk_widget = tk.LabelFrame(
    relief=relief_map.get(self.BorderStyle, 'groove')
)
```

#### 5. **AutoSize para Panel con título**

**Problema:** Panel con LabelFrame no tiene `_apply_autosize_panel` actualizado

**Verificar:** Si el cálculo de AutoSize necesita ajustes para LabelFrame

#### 6. **Validación de Padding**

**Mejora propuesta:**
```python
@Padding.setter
def Padding(self, value):
    """Establece el padding interno."""
    # Validar valores
    if isinstance(value, tuple):
        if len(value) == 2:
            padx, pady = value
            if padx < 0 or pady < 0:
                raise ValueError("Padding no puede ser negativo")
        elif len(value) == 4:
            if any(p < 0 for p in value):
                raise ValueError("Padding no puede ser negativo")
        else:
            raise ValueError("Padding debe ser tupla de 2 o 4 valores")
    
    self._padding = value
    # ... resto del código ...
```

## Comparación: Antes vs Ahora

### Antes (Frame + Label manual)

```python
# Crear Frame principal
self._tk_widget = tk.Frame(master, relief='groove', borderwidth=2)

# Crear Label para título (manual)
title_label = tk.Label(
    self._tk_widget,
    text=self._text,
    bg=self.BackColor
)
title_label.place(x=10, y=0, height=18)  # Altura fija, posición manual

# Crear container (cálculos manuales)
title_height = 18
self._container = tk.Frame(self._tk_widget)
self._container.place(
    x=3,                          # Margen manual
    y=title_height + 3,           # Después del título
    relwidth=1,
    width=-6,                     # Compensar bordes
    relheight=1,
    height=-(title_height + 6)    # Compensar título y bordes
)
```

**Problemas:**
- ❌ Números mágicos (3, 6, 18)
- ❌ Cálculos manuales propensos a errores
- ❌ Difícil de mantener
- ❌ Título no se actualiza automáticamente

### Ahora (LabelFrame)

```python
# Crear LabelFrame (todo integrado)
self._tk_widget = tk.LabelFrame(
    master,
    text=self._text,
    relief='groove',
    borderwidth=2,
    padx=10,                      # Padding horizontal
    pady=20                       # Padding vertical
)

# Crear container (simple y automático)
self._container = tk.Frame(self._tk_widget)
self._container.place(x=0, y=0, relwidth=1, relheight=1)
```

**Ventajas:**
- ✅ Sin números mágicos
- ✅ Tkinter gestiona todo automáticamente
- ✅ Fácil de mantener
- ✅ Título integrado y actualizable
- ✅ Padding configurable y preciso

## Debugging y Troubleshooting

### Problema: Controles no aparecen

**Causa:** No llamaste a `AddControl()`

```python
# ❌ MAL: Control no se agrega a Controls[]
button = Button(groupbox, {'Left': 10, 'Top': 10})

# ✅ BIEN: Control registrado correctamente
button = Button(groupbox, {'Left': 10, 'Top': 10})
groupbox.AddControl(button)
```

### Problema: Padding no se aplica

**Causa:** Padding se establece después de crear el widget

```python
# ❌ MAL: Padding después de crear
groupbox = GroupBox(form, {'Text': 'Test'})
groupbox.Padding = (10, 20)  # No se aplica al LabelFrame existente

# ✅ BIEN: Padding en la inicialización
groupbox = GroupBox(form, {'Text': 'Test', 'Padding': (10, 20)})
```

**Solución con setter:**
```python
@Padding.setter
def Padding(self, value):
    self._padding = value
    if self._tk_widget:
        # Actualizar LabelFrame dinámicamente
        padx, pady = self._parse_padding(value)
        self._tk_widget.config(padx=padx, pady=pady)
```

### Problema: AutoSize no funciona

**Causa:** Controles no están en `Controls[]`

```python
# Verificar
print(f"Controles: {len(groupbox.Controls)}")

# Si es 0, asegúrate de llamar AddControl()
```

## Mejores Prácticas

### 1. Siempre usa AddControl()

```python
button = Button(groupbox, {'Left': 10, 'Top': 10})
groupbox.AddControl(button)  # ← Obligatorio
```

### 2. Configura Padding en la inicialización

```python
groupbox = GroupBox(form, {
    'Text': 'Opciones',
    'Padding': (10, 20)  # ← Aquí, no después
})
```

### 3. Usa AutoSize cuando sea apropiado

```python
groupbox = GroupBox(form, {
    'Text': 'Dinámico',
    'AutoSize': True,
    'AutoSizeMode': 'GrowAndShrink'
})
```

### 4. Aprovecha relwidth/relheight para layouts dinámicos

```python
# Si necesitas que un control llene el container
textbox = TextBox(groupbox, {
    'Left': 0,
    'Top': 0,
    'Width': groupbox.Width - 20,  # Menos padding
    'Height': groupbox.Height - 40
})
```

## Referencias

- [Tkinter LabelFrame Documentation](https://docs.python.org/3/library/tkinter.html#tkinter.LabelFrame)
- [Tkinter place() Geometry Manager](https://docs.python.org/3/library/tkinter.html#the-place-manager)
- [Windows Forms GroupBox](https://learn.microsoft.com/en-us/dotnet/api/system.windows.forms.groupbox)
- [Windows Forms Panel](https://learn.microsoft.com/en-us/dotnet/api/system.windows.forms.panel)

## Conclusión

El uso de `LabelFrame` con `padx`/`pady` y un `_container` interno posicionado con `relwidth=1, relheight=1` proporciona:

1. **Simplicidad**: Menos código, menos cálculos manuales
2. **Precisión**: Tkinter gestiona bordes, título y padding automáticamente
3. **Mantenibilidad**: Cambios en padding o tamaño se propagan automáticamente
4. **Consistencia**: Comportamiento estándar de Tkinter

Esta arquitectura es la base para una implementación robusta y profesional de controles contenedores en winform-py.
