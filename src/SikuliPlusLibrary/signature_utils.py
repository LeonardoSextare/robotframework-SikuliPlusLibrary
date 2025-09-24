import inspect
from typing import Dict, Any, List, Set
from .helpers import get_user_defined_methods


def apply_methods_defaults(obj, defaults_map: Dict[str, Any]) -> None:
    cls = obj.__class__
    method_names = get_user_defined_methods(cls)

    for method_name in method_names:
        method = getattr(cls, method_name)
        _apply_defaults_to_method(method, defaults_map)





def _apply_defaults_to_method(method, defaults_map: Dict[str, Any]) -> None:
    sig = inspect.signature(method)
    param_names = set(sig.parameters.keys())
    matching_params = set(defaults_map.keys()) & param_names

    if matching_params:
        new_params = _create_updated_parameters(sig, defaults_map, matching_params)
        _update_method_signature(method, sig, new_params)


def _create_updated_parameters(signature: inspect.Signature, defaults_map: Dict[str, Any], matching_params: Set[str]) -> List[inspect.Parameter]:
    new_params = []

    for param in signature.parameters.values():
        if param.name in matching_params:
            new_params.append(param.replace(default=defaults_map[param.name]))
        else:
            new_params.append(param)

    return new_params


def _update_method_signature(method, original_sig: inspect.Signature, new_params: List[inspect.Parameter]) -> None:
    new_sig = original_sig.replace(parameters=new_params)
    method.__signature__ = new_sig

    _update_runtime_defaults(method, new_params)


def _update_runtime_defaults(func, params: List[inspect.Parameter]) -> None:
    empty = inspect.Parameter.empty
    positional_only = inspect.Parameter.POSITIONAL_ONLY
    positional_or_keyword = inspect.Parameter.POSITIONAL_OR_KEYWORD
    keyword_only = inspect.Parameter.KEYWORD_ONLY
    
    positional_defaults = []
    kwonly_defaults = {}

    for param in params:
        if param.default is empty:
            continue
        
        if param.kind in (positional_only, positional_or_keyword):
            positional_defaults.append(param.default)
        elif param.kind is keyword_only:
            kwonly_defaults[param.name] = param.default

    if positional_defaults:
        func.__defaults__ = tuple(positional_defaults)
    if kwonly_defaults:
        func.__kwdefaults__ = kwonly_defaults
