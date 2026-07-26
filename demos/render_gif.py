#!/usr/bin/env python3
"""Render c4rlib demos to animated GIFs — no external tools.

vhs (see the .tape files) produces nicer captures on Linux and macOS, but it
needs ttyd plus a headless Chromium and does not work reliably on Windows. This
renderer needs only Pillow, which c4rlib already depends on, so the GIFs can be
regenerated anywhere — including in CI.

How it works:

1. A small terminal emulator (`Screen`) consumes the escape sequences c4rlib
   actually emits: SGR colour and attributes, cursor positioning and movement,
   erase-display and erase-line.
2. `sys.stdout` is redirected into it, and `time.sleep` is patched. The library
   writes a frame and then sleeps — so every sleep is a frame boundary, and its
   duration is that frame's delay. Frames come from the animation itself rather
   than from a sampling clock, so nothing is missed or duplicated.
3. Each snapshot is drawn with a monospace font and the frames are written as a
   GIF.

Usage:
    python demos/render_gif.py            # every demo
    python demos/render_gif.py matrix     # just one
"""
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from PIL import Image, ImageDraw, ImageFont            # noqa: E402

COLS, ROWS = 100, 28
MAX_FRAMES = 240                      # keeps GIFs under a few MB
DEFAULT_FG = (205, 214, 244)          # Catppuccin Mocha text
BACKGROUND = (30, 30, 46)             # Catppuccin Mocha base

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\consola.ttf",
    r"C:\Windows\Fonts\lucon.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Menlo.ttc",
    "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
]

# Latin monospace fonts have no katakana, and matrix_rain is full of it — those
# cells would render as tofu without a fallback.
CJK_FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msgothic.ttc",
    r"C:\Windows\Fonts\YuGothR.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
]

# The 16 base ANSI colours, Catppuccin Mocha flavoured.
BASE16 = [
    (69, 71, 90),    (243, 139, 168), (166, 227, 161), (249, 226, 175),
    (137, 180, 250), (245, 194, 231), (148, 226, 213), (186, 194, 222),
    (88, 91, 112),   (243, 139, 168), (166, 227, 161), (249, 226, 175),
    (137, 180, 250), (245, 194, 231), (148, 226, 213), (166, 173, 200),
]

CSI = re.compile(r"\033\[([0-9;?]*)([A-Za-z])")


