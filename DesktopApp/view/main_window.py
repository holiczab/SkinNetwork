import tkinter as tk
import ttkbootstrap as ttk


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

        self.__initialize_and_configure_components()
        self.__place_components()

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
        self.btn_1 = ttk.Button(master=self.frame_left, text="First push button")

        # Components in the section in the middle

        # Components in the section on the right
        self.btn_2 = ttk.Button(master=self.frame_right, text="Second push button")

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
        self.btn_1.pack()

        # Components in the section in the middle

        # Components in the section on the right
        self.btn_2.pack()
