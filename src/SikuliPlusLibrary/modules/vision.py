from SikuliLibrary import SikuliLibrary
from typing import Optional, List

class VisionModule:
    def __init__(self, sikuli: SikuliLibrary):
        self.sikuli = sikuli

    def wait_for_image(self, image_path: str, timeout: int = 0) -> bool:
        raise NotImplementedError("This method should be implemented in the future.")
    
    def wait_for_any_image(self, image_paths: List[str], timeout: int = 0) -> Optional[str]:
        raise NotImplementedError("This method should be implemented in the future.")

    def wait_for_all_images(self, image_paths: List[str], timeout: int = 0) -> bool:
        raise NotImplementedError("This method should be implemented in the future.")