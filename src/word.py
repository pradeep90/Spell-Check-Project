# Contains functions related to individual word phase of spell checking.
import re, collections

max_num_word_suggestions = 10
lexicon_filename = "words.txt"

def build_frequency_dict_from_list (lst):
    """ input example : [a, b, a, a, k, k]
    output example : {a:3, b:1, k:2}
    Output dict keys are input lst members and values are their counts
    in the same."""
    dictionary = collections.defaultdict (lambda : 1)
    for word in lst:
        dictionary[word] += 1
    return dictionary

# lexicon is a dictionary. Keys are words and values are frequency of the
# key in lexicon_file
lexicon = build_frequency_dict_from_list (
    re.findall ('[a-z]+', file(lexicon_filename).read().lower()))

# Source : http://norvig.com/spell-correct.html
def words_one_edit_away (word):
    """ Given a word, returns a set of strings one edit distance away.
    Note that the strings returned need not be valid words."""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts    = [a + c + b     for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def words_two_edits_away (word):
    """ Given a word, returns a set of strings two edit distance away.
    Note that the strings returned need not be valid words."""
    return set(e2 for e1 in
               words_one_edit_away (word) for e2 in
               words_one_edit_away (e1))

def known_words (word_set, lexicon):
    """Lexicon is a dictionary with keys as valid words and
    word_set is a set of strings.
    returns the set of valid words belonging to word_set."""
    return word_set.intersection (lexicon)

def known_words_one_edit_away (word):
    return known_words (words_one_edit_away (word),
                        lexicon)

def known_words_two_edits_away (word):
    return known_words (words_two_edits_away (word),
                        lexicon)

def get_most_frequent_n_words (word_set, lexicon, n):
    """Returns a set of most frequent n words from word_set using
    the frequencies from the lexicon"""
    word_set = list (word_set)
    word_set.sort (key = lexicon.get, reverse = True)
    return set (word_set [:n])

def get_word_suggestions (word):
    """Returns :
    - word itself if it is valid
    - max_num_word_suggestions number of most frequent words out of
      the valid words within an edit distance of 1.
    - if no words within edit distance of 1, then go for 2 edit dist.
    - word itsef if both of the above fail."""
    return (known_words (set([word]), lexicon)
            or
            get_most_frequent_n_words (known_words_one_edit_away (word),
                                       lexicon,
                                       max_num_word_suggestions)
            or
            get_most_frequent_n_words (known_words_two_edits_away (word),
                                       lexicon,
                                       max_num_word_suggestions)
            or
            set([word]))

if __name__ == "__main__" :
    print get_word_suggestions ("greatz")
