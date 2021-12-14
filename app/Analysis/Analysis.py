
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import sys 

# Adds higher directory to python modules path.
sys.path.append("..") 
from utils.DB import DB


class Analysis():

    def __init__(self):
        self.db = DB()
        self.frame = pd.DataFrame(self.db.get_entries())

    def get_frame(self):
        return pd.DataFrame(self.db.get_entries())

    def get_player_win_relation(self, frame):
        # get the last turn --> won or draw ?
        who_won = pd.DataFrame([turn[-1] for turn in frame.turns])
        # latest_turn == True indicates that the current player won with this move
        player_one_wins = who_won[(who_won.player_id == 0) &
                                  (who_won.latest_turn == True)]
        player_two_wins = who_won[(who_won.player_id == 1) &
                                  (who_won.latest_turn == True)]
        draws = who_won[who_won.latest_turn == False]
        return {
            'player_one_won': len(player_one_wins),
            'player_two_won': len(player_two_wins),
            'draws': len(draws)
        }

    def draw_win_pie(self, data):
        # https://stackoverflow.com/questions/44076203/getting-percentages-in-legend-from-pie-matplotlib-pie-chart
        plt.pie(data.values(), autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        labels = [f'{key}: {value}' for key, value in data.items()]
        plt.legend(loc='best', labels=labels)
        # plt.show()
        # return plt.figure()
        return plt.gcf()

    def avg_game_len(self, df):
        date_format = "%d.%m.%Y %H:%M:%S"
        date_diff = []
        for index, row in df.iterrows():
            diff = datetime.strptime(
                row.end_time, date_format) - datetime.strptime(row.start_time, date_format)
            date_diff.append(diff)
        df['game_len'] = date_diff
        game_len_avg = df['game_len'].mean()
        return game_len_avg


    def avg_turns(self, df):
        return np.mean([len(x) for x in df.turns.values])

if __name__ == '__main__':
    temp = Analysis()
    print(temp.frame.columns)
