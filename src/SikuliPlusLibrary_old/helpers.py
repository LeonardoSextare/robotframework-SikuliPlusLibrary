import inspect
from typing import List


def get_user_defined_methods(cls) -> List[str]:
    method_names = []
    
    for name in dir(cls):
        if name.startswith("_"):
            continue
            
        attr = getattr(cls, name)
        
        if inspect.isfunction(attr):
            method_names.append(name)
    
    return method_names