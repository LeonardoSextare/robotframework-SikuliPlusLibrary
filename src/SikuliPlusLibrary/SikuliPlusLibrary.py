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

        # Placeholders for dynamic keyword management
        self._keywords = {
            "Wait For Image": self.vision.wait_for_image,
            "Wait For Any Image": self.vision.wait_for_any_image,
            "Wait For All Images": self.vision.wait_for_all_images,
        }

        self.similarity_default = 0.7
        self.timeout_default = 0
        self.roi_default = None

        self._keywords_arguments = {
            "Wait For Image": [
                "image",
                f"timeout={self.timeout_default}",
                "*",
                f"similarity={self.similarity_default}",
                f"roi={self.roi_default}",
            ],
            "Wait For Any Image": [
                "image",
                f"timeout={self.timeout_default}",
                "*",
                f"similarity={self.similarity_default}",
                f"roi={self.roi_default}",
            ],
            "Wait For All Images": [
                "image",
                f"timeout={self.timeout_default}",
                "*",
                f"similarity={self.similarity_default}",
                f"roi={self.roi_default}",
            ],
        }

        self._keywords_documentation = {
            "Wait For Image": "Waits until the specified image appears on the screen.",
            "Wait For Any Image": "Waits until any of the specified images appear on the screen.",
            "Wait For All Images": "Waits until all of the specified images appear on the screen.",
        }

        self._keywords_arguments_types = {
            "Wait For Image": {
                "image": str,
                "timeout": float,
                "similarity": float,
                "roi": Optional[Union[str, list[int]]],
            },
            "Wait For Any Image": {
                "image": list[str],
                "timeout": float,
                "similarity": float,
                "roi": Optional[Union[str, list[int]]],
                "return": str,
            },
            "Wait For All Images": {
                "image": list[str],
                "timeout": float,
                "similarity": float,
                "roi": Optional[Union[str, list[int]]],
            },
        }

    def run_keyword(self, name: str, args: list, kwargs: Optional[dict] = None) -> Any:
        return self._keywords[name](*args, **(kwargs or {}))

    def get_keyword_names(self) -> list[str]:
        return list(self._keywords.keys())

    def get_keyword_arguments(self, name: str) -> list[str]:
        return self._keywords_arguments.get(name, [])

    def get_keyword_documentation(self, name: str) -> str:
        return self._keywords_documentation.get(name, "")

    def get_keyword_types(self, name: str) -> dict:
        return self._keywords_arguments_types.get(name, {})

    def start_suite(self, name: str, attrs: dict) -> None:
        self.sikuli.start_sikuli_process()

    def close(self) -> None:
        self.sikuli.run_keyword("stop_remote_server")
