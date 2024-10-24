import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model

# Đường dẫn đến mô hình đã huấn luyện
model_path = 'sudoku_model.h5'

# Đường dẫn đến file sudoku_dataset.csv
dataset_path = 'sudoku_dataset.csv'

# Tải mô hình đã huấn luyện
model = load_model(model_path)

# Khởi tạo danh sách các ô nhập liệu (9x9)
entries = [[None for _ in range(9)] for _ in range(9)]

# Hàm kiểm tra nếu số nhập vào là từ 0 đến 9
def validate_input(value_if_allowed):
    if value_if_allowed == "" or (value_if_allowed.isdigit() and 0 <= int(value_if_allowed) <= 9):
        return True
    return False

# Hàm lấy dữ liệu từ các ô nhập liệu và chuyển thành ma trận
def get_board_from_ui():
    board = []
    for i in range(9):
        row = []
        for j in range(9):
            value = entries[i][j].get()
            if value.isdigit():
                row.append(int(value))
            else:
                row.append(0)  # Ô trống được điền bằng 0
        board.append(row)
    return board

# Hàm cập nhật giao diện sau khi giải xong
def update_board_on_ui(solved_board):
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)
            entries[i][j].insert(0, str(solved_board[i][j]))

# Hàm kiểm tra nếu bảng đã có trong dataset và lấy lời giải
def check_if_trained():
    board = get_board_from_ui()  # Lấy dữ liệu từ giao diện
    board_str = ''.join(map(str, sum(board, [])))  # Chuyển ma trận thành chuỗi

    try:
        df = pd.read_csv(dataset_path)
        if board_str in df['puzzle'].values:  # So sánh chuỗi bảng với dữ liệu đã học
            messagebox.showinfo("Kết quả", "Bảng này đã được học. Đang hiển thị lời giải...")
            solution_str = df.loc[df['puzzle'] == board_str, 'solution'].values[0]
            solved_board = [[int(solution_str[i*9 + j]) for j in range(9)] for i in range(9)]
            update_board_on_ui(solved_board)  # Cập nhật giao diện với lời giải từ dataset
        else:
            messagebox.showinfo("Kết quả", "Bảng này chưa được học. Đang giải bằng mô hình...")
            solve_board(board)  # Gọi hàm giải bảng Sudoku bằng mô hình
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể đọc file dataset: {str(e)}")

# Hàm giải bảng Sudoku bằng mô hình
def solve_board(board):
    try:
        input_board = tf.convert_to_tensor(board, dtype=tf.float32)
        input_board = tf.reshape(input_board, (1, 9, 9, 1))  # Chuyển thành tensor có shape phù hợp

        # Dự đoán bảng Sudoku đã giải
        predicted_board = model.predict(input_board)
        
        # Sử dụng argmax để lấy giá trị dự đoán cao nhất cho mỗi ô
        predicted_board = tf.argmax(predicted_board, axis=-1)
        predicted_board = tf.reshape(predicted_board, (9, 9)).numpy() + 1  # Chuyển về giá trị từ 1-9

        # Cập nhật giao diện
        update_board_on_ui(predicted_board)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra trong quá trình giải: {str(e)}")

# Hàm xóa toàn bộ nội dung bảng Sudoku
def clear_board():
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)  # Xóa nội dung các ô nhập liệu

# Hàm hiển thị Sudoku và ẩn khung bắt đầu
def show_sudoku():
    start_frame.pack_forget()  # Ẩn khung bắt đầu
    sudoku_frame.pack(fill="both", expand=True)  # Hiển thị Sudoku

