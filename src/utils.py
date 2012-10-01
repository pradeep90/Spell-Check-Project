#!/usr/bin/python

import itertools

# Utility functions for the Spell Check program.

def get_EP(query_list, suggestion_dict, human_suggestion_dict):
    """Return EP for the suggestions as judged by human_suggestion_dict.

    EP: Expected Precision.
    Average over queries in query_list of posteriors for those
    suggestions that are in the human_suggestion_dict.
    """
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
    total = sum(sum(1
                    for human_suggestion in human_suggestion_dict[query] 
                    if human_suggestion in zip(*suggestion_dict[query])[0]
                    ) / float(len(human_suggestion_dict[query]))
                for query in query_list)
    return total / float(len(query_list))
            
def get_HM(x, y):
    """Return HM of x and y."""
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

def get_splits(run_on_word, num_splits):
    """Return all possible valid splits for run_on_word.

    TODO: Check for validity of each word.
    TODO: Use DP and memoize valid word splits for substrings.
    """
    # List of all valid indices that a string can be partitioned at.
    all_indices = range(1, len(run_on_word))

    valid_split_indices = itertools.combinations(all_indices, num_splits)
    valid_split_indices = [list(tuple_) for tuple_ in valid_split_indices]
    return [partition(run_on_word, index_list) 
            for index_list in valid_split_indices]

def get_corrected_run_on_queries(query):
    """Correct run-on query by splitting run-on words.

    Return list of phrase/sentence queries with any run-on word split.

    Assumption: max two words have been joined together.
    TODO: Remove the original query from the final list. It will be
    present cos of the cross-product.
    TODO: Not checking for valid words now.

    Arguments:
    - `query`: list of word(s)
    """
    term_suggestions_list = [get_splits(word, 1) + [[word]] for word in query]
    crude_suggestions_list = itertools.product(*term_suggestions_list)
    # Note: crude_suggestions_list for [foobar, yoboyz] will contain 
    # ([foo bar], [yo boyz],)
    # whereas we want 
    # [foo bar yo boyz]
    split_suggestions_list = [list(itertools.chain(*incomplete_suggestion)) 
                              for incomplete_suggestion in crude_suggestions_list]
    return split_suggestions_list

def get_corrected_split_queries(query):
    """Correct split query by joining words.

    Return list of word/phrase/sentence queries with the split words joined.

    Assumption: a word has been split only once.
    Note: The original query is NOT part of the returned list.
    TODO: Not filtering using valid words now.

    Arguments:
    - `query`: list of word(s)
    """
    joined_up_suggestion_list = [query[:i] + [query[i] + query[i + 1]] + query[i+2:]
                                 for i in range(len(query) - 1)]
    return joined_up_suggestion_list

def get_normalized_probabilities(probability_list):
    """Return probability_list with the values normalized.
    
    Arguments:
    - `probability_list`:
    """
    total = float(sum(probability_list))
    return [prob / total for prob in probability_list]
