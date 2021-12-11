
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from utils.DB import DB
import pandas as pd

class Analysis():

    def __init__(self):
        self.db = DB()
        self.frame = pd.DataFrame(self.db.get_entries())

    def get_player_win_relation(self):
        

if __name__  == '__main__':
    temp = Analysis()
    print(temp.frame.columns)