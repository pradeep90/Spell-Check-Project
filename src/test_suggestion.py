#!/usr/bin/python

import suggestion
import unittest

class SuggestionTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_init(self): 
        test_list = [1, 2, 3]
        # Term list
        actual = suggestion.Suggestion(test_list)
        expected = test_list
        self.assertEqual(actual,
                         expected)

        # suggestion_string = 'yo boyz'
        # # Suggestion string
        # actual = suggestion.Suggestion(suggestion_string)
        # expected = suggestion_string.split()
        # self.assertEqual(actual,
        #                  expected)

    def test_equal(self): 
        test_str = 'yo boyz'
        test_list = ['yo', 'boyz']
        s1 = suggestion.Suggestion(suggestion_str = test_str)
        s2 = suggestion.Suggestion(test_list)

        # Suggestion-Suggestion
        self.assertEqual(s1, s1)

        # Suggestion-list
        self.assertEqual(s2, test_list)

        # Suggestion-str
        self.assertEqual(s1, test_str)

        # gen
        self.assertNotEqual(s1, 3)

        # gen list
        self.assertNotEqual(s1, [2])

        # gen string
        self.assertNotEqual(s1, 'onuthe')

    def test_set_term_list(self): 
        s = suggestion.Suggestion(suggestion_type = 'phrase')
        test_list = ['foo', 'bar']
        test_str = 'foo bar'
        s.set_term_list(test_list)

        self.assertEqual(s.term_list,
                         test_list)

        # suggestion_str
        self.assertEqual(s.suggestion_str,
                         test_str)

        test_list = []
        test_str = ''
        s.set_term_list(test_list)

        self.assertEqual(s.term_list,
                         test_list)

        # suggestion_str
        self.assertEqual(s.suggestion_str,
                         test_str)


    def test_set_term_list_sentence(self): 
        s = suggestion.Suggestion(suggestion_type = 'sentence')
        test_list = ['foo', 'bar']
        test_str = 'Foo bar.'
        s.set_term_list(test_list)

        self.assertEqual(s.term_list,
                         test_list)

        # suggestion_str
        self.assertEqual(s.suggestion_str,
                         test_str)

        test_list = []
        test_str = ''
        s.set_term_list(test_list)

        self.assertEqual(s.term_list,
                         test_list)

        # suggestion_str
        self.assertEqual(s.suggestion_str,
                         test_str)

    def test_set_term_list_word(self): 
        s = suggestion.Suggestion(suggestion_type = 'word')
        test_list = ['foo']
        test_str = 'foo'
        s.set_term_list(test_list)

        self.assertEqual(s.term_list,
                         test_list)

        # suggestion_str
        self.assertEqual(s.suggestion_str,
                         test_str)

        test_list = []
        test_str = ''
        s.set_term_list(test_list)

        self.assertEqual(s.term_list,
                         test_list)

        # suggestion_str
        self.assertEqual(s.suggestion_str,
                         test_str)

def get_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(SuggestionTest)
    return suite

if __name__ == '__main__':
    suite = get_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
