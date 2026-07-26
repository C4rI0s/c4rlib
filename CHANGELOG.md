# Changelog

All notable changes to **c4rlib** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Public GitHub repository: MIT `LICENSE`, `CONTRIBUTING.md`, issue templates.
- `tests/` — pytest suite covering imports, `__all__` integrity, colour maths,
  crypto vectors, text/utils/files helpers, and ANSI escape balance.
- `.github/workflows/ci.yml` — build + test matrix on Ubuntu, Windows and macOS
  across Python 3.9, 3.12 and 3.13.
- `.github/workflows/publish.yml` — automatic PyPI release on `v*` tags via
  Trusted Publishing (no long-lived API token).
- `demos/*.tape` — reproducible [vhs](https://github.com/charmbracelet/vhs)
  scripts that regenerate the README GIFs.

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

[Unreleased]: https://github.com/C4rI0s/c4rlib/compare/v3.0.3...HEAD
[3.0.3]: https://github.com/C4rI0s/c4rlib/compare/v3.0.2...v3.0.3
[3.0.2]: https://github.com/C4rI0s/c4rlib/compare/v3.0.1...v3.0.2
[3.0.1]: https://github.com/C4rI0s/c4rlib/compare/v3.0.0...v3.0.1
[3.0.0]: https://github.com/C4rI0s/c4rlib/releases/tag/v3.0.0
