import inspect
from typing import List


def get_user_defined_methods(cls) -> List[str]:
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