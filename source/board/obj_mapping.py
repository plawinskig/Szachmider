from square import BasicSquare, TeleportSquare, TrapSquare, HeartSquare, ShieldSquare, GrassSquare
from piece import Rook, Knight, Bishop, Queen, King, Pawn


square_mapping: dict[str, type] = {
    "Bsc": BasicSquare,
    "Tel": TeleportSquare,
    "Tra": TrapSquare,
    "Hrt": HeartSquare,
    "Shl": ShieldSquare,
    "Grs": GrassSquare
}

piece_mapping: dict[str, type] = {
    "Roo": Rook,
    "Kni": Knight,
    "Bis": Bishop,
    "Que": Queen,
    "Kin": King,
    "Paw": Pawn
}