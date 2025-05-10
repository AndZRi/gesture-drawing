import math

from PIL import Image
from math import floor, ceil

from dataclasses import dataclass

def get_rationed_size(src_size: tuple[int, int], new_size: tuple[int, int], round_func=floor):
    width, height = new_size
    ratio = src_size[0] / src_size[1]
    nw1 = round_func(height * ratio)
    nh1 = round_func(nw1 / ratio)

    nh2 = round_func(width / ratio)
    nw2 = round_func(nh2 * ratio)

    if nw1 <= nw2:
        return nw1, nh1
    return nw2, nh2


def resize_rationed(image: Image.Image, new_size, resample=Image.Resampling.BOX, round_func=floor):
    return image.resize(get_rationed_size(image.size, new_size, round_func), resample)


def compress_image(image: Image.Image, scale: int):  # scale <= 1
    if scale < 0 or scale > 1:
        raise ValueError("Provided scale is more than 1 or less than 0 (0 < scale <= 1).")
    if scale == 1:
        return image

    return resize_rationed(image, (image.width * scale, image.height * scale), Image.Resampling.LANCZOS, ceil)


class OptimizedImage:
    def __init__(self, image: Image.Image, step: int = 0.5, grades: int = 5):
        self.native_size = image.size
        self.step = step

        self.series = [compress_image(image, step ** i) for i in range(grades)]

    def __getitem__(self, size: tuple[int, int]):
        size = get_rationed_size(self.native_size, size, ceil)
        scale = min(size[0] / self.native_size[0], 1)
        grade = floor(math.log(scale, self.step))

        return self.series[grade]


if __name__ == '__main__':
    a = OptimizedImage(Image.open("test_image2.jpg"))
    for i in a.series:
        i.show()
    # a[(1000, 1000)].show()
