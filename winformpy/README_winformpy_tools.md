# WinFormPy Tools

Este módulo proporciona utilidades para trabajar con Windows Forms en Python, facilitando la creación de interfaces gráficas nativas.

## LayoutManager

La clase `LayoutManager` es una herramienta potente para organizar controles automáticamente dentro de un contenedor (como un `Panel`). Sustituye al antiguo `AutoLayoutManager` con capacidades mejoradas.

### Características

*   **Distribución Automática**: Organiza los controles vertical u horizontalmente.
*   **Alineación**: Permite alinear los controles dentro del flujo (Izquierda/Derecha/Arriba/Abajo).
*   **Posición de Partida**: Configurable (TopLeft, TopRight, BottomLeft, BottomRight).
*   **Márgenes y Padding**: Control preciso del espaciado.
*   **Ignora Controles Fijos**: Respeta controles que ya tienen `Dock` o `Anchor` configurados.

### Enumerados

La clase cuenta con los siguientes enumerados para configuración:

*   **StartPosition**: `TopLeft` (default), `TopRight`, `BottomRight`, `BottomLeft`.
*   **Distribution**:
    *   Vertical: `UpDown` (default), `DownUp`.
    *   Horizontal: `LeftRight`, `RightLeft`.
*   **Alignment**:
    *   Vertical: `Up` (default), `Down`.
    *   Horizontal: `Left` (default), `Right`.
*   **LayoutType**: `FlowLayout` (default), `Autosize`, `Dock`, `Anchor`, `TableLayout`.

### Uso Básico

#### Layout Vertical (Por defecto)

```python
from winformpy_tools import LayoutManager

panel = Panel(form, {'AutoSize': True})
layout = LayoutManager(panel, margin=10, padding=20)

# Los controles se añaden de arriba a abajo
layout.add_control(label1)
layout.add_control(textbox1)
layout.add_control(button1)
```

#### Layout Horizontal

```python
from winformpy_tools import LayoutManager

row_panel = Panel(form, {'AutoSize': True})
layout = LayoutManager(row_panel, margin=5)

# Configurar para distribución horizontal (Izquierda a Derecha)
layout.distribution = LayoutManager.Distribution.LeftRight

# Los controles se añaden de izquierda a derecha
layout.add_control(label_nombre)
layout.add_control(textbox_nombre)
```

### Propiedades

*   `Padding`: Espacio interno desde los bordes del contenedor.
*   `Margin`: Espacio entre controles consecutivos.
*   `start_position`: Punto de inicio del layout.
*   `distribution`: Dirección del flujo principal.
*   `alignment`: Alineación de los controles en el eje secundario.

## Otras Utilidades

*   **FontManager**: Gestión de fuentes del sistema.
*   **ColorManager**: Gestión de colores del sistema Windows.
*   **CSSManager**: Utilidades para aplicar estilos CSS a controles (experimental).
