import chess
board = chess.Board()
print(board.unicode(
    invert_color=True,
    borders=False,
    empty_square=".",
    orientation=chess.WHITE
))