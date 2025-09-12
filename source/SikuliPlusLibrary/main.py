from __future__ import annotations

from typing import Optional, Union, List, Dict

from robot.libraries.BuiltIn import BuiltIn
from SikuliLibrary import SikuliLibrary
from robot.api.deco import library, keyword
import os
from contextlib import redirect_stdout

from .config import load_config, Config, ConfigError


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
        raise NotImplementedError("wait_until_image_appear is not implemented yet")

    @keyword
    def wait_until_image_dissapear(
        self,
        image: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ):
        raise NotImplementedError("wait_until_image_dissapear is not implemented yet")

    @keyword
    def count_image(
        self,
        image: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ) -> int:
        raise NotImplementedError("count_image is not implemented yet")

    @keyword
    def count_multiple_images(
        self,
        *images: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ) -> Dict[str, int]:
        raise NotImplementedError("count_multiple_images is not implemented yet")

    @keyword
    def image_exists(
        self,
        image: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ) -> bool:
        raise NotImplementedError("image_exists is not implemented yet")

    @keyword
    def multiple_images_exists(
        self,
        *images: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ) -> Dict[str, bool]:
        raise NotImplementedError("multiple_images_exists is not implemented yet")

    @keyword
    def wait_one_of_multiple_images(
        self,
        *images: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ) -> str:
        raise NotImplementedError("wait_one_of_multiple_images is not implemented yet")

    @keyword
    def wait_multiple_images(
        self,
        *images: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ):
        raise NotImplementedError("wait_multiple_images is not implemented yet")
