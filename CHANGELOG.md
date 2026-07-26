# Changelog

All notable changes to **c4rlib** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **`c4rlib` command line entry point.** `pipx run c4rlib` plays the demo reel
  without installing anything; `c4rlib --info` reports the terminal's detected
  capabilities, which is the fastest answer to "why is my output not coloured?".
  Also available as `python -m c4rlib`.

### Fixed
- **`Box.titled` and `Box.multiline` were one character too narrow.** Content
  rows carry two spaces of padding on the left and one on the right, but the
  border was drawn for two — so every multi-line box ever rendered had its
  contents overhanging the frame. Both now measure in display columns as well,
  so CJK and emoji no longer ragged them either.

## [3.1.0] — 2026-07-26

### Security
- **Credential generators now draw from `secrets` instead of `random`.**
  `Utils.generate_token`, `generate_hex_token`, `generate_pin` and
  `generate_password` were built on `random`, a Mersenne Twister whose internal
  state — and therefore every future value — can be reconstructed from enough
  observed output. Anything generated with these functions in an earlier version
  should be considered predictable and rotated. The fake-data generators
  (`random_name`, `random_ipv4`, `random_credit_card`…) still use `random` by
  design; they are fixtures, not credentials, and are now documented as such.

### Added
- **`Terminal` — capability detection and a central colour gate.** Colour is
  emitted only when something can render it: `NO_COLOR` and `FORCE_COLOR` are
  honoured, `TERM=dumb` and non-tty output turn escapes off, and Windows legacy
  consoles are detected. Previously `python app.py > log.txt` wrote raw escape
  sequences into the file.
  - `Terminal.enable_colors(True/False/None)` to force or restore auto-detection.
  - `Terminal.color_depth()` with automatic downgrading: truecolor sequences
    become 256-colour or the nearest of the 16 base colours when that is all the
    terminal supports.
  - `Terminal.display_width()` / `pad_display()` — column-accurate measurement
    that counts CJK and emoji as two and combining marks as zero.
  - `Terminal.strip_ansi()`, `size()`, and `info()` for bug reports.
- `ColorUtils.reset()` — the gated equivalent of the `RESET` constant, which is
  kept for backwards compatibility.
- `ColorUtils.hex_to_rgb` accepts the `#rgb` shorthand and raises `ValueError`
  on malformed input instead of `IndexError`.

### Fixed
- **`Table` measured column widths with `len()`**, so any row containing CJK or
  emoji ragged the borders — a three-character string like `日本語` occupies six
  columns. Widths and padding now use display width.
- **`Table`'s title row was `len(columns)` characters wider than every other
  row.** The inner-width formula counted each column once too often; invisible
  with ASCII titles, obvious once measured.
- `ColorUtils.palette(color, steps=1)` raised `ZeroDivisionError`; it now returns
  a single-entry list, and `steps < 1` returns an empty one.

### Added — repository and tooling
- Public GitHub repository: MIT `LICENSE`, `CONTRIBUTING.md`, issue templates.
- `tests/` — pytest suite (268 tests) covering imports, `__all__` integrity,
  colour maths, crypto vectors, text/utils/files helpers, ANSI escape balance,
  and terminal capability detection.
- `.github/workflows/ci.yml` — build + test matrix on Ubuntu, Windows and macOS
  across Python 3.9, 3.12 and 3.13.
- `.github/workflows/publish.yml` — automatic PyPI release on `v*` tags via
  Trusted Publishing (no long-lived API token).
- `demos/render_gif.py` — regenerates every README GIF from the live API using
  only Pillow. A miniature terminal emulator consumes the library's escape
  sequences while a virtual clock replaces `time.sleep`, so recording is
  deterministic, needs no external tools, and captures exactly the frames the
  animation produces.
- `assets/*.gif` — the rendered gallery: matrix rain, gradients and banners,
  tables and logging, text effects, sprites.

### Changed
- Interactive showcases moved from `tests/` to `examples/`; `tests/` now holds
  actual automated tests.
