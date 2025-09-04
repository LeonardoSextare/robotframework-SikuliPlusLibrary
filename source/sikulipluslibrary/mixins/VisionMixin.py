from robot.api.deco import keyword
from SikuliPlusLibrary.decorators.similarity import with_similarity
from SikuliPlusLibrary.decorators.roi import with_roi
from robot.libraries.BuiltIn import BuiltIn
from SikuliLibrary import SikuliLibrary


class VisionMixin:
    def __init__(self) -> None:
        self.global_similarity: float

        self.global_vision_timeout: float
        self.show_vision_highlight: bool
        self.vision_highlight_timeout: float

        self.show_actions_highlight: bool
        self.global_action_speed: float

        self.robot: BuiltIn
        self.sikuli: SikuliLibrary

    @with_roi
    @with_similarity
    @keyword
    def wait_until_image_appear(self, image: str, timeout: float):
        self.sikuli.run_keyword("Wait Until Screen Contain", [image, timeout])

    @with_roi
    @with_similarity
    @keyword
    def wait_until_image_dissapear(self, image: str, timeout: float):
        self.sikuli.run_keyword("Wait Until Screen Not Contain", [image, timeout])

    def count_images(self): ...
    def image_exists(self): ...
    def wait_one_of_multiple_images(self): ...
    def wait_multiple_images(self): ...

    def _highlight(self): ...
    def _get_image_region(self): ...
