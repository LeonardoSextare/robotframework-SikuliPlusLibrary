from SikuliLibrary import SikuliLibrary
from contextlib import contextmanager
import time
from typing import Optional, Union, List


class VisionContextMixin:
    sikuli: SikuliLibrary

    @contextmanager
    def _similarity_context(self, similarity: float):
        # Placeholder for default similarity value from config
        if similarity == 0.7:
            yield None
            return None

        previous_similarity = self.sikuli.run_keyword(
            "Set Min Similarity", [similarity]
        )
        try:
            yield similarity
        finally:
            self.sikuli.run_keyword("Set Min Similarity", [previous_similarity])

    @contextmanager
    def _roi_context(self, roi: Optional[Union[str, List[int]]], timeout: float):
        if roi is None:
            yield None
            return None

        highlights_enabled = True  # Placeholder for self.config.highlight

        try:
            if isinstance(roi, str):
                self.sikuli.run_keyword("Wait Until Screen Contain", [roi, timeout])
                roi_coords = self.sikuli.run_keyword("Get Image Coordinates", [roi])
                self.sikuli.run_keyword("Set Roi", [roi_coords])

                if highlights_enabled:
                    self.sikuli.run_keyword("Highlight", [roi])
            else:
                self.sikuli.run_keyword("Set Roi", [roi])
                if highlights_enabled:
                    temp_roi_image = self.sikuli.run_keyword(
                        "Capture Roi", ["temp_roi_region.png"]
                    )
                    self.sikuli.run_keyword("Highlight", [temp_roi_image])

            yield roi

        finally:
            self.sikuli.run_keyword("Reset Roi", [])

    @contextmanager
    def _highlight_context(self):
        highlights_enabled = True  # Placeholder for self.config.highlight

        def add_highlight(image: str) -> None:
            if highlights_enabled:
                self.sikuli.run_keyword("Highlight", [image])

        try:
            yield add_highlight
        finally:
            if highlights_enabled:
                time.sleep(1)  # Simulate highlight duration from config
                self.sikuli.run_keyword("Clear All Highlights", [])

    @contextmanager
    def _vision_context(
        self,
        similarity: float,
        timeout: float = 0,
        roi: Optional[Union[str, List[int]]] = None,
    ):
        with self._similarity_context(similarity):
            with self._roi_context(roi, timeout):
                with self._highlight_context() as add_highlight:
                    yield add_highlight
