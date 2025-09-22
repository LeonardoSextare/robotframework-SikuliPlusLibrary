import inspect
import tomllib
from pathlib import Path
from typing import Dict, Any, List
from .helpers import get_user_defined_methods


def locale_methods(obj, language: str) -> None:
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
    current_dir = Path(__file__).parent
    locale_file = current_dir / "keywords_names" / f"{language}.toml"
    
    if locale_file.exists():
        with open(locale_file, "rb") as f:
            return tomllib.load(f)
    


def _apply_locale_to_method(method, method_name: str, locale_data: Dict[str, Any]) -> None:
    method_data = locale_data[method_name]
    
    method.robot_name = method_data["robot_name"]
    method.__doc__ = method_data["doc_string"]

    