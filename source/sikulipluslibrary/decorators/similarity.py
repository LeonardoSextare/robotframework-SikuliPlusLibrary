from functools import wraps
from inspect import signature, Parameter
from typing import Optional

# TODO:  Deixar as exceções mais claras
def with_similarity(func):
    original_signature = signature(func)
    original_parameters = list(original_signature.parameters.values())

    new_parameter = [Parameter("similarity", kind=Parameter.KEYWORD_ONLY, default=None, annotation=float)]
    new_signature = original_signature.replace(parameters=original_parameters + new_parameter)

    @wraps(func)
    def decorator(self, *args, **kwargs):
        similarity = kwargs.pop("similarity", None)
        if similarity is None:
            similarity = self.global_similarity

        self.sikuli.run_keyword("Set Min Similarity", [similarity])
        try:
            result = func(self, *args, **kwargs)
        finally:
            self.sikuli.run_keyword("Set Min Similarity", [self.global_similarity])

        return result

    anns = dict(getattr(func, "__annotations__", {}))
    anns["similarity"] = float
    decorator.__annotations__ = anns

    setattr(decorator, "__signature__", new_signature)
    return decorator
