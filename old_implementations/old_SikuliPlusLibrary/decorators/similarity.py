from functools import wraps
from inspect import Parameter
from .helper import _add_parameters_to_function
from old_SikuliPlusLibrary.Settings import get_settings

# TODO:  Deixar as exceções mais claras
def similarity_parameter(func):
    default_similarity = get_settings().similarity
    similarity_param = Parameter(
        "similarity",
        kind=Parameter.KEYWORD_ONLY,
        default=default_similarity,
        annotation=float,
    )

    new_function = _add_parameters_to_function(func, similarity_param)

    @wraps(new_function)
    def decorator(self, *args, **kwargs):
        similarity = kwargs.pop("similarity", default_similarity)

        try:
            self.sikuli.run_keyword("Set Min Similarity", [similarity])
            result = new_function(self, *args, **kwargs)
        finally:
            self.sikuli.run_keyword("Set Min Similarity", [default_similarity])

        return result

    return decorator
