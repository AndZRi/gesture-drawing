from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import os

# i couldn't make this work for me because of some cairo errors, so...

# i don't think you need this, but in case you want all of a sudden
# install cairosvg via pip

def convert_svgs_to_pngs(src_dir: str, dest_dir: str, width, height):
    success, failure = 0, 0

    if not os.path.isdir(src_dir):
        raise NotADirectoryError(f"Provided '{src_dir}' is not a directory")
    for filename in os.listdir(src_dir):
        path = src_dir + '/' + filename
        drawing = svg2rlg(path)
        renderPM.drawToFile(drawing, dest_dir, fmt='PNG', width=width, height=height)
        success += 1

    print(f"(svg) loaded {success}/{failure + success} files")


convert_svgs_to_pngs('icons-svg', 'test', 48, 48)
