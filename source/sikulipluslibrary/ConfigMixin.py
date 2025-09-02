from robot.libraries.BuiltIn import BuiltIn
from SikuliLibrary import SikuliLibrary
import subprocess as sub


class ConfigMixin:
    def __init__(self) -> None:
        self.global_vision_timeout: float
        self.global_similarity: float

        self.show_vision_highlight: bool
        self.vision_highlight_timeout: int

        self.show_actions_highlight: bool
        self.global_action_speed: float

        self.robot: BuiltIn
        self.sikuli: SikuliLibrary

    def set_global_similarity(self): ...
    def set_global_vision_timeout(self): ...
    def set_global_vision_highlight(self): ...
    def set_global_vision_highlight_timeout(self): ...

    def set_global_action_speed(self): ...
    def set_global_action_highlight(self): ...

    def _set_temporary_roi(self): ...
    def _set_temporary_similarity(self): ...

    def _bootstrap(self):
        self.robot = BuiltIn()

        try:
            self.sikuli = self.robot.get_library_instance("SikuliLibrary")
        except RuntimeError:
            self.robot.import_library("SikuliLibrary", "mode=NEW")
            self.sikuli = self.robot.get_library_instance("SikuliLibrary")
            self.sikuli.start_sikuli_process()

    def _shutdown(self):
        self.sikuli.run_keyword("stop_remote_server")

        comando_out = sub.run(["powershell", "Get-Process", "java"])
        print(comando_out.stdout)
        # os.system('powershell Stop-Process -Name "java"')
