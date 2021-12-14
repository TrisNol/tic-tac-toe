import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from Analysis import Analysis


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100, fig=None):
        super(MplCanvas, self).__init__(fig)

class AnalysisWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.analysis = Analysis()

        self.build_layout()

    def build_layout(self):
        self.setFixedSize(640, 480)
        layout = QVBoxLayout()
        self.label = QLabel("Game Analysis")
        layout.addWidget(self.label)

        frame = self.analysis.get_frame()
        win_relation = self.analysis.get_player_win_relation(frame)
        print(win_relation)
        sc = MplCanvas(self, width=5, height=4, dpi=100, fig=self.analysis.draw_win_pie(win_relation))

        self.setLayout(layout)
        layout.addWidget(sc)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.w = AnalysisWindow()

    def show_new_window(self):
        self.w.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
w.show_new_window()
app.exec()
