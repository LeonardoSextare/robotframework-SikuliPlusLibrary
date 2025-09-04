from functools import wraps
from inspect import signature, Parameter
from typing import Optional


def _set_temporary_similarity(func):
    original_signature = signature(func)
    original_parameters = list(original_signature.parameters.values())

    new_parameter = [Parameter("similarity", kind=Parameter.KEYWORD_ONLY, default=None, annotation=float)]
    new_signature = original_signature.replace(parameters=original_parameters + new_parameter)

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        similarity = kwargs.pop("similarity", None)
        if similarity is None:
            similarity = self.global_similarity

        self.sikuli.run_keyword("Set Min Similarity", [similarity])
        try:
            result = func(self, *args, **kwargs)  # testar em situação de exceção
        finally:
            self.sikuli.run_keyword("Set Min Similarity", [self.global_similarity])

        return result

    # Adicionar float ao tipo similarity
    anns = dict(getattr(func, "__annotations__", {}))
    anns["similarity"] = float
    wrapper.__annotations__ = anns

    # Adicionar assiantura nova
    setattr(wrapper, "__signature__", new_signature)
    return wrapper
