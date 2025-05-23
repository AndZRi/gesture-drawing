import sys
import os

from PIL import Image
from modules.MenuFrame import get_images_from_dir

# THIS MODULE MUST NOT BE MOVED FROM PROJECT DIRECTORY (because of compile.py data directories)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class RelativePaths:
    TEST_IMAGES_DIR = "test_images"
    PLAY_ICON = "icons\\play.png"
    NEXT_ICON = "icons\\next.png"
    PREVIOUS_ICON = "icons\\previous.png"
    PAUSE_ICON = "icons\\pause.png"

class Processed:
    TestImages = get_images_from_dir(resource_path(RelativePaths.TEST_IMAGES_DIR))
    PlayIcon = Image.open(resource_path(RelativePaths.PLAY_ICON))
    NextIcon = Image.open(resource_path(RelativePaths.NEXT_ICON))
    PreviousIcon = Image.open(resource_path(RelativePaths.PREVIOUS_ICON))
    PauseIcon = Image.open(resource_path(RelativePaths.PAUSE_ICON))
