import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5 import QtCore, QtGui

from lab_02.mpl_canvas import MyMplCanvas
from lab_02.ui.graph_window_ui import Ui_GraphWindow
from math import *


class MainWindow(QMainWindow, Ui_GraphWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.mpl_widget = MyMplCanvas(self)
        plot_box = QVBoxLayout()
        plot_box.addWidget(self.mpl_widget.canvas)
        self.graph_widget.setLayout(plot_box)
        self.progressBar.setVisible(False)

        self.build_graph.clicked.connect(self.run)

    def run(self):
        a = self.start_edit.text()
        b = self.end_edit.text()
        h = self.step_edit.text()
        try:
            f_x_text = self.func_edit.text()
            f_x = lambda x: eval(self.func_edit.text())
        except SyntaxError:
            return
        except ValueError:
            return

        self.mpl_widget.plot_data(float(a), float(b), float(h), f_x, f_x_text)
        # self.mpl_widget.plot_data(-100, 100, 0.1, lambda x: x**3, 'x**3')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
