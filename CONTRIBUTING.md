# Contributing to c4rlib

Thanks for wanting to make the terminal louder.

## Getting set up

```bash
git clone https://github.com/C4rI0s/c4rlib.git
cd c4rlib
python -m venv .venv
# Windows:  .venv\Scripts\activate
# Unix:     source .venv/bin/activate
pip install -e ".[dev]"
```

## Running things

```bash
pytest                        # automated tests
python examples/showcase.py   # interactive walkthrough of every module
python examples/test.py       # scripted feature tour
```

Note that `pytest` covers only the deterministic surface. Animations, audio,
sprites and interactive widgets depend on real time, a keyboard and an audio
device, so they are verified by eye through `examples/`. If you touch them, say
in your PR which terminal and OS you tested on.

## What a good contribution looks like

**New effects, sprites, gradients, melodies and fonts are very welcome.** So are
bug fixes for terminal quirks — those are the hardest thing to get right across
Windows Terminal, iTerm2, gnome-terminal, alacritty and friends.

A few conventions the codebase holds to:

- **Renderers return strings; players print.** Anything named `render`, `apply`,
  `gradient` or similar returns a `str` and writes nothing to stdout. Anything
  that animates prints and returns `None`. Keeping that split is what makes the
  library composable.
- **Every escape sequence you open, you close.** A colour without its reset
  leaks into the user's prompt long after your function returned.
  `tests/test_ansi_purity.py` enforces this — add your renderer to it.
- **Platform-specific imports stay inside the branch that needs them.**
  `winsound`, `msvcrt`, `ctypes.wintypes`, `termios` and `tty` must never be
  imported at module scope unconditionally.
- **Degrade, don't crash.** No audio device, no truecolor, a 40-column
  terminal — the call should still do something reasonable. `Audio` already
  models this with `is_available()`.
- **Only two runtime dependencies** (`pyfiglet`, `pillow`), and both are used
  lazily. Adding a third needs a good argument.
- Type hints on public signatures, four-space indent, no trailing whitespace.

## Pull requests

1. Branch off `main`.
2. Add or update tests where the behaviour is deterministic.
3. Add a `CHANGELOG.md` entry under `## [Unreleased]`.
4. Make sure CI is green on all three operating systems.

Don't bump `version` in `pyproject.toml` — releases are cut by tag.

## Reporting bugs

Terminal bugs are environment bugs. Please include your OS, terminal emulator,
Python version, `c4rlib` version, and what you saw versus what you expected. A
screenshot or asciinema recording is worth a lot for anything visual.

## Releases

Maintainers only — see [docs/PUBLISHING.md](docs/PUBLISHING.md).
