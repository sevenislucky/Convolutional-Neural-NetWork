# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 10:12:09 2018

@author: kjwil
"""

#Part 1 - Building Convolutional Neural Network
# import libraries
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

#Initialising the Convolutional Neural Network
classifier = Sequential()

# Step 1 - Convolution (creating Feature maps)

classifier.add(Conv2D(32,(3,3), input_shape = (64,64,3), activation = "relu"))

# Step 2 - Max Pooling reduced feature map, maintaining features

classifier.add(MaxPooling2D(pool_size = (2,2)))
#Adding another convolutional layer to increase accuracy and decrease over fitting
classifier.add(Conv2D(32,(3,3), activation = "relu"))
classifier.add(MaxPooling2D(pool_size = (2,2)))

 #Flattening turn the feature map into one vector (column)
 
classifier.add(Flatten())
 
 #Step 4 Full connection
 
classifier.add(Dense(units = 128, activation = "relu" ))
#classifier.add(Dense(units = 128, activation = "relu" ))
classifier.add(Dense(units =  1, activation = "sigmoid" ))

#compiling convolution neural network
classifier.compile(optimizer = "adam", loss = "binary_crossentropy", metrics = ["accuracy"])

#Part 2 - Fitting the CNN to the images. 
from keras.preprocessing.image import ImageDataGenerator
#import ImageDataGenerator, this functions gets all the images and changes them
# to help with overfitting issues, you can change target_size to larger area
# but this will need a gpu to gan results within a timely manner a cpu will
# take possibly days to process. 

train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('training_set',
                                                    target_size=(64, 64),
                                                    batch_size=32,
                                                    class_mode='binary')

test_set = test_datagen.flow_from_directory(
                                            'test_set',
                                            target_size=(64, 64),
                                            batch_size=32,
                                            class_mode='binary')

classifier.fit_generator(
                            training_set,
                            steps_per_epoch=(8000/32),
                            epochs=25,
                            validation_data=test_set,
                            validation_steps=(2000/32))

#save model...really need this after 20/14hrs trainging!!
# Update to above comment, divided training set and test set to cut processing time drastically
# and still have a good enough result.
classifier.save("model_1.h5")

# predict against images not in test file or training file
import numpy as np
from keras.preprocessing import image 

# change file to what ever picture you want tested answer will always
# be a cat or dog...so if you try insert an image of a person dont be disapointed!
newTest = image.load_img("single_prediction/cat_or_dog6.jpg", target_size =(64,64))
newTest = image.img_to_array(newTest)
newTest = np.expand_dims(newTest, axis = 0)
result = classifier.predict_classes(newTest)
#result = (np.argmax(result))
training_set.class_indices
if result[0][0] == 1:
    prediction = "Dog"
else:
    prediction = "Cat"
    
from keras.models import load_model
classifier1 = load_model("model.h5")

classifier.summary()
classifier.get_weights()
classifier.optimizer
    