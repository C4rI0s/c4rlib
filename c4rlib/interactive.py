import os
import re
import sys
import time
import shutil
import threading
from .colors import ColorUtils, Gradient


_IS_WINDOWS = os.name == "nt"

if _IS_WINDOWS:
    import ctypes
    from ctypes import wintypes
else:
    import tty
    import termios
    import select


# ─────────────────────────────────────────────────────────────────────────────
# Mouse mode helpers
#
# Windows path: read events directly with ReadConsoleInputW (msvcrt.getch
# silently drops MOUSE_EVENTs, which is why the previous attempts failed).
# Unix path: xterm SGR mouse mode escape sequences via stdin in raw mode.
# ─────────────────────────────────────────────────────────────────────────────
_WIN_SAVED_IN_MODE  = None
_WIN_SAVED_OUT_MODE = None


if _IS_WINDOWS:
    # Win32 INPUT_RECORD layout
    class _COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    class _UCHAR(ctypes.Union):
        _fields_ = [("UnicodeChar", ctypes.c_wchar),
                    ("AsciiChar",   ctypes.c_char)]

    class _KEY_EVENT(ctypes.Structure):
        _fields_ = [("bKeyDown",          ctypes.c_int),
                    ("wRepeatCount",      ctypes.c_ushort),
                    ("wVirtualKeyCode",   ctypes.c_ushort),
                    ("wVirtualScanCode",  ctypes.c_ushort),
                    ("uChar",             _UCHAR),
                    ("dwControlKeyState", ctypes.c_ulong)]

    class _MOUSE_EVENT(ctypes.Structure):
        _fields_ = [("dwMousePosition",   _COORD),
                    ("dwButtonState",     ctypes.c_ulong),
                    ("dwControlKeyState", ctypes.c_ulong),
                    ("dwEventFlags",      ctypes.c_ulong)]

    class _WIN_BUFFER_SIZE(ctypes.Structure):
        _fields_ = [("dwSize", _COORD)]

    class _MENU_EVENT(ctypes.Structure):
        _fields_ = [("dwCommandId", ctypes.c_uint)]

    class _FOCUS_EVENT(ctypes.Structure):
        _fields_ = [("bSetFocus", ctypes.c_int)]

    class _EVENT_UNION(ctypes.Union):
        _fields_ = [("KeyEvent",              _KEY_EVENT),
                    ("MouseEvent",            _MOUSE_EVENT),
                    ("WindowBufferSizeEvent", _WIN_BUFFER_SIZE),
                    ("MenuEvent",             _MENU_EVENT),
                    ("FocusEvent",            _FOCUS_EVENT)]

    class _INPUT_RECORD(ctypes.Structure):
        _fields_ = [("EventType", ctypes.c_ushort),
                    ("Event",     _EVENT_UNION)]

    class _SMALL_RECT(ctypes.Structure):
        _fields_ = [("Left",   ctypes.c_short),
                    ("Top",    ctypes.c_short),
                    ("Right",  ctypes.c_short),
                    ("Bottom", ctypes.c_short)]

    class _CSBI(ctypes.Structure):
        _fields_ = [("dwSize",              _COORD),
                    ("dwCursorPosition",    _COORD),
                    ("wAttributes",         ctypes.c_ushort),
                    ("srWindow",            _SMALL_RECT),
                    ("dwMaximumWindowSize", _COORD)]

    _STD_INPUT  = -10
    _STD_OUTPUT = -11
    _EVT_KEY    = 0x0001
    _EVT_MOUSE  = 0x0002
    _MOUSE_WHEELED = 0x0004
    _LEFT_BTN   = 0x0001
    _RIGHT_BTN  = 0x0002
    _MIDDLE_BTN = 0x0004

    _VK_MAP = {
        0x26: "up",     0x28: "down",   0x25: "left",   0x27: "right",
        0x0D: "enter",  0x1B: "esc",    0x20: "space",  0x09: "tab",
        0x08: "backspace",
        0x24: "home",   0x23: "end",
        0x21: "pageup", 0x22: "pagedown",
        0x2E: "delete",
    }


