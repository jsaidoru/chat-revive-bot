import chess
import chess.engine

def evaluate(fen: str, time_limit=0.5) -> str:
    board = chess.Board(fen)
    engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\DEFAULTUSER\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe")

    try:
        info = engine.analyse(board, chess.engine.Limit(time=time_limit))
        score = info["score"].white()  # evaluation from White's point of view

        if score.is_mate():
            return f"Mate in {score.mate()}"
        else:
            return f"Evaluation: {score.score() / 100}"
    finally:
        engine.quit()