from robot.libraries.BuiltIn import BuiltIn
from SikuliLibrary import SikuliLibrary
from robot.api.deco import library, keyword
from .SikuliWrapper import SikuliPlusMixin
from .mixins.ConfigMixin import ConfigMixin
from .functions import _normalize_str_paths

from robot.api.logger import console

@library(scope="GLOBAL", version="0.1.0")
class SikuliPlusLibrary(ConfigMixin):

    def __init__(self) -> None:
        self.ROBOT_LIBRARY_LISTENER = self  # Estudar
        self.ROBOT_LISTENER_API_VERSION = 3  # Estudar

        self.global_vision_timeout: float
        self.global_similarity: float

        self.show_vision_highlight: bool
        self.vision_highlight_timeout: int

        self.show_actions_highlight: bool
        self.global_action_speed: float

        self.robot: BuiltIn
        self.sikuli: SikuliLibrary

    def start_suite(self, data, result):
        self._bootstrap()

    def close(self):
        self._shutdown()

    def set_highlight(self, setting: bool, timeout: float):
        self.show_highlight = setting
        self.highlight_timeout = timeout

    @keyword
    def wait_screen_Contain(self, image: str, timeout: int = 5, similarity: float = 0.8, roi_image: str = ""):
        obj_image, obj_roi_image = _normalize_str_paths(image, roi_image)
        self.robot.run_keyword("Wait Until Screen Contain", obj_image, timeout)

        # if roi_image:
        #     self._set_roi(obj_roi_image)

        # if self.show_highlight:
        #     self._highlight(obj_image)

        # self.robot.run_keyword("Wait Until Screen Contain", obj_image, timeout)

        # self._reset_definitions()

    @keyword
    def image_exists(
        self,
        image: str,
        timeout: int = 5,
        similarity: float = 0.8,
    ):
        print("teste")
