import itertools
import re
import time
import tkinter
from tkinter import filedialog
from typing import List, Tuple, Dict, Callable

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
ALL_COLORS: List[int] = list(itertools.chain(*COLORS))


def get_image() -> Image:
    """
    Open file explorer, wait for user to open an image
    :return: The opened image
    """
    print("Open image ", end="\r")
    root = tkinter.Tk()
    root.withdraw()
    img_path = filedialog.askopenfilename(filetypes=[("Image", ".png .jpg")])
    root.destroy()

    img = Image.open(img_path)
    print("Selected image: ", img_path.split("/")[-1])
    return img, img_path


def quantize(img: Image, dither: int = 1) -> Image:
    """
    Convert the passed image into a predefined color palette

    :param dither: 1 = dither, 0 = not dither
    :param img: The image to be dithered
    :return: THe dithered image
    """
    img = img.convert("RGB")

    palette_image = Image.new("P", img.size)
    palette_image.putpalette(ALL_COLORS)
    new_image = img.quantize(palette=palette_image,
                             dither=dither).convert("RGB")

    print("Opening final image")
    new_image.show()

    return new_image


def resize(img: Image) -> Image:
    """
    Resize the passed image to the entered dimensions
    :param img: Image to be resized
    :return: Resized image
    """
    m = None
    new_size = (-1, -1)

    print(f"\nOriginal image dimension: {img.width}x{img.height}")

    print("\nHow would you like to scale the image; [enter number]\n"
          "1. Scale to WIDTH & HEIGHT\n"
          "2. Scale uniformly by PERCENTAGE\n"
          "3. Fit to WIDTH\n"
          "4. Fit to HEIGHT")

    while True:
        try:
            scale_method: int = int(re.match(r"(\d+)", input("> ").strip()).group(1))
            break
        except AttributeError:
            print("Enter a number between 1 and 4")

    # Scale to WxH
    if scale_method == 1:
        while not m:
            m = re.match(r"^(\d+)\D+(\d+)$", input("Enter the new image dimensions [WxH]\n> ").strip())
        new_size: Tuple[int, int] = (int(m.group(1)), int(m.group(2)))

    # Scale to Percentage
    if scale_method == 2:
        while not m:
            m = re.match(r"(\d+)", input("Enter the PERCENTAGE of the image dimension [__%]\n> ").strip())
        new_size = int(img.width * float(m.group(1)) / 100), int(img.height * float(m.group(1)) / 100)

    # Fit to Width
    if scale_method == 3:
        while not m:
            m = re.match(r"(\d+)", input("Enter the new image WIDTH\n> ").strip())
        new_size = int(m.group(1)), int(float(m.group(1)) / img.width * img.height)

    # Fit to Height
    if scale_method == 4:
        while not m:
            m = re.match(r"(\d+)", input("Enter the new image HEIGHT\n> ").strip())
        new_size = int(float(m.group(1)) / img.height * img.width), int(m.group(1))

    return img.resize(new_size)


def choose():
    """
    Prompt the player to select a function
    :return: Name of the function [Callable]
    """
    functions: Dict[Callable[[Image], Image], str] = {
        lambda img_: quantize(img_, dither=0): "Convert to RecRoom colors",
        lambda img_: quantize(img_, dither=1): "Convert and Dither to RecRoom colors",
        resize: "Resize image"
    }
    print("\nType the numer in front of the action you wish to perform on the image\n"
          + "\n".join(f"{num}. {name}" for num, name in enumerate(functions.values(), 1)))
    while True:
        selection = input("> ").strip()
        try:
            return list(functions.keys())[int(selection) - 1]
        except (ValueError, TypeError, IndexError):
            pass


def main() -> None:
    """
    Main function that ties all the others together.
    Handles image saving
    """
    while True:
        img, img_path = get_image()
        img = choose()(img)

        path = img_path[::-1].split(".")
        path.insert(1, "wen")
        path = ".".join(path)
        path = path[::-1]

        # Save the image to the same directory as the original, with "dithered" suffix
        img.save(path)
        print("Image saved to '" + path + "'")

        if input("\n1. New image\n2. Exit [Default: Exit]\n> ").find("1") == -1:
            exit()
        time.sleep(0.5)


if __name__ == '__main__':
    main()
