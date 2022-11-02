from main_window import MainWindow
from model import Model


class Controller(object):
    """
    Class for controlling the application.

    """

    def __init__(self, view: MainWindow, model: Model) -> None:
        """
        Constructor of the Controller class.

        :param view: an instance of MainWindow
        :param model: an instance of Model
        :return: None
        """

        super(Controller, self).__init__()

        self.view = view
        self.model = model
        self.__bind_commands()

    # Public non-static methods
    def mainloop(self) -> None:
        """
        The main loop of the application.

        :return: None
        """

        self.view.show()

    # Private non-static methods
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
        if path != "":
            # self.view.show_image(path)
            self.view.show_image_file(self.model.open_image(path))
        # self.view.stop_progressbar(self.view.thread)

    def __more_info_button_clicked(self):
        pass

    def __generate_report_button_clicked(self) -> None:
        """
        Handles the report generation button clicked event.

        :return: None
        """

        path = self.view.open_report_dialog()
        if path != "":
            self.model.save_report(path)
            # Could do: self.view.report_generated_successfully_popup

    def __update_labels(self, result: str, confidence: int) -> None:
        """
        Updates the feedback widgets on the main window.

        :param result: name of the disease
        :param confidence: confidence oof the classification
        :return: None
        """

        result = self.model.result  # json-like data
        self.view.result_label.configure(text="Result:\n{}".format(result))
        self.view.prob_meter.configure(amountused=confidence * 100)

        if confidence >= 0.9:
            bootstyle = "danger"
        elif 0.8 <= confidence < 0.9:
            bootstyle = "warning"
        else:
            bootstyle = "success"

        self.view.result_label["bootstyle"] = bootstyle
        self.view.prob_meter["bootstyle"] = bootstyle
