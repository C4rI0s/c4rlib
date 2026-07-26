import re
import json
import base64
import random
import string
import time
import datetime


class Discord:
    @staticmethod
    def is_valid_token(token: str) -> bool:
        parts = token.split(".")
        return len(parts) == 3 and all(len(p) > 0 for p in parts)

    @staticmethod
    def decode_token(token: str) -> dict:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid token format")
        user_id_b64 = parts[0]
        padding = 4 - len(user_id_b64) % 4
        if padding != 4: user_id_b64 += "=" * padding
        user_id = base64.b64decode(user_id_b64).decode(errors="replace")
        return {
            "user_id":    user_id,
            "token_part": parts[1],
            "hmac":       parts[2],
        }

    @staticmethod
    def snowflake_to_timestamp(snowflake: int) -> str:
        ts = ((snowflake >> 22) + 1420070400000) / 1000
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def timestamp_to_snowflake(dt: datetime.datetime = None) -> int:
        if dt is None: dt = datetime.datetime.utcnow()
        ts = int(dt.timestamp() * 1000) - 1420070400000
        return ts << 22

    @staticmethod
    def generate_nonce() -> str:
        ts = int(time.time() * 1000) - 1420070400000
        return str((ts << 22) + random.randint(0, 4194303))

    @staticmethod
    def generate_session_id() -> str:
        return "".join(random.choices(string.hexdigits.lower(), k=32))

    @staticmethod
    def generate_device_id() -> str:
        return "".join(random.choices(string.hexdigits.lower(), k=16))

    @staticmethod
    def make_xsuper(client_version: str = "0.0.309", build_number: int = 9999,
                    native_build: int = 50150) -> str:
        payload = {
            "os":                  "Windows",
            "browser":             "Discord Client",
            "release_channel":     "stable",
            "client_version":      client_version,
            "os_version":          "10.0.19045",
            "os_arch":             "x64",
            "app_arch":            "ia32",
            "system_locale":       "en",
            "browser_user_agent":  "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9038 Chrome/120.0.6099.291 Electron/28.2.7 Safari/537.36",
            "browser_version":     "28.2.7",
            "client_build_number": build_number,
            "native_build_number": native_build,
            "client_event_source": None,
            "design_id":           0
        }
        return base64.b64encode(json.dumps(payload, separators=(",",":")).encode()).decode()

    @staticmethod
    def make_headers(token: str = None, xsuper: str = None) -> dict:
        headers = {
            "Content-Type":      "application/json",
            "User-Agent":        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9038 Chrome/120.0.6099.291 Electron/28.2.7 Safari/537.36",
            "Accept":            "*/*",
            "Accept-Language":   "en-US,en;q=0.9",
            "Accept-Encoding":   "gzip, deflate, br",
            "Origin":            "https://discord.com",
            "Referer":           "https://discord.com/channels/@me",
            "Sec-Ch-Ua":         '"Not_A Brand";v="8", "Chromium";v="120"',
            "Sec-Ch-Ua-Mobile":  "?0",
            "Sec-Ch-Ua-Platform":'"Windows"',
            "Sec-Fetch-Dest":    "empty",
            "Sec-Fetch-Mode":    "cors",
            "Sec-Fetch-Site":    "same-origin",
        }
        if token:  headers["Authorization"] = token
        if xsuper: headers["X-Super-Properties"] = xsuper
        return headers

    @staticmethod
    def generate_birthdate(min_year: int = 1970, max_year: int = 2000) -> str:
        year  = random.randint(min_year, max_year)
        month = random.randint(1, 12)
        day   = random.randint(1, 28)
        return f"{year}-{month:02d}-{day:02d}"

    @staticmethod
    def generate_username(length: int = None) -> str:
        adjectives = ["cool","fast","dark","sharp","raw","pure","deep","bold","wild","grim"]
        nouns      = ["wolf","fox","hawk","lion","void","ghost","storm","blade","shade","echo"]
        name       = random.choice(adjectives) + random.choice(nouns)
        if length:
            name = name[:length]
        return name + str(random.randint(100, 9999))

    @staticmethod
    def random_invite_code(length: int = 8) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def parse_invite(url: str) -> str:
        match = re.search(r"discord(?:\.gg|\.com/invite)/([a-zA-Z0-9-]+)", url)
        return match.group(1) if match else url

    @staticmethod
    def message_link(guild_id: int, channel_id: int, message_id: int) -> str:
        return f"https://discord.com/channels/{guild_id}/{channel_id}/{message_id}"

    @staticmethod
    def channel_link(guild_id: int, channel_id: int) -> str:
        return f"https://discord.com/channels/{guild_id}/{channel_id}"

    @staticmethod
    def invite_link(code: str) -> str:
        return f"https://discord.gg/{code}"

    @staticmethod
    def format_mention_user(user_id: int) -> str:
        return f"<@{user_id}>"

    @staticmethod
    def format_mention_role(role_id: int) -> str:
        return f"<@&{role_id}>"

    @staticmethod
    def format_mention_channel(channel_id: int) -> str:
        return f"<#{channel_id}>"

    @staticmethod
    def format_emoji(name: str, emoji_id: int, animated: bool = False) -> str:
        prefix = "a" if animated else ""
        return f"<{prefix}:{name}:{emoji_id}>"

    @staticmethod
    def format_timestamp(dt: datetime.datetime = None, style: str = "f") -> str:
        if dt is None: dt = datetime.datetime.utcnow()
        ts = int(dt.timestamp())
        return f"<t:{ts}:{style}>"

    @staticmethod
    def format_spoiler(text: str) -> str:
        return f"||{text}||"

    @staticmethod
    def format_code(text: str, language: str = "") -> str:
        return f"```{language}\n{text}\n```"

    @staticmethod
    def format_inline_code(text: str) -> str:
        return f"`{text}`"

    @staticmethod
    def format_bold(text: str) -> str:
        return f"**{text}**"

    @staticmethod
    def format_italic(text: str) -> str:
        return f"*{text}*"

    @staticmethod
    def format_underline(text: str) -> str:
        return f"__{text}__"

    @staticmethod
    def format_strikethrough(text: str) -> str:
        return f"~~{text}~~"

    @staticmethod
    def format_quote(text: str) -> str:
        return "\n".join(f"> {line}" for line in text.split("\n"))

    @staticmethod
    def format_embed_color(hex_color: str) -> int:
        return int(hex_color.lstrip("#"), 16)

    @staticmethod
    def make_embed(title: str = None, description: str = None, color: str = "#5865F2",
                   fields: list = None, footer: str = None, thumbnail: str = None,
                   image: str = None, author: str = None, timestamp: bool = False) -> dict:
        embed = {}
        if title:       embed["title"]       = title
        if description: embed["description"] = description
        if color:       embed["color"]       = Discord.format_embed_color(color)
        if footer:      embed["footer"]      = {"text": footer}
        if thumbnail:   embed["thumbnail"]   = {"url": thumbnail}
        if image:       embed["image"]       = {"url": image}
        if author:      embed["author"]      = {"name": author}
        if timestamp:   embed["timestamp"]   = datetime.datetime.utcnow().isoformat()
        if fields:      embed["fields"]      = fields
        return embed

    @staticmethod
    def make_field(name: str, value: str, inline: bool = False) -> dict:
        return {"name": name, "value": value, "inline": inline}

    @staticmethod
    def permissions_to_list(permissions: int) -> list:
        perm_map = {
            0x0000000000000001: "CREATE_INSTANT_INVITE",
            0x0000000000000002: "KICK_MEMBERS",
            0x0000000000000004: "BAN_MEMBERS",
            0x0000000000000008: "ADMINISTRATOR",
            0x0000000000000010: "MANAGE_CHANNELS",
            0x0000000000000020: "MANAGE_GUILD",
            0x0000000000000040: "ADD_REACTIONS",
            0x0000000000000080: "VIEW_AUDIT_LOG",
            0x0000000000000400: "VIEW_CHANNEL",
            0x0000000000000800: "SEND_MESSAGES",
            0x0000000000002000: "MANAGE_MESSAGES",
            0x0000000000004000: "EMBED_LINKS",
            0x0000000000008000: "ATTACH_FILES",
            0x0000000000010000: "READ_MESSAGE_HISTORY",
            0x0000000000020000: "MENTION_EVERYONE",
            0x0000000000100000: "CONNECT",
            0x0000000000200000: "SPEAK",
            0x0000000008000000: "MANAGE_ROLES",
            0x0000000010000000: "MANAGE_WEBHOOKS",
        }
        return [name for bit, name in perm_map.items() if permissions & bit]
