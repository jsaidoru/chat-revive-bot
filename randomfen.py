import chess
import random

def random_fen(max_plies=100):
    board = chess.Board()
    num_plies = random.randint(0, max_plies)

    for _ in range(num_plies):
        if board.is_game_over():
            break
        move = random.choice(list(board.legal_moves))
        board.push(move)

    return board.fen()