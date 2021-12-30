from dataclasses import dataclass
from typing import List

@dataclass()
class GameTurn(object):
    """ Class to store data related to a turn"""
    player_id: int
    row: int
    column: int
    state: List[List[int]]
    turn_number: int
    latest_turn: bool
