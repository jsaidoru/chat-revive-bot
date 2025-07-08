import chess
import random


def random_fen(min_plies=10, max_plies=476):
    board = chess.Board()
    num_plies = random.randint(min_plies, max_plies)

    for _ in range(num_plies):
        if board.is_game_over():
            break
        move = random.choice(list(board.legal_moves))
        board.push(move)

    return board.fen()
