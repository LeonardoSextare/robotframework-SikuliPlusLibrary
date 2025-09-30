# from SikuliLibrary import SikuliLibrary
from robot.api.deco import library, keyword
# from typing import Optional, Union, List, Any


@library(scope="GLOBAL", version="0.1.0")
class SikuliPlusLibrary:
    def __init__(self) -> None:
        # self.sikuli: SikuliLibrary
        self._handlers = {
            "Diga Ola": self._diga_ola,
        }
        # self.vision: VisionModule

    # # === API dinâmica (obrigatória) ===
    # def get_keyword_names(self):
    #     return list(self._handlers.keys())

    # def run_keyword(self, name, args, kwargs=None):
    #     return self._handlers[name](*args, **(kwargs or {}))

    # === implementação real ===
    @keyword
    def diga_ola(self, nome="mundo"):
        return f"Olá, {nome}!"
