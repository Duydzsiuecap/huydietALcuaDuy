import tensorflow as tf
from tensorflow.keras import layers, models
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

# Xây dựng mô hình CNN
def build_sudoku_model():
    model = models.Sequential()
    model.add(layers.Conv2D(64, (3, 3), activation='relu', input_shape=(9, 9, 1)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(81*9, activation='softmax'))  # 81 ô của Sudoku, mỗi ô có 9 khả năng (1-9)
    model.add(layers.Reshape((9, 9, 9)))  # Đưa về ma trận 9x9x9, mỗi ô có 9 giá trị xác suất cho 1-9
    return model

# Chuẩn bị dữ liệu từ file CSV
def prepare_data(input_file):
    data = pd.read_csv(input_file)
    
    # Chuyển đổi 'puzzle' và 'solution' thành ma trận 9x9
    X = data['puzzle'].apply(lambda x: [[int(num) for num in x[i:i+9]] for i in range(0, 81, 9)])
    y = data['solution'].apply(lambda x: [[int(num) for num in x[i:i+9]] for i in range(0, 81, 9)])
    
    # Chuyển đổi về định dạng numpy array để huấn luyện
    X = np.array(list(X)).reshape(-1, 9, 9, 1)
    y = np.array(list(y)).reshape(-1, 9, 9)
    
    # One-hot encoding cho nhãn y
    y = tf.keras.utils.to_categorical(y - 1, num_classes=9)  # Chuyển về dạng one-hot với các nhãn từ 0-8
    
    # Chia thành tập huấn luyện và kiểm thử
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return (X_train, y_train), (X_test, y_test)

# Huấn luyện mô hình
def train_model(input_file):
    # Chuẩn bị dữ liệu
    (X_train, y_train), (X_test, y_test) = prepare_data(input_file)

    # Xây dựng mô hình
    model = build_sudoku_model()
    
    # Compile mô hình với loss categorical_crossentropy và accuracy metrics
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    # Huấn luyện mô hình
    model.fit(X_train, y_train, epochs=10, batch_size=64, validation_data=(X_test, y_test))
    
    # Lưu mô hình sau khi huấn luyện
    model.save('sudoku_model.h5')
    print("Mô hình đã được lưu vào file 'sudoku_model.h5'")

if __name__ == "__main__":
    # Huấn luyện mô hình với dữ liệu từ sudoku_dataset.csv
    train_model('sudoku_dataset.csv')
