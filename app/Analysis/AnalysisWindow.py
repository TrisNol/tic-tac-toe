from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

from analysis.analysis import Analysis
from analysis.mpl_canvas import MplCanvas

class AnalysisWindow(QWidget):
    """Window used to show the results provided by the Analysis class."""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.analysis = Analysis()
        self.build_layout()

    def build_layout(self):
        """Contains the assignments to build the UI."""
        self.setFixedSize(640, 480)
        self.setWindowTitle("Analysis")
        layout = QVBoxLayout()

        frame = self.analysis.get_frame()
        win_relation = self.analysis.get_player_win_relation(frame)

        label_avg_game_len = QLabel(
            f"Average Game Length: {self.analysis.avg_game_len(frame)}")
        label_avg_turns = QLabel(
            f"Average amount of turns: {self.analysis.avg_turns(frame)}")
        sc = MplCanvas(self, width=5, height=4, dpi=100,
                       fig=self.analysis.draw_win_pie(win_relation))

        self.setLayout(layout)
        layout.addWidget(label_avg_game_len)
        layout.addWidget(label_avg_turns)
        layout.addWidget(sc)
