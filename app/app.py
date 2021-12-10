from PyQt5.QtWidgets import *
import sys
from Visual import MainWindow

# create pyqt5 app
App = QApplication(sys.argv)

# Erstelle die Instanz für das Hauptfenster
windowMain = MainWindow.Window()

# start the app
sys.exit(App.exec())
