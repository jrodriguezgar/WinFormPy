# Controles de Layout Automático - winformpy_extended

Extensión del módulo `winformpy` con herramientas avanzadas de layout automático que simplifican la organización de controles sin gestionar manualmente las propiedades `Location` y `Size`.

## Controles Implementados

### 1. FlowLayoutPanel

Control contenedor que organiza controles secundarios en una secuencia direccional (horizontal o vertical) con ajuste automático.

#### Características Principales

- **FlowDirection**: Dirección del flujo

  - `'LeftToRight'`: Izquierda a derecha (predeterminado)
  - `'RightToLeft'`: Derecha a izquierda
  - `'TopDown'`: Arriba a abajo
  - `'BottomUp'`: Abajo a arriba
- **WrapContents**: Si `True` (predeterminado), los controles pasan a la siguiente línea/columna cuando no hay espacio
- **Padding**: Espaciado interno del panel `(left, top, right, bottom)`
- **AutoScroll**: Añade scrollbars cuando el contenido no cabe

#### Uso Básico

```python
from winformpy import Form, Button
from winformpy_extended import FlowLayoutPanel

# Crear formulario
form = Form({'Text': 'FlowLayout Demo', 'Width': 500, 'Height': 400})

# Crear FlowLayoutPanel
flowPanel = FlowLayoutPanel(form, {
    'Left': 10,
    'Top': 10,
    'Width': 460,
    'Height': 350,
    'FlowDirection': 'LeftToRight',
    'WrapContents': True,
    'Padding': (5, 5, 5, 5)
})

# Añadir botones - se organizan automáticamente
for i in range(10):
    Button(flowPanel, {'Text': f'Botón {i+1}', 'Width': 80, 'Height': 30})
```

#### Casos de Uso Ideales

- ✅ Barras de herramientas con botones
- ✅ Menús dinámicos
- ✅ Listas de elementos con orden lineal
- ✅ Galerías de imágenes o tarjetas
- ✅ Paneles de navegación lateral

#### Ejemplo: Barra de Herramientas

```python
toolbar = FlowLayoutPanel(form, {
    'Left': 0,
    'Top': 0,
    'Width': 800,
    'Height': 60,
    'FlowDirection': 'LeftToRight',
    'BackColor': '#E0E0E0',
    'Dock': 'Top'
})

# Los botones se organizan automáticamente de izquierda a derecha
for name in ['Nuevo', 'Abrir', 'Guardar', 'Cortar', 'Copiar', 'Pegar']:
    Button(toolbar, {'Text': name, 'Width': 70, 'Height': 35})
```

---

### 2. TableLayoutPanel

Control contenedor que organiza controles en una cuadrícula de filas y columnas con redimensionamiento proporcional automático.

#### Características Principales

- **RowCount**: Número de filas
- **ColumnCount**: Número de columnas
- **RowStyles**: Lista de tuplas `(SizeType, Value)` para cada fila
- **ColumnStyles**: Lista de tuplas `(SizeType, Value)` para cada columna

#### Tipos de Tamaño (SizeType)

1. **`'Absolute'`**: Tamaño fijo en píxeles

   ```python
   ('Absolute', 50)  # 50 píxeles fijos
   ```
2. **`'Percent'`**: Porcentaje del espacio disponible (clave para autolayout)

   ```python
   ('Percent', 33.33)  # 33.33% del espacio
   ```
3. **`'AutoSize'`**: Se ajusta al contenido más grande

   ```python
   ('AutoSize', 0)  # Valor ignorado, se calcula automáticamente
   ```

#### Uso Básico

