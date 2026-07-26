import datetime
from .colors import ColorUtils, Gradient, GradientPresets


_SOUND_ENABLED = False
_SOUND_MAP = {
    "SUC": "success",
    "ERR": "error",
    "WAR": "warning",
    "CRT": "alarm",
    "DON": "success",
    "LCK": "click",
    "ULK": "pop",
}


def _maybe_sound(label: str) -> None:
    if not _SOUND_ENABLED: return
    try:
        from .audio import Audio
        kind = _SOUND_MAP.get(label)
        if kind == "success": Audio.play_async(Audio.success)
        elif kind == "error": Audio.play_async(Audio.error)
        elif kind == "warning": Audio.play_async(Audio.warning)
        elif kind == "alarm": Audio.play_async(Audio.alarm, 1)
        elif kind == "click": Audio.play_async(Audio.click)
        elif kind == "pop":   Audio.play_async(Audio.pop)
    except Exception:
        pass


def _ts() -> str:
    return "{:%H:%M:%S}".format(datetime.datetime.now())


def _base(level_color: str, symbol: str, label: str, *parts) -> None:
    ts  = f"{ColorUtils.hex('#6c757d')}{_ts()}{ColorUtils.RESET}"
    sym = f"{ColorUtils.hex(level_color)}{symbol}{ColorUtils.RESET}"
    lbl = f"{ColorUtils.hex(level_color)}{label}{ColorUtils.RESET}"
    msg = f"  {ColorUtils.hex('#00ccff')}{ColorUtils.RESET}".join(str(p) for p in parts)
    print(f" [{ts}] {ColorUtils.hex('#6c757d')}|{ColorUtils.RESET} {sym} {ColorUtils.hex('#6c757d')}|{ColorUtils.RESET} {lbl} {ColorUtils.hex('#6c757d')}>{ColorUtils.RESET} {msg}")
    _maybe_sound(label)


class Logger:
    @staticmethod
    def success(*parts) -> None:
        _base("#29bf12", "✔", "SUC", *parts)

    @staticmethod
    def error(*parts) -> None:
        _base("#d00000", "✘", "ERR", *parts)

    @staticmethod
    def info(*parts) -> None:
        _base("#2a9d8f", "ℹ", "INF", *parts)

    @staticmethod
    def warning(*parts) -> None:
        _base("#ffd60a", "⚠", "WAR", *parts)

    @staticmethod
    def debug(*parts) -> None:
        _base("#ff7b00", "⚙", "DBG", *parts)

    @staticmethod
    def critical(*parts) -> None:
        _base("#ff0000", "☠", "CRT", *parts)

    @staticmethod
    def network(*parts) -> None:
        _base("#4361ee", "⇄", "NET", *parts)

    @staticmethod
    def input(*parts) -> None:
        _base("#9b5de5", "→", "INP", *parts)

    @staticmethod
    def output(*parts) -> None:
        _base("#00bbf9", "←", "OUT", *parts)

    @staticmethod
    def captcha(*parts) -> None:
        _base("#fcf300", "$", "CAP", *parts)

    @staticmethod
    def proxy(*parts) -> None:
        _base("#06d6a0", "⬡", "PRX", *parts)

    @staticmethod
    def token(*parts) -> None:
        _base("#f72585", "⚿", "TKN", *parts)

    @staticmethod
    def upload(*parts) -> None:
        _base("#4cc9f0", "↑", "UPL", *parts)

    @staticmethod
    def download(*parts) -> None:
        _base("#4cc9f0", "↓", "DWN", *parts)

    @staticmethod
    def database(*parts) -> None:
        _base("#7209b7", "⛁", "DBS", *parts)

    @staticmethod
    def file(*parts) -> None:
        _base("#3a86ff", "⎗", "FIL", *parts)

    @staticmethod
    def crypto(*parts) -> None:
        _base("#fb8500", "⚷", "CRY", *parts)

    @staticmethod
    def wait(*parts) -> None:
        _base("#adb5bd", "◌", "WAI", *parts)

    @staticmethod
    def done(*parts) -> None:
        _base("#80ffdb", "◉", "DON", *parts)

    @staticmethod
    def send(*parts) -> None:
        _base("#48cae4", "➤", "SND", *parts)

    @staticmethod
    def receive(*parts) -> None:
        _base("#48cae4", "◄", "RCV", *parts)

    @staticmethod
    def locked(*parts) -> None:
        _base("#ef233c", "🔒", "LCK", *parts)

    @staticmethod
    def unlocked(*parts) -> None:
        _base("#06d6a0", "🔓", "ULK", *parts)

    @staticmethod
    def custom(hex_color: str, symbol: str, label: str, *parts) -> None:
        _base(hex_color, symbol, label, *parts)

    @staticmethod
    def enable_sounds() -> None:
        """Each log level emits a small sound (success/error/warning/critical)."""
        global _SOUND_ENABLED
        _SOUND_ENABLED = True

    @staticmethod
    def disable_sounds() -> None:
        global _SOUND_ENABLED
        _SOUND_ENABLED = False

    @staticmethod
    def sounds_enabled() -> bool:
        return _SOUND_ENABLED

    @staticmethod
    def gradient_log(text: str, start: tuple = (0,200,255), end: tuple = (200,0,255)) -> None:
        ts  = f"{ColorUtils.hex('#6c757d')}{_ts()}{ColorUtils.RESET}"
        msg = Gradient.apply(text, start, end)
        print(f" [{ts}] {ColorUtils.hex('#6c757d')}|{ColorUtils.RESET} ✦ {ColorUtils.hex('#6c757d')}|{ColorUtils.RESET} {msg}")

    @staticmethod
    def banner_log(text: str, hex_color: str = "#00ccff") -> None:
        ts  = f"{ColorUtils.hex('#6c757d')}{_ts()}{ColorUtils.RESET}"
        col = ColorUtils.hex(hex_color)
        bar = f"{col}{'━' * (len(text) + 6)}{ColorUtils.RESET}"
        print(f" [{ts}]\n {bar}\n  {col}  {text}  {ColorUtils.RESET}\n {bar}")

    @staticmethod
    def fire(*parts) -> None:
        ts  = f"{ColorUtils.hex('#6c757d')}{_ts()}{ColorUtils.RESET}"
        msg = Gradient.fire(" ".join(str(p) for p in parts))
        print(f" [{ts}] {ColorUtils.hex('#6c757d')}|{ColorUtils.RESET} 🔥 {ColorUtils.hex('#6c757d')}|{ColorUtils.RESET} {msg}")

    @staticmethod
    def galaxy(*parts) -> None:
        ts  = f"{ColorUtils.hex('#6c757d')}{_ts()}{ColorUtils.RESET}"
        msg = Gradient.galaxy(" ".join(str(p) for p in parts))
        print(f" [{ts}] {ColorUtils.hex('#6c757d')}|{ColorUtils.RESET} 🌌 {ColorUtils.hex('#6c757d')}|{ColorUtils.RESET} {msg}")

    @staticmethod
    def neon(*parts) -> None:
        ts  = f"{ColorUtils.hex('#6c757d')}{_ts()}{ColorUtils.RESET}"
        msg = Gradient.neon(" ".join(str(p) for p in parts))
        print(f" [{ts}] {ColorUtils.hex('#6c757d')}|{ColorUtils.RESET} ⚡ {ColorUtils.hex('#6c757d')}|{ColorUtils.RESET} {msg}")
