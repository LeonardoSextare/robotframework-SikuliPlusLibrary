from robot.libraries.BuiltIn import BuiltIn
from SikuliLibrary import SikuliLibrary
from robot.api.deco import library, keyword
from .mixins import VisionMixin, ConfigMixin

from robot.api.logger import console

@library(scope="GLOBAL", version="0.1.0")
class SikuliPlusLibrary(ConfigMixin, VisionMixin):

    def __init__(self) -> None:
        self.ROBOT_LIBRARY_LISTENER = self  # Estudar
        self.ROBOT_LISTENER_API_VERSION = 3  # Estudar

        self.global_similarity: float = 0.80

        self.global_vision_timeout: float = 5.0
        self.show_vision_highlight: bool
        self.vision_highlight_timeout: float

        self.show_actions_highlight: bool
        self.global_action_speed: float

        self.robot: BuiltIn
        self.sikuli: SikuliLibrary


    def start_suite(self, data, result):
        self._bootstrap()

    def close(self):
        self._shutdown()