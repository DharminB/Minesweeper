from __future__ import print_function
import random

# =============================================================================

class Cell :
    def __init__(self) :
        self.mine = False
        self.number = 0
        self.flagged = False
        self.visible = False

    def flag(self) :
        if self.visible :
            return False
        else :
            self.flagged = not self.flagged
            return True

    def set_visible(self) :
        if self.flagged :
            return
        else :
            self.visible = True

    def get_character(self) :
        if self.flagged :
            return "F"
        if not self.visible :
            return "-"
        if self.mine :
            return "X"
        else :
            return str(self.number)

# =============================================================================

class Grid :
    def __init__(self, size, num_mines) :
        self.size = size
        self.num_mines = num_mines
        self.grid = []
        self.init_grid()
        self.init_mines()
        self.init_numbers()
#        self.set_all_visible()
        self.recently_opened = []

    def init_grid(self) :
        for i in range(self.size) :
            self.grid.append([])
            for j in range(self.size) :
                self.grid[-1].append(Cell())

    def init_mines(self) :
        for mines in range(self.num_mines) :
            while True :
                x = random.randint(0,self.size-1)
                y = random.randint(0,self.size-1)
                if not self.grid[x][y].mine :
                    self.grid[x][y].mine = True
                    break

    def init_numbers(self) :
        for i in range(self.size) :
            for j in range (self.size) :
                neighbours = self.get_valid_neighbour_positions(i,j)
                for n in neighbours :
                    if self.grid[n[0]][n[1]].mine :
                        self.grid[i][j].number += 1
        
    def get_valid_neighbour_positions(self, row, col) :
        neighbour = []
        for i in range(-1,2) :
            for j in range(-1,2) :
                neighbour.append((row+i,col+j))
#        neighbour = [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]
        neighbour.remove((row,col))
        temp = []
        for i in neighbour :
            if i[0] < 0 or i[1] < 0 or i[0] >= self.size or i[1] >= self.size :
                temp.append(i)
        for i in temp :
            neighbour.remove(i)
        return neighbour
 
    def set_all_visible(self) :
        for i in range(self.size) :
            for j in range(self.size) :
                self.grid[i][j].set_visible()

    def __str__(self) :
        s = " |"
        for i in range(self.size) :
            s += str(i) + " "
        s += "\n"
        s += "-"*(self.size*2+2)
        for i in range(self.size) :
            s += "\n"
            s += str(i) + "|"
            for j in range(self.size) :
                s += self.grid[i][j].get_character() + " "
        return s

    def recursive_open_cell(self, x, y) :
        cell = self.grid[x][y]
        if cell.number > 0 :
            cell.set_visible()
            return
        elif cell.flagged :
            return 
        elif cell in self.recently_opened :
            return
        else :
            cell.set_visible()
            self.recently_opened.append(cell)
            neighbours = self.get_valid_neighbour_positions(x, y)
            for i in neighbours :
                nx, ny = i
                self.recursive_open_cell(nx, ny)

    def open_cell(self, x, y) :
        cell = self.grid[x][y]
        cell.set_visible()
        if cell.flagged :
             return True
        elif cell.mine :
            print("Mine!!")
            return False
        elif cell.number > 0 :
            return True
        else :
            self.recursive_open_cell(x,y)
            self.recently_opened = []
            return True
            
    def flag_cell(self, x, y) :
        cell = self.grid[x][y]
        return cell.flag()

    def is_all_correct(self) :
        for i in range(self.size) :
            for j in range(self.size) :
                cell = self.grid[i][j]
                if not cell.visible and not cell.flagged :
                    return False
                elif not cell.visible and cell.flagged and not cell.mine :
                    return False
                elif cell.visible and cell.mine :
                    return False
        return True

    def is_cell_open(self, x, y) :
        return self.grid[x][y].visible


# =============================================================================

class Minesweeper(object) :
    def __init__(self, grid_size, num_of_mines) :
        self.grid_size = grid_size
        self.num_of_mines = num_of_mines
        self.__grid = Grid(grid_size, num_of_mines)
        self.game_over = False

    def action_flag(self, x, y) :
        if self.game_over : 
            return False
        if not self.is_cell_valid(x, y) :
            print("Invalid cell index")
            return False
        else :
            return self.__grid.flag_cell(x,y)

    def action_open(self, x, y) :
        if self.game_over :
            return False
        if not self.is_cell_valid(x, y) :
            print("Invalid cell index")
            return False
        if not self.__grid.is_cell_open(x, y) :
            if not self.__grid.open_cell(x,y) :
                self.game_over = True
            return True
        else :
            neighbours = self.__grid.get_valid_neighbour_positions(x, y)
            for cell in neighbours :
                if not self.__grid.open_cell(cell[0], cell[1]) :
                    self.game_over = True
                    break
            return True

    def get_board(self) :
        board = []
        for i in range(self.grid_size) :
            board.append([])
            for j in range(self.grid_size) :
                board[i].append(self.__grid.grid[i][j].get_character())
        return board

    def get_printable_grid(self) :
        return self.__grid.__str__()

    def get_printable_game_over_grid(self) :
        self.game_over = True
        self.__grid.set_all_visible()
        return self.get_printable_grid()


    def is_game_won(self) :
        return self.__grid.is_all_correct()

    def is_cell_valid(self, x, y) :
        return x > 0 or x < self.grid_size or y > 0 or y < self.grid_size
# =============================================================================

