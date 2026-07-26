"""`python -m c4rlib` / `c4rlib` — see the library without writing any code.

    pipx run c4rlib          # no install, just the show
    python -m c4rlib         # in a checkout or after pip install
    c4rlib --info            # what this terminal supports
"""
import sys

from . import __version__
from .terminal import Terminal

USAGE = """c4rlib {version} — showtime CLI toolkit for Python

  c4rlib               play the demo reel
  c4rlib --quiet       the reel, without sound
  c4rlib --info        report this terminal's capabilities
  c4rlib --version     print the version
  c4rlib --help        this message

Docs: https://github.com/C4rI0s/c4rlib
"""


def show_info() -> int:
    from .banners import Box
    from .colors import ColorUtils

    info  = Terminal.info()
    width = max(len(k) for k in info)
    lines = [f"{k.ljust(width)}  {v}" for k, v in info.items()]
    print(Box.titled("terminal", lines, title_color="#00ccff"))

    if not info["colors_enabled"]:
        print(ColorUtils.paint(
            "\ncolour is off — output is redirected, NO_COLOR is set, or the "
            "terminal reports no support.\nForce it with FORCE_COLOR=1 or "
            "Terminal.enable_colors(True).", "#ffd60a"))
    return 0


def play(sound: bool) -> int:
    from .fx import FX

    if not Terminal.is_tty():
        print("c4rlib: the demo needs a real terminal — this output is redirected.",
              file=sys.stderr)
        return 1
    try:
        FX.demo_all(skip_audio=not sound)
    except KeyboardInterrupt:
        from .console import Console
        Console.show_cursor()
        print("\ninterrupted")
        return 130
    return 0


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    if "--help" in args or "-h" in args:
        print(USAGE.format(version=__version__))
        return 0
    if "--version" in args or "-V" in args:
        print(__version__)
        return 0
    if "--info" in args:
        return show_info()

    sound = not ("--quiet" in args or "-q" in args)
    unknown = [a for a in args if a not in ("--quiet", "-q")]
    if unknown:
        print(f"c4rlib: unknown option(s): {' '.join(unknown)}\n", file=sys.stderr)
        print(USAGE.format(version=__version__), file=sys.stderr)
        return 2
    return play(sound)


if __name__ == "__main__":
    sys.exit(main())
