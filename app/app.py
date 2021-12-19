from PyQt5.QtWidgets import *
import sys
from Visual.MainWindow import Window


# create pyqt5 app
App = QApplication(sys.argv)

# Erstelle die Instanz für das Hauptfenster
windowMain = Window()

# start the app
sys.exit(App.exec())
