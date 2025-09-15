from __future__ import annotations

import time
from typing import Optional, Union, List
from contextlib import contextmanager

from SikuliLibrary import SikuliLibrary
from ..config import Config


class ContextManagerMixin:
    """Mixin that provides context managers for all modules.
    
    This mixin requires the including class to have:
    - self.sikuli: SikuliLibrary instance
    - self.config: Config instance with similarity, highlight, highlight_time attributes
    """
    
    # Type hints for required attributes (to be provided by implementing class)
    sikuli: SikuliLibrary
    config: Config

    @contextmanager
    def _temporary_similarity(self, similarity: float):
        """Context manager to temporarily set similarity and restore original value."""        
        if similarity == self.config.similarity:
            yield similarity
            return
            
        previous_similarity = self.sikuli.run_keyword("Set Min Similarity", [similarity])
        
        try:
            yield similarity
        finally:
            # Always restore similarity, even if exception occurred (fail fast principle)
            self.sikuli.run_keyword("Set Min Similarity", [previous_similarity])

    @contextmanager
    def _temporary_roi(self, roi: Optional[Union[str, List[int]]], timeout: float):
        """Context manager to temporarily set ROI and restore original state.
        
        ROI can be:
        - None: No ROI (default)
        - List[int]: Coordinates [x, y, width, height] 
        - str: Image path to use as ROI
        """
        if roi is None:
            yield None
            return

        roi_applied = False
        captured_roi_image = None
        
        try:
            if isinstance(roi, str):
                # ROI is an image - wait for it and get coordinates
                self.sikuli.run_keyword("Wait Until Screen Contain", [roi, timeout])
                roi_coords = self.sikuli.run_keyword("Get Image Coordinates", [roi])
                self.sikuli.run_keyword("Set Roi", [roi_coords])
                
                # Highlight the ROI image itself (not the captured region)
                if self.config.highlight:
                    self.sikuli.run_keyword("Highlight", [roi])
            else:
                # ROI is coordinates list [x, y, width, height]
                self.sikuli.run_keyword("Set Roi", [roi])
                # Capture and highlight the ROI region
                if self.config.highlight:
                    captured_roi_image = self.sikuli.run_keyword("Capture Roi", ["temp_roi_region.png"])
                    self.sikuli.run_keyword("Highlight", [captured_roi_image])
            
            roi_applied = True
            yield roi
            
        finally:
            # Always reset ROI, even if exception occurred
            if roi_applied:
                self.sikuli.run_keyword("Reset Roi", [])
            # Note: Highlights are managed separately and cleared by calling code

    @contextmanager
    def _managed_highlights(self):
        """Context manager for image operations with automatic highlight cleanup."""
        
        def add_highlight(image: str) -> None:
            """Add highlight for an image without clearing (for accumulative highlighting)."""
            if self.config.highlight:
                self.sikuli.run_keyword("Highlight", [image])

        def clear_highlights() -> None:
            """Clear all highlights with appropriate timing."""
            if self.config.highlight:
                time.sleep(self.config.highlight_time)
                self.sikuli.run_keyword("Clear All Highlights", [])
        
        try:
            yield add_highlight
        finally:
            clear_highlights()

    @contextmanager
    def _standard_context(self, similarity: float, roi: Optional[Union[str, List[int]]] = None, timeout: float = 10.0):
        """Standard context manager combining similarity, ROI, and highlights.
        
        For special cases where you need different combinations, compose the
        individual context managers (_temporary_similarity, _temporary_roi, 
        _managed_highlights) as needed.
        
        Args:
            similarity: Similarity threshold (required, no longer optional)
            roi: Region of Interest - image path or [x, y, width, height] coordinates
            timeout: Timeout for ROI image search and general operations
            
        Yields:
            add_highlight: Function to add highlights (same as _managed_highlights)
        """
        with self._temporary_similarity(similarity):
            with self._temporary_roi(roi, timeout):
                with self._managed_highlights() as add_highlight:
                    yield add_highlight