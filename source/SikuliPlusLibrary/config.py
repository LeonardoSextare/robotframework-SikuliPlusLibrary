from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict
import os


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
    language: str = "en_US"
    screen_id: int = 0

    @classmethod
    def from_kwargs(cls, **kwargs: Any) -> Dict[str, Any]:
        """Create config dict from kwargs with type coercion and validation.
        
        Args:
            **kwargs: Configuration parameters
            
        Returns:
            Dict: Coerced and validated config values
            
        Raises:
            ConfigError: If invalid values are provided
        """
        coerced = _coerce_types(kwargs)
        _validate_config_values(coerced)
        return coerced
    
    @classmethod
    def from_environment(cls, prefix: str = "SIKULIPLUS_") -> Dict[str, Any]:
        """Create config dict from environment variables.
        
        Args:
            prefix: Environment variable prefix (default: SIKULIPLUS_)
            
        Returns:
            Dict: Environment config values (coerced and validated)
        """
        out: Dict[str, Any] = {}
        for env_name, env_value in os.environ.items():
            if not env_name.startswith(prefix):
                continue
            key = env_name[len(prefix):].lower()
            key = key.replace("-", "_")
            out[key] = env_value
        
        return cls.from_kwargs(**out)
    
    @classmethod
    def load_config(cls, language: str = "en_US", **kwargs: Any) -> Config:
        """Load configuration with precedence: defaults < kwargs < environment.
        
        Args:
            language: Language setting (default: en_US)
            **kwargs: Additional configuration parameters
            
        Returns:
            Config: Configured instance with proper precedence
        """
        # Start with defaults
        defaults = cls().__dict__
        
        # Apply kwargs
        kwargs_dict = cls.from_kwargs(language=language, **kwargs)
        
        # Apply environment (highest precedence)
        env_dict = cls.from_environment("SIKULIPLUS_")
        
        # Merge with precedence: defaults < kwargs < environment
        merged = {**defaults, **kwargs_dict, **env_dict}
        
        return cls(
            similarity=float(merged["similarity"]),
            timeout=float(merged["timeout"]),
            action_speed=float(merged["action_speed"]),
            highlight=bool(merged["highlight"]),
            highlight_time=float(merged["highlight_time"]),
            language=str(merged["language"]),
            screen_id=int(merged["screen_id"]),
        )


def _coerce_types(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Coerce raw configuration values to proper types.
    
    Args:
        raw: Raw configuration dictionary
        
    Returns:
        Dict with properly typed values
        
    Raises:
        ConfigError: If type coercion fails
    """
    # Simple mapping of exact key names to converter functions
    TYPE_MAPPING = {
        "similarity": float,
        "timeout": float,
        "action_speed": float,
        "highlight": coerce_bool,
        "highlight_time": float,
        "language": str,
        "screen_id": int,
    }
    
    out: Dict[str, Any] = {}
    for raw_key, raw_value in raw.items():
        normalized_key = raw_key.lower()
        
        if normalized_key in TYPE_MAPPING:
            converter = TYPE_MAPPING[normalized_key]
            try:
                out[normalized_key] = converter(raw_value)
            except (ValueError, TypeError) as e:
                raise ConfigError(f"Invalid value for '{raw_key}': {raw_value}. {str(e)}") from e
        else:
            # Unknown keys are ignored in strict mode
            pass
    
    return out


def coerce_bool(value: Any) -> bool:
    """Coerce boolean values with support for string "true"/"false".
    
    Handles:
    - Strings "true"/"false" (case insensitive) -> converts to bool
    - Everything else -> passed to Python's built-in bool() (0, 1, None, etc.)
    
    Does NOT handle special cases like "yes"/"no", "on"/"off", etc.
    
    Args:
        value: Value to convert to boolean
        
    Returns:
        Boolean value
        
    Raises:
        ValueError: If string is not "true" or "false"
    """
    if isinstance(value, str):
        lowered = value.lower()
        if lowered == "true":
            return True
        elif lowered == "false":
            return False
        else:
            raise ValueError("string must be 'true' or 'false' (case insensitive)")
    else:
        return bool(value)


def _validate_config_values(config_dict: Dict[str, Any]) -> None:
    """Validate configuration values.
    
    Args:
        config_dict: Configuration dictionary to validate
        
    Raises:
        ConfigError: If validation fails
    """
    if "similarity" in config_dict:
        sim = float(config_dict["similarity"])
        if not (0.0 <= sim <= 1.0):
            raise ConfigError("'similarity' must be between 0.0 and 1.0")

    if "screen_id" in config_dict:
        screen_id = int(config_dict["screen_id"])
        if screen_id < 0:
            raise ConfigError("'screen_id' must be >= 0")
            
    if "timeout" in config_dict:
        timeout = float(config_dict["timeout"])
        if timeout <= 0:
            raise ConfigError("'timeout' must be > 0")
            
    if "action_speed" in config_dict:
        action_speed = float(config_dict["action_speed"])
        if action_speed < 0:
            raise ConfigError("'action_speed' must be >= 0")
            
    if "highlight_time" in config_dict:
        highlight_time = float(config_dict["highlight_time"])
        if highlight_time <= 0:
            raise ConfigError("'highlight_time' must be > 0")



