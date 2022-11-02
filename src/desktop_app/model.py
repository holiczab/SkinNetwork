import _io

import numpy as np
from PIL import ImageTk, Image
import requests as rqs
import base64
import json
import sys


class Model:
    """
    Class for handling data, and communication.

    """
    def __init__(self) -> None:
        """
        Constructor of Model. # Could get parameters from the main app, like server address, etc.

        return None
        """
        self.path = ""
        self.image = ImageTk.PhotoImage
        self.result = {}
        self.links = {}

    def send_data(self, opened_image) -> None:
        """
        Sending the data to the server. Needs to be public, because it's called in open_image()

        :param opened_image: The image opened in open_image() with the built-in function open()
        :return: Currently None, could change if we get an acknowledgement/result from server
        """
        fh = {"image": opened_image}
        address = "http://127.0.0.1:8080"
        resp = rqs.get(address, files=fh, headers={"client": "desktop"})
        # wait_for_result

    def __wait_for_result(self) -> bool:
        pass

    def __open_image(self, input_path: str) -> ImageTk.PhotoImage:
        """
        Opens image. First for sending the data, second, for visualising it. # Might change later

        :param input_path: Path to the file
        :return: The PIL image for the View
        """
        with open(input_path) as img:
            self.send_data(img)

        with Image.open(input_path) as img:
            self.image = img
            self.image.thumbnail((600, 600), Image.ANTIALIAS)
            return ImageTk.PhotoImage(self.image)

    def __save_report(self, path: str) -> bool:
        """
        Saving the report.

        :param path: Output path
        :return: Success
        """
        pass
