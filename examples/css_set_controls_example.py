"""
Example of using CSSManager to apply CSS styles to WinFormPy controls.

This script demonstrates how to convert CSS strings to property dictionaries
compatible with WinFormPy and apply them to controls using dictionaries.
Includes dynamic switching between two different themes.
"""

import sys
import os
import importlib.util

# Load winformpy.py from lib directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lib_dir = os.path.join(parent_dir, "lib")
module_path = os.path.join(lib_dir, "winformpy.py")

spec = importlib.util.spec_from_file_location("winform_py", module_path)
winform_py = importlib.util.module_from_spec(spec)
spec.loader.exec_module(winform_py)

# Load winform_py_tools.py
tools_path = os.path.join(lib_dir, "winformpy_tools.py")
spec_tools = importlib.util.spec_from_file_location("winform_py_tools", tools_path)
winform_py_tools = importlib.util.module_from_spec(spec_tools)
spec_tools.loader.exec_module(winform_py_tools)

# Import classes
Form = winform_py.Form
Button = winform_py.Button
Label = winform_py.Label
TextBox = winform_py.TextBox
Panel = winform_py.Panel

# Import CSSManager
CSSManager = winform_py_tools.CSSManager


# Definir temas CSS completos
LIGHT_CSS = """
/* Light Theme - Complete Styles */
body {
    background-color: #FFFFFF;
    color: #212529;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 12px;
}

.panel {
    background-color: #F8F9FA;
    border: 2px groove #DEE2E6;
    font-family: Arial;
    font-size: 11px;
}

.button {
    background-color: #0078D7;
    color: #FFFFFF;
    font-family: Arial;
    font-size: 10px;
    font-weight: bold;
    border: 1px solid #005A9E;
    width: 120px;
    height: 35px;
    padding: 5px 10px;
}

.label {
    background-color: #F8F9FA;
    color: #212529;
    font-family: Arial;
    font-size: 9px;
    font-weight: normal;
    border: none;
}

.textbox {
    background-color: #FFFFFF;
    color: #212529;
    font-family: Consolas;
    font-size: 9px;
    border: 1px solid #DEE2E6;
    width: 180px;
    height: 25px;
    padding: 2px;
}

.title-label {
    background-color: #F8F9FA;
    color: #212529;
    font-family: Arial;
    font-size: 12px;
    font-weight: bold;
}

.info-label {
    background-color: #F8F9FA;
    color: #6C757D;
    font-family: Consolas;
    font-size: 8px;
    font-weight: normal;
}
"""

DARK_CSS = """
/* Dark Theme - Complete Styles */
body {
    background-color: #2D3748;
    color: #F7FAFC;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 12px;
}

.panel {
    background-color: #374151;
    border: 2px groove #4A5568;
    font-family: Arial;
    font-size: 11px;
}

.button {
    background-color: #3182CE;
    color: #FFFFFF;
    font-family: Arial;
    font-size: 10px;
    font-weight: bold;
    border: 1px solid #2C5282;
    width: 120px;
    height: 35px;
    padding: 5px 10px;
}

.label {
    background-color: #4A5568;
    color: #F7FAFC;
    font-family: Arial;
    font-size: 9px;
    font-weight: normal;
    border: none;
}

.textbox {
    background-color: #2D3748;
    color: #F7FAFC;
    font-family: Consolas;
    font-size: 9px;
    border: 1px solid #4A5568;
    width: 180px;
    height: 25px;
    padding: 2px;
}

.title-label {
    background-color: #374151;
    color: #F7FAFC;
    font-family: Arial;
    font-size: 12px;
    font-weight: bold;
}

.info-label {
    background-color: #374151;
    color: #A0AEC0;
    font-family: Consolas;
    font-size: 8px;
    font-weight: normal;
}
"""

