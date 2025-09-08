from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from SikuliLibrary import SikuliLibrary
import time


class MouseMixin:
    def __init__(self) -> None:
        self.robot: BuiltIn
        self.sikuli: SikuliLibrary

    
