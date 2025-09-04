from functools import wraps
from inspect import signature, Parameter

# TODO:  Deixar as exceções mais claras de quem causou e porque 
def with_roi(func):
    original_signature = signature(func)
    original_parameters = list(original_signature.parameters.values())

    new_parameter = [Parameter("roi", kind=Parameter.KEYWORD_ONLY, default=None, annotation=list[int] | str)]
    new_signature = original_signature.replace(parameters=original_parameters + new_parameter)

    @wraps(func)
    def decorator(self, *args, **kwargs):
        roi = kwargs.pop("roi", None)

        if roi is not None:
            if isinstance(roi, str):
                timeout = args[1]
                self.sikuli.run_keyword("Wait Until Screen Contain", [roi, timeout])
                
                roi = self.sikuli.run_keyword("Get Image Coordinates", [roi])
                print(f"Roi image cordinates: {roi}")

            self.sikuli.run_keyword("Set Roi", [roi])
        
        try:
            result = func(self, *args, **kwargs)
        finally:
            self.sikuli.run_keyword("Reset Roi")

        return result

    # Adicionar float ao tipo similarity
    anns = dict(getattr(func, "__annotations__", {}))
    anns["roi"] = list[int] | str
    decorator.__annotations__ = anns

    # Adicionar assiantura nova
    setattr(decorator, "__signature__", new_signature)
    return decorator