# Definir temas con CSS completos por tipo de control
LIGHT_THEME = {
    'full_css': LIGHT_CSS,
    'form': "background-color: #FFFFFF; color: #212529; font-family: 'Segoe UI', Arial, sans-serif; font-size: 12px;",
    'panel': "background-color: #F8F9FA; border: 2px groove #DEE2E6; font-family: Arial; font-size: 11px;",
    'button': "background-color: #0078D7; color: #FFFFFF; font-family: Arial; font-size: 10px; font-weight: bold; border: 1px solid #005A9E; width: 120px; height: 35px; padding: 5px 10px;",
    'label': "background-color: #F8F9FA; color: #212529; font-family: Arial; font-size: 9px; font-weight: normal; border: none;",
    'textbox': "background-color: #FFFFFF; color: #212529; font-family: Consolas; font-size: 9px; border: 1px solid #DEE2E6; width: 180px; height: 25px; padding: 2px;",
    'title_label': "background-color: #F8F9FA; color: #212529; font-family: Arial; font-size: 12px; font-weight: bold;",
    'info_label': "background-color: #F8F9FA; color: #6C757D; font-family: Consolas; font-size: 8px; font-weight: normal;",
    'color_buttons': {
        'red': "background-color: #DC3545; color: #FFFFFF; font-family: Arial; font-size: 9px; font-weight: bold;",
        'green': "background-color: #28A745; color: #FFFFFF; font-family: Arial; font-size: 9px; font-weight: bold;",
        'blue': "background-color: #0078D7; color: #FFFFFF; font-family: Arial; font-size: 9px; font-weight: bold;",
        'yellow': "background-color: #FFC107; color: #212529; font-family: Arial; font-size: 9px; font-weight: bold;"
    }
}

DARK_THEME = {
    'full_css': DARK_CSS,
    'form': "background-color: #2D3748; color: #F7FAFC; font-family: 'Segoe UI', Arial, sans-serif; font-size: 12px;",
    'panel': "background-color: #374151; border: 2px groove #4A5568; font-family: Arial; font-size: 11px;",
    'button': "background-color: #3182CE; color: #FFFFFF; font-family: Arial; font-size: 10px; font-weight: bold; border: 1px solid #2C5282; width: 120px; height: 35px; padding: 5px 10px;",
    'label': "background-color: #4A5568; color: #F7FAFC; font-family: Arial; font-size: 9px; font-weight: normal; border: none;",
    'textbox': "background-color: #2D3748; color: #F7FAFC; font-family: Consolas; font-size: 9px; border: 1px solid #4A5568; width: 180px; height: 25px; padding: 2px;",
    'title_label': "background-color: #374151; color: #F7FAFC; font-family: Arial; font-size: 12px; font-weight: bold;",
    'info_label': "background-color: #374151; color: #A0AEC0; font-family: Consolas; font-size: 8px; font-weight: normal;",
    'color_buttons': {
        'red': "background-color: #9F7AEA; color: #FFFFFF; font-family: Arial; font-size: 9px; font-weight: bold;",
        'green': "background-color: #ED8936; color: #FFFFFF; font-family: Arial; font-size: 9px; font-weight: bold;",
        'blue': "background-color: #38B2AC; color: #FFFFFF; font-family: Arial; font-size: 9px; font-weight: bold;",
        'yellow': "background-color: #F56565; color: #FFFFFF; font-family: Arial; font-size: 9px; font-weight: bold;"
    }
}


def apply_theme_to_control(control, theme_colors, control_type):
    """Aplica un tema específico a un control."""
    if control_type == 'button':
        control.BackColor = theme_colors['accent_bg']
        control.ForeColor = theme_colors['button_text']
    elif control_type == 'label':
        control.BackColor = theme_colors['secondary_bg']
        control.ForeColor = theme_colors['text_primary']
    elif control_type == 'textbox':
        control.BackColor = theme_colors['primary_bg']
        control.ForeColor = theme_colors['text_primary']
    elif control_type == 'panel':
        control.BackColor = theme_colors['panel_bg']