- `requires-python` raised to `>=3.9`. Python 3.8 reached end of life in
  October 2024 and is no longer covered by CI.
- `PUBLISH.md` moved to `docs/PUBLISHING.md` and rewritten around Trusted
  Publishing and the tag-driven release flow.

## [3.0.3] — 2026-06-20

### Fixed
- Windows mouse input rewritten on top of `ReadConsoleInputW` via `ctypes`.
  `msvcrt.getch()` silently discards `MOUSE_EVENT` records, so clicks and
  scroll never reached `Menu` / `Dashboard` on Windows regardless of console
  mode. Key events keep working through the same event loop.

## [3.0.2] — 2026-06-20

### Fixed
- Windows console modes are now configured explicitly before enabling mouse
  tracking: `ENABLE_MOUSE_INPUT`, `ENABLE_VIRTUAL_TERMINAL_INPUT` and
  `ENABLE_EXTENDED_FLAGS` on, quick-edit mode off (it was consuming
  left-clicks as text selection). Previous modes are restored on exit.
- Added `?1002` (motion-with-button) to the mouse enable sequence.

## [3.0.1] — 2026-06-20

### Added
- Mouse support in interactive widgets via xterm SGR tracking: `scroll_up`,
  `scroll_down`, `mouse_click:x,y`, `mouse_middle:x,y`, `mouse_right:x,y`.
- Extra keys recognised by `_read_key()`: `pageup`, `pagedown`, `home`, `end`,
  `delete`, `shift_tab`.

## [3.0.0] — 2026-06-20

### Added
- **ASCII art** — `Figlet` (400+ fonts), `ImageAscii` (image→ASCII from file or
  URL), `Ascii` (mini-banners, dividers, boxed titles).
- **Animated sprites** — `Sprite` with 15 presets plus `.move()`, `.bounce()`,
  `.shake()`, `.float()`, `.fade_in()`, `.parade()`, `.race()` and custom
  frames via `Sprite.from_frames()`.
- **Full-screen animations** — matrix rain, fireworks, starfield, snow, rain,
  confetti, glitch, scanlines.
- **Text effects** — typewriter, glitch, scramble, fade, slide, wave, shake,
  explode, implode, rainbow scroll, flash, countdown, path-following fly text.
- **Particles** — `Particle.emit()`, `.explosion()`, `.trail()` with spark,
  dust, fire, smoke, bubble and snow kinds.
- **Audio** — cross-platform beeps, 12+ SFX presets, 15 chiptune `Melody`
  presets, WAV playback via `Sound`, and `Logger.enable_sounds()`.
- **Interactive** — `Menu.select / multi_select / tabs`, `Prompt.text /
  password / number / confirm / path / autocomplete`, `Form.ask`, and a live
  `Dashboard`.
- **FX layer** — composed one-liners: `FX.intro`, `FX.outro`, `FX.celebrate`,
  `FX.error_explosion`, `FX.level_up`, `FX.matrix_intro`, `FX.terminal_hack`,
  `FX.boot_sequence`, `FX.demo_all`.

## [2.0.1] and earlier

Released before the changelog was kept. Core toolkit: `ColorUtils`,
`Gradient`, `Logger`, `Box`, `Banner`, `TextStyle`, `Spinner`, `ProgressBar`,
`Table`, `Console`, `Http`, `Crypto`, `Files`, `Discord`, `Utils`.

[Unreleased]: https://github.com/C4rI0s/c4rlib/compare/v3.1.0...HEAD
[3.1.0]: https://github.com/C4rI0s/c4rlib/compare/v3.0.3...v3.1.0
[3.0.3]: https://github.com/C4rI0s/c4rlib/compare/v3.0.2...v3.0.3
[3.0.2]: https://github.com/C4rI0s/c4rlib/compare/v3.0.1...v3.0.2
[3.0.1]: https://github.com/C4rI0s/c4rlib/compare/v3.0.0...v3.0.1
[3.0.0]: https://github.com/C4rI0s/c4rlib/releases/tag/v3.0.0
