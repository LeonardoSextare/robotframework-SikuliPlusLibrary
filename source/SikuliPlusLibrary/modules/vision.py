from __future__ import annotations

from typing import Optional, Union, List, Dict


class VisionModule:
    """
    TODO: implementar doctstring
    """

    def __init__(self, sikuli, config) -> None:
        self.sikuli = sikuli
        self.config = config

    def wait_until_image_appear(
        self,
        image: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ):
        raise NotImplementedError("wait_until_image_appear is not implemented yet")

    def wait_until_image_dissapear(
        self,
        image: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ):
        raise NotImplementedError("wait_until_image_dissapear is not implemented yet")

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
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
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
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ) -> Dict[str, bool]:
        raise NotImplementedError("multiple_images_exists is not implemented yet")

    def wait_one_of_multiple_images(
        self,
        *images: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ) -> str:
        raise NotImplementedError("wait_one_of_multiple_images is not implemented yet")

    def wait_multiple_images(
        self,
        *images: str,
        timeout: Optional[float] = None,
        roi: Optional[Union[str, List[int]]] = None,
        similarity: Optional[float] = None,
    ):
        raise NotImplementedError("wait_multiple_images is not implemented yet")
