import os
import sys
import time
import uuid
import random
import secrets
import string
import hashlib
import datetime
import platform
import subprocess


class Utils:
    """General-purpose helpers.

    Anything that produces a credential — tokens, PINs, passwords — draws from
    `secrets`, not `random`. `random` is a Mersenne Twister: observe enough of
    its output and the internal state, and therefore every future value, can be
    reconstructed. The fake-data generators below (`random_name`, `random_ipv4`,
    `random_credit_card`…) deliberately keep using `random` — they are for
    fixtures and seeding, and must never be used as credentials or as anything
    a security decision depends on.
    """

    @staticmethod
    def generate_uuid(version: int = 4) -> str:
        return str(uuid.uuid1() if version == 1 else uuid.uuid4())

    @staticmethod
    def generate_uuid_hex() -> str:
        return uuid.uuid4().hex

    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Cryptographically secure alphanumeric token of `length` characters."""
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))

    @staticmethod
    def generate_hex_token(length: int = 32) -> str:
        """Secure hex token of `length` characters (not bytes)."""
        return "".join(secrets.choice("abcdef0123456789") for _ in range(length))

    @staticmethod
    def generate_pin(digits: int = 6) -> str:
        return "".join(secrets.choice(string.digits) for _ in range(digits))

    @staticmethod
    def generate_password(length: int = 16, symbols: bool = True) -> str:
        chars = string.ascii_letters + string.digits
        if symbols: chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"
        return "".join(secrets.choice(chars) for _ in range(length))

    @staticmethod
    def timestamp() -> int:
        return int(time.time() * 1000)

    @staticmethod
    def timestamp_seconds() -> int:
        return int(time.time())

    @staticmethod
    def log_time() -> str:
        return "{:%H:%M:%S}".format(datetime.datetime.now())

    @staticmethod
    def log_date() -> str:
        return "{:%Y-%m-%d}".format(datetime.datetime.now())

    @staticmethod
    def log_datetime() -> str:
        return "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())

    @staticmethod
    def elapsed(start: float) -> str:
        e = time.time() - start
        if e < 60:   return f"{e:.2f}s"
        elif e < 3600: return f"{e/60:.1f}m"
        else:          return f"{e/3600:.1f}h"

    @staticmethod
    def random_string(length: int = 8, charset: str = None) -> str:
        chars = charset or (string.ascii_letters + string.digits)
        return "".join(random.choices(chars, k=length))

    @staticmethod
    def random_hex(length: int = 8) -> str:
        return "".join(random.choices("abcdef0123456789", k=length))

    @staticmethod
    def hash_md5(text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()

    @staticmethod
    def hash_sha1(text: str) -> str:
        return hashlib.sha1(text.encode()).hexdigest()

    @staticmethod
    def hash_sha256(text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()

    @staticmethod
    def hash_sha512(text: str) -> str:
        return hashlib.sha512(text.encode()).hexdigest()

    @staticmethod
    def hash_sha3_256(text: str) -> str:
        return hashlib.sha3_256(text.encode()).hexdigest()

    @staticmethod
    def generate_mac() -> str:
        return ":".join("{:02x}".format(random.randint(0,255)) for _ in range(6))

    @staticmethod
    def generate_ipv4() -> str:
        return ".".join(str(random.randint(1,254)) for _ in range(4))

    @staticmethod
    def generate_ipv6() -> str:
        return ":".join("{:04x}".format(random.randint(0,65535)) for _ in range(8))

    @staticmethod
    def generate_port() -> int:
        return random.randint(1024, 65535)

    @staticmethod
    def is_windows() -> bool:
        return os.name == "nt"

    @staticmethod
    def is_linux() -> bool:
        return sys.platform.startswith("linux")

    @staticmethod
    def is_mac() -> bool:
        return sys.platform == "darwin"

    @staticmethod
    def os_info() -> dict:
        return {
            "os":      platform.system(),
            "release": platform.release(),
            "arch":    platform.machine(),
            "python":  platform.python_version(),
            "node":    platform.node(),
        }

    @staticmethod
    def run(command: str) -> str:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()

    _FIRST = [
        "James","Mary","John","Patricia","Robert","Jennifer","Michael","Linda",
        "William","Barbara","David","Elizabeth","Richard","Susan","Joseph","Jessica",
        "Thomas","Sarah","Charles","Karen","Daniel","Lisa","Matthew","Nancy",
        "Anthony","Betty","Mark","Margaret","Donald","Sandra","Steven","Ashley",
        "Paul","Emily","Andrew","Kimberly","Kenneth","Donna","George","Carol",
        "Joshua","Michelle","Kevin","Amanda","Brian","Melissa","Edward","Deborah",
        "Ronald","Stephanie","Timothy","Rebecca","Jason","Sharon","Jeffrey","Laura",
        "Ryan","Cynthia","Jacob","Kathleen","Gary","Amy","Nicholas","Angela",
        "Eric","Shirley","Jonathan","Anna","Stephen","Brenda","Larry","Pamela",
        "Justin","Emma","Scott","Nicole","Brandon","Helen","Frank","Samantha",
        "Benjamin","Katherine","Gregory","Christine","Samuel","Debra","Raymond","Rachel"
    ]

    _LAST = [
        "Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis",
        "Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson",
        "Thomas","Taylor","Moore","Jackson","Martin","Lee","Perez","Thompson",
        "White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson","Walker",
        "Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores",
        "Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell",
        "Carter","Roberts","Phillips","Evans","Turner","Torres","Parker","Collins",
        "Edwards","Stewart","Flores","Morris","Nguyen","Murphy","Rivera","Cook",
        "Rogers","Morgan","Peterson","Cooper","Reed","Bailey","Bell","Gomez",
        "Kelly","Howard","Ward","Cox","Diaz","Richardson","Wood","Watson","Brooks"
    ]

    _DOMAINS = ["gmail.com","yahoo.com","hotmail.com","outlook.com","proton.me","icloud.com","mail.com"]

    @staticmethod
    def random_name() -> str:
        return f"{random.choice(Utils._FIRST)} {random.choice(Utils._LAST)}"

    @staticmethod
    def random_first_name() -> str:
        return random.choice(Utils._FIRST)

    @staticmethod
    def random_last_name() -> str:
        return random.choice(Utils._LAST)

    @staticmethod
    def random_email(domain: str = None) -> str:
        first = random.choice(Utils._FIRST).lower()
        last  = random.choice(Utils._LAST).lower()
        num   = random.randint(1, 999)
        dom   = domain or random.choice(Utils._DOMAINS)
        return f"{first}.{last}{num}@{dom}"

    @staticmethod
    def random_username(length: int = 10) -> str:
        return random.choice(Utils._FIRST).lower() + Utils.random_hex(length-4)

    @staticmethod
    def random_birthdate(min_year: int = 1970, max_year: int = 2003) -> str:
        return f"{random.randint(min_year,max_year)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"

    @staticmethod
    def random_phone(country_code: str = "+1") -> str:
        return f"{country_code} ({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}"

    @staticmethod
    def random_address() -> str:
        streets = ["Main St","Oak Ave","Maple Dr","Cedar Ln","Park Blvd","Lake Rd","Hill Ct","River Way","Forest Path","Sunset Blvd"]
        cities  = ["New York","Los Angeles","Chicago","Houston","Phoenix","Philadelphia","San Antonio","San Diego","Dallas","San Jose"]
        states  = ["CA","TX","FL","NY","PA","IL","OH","GA","NC","MI"]
        return f"{random.randint(100,9999)} {random.choice(streets)}, {random.choice(cities)}, {random.choice(states)} {random.randint(10000,99999)}"

    @staticmethod
    def random_zip(country: str = "US") -> str:
        if country == "US":  return f"{random.randint(10000,99999)}"
        if country == "UK":  return f"{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}{random.randint(1,9)} {random.randint(1,9)}{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}"
        if country == "CA":  return f"{random.choice('ABCEGHJKLMNPRSTVXY')}{random.randint(0,9)}{random.choice(string.ascii_uppercase)} {random.randint(0,9)}{random.choice(string.ascii_uppercase)}{random.randint(0,9)}"
        return str(random.randint(10000,99999))

    @staticmethod
    def random_credit_card(brand: str = "visa") -> dict:
        prefixes = {"visa": "4", "mastercard": "5", "amex": "3", "discover": "6"}
        prefix   = prefixes.get(brand.lower(), "4")
        number   = prefix + "".join(random.choices(string.digits, k=15))
        return {
            "number": number,
            "expiry": f"{random.randint(1,12):02d}/{random.randint(25,30)}",
            "cvv":    "".join(random.choices(string.digits, k=3)),
            "brand":  brand.capitalize()
        }

    @staticmethod
    def random_user_agent() -> str:
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Android 14; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0",
        ]
        return random.choice(agents)

    @staticmethod
    def random_color_hex() -> str:
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    @staticmethod
    def chunk(lst: list, size: int) -> list:
        return [lst[i:i+size] for i in range(0, len(lst), size)]

    @staticmethod
    def flatten(lst: list) -> list:
        result = []
        for item in lst:
            if isinstance(item, list):
                result.extend(Utils.flatten(item))
            else:
                result.append(item)
        return result

    @staticmethod
    def unique(lst: list) -> list:
        seen = set()
        return [x for x in lst if not (x in seen or seen.add(x))]

    @staticmethod
    def clamp(value: float, min_val: float, max_val: float) -> float:
        return max(min_val, min(max_val, value))

    @staticmethod
    def lerp(a: float, b: float, t: float) -> float:
        return a + (b-a)*t

    @staticmethod
    def percentage(value: float, total: float, decimals: int = 2) -> float:
        return round((value/total)*100, decimals) if total else 0.0

    @staticmethod
    def format_bytes(size: int) -> str:
        for unit in ["B","KB","MB","GB","TB"]:
            if size < 1024: return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

    @staticmethod
    def format_number(n: int) -> str:
        return "{:,}".format(n)

    @staticmethod
    def retry(func, times: int = 3, delay: float = 1.0):
        import time
        for attempt in range(times):
            try:
                return func()
            except Exception as e:
                if attempt == times-1: raise e
                time.sleep(delay)
