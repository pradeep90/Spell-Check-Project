#!/usr/bin/python

# Program to correct spelling errors.

import edit_distance_calculator
import itertools
import lexicon
import phrase
import pickle
from suggestion import Suggestion
import re
import utils

MAX_NUM_TERMS = 10
MAX_NUM_SUGGESTIONS = 7

class SpellChecker(object):
    """Suggest corrections for errors in queries.
    """

    def __init__(self, given_lexicon = None):
        """Initialize all the dicts for suggestions, etc.
        """
        # key: query (which is a Suggestion object)
        # val: list of (Suggestion object, posterior) pairs;
        self.suggestion_dict = {}

        self.lexicon = given_lexicon
        if self.lexicon is None:
            self.lexicon = lexicon.Lexicon()

        self.edit_distance_calculator = edit_distance_calculator.EditDistanceCalculator(self.lexicon)
        self.get_posterior_fn = phrase.get_posterior

    def get_suggestion_dict(self):
        return self.suggestion_dict

    def generate_candidate_terms(self, 
                                 term, 
                                 num_candidates_terms_per_word = MAX_NUM_TERMS):
        """Return list of candidate terms for term.

        Return:
        - list of the term alone, if it is valid.
        - list of words one edit away, if possible.
        - list of words two edits away, if no valid one-edit words
          exist.
        - Else (nothing was found), return a list of the term alone.
        """
        if self.lexicon.is_known_word(term):
            return [term]

        candidate_terms = self.edit_distance_calculator.get_top_known_words(
            term, num_candidates_terms_per_word)
        
        return candidate_terms

    def generate_candidate_suggestions(self, term_possibilities_list, suggestion_type):
        """Return list of candidate Suggestions by combining all possibilities.
        
        Arguments:
        - `term_possibilities_list`: list of list of possibilities for
          each term in the query phrase.
        """
        # suggestion is a tuple, so converting it to a list
        return [Suggestion(list(suggestion), suggestion_type = suggestion_type) 
                for suggestion in itertools.product(*term_possibilities_list)]
    
    def generate_suggestions_and_posteriors(self, query, 
                                            get_posterior_fn = None):
        """Return (suggestion, posterior) pairs for query.

        Get a list of candidate suggestions and calculate posteriors
        for each of them.

        Arguments:
        - `query`: Suggestion object.
        """
        if get_posterior_fn == None:
            get_posterior_fn = self.get_posterior_fn

        all_queries = [query] + utils.get_corrected_split_queries(query) + utils.get_corrected_run_on_queries(query)
        print 'all_queries', all_queries

        # List of list of (query, suggestion, likelihood) for each query
        all_suggestions = [[(query, suggestion, phrase.get_likelihood(query, suggestion)) 
                            for suggestion in self.generate_candidate_suggestions(
                                    map(self.generate_candidate_terms, query),
                                    query.suggestion_type)] 
                                    for query in all_queries]

        # Flatten the list of list of suggestions
        all_suggestions = list(itertools.chain(*all_suggestions))

        all_suggestions.sort(key = lambda _tuple: _tuple[2], 
                             reverse = True)

        # Take only the top few suggestions
        all_suggestions = all_suggestions[:MAX_NUM_SUGGESTIONS]

        print 'len(all_suggestions)', len(all_suggestions)

        all_posteriors = [get_posterior_fn(suggestion, query)
                          for query, suggestion, likelihood in all_suggestions]

        all_suggestions = zip(*all_suggestions)[1]
        normalized_posteriors = utils.get_normalized_probabilities(all_posteriors)
        return zip(all_suggestions, normalized_posteriors)

    def run_spell_check(self, query_list):
        """Run spell check on queries in query_list and store the suggestions.
        
        ASSUMPTION: all words in query_list are lowercase.
        Arguments:
        - `query_list`: a string (NOT list) representing word/phrase/sentence.
        """
        self.query_list = query_list
        # self.query_list = map(str.lower, query_list)
        # self.query_list = [for query in self.query_list]
        for query in self.query_list:
            self.suggestion_dict[query] = self.generate_suggestions_and_posteriors(
                query)

    def get_EF1_measure(self, human_suggestion_dict):
        """Return EF1 value for the performance as judged by human_suggestion_dict.
        
        Arguments:
        - `human_suggestion_dict`: dict of query -> list of
          human-annotated suggestions
        """
        args = [self.query_list, self.suggestion_dict, human_suggestion_dict]
        return utils.get_HM (utils.get_EP(*args),
                             utils.get_ER(*args))
    
    def get_all_stats(self, 
                      human_suggestion_dict,
                      query_list = None,
                      suggestion_dict = None):
        """Return [EP, ER, EF1] for performance as judged by human_suggestion_dict.
        
        Arguments:
        - `human_suggestion_dict`:
        """

        if query_list == None:
            query_list = self.query_list
        if suggestion_dict == None:
            suggestion_dict = self.suggestion_dict

        args = [self.query_list, self.suggestion_dict, human_suggestion_dict]
        return [utils.get_EP(*args), utils.get_ER(*args), 
                self.get_EF1_measure(human_suggestion_dict)]

if __name__ == '__main__':
    spell_checker = SpellChecker()
    query_list = ['why this kolaveri', 'i am sixg sxng']
    query_list = [Suggestion(query) for query in query_list]
    spell_checker.run_spell_check(query_list)
    human_dict = { query_list[0]: [Suggestion('why this kolaveri'.split())], 
                   query_list[1]: [Suggestion('i am sing song'.split())] }
    print 'spell_checker.get_EF1_measure(human_dict)', spell_checker.get_EF1_measure(human_dict)
    print 'spell_checker.get_all_stats(human_dict)', spell_checker.get_all_stats(human_dict)


