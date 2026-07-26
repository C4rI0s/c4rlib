"""Crypto helpers — checked against known vectors, not against themselves."""
import base64
import hashlib

import pytest

from c4rlib import Crypto

# Digests of the empty string: canonical, unambiguous vectors.
EMPTY_DIGESTS = {
    "md5":      "d41d8cd98f00b204e9800998ecf8427e",
    "sha1":     "da39a3ee5e6b4b0d3255bfef95601890afd80709",
    "sha256":   "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "sha3_256": "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a",
}


@pytest.mark.parametrize("algo,expected", EMPTY_DIGESTS.items())
def test_hash_vectors_empty_string(algo, expected):
    assert getattr(Crypto, algo)("") == expected


def test_sha256_abc_vector():
    assert Crypto.sha256("abc") == (
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    )


def test_sha512_and_blake_lengths():
    assert len(Crypto.sha512("x")) == 128
    assert len(Crypto.sha3_512("x")) == 128
    assert len(Crypto.blake2b("x")) == 128
    assert len(Crypto.blake2s("x")) == 64


def test_hmac_matches_stdlib():
    import hmac

    expected = hmac.new(b"key", b"message", hashlib.sha256).hexdigest()
    assert Crypto.hmac_sha256("key", "message") == expected


def test_base64_roundtrip():
    for text in ["", "hello", "ünïcødé ✨", "a" * 500]:
        assert Crypto.b64_decode(Crypto.b64_encode(text)) == text
        assert Crypto.b64_urlsafe_decode(Crypto.b64_urlsafe_encode(text)) == text


def test_base64_urlsafe_avoids_url_hostile_chars():
    encoded = Crypto.b64_urlsafe_encode("\xfb\xff\xfe" * 10)
    assert "+" not in encoded and "/" not in encoded


def test_hex_roundtrip():
    assert Crypto.hex_decode(Crypto.hex_encode("hello ünï")) == "hello ünï"


@pytest.mark.parametrize("text", ["hello", "ünïcødé", "a" * 200, "!@#$%^&*()"])
def test_xor_is_its_own_inverse(text):
    assert Crypto.xor_decrypt(Crypto.xor_encrypt(text, "s3cret"), "s3cret") == text


def test_rot13_is_involutive():
    assert Crypto.rot13(Crypto.rot13("Hello, World!")) == "Hello, World!"


def test_rot13_known_value():
    assert Crypto.rot13("abc") == "nop"


def test_caesar_roundtrip_and_punctuation_preserved():
    assert Crypto.caesar(Crypto.caesar("Attack at dawn!", 5), -5) == "Attack at dawn!"
    assert Crypto.caesar("a-b", 1) == "b-c"


def test_vigenere_roundtrip():
    assert Crypto.vigenere_decrypt(Crypto.vigenere_encrypt("attackatdawn", "lemon"), "lemon") == (
        "attackatdawn"
    )


def test_vigenere_known_vector():
    assert Crypto.vigenere_encrypt("attackatdawn", "lemon").lower() == "lxfopvefrnhr"


def test_jwt_make_decode_verify():
    payload = {"sub": "1234", "name": "c4r", "admin": True}
    token = Crypto.make_jwt(payload, "secret")
    assert token.count(".") == 2
    assert Crypto.decode_jwt(token) == payload
    assert Crypto.verify_jwt(token, "secret") is True


def test_jwt_rejects_wrong_secret_and_tampering():
    token = Crypto.make_jwt({"sub": "1"}, "secret")
    assert Crypto.verify_jwt(token, "wrong") is False
    header, body, sig = token.split(".")
    forged = Crypto.b64_urlsafe_encode('{"sub":"admin"}')
    assert Crypto.verify_jwt(f"{header}.{forged}.{sig}", "secret") is False


def test_decode_jwt_rejects_malformed():
    with pytest.raises(ValueError):
        Crypto.decode_jwt("not.a.jwt.token")


def test_pbkdf2_is_deterministic_for_a_given_salt():
    a = Crypto.pbkdf2("password", salt="fixedsalt", iterations=1000)
    b = Crypto.pbkdf2("password", salt="fixedsalt", iterations=1000)
    assert a == b
    assert a["salt"] == "fixedsalt" and a["iterations"] == 1000
    assert Crypto.pbkdf2("other", salt="fixedsalt", iterations=1000)["hash"] != a["hash"]


def test_pbkdf2_generates_a_salt_when_omitted():
    a = Crypto.pbkdf2("password", iterations=1000)
    b = Crypto.pbkdf2("password", iterations=1000)
    assert a["salt"] != b["salt"]


def test_totp_rfc6238_vector(monkeypatch):
    """RFC 6238 test vector: ASCII secret '12345678901234567890' at T=59."""
    secret_b32 = base64.b32encode(b"12345678901234567890").decode()
    monkeypatch.setattr("c4rlib.crypto.time.time", lambda: 59)
    assert Crypto.totp(secret_b32, interval=30, digits=8) == "94287082"
    assert Crypto.totp(secret_b32, interval=30, digits=6) == "287082"


def test_totp_is_stable_inside_a_window(monkeypatch):
    secret_b32 = base64.b32encode(b"12345678901234567890").decode()
    monkeypatch.setattr("c4rlib.crypto.time.time", lambda: 30)
    first = Crypto.totp(secret_b32)
    monkeypatch.setattr("c4rlib.crypto.time.time", lambda: 59)
    assert Crypto.totp(secret_b32) == first
    monkeypatch.setattr("c4rlib.crypto.time.time", lambda: 60)
    assert Crypto.totp(secret_b32) != first


def test_random_helpers_lengths_and_uniqueness():
    assert len(Crypto.random_bytes(16)) == 16
    assert len(Crypto.random_hex(16)) == 32          # token_hex → 2 chars per byte
    assert Crypto.random_hex(16) != Crypto.random_hex(16)
    assert Crypto.random_urlsafe(16) != Crypto.random_urlsafe(16)


def test_hash_file_and_compare(tmp_path):
    target = tmp_path / "payload.bin"
    target.write_bytes(b"c4rlib")
    expected = hashlib.sha256(b"c4rlib").hexdigest()
    assert Crypto.hash_file(str(target)) == expected
    assert Crypto.compare_hash("c4rlib", expected) is True
    assert Crypto.compare_hash("c4rlib", expected.replace("a", "b", 1)) is False


def test_url_and_html_encoding_roundtrip():
    assert Crypto.url_decode(Crypto.url_encode("a b&c=d/e")) == "a b&c=d/e"
    assert Crypto.html_decode(Crypto.html_encode("<script>&\"'")) == "<script>&\"'"
