import random
import string


class TextStyle:
    _FANCY_LOWER    = "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃"
    _FANCY_UPPER    = "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩"
    _DOUBLE_LOWER   = "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫"
    _DOUBLE_UPPER   = "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"
    _CURSIVE_LOWER  = "𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏"
    _CURSIVE_UPPER  = "𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"
    _FRAKTUR_LOWER  = "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟"
    _FRAKTUR_UPPER  = "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅"
    _SYLLABIC       = "ᗩᗷᑕᗪEᖴGᕼIᒍKᒪᗰᑎOᑭᑫᖇᔕTᑌᐯᗯ᙭Yᘔ"
    _BOLD_LOWER     = "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳"
    _BOLD_UPPER     = "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙"
    _SANS_LOWER     = "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇"
    _SANS_UPPER     = "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"
    _MONO_LOWER     = "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣"
    _MONO_UPPER     = "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉"

    @staticmethod
    def _convert(text: str, lower_map: str, upper_map: str) -> str:
        result = []
        for ch in text:
            if "a" <= ch <= "z":
                result.append(lower_map[ord(ch)-ord("a")])
            elif "A" <= ch <= "Z":
                result.append(upper_map[ord(ch)-ord("A")])
            else:
                result.append(ch)
        return "".join(result)

    @staticmethod
    def fancy(text: str) -> str:
        return TextStyle._convert(text, TextStyle._FANCY_LOWER, TextStyle._FANCY_UPPER)

    @staticmethod
    def double_struck(text: str) -> str:
        return TextStyle._convert(text, TextStyle._DOUBLE_LOWER, TextStyle._DOUBLE_UPPER)

    @staticmethod
    def cursive(text: str) -> str:
        return TextStyle._convert(text, TextStyle._CURSIVE_LOWER, TextStyle._CURSIVE_UPPER)

    @staticmethod
    def fraktur(text: str) -> str:
        return TextStyle._convert(text, TextStyle._FRAKTUR_LOWER, TextStyle._FRAKTUR_UPPER)

    @staticmethod
    def bold_serif(text: str) -> str:
        return TextStyle._convert(text, TextStyle._BOLD_LOWER, TextStyle._BOLD_UPPER)

    @staticmethod
    def sans_bold(text: str) -> str:
        return TextStyle._convert(text, TextStyle._SANS_LOWER, TextStyle._SANS_UPPER)

    @staticmethod
    def monospace(text: str) -> str:
        return TextStyle._convert(text, TextStyle._MONO_LOWER, TextStyle._MONO_UPPER)

    @staticmethod
    def syllabic(text: str) -> str:
        result = []
        for ch in text:
            if "a" <= ch <= "z":
                result.append(TextStyle._SYLLABIC[ord(ch)-ord("a")])
            elif "A" <= ch <= "Z":
                result.append(TextStyle._SYLLABIC[ord(ch)-ord("A")])
            else:
                result.append(ch)
        return "".join(result)

    @staticmethod
    def strikethrough(text: str) -> str:
        return "".join(c + "\u0337" for c in text)

    @staticmethod
    def underline_text(text: str) -> str:
        return "".join(c + "\u0332" for c in text)

    @staticmethod
    def overline_text(text: str) -> str:
        return "".join(c + "\u0305" for c in text)

    @staticmethod
    def double_underline(text: str) -> str:
        return "".join(c + "\u0333" for c in text)

    @staticmethod
    def small_caps(text: str) -> str:
        sc = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘQʀꜱᴛᴜᴠᴡxʏᴢ"
        return "".join(sc[ord(c)-ord("a")] if "a" <= c <= "z" else c for c in text)

    @staticmethod
    def wide(text: str) -> str:
        return "".join(chr(ord(c)+0xFEE0) if "!" <= c <= "~" else c for c in text)

    @staticmethod
    def superscript(text: str) -> str:
        table = str.maketrans("abcdefghijklmnoprstuvwxyz0123456789",
                              "ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹")
        return text.translate(table)

    @staticmethod
    def subscript(text: str) -> str:
        table = str.maketrans("0123456789aehijklmnoprstuvx",
                              "₀₁₂₃₄₅₆₇₈₉ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ")
        return text.translate(table)

    @staticmethod
    def zalgo(text: str, intensity: int = 3) -> str:
        combining = [chr(i) for i in range(0x0300, 0x036F)]
        result = []
        for ch in text:
            result.append(ch)
            for _ in range(intensity):
                result.append(random.choice(combining))
        return "".join(result)

    @staticmethod
    def reverse(text: str) -> str:
        return text[::-1]

    @staticmethod
    def mirror(text: str) -> str:
        table = str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "ÀBƆDƎℲƃHIſKLWNOꟼQᴚƧTUVMXYZɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz"
        )
        return text[::-1].translate(table)

    @staticmethod
    def alternate_case(text: str) -> str:
        return "".join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(text))

    @staticmethod
    def leet(text: str) -> str:
        table = str.maketrans("aAeEiIoOsSbBtTgGlL", "4433117755886677|1")
        return text.translate(table)

    @staticmethod
    def nato(text: str) -> str:
        alphabet = {
            "a":"Alpha","b":"Bravo","c":"Charlie","d":"Delta","e":"Echo",
            "f":"Foxtrot","g":"Golf","h":"Hotel","i":"India","j":"Juliet",
            "k":"Kilo","l":"Lima","m":"Mike","n":"November","o":"Oscar",
            "p":"Papa","q":"Quebec","r":"Romeo","s":"Sierra","t":"Tango",
            "u":"Uniform","v":"Victor","w":"Whiskey","x":"X-ray","y":"Yankee","z":"Zulu"
        }
        return " ".join(alphabet.get(c.lower(), c) for c in text)

    @staticmethod
    def morse(text: str) -> str:
        table = {
            "a":".-","b":"-...","c":"-.-.","d":"-..","e":".","f":"..-.","g":"--.","h":"....","i":"..","j":".---",
            "k":"-.-","l":".-..","m":"--","n":"-.","o":"---","p":".--.","q":"--.-","r":".-.","s":"...","t":"-",
            "u":"..-","v":"...-","w":".--","x":"-..-","y":"-.--","z":"--..",
            "0":"-----","1":".----","2":"..---","3":"...--","4":"....-","5":".....",
            "6":"-....","7":"--...","8":"---..","9":"----."," ":"/"
        }
        return " ".join(table.get(c.lower(), c) for c in text)

    @staticmethod
    def binary(text: str) -> str:
        return " ".join(format(ord(c), "08b") for c in text)

    @staticmethod
    def hex_encode(text: str) -> str:
        return " ".join(format(ord(c), "02x") for c in text)

    @staticmethod
    def rot13(text: str) -> str:
        result = []
        for ch in text:
            if "a" <= ch <= "z":
                result.append(chr((ord(ch)-ord("a")+13) % 26 + ord("a")))
            elif "A" <= ch <= "Z":
                result.append(chr((ord(ch)-ord("A")+13) % 26 + ord("A")))
            else:
                result.append(ch)
        return "".join(result)

    @staticmethod
    def caesar(text: str, shift: int = 3) -> str:
        result = []
        for ch in text:
            if "a" <= ch <= "z":
                result.append(chr((ord(ch)-ord("a")+shift) % 26 + ord("a")))
            elif "A" <= ch <= "Z":
                result.append(chr((ord(ch)-ord("A")+shift) % 26 + ord("A")))
            else:
                result.append(ch)
        return "".join(result)

    @staticmethod
    def bubble(text: str) -> str:
        lower = "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ"
        upper = "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ"
        result = []
        for ch in text:
            if "a" <= ch <= "z":
                result.append(lower[ord(ch)-ord("a")])
            elif "A" <= ch <= "Z":
                result.append(upper[ord(ch)-ord("A")])
            else:
                result.append(ch)
        return "".join(result)

    @staticmethod
    def negative_square(text: str) -> str:
        lower = "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩"
        upper = "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩"
        result = []
        for ch in text:
            if "a" <= ch <= "z":
                result.append(lower[ord(ch)-ord("a")])
            elif "A" <= ch <= "Z":
                result.append(upper[ord(ch)-ord("A")])
            else:
                result.append(ch)
        return "".join(result)

    @staticmethod
    def space_out(text: str, spaces: int = 1) -> str:
        return (" " * spaces).join(text)

    @staticmethod
    def clap(text: str) -> str:
        return " 👏 ".join(text.split())

    @staticmethod
    def uwuify(text: str) -> str:
        text = text.replace("r", "w").replace("l", "w")
        text = text.replace("R", "W").replace("L", "W")
        text = text.replace("na", "nya").replace("ni", "nyi")
        text = text.replace("no", "nyo").replace("nu", "nyu")
        suffixes = [" uwu", " owo", " :3", " >w<", " rawr"]
        return text + random.choice(suffixes)

    @staticmethod
    def repeat_chars(text: str, times: int = 2) -> str:
        return "".join(c * times for c in text)

    @staticmethod
    def titlecase(text: str) -> str:
        return text.title()

    @staticmethod
    def word_count(text: str) -> int:
        return len(text.split())

    @staticmethod
    def char_count(text: str, include_spaces: bool = True) -> int:
        return len(text) if include_spaces else len(text.replace(" ", ""))

    @staticmethod
    def truncate(text: str, max_len: int = 50, suffix: str = "...") -> str:
        return text[:max_len-len(suffix)] + suffix if len(text) > max_len else text

    @staticmethod
    def pad_left(text: str, width: int, char: str = " ") -> str:
        return text.rjust(width, char)

    @staticmethod
    def pad_right(text: str, width: int, char: str = " ") -> str:
        return text.ljust(width, char)

    @staticmethod
    def pad_center(text: str, width: int, char: str = " ") -> str:
        return text.center(width, char)

    @staticmethod
    def wrap(text: str, width: int = 80) -> str:
        words  = text.split()
        lines  = []
        current = ""
        for word in words:
            if len(current) + len(word) + 1 <= width:
                current += (" " if current else "") + word
            else:
                if current: lines.append(current)
                current = word
        if current: lines.append(current)
        return "\n".join(lines)
