#!/usr/bin/python

# Program to correct spelling errors.

import itertools
import utils
import lexicon
import edit_distance_calculator

max_num_word_suggestions = 10

class SpellChecker(object):
    """Suggest corrections for errors in queries.
    """

    def __init__(self):
        """Initialize all the dicts for suggestions, etc.
        """
        self.suggestion_dict = {}
        self.lexicon = lexicon.Lexicon()
        self.edit_dist_calculator = edit_distance_calculator.EditDistanceCalculator(self.lexicon)

        # TODO: Check with the full lexicon instead of dummy lexicon.
    # def generate_candidate_terms(self, term):
    #     """Return list of candidate terms for term.

    #     Return:
    #     - list of the term alone, if it is valid.
    #     - list of words one edit away, if possible.
    #     - list of words two edits away, if no valid one-edit words
    #       exist.
    #     """
    #     if self.lexicon.is_known_word(term):
    #         return [term]

    #     candidate_terms = self.edit_dist_calculator.known_words_one_edit_away (term) 
    #     # or self.edit_dist_calculator.known_words_two_edits_away (term)

    #     candidate_terms = self.lexicon.get_top_words(candidate_terms, 
    #                                                  max_num_word_suggestions)
    #     return candidate_terms
    #     pass

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

    def run_spell_check(self, query_list):
        """Run spell check on queries in query_list and store the suggestions.
        
        Arguments:
        - `query_list`:
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
