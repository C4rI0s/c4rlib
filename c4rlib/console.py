import os
import sys
import time
import threading
from .colors import ColorUtils, Gradient
from .terminal import Terminal


class Spinner:
    STYLES = {
        "dots":      ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"],
        "dots2":     ["⣾","⣽","⣻","⢿","⡿","⣟","⣯","⣷"],
        "dots3":     ["⡀","⡄","⡆","⡇","⡏","⡟","⡿","⣿","⢿","⢻","⢹","⢸","⢰","⢠","⢀"],
        "line":      ["|","/","─","\\"],
        "arrows":    ["←","↖","↑","↗","→","↘","↓","↙"],
        "arrows2":   ["⬆","↗","➡","↘","⬇","↙","⬅","↖"],
        "bounce":    ["▁","▂","▃","▄","▅","▆","▇","█","▇","▆","▅","▄","▃","▂"],
        "circle":    ["◐","◓","◑","◒"],
        "circle2":   ["◴","◷","◶","◵"],
        "square":    ["◰","◳","◲","◱"],
        "star":      ["✶","✸","✹","✺","✹","✸"],
        "star2":     ["★","☆","★","☆"],
        "grow":      ["▏","▎","▍","▌","▋","▊","▉","█","▉","▊","▋","▌","▍","▎"],
        "pulse":     ["·","•","●","•"],
        "flip":      ["_","_","_","-","`","`","'","´","-","_","_","_"],
        "balloon":   [" ",".","o","O","@","*"," "],
        "noise":     ["▓","▒","░","▒"],
        "point":     ["∙∙∙","●∙∙","∙●∙","∙∙●"],
        "layer":     ["-","=","≡"],
        "earth":     ["🌍","🌎","🌏"],
        "moon":      ["🌑","🌒","🌓","🌔","🌕","🌖","🌗","🌘"],
        "hearts":    ["💛","💙","💜","💚","❤️"],
        "clock":     ["🕛","🕐","🕑","🕒","🕓","🕔","🕕","🕖","🕗","🕘","🕙","🕚"],
        "runner":    ["🚶","🏃"],
        "weather":   ["☀️","🌤️","⛅","🌥️","☁️","🌦️","🌧️","⛈️","🌩️","🌨️"],
        "dice":      ["⚀","⚁","⚂","⚃","⚄","⚅"],
        "aesthetic": ["◢◤","◣◥"],
        "matrix":    ["0","1"],
    }

    def __init__(self, text: str = "Loading...", style: str = "dots", color: str = "#00ccff", interval: float = 0.1):
        self.text      = text
        self._frames   = self.STYLES.get(style, self.STYLES["dots"])
        self._color    = color
        self._interval = interval
        self._running  = False
        self._thread   = None
        self._idx      = 0

    def _spin(self) -> None:
        while self._running:
            frame = self._frames[self._idx % len(self._frames)]
            col   = ColorUtils.hex(self._color)
            sys.stdout.write(f"\r {col}{frame}{ColorUtils.reset()}  {self.text}   ")
            sys.stdout.flush()
            self._idx += 1
            time.sleep(self._interval)

    def start(self) -> "Spinner":
        self._running = True
        self._thread  = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()
        return self

    def stop(self, final_text: str = None, success: bool = True) -> None:
        self._running = False
        if self._thread: self._thread.join()
        icon = f"{ColorUtils.hex('#29bf12')}✔" if success else f"{ColorUtils.hex('#d00000')}✘"
        sys.stdout.write(f"\r {icon}{ColorUtils.reset()}  {final_text or self.text}   \n")
        sys.stdout.flush()

    def __enter__(self) -> "Spinner":
        return self.start()

    def __exit__(self, exc_type, *_) -> None:
        self.stop(success=exc_type is None)


