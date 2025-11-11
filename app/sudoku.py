# The logic

import random, copy

SIZE = 9
BOX = 3

def valid(board, r, c, val):
    if any(board[r][i] == val for i in range(SIZE)): return False
    if any(board[i][c] == val for i in range(SIZE)): return False
    br, bc = (r // BOX) * BOX, (c // BOX) * BOX
    for i in range(br, br + BOX):
        for j in range(bc, bc + BOX):
            if board[i][j] == val: return False
    return True

def find_empty(board):
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 0:
                return r, c
    return None

def solve(board):
    empty = find_empty(board)
    if not empty: return True
    r, c = empty
    for val in range(1, 10):
        if valid(board, r, c, val):
            board[r][c] = val
            if solve(board): return True
            board[r][c] = 0
    return False

def generate_full_board():
    board = [[0]*SIZE for _ in range(SIZE)]
    nums = list(range(1, 10))
    def fill():
        empty = find_empty(board)
        if not empty: return True
        r, c = empty
        random.shuffle(nums)
        for val in nums:
            if valid(board, r, c, val):
                board[r][c] = val
                if fill(): return True
                board[r][c] = 0
        return False
    fill()
    return board

def make_puzzle(full, clues=40):
    puzzle = copy.deepcopy(full)
    cells = [(r, c) for r in range(SIZE) for c in range(SIZE)]
    random.shuffle(cells)
    for (r, c) in cells:
        if sum(1 for row in puzzle for v in row if v != 0) <= clues:
            break
        backup = puzzle[r][c]
        puzzle[r][c] = 0
        test = copy.deepcopy(puzzle)
        if not solve(test): 
            puzzle[r][c] = backup
    return puzzle
