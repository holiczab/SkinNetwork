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

        self.__displayed_img = None

        self.__set_main_window_properties()
        self.__initialize_and_configure_components()
        self.__place_components()

    # Properties
    @property
    def upload_btn(self) -> ttk.Button:
        return self.__upload_btn

    @property
    def progress_bar(self) -> ttk.Progressbar:
        return self.__progress_bar

    @property
    def result_label(self) -> ttk.Checkbutton:
        return self.__result_label

    @property
    def prob_meter(self) -> ttk.Meter:
        return self.__prob_meter

    @property
    def more_btn(self) -> ttk.Button:
        return self.__more_btn

    @property
    def report_btn(self) -> ttk.Button:
        return self.__report_btn

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
        self.__displayed_img = image_to_open
        self.__img_frame.configure(image=self.__displayed_img)

    def open_file_dialog(self) -> str:
        """
        Handles the user interaction to open a file with an Open File Dialog.

        :return: path of opened file
        """

        filetypes = (
            ("JPG fájlok", "*.jpg"),
            ("PNG fájlok", "*.png"),
            ("Minden fájl", "*.*")
        )

        filename = fd.askopenfilename(
            parent=self,
            title="Megnyitás",
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
            ("PDF fájlok", "*.pdf"),
            ("Minden fájl", "*.*")
        )

        path = fd.asksaveasfilename(
            parent=self,
            title="Mentés",
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
        self.__frame_left = ttk.Labelframe(master=self, text="-")
        self.__frame_middle = ttk.Labelframe(master=self, text="-")
        self.__frame_right = ttk.Labelframe(master=self, text="-")

        self.__frame_left["bootstyle"] = "primary"
        self.__frame_middle["bootstyle"] = "primary"
        self.__frame_right["bootstyle"] = "primary"

        # Components in the section on the left
        logo_img_path = os.path.join(os.getcwd(), "resources/pics/logo.png")
        self.__logo_img = ImageTk.PhotoImage(Image.open(logo_img_path).resize((200, 200)))

        upload_img_path = os.path.join(os.getcwd(), "resources/pics/upload.png")
        self.__upload_img = ImageTk.PhotoImage(Image.open(upload_img_path).resize((64, 64)))

        self.__logo_img_frame = ttk.Label(master=self.__frame_left)
        self.__upload_frame = ttk.Frame(master=self.__frame_left, padding=5)

        self.__upload_img_frame = ttk.Label(master=self.__upload_frame)
        self.__upload_btn = ttk.Button(master=self.__upload_frame, text="Kép feltöltése...")

        self.__logo_img_frame.configure(image=self.__logo_img)
        self.__upload_img_frame.configure(image=self.__upload_img)

        self.__upload_btn["bootstyle"] = "primary"

        # Components in the section in the middle
        self.__img_frame = ttk.Label(master=self.__frame_middle)

        self.__progress_bar = ttk.Progressbar(master=self.__frame_middle, mode="determinate")

        self.__progress_bar["bootstyle"] = "primary"

        # Components in the section on the right
        self.__result_frame = ttk.Frame(master=self.__frame_right, padding=10)

        self.__result_label = ttk.Checkbutton(
            master=self.__result_frame,
            text="Eredmény:\n",
            variable=ttk.IntVar(value=1),
            onvalue=1,
            offvalue=1
        )

        self.__prob_meter = ttk.Meter(
            master=self.__result_frame,
            metertype="semi",
            textright="%",
            subtext="Bizonyosság",
            interactive=False,
            amountused=0,
            amounttotal=100,
        )

        self.__more_frame = ttk.Frame(master=self.__frame_right, padding=5)

        self.__more_btn = ttk.Button(master=self.__more_frame, text="Több információ...", state=DISABLED)
        self.__report_btn = ttk.Button(master=self.__more_frame, text="Jelentés generálása...", state=DISABLED)

        self.__result_label["bootstyle"] = "primary-outline-toolbutton"
        self.__prob_meter["bootstyle"] = "primary"

        self.__more_btn["bootstyle"] = "primary"
        self.__report_btn["bootstyle"] = "primary"

    def __place_components(self) -> None:
        """
        Places the components on the main window.

        :return: None
        """

        # Three sections of the UI
        self.__frame_left.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)
        self.__frame_middle.grid(row=0, column=1, sticky=NSEW, padx=10, pady=10)
        self.__frame_right.grid(row=0, column=2, sticky=NSEW, padx=10, pady=10)

        # Components in the section on the left
        self.__logo_img_frame.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)
        self.__upload_frame.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)
        self.__upload_img_frame.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)
        self.__upload_btn.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)

        # Components in the section in the middle
        self.__img_frame.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)
        self.__progress_bar.pack(side=TOP, expand=NO, padx=5, pady=5, fill=X)

        # Components in the section on the right
        self.__result_frame.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)
        self.__result_label.pack(side=TOP, expand=YES, padx=5, pady=5, fill=X)
        self.__prob_meter.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)
        self.__more_frame.pack(side=TOP, expand=YES, padx=5, pady=5, fill=NONE)
        self.__more_btn.pack(side=TOP, expand=YES, padx=5, pady=5, fill=X)
        self.__report_btn.pack(side=TOP, expand=YES, padx=5, pady=5, fill=X)
