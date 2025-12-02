# Dock y Anchor en Windows Forms y winformpy

Este documento explica las propiedades `Dock` y `Anchor` de Windows Forms y cómo se implementan en la biblioteca `winformpy`, que permite desarrollar interfaces gráficas similares a VB.NET/WinForms en Python usando Tkinter.

## Índice

1. [Introducción](#introducción)
2. [Propiedad Dock](#propiedad-dock)
3. [Propiedad Anchor](#propiedad-anchor)
4. [Implementación en winformpy](#implementación-en-winformpy)
5. [Ejemplos de Uso](#ejemplos-de-uso)
6. [Mejores Prácticas](#mejores-prácticas)
7. [Notas Técnicas](#notas-técnicas)

## Introducción

En Windows Forms (VB.NET/C#), las propiedades `Dock` y `Anchor` son fundamentales para crear interfaces responsive que se adaptan automáticamente al redimensionamiento de formularios y contenedores.

- **Dock**: "Acopla" un control a un borde del contenedor, haciendo que ocupe todo el espacio disponible en esa dirección.
- **Anchor**: "Ancla" un control a uno o más bordes del contenedor, manteniendo distancias fijas mientras permite redimensionamiento.

Estas propiedades eliminan la necesidad de calcular manualmente posiciones y tamaños al redimensionar la ventana.

## Propiedad Dock

### Concepto en Windows Forms

La propiedad `Dock` especifica qué borde del contenedor padre debe "acoplarse" el control. Cuando un control está acoplado:

- Ocupa todo el espacio disponible en la dirección especificada
- Se redimensiona automáticamente cuando cambia el tamaño del contenedor
- Puede combinarse con otros controles acoplados para crear layouts complejos

### Valores de Dock

- **`None`** (predeterminado): Sin acoplamiento, posicionamiento absoluto
- **`Top`**: Acoplado al borde superior, ocupa todo el ancho
- **`Bottom`**: Acoplado al borde inferior, ocupa todo el ancho
- **`Left`**: Acoplado al borde izquierdo, ocupa toda la altura
- **`Right`**: Acoplado al borde derecho, ocupa toda la altura
- **`Fill`**: Ocupa todo el espacio disponible del contenedor

### Orden de Acoplamiento

Cuando múltiples controles están acoplados en el mismo contenedor, el orden importa:

1. Controles `Top` se procesan primero (de arriba hacia abajo)
2. Controles `Bottom` se procesan después (de abajo hacia arriba)
3. Controles `Left` se procesan después (de izquierda a derecha)
4. Controles `Right` se procesan después (de derecha a izquierda)
5. Controles `Fill` ocupan el espacio restante

## Propiedad Anchor

### Concepto en Windows Forms

La propiedad `Anchor` especifica qué bordes del contenedor padre deben mantenerse a distancia fija del control. Es útil para:

- Mantener márgenes constantes al redimensionar
- Permitir que controles crezcan o se muevan con la ventana
- Crear layouts donde algunos controles permanecen fijos mientras otros se ajustan

### Valores de Anchor

`Anchor` es una combinación de bordes (flags):

- **`Top`**: Distancia fija al borde superior
- **`Bottom`**: Distancia fija al borde inferior
- **`Left`**: Distancia fija al borde izquierdo
- **`Right`**: Distancia fija al borde derecho

**Combinaciones comunes:**

- **`Top, Left`** (predeterminado): Esquina superior izquierda fija, control no se redimensiona
- **`Top, Bottom, Left`**: Altura variable, ancho fijo, esquina izquierda fija
- **`Top, Left, Right`**: Ancho variable, altura fija, borde superior fijo
- **`Top, Bottom, Left, Right`**: Control se redimensiona en ambas direcciones

### Comportamiento

- Si se ancla a lados opuestos (Left+Right), el control se estira horizontalmente
- Si se ancla a lados opuestos (Top+Bottom), el control se estira verticalmente
- Las distancias iniciales a los bordes se calculan cuando se muestra el control por primera vez

## Implementación en winformpy

### Compatibilidad con Windows Forms

`winformpy` implementa `Dock` y `Anchor` con alta fidelidad a Windows Forms:

```python
from winformpy import Form, Button, Panel

# Crear formulario
form = Form({'Text': 'Dock y Anchor Demo', 'Width': 600, 'Height': 400})

# Panel acoplado que ocupa toda la ventana
main_panel = Panel(form, {'Dock': 'Fill'})

# Botón anclado a la esquina inferior derecha
button = Button(main_panel, {
    'Text': 'OK',
    'Anchor': ['Bottom', 'Right'],
    'Width': 80,
    'Height': 30
})
```

### Propiedades Específicas

#### Dock

```python
control.Dock = 'Fill'  # Ocupa todo el espacio disponible
control.Dock = 'Top'   # Acoplado arriba
control.Dock = 'None'  # Sin acoplamiento (predeterminado)
```

#### Anchor

```python
control.Anchor = ['Top', 'Left']        # Predeterminado
control.Anchor = ['Top', 'Bottom', 'Left', 'Right']  # Se estira en ambas direcciones
control.Anchor = ['Bottom', 'Right']    # Esquina inferior derecha fija
```

### Soporte para Margin

Ambos sistemas respetan la propiedad `Margin` del control:

```python
button = Button(panel, {
    'Text': 'Botón con margen',
    'Dock': 'Bottom',
    'Margin': (10, 5, 10, 5)  # Izquierda, arriba, derecha, abajo
})
```

### Eventos de Redimensionamiento

- `Dock` se actualiza automáticamente en eventos `<Configure>` del contenedor
- `Anchor` calcula distancias iniciales en el primer evento `<Map>` o `<Configure>`
- Los cambios se aplican en tiempo real sin intervención del programador

## Ejemplos de Uso

### Ejemplo 1: Layout Básico con Dock

```python
from winformpy import Form, Panel, Button, TextBox

form = Form({'Text': 'Layout con Dock', 'Width': 500, 'Height': 400})

# Barra de herramientas arriba
toolbar = Panel(form, {
    'Dock': 'Top',
    'Height': 50,
    'BackColor': 'LightBlue'
})

# Barra de estado abajo
status_bar = Panel(form, {
    'Dock': 'Bottom',
    'Height': 30,
    'BackColor': 'LightGray'
})

# Panel principal que ocupa el espacio restante
main_panel = Panel(form, {
    'Dock': 'Fill',
    'BackColor': 'White'
})

# Contenido en el panel principal
text_box = TextBox(main_panel, {
    'Dock': 'Fill',
    'Multiline': True
})
```

### Ejemplo 2: Formulario con Anchor

```python
from winformpy import Form, Label, TextBox, Button

form = Form({'Text': 'Formulario con Anchor', 'Width': 400, 'Height': 300})

# Etiqueta que se estira horizontalmente
title_label = Label(form, {
    'Text': 'Título del Formulario',
    'Anchor': ['Top', 'Left', 'Right'],
    'Top': 20,
    'Left': 20,
    'Right': 20,
    'Height': 30,
    'TextAlign': 'center'
})

# Campo de texto que se estira
name_textbox = TextBox(form, {
    'Anchor': ['Top', 'Left', 'Right'],
    'Top': 70,
    'Left': 20,
    'Right': 20,
    'Height': 25
})

# Botones anclados a la esquina inferior derecha
ok_button = Button(form, {
    'Text': 'OK',
    'Anchor': ['Bottom', 'Right'],
    'Width': 80,
    'Height': 30,
    'Bottom': 20,
    'Right': 20
})

cancel_button = Button(form, {
    'Text': 'Cancelar',
    'Anchor': ['Bottom', 'Right'],
    'Width': 80,
    'Height': 30,
    'Bottom': 20,
    'Right': 120
})
```

### Ejemplo 3: Layout Complejo Combinado

```python
from winformpy import Form, Panel, Button, ListBox, TextBox

form = Form({'Text': 'Layout Complejo', 'Width': 800, 'Height': 600})

# Panel izquierdo para navegación
nav_panel = Panel(form, {
    'Dock': 'Left',
    'Width': 200,
    'BackColor': 'LightGray'
})

# Lista de navegación
nav_list = ListBox(nav_panel, {
    'Dock': 'Fill'
})

# Panel derecho que ocupa el resto
content_panel = Panel(form, {
    'Dock': 'Fill'
})

# Barra de herramientas en el contenido
toolbar = Panel(content_panel, {
    'Dock': 'Top',
    'Height': 40,
    'BackColor': 'WhiteSmoke'
})

# Área de contenido principal
main_area = Panel(content_panel, {
    'Dock': 'Fill'
})

# Botón flotante anclado abajo a la derecha
action_button = Button(main_area, {
    'Text': 'Acción',
    'Anchor': ['Bottom', 'Right'],
    'Width': 100,
    'Height': 35,
    'Bottom': 20,
    'Right': 20
})
```

## Mejores Prácticas

### Elegir entre Dock y Anchor

- **Usa Dock cuando:**

  - Quieres que un control ocupe todo el espacio disponible en una dirección
  - Creas layouts con secciones distintas (header, sidebar, footer, content)
  - El control debe redimensionarse proporcionalmente con el contenedor
- **Usa Anchor cuando:**

  - Quieres mantener márgenes fijos alrededor de un control
  - Algunos controles deben permanecer en posiciones fijas mientras otros se ajustan
  - Creas diálogos o formularios con elementos que no deben estirarse

### Consejos de Diseño

1. **Orden de creación**: Crea controles Dock en orden lógico (Top, luego Bottom, luego Left, Right, Fill)
2. **Evita conflictos**: No uses Dock y Anchor en el mismo control
3. **Prueba redimensionamiento**: Siempre prueba cómo se comporta la interfaz al redimensionar
4. **Usa paneles contenedores**: Agrupa controles relacionados en Paneles para layouts más complejos
5. **Considera MinimumSize**: Establece tamaños mínimos para evitar que los controles se hagan demasiado pequeños

### Rendimiento

- Dock y Anchor se actualizan automáticamente en eventos de redimensionamiento
- Para interfaces complejas, considera usar Paneles anidados para reducir cálculos
- Evita crear demasiados controles con Anchor en contenedores muy dinámicos

## Notas Técnicas

### Implementación Interna

`winformpy` implementa Dock y Anchor mediante:

- **Eventos Tkinter**: Vincula `<Configure>` para detectar cambios de tamaño
- **Cálculos de geometría**: Mantiene distancias relativas y absolutas
- **Layout automático**: Reorganiza controles cuando cambian las propiedades
- **Jerarquía de contenedores**: Respeta la estructura padre-hijo de controles

### Limitaciones vs Windows Forms

- **Subpixel positioning**: Tkinter puede tener ligeras diferencias en posicionamiento
- **Complex layouts**: Para layouts muy complejos, considera usar `TableLayoutPanel` o `FlowLayoutPanel`
- **Animation**: Los cambios son inmediatos

### Compatibilidad

- ✅ Funciona con todos los controles de `winformpy`
- ✅ Compatible con `AutoSize` y otras propiedades de layout
- ✅ Respeta `Margin` y `Padding`

### Depuración

Para depurar problemas de layout:

```python
# Ver propiedades actuales
print(f"Dock: {control.Dock}")
print(f"Anchor: {control.Anchor}")
print(f"Size: {control.Size}")
print(f"Location: {control.Location}")

# Forzar actualización manual
control.Invalidate()
control.Refresh()
```

---

**Autor**: Vibe coding by DatamanEdge
**Versión**: 1.0.4
**Licencia**: MIT
