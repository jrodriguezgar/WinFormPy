# StatusBar - Control de Barra de Estado

## Descripción

`StatusBar` es un control de interfaz de usuario de Windows Forms que se utiliza para mostrar información de estado en un área, usualmente ubicada en la parte inferior de una ventana.

## Características

El control `StatusBar` puede funcionar de dos maneras principales:
1. **Modo Simple**: Mostrando un solo mensaje de texto
2. **Modo Paneles**: Dividiéndose en múltiples paneles (`StatusBarPanel`) para mostrar diferentes tipos de información

## Clases

### `StatusBar`

Control principal de barra de estado.

#### Constructor

```python
StatusBar(
    master_form,
    Text="Ready",
    Left=0, Top=570,
    Width=800, Height=25,
    ShowPanels=False,
    SizingGrip=True,
    BorderStyle="Fixed3D",
    Name=""
)
```

#### Propiedades

| Propiedad | Tipo | Descripción |
|-----------|------|-------------|
| `Text` | str | Texto que se muestra cuando `ShowPanels` es `False` |
| `ShowPanels` | bool | Si `True`, muestra los paneles; si `False`, solo muestra `Text` |
| `Panels` | list | Colección de objetos `StatusBarPanel` |
| `SizingGrip` | bool | Si `True`, muestra un controlador en la esquina inferior derecha |
| `BorderStyle` | str | Estilo del borde: `'None'`, `'Fixed3D'`, `'FixedSingle'` |
| `BackColor` | str | Color de fondo de la barra |
| `ForeColor` | str | Color del texto |
| `Font` | tuple | Fuente del texto: `(nombre, tamaño[, estilo])` |
| `Width` | int | Ancho del control |
| `Height` | int | Alto del control (típicamente 25px) |

#### Métodos

##### `AddPanel(panel)`
Añade un panel a la colección de paneles.

```python
panel = StatusBarPanel(Text="Estado: Listo")
statusbar.AddPanel(panel)
```

##### `RemovePanel(panel)`
Elimina un panel de la colección.

```python
statusbar.RemovePanel(panel)
```

##### `Dock(side='bottom')`
Ancla el StatusBar a un lado del formulario.

```python
statusbar.Dock('bottom')  # Valores: 'bottom', 'top', 'left', 'right'
```

#### Eventos

##### `PanelClick`
Se dispara cuando el usuario hace clic en cualquiera de los paneles.

```python
def on_panel_click(sender, panel):
    print(f"Panel clickeado: {panel.Text}")

statusbar.PanelClick = on_panel_click
```

##### `DrawItem`
Se dispara cuando un panel necesita ser dibujado (para paneles con `Style='OwnerDraw'`).

```python
def on_draw_item(sender, e):
    # Dibujo personalizado
    pass

statusbar.DrawItem = on_draw_item
```

---

### `StatusBarPanel`

Representa un panel individual dentro de un `StatusBar`.

#### Constructor

```python
StatusBarPanel(
    Text="",
    Width=100,
    AutoSize="None",
    Icon=None,
    ToolTipText="",
    Bevel="Sunken",
    Style="Text"
)
```

#### Propiedades

| Propiedad | Tipo | Descripción |
|-----------|------|-------------|
| `Text` | str | Texto que se muestra dentro del panel |
| `Width` | int | Ancho del panel en píxeles |
| `AutoSize` | str | Modo de redimensionamiento: `'None'`, `'Spring'`, `'Contents'` |
| `Icon` | Image | Imagen o icono que se muestra junto al texto |
| `ToolTipText` | str | Texto del tooltip que aparece al pasar el ratón |
| `Bevel` | str | Estilo del borde: `'Raised'`, `'Sunken'`, `'None'` |
| `Style` | str | Estilo del panel: `'Text'`, `'OwnerDraw'` |
| `MinWidth` | int | Ancho mínimo del panel |
| `Alignment` | str | Alineación del texto: `'Left'`, `'Center'`, `'Right'` |

