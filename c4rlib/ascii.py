import os
import sys
import time
import math
import shutil
import random
import threading
from .colors import ColorUtils, Gradient


try:
    import pyfiglet
    _HAS_FIGLET = True
except Exception:
    _HAS_FIGLET = False

try:
    from PIL import Image
    _HAS_PIL = True
except Exception:
    _HAS_PIL = False


_CHARSETS = {
    "dense":  "@%#*+=-:. ",
    "blocks": "█▓▒░ ",
    "sparse": "#+- ",
    "binary": "10 ",
    "emoji":  "🟥🟧🟨🟩🟦🟪⬛⬜",
    "ascii":  "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
}


def _hide():
    sys.stdout.write("\033[?25l"); sys.stdout.flush()

def _show():
    sys.stdout.write("\033[?25h"); sys.stdout.flush()

def _clear():
    os.system("cls" if os.name == "nt" else "clear")

def _at(x: int, y: int, text: str = "") -> None:
    sys.stdout.write(f"\033[{y};{x}H{text}")

def _termsize() -> tuple:
    s = shutil.get_terminal_size()
    return s.columns, s.lines


class Figlet:
    DEFAULT_FONT = "standard"

    @staticmethod
    def render(text: str, font: str = "standard", width: int = None) -> str:
        if not _HAS_FIGLET:
            return Ascii.banner(text, style="block")
        w = width or shutil.get_terminal_size().columns
        f = pyfiglet.Figlet(font=font, width=w)
        return f.renderText(text).rstrip("\n")

    @staticmethod
    def print(text: str, font: str = "standard", color: str = None) -> None:
        out = Figlet.render(text, font=font)
        if color:
            col = ColorUtils.hex(color)
            out = "\n".join(col + line + ColorUtils.RESET for line in out.split("\n"))
        print(out)

    @staticmethod
    def gradient(text: str, font: str = "standard",
                 start: tuple = (0, 200, 255), end: tuple = (200, 0, 255),
                 vertical: bool = False) -> str:
        out   = Figlet.render(text, font=font)
        lines = out.split("\n")
        if vertical:
            n      = max(len(lines) - 1, 1)
            result = []
            for i, line in enumerate(lines):
                t = i / n
                r = int((1 - t) * start[0] + t * end[0])
                g = int((1 - t) * start[1] + t * end[1])
                b = int((1 - t) * start[2] + t * end[2])
                result.append(f"\033[38;2;{r};{g};{b}m{line}{ColorUtils.RESET}")
            return "\n".join(result)
        return "\n".join(Gradient.apply(line, start, end) for line in lines)

    @staticmethod
    def print_gradient(text: str, font: str = "standard",
                       start: tuple = (0, 200, 255), end: tuple = (200, 0, 255),
                       vertical: bool = False) -> None:
        print(Figlet.gradient(text, font, start, end, vertical))

    @staticmethod
    def rainbow(text: str, font: str = "standard") -> str:
        out   = Figlet.render(text, font=font)
        return "\n".join(ColorUtils.rainbow(line) for line in out.split("\n"))

    @staticmethod
    def list_fonts() -> list:
        if not _HAS_FIGLET:
            return []
        return sorted(pyfiglet.FigletFont.getFonts())

    @staticmethod
    def preview_all(text: str = "Hi", limit: int = None) -> None:
        fonts = Figlet.list_fonts()
        if limit:
            fonts = fonts[:limit]
        for font in fonts:
            print(f"\n{ColorUtils.hex('#9b5de5')}═══ {font} ═══{ColorUtils.RESET}")
            try:
                Figlet.print(text, font=font)
            except Exception:
                print(f"  {ColorUtils.hex('#d00000')}[failed]{ColorUtils.RESET}")

    @staticmethod
    def boxed(text: str, font: str = "standard", color: str = "#00ccff",
              border_color: str = "#6c757d") -> str:
        out      = Figlet.render(text, font=font)
        lines    = out.split("\n")
        width    = max(len(l) for l in lines) if lines else 0
        bc       = ColorUtils.hex(border_color)
        tc       = ColorUtils.hex(color)
        reset    = ColorUtils.RESET
        top      = bc + "╔" + "═" * (width + 2) + "╗" + reset
        bot      = bc + "╚" + "═" * (width + 2) + "╝" + reset
        body     = []
        for line in lines:
            padded = line.ljust(width)
            body.append(bc + "║ " + reset + tc + padded + reset + bc + " ║" + reset)
        return "\n".join([top] + body + [bot])


