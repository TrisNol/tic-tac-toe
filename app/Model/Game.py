from typing import List, TypeVar
from dataclasses import dataclass

from Model.GameTurn import GameTurn

T = TypeVar('T')
@dataclass()
class Game:
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