#### Modos de AutoSize

- **`'None'`**: Ancho fijo especificado por la propiedad `Width`
- **`'Spring'`**: El panel se expande para llenar el espacio disponible
- **`'Contents'`**: El panel se ajusta automáticamente al contenido

#### Eventos

##### `Click`
Se dispara cuando se hace clic en el panel.

```python
panel.Click = lambda: print("Panel clickeado!")
```

##### `DoubleClick`
Se dispara cuando se hace doble clic en el panel.

```python
panel.DoubleClick = lambda: print("Doble clic en panel!")
```

## Ejemplos de Uso

### Ejemplo 1: StatusBar Simple

```python
from winform_py import Form, StatusBar

class MyForm(Form):
    def __init__(self):
        super().__init__(Title="Mi Aplicación", Width=800, Height=600)
        
        # Crear StatusBar simple
        self.status = StatusBar(
            self,
            Text="Listo",
            ShowPanels=False,
            SizingGrip=True
        )
        self.AddControl(self.status)
        self.status.Dock('bottom')
        
        # Cambiar el texto
        self.status.Text = "Procesando..."
```

### Ejemplo 2: StatusBar con Múltiples Paneles

```python
from winform_py import Form, StatusBar, StatusBarPanel
import datetime

class MyForm(Form):
    def __init__(self):
        super().__init__(Title="Mi Aplicación", Width=800, Height=600)
        
        # Crear StatusBar con paneles
        self.status = StatusBar(
            self,
            ShowPanels=True,
            SizingGrip=True
        )
        self.AddControl(self.status)
        
        # Panel 1: Mensaje principal (se expande)
        panel_msg = StatusBarPanel(
            Text="Listo",
            AutoSize="Spring",
            Alignment="Left"
        )
        self.status.AddPanel(panel_msg)
        
        # Panel 2: Contador
        panel_counter = StatusBarPanel(
            Text="Elementos: 0",
            Width=120,
            AutoSize="None",
            Alignment="Center"
        )
        self.status.AddPanel(panel_counter)
        
        # Panel 3: Hora
        panel_time = StatusBarPanel(
            Text=datetime.datetime.now().strftime("%H:%M:%S"),
            Width=100,
            AutoSize="None",
            Alignment="Center"
        )
        self.status.AddPanel(panel_time)
        
        # Panel 4: Usuario
        panel_user = StatusBarPanel(
            Text="Usuario: Admin",
            Width=150,
            AutoSize="None"
        )
        self.status.AddPanel(panel_user)
        
        # Anclar al fondo
        self.status.Dock('bottom')
```

### Ejemplo 3: Manejo de Eventos

```python
from winform_py import Form, StatusBar, StatusBarPanel, MessageBox

class MyForm(Form):
    def __init__(self):
        super().__init__(Title="Eventos de StatusBar", Width=800, Height=600)
        
        self.status = StatusBar(self, ShowPanels=True)
        self.AddControl(self.status)
        
        # Crear paneles
        panel1 = StatusBarPanel(
            Text="Panel 1",
            Width=200,
            ToolTipText="Haz clic para ver información"
        )
        panel2 = StatusBarPanel(
            Text="Panel 2",
            Width=200,
            ToolTipText="Contador de clics"
        )
        
        self.click_count = 0
        
        # Evento individual del panel
        panel1.Click = lambda: MessageBox.Show("¡Clic en Panel 1!")
        panel2.Click = self.on_panel2_click
        
        self.status.AddPanel(panel1)
        self.status.AddPanel(panel2)
        
        # Evento general del StatusBar
        self.status.PanelClick = self.on_any_panel_click
        
        self.status.Dock('bottom')
    
    def on_panel2_click(self):
        self.click_count += 1
        panel = self.status.Panels[1]
        panel.Text = f"Clics: {self.click_count}"
    
    def on_any_panel_click(self, sender, panel):
        index = sender.Panels.index(panel)
        print(f"Panel {index} clickeado: {panel.Text}")
```

