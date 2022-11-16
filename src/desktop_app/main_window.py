import os

import ttkbootstrap as ttk

from PIL import ImageTk, Image
from tkinter import filedialog as fd
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

        self.source_image = None
        self.displayed_img = None
        self.window_width = None
        self.window_height = None

        self.__set_main_window_properties()
        self.__initialize_and_configure_components()
        self.__place_components()

    # Public non-static methods
    def show(self) -> None:
        """
        Displays the main window.

        :return: None
        """

        self.mainloop()

    def show_image(self, image_to_open: ImageTk.PhotoImage):
        """
        Displays the image contained in Model

        :param image_to_open: image to open
        :return:
        """
        self.displayed_img = image_to_open
        self.img_frame.configure(image=self.displayed_img)

    def open_file_dialog(self) -> str:
        """
        Handles the user interaction to open a file with an Open File Dialog.

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

    def save_file_dialog(self) -> str:
        """
        Handles the user interaction to save a file with a Save File Dialog.

        :return: output path
        """

        filetypes = (
            ("PDF files", "*.pdf"),
            ("All files", "*.*")
        )

        path = fd.asksaveasfilename(
            parent=self,
            title="Save file",
            initialdir="../",
            filetypes=filetypes,
            defaultextension="pdf"
        )

        return path

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
        logo_img_path = os.path.join(os.getcwd(), "resources/pics/logo.png")
        self.logo_img = ImageTk.PhotoImage(Image.open(logo_img_path).resize((200, 200)))

        upload_img_path = os.path.join(os.getcwd(), "resources/pics/upload.png")
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
            text="Eredmény:\n",
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
            amountused=0,
            amounttotal=100,
        )

        self.more_frame = ttk.Frame(master=self.frame_right, padding=5)

        self.more_btn = ttk.Button(master=self.more_frame, text="Több információ...", state=DISABLED)
        self.report_btn = ttk.Button(master=self.more_frame, text="Jelentés generálása...", state=DISABLED)

        self.result_label["bootstyle"] = "primary-outline-toolbutton"
        self.prob_meter["bootstyle"] = "primary"

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
