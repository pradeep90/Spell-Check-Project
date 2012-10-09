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
        word = 'edt'
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
    def test_known_words_two_edit_away(self): 
        word1 = 'boyz'
        word_list = [
            'bola', 'bogs', 'bomb', 'bozo', 'bogy', 'both', 'boozy',
            'born', 'booze', 'toys', 'soy', 'boas', 'bore', 'bow', 'boat', 'bold',
            'toy', 'bobs', 'joys', 'boor', 'boos', 'bowl', 'bog', 'bays', 'boom',
            'boon', 'buys', 'bout', 'bye', 'boar', 'body', 'buy', 'bole', 'cozy',
            'buoys', 'joy', 'boo', 'boll', 'boss', 'boob', 'boys', 'bosh', 'bolt',
            'boot', 'bode', 'by', 'box', 'boy', 'bony', 'bop', 'bows', 'bay',
            'coy', 'boil', 'bops', 'buzz', 'boa', 'bob', 'buoy', 'bong', 'book',
            'bone', 'bond'
            ]

        full_lexicon = lexicon.Lexicon(word_list = word_list + ['yo', 'foo'])
        full_edit_distance_calculator = edit_distance_calculator.EditDistanceCalculator(
            full_lexicon)
        self.assertEqual(
            full_edit_distance_calculator.known_words_two_edits_away(word1),
            word_list)

    def test_get_top_known_words(self): 
        word1 = 'boyz'
        ans1 = ['boyz']
        word2 = 'goo'
        ans2 = ['foo']
        word3 = 'yoo'
        ans3 = ['foo', 'yo']
        ans4 = ['foo']
        self.assertEqual(self.edit_distance_calculator.get_top_known_words(word1, 10),
                         ans1)
        self.assertEqual(self.edit_distance_calculator.get_top_known_words(word2, 10),
                         ans2)
        self.assertEqual(self.edit_distance_calculator.get_top_known_words(word3, 10),
                         ans3)
        self.assertEqual(self.edit_distance_calculator.get_top_known_words(word3, 1),
                         ans4)
    
def get_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(EditDistanceCalculatorTest)
    return suite

if __name__ == '__main__':
    suite = get_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

