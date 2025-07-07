from agent import TicTacToeAgent

WIN_LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
Symbols = {0: ' ', 1: 'X', -1: 'O'}

def print_board(b):
    print('------')
    for i in range(3):
        row = [Symbols[b[3*i+j]] for j in range(3)]
        print(' | '.join(row))
        if i < 2:
            print('---------')
    print('------')

def winner(board):
    for a,b,c in WIN_LINES:
        s = board[a] + board[b] + board[c]
        if s == 3:
            return 1
        if s == -3:
            return -1
    if 0 not in board:
        return 0
    return None

def play_game():
    agent = TicTacToeAgent(ai_player=-1)
    board = [0]*9
    turn = 1

    while True:
        print_board(board)
        w = winner(board)
        if w is not None:
            if w == 1:
                print('Vous avez gagné !')
            elif w == -1:
                print("L'IA a gagné !")
            else:
                print('Match nul.')
            break

        if turn == 1:
            try:
                mv = int(input('Votre coup (0‑8) : '))
            except ValueError:
                continue
            if 0 <= mv <= 8 and board[mv] == 0:
                board[mv] = 1
                turn = -1
        else:
            mv = agent.play(board, player=-1)
            print(f'IA joue {mv}')
            board[mv] = -1
            turn = 1