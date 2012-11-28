#!/usr/bin/python

import lexicon
import unittest

class LexiconTest(unittest.TestCase):
    def setUp(self):
        self.lexicon = lexicon.Lexicon(word_list = ['yo', 'boyz'])
    
    def tearDown(self):
        pass

    def test_init(self): 
        full_lexicon = lexicon.Lexicon()
        self.assertFalse(len(full_lexicon.word_set) == 0)

    def test_known_words(self): 
        word_list = ['foo', 'yo', 'bar']
        self.assertEqual(self.lexicon.known_words(word_list),
                         ['yo'])

    def test_is_known_word(self): 
        word1 = 'foo'
        word2 = 'boyz'
        self.assertFalse(self.lexicon.is_known_word(word1))
        self.assertTrue(self.lexicon.is_known_word(word2))

    def test_get_words_from_lexicon_file_lowercase(self): 
        test_lexicon = lexicon.Lexicon()

        self.assertTrue(all(word.islower() for word in test_lexicon.word_set))

        # There should be one-letter words
        self.assertFalse(all(len(word) > 1 for word in test_lexicon.word_set))
        self.assertTrue(test_lexicon.is_known_word('chester'))
        self.assertTrue(test_lexicon.is_known_word('arthur'))

    def test_get_top_words(self): 
        word_list = ['yo', 'boyz']
        ans1 = ['boyz']
        ans2 = ['boyz', 'yo']

        self.assertEqual(self.lexicon.get_top_words(word_list, 1),
                         ans1)
        self.assertEqual(self.lexicon.get_top_words(word_list, 2),
                         ans2)
    
def get_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(LexiconTest)
    return suite

if __name__ == '__main__':
    suite = get_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
