from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import numpy as np

class MyMplCanvas(QWidget):
    def __init__(self, parent=None):
        super(MyMplCanvas, self).__init__(parent)
        self.fig = plt.figure()
        plt.style.use('seaborn-whitegrid')
        plt.axis('tight')
        self.canvas = FigureCanvasQTAgg(self.fig)

    def plot_data(self, a, b, h, f_x, f_x_text):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        x = np.arange(a, b, h)
        y = list(map(f_x, x))
        ax.hlines(y=0, xmin=min(x), xmax=max(x), linewidth=1, color='g')
        ax.vlines(x=0, ymin=min(y), ymax=max(y), linewidth=1, color='g')
        plt.title(f_x_text)
        ax.plot(x, y)
        self.canvas.draw()
