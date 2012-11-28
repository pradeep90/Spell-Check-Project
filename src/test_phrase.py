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

        
    def test_get_likelihood_splits_special(self):
        # TODO
        suggestion_likelihood_list = [
            (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
             Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'horses', 'conducted', 'by', 'highly', 'qualified', 'staff']), 0.0),
             (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
              Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'courses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
              -0.0092284029735965143),
            (Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'horses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            0.0),
            (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'horses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            0.0),
            (Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'cores', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.0015698587127158554),
            (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'cores', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.0015887726731100226),
            (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'cores', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.0015887726731100226),
            (Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'cortes', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.007872379721119217),
            (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'cortes', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.0079672276695664374),
            (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'cortes', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.0079672276695664374),
            (Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'courses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.0091185410334346517),
            (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'courses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.0092284029735965143),
            (Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'torses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.010714285714285714),
            (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'torses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.010843373493975905),
            (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'torses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.010843373493975905),
            (Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'curses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.010989010989010988),
            (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'curses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.011121408711770158),
            (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'curses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.011121408711770158),
            (Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'corsets', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.012605042016806723),
            (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'corsets', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.012756909992912829),
            (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'corsets', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.012756909992912829),
            (Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'corset', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.013632791245994799),
            (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'corset', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.013797041742934496),
            (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'corset', 'conducted', 'by', 'highly', 'qualified', 'staff']),
            -0.013797041742934496),
            (Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
             Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'copses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
             -0.030612244897959183),
             (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
              Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'copses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
              -0.030981067125645436),
              (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
               Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'copses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
               -0.030981067125645436),
               (Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
                Suggestion(['the', 'departments', 'of', 'the', 'ins', 'tit', 'ute', 'offer', 'corpses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
                -0.034985422740524783),
                (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
                 Suggestion(['the', 'departments', 'of', 'the', 'institute', 'offer', 'corpses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
                 -0.035406933857880504),
                 (Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
                  Suggestion(['the', 'departments', 'of', 'the', 'institute', 'of', 'fer', 'corpses', 'conducted', 'by', 'highly', 'qualified', 'staff']),
                  -0.035406933857880504)]
        for i, _tuple in enumerate(suggestion_likelihood_list):
            query, suggestion, likelihood = _tuple
            # print 'suggestion number: ', i
            self.assertAlmostEqual(phrase.get_likelihood(query, suggestion),
                                   likelihood, 2)

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
