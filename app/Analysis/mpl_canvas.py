from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

# Reference: https://www.pythonguis.com/tutorials/plotting-matplotlib/

class MplCanvas(FigureCanvasQTAgg):
    """PyQT5-component to display a matplotlib-figure in the UI"""

    def __init__(self, parent=None, width=5, height=4, dpi=100, fig=None):
        super(MplCanvas, self).__init__(fig)
