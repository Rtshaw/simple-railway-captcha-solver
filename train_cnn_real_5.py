from keras.models import Model
# from keras.layers import Input, Dense, Dropout, Flatten, Conv2D, MaxPool2D, BatchNormalization
from keras.layers import Input, Dense, Dropout, Flatten, Conv2D, MaxPooling2D, BatchNormalization
from keras.callbacks import ModelCheckpoint, EarlyStopping, TensorBoard
from PIL import Image
import numpy as np
import csv
import os

LETTERSTR = "23456789ABCDEFGHJKLMNPRSTUVWXYZabcdefghjklmnprstuvwxyz"


def toonehot(text):
    labellist = []
    for letter in text:
        onehot = [0 for _ in range(31)]
        num = LETTERSTR.find(letter)
        onehot[num] = 1
        labellist.append(onehot)
    return labellist


# Create CNN Model
print("Creating CNN model...")
in_ = Input((41, 157, 3))
out = in_
out = Conv2D(filters=32, kernel_size=(3, 3), padding='same', activation='relu')(out)
out = Conv2D(filters=32, kernel_size=(3, 3), activation='relu')(out)
out = BatchNormalization()(out)
# out = MaxPool2D((2, 2))(out)
out = MaxPooling2D(pool_size=(2, 2), dim_ordering='th')(out)
out = Dropout(0.5)(out)
out = Conv2D(filters=64, kernel_size=(3, 3), padding='same', activation='relu')(out)
out = Conv2D(filters=64, kernel_size=(3, 3), activation='relu')(out)
out = BatchNormalization()(out)
# out = MaxPool2D((2, 2))(out)
out = MaxPooling2D(pool_size=(2, 2), dim_ordering='th')(out)
out = Dropout(0.5)(out)
out = Conv2D(filters=128, kernel_size=(3, 3), padding='same', activation='relu')(out)
out = Conv2D(filters=128, kernel_size=(3, 3), activation='relu')(out)
out = BatchNormalization()(out)
# out = MaxPool2D((2, 2))(out)
out = MaxPooling2D(pool_size=(2, 2), dim_ordering='th')(out)
out = Dropout(0.5)(out)
out = Conv2D(filters=256, kernel_size=(3, 3), activation='relu')(out)
out = BatchNormalization()(out)
# out = MaxPool2D((2, 2))(out)
out = MaxPooling2D(pool_size=(2, 2), dim_ordering='th')(out)
out = Flatten()(out)
out = Dropout(0.5)(out)
out = [Dense(31, name='digit1', activation='softmax')(out),\
    Dense(31, name='digit2', activation='softmax')(out),\
    Dense(31, name='digit3', activation='softmax')(out),\
    Dense(31, name='digit4', activation='softmax')(out),\
    Dense(31, name='digit5', activation='softmax')(out)]
model = Model(inputs=in_, outputs=out)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

print("Reading training data...")
traincsv = open('./data/5_real_train_set/captcha_train.csv', 'r', encoding = 'utf8')
train_data = np.stack([np.array(Image.open('./data/5_real_train_set/' + str(i) + ".png"))/255.0 for i in range(1, 24)])
traincsv = open('./data/5_real_train_set/captcha_train.csv', 'r', encoding = 'utf8')
read_label = [toonehot(row[1]) for row in csv.reader(traincsv)][:26]
train_label = [[] for _ in range(5)]
for arr in read_label:
    for index in range(5):
        train_label[index].append(arr[index])
train_label = [arr for arr in np.asarray(train_label)]
print("Shape of train data:", train_data.shape)

print("Reading validation data...")
valicsv = open('./data/5_real_train_set/captcha_train.csv', 'r', encoding = 'utf8')
vali_data = np.stack([np.array(Image.open('./data/5_real_train_set/' + str(i) + ".png"))/255.0 for i in range(25, 27)])
valicsv = open('./data/5_real_train_set/captcha_train.csv', 'r', encoding = 'utf8')
read_label = [toonehot(row[1]) for row in csv.reader(valicsv)][26:]
vali_label = [[] for _ in range(5)]
for arr in read_label:
    for index in range(5):
        vali_label[index].append(arr[index])
vali_label = [arr for arr in np.asarray(vali_label)]
print("Shape of validation data:", vali_data.shape)

filepath="./data/model/real_5_model.h5"
# checkpoint = ModelCheckpoint(filepath, monitor='val_digit5_acc', verbose=1, save_best_only=True, mode='max')
checkpoint = ModelCheckpoint(filepath, save_best_only=True)
# earlystop = EarlyStopping(monitor='val_digit5_acc', patience=5, verbose=1, mode='auto')
tensorBoard = TensorBoard(log_dir = "./logs", histogram_freq = 1)
callbacks_list = [checkpoint, earlystop, tensorBoard]
model.fit(train_data, train_label, batch_size=400, epochs=100, verbose=2, validation_data=(vali_data, vali_label), callbacks=callbacks_list)
