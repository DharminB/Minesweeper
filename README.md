# Minesweeper
Minesweeper game and its AI

- `minesweeper.py` contains the framework for the game minesweeper
- `cmd_line_minesweeper.py` contains the command line interface for the framework for a human single player
- `gui_stuff.py` contains Tkinter library based GUI interface for the game (also for human single player)
- `ai_minesweeper.py` contains an extension of commmand line interface but it contains a bot which solves the puzzle using a set of logical rules.

### Logic for AI
The AI tries to solve the puzzle by applying the following set of rules 

1. Already satisfied : 
```
if 
    number_on_tile == number_of_bombs_around_that_tile
then
    open all its closed neighbours
```

2. Obvious choice :
```
if
    number_on_tile == number_of_bombs_around_that_tile + number_of_closed_tiles_around_that_tile
then 
    flag all closed neighbours
```

3. Mutant already satisfied
Here  `+ 1` is for `bombtile_pair`
```
if
    number_on_tile == number_of_bombs_around_that_tile + 1
then
    open all other tiles
```

4. Mutant obvious choice
Here also `+ 1` is for `bombtile_pair`
```
if
    number_on_tile == number_of_bombs_around_that_tile + 1 + number_of_closed_tiles_around_that_tile
then
    flag all other neighbours
```

Here `bombtile_pair` means a pair of tiles (2 tiles) which are common closed tiles for 2 open tiles and they have exactly one bomb tile and one safe tile within the pair.

For example, let us consider a scenario as shown below
```
... -----|
... - - -|
... - - -|
... 1 1 1| 
```
Here, Rule 1 and Rule 2 cannot be applied. Here Rule 3 can be applied. To understand the matters clearly, let us name the tiles
```
... -----|
... - - -|
... A B C|
... 1 1 1| 
```
Here, according to Rule 3, A can be considered safe because B and C form a `bombtile_pair`. 
The `1` below tile C demands exactly 1 bomb. This demand can only be satisfied if either tile B or tile C is bomb. If B is bomb then C is safe and vice versa. Now the `1` below B also demands exaclty 1 bomb, which can be satisfied by either A, B or C being a bomb. But as we already know that one of tile B or C is definitely a bomb. This satisfies `1` below B and thus A can be safely opened.
