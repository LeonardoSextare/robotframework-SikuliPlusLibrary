from inspect import signature, Parameter
from functools import wraps
from typing import Callable


def _add_parameters_to_function(func: Callable, *extra_params: Parameter):
    old_signature = signature(func)
    old_parameters = old_signature.parameters.values()
    new_signature = old_signature.replace(parameters=[*old_parameters, *extra_params])

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    anns = dict(getattr(func, "__annotations__", {}))
    for parameter in extra_params:
        if parameter.annotation is not Parameter.empty:
            anns[parameter.name] = parameter.annotation
    
    setattr(wrapper, "__annotations__", anns)
    setattr(wrapper, "__signature__", new_signature)

    return wrapper
