#!/usr/bin/python

# Lexicon for the Spell Check program.

import re
import collections

class Lexicon(object):
    """Class containing valid English words and their frequency.
    """

    small_nonsense_words = [
        'Ag', 'Al', 'Am', 'Ar', 'Au', 'Av', 'B', 'Be', 'Bi', 'Bk', 'Br', 
        'C', 'Ca', 'Cd', 'Cf', 'Ci', 'Cl', 'Cm', 'Co', 'Cr', 'Cs', 'Cu', 
        'D', 'Di', 'Dr', 'E', 'Er', 'Es', 'Eu', 'F', 'Fe', 'Fm', 'Fr', 
        'G', 'GE', 'Ga', 'Gd', 'Ge', 'H', 'Hf', 'Hg', 'Hz', 'I', 'In', 
        'Io', 'Ir', 'It', 'J', 'Jo', 'Jr', 'K', 'Kr', 'L', 'La', 'Le', 
        'Li', 'Ln', 'Lr', 'Lt', 'Lu', 'M', 'Mb', 'Md', 'Mg', 'Mn', 'Mo', 
        'Mr', 'Ms', 'Mt', 'N', 'Na', 'Nb', 'Nd', 'Ne', 'Ni', 'Np', 'O', 
        'Os', 'P', 'Pb', 'Pd', 'Pl', 'Pm', 'Po', 'Pt', 'Pu', 'Q', 'R', 
        'Ra', 'Rb', 'Rd', 'Re', 'Rh', 'Rn', 'Ru', 'Rx', 'S', 'Sb', 'Sc', 
        'Se', 'Si', 'Sm', 'Sn', 'Sq', 'Sr', 'St', 'T', 'Ta', 'Tb', 'Tc', 
        'Th', 'Ti', 'Tl', 'Tm', 'Ty', 'U', 'Ur', 'V', 'Va', 'W', 'Wm', 
        'Wu', 'X', 'Xe', 'Y', 'Yb', 'Z', 'Zn', 'Zr', 'b', 'c', 'cs', 
        'd', 'dB', 'e', 'em', 'es', 'ex', 'f', 'fa', 'g', 'gs', 'h', 
        'he', 'i', 'j', 'k', 'kW', 'kc', 'ks', 'l', 'la', 'lo', 'ls', 
        'm', 'ma', 'mi', 'ms', 'mu', 'n', 'nu', 'o', 'p', 'pH', 'pa', 
        'q', 'r', 're', 's', 'sh', 't', 'ti', 'ts', 'u', 'uh', 'um', 
        'v', 'vs', 'w', 'x', 'y', 'ya', 'ye', 'z'
        ]
    
    def __init__(self, lexicon_filename = None, word_list = None):
        """Build lexicon from lexicon_filename.
        
        Arguments:
        - `lexicon_filename`:
        """

        if word_list != None:
            self.set_lexicon(word_list)
            return

        if lexicon_filename == None:
            # lexicon_filename = 'all-words.txt'
            lexicon_filename = 'decently-big-words.txt'

        self._lexicon_filename = lexicon_filename
        self.set_lexicon(self.get_words_from_lexicon_file(open(self._lexicon_filename)))

    def get_words_from_lexicon_file(self, lexicon_file):
        """Return list of words from lexicon_file.
        """
        prog = re.compile('^[a-zA-z][a-z]+$')
        return [prog.match(line.lower().strip()).group(0) for line in lexicon_file 
                if prog.match(line.strip())]

    def set_lexicon(self, word_list):
        """Set the word_set of this lexicon as word_list."""
        self.word_set = set([word for word in word_list 
                             if word not in self.small_nonsense_words])

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
    test_lexicon = Lexicon()
    test_lexicon.get_words_from_lexicon_file(open(test_lexicon._lexicon_filename))
