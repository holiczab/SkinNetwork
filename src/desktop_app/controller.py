import threading
import webbrowser
import tkinter.messagebox

from model import Model
from main_window import MainWindow
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

        self.__view = view
        self.__model = model

        self.__bind_commands()

    # Public non-static methods
    def mainloop(self) -> None:
        """
        The main loop of the application.

        :return: None
        """

        self.__view.show()

    # Private non-static methods
    def __bind_commands(self) -> None:
        """
        Binds all commands to the components on the main window.

        :return: None
        """

        self.__view.upload_btn.configure(command=self.__upload_button_clicked)
        self.__view.more_btn.configure(command=self.__more_info_button_clicked)
        self.__view.report_btn.configure(command=self.__generate_report_button_clicked)

    def __upload_button_clicked(self) -> None:
        """
        Handles the upload button clicked event.

        :return: None
        """

        path = self.__view.open_file_dialog()
        if path != "":
            opened_image = self.__model.open_image(path)
            self.__view.show_image(opened_image)

            self.__start_process()

    def __start_process(self) -> None:
        """
        Creates and starts a new thread for the process.

        :return: None
        """

        process_thread = threading.Thread(target=self.__process, daemon=True)
        process_thread.start()

    def __process(self) -> None:
        """
        The main process.

        :return: None
        """

        self.__view.upload_btn.configure(state=DISABLED)
        self.__view.progress_bar.configure(mode="indeterminate")
        self.__view.progress_bar.start(25)

        self.__reset_results()

        self.__model.send_data(self.__model.image)

        if self.__model.result is not None:
            # Successful classification
            # Result ought to be a json. (for details ask Zsombor)

            prediction = self.__model.result["prediction"]
            probability = self.__model.result["probability"]

            self.__update_labels(prediction, probability)

            self.__view.more_btn.configure(state=NORMAL)
            self.__view.report_btn.configure(state=NORMAL)
        else:
            # Error popup
            tkinter.messagebox.showerror(
                parent=self.__view,
                title="Hiba!",
                message="Nem sikerült az azonosítás!"
            )

        self.__view.progress_bar.stop()
        self.__view.progress_bar.configure(value=0, mode="determinate")
        self.__view.upload_btn.configure(state=NORMAL)

    def __more_info_button_clicked(self) -> None:
        """
        Opens a new tab in browser and searches for prediction result.

        :return: None
        """

        prediction = self.__model.result["prediction"]
        url = "https://www.google.com/search?q={}".format(prediction)
        webbrowser.open_new_tab(url)

    def __generate_report_button_clicked(self) -> None:
        """
        Handles the report generation button clicked event.

        :return: None
        """

        path = self.__view.save_file_dialog()
        if path != "":
            prediction = self.__model.result["prediction"]
            probability = int(self.__model.result["probability"] * 100)
            success = self.__model.save_report(path, self.__model.path, prediction, probability, lang="hu")
            if success:
                tkinter.messagebox.showinfo(
                    parent=self.__view,
                    title="Siker!",
                    message="A PDF riport létrehozása sikeres!"
                )
            else:
                tkinter.messagebox.showerror(
                    parent=self.__view,
                    title="Hiba!",
                    message="A PDF riport létrehozása sikertelen!"
                )

    def __update_labels(self, prediction: str, confidence: float) -> None:
        """
        Updates the feedback widgets on the main window.

        :param prediction: name of the disease
        :param confidence: confidence oof the classification
        :return: None
        """

        self.__view.result_label.configure(text="Eredmény:\n{}".format(prediction))
        self.__view.prob_meter.configure(amountused=int(confidence * 100))

        if confidence >= 0.9:
            bootstyle = "danger"
        elif 0.8 <= confidence < 0.9:
            bootstyle = "warning"
        else:
            bootstyle = "success"

        self.__view.result_label["bootstyle"] = "{}-outline-toolbutton".format(bootstyle)
        self.__view.prob_meter["bootstyle"] = bootstyle

    def __reset_results(self) -> None:
        """
        Resets the result labels and disables the buttons on the right side of the window.

        :return: None
        """

        self.__view.result_label.configure(text="Eredmény:\n")
        self.__view.result_label["bootstyle"] = "primary-outline-toolbutton"
        self.__view.prob_meter["bootstyle"] = "primary"
        self.__view.prob_meter.configure(amountused=0)
        self.__view.more_btn.configure(state=DISABLED)
        self.__view.report_btn.configure(state=DISABLED)