```python
from pentano.gui.winform-py.lib.winform-py import Form, Label, TextBox
from pentano.gui.winform-py.lib.winform-py_extended import TableLayoutPanel

# Crear formulario
form = Form({'Text': 'TableLayout Demo', 'Width': 600, 'Height': 400})

# Crear TableLayoutPanel con 3 filas y 2 columnas
tablePanel = TableLayoutPanel(form, {
    'Left': 10,
    'Top': 10,
    'Width': 560,
    'Height': 350,
    'RowCount': 3,
    'ColumnCount': 2,
    'RowStyles': [
        ('Percent', 33.33),  # Fila 1: 33.33%
        ('Percent', 33.33),  # Fila 2: 33.33%
        ('Percent', 33.34)   # Fila 3: 33.34%
    ],
    'ColumnStyles': [
        ('Percent', 30),     # Columna 1: 30% (etiquetas)
        ('Percent', 70)      # Columna 2: 70% (campos)
    ]
})

# Añadir controles a celdas específicas
label_nombre = Label(tablePanel, {'Text': 'Nombre:', 'TextAlign': 'e'})
tablePanel.AddControl(label_nombre, column=0, row=0)

text_nombre = TextBox(tablePanel, {'Width': 300})
text_nombre.Dock = 'Fill'  # Llenar toda la celda
tablePanel.AddControl(text_nombre, column=1, row=0)
```

#### Métodos Útiles

```python
# Añadir control a celda específica
tablePanel.AddControl(control, column=1, row=2)

# Cambiar posición de un control
tablePanel.SetCellPosition(control, column=0, row=1)

# Obtener posición de un control
row, col = tablePanel.GetCellPosition(control)

# Cambiar número de filas/columnas
tablePanel.set_RowCount(5)
tablePanel.set_ColumnCount(3)

# Actualizar estilos
tablePanel.set_RowStyles([('Percent', 50), ('Percent', 50)])
tablePanel.set_ColumnStyles([('Absolute', 100), ('Percent', 100)])
```

#### Casos de Uso Ideales

- ✅ Formularios de entrada de datos
- ✅ Dashboards con secciones proporcionadas
- ✅ Layouts complejos con alineación precisa
- ✅ Diseños responsive que se adaptan al tamaño
- ✅ Grillas de contenido (ej. galería de productos)

#### Ejemplo: Formulario de Registro

```python
# Formulario con etiquetas (30%) y campos (70%)
tablePanel = TableLayoutPanel(form, {
    'RowCount': 4,
    'ColumnCount': 2,
    'RowStyles': [('Percent', 25)] * 4,
    'ColumnStyles': [('Percent', 30), ('Percent', 70)]
})

# Fila 0: Nombre
Label(tablePanel, {'Text': 'Nombre:'})
tablePanel.AddControl(Label(...), column=0, row=0)
text_nombre = TextBox(tablePanel)
text_nombre.Dock = 'Fill'
tablePanel.AddControl(text_nombre, column=1, row=0)

# Fila 1: Email
Label(tablePanel, {'Text': 'Email:'})
tablePanel.AddControl(Label(...), column=0, row=1)
text_email = TextBox(tablePanel)
text_email.Dock = 'Fill'
tablePanel.AddControl(text_email, column=1, row=1)

# ... y así sucesivamente
```

---

## Combinación de Layouts

Puedes anidar `FlowLayoutPanel` y `TableLayoutPanel` para crear diseños complejos y totalmente responsive:

```python
# Layout principal: TableLayoutPanel (estructura general)
mainTable = TableLayoutPanel(form, {
    'RowCount': 2,
    'ColumnCount': 2,
    'RowStyles': [
        ('Absolute', 60),   # Header fijo
        ('Percent', 100)    # Contenido dinámico
    ],
    'ColumnStyles': [
        ('Percent', 70),    # Área principal
        ('Percent', 30)     # Sidebar
    ]
})

# Header: FlowLayoutPanel para botones
toolbar = FlowLayoutPanel(form, {
    'FlowDirection': 'LeftToRight',
    'BackColor': '#2C3E50'
})
toolbar.Dock = 'Fill'
mainTable.AddControl(toolbar, column=0, row=0)

# Contenido principal: FlowLayoutPanel vertical
contentPanel = FlowLayoutPanel(form, {
    'FlowDirection': 'TopDown',
    'BackColor': 'White'
})
contentPanel.Dock = 'Fill'
mainTable.AddControl(contentPanel, column=0, row=1)

# Sidebar: FlowLayoutPanel para acciones rápidas
sidebarPanel = FlowLayoutPanel(form, {
    'FlowDirection': 'TopDown',
    'BackColor': '#ECF0F1'
})
sidebarPanel.Dock = 'Fill'
mainTable.AddControl(sidebarPanel, column=1, row=1)
```

