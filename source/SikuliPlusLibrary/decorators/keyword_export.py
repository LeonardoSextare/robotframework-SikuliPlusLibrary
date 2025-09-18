"""
Keyword Export Decorator

This module provides the export_keyword decorator that wraps the Robot Framework
@keyword decorator with additional functionality for localization, documentation,
and exception handling.

For now, it simply passes through all arguments to the original @keyword decorator.
"""

from typing import Any, Callable
from robot.api.deco import keyword


def export_keyword(name: str, docstring: str = ""):
    """
    Enhanced keyword decorator that wraps Robot Framework's @keyword decorator.
    
    This decorator takes a keyword name and optional docstring, applying them to 
    the original @keyword decorator. Type hints are automatically detected from 
    function annotations. Future enhancements will include:
    - Automatic localization of keyword names and documentation
    - Enhanced exception handling with localized messages
    - Improved IDE support and documentation generation
    
    Args:
        name: Custom keyword name (required)
        docstring: Custom docstring for the keyword (optional)
        
    Returns:
        Decorated function with Robot Framework keyword attributes
        
    Examples:
        @export_keyword('Wait Until Image Appear')
        def wait_until_image_appear():
            '''Original docstring will be preserved if no docstring parameter.'''
            pass
            
        @export_keyword('Click On Image', docstring='Clicks on the specified image')
        def click_on_image(image: str, timeout: float = 5.0):
            '''This docstring will be replaced by the decorator parameter.'''
            pass
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        # Apply the Robot Framework @keyword decorator with the specified name
        decorated_func = keyword(name=name)(func)
        
        if docstring:
            decorated_func.__doc__ = docstring
            
        return decorated_func
    
    return decorator