# this file makes use of code presented in this resources
# https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1
# https://github.com/npezolano/Python-T9-implementation
# performance can be improved by hard-coding KEY_TO_LET correspondence
import logging


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
    def __init__(self):
        self.children = []

    # perform tree setup on a given file
    def train(self,  file_name: str):
        pass

    # predict a typed word
    def predict(self, keys: list):
        pass

    # update the trie with a new word
    def update(self, word: str):
        # init node reference
        current_node = None
        # update the log file
        logging.debug("update method started working on word %s", word)
        logging.debug("update method processes letter %s", word[0])
        # if corresponding node already exists, get it
        for child in self.children:
            if child.symbol == LET_TO_KEY[word[0]]:
                current_node = child
        # if there is no node to be found, create one
        if current_node is None:
            self.children.append(TrieNode(LET_TO_KEY[word[0]]))
            current_node = self.children[-1]

        # process all letters of the word until the last one
        for letter in word[1:-1]:
            # init temp node reference
            temp_node = None
            # log update stage
            logging.debug("update method processes letter %s", letter)
            # check if corresponding node already exists
            for child in current_node.children:
                if child.symbol == LET_TO_KEY[letter]:
                    temp_node = child
            # if there is no node to be found, create one
            if temp_node is None:
                current_node.children.append(TrieNode(LET_TO_KEY[letter]))
                temp_node = current_node.children[-1]
            # switch to temp node
            current_node = temp_node

        # process the last letter of the node




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
