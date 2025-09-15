import inspect
from typing import Dict, Any


def _resolve_function(obj, method_name: str):
    """Return the function object for a method on obj.

    Prefer the class attribute (unbound function) so we update the function
    that's shared by instances. If not present, fall back to the bound method
    and its __func__.
    """
    cls = obj.__class__
    if hasattr(cls, method_name):
        return getattr(cls, method_name)
    raise ValueError(f"Method '{method_name}' not found on {cls.__name__}; expected a class-defined method")


def update_method_defaults(obj, method_name: str, defaults_map: Dict[str, Any]) -> None:
    """Set parameter defaults for a method so they appear in help and at runtime.

    - obj: instance containing the method
    - method_name: name of the method to update
    - defaults_map: dict mapping parameter name -> default value
    """
    func = _resolve_function(obj, method_name)
    sig = inspect.signature(func)
    params = list(sig.parameters.values())

    # quick validation: ensure defaults_map keys exist in the function signature
    param_names = {p.name for p in params}
    invalid = set(defaults_map) - param_names
    if invalid:
        raise ValueError(
            f"Invalid default parameter(s) for '{method_name}': {', '.join(sorted(invalid))}. " f"Available parameters: {', '.join(sorted(param_names))}"
        )

    # create new Parameter list with replaced defaults
    new_params = []
    for param in params:
        if param.name in defaults_map:
            new_params.append(param.replace(default=defaults_map[param.name]))
        else:
            new_params.append(param)

    func.__signature__ = sig.replace(parameters=new_params)

    positional_kinds = (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    kwonly_kind = inspect.Parameter.KEYWORD_ONLY
    empty = inspect._empty

    positional_defaults = []
    for param in new_params:
        if param.kind in positional_kinds and param.default is not empty:
            positional_defaults.append(param.default)

    kwonly_defaults = {}
    for param in new_params:
        if param.kind is kwonly_kind and param.default is not empty:
            kwonly_defaults[param.name] = param.default

    if positional_defaults:
        func.__defaults__ = tuple(positional_defaults)
    if kwonly_defaults:
        func.__kwdefaults__ = kwonly_defaults


def update_methods_defaults(obj, mapping: Dict[str, Dict[str, Any]]) -> None:
    """Apply defaults_map for multiple methods.

    mapping example: { 'method_name': {'timeout': 1.0, 'similarity': 0.7}, ... }
    """
    for method_name, defaults_map in mapping.items():
        update_method_defaults(obj, method_name, defaults_map)