class ImageAscii:
    charsets = list(_CHARSETS.keys())

    @staticmethod
    def from_file(path: str, width: int = 80, charset: str = "dense",
                  color: bool = True, invert: bool = False) -> str:
        if not _HAS_PIL:
            raise RuntimeError("Pillow not installed. Run: pip install pillow")
        img = Image.open(path).convert("RGB")
        return ImageAscii._render(img, width, charset, color, invert)

    @staticmethod
    def from_url(url: str, width: int = 80, charset: str = "dense",
                 color: bool = True, invert: bool = False) -> str:
        if not _HAS_PIL:
            raise RuntimeError("Pillow not installed. Run: pip install pillow")
        from io import BytesIO
        from urllib.request import urlopen, Request
        req  = Request(url, headers={"User-Agent": "c4rlib/3.0.0"})
        data = urlopen(req, timeout=10).read()
        img  = Image.open(BytesIO(data)).convert("RGB")
        return ImageAscii._render(img, width, charset, color, invert)

    @staticmethod
    def _render(img, width: int, charset: str, color: bool, invert: bool) -> str:
        chars = _CHARSETS.get(charset, _CHARSETS["dense"])
        if invert:
            chars = chars[::-1]
        w, h         = img.size
        aspect       = h / w * 0.55
        new_height   = max(1, int(width * aspect))
        img          = img.resize((width, new_height))
        pixels       = img.load()
        n            = len(chars) - 1
        out_lines    = []
        for y in range(new_height):
            row = []
            for x in range(width):
                r, g, b   = pixels[x, y]
                brightness = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
                idx        = int(brightness * n)
                ch         = chars[idx]
                if color:
                    row.append(f"\033[38;2;{r};{g};{b}m{ch}")
                else:
                    row.append(ch)
            if color:
                row.append(ColorUtils.RESET)
            out_lines.append("".join(row))
        return "\n".join(out_lines)

    @staticmethod
    def print(path: str, **kwargs) -> None:
        print(ImageAscii.from_file(path, **kwargs))

    @staticmethod
    def save(in_path: str, out_path: str, **kwargs) -> None:
        kwargs.setdefault("color", False)
        out = ImageAscii.from_file(in_path, **kwargs)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(out)


