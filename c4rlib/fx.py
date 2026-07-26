import os
import sys
import time
import random
import shutil
from .colors      import ColorUtils, Gradient
from .ascii       import Figlet, Ascii, Sprite
from .animations  import Animations, Effect, Particle
from .audio       import Audio, Melody


def _clear():
    os.system("cls" if os.name == "nt" else "clear")

def _termsize():
    s = shutil.get_terminal_size()
    return s.columns, s.lines


class FX:
    # ── Intros & outros ───────────────────────────────────────────────────
    @staticmethod
    def intro(title: str, subtitle: str = None, style: str = "fireworks",
              color: str = "#00ccff", sound: bool = True) -> None:
        _clear()
        if style == "fireworks":
            if sound: Melody.preset_async("fanfare")
            Animations.fireworks(count=4, duration=2.5)
        elif style == "matrix":
            if sound: Melody.preset_async("ufo")
            Animations.matrix_rain(duration=2.5)
        elif style == "glitch":
            if sound: Audio.play_async(Audio.alarm, 2)
            Animations.glitch_screen(duration=1.0)
        else:
            time.sleep(0.3)
        _clear()
        title_block = Figlet.gradient(title,
                                      font="standard",
                                      start=ColorUtils.hex_to_rgb(color),
                                      end=ColorUtils.hex_to_rgb(ColorUtils.lighten(color, 0.3)))
        print(title_block)
        if subtitle:
            width = max(len(l) for l in title_block.split("\n"))
            print()
            print(f"  {ColorUtils.hex('#adb5bd')}{subtitle.center(width)}{ColorUtils.RESET}")
        if sound:
            try: Audio.success()
            except Exception: pass

    @staticmethod
    def outro(text: str = "Thanks for using!", style: str = "confetti",
              color: str = "#9b5de5", sound: bool = True) -> None:
        _clear()
        if style == "confetti":
            if sound: Melody.preset_async("victory")
            Animations.confetti(duration=2.5)
        elif style == "fade":
            Effect.fade_out(text, duration=1.5, color=color)
            return
        _clear()
        block = Figlet.gradient(text, font="small",
                                start=ColorUtils.hex_to_rgb(color),
                                end=(255, 105, 180))
        print(block)
        Effect.fade_in(" " * 20 + text, color=color, duration=0.8)

    @staticmethod
    def splash(text: str = "LOADING", duration: float = 3.0,
               color: str = "#00ccff") -> None:
        _clear()
        cols, rows = _termsize()
        block = Figlet.gradient(text, font="standard",
                                start=ColorUtils.hex_to_rgb(color),
                                end=ColorUtils.hex_to_rgb(ColorUtils.lighten(color, 0.4)))
        lines = block.split("\n")
        y_off = max(1, (rows - len(lines)) // 2 - 2)
        for _ in range(y_off):
            print()
        print(block)
        print()
        from .console import Spinner
        with Spinner(f"Initializing...", color=color):
            time.sleep(duration)

    # ── Resultados ────────────────────────────────────────────────────────
    @staticmethod
    def celebrate(text: str = "DONE!", confetti: bool = True, sound: bool = True) -> None:
        if sound: Melody.preset_async("victory")
        if confetti:
            Animations.confetti(duration=1.5)
        block = Figlet.gradient(text, font="standard",
                                start=(41, 191, 18), end=(255, 214, 10))
        print(block)
        print(f"  {ColorUtils.hex('#29bf12')}✔ Success!{ColorUtils.RESET}\n")

    @staticmethod
    def error_explosion(text: str = "FAILED!", shake: bool = True, sound: bool = True) -> None:
        if sound: Melody.preset_async("defeat")
        if shake:
            Effect.shake(f"  ✘  {text}  ✘", duration=0.8, color="#ff4444", intensity=3)
        Effect.flash(f"  💥 {text} 💥", times=3, color="#ff4444", delay=0.15)
        print()

    @staticmethod
    def warning_flash(text: str = "CAREFUL!", times: int = 3, sound: bool = True) -> None:
        if sound:
            Audio.play_async(Audio.warning)
        Effect.flash(f"  ⚠  {text}  ⚠", times=times, color="#ffd60a", delay=0.2)

    @staticmethod
    def success_check(text: str = "Saved!", sound: bool = True) -> None:
        if sound:
            Audio.play_async(Audio.success)
        col = ColorUtils.hex("#29bf12")
        print(f"\n  {col}  ✔  {text}{ColorUtils.RESET}")
        Effect.fade_in("  " + "─" * (len(text) + 8), color="#29bf12", duration=0.4)

    @staticmethod
    def level_up(text: str = "LEVEL 2", sparkles: bool = True, sound: bool = True) -> None:
        if sound: Melody.preset_async("level_up")
        if sparkles:
            cols, rows = _termsize()
            Particle.emit(cols // 2, rows // 2, kind="spark", count=40,
                          color="#ffd60a", duration=1.0)
        Effect.scramble(f"  ⬆  {text}  ⬆", duration=1.2, color="#ffd60a")

    # ── Transiciones ──────────────────────────────────────────────────────
    @staticmethod
    def transition_fade(from_text: str, to_text: str,
                        color: str = "#00ccff") -> None:
        Effect.fade_out(from_text, duration=0.6, color=color)
        Effect.fade_in(to_text, duration=0.6, color=color)

    @staticmethod
    def transition_glitch(from_text: str, to_text: str,
                          color: str = "#00ff41") -> None:
        Effect.glitch(from_text, duration=0.6, color=color, intensity=4)
        time.sleep(0.05)
        Effect.scramble(to_text, duration=0.8, color=color)

    # ── Showcases ─────────────────────────────────────────────────────────
    @staticmethod
    def matrix_intro(text: str = "WAKE UP, NEO", duration: float = 4.0,
                     sound: bool = True) -> None:
        _clear()
        if sound: Melody.preset_async("ufo")
        Animations.matrix_rain(duration=duration)
        _clear()
        Effect.typewriter(f"\n  {text}", delay=0.1, color="#00ff41")
        time.sleep(0.5)
        Effect.typewriter("  The Matrix has you...", delay=0.05, color="#00ff41")
        time.sleep(0.5)
        Effect.typewriter("  Follow the white rabbit.", delay=0.05, color="#00ff41")
        print()

    @staticmethod
    def terminal_hack(text: str = "ACCESS GRANTED",
                      target: str = "MAINFRAME-7", sound: bool = True) -> None:
        steps = [
            "Connecting to " + target + " ...",
            "Bypassing firewall (1/3) ...",
            "Bypassing firewall (2/3) ...",
            "Bypassing firewall (3/3) ...",
            "Cracking 4096-bit RSA ...",
            "Injecting payload ...",
        ]
        for s in steps:
            if sound: Audio.play_async(Audio.click)
            Effect.typewriter("  > " + s, delay=0.015, color="#00ff41")
            time.sleep(0.2)
        time.sleep(0.3)
        Effect.glitch("  >>> " + text + " <<<", duration=1.2,
                      color="#00ff41", intensity=4)
        if sound: Audio.play_async(Audio.success)
        print(f"\n  {ColorUtils.hex('#29bf12')}✔ Connection established{ColorUtils.RESET}\n")

    @staticmethod
    def boot_sequence(steps: list = None, fail_at: int = None,
                      sound: bool = True) -> None:
        """Fake-boot sequence à la BIOS / linux boot."""
        steps = steps or [
            "Loading kernel",
            "Mounting / (read-only)",
            "Starting udev",
            "Starting systemd",
            "Initializing network",
            "Starting services",
            "Loading user profile",
        ]
        for i, s in enumerate(steps):
            t = ColorUtils.hex("#6c757d") + "  [    OK    ]  " + ColorUtils.RESET
            ok = (fail_at is None or i != fail_at)
            mark = (ColorUtils.hex("#29bf12") + "  [   OK   ]" + ColorUtils.RESET) if ok \
                   else (ColorUtils.hex("#d00000") + "  [ FAILED ]" + ColorUtils.RESET)
            sys.stdout.write(f" {mark}  {s} ")
            sys.stdout.flush()
            time.sleep(random.uniform(0.15, 0.5))
            # simulate progress dots
            for _ in range(random.randint(2, 5)):
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(random.uniform(0.03, 0.12))
            sys.stdout.write("\n")
            if sound:
                try: Audio.click()
                except Exception: pass
            if fail_at is not None and i == fail_at:
                if sound: Audio.error()
                return
        print()
        if sound: Audio.fanfare()

    @staticmethod
    def demo_all(skip_audio: bool = False) -> None:
        """Visual walkthrough of every showcase. Bring popcorn."""
        from .console import Console
        Console.hide_cursor()
        try:
            FX.intro("c4rlib 3", subtitle="v3.0.0 — Showtime", style="fireworks",
                     sound=not skip_audio)
            time.sleep(1.0)
            FX.boot_sequence(sound=not skip_audio)
            time.sleep(0.5)
            FX.matrix_intro("THE MATRIX HAS YOU", duration=2.5,
                            sound=not skip_audio)
            FX.terminal_hack("ACCESS GRANTED", sound=not skip_audio)
            time.sleep(0.5)
            print("\n  Ghost sprite incoming…\n")
            Sprite.preset("ghost", color="#a78bfa").move(from_x=2, to_x=70, duration=2.5, bob=True)
            print("\n  Sprite race…\n")
            Sprite.race(["rocket", "ufo", "car"], length=50,
                        colors=["#ff4444", "#00ccff", "#ffd60a"])
            print("\n  Level-up effect\n")
            FX.level_up("LEVEL 99", sparkles=True, sound=not skip_audio)
            time.sleep(0.6)
            print("\n  Celebrate\n")
            FX.celebrate("ALL DONE!", confetti=True, sound=not skip_audio)
            time.sleep(0.4)
            FX.outro("See you!", style="confetti", sound=not skip_audio)
        finally:
            Console.show_cursor()
