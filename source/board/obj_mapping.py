import square
import piece


square_mapping: dict[str, type] = {
    "Bsc": square.BasicSquare,
    "Tel": square.TeleportSquare,
    "Tra": square.TrapSquare,
    "Hrt": square.HeartSquare,
    "Shl": square.ShieldSquare,
    "Grs": square.GrassSquare
}

piece_mapping: dict[str, type] = {
    "Roo": piece.Rook,
    "Kni": piece.Knight,
    "Bis": piece.Bishop,
    "Que": piece.Queen,
    "Kin": piece.King,
    "Paw": piece.Pawn
}