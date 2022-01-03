
from matplotlib.figure import Figure
from utils.db import DB
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import sys

from pandas.core.frame import DataFrame

# Adds higher directory to python modules path.
sys.path.append("..")


class Analysis():
    """Class containing methods to provide analytics of past Tic-Tac-Toe games that have been recorded in the DB"""

    def __init__(self):
        self.db = DB()
        self.frame = pd.DataFrame(self.db.get_entries())

    def get_frame(self) -> DataFrame:
        """Reads the entries in the DB and returns them as a pandas DataFrame

        Returns:
            DataFrame: Frame containing the entries in the DB
        """
        return pd.DataFrame(self.db.get_entries())

    def get_player_win_relation(self, frame: DataFrame) -> dict:
        """Calculates the win-/loss-relation of player 1 and player 2

        Parameters:
            frame (DataFrame): DataFrame containing the DB entries

        Returns:
            dict: Dictionary listing how often player 1/player 2 won and how often a draw has been played 
            
            (keys: player_one_won, player_two_won, draw).

        """
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
            'draw': len(draws)
        }

    def draw_win_pie(self, data: dict) -> Figure:
        """Constructs a pie-chart of the provided data and returns it

        Parameters:
            data (dict): Dictionary containing the data to be drawn as a pie-chart

        Returns:
            Figure: Pie-chart
        """
        # workaround to fix the chart issues, where old and new chart are stacked --> alternative: fig, axes instead plt
        x = np.array([0])
        y = np.array([1])
        plt.subplot(1,2,1)
        plt.plot(x,y)

        # https://stackoverflow.com/questions/44076203/getting-percentages-in-legend-from-pie-matplotlib-pie-chart
        plt.subplot()
        plt.pie(data.values(), autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        labels = [f'{key}: {value}' for key, value in data.items()]
        plt.legend(loc='best', labels=labels)
        return plt.gcf()

    def avg_game_len(self, df: DataFrame) -> timedelta:
        """Calculates the average game length based on the provided DataFrame

        Parameters:
            df (DataFrame): DataFrame containing the DB entries.

        Returns:
            timedelta: Average game time in days hours:minutes:seconds
        """
        date_format = "%d.%m.%Y %H:%M:%S"
        date_diff = []
        for index, row in df.iterrows():
            diff = datetime.strptime(
                row.end_time, date_format) - datetime.strptime(row.start_time, date_format)
            date_diff.append(diff)
        df['game_len'] = date_diff
        game_len_avg = df['game_len'].mean()
        return game_len_avg

    def avg_turns(self, df: DataFrame) -> float:
        """Calculates the average number of turns

        Parameters:
            df (DataFrame): DataFrame containing the DB entries

        Returns:
            float: Average number of turns
        """
        return np.mean([len(x) for x in df.turns.values])


if __name__ == '__main__':
    temp = Analysis()
    print(temp.frame.columns)
