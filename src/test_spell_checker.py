#!/usr/bin/python

import spell_checker
import unittest

class SpellCheckerTest(unittest.TestCase):
    def setUp(self):
        self.spell_checker = spell_checker.SpellChecker()

    def tearDown(self):
        pass

    def test_get_EP(self):
        test_dict = { 1: [('foo', 0.3), ('bar', 0.7)], 
                      2: [('baz', 0.8), ('bah', 0.2)]}
        ans_dict = { 1: ['bar', 'jack'], 2: ['all', 'work', 'baz'] }
        self.assertAlmostEqual(spell_checker.get_EP([1, 2], test_dict, ans_dict),
                               0.75)
        self.assertAlmostEqual(spell_checker.get_EP([1], test_dict, ans_dict),
                               0.7)

    def test_get_ER(self):
        test_dict = { 1: [('foo', 0.3), ('bar', 0.7)], 
                      2: [('baz', 0.8), ('bah', 0.2)]}
        ans_dict = { 1: ['bar', 'jack'], 2: ['all', 'work', 'baz'] }
        self.assertAlmostEqual(spell_checker.get_ER([1, 2], test_dict, ans_dict),
                               5.0/12)
        self.assertAlmostEqual(spell_checker.get_ER([1], test_dict, ans_dict),
                               1.0/2)
        self.assertAlmostEqual(spell_checker.get_ER([2], test_dict, ans_dict),
                               1.0/3)

    def test_get_HM(self):
        self.assertAlmostEqual(spell_checker.get_HM(3, 3),
                               3, 1)
        self.assertAlmostEqual(spell_checker.get_HM(3, 0),
                               0, 1)
        self.assertAlmostEqual(spell_checker.get_HM(0.3, 0.7),
                               0.42, 1)
        self.assertAlmostEqual(spell_checker.get_HM(0.5, 0.5),
                               0.5 , 1)
        self.assertAlmostEqual(spell_checker.get_HM(0.1, 0.9),
                               0.18, 1)

    def test_partition(self):
        given_list = [1, 2, 3, 4, 5, 6, 7, 8]
        indices1 = [1]
        indices2 = [1, 5]
        indices3 = [1, 3, 5]
        ans1 = [[1], [2, 3, 4, 5, 6, 7, 8]]
        ans2 = [[1], [2, 3, 4, 5], [6, 7, 8]]
        ans3 = [[1], [2, 3], [4, 5], [6, 7, 8]]
        
        self.assertEqual(spell_checker.partition(given_list, indices1),
                         ans1)
        self.assertEqual(spell_checker.partition(given_list, indices2),
                         ans2)
        self.assertEqual(spell_checker.partition(given_list, indices3),
                         ans3)
        
    def test_is_sorted(self):
        sorted_list = [2, 3, 6, 7]
        unsorted_list = [3, 2, 6, 7]
        self.assertTrue(spell_checker.is_sorted(sorted_list))
        self.assertFalse(spell_checker.is_sorted(unsorted_list))
        
    def test_get_splits(self):
        run_on_word = 'giantkick'
        ans_1_splits = [['g', 'iantkick'],
                        ['gi', 'antkick'],
                        ['gia', 'ntkick'],
                        ['gian', 'tkick'],
                        ['giant', 'kick'],
                        ['giantk', 'ick'],
                        ['giantki', 'ck'],
                        ['giantkic', 'k']]
        ans_2_splits = [['g', 'i', 'antkick'],
                        ['g', 'ia', 'ntkick'],
                        ['g', 'ian', 'tkick'],
                        ['g', 'iant', 'kick'],
                        ['g', 'iantk', 'ick'],
                        ['g', 'iantki', 'ck'],
                        ['g', 'iantkic', 'k'],
                        ['gi', 'a', 'ntkick'],
                        ['gi', 'an', 'tkick'],
                        ['gi', 'ant', 'kick'],
                        ['gi', 'antk', 'ick'],
                        ['gi', 'antki', 'ck'],
                        ['gi', 'antkic', 'k'],
                        ['gia', 'n', 'tkick'],
                        ['gia', 'nt', 'kick'],
                        ['gia', 'ntk', 'ick'],
                        ['gia', 'ntki', 'ck'],
                        ['gia', 'ntkic', 'k'],
                        ['gian', 't', 'kick'],
                        ['gian', 'tk', 'ick'],
                        ['gian', 'tki', 'ck'],
                        ['gian', 'tkic', 'k'],
                        ['giant', 'k', 'ick'],
                        ['giant', 'ki', 'ck'],
                        ['giant', 'kic', 'k'],
                        ['giantk', 'i', 'ck'],
                        ['giantk', 'ic', 'k'],
                        ['giantki', 'c', 'k']]
        self.assertEqual(spell_checker.get_splits(run_on_word, 1),
                         ans_1_splits)
        self.assertEqual(spell_checker.get_splits(run_on_word, 2),
                         ans_2_splits)

    def test_get_corrected_run_on_queries(self):
        query_3_words = ['footballhalloffame']
        ans_3_words = ['football', 'hall', 'of', 'fame']

        query_2_words = ['giantcell', 'M']

        ans_2_words = [['g', 'iantcell', 'M'],
                       ['gi', 'antcell', 'M'],
                       ['gia', 'ntcell', 'M'],
                       ['gian', 'tcell', 'M'],
                       ['giant', 'cell', 'M'],
                       ['giantc', 'ell', 'M'],
                       ['giantce', 'll', 'M'],
                       ['giantcel', 'l', 'M'],
                       ['giantcell', 'M']]
        self.assertEqual(spell_checker.get_corrected_run_on_queries(query_2_words),
                         ans_2_words)

        # Skipping this for now, cos we aren't doing valid words
        # check.
        # self.assertEqual(spell_checker.get_corrected_run_on_queries(query_3_words),
        #                  ans_3_words)

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

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SpellCheckerTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
