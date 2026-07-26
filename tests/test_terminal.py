"""Terminal capability detection and the colour gate.

The whole point of this module is that `python app.py > log.txt` must not end up
full of escape codes, so these tests exercise the gate from both directions.
"""
import pytest

from c4rlib import Banner, Box, ColorUtils, Gradient, Table, Terminal


@pytest.fixture(autouse=True)
def restore_auto_detection():
    """Every test starts and ends with detection back on automatic."""
    Terminal.enable_colors(None)
    yield
    Terminal.enable_colors(None)


# ── The switch ────────────────────────────────────────────────────────────────

def test_override_forces_colour_on_and_off():
    Terminal.enable_colors(True)
    assert Terminal.colors_enabled() is True
    assert Terminal.reset() == "\033[0m"

    Terminal.enable_colors(False)
    assert Terminal.colors_enabled() is False
    assert Terminal.reset() == ""

    Terminal.enable_colors(None)
    assert Terminal.colors_enabled() == Terminal.supports_color()


def test_disable_colors_shortcut():
    Terminal.disable_colors()
    assert Terminal.colors_enabled() is False


def test_no_color_env_disables_even_when_forced(monkeypatch):
    """NO_COLOR wins over FORCE_COLOR — https://no-color.org."""
    monkeypatch.setenv("NO_COLOR", "")
    monkeypatch.setenv("FORCE_COLOR", "1")
    assert Terminal.supports_color() is False


