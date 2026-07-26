"""Renderers must be pure and must not leak ANSI state.

Two invariants that are invisible to a visual review but very visible to a
user whose prompt turns cyan forever:

1. Anything that *returns* a string writes nothing to stdout.
2. Every SGR sequence that sets a colour or attribute is eventually reset.
"""
import re

import pytest

from c4rlib import Banner, Box, ColorUtils, Gradient, Table, TextStyle

SGR = re.compile(r"\033\[([0-9;]*)m")
RESET_CODES = {"", "0", "00"}

BOX_RENDERERS = [
    Box.double, Box.rounded, Box.heavy, Box.simple, Box.dots, Box.stars,
    Box.hash_box, Box.ascii, Box.diamond, Box.arrows, Box.classic_round,
    Box.neon,
]

BANNER_RENDERERS = [
    Banner.double_line, Banner.arrow_line, Banner.heart_line, Banner.wave_line,
    Banner.star_line, Banner.dot_line, Banner.slash_line, Banner.diamond_line,
    Banner.lightning_line, Banner.fire_line, Banner.title, Banner.section,
]

GRADIENT_RENDERERS = [
    Gradient.fire, Gradient.ice, Gradient.toxic, Gradient.sunset,
    Gradient.ocean, Gradient.galaxy, Gradient.neon, Gradient.matrix,
    Gradient.lava, Gradient.candy, Gradient.aurora, Gradient.electric,
    Gradient.rose,
]

ALL_RENDERERS = BOX_RENDERERS + BANNER_RENDERERS + GRADIENT_RENDERERS


def _is_balanced(text):
    """True if the string never ends while a colour or attribute is still set."""
    open_state = False
    for match in SGR.finditer(text):
        params = match.group(1)
        if params in RESET_CODES:
            open_state = False
        else:
            open_state = True
    return not open_state


@pytest.mark.parametrize("fn", ALL_RENDERERS, ids=lambda f: f.__name__)
def test_renderer_returns_string_and_prints_nothing(fn, capsys):
    result = fn("payload")
    assert isinstance(result, str)
    captured = capsys.readouterr()
    assert captured.out == "", f"{fn.__name__} wrote to stdout"
    assert captured.err == ""


@pytest.mark.parametrize("fn", ALL_RENDERERS, ids=lambda f: f.__name__)
def test_renderer_resets_ansi_state(fn):
    assert _is_balanced(fn("payload")), f"{fn.__name__} leaves ANSI state open"


@pytest.mark.parametrize("fn", ALL_RENDERERS, ids=lambda f: f.__name__)
def test_renderer_survives_empty_input(fn):
    assert isinstance(fn(""), str)


def test_colorutils_wrappers_reset():
    for fn in (ColorUtils.bold, ColorUtils.italic, ColorUtils.underline,
               ColorUtils.strike, ColorUtils.dim, ColorUtils.rainbow,
               ColorUtils.random_color):
        out = fn("payload")
        assert _is_balanced(out), fn.__name__
    assert _is_balanced(ColorUtils.paint("payload", "#00ccff"))
    assert _is_balanced(ColorUtils.style("payload", "#00ccff", bold=True, underline=True))


def test_gradient_apply_and_multicolor_reset():
    assert _is_balanced(Gradient.apply("payload", (0, 0, 0), (255, 255, 255)))
    assert _is_balanced(Gradient.multicolor("payload", [(255, 0, 0), (0, 255, 0), (0, 0, 255)]))
    assert _is_balanced(Gradient.bg_apply("payload", (0, 0, 0), (255, 255, 255)))


def test_box_multiline_and_titled_reset():
    assert _is_balanced(Box.multiline(["one", "two", "three"]))
    assert _is_balanced(Box.titled("Title", ["one", "two"]))
    assert _is_balanced(Box.gradient_box("payload"))


def test_table_render_is_pure_and_balanced(capsys):
    table = Table(headers=["id", "name"], title="Users")
    table.add_rows([[1, "c4r"], [2, "someone else"]])
    rendered = table.render()
    assert capsys.readouterr().out == ""
    assert _is_balanced(rendered)
    assert "c4r" in rendered


def test_table_to_csv_has_no_ansi():
    table = Table(headers=["a", "b"])
    table.add_row([1, 2])
    csv = table.to_csv()
    assert not SGR.search(csv)
    assert csv == "a,b\n1,2"


def test_table_renders_without_headers_or_rows():
    assert isinstance(Table().render(), str)
    empty = Table(headers=["only", "headers"])
    assert _is_balanced(empty.render())


def test_table_pads_short_rows():
    table = Table(headers=["a", "b", "c"])
    table.add_row([1])
    rendered = table.render()
    assert _is_balanced(rendered)
    line_widths = {len(SGR.sub("", line)) for line in rendered.splitlines()}
    assert len(line_widths) == 1, f"ragged table borders: {line_widths}"


def test_textstyle_output_carries_no_ansi():
    """TextStyle is Unicode substitution, not colour — it must stay escape-free."""
    for fn in (TextStyle.fancy, TextStyle.bubble, TextStyle.small_caps,
               TextStyle.leet, TextStyle.wide, TextStyle.mirror):
        assert not SGR.search(fn("payload")), fn.__name__