class ProgressBar:
    STYLES = {
        "block":   ("█","░"),
        "shade":   ("▓","░"),
        "smooth":  ("━","─"),
        "classic": ("#","."),
        "arrow":   ("=","-"),
        "dot":     ("●","○"),
        "square":  ("■","□"),
        "diamond": ("◆","◇"),
        "line":    ("─"," "),
        "wave":    ("≈","~"),
        "star":    ("★","☆"),
        "heart":   ("♥","♡"),
        "fire":    ("█","░"),
        "thin":    ("▬","▭"),
    }

    def __init__(self, total: int = 100, label: str = "Progress", width: int = 40,
                 style: str = "block", color: str = "#00ccff", bg_color: str = "#6c757d",
                 show_eta: bool = True, show_speed: bool = True, show_count: bool = True):
        self.total       = total
        self.label       = label
        self.width       = width
        self._fill, self._empty = self.STYLES.get(style, self.STYLES["block"])
        self._color      = color
        self._bg_color   = bg_color
        self._show_eta   = show_eta
        self._show_speed = show_speed
        self._show_count = show_count
        self._current    = 0
        self._start      = time.time()

    def update(self, amount: int = 1) -> None:
        self._current = min(self._current + amount, self.total)
        self._render()

    def set(self, value: int) -> None:
        self._current = min(max(value, 0), self.total)
        self._render()

    def _render(self) -> None:
        pct    = self._current / self.total if self.total else 0
        filled = int(self.width * pct)
        bar_f  = ColorUtils.hex(self._color)    + self._fill  * filled
        bar_e  = ColorUtils.hex(self._bg_color) + self._empty * (self.width - filled)
        bar    = bar_f + bar_e + ColorUtils.reset()
        elapsed = time.time() - self._start
        extras  = ""
        if self._show_speed and elapsed > 0:
            speed   = self._current / elapsed
            extras += f"  {ColorUtils.hex('#f77f00')}{speed:.1f}/s{ColorUtils.reset()}"
        if self._show_eta and self._current > 0 and self._current < self.total:
            remaining = (elapsed / self._current) * (self.total - self._current)
            extras   += f"  ETA {ColorUtils.hex('#ffd60a')}{remaining:.1f}s{ColorUtils.reset()}"
        pct_str = f"{ColorUtils.hex(self._color)}{pct*100:5.1f}%{ColorUtils.reset()}"
        cnt_str = f"{ColorUtils.hex('#6c757d')}{self._current}/{self.total}{ColorUtils.reset()}" if self._show_count else ""
        sys.stdout.write(f"\r {self.label}  [{bar}]  {pct_str}  {cnt_str}{extras}  ")
        sys.stdout.flush()

    def finish(self, text: str = None) -> None:
        self._current = self.total
        self._render()
        sys.stdout.write(f"\n {ColorUtils.hex('#29bf12')}✔{ColorUtils.reset()}  {text or self.label} complete\n")
        sys.stdout.flush()


class MultiProgressBar:
    def __init__(self, bars: list):
        self._bars    = bars
        self._started = False

    def update(self, index: int, amount: int = 1) -> None:
        if index < len(self._bars):
            self._bars[index]._current = min(self._bars[index]._current + amount, self._bars[index].total)
        self._render_all()

    def _render_all(self) -> None:
        sys.stdout.write(f"\033[{len(self._bars)}A")
        for bar in self._bars:
            bar._render()
            sys.stdout.write("\n")
        sys.stdout.flush()

    def start(self) -> None:
        for bar in self._bars:
            bar._render()
            sys.stdout.write("\n")
        sys.stdout.flush()


class Table:
    def __init__(self, headers: list = None, title: str = None,
                 header_color: str = "#00ccff", border_color: str = "#6c757d",
                 row_colors: list = None, align: str = "left",
                 zebra: bool = True):
        self.headers       = headers or []
        self.title         = title
        self._header_color = header_color
        self._border_color = border_color
        self._row_colors   = row_colors or (["#ffffff","#cccccc"] if zebra else ["#ffffff"])
        self._align        = align
        self._rows         = []

    def add_row(self, row: list) -> None:
        self._rows.append([str(c) for c in row])

    def add_rows(self, rows: list) -> None:
        for row in rows: self.add_row(row)

    def clear(self) -> None:
        self._rows = []

    def _col_widths(self) -> list:
        # Measured in display columns, not characters: "日本語" is 3 code points
        # but 6 columns, and using len() here ragged the borders.
        all_rows = [self.headers] + self._rows if self.headers else self._rows
        cols     = max(len(r) for r in all_rows) if all_rows else 0
        return [
            max(Terminal.display_width(r[i]) if i < len(r) else 0 for r in all_rows)
            for i in range(cols)
        ]

    def render(self) -> str:
        widths = self._col_widths()
        bc     = ColorUtils.hex(self._border_color)
        hc     = ColorUtils.hex(self._header_color)
        reset  = ColorUtils.reset()

        def sep(l, m, r, h):
            return bc + l + m.join(h * (w+2) for w in widths) + r + reset

        def fmt_cell(text, width, color):
            padded = Terminal.pad_display(text, width, self._align)
            return f" {color}{padded}{reset} "

        lines = []
        if self.title:
            # Inner width = each cell (w + 2 padding) plus the separators
            # between them. The previous formula added len(widths) too many.
            total_w = sum(widths) + 3*len(widths) - 1
            lines.append(sep("╔","═","╗","═"))
            lines.append(bc+"║"+reset+hc+Terminal.pad_display(self.title, total_w, "center")+reset+bc+"║"+reset)
            lines.append(sep("╠","╦","╣","═"))
        else:
            lines.append(sep("╔","╦","╗","═"))

        if self.headers:
            cells = bc+"║"+reset
            for i, h in enumerate(self.headers):
                w = widths[i] if i < len(widths) else len(h)
                cells += fmt_cell(h, w, hc) + bc+"║"+reset
            lines.append(cells)
            lines.append(sep("╠","╬","╣","═"))

        for ri, row in enumerate(self._rows):
            rc    = ColorUtils.hex(self._row_colors[ri % len(self._row_colors)])
            cells = bc+"║"+reset
            for i in range(len(widths)):
                val   = row[i] if i < len(row) else ""
                cells += fmt_cell(val, widths[i], rc) + bc+"║"+reset
            lines.append(cells)
            if ri < len(self._rows)-1:
                lines.append(sep("╠","╬","╣","─"))

        lines.append(sep("╚","╩","╝","═"))
        return "\n".join(lines)

    def print(self) -> None:
        print(self.render())

    def to_csv(self, separator: str = ",") -> str:
        lines = []
        if self.headers: lines.append(separator.join(self.headers))
        for row in self._rows: lines.append(separator.join(row))
        return "\n".join(lines)


