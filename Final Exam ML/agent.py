from functools import lru_cache

WIN_LINES = (
    (0,1,2),(3,4,5),(6,7,8),  # rangées
    (0,3,6),(1,4,7),(2,5,8),  # colonnes
    (0,4,8),(2,4,6)           # diagonales
)

class TicTacToeAgent:
    def __init__(self, ai_player: int = -1):
        """ai_player = -1 (O) par défaut si l'humain joue X (=+1)."""
        self.ai = ai_player
        self.human = -ai_player

    # ---------------- Utils ---------------- #
    @staticmethod
    def winner(board):
        for a,b,c in WIN_LINES:
            s = board[a] + board[b] + board[c]
            if s == 3:
                return 1
            if s == -3:
                return -1
        if 0 not in board:
            return 0  # draw
        return None   # ongoing

    # --------------- Minimax --------------- #
    @lru_cache(maxsize=None)
    def _minimax(self, board_tuple: tuple, player: int, alpha: int, beta: int):
        """Retourne (score, move).  Score : +1 si 'player' gagne, -1 s'il perd, 0 sinon."""
        board = list(board_tuple)
        result = self.winner(board)
        if result is not None:
            return result * player, None  # perspective du joueur courant

        best_score = -2  # plus mauvais possible (< -1)
        best_move = None
        for idx in range(9):
            if board[idx] == 0:
                board[idx] = player
                score, _ = self._minimax(tuple(board), -player, -beta, -alpha)
                score = -score  # inversion de point de vue
                board[idx] = 0

                if score > best_score:
                    best_score, best_move = score, idx
                alpha = max(alpha, score)
                if alpha >= beta:
                    break  # élagage
        return best_score, best_move

    # --------------- API publique ---------- #
    def play(self, board: list[int], player: int = None) -> int:
        """Renvoie le meilleur coup pour 'player' (par défaut l'IA)."""
        if player is None:
            player = self.ai
        _, move = self._minimax(tuple(board), player, -2, 2)
        return move