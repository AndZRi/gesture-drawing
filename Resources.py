import sys
import os

from modules.MenuFrame import get_images_from_dir

# THIS MODULE MUST NOT BE MOVED FROM PROJECT DIRECTORY (because of compile.py data directories)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class RelativePaths:
    TEST_IMAGES_DIR = "test_images"

class Processed:
    TestImages = get_images_from_dir(resource_path(RelativePaths.TEST_IMAGES_DIR))
