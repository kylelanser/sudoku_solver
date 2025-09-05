
from src.SudokuMap import SudokuMap

if __name__ == '__main__':
    easy_puzzle = [ 
        [4,0,0,5,0,1,0,0,8],
        [0,0,7,3,8,0,4,0,0],
        [ 0,6,0,4,0,7,0,0,1 ],
        [ 7,0,0,0,0,0,9,1,0 ],
        [ 1,0,6,0,0,0,5,0,7 ],
        [ 0,2,4,0,0,0,0,0,3 ],
        [ 8,0,0,2,0,6,0,7,0 ],
        [ 0,0,3,0,1,4,8,0,0 ],
        [ 6,0,0,7,0,8,0,0,9 ]
    ]
    sudoku = SudokuMap(easy_puzzle)
    sudoku.solve()
    # Print final map
    for row in sudoku.possibilities:
        print(row)