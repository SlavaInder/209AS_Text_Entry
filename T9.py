# this file makes use of code presented in this resources
# https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1
# https://github.com/npezolano/Python-T9-implementation
# and dataset presented here (don't forget to site in the presentations!)
# https://www.kaggle.com/rtatman/the-national-university-of-singapore-sms-corpus
# used tis code fragment for filtering
# https://www.kite.com/python/answers/how-to-remove-non-ascii-characters-in-python
# performance can be improved by hard-coding KEY_TO_LET correspondence
# there is no capital letters in the testing set so we shouldn't differentiate between them and lower case letters
import logging
import json
import pandas as pd


# set info messages for json adapter
json_file = "json adapter received {file}"
json_data = "json adapter fetched data\n{data}"
json_msg = "json adapter processes message\n{msg}"
# set info messages for training
train_text_raw = "train method received raw text:\n{text}"
train_text_filtered = "train method filtered all prepositions:\n{text}"
train_unable_to_filter = "train method can not process this text"
train_word = "train method processes word {word}"
train_add = "train method adds word {word} to the trie"
# set info messages for prediction
predict_start = "predict method started working on seq {seq}"
predict_node_search = "predict method searches for node {node}"
predict_node_not_found = "node {node} is not found. Prediction is empty"
predict_added = "predictions of the node {node} (depth level = {depth}) are included"
predict_count = "on the depth level {depth} prediction considers {node_num} node(s)"
predict_unsorted = "the dictionary of all possible predictions is:\n{predict}"
predict_sorted = "the sorted list of all possible predictions is:\n{predict}"
predict_empty = "prediction is empty"
# set info messages for update
upd_start = "update method started working on word {word}"
upd_node_search = "update method processes letter {letter}"
upd_node_not_found = "Node {node} is not found. Creating node {node}"
# dummy text
dummy = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna
aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""
# symbols to replace
for_replacement = "1234567890=+-!?&.,:;%^_<>#\\*\'\"@\n\t$()/~"
# set up forward mapping
KEY_TO_LET = {"1": ["'"],
              "2": ["a", "A", "b", "B", "c", "C"],
              "3": ["d", "D", "e", "E", "f", "F"],
              "4": ["g", "G", "h", "H", "i", "I"],
              "5": ["j", "J", "k", "K", "l", "L"],
              "6": ["m", "M", "n", "N", "o", "O"],
              "7": ["p", "P", "q", "Q", "r", "R", "s", "S"],
              "8": ["t", "T", "u", "U", "v", "V"],
              "9": ["w", "W", "x", "X", "y", "Y", "z", "Z"]}
# set up backwards mapping
LET_TO_KEY = {}
for key in KEY_TO_LET.keys():
    for value in KEY_TO_LET[key]:
        LET_TO_KEY[value] = key


