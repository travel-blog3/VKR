import os # библиотека os
from PIL import Image # библиотека PIL для обработки изображения
import numpy as np # библиотека numpy для работы с массивами
from skimage.transform import resize # библиотека skimage.transform для обработки изображения
 
from keras.models import Sequential # библиотека keras для создания нейронной сети
from keras.layers import Conv2D # модуль для создания слоев
from keras.layers import AveragePooling2D # модуль для создания слоев
from keras.layers import Flatten # модуль для создания слоев
from keras.layers import Dense # модуль для создания слоев
from keras.models import model_from_json # модуль для сохранения результатов обучения
from keras.preprocessing.image import ImageDataGenerator # модуль для обработки изображения
import cv2 # библиотека компьютерного зрения


IMG_SIZE = 24 # размер изображения

def collecting(): # функция для разделения данных на тренировочную и тестовую часть
	t_d = ImageDataGenerator( # изменение изображения для использования при обучении
			rescale=1./255,
			shear_range=0.2,
			horizontal_flip=True, 
		)

	val_d = ImageDataGenerator( # изменение изображения для тестирования
			rescale=1./255,
			shear_range=0.2,
			horizontal_flip=True,		)

	train_generator = t_d.flow_from_directory( # информация о данных для тренировки
	    directory="dataset/train", # путь к директории
	    target_size=(IMG_SIZE, IMG_SIZE), # размер изображения
	    color_m="grayscale", # преобразование цвета
	    batch_size=32, # размер батча
	    class_mode="binary",
	    shuffle=True, # перемешивание
	    seed=42 
	)

	val_generator = val_d.flow_from_directory( # информация о данных для тестирования
	    directory="dataset/val", # путь к директории
	    target_size=(IMG_SIZE, IMG_SIZE), # размер изображения
	    color_mode="grayscale", # преобразование цвета
	    batch_size=32, # размер батча
	    class_mode="binary",
	    shuffle=True, # перемешивание
	    seed=42
	)
	return train_generator, val_generator


def save_m(model): # функция для сохранения результатов обучения
	m_json = model.to_json() 
	with open("model.json", "w") as json_file:
		json_file.write(m_json)
	model.save_weights("model.h5")

def load_m(): # функция для загрузки результатов
	json_file = open('model.json', 'r') # открытие файла
	loaded_model_json = json_file.read()# чтение файла
	json_file.close() # закрытие файла
	loaded_model = model_from_json(loaded_model_json) 
	loaded_model.load_weights("model.h5") # загрузка параметров
	loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy']) # компиляция с оптимизатором, метриками, ошибкой
	return loaded_model

def training(train_generator, val_generator): # обучение модели
	STEP_SIZE_TRAIN=train_generator.n//train_generator.batch_size # размер батча для обучения
	STEP_SIZE_VALID=val_generator.n//val_generator.batch_size# размер батча для тренировки
	model = Sequential()

	model.add(Conv2D(filters=6, kernel_size=(3, 3), activation='relu', input_shape=(IMG_SIZE,IMG_SIZE,1))) # 1 слой
	model.add(AveragePooling2D()) 

	model.add(Conv2D(filters=16, kernel_size=(3, 3), activation='relu')) # 2 слой
	model.add(AveragePooling2D())

	model.add(Flatten())

	model.add(Dense(units=120, activation='relu')) # 3 слой

	model.add(Dense(units=84, activation='relu')) # 4 слой

	model.add(Dense(units=1, activation = 'sigmoid')) # 5 слой


	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy']) # компиляция модели

	model.fit_generator(generator=train_generator, # задание параметров для обучения и запуск
	                    steps_per_epoch=STEP_SIZE_TRAIN, # размер батча для тренировки
	                    validation_data=val_generator,
	                    validation_steps=STEP_SIZE_VALID,# размер батча для тестирования
	                    epochs=25 # количество эпох
	)
	save_m(model)

def pred(img, model): # функция предсказания
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))
	img = img.astype("float") / 255.0
	img = img.reshape((1, img.shape[0], img.shape[1]))
	prediction = model.predict(img)
	if prediction < 0.1: # закрытый глаз
		prediction = 'closed'
	elif prediction > 0.9: # открытый глаз
		prediction = 'open'
	else:
		prediction = 'idk' 
	return prediction

def evaluate(X_test, y_test):
	model = load_m()
	print('Evaluate model')
	loss, acc = model.evaluate(X_test, y_test, verbose = 0)
	print(acc * 100)

if __name__ == '__main__':	
	train_generator , val_generator = collecting()
	training(train_generator,val_generator)
