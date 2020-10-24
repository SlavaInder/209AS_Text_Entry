# this file makes use of code presented in this resources
#https://medium.com/analytics-vidhya/build-a-simple-predictive-keyboard-using-python-and-keras-b78d3c88cffb

import numpy as np
import tensorflow as tf
import nltk

# optimizer = RMSprop(lr=0.01)
# model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
# history = model.fit(X, Y, validation_split=0.05, batch_size=128, epochs=2, shuffle=True).history