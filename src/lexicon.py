#!/usr/bin/python

# Lexicon for the Spell Check program.

import re
import collections

max_num_word_suggestions = 10

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
        """Set the word list of this lexicon as word_list."""
        self.word_list = word_list

    # TODO: Optimize this.
    def known_words (self, given_word_list):
        """Return the set of valid words in given_word_list."""
        return [word for word in given_word_list 
                if word in self.word_list]

if __name__ == "__main__" :
    print get_word_suggestions ("greatz")
