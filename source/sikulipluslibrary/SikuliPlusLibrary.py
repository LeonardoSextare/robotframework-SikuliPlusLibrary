from robot.libraries.BuiltIn import BuiltIn
from SikuliLibrary import SikuliLibrary
from robot.api.deco import library
from robot.api.logger import console
from .mixins import VisionMixin
import os
from contextlib import redirect_stdout

from .Settings import Settings, get_settings


@library(scope="GLOBAL", version="0.1.0")
class SikuliPlusLibrary(VisionMixin):

    def __init__(self, config_file="auto") -> None:
        self.ROBOT_LIBRARY_LISTENER = self  # Estudar
        self.ROBOT_LISTENER_API_VERSION = 3  # Estudar

        self.configs: Settings = get_settings(config_file)
        self.similarity: float = self.configs.similarity

        self.vision_timeout: float = self.configs.vision_timeout
        self.action_speed: float = self.configs.action_speed

        self.highlight: bool = self.configs.highlight
        self.highlight_time: float = self.configs.highlight_time
        self.language: str = self.configs.language

        self.robot: BuiltIn
        self.sikuli: SikuliLibrary

    def start_suite(self, data, result):
        self.robot = BuiltIn()

        console(f"{self.configs}")
        try:
            self.sikuli = self.robot.get_library_instance("SikuliLibrary")
        except RuntimeError:
            self.robot.import_library("SikuliLibrary", "mode=NEW")
            self.sikuli = self.robot.get_library_instance("SikuliLibrary")
            self.sikuli.start_sikuli_process()

    def close(self):
        with open(os.devnull, "w") as _, redirect_stdout(_):
            self.sikuli.run_keyword("stop_remote_server")
