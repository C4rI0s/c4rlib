import os
import sys
import time
import math
import struct
import threading
import subprocess


_IS_WINDOWS = os.name == "nt"
_IS_MAC     = sys.platform == "darwin"
_IS_LINUX   = sys.platform.startswith("linux")

try:
    if _IS_WINDOWS:
        import winsound
        _HAS_WINSOUND = True
    else:
        _HAS_WINSOUND = False
except Exception:
    _HAS_WINSOUND = False


def _which(cmd: str) -> bool:
    from shutil import which
    return which(cmd) is not None


_AUDIO_PLAYER = None
if _IS_MAC and _which("afplay"):
    _AUDIO_PLAYER = "afplay"
elif _IS_LINUX:
    for p in ("paplay", "aplay", "play", "ffplay"):
        if _which(p):
            _AUDIO_PLAYER = p
            break


# ─────────────────────────────────────────────────────────────────────────────
# Note-frequency lookup (equal-temperament)
# ─────────────────────────────────────────────────────────────────────────────
_NOTES = {
    "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5,
    "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11,
}


def _note_to_freq(note: str) -> int:
    if not note or note in ("R", "rest"):
        return 0
    n     = note.strip()
    octv  = int(n[-1])
    pitch = n[:-1]
    if pitch not in _NOTES:
        return 0
    semitones_from_a4 = (octv - 4) * 12 + _NOTES[pitch] - _NOTES["A"]
    return int(440.0 * (2 ** (semitones_from_a4 / 12.0)))


def _generate_wav(notes: list, sample_rate: int = 22050,
                  amplitude: int = 16000, fade: float = 0.01) -> bytes:
    """Generate a tiny PCM WAV in memory from a list of (note, duration_s)."""
    samples = []
    for note, dur in notes:
        f       = _note_to_freq(note)
        n       = int(sample_rate * dur)
        fade_n  = int(sample_rate * fade)
        for i in range(n):
            if f == 0:
                samples.append(0)
            else:
                v = amplitude * math.sin(2 * math.pi * f * i / sample_rate)
                # square-ish to feel chiptune
                v = amplitude if v > 0 else -amplitude
                if i < fade_n:
                    v *= i / fade_n
                elif i > n - fade_n:
                    v *= (n - i) / fade_n
                samples.append(int(v))
    pcm = b"".join(struct.pack("<h", s) for s in samples)
    n   = len(samples)
    header = (
        b"RIFF" + struct.pack("<I", 36 + n * 2) + b"WAVE"
        + b"fmt " + struct.pack("<IHHIIHH", 16, 1, 1, sample_rate, sample_rate * 2, 2, 16)
        + b"data" + struct.pack("<I", n * 2)
    )
    return header + pcm


def _play_wav_bytes(data: bytes) -> bool:
    """Play wav bytes blocking; return True if it played."""
    if _HAS_WINSOUND:
        try:
            winsound.PlaySound(data, winsound.SND_MEMORY)
            return True
        except Exception:
            return False
    # write to temp file, play with system player
    if _AUDIO_PLAYER:
        import tempfile
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(data)
                path = f.name
            subprocess.run([_AUDIO_PLAYER, path],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           check=False)
            try: os.remove(path)
            except Exception: pass
            return True
        except Exception:
            return False
    return False