def main():
    # Variable global para el tema actual
    current_theme_css = LIGHT_CSS
    current_theme_name = "Light"

    # Crear formulario principal
    form = Form({
        'Text': 'CSS in WinFormPy Controls - Interchangeable Theme',
        'Width': 1000,
        'Height': 800,
        'StartPosition': 'CenterScreen',
        'BackColor': '#FFFFFF'
    })

    # Panel superior para controles de tema
    theme_panel = Panel(form, {
        'Left': 20,
        'Top': 20,
        'Width': 960,
        'Height': 80,
        'BackColor': '#F8F9FA',
        'BorderStyle': 'groove'
    })

    # Título del panel de tema
    lbl_theme_title = Label(form, {
        'Text': 'THEME SELECTION',
        'Left': 40,
        'Top': 30,
        'Width': 200,
        'Height': 25,
        'Font': ('Arial', 12, 'bold'),
        'ForeColor': '#212529',
        'BackColor': '#F8F9FA'
    })

    # Botón para tema claro
    btn_light_theme = Button(form, {
        'Text': 'Light Theme',
        'Left': 280,
        'Top': 30,
        'Width': 120,
        'Height': 35,
        'BackColor': '#0078D7',
        'ForeColor': '#FFFFFF',
        'Font': ('Arial', 10, 'bold')
    })

    # Botón para tema oscuro
    btn_dark_theme = Button(form, {
        'Text': 'Dark Theme',
        'Left': 420,
        'Top': 30,
        'Width': 120,
        'Height': 35,
        'BackColor': '#0078D7',
        'ForeColor': '#FFFFFF',
        'Font': ('Arial', 10, 'bold')
    })

    # Etiqueta que muestra el tema actual
    lbl_current_theme = Label(form, {
        'Text': 'Current theme: Light',
        'Left': 580,
        'Top': 35,
        'Width': 200,
        'Height': 25,
        'Font': ('Arial', 10),
        'ForeColor': '#212529',
        'BackColor': '#F8F9FA'
    })

    # ========================================================================
    # PANEL IZQUIERDO: Controles básicos
    # ========================================================================

    left_panel = Panel(form, {
        'Left': 20,
        'Top': 120,
        'Width': 470,
        'Height': 520,
        'BackColor': '#F8F9FA',
        'BorderStyle': 'groove'
    })

    # Título del panel izquierdo
    lbl_left_title = Label(form, {
        'Text': 'BASIC CONTROLS',
        'Left': 40,
        'Top': 130,
        'Width': 200,
        'Height': 25,
        'Font': ('Arial', 12, 'bold'),
        'ForeColor': '#212529',
        'BackColor': '#F8F9FA'
    })

    # Botón de ejemplo
    btn_example = Button(form, {
        'Text': 'Interactive Button',
        'Left': 40,
        'Top': 170,
        'Width': 180,
        'Height': 40,
        'BackColor': '#0078D7',
        'ForeColor': '#FFFFFF',
        'Font': ('Arial', 10, 'bold')
    })

    # Etiqueta de ejemplo
    lbl_example = Label(form, {
        'Text': 'This is an example label\nwith multiple lines of text',
        'Left': 40,
        'Top': 230,
        'Width': 180,
        'Height': 60,
        'BackColor': '#F8F9FA',
        'ForeColor': '#212529',
        'Font': ('Arial', 9)
    })

    # TextBox de ejemplo
    txt_example = TextBox(form, {
        'Text': 'Editable text field',
        'Left': 40,
        'Top': 310,
        'Width': 180,
        'Height': 25,
        'BackColor': '#FFFFFF',
        'ForeColor': '#212529',
        'Font': ('Consolas', 9)
    })

    # ========================================================================
    # PANEL DERECHO: Controles avanzados
    # ========================================================================

    right_panel = Panel(form, {
        'Left': 510,
        'Top': 120,
        'Width': 470,
        'Height': 520,
        'BackColor': '#F8F9FA',
        'BorderStyle': 'groove'
    })

    # Título del panel derecho
    lbl_right_title = Label(form, {
        'Text': 'ADVANCED CONTROLS',
        'Left': 530,
        'Top': 130,
        'Width': 200,
        'Height': 25,
        'Font': ('Arial', 12, 'bold'),
        'ForeColor': '#212529',
        'BackColor': '#F8F9FA'
    })

    # Panel interno con botones de colores
    color_panel = Panel(form, {
        'Left': 530,
        'Top': 170,
        'Width': 420,
        'Height': 120,
        'BackColor': '#F8F9FA',
        'BorderStyle': 'solid'
    })

    # Botones de colores dentro del panel
    btn_red = Button(form, {
        'Text': 'Red',
        'Left': 540,
        'Top': 180,
        'Width': 80,
        'Height': 35,
        'BackColor': '#DC3545',
        'ForeColor': '#FFFFFF',
        'Font': ('Arial', 9, 'bold')
    })

    btn_green = Button(form, {
        'Text': 'Green',
        'Left': 630,
        'Top': 180,
        'Width': 80,
        'Height': 35,
        'BackColor': '#28A745',
        'ForeColor': '#FFFFFF',
        'Font': ('Arial', 9, 'bold')
    })

    btn_blue = Button(form, {
        'Text': 'Blue',
        'Left': 720,
        'Top': 180,
        'Width': 80,
        'Height': 35,
        'BackColor': '#0078D7',
        'ForeColor': '#FFFFFF',
        'Font': ('Arial', 9, 'bold')
    })

    btn_yellow = Button(form, {
        'Text': 'Yellow',
        'Left': 810,
        'Top': 180,
        'Width': 80,
        'Height': 35,
        'BackColor': '#FFC107',
        'ForeColor': '#212529',
        'Font': ('Arial', 9, 'bold')
    })

    # Etiqueta informativa
    lbl_info = Label(form, {
        'Text': 'These buttons demonstrate different\ncolor styles applied dynamically\naccording to the selected theme.',
        'Left': 530,
        'Top': 230,
        'Width': 420,
        'Height': 60,
        'BackColor': '#F8F9FA',
        'ForeColor': '#6C757D',
        'Font': ('Arial', 9)
    })

    # ========================================================================
    # PANEL INFERIOR: Información del sistema
    # ========================================================================

    info_panel = Panel(form, {
        'Left': 20,
        'Top': 560,
        'Width': 960,
        'Height': 140,
        'BackColor': '#F8F9FA',
        'BorderStyle': 'groove'
    })

    # Título informativo
    lbl_info_title = Label(form, {
        'Text': 'SYSTEM INFORMATION',
        'Left': 40,
        'Top': 570,
        'Width': 200,
        'Height': 20,
        'Font': ('Arial', 10, 'bold'),
        'ForeColor': '#212529',
        'BackColor': '#F8F9FA'
    })

    # Texto explicativo
    lbl_system_info = Label(form, {
        'Text': 'CSSManager allows applying CSS styles to WinFormPy controls.',
        'Left': 40,
        'Top': 595,
        'Width': 920,
        'Height': 25,
        'Font': ('Consolas', 8),
        'ForeColor': '#6C757D',
        'BackColor': '#F8F9FA'
    })

    # TextBox para mostrar el CSS actual
    txt_css_display = TextBox(form, {
        'Text': current_theme_css,
        'Multiline': True,
        'Left': 40,
        'Top': 625,
        'Width': 920,
        'Height': 70,
        'ReadOnly': True,
        'Font': ('Consolas', 8),
        'BackColor': '#FFFFFF',
        'ForeColor': '#000000'
    })

    # ========================================================================
    # FUNCIONES PARA CAMBIAR TEMAS
    # ========================================================================

    def apply_theme(theme, theme_name):
        # Aplicar propiedades basadas en tema
        if theme_name == "Light":
            form.BackColor = '#FFFFFF'
            theme_panel.BackColor = '#F8F9FA'
            lbl_theme_title.BackColor = '#F8F9FA'
            lbl_theme_title.ForeColor = '#212529'
            btn_light_theme.BackColor = '#0078D7'
            btn_light_theme.ForeColor = '#FFFFFF'
            btn_dark_theme.BackColor = '#0078D7'
            btn_dark_theme.ForeColor = '#FFFFFF'
            lbl_current_theme.BackColor = '#F8F9FA'
            lbl_current_theme.ForeColor = '#212529'
            left_panel.BackColor = '#F8F9FA'
            lbl_left_title.BackColor = '#F8F9FA'
            lbl_left_title.ForeColor = '#212529'
            btn_example.BackColor = '#0078D7'
            btn_example.ForeColor = '#FFFFFF'
            lbl_example.BackColor = '#F8F9FA'
            lbl_example.ForeColor = '#212529'
            txt_example.BackColor = '#FFFFFF'
            txt_example.ForeColor = '#212529'
            right_panel.BackColor = '#F8F9FA'
            lbl_right_title.BackColor = '#F8F9FA'
            lbl_right_title.ForeColor = '#212529'
            color_panel.BackColor = '#F8F9FA'
            btn_red.BackColor = '#DC3545'
            btn_red.ForeColor = '#FFFFFF'
            btn_green.BackColor = '#28A745'
            btn_green.ForeColor = '#FFFFFF'
            btn_blue.BackColor = '#0078D7'
            btn_blue.ForeColor = '#FFFFFF'
            btn_yellow.BackColor = '#FFC107'
            btn_yellow.ForeColor = '#212529'
            lbl_info.BackColor = '#F8F9FA'
            lbl_info.ForeColor = '#6C757D'
            info_panel.BackColor = '#F8F9FA'
            lbl_info_title.BackColor = '#F8F9FA'
            lbl_info_title.ForeColor = '#212529'
            lbl_system_info.BackColor = '#F8F9FA'
            lbl_system_info.ForeColor = '#6C757D'
        else:  # Dark
            form.BackColor = '#2D3748'
            theme_panel.BackColor = '#374151'
            lbl_theme_title.BackColor = '#374151'
            lbl_theme_title.ForeColor = '#F7FAFC'
            btn_light_theme.BackColor = '#3182CE'
            btn_light_theme.ForeColor = '#FFFFFF'
            btn_dark_theme.BackColor = '#3182CE'
            btn_dark_theme.ForeColor = '#FFFFFF'
            lbl_current_theme.BackColor = '#374151'
            lbl_current_theme.ForeColor = '#F7FAFC'
            left_panel.BackColor = '#374151'
            lbl_left_title.BackColor = '#374151'
            lbl_left_title.ForeColor = '#F7FAFC'
            btn_example.BackColor = '#3182CE'
            btn_example.ForeColor = '#FFFFFF'
            lbl_example.BackColor = '#4A5568'
            lbl_example.ForeColor = '#F7FAFC'
            txt_example.BackColor = '#2D3748'
            txt_example.ForeColor = '#F7FAFC'
            right_panel.BackColor = '#374151'
            lbl_right_title.BackColor = '#374151'
            lbl_right_title.ForeColor = '#F7FAFC'
            color_panel.BackColor = '#374151'
            btn_red.BackColor = '#9F7AEA'
            btn_red.ForeColor = '#FFFFFF'
            btn_green.BackColor = '#ED8936'
            btn_green.ForeColor = '#FFFFFF'
            btn_blue.BackColor = '#38B2AC'
            btn_blue.ForeColor = '#FFFFFF'
            btn_yellow.BackColor = '#F56565'
            btn_yellow.ForeColor = '#FFFFFF'
            lbl_info.BackColor = '#374151'
            lbl_info.ForeColor = '#A0AEC0'
            info_panel.BackColor = '#374151'
            lbl_info_title.BackColor = '#374151'
            lbl_info_title.ForeColor = '#F7FAFC'
            lbl_system_info.BackColor = '#374151'
            lbl_system_info.ForeColor = '#A0AEC0'
        
        txt_css_display.Text = theme['full_css']
        lbl_current_theme.Text = f'Current theme: {theme_name}'

    def switch_to_light_theme():
        global current_theme_css
        current_theme_css = LIGHT_CSS
        apply_theme(LIGHT_THEME, "Light")

    def switch_to_dark_theme():
        global current_theme_css
        current_theme_css = DARK_CSS
        apply_theme(DARK_THEME, "Dark")

    # Conectar eventos de los botones de tema
    btn_light_theme.Click = switch_to_light_theme
    btn_dark_theme.Click = switch_to_dark_theme

    # Aplicar tema inicial
    apply_theme(LIGHT_THEME, "Light")

    # Mostrar el formulario
    form.ShowDialog()


if __name__ == "__main__":
    main()