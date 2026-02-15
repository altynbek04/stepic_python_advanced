class File:
    def __init__(self, size_in_bytes):
        self._size_in_bytes = size_in_bytes
    @property
    def size(self):
        if self._size_in_bytes < 1024:
            return f"{self._size_in_bytes} B"
        elif self._size_in_bytes < 1024 * 1024:
            return f"{self._size_in_bytes / 1024 :.2f} KB"
        elif self._size_in_bytes < 1024 * 1024 * 1024:
            return f"{self._size_in_bytes / 1024 * 2 :.2f} MB"
        else:
            return f"{self._size_in_bytes / 1024 * 3 :.2f} GB"
    @size.setter
    def size(self, value):
        self._size_in_bytes = value