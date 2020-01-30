## Sudoku solver ##
## by A.C.B. ##

from board import Board, Element
from typing import List

# TODO not hard-code
def initBoard() -> Board:
    board = Board()

    board.grid[0][1].fix(7)
    board.grid[0][5].fix(6)

    board.grid[1][0].fix(9)
    board.grid[1][7].fix(4)
    board.grid[1][8].fix(1)

    board.grid[2][2].fix(8)
    board.grid[2][5].fix(9)
    board.grid[2][7].fix(5)

    board.grid[3][1].fix(9)
    board.grid[3][5].fix(7)
    board.grid[3][8].fix(2)

    board.grid[4][2].fix(3)
    board.grid[4][6].fix(8)

    board.grid[5][0].fix(4)
    board.grid[5][3].fix(8)
    board.grid[5][7].fix(1)

    board.grid[6][1].fix(8)
    board.grid[6][3].fix(3)
    board.grid[6][6].fix(9)

    board.grid[7][0].fix(1)
    board.grid[7][1].fix(6)
    board.grid[7][8].fix(7)

    board.grid[8][3].fix(5)
    board.grid[8][7].fix(8)

    return board

def choice_to_boards(board: Board, choice: tuple) -> List[Board]:
    choice_e = board.grid[choice[0]][choice[1]]
    print("Choice is {} at {}".format(choice_e, choice))
    boards = []
    for val in choice_e.likelies:
        b = Board(board)
        b.grid[choice[0]][choice[1]].fix(val)
        if b.validate():
            boards.append(b)
    return boards

# stats state
brush_count = 0
total_dumps = 0

def groom(board: Board) -> bool:
    global brush_count
    global total_dumps

    brushes = 1
    while(brushes > 0):
        print(board)
        brushes = board.brush()
        print("Brushing #{}, changed #{} elements".format(brush_count, brushes))
        brush_count += 1
        total_dumps += brushes

        choice = board.shiniest_element()
        if choice is None:
            print("No choices left!")
            break
        else:
            candidate_boards = choice_to_boards(board, choice)
            if len(candidate_boards) == 0:
                return False
            elif len(candidate_boards) == 1:
                board = candidate_boards[0]
            else:
                for board in candidate_boards:
                    res = groom(board)
                    if res:
                        board = res
                        return True

    return board.done()

def main():
    board = initBoard()

    if (groom(board)):
        print("Solved board.")
    else:
        print("No solution found.")
    
    print("Total dump() calls: " + str(total_dumps))
    print("Total brush() calls: " + str(brush_count))
    print(board)

if __name__ == "__main__":
    main()