class Audio:
    @staticmethod
    def is_available() -> bool:
        return _HAS_WINSOUND or _AUDIO_PLAYER is not None or True  # bell always works

    @staticmethod
    def beep(freq: int = 800, duration: float = 0.1) -> None:
        if _HAS_WINSOUND:
            try:
                winsound.Beep(max(37, min(freq, 32767)), int(duration * 1000))
                return
            except Exception:
                pass
        if _AUDIO_PLAYER:
            wav = _generate_wav([(_freq_to_note(freq), duration)])
            _play_wav_bytes(wav)
            return
        sys.stdout.write("\a")
        sys.stdout.flush()

    @staticmethod
    def play_freq(freq: int, duration: float = 0.2) -> None:
        Audio.beep(freq, duration)

    @staticmethod
    def play_freqs(freqs: list, duration: float = 0.15) -> None:
        for f in freqs:
            Audio.beep(f, duration)

    # ── Quick presets (composed of beeps/freq) ──────────────────────────────
    @staticmethod
    def success() -> None:
        Audio.play_freqs([523, 659, 784], duration=0.1)

    @staticmethod
    def error() -> None:
        Audio.play_freqs([400, 300, 200], duration=0.12)

    @staticmethod
    def warning() -> None:
        Audio.play_freqs([700, 700], duration=0.15)

    @staticmethod
    def notify() -> None:
        Audio.play_freqs([880, 1100], duration=0.08)

    @staticmethod
    def click() -> None:
        Audio.beep(1200, 0.015)

    @staticmethod
    def pop() -> None:
        Audio.beep(450, 0.04)

    @staticmethod
    def coin() -> None:
        Audio.play_freqs([988, 1319], duration=0.1)

    @staticmethod
    def powerup() -> None:
        Audio.play_freqs([523, 659, 784, 1047], duration=0.08)

    @staticmethod
    def gameover() -> None:
        Audio.play_freqs([523, 466, 415, 349, 311], duration=0.18)

    @staticmethod
    def fanfare() -> None:
        Audio.play_freqs([523, 659, 784, 523, 659, 784, 1047], duration=0.12)

    @staticmethod
    def alarm(times: int = 3) -> None:
        for _ in range(times):
            Audio.beep(1000, 0.15)
            time.sleep(0.05)
            Audio.beep(700, 0.15)
            time.sleep(0.05)

    @staticmethod
    def play_async(callable_, *args, **kwargs) -> threading.Thread:
        """Run any Audio.* method in background. Example:
            Audio.play_async(Audio.fanfare)
        """
        t = threading.Thread(target=callable_, args=args, kwargs=kwargs, daemon=True)
        t.start()
        return t