### Ejemplo 4: Actualización Dinámica

```python
import threading
import time
from datetime import datetime

class MyForm(Form):
    def __init__(self):
        super().__init__(Title="StatusBar Dinámico", Width=800, Height=600)
        
        self.status = StatusBar(self, ShowPanels=True)
        self.AddControl(self.status)
        
        # Panel de hora que se actualiza automáticamente
        self.time_panel = StatusBarPanel(
            Text=datetime.now().strftime("%H:%M:%S"),
            Width=100
        )
        self.status.AddPanel(self.time_panel)
        
        self.status.Dock('bottom')
        
        # Iniciar actualización de hora
        self.start_time_update()
    
    def start_time_update(self):
        def update_time():
            while True:
                time.sleep(1)
                current_time = datetime.now().strftime("%H:%M:%S")
                self._root.after(0, lambda: setattr(self.time_panel, 'Text', current_time))
        
        thread = threading.Thread(target=update_time, daemon=True)
        thread.start()
```

## Patrones Comunes de Uso

### 1. Barra de Estado de Aplicación

```python
# Panel principal con estado general
panel_status = StatusBarPanel(Text="Listo", AutoSize="Spring")

# Panel con progreso
panel_progress = StatusBarPanel(Text="0%", Width=80)

# Panel con información del documento
panel_doc = StatusBarPanel(Text="Sin documento", Width=150)

# Panel con posición del cursor (editor de texto)
panel_pos = StatusBarPanel(Text="Ln 1, Col 1", Width=100)
```

### 2. Barra de Estado de Conexión

```python
# Estado de conexión
panel_conn = StatusBarPanel(Text="● Conectado", AutoSize="Spring")

# Servidor
panel_server = StatusBarPanel(Text="Servidor: localhost", Width=180)

# Usuario
panel_user = StatusBarPanel(Text="Usuario: admin", Width=150)
```

### 3. Barra de Estado de Progreso

```python
# Mensaje de operación
panel_operation = StatusBarPanel(Text="Copiando archivos...", AutoSize="Spring")

# Progreso (se actualiza dinámicamente)
panel_progress = StatusBarPanel(Text="50/100 (50%)", Width=120)

# Tiempo transcurrido
panel_time = StatusBarPanel(Text="Tiempo: 00:05", Width=100)
```

## Mejores Prácticas

1. **Anclaje**: Siempre usar `Dock('bottom')` para anclar el StatusBar al fondo del formulario
2. **Altura**: Mantener una altura estándar de 25px para consistencia visual
3. **Paneles Spring**: Usar al menos un panel con `AutoSize='Spring'` para mensajes largos
4. **Tooltips**: Añadir `ToolTipText` a paneles que puedan mostrar texto truncado
5. **Actualización**: Evitar actualizaciones muy frecuentes que puedan afectar el rendimiento
6. **SizingGrip**: Mantener `SizingGrip=True` para indicar que la ventana es redimensionable

## Notas de Implementación

- El control está implementado usando `tk.Frame` como contenedor base
- Los paneles individuales usan `tk.Label` para mostrar texto
- El SizingGrip se dibuja usando `tk.Canvas` con líneas diagonales
- Los tooltips se implementan usando `tk.Toplevel` temporal
- El método `Dock()` usa `pack()` de tkinter para anclaje

## Archivo de Ejemplo

Ejecuta el archivo de ejemplo completo:

```bash
python examples/statusbar_example.py
```

Este ejemplo demuestra todas las características del control StatusBar incluyendo:
- StatusBar simple con texto
- StatusBar con múltiples paneles
- Diferentes modos de AutoSize
- Manejo de eventos PanelClick
- Actualización dinámica de paneles
- Tooltips y alineación de texto
