import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QToolTip, QMessageBox, QLabel
 
 
class Leaderboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Leaderboard")