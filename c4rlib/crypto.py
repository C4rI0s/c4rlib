import os
import base64
import hashlib
import hmac
import json
import secrets
import struct
import time


class Crypto:
    @staticmethod
    def b64_encode(data: str) -> str:
        if isinstance(data, str): data = data.encode()
        return base64.b64encode(data).decode()

    @staticmethod
    def b64_decode(data: str) -> str:
        return base64.b64decode(data).decode()

    @staticmethod
    def b64_encode_bytes(data: bytes) -> bytes:
        return base64.b64encode(data)

    @staticmethod
    def b64_decode_bytes(data: str) -> bytes:
        return base64.b64decode(data)

    @staticmethod
    def b64_urlsafe_encode(data: str) -> str:
        if isinstance(data, str): data = data.encode()
        return base64.urlsafe_b64encode(data).decode().rstrip("=")

    @staticmethod
    def b64_urlsafe_decode(data: str) -> str:
        padding = 4 - len(data) % 4
        if padding != 4: data += "=" * padding
        return base64.urlsafe_b64decode(data).decode()

    @staticmethod
    def md5(text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()

    @staticmethod
    def sha1(text: str) -> str:
        return hashlib.sha1(text.encode()).hexdigest()

    @staticmethod
    def sha256(text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()

    @staticmethod
    def sha512(text: str) -> str:
        return hashlib.sha512(text.encode()).hexdigest()

    @staticmethod
    def sha3_256(text: str) -> str:
        return hashlib.sha3_256(text.encode()).hexdigest()

    @staticmethod
    def sha3_512(text: str) -> str:
        return hashlib.sha3_512(text.encode()).hexdigest()

    @staticmethod
    def blake2b(text: str) -> str:
        return hashlib.blake2b(text.encode()).hexdigest()

    @staticmethod
    def blake2s(text: str) -> str:
        return hashlib.blake2s(text.encode()).hexdigest()

    @staticmethod
    def hmac_sha256(key: str, message: str) -> str:
        return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()

    @staticmethod
    def hmac_sha512(key: str, message: str) -> str:
        return hmac.new(key.encode(), message.encode(), hashlib.sha512).hexdigest()

    @staticmethod
    def hash_file(path: str, algorithm: str = "sha256") -> str:
        h = hashlib.new(algorithm)
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    @staticmethod
    def compare_hash(text: str, hash_value: str, algorithm: str = "sha256") -> bool:
        h = hashlib.new(algorithm, text.encode()).hexdigest()
        return hmac.compare_digest(h, hash_value)

    @staticmethod
    def random_bytes(length: int = 32) -> bytes:
        return secrets.token_bytes(length)

    @staticmethod
    def random_hex(length: int = 32) -> str:
        return secrets.token_hex(length)

    @staticmethod
    def random_urlsafe(length: int = 32) -> str:
        return secrets.token_urlsafe(length)

    @staticmethod
    def xor_encrypt(text: str, key: str) -> str:
        key_bytes = key.encode()
        result    = bytes(ord(c) ^ key_bytes[i % len(key_bytes)] for i, c in enumerate(text))
        return base64.b64encode(result).decode()

    @staticmethod
    def xor_decrypt(encrypted: str, key: str) -> str:
        data      = base64.b64decode(encrypted)
        key_bytes = key.encode()
        return "".join(chr(b ^ key_bytes[i % len(key_bytes)]) for i, b in enumerate(data))

    @staticmethod
    def vigenere_encrypt(text: str, key: str) -> str:
        result  = []
        key     = key.lower()
        key_idx = 0
        for ch in text:
            if ch.isalpha():
                shift = ord(key[key_idx % len(key)]) - ord("a")
                base  = ord("a") if ch.islower() else ord("A")
                result.append(chr((ord(ch) - base + shift) % 26 + base))
                key_idx += 1
            else:
                result.append(ch)
        return "".join(result)

    @staticmethod
    def vigenere_decrypt(text: str, key: str) -> str:
        result  = []
        key     = key.lower()
        key_idx = 0
        for ch in text:
            if ch.isalpha():
                shift = ord(key[key_idx % len(key)]) - ord("a")
                base  = ord("a") if ch.islower() else ord("A")
                result.append(chr((ord(ch) - base - shift) % 26 + base))
                key_idx += 1
            else:
                result.append(ch)
        return "".join(result)

    @staticmethod
    def make_jwt(payload: dict, secret: str, algorithm: str = "HS256") -> str:
        header  = {"alg": algorithm, "typ": "JWT"}
        h_enc   = Crypto.b64_urlsafe_encode(json.dumps(header, separators=(",",":")))
        p_enc   = Crypto.b64_urlsafe_encode(json.dumps(payload, separators=(",",":")))
        signing = f"{h_enc}.{p_enc}"
        sig     = hmac.new(secret.encode(), signing.encode(), hashlib.sha256).digest()
        sig_enc = Crypto.b64_urlsafe_encode(sig)
        return f"{signing}.{sig_enc}"

    @staticmethod
    def decode_jwt(token: str) -> dict:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid JWT format")
        payload = parts[1]
        padding = 4 - len(payload) % 4
        if padding != 4: payload += "=" * padding
        return json.loads(base64.urlsafe_b64decode(payload).decode())

    @staticmethod
    def verify_jwt(token: str, secret: str) -> bool:
        try:
            parts   = token.split(".")
            signing = f"{parts[0]}.{parts[1]}"
            sig     = hmac.new(secret.encode(), signing.encode(), hashlib.sha256).digest()
            expected = Crypto.b64_urlsafe_encode(sig)
            return hmac.compare_digest(parts[2], expected)
        except Exception:
            return False

    @staticmethod
    def pbkdf2(password: str, salt: str = None, iterations: int = 100000) -> dict:
        if salt is None: salt = secrets.token_hex(16)
        key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), iterations)
        return {"hash": key.hex(), "salt": salt, "iterations": iterations}

    @staticmethod
    def totp(secret: str, interval: int = 30, digits: int = 6) -> str:
        key      = base64.b32decode(secret.upper().replace(" ",""))
        counter  = int(time.time()) // interval
        msg      = struct.pack(">Q", counter)
        h        = hmac.new(key, msg, hashlib.sha1).digest()
        offset   = h[-1] & 0x0F
        code     = struct.unpack(">I", h[offset:offset+4])[0] & 0x7FFFFFFF
        return str(code % (10**digits)).zfill(digits)

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
    def hex_encode(text: str) -> str:
        return text.encode().hex()

    @staticmethod
    def hex_decode(hex_text: str) -> str:
        return bytes.fromhex(hex_text).decode()

    @staticmethod
    def url_encode(text: str) -> str:
        import urllib.parse
        return urllib.parse.quote(text)

    @staticmethod
    def url_decode(text: str) -> str:
        import urllib.parse
        return urllib.parse.unquote(text)

    @staticmethod
    def html_encode(text: str) -> str:
        return (text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                    .replace('"',"&quot;").replace("'","&#x27;"))

    @staticmethod
    def html_decode(text: str) -> str:
        return (text.replace("&amp;","&").replace("&lt;","<").replace("&gt;",">")
                    .replace("&quot;",'"').replace("&#x27;","'"))
