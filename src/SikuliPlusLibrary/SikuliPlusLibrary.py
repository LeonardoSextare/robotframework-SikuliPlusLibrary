from SikuliLibrary import SikuliLibrary
from robot.api.deco import library, keyword
from typing import Optional, Union, List, Any
from .modules.vision import VisionModule


@library(scope="GLOBAL", listener="SELF", version="0.1.0")
class SikuliPlusLibrary:
    def __init__(self) -> None:
        self.sikuli = SikuliLibrary(mode="NEW")
        self.vision = VisionModule(self.sikuli)
        self.mouse = None  # Placeholder for future MouseModule
        self.keyboard = None  # Placeholder for future KeyboardModule

        # Placeholders for future features
        self._keywords = {
            "Wait For Image": self.vision.wait_for_image,
            "Wait For Any Image": self.vision.wait_for_any_image,
            "Wait For All Images": self.vision.wait_for_all_images,
        }

    # === API dinâmica (obrigatória) ===
    def get_keyword_names(self) -> List[str]:
        return list(self._keywords.keys())

    def run_keyword(self, name: str, args: list, kwargs: Optional[dict] = None) -> Any:
        return self._keywords[name](*args, **(kwargs or {}))

    def start_suite(self, name: str, attrs: dict) -> None:
        self.sikuli.start_sikuli_process()

    def close(self) -> None:
        self.sikuli.run_keyword("stop_remote_server")
