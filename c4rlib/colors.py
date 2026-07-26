import colorsys
import random

from .terminal import Terminal


class ColorUtils:
    # Kept as literals for backwards compatibility and for callers that build
    # sequences by hand. Prefer the methods below, which return "" when the
    # output is not a terminal — see c4rlib.terminal.
    RESET         = "\033[0m"
    BOLD          = "\033[1m"
    DIM           = "\033[2m"
    ITALIC        = "\033[3m"
    UNDERLINE     = "\033[4m"
    BLINK         = "\033[5m"
    RAPID_BLINK   = "\033[6m"
    REVERSE       = "\033[7m"
    HIDDEN        = "\033[8m"
    STRIKETHROUGH = "\033[9m"
    DOUBLE_UNDER  = "\033[21m"
    OVERLINE      = "\033[53m"

    @staticmethod
    def reset() -> str:
        """The reset sequence, or "" when colour is off."""
        return Terminal.reset()

    @staticmethod
    def rgb(r: int, g: int, b: int) -> str:
        return Terminal.fg(r, g, b)

    @staticmethod
    def bg_rgb(r: int, g: int, b: int) -> str:
        return Terminal.bg(r, g, b)

    @staticmethod
    def hex(hex_color: str) -> str:
        return Terminal.fg(*ColorUtils.hex_to_rgb(hex_color))

    @staticmethod
    def bg_hex(hex_color: str) -> str:
        return Terminal.bg(*ColorUtils.hex_to_rgb(hex_color))

    @staticmethod
    def hsl(h: int, s: int, l: int) -> str:
        r, g, b = colorsys.hls_to_rgb(h/360, l/100, s/100)
        return Terminal.fg(int(r*255), int(g*255), int(b*255))

    @staticmethod
    def bg_hsl(h: int, s: int, l: int) -> str:
        r, g, b = colorsys.hls_to_rgb(h/360, l/100, s/100)
        return Terminal.bg(int(r*255), int(g*255), int(b*255))

    @staticmethod
    def paint(text: str, hex_color: str) -> str:
        return f"{ColorUtils.hex(hex_color)}{text}{ColorUtils.reset()}"

    @staticmethod
    def bg_paint(text: str, fg: str, bg: str) -> str:
        return f"{ColorUtils.hex(fg)}{ColorUtils.bg_hex(bg)}{text}{ColorUtils.reset()}"

    @staticmethod
    def _attr(text: str, code: str) -> str:
        return f"{Terminal.sgr(code)}{text}{ColorUtils.reset()}"

    @staticmethod
    def bold(text: str) -> str:
        return ColorUtils._attr(text, "1")

    @staticmethod
    def italic(text: str) -> str:
        return ColorUtils._attr(text, "3")

    @staticmethod
    def underline(text: str) -> str:
        return ColorUtils._attr(text, "4")

    @staticmethod
    def strike(text: str) -> str:
        return ColorUtils._attr(text, "9")

    @staticmethod
    def blink(text: str) -> str:
        return ColorUtils._attr(text, "5")

    @staticmethod
    def dim(text: str) -> str:
        return ColorUtils._attr(text, "2")

    @staticmethod
    def reverse_text(text: str) -> str:
        return ColorUtils._attr(text, "7")

    @staticmethod
    def overline(text: str) -> str:
        return ColorUtils._attr(text, "53")

    @staticmethod
    def rainbow(text: str) -> str:
        colors = [(255,0,0),(255,127,0),(255,255,0),(0,255,0),(0,0,255),(75,0,130),(148,0,211)]
        result = ""
        for i, char in enumerate(text):
            result += Terminal.fg(*colors[i % len(colors)]) + char
        return result + ColorUtils.reset()

    @staticmethod
    def random_color(text: str) -> str:
        r, g, b = random.randint(50,255), random.randint(50,255), random.randint(50,255)
        return f"{Terminal.fg(r, g, b)}{text}{ColorUtils.reset()}"

    @staticmethod
    def style(text: str, hex_color: str, bold: bool = False, italic: bool = False, underline: bool = False) -> str:
        result = ColorUtils.hex(hex_color)
        if bold:      result += Terminal.sgr("1")
        if italic:    result += Terminal.sgr("3")
        if underline: result += Terminal.sgr("4")
        return result + text + ColorUtils.reset()

    @staticmethod
    def hex_to_rgb(hex_color: str) -> tuple:
        """Accepts ``#rrggbb`` and the ``#rgb`` shorthand, with or without ``#``."""
        h = hex_color.lstrip("#")
        if len(h) == 3:
            h = h[0]*2 + h[1]*2 + h[2]*2
        if len(h) != 6:
            raise ValueError(f"not a hex colour: {hex_color!r}")
        return int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)

    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    @staticmethod
    def rgb_to_hsl(r: int, g: int, b: int) -> tuple:
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        return round(h*360), round(s*100), round(l*100)

    @staticmethod
    def blend(hex1: str, hex2: str, t: float = 0.5) -> str:
        r1, g1, b1 = ColorUtils.hex_to_rgb(hex1)
        r2, g2, b2 = ColorUtils.hex_to_rgb(hex2)
        return ColorUtils.rgb_to_hex(int(r1+(r2-r1)*t), int(g1+(g2-g1)*t), int(b1+(b2-b1)*t))

    @staticmethod
    def lighten(hex_color: str, amount: float = 0.2) -> str:
        r, g, b = ColorUtils.hex_to_rgb(hex_color)
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        r2, g2, b2 = colorsys.hls_to_rgb(h, min(1.0, l+amount), s)
        return ColorUtils.rgb_to_hex(int(r2*255), int(g2*255), int(b2*255))

    @staticmethod
    def darken(hex_color: str, amount: float = 0.2) -> str:
        r, g, b = ColorUtils.hex_to_rgb(hex_color)
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        r2, g2, b2 = colorsys.hls_to_rgb(h, max(0.0, l-amount), s)
        return ColorUtils.rgb_to_hex(int(r2*255), int(g2*255), int(b2*255))

    @staticmethod
    def complementary(hex_color: str) -> str:
        r, g, b = ColorUtils.hex_to_rgb(hex_color)
        return ColorUtils.rgb_to_hex(255-r, 255-g, 255-b)

    @staticmethod
    def palette(hex_color: str, steps: int = 5) -> list:
        if steps < 1:
            return []
        r, g, b = ColorUtils.hex_to_rgb(hex_color)
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        if steps == 1:
            return [hex_color if hex_color.startswith("#") else f"#{hex_color}"]
        result = []
        for i in range(steps):
            li = i / (steps-1)
            r2, g2, b2 = colorsys.hls_to_rgb(h, li, s)
            result.append(ColorUtils.rgb_to_hex(int(r2*255), int(g2*255), int(b2*255)))
        return result

    @staticmethod
    def triadic(hex_color: str) -> list:
        r, g, b = ColorUtils.hex_to_rgb(hex_color)
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        result = []
        for offset in [0, 120, 240]:
            h2 = (h + offset/360) % 1.0
            r2, g2, b2 = colorsys.hls_to_rgb(h2, l, s)
            result.append(ColorUtils.rgb_to_hex(int(r2*255), int(g2*255), int(b2*255)))
        return result


