#!/usr/bin/python

# Lexicon for the Spell Check program.

import re
import collections

class Lexicon(object):
    """Class containing valid English words and their frequency.
    """
    
    def __init__(self, lexicon_filename = None, word_list = None):
        """Build lexicon from lexicon_filename.
        
        Arguments:
        - `lexicon_filename`:
        """

        if word_list != None:
            self.set_lexicon(word_list)
            return

        if lexicon_filename == None:
            lexicon_filename = 'words.txt'

        self._lexicon_filename = lexicon_filename
        self.set_lexicon(re.findall('[a-z]+', 
                                    file(lexicon_filename).read().lower()))
    
    def set_lexicon(self, word_list):
        """Set the word_set of this lexicon as word_list."""
        self.word_set = set(word_list)

    # TODO: Optimize this.
    def known_words (self, given_word_list):
        """Return the set of valid words in given_word_list."""
        # TODO: Check if it's better to use if word in self.word_set
        # instead of the method call to is_known_word.
        return [word for word in given_word_list 
                if self.is_known_word(word)]

    def is_known_word(self, word):
        """Return True iff word is in the lexicon.
        
        Arguments:
        - `word`:
        """
        return word in self.word_set

    # TODO: Later this should be based on the fine edit distance cost
    # of the word.
    def get_top_words(self, word_list, num_words_required):
        """Return top num_words_required words from word_list.

        Assumption: The words are all already valid words.
        """
        word_list.sort()
        return word_list[:num_words_required]

if __name__ == "__main__" :
    print get_word_suggestions ("greatz")