def _freq_to_note(freq: int) -> str:
    """Reverse map (approximate) — needed for non-winsound playback."""
    if freq <= 0: return "R"
    semis = round(12 * math.log2(freq / 440.0))
    octv  = 4 + (semis + 9) // 12
    pitch_idx = (semis + 9) % 12
    names = ["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
    name  = names[pitch_idx]
    if name in ("A","A#","B"):
        octv = octv - 1 if pitch_idx >= 3 else octv  # keep simple
    return f"{name}{octv}"


class Sound:
    """Play sound files (WAV preferred)."""

    @staticmethod
    def play(path: str) -> bool:
        if not os.path.isfile(path):
            return False
        if _HAS_WINSOUND and path.lower().endswith(".wav"):
            try:
                winsound.PlaySound(path, winsound.SND_FILENAME)
                return True
            except Exception:
                return False
        if _AUDIO_PLAYER:
            try:
                subprocess.run([_AUDIO_PLAYER, path],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL,
                               check=False)
                return True
            except Exception:
                return False
        return False

    @staticmethod
    def play_async(path: str) -> threading.Thread:
        t = threading.Thread(target=Sound.play, args=(path,), daemon=True)
        t.start()
        return t

    @staticmethod
    def stop() -> None:
        if _HAS_WINSOUND:
            try:
                winsound.PlaySound(None, winsound.SND_PURGE)
            except Exception:
                pass


# ─────────────────────────────────────────────────────────────────────────────
# Melody — sequences of (note, duration)
# ─────────────────────────────────────────────────────────────────────────────
_MELODY_PRESETS = {
    "mario_intro": [
        ("E5",0.1),("E5",0.1),("R",0.1),("E5",0.1),("R",0.1),("C5",0.1),("E5",0.1),
        ("G5",0.2),("R",0.2),("G4",0.2),
    ],
    "zelda_secret": [
        ("G4",0.15),("F#4",0.15),("D#4",0.15),("A4",0.15),
        ("G#4",0.15),("E4",0.15),("G#4",0.15),("C5",0.3),
    ],
    "tetris_loop": [
        ("E5",0.2),("B4",0.1),("C5",0.1),("D5",0.2),("C5",0.1),("B4",0.1),
        ("A4",0.2),("A4",0.1),("C5",0.1),("E5",0.2),("D5",0.1),("C5",0.1),
        ("B4",0.3),("C5",0.1),("D5",0.2),("E5",0.2),("C5",0.2),("A4",0.2),
    ],
    "victory": [
        ("C5",0.15),("E5",0.15),("G5",0.15),("C6",0.3),
        ("G5",0.15),("C6",0.45),
    ],
    "defeat": [
        ("C5",0.2),("B4",0.2),("A4",0.2),("G4",0.2),("F4",0.4),
    ],
    "level_up": [
        ("C5",0.08),("D5",0.08),("E5",0.08),("F5",0.08),("G5",0.08),
        ("A5",0.08),("B5",0.08),("C6",0.3),
    ],
    "coin_collect": [
        ("B5",0.08),("E6",0.25),
    ],
    "alert": [
        ("A5",0.15),("F5",0.15),("A5",0.15),("F5",0.15),
    ],
    "doorbell": [
        ("E5",0.3),("C5",0.6),
    ],
    "jingle": [
        ("C5",0.15),("E5",0.15),("G5",0.15),("E5",0.15),("C5",0.3),
    ],
    "ufo": [
        ("E5",0.1),("F#5",0.1),("G5",0.1),("A5",0.1),("B5",0.1),("C6",0.1),
        ("B5",0.1),("A5",0.1),("G5",0.1),("F#5",0.1),("E5",0.2),
    ],
    "powerdown": [
        ("G5",0.1),("F5",0.1),("E5",0.1),("D5",0.1),("C5",0.1),("B4",0.1),
        ("A4",0.1),("G4",0.3),
    ],
    "fanfare": [
        ("C5",0.12),("E5",0.12),("G5",0.12),("C6",0.25),
        ("G5",0.12),("C6",0.4),
    ],
    "intro": [
        ("E5",0.1),("G5",0.1),("C6",0.1),("E6",0.25),
    ],
    "boot": [
        ("C4",0.08),("E4",0.08),("G4",0.08),("C5",0.15),
    ],
}


class Melody:
    @staticmethod
    def play(notes: list) -> None:
        """Play a list of (note, duration) tuples."""
        if _HAS_WINSOUND:
            for n, d in notes:
                f = _note_to_freq(n)
                if f == 0:
                    time.sleep(d)
                else:
                    try:
                        winsound.Beep(max(37, min(f, 32767)), int(d * 1000))
                    except Exception:
                        time.sleep(d)
            return
        wav = _generate_wav(notes)
        if not _play_wav_bytes(wav):
            for _, d in notes:
                sys.stdout.write("\a"); sys.stdout.flush()
                time.sleep(d)

    @staticmethod
    def play_async(notes: list) -> threading.Thread:
        t = threading.Thread(target=Melody.play, args=(notes,), daemon=True)
        t.start()
        return t

    @staticmethod
    def preset(name: str) -> None:
        if name not in _MELODY_PRESETS:
            raise ValueError(f"Unknown melody '{name}'. Available: {Melody.list_presets()}")
        Melody.play(_MELODY_PRESETS[name])

    @staticmethod
    def preset_async(name: str) -> threading.Thread:
        if name not in _MELODY_PRESETS:
            raise ValueError(f"Unknown melody '{name}'.")
        return Melody.play_async(_MELODY_PRESETS[name])

    @staticmethod
    def list_presets() -> list:
        return sorted(_MELODY_PRESETS.keys())
