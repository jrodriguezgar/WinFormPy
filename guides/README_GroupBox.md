# GroupBox - Control Contenedor de Windows Forms

## Descripción

El `GroupBox` es un control contenedor de Windows Forms implementado en winform-py que se utiliza para agrupar visual y lógicamente otros controles relacionados en la interfaz de usuario.

Proporciona un borde rectangular con un título opcional para delimitar visualmente una sección, mejorando la organización y usabilidad del formulario.

## Características Principales

### Herencia

`GroupBox` hereda de `ControlBase` y actúa como un contenedor para agrupar controles relacionados.

### Representación Visual

- Marco rectangular con borde estilo `groove` (3D)
- Área en la parte superior izquierda para el título (propiedad `Text`)
- Padding interno configurable para espaciar los controles hijos
- Color de fondo y fuente personalizables

## Propiedades

### Propiedades Visuales

| Propiedad     | Tipo      | Descripción                                              | Valor por Defecto    |
| ------------- | --------- | --------------------------------------------------------- | -------------------- |
| `Text`      | str       | Texto del título mostrado en la parte superior del marco | `'GroupBox'`       |
| `Width`     | int       | Ancho del control en píxeles                             | `200`              |
| `Height`    | int       | Alto del control en píxeles                              | `100`              |
| `Left`      | int       | Posición X relativa al contenedor padre                  | `0`                |
| `Top`       | int       | Posición Y relativa al contenedor padre                  | `0`                |
| `BackColor` | str       | Color de fondo del área dentro del marco                 | `None` (sistema)   |
| `ForeColor` | str       | Color del texto del título                               | `None` (sistema)   |
| `Font`      | str/tuple | Fuente utilizada para el texto del título                | `None` (sistema)   |
| `Padding`   | tuple     | Espaciado interno (left, top, right, bottom)              | `(10, 20, 10, 10)` |

### Propiedades de Estado

| Propiedad   | Tipo | Descripción                                                            | Valor por Defecto |
| ----------- | ---- | ----------------------------------------------------------------------- | ----------------- |
| `Enabled` | bool | Determina si el GroupBox y todos sus controles hijos están habilitados | `True`          |
| `Visible` | bool | Determina si el GroupBox y todos sus controles hijos son visibles       | `True`          |
| `Name`    | str  | Nombre del control para identificación                                 | `''`            |

### Propiedades de Navegación

| Propiedad    | Tipo | Descripción                                               | Valor por Defecto |
| ------------ | ---- | ---------------------------------------------------------- | ----------------- |
| `TabStop`  | bool | Determina si el control puede recibir el foco mediante Tab | `False`         |
| `TabIndex` | int  | Orden de tabulación del control                           | `0`             |

### Colección de Controles

| Propiedad    | Tipo | Descripción                                                           |
| ------------ | ---- | ---------------------------------------------------------------------- |
| `Controls` | list | Lista que contiene todos los controles secundarios dentro del GroupBox |

## Eventos

### Eventos de Contenedor

| Evento             | Parámetros | Descripción                                                               |
| ------------------ | ----------- | -------------------------------------------------------------------------- |
| `ControlAdded`   | `control` | Ocurre cuando se añade dinámicamente un control a la colección Controls |
| `ControlRemoved` | `control` | Ocurre cuando se elimina un control de la colección Controls              |

### Eventos de Interacción

| Evento    | Parámetros | Descripción                                                        |
| --------- | ----------- | ------------------------------------------------------------------- |
| `Enter` | -           | Ocurre cuando el usuario entra en el GroupBox (navegación con Tab) |
| `Leave` | -           | Ocurre cuando el usuario sale del área del GroupBox                |
| `Click` | -           | Ocurre cuando el usuario hace clic en el área del contenedor       |

### Eventos de Renderizado

| Evento    | Parámetros | Descripción                                |
| --------- | ----------- | ------------------------------------------- |
| `Paint` | -           | Ocurre cuando el control necesita dibujarse |

## Métodos

### Gestión de Controles

#### `AddControl(control)`

Añade un control al GroupBox con posiciones relativas.

**Comportamiento:**

- El control se añade al GroupBox (se convierte en su padre)
- El control solo será visible si su propia propiedad `Visible` es `True` Y el GroupBox también está visible
- Los controles heredan el estado `Enabled` del GroupBox

```python
group = GroupBox(form, {'Text': 'Opciones'})
check = CheckBox(form, {'Text': 'Opción 1', 'Left': 20, 'Top': 10})
group.AddControl(check)
```

#### `RemoveControl(control)`

Elimina un control del GroupBox.

```python
group.RemoveControl(check)
```

### Métodos de Renderizado (heredados de ControlBase)

#### `Invalidate()`

Marca el control como no válido y solicita repintado (se agrega a la cola de mensajes).

#### `Refresh()`

Fuerza un repintado inmediato (equivalente a `Invalidate()` + `Update()`).

## Ejemplos de Uso

### Ejemplo 1: Uso Básico

```python
from winformpy import Form, GroupBox, CheckBox

# Crear formulario
form = Form({'Text': 'Ejemplo GroupBox', 'Width': 400, 'Height': 300})

# Crear GroupBox
group = GroupBox(form, {
    'Text': 'Opciones',
    'Left': 20,
    'Top': 20,
    'Width': 350,
    'Height': 150
})
form.AddControl(group)

# Añadir controles al grupo
check1 = CheckBox(form, {'Text': 'Opción 1', 'Left': 20, 'Top': 20})
group.AddControl(check1)

check2 = CheckBox(form, {'Text': 'Opción 2', 'Left': 20, 'Top': 60})
group.AddControl(check2)

form.Show()
```

