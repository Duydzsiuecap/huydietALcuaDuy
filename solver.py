def is_valid(board, row, col, num):
    # Kiểm tra hàng
    for i in range(9):
        if board[row][i] == num:
            return False
    
    # Kiểm tra cột
    for i in range(9):
        if board[i][col] == num:
            return False

    # Kiểm tra vùng 3x3
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:  # Nếu ô trống
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0  # Quay lui
                return False
    return True

# Hàm in ra bảng Sudoku
def print_board(board):
    for row in board:
        print(row)

# Ví dụ chạy thử
if __name__ == "__main__":
    # Bảng Sudoku chưa giải
    sudoku_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    if solve_sudoku(sudoku_board):
        print("Solved Sudoku:")
        print_board(sudoku_board)
    else:
        print("No solution exists.")