class GradientPresets:
    red_to_blue      = ((255,0,0),     (0,0,255))
    red_to_yellow    = ((255,0,0),     (255,255,0))
    red_to_green     = ((255,0,0),     (0,255,0))
    red_to_purple    = ((255,0,0),     (128,0,128))
    red_to_cyan      = ((255,0,0),     (0,255,255))
    red_to_gold      = ((255,0,0),     (255,215,0))
    red_to_pink      = ((255,0,0),     (255,105,180))
    red_to_white     = ((255,0,0),     (255,255,255))
    blue_to_green    = ((0,0,255),     (0,255,0))
    blue_to_purple   = ((0,0,255),     (128,0,128))
    blue_to_cyan     = ((0,0,255),     (0,255,255))
    blue_to_pink     = ((0,0,255),     (255,192,203))
    blue_to_white    = ((0,0,255),     (255,255,255))
    blue_to_gold     = ((0,0,255),     (255,215,0))
    blue_to_red      = ((0,0,255),     (255,0,0))
    blue_to_orange   = ((0,0,255),     (255,165,0))
    green_to_yellow  = ((0,255,0),     (255,255,0))
    green_to_cyan    = ((0,255,0),     (0,255,255))
    green_to_white   = ((0,255,0),     (255,255,255))
    green_to_blue    = ((0,255,0),     (0,0,255))
    green_to_gold    = ((0,255,0),     (255,215,0))
    purple_to_pink   = ((128,0,128),   (255,192,203))
    purple_to_cyan   = ((128,0,128),   (0,255,255))
    purple_to_gold   = ((128,0,128),   (255,215,0))
    purple_to_blue   = ((128,0,128),   (0,0,255))
    purple_to_white  = ((128,0,128),   (255,255,255))
    cyan_to_gold     = ((0,255,255),   (255,215,0))
    cyan_to_pink     = ((0,255,255),   (255,192,203))
    cyan_to_purple   = ((0,255,255),   (128,0,128))
    cyan_to_white    = ((0,255,255),   (255,255,255))
    cyan_to_red      = ((0,255,255),   (255,0,0))
    gold_to_white    = ((255,215,0),   (255,255,255))
    gold_to_red      = ((255,215,0),   (255,0,0))
    gold_to_purple   = ((255,215,0),   (128,0,128))
    gold_to_cyan     = ((255,215,0),   (0,255,255))
    orange_to_purple = ((255,165,0),   (128,0,128))
    orange_to_blue   = ((255,165,0),   (0,0,255))
    orange_to_cyan   = ((255,165,0),   (0,255,255))
    pink_to_purple   = ((255,192,203), (128,0,128))
    pink_to_blue     = ((255,192,203), (0,0,255))
    pink_to_cyan     = ((255,192,203), (0,255,255))
    white_to_black   = ((255,255,255), (0,0,0))
    black_to_white   = ((0,0,0),       (255,255,255))
    black_to_cyan    = ((0,0,0),       (0,255,255))
    black_to_gold    = ((0,0,0),       (255,215,0))
    black_to_purple  = ((0,0,0),       (128,0,128))
    neon_green_blue  = ((57,255,20),   (0,150,255))
    neon_pink_purple = ((255,0,110),   (140,0,255))
    neon_yellow_cyan = ((255,240,0),   (0,255,200))
    fire             = ((255,50,0),    (255,200,0))
    ice              = ((180,230,255), (0,100,255))
    toxic            = ((0,255,50),    (180,255,0))
    sunset           = ((255,100,0),   (200,0,100))
    ocean            = ((0,100,200),   (0,220,180))
    candy            = ((255,100,150), (150,100,255))
    matrix           = ((0,255,0),     (0,100,0))
    lava             = ((255,80,0),    (200,0,50))
    galaxy           = ((100,0,200),   (0,200,255))
    aurora           = ((0,255,150),   (100,0,255))
    blood            = ((180,0,0),     (80,0,0))
    mint             = ((0,255,150),   (0,200,100))
    rose             = ((255,0,80),    (255,150,180))
    electric         = ((0,200,255),   (150,0,255))


