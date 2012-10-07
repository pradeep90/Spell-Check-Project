#!/usr/bin/python

import utils
import unittest
from suggestion import Suggestion

class UtilsTest(unittest.TestCase):
    def setUp(self):
        # self.spell_checker = utils.SpellChecker()
        pass

    def tearDown(self):
        pass

    def test_get_EP(self):
        test_dict = { 1: [('foo', 0.3), ('bar', 0.7)], 
                      2: [('baz', 0.8), ('bah', 0.2)]}
        ans_dict = { 1: ['bar', 'jack'], 2: ['all', 'work', 'baz'] }
        self.assertAlmostEqual(utils.get_EP([1, 2], test_dict, ans_dict),
                               0.75)
        self.assertAlmostEqual(utils.get_EP([1], test_dict, ans_dict),
                               0.7)

    def test_get_EP_corner_cases(self): 
        test_dict = { 1: [('foo', 0.3), ('bar', 0.7)], 
                      2: [('baz', 0.8), ('bah', 0.2)]}
        # key's ans_dict value is []
        ans_dict = { 1: [], 2: [] }
        self.assertAlmostEqual(utils.get_EP([1, 2], test_dict, ans_dict),
                               0)

        # query_list is empty
        self.assertAlmostEqual(utils.get_EP([], test_dict, ans_dict),
                               0)

    def test_get_ER(self):
        test_dict = { 1: [('foo', 0.3), ('bar', 0.7)], 
                      2: [('baz', 0.8), ('bah', 0.2)]}
        ans_dict = { 1: ['bar', 'jack'], 2: ['all', 'work', 'baz'] }
        self.assertAlmostEqual(utils.get_ER([1, 2], test_dict, ans_dict),
                               5.0/12)
        self.assertAlmostEqual(utils.get_ER([1], test_dict, ans_dict),
                               1.0/2)
        self.assertAlmostEqual(utils.get_ER([2], test_dict, ans_dict),
                               1.0/3)

    def test_get_ER(self): 
        test_dict = { 1: [('foo', 0.3), ('bar', 0.7)], 
                      2: [('baz', 0.8), ('bah', 0.2)]}
        ans_dict = { 1: [], 2: ['all', 'work', 'baz'] }

        # key's ans_dict value is []
        self.assertAlmostEqual(utils.get_ER([1, 2], test_dict, ans_dict),
                               1.0/6)
        # query_list is empty
        self.assertAlmostEqual(utils.get_ER([], test_dict, ans_dict),
                               0)
        
    def test_get_HM(self):
        self.assertAlmostEqual(utils.get_HM(3, 3),
                               3, 1)
        self.assertAlmostEqual(utils.get_HM(3, 0),
                               0, 1)
        self.assertAlmostEqual(utils.get_HM(0.3, 0.7),
                               0.42, 1)
        self.assertAlmostEqual(utils.get_HM(0.5, 0.5),
                               0.5 , 1)
        self.assertAlmostEqual(utils.get_HM(0.1, 0.9),
                               0.18, 1)

    def test_get_HM_corner_cases(self): 
        self.assertAlmostEqual(utils.get_HM(0.0, 3.0),
                               0.0, 1)
        self.assertAlmostEqual(utils.get_HM(0.3, 0.0),
                               0.0, 1)
        self.assertAlmostEqual(utils.get_HM(0.0, 0.0),
                               0.0, 1)

    def test_partition(self):
        given_list = [1, 2, 3, 4, 5, 6, 7, 8]
        indices1 = [1]
        indices2 = [1, 5]
        indices3 = [1, 3, 5]
        ans1 = [[1], [2, 3, 4, 5, 6, 7, 8]]
        ans2 = [[1], [2, 3, 4, 5], [6, 7, 8]]
        ans3 = [[1], [2, 3], [4, 5], [6, 7, 8]]
        
        self.assertEqual(utils.partition(given_list, indices1),
                         ans1)
        self.assertEqual(utils.partition(given_list, indices2),
                         ans2)
        self.assertEqual(utils.partition(given_list, indices3),
                         ans3)
        
    def test_is_sorted(self):
        sorted_list = [2, 3, 6, 7]
        unsorted_list = [3, 2, 6, 7]
        self.assertTrue(utils.is_sorted(sorted_list))
        self.assertFalse(utils.is_sorted(unsorted_list))
        
    def test_get_splits(self):
        run_on_word = 'giantkick'
        ans_1_splits = [['giant', 'kick'],]
        ans_2_splits = []
        self.assertEqual(utils.get_splits(run_on_word, 1),
                         ans_1_splits)
        self.assertEqual(utils.get_splits(run_on_word, 2),
                         ans_2_splits)

    def test_get_corrected_run_on_queries(self):
        query_3_words = Suggestion(['footballhalloffame', 'rocks'])
        ans_3_words = [Suggestion(['football', 'hall', 'of', 'fame', 'rocks'])]
                       
        query_2_words = Suggestion(['giantcell', 'M'])

        ans_2_words = [Suggestion(['giant', 'cell', 'M'])]
        self.assertEqual(utils.get_corrected_run_on_queries(query_2_words),
                         ans_2_words)

        self.assertEqual(utils.get_corrected_run_on_queries(query_3_words),
                         ans_3_words)

    def test_get_corrected_split_queries(self):
        # No splits
        query_1_word = ['fast']
        ans_1_word = []
        # one split, total two words
        query_2_word = ['forw', 'ard']
        ans_2_word = [['forward']]
        # one split, total three words
        query_3_word = ['forw', 'ard', 'march']
        ans_3_word = [['forward', 'march']]
        # one split, total four words
        query_4_word = ['fast', 'forw', 'ard', 'march']
        ans_4_word = [['fast', 'forward', 'march']]

        queries = [query_1_word, query_2_word, query_3_word, query_4_word]
        queries = [Suggestion(query) for query in queries]
        answers = [ans_1_word, ans_2_word, ans_3_word, ans_4_word]

        for i in xrange(4):
            self.assertEqual(utils.get_corrected_split_queries(queries[i]),
                             answers[i])

    def test_get_normalized_probabilities(self): 
        probability_list = [0.2, 0.3, 0.2]
        ans = [0.28571428571428575, 0.4285714285714286, 0.28571428571428575]

        actual_list = utils.get_normalized_probabilities(probability_list)

        for i in xrange(len(actual_list)):
            self.assertAlmostEqual(actual_list[i], ans[i])

        self.assertAlmostEqual(sum(actual_list),
                               1.0)

    def test_get_phrase_from_sentence(self): 
        sentence = 'Foo bar yo.'
        expected = 'foo bar yo'
        self.assertEqual(utils.get_phrase_from_sentence(sentence),
                         expected)

    def test_get_sentence_from_phrase(self): 
        phrase = 'foo bar yo'
        expected = 'Foo bar yo.'
        self.assertEqual(utils.get_sentence_from_phrase(phrase),
                         expected)

    def test_get_sentence_suggestion_from_phrase_suggestion(self): 
        phrase_suggestion = 'foo bar yo'.split()
        expected_sentence_suggestion = 'Foo bar yo.'.split()
        self.assertEqual(
            utils.get_sentence_suggestion_from_phrase_suggestion(phrase_suggestion),
            expected_sentence_suggestion)
        
def get_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(UtilsTest)
    return suite

if __name__ == '__main__':
    suite = get_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
