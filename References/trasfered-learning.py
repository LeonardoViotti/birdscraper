
# https://towardsdatascience.com/keras-transfer-learning-for-beginners-6c9b8b7143e
# https://github.com/adityaanantharaman/transfer-learning/blob/master/transfer-learning.py


# coding: utf-8


# Import  dependencies
import pandas as pd
import numpy as np
import os
import keras
import matplotlib.pyplot as plt
from keras.layers import Dense,GlobalAveragePooling2D
from keras.applications import MobileNet
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.optimizers import Adam



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
    preprocessing_function=preprocess_input) 

train_generator=train_datagen\
    .flow_from_directory('./train/', # this is where you specify the path to the main data folder
                         target_size=(224,224),
                         color_mode='rgb',
                         batch_size=32,
                         class_mode='categorical',
                         shuffle=True)



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
                    epochs=5)