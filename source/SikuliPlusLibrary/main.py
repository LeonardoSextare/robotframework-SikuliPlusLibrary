from __future__ import annotations

from typing import Optional, Union, List, Dict
import inspect

from robot.libraries.BuiltIn import BuiltIn
from SikuliLibrary import SikuliLibrary
from robot.api.deco import library, keyword
import os
from contextlib import redirect_stdout

from .config import load_config, Config
from .signature_utils import update_methods_defaults
from .modules.vision import VisionModule


@library(scope="GLOBAL", version="0.1.0")
class SikuliPlusLibrary:
    """Main Robot library entrypoint (skeleton).

    This class loads configuration via `load_config` and implements the
    Robot listener hooks `start_suite` and `close`. Configuration errors are
    not silenced: a `ConfigError` will propagate so the user sees the problem.
    """

    def __init__(self, config_path: Optional[str] = None) -> None:
        # Make this object a Robot listener (keeps compatibility with older code)
        self.ROBOT_LIBRARY_LISTENER = self
        self.ROBOT_LISTENER_API_VERSION = 3

        self.config: Config = load_config(config_path)

        self.robot: BuiltIn
        self.sikuli: SikuliLibrary

        # Update vision keywords defaults from config using explicit mapping
        update_methods_defaults(
            self,
            {
                "wait_until_image_appear": {"timeout": self.config.timeout, "similarity": self.config.similarity},
                "wait_until_image_dissapear": {"timeout": self.config.timeout, "similarity": self.config.similarity},
                "count_image": {"timeout": self.config.timeout, "similarity": self.config.similarity},
                "count_multiple_images": {"timeout": self.config.timeout, "similarity": self.config.similarity},
                "image_exists": {"timeout": self.config.timeout, "similarity": self.config.similarity},
                "multiple_images_exists": {"timeout": self.config.timeout, "similarity": self.config.similarity},
                "wait_one_of_multiple_images": {"timeout": self.config.timeout, "similarity": self.config.similarity},
                "wait_multiple_images": {"timeout": self.config.timeout, "similarity": self.config.similarity},
            },
        )

    def start_suite(self, data, result):
        """Robot Framework listener invoked when a test suite starts.

        Behaviour:
        - Obtain the current `SikuliLibrary` instance if already imported.
        - Otherwise import it in NEW mode and start its process (best-effort).
        This mirrors the behaviour of the previous implementation to keep
        compatibility with existing test suites.
        """
        self.robot = BuiltIn()

        try:
            self.sikuli = self.robot.get_library_instance("SikuliLibrary")
        except RuntimeError:
            self.robot.import_library("SikuliLibrary", "mode=NEW")
            self.sikuli = self.robot.get_library_instance("SikuliLibrary")
            self.sikuli.start_sikuli_process()

        # instantiate service objects that depend on a live SikuliLibrary
        self.vision = VisionModule(self.sikuli, self.config)

    def close(self):
        """Robot Framework listener invoked when the library is closed.

        Attempts to stop the remote Sikuli server (best-effort).
        """

        try:
            with open(os.devnull, "w") as _, redirect_stdout(_):
                self.sikuli.run_keyword("stop_remote_server")
        except Exception:
            # best-effort - ignore errors during shutdown
            pass

    # --- Vision keywords (skeletons copied from VisionMixin signatures) ---
    @keyword
    def wait_until_image_appear(
        self,
        image: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ):
        return self.vision.wait_until_image_appear(image, timeout=timeout, roi=roi, similarity=similarity)

    @keyword
    def wait_until_image_dissapear(
        self,
        image: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ):
        return self.vision.wait_until_image_dissapear(image, timeout=timeout, roi=roi, similarity=similarity)

    @keyword
    def count_image(
        self,
        image: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ) -> int:
        return self.vision.count_image(image, timeout=timeout, roi=roi, similarity=similarity)

    @keyword
    def count_multiple_images(
        self,
        *images: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ) -> Dict[str, int]:
        return self.vision.count_multiple_images(*images, timeout=timeout, roi=roi, similarity=similarity)

    @keyword
    def image_exists(
        self,
        image: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ) -> bool:
        return self.vision.image_exists(image, timeout=timeout, roi=roi, similarity=similarity)

    @keyword
    def multiple_images_exists(
        self,
        *images: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ) -> Dict[str, bool]:
        return self.vision.multiple_images_exists(*images, timeout=timeout, roi=roi, similarity=similarity)

    @keyword
    def wait_one_of_multiple_images(
        self,
        *images: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ) -> str:
        return self.vision.wait_one_of_multiple_images(*images, timeout=timeout, roi=roi, similarity=similarity)

    @keyword
    def wait_multiple_images(
        self,
        *images: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ):
        return self.vision.wait_multiple_images(*images, timeout=timeout, roi=roi, similarity=similarity)
