import random
import csv

def generate_sudoku_solution():
    """Tạo ra một bảng Sudoku đã giải hoàn chỉnh"""
    base = 3
    side = base * base

    # Hàm để tạo các mẫu từ 1 đến 9
    def pattern(r, c): return (base * (r % base) + r // base + c) % side
    def shuffle(s): return random.sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    # Tạo bảng Sudoku hoàn chỉnh
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]
    return board

def generate_sudoku_puzzle(solution, difficulty=0.5):
    """Xóa một số ô trên bảng Sudoku để tạo bảng chưa giải (puzzle)"""
    puzzle = [[solution[r][c] for c in range(9)] for r in range(9)]
    num_cells_to_remove = int(81 * difficulty)
    
    while num_cells_to_remove > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            num_cells_to_remove -= 1
    return puzzle

def board_to_string(board):
    """Chuyển bảng 9x9 thành chuỗi 81 ký tự"""
    return ''.join(str(cell) if cell != 0 else '0' for row in board for cell in row)

def generate_sudoku_dataset(filename, num_samples=30):
    """Tạo và lưu dataset Sudoku"""
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['puzzle', 'solution']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for _ in range(num_samples):
            solution = generate_sudoku_solution()
            puzzle = generate_sudoku_puzzle(solution, difficulty=0.5)
            
            puzzle_str = board_to_string(puzzle)
            solution_str = board_to_string(solution)
            
            writer.writerow({'puzzle': puzzle_str, 'solution': solution_str})

    print(f'Dataset với {num_samples} bảng Sudoku đã được tạo và lưu vào {filename}')

# Tạo dataset với 30 bảng Sudoku
generate_sudoku_dataset('sudoku_dataset.csv', num_samples=30)
