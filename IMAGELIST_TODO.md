# ImageList - Implementación Completa TODO

## Estado Actual

### ✅ IMPLEMENTADO

#### Clase ImageList
- [x] Estructura básica de la clase
- [x] Constructor con diccionario de propiedades
- [x] ImageCollection interna con métodos Add, Remove, Clear
- [x] Propiedades: Name, ImageSize, ColorDepth, TransparentColor, Tag
- [x] Propiedades Handle y HandleCreated (simuladas)
- [x] Método GetImage(key) - acceso por índice o clave
- [x] Método Count() - número de imágenes
- [x] Método Draw() - básico para Canvas
- [x] Método Dispose() y ToString()
- [x] Eventos: CollectionChanged, Disposed, RecreateHandle
- [x] Acceso mediante `Images[0]` o `Images['key']`
- [x] Iteración sobre imágenes
- [x] len(Images) funcional

#### Integración con ListView
- [x] Propiedades SmallImageList y LargeImageList definidas
- [x] ListViewItem.ImageIndex y ImageKey propiedades

#### Integración con TreeView
- [x] TreeView.ImageList propiedad (necesita verificar)
- [x] TreeNode.ImageIndex y SelectedImageIndex propiedades

---

## ❌ PENDIENTE DE IMPLEMENTAR

### 1. Procesamiento de Imágenes

#### Alto Prioridad
- [ ] **Redimensionamiento automático a ImageSize**
  ```python
  def _add_image(self, image, key=None):
      # TODO: Resize image to self.ImageSize
      # Actualmente en línea 17900 dice:
      # "Without PIL, resizing is limited. We assume the user provides correct size"
  ```
  - Detectar si la imagen es PIL Image
  - Redimensionar usando PIL: `image.resize(self.ImageSize, Image.LANCZOS)`
  - Convertir a PhotoImage para tkinter

#### Medio Prioridad
- [ ] **Conversión automática PIL Image → PhotoImage**
  ```python
  from PIL import ImageTk
  
  if isinstance(image, Image.Image):  # PIL Image
      photo = ImageTk.PhotoImage(image)
      self._images[key] = photo
  ```

- [ ] **Soporte para TransparentColor**
  - Aplicar color transparente durante conversión
  - Usar alpha channel si ColorDepth >= 32

### 2. Integración con Controles

#### ListView - Renderizado de Íconos
**CRÍTICO**: Actualmente SmallImageList y LargeImageList están definidos pero NO se renderizan

- [ ] Modificar `ListView._render_items()` para usar ImageList
  ```python
  def _render_items(self):
      for item in self.Items:
          if item.ImageIndex >= 0 and self.SmallImageList:
              img = self.SmallImageList.GetImage(item.ImageIndex)
              # Renderizar imagen en el Treeview
          elif item.ImageKey and self.SmallImageList:
              img = self.SmallImageList.GetImage(item.ImageKey)
  ```

- [ ] Agregar columna de imagen en ttk.Treeview
- [ ] Configurar tags con imágenes

#### TreeView - Renderizado de Íconos
- [ ] Verificar si TreeView.ImageList está conectado
- [ ] Implementar renderizado de TreeNode.ImageIndex
- [ ] Implementar TreeNode.SelectedImageIndex (imagen al seleccionar)

#### TabControl
- [ ] Agregar propiedad `TabControl.ImageList`
- [ ] Agregar propiedad `TabPage.ImageIndex` y `ImageKey`
- [ ] Renderizar íconos en las pestañas

#### Button
- [ ] Agregar propiedades `Button.ImageList`
- [ ] Agregar propiedades `Button.ImageIndex` y `ImageKey`
- [ ] Renderizar imagen del ImageList en el botón

#### ToolStrip (si existe)
- [ ] Verificar si ToolStrip está implementado
- [ ] Agregar ImageList a ToolStrip
- [ ] ToolStripButton con ImageIndex/ImageKey

### 3. Métodos Avanzados de ImageList

#### Draw() - Sobrecargas
```python
# Actualmente solo básico
def Draw(self, graphics, x, y, index=None, width=None, height=None):
    pass

# Falta implementar:
def Draw(self, graphics, point, index):
    """Draw at Point location"""
    
def Draw(self, graphics, x, y, width, height, index):
    """Draw with specific size"""
```

