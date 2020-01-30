## Sudoku solver ##
## by A.C.B. ##

from board import Board

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

def main():
    board = initBoard()

    brush_count = 0
    brushes = 1
    total_dumps = 0
    while(brushes > 0): # TODO: do we need multiple passes?
        brushes = board.brush()
        print("Brushing #{}, changed #{} elements".format(brush_count, brushes))
        brush_count += 1
        total_dumps += brushes
    
    print("Total dump() calls: " + str(total_dumps))
    print(board)

if __name__ == "__main__":
    main()