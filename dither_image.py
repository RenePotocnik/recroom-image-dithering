import tkinter
from tkinter import filedialog

from PIL import Image


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

    return img


get_image()
