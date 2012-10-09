#!/usr/bin/python

import phrase
import unittest
import math
import utils
from suggestion import Suggestion

class PhraseTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_get_edits(self): 
        word1 = 'foo'
        word2 = 'bar'
        expected = (0.61411943319838058, 'sfb soa do ir')
        self.assertEqual(phrase.get_edits(word1, word2),
                         expected)
    
    def test_get_likelihood(self): 
        query = Suggestion(['foo'])
        suggestion = Suggestion(['bar'])
        expected = phrase.error_penalization * -(phrase.get_edits(suggestion[0], 
                                                 query[0])[0] / len(str(query)))
        self.assertAlmostEqual(phrase.get_likelihood(query, suggestion),
                               expected, 2)

        # phrase with splits joined up
        split_str = 'fo o bar roc ks'
        joined_str = 'foo bar rocks'
        query = Suggestion(suggestion_str = split_str)
        suggestion = Suggestion(suggestion_str = joined_str)
        expected = phrase.error_penalization * -(2 * phrase.space_edit_cost / len(split_str))
        self.assertAlmostEqual(phrase.get_likelihood(query, suggestion),
                               expected)

        # phrases with joins split up
        split_str = 'fo o bar roc ks'
        joined_str = 'foo bar rocks'
        query = Suggestion(suggestion_str = joined_str)
        suggestion = Suggestion(suggestion_str = split_str)
        expected = phrase.error_penalization * -(2 * phrase.space_edit_cost / len(joined_str))
        self.assertAlmostEqual(phrase.get_likelihood(query, suggestion),
                               expected)

        # phrases with splits and errors
        split_str = 'fo o bcr rxc ks'
        joined_str = 'foo bar rocks'
        query = Suggestion(suggestion_str = split_str)
        suggestion = Suggestion(suggestion_str = joined_str)
        edit_distance = (phrase.get_edits(''.join(joined_str.split()), 
                                          ''.join(split_str.split()))[0]\
                                          + 2 * phrase.space_edit_cost)
        expected = phrase.error_penalization * -(edit_distance / len(str(split_str)))
        self.assertAlmostEqual(phrase.get_likelihood(query, suggestion),
                               expected)

    def test_get_posterior(self):
        motor_cycles_prior = -19.400790000000001
        motor_space_cycles_prior = -20.64209
        # phrases with splits and errors
        split_str = 'picture of state trooper motor cycles'
        joined_str = 'picture of state trooper motorcycles'

        query = Suggestion(suggestion_str = joined_str)
        suggestion = Suggestion(suggestion_str = split_str)
        # edit_distance = (phrase.get_edits(''.join(joined_str.split()), 
        #                                   ''.join(split_str.split()))[0]\
        #                                   + 2 * phrase.space_edit_cost)
        # expected = -(edit_distance / len(str(split_str)))

        expected = -0.0033333333333333335

        likelihood = phrase.get_likelihood(query, suggestion)
        self.assertAlmostEqual(likelihood,
                               expected)

        log_split_posterior = motor_space_cycles_prior + phrase.get_likelihood(query, 
                                                                               suggestion)

        log_joined_posterior = motor_cycles_prior + phrase.get_likelihood(query, 
                                                                          query)
        self.assertAlmostEqual(log_split_posterior, -20.645423333333333)
        self.assertAlmostEqual(log_joined_posterior, -19.400790000000001)

        # self.assertEqual(utils.get_normalized_probabilities([log_split_posterior, 
        #                                                      log_joined_posterior]),
        #                  [])

def get_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(PhraseTest)
    return suite

if __name__ == '__main__':
    suite = get_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