def _win_configure_console(enable: bool) -> None:
    """Switch the console into a mode that delivers mouse events to us.

    - ENABLE_MOUSE_INPUT (0x0010): make ReadConsoleInput surface mouse events.
    - ENABLE_EXTENDED_FLAGS (0x0080) + clear ENABLE_QUICK_EDIT_MODE (0x0040):
      stop conhost from grabbing left-clicks for text selection.
    - Clear ENABLE_LINE_INPUT (0x0002) and ENABLE_PROCESSED_INPUT (0x0001) so
      we get individual events instead of cooked lines.
    """
    if not _IS_WINDOWS:
        return
    global _WIN_SAVED_IN_MODE, _WIN_SAVED_OUT_MODE
    try:
        kernel32 = ctypes.windll.kernel32
        h_in  = kernel32.GetStdHandle(_STD_INPUT)
        h_out = kernel32.GetStdHandle(_STD_OUTPUT)
        in_mode  = ctypes.c_ulong()
        out_mode = ctypes.c_ulong()
        if not kernel32.GetConsoleMode(h_in,  ctypes.byref(in_mode)):  return
        if not kernel32.GetConsoleMode(h_out, ctypes.byref(out_mode)): return
        if enable:
            _WIN_SAVED_IN_MODE  = in_mode.value
            _WIN_SAVED_OUT_MODE = out_mode.value
            new_in = ((in_mode.value
                       | 0x0080      # ENABLE_EXTENDED_FLAGS
                       | 0x0010)     # ENABLE_MOUSE_INPUT
                      & ~0x0040      # disable QUICK_EDIT_MODE
                      & ~0x0002      # disable LINE_INPUT
                      & ~0x0001)     # disable PROCESSED_INPUT (so Ctrl+C is read)
            kernel32.SetConsoleMode(h_in,  new_in)
            new_out = out_mode.value | 0x0004  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
            kernel32.SetConsoleMode(h_out, new_out)
        else:
            if _WIN_SAVED_IN_MODE  is not None: kernel32.SetConsoleMode(h_in,  _WIN_SAVED_IN_MODE)
            if _WIN_SAVED_OUT_MODE is not None: kernel32.SetConsoleMode(h_out, _WIN_SAVED_OUT_MODE)
            _WIN_SAVED_IN_MODE = _WIN_SAVED_OUT_MODE = None
    except Exception:
        pass


def _enable_mouse() -> None:
    """Turn on mouse tracking (clicks + scroll)."""
    _win_configure_console(True)
    if not _IS_WINDOWS:
        # ?1000 = button events, ?1002 = drag, ?1006 = SGR coords
        sys.stdout.write("\033[?1000h\033[?1002h\033[?1006h")
        sys.stdout.flush()


def _disable_mouse() -> None:
    if not _IS_WINDOWS:
        sys.stdout.write("\033[?1000l\033[?1002l\033[?1006l")
        sys.stdout.flush()
    _win_configure_console(False)


def _parse_escape(seq: str) -> str:
    """Parse a buffered escape sequence into a logical key/event."""
    if not seq.startswith("\x1b["):
        return "esc"
    body = seq[2:]
    simple = {"A":"up","B":"down","C":"right","D":"left",
              "H":"home","F":"end","Z":"shift_tab"}
    if body in simple:
        return simple[body]
    if body == "3~": return "delete"
    if body == "5~": return "pageup"
    if body == "6~": return "pagedown"
    # SGR mouse: <btn;col;row(M|m)
    if body.startswith("<") and body[-1:] in ("M", "m"):
        action = body[-1]
        parts  = body[1:-1].split(";")
        if len(parts) == 3:
            try:
                btn = int(parts[0])
                x   = int(parts[1])
                y   = int(parts[2])
            except ValueError:
                return "unknown"
            if action == "M":  # press / scroll
                if btn == 64: return "scroll_up"
                if btn == 65: return "scroll_down"
                if btn == 0:  return f"mouse_click:{x},{y}"
                if btn == 1:  return f"mouse_middle:{x},{y}"
                if btn == 2:  return f"mouse_right:{x},{y}"
            return "mouse_release"
    return "esc"


