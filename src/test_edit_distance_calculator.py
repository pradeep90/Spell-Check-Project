#!/usr/bin/python

import lexicon
import edit_distance_calculator
import unittest
import test_data

class EditDistanceCalculatorTest(unittest.TestCase):
    def setUp(self):
        self.lexicon = lexicon.Lexicon(word_list = ['yo', 'boyz', 'foo'])
        self.edit_distance_calculator = edit_distance_calculator.EditDistanceCalculator(
            self.lexicon)

    def tearDown(self):
        pass

    def test_words_one_edit_away(self): 
        word = 'bz'
        self.assertEqual(self.edit_distance_calculator.words_one_edit_away(word),
                         test_data.ans_one_edit)
    
    def test_known_words_one_edit_away(self): 
        word1 = 'goo'
        ans1 = ['foo']
        word2 = 'boiz'
        ans2 = ['boyz']
        self.assertEqual(self.edit_distance_calculator.known_words_one_edit_away(word1),
                         ans1)
        self.assertEqual(self.edit_distance_calculator.known_words_one_edit_away(word2),
                         ans2)

        # TODO
    # def test_known_words_two_edit_away(self): 
    #     word1 = 'boyz'
    #     ans1 = ['foo', 'yo']
    #     word2 = 'boyz'
    #     ans2 = ['boyz']

    #     full_lexicon = lexicon.Lexicon()
    #     full_edit_distance_calculator = edit_distance_calculator.EditDistanceCalculator(
    #         full_lexicon)
    #     self.assertEqual(full_edit_distance_calculator.known_words_two_edits_away(word1),
    #                      test_data.ans_one_edit)
    #     self.assertEqual(full_edit_distance_calculator.known_words_two_edits_away(word2),
    #                      ans2)
    
def get_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(EditDistanceCalculatorTest)
    return suite

if __name__ == '__main__':
    suite = get_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

