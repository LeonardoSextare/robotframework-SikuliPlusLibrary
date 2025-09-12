from functools import wraps
from inspect import signature, Parameter
from .helper import _add_parameters_to_function
from old_SikuliPlusLibrary.Settings import get_settings
import time

# TODO: compartilhar o mesmo tempo de timeout original e não duplicar.
# TODO:  Deixar as exceções mais claras de quem causou e porque
def roi_parameter(func):
    original_signature = signature(func)
    
    roi_parameter = Parameter("roi", kind=Parameter.KEYWORD_ONLY, default=None, annotation=str | list[int])
    new_function = _add_parameters_to_function(func, roi_parameter)

    @wraps(new_function)
    def decorator(self, *args, **kwargs):
        roi_arg = kwargs.pop("roi", None)

        bound_args = original_signature.bind(self, *args, **kwargs)
        bound_args.apply_defaults()
        
        timeout = bound_args.arguments["timeout"]
        
        def roi_helper(roi, timeout):
            if isinstance(roi, str):
                self.sikuli.run_keyword("Wait Until Screen Contain", [roi, timeout])
                roi_arg = self.sikuli.run_keyword("Get Image Coordinates", [roi])
                print(f"Roi image cordinates: {roi_arg}")

            self.sikuli.run_keyword("Set Roi", [roi_arg])
            image_to_highlight = self.sikuli.run_keyword("Capture Roi", ["temp_roi_region.png"])
            self.sikuli.run_keyword("Highlight", [image_to_highlight])
            
        try:
            if roi_arg is not None:
                roi_helper(roi_arg, timeout)

            result = new_function(self, *args, **kwargs)
        finally:
            self.sikuli.run_keyword("Reset Roi")
            time.sleep(get_settings().highlight_time)
            self.sikuli.run_keyword("Clear All Highlights")

        return result

    return decorator
