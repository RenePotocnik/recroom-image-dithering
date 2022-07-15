import tkinter
from tkinter import filedialog
from typing import List, Tuple

from PIL import Image

# All the RecRoom colors ordered from `Salmon` to `Black`
COLORS: List[Tuple[int, int, int]] = [(228, 80, 80), (211, 23, 24), (117, 7, 6), (123, 47, 47), (239, 127, 79),
                                      (245, 92, 25), (193, 55, 9), (127, 66, 47), (247, 215, 106), (244, 197, 31),
                                      (181, 99, 0), (130, 97, 56), (137, 177, 81), (105, 161, 24), (47, 76, 9),
                                      (66, 82, 43), (103, 190, 122), (16, 101, 34), (6, 59, 17), (51, 76, 55),
                                      (103, 218, 205), (0, 155, 137), (0, 80, 71), (51, 86, 82), (101, 199, 236),
                                      (2, 172, 234), (6, 87, 117), (49, 91, 105), (100, 161, 244), (23, 107, 221),
                                      (7, 57, 128), (50, 79, 121), (165, 133, 242), (80, 24, 221), (46, 18, 120),
                                      (86, 72, 121), (225, 148, 242), (121, 66, 131), (66, 24, 74), (88, 61, 92),
                                      (238, 120, 178), (234, 46, 79), (130, 9, 63), (104, 56, 78), (126, 64, 25),
                                      (69, 40, 22), (61, 29, 14), (36, 16, 5), (197, 132, 92), (143, 99, 72),
                                      (90, 62, 48), (37, 28, 21), (246, 239, 233), (192, 188, 185),
                                      (153, 149, 146), (124, 120, 119), (99, 100, 102), (73, 74, 78), (45, 46, 50),
                                      (25, 23, 24), (255, 181, 136), (254, 254, 254)]

# All the RecRoom colors in one list. [R, G, B, R, G, B,...]
ALL_COLORS = [num for tup in COLORS for num in tup]


def get_image() -> Image:
    """
    Open file explorer, wait for user to open an image
    :return: The image
    """
    print("Open image", end="\r")
    root = tkinter.Tk()
    root.withdraw()
    img_path = filedialog.askopenfilename(filetypes=[("Image", ".png .jpg")])
    root.destroy()

    img = Image.open(img_path)
    print("Selected image: ", img_path.split("/")[-1])

    # # If the image has attributed `palette` its metadata is a bit different.
    # # To solve this just open the image in paint and save it
    # if img.palette:
    #     print("Image has `Palette` attribute. Open it in Paint and save.")
    #     os.system(f'mspaint.exe "{Path(img_path)}"')
    #     return None

    return img, img_path


def quantize(img: Image) -> Image:
    img = img.convert("RGB")

    palette_image = Image.new("P", img.size)
    palette_image.putpalette(ALL_COLORS)
    new_image = img.quantize(palette=palette_image,
                             dither=0 if input("Dither Image? [y/n] ").strip() == "n" else 1).convert("RGB")

    print("Opening the dithered image")
    new_image.show()

    return new_image


img, img_path = get_image()
img = quantize(img)

path = img_path[::-1].split(".")
path.insert(1, "derehtid")
path = ".".join(path)
path = path[::-1]

img.save(path)
print("Image saved to '", path, "'")
