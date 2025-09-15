from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional
import os
import tomllib


class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class Config:
    """Configuration dataclass for SikuliPlusLibrary with immutable default values."""
    similarity: float = 0.7
    timeout: float = 1.0
    action_speed: float = 0.1
    highlight: bool = True
    highlight_time: float = 2.0
    language: str = "pt_BR"


def _read_toml_file(path: str) -> Dict[str, Any]:
    try:
        with open(path, "rb") as f:
            return tomllib.load(f) or {}
    except FileNotFoundError:
        return {}
    except Exception as e:
        raise ConfigError(f"Error reading '{path}': {e}") from e


def _extract_pyproject_section(pyproject: Dict[str, Any], section: str = "tool.sikuliplus") -> Dict[str, Any]:
    parts = section.split(".")
    current: Any = pyproject
    for part in parts:
        if not isinstance(current, dict):
            return {}
        current = current.get(part, {})
    return current.copy() if isinstance(current, dict) else {}


def _coerce_types(raw: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for raw_key, raw_value in raw.items():
        key_name = raw_key.lower()
        match key_name:
            case "similarity":
                out["similarity"] = float(raw_value)
            case "timeout" | "vision_timeout":
                out["timeout"] = float(raw_value)
            case "action_speed":
                out["action_speed"] = float(raw_value)
            case "highlight":
                if isinstance(raw_value, bool):
                    out["highlight"] = raw_value
                elif isinstance(raw_value, str):
                    lowered = raw_value.lower()
                    if lowered == "true":
                        out["highlight"] = True
                    elif lowered == "false":
                        out["highlight"] = False
                    else:
                        raise ConfigError("'highlight' must be 'true' or 'false' when provided as a string")
                else:
                    raise ConfigError("'highlight' must be a boolean (true/false)")
            case "highlight_time" | "highlighttime":
                out["highlight_time"] = float(raw_value)
            case "language":
                out["language"] = str(raw_value)
            case _:
                out[key_name] = raw_value
    return out


def _read_env(prefix: str = "SIKULIPLUS_") -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for env_name, env_value in os.environ.items():
        if not env_name.startswith(prefix):
            continue
        key = env_name[len(prefix) :].lower()
        key = key.replace("-", "_")
        out[key] = env_value
    return _coerce_types(out)


def _find_config_file(provided: Optional[str] = None) -> Optional[str]:
    if provided:
        return provided
    cwd = os.getcwd()
    # walk the directory tree from cwd, top-down, returning the first match
    target_names = {"sikuli.toml", "config.sikuli"}
    for dirpath, dirnames, filenames in os.walk(cwd):
        for filename in filenames:
            if filename in target_names:
                return os.path.join(dirpath, filename)
    return None


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple dictionaries with later ones taking precedence."""
    result: Dict[str, Any] = {}
    for source_dict in dicts:
        if not source_dict:
            continue
        result.update(source_dict)
    return result


def load_config(
    config_path: Optional[str] = None,
    pyproject_path: str = "pyproject.toml",
    env_prefix: str = "SIKULIPLUS_",
) -> Config:
    """Load configuration with precedence:
    defaults <- pyproject.toml (tool.sikuliplus) <- config file (sikuli.toml|config.sikuli) <- env vars
    """
    defaults = Config().__dict__

    # pyproject.toml section
    pyproject_raw = _read_toml_file(pyproject_path)
    pyproject_cfg = _extract_pyproject_section(pyproject_raw, "tool.sikuliplus")
    pyproject_cfg = _coerce_types(pyproject_cfg or {})

    # config file
    cfg_file_path = _find_config_file(config_path)
    file_cfg: Dict[str, Any] = {}
    if cfg_file_path:
        file_raw = _read_toml_file(cfg_file_path)
        # if file has a top-level table matching 'sikuliplus' or 'inovarobot', try to use it
        if isinstance(file_raw, dict) and "sikuliplus" in file_raw:
            file_cfg = file_raw.get("sikuliplus", {})
        else:
            file_cfg = file_raw
        file_cfg = _coerce_types(file_cfg or {})

    # environment variables
    env_cfg = _read_env(env_prefix)

    merged = merge_dicts(defaults, pyproject_cfg, file_cfg, env_cfg)

    # validations
    if "similarity" in merged:
        sim = float(merged["similarity"])
        if not (0.0 <= sim <= 1.0):
            raise ConfigError("'similarity' must be between 0.0 and 1.0")

    return Config(
        similarity=float(merged.get("similarity", defaults["similarity"])),
        timeout=float(merged.get("timeout", defaults["timeout"])),
        action_speed=float(merged.get("action_speed", defaults["action_speed"])),
        highlight=bool(merged.get("highlight", defaults["highlight"])),
        highlight_time=float(merged.get("highlight_time", defaults["highlight_time"])),
        language=str(merged.get("language", defaults["language"])),
    )
