"""Deterministic helpers across TextStyle, Utils and Files."""
import hashlib

import pytest

from c4rlib import Files, TextStyle, Utils


# ── TextStyle ─────────────────────────────────────────────────────────────────

def test_unicode_maps_preserve_length_and_change_letters():
    for fn in (TextStyle.fancy, TextStyle.double_struck, TextStyle.cursive,
               TextStyle.fraktur, TextStyle.bold_serif, TextStyle.sans_bold,
               TextStyle.monospace, TextStyle.bubble, TextStyle.small_caps):
        out = fn("abc")
        assert len(out) == 3, fn.__name__
        assert out != "abc", fn.__name__


def test_maps_leave_non_letters_untouched():
    assert TextStyle.bubble("a-1")[1:] == "-1"


def test_rot13_and_caesar_are_reversible():
    assert TextStyle.rot13(TextStyle.rot13("Hello, World!")) == "Hello, World!"
    assert TextStyle.caesar(TextStyle.caesar("Hello", 7), -7) == "Hello"


def test_morse_known_value():
    assert TextStyle.morse("sos") == "... --- ..."
    assert TextStyle.morse("a b") == ".- / -..."   # spaces become '/'


def test_nato_known_value():
    assert TextStyle.nato("abc") == "Alpha Bravo Charlie"


def test_binary_and_hex_known_values():
    assert TextStyle.binary("A") == "01000001"
    assert TextStyle.binary("AB") == "01000001 01000010"
    assert TextStyle.hex_encode("AB") == "41 42"


def test_reverse_and_alternate_case():
    assert TextStyle.reverse("abc") == "cba"
    assert TextStyle.alternate_case("abcd") == "AbCd"


def test_counting_helpers():
    assert TextStyle.word_count("one two  three") == 3
    assert TextStyle.word_count("") == 0
    assert TextStyle.char_count("a b") == 3
    assert TextStyle.char_count("a b", include_spaces=False) == 2


def test_truncate_respects_max_length():
    assert TextStyle.truncate("hello", max_len=10) == "hello"
    out = TextStyle.truncate("a" * 100, max_len=20)
    assert len(out) == 20 and out.endswith("...")


def test_padding_helpers():
    assert TextStyle.pad_left("x", 5) == "    x"
    assert TextStyle.pad_right("x", 5) == "x    "
    assert TextStyle.pad_center("x", 5, "-") == "--x--"
    assert TextStyle.pad_left("toolong", 3) == "toolong"


def test_wrap_never_exceeds_width_for_ordinary_words():
    text = "the quick brown fox jumps over the lazy dog " * 4
    for line in TextStyle.wrap(text, width=20).splitlines():
        assert len(line) <= 20


def test_space_out_and_repeat_chars():
    assert TextStyle.space_out("abc") == "a b c"
    assert TextStyle.space_out("abc", 2) == "a  b  c"
    assert TextStyle.repeat_chars("ab", 3) == "aaabbb"


def test_zalgo_adds_combining_marks_without_losing_base_chars():
    out = TextStyle.zalgo("abc", intensity=2)
    assert len(out) > 3
    assert all(ch in out for ch in "abc")


# ── Utils ─────────────────────────────────────────────────────────────────────

def test_uuid_shape_and_uniqueness():
    a, b = Utils.generate_uuid(), Utils.generate_uuid()
    assert a != b
    assert len(a) == 36 and a.count("-") == 4
    assert len(Utils.generate_uuid_hex()) == 32


def test_token_lengths():
    # `length` counts characters here, not bytes.
    assert len(Utils.generate_hex_token(16)) == 16
    assert set(Utils.generate_hex_token(64)) <= set("abcdef0123456789")
    assert len(Utils.generate_token(20)) == 20
    assert len(Utils.generate_pin(8)) == 8
    assert Utils.generate_pin(4).isdigit()
    assert len(Utils.generate_password(24)) == 24
    assert len(Utils.random_string(12)) == 12
    assert len(Utils.random_hex(10)) == 10


def test_random_string_respects_charset():
    assert set(Utils.random_string(50, charset="ab")) <= {"a", "b"}


def test_hash_helpers_match_stdlib():
    assert Utils.hash_md5("x") == hashlib.md5(b"x").hexdigest()
    assert Utils.hash_sha256("x") == hashlib.sha256(b"x").hexdigest()
    assert Utils.hash_sha512("x") == hashlib.sha512(b"x").hexdigest()


def test_exactly_one_platform_predicate_is_true():
    assert sum([Utils.is_windows(), Utils.is_linux(), Utils.is_mac()]) == 1


def test_generated_network_identifiers_are_wellformed():
    mac = Utils.generate_mac()
    assert len(mac.split(":")) == 6
    assert all(len(part) == 2 for part in mac.split(":"))
    octets = Utils.generate_ipv4().split(".")
    assert len(octets) == 4
    assert all(0 <= int(o) <= 255 for o in octets)
    assert len(Utils.generate_ipv6().split(":")) == 8
    assert 1 <= Utils.generate_port() <= 65535