_SPRITE_PRESETS = {
    "ghost": [
        ["  .-.  ",
         " (o o) ",
         " | O | ",
         " '~~~' "],
        ["  .-.  ",
         " (o o) ",
         " | O | ",
         " ~'~'~ "],
    ],
    "ufo": [
        ["   _____   ",
         "  /     \\  ",
         " ( o o o ) ",
         "  '-----'  "],
        ["   _____   ",
         "  /     \\  ",
         " ( . . . ) ",
         "  '-----'  "],
    ],
    "skull": [
        [" .-----.  ",
         " | o o |  ",
         " |  ^  |  ",
         " | --- |  ",
         " '-----'  "],
    ],
    "cat": [
        [" /\\_/\\  ",
         "( o.o ) ",
         " > ^ <  "],
        [" /\\_/\\  ",
         "( -.- ) ",
         " > ^ <  "],
    ],
    "dog": [
        [" __      ",
         "(o o)____",
         " (___)   ",
         "  \" \"   "],
    ],
    "fish": [
        ["       ><((((°> "],
        ["    ><((((°>    "],
        [" ><((((°>       "],
    ],
    "rocket": [
        ["    /\\    ",
         "   /  \\   ",
         "  | || |  ",
         "  | || |  ",
         "  |_||_|  ",
         "  /_||_\\  ",
         "   ^^^^   "],
        ["    /\\    ",
         "   /  \\   ",
         "  | || |  ",
         "  | || |  ",
         "  |_||_|  ",
         "  /_||_\\  ",
         "   ****   "],
    ],
    "dragon": [
        [" ___====-_  _-====___       ",
         "  `--^\\\\\\__/____\\__//^--`   ",
         "      `--..__..--`         "],
    ],
    "car": [
        ["    ___n_n__     ",
         "   /        \\    ",
         "  |  o    o  |   ",
         "  |__O____O__|   ",
         "     0    0      "],
    ],
    "ball": [
        ["  ___  ",
         " /   \\ ",
         "|     |",
         " \\___/ "],
    ],
    "heart": [
        [" ♥♥   ♥♥ ",
         "♥♥♥♥♥♥♥♥♥",
         " ♥♥♥♥♥♥♥ ",
         "  ♥♥♥♥♥  ",
         "   ♥♥♥   ",
         "    ♥    "],
    ],
    "bird": [
        ["  \\___ ",
         "  /v v\\",
         " ( ^ ^ )",
         "  '---' "],
        ["  \\___ ",
         "  /- -\\",
         " ( ^ ^ )",
         "  '---' "],
    ],
    "spider": [
        [" /\\ /\\ ",
         "/  V  \\",
         "\\/ ^ \\/",
         "/\\/ \\/\\"],
    ],
    "robot": [
        [" [- -] ",
         " (o o) ",
         "/|=|=|\\",
         " d   b "],
        [" [o o] ",
         " (- -) ",
         "/|=|=|\\",
         " d   b "],
    ],
    "pacman": [
        [" .---. ",
         "/  __ \\",
         "|  /  /",
         "| /  / ",
         "\\ \\__ \\",
         " '----'"],
        [" .---. ",
         "/     \\",
         "|      |",
         "|      |",
         "\\      /",
         " '----'"],
    ],
}