def test_force_color_enables_when_not_a_tty(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("FORCE_COLOR", "1")
    monkeypatch.setattr(Terminal, "is_tty", staticmethod(lambda stream=None: False))
    assert Terminal.supports_color() is True


def test_force_color_zero_does_not_enable(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("FORCE_COLOR", "0")
    monkeypatch.setattr(Terminal, "is_tty", staticmethod(lambda stream=None: False))
    assert Terminal.supports_color() is False


def test_term_dumb_disables(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    monkeypatch.setenv("TERM", "dumb")
    assert Terminal.supports_color() is False


def test_non_tty_disables(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")
    monkeypatch.setattr(Terminal, "is_tty", staticmethod(lambda stream=None: False))
    assert Terminal.supports_color() is False


# ── Depth and downgrading ─────────────────────────────────────────────────────

def test_depth_is_none_when_colour_is_off():
    Terminal.enable_colors(False)
    assert Terminal.color_depth() == "none"
    assert Terminal.fg(255, 0, 0) == ""
    assert Terminal.bg(255, 0, 0) == ""
    assert Terminal.sgr("1") == ""


def test_truecolor_emits_24bit_sequences(monkeypatch):
    Terminal.enable_colors(True)
    monkeypatch.setenv("COLORTERM", "truecolor")
    assert Terminal.color_depth() == "truecolor"
    assert Terminal.fg(1, 2, 3) == "\033[38;2;1;2;3m"
    assert Terminal.bg(1, 2, 3) == "\033[48;2;1;2;3m"


def test_256_depth_downgrades(monkeypatch):
    Terminal.enable_colors(True)
    monkeypatch.delenv("COLORTERM", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")
    assert Terminal.color_depth() == "256"
    assert Terminal.fg(255, 0, 0) == "\033[38;5;196m"        # cube corner
    assert Terminal.fg(0, 0, 0) == "\033[38;5;16m"
    assert Terminal.fg(255, 255, 255) == "\033[38;5;231m"
    assert Terminal.fg(128, 128, 128).startswith("\033[38;5;2")   # grey ramp


def test_16_colour_downgrade_picks_nearest_base(monkeypatch):
    from c4rlib.terminal import _to_16

    assert _to_16(255, 0, 0) == 91          # bright red
    assert _to_16(0, 0, 0) == 30            # black
    assert _to_16(255, 255, 255) == 97      # bright white
    assert 30 <= _to_16(10, 90, 10) <= 97


def test_256_mapping_is_in_range():
    from c4rlib.terminal import _to_256

    for r in (0, 1, 127, 128, 254, 255):
        for g in (0, 128, 255):
            for b in (0, 128, 255):
                assert 16 <= _to_256(r, g, b) <= 255


# ── Nothing leaks when colour is off ──────────────────────────────────────────

RENDERERS = [
    lambda: Box.double("payload"),
    lambda: Box.neon("payload"),
    lambda: Box.gradient_box("payload"),
    lambda: Box.titled("Title", ["one", "two"]),
    lambda: Banner.title("payload"),
    lambda: Banner.gradient_title("payload"),
    lambda: Banner.section("payload"),
    lambda: Gradient.fire("payload"),
    lambda: Gradient.apply("payload", (0, 0, 0), (255, 255, 255)),
    lambda: Gradient.multicolor("payload", [(255, 0, 0), (0, 0, 255)]),
    lambda: Gradient.bg_apply("payload", (0, 0, 0), (255, 255, 255)),
    lambda: ColorUtils.paint("payload", "#00ccff"),
    lambda: ColorUtils.bold("payload"),
    lambda: ColorUtils.style("payload", "#00ccff", bold=True, underline=True),
    lambda: ColorUtils.rainbow("payload"),
    lambda: ColorUtils.random_color("payload"),
    lambda: ColorUtils.bg_paint("payload", "#ffffff", "#000000"),
]


@pytest.mark.parametrize("render", RENDERERS, ids=range(len(RENDERERS)))
def test_no_escapes_at_all_when_colour_is_off(render):
    Terminal.enable_colors(False)
    out = render()
    assert "\033" not in out, f"escape sequence leaked: {out!r}"


def test_table_render_is_escape_free_when_colour_is_off():
    Terminal.enable_colors(False)
    table = Table(headers=["id", "name"], title="Users")
    table.add_rows([[1, "c4r"], [2, "someone"]])
    rendered = table.render()
    assert "\033" not in rendered
    assert "c4r" in rendered and "Users" in rendered


def test_colour_returns_when_switched_back_on():
    Terminal.enable_colors(False)
    assert "\033" not in Gradient.fire("payload")
    Terminal.enable_colors(True)
    assert "\033" in Gradient.fire("payload")


# ── Width measurement ─────────────────────────────────────────────────────────

def test_display_width_counts_wide_characters_as_two():
    assert Terminal.display_width("abc") == 3
    assert Terminal.display_width("日本語") == 6
    assert Terminal.display_width("a日b") == 4


def test_display_width_ignores_combining_marks_and_escapes():
    assert Terminal.display_width("é") == 1
    assert Terminal.display_width("\033[38;2;1;2;3mabc\033[0m") == 3


def test_pad_display_aligns_by_columns():
    assert Terminal.pad_display("ab", 5) == "ab   "
    assert Terminal.pad_display("ab", 5, "right") == "   ab"
    assert Terminal.pad_display("ab", 6, "center", "-") == "--ab--"
    assert Terminal.pad_display("日本", 6) == "日本  "        # 4 columns + 2
    assert Terminal.pad_display("toolong", 3) == "toolong"


def test_strip_ansi_removes_more_than_colour():
    assert Terminal.strip_ansi("\033[2J\033[10;5H\033[38;2;1;2;3mx\033[0m") == "x"


# ── Table alignment with wide characters ──────────────────────────────────────

def test_table_borders_stay_aligned_with_cjk_and_emoji():
    Terminal.enable_colors(False)
    table = Table(headers=["name", "n"])
    table.add_rows([["ascii", 1], ["日本語テキスト", 2], ["mixed 日本", 3]])
    widths = {Terminal.display_width(line) for line in table.render().splitlines()}
    assert len(widths) == 1, f"ragged borders across rows: {widths}"


def test_table_title_stays_aligned_with_wide_characters():
    Terminal.enable_colors(False)
    table = Table(headers=["col"], title="日本語")
    table.add_row(["value"])
    widths = {Terminal.display_width(line) for line in table.render().splitlines()}
    assert len(widths) == 1, f"ragged borders with a wide title: {widths}"


# ── Diagnostics ───────────────────────────────────────────────────────────────

def test_info_reports_the_state_it_decided():
    Terminal.enable_colors(False)
    info = Terminal.info()
    assert info["colors_enabled"] is False
    assert info["color_depth"] == "none"
    assert info["override"] is False
    assert len(info["size"]) == 2


def test_size_helpers_return_positive_numbers():
    assert Terminal.width() > 0
    assert Terminal.height() > 0
    cols, rows = Terminal.size()
    assert cols > 0 and rows > 0
