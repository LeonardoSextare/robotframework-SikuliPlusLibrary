from SikuliLibrary import SikuliLibrary
from ..mixins.vision_context import VisionContextMixin
from typing import Optional, List

class VisionModule(VisionContextMixin):
    def __init__(self, sikuli: SikuliLibrary):
        self.sikuli = sikuli

    def wait_for_image(self, image: str, timeout: int, similarity: float, roi: Optional[List[int]]) -> Optional[str]:
        with self._vision_context(similarity, roi=roi, timeout=timeout) as add_highlight:
            self.sikuli.run_keyword("Wait Until Screen Contain", [image, timeout])
            add_highlight(image)
            return
    
    def wait_for_any_image(self, images: List[str], timeout: int = 0) -> Optional[str]:
        raise NotImplementedError("This method should be implemented in the future.")

    def wait_for_all_images(self, images: List[str], timeout: int = 0) -> bool:
        raise NotImplementedError("This method should be implemented in the future.")