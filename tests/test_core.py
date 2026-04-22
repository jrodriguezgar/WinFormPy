"""Tests for core non-GUI classes in winformpy.winformpy.

Covers: EventArgs, Color, Size, Point, Rectangle, Font, FontStyle, enums.
These classes have no Tkinter dependency and can be tested headlessly.
"""

import pytest
from winformpy.winformpy import (
    EventArgs,
    Color,
    Size,
    Point,
    Rectangle,
    Font,
    FontStyle,
    DockStyle,
    AnchorStyles,
    DialogResult,
    FormBorderStyle,
    FormStartPosition,
    ContentAlignment,
    FlatStyle,
    FormWindowState,
    Orientation,
    MessageBoxButtons,
    MessageBoxIcon,
    CheckState,
    AutoSizeMode,
    BorderStyle,
)


# =============================================================================
# EventArgs
# =============================================================================


class TestEventArgs:
    """Tests for EventArgs data class."""

    def test_empty_instance(self):
        e = EventArgs()
        assert e.IsEmpty is True
        assert e.X == 0
        assert e.Y == 0
        assert e.Button == 0
        assert e.KeyChar == ""
        assert e.KeyCode == 0
        assert e.Delta == 0
        assert e.Shift is False
        assert e.Control is False
        assert e.Alt is False
        assert e.Data is None
        assert e.Cancel is False

    def test_static_empty(self):
        assert EventArgs.Empty is not None
        assert EventArgs.Empty.IsEmpty is True

    def test_from_dict(self):
        data = {"key": "value", "count": 42}
        e = EventArgs(data)
        assert e.Data == data
        assert e.IsEmpty is False

    def test_from_mock_event(self):
        class MockEvent:
            x = 100
            y = 200
            num = 1
            char = "a"
            keycode = 65
            delta = 120
            state = 0x0005  # Shift + Control

        e = EventArgs(MockEvent())
        assert e.X == 100
        assert e.Y == 200
        assert e.Button == 1
        assert e.KeyChar == "a"
        assert e.KeyCode == 65
        assert e.Delta == 120
        assert e.Shift is True
        assert e.Control is True
        assert e.Alt is False

    def test_cancel_property(self):
        e = EventArgs()
        e.Cancel = True
        assert e.Cancel is True


# =============================================================================
# Color
# =============================================================================


class TestColor:
    """Tests for Color class."""

    def test_from_hex_string(self):
        c = Color("#FF0000")
        assert str(c) == "#FF0000"

    def test_from_hex_without_hash(self):
        c = Color("FF0000")
        assert str(c) == "#FF0000"

    def test_from_named_color(self):
        c = Color("red")
        assert str(c) == "red"

    def test_from_none(self):
        c = Color(None)
        assert str(c) == "#000000"

    def test_from_empty_string(self):
        c = Color("")
        assert str(c) == "#000000"

    def test_from_rgb(self):
        c = Color.FromRgb(255, 128, 0)
        assert str(c) == "#FF8000"

    def test_from_rgb_clamped(self):
        c = Color.FromRgb(300, -10, 128)
        assert c.R == 255
        assert c.G == 0
        assert c.B == 128

    def test_from_hex_static(self):
        c = Color.FromHex("#00FF00")
        assert str(c) == "#00FF00"

    def test_from_hex_static_no_hash(self):
        c = Color.FromHex("0000FF")
        assert str(c) == "#0000FF"

    def test_from_hex_empty(self):
        c = Color.FromHex("")
        assert str(c) == "#000000"

    def test_from_name(self):
        c = Color.FromName("Red")
        assert str(c) == "#FF0000"

    def test_from_name_case_insensitive(self):
        c = Color.FromName("red")
        assert str(c) == "#FF0000"

    def test_rgb_components(self):
        c = Color("#1A2B3C")
        assert c.R == 0x1A
        assert c.G == 0x2B
        assert c.B == 0x3C
        assert c.A == 255

    def test_named_color_constants(self):
        assert Color.Red == "#FF0000"
        assert Color.Green == "#008000"
        assert Color.Blue == "#0000FF"
        assert Color.White == "#FFFFFF"
        assert Color.Black == "#000000"

    def test_repr(self):
        c = Color("#AABBCC")
        assert repr(c) == "Color('#AABBCC')"

    def test_color_name_property(self):
        c = Color("#FF0000")
        assert c.Name == "Red"

    def test_color_unknown_name(self):
        c = Color("#123456")
        assert c.Name == "#123456"


# =============================================================================
# Size, Point, Rectangle
# =============================================================================