### Ejemplo 2: RadioButtons Mutuamente Exclusivos

```python
# GroupBox para agrupar RadioButtons (comportamiento exclusivo)
group_gender = GroupBox(form, {
    'Text': 'Género',
    'Left': 20,
    'Top': 20,
    'Width': 240,
    'Height': 120
})
form.AddControl(group_gender)

# Los RadioButtons dentro del mismo grupo son mutuamente exclusivos
radio_male = RadioButton(form, {'Text': 'Masculino', 'Left': 20, 'Top': 10})
group_gender.AddControl(radio_male)

radio_female = RadioButton(form, {'Text': 'Femenino', 'Left': 20, 'Top': 40})
group_gender.AddControl(radio_female)
```

### Ejemplo 3: Control de Visibilidad y Estado

```python
# Crear grupo con controles
group = GroupBox(form, {'Text': 'Configuración', 'Left': 20, 'Top': 20})
form.AddControl(group)

# Botón para deshabilitar el grupo completo
btn_toggle = Button(form, {'Text': 'Deshabilitar Grupo', 'Left': 20, 'Top': 200})
form.AddControl(btn_toggle)

def toggle_enabled():
    group.Enabled = not group.Enabled
    btn_toggle.Text = 'Habilitar Grupo' if not group.Enabled else 'Deshabilitar Grupo'

btn_toggle.Click = toggle_enabled
```

### Ejemplo 4: Personalización Visual

```python
# GroupBox con estilo personalizado
group = GroupBox(form, {
    'Text': 'Información Personal',
    'Left': 20,
    'Top': 20,
    'Width': 500,
    'Height': 180,
    'BackColor': '#f0f0f0',  # Fondo gris claro
    'ForeColor': '#003366',   # Título azul oscuro
    'Font': ('Arial', 10, 'bold'),
    'Padding': (15, 25, 15, 15)  # Mayor espaciado
})
form.AddControl(group)
```

### Ejemplo 5: Eventos del GroupBox

```python
def on_control_added(control):
    print(f"Control añadido: {control.Name}")

def on_control_removed(control):
    print(f"Control eliminado: {control.Name}")

def on_enter():
    print("Entrando en el GroupBox")

def on_leave():
    print("Saliendo del GroupBox")

group.ControlAdded = on_control_added
group.ControlRemoved = on_control_removed
group.Enter = on_enter
group.Leave = on_leave
```

## Jerarquía de Visibilidad

El GroupBox implementa la jerarquía de visibilidad de Windows Forms:

1. **Cuando el GroupBox se oculta (`Visible = False`):**

   - Automáticamente oculta todos sus controles hijos
   - No importa la propiedad `Visible` individual de cada control hijo
2. **Cuando el GroupBox se hace visible (`Visible = True`):**

   - Solo muestra los controles hijos cuya propiedad `Visible` individual sea `True`

```python
# Ocultar todo el grupo
group.Visible = False  # Todos los controles hijos se ocultan

# Mostrar el grupo
group.Visible = True   # Solo los controles con Visible=True se muestran
```

## Estado Enabled

De manera similar, cuando el GroupBox se deshabilita:

```python
# Deshabilitar todo el grupo
group.Enabled = False  # Todos los controles hijos se deshabilitan

# Habilitar el grupo
group.Enabled = True   # Todos los controles hijos se habilitan
```

## Casos de Uso Comunes

### 1. Agrupar RadioButtons

Los RadioButtons dentro del mismo GroupBox funcionan como un grupo exclusivo.

### 2. Secciones de Formularios

Organizar campos de entrada relacionados (nombre, dirección, etc.)

### 3. Opciones de Configuración

Agrupar checkboxes de preferencias o configuraciones relacionadas.

### 4. Deshabilitar Secciones Completas

Habilitar/deshabilitar grupos de controles según el contexto de la aplicación.

## Diferencias con Panel

| Característica | GroupBox                                   | Panel                               |
| --------------- | ------------------------------------------ | ----------------------------------- |
| Borde visual    | Siempre visible con título                | Configurable (puede no tener borde) |
| Título         | Sí, en la parte superior                  | Opcional (LabelFrame)               |
| Uso principal   | Agrupar controles relacionados visualmente | Contenedor general flexible         |
| AutoScroll      | No                                         | Sí (opcional)                      |
| Estilo típico  | Borde 3D (groove)                          | Varios estilos disponibles          |

## Notas Técnicas

- El GroupBox utiliza `tk.LabelFrame` de Tkinter como widget subyacente
- El padding predeterminado reserva espacio extra en la parte superior (20px) para el título
- No soporta `AutoScroll` (usar Panel si se necesita scroll)
- Los controles hijos usan posicionamiento relativo al GroupBox, no al formulario

## Ver También

- [Panel](README_Panel.md) - Contenedor general más flexible
- [CheckBox](README_CheckBox.md) - Control de casilla de verificación
- [RadioButton](README_RadioButton.md) - Botón de opción exclusiva
- [ControlBase](README_ControlBase.md) - Clase base de todos los controles