def _win_read_event() -> str:
    """Read one event via ReadConsoleInputW. Returns logical key/mouse string."""
    kernel32 = ctypes.windll.kernel32
    h_in     = kernel32.GetStdHandle(_STD_INPUT)
    record   = _INPUT_RECORD()
    n_read   = ctypes.c_ulong()
    while True:
        ok = kernel32.ReadConsoleInputW(h_in, ctypes.byref(record), 1, ctypes.byref(n_read))
        if not ok or n_read.value == 0:
            return "unknown"
        et = record.EventType
        if et == _EVT_KEY:
            ke = record.Event.KeyEvent
            if not ke.bKeyDown:
                continue
            vk = ke.wVirtualKeyCode
            if vk in _VK_MAP:
                return _VK_MAP[vk]
            ch = ke.uChar.UnicodeChar
            if ch and ch != "\x00":
                return ch
            continue
        if et == _EVT_MOUSE:
            me     = record.Event.MouseEvent
            x      = me.dwMousePosition.X + 1     # 1-indexed to match xterm
            y      = me.dwMousePosition.Y + 1
            flags  = me.dwEventFlags
            if flags & _MOUSE_WHEELED:
                delta = ctypes.c_short((me.dwButtonState >> 16) & 0xFFFF).value
                return "scroll_up" if delta > 0 else "scroll_down"
            if flags == 0:  # button-down (not movement, not wheel, not double-click)
                btn = me.dwButtonState
                if btn & _LEFT_BTN:   return f"mouse_click:{x},{y}"
                if btn & _RIGHT_BTN:  return f"mouse_right:{x},{y}"
                if btn & _MIDDLE_BTN: return f"mouse_middle:{x},{y}"
                # button release (btn == 0) → ignore
                continue
            continue
        # other event types (size change, focus, menu) → ignore
        continue


def _read_key() -> str:
    """Cross-platform single-key read. Returns:
       'up','down','left','right','enter','esc','space','backspace','tab',
       'pageup','pagedown','home','end','delete',
       'scroll_up','scroll_down', 'mouse_click:x,y', 'mouse_right:x,y',
       or the actual character.
    """
    if _IS_WINDOWS:
        return _win_read_event()
    else:
        fd  = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                if not select.select([sys.stdin], [], [], 0.005)[0]:
                    return "esc"
                seq = "\x1b"
                while select.select([sys.stdin], [], [], 0.005)[0]:
                    c = sys.stdin.read(1)
                    seq += c
                    if c in ("M", "m", "~"):
                        break
                    if len(seq) <= 3 and c in ("A","B","C","D","H","F","Z"):
                        break
                    if len(seq) > 64:
                        break
                return _parse_escape(seq)
            if ch == "\r" or ch == "\n": return "enter"
            if ch == " ":                return "space"
            if ch == "\x7f":             return "backspace"
            if ch == "\t":               return "tab"
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def _query_cursor_pos() -> tuple:
    """Ask the terminal where the cursor is. Returns (row, col) or (None, None).
    On Windows we use GetConsoleScreenBufferInfo (no terminal cooperation needed).
    """
    if _IS_WINDOWS:
        try:
            kernel32 = ctypes.windll.kernel32
            h_out    = kernel32.GetStdHandle(_STD_OUTPUT)
            csbi     = _CSBI()
            if kernel32.GetConsoleScreenBufferInfo(h_out, ctypes.byref(csbi)):
                # Both the cursor pos and ReadConsoleInput mouse pos are buffer
                # coordinates (0-indexed). Just +1 to match xterm 1-indexed convention.
                return csbi.dwCursorPosition.Y + 1, csbi.dwCursorPosition.X + 1
        except Exception:
            pass
        return None, None
    else:
        fd  = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            sys.stdout.write("\033[6n")
            sys.stdout.flush()
            buf      = ""
            deadline = time.time() + 0.25
            while time.time() < deadline:
                r, _, _ = select.select([sys.stdin], [], [], 0.05)
                if r:
                    buf += sys.stdin.read(1)
                    if buf.endswith("R"):
                        break
            m = re.search(r"\[(\d+);(\d+)R", buf)
            if m: return int(m.group(1)), int(m.group(2))
            return None, None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def _hide(): sys.stdout.write("\033[?25l"); sys.stdout.flush()
