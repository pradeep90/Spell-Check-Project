#!/usr/bin/python

import itertools

# Program to correct spelling errors.

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
    print valid_split_indices
    return [partition(run_on_word, index_list) 
            for index_list in valid_split_indices]

def get_corrected_run_on_queries(query):
    """Return list of phrases/sentences queries with any run-on word split.

    Assumption: max three words have been joined together.
    Arguments:
    - `query`: list of word(s)
    """
    pass

class SpellChecker(object):
    """Suggest corrections for errors in queries.
    """

    def __init__(self):
        """Initialize all the dicts for suggestions, etc.
        """
        self.suggestion_dict = {}

    def run_spell_check(self, query_list):
        """Run spell check on queries in query_list and store the suggestions.
        
        Arguments:
        - `query_list`:
        """
        self.query_list = query_list
        for query in self.query_list:
            self.suggestion_dict[query] = self.generate_suggestions_and_posteriors(
                query)
    
    # To be tested once the rest is done 
    def generate_suggestions_and_posteriors(self, query):
        """Return (suggestion, posterior) pairs for query.

        Get a list of candidate suggestions and calculate posteriors
        for each of them.

        Arguments:
        - `query`: list of word(s) making up the word/phrase/sentence
          query.
        """
        # List of list of possibilities for each term
        all_term_possibilities = [generate_candidate_terms(term) for term in query]

        # Lust of all suggestions
        all_suggestions = generate_candidate_suggestions(all_term_combinations)

        posteriors = [get_posterior(suggestion, query) 
                      for suggestion in all_suggestions]

        normalized_posteriors = get_normalized_probabilities(posteriors)

        return zip(all_suggestions, normalized_posteriors)
        
        # suggestions = ["believe", "buoyant", "committed", "distract", 
        #                "ecstacy", "fairy", "hello", "gracefully", 
        #                "liaison", "occasion", "possible", "throughout", 
        #                "volley", "tattoos", "respect"]

        # posteriors = [0.11, 0.02, 0.15, 0.04, 0.04, 0.05, 0.02, 0.06, 0.07, 
        #               0.1, 0.01, 0.03, 0.07, 0.04, 0.19]
        # return zip(suggestions, posteriors)

    def get_EF1_measure(self, human_suggestion_dict):
        """Return EF1 value for the performance as judged by human_suggestion_dict.
        
        Arguments:
        - `human_suggestion_dict`: dict of query -> list of
          human-annotated suggestions
        """
        args = [self.query_list, self.suggestion_dict, human_suggestion_dict]
        return get_HM (get_EP(*args),
                       get_ER(*args))
    
    def get_all_stats(self, human_suggestion_dict):
        """Return [EP, ER, EF1] for performance as judged by human_suggestion_dict.
        
        Arguments:
        - `human_suggestion_dict`:
        """
        args = [self.query_list, self.suggestion_dict, human_suggestion_dict]
        return [get_EP(*args), get_ER(*args), 
                self.get_EF1_measure(human_suggestion_dict)]

if __name__ == '__main__':
    spell_checker = SpellChecker()
    spell_checker.run_spell_check(['yo', 'boyz'])
    human_dict = { 'yo': ['bar', 'jack'], 'boyz': ['tattoos', 'respect', 'baz'] }
    print spell_checker.get_EF1_measure(human_dict)
    print spell_checker.get_all_stats(human_dict)
