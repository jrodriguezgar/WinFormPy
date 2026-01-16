# MAUI Style in WinFormPy

This guide explains how to use the `mauipy` module to create cross-platform applications with a MAUI (Multi-platform App UI) style using WinFormPy.

## Índice de Controles

| # | Control | Categoría | Descripción |
|---|---------|-----------|-------------|
| 1 | [Shell](#shell) | Core | Contenedor principal de la aplicación |
| 2 | [ContentPage](#pages) | Pages | Página base con área de contenido scrollable |
| 3 | [NavigationPage](#pages) | Pages | Pila de páginas con navegación hacia atrás |
| 4 | [TabbedPage](#pages) | Pages | Página con navegación por pestañas |
| 5 | [VerticalStackLayout](#layouts) | Layouts | Organiza hijos verticalmente |
| 6 | [HorizontalStackLayout](#layouts) | Layouts | Organiza hijos horizontalmente |
| 7 | [Grid](#layouts) | Layouts | Organiza hijos en filas y columnas |
| 8 | [Label](#basic-controls) | Basic | Control de texto |
| 9 | [Button](#basic-controls) | Basic | Botón clickeable |
| 10 | [Entry](#basic-controls) | Basic | Entrada de texto de una línea |
| 11 | [Editor](#basic-controls) | Basic | Entrada de texto multilínea |
| 12 | [Image](#basic-controls) | Basic | Visualización de imágenes |
| 13 | [CheckBox](#selection-controls) | Selection | Toggle booleano con etiqueta |
| 14 | [Switch](#selection-controls) | Selection | Control de interruptor |
| 15 | [RadioButton](#selection-controls) | Selection | Opción de selección única |
| 16 | [RadioButtonGroup](#selection-controls) | Selection | Gestiona selección exclusiva de radio |
| 17 | [Picker](#selection-controls) | Selection | Dropdown/ComboBox |
| 18 | [Slider](#selection-controls) | Selection | Selector de valor en rango |
| 19 | [Stepper](#selection-controls) | Selection | Incremento/decremento numérico |
| 20 | [DatePicker](#date--time) | Date & Time | Selección de fecha con calendario |
| 21 | [TimePicker](#date--time) | Date & Time | Selección de hora |
| 22 | [ActivityIndicator](#progress--activity) | Progress | Indicador de carga giratorio |
| 23 | [ProgressBar](#progress--activity) | Progress | Barra de progreso horizontal |
| 24 | [Frame](#containers--layout) | Containers | Contenedor con borde |
| 25 | [Card](#containers--layout) | Containers | Tarjeta Material Design |
| 26 | [Expander](#containers--layout) | Containers | Panel de contenido colapsable |
| 27 | [FlyoutMenu](#navigation--menus) | Navigation | Menú flyout independiente |
| 28 | [Toolbar](#navigation--menus) | Navigation | Barra de herramientas horizontal |
| 29 | [BottomNavigationBar](#navigation--menus) | Navigation | Pestañas de navegación inferior |
| 30 | [CarouselView](#navigation--menus) | Navigation | Carrusel de elementos deslizable |
| 31 | [IndicatorView](#navigation--menus) | Navigation | Puntos indicadores de página |
| 32 | [ToastNotification](#popups--overlays) | Popups | Mensajes emergentes breves |
| 33 | [PopUpFlyout](#popups--overlays) | Popups | Diálogo popup modal |
| 34 | [BottomSheet](#popups--overlays) | Popups | Panel modal deslizante |
| 35 | [SearchBar](#specialized-controls) | Specialized | Entrada de búsqueda con botón |
| 36 | [ChipTag](#specialized-controls) | Specialized | Elemento tag/chip compacto |
| 37 | [Badge](#specialized-controls) | Specialized | Insignia de notificación |
| 38 | [Avatar](#specialized-controls) | Specialized | Imagen/iniciales de perfil circular |
| 39 | [FloatingActionButton](#specialized-controls) | Specialized | FAB Material Design |
| 40 | [CollectionView](#data-display) | Data Display | Vista de lista/cuadrícula con plantilla |
| 41 | [RefreshView](#data-display) | Data Display | Contenedor pull-to-refresh |

---

## Core Concepts

### Shell
The `Shell` is the main container for your application. It provides a standard navigation structure with a Flyout menu and a content area.

```python
from winformpy.mauipy import Shell, ContentPage, Label

class HomePage(ContentPage):
    def __init__(self, master):
        super().__init__(master)
        self.Title = "Home"
        Label(self, text="Welcome!", font=("Segoe UI", 24, "bold"))

class MyApp(Shell):
    def __init__(self):
        super().__init__()
        self.Text = "My App"
        self.HeaderColor = "#512BD4"
        
        # Add items to the Flyout Menu
        self.AddMenuItem("Home", lambda: self.NavigateTo(HomePage), icon="🏠")
        self.AddMenuItem("Settings", lambda: self.NavigateTo(SettingsPage), icon="⚙️")
        
        # Navigate to initial page
        self.NavigateTo(HomePage)

if __name__ == "__main__":
    app = MyApp()
    app.Run()
```

## Pages

| Page | Description |
|------|-------------|
| **ContentPage** | Base page with scrollable content area |
| **NavigationPage** | Page stack with back navigation support |
| **TabbedPage** | Page with tab-based navigation |

## Layouts

| Layout | Description |
|--------|-------------|
| **VerticalStackLayout** | Arranges children vertically with spacing |
| **HorizontalStackLayout** | Arranges children horizontally with spacing |
| **Grid** | Arranges children in rows and columns |

## Controls

### Basic Controls

| Control | Description | Key Properties/Events |
|---------|-------------|----------------------|
| **Label** | Text display control | `Text`, `Font`, `ForeColor` |
| **Button** | Clickable button | `Text`, `Click` |
| **Entry** | Single-line text input | `Text`, `Placeholder`, `TextChanged` |
| **Editor** | Multi-line text input | `Text`, `Placeholder`, `TextChanged` |
| **Image** | Image display | `Source`, `Click` |

### Selection Controls

| Control | Description | Key Properties/Events |
|---------|-------------|----------------------|
| **CheckBox** | Boolean toggle with label | `IsChecked`, `Text`, `CheckedChanged` |
| **Switch** | Toggle switch control | `IsToggled`, `OnColor`, `Toggled` |
| **RadioButton** | Single selection option | `IsChecked`, `Value`, `CheckedChanged` |
| **RadioButtonGroup** | Manages exclusive radio selection | `SelectedValue`, `SelectionChanged` |
| **Picker** | Dropdown/ComboBox selection | `Items`, `SelectedIndex`, `SelectedIndexChanged` |
| **Slider** | Range value selector | `Value`, `Minimum`, `Maximum`, `ValueChanged` |
| **Stepper** | Numeric increment/decrement | `Value`, `Minimum`, `Maximum`, `ValueChanged` |

### Date & Time

| Control | Description | Key Properties/Events |
|---------|-------------|----------------------|
| **DatePicker** | Calendar date selection | `Date`, `MinimumDate`, `MaximumDate`, `DateSelected` |
| **TimePicker** | Time selection with spinboxes | `Time`, `Hour`, `Minute`, `Second`, `TimeSelected` |

### Progress & Activity

| Control | Description | Key Properties/Events |
|---------|-------------|----------------------|
| **ActivityIndicator** | Spinning loading indicator | `IsRunning`, `Color`, `Start()`, `Stop()` |
| **ProgressBar** | Horizontal progress display | `Progress`, `IsIndeterminate`, `ProgressColor` |

### Containers & Layout

| Control | Description | Key Properties/Events |
|---------|-------------|----------------------|
| **Frame** | Bordered container | `Content`, `BorderColor`, `BackgroundColor` |
| **Card** | Material Design elevated card | `Content`, `Title`, `Subtitle` |
| **Expander** | Collapsible content panel | `Content`, `Header`, `IsExpanded`, `ExpandedChanged` |

### Navigation & Menus

| Control | Description | Key Properties/Events |
|---------|-------------|----------------------|
| **FlyoutMenu** | Standalone flyout menu | `AddItem()`, `AddSeparator()` |
| **Toolbar** | Horizontal action toolbar | `AddItem()`, `AddSeparator()`, `AddSpacer()` |
| **BottomNavigationBar** | Bottom navigation tabs | `AddItem()`, `SelectedIndex`, `SelectedIndexChanged` |
| **CarouselView** | Swipeable item carousel | `SetItems()`, `PositionChanged` |
| **IndicatorView** | Page indicator dots | `Count`, `Position`, `PositionChanged` |

### Popups & Overlays

| Control | Description | Key Properties/Events |
|---------|-------------|----------------------|
| **ToastNotification** | Brief popup messages | `Show(master, message, duration)` |
| **PopUpFlyout** | Modal popup dialog | `Content`, `Show()`, `Hide()` |
| **BottomSheet** | Slide-up modal panel | `Content`, `Title`, `Open()`, `Close()`, `StateChanged` |

### Specialized Controls

| Control | Description | Key Properties/Events |
|---------|-------------|----------------------|
| **SearchBar** | Search input with button | `Text`, `Placeholder`, `SearchCommand` |
| **ChipTag** | Compact tag/chip element | `Text`, `CloseCommand` |
| **Badge** | Notification badge overlay | `Text`, `BackgroundColor` |
| **Avatar** | Circular profile image/initials | `Text`, `BackgroundColor`, `Size` |
| **FloatingActionButton** | Material Design FAB | `Icon`, `Clicked`, `IsVisible` |

### Data Display

| Control | Description | Key Properties/Events |
|---------|-------------|----------------------|
| **CollectionView** | Templated list/grid view | `ItemsSource`, `SelectedItem`, `SelectionChanged`, `ItemTapped` |
| **RefreshView** | Pull-to-refresh container | `Content`, `IsRefreshing`, `Refreshing` |

## Events

MAUIPy controls use the same event pattern as the core library. All event handlers receive `(sender, e)`:

```python
def on_btn_clicked(sender, e):
    print(f"Clicked {sender.Text}")

btn = Button(self, text="Click Me")
btn.Click = on_btn_clicked
```

## Example Usage

### Basic Controls

```python
from winformpy.mauipy import (
    Shell, ContentPage, VerticalStackLayout,
    Label, Button, Entry, Switch, Slider
)

class DemoPage(ContentPage):
    def __init__(self, master):
        super().__init__(master)
        self.Title = "Demo"
        
        layout = VerticalStackLayout(self, props={'Spacing': 15, 'Padding': (20, 20, 20, 20)})
        
        # Label
        layout.AddChild(Label, text="Welcome!", font=("Segoe UI", 20, "bold"))
        
        # Entry with placeholder
        self.name_entry = layout.AddChild(Entry, placeholder="Enter your name")
        
        # Button with click handler
        btn = layout.AddChild(Button, text="Submit")
        btn.Click = self.on_submit
        
        # Switch
        switch = Switch(self)
        switch.Toggled = lambda is_on: print(f"Switch is {'on' if is_on else 'off'}")
        
        # Slider
        slider = Slider(self, minimum=0, maximum=100, value=50)
        slider.ValueChanged = lambda v: print(f"Value: {v}")
    
    def on_submit(self):
        print(f"Name: {self.name_entry.Text}")
```

### Selection Controls

```python
from winformpy.mauipy import CheckBox, RadioButton, RadioButtonGroup, Picker

# CheckBox
agree = CheckBox(page, text="I agree to the terms")
agree.CheckedChanged = lambda checked: enable_submit(checked)

# RadioButtonGroup
group = RadioButtonGroup()
group.SelectionChanged = lambda val: print(f"Selected: {val}")

RadioButton(page, text="Small", value="S", group=group)
RadioButton(page, text="Medium", value="M", group=group)
RadioButton(page, text="Large", value="L", group=group)

# Picker (Dropdown)
colors = Picker(page, items=['Red', 'Green', 'Blue'], title='Choose color')
colors.SelectedIndexChanged = lambda idx: apply_color(colors.SelectedItem)
```

### Date and Time

```python
from winformpy.mauipy import DatePicker, TimePicker
from datetime import date, time

# DatePicker
birth_date = DatePicker(page)
birth_date.MaximumDate = date.today()
birth_date.DateSelected = lambda d: print(f"Selected: {d}")

# TimePicker
alarm = TimePicker(page)
alarm.Time = time(7, 30, 0)
alarm.TimeSelected = lambda t: set_alarm(t)
```

### Cards and Expanders

```python
from winformpy.mauipy import Card, Expander, Label, Button

# Card with shadow
card = Card(page, title="User Profile", subtitle="Account settings")
Button(card.Content, text="Edit Profile")

# Expander
details = Expander(page, header="Advanced Options", is_expanded=False)
CheckBox(details.Content, text="Enable logging")
details.ExpandedChanged = lambda expanded: print(f"Expanded: {expanded}")
```

### Collection View

```python
from winformpy.mauipy import CollectionView, Label

def render_item(parent, item):
    Label(parent, text=item['name'], font=("Segoe UI", 12))

data = [{'name': 'Item 1'}, {'name': 'Item 2'}, {'name': 'Item 3'}]

collection = CollectionView(page, items=data, item_template=render_item)
collection.SelectionChanged = lambda indices: print(f"Selected: {indices}")
collection.ItemTapped = lambda idx, item: show_detail(item)
```

### Bottom Sheet

```python
from winformpy.mauipy import BottomSheet, Button, Label

sheet = BottomSheet(app, title="Share via")
Button(sheet.Content, text="Email")
Button(sheet.Content, text="Message")
sheet.StateChanged = lambda is_open: print(f"Sheet {'opened' if is_open else 'closed'}")

# Open the sheet
sheet.Open()
```

### Floating Action Button

```python
from winformpy.mauipy import FloatingActionButton

fab = FloatingActionButton(page, icon="➕")
fab.Clicked = lambda: open_create_dialog()
```

## See Also

- `examples/maui_example.py` - Complete working example
- `winformpy/mauipy.py` - Full source with detailed docstrings
