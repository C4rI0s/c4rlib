"""
c4rlib 3.0.0 — Full showcase / interactive demo
================================================

Run:
    python tests/showcase.py

Pick what you want to see from the menu. Each section explains and demos.
ESC at any prompt to exit early.
"""

import os
import sys
import time

# Allow running from project root or tests/
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

# Force UTF-8 stdout on Windows so block chars don't crash
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from c4rlib import (
    ColorUtils, Gradient, GradientPresets,
    Logger,
    Box, Banner,
    TextStyle,
    Utils,
    Spinner, ProgressBar, Table, Console,
    Figlet, Ascii, ImageAscii, Sprite,
    Animations, Effect, Particle,
    Audio, Sound, Melody,
    Menu, Form, Prompt, Dashboard,
    FX,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def header(title: str) -> None:
    Console.clear()
    print()
    print(Banner.giant(title, font="small",
                       gradient=((0, 200, 255), (200, 0, 255))))
    print(Ascii.divider("dash", color="#6c757d"))
    print()


def section(title: str, description: str = "") -> None:
    print()
    print(f"  {ColorUtils.hex('#00ccff')}▶ {title}{ColorUtils.RESET}")
    if description:
        print(f"  {ColorUtils.hex('#adb5bd')}{description}{ColorUtils.RESET}")
    print()


def pause() -> None:
    print()
    Console.pause(f"  {ColorUtils.hex('#6c757d')}↵ ENTER to continue...{ColorUtils.RESET}")


# ─────────────────────────────────────────────────────────────────────────────
# Demos por sección
# ─────────────────────────────────────────────────────────────────────────────
def demo_colors() -> None:
    header("COLORS")

    section("ColorUtils — paint, styles, mixing",
            "Tinta texto, blende colores, genera paletas.")
    print(" ", ColorUtils.paint("Hello in cyan", "#00ccff"))
    print(" ", ColorUtils.bg_paint(" Hello on red ", "#ffffff", "#d00000"))
    print(" ", ColorUtils.bold("Bold"),
          ColorUtils.italic("Italic"),
          ColorUtils.underline("Underline"),
          ColorUtils.strike("Strike"))
    print(" ", ColorUtils.rainbow("RAINBOW TEXT EVERYWHERE"))
    print(" ", "Blend red→blue:", ColorUtils.blend("#FF0000", "#0000FF", 0.5))
    print(" ", "Palette of #00ccff:", " ".join(ColorUtils.palette("#00ccff", steps=5)))

    section("Gradient — presets espectaculares",
            "Aplica degradados a cualquier texto.")
    samples = [
        ("fire",     Gradient.fire("🔥 fire gradient over a long text 🔥")),
        ("ocean",    Gradient.ocean("🌊 ocean gradient over a long text 🌊")),
        ("galaxy",   Gradient.galaxy("🌌 galaxy gradient over a long text 🌌")),
        ("matrix",   Gradient.matrix("[ matrix gradient over a long text ]")),
        ("aurora",   Gradient.aurora("✨ aurora gradient over a long text ✨")),
        ("neon",     Gradient.neon("⚡ neon gradient over a long text ⚡")),
    ]
    for name, s in samples:
        print(f"  {ColorUtils.hex('#6c757d')}{name:8s}{ColorUtils.RESET} {s}")

    pause()


def demo_logger() -> None:
    header("LOGGER")
    section("Logger — niveles coloreados", "Logs con timestamp y símbolos por tipo.")
    Logger.success("BOOT", "system online")
    Logger.error("DB",     "connection refused")
    Logger.warning("CFG",  "deprecated key")
    Logger.info("APP",     "version 3.0.0")
    Logger.debug("REQ",    "GET /users 200ms")
    Logger.critical("KRN", "kernel panic (drill)")
    Logger.network("HTTP", "POST /api/login")
    Logger.proxy("PROXY",  "rotated to 1.2.3.4")
    Logger.token("AUTH",   "JWT verified")
    Logger.download("FILE","movie.mp4")
    Logger.crypto("ENC",   "AES-256 OK")
    Logger.locked("LOCK",  "vault sealed")
    Logger.unlocked("LOCK","vault opened")
    Logger.custom("#ff69b4", "♥", "LOVE", "logger with custom level")

    section("Logger.gradient/fire/galaxy/neon", "Y con efectos especiales.")
    Logger.fire("Algo ardiendo en producción")
    Logger.galaxy("Mensaje cósmico")
    Logger.neon("Modo neón activado")
    Logger.gradient_log("Texto con gradiente custom",
                        start=(255, 100, 0), end=(255, 0, 200))
    pause()


def demo_text() -> None:
    header("TEXT STYLES")
    section("TextStyle — transformaciones Unicode")
    print("  fancy        :", TextStyle.fancy("Hello World"))
    print("  cursive      :", TextStyle.cursive("Hello World"))
    print("  double_struck:", TextStyle.double_struck("Hello World"))
    print("  bubble       :", TextStyle.bubble("Hello World"))
    print("  small_caps   :", TextStyle.small_caps("Hello World"))
    print("  wide         :", TextStyle.wide("Hello"))
    print("  leet         :", TextStyle.leet("Hello World"))
    print("  uwuify       :", TextStyle.uwuify("Hello world"))
    print("  zalgo (lvl 2):", TextStyle.zalgo("zalgo", intensity=2))
    print("  rot13        :", TextStyle.rot13("Hello World"))
    print("  morse        :", TextStyle.morse("SOS"))
    print("  binary       :", TextStyle.binary("hi"))
    print("  hex_encode   :", TextStyle.hex_encode("hi"))
    pause()


def demo_boxes_banners() -> None:
    header("BOXES & BANNERS")
    section("Box — variantes")
    print(Box.rounded("rounded", color="#00ccff"))
    print(Box.double("double",  color="#9b5de5"))
    print(Box.heavy("heavy",    color="#29bf12"))
    print(Box.stars("stars",    color="#ffd60a"))
    print(Box.diamond("diamond", color="#00bbf9"))
    print(Box.neon("neon",      color="#00ccff"))
    print(Box.gradient_box("gradient_box"))

    section("Banner — divisores y títulos")
    print(Banner.line("title line", color="#00ccff"))
    print(Banner.arrow_line("arrows", color="#ffd60a"))
    print(Banner.heart_line("hearts", color="#FF69B4"))
    print(Banner.wave_line("waves", color="#29bf12"))
    print(Banner.lightning_line("lightning", color="#ffd60a"))
    print(Banner.gradient_banner("gradient banner"))

    section("Banner.giant — texto enorme con FIGlet")
    print(Banner.giant("BIG!", font="standard", color="#00ccff"))
    print()
    print(Banner.print_giant.__name__,
          "→ same but prints directly")
    pause()


def demo_ascii_figlet() -> None:
    header("ASCII ART")
    section("Figlet — texto enorme",
            "Cientos de fuentes via pyfiglet.")
    for font in ("standard", "slant", "small", "big", "block"):
        try:
            print(f"\n  {ColorUtils.hex('#9b5de5')}font: {font}{ColorUtils.RESET}")
            Figlet.print("HELLO", font=font, color="#00ccff")
        except Exception:
            print(f"  (font {font} not available)")

    section("Figlet.gradient — degradado letras gigantes")
    Figlet.print_gradient("c4rlib", font="standard",
                          start=(0, 200, 255), end=(200, 0, 255))
    print()
    Figlet.print_gradient("c4rlib", font="standard",
                          start=(255, 200, 0), end=(255, 0, 100),
                          vertical=True)

    section("Figlet.boxed — gigante en caja")
    print(Figlet.boxed("FX", font="standard", color="#ffd60a"))

    section("Ascii.divider — separadores",
            "Diferentes estilos para romper secciones.")
    for s in ("zigzag", "wave", "stars", "lightning", "fire", "heart", "diamond"):
        Ascii.print_divider(s, width=40, color="#00ccff")
    pause()


def demo_ascii_sprites() -> None:
    header("ASCII SPRITES")
    section("Sprite.preset — 15 presets incluidos",
            f"Disponibles: {', '.join(Sprite.PRESETS)}")
    for name in Sprite.PRESETS[:6]:
        s = Sprite.preset(name, color="#00ccff")
        print(f"\n  {ColorUtils.hex('#9b5de5')}{name}{ColorUtils.RESET}")
        for frame in s.frames[:1]:
            for line in frame:
                print("    " + line)

    section("Sprite.move — fantasma cruzando con bob",
            "Mueve sprite de izquierda a derecha con vaivén.")
    Sprite.preset("ghost", color="#a78bfa").move(from_x=2, to_x=70,
                                                  duration=2.5, bob=True)

    section("Sprite.bounce — pelota rebotando")
    Sprite.preset("ball", color="#FF69B4").bounce(times=3, height=8)

    section("Sprite.shake — sprite temblando")
    Sprite.preset("ufo", color="#00bbf9").shake(duration=1.5, intensity=2)

    section("Sprite.float — flota suavemente")
    Sprite.preset("rocket", color="#ffd60a").float(amplitude=2, duration=3.0)

    section("Sprite.from_frames — tu propio sprite",
            "Pasa los frames que quieras.")
    my = Sprite.from_frames([
        " (o_o) ",
        " (^_^) ",
        " (>_<) ",
    ], fps=4, color="#FF69B4")
    my.play(duration=3.0)

    section("Sprite.parade — desfile multi-sprite")
    Sprite.parade(["ghost", "ufo", "rocket", "cat"],
                  speed=25, gap=6,
                  colors=["#a78bfa", "#00bbf9", "#ff4444", "#ffd60a"])

    section("Sprite.race — carrera con ganador aleatorio")
    Sprite.race(["rocket", "ufo", "car"], length=50,
                colors=["#ff4444", "#00ccff", "#ffd60a"])
    pause()


def demo_image_to_ascii() -> None:
    header("IMAGE → ASCII")
    section("ImageAscii — convierte cualquier imagen",
            "Necesita Pillow. Si no lo tienes: pip install pillow")
    print(f"  Charsets disponibles: {ImageAscii.charsets}\n")
    path = Prompt.text("Ruta a imagen (vacío para saltar)", default="")
    if not path:
        print("  Saltado.")
        return
    try:
        for cs in ("blocks", "dense", "sparse"):
            print(f"\n  {ColorUtils.hex('#9b5de5')}charset: {cs}{ColorUtils.RESET}")
            print(ImageAscii.from_file(path, width=50, charset=cs, color=True))
    except Exception as e:
        print(f"  Error: {e}")
    pause()


def demo_animations() -> None:
    header("ANIMATIONS")

    section("Animations.matrix_rain — lluvia Matrix",
            "Letras cayendo estilo The Matrix. 4s.")
    Animations.matrix_rain(duration=4.0)

    section("Animations.fireworks — fuegos artificiales", "5 cohetes, 5s.")
    Animations.fireworks(count=5, duration=5.0)

    section("Animations.starfield — campo de estrellas en movimiento")
    Animations.starfield(duration=3.0, density=0.5)

    section("Animations.snow / rain / confetti")
    Animations.snow(duration=3.0)
    Animations.rain(duration=3.0)
    Animations.confetti(duration=3.0)

    section("Animations.glitch_screen — pantalla glitch")
    Animations.glitch_screen(duration=1.2)

    section("Animations.scanlines — efecto CRT")
    Animations.scanlines(duration=3.0, color="#00ff41")

    section("Effect.typewriter / scramble / glitch / shake")
    Effect.typewriter("  Loading the matrix systems...", delay=0.04, color="#00ff41")
    Effect.scramble("  Decrypting message: HELLO HUMAN", duration=1.5,
                    color="#ffd60a")
    Effect.glitch("  >> CONNECTION UNSTABLE <<", duration=1.5, color="#ff4444")
    Effect.shake("  EARTHQUAKE", duration=1.0, color="#ff7b00")

    section("Effect.fade_in / fade_out")
    Effect.fade_in("  Appearing softly...", duration=1.0, color="#00ccff")
    Effect.fade_out("  Disappearing softly...", duration=1.0, color="#9b5de5")

    section("Effect.slide_in / slide_out")
    Effect.slide_in("  >>> SLIDING IN <<<", from_="left", color="#ffd60a")
    Effect.slide_out("  <<< SLIDING OUT >>>", to="right", color="#9b5de5")

    section("Effect.wave — texto ondeando")
    Effect.wave("  Surfing the waves of c4rlib", duration=3.0,
                color="#00ccff", amplitude=2)

    section("Effect.rainbow_scroll")
    Effect.rainbow_scroll("  🌈 ABCDEFGHIJKLMNOPQRSTUVWXYZ", duration=2.5)

    section("Effect.flash — parpadeo")
    Effect.flash("  ⚠  ATTENTION ⚠", times=3, color="#ff4444")

    section("Effect.explode — texto explota en partículas")
    Effect.explode("BOOM!", duration=1.5, color="#ffd60a")

    section("Effect.implode — partículas se juntan")
    Effect.implode("HELLO", duration=1.5, color="#00ccff")

    section("Effect.fly_text — texto volando por caminos",
            "Path puede ser: wave, spiral, zigzag")
    Effect.fly_text("c4rlib 3.0", path="wave", duration=2.5, color="#00ccff")
    Effect.fly_text("c4rlib 3.0", path="spiral", duration=2.5, color="#9b5de5")

    section("Effect.countdown_explode — countdown y BOOM")
    Effect.countdown_explode(3)

    section("Particle — partículas custom")
    Particle.emit(x=40, y=12, kind="spark", count=30,
                  color="#ffd60a", duration=1.5)
    Particle.explosion(x=40, y=10, radius=12, duration=1.5)
    Particle.trail(from_=(2, 10), to=(70, 5), kind="dust", color="#adb5bd")
    pause()


def demo_audio() -> None:
    header("AUDIO")
    section("Audio — beeps y SFX", "Si no oyes nada, no tienes salida de audio activa.")
    print(f"  Audio disponible: {Audio.is_available()}\n")

    samples = [
        ("success",  Audio.success),
        ("error",    Audio.error),
        ("warning",  Audio.warning),
        ("notify",   Audio.notify),
        ("click",    Audio.click),
        ("pop",      Audio.pop),
        ("coin",     Audio.coin),
        ("powerup",  Audio.powerup),
        ("gameover", Audio.gameover),
        ("fanfare",  Audio.fanfare),
    ]
    for name, fn in samples:
        print(f"  Playing: {ColorUtils.hex('#00ccff')}{name}{ColorUtils.RESET}")
        try: fn()
        except Exception: pass
        time.sleep(0.3)

    section("Audio.beep — tono custom (freq + duración)")
    for f in (440, 523, 659, 784, 988):
        print(f"  beep {f}Hz")
        Audio.beep(f, 0.15)

    section("Melody — melodías chiptune predefinidas",
            f"Presets: {', '.join(Melody.list_presets())}")
    for preset in ("mario_intro", "zelda_secret", "victory", "level_up", "coin_collect"):
        print(f"\n  Playing: {ColorUtils.hex('#9b5de5')}{preset}{ColorUtils.RESET}")
        try: Melody.preset(preset)
        except Exception as e: print(f"  failed: {e}")
        time.sleep(0.2)

    section("Melody.play — tu propia melodía",
            "Lista de tuples (nota, duración_segundos). R = silencio")
    Melody.play([("C5", 0.2), ("E5", 0.2), ("G5", 0.2),
                 ("C6", 0.4), ("G5", 0.2), ("C6", 0.5)])

    section("Logger.enable_sounds — logs con sonido")
    Logger.enable_sounds()
    Logger.success("SOUND", "this log just played a sound")
    Logger.error("SOUND",   "and this one a different sound")
    Logger.warning("SOUND", "and this another")
    Logger.disable_sounds()
    pause()


def demo_interactive() -> None:
    header("INTERACTIVE")
    section("Menu.select — menú navegable con flechas",
            "↑/↓ para moverte, Enter para elegir, ESC para salir")
    choice = Menu.select("Choose your favorite preset",
                         options=["fire", "ocean", "galaxy", "matrix", "aurora", "candy"],
                         color="#00ccff")
    print(f"\n  You picked: {ColorUtils.hex('#29bf12')}{choice}{ColorUtils.RESET}")
    if choice:
        print(" ", getattr(Gradient, choice)(f"You chose {choice} gradient — pretty, right?"))

    section("Menu.multi_select — selecciona varias",
            "SPACE para marcar, Enter para confirmar")
    picks = Menu.multi_select("Pick features you want",
                              options=["audio", "animations", "ascii", "interactive", "fx"],
                              color="#9b5de5")
    print(f"\n  You picked: {picks}")

    section("Menu.tabs — pestañas (←/→ y Enter)")
    tab = Menu.tabs(["General", "Audio", "Video", "Network"], color="#ffd60a")
    print(f"\n  Tab: {tab}")

    section("Prompt — text / password / number / confirm / path / autocomplete")
    name = Prompt.text("Your name", default="anonymous")
    age  = Prompt.number("Your age", default=18, min=1, max=120)
    ok   = Prompt.confirm("Do you like it?", default=True)
    print(f"  → name={name}  age={age}  like={ok}")

    section("Prompt.autocomplete — TAB para completar")
    cmd = Prompt.autocomplete("Command", options=["start", "stop", "status", "restart", "logs"])
    print(f"  → command={cmd}")

    section("Form.ask — formulario multi-campo")
    data = Form.ask([
        Form.field("user",  "Username",   required=True),
        Form.field("email", "Email",      validator=Form.is_email),
        Form.field("age",   "Age",        type=int, min=1),
        Form.confirm("nl",  "Subscribe to newsletter?"),
    ], title="Sign up")
    print(f"\n  → {data}")
    pause()


def demo_dashboard() -> None:
    header("DASHBOARD")
    section("Dashboard — paneles en vivo",
            "Multipanel actualizable, refrescado por thread. 8s de demo.")
    dash = Dashboard(title="c4rlib live dashboard")
    dash.add_panel("stats",  position="top-left",     title="📊 stats")
    dash.add_panel("status", position="top-right",    title="🟢 status",  color="#29bf12")
    dash.add_panel("logs",   position="bottom",       title="📜 logs",    color="#adb5bd")
    with dash.live(refresh=8):
        for i in range(40):
            dash.update("stats",
                        [f"requests : {i*7}",
                         f"errors   : {i//3}",
                         f"uptime   : {i*0.2:.1f}s",
                         f"cpu      : {30 + (i%30)}%",
                         f"mem      : {200 + i*4}MB"])
            dash.set_status("status", f"RUNNING — tick {i}", color="#29bf12")
            dash.append("logs", f"[{i:02d}] event #{i} processed",
                        max_lines=10)
            time.sleep(0.2)
    print("\n  Dashboard cerrado.\n")
    pause()


def demo_fx() -> None:
    header("FX — Showcases")
    section("FX.boot_sequence — arranque tipo Linux/BIOS")
    FX.boot_sequence(sound=True)
    time.sleep(0.5)

    section("FX.matrix_intro — secuencia Matrix")
    FX.matrix_intro("WAKE UP", sound=True)
    time.sleep(0.5)

    section("FX.terminal_hack — estética hacker movie")
    FX.terminal_hack("ROOT ACCESS GRANTED", target="GIBSON-XV", sound=True)
    time.sleep(0.5)

    section("FX.level_up — sube de nivel con partículas")
    FX.level_up("LEVEL 99", sparkles=True, sound=True)
    time.sleep(0.5)

    section("FX.celebrate — confetti + fanfare")
    FX.celebrate("WIN!", confetti=True, sound=True)
    time.sleep(0.5)

    section("FX.error_explosion — fallo dramático")
    FX.error_explosion("CRASH!", shake=True, sound=True)
    time.sleep(0.5)

    section("FX.warning_flash + FX.success_check")
    FX.warning_flash("CHECK INPUT", times=2)
    time.sleep(0.3)
    FX.success_check("All good")

    section("FX.intro / FX.outro — entradas y salidas con estilo")
    FX.intro("My App", subtitle="v1.0.0 — by you", style="fireworks", sound=True)
    time.sleep(1.0)
    FX.outro("Bye!", style="confetti", sound=True)
    pause()


def demo_progress_table() -> None:
    header("SPINNER · PROGRESS · TABLE")

    section("Spinner — 28 estilos")
    for style in ("dots", "moon", "earth", "weather", "runner", "hearts"):
        with Spinner(f"Loading with {style}", style=style, color="#00ccff"):
            time.sleep(1.0)

    section("ProgressBar — 14 estilos con ETA/speed")
    for style in ("block", "smooth", "arrow", "wave", "fire", "heart"):
        bar = ProgressBar(total=50, label=f"download ({style})",
                          style=style, color="#9b5de5")
        for _ in range(50):
            time.sleep(0.02)
            bar.update(1)
        bar.finish()

    section("Table — tabla bordeada con título y zebra")
    t = Table(headers=["Name", "Score", "Status"],
              title="Leaderboard",
              header_color="#ffd60a",
              border_color="#6c757d", zebra=True)
    t.add_rows([
        ["Alice",   "98", "✔ Pass"],
        ["Bob",     "74", "✔ Pass"],
        ["Charlie", "41", "✘ Fail"],
        ["Diana",   "87", "✔ Pass"],
    ])
    t.print()
    pause()


def demo_utils() -> None:
    header("UTILS")
    section("Utils — generadores rápidos para CLIs / pentest / fakes")
    print(f"  uuid         : {Utils.generate_uuid()}")
    print(f"  token (24)   : {Utils.generate_token(24)}")
    print(f"  pin (6)      : {Utils.generate_pin(6)}")
    print(f"  password     : {Utils.generate_password(20, symbols=True)}")
    print(f"  hex          : {Utils.random_hex(16)}")
    print(f"  mac          : {Utils.generate_mac()}")
    print(f"  ipv4         : {Utils.generate_ipv4()}")
    print(f"  ipv6         : {Utils.generate_ipv6()}")
    print(f"  name         : {Utils.random_name()}")
    print(f"  email        : {Utils.random_email()}")
    print(f"  user-agent   : {Utils.random_user_agent()}")
    print(f"  credit card  : {Utils.random_credit_card(brand='visa')}")
    print(f"  format bytes : {Utils.format_bytes(1536000)}")
    print(f"  format num   : {Utils.format_number(1234567)}")
    print(f"  os_info      : {Utils.os_info()}")
    print(f"  hash sha256  : {Utils.hash_sha256('c4rlib')}")
    pause()


# ─────────────────────────────────────────────────────────────────────────────
# Menu principal
# ─────────────────────────────────────────────────────────────────────────────
SECTIONS = [
    ("🎨  Colors & Gradients",         demo_colors),
    ("📝  Logger",                     demo_logger),
    ("🔤  Text styles (Unicode/leet)", demo_text),
    ("📦  Boxes & Banners",            demo_boxes_banners),
    ("🅰️   ASCII art (Figlet, divider)", demo_ascii_figlet),
    ("👻  ASCII sprites animados",     demo_ascii_sprites),
    ("🖼️   Image → ASCII",              demo_image_to_ascii),
    ("✨  Animations & Effects",       demo_animations),
    ("🔊  Audio & Melody",             demo_audio),
    ("⌨️   Interactive (menus/forms)",  demo_interactive),
    ("📊  Live Dashboard",             demo_dashboard),
    ("🎬  FX — Showcases (intro/hack…)", demo_fx),
    ("⏳  Spinner · Progress · Table", demo_progress_table),
    ("🛠️   Utils",                      demo_utils),
    ("🎆  FX.demo_all (todo seguido)", lambda: FX.demo_all()),
]


def main() -> None:
    Console.title("c4rlib 3.0.0 — Showcase")
    Console.clear()
    FX.intro("c4rlib 3", subtitle="v3.0.0 — Showtime", style="fireworks", sound=True)
    time.sleep(0.6)

    while True:
        Console.clear()
        print()
        print(Banner.giant("c4rlib", font="small",
                           gradient=((0, 200, 255), (200, 0, 255))))
        print(f"  {ColorUtils.hex('#adb5bd')}v3.0.0 — full feature showcase{ColorUtils.RESET}")
        print(Ascii.divider("dash", color="#6c757d"))
        print()

        choice = Menu.select(
            "Choose a demo to run",
            options=[s[0] for s in SECTIONS] + ["❌  Exit"],
            color="#00ccff",
        )
        if choice is None or choice.startswith("❌"):
            FX.outro("¡Hasta la próxima!", style="confetti", sound=True)
            return

        for label, fn in SECTIONS:
            if label == choice:
                try:
                    fn()
                except KeyboardInterrupt:
                    print(f"\n  {ColorUtils.hex('#ffd60a')}⚠ interrupted{ColorUtils.RESET}")
                except Exception as e:
                    print(f"\n  {ColorUtils.hex('#d00000')}✘ demo error: {e}{ColorUtils.RESET}")
                break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        Console.show_cursor()
        print("\n\n  Bye!\n")
