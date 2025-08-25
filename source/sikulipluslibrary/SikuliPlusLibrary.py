from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import library, keyword


@library(scope="GLOBAL", version="0.1.0")
class SikuliPlusLibrary:

    def __init__(
        self,
        default_similarity: float = 0.80,
        sikuli_name: str = "SikuliLibrary",
    ) -> None:
        self.robot = BuiltIn()
        self.DEFAULT_SIMILARITY = default_similarity
        self.sikuli = self._get_sikuli_instance(sikuli_name)

    def _get_sikuli_instance(self, sikuli_name: str):
        try:
            instance = self.robot.get_library_instance(sikuli_name)
        except RuntimeError:
            instance = self.robot.import_library(sikuli_name)

        return instance

