from tkinter import *
from tkinter import messagebox
import random

class Board:
    bg_color = {
        '2': '#eee4da', '4': '#ede0c8', '8': '#edc850',
        '16': '#edc53f', '32': '#f67c5f', '64': '#f65e3b',
        '128': '#edcf72', '256': '#edcc61', '512': '#f2b179',
        '1024': '#f59563', '2048': '#edc22e',
    }

    color = {
        '2': '#776e65', '4': '#776e65', '8': '#f9f6f2',
        '16': '#f9f6f2', '32': '#f9f6f2', '64': '#f9f6f2',
        '128': '#f9f6f2', '256': '#f9f6f2', '512': '#f9f6f2',
        '1024': '#f9f6f2', '2048': '#f9f6f2',
    }

    def __init__(self):
        self.n = 4
        self.window = Tk()
        self.window.title('Tum Tum 2048 Game')
        self.gameArea = Frame(self.window, bg='azure3')
        self.board = []
        self.gridCell = [[0]*4 for _ in range(4)]
        self.compress = False
        self.merge = False
        self.moved = False
        self.score = 0

        for i in range(4):
            row = []
            for j in range(4):
                label = Label(self.gameArea, text='', bg='azure4',
                              font=('arial', 22, 'bold'), width=4, height=2)
                label.grid(row=i, column=j, padx=7, pady=7)
                row.append(label)
            self.board.append(row)
        self.gameArea.grid()

    def reverse(self):
        for i in range(4):
            self.gridCell[i].reverse()

    def transpose(self):
        self.gridCell = [list(row) for row in zip(*self.gridCell)]

    def compressGrid(self):
        self.compress = False
        new_grid = [[0]*4 for _ in range(4)]
        for i in range(4):
            pos = 0
            for j in range(4):
                if self.gridCell[i][j] != 0:
                    new_grid[i][pos] = self.gridCell[i][j]
                    if j != pos:
                        self.compress = True
                    pos += 1
        self.gridCell = new_grid

    def mergeGrid(self):
        self.merge = False
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j] == self.gridCell[i][j+1] and self.gridCell[i][j] != 0:
                    self.gridCell[i][j] *= 2
                    self.gridCell[i][j+1] = 0
                    self.score += self.gridCell[i][j]
                    self.merge = True

    def random_cell(self):
        empty = [(i, j) for i in range(4) for j in range(4) if self.gridCell[i][j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.gridCell[i][j] = 2

    def can_merge(self):
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j] == self.gridCell[i][j+1]:
                    return True
        for i in range(3):
            for j in range(4):
                if self.gridCell[i][j] == self.gridCell[i+1][j]:
                    return True
        return False

    def paintGrid(self):
        for i in range(4):
            for j in range(4):
                value = self.gridCell[i][j]
                if value == 0:
                    self.board[i][j].config(text='', bg='azure4')
                else:
                    self.board[i][j].config(
                        text=str(value),
                        bg=self.bg_color.get(str(value), '#3c3a32'),
                        fg=self.color.get(str(value), 'white')
                    )

class Game:
    def __init__(self, gamepanel):
        self.gamepanel = gamepanel
        self.end = False
        self.won = False

    def start(self):
        self.gamepanel.random_cell()
        self.gamepanel.random_cell()
        self.gamepanel.paintGrid()
        self.gamepanel.window.bind('<Key>', self.link_keys)
        self.gamepanel.window.mainloop()

    def link_keys(self, event):
        if self.end or self.won:
            return

        key = event.keysym
        self.gamepanel.compress = False
        self.gamepanel.merge = False
        self.gamepanel.moved = False

        if key == 'Up':
            self.gamepanel.transpose()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.compressGrid()
            self.gamepanel.transpose()
        elif key == 'Down':
            self.gamepanel.transpose()
            self.gamepanel.reverse()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.compressGrid()
            self.gamepanel.reverse()
            self.gamepanel.transpose()
        elif key == 'Left':
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.compressGrid()
        elif key == 'Right':
            self.gamepanel.reverse()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.compressGrid()
            self.gamepanel.reverse()

        self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge

        if self.gamepanel.moved:
            self.gamepanel.random_cell()

        self.gamepanel.paintGrid()

        for row in self.gamepanel.gridCell:
            if 2048 in row:
                self.won = True
                messagebox.showinfo("Tum Tum 2048", "You Won!!!")
                return

        if not any(0 in row for row in self.gamepanel.gridCell) and not self.gamepanel.can_merge():
            self.end = True
            messagebox.showinfo("Tum Tum 2048", "Game Over!")
            return

# Run the game
if __name__ == '__main__':
    gamepanel = Board()
    game = Game(gamepanel)
    game.start()
