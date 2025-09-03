import pytest
from src.SudokuMap import SudokuMap


@pytest.fixture
def easy_puzzle():
    return [ 
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

@pytest.fixture
def easy_puzzle_solution():
    return[
        [4,9,2,5,6,1,7,3,8],
        [5,1,7,3,8,2,4,9,6],
        [3,6,8,4,9,7,2,5,1],
        [7,8,5,6,4,3,9,1,2],
        [1,3,6,8,2,9,5,4,7],
        [9,2,4,1,7,5,6,8,3],
        [8,5,9,2,3,6,1,7,4],
        [2,7,3,9,1,4,8,6,5],
        [6,4,1,7,5,8,3,2,9]
    ]

@pytest.fixture
def medium_puzzle():
    return [
        [ 0,5,0,0,7,0,0,2,0 ],
        [ 0,0,0,0,0,0,4,9,7 ],
        [ 0,0,0,2,0,8,0,5,0 ],
        [ 0,4,0,0,0,0,0,3,9 ],
        [ 9,0,0,1,3,7,0,0,6 ],
        [ 1,2,0,0,0,0,0,7,0 ],
        [ 0,9,0,8,0,6,0,0,0 ],
        [ 3,1,8,0,0,0,0,0,0 ],
        [ 0,7,0,0,1,0,0,8,0 ]
    ]

@pytest.fixture
def medium_puzzle_solution():
    return [
        [4,5,1,9,7,3,6,2,8],
        [8,3,2,6,5,1,4,9,7],
        [7,6,9,2,4,8,3,5,1],
        [6,4,7,5,8,2,1,3,9],
        [9,8,5,1,3,7,2,4,6],
        [1,2,3,4,6,9,8,7,5],
        [5,9,4,8,2,6,7,1,3],
        [3,1,8,7,9,4,5,6,2],
        [2,7,6,3,1,5,9,8,4]
    ]

@pytest.fixture
def hard_puzzle():
    return [ 
        [6,0,0,2,9,0,7,0,0],
        [0,0,7,0,3,4,0,8,6],
        [1,0,0,7,8,0,0,2,0],
        [8,0,0,0,2,0,4,9,0],
        [0,3,0,9,6,8,0,7,0],
        [0,2,9,0,4,0,0,0,8],
        [0,7,0,0,1,2,0,0,9],
        [3,1,0,4,7,0,6,0,0],
        [0,0,2,0,5,3,0,0,7]
    ]


def test_easy_puzzle_solution(easy_puzzle, easy_puzzle_solution):
    sudoku = SudokuMap(easy_puzzle)
    sudoku.solve()
    # verify all cells are solved (len == 1)
    for row in sudoku.possibilities:
        for cell in row:
            assert len(cell) == 1

    
    for y in range(9):
        for x in range(9):
            assert sudoku.possibilities[y][x][0]==easy_puzzle_solution[y][x]


def test_medium_puzzle_solution(medium_puzzle, medium_puzzle_solution):
    sudoku = SudokuMap(medium_puzzle)
    sudoku.solve()
    # verify all cells are solved (len == 1)
    for row in sudoku.possibilities:
        for cell in row:
            assert len(cell) == 1

    
    for y in range(9):
        for x in range(9):
            assert sudoku.possibilities[y][x][0]==medium_puzzle_solution[y][x]

