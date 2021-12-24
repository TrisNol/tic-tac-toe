class Player:
    _name = ""
    _label = ""

    def __init__(self, name, label):
        self._name = name
        self._label = label

    @property
    def name(self):
        return self._name
    @property
    def label(self):
        return self._label