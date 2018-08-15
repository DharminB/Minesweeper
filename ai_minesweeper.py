from __future__ import print_function
from cmd_line_minesweeper import Interactive_player
from minesweeper import Minesweeper
import random
import time

class Logical_bot(Interactive_player) :
    def __init__(self) :
        pass

    def ask_choice(self) :
        self.grid = self.game.get_board()
        self.size = self.game.grid_size
        self.main_logic_block()
#        time.sleep(1)

    def main_logic_block(self) :
        border = self.get_border_cells()
        if self.apply_already_satisfied_rule(border) :
            print("Already satisfied", self.option, self.x, self.y)
            return
        if self.apply_obvious_choice_rule(border) :
            print("Obvious choice", self.option, self.x, self.y)
            return
        if self.apply_mutant_already_satisfied_rule(border) :
            print("Mutant already satisfied", self.option, self.x, self.y)
            return
        if self.apply_mutant_obvious_choice_rule(border) :
            print("Mutant obvious choice", self.option, self.x, self.y)
            return
        self.apply_random_choices()

    def apply_already_satisfied_rule(self, border) :
        for (x, y) in border :
            num = int(self.grid[x][y])
            nbr_char = self.get_neighbour_characters(x, y)
            num_bombs = nbr_char.count("F")
            if num == num_bombs :
                self.x = x
                self.y = y
                self.option = "o"
                return True
        return False

    def apply_obvious_choice_rule(self, border) :
        for (x, y) in border :
            num = int(self.grid[x][y])
            nbr_char = self.get_neighbour_characters(x, y)
            num_bombs = nbr_char.count("F")
            num_closed = nbr_char.count("-")
#            print(x, y, num, num_bombs+num_closed)
            if num == num_bombs + num_closed :
                neighbours = self.get_valid_neighbour_positions(x, y)
                for n in neighbours :
                    if self.grid[n[0]][n[1]] == "-" :
                        break
                self.x = n[0]
                self.y = n[1]
                self.option = "f"
                return True
        return False

    def apply_mutant_already_satisfied_rule(self, border) :
        for (x, y) in border :
            num = int(self.grid[x][y])
            nbr_char = self.get_neighbour_characters(x, y)
            num_bombs = nbr_char.count("F")
            num_closed = nbr_char.count("-")
            if num_closed > 2 and num == 1 + num_bombs :
                bombtile_pair = self.get_bombtile_pair(x, y, border)
                if len(bombtile_pair) == 0 :
                    continue
                neighbours = self.get_valid_neighbour_positions(x, y)
                for n in neighbours :
                    if self.grid[n[0]][n[1]] == "-" and n not in bombtile_pair :
                        self.x = n[0]
                        self.y = n[1]
                        self.option = "o"
                        return True
        return False

    def apply_mutant_obvious_choice_rule(self, border) :
        for (x, y) in border :
            num = int(self.grid[x][y])
            nbr_char = self.get_neighbour_characters(x, y)
            num_bombs = nbr_char.count("F")
            num_closed = nbr_char.count("-")
            if num_closed > 2 and num == 1 + num_bombs + (num_closed-2) :
                bombtile_pair = self.get_bombtile_pair(x, y, border)
                if len(bombtile_pair) == 0 :
                    continue
                neighbours = self.get_valid_neighbour_positions(x, y)
                for n in neighbours :
                    if self.grid[n[0]][n[1]] == "-" and n not in bombtile_pair :
                        self.x = n[0]
                        self.y = n[1]
                        self.option = "f"
                        return True
        return False

    def apply_random_choices(self) :
        x = random.randint(0, self.size - 1)
        y = random.randint(0, self.size - 1)
        while self.grid[x][y] != "-" :
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
        self.x = x
        self.y = y
        self.option = "o"
        print("Random", self.x, self.y)

    def get_valid_neighbour_positions(self, row, col) :
        neighbour = []
        for i in range(-1,2) :
            for j in range(-1,2) :
                neighbour.append((row+i,col+j))
        neighbour.remove((row,col))
        temp = []
        for i in neighbour :
            if i[0] < 0 or i[1] < 0 or i[0] >= self.size or i[1] >= self.size :
                temp.append(i)
        for i in temp :
            neighbour.remove(i)
        return neighbour

    def get_neighbour_characters(self, row, col) :
        neighbours = self.get_valid_neighbour_positions(row, col)
        characters = [self.grid[n[0]][n[1]] for n in neighbours]
        return characters

    def get_border_cells(self) :
        border = []
        for i in range(self.size) :
            for j in range(self.size) :
                if self.grid[i][j] not in ["-", "F", "0"] :
                    neighbour_characters = self.get_neighbour_characters(i, j)
                    if "-" in neighbour_characters :
                        border.append((i, j))
        return border

    def get_bombtile_pair(self, x, y, border) :
        neighbours = self.get_valid_neighbour_positions(x, y)
        for n in neighbours : 
            if n in border :
                nbr_char = self.get_neighbour_characters(n[0], n[1])
                if nbr_char.count("-") == 2 and nbr_char.count("F") + 1 == int(self.grid[n[0]][n[1]]) :
                    common_clsd_tile = self.get_common_closed_tiles(x, y, n[0], n[1])
                    if len(common_clsd_tile) == 2 :
                        return common_clsd_tile
        return []

    def get_common_closed_tiles(self, x1, y1, x2, y2) :
        nbr1 = self.get_valid_neighbour_positions(x1, y1)
        nbr2 = self.get_valid_neighbour_positions(x2, y2)
        common_nbr = []
        for n in nbr1 :
            if self.grid[n[0]][n[1]] == "-" and n in nbr2 :
                common_nbr.append(n)
        return common_nbr
        


if __name__ == "__main__" :
    grid_size = 8
    num_of_mines = 10
    game = Minesweeper(grid_size, num_of_mines)
    bot = Logical_bot()
    bot.play(game)
