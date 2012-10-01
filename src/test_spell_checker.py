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

    def tearDown(self):
        pass
    
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
        
    # def test_generate_suggestions_and_posteriors(self):
    #     query = 'foo'
    #     suggestions = self.spell_checker.generate_suggestions_and_posteriors(query)
    #     expected = [('believe', 0.11),
    #                 ('buoyant', 0.02),
    #                 ('committed', 0.14999999999999999),
    #                 ('distract', 0.040000000000000001),
    #                 ('ecstacy', 0.040000000000000001),
    #                 ('fairy', 0.050000000000000003),
    #                 ('hello', 0.02),
    #                 ('gracefully', 0.059999999999999998),
    #                 ('liaison', 0.070000000000000007),
    #                 ('occasion', 0.10000000000000001),
    #                 ('possible', 0.01),
    #                 ('throughout', 0.029999999999999999),
    #                 ('volley', 0.070000000000000007),
    #                 ('tattoos', 0.040000000000000001),
    #                 ('respect', 0.19)
    #                 ]
    #     self.assertEqual(suggestions,
    #                      expected)

    # def test_run_spell_check(self):
    #     self.spell_checker.run_spell_check(['yo', 'boyz'])
    #     self.assertEqual(self.spell_checker.suggestion_dict['yo'],
    #                      self.spell_checker.generate_suggestions_and_posteriors('yo'))
    #     self.assertEqual(self.spell_checker.suggestion_dict['boyz'],
    #                      self.spell_checker.generate_suggestions_and_posteriors('boyz'))

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
