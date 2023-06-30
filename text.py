import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# 设置验证码图片目录和标注文件路径
captcha_dir = 'captcha_images/'
annotation_file = 'annotations.txt'

# 加载验证码图片和标注数据
def load_data():
    images = []
    labels = []
    with open(annotation_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            filename, label = line.strip().split(',')
            image = cv2.imread(os.path.join(captcha_dir, filename), cv2.IMREAD_GRAYSCALE)
            images.append(image)
            labels.append(label)
    return images, labels

# 数据预处理：将图片调整为统一的大小并进行归一化
def preprocess_data(images):
    processed_images = []
    for image in images:
        image = cv2.resize(image, (32, 32))
        image = image / 255.0
        processed_images.append(image)
    return np.array(processed_images)

# 模型定义
def create_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 1)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    return model

# 加载数据
images, labels = load_data()

# 数据预处理
processed_images = preprocess_data(images)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(processed_images, labels, test_size=0.2, random_state=42)

# 调整数据形状
X_train = np.expand_dims(X_train, axis=-1)
X_test = np.expand_dims(X_test, axis=-1)

# 创建模型
model = create_model()

# 编译模型
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 训练模型
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# 保存模型
model.save('captcha_model.h5')