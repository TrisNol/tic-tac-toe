import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget


class AnalysisWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.db = DB()

        self.build_layout()

    def build_layout(self):
        self.setFixedSize(640, 480)
        layout = QVBoxLayout()
        self.label = QLabel("Game Analysis")
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.w = AnalysisWindow()
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

    def show_new_window(self, checked):
        self.w.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
