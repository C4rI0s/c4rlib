"""Terminal capability detection — the gate every escape sequence passes through.

Without this, a library whose entire product is ANSI writes raw escape codes into
`app.py > log.txt`, into CI logs, and into `| grep`. Colour is emitted only when
something is there to render it, and at the depth that something supports.

Detection order (first match wins):

1. An explicit override from `Terminal.enable_colors(True/False)`.
2. `NO_COLOR` present — https://no-color.org. Any value, including empty, means
   "do not emit colour".
3. `FORCE_COLOR` present and not `0` — colour even when piped. Useful in CI.
4. `TERM=dumb` — no capabilities at all.
5. Whether stdout is a terminal.

Depth is then read from `COLORTERM` / `TERM` / platform, and truecolor sequences
are downgraded to 256-colour or the 16 base colours when that is all the terminal
can render.
"""
import os
import shutil
import sys

_TRUECOLOR = "truecolor"
_256       = "256"
_16        = "16"
_NONE      = "none"

# None = follow detection; True/False = explicit override.
_OVERRIDE = None

# The 16 base ANSI colours, in palette order, as RGB.
_BASE16 = [
    (0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0),
    (0, 0, 128), (128, 0, 128), (0, 128, 128), (192, 192, 192),
    (128, 128, 128), (255, 0, 0), (0, 255, 0), (255, 255, 0),
    (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255),
]


def _windows_enable_vt() -> bool:
    """Turn on ANSI processing for the current console. True if it is available.

    Windows 10 1511+ supports VT sequences but not by default in every host.
    Returns False on legacy consoles, where colour has to be switched off.
    """
    if os.name != "nt":
        return True
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle   = kernel32.GetStdHandle(-11)          # STD_OUTPUT_HANDLE
        mode     = ctypes.c_ulong()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            # Not a console at all (redirected). VT support is irrelevant here;
            # the isatty check decides.
            return True
        return bool(
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)  # VT_PROCESSING
            or mode.value & 0x0004
        )
    except Exception:
        return False


