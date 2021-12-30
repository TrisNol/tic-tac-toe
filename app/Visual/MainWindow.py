from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from random import randint

from logic import gamemaster
from visual import gamewindow, scoreboard
from analysis.analysiswindow import AnalysisWindow
from model.game import Game
from ai.random import Random
from ai.statistic import Statistic
from ai.minimax import MiniMax
from utils.db import DB
from datetime import datetime

class Window(QMainWindow):
    master = None
    def __init__(self):
        super().__init__()
        self.game = Game()  
        self.start = False
        self.game_window = None  
        self.ki_enabled = False 
        self.ai = {'enabled': False, 'ai': None}
        self.scoreboard = None
        self.setStyleSheet("background-color: grey;")
        self.helper = None

        self.setWindowTitle("TicTacToe")
        self.setGeometry(100, 100,
                         300, 800)  
       
        self.ui_components()
        self.show()

    
    def ui_components(self):
        """Initialize UI elements on the window"""
        self.label = QLabel(self)
        self.label.setGeometry(20, 450, 260, 60)
        self.label.setStyleSheet("QLabel"
                                 "{"
                                 "border : 3px solid black;"
                                 "background : white;"
                                 "}")

        # setting label alignment
        self.label.setAlignment(Qt.AlignCenter)

        # setting font to the label
        self.label.setFont(QFont('Times', 15))
        exit_game = QPushButton("Exit", self)

        # setting geometry
        exit_game.setGeometry(50, 700, 200, 50)  # (X, Y, width, hight)
        exit_game.setStyleSheet('background-color: red')

        # adding action action to the reset push button
        exit_game.clicked.connect(self.exit_game_action)
        self.start_game = QPushButton("Start", self)

        # setting geometry
        self.start_game.setGeometry(50, 550, 200, 50) 
        self.start_game.setStyleSheet('background-color: green')

        # adding action action to the reset push button
        self.start_game.clicked.connect(self.start_game_action)

        self.open_scoreboard = QPushButton("Scoreboard", self)
        self.open_scoreboard.setGeometry(
            50, 650, 200, 50)  
        self.open_scoreboard.setStyleSheet('background-color: yellow')
        self.open_scoreboard.clicked.connect(self.show_scoreboard)

        self.label_player1 = QLabel(self)
        self.show_analysis = QPushButton("Analysis", self)
        self.show_analysis.setGeometry(
            50, 600, 200, 50)  
        self.show_analysis.setStyleSheet('background-color: orange')

        # adding action action to the reset push button
        self.show_analysis.clicked.connect(self.show_analysis_action)

        self.label_player1 = QLabel(self)
        self.label_player1.setText('Player 1')
        self.label_player1.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.label_player1.setFont(QFont('Arial', 16))

        self.label_player2 = QLabel(self)
        self.label_player2.setText('Player 2')
        self.label_player2.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.label_player2.setFont(QFont('Arial', 16))

        self.playername1 = QLineEdit(self)  
        self.playername1.setText('Player 1')
        self.playername1.setFont(QFont('Arial', 12))
        self.playername1.setStyleSheet('background: lightblue')

        self.game.name_player1 = 'Player 1'
        self.select_sign1 = QComboBox(self)
        self.select_sign1.setFont(QFont('Arial', 20))
        self.select_sign1.setStyleSheet('background: lightgrey')
        # ------------------------------------------------
        # Dropdown for mode 3x3 - 4x4 - 5x5
        # ------------------------------------------------
        self.label_gamemode = QLabel(self)
        self.label_gamemode.setText('mode')
        self.label_gamemode.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.label_gamemode.setFont(QFont('Arial', 16))

        # Create DropDown Object 
        self.gamemode = QComboBox(self)
        self.gamemode.setFont(QFont('Arial', 16))
        self.gamemode.setStyleSheet('background: lightgrey')
        self.gamemode.addItem('')
        self.gamemode.addItem('3x3')
        self.gamemode.addItem('4x4')
        self.gamemode.addItem('5x5')
        self.gamemode.currentTextChanged.connect(self.conditional_render_player_help)

        self.helper_check_box = QCheckBox(self)
        self.helper_check_box.setText("Player 1 helper")
        self.helper_check_box.setToolTip("If this checkbox is checked, Player 1 will get hints to play succesful.\n Only available in the 3x3 game mode")

        self.ai_modes = {'1 vs 1': {"enabled": False, "ai": None},
                        '1 vs Random': {"enabled": True, "ai": Random()},
                        '1 vs Statistic': {"enabled": True, "ai": Statistic()},
                        '1 vs MiniMax': {"enabled": True, "ai": MiniMax()}
                        }
        self.ai_mode = QComboBox(self)
        self.ai_mode.setFont(QFont('Arial', 16))
        self.ai_mode.setStyleSheet('background: lightgrey')
        self.ai_mode.addItem('1 vs 1')
        self.ai_mode.addItem('1 vs Random')
        self.ai_mode.addItem('1 vs Statistic')
        self.ai_mode.addItem('1 vs MiniMax')
       
        self.playername2 = QLineEdit(self)  
        self.playername2.setText('Player 2')
        self.playername2.setFont(QFont('Arial', 12))
        self.playername2.setStyleSheet('background: yellow')

        self.game.name_player2 = 'Player 2'
        self.select_sign2 = QComboBox(self)
        self.select_sign2.setFont(QFont('Arial', 20))
        self.select_sign2.setStyleSheet('background: lightgrey')
    
        self.sign_array = ['', 'X', 'O', 'Ø', '@', '!', '?']

        for x in range(len(self.sign_array)):
            self.select_sign1.addItem(self.sign_array[x])
            self.select_sign2.addItem(self.sign_array[x])

        # Placing GUI elements
        self.label_player1.setGeometry(30, 10, 100, 35)
        self.playername1.setGeometry(30, 45, 100, 35)

        
        self.select_sign1.setGeometry(30, 80, 100, 35)

        self.label_player2.setGeometry(180, 10, 100, 35)
        self.select_sign2.setGeometry(180, 80, 100, 35)
        self.playername2.setGeometry(180, 45, 100, 35)

        self.label_gamemode.setGeometry(100, 130, 100, 35)
        self.gamemode.setGeometry(100, 170, 100, 35)
        self.helper_check_box.setGeometry(70, 260, 200,35)
        self.ai_mode.setGeometry(75, 210, 150, 35)

        self.select_sign1.activated[str].connect(self.sign_changed1)
        self.select_sign2.activated[str].connect(self.sign_changed2)
        self.playername1.textChanged.connect(self.textchangedPlayer1)
        self.playername2.textChanged.connect(self.textchangedPlayer2)
        self.gamemode.activated[str].connect(self.gamemode_changed)
        self.ai_mode.activated[str].connect(self.ai_changed)

    def change_ai(self):
        """Changes the AI to the selected one"""
        if self.ki_button.isChecked():
            self.ki_button.setStyleSheet('background-color: lightblue')
            self.ki_button.setText('1 vs KI')
            self.playername2.setText('KI')
            self.playername2.setEnabled(False)
            self.select_sign2.setEnabled(False)
            self.select_sign2.addItem('©')  
            self.select_sign2.setCurrentText('©')
            self.game.sign_player2 = '©'
            self.ki_enabled = True
        else:
            self.ki_button.setStyleSheet('background-color: lightgrey')
            self.ki_button.setText('1 vs 1')
            self.select_sign2.removeItem(7)
            self.select_sign2.setEnabled(True)
            self.select_sign2.setCurrentIndex(0)
            self.playername2.setText('Player 2')
            self.playername2.setEnabled(True)
            self.game.sign_player2 = ""
            self.ki_enabled = False

    def gamemode_changed(self, s):
        """Changes the boardsize"""  
        print('gamemode changed to: ', s)
        if s == '3x3':
            self.game.size = 3
        elif s == '4x4':
            self.game.size = 4
        elif s == '5x5':
            self.game.size = 5
        else:
            self.game.size = 0

    def close_game(self):
        """resets the variables and fields"""
        self.game_window = None
        # resetting values
        sign1_tmp = self.game.sign_player1
        sign2_tmp = self.game.sign_player2
        name1_tmp = self.game.name_player1
        name2_tmp = self.game.name_player2
        size_tmp = self.game.size

        self.game = Game()

        self.game.sign_player1 = sign1_tmp
        self.game.sign_player2 = sign2_tmp
        self.game.name_player1 = name1_tmp
        self.game.name_player2 = name2_tmp
        self.game.size = size_tmp

        self.select_sign1.setEnabled(True)
        self.select_sign2.setEnabled(True)
        self.playername1.setEnabled(True)
        self.select_sign2.setEnabled(True)
        self.playername2.setEnabled(True)
        self.gamemode.setEnabled(True)

        self.ai_mode.setEnabled(True)
        self.start_game.setEnabled(True)
        self.label_player1.setStyleSheet('background: grey')
        self.label_player2.setStyleSheet('background: grey')
        self.label.setText('Game finished')

    def show_game_window(self):
        """Shows the actual game UI"""
        self.initialize_game_class()
        if self.game_window is None:
            self.game_window = gamewindow.GameWindow(
                self.game, self, self.ai['enabled'], self.ai['ai'], self.helper_check_box.isChecked())
        self.game_window.show()

    def show_scoreboard(self):
        """Opens new window with the scoreboard"""
        self.scoreboard = scoreboard.Scoreboard()
        if self.scoreboard is None:
            self.scoreboard = scoreboard.Scoreboard()
        self.scoreboard.show()

    def show_analysis_action(self):
        """Opens new window with the analysis pie-chart"""
        self.analysis_window = AnalysisWindow(self)
        self.analysis_window.show()

    def textchangedPlayer1(self, s):  
        """Helperfunction: asiigns variable to the value from field"""
        self.game.name_player1 = s

    def textchangedPlayer2(self, s): 
        """Helperfunction: asigns variable to the value from field"""
        self.game.name_player2 = s

    def sign_changed1(self, s):  
        """Helperfunction: asigns variable to the value from field"""
        sign_tmp = self.game.sign_player1
        self.game.sign_player1 = s
        if sign_tmp:
            index = self.sign_array.index(sign_tmp)
            self.select_sign2.insertItem(index, sign_tmp)
        self.select_sign2.removeItem(self.select_sign2.findText(s))

    def sign_changed2(self, s): 
        """Helperfunction: asigns variable to the value from field"""
        sign_tmp = self.game.sign_player2
        self.game.sign_player2 = s

        if sign_tmp:
            index = self.sign_array.index(sign_tmp)
            self.select_sign1.insertItem(index, sign_tmp)
        self.select_sign1.removeItem(self.select_sign1.findText(s))

    def ai_changed(self, mode):
        """Helperfunction: asigns ai to the selected value"""
        self.ai = self.ai_modes[mode]
        if self.ai['enabled']:
            self.playername2.setEnabled(False)
            self.select_sign2.setEnabled(False)
            self.select_sign2.addItem('©')  
            self.select_sign2.setCurrentText('©')
            self.game.sign_player2 = '©'
        else:
            self.playername2.setEnabled(True)
            self.select_sign2.setEnabled(True)
        print(self.ai)

    def start_game_action(self):  
        """Starts the game and disables all config fields"""
        if self.game.sign_player1 == '':
            self.label.setFont(QFont('Arial', 10))
            self.label.setStyleSheet('background: red')
            self.label.setText('Error Player 1: no sign selected')
            return
        elif self.game.sign_player2 == '':
            self.label.setStyleSheet('background: red')
            self.label.setFont(QFont('Arial', 10))
            self.label.setText('Error Player 2: no sign selected')
            return
        elif self.game.size == 0:
            self.label.setStyleSheet('background: red')
            self.label.setFont(QFont('Arial', 10))
            self.label.setText('Error mode: no mode selected')
            return

        self.select_sign1.setEnabled(False)
        self.playername1.setEnabled(False)
        self.select_sign2.setEnabled(False)
        self.playername2.setEnabled(False)
        self.gamemode.setEnabled(False)
        self.ai_mode.setEnabled(False)
        self.start_game.setEnabled(False)
        self.start = True
        self.label.setStyleSheet('background: white')
        self.label.setFont(QFont('Arial', 16))
        self.label.setText('Game started')
        self.show_game_window()

    def exit_game_action(self): 
        """Closes the programm"""
        sys.exit() 

    def initialize_game_class(self):
        """Connects to database"""
        self.DB = DB()
        self.game.id = self.DB.get_amount_off_documents()
        now = datetime.now()
        self.game.start_time = now.strftime("%d.%m.%Y %H:%M:%S")

    def conditional_render_player_help(self, selected_mode):
        """Shows a helper checkbox on 3x3"""
        if selected_mode == '3x3':
            self.helper_check_box.show()
        else:
            self.helper_check_box.setChecked(False)
            self.helper_check_box.hide()