import itertools, collections, urllib2, math
from word import *

memtable = {}

def find_delete_cost (chars):
    return 0
def find_ex_cost (foo):
    return 0
def find_insert_cost (foo):
    return 0
def find_sub_cost (foo):
    return 0

def generate_all_candidate_suggestions (phrase):
    """ Phrase is either a list of words or a single string.
    returns a list of lists.
    each list is a combination of suggested words corresponding to one
    ord in the phrase."""
    # if type (phrase) != type (list) : phrase = phrase.split ()
    word_suggestions = [get_word_suggestions (word) for word in phrase]
    return [product for product in itertools.product (*word_suggestions)]

def get_likelihood (query, suggestion):
    """ Returns the probability P (query | suggestion)
    Query is a potentially misspelt phrase while suggestion is
    a phrase consisting of dictionary words.

    0 - (edit_dist (q, s) / length (q)) """
    edit_dist = 0
    for corrected_word, misspelt_word in zip (suggestion,
                                              query):
        edit_cost, foobar = get_edits (corrected_word, misspelt_word)
        edit_dist += edit_cost
    return 0 - (edit_dist / len (query))

def get_edits (correct, mistake):
    """ Returns (edit cost, edits string space separated)
        dx means x mapped to _
        ix means _ mapped to x
        sxy means x mapped to y
        exy means x and y were swapped """
    ans = memtable.get (correct + ":" + mistake)
    if ans : return ans

    if mistake == correct : return (0, "")
    if correct == "" : return (len (mistake),
                               "i" + " i".join(list(mistake)))
    if mistake == "" : return (len (correct),
                               "d" + " d".join(list(correct)))

    del_cost, del_ops = get_edits (correct [:-1], mistake)
    del_cost += 1 - find_delete_cost (correct [-2:])
    del_ops += " d" + correct [-1]

    ins_cost, ins_ops = get_edits (correct, mistake [:-1])
    ins_cost += 1 - find_insert_cost (correct [-1] + mistake [-1])
    ins_ops += " i" + mistake [-1]

    sub_cost, sub_ops = get_edits (correct [:-1], mistake [:-1])
    if not correct [-1] == mistake [-1] :
        sub_cost += 1 - find_sub_cost (correct [-1] + mistake [-1])
        sub_ops += " s" + correct [-1] + mistake [-1]

    if del_cost < min (ins_cost, sub_cost) : ans = (del_cost, del_ops)
    elif ins_cost < sub_cost : ans = (ins_cost, ins_ops)
    else : ans = (sub_cost, sub_ops)

    if (len (correct) >= 2
        and len (mistake) >= 2
        and correct [-2:] == mistake [-2:][::-1]):
        ex_cost, ex_ops = get_edits (correct [:-2], mistake [:-2])
        ex_cost += 1 - find_ex_cost (correct [-2:])
        ex_ops += ' e' + correct [-1] + mistake [-1]
        if ans [0] > ex_cost :
            ans = (ex_cost, ex_ops)

    memtable [correct + ":" + mistake] = ans
    return (ans [0], ans [1].strip())

def get_prior (phrase):
    """Returns log (P (phrase)) as given by MS N-gram service."""
    if type (phrase) != str : phrase = " ".join (phrase)
    n_gram_service_url = 'http://web-ngram.research.microsoft.com/rest/lookup.svc/bing-body/jun09/3/jp?u=985fcdfc-9d64-4d03-b650-aabc17f1ea1e'
    prob = urllib2.urlopen (urllib2.Request (n_gram_service_url,
                                             phrase)).read()
    return float(prob.strip())

def get_posterior (suggestion, query):
    return math.exp(get_prior (suggestion) + get_likelihood (query, suggestion))

if __name__ == "__main__":
    for suggestion in generate_all_candidate_suggestions ("i can haz cheezburger".split()) :
        print suggestion
        print get_prior(suggestion)
        # print get_posterior(suggestion, 'cat aret gonne'.split())
        # print " ".join (suggestion)
    # print get_edits ("sujeet", "usjeet")
    # print get_phrase_prior ("I am a dog")
