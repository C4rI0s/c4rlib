from .terminal import Terminal
from .colors import ColorUtils, Gradient, GradientPresets


class Box:
    @staticmethod
    def _make(tl, tr, bl, br, h, v, text: str, color: str = None) -> str:
        w      = len(text) + 2
        top    = tl + h * w + tr
        middle = v  + f" {text} " + v
        bottom = bl + h * w + br
        result = f"{top}\n{middle}\n{bottom}"
        if color:
            result = f"{ColorUtils.hex(color)}{result}{ColorUtils.reset()}"
        return result

    @staticmethod
    def double(text: str, color: str = None) -> str:
        return Box._make("╔","╗","╚","╝","═","║", text, color)

    @staticmethod
    def rounded(text: str, color: str = None) -> str:
        return Box._make("╭","╮","╰","╯","─","│", text, color)

    @staticmethod
    def heavy(text: str, color: str = None) -> str:
        return Box._make("┏","┓","┗","┛","━","┃", text, color)

    @staticmethod
    def simple(text: str, color: str = None) -> str:
        return Box._make("┌","┐","└","┘","─","│", text, color)

    @staticmethod
    def dots(text: str, color: str = None) -> str:
        return Box._make("·","·","·","·","·","·", text, color)

    @staticmethod
    def stars(text: str, color: str = None) -> str:
        return Box._make("★","★","★","★","★","★", text, color)

    @staticmethod
    def hash_box(text: str, color: str = None) -> str:
        return Box._make("#","#","#","#","#","#", text, color)

    @staticmethod
    def ascii(text: str, color: str = None) -> str:
        return Box._make("+","+","+","+","-","|", text, color)

    @staticmethod
    def diamond(text: str, color: str = None) -> str:
        return Box._make("◆","◆","◆","◆","◆","◆", text, color)

    @staticmethod
    def arrows(text: str, color: str = None) -> str:
        return Box._make("»","«","»","«","─","│", text, color)

    @staticmethod
    def classic_round(text: str, color: str = None) -> str:
        return Box._make("╭","╮","╰","╯","━","┃", text, color)

    @staticmethod
    def neon(text: str, color: str = "#00ccff") -> str:
        w      = len(text) + 2
        col    = ColorUtils.hex(color)
        glow   = ColorUtils.hex(ColorUtils.lighten(color, 0.3)) if color else col
        top    = col + "╔" + "═" * w + "╗" + ColorUtils.reset()
        mid    = col + "║" + ColorUtils.reset() + f" {glow}{text}{ColorUtils.reset()} " + col + "║" + ColorUtils.reset()
        bot    = col + "╚" + "═" * w + "╝" + ColorUtils.reset()
        return f"{top}\n{mid}\n{bot}"

    @staticmethod
    def gradient_box(text: str, start: tuple = (0,200,255), end: tuple = (200,0,255)) -> str:
        w   = len(text) + 2
        top = "╭" + "─" * w + "╮"
        mid = "│" + f" {text} " + "│"
        bot = "╰" + "─" * w + "╯"
        return Gradient.apply(f"{top}\n{mid}\n{bot}", start, end)

    @staticmethod
    def multiline(lines: list, style: str = "rounded", color: str = None) -> str:
        styles = {
            "rounded": ("╭","╮","╰","╯","─","│"),
            "double":  ("╔","╗","╚","╝","═","║"),
            "heavy":   ("┏","┓","┗","┛","━","┃"),
            "simple":  ("┌","┐","└","┘","─","│"),
            "ascii":   ("+","+","+","+","-","|"),
        }
        tl, tr, bl, br, h, v = styles.get(style, styles["rounded"])
        width  = max(Terminal.display_width(l) for l in lines) + 2
        # Content rows carry two spaces of padding on the left and one on the
        # right, so the border spans width + 3. It used to span width + 2,
        # leaving every box one character short of its own contents.
        top    = tl + h * (width + 3) + tr
        bottom = bl + h * (width + 3) + br
        rows   = [top]
        for line in lines:
            rows.append(f"{v}  {Terminal.pad_display(line, width)} {v}")
        rows.append(bottom)
        result = "\n".join(rows)
        if color:
            result = f"{ColorUtils.hex(color)}{result}{ColorUtils.reset()}"
        return result

    @staticmethod
    def titled(title: str, lines: list, style: str = "rounded", title_color: str = "#00ccff", border_color: str = "#6c757d") -> str:
        styles = {
            "rounded": ("╭","╮","╰","╯","─","│","├","┤"),
            "double":  ("╔","╗","╚","╝","═","║","╠","╣"),
            "heavy":   ("┏","┓","┗","┛","━","┃","┣","┫"),
        }
        tl, tr, bl, br, h, v, ml, mr = styles.get(style, styles["rounded"])
        width  = max(max(Terminal.display_width(l) for l in lines),
                     Terminal.display_width(title)) + 2
        bc     = ColorUtils.hex(border_color)
        tc     = ColorUtils.hex(title_color)
        reset  = ColorUtils.reset()
        # Border spans width + 3 to match the content rows' 2 + width + 1.
        rows   = []
        rows.append(bc + tl + h*(width+3) + tr + reset)
        rows.append(bc + v + reset + "  " + tc +
                    Terminal.pad_display(title, width, "center") + reset +
                    " " + bc + v + reset)
        rows.append(bc + ml + h*(width+3) + mr + reset)
        for line in lines:
            rows.append(bc + v + reset + f"  {Terminal.pad_display(line, width)} " +
                        bc + v + reset)
        rows.append(bc + bl + h*(width+3) + br + reset)
        return "\n".join(rows)