class TestSize:
    """Tests for Size class."""

    def test_default(self):
        s = Size()
        assert s.Width == 0
        assert s.Height == 0

    def test_with_values(self):
        s = Size(800, 600)
        assert s.Width == 800
        assert s.Height == 600


class TestPoint:
    """Tests for Point class."""

    def test_default(self):
        p = Point()
        assert p.X == 0
        assert p.Y == 0

    def test_with_values(self):
        p = Point(10, 20)
        assert p.X == 10
        assert p.Y == 20

    def test_str(self):
        p = Point(5, 10)
        assert str(p) == "{X=5,Y=10}"


class TestRectangle:
    """Tests for Rectangle class."""

    def test_default(self):
        r = Rectangle()
        assert r.X == 0
        assert r.Y == 0
        assert r.Width == 0
        assert r.Height == 0

    def test_with_values(self):
        r = Rectangle(10, 20, 100, 50)
        assert r.Left == 10
        assert r.Top == 20
        assert r.Right == 110
        assert r.Bottom == 70

    def test_contains(self):
        r = Rectangle(0, 0, 100, 100)
        assert r.Contains(50, 50) is True
        assert r.Contains(0, 0) is True
        assert r.Contains(99, 99) is True
        assert r.Contains(100, 100) is False
        assert r.Contains(-1, 50) is False

    def test_str(self):
        r = Rectangle(1, 2, 3, 4)
        assert str(r) == "{X=1,Y=2,Width=3,Height=4}"


# =============================================================================
# FontStyle
# =============================================================================


class TestFontStyle:
    """Tests for FontStyle IntFlag enum."""

    def test_regular(self):
        assert FontStyle.Regular == 0

    def test_bold(self):
        assert FontStyle.Bold == 1

    def test_combined(self):
        style = FontStyle.Bold | FontStyle.Italic
        assert FontStyle.Bold in style
        assert FontStyle.Italic in style
        assert FontStyle.Underline not in style

    def test_all_combined(self):
        style = FontStyle.Bold | FontStyle.Italic | FontStyle.Underline | FontStyle.Strikeout
        assert style == 15


# =============================================================================
# Enums
# =============================================================================


class TestEnums:
    """Tests for WinForms enum types."""

    def test_dock_style_values(self):
        assert DockStyle.None_.value == 0
        assert DockStyle.Top.value == 1
        assert DockStyle.Bottom.value == 2
        assert DockStyle.Left.value == 3
        assert DockStyle.Right.value == 4
        assert DockStyle.Fill.value == 5

    def test_anchor_styles_flags(self):
        anchor = AnchorStyles.Top | AnchorStyles.Left
        assert AnchorStyles.Top in anchor
        assert AnchorStyles.Left in anchor
        assert AnchorStyles.Bottom not in anchor

    def test_dialog_result(self):
        assert DialogResult.OK.value == 1
        assert DialogResult.Cancel.value == 2
        assert DialogResult.Yes.value == 6
        assert DialogResult.No.value == 7

    def test_form_border_style(self):
        assert FormBorderStyle.None_.value == 0
        assert FormBorderStyle.Sizable.value == 4

    def test_form_start_position(self):
        assert FormStartPosition.CenterScreen.value == 1
        assert FormStartPosition.Manual.value == 0

    def test_content_alignment(self):
        assert ContentAlignment.TopLeft.value == 1
        assert ContentAlignment.MiddleCenter.value == 32
        assert ContentAlignment.BottomRight.value == 1024

    def test_flat_style(self):
        assert FlatStyle.Flat.value == 0
        assert FlatStyle.Popup.value == 1
        assert FlatStyle.Standard.value == 2
        assert FlatStyle.System.value == 3

    def test_form_window_state(self):
        assert FormWindowState.Normal.value == 0
        assert FormWindowState.Minimized.value == 1
        assert FormWindowState.Maximized.value == 2

    def test_orientation(self):
        assert Orientation.Horizontal.value == 0
        assert Orientation.Vertical.value == 1

    def test_message_box_buttons(self):
        assert MessageBoxButtons.OK.value == 0
        assert MessageBoxButtons.YesNo.value == 4

    def test_message_box_icon(self):
        assert MessageBoxIcon.Error.value == 16
        assert MessageBoxIcon.Information.value == 64

    def test_check_state(self):
        assert CheckState.Unchecked == 0
        assert CheckState.Checked == 1
        assert CheckState.Indeterminate == 2

    def test_auto_size_mode(self):
        assert AutoSizeMode.GrowAndShrink.value == 0
        assert AutoSizeMode.GrowOnly.value == 1

    def test_border_style(self):
        assert BorderStyle.None_.value == 0
        assert BorderStyle.FixedSingle.value == 1
        assert BorderStyle.Fixed3D.value == 2
