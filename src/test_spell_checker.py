#!/usr/bin/python

import spell_checker
import utils
import test_utils
import lexicon
import test_lexicon
import edit_distance_calculator
import test_edit_distance_calculator
import unittest

class SpellCheckerTest(unittest.TestCase):
    def setUp(self):
        self.lexicon = lexicon.Lexicon(word_list = [
            'yo', 'am', 'an', 
            'foo', 'bar', 'baz', 
            'boyz', 'edit', 'fast', 'cast',
            ])
        self.spell_checker = spell_checker.SpellChecker(given_lexicon = self.lexicon)

        # It'll end up being 1/3 anyway if every suggestion has the
        # same posterior, cos of normalization
        self.dummy_posterior = 1 / 3.0
        self.dummy_posterior_fn = lambda suggestion, query: self.dummy_posterior

    def tearDown(self):
        pass

    def assertListAlmostEqual(self, actual_list, expected_list):
        """Assert that actual_list and expected_list are almost equal.

        ie. assertAlmostEqual(actual_elem, expected_elem) in each list.
        Assumption: They are of same length.
        """
        self.assertTrue(len(actual_list) == len(expected_list))
        for i in xrange(len(actual_list)):
            self.assertAlmostEqual(actual_list[i], expected_list[i])
        
    def test_generate_candidate_terms(self):
        word1 = 'grst'
        word2 = 'fr'
        word3 = 'barz'

        ans1 = ['cast', 'fast']
        ans2 = ['am', 'an', 'bar', 'foo', 'yo']
        ans3 = ['bar', 'baz']
        self.assertEqual(self.spell_checker.generate_candidate_terms(word1),
                         ans1)
        self.assertEqual(self.spell_checker.generate_candidate_terms(word2),
                         ans2)
        self.assertEqual(self.spell_checker.generate_candidate_terms(word3),
                         ans3)

    def test_generate_candidate_suggestions(self): 
        term1_possibilities = ['cast', 'fast']
        term2_possibilities = ['edit']
        term3_possibilities = ['boyz', 'baz']
        term_possibilities_list = [term1_possibilities, term2_possibilities, 
                                   term3_possibilities]
        ans_term_possibilities_list = [['cast', 'edit', 'boyz'], 
                                       ['cast', 'edit', 'baz'], 
                                       ['fast', 'edit', 'boyz'], 
                                       ['fast', 'edit', 'baz']]

        self.assertEqual(
            self.spell_checker.generate_candidate_suggestions(term_possibilities_list),
            ans_term_possibilities_list)
    
    def test_generate_suggestions_and_posteriors(self):
        # Note: All this is with our tiny dummy lexicon
        query = 'wheere are yu going'
        suggestions = self.spell_checker.generate_suggestions_and_posteriors(
            query,
            get_posterior_fn = self.dummy_posterior_fn)
        expected_suggestion_list = [['wheere', 'am', 'yo', 'going'], 
                                    ['wheere', 'an', 'yo', 'going'], 
                                    ['wheere', 'bar', 'yo', 'going']]
               
        expected_posterior_list = [self.dummy_posterior] * 3

        actual_suggestion_list, actual_posterior_list = [list(produced_tuple) 
                                                         for produced_tuple 
                                                         in zip(*suggestions)]
        
        self.assertEqual(actual_suggestion_list,
                         expected_suggestion_list)
        self.assertEqual(actual_posterior_list,
                         expected_posterior_list)

    def test_run_spell_check(self):
        # Setting this here so that we don't have to call MS N-gram API
        self.spell_checker.get_posterior_fn = self.dummy_posterior_fn
        self.spell_checker.run_spell_check(['yo boyz'])
        self.assertEqual(
            self.spell_checker.generate_suggestions_and_posteriors('yo boyz'),
            self.spell_checker.suggestion_dict['yo boyz'])

    def test_get_all_stats(self): 
        self.spell_checker.get_posterior_fn = self.dummy_posterior_fn
        query_list = ['yo boyz i am sing song',
                      'faster and faster edits',
                      'jack in a bark floor']
        self.spell_checker.run_spell_check(query_list)
        human_dict = {
            query_list[0]: [['yo', 'boyz', 'am', 'am', 'sing', 'song']],
            query_list[1]: [['fast', 'an', 'fast', 'edit']],
            query_list[2]: [['jack', 'an', 'an', 'bar', 'foo']],
            }
        actual_stats = self.spell_checker.get_all_stats(human_dict)
        expected_stats = [0.55555555555555558, 1.0, 0.7142857142857143]
        self.assertEqual(actual_stats,
                         expected_stats)

    def test_get_all_stats_corner_cases(self): 
        self.spell_checker.get_posterior_fn = self.dummy_posterior_fn
        query_list = ['yo boyz i am sing song',
                      'faster and faster edits',
                      'jack in a bark floor']
        self.spell_checker.run_spell_check(query_list)

        # key's dict value is empty
        human_dict = {
            query_list[0]: [],
            query_list[1]: [['fast', 'an', 'fast', 'edit']],
            query_list[2]: [['jack', 'an', 'an', 'bar', 'foo']],
            }
        actual_stats = self.spell_checker.get_all_stats(human_dict)
        expected_stats = [0.5, 0.66666666666666663, 0.57142857142857151]
        self.assertEqual(actual_stats,
                         expected_stats)

        # All keys' dict values are empty
        human_dict = {
            query_list[0]: [],
            query_list[1]: [],
            query_list[2]: [],
            }
        actual_stats = self.spell_checker.get_all_stats(human_dict)
        expected_stats = [0.0, 0.0, 0.0]
        self.assertEqual(actual_stats,
                         expected_stats)

def get_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(SpellCheckerTest)
    return suite

if __name__ == '__main__':
    spell_checker_suite = get_suite()
    utils_suite = test_utils.get_suite()
    lexicon_suite = test_lexicon.get_suite()
    edit_distance_calculator_suite = test_edit_distance_calculator.get_suite()
    test_suites = [spell_checker_suite, utils_suite, lexicon_suite, 
                   edit_distance_calculator_suite]

    all_tests = unittest.TestSuite(test_suites)
    unittest.TextTestRunner(verbosity=2).run(all_tests)
