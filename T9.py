# this file makes use of code presented in this resources
# https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1
# https://github.com/npezolano/Python-T9-implementation
import logging


mapping = {1: ["'"],
           2: ["a", "A", "b", "B", "c", "C"],
           3: ["d", "D", "e", "E", "f", "F"],
           4: ["g", "G", "h", "H", "i", "I"],
           5: ["j", "J", "k", "K", "l", "L"],
           6: ["m", "M", "n", "N", "o", "O"],
           7: ["p", "P", "q", "Q", "r", "R", "s", "S"],
           8: ["t", "T", "u", "U", "v", "V"],
           9: ["w", "W", "x", "X", "y", "Y", "z", "Z"]}


class Trie(object):
    def __init__(self):
        self.root = None


class TrieNode(object):
    def __init__(self, char: str):
        self.symbol = char
        self.children = []
        # Is it the last character of the word.`
        self.word_finished = False
        # How many times this character appeared in the addition process
        self.counter = 1


if __name__ == "__main__":
    # setup logging
    logging.basicConfig(filename='logs/T9_execution.log', level=logging.DEBUG)
    t9 = Trie()
