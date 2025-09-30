import time
from robot.libraries.BuiltIn import BuiltIn
from SikuliLibrary import SikuliLibrary
from robot.api.deco import keyword
from old_SikuliPlusLibrary.decorators.similarity import similarity_parameter
from old_SikuliPlusLibrary.decorators.roi import roi_parameter
from old_SikuliPlusLibrary.decorators.timeout import override_timeout_parameter


class VisionMixin:
    def __init__(self) -> None:
        self.highlight_time: float
        self.robot: BuiltIn
        self.sikuli: SikuliLibrary

    @roi_parameter
    @similarity_parameter
    @override_timeout_parameter
    @keyword
    def wait_until_image_appear(self, image: str, timeout: float):
        self.sikuli.run_keyword("Wait Until Screen Contain", [image, timeout])
        self.sikuli.run_keyword("Highlight", [image])
        time.sleep(self.highlight_time)
        self.sikuli.run_keyword("Clear All Highlights")

    @roi_parameter
    @similarity_parameter
    @override_timeout_parameter
    @keyword
    def wait_until_image_dissapear(self, image: str, timeout: float):
        self.sikuli.run_keyword("Highlight", [image])
        self.sikuli.run_keyword("Wait Until Screen Not Contain", [image, timeout])
        time.sleep(self.highlight_time)
        self.sikuli.run_keyword("Clear All Highlights")


    @roi_parameter
    @similarity_parameter
    @override_timeout_parameter
    @keyword
    def count_image(self, image: str, timeout: float) -> int:
        image_exists = self.sikuli.run_keyword("Exists", [image, timeout])

            
        result = self.sikuli.run_keyword("Image Count", [image])

        if image_exists:
            self.sikuli.run_keyword("Highlight", [image])
            time.sleep(self.highlight_time)
            self.sikuli.run_keyword("Clear All Highlights")
            

        return result  # type: ignore

    @roi_parameter
    @similarity_parameter
    @override_timeout_parameter
    @keyword
    def count_multiple_images(self, *images: str, timeout: float) -> dict[str, int]:
        tempo = timeout
        self.multiple_images_exists(*images, timeout=tempo)

        images_counts: dict[str, int] = {}
        for img in images:
            images_counts[img] = self.sikuli.run_keyword("Image Count", [img])  # type: ignore

            if images_counts[img] > 0:
                self.sikuli.run_keyword("Highlight", [img])
                time.sleep(self.highlight_time)
                self.sikuli.run_keyword("Clear All Highlights")
        return images_counts

    @roi_parameter
    @similarity_parameter
    @override_timeout_parameter
    @keyword
    def image_exists(self, image: str, timeout: float) -> bool:
        result = self.sikuli.run_keyword("Exists", [image, timeout])
        return result  # type: ignore

    @roi_parameter
    @similarity_parameter
    @override_timeout_parameter
    @keyword
    def multiple_images_exists(self, *images: str, timeout: float) -> dict[str, bool]:
        polling_inverval = 1.0
        deadline = time.monotonic() + timeout

        remaining_images = set(images)
        status = {img: False for img in images}

        while True:
            for img in list(remaining_images):
                image_found = self.sikuli.run_keyword("Exists", [img])

                if image_found:
                    status[img] = True
                    remaining_images.discard(img)

            if not remaining_images:
                return status

            now = time.monotonic()
            if now >= deadline:
                return status

            time.sleep(min(polling_inverval, deadline - now))

    @roi_parameter
    @similarity_parameter
    @override_timeout_parameter
    @keyword
    def wait_one_of_multiple_images(self, *images: str, timeout: float) -> str:
        image_found = self.sikuli.run_keyword("Wait For Multiple Images", [timeout, 1, images, []])
        return image_found  # type: ignore

    @roi_parameter
    @similarity_parameter
    @override_timeout_parameter
    @keyword
    def wait_multiple_images(self, *images: str, timeout: float):
        polling_inverval = 1.0
        deadline = time.monotonic() + timeout

        def check_image(img):
            result = self.sikuli.run_keyword("Exists", [img])
            return bool(result)

        while True:
            status = {img: check_image(img) for img in images}

            if all(status.values()):
                return

            now = time.monotonic()
            if now >= deadline:
                break

            time.sleep(min(polling_inverval, deadline - now))

        remaning_images = [img for img, found in status.items() if not found]
        raise TimeoutError(f"Timed out after {timeout:.2f}s waiting for all images to be present. " f"The following images still missing: {remaning_images}.")

    def _highlight(self, image, reset=True):
        self.sikuli.run_keyword("Highlight", [image])

        
        time.sleep(self.highlight_time)
        self.sikuli.run_keyword("Clear All Highlights")
        
