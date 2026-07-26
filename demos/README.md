# Demo recordings

The GIFs in the main README are generated from these
[vhs](https://github.com/charmbracelet/vhs) scripts, so they can be regenerated
whenever the API changes instead of being re-recorded by hand.

## Setup

```bash
winget install charmbracelet.vhs     # Windows
brew install vhs                     # macOS
# Linux: see https://github.com/charmbracelet/vhs#installation
```

vhs pulls in `ttyd` and `ffmpeg`. On Windows, running the tapes from WSL is
smoother than from PowerShell — `ttyd` behaves better there.

## Recording

From this directory, with `c4rlib` installed (`pip install -e ..`):

```bash
vhs intro.tape          # → ../assets/intro.gif
vhs matrix.tape         # → ../assets/matrix.gif
vhs gradients.tape      # → ../assets/gradients.gif
vhs sprites.tape        # → ../assets/sprites.gif
vhs interactive.tape    # → ../assets/interactive.gif
```

Or all of them:

```bash
for tape in *.tape; do vhs "$tape"; done
```

| Tape               | Shows                                              |
| ------------------ | -------------------------------------------------- |
| `intro.tape`       | `FX.intro` with the fireworks style                |
| `matrix.tape`      | `Animations.matrix_rain` full-screen               |
| `gradients.tape`   | `Figlet`, `Gradient`, `Box` and `Banner` output     |
| `sprites.tape`     | `Sprite.move` and `Sprite.parade`                  |
| `interactive.tape` | `Menu.select` driven by keystrokes, plus `Table`    |

## Notes

- `sound=False` everywhere — recordings are silent, and the audio calls block.
- The `Sleep` durations are tuned to each animation's `duration`. If you change
  a `duration` in a tape, change its `Sleep` to match or the GIF cuts off.
- Terminal size is fixed by `Set Width`/`Set Height` so full-screen animations
  compose the same way on every machine.
- Keep the GIFs under about 4 MB each; GitHub renders them inline but large
  files make the README crawl on mobile.