---

## Ventajas del Layout Automático

### ✅ Sin Cálculos Manuales

No necesitas calcular `Left`, `Top`, `Width`, `Height` para cada control.

### ✅ Diseño Responsive

Los controles se ajustan automáticamente al redimensionar el contenedor.

### ✅ Código Más Limpio

Menos líneas de código repetitivo para posicionar controles.

### ✅ Fácil Mantenimiento

Agregar, quitar o reorganizar controles es trivial.

### ✅ Diseños Complejos

Combinando layouts puedes crear interfaces profesionales fácilmente.

---

## Comparación: Antes vs Después

### ANTES (Manual)

```python
# Posicionamiento manual - tedioso y propenso a errores
button1 = Button(form, {'Left': 10, 'Top': 10, 'Width': 80, 'Height': 30})
button2 = Button(form, {'Left': 100, 'Top': 10, 'Width': 80, 'Height': 30})
button3 = Button(form, {'Left': 190, 'Top': 10, 'Width': 80, 'Height': 30})
# Si cambias el tamaño de button1, debes recalcular todo...
```

### DESPUÉS (Automático)

```python
# Layout automático - simple y adaptable
flowPanel = FlowLayoutPanel(form, {'FlowDirection': 'LeftToRight'})
Button(flowPanel, {'Width': 80, 'Height': 30, 'Text': 'Botón 1'})
Button(flowPanel, {'Width': 80, 'Height': 30, 'Text': 'Botón 2'})
Button(flowPanel, {'Width': 80, 'Height': 30, 'Text': 'Botón 3'})
# Se organizan automáticamente, sin importar el tamaño
```

---

## Ejemplos Completos

Consulta los ejemplos completos en:

- `examples/test_layout_panels.py` - Ejemplos básicos y avanzados
- `examples/dashboard_demo.py` - Dashboard completo con layouts anidados

Para ejecutar:

```bash
python examples/test_layout_panels.py
```

---

## Notas Técnicas

### Auto-registro

Ambos controles heredan de `Panel`, por lo que tienen auto-registro implementado:

```python
flowPanel = FlowLayoutPanel(form, {...})
# Se registra automáticamente en form.Controls ✅
```

### Propiedad Dock

Los controles dentro de `TableLayoutPanel` pueden usar `Dock='Fill'` para llenar toda su celda:

```python
textbox = TextBox(tablePanel)
textbox.Dock = 'Fill'  # Ocupa toda la celda
```

### Reorganización Automática

Ambos controles reorganizan el layout automáticamente cuando:

- Se añade o quita un control
- Se cambia `FlowDirection` o estilos de filas/columnas
- Se redimensiona el panel contenedor

---

## Compatibilidad

✅ Compatible con todos los controles de `winform-py`
✅ Soporta auto-registro de controles
✅ Funciona con propiedades `Dock` y `Anchor`
✅ Compatible con `Visible`, `Enabled`, y eventos

---

## Próximas Características

- [ ] SplitContainer para paneles redimensionables
- [ ] DockPanel para anclar controles en bordes
- [ ] GridPanel para mallas más avanzadas
- [ ] Animaciones al reorganizar controles

---

**Autor**: Vibe coding by DatamanEdge
**Versión**: 1.0.4
**Licencia**: MIT