class Gradient:
    @staticmethod
    def apply(text: str, start: tuple, end: tuple) -> str:
        if len(text) <= 1:
            return f"{Terminal.fg(*start)}{text}{ColorUtils.reset()}"
        result = ""
        steps = len(text) - 1
        for i, char in enumerate(text):
            t = i / steps
            r = int((1-t)*start[0] + t*end[0])
            g = int((1-t)*start[1] + t*end[1])
            b = int((1-t)*start[2] + t*end[2])
            result += Terminal.fg(r, g, b) + char
        return result + ColorUtils.reset()

    @staticmethod
    def preset(text: str, preset) -> str:
        return Gradient.apply(text, preset[0], preset[1])

    @staticmethod
    def multicolor(text: str, colors: list) -> str:
        if not colors: return text
        if len(colors) == 1:
            return f"{Terminal.fg(*colors[0])}{text}{ColorUtils.reset()}"
        n = len(text)
        segments = len(colors) - 1
        result = ""
        for i, char in enumerate(text):
            pos = i / max(n-1, 1) * segments
            seg = min(int(pos), segments-1)
            t = pos - seg
            r = int((1-t)*colors[seg][0] + t*colors[seg+1][0])
            g = int((1-t)*colors[seg][1] + t*colors[seg+1][1])
            b = int((1-t)*colors[seg][2] + t*colors[seg+1][2])
            result += Terminal.fg(r, g, b) + char
        return result + ColorUtils.reset()

    @staticmethod
    def random_gradient(text: str) -> str:
        start = (random.randint(50,255), random.randint(50,255), random.randint(50,255))
        end   = (random.randint(50,255), random.randint(50,255), random.randint(50,255))
        return Gradient.apply(text, start, end)

    @staticmethod
    def bg_apply(text: str, start: tuple, end: tuple) -> str:
        if len(text) <= 1:
            return f"{Terminal.bg(*start)}{text}{ColorUtils.reset()}"
        result = ""
        steps = len(text) - 1
        for i, char in enumerate(text):
            t = i / steps
            r = int((1-t)*start[0] + t*end[0])
            g = int((1-t)*start[1] + t*end[1])
            b = int((1-t)*start[2] + t*end[2])
            result += Terminal.bg(r, g, b) + char
        return result + ColorUtils.reset()

    @staticmethod
    def fire(text: str) -> str:
        return Gradient.preset(text, GradientPresets.fire)

    @staticmethod
    def ice(text: str) -> str:
        return Gradient.preset(text, GradientPresets.ice)

    @staticmethod
    def toxic(text: str) -> str:
        return Gradient.preset(text, GradientPresets.toxic)

    @staticmethod
    def sunset(text: str) -> str:
        return Gradient.preset(text, GradientPresets.sunset)

    @staticmethod
    def ocean(text: str) -> str:
        return Gradient.preset(text, GradientPresets.ocean)

    @staticmethod
    def galaxy(text: str) -> str:
        return Gradient.preset(text, GradientPresets.galaxy)

    @staticmethod
    def neon(text: str) -> str:
        return Gradient.preset(text, GradientPresets.neon_pink_purple)

    @staticmethod
    def matrix(text: str) -> str:
        return Gradient.preset(text, GradientPresets.matrix)

    @staticmethod
    def lava(text: str) -> str:
        return Gradient.preset(text, GradientPresets.lava)

    @staticmethod
    def candy(text: str) -> str:
        return Gradient.preset(text, GradientPresets.candy)

    @staticmethod
    def aurora(text: str) -> str:
        return Gradient.preset(text, GradientPresets.aurora)

    @staticmethod
    def electric(text: str) -> str:
        return Gradient.preset(text, GradientPresets.electric)

    @staticmethod
    def rose(text: str) -> str:
        return Gradient.preset(text, GradientPresets.rose)
