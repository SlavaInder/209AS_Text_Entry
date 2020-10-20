# this file makes use of code presented in this resources
# https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1
# https://github.com/npezolano/Python-T9-implementation
# performance can be improved by hard-coding KEY_TO_LET correspondence
# there is no capital letters in the testing set so we shouldn't differentiate between them and lower case letters
import logging


# set info messages for prediction
predict_start = "predict method started working on seq {seq}"
predict_node_search = "predict method searches for node {node}"
predict_node_not_found = "node {node} is not found. Prediction is empty"
# set info messages for update
upd_start = "update method started working on word {word}"
upd_node_search = "update method processes letter {letter}"
upd_node_not_found = "Node {node} is not found. Creating node {node}"
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

    # perform tree setup on a given file
    def train(self,  file_name: str, depth: int):
        pass

    # func to predict a typed word
    # returns a list of possible words in order from
    # the most probable to the least probable
    def predict(self, seq: str):
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
        # init prediction dictionary
        prediction_dict = {}
        #prediction_dict + current_node.words



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
    t9 = Trie()
    t9.update("Slava")
    t9.update("Slavb")
    t9.update("Slaba")
    t9.update("Slbva")
    t9.update("Sbava")
    t9.update("Blava")
    logging.info(str(t9))
    t9.predict("75")
    t9.predict("21")
    t9.predict("31")
