import os
import sys
import time
import math
import random
import shutil
from .colors import ColorUtils, Gradient


def _hide():
    sys.stdout.write("\033[?25l"); sys.stdout.flush()

def _show():
    sys.stdout.write("\033[?25h"); sys.stdout.flush()

def _at(x: int, y: int, text: str = "") -> None:
    sys.stdout.write(f"\033[{y};{x}H{text}")

def _clear_screen():
    sys.stdout.write("\033[2J\033[H"); sys.stdout.flush()

def _termsize() -> tuple:
    s = shutil.get_terminal_size()
    return s.columns, s.lines


class _Buffer:
    """Cheap in-memory char buffer for additive frame composition."""

    def __init__(self, cols: int, rows: int):
        self.cols = cols
        self.rows = rows
        self.chars  = [[" "] * cols for _ in range(rows)]
        self.colors = [[None] * cols for _ in range(rows)]

    def clear(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.chars[r][c]  = " "
                self.colors[r][c] = None

    def put(self, x: int, y: int, ch: str, color: tuple = None):
        if 0 <= x < self.cols and 0 <= y < self.rows:
            self.chars[y][x]  = ch
            self.colors[y][x] = color

    def render(self):
        out  = ["\033[H"]
        prev = None
        for r in range(self.rows):
            for c in range(self.cols):
                col = self.colors[r][c]
                if col != prev:
                    if col is None:
                        out.append(ColorUtils.RESET)
                    else:
                        out.append(f"\033[38;2;{col[0]};{col[1]};{col[2]}m")
                    prev = col
                out.append(self.chars[r][c])
            if r < self.rows - 1:
                out.append("\n")
        out.append(ColorUtils.RESET)
        sys.stdout.write("".join(out))
        sys.stdout.flush()


class Animations:
    @staticmethod
    def matrix_rain(duration: float = 5.0, color: str = "#00ff41",
                    density: float = 0.7, fps: int = 20) -> None:
        cols, rows = _termsize()
        chars      = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()アイウエオカキクケコ"
        head_rgb   = ColorUtils.hex_to_rgb(ColorUtils.lighten(color, 0.4))
        body_rgb   = ColorUtils.hex_to_rgb(color)
        tail_rgb   = ColorUtils.hex_to_rgb(ColorUtils.darken(color, 0.4))
        streams    = []
        for _ in range(int(cols * density)):
            streams.append({
                "x":      random.randint(0, cols - 1),
                "y":      random.randint(-rows, 0),
                "speed":  random.uniform(0.5, 1.4),
                "length": random.randint(5, 20),
            })
        buf  = _Buffer(cols, rows)
        end  = time.time() + duration
        delay = 1.0 / fps
        _clear_screen()
        _hide()
        try:
            while time.time() < end:
                buf.clear()
                for s in streams:
                    s["y"] += s["speed"]
                    head = int(s["y"])
                    for i in range(s["length"]):
                        y = head - i
                        if 0 <= y < rows:
                            ch  = random.choice(chars)
                            if i == 0:
                                col = head_rgb
                            elif i < s["length"] // 3:
                                col = body_rgb
                            else:
                                col = tail_rgb
                            buf.put(s["x"], y, ch, col)
                    if s["y"] - s["length"] > rows:
                        s["y"]      = random.randint(-10, 0)
                        s["x"]      = random.randint(0, cols - 1)
                        s["speed"]  = random.uniform(0.5, 1.4)
                        s["length"] = random.randint(5, 20)
                buf.render()
                time.sleep(delay)
        finally:
            _show()
            _clear_screen()

    @staticmethod
    def fireworks(count: int = 6, duration: float = 5.0,
                  colors: list = None, fps: int = 30) -> None:
        cols, rows = _termsize()
        palette    = colors or ["#ff4444", "#ffd60a", "#00ccff", "#9b5de5",
                                "#29bf12", "#FF69B4", "#f72585"]
        particles  = []
        rockets    = []
        delay      = 1.0 / fps
        end        = time.time() + duration
        launched   = 0
        next_launch = time.time()
        buf        = _Buffer(cols, rows)
        _clear_screen()
        _hide()
        try:
            while time.time() < end or particles or rockets:
                buf.clear()
                if time.time() >= next_launch and launched < count and time.time() < end:
                    x = random.randint(10, cols - 10)
                    rockets.append({
                        "x":  x, "y": rows - 1,
                        "tx": x + random.randint(-5, 5),
                        "ty": random.randint(3, rows // 2),
                        "vy": -1.5,
                        "color": random.choice(palette),
                    })
                    launched   += 1
                    next_launch = time.time() + random.uniform(0.3, 0.8)
                for r in rockets[:]:
                    r["y"] += r["vy"]
                    rgb     = ColorUtils.hex_to_rgb(r["color"])
                    buf.put(int(r["x"]), int(r["y"]), "│", rgb)
                    buf.put(int(r["x"]), int(r["y"]) + 1, "•", (200, 200, 200))
                    if r["y"] <= r["ty"]:
                        rockets.remove(r)
                        n_p = random.randint(20, 35)
                        for _ in range(n_p):
                            ang = random.uniform(0, math.tau)
                            spd = random.uniform(0.3, 1.0)
                            particles.append({
                                "x":   r["x"], "y": r["y"],
                                "vx":  math.cos(ang) * spd,
                                "vy":  math.sin(ang) * spd * 0.5,
                                "life": random.uniform(0.8, 1.5),
                                "age":  0.0,
                                "color": r["color"],
                            })
                for p in particles[:]:
                    p["x"]   += p["vx"]
                    p["y"]   += p["vy"]
                    p["vy"]  += 0.08
                    p["age"] += delay
                    if p["age"] > p["life"]:
                        particles.remove(p)
                        continue
                    rgb  = ColorUtils.hex_to_rgb(p["color"])
                    fade = 1 - (p["age"] / p["life"])
                    rgb  = (int(rgb[0] * fade), int(rgb[1] * fade), int(rgb[2] * fade))
                    ch   = random.choice("*+.•·✦")
                    buf.put(int(p["x"]), int(p["y"]), ch, rgb)
                buf.render()
                time.sleep(delay)
        finally:
            _show()
            _clear_screen()

    @staticmethod
    def starfield(duration: float = 4.0, density: float = 0.3, fps: int = 25) -> None:
        cols, rows = _termsize()
        n_stars    = int(cols * rows * density / 10)
        stars      = []
        for _ in range(n_stars):
            stars.append({
                "x":     random.uniform(0, cols),
                "y":     random.uniform(0, rows),
                "vx":    random.uniform(-1.5, 1.5),
                "depth": random.uniform(0.3, 1.0),
            })
        buf   = _Buffer(cols, rows)
        end   = time.time() + duration
        delay = 1.0 / fps
        _clear_screen()
        _hide()
        try:
            while time.time() < end:
                buf.clear()
                for s in stars:
                    s["x"] += s["vx"] * s["depth"]
                    if s["x"] >= cols: s["x"] = 0
                    if s["x"] < 0:     s["x"] = cols - 1
                    brt = int(60 + s["depth"] * 195)
                    ch  = "·" if s["depth"] < 0.5 else "•" if s["depth"] < 0.8 else "*"
                    buf.put(int(s["x"]), int(s["y"]), ch, (brt, brt, brt))
                buf.render()
                time.sleep(delay)
        finally:
            _show()
            _clear_screen()

    @staticmethod
    def snow(duration: float = 6.0, fps: int = 20) -> None:
        Animations._falling(duration, fps, chars=["*", "❄", "❉", "❅", ".", "·"],
                            color=(255, 255, 255))

    @staticmethod
    def rain(duration: float = 5.0, fps: int = 25) -> None:
        Animations._falling(duration, fps, chars=["│", "│", "."], color=(120, 180, 255),
                            speed_range=(1.5, 2.5))

    @staticmethod
    def confetti(duration: float = 3.0, fps: int = 25) -> None:
        cols, rows = _termsize()
        palette    = [(255, 68, 68), (255, 214, 10), (0, 204, 255), (155, 93, 229),
                      (41, 191, 18), (255, 105, 180)]
        flakes     = []
        for _ in range(int(cols * 0.5)):
            flakes.append({
                "x":     random.uniform(0, cols),
                "y":     random.uniform(-rows, 0),
                "vx":    random.uniform(-0.5, 0.5),
                "vy":    random.uniform(0.5, 1.5),
                "color": random.choice(palette),
            })
        buf   = _Buffer(cols, rows)
        end   = time.time() + duration
        delay = 1.0 / fps
        _clear_screen()
        _hide()
        try:
            while time.time() < end:
                buf.clear()
                for f in flakes:
                    f["x"] += f["vx"]
                    f["y"] += f["vy"]
                    if f["y"] >= rows:
                        f["y"] = 0
                        f["x"] = random.uniform(0, cols)
                    if f["x"] >= cols: f["x"] = 0
                    if f["x"] < 0:     f["x"] = cols - 1
                    buf.put(int(f["x"]), int(f["y"]), random.choice("*✦●▪"), f["color"])
                buf.render()
                time.sleep(delay)
        finally:
            _show()
            _clear_screen()

    @staticmethod
    def _falling(duration: float, fps: int, chars: list, color: tuple,
                 speed_range: tuple = (0.5, 1.5)) -> None:
        cols, rows = _termsize()
        items      = []
        for _ in range(int(cols * 0.6)):
            items.append({
                "x":     random.randint(0, cols - 1),
                "y":     random.uniform(-rows, 0),
                "vy":    random.uniform(*speed_range),
                "char":  random.choice(chars),
            })
        buf   = _Buffer(cols, rows)
        end   = time.time() + duration
        delay = 1.0 / fps
        _clear_screen()
        _hide()
        try:
            while time.time() < end:
                buf.clear()
                for it in items:
                    it["y"] += it["vy"]
                    if it["y"] >= rows:
                        it["y"] = 0
                        it["x"] = random.randint(0, cols - 1)
                    buf.put(it["x"], int(it["y"]), it["char"], color)
                buf.render()
                time.sleep(delay)
        finally:
            _show()
            _clear_screen()

    @staticmethod
    def glitch_screen(duration: float = 1.5, fps: int = 20) -> None:
        cols, rows = _termsize()
        end        = time.time() + duration
        delay      = 1.0 / fps
        buf        = _Buffer(cols, rows)
        glitchset  = "▓▒░█░▒▓█▌▐"
        palette    = [(0, 255, 65), (255, 0, 100), (0, 200, 255), (255, 255, 255)]
        _clear_screen()
        _hide()
        try:
            while time.time() < end:
                buf.clear()
                for _ in range(int(cols * rows * 0.3)):
                    x = random.randint(0, cols - 1)
                    y = random.randint(0, rows - 1)
                    buf.put(x, y, random.choice(glitchset), random.choice(palette))
                buf.render()
                time.sleep(delay)
        finally:
            _show()
            _clear_screen()

    @staticmethod
    def scanlines(duration: float = 3.0, color: str = "#00ff41", fps: int = 30) -> None:
        cols, rows = _termsize()
        end        = time.time() + duration
        delay      = 1.0 / fps
        rgb        = ColorUtils.hex_to_rgb(color)
        buf        = _Buffer(cols, rows)
        pos        = 0
        _clear_screen()
        _hide()
        try:
            while time.time() < end:
                buf.clear()
                y = pos % rows
                for x in range(cols):
                    buf.put(x, y, "─", rgb)
                # ghost lines
                for off in (1, 2, 3):
                    y2 = (pos - off) % rows
                    fade = 1 - off * 0.25
                    rgb2 = (int(rgb[0] * fade), int(rgb[1] * fade), int(rgb[2] * fade))
                    for x in range(cols):
                        buf.put(x, y2, "─", rgb2)
                buf.render()
                time.sleep(delay)
                pos += 1
        finally:
            _show()
            _clear_screen()


class Effect:
    @staticmethod
    def typewriter(text: str, delay: float = 0.05, color: str = None,
                   sound: bool = False, newline: bool = True) -> None:
        col   = ColorUtils.hex(color) if color else ""
        reset = ColorUtils.RESET if color else ""
        for ch in text:
            sys.stdout.write(col + ch + reset)
            sys.stdout.flush()
            if sound and ch.strip():
                try:
                    from .audio import Audio
                    Audio.click()
                except Exception:
                    pass
            time.sleep(delay)
        if newline:
            sys.stdout.write("\n")
        sys.stdout.flush()

    @staticmethod
    def glitch(text: str, duration: float = 2.0, intensity: int = 3,
               color: str = "#00ff41", fps: int = 20) -> None:
        col   = ColorUtils.hex(color)
        reset = ColorUtils.RESET
        gset  = "!@#$%^&*()_+-=[]{}|;:,.<>?/`~░▒▓█"
        end   = time.time() + duration
        delay = 1.0 / fps
        _hide()
        try:
            while time.time() < end:
                out = []
                for ch in text:
                    if ch != " " and random.randint(0, 10) < intensity:
                        out.append(random.choice(gset))
                    else:
                        out.append(ch)
                sys.stdout.write("\r" + col + "".join(out) + reset)
                sys.stdout.flush()
                time.sleep(delay)
            sys.stdout.write("\r" + col + text + reset + "\n")
            sys.stdout.flush()
        finally:
            _show()

    @staticmethod
    def fade_in(text: str, duration: float = 1.0, color: str = "#ffffff",
                steps: int = 15) -> None:
        Effect._fade(text, duration, color, steps, fade_in=True)

    @staticmethod
    def fade_out(text: str, duration: float = 1.0, color: str = "#ffffff",
                 steps: int = 15) -> None:
        Effect._fade(text, duration, color, steps, fade_in=False)

    @staticmethod
    def _fade(text: str, duration: float, color: str, steps: int, fade_in: bool) -> None:
        r, g, b = ColorUtils.hex_to_rgb(color)
        delay   = duration / steps
        for i in range(steps + 1):
            t  = i / steps if fade_in else (steps - i) / steps
            R  = int(r * t); G = int(g * t); B = int(b * t)
            sys.stdout.write(f"\r\033[38;2;{R};{G};{B}m{text}{ColorUtils.RESET}")
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\n")

    @staticmethod
    def slide_in(text: str, from_: str = "left", duration: float = 0.8,
                 color: str = "#00ccff", width: int = None) -> None:
        cols  = width or shutil.get_terminal_size().columns
        col   = ColorUtils.hex(color)
        reset = ColorUtils.RESET
        steps = 25
        delay = duration / steps
        for i in range(steps + 1):
            t = i / steps
            if from_ == "left":
                pad = int((cols - len(text)) * (1 - t))
                pad = max(0, pad)
                sys.stdout.write("\r" + " " * pad + col + text + reset)
            elif from_ == "right":
                pad = int((cols - len(text)) * t)
                pad = max(0, pad)
                sys.stdout.write("\r" + " " * pad + col + text + reset)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\n")

    @staticmethod
    def slide_out(text: str, to: str = "right", duration: float = 0.8,
                  color: str = "#00ccff", width: int = None) -> None:
        cols  = width or shutil.get_terminal_size().columns
        col   = ColorUtils.hex(color)
        reset = ColorUtils.RESET
        steps = 25
        delay = duration / steps
        for i in range(steps + 1):
            t = i / steps
            if to == "right":
                pad = int((cols - len(text)) * t)
            else:
                pad = int((cols - len(text)) * (1 - t))
            sys.stdout.write("\r" + " " * cols + "\r" + " " * pad + col + text + reset)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\r" + " " * cols + "\r\n")

    @staticmethod
    def wave(text: str, duration: float = 3.0, color: str = "#00ccff",
             amplitude: int = 2, fps: int = 25) -> None:
        cols       = shutil.get_terminal_size().columns
        rows_used  = amplitude * 2 + 1
        end        = time.time() + duration
        delay      = 1.0 / fps
        r, g, b    = ColorUtils.hex_to_rgb(color)
        col        = f"\033[38;2;{r};{g};{b}m"
        rst        = ColorUtils.RESET
        for _ in range(rows_used):
            sys.stdout.write("\n")
        _hide()
        try:
            t0 = time.time()
            while time.time() < end:
                t      = time.time() - t0
                # move cursor up rows_used to redraw
                sys.stdout.write(f"\033[{rows_used}A")
                lines = [[" "] * cols for _ in range(rows_used)]
                for i, ch in enumerate(text):
                    if i >= cols: break
                    y = amplitude + int(math.sin((i / 3.0) + t * 4) * amplitude)
                    lines[y][i] = ch
                for row in lines:
                    sys.stdout.write("\r" + col + "".join(row) + rst + "\n")
                sys.stdout.flush()
                time.sleep(delay)
        finally:
            _show()

    @staticmethod
    def shake(text: str, duration: float = 1.0, color: str = "#ff4444",
              intensity: int = 2, fps: int = 25) -> None:
        col   = ColorUtils.hex(color)
        reset = ColorUtils.RESET
        cols  = shutil.get_terminal_size().columns
        end   = time.time() + duration
        delay = 1.0 / fps
        while time.time() < end:
            pad = " " * random.randint(0, intensity * 2)
            sys.stdout.write("\r" + " " * cols + "\r" + pad + col + text + reset)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\r" + " " * cols + "\r" + col + text + reset + "\n")

    @staticmethod
    def explode(text: str, duration: float = 1.5, color: str = "#ffd60a",
                fps: int = 25) -> None:
        cols, rows = _termsize()
        start_x    = max(1, (cols - len(text)) // 2)
        start_y    = rows // 2
        particles  = []
        for i, ch in enumerate(text):
            ang = random.uniform(0, math.tau)
            spd = random.uniform(0.5, 1.5)
            particles.append({
                "ch": ch,
                "x":  start_x + i, "y": start_y,
                "vx": math.cos(ang) * spd,
                "vy": math.sin(ang) * spd * 0.5,
            })
        buf   = _Buffer(cols, rows)
        end   = time.time() + duration
        delay = 1.0 / fps
        rgb   = ColorUtils.hex_to_rgb(color)
        _clear_screen()
        _hide()
        try:
            while time.time() < end:
                buf.clear()
                for p in particles:
                    p["x"]  += p["vx"]
                    p["y"]  += p["vy"]
                    p["vy"] += 0.05
                    buf.put(int(p["x"]), int(p["y"]), p["ch"], rgb)
                buf.render()
                time.sleep(delay)
        finally:
            _show()
            _clear_screen()

    @staticmethod
    def implode(text: str, duration: float = 1.5, color: str = "#ffd60a",
                fps: int = 25) -> None:
        cols, rows = _termsize()
        end_x      = max(1, (cols - len(text)) // 2)
        end_y      = rows // 2
        particles  = []
        for i, ch in enumerate(text):
            ang = random.uniform(0, math.tau)
            dist = random.uniform(15, 30)
            particles.append({
                "ch":   ch,
                "ex":   end_x + i, "ey": end_y,
                "x":    end_x + i + math.cos(ang) * dist,
                "y":    end_y + math.sin(ang) * dist * 0.5,
            })
        buf   = _Buffer(cols, rows)
        end   = time.time() + duration
        steps = int(duration / (1.0 / fps))
        delay = duration / steps
        rgb   = ColorUtils.hex_to_rgb(color)
        _clear_screen()
        _hide()
        try:
            for i in range(steps + 1):
                t = i / steps
                buf.clear()
                for p in particles:
                    cx = p["x"] + (p["ex"] - p["x"]) * t
                    cy = p["y"] + (p["ey"] - p["y"]) * t
                    buf.put(int(cx), int(cy), p["ch"], rgb)
                buf.render()
                time.sleep(delay)
        finally:
            _show()
            _clear_screen()

    @staticmethod
    def scramble(text: str, duration: float = 1.5, color: str = "#00ff41",
                 fps: int = 20) -> None:
        chars   = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*"
        col     = ColorUtils.hex(color)
        reset   = ColorUtils.RESET
        n       = len(text)
        steps   = max(1, int(duration * fps))
        delay   = duration / steps
        revealed = [False] * n
        order    = [i for i in range(n) if text[i] != " "]
        random.shuffle(order)
        per_step = max(1, len(order) // steps)
        for s in range(steps + 1):
            # reveal more characters
            for _ in range(per_step):
                if order:
                    revealed[order.pop()] = True
            out = []
            for i, ch in enumerate(text):
                if revealed[i] or ch == " ":
                    out.append(ch)
                else:
                    out.append(random.choice(chars))
            sys.stdout.write("\r" + col + "".join(out) + reset)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\r" + col + text + reset + "\n")

    @staticmethod
    def rainbow_scroll(text: str, duration: float = 3.0, fps: int = 20) -> None:
        end   = time.time() + duration
        delay = 1.0 / fps
        offset = 0
        while time.time() < end:
            out = []
            for i, ch in enumerate(text):
                hue = ((i + offset) * 20) % 360
                rgb = ColorUtils.hsl(hue, 100, 50)
                out.append(rgb + ch)
            sys.stdout.write("\r" + "".join(out) + ColorUtils.RESET)
            sys.stdout.flush()
            time.sleep(delay)
            offset += 1
        sys.stdout.write("\n")

    @staticmethod
    def flash(text: str, times: int = 3, color: str = "#ff4444", delay: float = 0.2) -> None:
        col   = ColorUtils.hex(color)
        reset = ColorUtils.RESET
        blank = " " * len(text)
        for _ in range(times):
            sys.stdout.write("\r" + col + text + reset); sys.stdout.flush()
            time.sleep(delay)
            sys.stdout.write("\r" + blank); sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\r" + col + text + reset + "\n")

    @staticmethod
    def countdown_explode(seconds: int = 5, color: str = "#ffd60a",
                          boom_color: str = "#ff4444") -> None:
        col   = ColorUtils.hex(color)
        reset = ColorUtils.RESET
        for i in range(seconds, 0, -1):
            sys.stdout.write("\r " + col + f"⏱  {i}  " + reset + " " * 20)
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write("\r")
        Effect.explode("💥 BOOM! 💥", duration=1.5, color=boom_color)

    @staticmethod
    def fly_text(text: str, path: str = "wave", duration: float = 3.0,
                 color: str = "#00ccff", fps: int = 25) -> None:
        cols, rows = _termsize()
        delay      = 1.0 / fps
        end        = time.time() + duration
        rgb        = ColorUtils.hex_to_rgb(color)
        buf        = _Buffer(cols, rows)
        _clear_screen()
        _hide()
        t0 = time.time()
        try:
            while time.time() < end:
                t = time.time() - t0
                buf.clear()
                for i, ch in enumerate(text):
                    if path == "wave":
                        x = int((t * 20 + i * 2) % cols)
                        y = rows // 2 + int(math.sin((t * 4) + i / 2) * (rows // 4))
                    elif path == "spiral":
                        ang = t * 2 + i * 0.3
                        rad = (t * 2) % min(cols, rows) / 3
                        x = int(cols // 2 + math.cos(ang) * rad)
                        y = int(rows // 2 + math.sin(ang) * rad * 0.5)
                    elif path == "zigzag":
                        x = int((t * 15 + i * 2) % cols)
                        y = rows // 2 + (1 if int(x / 4) % 2 else -1) * 3
                    else:
                        x = int((t * 15 + i) % cols)
                        y = rows // 2
                    buf.put(x, y, ch, rgb)
                buf.render()
                time.sleep(delay)
        finally:
            _show()
            _clear_screen()


class Particle:
    @staticmethod
    def emit(x: int, y: int, kind: str = "spark", count: int = 20,
             duration: float = 1.0, color: str = "#ffd60a", fps: int = 25) -> None:
        cols, rows = _termsize()
        chars_map  = {
            "spark":     ("*+•.",        (255, 214, 10)),
            "dust":      ("·.",          (200, 200, 200)),
            "fire":      ("^*•",         (255, 80, 0)),
            "smoke":     ("░▒▓",         (120, 120, 120)),
            "bubble":    ("oO○",         (100, 200, 255)),
            "snow":      ("*❄.",         (255, 255, 255)),
        }
        chars, def_col = chars_map.get(kind, chars_map["spark"])
        rgb = ColorUtils.hex_to_rgb(color) if color else def_col
        particles = []
        for _ in range(count):
            ang = random.uniform(0, math.tau)
            spd = random.uniform(0.3, 1.0)
            particles.append({
                "x":  x, "y": y,
                "vx": math.cos(ang) * spd,
                "vy": math.sin(ang) * spd * 0.5,
                "ch": random.choice(chars),
                "age": 0,
                "life": random.uniform(0.5, duration),
            })
        buf   = _Buffer(cols, rows)
        end   = time.time() + duration
        delay = 1.0 / fps
        _clear_screen()
        _hide()
        try:
            while time.time() < end:
                buf.clear()
                for p in particles[:]:
                    p["x"]   += p["vx"]
                    p["y"]   += p["vy"]
                    p["age"] += delay
                    if p["age"] > p["life"]:
                        particles.remove(p)
                        continue
                    buf.put(int(p["x"]), int(p["y"]), p["ch"], rgb)
                buf.render()
                time.sleep(delay)
                if not particles:
                    break
        finally:
            _show()
            _clear_screen()

    @staticmethod
    def explosion(x: int, y: int, radius: int = 15, duration: float = 1.5,
                  colors: list = None, fps: int = 25) -> None:
        cols, rows = _termsize()
        palette    = [ColorUtils.hex_to_rgb(c) for c in (colors or
                       ["#ffd60a", "#ff4444", "#ff7b00", "#ffffff"])]
        particles = []
        for _ in range(60):
            ang = random.uniform(0, math.tau)
            spd = random.uniform(0.3, radius / 8)
            particles.append({
                "x":  x, "y": y,
                "vx": math.cos(ang) * spd,
                "vy": math.sin(ang) * spd * 0.5,
                "color": random.choice(palette),
                "life":  random.uniform(0.6, duration),
                "age":   0,
            })
        buf   = _Buffer(cols, rows)
        end   = time.time() + duration
        delay = 1.0 / fps
        _clear_screen()
        _hide()
        try:
            while time.time() < end:
                buf.clear()
                for p in particles[:]:
                    p["x"]   += p["vx"]
                    p["y"]   += p["vy"]
                    p["vy"]  += 0.05
                    p["age"] += delay
                    if p["age"] > p["life"]:
                        particles.remove(p)
                        continue
                    fade = 1 - p["age"] / p["life"]
                    col  = p["color"]
                    col  = (int(col[0] * fade), int(col[1] * fade), int(col[2] * fade))
                    buf.put(int(p["x"]), int(p["y"]), random.choice("*+•·✦"), col)
                buf.render()
                time.sleep(delay)
                if not particles:
                    break
        finally:
            _show()
            _clear_screen()

    @staticmethod
    def trail(from_: tuple, to: tuple, kind: str = "dust",
              steps: int = 20, color: str = "#adb5bd", fps: int = 25) -> None:
        cols, rows = _termsize()
        chars_map  = {
            "dust":   "·.",
            "spark":  "*+•",
            "fire":   "^*•",
            "bubble": "oO○",
        }
        chars = chars_map.get(kind, chars_map["dust"])
        rgb   = ColorUtils.hex_to_rgb(color)
        buf   = _Buffer(cols, rows)
        delay = 1.0 / fps
        dx    = (to[0] - from_[0]) / steps
        dy    = (to[1] - from_[1]) / steps
        positions = []
        _clear_screen()
        _hide()
        try:
            for i in range(steps + 1):
                buf.clear()
                px = from_[0] + dx * i
                py = from_[1] + dy * i
                positions.append((px, py))
                if len(positions) > 8:
                    positions.pop(0)
                for j, (x, y) in enumerate(positions):
                    fade = (j + 1) / len(positions)
                    c    = (int(rgb[0] * fade), int(rgb[1] * fade), int(rgb[2] * fade))
                    buf.put(int(x), int(y), random.choice(chars), c)
                buf.render()
                time.sleep(delay)
        finally:
            _show()
            _clear_screen()
