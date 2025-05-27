import sys
import os
from enum import StrEnum

from PIL import Image, UnidentifiedImageError

# THIS MODULE MUST NOT BE MOVED FROM PROJECT DIRECTORY (because of compile.py data directories)

def resource_path(relative_path) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def get_images_from_dir(src_dir: str) -> list[Image.Image]:
    images = []
    success, failure = 0, 0

    if not os.path.isdir(src_dir):
        return []
    for filename in os.listdir(src_dir):
        try:
            images.append(Image.open(src_dir + '/' + filename))
            success += 1

        except UnidentifiedImageError as ex:
            print(ex)
            failure += 1

    print(f"loaded {success}/{failure + success} files")

    return images


class AbsolutePaths(StrEnum):
    TEST_IMAGES_DIR = resource_path("data/test_images/")
    PLAY_ICON = resource_path("data/icons/play.png")
    NEXT_ICON = resource_path("data/icons/next.png")
    PREVIOUS_ICON = resource_path("data/icons/previous.png")
    PAUSE_ICON = resource_path("data/icons/pause.png")

class Processed:
    TestImages = get_images_from_dir(AbsolutePaths.TEST_IMAGES_DIR)
    PlayIcon = Image.open(AbsolutePaths.PLAY_ICON)
    NextIcon = Image.open(AbsolutePaths.NEXT_ICON)
    PreviousIcon = Image.open(AbsolutePaths.PREVIOUS_ICON)
    PauseIcon = Image.open(AbsolutePaths.PAUSE_ICON)