def xterm256(n):
    """Colour n of the xterm-256 palette as RGB."""
    if n < 16:
        return BASE16[n]
    if n < 232:
        n -= 16
        levels = (0, 95, 135, 175, 215, 255)
        return levels[n // 36], levels[(n // 6) % 6], levels[n % 6]
    grey = 8 + (n - 232) * 10
    return grey, grey, grey


class Cell:
    __slots__ = ("ch", "fg", "bg", "bold")

    def __init__(self, ch=" ", fg=None, bg=None, bold=False):
        self.ch, self.fg, self.bg, self.bold = ch, fg, bg, bold


class Screen:
    """Just enough terminal to render what c4rlib writes."""

    def __init__(self, cols=COLS, rows=ROWS):
        self.cols, self.rows = cols, rows
        self.reset()

    def reset(self):
        self.grid = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]
        self.x = self.y = 0
        self.fg = self.bg = None
        self.bold = False
        self.saved = (0, 0)

    # ── Writing ──────────────────────────────────────────────────────────────

    def write(self, text):
        i = 0
        while i < len(text):
            ch = text[i]
            if ch == "\033":
                match = CSI.match(text, i)
                if match:
                    self._csi(match.group(1), match.group(2))
                    i = match.end()
                    continue
                # OSC / charset / anything else: skip to a plausible end.
                i += 2
                continue
            if ch == "\n":
                self.y += 1
                self.x = 0
                if self.y >= self.rows:
                    self._scroll()
            elif ch == "\r":
                self.x = 0
            elif ch == "\b":
                self.x = max(0, self.x - 1)
            elif ch == "\t":
                self.x = min(self.cols - 1, (self.x // 8 + 1) * 8)
            elif ch == "\a":
                pass
            else:
                self._put(ch)
            i += 1

    def _put(self, ch):
        import unicodedata

        if unicodedata.combining(ch):
            return                                  # marks ride on the previous cell
        width = 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
        if self.x + width > self.cols:
            self.x = 0
            self.y += 1
            if self.y >= self.rows:
                self._scroll()
        if 0 <= self.y < self.rows:
            self.grid[self.y][self.x] = Cell(ch, self.fg, self.bg, self.bold)
            if width == 2 and self.x + 1 < self.cols:
                # Continuation cell: keeps the grid aligned with the terminal,
                # which advances two columns for a wide glyph.
                self.grid[self.y][self.x + 1] = Cell("", self.fg, self.bg, self.bold)
        self.x += width

    def _scroll(self):
        self.grid.pop(0)
        self.grid.append([Cell() for _ in range(self.cols)])
        self.y = self.rows - 1

    # ── Escape handling ──────────────────────────────────────────────────────

    def _csi(self, params, final):
        if params.startswith("?"):
            return                                  # cursor visibility etc.
        nums = [int(p) for p in params.split(";") if p.isdigit()]

        if final == "m":
            self._sgr(nums or [0])
        elif final in "Hf":
            self.y = max(0, (nums[0] if nums else 1) - 1)
            self.x = max(0, (nums[1] if len(nums) > 1 else 1) - 1)
            self.y = min(self.y, self.rows - 1)
            self.x = min(self.x, self.cols - 1)
        elif final == "A":
            self.y = max(0, self.y - (nums[0] if nums else 1))
        elif final == "B":
            self.y = min(self.rows - 1, self.y + (nums[0] if nums else 1))
        elif final == "C":
            self.x = min(self.cols - 1, self.x + (nums[0] if nums else 1))
        elif final == "D":
            self.x = max(0, self.x - (nums[0] if nums else 1))
        elif final == "G":
            self.x = max(0, (nums[0] if nums else 1) - 1)
        elif final == "J":
            self._erase_display(nums[0] if nums else 0)
        elif final == "K":
            self._erase_line(nums[0] if nums else 0)
        elif final == "s":
            self.saved = (self.x, self.y)
        elif final == "u":
            self.x, self.y = self.saved

    def _erase_display(self, mode):
        blank = lambda: [Cell() for _ in range(self.cols)]      # noqa: E731
        if mode == 2:
            self.grid = [blank() for _ in range(self.rows)]
            self.x = self.y = 0
        elif mode == 0:
            self._erase_line(0)
            for row in range(self.y + 1, self.rows):
                self.grid[row] = blank()
        elif mode == 1:
            for row in range(0, self.y):
                self.grid[row] = blank()
            self._erase_line(1)

    def _erase_line(self, mode):
        if not (0 <= self.y < self.rows):
            return
        row = self.grid[self.y]
        span = range(self.x, self.cols) if mode == 0 else \
               range(0, self.x + 1) if mode == 1 else range(0, self.cols)
        for col in span:
            row[col] = Cell()

    def _sgr(self, nums):
        i = 0
        while i < len(nums):
            n = nums[i]
            if n == 0:
                self.fg = self.bg = None
                self.bold = False
            elif n == 1:
                self.bold = True
            elif n == 22:
                self.bold = False
            elif n == 7:
                self.fg, self.bg = self.bg or BACKGROUND, self.fg or DEFAULT_FG
            elif 30 <= n <= 37:
                self.fg = BASE16[n - 30]
            elif 90 <= n <= 97:
                self.fg = BASE16[n - 90 + 8]
            elif 40 <= n <= 47:
                self.bg = BASE16[n - 40]
            elif 100 <= n <= 107:
                self.bg = BASE16[n - 100 + 8]
            elif n == 39:
                self.fg = None
            elif n == 49:
                self.bg = None
            elif n in (38, 48) and i + 1 < len(nums):
                mode = nums[i + 1]
                if mode == 2 and i + 4 < len(nums):
                    colour = (nums[i + 2], nums[i + 3], nums[i + 4])
                    i += 4
                elif mode == 5 and i + 2 < len(nums):
                    colour = xterm256(nums[i + 2])
                    i += 2
                else:
                    i += 1
                    colour = None
                if colour:
                    if n == 38:
                        self.fg = colour
                    else:
                        self.bg = colour
            i += 1

    def snapshot(self):
        """A copy of the visible grid, cheap enough to keep hundreds of."""
        return [[Cell(c.ch, c.fg, c.bg, c.bold) for c in row] for row in self.grid]


class Recorder:
    """Redirects stdout into a Screen and records a frame per sleep."""

    def __init__(self, screen, max_frames=MAX_FRAMES):
        self.screen = screen
        self.frames = []          # (snapshot, delay_ms)
        self.max_frames = max_frames
        self.dropped = 0

    # stdout interface
    def write(self, text):
        self.screen.write(text)
        return len(text)

    def flush(self):
        pass

    def isatty(self):
        return True               # so the library keeps emitting colour

    def capture(self, delay):
        """Called in place of time.sleep."""
        if len(self.frames) >= self.max_frames:
            self.dropped += 1
            return
        ms = max(20, int(delay * 1000))
        self.frames.append((self.screen.snapshot(), ms))

    def hold(self, ms):
        """Freeze the last frame for a moment — used at the end of a demo."""
        if self.frames:
            self.frames.append((self.screen.snapshot(), ms))


def load_font(size, candidates=FONT_CANDIDATES, required=True):
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    if required:
        print("  ! no monospace TTF found, falling back to the bitmap default")
        return ImageFont.load_default()
    return None


def needs_cjk(ch):
    """True for the ranges a Latin monospace font will not cover."""
    code = ord(ch)
    return (0x2E80 <= code <= 0x9FFF or        # CJK radicals through unified
            0x3040 <= code <= 0x30FF or        # hiragana + katakana
            0xAC00 <= code <= 0xD7AF or        # hangul
            0xFF00 <= code <= 0xFFEF)          # fullwidth forms


def used_extent(frames):
    """Largest row and column with content in any frame, so GIFs aren't padded
    with a screenful of empty terminal."""
    max_row = max_col = 0
    for grid, _ in frames:
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell.ch != " " or cell.bg:
                    max_row = max(max_row, y)
                    max_col = max(max_col, x)
    return max_row + 1, max_col + 1


def render_frame(grid, font, cell_w, cell_h, rows, cols, cjk_font=None):
    img  = Image.new("RGB", (cols * cell_w, rows * cell_h), BACKGROUND)
    draw = ImageDraw.Draw(img)
    for y, row in enumerate(grid[:rows]):
        # Background runs first, so glyphs are never clipped by the next cell.
        for x, cell in enumerate(row[:cols]):
            if cell.bg:
                draw.rectangle([x * cell_w, y * cell_h,
                                (x + 1) * cell_w - 1, (y + 1) * cell_h - 1],
                               fill=cell.bg)
        for x, cell in enumerate(row[:cols]):
            if cell.ch and cell.ch != " ":
                glyph_font = cjk_font if (cjk_font and needs_cjk(cell.ch)) else font
                draw.text((x * cell_w, y * cell_h), cell.ch,
                          font=glyph_font, fill=cell.fg or DEFAULT_FG)
    return img


def write_gif(frames, path, font_size=16, colors=64):
    if not frames:
        raise RuntimeError("no frames captured")
    font     = load_font(font_size)
    cjk_font = load_font(font_size, CJK_FONT_CANDIDATES, required=False)

    # The *advance* width, not the ink extent — otherwise box-drawing
    # characters leave gaps and every border renders dashed.
    try:
        cell_w = round(font.getlength("M"))
        ascent, descent = font.getmetrics()
        cell_h = ascent + descent
    except AttributeError:
        cell_w, cell_h = 8, int(font_size * 1.35)
    cell_w = max(1, cell_w)

    rows, cols = used_extent(frames)
    rows = max(rows, 3)
    cols = max(cols, 20)

    images    = [render_frame(g, font, cell_w, cell_h, rows, cols, cjk_font)
                 for g, _ in frames]
    durations = [d for _, d in frames]

    # Quantise to a shared palette. Terminal output uses few distinct colours,
    # so this is nearly lossless and cuts file size by an order of magnitude.
    # The palette must be sampled across the whole animation: derived from the
    # first frame alone, a demo that starts on an empty screen yields a
    # one-colour palette and every later frame collapses to the background.
    step   = max(1, len(images) // 12)
    sample = images[::step][:12]
    strip  = Image.new("RGB", (images[0].width, images[0].height * len(sample)))
    for i, im in enumerate(sample):
        strip.paste(im, (0, i * images[0].height))
    palette = strip.quantize(colors=colors, method=Image.Quantize.MAXCOVERAGE)
    images  = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in images]

    path.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(
        path, save_all=True, append_images=images[1:],
        duration=durations, loop=0, optimize=True,
        disposal=2,
    )
    size_kb = path.stat().st_size / 1024
    print(f"  -> {path.relative_to(ROOT)}  {len(images)} frames, "
          f"{images[0].width}x{images[0].height}, {size_kb:.0f} KB")
    if size_kb > 4096:
        print(f"  ! {path.name} is over 4 MB — lower max_frames or font_size")


def record(demo_fn, modules, max_frames=MAX_FRAMES):
    """Run demo_fn with stdout captured, on a virtual clock.

    `time.sleep` records a frame and advances a virtual clock instead of
    blocking; `time.time` reads that clock. Animations driven by a `duration`
    therefore advance exactly as they would in real time, but the recording
    finishes as fast as the CPU allows and is deterministic. Without the clock,
    those loops spin at full speed and produce tens of thousands of identical
    frames.
    """
    from c4rlib import Terminal

    screen   = Screen()
    recorder = Recorder(screen, max_frames)
    Terminal.enable_colors(True)

    os.environ["COLUMNS"], os.environ["LINES"] = str(COLS), str(ROWS)
    real_stdout = sys.stdout
    real_sleep, real_time, real_monotonic = time.sleep, time.time, time.monotonic
    clock = [real_time()]

    def fake_sleep(seconds):
        clock[0] += max(0.0, seconds)
        recorder.capture(seconds)

    def fake_time():
        return clock[0]

    try:
        sys.stdout = recorder
        time.sleep, time.time, time.monotonic = fake_sleep, fake_time, fake_time
        demo_fn()
    finally:
        time.sleep, time.time, time.monotonic = real_sleep, real_time, real_monotonic
        sys.stdout = real_stdout
        Terminal.enable_colors(None)

    recorder.hold(1200)
    if recorder.dropped:
        print(f"  ! capped at {max_frames} frames ({recorder.dropped} dropped) "
              f"— the demo is longer than the GIF shows")
    return recorder.frames


# ── The demos ─────────────────────────────────────────────────────────────────

def demo_gradients():
    from c4rlib import Ascii, Banner, Box, Figlet, Gradient

    print()
    print(Figlet.gradient("c4rlib", font="slant", start=(0, 200, 255), end=(200, 0, 255)))
    time.sleep(0.7)
    print("  " + Gradient.fire("fire") + "   " + Gradient.ice("ice") +
          "   " + Gradient.toxic("toxic") + "   " + Gradient.galaxy("galaxy") +
          "   " + Gradient.aurora("aurora"))
    time.sleep(0.7)
    print()
    print(Box.neon("64 gradient presets  ·  12 box styles"))
    time.sleep(0.7)
    print(Ascii.divider("zigzag", width=70, color="#f5c2e7"))
    time.sleep(0.7)
    print(Banner.gradient_title("SHOWTIME"))
    time.sleep(0.9)


def demo_table():
    from c4rlib import Logger, Table

    print()
    table = Table(headers=["service", "status", "latency"], title="Health")
    # No CJK here: the fonts available to this renderer have no such glyphs, so
    # they would show as tofu. Wide-character alignment is covered by
    # tests/test_terminal.py instead.
    table.add_rows([["api", "ok", "12ms"],
                    ["worker", "ok", "31ms"],
                    ["cache", "degraded", "204ms"],
                    ["queue", "ok", "8ms"]])
    print(table.render())
    time.sleep(1.0)
    Logger.success("DEPLOY", "all services reachable")
    time.sleep(0.5)
    Logger.warning("CACHE", "latency above threshold")
    time.sleep(0.5)
    Logger.error("RETRY", "scheduled in 30s")
    time.sleep(0.9)


def demo_matrix():
    from c4rlib import Animations

    Animations.matrix_rain(duration=4.0, color="#00ff41", fps=18)


def demo_effects():
    from c4rlib import Effect

    print()
    Effect.typewriter("  Every effect is one call.", delay=0.045, color="#89b4fa")
    time.sleep(0.4)
    Effect.scramble("  SCRAMBLE", duration=1.0, color="#a6e3a1")
    time.sleep(0.3)
    Effect.wave("  ~ WAVE ~", duration=1.4, color="#89dceb")
    time.sleep(0.3)
    Effect.glitch("  GLITCH", duration=1.0, intensity=3, color="#f38ba8")
    time.sleep(0.6)


def demo_sprites():
    from c4rlib import Sprite

    Sprite.preset("rocket", color="#f9e2af").move(from_x=2, to_x=80, y=6,
                                                  duration=1.8, bob=True)
    Sprite.preset("ghost", color="#cba6f7").move(from_x=80, to_x=2, y=14,
                                                 duration=1.8, bob=True)


# name: (function, modules whose time.sleep to patch, font size, max frames, palette)
DEMOS = {
    "gradients": (demo_gradients, ["ascii", "banners", "colors"], 18,  60, 64),
    "table":     (demo_table,     ["console", "logger"],          18,  60, 32),
    "matrix":    (demo_matrix,    ["animations"],                 13, 100, 32),
    "effects":   (demo_effects,   ["animations"],                 18, 120, 32),
    "sprites":   (demo_sprites,   ["ascii"],                      14, 120, 32),
}


def main():
    wanted = sys.argv[1:] or list(DEMOS)
    unknown = [name for name in wanted if name not in DEMOS]
    if unknown:
        sys.exit(f"unknown demo(s): {', '.join(unknown)}\navailable: {', '.join(DEMOS)}")

    for name in wanted:
        demo_fn, modules, font_size, max_frames, colors = DEMOS[name]
        print(f"recording {name}...")
        frames = record(demo_fn, modules, max_frames)
        write_gif(frames, ROOT / "assets" / f"{name}.gif", font_size, colors)


if __name__ == "__main__":
    main()
