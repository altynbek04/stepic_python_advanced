class Notebook:
    def __init__(self, notes):
        self._notes = notes
    @property
    def notes_list(self):
        for i, note in enumerate(self._notes, start=1):
            print(f"{i}.{note}")