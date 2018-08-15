from __future__ import print_function
from minesweeper import Minesweeper

try :
    input = raw_input
except :
    pass

class Interactive_player(object) :
    def __init__(self) :
        print("="*30)
        print("Usage : [Option] X Y")
        print("Options :")
        print("\to : open a cell")
        print("\tf : flag a cell")
        print("\tq : quit (does not require X and Y)")
        print("="*30)

    def ask_choice(self) :
        choice = input("Command : ")
        choice_list = choice.split()
        self.option = choice_list[0]
        if len(choice_list) == 3 :
            self.x, self.y = map(int, choice_list[1:3])

    def play(self, game) :
        self.game = game
        while not self.game.is_game_won() and not self.game.game_over :
            print(self.game.get_printable_grid())
            self.ask_choice()
            if self.option == "q" :
                print("Thank you for playing")
                break
            if self.option == 'f' :
                if not self.game.action_flag(self.x, self.y) :
                    print("Flag unsuccessfull")
            elif self.option == "o" :
                if not self.game.action_open(self.x, self.y) :
                    print("Open unsuccessfull")
            else :
                print("Invalid command")

        if self.game.game_over :
            print(self.game.get_printable_game_over_grid())
            print("Game over!")
        if self.game.is_game_won() :
            print(self.game.get_printable_grid())
            print("Congratulations!! You won.")

if __name__ == "__main__" :
    grid_size = 5
    num_of_mines = 3
    game = Minesweeper(grid_size, num_of_mines)
    human = Interactive_player()
    human.play(game)
