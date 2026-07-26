# Demo recordings

The GIFs in the main README are generated from code, not recorded by hand, so
they can never drift from what the library actually does.

## The default: `render_gif.py`

```bash
python demos/render_gif.py            # regenerate every GIF into assets/
python demos/render_gif.py matrix     # just one
```

Needs nothing but Pillow, which `c4rlib` already depends on. Run it from the
repository root.

How it works: a small terminal emulator consumes the escape sequences the
library emits, `sys.stdout` is redirected into it, and `time.sleep` is replaced
by a function that records a frame and advances a **virtual clock** that
`time.time` then reads. Two consequences worth knowing:

- Frames come from the library's own frame boundaries, so nothing is sampled,
  missed or duplicated.
- Recording runs as fast as the CPU allows and is deterministic — a four-second
  animation does not take four seconds to render, and produces the same GIF
  every time.

Each demo is a plain function in the `DEMOS` table at the bottom of the file,
with its font size, frame cap and palette size. Add one there to add a GIF.

| GIF                    | Shows                                            |
| ---------------------- | ------------------------------------------------ |
| `assets/matrix.gif`    | `Animations.matrix_rain`                          |
| `assets/gradients.gif` | `Figlet`, `Gradient`, `Box`, `Banner`, `Ascii`    |
| `assets/table.gif`     | `Table` with a title and zebra rows, plus `Logger`|
| `assets/effects.gif`   | `Effect.typewriter / scramble / wave / glitch`    |
| `assets/sprites.gif`   | `Sprite.move` with bob                            |

### Fonts

The renderer looks for a monospace TTF (Consolas, DejaVu Sans Mono, Menlo) and
a CJK fallback (MS Gothic, Yu Gothic, Noto Sans CJK). The fallback matters:
`matrix_rain` is full of katakana, which Latin monospace fonts render as tofu.

## Why not vhs?

[vhs](https://github.com/charmbracelet/vhs) captures a real terminal and is the
obvious tool for this, but it drives a headless Chromium against a `ttyd`
server, and that combination hangs on Windows even with vhs, ttyd, ffmpeg and
Chrome all installed. Since these GIFs have to be regeneratable by anyone on any
platform — and in CI — `render_gif.py` is the supported path. If you prefer vhs
on Linux or macOS, the demo functions in `render_gif.py` are a direct
translation guide for writing tapes.

## Notes

- `sound=False` everywhere — recordings are silent and the audio calls block.
- Keep each GIF under about 4 MB. `render_gif.py` warns when one goes over and
  the per-demo `max_frames` and font size are the knobs to turn.
- `Terminal.enable_colors(True)` is forced during recording, since stdout is
  redirected and would otherwise correctly suppress all colour.