class Terminal:
    """Capability detection and the central colour switch."""

    # ── Detection ────────────────────────────────────────────────────────────

    @staticmethod
    def is_tty(stream=None) -> bool:
        stream = stream or sys.stdout
        try:
            return bool(stream.isatty())
        except Exception:
            return False

    @staticmethod
    def color_depth() -> str:
        """One of ``truecolor``, ``256``, ``16`` or ``none``."""
        if not Terminal.colors_enabled():
            return _NONE
        if os.environ.get("COLORTERM", "").lower() in ("truecolor", "24bit"):
            return _TRUECOLOR
        term = os.environ.get("TERM", "").lower()
        if "256" in term:
            return _256
        if term in ("dumb", ""):
            # No TERM on Windows Terminal / VS Code is normal, and both do
            # truecolor. Elsewhere an empty TERM means assume very little.
            if os.name == "nt" or os.environ.get("WT_SESSION") or \
               os.environ.get("TERM_PROGRAM"):
                return _TRUECOLOR
            return _16 if term else _TRUECOLOR
        if term.startswith(("xterm", "screen", "tmux", "rxvt", "alacritty",
                            "kitty", "wezterm", "vte", "konsole", "linux")):
            return _TRUECOLOR
        return _256

    @staticmethod
    def supports_color() -> bool:
        """Detection only — ignores any explicit override."""
        if "NO_COLOR" in os.environ:
            return False
        force = os.environ.get("FORCE_COLOR")
        if force is not None and force != "0":
            return True
        if os.environ.get("TERM", "").lower() == "dumb":
            return False
        if not Terminal.is_tty():
            return False
        return _windows_enable_vt()

    # ── The switch ───────────────────────────────────────────────────────────

    @staticmethod
    def colors_enabled() -> bool:
        return Terminal.supports_color() if _OVERRIDE is None else _OVERRIDE

    @staticmethod
    def enable_colors(enabled=True) -> None:
        """Force colour on (``True``), off (``False``), or back to auto (``None``)."""
        global _OVERRIDE
        _OVERRIDE = None if enabled is None else bool(enabled)

    @staticmethod
    def disable_colors() -> None:
        Terminal.enable_colors(False)

    # ── Emission ─────────────────────────────────────────────────────────────

    @staticmethod
    def fg(r: int, g: int, b: int) -> str:
        """Foreground escape at the deepest colour this terminal can render."""
        depth = Terminal.color_depth()
        if depth == _NONE:
            return ""
        if depth == _TRUECOLOR:
            return f"\033[38;2;{r};{g};{b}m"
        if depth == _256:
            return f"\033[38;5;{_to_256(r, g, b)}m"
        return f"\033[{_to_16(r, g, b)}m"

    @staticmethod
    def bg(r: int, g: int, b: int) -> str:
        depth = Terminal.color_depth()
        if depth == _NONE:
            return ""
        if depth == _TRUECOLOR:
            return f"\033[48;2;{r};{g};{b}m"
        if depth == _256:
            return f"\033[48;5;{_to_256(r, g, b)}m"
        return f"\033[{_to_16(r, g, b) + 10}m"

    @staticmethod
    def sgr(code: str) -> str:
        """An attribute sequence (bold, italic, reset…), or "" when disabled."""
        return "" if not Terminal.colors_enabled() else f"\033[{code}m"

    @staticmethod
    def reset() -> str:
        return Terminal.sgr("0")

    # ── Utilities ────────────────────────────────────────────────────────────

    @staticmethod
    def strip_ansi(text: str) -> str:
        """Remove every escape sequence — SGR, cursor moves, erases, the lot."""
        import re

        return re.sub(r"\033(?:\[[0-9;?]*[A-Za-z]|\][^\007\033]*(?:\007|\033\\)|[()][A-Za-z0-9])",
                      "", text)

    @staticmethod
    def width(default: int = 80) -> int:
        return shutil.get_terminal_size((default, 24)).columns

    @staticmethod
    def height(default: int = 24) -> int:
        return shutil.get_terminal_size((80, default)).lines

    @staticmethod
    def size(default: tuple = (80, 24)) -> tuple:
        size = shutil.get_terminal_size(default)
        return size.columns, size.lines

    @staticmethod
    def display_width(text: str) -> int:
        """Columns `text` occupies, counting CJK and emoji as two.

        `len()` is wrong for anything a table has to align: "日本語" is three
        code points but six columns wide, and combining marks are zero.
        """
        import unicodedata

        width = 0
        for ch in Terminal.strip_ansi(text):
            if unicodedata.combining(ch):
                continue
            width += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
        return width

    @staticmethod
    def pad_display(text: str, width: int, align: str = "left",
                    fill: str = " ") -> str:
        """Pad to `width` *display* columns rather than character count."""
        deficit = max(0, width - Terminal.display_width(text))
        if align == "right":
            return fill * deficit + text
        if align == "center":
            left = deficit // 2
            return fill * left + text + fill * (deficit - left)
        return text + fill * deficit

    @staticmethod
    def info() -> dict:
        """Everything detection concluded — useful in bug reports."""
        return {
            "is_tty":         Terminal.is_tty(),
            "colors_enabled": Terminal.colors_enabled(),
            "color_depth":    Terminal.color_depth(),
            "override":       _OVERRIDE,
            "size":           Terminal.size(),
            "TERM":           os.environ.get("TERM"),
            "COLORTERM":      os.environ.get("COLORTERM"),
            "NO_COLOR":       "NO_COLOR" in os.environ,
            "FORCE_COLOR":    os.environ.get("FORCE_COLOR"),
            "platform":       sys.platform,
        }


def _to_256(r: int, g: int, b: int) -> int:
    """Map RGB onto the xterm-256 cube, using the grey ramp when it is grey."""
    if r == g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return 232 + round((r - 8) / 247 * 24)
    return 16 + 36 * round(r / 255 * 5) + 6 * round(g / 255 * 5) + round(b / 255 * 5)


def _to_16(r: int, g: int, b: int) -> int:
    """Nearest of the 16 base colours, as an SGR foreground code (30-37/90-97)."""
    best, best_distance = 0, None
    for index, (br, bg_, bb) in enumerate(_BASE16):
        distance = (r - br) ** 2 + (g - bg_) ** 2 + (b - bb) ** 2
        if best_distance is None or distance < best_distance:
            best, best_distance = index, distance
    return 30 + best if best < 8 else 90 + (best - 8)
