from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
from SikuliLibrary import SikuliLibrary


class ConfigMixin:
    def __init__(self) -> None:
        self.global_similarity: float

        self.global_vision_timeout: float
        self.show_vision_highlight: bool
        self.vision_highlight_timeout: float

        self.show_actions_highlight: bool
        self.global_action_speed: float

        self.robot: BuiltIn
        self.sikuli: SikuliLibrary

    @keyword
    def set_global_similarity(self, similarity: float):
        self.global_similarity = similarity

    @keyword
    def set_global_vision_timeout(self, seconds: float):
        self.global_vision_timeout = seconds

    @keyword
    def set_vision_highlight(self, setting: bool):
        self.show_vision_highlight = setting

    @keyword
    def set_global_vision_highlight_timeout(self, seconds: float):
        self.vision_highlight_timeout = seconds

    @keyword
    def set_global_action_speed(self, seconds: float):
        self.global_action_speed = seconds

    @keyword
    def set_action_highlight(self, setting: bool):
        self.show_actions_highlight = setting

    def set_temporary_roi(self): ...

    def _bootstrap(self):
        self.robot = BuiltIn()

        try:
            self.sikuli = self.robot.get_library_instance("SikuliLibrary")
        except RuntimeError:
            self.robot.import_library("SikuliLibrary", "mode=NEW")
            self.sikuli = self.robot.get_library_instance("SikuliLibrary")
            self.sikuli.start_sikuli_process()
        
        self.sikuli.run_keyword("Set Min Similarity", [self.global_similarity])
    def _shutdown(self):
        self.sikuli.run_keyword("stop_remote_server")
