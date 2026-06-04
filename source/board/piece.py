
class Piece:
    def __init__(self, name: str = "Piece"):
        self.name = name

    def __str__(self):
        return f"{self.name}"