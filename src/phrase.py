import itertools
from word import *

def generate_all_candidate_suggestions (phrase):
    """Phrase is either a list of words or a single string.
    returns a list of lists.
    each list is a combination of suggested words corresponding to one
    ord in the phrase."""
    if type (phrase) != type (list) : phrase = phrase.split ()
    word_suggestions = [get_word_suggestions (word) for word in phrase]
    return [product for product in itertools.product (*word_suggestions)]

if __name__ == "__main__":
    for suggestion in generate_all_candidate_suggestions ("cat aret gonne") :
        print " ".join (suggestion)
