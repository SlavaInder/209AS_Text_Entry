# this file makes use of code presented in this resources
# https://medium.com/analytics-vidhya/build-a-simple-predictive-keyboard-using-python-and-keras-b78d3c88cffb

import logging
import numpy as np
import tensorflow as tf
import nltk


# set info messages for json adapter
# set info messages for txt adapter
txt_adt_text_fetched = "Text adapter successfully fetched text from {file}"
# set info messages for model builder
model_builder_finished = "Tf successfully build the model"
# training text
training_set_location = './training_sets/1661-0.txt'


# this class is responsible for preparing data in the form
# acceptable for the model
class DataProcessor(object):
    def json_adapter(self, file_name: str):
        pass

    # fetch the text from .txt file
    def txt_adapter(self, file_name: str):
        # read the file
        with open(training_set_location, "r", encoding='utf-8') as f:
            text = f.read()

        text = text.lower()
        logging.info(txt_adt_text_fetched.format(file_name))
        self.text_processor(text)

    def text_processor(self, text: str):
        # tokenizer is basically the same as str.split(),
        # but performs several things simultaneously:
        # splits string by whitespaces, prepositions, new lines, and such staff
        tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
        words = tokenizer.tokenize(text)
        # same as set(), but performs faster
        unique_words = np.unique(words)
        unique_word_index = dict((c, i) for i, c in enumerate(unique_words))
        print('corpus length:', len(unique_words))

        WORD_LENGTH = 5
        prev_words = []
        next_words = []
        for i in range(len(words) - WORD_LENGTH):
            prev_words.append(words[i:i + WORD_LENGTH])
            next_words.append(words[i + WORD_LENGTH])
        print(prev_words[0])
        print(next_words[0])

        X = np.zeros((len(prev_words), WORD_LENGTH, len(unique_words)), dtype=bool)
        Y = np.zeros((len(next_words), len(unique_words)), dtype=bool)
        for i, each_words in enumerate(prev_words):
            for j, each_word in enumerate(each_words):
                X[i, j, unique_word_index[each_word]] = 1
            Y[i, unique_word_index[next_words[i]]] = 1


# model input is a tuple of
# memory_length (in words) X number_of_unique_words
def model_builder(input_shape: tuple):
    # init model
    model = tf.keras.Sequential()
    # add LSTM layer
    model.add(tf.keras.layers.LSTM(128, input_shape=input_shape))
    # add Fully connected layer
    model.add(tf.keras.layers.Dense(input_shape[1], activation='softmax'))
    # log the result
    logging.info(model_builder_finished)
    return model


if __name__ == "__main__":
    # setup logging
    logging.basicConfig(filename='logs/NN_predictor_execution.log', filemode='w', level=logging.DEBUG)

    # setup input shape
    shape = (15, 100)

    my_model = model_builder(shape)