class Banner:
    @staticmethod
    def line(text: str, char: str = "─", color: str = None) -> str:
        pad    = char * 14
        result = f"{pad} {text} {pad}"
        if color:
            result = f"{ColorUtils.hex(color)}{result}{ColorUtils.reset()}"
        return result

    @staticmethod
    def double_line(text: str, color: str = None) -> str:
        bar    = "═" * (len(text) + 28)
        result = f"{bar}\n{text.center(len(bar))}\n{bar}"
        if color:
            result = f"{ColorUtils.hex(color)}{result}{ColorUtils.reset()}"
        return result

    @staticmethod
    def arrow_line(text: str, color: str = None) -> str:
        result = f"─═{'═'*(len(text)//2)}❯❯ {text} ❮❮{'═'*(len(text)//2)}═─"
        if color:
            result = f"{ColorUtils.hex(color)}{result}{ColorUtils.reset()}"
        return result

    @staticmethod
    def heart_line(text: str, color: str = None) -> str:
        bar    = "━" * (len(text) + 12)
        result = f"❤{bar}❤\n    {text}\n❤{bar}❤"
        if color:
            result = f"{ColorUtils.hex(color)}{result}{ColorUtils.reset()}"
        return result

    @staticmethod
    def wave_line(text: str, color: str = None) -> str:
        result = f"~{'≈'*8} {text} {'≈'*8}~"
        if color:
            result = f"{ColorUtils.hex(color)}{result}{ColorUtils.reset()}"
        return result

    @staticmethod
    def star_line(text: str, color: str = None) -> str:
        result = f"{'★'*4} {text} {'★'*4}"
        if color:
            result = f"{ColorUtils.hex(color)}{result}{ColorUtils.reset()}"
        return result

    @staticmethod
    def dot_line(text: str, color: str = None) -> str:
        result = f"{'·'*10} {text} {'·'*10}"
        if color:
            result = f"{ColorUtils.hex(color)}{result}{ColorUtils.reset()}"
        return result

    @staticmethod
    def slash_line(text: str, color: str = None) -> str:
        result = f"{'╱╲'*4} {text} {'╱╲'*4}"
        if color:
            result = f"{ColorUtils.hex(color)}{result}{ColorUtils.reset()}"
        return result

    @staticmethod
    def diamond_line(text: str, color: str = None) -> str:
        result = f"◆{'─'*6}◆ {text} ◆{'─'*6}◆"
        if color:
            result = f"{ColorUtils.hex(color)}{result}{ColorUtils.reset()}"
        return result

    @staticmethod
    def lightning_line(text: str, color: str = None) -> str:
        result = f"⚡{'━'*6} {text} {'━'*6}⚡"
        if color:
            result = f"{ColorUtils.hex(color)}{result}{ColorUtils.reset()}"
        return result

    @staticmethod
    def fire_line(text: str, color: str = None) -> str:
        result = f"🔥{'─'*6} {text} {'─'*6}🔥"
        if color:
            result = f"{ColorUtils.hex(color)}{result}{ColorUtils.reset()}"
        return result

    @staticmethod
    def gradient_banner(text: str, start: tuple = (0,200,255), end: tuple = (200,0,255)) -> str:
        full = f"  ══{'═'*6}  {text}  {'═'*6}══  "
        return Gradient.apply(full, start, end)

    @staticmethod
    def title(text: str, color: str = "#00ccff") -> str:
        width  = max(len(text) + 8, 40)
        top    = "╔" + "═" * width + "╗"
        mid    = "║" + text.center(width) + "║"
        bot    = "╚" + "═" * width + "╝"
        col    = ColorUtils.hex(color)
        return f"{col}{top}\n{mid}\n{bot}{ColorUtils.reset()}"

    @staticmethod
    def gradient_title(text: str, start: tuple = (0,200,255), end: tuple = (200,0,255)) -> str:
        width = max(len(text) + 8, 40)
        top   = "╔" + "═" * width + "╗"
        mid   = "║" + text.center(width) + "║"
        bot   = "╚" + "═" * width + "╝"
        return Gradient.apply(f"{top}\n{mid}\n{bot}", start, end)

    @staticmethod
    def center(text: str, width: int = 80, color: str = None) -> str:
        result = text.center(width)
        if color:
            result = f"{ColorUtils.hex(color)}{result}{ColorUtils.reset()}"
        return result

    @staticmethod
    def section(text: str, color: str = "#00ccff") -> str:
        col    = ColorUtils.hex(color)
        gray   = ColorUtils.hex("#6c757d")
        reset  = ColorUtils.reset()
        line   = gray + "─" * 60 + reset
        label  = col + f"  {text}  " + reset
        return f"{line}\n{label}\n{line}"

    @staticmethod
    def giant(text: str, font: str = "standard", color: str = None,
              gradient: tuple = None) -> str:
        """Giant FIGlet-rendered banner. Falls back to block style if pyfiglet is missing."""
        from .ascii import Figlet, Ascii, _HAS_FIGLET
        if gradient:
            return Figlet.gradient(text, font=font, start=gradient[0], end=gradient[1])
        rendered = Figlet.render(text, font=font) if _HAS_FIGLET else Ascii.banner(text, "block")
        if color:
            col = ColorUtils.hex(color)
            return "\n".join(col + line + ColorUtils.reset() for line in rendered.split("\n"))
        return rendered

    @staticmethod
    def print_giant(text: str, font: str = "standard", color: str = None,
                    gradient: tuple = None) -> None:
        print(Banner.giant(text, font=font, color=color, gradient=gradient))
