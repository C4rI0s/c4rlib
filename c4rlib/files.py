import os
import json
import shutil
import hashlib
import datetime
import pathlib


class Files:
    @staticmethod
    def read(path: str, encoding: str = "utf-8") -> str:
        with open(path, "r", encoding=encoding) as f:
            return f.read()

    @staticmethod
    def read_lines(path: str, encoding: str = "utf-8") -> list:
        with open(path, "r", encoding=encoding) as f:
            return [line.rstrip("\n") for line in f.readlines()]

    @staticmethod
    def read_bytes(path: str) -> bytes:
        with open(path, "rb") as f:
            return f.read()

    @staticmethod
    def write(path: str, content: str, encoding: str = "utf-8") -> int:
        Files.mkdir(os.path.dirname(path))
        with open(path, "w", encoding=encoding) as f:
            return f.write(content)

    @staticmethod
    def write_bytes(path: str, data: bytes) -> int:
        Files.mkdir(os.path.dirname(path))
        with open(path, "wb") as f:
            return f.write(data)

    @staticmethod
    def append(path: str, content: str, encoding: str = "utf-8") -> None:
        with open(path, "a", encoding=encoding) as f:
            f.write(content)

    @staticmethod
    def append_line(path: str, line: str, encoding: str = "utf-8") -> None:
        Files.append(path, line + "\n", encoding)

    @staticmethod
    def write_json(path: str, data: dict, indent: int = 4) -> None:
        Files.mkdir(os.path.dirname(path))
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)

    @staticmethod
    def read_json(path: str) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def exists(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    def is_file(path: str) -> bool:
        return os.path.isfile(path)

    @staticmethod
    def is_dir(path: str) -> bool:
        return os.path.isdir(path)

    @staticmethod
    def mkdir(path: str) -> None:
        if path and not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    @staticmethod
    def delete(path: str) -> bool:
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            return True
        except Exception:
            return False

    @staticmethod
    def copy(src: str, dst: str) -> str:
        Files.mkdir(os.path.dirname(dst))
        return shutil.copy2(src, dst)

    @staticmethod
    def move(src: str, dst: str) -> str:
        Files.mkdir(os.path.dirname(dst))
        return shutil.move(src, dst)

    @staticmethod
    def rename(path: str, new_name: str) -> str:
        new_path = os.path.join(os.path.dirname(path), new_name)
        os.rename(path, new_path)
        return new_path

    @staticmethod
    def size(path: str) -> int:
        return os.path.getsize(path)

    @staticmethod
    def size_human(path: str) -> str:
        size = Files.size(path)
        for unit in ["B","KB","MB","GB","TB"]:
            if size < 1024: return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

    @staticmethod
    def extension(path: str) -> str:
        return os.path.splitext(path)[1].lstrip(".")

    @staticmethod
    def basename(path: str) -> str:
        return os.path.basename(path)

    @staticmethod
    def dirname(path: str) -> str:
        return os.path.dirname(path)

    @staticmethod
    def stem(path: str) -> str:
        return pathlib.Path(path).stem

    @staticmethod
    def abspath(path: str) -> str:
        return os.path.abspath(path)

    @staticmethod
    def join(*parts) -> str:
        return os.path.join(*parts)

    @staticmethod
    def list_dir(path: str = ".") -> list:
        return os.listdir(path)

    @staticmethod
    def list_files(path: str = ".", pattern: str = "*", recursive: bool = False) -> list:
        p = pathlib.Path(path)
        if recursive:
            return [str(f) for f in p.rglob(pattern) if f.is_file()]
        return [str(f) for f in p.glob(pattern) if f.is_file()]

    @staticmethod
    def list_dirs(path: str = ".") -> list:
        return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    @staticmethod
    def find(path: str, name: str, recursive: bool = True) -> list:
        results = []
        if recursive:
            for root, dirs, files in os.walk(path):
                for f in files:
                    if name.lower() in f.lower():
                        results.append(os.path.join(root, f))
        else:
            for f in os.listdir(path):
                if name.lower() in f.lower():
                    results.append(os.path.join(path, f))
        return results

    @staticmethod
    def find_by_extension(path: str, ext: str, recursive: bool = True) -> list:
        ext = ext.lstrip(".")
        return Files.list_files(path, f"*.{ext}", recursive)

    @staticmethod
    def count_lines(path: str, encoding: str = "utf-8") -> int:
        with open(path, "r", encoding=encoding) as f:
            return sum(1 for _ in f)

    @staticmethod
    def hash(path: str, algorithm: str = "sha256") -> str:
        h = hashlib.new(algorithm)
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    @staticmethod
    def modified_time(path: str) -> str:
        ts = os.path.getmtime(path)
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def created_time(path: str) -> str:
        ts = os.path.getctime(path)
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def tree(path: str = ".", indent: int = 0) -> str:
        result = []
        prefix = "  " * indent
        name   = os.path.basename(path) or path
        result.append(f"{prefix}{'📁 ' if os.path.isdir(path) else '📄 '}{name}")
        if os.path.isdir(path):
            try:
                for item in sorted(os.listdir(path)):
                    full = os.path.join(path, item)
                    result.append(Files.tree(full, indent+1))
            except PermissionError:
                result.append(f"{'  '*(indent+1)}[Permission denied]")
        return "\n".join(result)

    @staticmethod
    def safe_filename(name: str) -> str:
        invalid = r'\/:*?"<>|'
        return "".join(c if c not in invalid else "_" for c in name)

    @staticmethod
    def temp_path(suffix: str = ".tmp") -> str:
        import tempfile
        return tempfile.mktemp(suffix=suffix)

    @staticmethod
    def cwd() -> str:
        return os.getcwd()

    @staticmethod
    def home() -> str:
        return str(pathlib.Path.home())