def _show(): sys.stdout.write("\033[?25h"); sys.stdout.flush()


class Menu:
    @staticmethod
    def select(title: str, options: list, color: str = "#00ccff",
               cursor: str = "❯ ", mouse: bool = True,
               help_text: str = None) -> str:
        """Returns the selected option (str). Returns None on ESC.

        Supports arrow keys, Enter, ESC — *plus* mouse clicks and scroll wheel
        when ``mouse=True`` (default). Modern terminals (Windows Terminal,
        iTerm2, gnome-terminal, alacritty) detect xterm SGR mouse mode.
        """
        col      = ColorUtils.hex(color)
        gray     = ColorUtils.hex("#6c757d")
        dim      = ColorUtils.hex("#adb5bd")
        reset    = ColorUtils.RESET
        idx      = 0
        n        = len(options)
        rendered = False
        anchor_row = None
        help_text  = help_text or (
            "↑/↓ navigate · click an option · scroll wheel · Enter select · ESC quit"
            if mouse else
            "↑/↓ navigate · Enter select · ESC quit"
        )

        def render():
            nonlocal rendered
            if rendered:
                # move up n+3 lines
                sys.stdout.write(f"\033[{n + 3}A")
            print(f"\n {col}?{reset} {col}{title}{reset}")
            for i, opt in enumerate(options):
                if i == idx:
                    print(f"   {col}{cursor}{opt}{reset}".ljust(80))
                else:
                    print(f"     {dim}{opt}{reset}".ljust(80))
            print(f" {gray}{help_text}{reset}".ljust(80))
            sys.stdout.flush()
            rendered = True

        def click_to_idx(y: int) -> int:
            if anchor_row is None: return -1
            # menu layout (1-indexed rows):
            #   anchor_row     = blank line (the \n at start of "\n {col}?…")
            #   anchor_row + 1 = title line
            #   anchor_row+2.. = option lines
            #   anchor_row+2+n = help line
            opt_idx = y - (anchor_row + 2)
            if 0 <= opt_idx < n:
                return opt_idx
            return -1

        _hide()
        if mouse: _enable_mouse()
        try:
            # measure anchor row BEFORE first render
            cur_row, _ = _query_cursor_pos()
            anchor_row = cur_row
            render()
            while True:
                key = _read_key()
                if   key == "up":     idx = (idx - 1) % n
                elif key == "down":   idx = (idx + 1) % n
                elif key == "scroll_up":   idx = (idx - 1) % n
                elif key == "scroll_down": idx = (idx + 1) % n
                elif key == "pageup":  idx = 0
                elif key == "pagedown": idx = n - 1
                elif key == "home":    idx = 0
                elif key == "end":     idx = n - 1
                elif key == "enter":   return options[idx]
                elif key == "esc":     return None
                elif isinstance(key, str) and key.startswith("mouse_click:"):
                    try:
                        _, coords = key.split(":", 1)
                        _, y = coords.split(",")
                        clicked = click_to_idx(int(y))
                        if clicked >= 0:
                            idx = clicked
                            return options[idx]
                    except Exception:
                        pass
                render()
        finally:
            if mouse: _disable_mouse()
            _show()

    @staticmethod
    def multi_select(title: str, options: list, color: str = "#00ccff",
                     mouse: bool = True,
                     help_text: str = None) -> list:
        col, gray, dim = ColorUtils.hex(color), ColorUtils.hex("#6c757d"), ColorUtils.hex("#adb5bd")
        ok            = ColorUtils.hex("#29bf12")
        reset         = ColorUtils.RESET
        idx           = 0
        n             = len(options)
        selected      = [False] * n
        rendered      = False
        anchor_row    = None
        help_text     = help_text or (
            "↑/↓ · click toggles · scroll · Enter confirm · ESC cancel"
            if mouse else
            "↑/↓ navigate · SPACE toggle · Enter confirm · ESC cancel"
        )

        def render():
            nonlocal rendered
            if rendered:
                sys.stdout.write(f"\033[{n + 3}A")
            print(f"\n {col}?{reset} {col}{title}{reset}")
            for i, opt in enumerate(options):
                mark = f"{ok}[x]{reset}" if selected[i] else f"{gray}[ ]{reset}"
                if i == idx:
                    print(f"   {col}❯{reset} {mark} {col}{opt}{reset}".ljust(80))
                else:
                    print(f"     {mark} {dim}{opt}{reset}".ljust(80))
            print(f" {gray}{help_text}{reset}".ljust(80))
            sys.stdout.flush()
            rendered = True

        def click_to_idx(y: int) -> int:
            if anchor_row is None: return -1
            opt_idx = y - (anchor_row + 2)
            return opt_idx if 0 <= opt_idx < n else -1

        _hide()
        if mouse: _enable_mouse()
        try:
            cur_row, _ = _query_cursor_pos()
            anchor_row = cur_row
            render()
            while True:
                key = _read_key()
                if   key == "up":    idx = (idx - 1) % n
                elif key == "down":  idx = (idx + 1) % n
                elif key == "scroll_up":   idx = (idx - 1) % n
                elif key == "scroll_down": idx = (idx + 1) % n
                elif key == "space": selected[idx] = not selected[idx]
                elif key == "enter": return [opt for opt, s in zip(options, selected) if s]
                elif key == "esc":   return []
                elif isinstance(key, str) and key.startswith("mouse_click:"):
                    try:
                        _, coords = key.split(":", 1)
                        _, y = coords.split(",")
                        clicked = click_to_idx(int(y))
                        if clicked >= 0:
                            idx = clicked
                            selected[idx] = not selected[idx]
                    except Exception:
                        pass
                render()
        finally:
            if mouse: _disable_mouse()
            _show()

    @staticmethod
    def tabs(tabs: list, color: str = "#00ccff", mouse: bool = True,
             help_text: str = None) -> str:
        col   = ColorUtils.hex(color)
        gray  = ColorUtils.hex("#6c757d")
        dim   = ColorUtils.hex("#adb5bd")
        reset = ColorUtils.RESET
        idx   = 0
        n     = len(tabs)
        rendered    = False
        anchor_row  = None
        tab_ranges  = []      # list of (start_col, end_col) per tab on the rendered row
        help_text   = help_text or (
            "←/→ · click a tab · scroll · Enter select · ESC quit"
            if mouse else
            "←/→ navigate · Enter select · ESC quit"
        )

        def render():
            nonlocal rendered, tab_ranges
            if rendered:
                sys.stdout.write("\033[3A")
            parts      = []
            tab_ranges = []
            # the row starts with one leading space (" ") then content
            cur_col = 2  # after "\n " + 1 for the leading space
            for i, t in enumerate(tabs):
                if i == idx:
                    label = f" [ {t} ] "
                    parts.append(f"{col}[ {t} ]{reset} ")
                else:
                    label = f"   {t}   "
                    parts.append(f"  {dim}{t}{reset}   ")
                tab_ranges.append((cur_col, cur_col + len(label) - 1))
                cur_col += len(label) + 1   # +1 for the "│" separator
            print("\n " + "│".join(p for p in parts))
            print(f" {gray}{help_text}{reset}".ljust(80))
            sys.stdout.flush()
            rendered = True

        def click_to_idx(x: int, y: int) -> int:
            if anchor_row is None: return -1
            # tabs render on (anchor_row + 1)  (after the leading \n)
            if y != anchor_row + 1:
                return -1
            for i, (s, e) in enumerate(tab_ranges):
                if s <= x <= e:
                    return i
            return -1

        _hide()
        if mouse: _enable_mouse()
        try:
            cur_row, _ = _query_cursor_pos()
            anchor_row = cur_row
            render()
            while True:
                key = _read_key()
                if   key == "left":  idx = (idx - 1) % n
                elif key == "right": idx = (idx + 1) % n
                elif key == "scroll_up":   idx = (idx - 1) % n
                elif key == "scroll_down": idx = (idx + 1) % n
                elif key == "enter": return tabs[idx]
                elif key == "esc":   return None
                elif isinstance(key, str) and key.startswith("mouse_click:"):
                    try:
                        _, coords = key.split(":", 1)
                        x, y = coords.split(",")
                        clicked = click_to_idx(int(x), int(y))
                        if clicked >= 0:
                            idx = clicked
                            return tabs[idx]
                    except Exception:
                        pass
                render()
        finally:
            if mouse: _disable_mouse()
            _show()


