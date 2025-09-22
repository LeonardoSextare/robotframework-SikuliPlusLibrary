from __future__ import annotations

import time
from typing import Optional, Union, List
from contextlib import contextmanager

from SikuliLibrary import SikuliLibrary
from ..config import Config


class ContextManagerMixin:
    sikuli: SikuliLibrary
    config: Config

    @contextmanager
    def _temporary_similarity(self, similarity: float):
        if similarity == self.config.similarity:
            yield similarity
            return
            
        previous_similarity = self.sikuli.run_keyword("Set Min Similarity", [similarity])
        
        try:
            yield similarity
        finally:
            self.sikuli.run_keyword("Set Min Similarity", [previous_similarity])

    @contextmanager
    def _temporary_roi(self, roi: Optional[Union[str, List[int]]], timeout: float):
        if roi is None:
            yield None
            return

        roi_applied = False
        captured_roi_image = None
        
        try:
            if isinstance(roi, str):
                self.sikuli.run_keyword("Wait Until Screen Contain", [roi, timeout])
                roi_coords = self.sikuli.run_keyword("Get Image Coordinates", [roi])
                self.sikuli.run_keyword("Set Roi", [roi_coords])
                
                if self.config.highlight:
                    self.sikuli.run_keyword("Highlight", [roi])
            else:
                self.sikuli.run_keyword("Set Roi", [roi])
                if self.config.highlight:
                    captured_roi_image = self.sikuli.run_keyword("Capture Roi", ["temp_roi_region.png"])
                    self.sikuli.run_keyword("Highlight", [captured_roi_image])
            
            roi_applied = True
            yield roi
            
        finally:
            if roi_applied:
                self.sikuli.run_keyword("Reset Roi", [])

    @contextmanager
    def _managed_highlights(self):
        def add_highlight(image: str) -> None:
            if self.config.highlight:
                self.sikuli.run_keyword("Highlight", [image])

        def clear_highlights() -> None:
            if self.config.highlight:
                time.sleep(self.config.highlight_time)
                self.sikuli.run_keyword("Clear All Highlights", [])
        
        try:
            yield add_highlight
        finally:
            clear_highlights()

    @contextmanager
    def _standard_context(self, similarity: float, roi: Optional[Union[str, List[int]]] = None, timeout: float = 10.0):
        with self._temporary_similarity(similarity):
            with self._temporary_roi(roi, timeout):
                with self._managed_highlights() as add_highlight:
                    yield add_highlight