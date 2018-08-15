from __future__ import print_function
import Tkinter as tk
from tkMessageBox import showinfo, askyesno, showerror
from minesweeper import Minesweeper

class Gui_stuff(object) :
    def __init__(self, grid_size, num_of_mines) :
        self.size = grid_size
        self.num_of_mines = num_of_mines
        self.button_size = 1
        self.game = Minesweeper(self.size, self.num_of_mines)
        self.root = tk.Tk()
        self.root.title("DG Mines")
        self.root.resizable(width = False, height = False)
        self.button = []
        self.pos = []
        self.colors = ["#000000", "#0000ff", "#00aa00", "#ff00ff", "#ffff00", "#000000", "#000000", "#000000", "#000000"]
        self.add_buttons()

    def button_test(self) :
        button = tk.Button(self.root, text="test", image=self.pixel, width=30, height=30, compound="c")
        button.bind("<Button-1>", self.pressed)
        button.grid(row = 1, column = 1, padx = 3, pady = 3)

    def add_buttons(self) :
        for i in range(self.size) :
            self.button.append([])
            for j in range(self.size) :
                self.button[i].append(tk.Button(self.root, 
                                                text=" ", 
                                                width=self.button_size,
                                                height=self.button_size, 
                                                bd = 2, 
                                                font = "Ariel 10 bold",
                                                bg = "#aaaaaa", 
                                                fg = "#000000",
                                                disabledforeground = "#000000",
                                                activebackground = "#bbbbbb"))
                self.button[i][j].bind("<ButtonRelease-1>", self.pressed)
                self.button[i][j].bind("<Button-3>", self.rightPressed)
                self.button[i][j].grid(row = i+1, column = j, padx = 0, pady = 0)

    def pressed(self,event) :
        print("left button pressed")
        row, col = self.get_button_position(event)
        print(row, col)
        status = self.game.action_open(row, col)
        if not status :
            showerror("Minesweeper", 
			"Sorry !!\n You clicked on a mine and lost.")
            self.root.destroy()
        else :
            self.update()

    def rightPressed(self,event) :
        print("right button pressed")
        row, col = self.get_button_position(event)
        print(row, col)
        self.game.action_flag(row, col)
        self.update()

    def get_button_position(self, event) :
        x = event.x_root - self.root.winfo_x()
        y = event.y_root - self.root.winfo_y()
#        print("x", x)
#        print("y", y)
        button_height = self.root.winfo_height() / self.size
        button_width = self.root.winfo_width() / self.size
#        print(button_height, button_width)
        button_row = y / button_height
        button_col = x / button_width
#        print("row", button_row)
#        print("col", button_col)
        return (button_row, button_col)

    def update(self) :
#        print(self.game.__grid)
        board = self.game.get_board()
        print(self.game.get_printable_grid())
        for i in range(self.size) :
            for j in range(self.size) :
                cell_char = board[i][j]
                btn = self.button[i][j]
                if cell_char not in ['-', 'F']:
                    char = cell_char
                    btn.config(relief=tk.SUNKEN)
                    btn.config(fg=self.colors[int(char)])
                    btn.config(highlightcolor=self.colors[int(char)])
                    btn.config(text=char)
                    if char == "0" :
                        btn.config(text=" ")
                elif cell_char == 'F' :
                    btn.config(relief=tk.RAISED)
                    btn.config(fg="#ff0000")
                    btn.config(highlightcolor="#ff0000")
                    btn.config(text="F")
                else :
                    btn.config(relief=tk.RAISED)
                    btn.config(fg="#000000")
                    btn.config(text=" ")
        if self.game.is_game_won() :
            showinfo("Minesweeper", "Congratulations!\nYou won!")
            self.root.destroy()
                    

if __name__ == "__main__" :
    grid_size = 8
    num_of_mines = 10
    gui = Gui_stuff(grid_size, num_of_mines)
    print("something")
    gui.root.mainloop()