#### Métodos de Windows Forms faltantes
- [ ] `ImageList.Draw(Graphics g, Point pt, int index)`
- [ ] `ImageList.Draw(Graphics g, int x, int y, int width, int height, int index)`
- [ ] `ImageList.Images.SetKeyName(int index, string name)` 
- [ ] `ImageList.Images.ContainsKey(string key)`
- [ ] `ImageList.Images.IndexOfKey(string key)`

### 4. Propiedades Funcionales

#### ColorDepth
Actualmente es solo un valor almacenado. Implementar:
- [ ] Validar valores permitidos (4, 8, 16, 24, 32 bits)
- [ ] Aplicar conversión de profundidad de color al agregar imágenes

#### ImageStream
- [ ] Implementar serialización básica
- [ ] Guardar/cargar ImageList a/desde stream

### 5. Testing y Ejemplos

- [x] Ejemplo básico de ImageList (imagelist_example.py)
- [ ] Ejemplo de ListView con íconos reales
- [ ] Ejemplo de TreeView con íconos
- [ ] Ejemplo de TabControl con íconos
- [ ] Tests unitarios para ImageList
- [ ] Tests de integración con controles

---

## 📋 Plan de Implementación Sugerido

### Fase 1: Funcionalidad Básica (CRÍTICO)
1. Redimensionamiento automático con PIL
2. Conversión PIL Image → PhotoImage
3. Renderizado en ListView (CRÍTICO para demostrar funcionalidad)

### Fase 2: Integración Completa
4. Renderizado en TreeView
5. TabControl con ImageList
6. Button con ImageList

### Fase 3: Características Avanzadas
7. TransparentColor funcional
8. ColorDepth funcional
9. Métodos Draw() completos
10. ImageStream serialización

### Fase 4: Pulido
11. Tests unitarios
12. Ejemplos completos
13. Documentación

---

## 🔧 Código de Ejemplo para Implementar

### 1. Redimensionamiento en _add_image:

```python
def _add_image(self, image, key=None):
    """Internal method to add image."""
    if key is None:
        key = self._next_index
        self._next_index += 1
    
    # Convert and resize image
    photo_image = self._prepare_image(image)
    
    self._images[key] = photo_image
    self.CollectionChanged()
    return key

def _prepare_image(self, image):
    """Convert and resize image to PhotoImage at ImageSize."""
    try:
        from PIL import Image, ImageTk
        
        # If it's already a PhotoImage, try to extract PIL Image
        if hasattr(image, '_PhotoImage__photo'):
            # Already a tkinter PhotoImage, return as-is
            # (ideally we'd extract and resize, but tkinter doesn't allow this)
            return image
        
        # If it's a PIL Image
        if isinstance(image, Image.Image):
            # Resize to ImageSize
            if image.size != self.ImageSize:
                image = image.resize(self.ImageSize, Image.LANCZOS)
            
            # Apply transparent color if set
            if self.TransparentColor:
                # Convert to RGBA and set transparency
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')
                # ... apply transparent color logic
            
            # Convert to PhotoImage
            return ImageTk.PhotoImage(image)
        
        # If it's already a PhotoImage-compatible object
        return image
        
    except ImportError:
        # PIL not available, return image as-is
        return image
```

### 2. Renderizado en ListView:

```python
# En ListView._render_items()
def _render_items(self):
    """Render items in the treeview."""
    self._tree.delete(*self._tree.get_children())
    
    for idx, item in enumerate(self._items):
        # Get image from ImageList if available
        image = None
        if self._small_image_list:
            if item.ImageIndex >= 0:
                image = self._small_image_list.GetImage(item.ImageIndex)
            elif item.ImageKey:
                image = self._small_image_list.GetImage(item.ImageKey)
        
        # Build values
        values = item.SubItems if item.SubItems else []
        
        # Insert with image if available
        if image:
            # Note: ttk.Treeview doesn't support images directly
            # Need to use tags or custom rendering
            # Option 1: Use text with emoji/symbol prefix
            # Option 2: Custom rendering with Canvas overlay
            text = f"  {item.Text}"  # Space for image
            self._tree.insert('', 'end', text=text, values=values, image=image)
        else:
            self._tree.insert('', 'end', text=item.Text, values=values)
```

---

## 📚 Referencias

- Windows Forms ImageList: https://docs.microsoft.com/en-us/dotnet/api/system.windows.forms.imagelist
- PIL/Pillow: https://pillow.readthedocs.io/
- tkinter PhotoImage: https://docs.python.org/3/library/tkinter.html#images

---

**Última actualización**: 2026-01-26
