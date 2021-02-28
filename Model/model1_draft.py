
#-----------------------------------------------------------------#
# Model 1 DRAFT
#-----------------------------------------------------------------#

#-----------------------------------------------------------------#
#### To do and questions

# Set folder structure and my own parameters

# Validation and test set splits

# Different number of elements per class ?

# Check if there are other keras.applications that might be
# better suited for what I'm tryoing to make

# Change models parameters to suit my data

#-----------------------------------------------------------------#
#### References
# https://towardsdatascience.com/keras-transfer-learning-for-beginners-6c9b8b7143e
# https://github.com/adityaanantharaman/transfer-learning/blob/master/transfer-learning.py
# https://machinelearningmastery.com/save-load-keras-deep-learning-models/


#-----------------------------------------------------------------#
#### Settings

# Libaries
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import keras
import tensorflow as tf
from keras.layers import Dense,GlobalAveragePooling2D
from keras.applications import MobileNet
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.optimizers import Adam

# Set seed
np.seed(42)
tf. set_random_seed(42)

#-----------------------------------------------------------------#
#### File paths

# There must be a main data folder, inside that data folder, 
# there must be a folder for each class of data containing 
# the corresponding images. The names of the folders must 
# be the names of their respective classes.

DATA = 'C:/Users/wb519128/Dropbox/Work/Pessoal/Pokedex/Data/'
DATA_training = DATA + 'pilot'

#-----------------------------------------------------------------#
#### Import MobileNet model and process it

# Imports the mobilenet model and discards the last 1000 neuron layer.
base_model=MobileNet(weights='imagenet',
                     include_top=False) 

# Some processing here that I don't fully understand yet.
x=base_model.output
x=GlobalAveragePooling2D()(x)

# Add dense layers for the model can learn more complex functions 
# and classify for better results.
x=Dense(1024,activation='relu')(x) 
#dense layer 2
x=Dense(1024,activation='relu')(x)
#dense layer 3 
x=Dense(512,activation='relu')(x)
 #final layer with softmax activation
preds=Dense(3,activation='softmax')(x)


#-----------------------------------------------------------------#
#### Create my own model

# Create an instance of the Model class based on the original 
# architecture
model=Model(inputs=base_model.input,outputs=preds)
#specify the inputs
#specify the outputs

# Make sure just the added layers are trainable and it is uysing
# the MobileNet weights as they are.
# Carinha de gambiarra esse loop mas ta bom
for layer in model.layers[:20]:
    layer.trainable=False
for layer in model.layers[20:]:
    layer.trainable=True

# Pre-process images to be inputed in the network
train_datagen=ImageDataGenerator(
    preprocessing_function=preprocess_input,
    validation_split = 0.3) 

train_generator=train_datagen\
    .flow_from_directory(DATA_training,
                         target_size=(224,224),
                         color_mode='rgb',
                         batch_size=32,
                         class_mode='categorical',
                         shuffle=True)

#-----------------------------------------------------------------#
#### Compile and train the model

# Compile model
model.compile(optimizer='Adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
# Adam optimizer
# loss function will be categorical cross entropy
# evaluation metric will be accuracy

# Train the model in our set of images
step_size_train=train_generator.n//train_generator.batch_size
model.fit_generator(generator=train_generator,
                    steps_per_epoch=step_size_train,
                    epochs=1)


#-----------------------------------------------------------------#
#### Cross validation


#-----------------------------------------------------------------#
#### Test predictions 
# model.predict( ).

# image = tf.keras.preprocessing.image.load_img(DATA + 'principe.jpg')
# image = tf.keras.preprocessing.image.load_img(DATA + 'test_img4.png')
image = tf.keras.preprocessing.image.load_img(DATA + 'principe.jpg')

input_arr = keras.preprocessing.image.img_to_array(image)
input_arr = np.array([input_arr])  # Convert single image to a batch.

# train_generator.class_indices
model.predict(input_arr)


#-----------------------------------------------------------------#
#### Save trainned model


model.save(DATA + 'model_draft_2.h5')
# print("Saved model to disk")

# # load json and create model
# json_file = open('model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)
# # load weights into new model
# loaded_model.load_weights("model.h5")
# print("Loaded model from disk")
 
# # evaluate loaded model on test data
# loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
# score = loaded_model.evaluate(X, Y, verbose=0)
# print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))