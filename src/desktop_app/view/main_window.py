import os

import tkinter as tk
import ttkbootstrap as ttk

from PIL import ImageTk, Image
from ttkbootstrap.constants import *


class MainWindow(ttk.Window):
    """
    Main Window of the application.

    """

    def __init__(self, theme_name: str) -> None:
        """
        Constructor of the MainWindow class.

        :param theme_name: name of the theme style
        """

        super(MainWindow, self).__init__(themename=theme_name)

        self.__set_main_window_parameters()
        self.__initialize_and_configure_components()
        self.__place_components()

    def load_image(self, input_path: str) -> None:
        """
        Loads an image.

        :param input_path: path of image
        :return: None
        """

        pass

    def __set_main_window_parameters(self) -> None:
        """
        Sets the properties of the main window.

        :return: None
        """

        self.title("SkinNetwork")
        self.minsize(800, 500)

    def __initialize_and_configure_components(self) -> None:
        """
        Initializes and configures the components on the main window.

        :return None:
        """

        # Main window
        self.configure(padx=30, pady=30)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

        # Three sections of the UI
        self.frame_left = ttk.Frame(master=self)
        self.frame_middle = ttk.Frame(master=self)
        self.frame_right = ttk.Frame(master=self)

        self.frame_left["bootstyle"] = "info"
        self.frame_middle["bootstyle"] = "info"
        self.frame_right["bootstyle"] = "info"

        # Components in the section on the left
        logo_img_path = os.path.join(os.getcwd(), "pics/logo.png")
        self.logo_img = ImageTk.PhotoImage(Image.open(logo_img_path).resize((128, 128)))

        upload_img_path = os.path.join(os.getcwd(), "pics/upload.png")
        self.upload_img = ImageTk.PhotoImage(Image.open(upload_img_path).resize((64, 64)))

        self.logo_img_frame = ttk.Label(self.frame_left)
        self.upload_img_frame = ttk.Label(self.frame_left)
        self.upload_btn = ttk.Button(master=self.frame_left, text="Upload...")

        self.logo_img_frame.configure(image=self.logo_img)
        self.upload_img_frame.configure(image=self.upload_img, borderwidth=0)

        self.upload_btn["bootstyle"] = "light"

        # Components in the section in the middle
        self.img_labelframe = ttk.Labelframe(master=self.frame_middle, text="Uploaded image")
        self.img_labelframe.rowconfigure(0, weight=1)
        self.img_labelframe.columnconfigure(0, weight=1)

        self.img_canvas = tk.Canvas(
            master=self.img_labelframe,
            highlightthickness=0,
        )
        self.img_canvas.grid(row=0, column=0, sticky="nsew")

        self.progress_bar = ttk.Progressbar(master=self.frame_middle, value=26)

        self.img_labelframe["bootstyle"] = "dark"
        self.progress_bar["bootstyle"] = "success"

        # Components in the section on the right
        self.prob_meter = ttk.Meter(
            master=self.frame_right,
            metertype="semi",
            textright="%",
            subtext="Confidence",
            interactive=False,
            amountused=96,
        )

        self.more_btn = ttk.Button(master=self.frame_right, text="More info...")
        self.report_btn = ttk.Button(master=self.frame_right, text="Generate report...")

        self.prob_meter["bootstyle"] = "danger"
        self.more_btn["bootstyle"] = "primary"
        self.report_btn["bootstyle"] = "primary"

    def __place_components(self) -> None:
        """
        Places the components on the main window.

        :return: None
        """

        # Three sections of the UI
        self.frame_left.grid(row=0, column=0, sticky="nsew", padx=10)
        self.frame_middle.grid(row=0, column=1, sticky="nsew", padx=10)
        self.frame_right.grid(row=0, column=2, sticky="nsew", padx=10)

        # Components in the section on the left
        self.logo_img_frame.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)
        self.upload_img_frame.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)
        self.upload_btn.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)

        # Components in the section in the middle
        self.img_labelframe.pack(side=TOP, expand=TRUE, padx=5, pady=5, fill=BOTH)
        self.progress_bar.pack(side=TOP, expand=NO, padx=5, pady=5, fill=X)

        # Components in the section on the right
        self.prob_meter.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)
        self.more_btn.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)
        self.report_btn.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)