# Hàm nhập file .txt từ ngoài và cập nhật giao diện Sudoku
def load_txt_file():
    file_path = filedialog.askopenfilename(title="Chọn file Sudoku", filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            # Đọc file .txt
            with open(file_path, 'r') as f:
                board_str = f.readline().strip()  # Đọc dòng đầu tiên (81 ký tự)
                if len(board_str) != 81 or not board_str.isdigit():
                    raise ValueError("File không hợp lệ. Cần 81 số từ 0 đến 9.")
            
            # Chuyển dãy số thành bảng 9x9
            board = [[int(board_str[i*9 + j]) for j in range(9)] for i in range(9)]
            
            # Hiển thị bảng Sudoku trên giao diện
            for i in range(9):
                for j in range(9):
                    entries[i][j].delete(0, tk.END)  # Xóa nội dung cũ
                    if board[i][j] != 0:
                        entries[i][j].insert(0, str(board[i][j]))  # Điền số vào ô
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")

# Khởi tạo giao diện chính
root = tk.Tk()
root.title("Sudoku Solver")
root.geometry("1000x700")

# Khung chứa giao diện bắt đầu
start_frame = tk.Frame(root)
start_frame.pack()

# Tạo hình nền cho giao diện bắt đầu
bg_image_path = r"C:\Users\VICTUS\Pictures\Saved Pictures\background-nau-cafe.jpg"
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((1000, 700), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(start_frame, width=1000, height=700)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

canvas.create_text(500, 100, text="Sudoku", fill="white", font=('Arial', 40, 'bold'))

# Nút "Bắt đầu"
start_button = tk.Button(start_frame, text="Bắt đầu", command=show_sudoku, width=15, height=2, font=('Arial', 14))
canvas.create_window(500, 300, window=start_button)

# Nút "Thoát"
exit_button = tk.Button(start_frame, text="Thoát", command=root.destroy, width=15, height=2, font=('Arial', 14))
canvas.create_window(500, 400, window=exit_button)

# Khung chứa giao diện Sudoku (ẩn ban đầu)
sudoku_frame = tk.Frame(root)

game_frame = tk.Frame(sudoku_frame)
game_frame.grid(row=0, column=0, padx=50, pady=50)

# Tạo khung chứa các khối 3x3 có viền
for block_row in range(3):
    for block_col in range(3):
        frame = tk.Frame(game_frame, highlightbackground="black", highlightcolor="black", highlightthickness=2, bd=0)
        frame.grid(row=block_row*3, column=block_col*3, rowspan=3, columnspan=3, padx=2, pady=2)
        
        # Tạo các ô nhập liệu trong khung
        for i in range(3):
            for j in range(3):
                # Thêm kiểm tra giá trị nhập (validation)
                vcmd = (root.register(validate_input), '%P')
                entry = tk.Entry(frame, width=3, font=('Arial', 18), justify='center', bd=1, validate='key', validatecommand=vcmd)
                entry.grid(row=i, column=j, padx=1, pady=1)
                entries[block_row*3 + i][block_col*3 + j] = entry  # Gán entry vào danh sách 'entries'

# Khung chứa các nút điều khiển bên cạnh bảng Sudoku
button_frame = tk.Frame(sudoku_frame)
button_frame.grid(row=0, column=1, padx=20, pady=20)

# Nút "Nhập file .txt"
load_button = tk.Button(button_frame, text="Nhập file .txt", command=load_txt_file, width=15, height=2)
load_button.grid(row=0, column=0, pady=10)

# Nút "Kiểm tra" nếu bảng đã được học
check_button = tk.Button(button_frame, text="Kiểm tra", command=check_if_trained, width=15, height=2)
check_button.grid(row=1, column=0, pady=10)

# Nút "Xóa"
clear_button = tk.Button(button_frame, text="Xóa", command=clear_board, width=15, height=2)
clear_button.grid(row=2, column=0, pady=10)

# Nút "Thoát" để quay lại màn hình chính
back_button = tk.Button(button_frame, text="Thoát", command=lambda: sudoku_frame.pack_forget(), width=15, height=2)
back_button.grid(row=3, column=0, pady=10)

# Chạy giao diện chính
root.mainloop()
