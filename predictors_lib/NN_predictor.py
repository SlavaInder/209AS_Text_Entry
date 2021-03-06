# this file makes use of code presented in this resources
# https://medium.com/analytics-vidhya/build-a-simple-predictive-keyboard-using-python-and-keras-b78d3c88cffb

import logging
import os
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import LSTM
from keras.layers.core import Dense, Activation
from keras.optimizers import RMSprop
import nltk
import heapq

# NN hyper parameters
MEMORY_LENGTH = 5
# training text
training_set_location = './training_sets/1661-0.txt'


# DATA PROCESSOR MESSAGES
# set info messages for json adapter
msg_data_processor_json_adapter_start = ""
# set info messages for filter
msg_data_processor_text_filter_finished = "text filtering is complete"
# set info messages for txt adapter
msg_data_processor_text_adapter_text_fetched = "text adapter successfully fetched text from {file}"
# set info messages for text processor
msg_data_processor_text_processor_text_len = "dataset length is {length}"
msg_data_processor_text_processor_unique_words = "predictor can recognize {word_counter} different words"
msg_data_processor_text_processor_data_shape = "data processor formed a dataset of length {length} and shape {shape}"
# N NET PREDICTOR MESSAGES
# set info messages for model builder
msg_model_builder_finished = "tf successfully build the model"
# set info messages for train model
msg_train_model_complied = "tf successfully compiled the model"


# this class is responsible for preparing data in the form
# acceptable for the model
class DataProcessor(object):
    def __init__(self):
        self.word_index = {}

    # TODO: finish json adapter
    def json_adapter(self, file_name: str):
        pass

    # fetch the text from .txt file
    def txt_adapter(self, file_name: str):
        # read the file
        with open(training_set_location, "r", encoding='utf-8') as f:
            text = f.read()
        # log the results
        logging.info(msg_data_processor_text_adapter_text_fetched.format(file=file_name))
        # filter text
        text = self.text_filter(text)
        # process text
        processed_data, processed_labels = self.text_processor(text)
        return processed_data, processed_labels

    # delete all unprintable symbols, set everything to lowercase
    def text_filter(self, text: str):
        text = text.lower()
        return text

    # produce data vectors from text array
    def text_processor(self, text: str):
        # tokenizer is basically the same as str.split(),
        # but performs several things simultaneously:
        # splits string by whitespaces, prepositions, new lines, and such staff
        tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
        words = tokenizer.tokenize(text)
        logging.info(msg_data_processor_text_processor_text_len.format(length=len(words)))
        # same as set(), but performs faster
        unique_words = np.unique(words)
        logging.info(msg_data_processor_text_processor_unique_words.format(word_counter=len(unique_words)))
        # index words (for finding what prediction means when we get it)
        self.word_index = dict((c, i) for i, c in enumerate(unique_words))
        # create 2 lists: one with words MEMORY_LENGTH previous words,
        # another with the word directly following them
        # TODO: if there are not enough words in memory, switch the word to "empty"
        prev_words = []
        next_words = []
        for i in range(len(words) - MEMORY_LENGTH):
            prev_words.append(words[i:i + MEMORY_LENGTH])
            next_words.append(words[i + MEMORY_LENGTH])
        print(prev_words[0])
        print(next_words[0])
        # init data and label arrays
        processed_data = np.zeros((len(prev_words), MEMORY_LENGTH, len(unique_words)), dtype=bool)
        processed_labels = np.zeros((len(next_words), len(unique_words)), dtype=bool)
        for i, each_words in enumerate(prev_words):
            for j, each_word in enumerate(each_words):
                processed_data[i, j, self.word_index[each_word]] = 1
            processed_labels[i, self.word_index[next_words[i]]] = 1
        # log successful formatting
        logging.info(msg_data_processor_text_processor_data_shape.format(length=processed_data.shape[0],
                                                                         shape=(processed_data.shape[1],
                                                                                processed_data.shape[2])))
        return processed_data, processed_labels

    def prepare_input(self, text):
        x = np.zeros((1, MEMORY_LENGTH, len(self.word_index)))
        for t, word in enumerate(text.split()):
            print(word)
            x[0, t, self.word_index[word]] = 1
        return x


class NNetWordPredictor(object):
    def __init__(self):
        self.model = None

    # model input is a tuple of
    # memory_length (in words) X number_of_unique_words
    def build_model(self, input_shape: tuple):
        # init model
        self.model = Sequential()
        self.model.add(LSTM(128, input_shape=input_shape))
        self.model.add(Dense(input_shape[1]))
        self.model.add(Activation('softmax'))
        # log the result
        logging.info(msg_model_builder_finished)
 #       logger = logging.getLogger(__name__)
#        self.model.summary(print_fn=logger.info)

    # load the wights from previous run
    def load_model(self, path: str):
        # load model
        self.model = keras.models.load_model(path)

    def train_model(self, training_data, training_labels):
        # find the path to weights
        path = os.path.join("../weights", str(MEMORY_LENGTH) + "_next_words_model")
        # callback to save after each epoch
        # callbacks = [
        #     tf.keras.callbacks.ModelCheckpoint(
        #         # Stop training when `val_loss` is no longer improving
        #         filepath=path,
        #         save_best_only=True,  # Only save a model if `val_loss` has improved.
        #         monitor="val_loss",
        #         verbose=1,
        #     )
        # ]

        # compile model
        # self.model.compile(
        #     optimizer=keras.optimizers.RMSprop(learning_rate=1e-2),
        #     loss=keras.losses.CategoricalCrossentropy(),
        #     metrics=[keras.metrics.Accuracy(),],
        # )

        # log the result
        logging.info(msg_train_model_complied)
        # fit the model
        optimizer = RMSprop(lr=0.01)
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        history = self.model.fit(data, labels, validation_split=0.05, batch_size=128, epochs=2, shuffle=True).history

        # save model
        self.model.save(path)

    # TODO: finish predict method
    def predict(self, x):
        self.model.predict(x, verbose=0)[0]
        next_indices = self.sample(preds)

    def sample(self, preds, top_n=3):
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds)
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)

        return heapq.nlargest(top_n, range(len(preds)), preds.take)


if __name__ == "__main__":
    # setup logging
    logging.basicConfig(filename='../logs/NN_predictor_execution.log', filemode='w', level=logging.DEBUG)

    # init data processor
    word_processor = DataProcessor()
    data, labels = word_processor.txt_adapter(training_set_location)
    print(data[0])
    print(labels[0])

    # setup input shape
    shape = (data.shape[1], data.shape[2])

    # init predictor
    predictor = NNetWordPredictor()

    # # load model
    # path = os.path.join("weights", str(MEMORY_LENGTH) + "_next_words_model")
    # predictor.load_model(path)
    #
    # x = word_processor.prepare_input("your life will never be")
    # preds = predictor.predict(x)
    # word_processor.word_index[]


    # set up NN model
    predictor.build_model(shape)

    # find the path to weights


    # train model
    predictor.train_model(data, labels)