class Trie(object):
    def __init__(self, letters_ahead=0):
        self.children = []
        self.letters_ahead = letters_ahead

    # perform training on the text from json doc
    def json_train_adapter(self, file_name: str, portion=1):
        # start logging
        logging.debug(json_file.format(file=file_name))
        # load the data
        with open(file_name, "r") as f:
            data = json.load(f)
        data = data['smsCorpus']['message']
        data = pd.DataFrame(data)
        data = data[['@id', 'text']]
        data = pd.DataFrame(data)
        data = data['text']
        # log the data
        logging.debug(json_data.format(data=data))
        # process each message
        for i in range(1000):
            logging.debug(json_msg.format(msg=data[i]['$']))
            self.train(data[i]['$'])

    # perform tree setup on a given text
    def train(self, text: str):
        # start logging
        logging.debug(train_text_raw.format(text=text))
        try:
            # remove all dots, commas, question marks, exclamation marks, tabulations, new strings
            for char in for_replacement:
                text = text.replace(char, " ")
            # remove all non printable symbols
            encoded_string = text.encode("ascii", "ignore")
            text = encoded_string.decode()
        except AttributeError:
            # report error
            logging.debug(train_unable_to_filter)
            return
        # log filtered text
        logging.debug(train_text_filtered.format(text=text))
        # add each word of the remained text to the trie
        for word in text.split(" "):
            logging.debug(train_word.format(word=word))
            # if the word is not empty, add it to the trie
            if word != "":
                logging.debug(train_add.format(word=word))
                self.update(word)

    # func to predict a typed word
    # returns a list of possible words in order from
    # the most probable to the least probable
    def predict(self, seq: str, depth=3):
        # init node reference
        current_node = None
        # update the log file
        logging.debug(predict_start.format(seq=seq))
        logging.debug(predict_node_search.format(node=seq[0]))
        # check if there is a corresponding node
        for child in self.children:
            if child.symbol == seq[0]:
                current_node = child
        # if there is no, we can not give a prediction
        if current_node is None:
            logging.debug(predict_node_not_found.format(node=seq[0]))
            return []

        # if there is, traverse the trie if possible
        for num in seq[1:]:
            # init temp node reference
            temp_node = None
            # log update stage
            logging.debug(predict_node_search.format(node=num))
            # check if corresponding node already exists
            for child in current_node.children:
                if child.symbol == num:
                    temp_node = child
            # if there is no node to be found, we can not give a prediction
            if temp_node is None:
                logging.debug(predict_node_not_found.format(node=num))
                return []
            # else switch to the next node
            else:
                current_node = temp_node

        # after traversing until the end, we can start give predictions
        # search for children nodes until specified depth is reached
        # to do so, find children of all nodes in array $depth times
        # starting from current node
        node_array = [current_node]
        for i in range(depth):
            current_len = len(node_array)
            logging.debug(predict_count.format(depth=i, node_num=current_len))
            for j in range(current_len):
                for child in node_array[j].children:
                    if child not in node_array:
                        node_array.append(child)
                        logging.debug(predict_added.format(depth=0, node=child.symbol))
        # init prediction dictionary
        prediction_dict = {}
        # update prediction dictionary with all possible predictions
        for node in node_array:
            prediction_dict.update(node.words)
        # log the results
        logging.debug(predict_unsorted.format(predict=prediction_dict))
        # if prediction dict is empty
        if prediction_dict is bool:
            logging.debug(predict_empty)
            return []
        else:
            # else sort it
            prediction_dict = prediction_dict.items()
            prediction_dict = sorted(prediction_dict, key=lambda x: x[1], reverse=True)
            # and remove values from keys
            prediction_list = []
            for item in prediction_dict:
                prediction_list.append(item[0])
            # log the result
            logging.debug(predict_sorted.format(predict=prediction_list))
        return prediction_list

    # update the trie with a new word
    def update(self, word: str):
        # fix upper-case letters
        word = word.lower()
        # init node reference
        current_node = None
        # update the log file
        logging.debug(upd_start.format(word=word))
        logging.debug(upd_node_search.format(letter=word[0]))
        # if corresponding node already exists, get it
        for child in self.children:
            if child.symbol == LET_TO_KEY[word[0]]:
                current_node = child
        # if there is no node to be found, create one
        if current_node is None:
            logging.debug(upd_node_not_found.format(node=LET_TO_KEY[word[0]]))
            self.children.append(TrieNode(LET_TO_KEY[word[0]]))
            current_node = self.children[-1]

        # process all letters of the word until the last one
        for letter in word[1:-1]:
            # init temp node reference
            temp_node = None
            # log update stage
            logging.debug(upd_node_search.format(letter=letter))
            # check if corresponding node already exists
            for child in current_node.children:
                if child.symbol == LET_TO_KEY[letter]:
                    temp_node = child
            # if there is no node to be found, create one
            if temp_node is None:
                logging.debug(upd_node_not_found.format(node=LET_TO_KEY[letter]))
                current_node.children.append(TrieNode(LET_TO_KEY[letter]))
                temp_node = current_node.children[-1]
            # switch to temp node
            current_node = temp_node

        # process the last letter of the node
        logging.debug(upd_node_search.format(letter=word[-1]))
        temp_node = None
        # check if corresponding node already exists
        for child in current_node.children:
            if child.symbol == LET_TO_KEY[word[-1]]:
                temp_node = child
                # if it exists, check whether this word was already encountered before
                if word in temp_node.words.keys():
                    # if it was, increase frequency for this word
                    temp_node.words[word] += 1
                else:
                    # if it was not, create a new entry
                    temp_node.words[word] = 1
        # if there is no node to be found, create one
        if temp_node is None:
            logging.debug(upd_node_not_found.format(node=LET_TO_KEY[word[-1]]))
            current_node.children.append(TrieNode(LET_TO_KEY[word[-1]]))
            temp_node = current_node.children[-1]
            # and create an entry
            temp_node.words[word] = 1

    # def __str__(self):
    #     # init trie root
    #     out = "\nroot\n"
    #     # for each child of the root
    #     for i in range(len(self.children)):
    #         # place child first
    #         child_out = "|-" + self.children[i].symbol + "\n"
    #         # choose prefix
    #         if i < len(self.children) - 1: prefix = "|"
    #         else: prefix = "|"
    #         out += child_out
    #
    #     return out


class TrieNode(object):
    def __init__(self, char: str):
        self.symbol = char
        self.children = []
        self.words = {}


if __name__ == "__main__":
    # setup logging
    logging.basicConfig(filename='logs/T9_execution.log', filemode='w', level=logging.DEBUG)
    # init trie
    t9 = Trie()
    # train from text
    # t9.train(dummy)
    # specify training data
    training_set_location = "./training_sets/smsCorpus_en_2015.03.09_all.json"
    # train trie
    t9.json_train_adapter(training_set_location)

    print(t9.predict("44"))

    # t9.update("Slava")
    # t9.update("Slava")
    # t9.update("Slava")
    # t9.update("Slavf")
    # t9.update("Slavo")
    # t9.update("Slavo")
    # t9.predict("75282")
    # t9.predict("7528")
    # t9.predict("752")
    # t9.predict("75")
    # t9.predict("7")