def test_list_helpers():
    assert Utils.chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
    assert Utils.chunk([], 3) == []
    assert Utils.flatten([1, [2, [3, [4]]], 5]) == [1, 2, 3, 4, 5]
    assert Utils.unique([3, 1, 3, 2, 1]) == [3, 1, 2]


def test_math_helpers():
    assert Utils.clamp(15, 0, 10) == 10
    assert Utils.clamp(-5, 0, 10) == 0
    assert Utils.clamp(5, 0, 10) == 5
    assert Utils.lerp(0, 100, 0.25) == 25
    assert Utils.lerp(0, 100, 0) == 0
    assert Utils.lerp(0, 100, 1) == 100


def test_percentage_handles_zero_total():
    assert Utils.percentage(25, 200) == 12.5
    assert Utils.percentage(1, 0) == 0.0


def test_format_helpers():
    assert Utils.format_bytes(512) == "512.00 B"
    assert Utils.format_bytes(1024) == "1.00 KB"
    assert Utils.format_bytes(1024 ** 3) == "1.00 GB"
    assert Utils.format_number(1234567) == "1,234,567"


def test_random_email_and_credit_card_shape():
    assert "@" in Utils.random_email()
    assert Utils.random_email(domain="example.com").endswith("@example.com")
    card = Utils.random_credit_card("visa")
    assert card["number"].startswith("4") and len(card["number"]) == 16
    assert card["number"].isdigit() and len(card["cvv"]) == 3


def test_retry_returns_value_and_stops_early():
    calls = []

    def flaky():
        calls.append(1)
        if len(calls) < 2:
            raise RuntimeError("not yet")
        return "ok"

    assert Utils.retry(flaky, times=3, delay=0) == "ok"
    assert len(calls) == 2


# ── Files ─────────────────────────────────────────────────────────────────────

def test_write_read_roundtrip(tmp_path):
    target = tmp_path / "note.txt"
    Files.write(str(target), "hello")
    assert Files.read(str(target)) == "hello"
    assert Files.exists(str(target)) and Files.is_file(str(target))


def test_append_and_line_counting(tmp_path):
    target = str(tmp_path / "log.txt")
    Files.write(target, "")
    for i in range(3):
        Files.append_line(target, f"line {i}")
    assert Files.count_lines(target) == 3
    assert Files.read_lines(target)[0].rstrip("\n") == "line 0"


def test_json_roundtrip_creates_parent_directories(tmp_path):
    target = str(tmp_path / "nested" / "deep" / "data.json")
    payload = {"name": "c4r", "tags": ["cli", "fx"], "unicode": "ünï"}
    Files.write_json(target, payload)
    assert Files.read_json(target) == payload


def test_bytes_roundtrip_and_hash(tmp_path):
    target = str(tmp_path / "blob.bin")
    Files.write_bytes(target, b"\x00\x01\x02payload")
    assert Files.read_bytes(target) == b"\x00\x01\x02payload"
    assert Files.hash(target) == hashlib.sha256(b"\x00\x01\x02payload").hexdigest()


def test_path_helpers():
    assert Files.extension("dir/archive.tar.gz") == "gz"
    assert Files.extension("noext") == ""
    assert Files.basename("dir/file.txt") == "file.txt"
    assert Files.stem("dir/file.txt") == "file"


def test_size_and_human_size(tmp_path):
    target = str(tmp_path / "sized.bin")
    Files.write_bytes(target, b"x" * 2048)
    assert Files.size(target) == 2048
    assert Files.size_human(target) == "2.00 KB"


def test_copy_move_rename_and_delete(tmp_path):
    src = str(tmp_path / "a.txt")
    Files.write(src, "data")

    copied = Files.copy(src, str(tmp_path / "sub" / "b.txt"))
    assert Files.read(copied) == "data"

    renamed = Files.rename(copied, "c.txt")
    assert Files.basename(renamed) == "c.txt" and Files.exists(renamed)

    moved = Files.move(renamed, str(tmp_path / "moved" / "d.txt"))
    assert Files.exists(moved) and not Files.exists(renamed)

    assert Files.delete(moved) is True
    assert not Files.exists(moved)


def test_delete_is_idempotent_for_missing_paths(tmp_path):
    """Documents current behaviour: deleting a non-existent path reports True.

    `delete` answers "is this path gone", not "did I remove something". If that
    ever changes to a False/raise, this test should change with it deliberately.
    """
    assert Files.delete(str(tmp_path / "nope.txt")) is True


def test_listing_and_finding(tmp_path):
    Files.write(str(tmp_path / "one.py"), "")
    Files.write(str(tmp_path / "two.txt"), "")
    Files.mkdir(str(tmp_path / "pkg"))
    Files.write(str(tmp_path / "pkg" / "three.py"), "")

    assert sorted(Files.list_dirs(str(tmp_path))) == ["pkg"]
    assert len(Files.list_files(str(tmp_path))) == 2
    assert len(Files.find_by_extension(str(tmp_path), "py", recursive=True)) == 2
    assert len(Files.find_by_extension(str(tmp_path), ".py", recursive=False)) == 1
    assert len(Files.find(str(tmp_path), "THREE")) == 1        # case-insensitive
