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
from pprint import pprint

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
        self.MAX_NUM_TERMS = 10
        self.MAX_NUM_SUGGESTIONS = 7
        self.ORIGINAL_POSTERIOR_THRESHOLD = 0.1

    def get_suggestion_dict(self):
        return self.suggestion_dict

    def generate_candidate_terms(self, 
                                 term, 
                                 num_candidates_terms_per_word = None):
        """Return list of candidate terms for term.

        Return:
        - list of the term alone, if it is valid.
        - list of words one edit away, if possible.
        - list of words two edits away, if no valid one-edit words
          exist.
        - Else (nothing was found), return a list of the term alone.
        """
        if num_candidates_terms_per_word is None:
            num_candidates_terms_per_word = self.MAX_NUM_TERMS

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

        # all_queries = [query] + utils.get_corrected_split_queries(query, self.lexicon) \
        #   + utils.get_corrected_run_on_queries(query, self.lexicon)

        all_queries = [query] + utils.get_corrected_split_queries(query, self.lexicon)
        #   + utils.get_corrected_run_on_queries(query, self.lexicon)

        # print 'all_queries'
        # pprint(all_queries)

        # List of list of (query, suggestion, likelihood) for each query
        all_suggestions = [[(query, suggestion) 
                            for suggestion in self.generate_candidate_suggestions(
                                    map(self.generate_candidate_terms, query),
                                    query.suggestion_type)] 
                                    for query in all_queries]

        # Flatten the list of list of suggestions
        all_suggestions = list(itertools.chain(*all_suggestions))

        # print 'all_suggestions after flattening'
        # pprint(all_suggestions)

        all_suggestions.sort(key = lambda query_sugg_tuple: 
                             phrase.get_likelihood(*query_sugg_tuple), 
                             reverse = True)

        # print 'suggestions and likelihood'
        # pprint([(query, suggestion, phrase.get_likelihood(query, suggestion)) 
        #         for query, suggestion in all_suggestions])

        # Remove duplicates (if any)
        all_suggestions = [key for key, _ in itertools.groupby(all_suggestions)]

        # print 'all_suggestions after removing duplicates'
        # pprint(all_suggestions)

        # Take only the top few suggestions
        all_suggestions = all_suggestions[:self.MAX_NUM_SUGGESTIONS]

        # print 'len(all_suggestions)'
        # pprint(len(all_suggestions))

        # print 'all_suggestions after taking off the top'
        # pprint(all_suggestions)

        all_posteriors = [get_posterior_fn(suggestion, query)
                          for query, suggestion in all_suggestions]

        all_suggestions = list(zip(*all_suggestions)[1])

        # TODO
        # original_query = query
        # original_query_posterior = get_posterior_fn(query, query)
        # print 'original_query'
        # pprint(original_query, original_query_posterior)
        # if original_query_posterior > self.ORIGINAL_POSTERIOR_THRESHOLD:
        #     all_suggestions += [original_query]
        #     all_posteriors += [original_query_posterior]

        normalized_posteriors = utils.get_normalized_probabilities(all_posteriors)
        suggestion_posterior_list = list(zip(all_suggestions, normalized_posteriors))
        suggestion_posterior_list.sort(key = lambda pair: pair[1], reverse = True)
        return suggestion_posterior_list

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
    query_list = ['The departments of the institute offer corses, conducted by highly qualified staff.']
    query_list = [Suggestion(suggestion_str = query, suggestion_type = 'sentence') 
                  for query in query_list]
    spell_checker.run_spell_check(query_list)
    print 'spell_checker.get_suggestion_dict()'
    pprint(spell_checker.get_suggestion_dict())
    # human_dict = { query_list[0]: [Suggestion('why this kolaveri'.split())], 
    #                query_list[1]: [Suggestion('i am sing song'.split())] }
    # print 'spell_checker.get_EF1_measure(human_dict)'
    # pprint(spell_checker.get_EF1_measure(human_dict))
    # print 'spell_checker.get_all_stats(human_dict)'
    # pprint(spell_checker.get_all_stats(human_dict))