class Console:
    @staticmethod
    def clear() -> None:
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def title(text: str) -> None:
        if os.name == "nt":
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW(text)

    @staticmethod
    def move_cursor(x: int, y: int) -> None:
        sys.stdout.write(f"\033[{y};{x}H")
        sys.stdout.flush()

    @staticmethod
    def hide_cursor() -> None:
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    @staticmethod
    def show_cursor() -> None:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

    @staticmethod
    def bell() -> None:
        sys.stdout.write("\a")
        sys.stdout.flush()

    @staticmethod
    def width() -> int:
        import shutil
        return shutil.get_terminal_size().columns

    @staticmethod
    def height() -> int:
        import shutil
        return shutil.get_terminal_size().lines

    @staticmethod
    def size() -> tuple:
        import shutil
        s = shutil.get_terminal_size()
        return s.columns, s.lines

    @staticmethod
    def countdown(seconds: int, text: str = "Starting in", color: str = "#00ccff") -> None:
        col = ColorUtils.hex(color)
        for i in range(seconds, 0, -1):
            sys.stdout.write(f"\r {col}{text} {i}s...{ColorUtils.reset()}  ")
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write(f"\r {col}{text} 0s... GO!{ColorUtils.reset()}  \n")
        sys.stdout.flush()

    @staticmethod
    def typewriter(text: str, delay: float = 0.04, color: str = None) -> None:
        col   = ColorUtils.hex(color) if color else ""
        reset = ColorUtils.reset() if color else ""
        for char in text:
            sys.stdout.write(col+char+reset)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\n")
        sys.stdout.flush()

    @staticmethod
    def rule(char: str = "─", color: str = "#6c757d") -> None:
        import shutil
        w   = shutil.get_terminal_size().columns
        col = ColorUtils.hex(color)
        print(f"{col}{char * w}{ColorUtils.reset()}")

    @staticmethod
    def gradient_rule(start: tuple = (0,200,255), end: tuple = (200,0,255)) -> None:
        import shutil
        w    = shutil.get_terminal_size().columns
        line = "─" * w
        print(Gradient.apply(line, start, end))

    @staticmethod
    def input_prompt(text: str, color: str = "#00ccff") -> str:
        col   = ColorUtils.hex(color)
        reset = ColorUtils.reset()
        return input(f" {col}❯{reset} {text}: ")

    @staticmethod
    def confirm(text: str, color: str = "#ffd60a") -> bool:
        col    = ColorUtils.hex(color)
        reset  = ColorUtils.reset()
        answer = input(f" {col}?{reset} {text} [y/n]: ").strip().lower()
        return answer in ("y","yes","s","si","1","true")

    @staticmethod
    def select(text: str, options: list, color: str = "#00ccff") -> int:
        col   = ColorUtils.hex(color)
        gray  = ColorUtils.hex("#6c757d")
        reset = ColorUtils.reset()
        print(f"\n {col}?{reset} {text}")
        for i, opt in enumerate(options):
            print(f"  {gray}{i+1}.{reset} {opt}")
        while True:
            try:
                choice = int(input(f"\n {col}❯{reset} Select (1-{len(options)}): "))
                if 1 <= choice <= len(options):
                    return choice - 1
                print(f"  {ColorUtils.hex('#d00000')}Invalid choice{reset}")
            except ValueError:
                print(f"  {ColorUtils.hex('#d00000')}Enter a number{reset}")

    @staticmethod
    def pause(text: str = "Press ENTER to continue...") -> None:
        input(f" {ColorUtils.hex('#6c757d')}{text}{ColorUtils.reset()}")

    @staticmethod
    def print_cols(items: list, cols: int = 3, color: str = "#ffffff") -> None:
        import shutil
        col_width = shutil.get_terminal_size().columns // cols
        c = ColorUtils.hex(color)
        reset = ColorUtils.reset()
        for i, item in enumerate(items):
            end = "\n" if (i+1) % cols == 0 else ""
            sys.stdout.write(f"{c}{str(item).ljust(col_width)}{reset}{end}")
        if len(items) % cols != 0: sys.stdout.write("\n")
        sys.stdout.flush()

    @staticmethod
    def save_cursor() -> None:
        sys.stdout.write("\033[s"); sys.stdout.flush()

    @staticmethod
    def restore_cursor() -> None:
        sys.stdout.write("\033[u"); sys.stdout.flush()

    @staticmethod
    def clear_line() -> None:
        sys.stdout.write("\033[2K\r"); sys.stdout.flush()

    @staticmethod
    def clear_screen() -> None:
        sys.stdout.write("\033[2J\033[H"); sys.stdout.flush()

    @staticmethod
    def at(x: int, y: int, text: str = "") -> None:
        sys.stdout.write(f"\033[{y};{x}H{text}"); sys.stdout.flush()