class Prompt:
    @staticmethod
    def text(label: str, default: str = "", color: str = "#00ccff") -> str:
        col   = ColorUtils.hex(color)
        gray  = ColorUtils.hex("#6c757d")
        reset = ColorUtils.RESET
        suffix = f" {gray}[{default}]{reset}" if default else ""
        val   = input(f" {col}❯{reset} {label}{suffix}: ").strip()
        return val or default

    @staticmethod
    def password(label: str = "Password", color: str = "#00ccff") -> str:
        import getpass
        col   = ColorUtils.hex(color)
        reset = ColorUtils.RESET
        return getpass.getpass(f" {col}❯{reset} {label}: ")

    @staticmethod
    def number(label: str, default: int = None, min: int = None, max: int = None,
               color: str = "#00ccff") -> int:
        col   = ColorUtils.hex(color)
        gray  = ColorUtils.hex("#6c757d")
        red   = ColorUtils.hex("#d00000")
        reset = ColorUtils.RESET
        suffix = f" {gray}[{default}]{reset}" if default is not None else ""
        while True:
            raw = input(f" {col}❯{reset} {label}{suffix}: ").strip()
            if not raw and default is not None: return default
            try:
                v = int(raw)
                if min is not None and v < min:
                    print(f"   {red}Must be ≥ {min}{reset}"); continue
                if max is not None and v > max:
                    print(f"   {red}Must be ≤ {max}{reset}"); continue
                return v
            except ValueError:
                print(f"   {red}Enter a valid integer{reset}")

    @staticmethod
    def confirm(label: str, default: bool = True, color: str = "#ffd60a") -> bool:
        col   = ColorUtils.hex(color)
        gray  = ColorUtils.hex("#6c757d")
        reset = ColorUtils.RESET
        suffix = f" {gray}[Y/n]{reset}" if default else f" {gray}[y/N]{reset}"
        raw    = input(f" {col}?{reset} {label}{suffix}: ").strip().lower()
        if not raw: return default
        return raw in ("y", "yes", "s", "si", "sí", "1", "true")

    @staticmethod
    def path(label: str, exists: bool = False, color: str = "#00ccff") -> str:
        col   = ColorUtils.hex(color)
        red   = ColorUtils.hex("#d00000")
        reset = ColorUtils.RESET
        while True:
            p = input(f" {col}❯{reset} {label}: ").strip().strip('"').strip("'")
            if not exists or os.path.exists(p):
                return p
            print(f"   {red}Path does not exist{reset}")

    @staticmethod
    def autocomplete(label: str, options: list, color: str = "#00ccff") -> str:
        """Tab to cycle through filtered matches."""
        col   = ColorUtils.hex(color)
        gray  = ColorUtils.hex("#6c757d")
        reset = ColorUtils.RESET
        buf   = ""
        match_idx = 0
        sys.stdout.write(f" {col}❯{reset} {label}: ")
        sys.stdout.flush()
        while True:
            key = _read_key()
            if key == "enter":
                sys.stdout.write("\n")
                return buf
            elif key == "backspace":
                buf = buf[:-1]
            elif key == "tab":
                matches = [o for o in options if o.lower().startswith(buf.lower())]
                if matches:
                    buf = matches[match_idx % len(matches)]
                    match_idx += 1
            elif key == "esc":
                sys.stdout.write("\n"); return None
            elif len(key) == 1:
                buf += key
                match_idx = 0
            # redraw
            sys.stdout.write("\r\033[K")
            sys.stdout.write(f" {col}❯{reset} {label}: {buf}")
            hint = [o for o in options if o.lower().startswith(buf.lower()) and o != buf]
            if hint:
                sys.stdout.write(f" {gray}({hint[0]}){reset}")
            sys.stdout.flush()


