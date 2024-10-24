import pandas as pd
from sklearn.model_selection import train_test_split

def prepare_data(input_file, train_output, test_output, test_size=0.2, random_state=42):
    # Đọc dữ liệu từ file CSV
    data = pd.read_csv(input_file)
    
    # Chia dữ liệu thành train và test
    train_data, test_data = train_test_split(data, test_size=test_size, random_state=random_state)
    
    # Lưu ra file CSV
    train_data.to_csv(train_output, index=False)
    test_data.to_csv(test_output, index=False)
    print(f'Data prepared: {len(train_data)} training samples, {len(test_data)} testing samples.')

if __name__ == "__main__":
    # Gọi hàm với tên file input và output mong muốn
    prepare_data('sudoku_dataset.csv', 'train.csv', 'test.csv')
