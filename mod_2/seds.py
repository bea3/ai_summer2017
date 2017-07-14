import copy

prisoners_dilemma = [
    [(-5, -5), (-1, -10)],
    [(-10, -1), (-2, -2)]]

bar = [[(11, 11), (15, 13), (15, 16)],
       [(13, 15), (21, 21), (29, 16)],
       [(16, 15), (16, 29), (26, 26)]]

bar_2 = [[(10, 4), (5, 2), (2, 6)],
         [(7, 5), (3, 8), (7, 10)],
         [(2, 9), (8, 3), (9, 9)]]

weak_game = [
    [(5, 6), (3, 10), (5, 5)],
    [(10, 2), (1, 1), (10, 3)],
    [(7, 1), (2, 1), (7, 0)]
]


def is_solved(board):
    if len(board) == 1 and len(board[0]) == 1:
        return True
    else:
        return False


def remove_dominated_columns(board, weak, no_col_moves):
    num_rows = len(board)
    num_columns = len(board[0])

    dominates = True
    y = num_columns - 1
    is_dominated_col = None

    while y > 0:
        x = 0
        dominates = True
        while x < num_rows:
            right_col = board[x][y][1]
            left_col = board[x][y - 1][1]

            if (weak and left_col > right_col) or (not weak and (left_col >= right_col)):
                dominates = False
                x = num_rows
            x += 1
        if dominates:
            is_dominated_col = y - 1
            y = 0
        y -= 1

    if dominates:
        for x in range(num_rows):
            del board[x][is_dominated_col]
    else:
        dominates = True
        y = 0
        is_dominated_col = None
        while y < num_columns - 1:
            x = 0
            dominates = True
            while x < num_rows:
                right_col = board[x][y + 1][1]
                left_col = board[x][y][1]
                if (weak and left_col <= right_col) or (not weak and (left_col <= right_col)):
                    if left_col <= right_col:
                        dominates = False
                        x = num_rows
                x += 1
            if dominates:
                is_dominated_col = y + 1
                y = num_columns
            y += 1

        if dominates:
            for x in range(num_rows):
                del board[x][is_dominated_col]
        else:
            no_col_moves = True

    return board, no_col_moves


def remove_dominated_rows(board, weak, no_row_moves):
    num_rows = len(board)
    num_columns = len(board[0])

    dominates = True
    x = num_rows - 1
    is_dominated_row = None

    while x > 0:
        y = 0
        dominates = True
        while y < num_columns:
            top = board[x - 1][y][0]
            bottom = board[x][y][0]

            if (weak and (top >= bottom)) or (not weak and (top >= bottom)):
                dominates = False
                y = num_columns
            y += 1
        if dominates:
            is_dominated_row = x - 1
            x = 0
        x -= 1

    if dominates:
        del board[is_dominated_row]
    else:
        dominates = True
        x = 0
        is_dominated_row = None

        while x < num_rows - 1:
            y = 0
            dominates = True
            while y < num_columns:
                top = board[x][y][0]
                bottom = board[x + 1][y][0]

                if (weak and top <= bottom) or (not weak and (top <= bottom)):
                    if top <= bottom:
                        dominates = False
                        y = num_columns
                y += 1
            if dominates:
                is_dominated_row = x + 1
                x = num_rows
            x += 1

        if dominates:
            del board[is_dominated_row]
        else:
            no_row_moves = True
    return board, no_row_moves


def solve_game(game, weak=False):
    board = copy.deepcopy(game)
    is_player_2 = True
    no_col_moves = False
    no_row_moves = False

    while not is_solved(board) and not (no_col_moves and no_row_moves):
        num_rows = len(board)
        num_columns = len(board[0])

        if is_player_2 and num_columns > 1:
            board, no_col_moves = remove_dominated_columns(board, weak, no_col_moves)
            is_player_2 = False
        elif num_rows > 1:
            board, no_row_moves = remove_dominated_rows(board, weak, no_row_moves)
            is_player_2 = True

    if no_col_moves and no_row_moves:
        return None
    else:
        return board[0][0]


strategy_indices = solve_game(bar_2)
print("STRATEGY INDICES - should be None")
print(strategy_indices)

strategy_indices = solve_game(bar_2, True)
print("STRATEGY INDICES - should be 9,9")
print(strategy_indices)

strategy_indices = solve_game(bar)
print("STRATEGY INDICES - should be 21,21")
print(strategy_indices)

strategy_indices = solve_game(prisoners_dilemma)
print("STRATEGY INDICES - should be -5,-5")
print(strategy_indices)
