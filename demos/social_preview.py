#!/usr/bin/env python3
"""Generate the GitHub social preview card — assets/social-preview.png.

GitHub renders every shared link as a plain grey card unless a 1280x640 image is
uploaded under Settings -> Social preview. There is no API for that upload, so
this script only produces the file; putting it in place is a manual step.

    python demos/social_preview.py

The card is drawn from the library's own output, so it always shows what the
library actually renders.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from PIL import Image                                          # noqa: E402

from render_gif import (BACKGROUND, CJK_FONT_CANDIDATES, Screen,   # noqa: E402
                        load_font, render_frame)

WIDTH, HEIGHT = 1280, 640
FONT_SIZE = 20


def indent(block, spaces=3):
    """Indent every line of a block — indenting only the first one shifts the
    top border of a box away from the rest of it."""
    pad = " " * spaces
    return "\n".join(pad + line for line in block.split("\n"))


def compose():
    """Render the card content through the terminal emulator."""
    from c4rlib import Ascii, Banner, Figlet, Gradient, Terminal

    Terminal.enable_colors(True)
    screen = Screen(cols=62, rows=16)
    try:
        screen.write("\n")
        screen.write(indent(Figlet.gradient("c4rlib", font="standard",
                                            start=(0, 200, 255), end=(200, 0, 255))))
        screen.write("\n")
        screen.write(indent(Gradient.apply(
            "showtime CLI toolkit for Python", (0, 200, 255), (200, 0, 255)), 6))
        screen.write("\n\n")
        screen.write(indent(Ascii.divider("zigzag", width=52, color="#f5c2e7")))
        screen.write("\n\n")
        screen.write(indent("   ".join([
            Gradient.fire("animations"), Gradient.ice("ascii art"),
            Gradient.toxic("sprites"), Gradient.galaxy("audio"),
        ]), 4))
        screen.write("\n")
        screen.write(indent("   ".join([
            Gradient.aurora("menus"), Gradient.electric("gradients"),
            Gradient.candy("progress bars"),
        ]), 4))
        screen.write("\n\n")
        screen.write(indent(Banner.gradient_title("pipx run c4rlib"), 4))
    finally:
        Terminal.enable_colors(None)
    return screen.snapshot()


def main():
    grid = compose()
    font     = load_font(FONT_SIZE)
    cjk_font = load_font(FONT_SIZE, CJK_FONT_CANDIDATES, required=False)
    cell_w   = max(1, round(font.getlength("M")))
    ascent, descent = font.getmetrics()
    cell_h   = ascent + descent

    rendered = render_frame(grid, font, cell_w, cell_h,
                            len(grid), len(grid[0]), cjk_font)

    # Centre the rendering on an exactly 1280x640 canvas — GitHub crops anything
    # that is not that ratio.
    card = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    scale = min(WIDTH / rendered.width, HEIGHT / rendered.height, 1.0)
    if scale < 1.0:
        rendered = rendered.resize(
            (int(rendered.width * scale), int(rendered.height * scale)),
            Image.LANCZOS)
    card.paste(rendered, ((WIDTH - rendered.width) // 2,
                          (HEIGHT - rendered.height) // 2))

    out = ROOT / "assets" / "social-preview.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    card.save(out, optimize=True)
    print(f"-> {out.relative_to(ROOT)}  {card.width}x{card.height}, "
          f"{out.stat().st_size / 1024:.0f} KB")
    print("Upload it at Settings -> Social preview (there is no API for this).")


if __name__ == "__main__":
    main()
