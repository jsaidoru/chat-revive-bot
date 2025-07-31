import requests
import chess
def get_best_move_api(fen: str) -> str:
    base_url = "https://stockfish.online/api/s/v2.php"
    params = {
        "fen": fen,
        "depth": 15
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise Exception("Failed to fetch move from Stockfish API")

    data = response.json()
    bestmove = data.get("bestmove")

    return bestmove

def get_evaluation_api(fen: str) -> str:
    base_url = "https://stockfish.online/api/s/v2.php"
    params = {
        "fen": fen,
        "depth": 15
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise Exception("Failed to fetch move from Stockfish API")

    data = response.json()
    evaluation = data.get("evaluation")

    return evaluation

# Example usage
fen = "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 4 4"
nospace = fen.replace(" ", "%20")

board = chess.Board(fen)

best_move = get_best_move_api(fen)
best_move = best_move.removeprefix("bestmove ")
best_move = board.san(chess.Move.from_uci(best_move))

evaluation = get_evaluation_api(fen)

print("Best move:", best_move)
print(evaluation)