#!/usr/bin/python

# Edit Distance calculator

class EditDistanceCalculator(object):
    """Class for calculating Edit Distance between strings."""
    
    def __init__(self, lexicon):
        """Initialize lexicon.
        """
        self.lexicon = lexicon

    # Source : http://norvig.com/spell-correct.html
    def words_one_edit_away (self, word):
        """Given a word, return a list of strings one edit distance away.

        Note: the strings returned need not be valid words.
        """
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
        inserts    = [a + c + b     for a, b in splits for c in alphabet]
        return list(set(deletes + transposes + replaces + inserts))

    def words_two_edits_away (self, word):
        """Given a word, return a list of strings two edit distance away.
        
        Note: the strings returned need not be valid words.
        """
        return list(set(e2 for e1 in
                        self.words_one_edit_away (word) 
                        for e2 in self.words_one_edit_away (e1) 
                        if self.lexicon.is_known_word(e2)))

    def known_words_one_edit_away (self, word):
        return self.lexicon.known_words (self.words_one_edit_away (word))

    def known_words_two_edits_away (self, word):
        return self.lexicon.known_words (self.words_two_edits_away (word))

    def get_most_frequent_n_words (self, word_set, lexicon, n):
        """Returns a set of most frequent n words from word_set using
        the frequencies from the lexicon"""
        word_set = list (word_set)
        word_set.sort (key = lexicon.get, reverse = True)
        return set (word_set [:n])

