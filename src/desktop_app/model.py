import numpy as np
from PIL import ImageTk, Image
import base64
import json
import sys


class Model:
    def __init__(self):
        self.path = ""
        self.image = ImageTk.PhotoImage
        self.numpy_image = np.zeros((1,1))
        self.result = {}
        self.links = {}

    def send_data(self, image: ImageTk.PhotoImage) -> None:
        pass

    def wait_for_result(self) -> bool:
        pass

    def open_image(self, input_path: str) -> ImageTk.PhotoImage:
        with Image.open(input_path) as img:
            self.image = img
            self.image.thumbnail((600, 600), Image.ANTIALIAS)
            self.numpy_image = np.asarray(img)
            return ImageTk.PhotoImage(self.image)

    def save_report(self, path: str) -> bool:
        pass
