from functools import wraps
from inspect import signature, Parameter
from .helper import _add_parameters_to_function
from SikuliPlusLibrary.Settings import get_settings


# TODO:  Deixar as exceções mais claras
def override_timeout_parameter(func):
    default_timeout = get_settings().vision_timeout

    old_signature = signature(func)
    old_parameters = old_signature.parameters.values()

    new_params = [p.replace(default=default_timeout) if p.name == "timeout" else p for p in old_parameters]
    new_signature = old_signature.replace(parameters=new_params)
  
    func.__defaults__ = (default_timeout,)

    @wraps(func)
    def decorator(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        return result

    setattr(decorator, "__signature__", new_signature)
    return decorator
