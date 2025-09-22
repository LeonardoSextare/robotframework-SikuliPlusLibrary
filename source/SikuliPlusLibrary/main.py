from __future__ import annotations

from typing import Optional, Union, List, Dict

from robot.libraries.BuiltIn import BuiltIn
from SikuliLibrary import SikuliLibrary
from robot.api.deco import library, keyword
import os
from contextlib import redirect_stdout

from .config import Config
from .signature_utils import apply_methods_defaults
from .locale_utils import locale_methods
from .modules.vision import VisionModule


@library(scope="GLOBAL", version="0.1.0")
class SikuliPlusLibrary:
    """
    Wrapper library for SikuliLibrary for Robot Framework with enhanced keywords for image recognition and interaction.
    
    """

    def __init__(self, language: str = "en_US", **kwargs) -> None:
        self.ROBOT_LIBRARY_LISTENER = self
        self.ROBOT_LISTENER_API_VERSION = 3

        self.config: Config = Config.load_config(language=language, **kwargs)

        self.robot: BuiltIn
        self.sikuli: SikuliLibrary

        apply_methods_defaults(self, {
            "timeout": self.config.timeout,
            "similarity": self.config.similarity
        })
        
        locale_methods(self, language)

    def start_suite(self, data, result):
        self.robot = BuiltIn()

        try:
            self.sikuli = self.robot.get_library_instance("SikuliLibrary")
        except RuntimeError:
            self.robot.import_library("SikuliLibrary", "mode=NEW")
            self.sikuli = self.robot.get_library_instance("SikuliLibrary")
            self.sikuli.start_sikuli_process()

        self.sikuli.run_keyword("Set Min Similarity", [self.config.similarity])

        self._configure_monitor()

        self.vision = VisionModule(self.sikuli, self.config)

    def _configure_monitor(self) -> None:
        total_screens: int = self.sikuli.run_keyword("Get Number Of Screens")  # type: ignore

        if self.config.screen_id >= total_screens:
            raise ValueError(f"Invalid screen_id {self.config.screen_id}. " f"Available screens: 0 to {total_screens - 1} (total: {total_screens})")

        self.sikuli.run_keyword("Change Screen Id", [self.config.screen_id])

        if self.config.highlight:
            with open(os.devnull, "w") as _, redirect_stdout(_):
                roi_image = self.sikuli.run_keyword("Capture ROI")

                coordinates: List[int] = self.sikuli.run_keyword("Get Image Coordinates", [roi_image])  # type: ignore

                margin = 3
                adjusted_coordinates = [
                    coordinates[0] + margin,  # x + margin
                    coordinates[1] + margin,  # y + margin
                    coordinates[2] - (2 * margin),  # width - 2*margin
                    coordinates[3] - (2 * margin),  # height - 2*margin
                ]

                self.sikuli.run_keyword("Highlight Region", [adjusted_coordinates, 1])

    def close(self):
        try:
            with open(os.devnull, "w") as _, redirect_stdout(_):
                self.sikuli.run_keyword("stop_remote_server")
        except Exception:
            pass

    # Vision keywords
    @keyword
    def wait_until_image_appear(
        self,
        image: str,
        timeout: float,
        *,
        similarity: float,
        roi: Optional[Union[str, List[int]]] = None,
    ):
        return self.vision.wait_until_image_appear(image, timeout=timeout, roi=roi, similarity=similarity)

    @keyword
    def wait_until_image_dissapear(
        self,
        image: str,
        timeout: float,
        *,
        similarity: float,
        roi: Optional[Union[str, List[int]]] = None,
    ):
        return self.vision.wait_until_image_dissapear(image, timeout=timeout, similarity=similarity, roi=roi)

    @keyword
    def count_image(
        self,
        image: str,
        timeout: float,
        *,
        similarity: float,
        roi: Optional[Union[str, List[int]]] = None,
    ) -> int:
        return self.vision.count_image(image, timeout=timeout, roi=roi, similarity=similarity)

    @keyword
    def count_multiple_images(
        self,
        *images: str,
        timeout: float,
        similarity: float,
        roi: Optional[Union[str, List[int]]] = None,
    ) -> Dict[str, int]:
        return self.vision.count_multiple_images(*images, timeout=timeout, roi=roi, similarity=similarity)

    @keyword
    def image_exists(
        self,
        image: str,
        timeout: float,
        *,
        similarity: float,
        roi: Optional[Union[str, List[int]]] = None,
    ) -> bool:
        return self.vision.image_exists(image, timeout=timeout, similarity=similarity, roi=roi)

    @keyword
    def multiple_images_exists(
        self,
        *images: str,
        timeout: float,
        similarity: float,
        roi: Optional[Union[str, List[int]]] = None,
    ) -> Dict[str, bool]:
        return self.vision.multiple_images_exists(*images, timeout=timeout, roi=roi, similarity=similarity)

    @keyword
    def wait_one_of_multiple_images(
        self,
        *images: str,
        timeout: float,
        similarity: float,
        roi: Optional[Union[str, List[int]]] = None,
    ) -> str:
        return self.vision.wait_one_of_multiple_images(*images, timeout=timeout, roi=roi, similarity=similarity)

    @keyword
    def wait_multiple_images(
        self,
        *images: str,
        timeout: float,
        similarity: float,
        roi: Optional[Union[str, List[int]]] = None,
    ):
        return self.vision.wait_multiple_images(*images, timeout=timeout, roi=roi, similarity=similarity)
