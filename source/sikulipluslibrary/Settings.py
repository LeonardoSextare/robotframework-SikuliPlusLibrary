# config.py (Python 3.11+)
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import tomllib  # no 3.10: pip install tomli; import tomli as tomllib

@dataclass(frozen=True)
class Settings:
    similarity: float  = 0.7
    vision_timeout: float = 5.0
    action_speed: float = 0.1
    highlight: bool = True
    highlight_time: float = 2.0
    language: str = "en_US"

    @classmethod
    def load_config(cls, path: str | Path = "auto") -> "Settings":
        if path == "auto":
            file_path = cls.find_config_file()
            if file_path is None:
                return cls()
        else:
            file_path = Path(path).resolve()
            if not file_path.is_file():
                raise FileNotFoundError("Config file path not found!")

        with file_path.open("rb") as f:
            data = tomllib.load(f) or {}

        allowed = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**allowed)

    @classmethod
    def find_config_file(cls, filename: str = "Sikuli.toml") -> Path | None:
        root = Path.cwd().resolve()
        for p in (root, *root.parents):
            cand = p / filename
            if cand.is_file():
                return cand.resolve()
        return None

@lru_cache
def get_settings(path: str = "auto") -> Settings:
    return Settings.load_config(path)
