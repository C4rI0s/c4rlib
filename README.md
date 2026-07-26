<div align="center">

# c4rlib

**Showtime CLI toolkit for Python.**

[![PyPI](https://img.shields.io/pypi/v/c4rlib?color=00ccff&label=pypi)](https://pypi.org/project/c4rlib/)
[![Python](https://img.shields.io/pypi/pyversions/c4rlib?color=00ccff)](https://pypi.org/project/c4rlib/)
[![CI](https://github.com/C4rI0s/c4rlib/actions/workflows/ci.yml/badge.svg)](https://github.com/C4rI0s/c4rlib/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-c800ff)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/c4rlib?color=c800ff)](https://pypi.org/project/c4rlib/)

</div>

> Colors, gradients, logging, spinners, progress bars, tables, HTTP, crypto, files, Discord helpers — *plus* ASCII art (FIGlet, image→ASCII, animated sprites), full-screen terminal animations (matrix rain, fireworks, glitch…), cross-platform audio, interactive menus / forms / dashboards, and the **FX** layer that composes everything into one-liner intros, hacker-movie sequences, and celebrations.

```bash
pip install c4rlib
```

`pyfiglet` and `pillow` are installed automatically. No other runtime dependencies.

---

## Gallery

> **Recordings pending.** The demos are scripted as reproducible
> [vhs](https://github.com/charmbracelet/vhs) tapes in [`demos/`](demos/) rather
> than hand-recorded, so they can be regenerated whenever the API changes. Run
> them once to produce the GIFs, then replace each line below with its image.

| Demo                                             | Tape                  | Output                 |
| ------------------------------------------------ | --------------------- | ---------------------- |
| `FX.intro` with fireworks                        | `demos/intro.tape`      | `assets/intro.gif`       |
| `Animations.matrix_rain` full-screen             | `demos/matrix.tape`     | `assets/matrix.gif`      |
| `Figlet` + `Gradient` + `Box` + `Banner`         | `demos/gradients.tape`  | `assets/gradients.gif`   |
| `Sprite.move` and `Sprite.parade`                | `demos/sprites.tape`    | `assets/sprites.gif`     |
| `Menu.select` driven by keystrokes, plus `Table` | `demos/interactive.tape`| `assets/interactive.gif` |

```bash
cd demos && for tape in *.tape; do vhs "$tape"; done
```

---

## Table of Contents

- [Gallery](#gallery)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Showcase demo](#showcase-demo)
- [Terminal (colour gate & capabilities)](#terminal)
- **Visual**
  - [ColorUtils](#colorutils)
  - [Gradient](#gradient)
  - [Box & Banner](#box--banner)
  - [TextStyle](#textstyle)
  - [Figlet](#figlet)
  - [ImageAscii](#imageascii)
  - [Ascii (dividers, mini-banners)](#ascii)
- **Motion**
  - [Sprite (animated ASCII)](#sprite)
  - [Animations (full-screen FX)](#animations)
  - [Effect (text effects)](#effect)
  - [Particle](#particle)
- **Sound**
  - [Audio](#audio)
  - [Sound](#sound)
  - [Melody](#melody)
- **Interactivity**
  - [Menu](#menu)
  - [Prompt](#prompt)
  - [Form](#form)
  - [Dashboard](#dashboard)
- **Compositions**
  - [FX — showcases](#fx)
- **Output primitives**
  - [Logger](#logger)
  - [Spinner](#spinner)
  - [ProgressBar](#progressbar)
  - [Table](#table)
  - [Console](#console)
- **Infra**
  - [Http](#http)
  - [Crypto](#crypto)
  - [Files](#files)
  - [Discord](#discord)
  - [Utils](#utils)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

```bash
pip install c4rlib
```

Requires Python 3.9+. Auto-installs `pyfiglet` and `pillow`.

---

## Quickstart

```python
from c4rlib import FX, Sprite, Logger, Menu

FX.intro("My App", subtitle="v1.0.0", style="fireworks", sound=True)

Sprite.preset("ghost", color="#a78bfa").move(from_x=2, to_x=70, duration=2.5, bob=True)

choice = Menu.select("Pick one", options=["Start", "Settings", "Quit"])
Logger.success("CHOICE", choice)
```

---

## Showcase demo

A full interactive walkthrough of every module is bundled in the repo:

```bash
git clone https://github.com/C4rI0s/c4rlib.git
cd c4rlib
python examples/showcase.py
```

Pick a section from the arrow-key menu (15 demos) or run `FX.demo_all()` for the auto-playing reel.

---

## Terminal

Every escape sequence the library produces passes through here. Colour is
emitted only when something can render it, so redirecting output no longer fills
the file with escape codes.

```python
from c4rlib import Terminal

Terminal.colors_enabled()      # False when piped, when NO_COLOR is set, or TERM=dumb
Terminal.color_depth()         # 'truecolor' | '256' | '16' | 'none'
Terminal.info()                # everything detection concluded — paste this in bug reports
```

Detection is automatic, and honours the de-facto standards:

| Signal                    | Effect                                    |
| ------------------------- | ----------------------------------------- |
| `NO_COLOR` set (any value) | colour off — wins over everything          |
| `FORCE_COLOR` set, not `0` | colour on even when piped (useful in CI)   |
| `TERM=dumb`                | colour off                                 |
| stdout is not a terminal   | colour off                                 |
| Windows legacy console     | colour off if VT processing is unavailable  |

Override it when you need to:

```python
Terminal.enable_colors(True)    # force on — e.g. writing to a file you'll `less -R`
Terminal.disable_colors()       # force off
Terminal.enable_colors(None)    # back to automatic
```

Truecolor is **downgraded, not dropped**, on terminals that can't do 24-bit:
`Gradient.fire("text")` renders through the 256-colour cube or the 16 base
colours as needed, so gradients degrade instead of breaking.

Width helpers, because `len()` is the wrong measure for anything you align:

```python
Terminal.display_width("日本語")           # 6, not 3 — CJK and emoji are two columns
Terminal.pad_display("日本", 6, "center")  # pads by columns, not characters
Terminal.strip_ansi(text)                  # removes colour, cursor moves, erases
Terminal.size()                            # (columns, rows)
```

---

## ColorUtils

Apply ANSI colors, styles, and manipulate colors.

```python
from c4rlib import ColorUtils

ColorUtils.paint("text", "#FF4444")
ColorUtils.bg_paint("text", "#000000", "#00ccff")
ColorUtils.bold("text")
ColorUtils.italic("text")
ColorUtils.underline("text")
ColorUtils.strike("text")
ColorUtils.blink("text")
ColorUtils.dim("text")
ColorUtils.overline("text")
ColorUtils.rainbow("text")
ColorUtils.random_color("text")
ColorUtils.style("text", "#FF0000", bold=True, italic=True)

ColorUtils.hex_to_rgb("#00ccff")
ColorUtils.rgb_to_hex(0, 204, 255)
ColorUtils.rgb_to_hsl(0, 204, 255)
ColorUtils.blend("#FF0000", "#0000FF", 0.5)
ColorUtils.lighten("#FF0000", 0.2)
ColorUtils.darken("#FF0000", 0.2)
ColorUtils.complementary("#FF0000")
ColorUtils.palette("#00ccff", steps=5)
ColorUtils.triadic("#FF0000")
```

---

## Gradient

Apply gradient color effects to text.

```python
from c4rlib import Gradient, GradientPresets

Gradient.apply("text", start=(255,0,0), end=(0,0,255))
Gradient.preset("text", GradientPresets.cyan_to_gold)
Gradient.multicolor("text", [(255,0,0), (0,255,0), (0,0,255)])
Gradient.random_gradient("text")
Gradient.bg_apply("text", start=(0,0,0), end=(100,0,200))

Gradient.fire("text")
Gradient.ice("text")
Gradient.toxic("text")
Gradient.sunset("text")
Gradient.ocean("text")
Gradient.galaxy("text")
Gradient.neon("text")
Gradient.matrix("text")
Gradient.lava("text")
Gradient.candy("text")
Gradient.aurora("text")
Gradient.electric("text")
Gradient.rose("text")
```

**GradientPresets** — 60+ presets: `fire`, `ice`, `toxic`, `sunset`, `ocean`, `galaxy`, `candy`, `matrix`, `lava`, `aurora`, `blood`, `mint`, `rose`, `electric`, `neon_pink_purple`, `neon_green_blue`, `red_to_blue`, `cyan_to_gold`, `purple_to_pink`, and many more.

---

## Box & Banner

```python
from c4rlib import Box, Banner

Box.rounded("text", color="#00ccff")
Box.double("text", color="#9b5de5")
Box.heavy("text", color="#29bf12")
Box.simple("text", color="#ffd60a")
Box.dots("text", color="#ff7b00")
Box.stars("text", color="#FF69B4")
Box.diamond("text", color="#00bbf9")
Box.arrows("text", color="#f72585")
Box.neon("text", color="#00ccff")
Box.gradient_box("text", start=(0,200,255), end=(200,0,255))
Box.multiline(["line 1", "line 2"], style="rounded", color="#00ccff")
Box.titled("TITLE", ["line 1", "line 2"], style="double", title_color="#ffd60a")

Banner.line("text", color="#00ccff")
Banner.double_line("text", color="#9b5de5")
Banner.arrow_line("text", color="#ffd60a")
Banner.heart_line("text", color="#FF69B4")
Banner.wave_line("text", color="#29bf12")
Banner.gradient_banner("text")
Banner.title("text", color="#00ccff")
Banner.gradient_title("text")
Banner.section("text", color="#00ccff")

# NEW in v3 — giant FIGlet-rendered banner
Banner.giant("MY APP", font="standard", color="#00ccff")
Banner.print_giant("MY APP", gradient=((0,200,255), (200,0,255)))
```

---

## TextStyle

Transform text into different Unicode and styled formats.

```python
from c4rlib import TextStyle

TextStyle.fancy("text")
TextStyle.double_struck("text")
TextStyle.cursive("text")
TextStyle.fraktur("text")
TextStyle.bold_serif("text")
TextStyle.sans_bold("text")
TextStyle.monospace("text")
TextStyle.small_caps("text")
TextStyle.wide("text")
TextStyle.bubble("text")
TextStyle.negative_square("text")
TextStyle.leet("text")
TextStyle.alternate_case("text")
TextStyle.reverse("text")
TextStyle.strikethrough("text")
TextStyle.uwuify("hello world")
TextStyle.zalgo("text", intensity=3)
TextStyle.rot13("text")
TextStyle.caesar("text", shift=3)
TextStyle.morse("sos")
TextStyle.nato("sos")
TextStyle.binary("hi")
TextStyle.hex_encode("hi")
TextStyle.clap("text here")
TextStyle.space_out("text", spaces=2)
TextStyle.truncate("long text here", max_len=10)
TextStyle.wrap("long paragraph text here", width=40)
```

---

## Figlet

🆕 **v3** — full FIGlet rendering with 400+ fonts.

```python
from c4rlib import Figlet

Figlet.render("HELLO", font="standard")               # str
Figlet.print("HELLO", font="slant", color="#00ccff")
Figlet.print_gradient("HELLO", font="big",
                      start=(0,200,255), end=(200,0,255))
Figlet.print_gradient("HELLO", vertical=True)         # gradient row by row
Figlet.rainbow("HELLO")
Figlet.boxed("HELLO", font="standard", color="#ffd60a")

Figlet.list_fonts()                                   # ~400 fonts
Figlet.preview_all("Hi", limit=10)                    # sample a few
```

---

## ImageAscii

🆕 **v3** — convert any image to colored ASCII.

```python
from c4rlib import ImageAscii

ImageAscii.from_file("logo.png", width=80, color=True)
ImageAscii.from_url("https://example.com/cat.jpg", width=120, charset="blocks")
ImageAscii.print("photo.jpg", width=100, color=True, invert=False)
ImageAscii.save("photo.jpg", "photo.txt", color=False)

ImageAscii.charsets          # ['dense','blocks','sparse','binary','emoji','ascii']
```

---

## Ascii

🆕 **v3** — mini-FIGlet (works without pyfiglet), dividers, boxed titles.

```python
from c4rlib import Ascii

Ascii.banner("HELLO", style="block", color="#00ccff")
Ascii.print("HELLO")
Ascii.gradient("HELLO", start=(0,200,255), end=(200,0,255))

Ascii.divider("zigzag", width=80, color="#9b5de5")
# styles: zigzag, wave, dots, dash, double, stars, hash, lightning, fire, heart, diamond
Ascii.print_divider("lightning")
Ascii.boxed_title("My App", subtitle="v3.0.0", color="#00ccff")
```

---

## Sprite

🆕 **v3** — animated ASCII sprites: 15 presets + custom frames.

```python
from c4rlib import Sprite

Sprite.PRESETS
# ['ghost','ufo','skull','cat','dog','fish','rocket','dragon',
#  'car','ball','heart','bird','spider','robot','pacman']

ghost = Sprite.preset("ghost", color="#a78bfa")
ghost.move(from_x=2, to_x=70, duration=3.0, bob=True)   # cross the screen
ghost.bounce(times=5, color="#FF69B4", height=8)
ghost.shake(duration=1.0, intensity=2)
ghost.float(amplitude=2, duration=4.0)
ghost.fade_in(duration=0.5)
ghost.fade_out(duration=0.5)
ghost.play(duration=3.0)                                # play frames in place

# Custom sprite
my = Sprite.from_frames([
    " (o_o) ",
    " (^_^) ",
    " (>_<) ",
], fps=4, color="#FF69B4")
my.move(from_x=0, to_x=60, duration=4.0)

# Compositions
Sprite.parade(["ghost", "ufo", "rocket"], speed=25, gap=8)
Sprite.race(["car", "rocket", "ufo"], length=70)        # returns winner name
```

---

## Animations

🆕 **v3** — full-screen visual effects.

```python
from c4rlib import Animations

Animations.matrix_rain(duration=5.0, color="#00ff41", density=0.7)
Animations.fireworks(count=8, duration=5.0, colors=["#ff4444","#ffd60a","#00ccff"])
Animations.starfield(duration=4.0, density=0.3)
Animations.snow(duration=6.0)
Animations.rain(duration=5.0)
Animations.confetti(duration=3.0)
Animations.glitch_screen(duration=1.5)
Animations.scanlines(duration=3.0, color="#00ff41")
```

---

## Effect

🆕 **v3** — text-level effects.

```python
from c4rlib import Effect

Effect.typewriter("Hello world", delay=0.05, color="#00ccff", sound=True)
Effect.glitch("Hello world", duration=2.0, intensity=3, color="#00ff41")
Effect.fade_in("Hello world", duration=1.0, color="#00ccff")
Effect.fade_out("Hello world", duration=1.0)
Effect.slide_in("Hello world", from_="left", duration=0.8, color="#ffd60a")
Effect.slide_out("Hello world", to="right", duration=0.8)
Effect.wave("Hello world", duration=3.0, color="#00ccff", amplitude=2)
Effect.shake("Hello world", duration=1.0, color="#ff4444", intensity=2)
Effect.explode("BOOM!", duration=1.5, color="#ffd60a")
Effect.implode("HELLO", duration=1.5, color="#00ccff")
Effect.scramble("Decrypting…", duration=1.5, color="#00ff41")  # hacker reveal
Effect.rainbow_scroll("HELLO", duration=3.0)
Effect.flash("ALERT", times=3, color="#ff4444")
Effect.countdown_explode(5)                                    # 5..4..3..2..1 BOOM
Effect.fly_text("HELLO", path="wave", color="#00ccff")
# path: 'wave' | 'spiral' | 'zigzag'
```

---

## Particle

🆕 **v3** — emit individual particles or full explosions.

```python
from c4rlib import Particle

Particle.emit(x=40, y=10, kind="spark", count=30, color="#ffd60a")
# kinds: spark | dust | fire | smoke | bubble | snow
Particle.explosion(x=40, y=10, radius=15, colors=["#ffd60a","#ff4444","#ffffff"])
Particle.trail(from_=(0,5), to=(80,5), kind="dust", color="#adb5bd")
```

---

## Audio

🆕 **v3** — cross-platform beeps and SFX (`winsound` / `afplay` / `aplay` / `\a` fallback).

```python
from c4rlib import Audio

Audio.is_available()
Audio.beep(freq=880, duration=0.1)
Audio.play_freq(440, 0.2)
Audio.play_freqs([523, 659, 784], duration=0.15)

# SFX presets
Audio.success()
Audio.error()
Audio.warning()
Audio.notify()
Audio.click()
Audio.pop()
Audio.coin()
Audio.powerup()
Audio.gameover()
Audio.fanfare()
Audio.alarm(times=3)

# Non-blocking
Audio.play_async(Audio.fanfare)
```

---

## Sound

🆕 **v3** — play sound files.

```python
from c4rlib import Sound

Sound.play("path/to/sound.wav")        # blocking
Sound.play_async("path/to/sound.wav")  # background
Sound.stop()
```

---

## Melody

🆕 **v3** — chiptune-style melodies.

```python
from c4rlib import Melody

Melody.play([("C5", 0.2), ("E5", 0.2), ("G5", 0.4)])
Melody.preset("mario_intro")
Melody.preset("zelda_secret")
Melody.preset("tetris_loop")
Melody.preset_async("victory")
Melody.list_presets()
# alert, boot, coin_collect, defeat, doorbell, fanfare, intro, jingle,
# level_up, mario_intro, powerdown, tetris_loop, ufo, victory, zelda_secret
```

---

## Menu

🆕 **v3** — arrow-key navigable menus.

```python
from c4rlib import Menu

choice  = Menu.select("Choose option",
                      options=["Play", "Settings", "Quit"],
                      color="#00ccff")

choices = Menu.multi_select("Pick features",
                            options=["Audio", "Animations", "ASCII"],
                            color="#9b5de5")

tab = Menu.tabs(["General", "Audio", "Video"], color="#ffd60a")
```

Keys: `↑`/`↓` navigate · `Enter` select · `Space` toggle (multi) · `←`/`→` tabs · `ESC` cancel.

---

## Prompt

🆕 **v3** — typed prompts.

```python
from c4rlib import Prompt

Prompt.text("Your name", default="c4r", color="#00ccff")
Prompt.password("Password")
Prompt.number("Age", min=1, max=120, default=18)
Prompt.confirm("Continue?", default=True)
Prompt.path("Select file", exists=True)
Prompt.autocomplete("Command", options=["start", "stop", "status"])  # TAB completes
```

---

## Form

🆕 **v3** — multi-field forms with validators.

```python
from c4rlib import Form

data = Form.ask([
    Form.field("name",     "Your name",  required=True),
    Form.field("email",    "Email",      validator=Form.is_email),
    Form.field("age",      "Age",        type=int, min=18),
    Form.field("password", "Password",   secret=True),
    Form.choice("color",   "Favorite",   ["red", "blue", "green"]),
    Form.confirm("agree",  "Accept ToS?"),
], title="Sign up")
```

---

## Dashboard

🆕 **v3** — live multi-panel display (à la htop).

```python
from c4rlib import Dashboard

dash = Dashboard(title="My Tool — v3.0.0")
dash.add_panel("stats",  position="top-left",  title="📊 stats")
dash.add_panel("status", position="top-right", title="🟢 status", color="#29bf12")
dash.add_panel("logs",   position="bottom",    title="📜 logs")

with dash.live(refresh=10):                # 10 FPS auto-refresh
    dash.update("stats", [f"req: {n}", f"err: {e}"])
    dash.append("logs", "[ok] new request", max_lines=10)
    dash.set_status("status", "RUNNING", color="#29bf12")
```

---

## FX

🆕 **v3** — premade compositions that stack ASCII + animation + sound + color into one-liners.

```python
from c4rlib import FX

# Intros & outros
FX.intro("MY APP", subtitle="v3.0.0", style="fireworks")   # fireworks | matrix | glitch
FX.outro("Thanks!", style="confetti")
FX.splash("LOADING", duration=3.0)

# Results
FX.celebrate("DONE!", confetti=True, sound=True)
FX.error_explosion("FAILED!", shake=True, sound=True)
FX.warning_flash("CAREFUL!", times=3)
FX.success_check("Saved!")
FX.level_up("LEVEL 99", sparkles=True, sound=True)

# Transitions
FX.transition_fade(from_text="Step 1", to_text="Step 2")
FX.transition_glitch(from_text="Loading", to_text="Ready")

# Showcases
FX.matrix_intro("WAKE UP, NEO")
FX.terminal_hack(text="ACCESS GRANTED", target="MAINFRAME-7")
FX.boot_sequence(["Loading kernel", "Mounting fs", "Starting services"])
FX.demo_all()                                              # full reel
```

---

## Logger

Colored leveled logger with timestamps.

```python
from c4rlib import Logger

Logger.success("Tag", "message", "extra")
Logger.error("Tag", "message", "extra")
Logger.warning("Tag", "message", "extra")
Logger.info("Tag", "message", "extra")
Logger.debug("Tag", "message", "extra")
Logger.critical("Tag", "message", "extra")
Logger.network("Tag", "message", "extra")
Logger.captcha("Tag", "message", "extra")
Logger.input("Tag", "message", "extra")
Logger.output("Tag", "message", "extra")
Logger.proxy("Tag", "message", "extra")
Logger.token("Tag", "message", "extra")
Logger.upload("Tag", "message", "extra")
Logger.download("Tag", "message", "extra")
Logger.database("Tag", "message", "extra")
Logger.file("Tag", "message", "extra")
Logger.crypto("Tag", "message", "extra")
Logger.wait("Tag", "message", "extra")
Logger.done("Tag", "message", "extra")
Logger.send("Tag", "message", "extra")
Logger.receive("Tag", "message", "extra")
Logger.locked("Tag", "message", "extra")
Logger.unlocked("Tag", "message", "extra")
Logger.custom("#FF69B4", "♥", "LVL", "message", "extra")
Logger.gradient_log("message", start=(0,200,255), end=(200,0,255))
Logger.banner_log("message", hex_color="#00ccff")
Logger.fire("message")
Logger.galaxy("message")
Logger.neon("message")

# 🆕 v3 — each log emits a sound
Logger.enable_sounds()
Logger.disable_sounds()
```

---

## Spinner

Animated terminal spinners with 28 styles.

```python
from c4rlib import Spinner

with Spinner("Loading...", style="dots", color="#00ccff") as sp:
    sp.text = "Still loading..."
    time.sleep(2)

sp = Spinner("Working", style="moon", color="#9b5de5", interval=0.15)
sp.start()
time.sleep(2)
sp.stop("Done!", success=True)
```

**Styles:** `dots`, `dots2`, `dots3`, `line`, `arrows`, `arrows2`, `bounce`, `circle`, `circle2`, `square`, `star`, `star2`, `grow`, `pulse`, `flip`, `balloon`, `noise`, `point`, `layer`, `earth`, `moon`, `hearts`, `clock`, `runner`, `weather`, `dice`, `aesthetic`, `matrix`.

---

## ProgressBar

Animated progress bars with 14 styles.

```python
from c4rlib import ProgressBar

bar = ProgressBar(total=100, label="Downloading", style="block",
                  color="#00ccff", width=40, show_eta=True, show_speed=True)
for i in range(100):
    time.sleep(0.05)
    bar.update(1)
bar.finish("Download complete")
```

**Styles:** `block`, `shade`, `smooth`, `classic`, `arrow`, `dot`, `square`, `diamond`, `line`, `wave`, `star`, `heart`, `fire`, `thin`.

---

## Table

```python
from c4rlib import Table

table = Table(headers=["Name", "Score", "Status"],
              title="Leaderboard",
              header_color="#ffd60a", border_color="#6c757d",
              align="left", zebra=True)
table.add_row(["Alice", "98", "✔ Pass"])
table.add_rows([["Bob", "74", "✔ Pass"], ["Charlie", "41", "✘ Fail"]])
table.print()

print(table.render())
print(table.to_csv())
```

---

## Console

Terminal control utilities.

```python
from c4rlib import Console

Console.clear()
Console.clear_screen()
Console.clear_line()
Console.title("My Tool v3.0")
Console.width(); Console.height(); Console.size()
Console.hide_cursor(); Console.show_cursor()
Console.move_cursor(x=10, y=5)
Console.at(x=10, y=5, text="hi")           # 🆕 v3
Console.save_cursor(); Console.restore_cursor()
Console.bell()
Console.rule(char="─", color="#6c757d")
Console.gradient_rule(start=(0,200,255), end=(200,0,255))
Console.typewriter("text", delay=0.04, color="#00ccff")
Console.countdown(5, text="Starting in", color="#FF4444")
Console.input_prompt("Enter name", color="#00ccff")
Console.confirm("Are you sure?", color="#ffd60a")
Console.select("Choose", options=["A", "B", "C"])
Console.pause("Press ENTER...")
Console.print_cols(["a","b","c","d","e","f"], cols=3)
```

---

## Http

HTTP requests without external dependencies.

```python
from c4rlib import Http

r = Http.get("https://api.example.com/users", params={"page": 1}, timeout=10)
r = Http.post("https://api.example.com/login", json_data={"user": "c4r"})
r = Http.put("https://api.example.com/user/1", json_data={"name": "c4r"})
r = Http.delete("https://api.example.com/user/1")
r = Http.patch("https://api.example.com/user/1", json_data={"score": 99})
r = Http.head("https://api.example.com")

r.status; r.text; r.json(); r.content; r.headers; r.ok()

Http.download("https://example.com/file.zip", "output.zip")
Http.build_headers(token="Bearer xyz", content_type="application/json")
Http.random_headers(token="Bearer xyz")
Http.parse_url("https://example.com/path?foo=bar")
Http.encode_params({"key": "value"})
Http.build_url("https://api.example.com", "users", {"page": 1})
Http.is_reachable("https://google.com")
```

---

## Crypto

Hashing, encoding, encryption, and JWT utilities.

```python
from c4rlib import Crypto

Crypto.md5("text"); Crypto.sha1("text"); Crypto.sha256("text")
Crypto.sha512("text"); Crypto.sha3_256("text"); Crypto.sha3_512("text")
Crypto.blake2b("text"); Crypto.blake2s("text")
Crypto.hmac_sha256("key", "message"); Crypto.hmac_sha512("key", "message")
Crypto.hash_file("path/to/file.txt")
Crypto.compare_hash("text", "expected_hash")

Crypto.b64_encode("text"); Crypto.b64_decode("dGV4dA==")
Crypto.b64_urlsafe_encode("text"); Crypto.b64_urlsafe_decode("dGV4dA")
Crypto.hex_encode("text"); Crypto.hex_decode("74657874")
Crypto.url_encode("hello world"); Crypto.url_decode("hello%20world")
Crypto.html_encode("<script>"); Crypto.html_decode("&lt;script&gt;")

Crypto.xor_encrypt("message", "key"); Crypto.xor_decrypt(enc, "key")
Crypto.vigenere_encrypt("msg", "key"); Crypto.vigenere_decrypt(enc, "key")
Crypto.rot13("text"); Crypto.caesar("text", shift=3)

Crypto.make_jwt({"user": "c4r"}, "secret")
Crypto.decode_jwt(token); Crypto.verify_jwt(token, "secret")
Crypto.pbkdf2("password", salt="optional_salt")
Crypto.totp("BASE32SECRET")

Crypto.random_bytes(32); Crypto.random_hex(32); Crypto.random_urlsafe(32)
```

---

## Files

```python
from c4rlib import Files

Files.read("file.txt"); Files.read_lines("file.txt"); Files.read_bytes("file.bin")
Files.write("file.txt", "content"); Files.write_bytes("file.bin", b"data")
Files.append("file.txt", "more"); Files.append_line("file.txt", "line")
Files.write_json("data.json", {"key": "value"}); Files.read_json("data.json")

Files.exists("file.txt"); Files.is_file("file.txt"); Files.is_dir("folder/")
Files.mkdir("new/folder/path")
Files.delete("file.txt"); Files.copy("src.txt", "dst.txt")
Files.move("src.txt", "dst.txt"); Files.rename("old.txt", "new.txt")

Files.size("file.txt"); Files.size_human("file.txt")
Files.extension("file.txt"); Files.basename("path/to/file.txt")
Files.dirname("path/to/file.txt"); Files.stem("file.txt")
Files.abspath("file.txt"); Files.join("path", "to", "file.txt")

Files.list_dir("."); Files.list_files(".", pattern="*.py", recursive=True)
Files.list_dirs(".")
Files.find(".", "config", recursive=True)
Files.find_by_extension(".", "py", recursive=True)
Files.count_lines("file.txt")
Files.hash("file.txt", algorithm="sha256")
Files.modified_time("file.txt"); Files.created_time("file.txt")
Files.tree("."); Files.safe_filename("bad:file*name?.txt")
Files.temp_path(suffix=".tmp")
Files.cwd(); Files.home()
```

---

## Discord

Discord-specific utilities — no requests library needed.

```python
from c4rlib import Discord

Discord.is_valid_token(token); Discord.decode_token(token)
Discord.snowflake_to_timestamp(snowflake_id)
Discord.timestamp_to_snowflake(datetime_obj)
Discord.generate_nonce(); Discord.generate_session_id(); Discord.generate_device_id()

Discord.make_xsuper(client_version="1.0.9038", build_number=9038)
Discord.make_headers(token="Bot my_token", xsuper=xsuper)

Discord.generate_username()
Discord.generate_birthdate(min_year=1990, max_year=2000)
Discord.random_invite_code(); Discord.parse_invite("https://discord.gg/abc123")
Discord.invite_link("abc123")
Discord.message_link(guild_id, channel_id, message_id)
Discord.channel_link(guild_id, channel_id)

Discord.format_bold("text"); Discord.format_italic("text")
Discord.format_underline("text"); Discord.format_strikethrough("text")
Discord.format_spoiler("text"); Discord.format_code("code", "python")
Discord.format_inline_code("code")
Discord.format_mention_user(user_id); Discord.format_mention_role(role_id)
Discord.format_mention_channel(channel_id)
Discord.format_emoji("name", emoji_id, animated=False)
Discord.format_timestamp(datetime_obj, style="f")
Discord.format_quote("multi\nline\ntext")
Discord.format_embed_color("#5865F2")

Discord.make_embed(
    title="Title",
    description="Description",
    color="#5865F2",
    fields=[Discord.make_field("Name", "Value", inline=True)],
    footer="Footer text",
    thumbnail="https://...", image="https://...",
    author="Author name", timestamp=True,
)
Discord.permissions_to_list(permissions_integer)
```

---

## Utils

General-purpose utility functions.

```python
from c4rlib import Utils

Utils.generate_uuid(); Utils.generate_uuid_hex()
Utils.generate_token(32); Utils.generate_hex_token(16)
Utils.generate_pin(6); Utils.generate_password(20, symbols=True)

Utils.timestamp(); Utils.timestamp_seconds()
Utils.log_time(); Utils.log_date(); Utils.log_datetime()
Utils.elapsed(start_time)

Utils.random_string(8); Utils.random_hex(8)
Utils.hash_md5("text"); Utils.hash_sha1("text"); Utils.hash_sha256("text")
Utils.hash_sha512("text"); Utils.hash_sha3_256("text")

Utils.generate_mac(); Utils.generate_ipv4(); Utils.generate_ipv6()
Utils.generate_port()

Utils.random_name(); Utils.random_first_name(); Utils.random_last_name()
Utils.random_email(domain="gmail.com"); Utils.random_username()
Utils.random_birthdate(min_year=1990, max_year=2000)
Utils.random_phone(country_code="+34"); Utils.random_address()
Utils.random_zip(country="US")
Utils.random_credit_card(brand="visa")
Utils.random_user_agent(); Utils.random_color_hex()

Utils.chunk([1,2,3,4,5,6], size=2); Utils.flatten([[1,2],[3,[4,5]]])
Utils.unique([1,2,2,3,3]); Utils.clamp(150, 0, 100)
Utils.lerp(0, 100, 0.5); Utils.percentage(7, 10)
Utils.format_bytes(1536000); Utils.format_number(1000000)
Utils.retry(func, times=3, delay=1.0)

Utils.is_windows(); Utils.is_linux(); Utils.is_mac()
Utils.os_info(); Utils.run("echo hello")
```

---

## What's new in 3.0.0

- 🅰️ **ASCII art** — `Figlet` (400+ fonts), `ImageAscii` (image→ASCII), `Ascii` (mini-FIGlet, dividers)
- 👻 **Animated sprites** — `Sprite` with 15 presets, `.move()`, `.bounce()`, `.shake()`, `.float()`, `.parade()`, `.race()` and custom `Sprite.from_frames(...)`
- ✨ **Full-screen animations** — matrix rain, fireworks, starfield, snow, rain, confetti, glitch, scanlines
- 🎬 **Text effects** — typewriter, glitch, scramble, fade, slide, wave, shake, explode, implode, rainbow scroll, flash, fly text along paths, particles
- 🔊 **Audio** — cross-platform beeps, 12+ SFX presets (`success`, `coin`, `powerup`, `fanfare`…), and 15 chiptune `Melody` presets (mario, zelda, tetris…); `Logger.enable_sounds()`
- ⌨️ **Interactive** — arrow-key `Menu.select / multi_select / tabs`, `Prompt.text / password / number / confirm / path / autocomplete`, multi-field `Form.ask`, live `Dashboard` with refresh
- 🎆 **FX layer** — one-liner composed showcases: `FX.intro`, `FX.outro`, `FX.celebrate`, `FX.error_explosion`, `FX.level_up`, `FX.matrix_intro`, `FX.terminal_hack`, `FX.boot_sequence`, `FX.demo_all`

`pip install c4rlib --upgrade`

Full history in [CHANGELOG.md](CHANGELOG.md).

---

## Contributing

New effects, sprites, gradients, melodies and terminal-compatibility fixes are
all welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). Bug reports for terminal
quirks are especially useful; please include your OS and terminal emulator.

```bash
git clone https://github.com/C4rI0s/c4rlib.git
cd c4rlib
pip install -e ".[dev]"
pytest
```

---

## License

MIT © c4r — see [LICENSE](LICENSE).
