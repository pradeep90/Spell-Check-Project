#!/usr/bin/python

# Program to correct spelling errors.

import itertools
import utils
import lexicon
import edit_distance_calculator
import phrase

max_num_word_suggestions = 10

class SpellChecker(object):
    """Suggest corrections for errors in queries.
    """

    def __init__(self, given_lexicon = None):
        """Initialize all the dicts for suggestions, etc.
        """
        self.suggestion_dict = {}

        self.lexicon = given_lexicon
        if self.lexicon is None:
            self.lexicon = lexicon.Lexicon()

        self.edit_distance_calculator = edit_distance_calculator.EditDistanceCalculator(self.lexicon)
        self.get_posterior_fn = phrase.get_posterior

    def generate_candidate_terms(self, term):
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

        # TODO: I think we should use both and then filter.
        candidate_terms = self.edit_distance_calculator.get_top_known_words(term, 10)
        
        return candidate_terms

    def generate_candidate_suggestions(self, term_possibilities_list):
        """Return list of candidate suggestions by combining all possibilities.
        
        Arguments:
        - `term_possibilities_list`: list of list of possibilities for
          each term in the query phrase.
        """
        return [list(suggestion) 
                for suggestion in itertools.product(*term_possibilities_list)]
    
    def generate_suggestions_and_posteriors(self, query_string, 
                                            get_posterior_fn = None):
        """Return (suggestion, posterior) pairs for query.

        Get a list of candidate suggestions and calculate posteriors
        for each of them.

        Arguments:
        - `query_string`: string representing the word/phrase/sentence query.
        """
        if get_posterior_fn == None:
            get_posterior_fn = self.get_posterior_fn

        query = query_string.split()
        # List of list of possibilities for each term
        all_term_possibilities = [self.generate_candidate_terms(term) 
                                  for term in query]

        # List of all suggestions
        all_suggestions = self.generate_candidate_suggestions(all_term_possibilities)
        print all_suggestions

        posteriors = [get_posterior_fn(suggestion, query) 
                      for suggestion in all_suggestions]
        normalized_posteriors = utils.get_normalized_probabilities(posteriors)
        print normalized_posteriors

        return zip(all_suggestions, normalized_posteriors)

    def run_spell_check(self, query_list):
        """Run spell check on queries in query_list and store the suggestions.
        
        Arguments:
        - `query_list`: a string (NOT list) representing word/phrase/sentence.
        """
        self.query_list = query_list
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
    
    def get_all_stats(self, human_suggestion_dict):
        """Return [EP, ER, EF1] for performance as judged by human_suggestion_dict.
        
        Arguments:
        - `human_suggestion_dict`:
        """
        args = [self.query_list, self.suggestion_dict, human_suggestion_dict]
        return [utils.get_EP(*args), utils.get_ER(*args), 
                self.get_EF1_measure(human_suggestion_dict)]

if __name__ == '__main__':
    spell_checker = SpellChecker()
    spell_checker.run_spell_check(['yo', 'boyz'])
    human_dict = { 'yo': ['bar', 'jack'], 'boyz': ['tattoos', 'respect', 'baz'] }
    print spell_checker.get_EF1_measure(human_dict)
    print spell_checker.get_all_stats(human_dict)
