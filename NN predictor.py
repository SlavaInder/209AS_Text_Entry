# this file makes use of code presented in this resources
# https://medium.com/analytics-vidhya/build-a-simple-predictive-keyboard-using-python-and-keras-b78d3c88cffb

import logging
import numpy as np
import tensorflow as tf
import nltk

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
        logging.info(msg_data_processor_text_adapter_text_fetched.format(file_name))
        # filter text
        text = self.text_filter(text)
        # process text
        data, labels = self.text_processor(text)
        return data, labels

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


class NNetWordPredictor(object):
    def __init__(self):
        self.model = None

    # model input is a tuple of
    # memory_length (in words) X number_of_unique_words
    def build_model(self, input_shape: tuple):
        # init model
        model = tf.keras.Sequential()
        # add LSTM layer
        model.add(tf.keras.layers.LSTM(128, input_shape=input_shape))
        # add fully connected layer
        model.add(tf.keras.layers.Dense(input_shape[1], activation='softmax'))
        # log the result
        logging.info(msg_model_builder_finished)
        logger = logging.getLogger(__name__)
        model.summary(print_fn=logger.info)
        # save the result
        self.model = model

    def train_model(self, data, labels):
        # compile model
        self.model.compile(
            optimizer=tf.keras.optimizers.RMSprop(learning_rate=1e-2),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=[tf.keras.metrics.Accuracy()],
        )
        # log the result
        logging.info(msg_train_model_complied)
        # fit the model
        history = self.model.fit(data,
                                 labels,
                                 validation_split=0.05,
                                 batch_size=128,
                                 epochs=20,
                                 shuffle=True).history

    # TODO: finish predict method
    def predict(self):
        pass


if __name__ == "__main__":
    # setup logging
    logging.basicConfig(filename='logs/NN_predictor_execution.log', filemode='w', level=logging.DEBUG)

    # setup input shape
    shape = (15, 100)

    # init predictor
    predictor = NNetWordPredictor()
    # set up NN model
    predictor.build_model(shape)
    # init data processor
    word_processor = DataProcessor()
    data, labels =
    # train model
    predictor.train_model()

