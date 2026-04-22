"""Tests for WinFormPy theme modules."""

from winformpy.themes.winforms_theme import (
    SYSTEM_COLORS,
    TYPOGRAPHY,
    winforms_colors,
    winforms_fonts,
)
from winformpy.themes.winui3_theme import winui_colors, winui_fonts


class TestWinFormsTheme:
    """Tests for WinForms theme configuration."""

    def test_system_colors_is_dict(self):
        assert isinstance(SYSTEM_COLORS, dict)

    def test_system_colors_has_required_keys(self):
        required = ["control", "window", "control_text", "highlight"]
        for key in required:
            assert key in SYSTEM_COLORS, f"Missing key: {key}"

    def test_system_colors_are_hex_strings(self):
        for key, value in SYSTEM_COLORS.items():
            assert isinstance(value, str), f"{key} is not a string"
            assert value.startswith("#"), f"{key} does not start with #"

    def test_colors_instance_has_attributes(self):
        assert hasattr(winforms_colors, "Control")
        assert hasattr(winforms_colors, "Window")
        assert hasattr(winforms_colors, "Highlight")

    def test_colors_values_are_hex(self):
        assert winforms_colors.Control.startswith("#")

    def test_fonts_has_default(self):
        assert hasattr(winforms_fonts, "DefaultFont")
        assert isinstance(winforms_fonts.DefaultFont, tuple)

    def test_typography_has_font_family(self):
        assert "font_family" in TYPOGRAPHY


class TestWinUI3Theme:
    """Tests for WinUI 3 theme configuration."""

    def test_colors_instance_exists(self):
        assert winui_colors is not None

    def test_colors_has_accent(self):
        assert hasattr(winui_colors, "AccentDefault") or hasattr(
            winui_colors, "Accent"
        )

    def test_fonts_instance_exists(self):
        assert winui_fonts is not None

    def test_fonts_has_body(self):
        assert hasattr(winui_fonts, "Body") or hasattr(winui_fonts, "DefaultFont")