class Sprite:
    PRESETS = list(_SPRITE_PRESETS.keys())

    def __init__(self, frames, fps: float = 8.0, loop: bool = True, color: str = None):
        self.frames = [self._normalize(f) for f in frames]
        self.fps    = fps
        self.loop   = loop
        self.color  = color
        self._idx   = 0
        self._running = False

    @staticmethod
    def _normalize(frame) -> list:
        if isinstance(frame, str):
            return frame.split("\n")
        return list(frame)

    @staticmethod
    def preset(name: str, color: str = None, fps: float = 6.0) -> "Sprite":
        if name not in _SPRITE_PRESETS:
            raise ValueError(f"Unknown sprite preset '{name}'. Available: {Sprite.PRESETS}")
        return Sprite(_SPRITE_PRESETS[name], fps=fps, color=color)

    @staticmethod
    def from_frames(frames, fps: float = 8.0, loop: bool = True, color: str = None) -> "Sprite":
        return Sprite(frames, fps=fps, loop=loop, color=color)

    @property
    def width(self) -> int:
        return max((max(len(l) for l in f) if f else 0) for f in self.frames)

    @property
    def height(self) -> int:
        return max(len(f) for f in self.frames)

    def _draw(self, x: int, y: int, frame) -> None:
        col   = ColorUtils.hex(self.color) if self.color else ""
        reset = ColorUtils.RESET if self.color else ""
        for i, line in enumerate(frame):
            _at(x, y + i, col + line + reset)

    def _erase(self, x: int, y: int, w: int, h: int) -> None:
        blank = " " * w
        for i in range(h):
            _at(x, y + i, blank)

    def play(self, duration: float = 3.0, x: int = None, y: int = None) -> None:
        cols, rows = _termsize()
        w, h       = self.width, self.height
        if x is None: x = max(1, (cols - w) // 2)
        if y is None: y = max(1, (rows - h) // 2)
        end        = time.time() + duration
        delay      = 1.0 / max(self.fps, 1)
        _hide()
        try:
            while time.time() < end:
                frame = self.frames[self._idx % len(self.frames)]
                self._draw(x, y, frame)
                sys.stdout.flush()
                time.sleep(delay)
                self._erase(x, y, w, h)
                self._idx += 1
                if not self.loop and self._idx >= len(self.frames):
                    break
        finally:
            _show()
            sys.stdout.write("\n" * (h + 1))
            sys.stdout.flush()

    def move(self, from_x: int = 1, to_x: int = None, y: int = None,
             duration: float = 3.0, bob: bool = False, color: str = None) -> None:
        cols, rows = _termsize()
        if to_x is None:
            to_x = cols - self.width - 1
        if y is None:
            y = max(2, rows // 2 - self.height // 2)
        if color:
            self.color = color
        w, h   = self.width, self.height
        steps  = max(1, int(duration * self.fps))
        dx     = (to_x - from_x) / steps
        prev_x = None
        _hide()
        try:
            for i in range(steps + 1):
                cur_x  = int(from_x + dx * i)
                offset = int(math.sin(i * 0.5) * 1) if bob else 0
                if prev_x is not None:
                    self._erase(prev_x, y + offset, w, h)
                if prev_x is not None and bob:
                    self._erase(prev_x, y, w, h)
                frame = self.frames[i % len(self.frames)]
                self._draw(cur_x, y + offset, frame)
                sys.stdout.flush()
                time.sleep(1.0 / max(self.fps, 1))
                prev_x = cur_x
            self._erase(prev_x, y, w, h)
            for off in range(-2, 3):
                self._erase(prev_x, y + off, w, h)
        finally:
            _show()
            _at(1, rows, "")
            sys.stdout.write("\n")
            sys.stdout.flush()

    def bounce(self, times: int = 3, x: int = None, color: str = None,
               height: int = 6, fps: float = 20) -> None:
        cols, rows = _termsize()
        if x is None:
            x = max(1, (cols - self.width) // 2)
        if color:
            self.color = color
        floor  = rows - self.height - 1
        ceil_  = max(1, floor - height)
        steps  = 16
        delay  = 1.0 / fps
        prev_y = None
        w, h   = self.width, self.height
        _hide()
        try:
            for _ in range(times):
                for i in range(steps):
                    t  = i / steps
                    y  = int(floor - (math.sin(t * math.pi) * (floor - ceil_)))
                    if prev_y is not None:
                        self._erase(x, prev_y, w, h)
                    frame = self.frames[i % len(self.frames)]
                    self._draw(x, y, frame)
                    sys.stdout.flush()
                    time.sleep(delay)
                    prev_y = y
            if prev_y is not None:
                self._erase(x, prev_y, w, h)
        finally:
            _show()
            _at(1, rows, "")
            sys.stdout.write("\n")
            sys.stdout.flush()

    def shake(self, duration: float = 1.0, x: int = None, y: int = None,
              intensity: int = 2) -> None:
        cols, rows = _termsize()
        if x is None: x = max(1, (cols - self.width) // 2)
        if y is None: y = max(1, (rows - self.height) // 2)
        w, h    = self.width, self.height
        end     = time.time() + duration
        delay   = 0.05
        prev    = None
        _hide()
        try:
            i = 0
            while time.time() < end:
                ox = random.randint(-intensity, intensity)
                oy = random.randint(-intensity, intensity)
                if prev is not None:
                    self._erase(prev[0], prev[1], w, h)
                frame = self.frames[i % len(self.frames)]
                self._draw(x + ox, y + oy, frame)
                sys.stdout.flush()
                time.sleep(delay)
                prev = (x + ox, y + oy)
                i   += 1
            if prev is not None:
                self._erase(prev[0], prev[1], w, h)
        finally:
            _show()
            _at(1, rows, "")
            sys.stdout.write("\n")
            sys.stdout.flush()

    def float(self, amplitude: int = 2, duration: float = 4.0,
              x: int = None, y: int = None) -> None:
        cols, rows = _termsize()
        if x is None: x = max(1, (cols - self.width) // 2)
        if y is None: y = max(1, (rows - self.height) // 2)
        end   = time.time() + duration
        delay = 0.08
        w, h  = self.width, self.height
        prev_y = None
        i = 0
        _hide()
        try:
            while time.time() < end:
                oy = int(math.sin(i * 0.3) * amplitude)
                if prev_y is not None:
                    self._erase(x, prev_y, w, h)
                frame = self.frames[i % len(self.frames)]
                self._draw(x, y + oy, frame)
                sys.stdout.flush()
                time.sleep(delay)
                prev_y = y + oy
                i += 1
            if prev_y is not None:
                self._erase(x, prev_y, w, h)
        finally:
            _show()
            _at(1, rows, "")
            sys.stdout.write("\n")
            sys.stdout.flush()

    def fade_in(self, duration: float = 0.8, x: int = None, y: int = None) -> None:
        self._fade(duration, x, y, fade_out=False)

    def fade_out(self, duration: float = 0.8, x: int = None, y: int = None) -> None:
        self._fade(duration, x, y, fade_out=True)

    def _fade(self, duration: float, x: int, y: int, fade_out: bool) -> None:
        cols, rows = _termsize()
        if x is None: x = max(1, (cols - self.width) // 2)
        if y is None: y = max(1, (rows - self.height) // 2)
        steps = 12
        delay = duration / steps
        base  = self.color or "#ffffff"
        r, g, b = ColorUtils.hex_to_rgb(base)
        _hide()
        try:
            frame = self.frames[0]
            for i in range(steps + 1):
                t = (steps - i) / steps if fade_out else i / steps
                R = int(r * t); G = int(g * t); B = int(b * t)
                col = f"\033[38;2;{R};{G};{B}m"
                for li, line in enumerate(frame):
                    _at(x, y + li, col + line + ColorUtils.RESET)
                sys.stdout.flush()
                time.sleep(delay)
            if fade_out:
                self._erase(x, y, self.width, self.height)
        finally:
            _show()
            _at(1, rows, "")
            sys.stdout.write("\n")
            sys.stdout.flush()

    @staticmethod
    def parade(names, speed: float = 20, gap: int = 8, colors: list = None) -> None:
        cols, rows = _termsize()
        sprites    = []
        for i, n in enumerate(names):
            c = (colors[i % len(colors)] if colors else None)
            sprites.append(Sprite.preset(n, color=c))
        total_w = sum(s.width + gap for s in sprites)
        y       = max(2, rows // 2 - max(s.height for s in sprites) // 2)
        delay   = 1.0 / speed
        offset  = -total_w
        _hide()
        try:
            while offset < cols:
                # erase previous frame area
                for r_ in range(y - 1, y + max(s.height for s in sprites) + 2):
                    if 1 <= r_ <= rows:
                        _at(1, r_, " " * cols)
                cur_x = offset
                for s in sprites:
                    if 1 <= cur_x <= cols - s.width:
                        frame = s.frames[(s._idx) % len(s.frames)]
                        s._draw(cur_x, y, frame)
                    s._idx += 1
                    cur_x += s.width + gap
                sys.stdout.flush()
                time.sleep(delay)
                offset += 2
        finally:
            _show()
            _at(1, rows, "")
            sys.stdout.write("\n")
            sys.stdout.flush()

    @staticmethod
    def race(names: list, length: int = 60, colors: list = None) -> str:
        random.seed()
        sprites   = []
        for i, n in enumerate(names):
            c = (colors[i % len(colors)] if colors else None)
            sprites.append(Sprite.preset(n, color=c))
        positions = [0] * len(sprites)
        speeds    = [random.uniform(0.5, 1.2) for _ in sprites]
        y_off     = 2
        _hide()
        try:
            winner = None
            while winner is None:
                for r_ in range(1, y_off + len(sprites) * (sprites[0].height + 1) + 2):
                    _at(1, r_, " " * (length + 20))
                for i, s in enumerate(sprites):
                    positions[i] += speeds[i] * random.uniform(0.5, 1.5)
                    if positions[i] >= length and winner is None:
                        winner = (names[i], i)
                    y = y_off + i * (s.height + 1)
                    _at(1, y, f"{ColorUtils.hex('#6c757d')}|{ColorUtils.RESET}")
                    _at(length + 4, y, f"{ColorUtils.hex('#ffd60a')}|🏁{ColorUtils.RESET}")
                    frame = s.frames[(s._idx) % len(s.frames)]
                    s._idx += 1
                    px = 2 + min(int(positions[i]), length)
                    s._draw(px, y, frame)
                sys.stdout.flush()
                time.sleep(0.08)
        finally:
            _show()
            _at(1, y_off + len(sprites) * (sprites[0].height + 1) + 2,
                f" {ColorUtils.hex('#ffd60a')}🏆 Winner: {winner[0]}!{ColorUtils.RESET}\n")
            sys.stdout.flush()
        return winner[0]


class Ascii:
    @staticmethod
    def banner(text: str, style: str = "block", color: str = None) -> str:
        """Pure-stdlib mini-FIGlet (fallback when pyfiglet is unavailable)."""
        font = _MINI_FONTS.get(style, _MINI_FONTS["block"])
        rows = ["" for _ in range(font["height"])]
        for ch in text.upper():
            glyph = font["glyphs"].get(ch, font["glyphs"].get(" ", ["   "] * font["height"]))
            for i, row in enumerate(glyph):
                rows[i] += row + " "
        out = "\n".join(rows)
        if color:
            out = "\n".join(ColorUtils.hex(color) + r + ColorUtils.RESET for r in rows)
        return out

    @staticmethod
    def print(text: str, style: str = "block", color: str = None) -> None:
        print(Ascii.banner(text, style, color))

    @staticmethod
    def gradient(text: str, style: str = "block",
                 start: tuple = (0, 200, 255), end: tuple = (200, 0, 255)) -> str:
        out  = Ascii.banner(text, style)
        rows = out.split("\n")
        return "\n".join(Gradient.apply(r, start, end) for r in rows)

    @staticmethod
    def divider(style: str = "zigzag", width: int = None, color: str = None) -> str:
        w = width or shutil.get_terminal_size().columns
        styles = {
            "zigzag":   "╱╲" * (w // 2),
            "wave":     "~" * w,
            "dots":     "·" * w,
            "dash":     "─" * w,
            "double":   "═" * w,
            "stars":    "★" * w,
            "hash":     "#" * w,
            "lightning":"⚡" * (w // 1),
            "fire":     "🔥" * (w // 2),
            "heart":    "♥" * w,
            "diamond":  "◆" * w,
        }
        d = styles.get(style, styles["dash"])[:w]
        if color:
            d = ColorUtils.hex(color) + d + ColorUtils.RESET
        return d

    @staticmethod
    def print_divider(style: str = "zigzag", width: int = None, color: str = None) -> None:
        print(Ascii.divider(style, width, color))

    @staticmethod
    def boxed_title(title: str, subtitle: str = None, color: str = "#00ccff",
                    border_color: str = "#6c757d") -> str:
        body = Figlet.render(title, font="standard") if _HAS_FIGLET else Ascii.banner(title)
        lines = body.split("\n")
        if subtitle:
            lines += ["", subtitle.center(max(len(l) for l in lines))]
        width = max(len(l) for l in lines)
        bc    = ColorUtils.hex(border_color)
        tc    = ColorUtils.hex(color)
        rst   = ColorUtils.RESET
        top   = bc + "╭" + "─" * (width + 4) + "╮" + rst
        bot   = bc + "╰" + "─" * (width + 4) + "╯" + rst
        body  = "\n".join(bc + "│ " + rst + " " + tc + l.ljust(width) + rst + " " + bc + " │" + rst
                          for l in lines)
        return f"{top}\n{body}\n{bot}"


# Minimal embedded 5-row block font as fallback when pyfiglet not installed.
_MINI_BLOCK = {
    "height": 5,
    "glyphs": {
        " ": ["   ", "   ", "   ", "   ", "   "],
        "A": [" ██ ", "█  █", "████", "█  █", "█  █"],
        "B": ["███ ", "█  █", "███ ", "█  █", "███ "],
        "C": [" ███", "█   ", "█   ", "█   ", " ███"],
        "D": ["███ ", "█  █", "█  █", "█  █", "███ "],
        "E": ["████", "█   ", "███ ", "█   ", "████"],
        "F": ["████", "█   ", "███ ", "█   ", "█   "],
        "G": [" ███", "█   ", "█ ██", "█  █", " ███"],
        "H": ["█  █", "█  █", "████", "█  █", "█  █"],
        "I": ["███", " █ ", " █ ", " █ ", "███"],
        "J": ["  ██", "   █", "   █", "█  █", " ██ "],
        "K": ["█  █", "█ █ ", "██  ", "█ █ ", "█  █"],
        "L": ["█   ", "█   ", "█   ", "█   ", "████"],
        "M": ["█   █", "██ ██", "█ █ █", "█   █", "█   █"],
        "N": ["█   █", "██  █", "█ █ █", "█  ██", "█   █"],
        "O": [" ██ ", "█  █", "█  █", "█  █", " ██ "],
        "P": ["███ ", "█  █", "███ ", "█   ", "█   "],
        "Q": [" ██ ", "█  █", "█  █", "█ ██", " ███"],
        "R": ["███ ", "█  █", "███ ", "█ █ ", "█  █"],
        "S": [" ███", "█   ", " ██ ", "   █", "███ "],
        "T": ["█████", "  █  ", "  █  ", "  █  ", "  █  "],
        "U": ["█  █", "█  █", "█  █", "█  █", " ██ "],
        "V": ["█  █", "█  █", "█  █", " ██ ", " ██ "],
        "W": ["█   █", "█   █", "█ █ █", "██ ██", "█   █"],
        "X": ["█  █", " ██ ", " ██ ", " ██ ", "█  █"],
        "Y": ["█   █", " █ █ ", "  █  ", "  █  ", "  █  "],
        "Z": ["████", "  █ ", " █  ", "█   ", "████"],
        "0": [" ██ ", "█  █", "█  █", "█  █", " ██ "],
        "1": [" █ ", "██ ", " █ ", " █ ", "███"],
        "2": [" ██ ", "█  █", "  █ ", " █  ", "████"],
        "3": ["██ ", "  █", " █ ", "  █", "██ "],
        "4": ["█  █", "█  █", "████", "   █", "   █"],
        "5": ["████", "█   ", "███ ", "   █", "███ "],
        "6": [" ██ ", "█   ", "███ ", "█  █", " ██ "],
        "7": ["████", "   █", "  █ ", " █  ", "█   "],
        "8": [" ██ ", "█  █", " ██ ", "█  █", " ██ "],
        "9": [" ██ ", "█  █", " ███", "   █", " ██ "],
        "!": ["█", "█", "█", " ", "█"],
        "?": ["██ ", "  █", " █ ", "   ", " █ "],
        ".": ["  ", "  ", "  ", "  ", "█ "],
        ",": ["  ", "  ", "  ", " █", "█ "],
        ":": ["  ", "█ ", "  ", "█ ", "  "],
        "-": ["    ", "    ", "████", "    ", "    "],
        "_": ["    ", "    ", "    ", "    ", "████"],
        "/": ["   █", "  █ ", " █  ", "█   ", "█   "],
    }
}

_MINI_FONTS = {
    "block": _MINI_BLOCK,
}
