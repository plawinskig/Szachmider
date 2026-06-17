from source.board import square
from source.board import piece


SQUARE_MAP: dict[str, type] = {
    "Bsc": square.BasicSquare,
    "Tel": square.TeleportSquare,
    "Tra": square.TrapSquare,
    "Hrt": square.HeartSquare,
    "Shl": square.ShieldSquare,
    "Grs": square.GrassSquare
}

PIECE_MAP: dict[str, type] = {
    "Roo": piece.Rook,
    "Kni": piece.Knight,
    "Bis": piece.Bishop,
    "Que": piece.Queen,
    "Kin": piece.King,
    "Paw": piece.Pawn
}