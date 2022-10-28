import os
import time
import threading

import tkinter as tk
import ttkbootstrap as ttk

from typing import Union
from PIL import ImageTk, Image
from tkinter import filedialog as fd
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification


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

        self.source_image = None
        self.displayed_img = None
        self.window_width = None
        self.window_height = None
        self.progress_bar_thread = None

        self.__set_main_window_properties()
        self.__initialize_and_configure_components()
        self.__place_components()

    # Public non-static methods
    def show(self) -> None:
        """
        Displays the main window.

        :return: None
        """

        input_path = "./pics/birthmark.jpg"
        self.show_image(input_path)
        self.progress_bar_thread = self.start_progressbar_on_thread()
        self.mainloop()

    def start_progressbar_on_thread(self) -> threading.Thread:
        """
        Creates and starts a new thread for the progressbar.

        :return: None
        """

        process_thread = threading.Thread(target=self.start_progressbar, daemon=True)
        process_thread.start()

        return process_thread

    def start_progressbar(self) -> None:
        """
        Starts the progressbar in indeterminate mode.

        :return: None
        """

        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start(25)

    def stop_progressbar(self, thread: threading.Thread) -> None:
        """
        Stops the progressbar and waits for the thread to finish.

        :param thread: thread of the progressbar
        :return: None
        """

        self.progress_bar.stop()
        thread.join()
        self.progress_bar.configure(value=0, mode="determinate")

    def show_image(self, input_path: str) -> None:
        """
        Displays an image in the middle section of the main window.

        :param input_path: path of image
        :return: None
        """

        with Image.open(input_path) as img:
            self.source_image = img
            self.source_image.thumbnail((600, 600), Image.ANTIALIAS)

        self.displayed_img = ImageTk.PhotoImage(self.source_image)
        self.img_frame.configure(image=self.displayed_img)

    def open_file_dialog(self) -> str:
        """
        Handles the file opening with an Open File Dialog.

        :return: path of opened file
        """

        filetypes = (
            ("JPG files", "*.jpg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        )

        filename = fd.askopenfilename(
            parent=self,
            title="Open file",
            initialdir="../",
            filetypes=filetypes,
        )

        return filename

    def open_report_dialog(self):
        pass

    # Private non-static methods
    def __set_main_window_properties(self) -> None:
        """
        Sets the properties of the main window.

        :return: None
        """

        self.title("SkinNetwork")
        self.minsize(1280, 720)
        self.place_window_center()

    def __initialize_and_configure_components(self) -> None:
        """
        Initializes and configures the components on the main window.

        :return: None
        """

        # Main window
        self.configure(padx=30, pady=30)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

        # Three sections of the UI
        self.frame_left = ttk.Labelframe(master=self, text="-")
        self.frame_middle = ttk.Labelframe(master=self, text="-")
        self.frame_right = ttk.Labelframe(master=self, text="-")

        self.frame_left["bootstyle"] = "primary"
        self.frame_middle["bootstyle"] = "primary"
        self.frame_right["bootstyle"] = "primary"

        # Components in the section on the left
        logo_img_path = os.path.join(os.getcwd(), "pics/logo_2.png")
        self.logo_img = ImageTk.PhotoImage(Image.open(logo_img_path).resize((200, 200)))

        upload_img_path = os.path.join(os.getcwd(), "pics/upload.png")
        self.upload_img = ImageTk.PhotoImage(Image.open(upload_img_path).resize((64, 64)))

        self.logo_img_frame = ttk.Label(master=self.frame_left)
        self.upload_frame = ttk.Frame(master=self.frame_left, padding=5)

        self.upload_img_frame = ttk.Label(master=self.upload_frame)
        self.upload_btn = ttk.Button(master=self.upload_frame, text="Kép feltöltése...")

        self.logo_img_frame.configure(image=self.logo_img)
        self.upload_img_frame.configure(image=self.upload_img)

        self.upload_btn["bootstyle"] = "primary"

        # Components in the section in the middle
        self.img_frame = ttk.Label(master=self.frame_middle)

        self.progress_bar = ttk.Progressbar(master=self.frame_middle, mode="determinate")

        self.progress_bar["bootstyle"] = "primary"

        # Components in the section on the right
        self.result_frame = ttk.Frame(master=self.frame_right, padding=10)

        self.result_label = ttk.Checkbutton(
            master=self.result_frame,
            text="Eredmény:\nMelanoma",
            variable=ttk.IntVar(value=1),
            onvalue=1,
            offvalue=1
        )

        self.prob_meter = ttk.Meter(
            master=self.result_frame,
            metertype="semi",
            textright="%",
            subtext="Bizonyosság",
            interactive=False,
            amountused=96,
            amounttotal=100,
        )

        self.more_frame = ttk.Frame(master=self.frame_right, padding=5)

        self.more_btn = ttk.Button(master=self.more_frame, text="Több információ...")
        self.report_btn = ttk.Button(master=self.more_frame, text="Jelentés generálása...")

        self.result_label["bootstyle"] = "danger-outline-toolbutton"
        self.prob_meter["bootstyle"] = "danger"

        # self.prob_meter.configure(amountused=56)
        # self.prob_meter["bootstyle"] = "success"
        # self.result_label["bootstyle"] = "success-outline-toolbutton"
        #
        # self.prob_meter.configure(amountused=81)
        # self.prob_meter["bootstyle"] = "warning"
        # self.result_label["bootstyle"] = "warning-outline-toolbutton"

        self.more_btn["bootstyle"] = "primary"
        self.report_btn["bootstyle"] = "primary"

    def __place_components(self) -> None:
        """
        Places the components on the main window.

        :return: None
        """

        # Three sections of the UI
        self.frame_left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.frame_middle.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frame_right.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        # Components in the section on the left
        self.logo_img_frame.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)
        self.upload_frame.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)
        self.upload_img_frame.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)
        self.upload_btn.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)

        # Components in the section in the middle
        self.img_frame.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)
        self.progress_bar.pack(side=TOP, expand=NO, padx=5, pady=5, fill=X)

        # Components in the section on the right
        self.result_frame.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)
        self.result_label.pack(side=TOP, expand=YES, padx=5, pady=5, fill=X)
        self.prob_meter.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)
        self.more_frame.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)
        self.more_btn.pack(side=TOP, expand=YES, padx=5, pady=5, fill=X)
        self.report_btn.pack(side=TOP, expand=YES, padx=5, pady=5, fill=X)