# ─────────────────────────────────────────────────────────────────────────────
# Form
# ─────────────────────────────────────────────────────────────────────────────
class _Field:
    def __init__(self, key, label, kind="text", required=False, default=None,
                 validator=None, options=None, secret=False, type=str, min=None, max=None):
        self.key       = key
        self.label     = label
        self.kind      = kind
        self.required  = required
        self.default   = default
        self.validator = validator
        self.options   = options
        self.secret    = secret
        self.type      = type
        self.min       = min
        self.max       = max


class Form:
    @staticmethod
    def field(key, label, required=False, default=None,
              validator=None, secret=False, type=str, min=None, max=None) -> "_Field":
        return _Field(key, label, kind="text", required=required, default=default,
                      validator=validator, secret=secret, type=type, min=min, max=max)

    @staticmethod
    def choice(key, label, options, default=None) -> "_Field":
        return _Field(key, label, kind="choice", options=options, default=default)

    @staticmethod
    def confirm(key, label, default=True) -> "_Field":
        return _Field(key, label, kind="confirm", default=default)

    @staticmethod
    def is_email(value: str) -> bool:
        import re
        return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", str(value)))

    @staticmethod
    def is_url(value: str) -> bool:
        import re
        return bool(re.match(r"^https?://", str(value)))

    @staticmethod
    def ask(fields: list, title: str = None, color: str = "#00ccff") -> dict:
        col   = ColorUtils.hex(color)
        gray  = ColorUtils.hex("#6c757d")
        red   = ColorUtils.hex("#d00000")
        reset = ColorUtils.RESET
        if title:
            print(f"\n {col}▶ {title}{reset}")
            print(f" {gray}{'─' * 50}{reset}")
        out = {}
        for f in fields:
            while True:
                if f.kind == "text":
                    if f.secret:
                        val = Prompt.password(f.label, color=color)
                    else:
                        val = Prompt.text(f.label, default=f.default or "", color=color)
                    if not val and f.required:
                        print(f"   {red}Required{reset}"); continue
                    if val and f.type is int:
                        try:
                            val = int(val)
                            if f.min is not None and val < f.min:
                                print(f"   {red}Must be ≥ {f.min}{reset}"); continue
                            if f.max is not None and val > f.max:
                                print(f"   {red}Must be ≤ {f.max}{reset}"); continue
                        except ValueError:
                            print(f"   {red}Must be an integer{reset}"); continue
                    if f.validator and not f.validator(val):
                        print(f"   {red}Invalid value{reset}"); continue
                elif f.kind == "choice":
                    val = Menu.select(f.label, f.options, color=color)
                    if val is None: val = f.default
                elif f.kind == "confirm":
                    val = Prompt.confirm(f.label, default=f.default if f.default is not None else True,
                                          color=color)
                out[f.key] = val
                break
        return out


