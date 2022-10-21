from main_window import MainWindow


class Controller(object):
    """
    Class for controlling the application.

    """

    def __init__(self, view: MainWindow) -> None:
        """
        Constructor of the Controller class.

        :param view: an instance of MainWindow
        :return: None
        """

        super(Controller, self).__init__()

        self.view = view

        self.__bind_commands()

    def mainloop(self) -> None:
        """
        The main loop of the application.

        :return: None
        """

        self.view.show()

    def __bind_commands(self) -> None:
        """
        Binds all commands to the components on the main window.

        :return: None
        """

        self.view.upload_btn.configure(command=self.__upload_button_clicked)

    def __upload_button_clicked(self) -> None:
        """
        Handles the upload button clicked event.

        :return: None
        """

        path = self.view.open_file_dialog()
        self.view.show_image(path)
        # self.view.stop_progressbar(self.view.thread)

    def __more_info_button_clicked(self):
        pass

    def __generate_report_button_clicked(self):
        pass
