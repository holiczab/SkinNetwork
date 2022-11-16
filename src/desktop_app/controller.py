import tkinter.messagebox

from main_window import MainWindow
from model import Model
from PIL import ImageTk, Image
from ttkbootstrap.constants import *


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
        self.view.report_btn.configure(command=self.__generate_report_button_clicked)

    def __upload_button_clicked(self) -> None:
        """
        Handles the upload button clicked event.

        :return: None
        """

        path = self.view.open_file_dialog()
        if path != "":
            opened_image = self.model.open_image(path)
            self.view.show_image(opened_image)

            self.view.progress_bar_thread = self.view.start_progressbar_on_thread()

            self.model.send_data(self.model.image)  # Comment it until Zsombor is not ready

            if self.model.result is not None:
                # Successful classification
                # Result ought to be a json. (for details ask Zsombor)

                self.view.more_btn.configure(state=NORMAL)
                self.view.report_btn.configure(state=NORMAL)
                pass
            else:
                # Error popup or something
                self.view.more_btn.configure(state=DISABLED)
                self.view.report_btn.configure(state=DISABLED)
                pass
            # self.view.stop_progressbar(self.view.progress_bar_thread)

    def __more_info_button_clicked(self):
        pass

    def __generate_report_button_clicked(self) -> None:
        """
        Handles the report generation button clicked event.

        :return: None
        """

        path = self.view.save_file_dialog()
        if path != "":
            # TODO: set right parameters here
            success = self.model.save_report(path, self.model.path, 2, 60, lang="hu")
            if success:
                tkinter.messagebox.showinfo(
                    parent=self.view,
                    title="Success",
                    message="PDF Report generated successfully!"
                )
            else:
                tkinter.messagebox.showerror(
                    parent=self.view,
                    title="Error",
                    message="Could not generate PDF Report!"
                )

    def __update_labels(self, result: str, confidence: int) -> None:
        """
        Updates the feedback widgets on the main window.

        :param result: name of the disease
        :param confidence: confidence oof the classification
        :return: None
        """

        result = self.model.result  # json-like data
        self.view.result_label.configure(text="Eredmény:\n{}".format(result))
        self.view.prob_meter.configure(amountused=confidence * 100)

        if confidence >= 0.9:
            bootstyle = "danger"
        elif 0.8 <= confidence < 0.9:
            bootstyle = "warning"
        else:
            bootstyle = "success"

        self.view.result_label["bootstyle"] = "{}-outline-toolbutton".format(bootstyle)
        self.view.prob_meter["bootstyle"] = bootstyle
