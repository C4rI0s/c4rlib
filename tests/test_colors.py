"""Colour maths — pure functions, fully assertable."""
import pytest

from c4rlib import ColorUtils, Gradient, GradientPresets

CASES = ["#000000", "#ffffff", "#ff0000", "#00ccff", "#7f3f1f", "#123456"]


@pytest.mark.parametrize("hex_color", CASES)
def test_hex_rgb_roundtrip(hex_color):
    r, g, b = ColorUtils.hex_to_rgb(hex_color)
    assert ColorUtils.rgb_to_hex(r, g, b) == hex_color


def test_hex_to_rgb_accepts_missing_hash():
    assert ColorUtils.hex_to_rgb("00ccff") == ColorUtils.hex_to_rgb("#00ccff")


def test_hex_to_rgb_known_values():
    assert ColorUtils.hex_to_rgb("#ff0000") == (255, 0, 0)
    assert ColorUtils.hex_to_rgb("#00ff00") == (0, 255, 0)
    assert ColorUtils.hex_to_rgb("#0000ff") == (0, 0, 255)


def test_rgb_to_hsl_ranges():
    h, s, l = ColorUtils.rgb_to_hsl(255, 0, 0)
    assert (h, s, l) == (0, 100, 50)
    for r, g, b in [(0, 0, 0), (255, 255, 255), (12, 200, 90)]:
        h, s, l = ColorUtils.rgb_to_hsl(r, g, b)
        assert 0 <= h <= 360 and 0 <= s <= 100 and 0 <= l <= 100


def test_blend_endpoints():
    assert ColorUtils.blend("#000000", "#ffffff", 0.0) == "#000000"
    assert ColorUtils.blend("#000000", "#ffffff", 1.0) == "#ffffff"


def test_blend_midpoint_is_between():
    mid = ColorUtils.hex_to_rgb(ColorUtils.blend("#000000", "#ffffff", 0.5))
    assert all(100 < c < 155 for c in mid)


def test_lighten_and_darken_move_lightness():
    base = "#3366aa"
    lighter = ColorUtils.rgb_to_hsl(*ColorUtils.hex_to_rgb(ColorUtils.lighten(base)))
    darker = ColorUtils.rgb_to_hsl(*ColorUtils.hex_to_rgb(ColorUtils.darken(base)))
    original = ColorUtils.rgb_to_hsl(*ColorUtils.hex_to_rgb(base))
    assert lighter[2] > original[2] > darker[2]


def test_lighten_and_darken_clamp_at_extremes():
    # Must not raise or produce out-of-range channels.
    assert ColorUtils.lighten("#ffffff", 0.9) == "#ffffff"
    assert ColorUtils.darken("#000000", 0.9) == "#000000"


def test_complementary_is_involutive():
    for hex_color in CASES:
        assert ColorUtils.complementary(ColorUtils.complementary(hex_color)) == hex_color


def test_palette_length_and_bounds():
    result = ColorUtils.palette("#00ccff", steps=7)
    assert len(result) == 7
    assert result[0] == "#000000"          # lightness 0
    assert result[-1] == "#ffffff"         # lightness 1
    assert all(c.startswith("#") and len(c) == 7 for c in result)


def test_triadic_returns_three_distinct_hues():
    result = ColorUtils.triadic("#ff0000")
    assert len(result) == 3
    assert result[0] == "#ff0000"
    assert len(set(result)) == 3


@pytest.mark.parametrize("text", ["", "a", "hello world", "ünïcødé"])
def test_gradient_apply_preserves_visible_characters(text):
    out = Gradient.apply(text, (0, 0, 0), (255, 255, 255))
    stripped = _strip_ansi(out)
    assert stripped == text


def test_gradient_apply_single_char_does_not_divide_by_zero():
    assert _strip_ansi(Gradient.apply("x", (0, 0, 0), (255, 255, 255))) == "x"


def test_gradient_preset_matches_apply():
    assert Gradient.preset("hello", GradientPresets.fire) == Gradient.apply(
        "hello", *GradientPresets.fire
    )


def test_all_gradient_presets_are_rgb_pairs():
    presets = [
        (name, value)
        for name, value in vars(GradientPresets).items()
        if not name.startswith("_")
    ]
    assert len(presets) > 50
    for name, value in presets:
        assert isinstance(value, tuple) and len(value) == 2, name
        for channel_triplet in value:
            assert len(channel_triplet) == 3, name
            assert all(0 <= c <= 255 for c in channel_triplet), name


def test_multicolor_handles_empty_and_single_colour():
    assert Gradient.multicolor("hello", []) == "hello"
    assert _strip_ansi(Gradient.multicolor("hello", [(255, 0, 0)])) == "hello"
    assert _strip_ansi(Gradient.multicolor("hello", [(255, 0, 0), (0, 0, 255)])) == "hello"


def _strip_ansi(text):
    import re

    return re.sub(r"\033\[[0-9;]*m", "", text)
