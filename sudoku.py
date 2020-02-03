## Sudoku solver ##
## by A.C.B. ##

from board import Board, Element
from typing import List

def initBoard(grid: List[List[int]]) -> Board:
    board = Board()

    for r, row in enumerate(grid):
        for c, digit in enumerate(row):
            if digit != 0:
                board.grid[r][c].fix(digit)

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

def groom(board: Board) -> Board:
    global brush_count
    global total_dumps

    print("Groom: ")
    print(board)
    print()

    brushes = 1
    while(brushes > 0):
        brushes = board.brush()
        print("Brushed, board now: ")
        print(board)
        print()
        print("Brushing #{}, changed #{} elements".format(brush_count, brushes))
        brush_count += 1
        total_dumps += brushes

    if not board.validate():
        print("Unsolvable board:")
        print(board)
        print()
        return None

    choice = board.shiniest_element()
    if choice is None:
        print("No Choices.")
    else:
        candidate_boards = choice_to_boards(board, choice)
        if len(candidate_boards) == 0:
            print("No Choices.")
            print()
        elif len(candidate_boards) == 1:
            print("Single Candidate: ")
            print(board)
            print()
            board = candidate_boards[0]
        else:
            for candidate in candidate_boards:
                candidate = groom(candidate)
                if candidate is not None:
                    print("Chose candidate: ")
                    print(candidate)
                    print()
                    board = candidate

    if board.validate() and board.done():
        return board
    else:
        return None

def main():
    # grid = [[0,0,0, 0,0,0, 0,0,0],
    #         [0,0,0, 0,0,0, 0,0,0],
    #         [0,0,0, 0,0,0, 0,0,0],

    #         [0,0,0, 0,0,0, 0,0,0],
    #         [0,0,0, 0,0,0, 0,0,0],
    #         [0,0,0, 0,0,0, 0,0,0],

    #         [0,0,0, 0,0,0, 0,0,0],
    #         [0,0,0, 0,0,0, 0,0,0],
    #         [0,0,0, 0,0,0, 0,0,0]]

    grid = [[0,6,0, 3,0,0, 8,0,4],
            [5,3,7, 0,9,0, 0,0,0],
            [0,4,0, 0,0,6, 3,0,7],

            [0,9,0, 0,5,1, 2,3,8],
            [0,0,0, 0,0,0, 0,0,0],
            [7,1,3, 6,2,0, 0,4,0],

            [3,0,6, 4,0,0, 0,1,0],
            [0,0,0, 0,6,0, 5,2,3],
            [1,0,2, 0,0,9, 0,8,0]]

    board = initBoard(grid)

    board = groom(board)
    if board is not None:
        print("Solved board.")
        print(board)
    else:
        print("No solution found.")
    
    print("Total dump() calls: " + str(total_dumps))
    print("Total brush() calls: " + str(brush_count))

if __name__ == "__main__":
    main()