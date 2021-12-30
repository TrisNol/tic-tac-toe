from PyQt5.QtWidgets import QApplication
import sys
from visual.mainwindow import Window

App = QApplication(sys.argv)

windowMain = Window()

sys.exit(App.exec())
