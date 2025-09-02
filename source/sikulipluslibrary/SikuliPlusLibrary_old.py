from pathlib import Path
from robot.libraries.BuiltIn import BuiltIn
from SikuliLibrary import SikuliLibrary
from robot.api.deco import library, keyword
from robot.api import logger
from .SikuliWrapper import SikuliPlusMixin
from .functions import _normalize_str_paths


@library(scope="GLOBAL", version="0.1.0")
class SikuliPlusLibrary(SikuliPlusMixin):

    def __init__(self) -> None:
        self.ROBOT_LIBRARY_LISTENER = self
        self.ROBOT_LISTENER_API_VERSION = 2

        self.default_similarity = 0.80
        self.show_highlight = True
        self.highlight_timeout = 1.00

        self.robot: BuiltIn
        self.sikuli: SikuliLibrary

    def set_highlight(self, setting: bool, timeout: float):
        self.show_highlight = setting
        self.highlight_timeout = timeout

    @keyword
    def wait_screen_Contain(self, image: str, timeout: int = 5, similarity: float = 0.8, roi_image: str = ""):
        obj_image, obj_roi_image = _normalize_str_paths(image, roi_image)
        self._set_similarity(similarity)

        if roi_image:
            self._set_roi(obj_roi_image)

        if self.show_highlight:
            self._highlight(obj_image)

        self.robot.run_keyword("Wait Until Screen Contain", obj_image, timeout)

        self._reset_definitions()

    @keyword
    def image_exists(
        self,
        image: str,
        timeout: int = 5,
        similarity: float = 0.8,
    ):
        print("teste")
