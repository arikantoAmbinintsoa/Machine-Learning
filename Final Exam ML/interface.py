import tkinter as tk
from agent import TicTacToeAgent

WIN_LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

class TicTacToeGUI:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title('Tic‑Tac‑Toe IA')
        self.buttons = []
        self.board = [0]*9
        self.agent = TicTacToeAgent(ai_player=-1)
        self.turn = 1
        self.status = tk.StringVar(value="À vous de jouer !")
        self.build_board()

    def build_board(self):
        frame = tk.Frame(self.app)
        frame.pack(padx=10, pady=10)
        for i in range(9):
            btn = tk.Button(frame, text=' ', width=4, height=2,
                            font=('Helvetica', 24),
                            command=lambda idx=i: self.on_click(idx))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)
        tk.Label(self.app, textvariable=self.status, font=('Helvetica', 14)).pack(pady=5)
        tk.Button(self.app, text='Rejouer', command=self.reset).pack()

    def on_click(self, idx):
        if self.board[idx] != 0 or self.turn != 1:
            return
        self.board[idx] = 1
        self.buttons[idx]['text'] = 'X'
        self.buttons[idx]['state'] = 'disabled'
        if self.check_end():
            return
        self.turn = -1
        self.app.after(300, self.ai_move)

    def ai_move(self):
        idx = self.agent.play(self.board)
        self.board[idx] = -1
        self.buttons[idx]['text'] = 'O'
        self.buttons[idx]['state'] = 'disabled'
        self.check_end()
        self.turn = 1

    def check_end(self):
        result = self.winner()
        if result is not None:
            if result == 1:
                self.status.set('Vous gagnez !')
            elif result == -1:
                self.status.set("L’IA gagne !")
            else:
                self.status.set('Match nul.')
            for b in self.buttons:
                b['state'] = 'disabled'
            return True
        return False

    def winner(self):
        for a,b,c in WIN_LINES:
            s = self.board[a]+self.board[b]+self.board[c]
            if s == 3:
                return 1
            if s == -3:
                return -1
        if 0 not in self.board:
            return 0
        return None

    def reset(self):
        self.board = [0]*9
        self.turn = 1
        self.status.set('À vous de jouer !')
        for b in self.buttons:
            b['text'] = ' '
            b['state'] = 'normal'

    def run(self):
        self.app.mainloop()

def lancer_interface():
    TicTacToeGUI().run()