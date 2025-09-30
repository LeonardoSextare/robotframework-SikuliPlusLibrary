from __future__ import annotations

import time
from typing import Optional, Union, List, Dict, Any

from ..mixins import ContextManagerMixin


class VisionModule(ContextManagerMixin):
    def __init__(self, sikuli, config) -> None:
        self.sikuli = sikuli
        self.config = config

    def wait_until_image_appear(
        self,
        image: str,
        timeout: float,
        *,
        similarity: float,
        roi: Optional[Union[str, List[int]]] = None,
    ):
        with self._standard_context(similarity, roi, timeout) as add_highlight:
            self.sikuli.run_keyword("Wait Until Screen Contain", [image, timeout])
            add_highlight(image)

    def wait_until_image_dissapear(
        self,
        image: str,
        timeout: float,
        *,
        similarity: float,
        roi: Optional[Union[str, List[int]]] = None,
    ):
        with self._standard_context(similarity, roi, timeout) as add_highlight:
            self.sikuli.run_keyword("Wait Until Screen Not Contain", [image, timeout])
            # Note: We don't highlight here since the image should have disappeared

    def count_image(
        self,
        image: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ) -> int:
        raise NotImplementedError("count_image is not implemented yet")

    def count_multiple_images(
        self,
        *images: str,
        timeout: float,
        similarity: float,
        roi: Optional[Union[str, List[int]]] = None,
    ) -> Dict[str, int]:
        raise NotImplementedError("count_multiple_images is not implemented yet")

    def image_exists(
        self,
        image: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ) -> bool:
        raise NotImplementedError("image_exists is not implemented yet")

    def multiple_images_exists(
        self,
        *images: str,
        timeout: float,
        similarity: float,
        roi: Optional[Union[str, List[int]]] = None,
    ) -> Dict[str, bool]:
        polling_interval = 1.0
        deadline = time.monotonic() + timeout

        remaining_images = set(images)
        status = {img: False for img in images}

        with self._temporary_similarity(similarity):
            with self._temporary_roi(roi, timeout):
                with self._managed_highlights() as add_highlight:
                    
                    while True:
                        for img in list(remaining_images):
                            image_found = self.sikuli.run_keyword("Exists", [img])

                            if image_found:
                                status[img] = True
                                remaining_images.discard(img)
                                add_highlight(img)

                        if not remaining_images:
                            return status

                        now = time.monotonic()
                        if now >= deadline:
                            return status

                        time.sleep(min(polling_interval, deadline - now))

    def wait_one_of_multiple_images(
        self,
        *images: str,
        timeout: float,
        similarity: float,
        roi: Optional[Union[str, List[int]]] = None,
    ) -> str:
        polling_interval = 1.0
        deadline = time.monotonic() + timeout

        with self._standard_context(similarity, roi, timeout) as add_highlight:
            while True:
                for img in images:
                    image_found = self.sikuli.run_keyword("Exists", [img])
                    if image_found:
                        add_highlight(img)
                        return img

                now = time.monotonic()
                if now >= deadline:
                    break

                time.sleep(min(polling_interval, deadline - now))

    def wait_multiple_images_appear(
        self,
        *images: str,
        timeout: float,
        similarity: float,
        roi: Optional[Union[str, List[int]]] = None,
    ):
        polling_interval = 1.0
        deadline = time.monotonic() + timeout

        with self._standard_context(similarity, roi, timeout) as add_highlight:
                    found_images = set()
                    
                    while True:
                        for img in images:
                            if img not in found_images:
                                image_found = self.sikuli.run_keyword("Exists", [img])
                                if image_found:
                                    found_images.add(img)
                                    add_highlight(img)

                        if len(found_images) == len(images):
                            return

                        now = time.monotonic()
                        if now >= deadline:
                            break

                        time.sleep(min(polling_interval, deadline - now))
