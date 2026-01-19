"""
WinUI 3 Gallery Template - Modified Style
=========================================
Adaptado para coincidir con el estilo visual de Windows 11 (WinUI 3)
usando la biblioteca WinFormPy.

CAMBIOS VISUALES:
- Paleta de colores 'Mica' simulada.
- Navegación lateral estilo 'NavigationView'.
- Controles agrupados en 'Cards' (Tarjetas).
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from winformpy import (
    Form, Panel, Button, Label, TextBox, CheckBox, RadioButton,
    ListBox, ComboBox, ProgressBar, TrackBar, GroupBox,
    AnchorStyles, DockStyle, Font, FontStyle, Color, FlatStyle,
    TabControl, TabPage, TreeView, PictureBox, MessageBox
)

from winformpy_extended import WinUIToggleSwitch, WinUIExpander, ExtendedLabel, WinUITextBox, WinUIProgressBar

# --- Design System (WinUI 3 Theme - Light Mode) ---
# Colores extraídos de las guías de diseño de Windows 11

class WinUIColors:
    # Fondos
    WindowBg = "#F3F3F3"      # Color Mica Alt (fondo general)
    SidebarBg = "#F3F3F3"     # Barra lateral (se funde con el fondo en Win11)
    ContentBg = "#FFFFFF"     # Capa de contenido (Layer 1)
    CardBg = "#FFFFFF"        # Fondo de tarjetas/grupos
    CardBorder = "#E5E5E5"    # Borde sutil para tarjetas
    
    # Interacción
    Accent = "#0067C0"        # Windows Blue
    AccentHover = "#1975C5"
    AccentText = "#FFFFFF"
    
    # Estados de Botones/Nav
    ControlFill = "#FFFFFF"   # Fondo de inputs
    ControlBorder = "#D1D1D1" # Borde de inputs
    NavHover = "#EAEAEA"
    NavPressed = "#EDEDED"
    NavSelectedLine = "#0067C0" # Indicador de selección
    
    # Texto
    TextPrimary = "#202020"   # Casi negro
    TextSecondary = "#5D5D5D" # Gris oscuro
    TextDisabled = "#A0A0A0"

class WinUIFonts:
    # Segoe UI is the standard Windows font
    _Header = None
    _SubHeader = None
    _Body = None
    _Caption = None
    _Icon = None

    @classmethod
    def _init(cls):
        if cls._Header is None:
            cls._Header = Font("Segoe UI Variable Display", 20, FontStyle.Bold)
            cls._SubHeader = Font("Segoe UI Variable Display", 14, FontStyle.Bold)
            cls._Body = Font("Segoe UI Variable Text", 10, FontStyle.Regular)
            cls._Caption = Font("Segoe UI Variable Text", 9, FontStyle.Regular)
            cls._Icon = Font("Segoe MDL2 Assets", 12, FontStyle.Regular)

    @property
    def Header(self):
        self._init()
        return self._Header

    @property
    def SubHeader(self):
        self._init()
        return self._SubHeader

    @property
    def Body(self):
        self._init()
        return self._Body

    @property
    def Caption(self):
        self._init()
        return self._Caption

    @property
    def Icon(self):
        self._init()
        return self._Icon

# Instantiate for easier access
WinUIFonts = WinUIFonts()

# --- Helper Functions ---

def apply_bg_color(panel, color):
    """Force background color on a Panel and its internal tk containers.
    
    BackColor now applies to all internal widgets automatically.
    """
    panel.BackColor = color

# --- Auxiliary Components for Styling ---

class ContentCard(Panel):
    """
    Simulates a 'SettingsGroup' or 'Card' from WinUI 3.
    A white panel with a subtle gray border.
    """
    def __init__(self, parent, height=100, dock=DockStyle.Top):
        super().__init__(parent, {'BackColor': WinUIColors.CardBg})
        self.Height = height
        self.Dock = dock
        # Force the color on the tk widget
        apply_bg_color(self, WinUIColors.CardBg)
        
        # Bottom border/separator
        self.border_bottom = Panel(self, {'BackColor': WinUIColors.CardBorder})
        self.border_bottom.Height = 1
        self.border_bottom.Dock = DockStyle.Bottom
        apply_bg_color(self.border_bottom, WinUIColors.CardBorder)

class PrimaryButton(Button):
    """Botón con el color de acento (Azul)"""
    def __init__(self, parent, text="Button"):
        super().__init__(parent)
        self.Text = text
        self.FlatStyle = FlatStyle.Flat
        self.BackColor = WinUIColors.Accent
        self.ForeColor = WinUIColors.AccentText
        self.Font = WinUIFonts.Body
        self.Size = (120, 32)
        # Use WinFormPy method to remove borders
        self.RemoveBorders()

# --- Main Application ---

class WinUI3Gallery(Form):
    def __init__(self):
        super().__init__()
        self.Text = "WinUI 3 Gallery Template"
        self.Size = (1000, 700)
        self.BackColor = WinUIColors.WindowBg
        
        # CRITICAL: Apply geometry BEFORE adding children
        self.ApplyLayout()
        
        # Estado de navegación
        self.current_page = None
        self.nav_buttons = {} # Store references to update styles

        # 1. Crear Layout Principal
        self._init_layout()
        
        # 2. Inicializar Páginas
        self.pages = {}
        self._init_pages()
        
        # 3. Navegar a inicio
        self.navigate("inputs")

    def _init_layout(self):
        # IMPORTANT: In WinFormPy, create DockStyle.Fill LAST
        # Order: Left sidebar first, then Fill content area
        
        # --- Sidebar (NavigationView) ---
        self.sidebar = Panel(self, {'BackColor': WinUIColors.SidebarBg})
        self.sidebar.Dock = DockStyle.Left
        self.sidebar.Width = 280
        apply_bg_color(self.sidebar, WinUIColors.SidebarBg)

        # App Title (Top left)
        self.app_title = Label(self.sidebar, {'BackColor': WinUIColors.SidebarBg})
        self.app_title.Text = "WinUI 3 Gallery"
        self.app_title.Font = Font("Segoe UI", 14, FontStyle.Bold)
        self.app_title.ForeColor = WinUIColors.TextPrimary
        self.app_title.Dock = DockStyle.Top
        self.app_title.Height = 50
        
        # Search box (AutoSuggestBox simulation)
        self.search_panel = Panel(self.sidebar, {'BackColor': WinUIColors.SidebarBg})
        self.search_panel.Dock = DockStyle.Top
        self.search_panel.Height = 45
        apply_bg_color(self.search_panel, WinUIColors.SidebarBg)
        
        self.search_box = WinUITextBox(self.search_panel, {'BackColor': WinUIColors.ControlFill})
        self.search_box.Location = (10, 5)
        self.search_box.Size = (250, 30)
        self.search_box.Text = "Search..."
        self.search_box.ForeColor = WinUIColors.TextSecondary
        
        # Spacer
        spacer = Panel(self.sidebar, {'BackColor': WinUIColors.SidebarBg})
        spacer.Dock = DockStyle.Top
        spacer.Height = 15
        apply_bg_color(spacer, WinUIColors.SidebarBg)

        # Menu items container - Use Top dock with fixed height to avoid Fill issues
        self.menu_container = Panel(self.sidebar, {'BackColor': WinUIColors.SidebarBg})
        self.menu_container.Dock = DockStyle.Top
        self.menu_container.Height = 200  # Space for ~4-5 nav items (42px each)
        apply_bg_color(self.menu_container, WinUIColors.SidebarBg)

        # Crear botones de navegación - use Location instead of Dock for precise control
        self._add_nav_item("inputs", "Basic Input", 0)
        self._add_nav_item("collections", "Collections", 1)
        self._add_nav_item("dialogs", "Dialogs & Status", 2)
        self._add_nav_item("media", "Media", 3)

        # --- Content Area (Created AFTER sidebar so it fills remaining space) ---
        self.content_area = Panel(self, {'BackColor': WinUIColors.WindowBg})
        self.content_area.Dock = DockStyle.Fill
        apply_bg_color(self.content_area, WinUIColors.WindowBg)
        
        # The white panel where content goes
        self.main_frame = Panel(self.content_area, {'BackColor': WinUIColors.ContentBg})
        self.main_frame.Dock = DockStyle.Fill
        apply_bg_color(self.main_frame, WinUIColors.ContentBg)
        
        # Page header (Large title)
        self.page_header = Panel(self.main_frame, {'BackColor': WinUIColors.ContentBg})
        self.page_header.Dock = DockStyle.Top
        self.page_header.Height = 70
        apply_bg_color(self.page_header, WinUIColors.ContentBg)
        
        self.lbl_page_title = Label(self.page_header, {'BackColor': WinUIColors.ContentBg})
        self.lbl_page_title.Text = "Page Title"
        self.lbl_page_title.Font = WinUIFonts.Header
        self.lbl_page_title.ForeColor = WinUIColors.TextPrimary
        self.lbl_page_title.Location = (30, 20)
        self.lbl_page_title.AutoSize = True

        # Page content container
        self.page_content = Panel(self.main_frame, {'BackColor': WinUIColors.ContentBg})
        self.page_content.Dock = DockStyle.Fill
        self.page_content.AutoScroll = True
        apply_bg_color(self.page_content, WinUIColors.ContentBg) 

    def _add_nav_item(self, key, text, index):
        """Creates a NavigationViewItem-style button"""
        y_pos = index * 44  # 44px per item (42 + 2 spacing)
        
        container = Panel(self.menu_container, {'BackColor': WinUIColors.SidebarBg})
        container.Location = (0, y_pos)
        container.Size = (280, 42)
        apply_bg_color(container, WinUIColors.SidebarBg)
        
        # Selection indicator (Blue bar on left)
        indicator = Panel(container, {'BackColor': WinUIColors.Accent})
        indicator.Location = (8, 8)
        indicator.Size = (3, 24)
        apply_bg_color(indicator, WinUIColors.Accent)
        indicator.Visible = False
        
        btn = Button(container, {'BackColor': WinUIColors.SidebarBg})
        btn.Text = "    " + text
        btn.Location = (15, 4)
        btn.Size = (245, 34)
        btn.FlatStyle = FlatStyle.Flat
        btn.TextAlign = 'w'
        btn.ForeColor = WinUIColors.TextPrimary
        btn.Font = WinUIFonts.Body
        
        # Remove borders using WinFormPy method
        btn.RemoveBorders()
        btn.BackColor = WinUIColors.SidebarBg
        
        # Events
        btn.Click = lambda s, e: self.navigate(key)
        
        def on_enter(s, e):
            if self.current_page != key:
                btn.BackColor = WinUIColors.NavHover
        def on_leave(s, e):
            if self.current_page != key:
                btn.BackColor = WinUIColors.SidebarBg
                
        btn.MouseEnter = on_enter
        btn.MouseLeave = on_leave
        
        # Guardar referencias
        self.nav_buttons[key] = {
            'btn': btn,
            'indicator': indicator,
            'container': container
        }

    def navigate(self, key):
        # 1. Actualizar estilos visuales del menú
        for k, item in self.nav_buttons.items():
            if k == key:
                # Estado seleccionado
                item['indicator'].BackColor = WinUIColors.Accent
                apply_bg_color(item['indicator'], WinUIColors.Accent)
                item['indicator'].Visible = True
                item['btn'].BackColor = WinUIColors.NavPressed
                item['btn'].Font = Font("Segoe UI Variable Text", 10, FontStyle.Bold)
            else:
                # Estado normal
                item['indicator'].Visible = False
                item['btn'].BackColor = WinUIColors.SidebarBg
                item['btn'].Font = WinUIFonts.Body
        
        self.current_page = key
        
        # 2. Cambiar contenido
        # Ocultar todas las paginas
        for p in self.pages.values():
            p.Visible = False
            
        # Mostrar nueva
        if key in self.pages:
            self.pages[key].Visible = True
            # Actualizar título
            titles = {
                "inputs": "Basic Input", 
                "collections": "Collections", 
                "dialogs": "Dialogs & Status",
                "media": "Media Player"
            }
            self.lbl_page_title.Text = titles.get(key, "Gallery")

    def _init_pages(self):
        # Helper para crear paginas - Use Location instead of Dock.Fill to avoid conflicts
        def create_page_container():
            p = Panel(self.page_content, {'BackColor': WinUIColors.ContentBg})
            p.Location = (0, 0)
            p.Size = (700, 550)  # Large enough to contain content
            p.Visible = False
            apply_bg_color(p, WinUIColors.ContentBg)
            return p

        # --- PAGE 1: INPUTS ---
        self.pages['inputs'] = create_page_container()
        p1 = self.pages['inputs']
        
        # Section 1: Buttons
        card1 = ContentCard(p1, height=160)
        card1.BackColor = WinUIColors.CardBg
        
        lbl = Label(card1)
        lbl.Text = "Buttons"
        lbl.Font = WinUIFonts.SubHeader
        lbl.Location = (20, 15)
        lbl.AutoSize = True
        lbl.BackColor = WinUIColors.CardBg
        lbl.ForeColor = WinUIColors.TextPrimary
        
        desc = Label(card1)
        desc.Text = "Standard button controls following Windows 11 Fluent Design."
        desc.Font = WinUIFonts.Caption
        desc.ForeColor = WinUIColors.TextSecondary
        desc.Location = (20, 45)
        desc.AutoSize = True
        desc.BackColor = WinUIColors.CardBg
        
        # Accent button
        btn_primary = PrimaryButton(card1, "Primary")
        btn_primary.Location = (20, 85)
        
        # Standard button
        btn_sec = Button(card1)
        btn_sec.Text = "Secondary"
        btn_sec.Location = (160, 85)
        btn_sec.Size = (120, 32)
        btn_sec.BackColor = WinUIColors.ControlFill
        btn_sec.ForeColor = WinUIColors.TextPrimary
        btn_sec.FlatStyle = FlatStyle.Flat
        
        # Section 2: Checkboxes & Toggles
        card2 = ContentCard(p1, height=180)
        card2.BackColor = WinUIColors.CardBg
        
        lbl2 = Label(card2)
        lbl2.Text = "Checkboxes & Radios"
        lbl2.Font = WinUIFonts.SubHeader
        lbl2.Location = (20, 15)
        lbl2.AutoSize = True
        lbl2.BackColor = WinUIColors.CardBg
        lbl2.ForeColor = WinUIColors.TextPrimary
        
        chk1 = CheckBox(card2)
        chk1.Text = "Two-state CheckBox"
        chk1.Location = (20, 55)
        chk1.AutoSize = True
        chk1.BackColor = WinUIColors.CardBg
        chk1.ForeColor = WinUIColors.TextPrimary
        
        chk2 = CheckBox(card2)
        chk2.Text = "Three-state CheckBox"
        chk2.Location = (20, 85)
        chk2.Checked = True
        chk2.AutoSize = True
        chk2.BackColor = WinUIColors.CardBg
        chk2.ForeColor = WinUIColors.TextPrimary
        
        rb1 = RadioButton(card2)
        rb1.Text = "Option A"
        rb1.Location = (250, 55)
        rb1.AutoSize = True
        rb1.BackColor = WinUIColors.CardBg
        rb1.ForeColor = WinUIColors.TextPrimary
        
        rb2 = RadioButton(card2)
        rb2.Text = "Option B"
        rb2.Location = (250, 85)
        rb2.AutoSize = True
        rb2.BackColor = WinUIColors.CardBg
        rb2.ForeColor = WinUIColors.TextPrimary
        
        # WinUIToggleSwitch from winformpy_extended (inherits BackColor from parent)
        toggle = WinUIToggleSwitch(card2, text="WiFi Connection")
        toggle.Location = (20, 125)

        # Section 3: Expanders (winformpy_extended)
        card3 = ContentCard(p1, height=180)
        card3.BackColor = WinUIColors.CardBg
        
        lbl3 = Label(card3)
        lbl3.Text = "Expanders & Detailed Info"
        lbl3.Font = WinUIFonts.SubHeader
        lbl3.Location = (20, 15)
        lbl3.AutoSize = True
        lbl3.BackColor = WinUIColors.CardBg
        lbl3.ForeColor = WinUIColors.TextPrimary

        # WinUIExpander inherits BackColor from parent automatically
        exp = WinUIExpander(card3, title="Click to see more details", height_expanded=120)
        exp.Location = (20, 55)
        exp.Width = 450
        
        # Content inside the expander (Using ExtendedLabel for multiline)
        exp_lbl = ExtendedLabel(exp.content)
        exp_lbl.Text = "This content was hidden inside the Expander control from winformpy_extended. It supports automatic text wrapping when the window is resized."
        exp_lbl.Dock = DockStyle.Fill
        exp_lbl.BackColor = WinUIColors.CardBg
        exp_lbl.Font = WinUIFonts.Caption
        exp_lbl.ForeColor = WinUIColors.TextSecondary

        # --- PAGE 2: COLLECTIONS ---
        self.pages['collections'] = create_page_container()
        p2 = self.pages['collections']
        
        card_coll = ContentCard(p2, height=280)
        card_coll.BackColor = WinUIColors.CardBg
        
        lbl_list = Label(card_coll)
        lbl_list.Text = "ListBox & ComboBox"
        lbl_list.Font = WinUIFonts.SubHeader
        lbl_list.Location = (20, 15)
        lbl_list.AutoSize = True
        lbl_list.BackColor = WinUIColors.CardBg
        lbl_list.ForeColor = WinUIColors.TextPrimary
        
        cb = ComboBox(card_coll)
        cb.Location = (20, 55)
        cb.Size = (200, 30)
        cb.Items.AddRange(["Item 1", "Item 2", "Item 3", "Blue", "Red", "Green"])
        
        lb = ListBox(card_coll)
        lb.Location = (20, 100)
        lb.Size = (300, 140)
        lb.Items.AddRange(["List Item A", "List Item B", "List Item C"])
        lb.BackColor = WinUIColors.ControlFill


        # --- PAGE 3: DIALOGS ---
        self.pages['dialogs'] = create_page_container()
        p3 = self.pages['dialogs']
        
        # Card 1: Progress Controls
        card_prog = ContentCard(p3, height=160)
        card_prog.BackColor = WinUIColors.CardBg
        
        lbl_prog = Label(card_prog)
        lbl_prog.Text = "Progress Controls"
        lbl_prog.Font = WinUIFonts.SubHeader
        lbl_prog.Location = (20, 15)
        lbl_prog.AutoSize = True
        lbl_prog.BackColor = WinUIColors.CardBg
        lbl_prog.ForeColor = WinUIColors.TextPrimary
        
        pb = WinUIProgressBar(card_prog)
        pb.Location = (20, 55)
        pb.Size = (400, 25)
        pb.Value = 60
        
        tb = TrackBar(card_prog)
        tb.Location = (20, 95)
        tb.Size = (400, 40)

        # Card 2: Dialog Buttons
        card_dlg = ContentCard(p3, height=180)
        card_dlg.BackColor = WinUIColors.CardBg
        
        lbl_dlg = Label(card_dlg)
        lbl_dlg.Text = "Message Dialogs"
        lbl_dlg.Font = WinUIFonts.SubHeader
        lbl_dlg.Location = (20, 15)
        lbl_dlg.AutoSize = True
        lbl_dlg.BackColor = WinUIColors.CardBg
        lbl_dlg.ForeColor = WinUIColors.TextPrimary
        
        lbl_dlg_desc = Label(card_dlg)
        lbl_dlg_desc.Text = "Click buttons below to show different message dialogs."
        lbl_dlg_desc.Font = WinUIFonts.Caption
        lbl_dlg_desc.ForeColor = WinUIColors.TextSecondary
        lbl_dlg_desc.Location = (20, 45)
        lbl_dlg_desc.AutoSize = True
        lbl_dlg_desc.BackColor = WinUIColors.CardBg
        
        btn_info = PrimaryButton(card_dlg, "Info Dialog")
        btn_info.Location = (20, 80)
        btn_info.Click = lambda s, e: MessageBox.Show("This is an information message.", "Information")
        
        btn_warn = Button(card_dlg)
        btn_warn.Text = "Warning"
        btn_warn.Location = (160, 80)
        btn_warn.Size = (100, 32)
        btn_warn.BackColor = "#FFA500"  # Orange
        btn_warn.ForeColor = "#FFFFFF"
        btn_warn.FlatStyle = FlatStyle.Flat
        btn_warn.Click = lambda s, e: MessageBox.Show("This is a warning message!", "Warning")
        
        btn_error = Button(card_dlg)
        btn_error.Text = "Error"
        btn_error.Location = (280, 80)
        btn_error.Size = (100, 32)
        btn_error.BackColor = "#DC3545"  # Red
        btn_error.ForeColor = "#FFFFFF"
        btn_error.FlatStyle = FlatStyle.Flat
        btn_error.Click = lambda s, e: MessageBox.Show("This is an error message!", "Error")
        
        btn_confirm = Button(card_dlg)
        btn_confirm.Text = "Confirm Dialog"
        btn_confirm.Location = (20, 125)
        btn_confirm.Size = (120, 32)
        btn_confirm.BackColor = "#F0F0F0"  # WinUI 3 subtle/secondary button
        btn_confirm.ForeColor = WinUIColors.TextPrimary
        btn_confirm.FlatStyle = FlatStyle.Flat
        btn_confirm.Click = lambda s, e: MessageBox.Show(
            "Do you want to continue?", "Confirm", 
        )

        # --- PAGE 4: MEDIA ---
        self.pages['media'] = create_page_container()
        p4 = self.pages['media']
        
        # Card 1: PictureBox Demo
        card_pic = ContentCard(p4, height=250)
        card_pic.BackColor = WinUIColors.CardBg
        
        lbl_pic = Label(card_pic)
        lbl_pic.Text = "PictureBox Control"
        lbl_pic.Font = WinUIFonts.SubHeader
        lbl_pic.Location = (20, 15)
        lbl_pic.AutoSize = True
        lbl_pic.BackColor = WinUIColors.CardBg
        lbl_pic.ForeColor = WinUIColors.TextPrimary
        
        lbl_pic_desc = Label(card_pic)
        lbl_pic_desc.Text = "Display images in your application."
        lbl_pic_desc.Font = WinUIFonts.Caption
        lbl_pic_desc.ForeColor = WinUIColors.TextSecondary
        lbl_pic_desc.Location = (20, 45)
        lbl_pic_desc.AutoSize = True
        lbl_pic_desc.BackColor = WinUIColors.CardBg
        
        # Placeholder for image
        pic_frame = Panel(card_pic, {'BackColor': WinUIColors.ControlFill})
        pic_frame.Location = (20, 75)
        pic_frame.Size = (200, 150)
        apply_bg_color(pic_frame, WinUIColors.ControlFill)
        
        pic_placeholder = Label(pic_frame)
        pic_placeholder.Text = "📷 Image Placeholder"
        pic_placeholder.Location = (40, 60)
        pic_placeholder.AutoSize = True
        pic_placeholder.BackColor = WinUIColors.ControlFill
        pic_placeholder.ForeColor = WinUIColors.TextSecondary
        
        # Card 2: TreeView Demo
        card_tree = ContentCard(p4, height=220)
        card_tree.BackColor = WinUIColors.CardBg
        
        lbl_tree = Label(card_tree)
        lbl_tree.Text = "TreeView Control"
        lbl_tree.Font = WinUIFonts.SubHeader
        lbl_tree.Location = (20, 15)
        lbl_tree.AutoSize = True
        lbl_tree.BackColor = WinUIColors.CardBg
        lbl_tree.ForeColor = WinUIColors.TextPrimary
        
        tree = TreeView(card_tree)
        tree.Location = (20, 50)
        tree.Size = (300, 150)
        tree.BackColor = WinUIColors.ControlFill
        
        # Add sample nodes
        root1 = tree.Nodes.Add("Documents")
        root1.Nodes.Add("Work Files")
        root1.Nodes.Add("Personal")
        root2 = tree.Nodes.Add("Pictures")
        root2.Nodes.Add("Vacation 2025")
        root2.Nodes.Add("Family")
        tree.Nodes.Add("Downloads")

if __name__ == "__main__":
    app = WinUI3Gallery()
    app.Show()
