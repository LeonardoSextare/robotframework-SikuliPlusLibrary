import inspect
import tomllib
from pathlib import Path
from typing import Dict, Any, List
from .helpers import get_user_defined_methods


def locale_methods(obj, language: str) -> None:
    """Apply localized robot names and docstrings to all methods automatically.
    
    This function loads the TOML file for the specified language and applies
    robot_name and docstring translations to methods that exist in the locale file.
    
    Args:
        obj: Instance of the class to modify
        language: Language code (e.g., "en_US", "pt_BR")
    """
    locale_data = _load_locale_file(language)
    if not locale_data:
        return
        
    cls = obj.__class__
    method_names = get_user_defined_methods(cls)
    
    for method_name in method_names:
        if method_name in locale_data:
            method = getattr(cls, method_name)
            _apply_locale_to_method(method, method_name, locale_data)





def _load_locale_file(language: str) -> Dict[str, Any]:
    """Load locale data from TOML file.
    
    Args:
        language: Language code (e.g., "en_US", "pt_BR")
        
    Returns:
        Dict containing locale data or empty dict if file not found
    """
    current_dir = Path(__file__).parent
    locale_file = current_dir / "keywords_names" / f"{language}.toml"
    
    if locale_file.exists():
        with open(locale_file, "rb") as f:
            return tomllib.load(f)
    


def _apply_locale_to_method(method, method_name: str, locale_data: Dict[str, Any]) -> None:
    """Apply localized name and documentation to a method.
    
    Args:
        method: Function object to modify
        method_name: Name of the method
        locale_data: Locale data from TOML file
    """
    method_data = locale_data[method_name]
    
    method.robot_name = method_data["robot_name"]
    method.__doc__ = method_data["doc_string"]

    