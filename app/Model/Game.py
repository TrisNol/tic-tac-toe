from typing import List
from dataclasses import dataclass

from Model.GameTurn import GameTurn

@dataclass()
class Game(object):
    """ Class to store data related to a game. """
    id: int
    name_player1: str
    name_player2: str
    sign_player1: str
    sign_player2: str
    start_time: str
    end_time: str
    turns: List[GameTurn]

    def __init__(self) -> None:
        self.turns = []

