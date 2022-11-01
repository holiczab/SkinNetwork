from controller import Controller
from main_window import MainWindow
from ttkbootstrap.utility import enable_high_dpi_awareness
from model import Model

if __name__ == "__main__":
    enable_high_dpi_awareness(root=None, scaling=1.8)

    view = MainWindow(theme_name="lumen")
    model = Model()
    controller = Controller(view, model)

    controller.mainloop()
