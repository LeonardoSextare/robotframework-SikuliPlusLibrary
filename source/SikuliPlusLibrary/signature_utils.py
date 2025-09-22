import inspect
from typing import Dict, Any, List, Set


def apply_methods_defaults(obj, defaults_map: Dict[str, Any]) -> None:
    """Apply default values to all methods in a class automatically.

    This function introspects the class and applies default values to any
    parameter that matches the keys in defaults_map across ALL methods.

    Args:
        obj: Instance of the class to modify
        defaults_map: Dict mapping parameter name -> default value
                     Example: {'timeout': 1.0, 'similarity': 0.7}
    """
    cls = obj.__class__
    method_names = _get_user_defined_methods(cls)

    for method_name in method_names:
        method = getattr(cls, method_name)
        _apply_defaults_to_method(method, defaults_map)


def _get_user_defined_methods(cls) -> List[str]:
    """Get list of user-defined method names from a class.

    Args:
        cls: Class to inspect

    Returns:
        List of method names that are user-defined functions
    """
    method_names = []

    for name in dir(cls):
        # Skip private/special methods
        if name.startswith("_"):
            continue

        attr = getattr(cls, name)

        # Only include user-defined functions
        if inspect.isfunction(attr):
            method_names.append(name)

    return method_names


def _apply_defaults_to_method(method, defaults_map: Dict[str, Any]) -> None:
    """Apply default values to a specific method if it has matching parameters.

    Args:
        method: Function object to modify
        defaults_map: Dict mapping parameter name -> default value
    """

    sig = inspect.signature(method)
    param_names = set(sig.parameters.keys())
    matching_params = set(defaults_map.keys()) & param_names

    if matching_params:
        new_params = _create_updated_parameters(sig, defaults_map, matching_params)
        _update_method_signature(method, sig, new_params)


def _create_updated_parameters(signature: inspect.Signature, defaults_map: Dict[str, Any], matching_params: Set[str]) -> List[inspect.Parameter]:
    """Create new parameter list with updated default values.

    Args:
        signature: Original method signature
        defaults_map: Dict of new default values
        matching_params: Set of parameter names to update

    Returns:
        List of parameters with updated defaults
    """
    new_params = []

    for param in signature.parameters.values():
        if param.name in matching_params:
            new_params.append(param.replace(default=defaults_map[param.name]))
        else:
            new_params.append(param)

    return new_params


def _update_method_signature(method, original_sig: inspect.Signature, new_params: List[inspect.Parameter]) -> None:
    """Update method signature and runtime defaults.

    Args:
        method: Function object to update
        original_sig: Original signature
        new_params: New parameters with updated defaults
    """
    # Update the function signature for introspection
    new_sig = original_sig.replace(parameters=new_params)
    method.__signature__ = new_sig

    _update_runtime_defaults(method, new_params)


def _update_runtime_defaults(func, params: List[inspect.Parameter]) -> None:
    """Update function's runtime defaults (__defaults__ and __kwdefaults__).

    Args:
        func: Function to update
        params: List of parameters with default values
    """
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
