#!/usr/bin/python

import itertools
import lexicon
from suggestion import Suggestion

# Utility functions for the Spell Check program.
def get_EP(query_list, suggestion_dict, human_suggestion_dict):
    """Return EP for the suggestions as judged by human_suggestion_dict.

    EP: Expected Precision.
    Average over queries in query_list of posteriors for posteriors of
    suggestions that are in the human_suggestion_dict.
    """
    if not query_list:
        return 0.0

    total = sum(sum(posterior
                    for (suggestion, posterior) in suggestion_dict[query] 
                    if suggestion in human_suggestion_dict[query])
                for query in query_list)
    return total / float(len(query_list))

def get_ER(query_list, suggestion_dict, human_suggestion_dict):
    """Return ER for the suggestions as judged by human_suggestion_dict.

    ER: Expected Recall.
    Average over queries in query_list of number of human suggestions
    that have been suggested in suggestion_dict.
    """
    if not query_list:
        return 0.0
    total = sum(sum(1
                    for human_suggestion in human_suggestion_dict[query] 
                    if human_suggestion in zip(*suggestion_dict[query])[0]
                    ) / float(len(human_suggestion_dict[query]))
                for query in query_list if human_suggestion_dict[query])
    return total / float(len(query_list))
            
def get_HM(x, y):
    """Return HM of x and y."""
    if x == 0 or y == 0:
        return 0.0

    return (2 * x * y) / (x + y)

def partition(given_list, indices):
    """Return list of sublists of given_list when partitioned at indices.

    indices: list (not tuple) of indices
    http://stackoverflow.com/questions/1198512/split-a-list-into-parts-based-on-a-set-of-indexes-in-python
    """
    return [given_list[i:j] for i, j in zip([0]+indices, indices+[None])]

def is_sorted(given_list, key = lambda x: x):
    """Return True iff given_list is sorted.
    """
    return all([key(given_list[i]) <= key(given_list[i + 1]) 
                for i in xrange(len(given_list) - 1)])

def get_splits(run_on_word, num_splits, lexicon):
    """Return all possible valid splits for run_on_word.

    TODO: Check for validity of each word.
    TODO: Use DP and memoize valid word splits for substrings.
    """
    # List of all valid indices that a string can be partitioned at.
    all_indices = range(1, len(run_on_word))

    valid_split_indices = itertools.combinations(all_indices, num_splits)
    valid_split_indices = [list(tuple_) for tuple_ in valid_split_indices]
    crude_splits_list = [partition(run_on_word, index_list) 
                         for index_list in valid_split_indices]

    return [str_tuple for str_tuple in crude_splits_list 
            if all(lexicon.is_known_word(word) for word in str_tuple)]

def get_corrected_run_on_queries(query, lexicon):
    """Correct run-on query by splitting run-on words.

    Return list of phrase/sentence queries with any run-on word split.

    Assumption: A maximum of max_num_splits words have been joined together.
    Arguments:
    - `query`: Suggestion object
    - `lexicon`: lexicon of the spell checker
    """
    max_num_splits = 3
    print query
    # List of list of suggestions for each word
    term_suggestions_list = [
        list(itertools.chain(*[get_splits(word, i, lexicon) 
                               for i in xrange(1, max_num_splits + 1)])) + [[word]] 
                               for word in query]
    print 'term_suggestions_list', term_suggestions_list

    # All term_combos (considering only one word to be a run-on word
    # at a time)
    term_combos = [list(itertools.chain(*tuple_))
                   for i in xrange(len(query))
                   for tuple_ in itertools.product([query[:i]], 
                                                   term_suggestions_list[i], 
                                                   [query[i + 1:]])]
    
    print 'term_combos', term_combos
    term_combos.sort()
    # Remove duplicates
    # This requires that keys with same value be consecutive (hence sort).
    term_combos = [key for key, _ in itertools.groupby(term_combos)]
    print 'term_combos', term_combos
    term_combos.remove(query)
    print 'term_combos', term_combos
    return [Suggestion(term_combo, suggestion_type = 
                       'sentence' if query.suggestion_type == 'sentence' else 'phrase') 
                       for term_combo in term_combos]

def get_corrected_split_queries(query, lexicon):
    """Correct split query by joining words.

    Return list of word/phrase/sentence queries with the split words joined.

    Assumption: a word has been split only once.
    Note: The original query is NOT part of the returned list.

    Arguments:
    - `query`: Suggestion object
    - `lexicon`: lexicon of the spell checker
    """
    # TODO: Should probably check to see if the resultant suggestion
    # is a word/phrase/suggestion and then set its suggestion_type.
    # eg. 'No w.' (sentence) -> 'Now.' (word)
    joined_up_suggestion_list = [
        Suggestion(query[:i] + [query[i] + query[i + 1]] + query[i+2:], 
                   suggestion_type = query.suggestion_type)
        for i in range(len(query) - 1)
        if lexicon.is_known_word(query[i] + query[i + 1])]
    return joined_up_suggestion_list

def get_normalized_probabilities(probability_list):
    """Return probability_list with the values normalized.
    
    Arguments:
    - `probability_list`:
    """
    total = float(sum(probability_list))
    return [prob / total for prob in probability_list]