# ─────────────────────────────────────────────────────────────────────────────
# Dashboard — live multi-panel display
# ─────────────────────────────────────────────────────────────────────────────
class Dashboard:
    def __init__(self, title: str = None, border_color: str = "#6c757d",
                 title_color: str = "#00ccff"):
        self.title         = title
        self._border_color = border_color
        self._title_color  = title_color
        self._panels       = {}
        self._panel_order  = []
        self._lock         = threading.Lock()
        self._stop         = False

    def add_panel(self, key: str, position: str = "top-left",
                  width: int = None, height: int = None,
                  title: str = None, color: str = "#ffffff") -> None:
        self._panels[key] = {
            "position": position,
            "width":    width,
            "height":   height,
            "title":    title or key,
            "color":    color,
            "lines":    [],
            "kind":     "text",
            "value":    None,
        }
        if key not in self._panel_order:
            self._panel_order.append(key)

    def update(self, key: str, content) -> None:
        with self._lock:
            p = self._panels.get(key)
            if not p: return
            if isinstance(content, list):
                p["lines"] = [str(x) for x in content]
            else:
                p["lines"] = [str(content)]
            p["kind"] = "text"

    def append(self, key: str, line: str, max_lines: int = None) -> None:
        with self._lock:
            p = self._panels.get(key)
            if not p: return
            p["lines"].append(str(line))
            cap = max_lines or p["height"] or 10
            if len(p["lines"]) > cap:
                p["lines"] = p["lines"][-cap:]

    def set_status(self, key: str, status: str, color: str = "#29bf12") -> None:
        with self._lock:
            p = self._panels.get(key)
            if not p: return
            p["color"] = color
            p["lines"] = [status]

    def clear(self, key: str = None) -> None:
        with self._lock:
            if key:
                if key in self._panels:
                    self._panels[key]["lines"] = []
            else:
                for p in self._panels.values():
                    p["lines"] = []

    def _layout(self) -> dict:
        cols, rows = shutil.get_terminal_size().columns, shutil.get_terminal_size().lines
        rows = max(rows - 2, 10)
        # group panels by row
        positions = {p_id: self._panels[p_id]["position"] for p_id in self._panel_order}
        row_groups = {"top": [], "middle": [], "bottom": []}
        for pid in self._panel_order:
            pos = positions[pid]
            if "top" in pos:        row_groups["top"].append(pid)
            elif "bottom" in pos:   row_groups["bottom"].append(pid)
            else:                   row_groups["middle"].append(pid)

        avail_h     = rows - (2 if self.title else 0)
        row_count   = sum(1 for g in row_groups.values() if g)
        rh          = max(5, avail_h // max(row_count, 1))
        layout      = {}
        cur_y       = 2 if self.title else 1
        for row_name in ("top", "middle", "bottom"):
            group = row_groups[row_name]
            if not group: continue
            count = len(group)
            cw    = cols // count
            cur_x = 1
            for pid in group:
                p = self._panels[pid]
                w = p["width"] or cw
                h = p["height"] or rh
                layout[pid] = (cur_x, cur_y, min(w, cols - cur_x + 1), h)
                cur_x += w
            cur_y += rh
        return layout

    def _render_panel(self, pid: str, x: int, y: int, w: int, h: int) -> None:
        bc    = ColorUtils.hex(self._border_color)
        tc    = ColorUtils.hex(self._title_color)
        reset = ColorUtils.RESET
        p     = self._panels[pid]
        pc    = ColorUtils.hex(p["color"])
        title = p["title"]
        # top border
        sys.stdout.write(f"\033[{y};{x}H{bc}╭─[ {tc}{title}{bc} ]" + "─" * max(0, w - len(title) - 6) + "╮" + reset)
        # body
        lines = p["lines"][-(h-2):] if p["lines"] else []
        for i in range(h - 2):
            line = lines[i] if i < len(lines) else ""
            visible = line[:w-2]
            pad = " " * (w - 2 - len(visible))
            sys.stdout.write(f"\033[{y+1+i};{x}H{bc}│{reset}{pc}{visible}{pad}{bc}│{reset}")
        # bottom border
        sys.stdout.write(f"\033[{y+h-1};{x}H{bc}╰" + "─" * (w - 2) + "╯" + reset)

    def render(self) -> None:
        sys.stdout.write("\033[2J\033[H")
        if self.title:
            tc = ColorUtils.hex(self._title_color)
            sys.stdout.write(f"\033[1;1H {tc}▎ {self.title}{ColorUtils.RESET}")
        with self._lock:
            for pid, (x, y, w, h) in self._layout().items():
                self._render_panel(pid, x, y, w, h)
        sys.stdout.flush()

    def live(self, refresh: float = 10):
        """Context manager — auto refresh at N FPS."""
        return _DashboardLive(self, refresh)


class _DashboardLive:
    def __init__(self, dashboard, fps):
        self.dashboard = dashboard
        self.fps       = fps
        self._stop     = False
        self._thread   = None

    def __enter__(self):
        _hide()
        self.dashboard.render()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        return self.dashboard

    def __exit__(self, *args):
        self._stop = True
        if self._thread:
            self._thread.join(timeout=1)
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        _show()

    def _loop(self):
        delay = 1.0 / max(self.fps, 1)
        while not self._stop:
            self.dashboard.render()
            time.sleep(delay)
