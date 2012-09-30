#!/usr/bin/python

import lexicon
import unittest

class LexiconTest(unittest.TestCase):
    def setUp(self):
        self.lexicon = lexicon.Lexicon()
    
    def tearDown(self):
        pass

    def test_known_words(self): 
        word_list = ['are', 'yo', 'test']
        self.assertEqual(self.lexicon.known_words(word_list),
                         ['are', 'test'])
    
def get_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(LexiconTest)
    return suite

if __name__ == '__main__':
    suite = get_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
