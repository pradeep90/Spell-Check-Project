#!/usr/bin/python

import itertools, collections, urllib2, math
from accepts_decorator import accepts, returns
# from word import *

memtable = {}
delete_table = []
insert_table = []
sub_table = []
ex_table = []

STRONG = 2

def _ord (letter):
    return ord (letter) - ord ('a')

def read_table (filename):
    """ Returns a list lists. Each list has 26 numbers.
    ret_val [0] [2] means table [a, c] """
    table = [map (int, line.strip().split())
             for line in file (filename).readlines()
             if line.strip()]
    for row in table :
        if len (row) != 26 :
            print filename
            print ' '.join (map (str, row))
    return table


def find_delete_cost (chars):
    """
    chars : xy
    returns : the cost with which y can get deleted in the process
              of misspelling when x occurs before it.
              (between 0 and 1)"""
    # return 1
    global delete_table
    if not delete_table :
        delete_table = read_table ('../data/deletion_table.txt')

    freq = 0
    if len (chars) == 1:
        # First letter being deleted.
        freq = delete_table [-1] [_ord (chars)]
    else :
        freq = delete_table [_ord (chars[0])] [_ord (chars[1])]

    if freq : return 1.0/freq
    else : return 1

def find_insert_cost (chars):
    """
    chars : xy
    returns : the cost with which y can get inserted in the process
              of misspelling when x occurs before it.
              (between 0 and 1)"""
    # return 1
    global insert_table
    if not insert_table :
        insert_table = read_table ('../data/insertion_table.txt')

    freq = 0
    if len (chars) == 1:
        # First letter being insertd.
        freq = insert_table [-1] [_ord (chars)]
    else :
        freq = insert_table [_ord (chars[0])] [_ord (chars[1])]

    if freq : return 1.0/freq
    else : return 1

def find_ex_cost (chars):
    """
    chars : xy
    returns : the cost with which
              xy becomes yx
              (between 0 and 1)"""
    # return 1
    global ex_table
    if not ex_table :
        ex_table = read_table ('../data/swap_table.txt')

    freq = ex_table [_ord (chars[0])] [_ord (chars[1])]
    if freq : return 1.0/freq
    else : return 1

def find_sub_cost (chars):
    """
    chars : xy
    returns : the cost with which
              x becomes y
              (between 0 and 1)"""
    # return 1
    global sub_table
    if not sub_table :
        sub_table = read_table ('../data/sub_table.txt')

    # Note chars1 before chars0
    # That's the way the table in the paper is given.
    freq = sub_table [_ord (chars[1])] [_ord (chars[0])]
    if freq : return 1.0/freq
    else : return 1

def generate_all_candidate_suggestions (phrase):
    """ Phrase is either a list of words or a single string.
    returns a list of lists.
    each list is a combination of suggested words corresponding to one
    ord in the phrase."""
    # if type (phrase) != type (list) : phrase = phrase.split ()
    word_suggestions = [get_word_suggestions (word) for word in phrase]
    return [product for product in itertools.product (*word_suggestions)]

@accepts(list, list)
def get_likelihood (query, suggestion):
    """ Returns an approximation of P (query | suggestion).

    Query is a potentially misspelt phrase while suggestion is
    a phrase consisting of dictionary words.

    Likelihood = -(edit_dist (q, s) / total_length (q)).
    - 1 <= Likelihood <= 0

    TODO: Deal with the cases where the number of terms in the
    suggestion and query are different (eg. run-on and split queries).

    Arguments:
    - `query`: List of terms
    - `suggestion`: List of terms
    """
    # TODO: If number of terms is different just remove all spaces in
    # the phrase/sentence and treat it as one string.

    print 'query', query
    print 'suggestion', suggestion

    print zip(suggestion, query)
    edit_distance = sum(get_edits(correct_word, misspelt_word)[0] 
                        for correct_word, misspelt_word 
                        in zip(suggestion, query))
    query_string_length = len(''.join(query))
    return -(edit_distance / query_string_length)

def get_edits (correct, mistake):
    """ Returns (edit cost, edits string space separated)
        dx means x mapped to _
        ix means _ mapped to x
        sxy means x mapped to y
        exy means x and y were swapped """
    print 'get_edits', correct, mistake
    ans = memtable.get (correct + ":" + mistake)
    if ans : return ans

    if mistake == correct : return (0, "")
    if correct == "" : return (len (mistake),
                               "i" + " i".join(list(mistake)))
    if mistake == "" : return (len (correct),
                               "d" + " d".join(list(correct)))

    del_cost, del_ops = get_edits (correct [:-1], mistake)
    del_cost += find_delete_cost (correct [-2:])
    del_ops += " d" + correct [-1]

    ins_cost, ins_ops = get_edits (correct, mistake [:-1])
    ins_cost += find_insert_cost (correct [-1] + mistake [-1])
    ins_ops += " i" + mistake [-1]

    sub_cost, sub_ops = get_edits (correct [:-1], mistake [:-1])
    if not correct [-1] == mistake [-1] :
        sub_cost += find_sub_cost (correct [-1] + mistake [-1])
        sub_ops += " s" + correct [-1] + mistake [-1]

    if del_cost < min (ins_cost, sub_cost) : ans = (del_cost, del_ops)
    elif ins_cost < sub_cost : ans = (ins_cost, ins_ops)
    else : ans = (sub_cost, sub_ops)

    if (len (correct) >= 2
        and len (mistake) >= 2
        and correct [-2:] == mistake [-2:][::-1]):
        ex_cost, ex_ops = get_edits (correct [:-2], mistake [:-2])
        ex_cost += find_ex_cost (correct [-2:])
        ex_ops += ' e' + correct [-1] + mistake [-1]
        if ans [0] > ex_cost :
            ans = (ex_cost, ex_ops)

    memtable [correct + ":" + mistake] = ans
    # print correct, mistake
    return (ans [0], ans [1].strip())

def get_prior (phrase):
    """Returns log (P (phrase)) as given by MS N-gram service."""
    if type (phrase) != str : phrase = " ".join (phrase)
    n_gram_service_url = 'http://web-ngram.research.microsoft.com/rest/lookup.svc/bing-body/jun09/3/jp?u=985fcdfc-9d64-4d03-b650-aabc17f1ea1e'
    print 'get_prior', phrase
    prob = urllib2.urlopen (urllib2.Request (n_gram_service_url,
                                             phrase)).read()
    return float(prob.strip())

@accepts(list, list)
def get_posterior (suggestion, query):
    """Return P(suggestion | query).

    Arguments:
    - `query`: List of strings representing terms
    - `suggestion`: List of strings representing terms
    """
    return math.exp(get_prior (suggestion) + get_likelihood (query, suggestion))

if __name__ == "__main__":
    # print get_edits ("belie", "belive")
    # print get_posterior (["belie"], ["belive"])
    # for suggestion in generate_all_candidate_suggestions ("i can haz cheezburger".split()) :
    #     print suggestion
    #     print get_prior(suggestion)
        # print get_posterior(suggestion, 'cat aret gonne'.split())
        # print " ".join (suggestion)
    # print get_edits ("sujeet", "usjeet")
    # pass

    # Test the `accepts` decorator
    @accepts(list, int, int)
    @returns(float)
    def average(x, y, z):
        return (x[0] + y + z) / 2
    average([13], 10, 15.0)
    average([3], 10, 15)
