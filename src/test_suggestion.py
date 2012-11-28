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

        suggestion_string = 'yo boyz'
        # Suggestion string
        actual = suggestion.Suggestion(suggestion_str = suggestion_string)
        expected = suggestion_string
        self.assertEqual(str(actual),
                         expected)

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

        # Sentence with comma
        s_comma = 'Keep your friends close, and your enemies closer.'
        s_normal = 'Keep your friends close and your enemies closer.'
        s1 = suggestion.Suggestion(suggestion_str = s_comma)
        s2 = suggestion.Suggestion(suggestion_str = s_normal)

        self.assertEqual(s1, s2)

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

    def test_set_suggestion_str_phrase(self):
        s = suggestion.Suggestion(suggestion_type = 'phrase')
        test_str = 'yo boyz i am sing song'
        expected_list = test_str.split()
        s.set_suggestion_str(test_str)
        self.assertEqual(s.suggestion_str,
                         test_str)
        self.assertEqual(s.term_list,
                         expected_list)

        # Strings with commas
        comma_str = 'yo boyz, i am sing, song'
        expected_list = ['yo', 'boyz', 'i', 'am', 'sing', 'song']
        s.set_suggestion_str(comma_str)
        self.assertEqual(s.term_list,
                         expected_list)

    def test_set_suggestion_str_sentence(self):
        s = suggestion.Suggestion(suggestion_type = 'sentence')
        test_str = 'Yo boyz i am sing song.'
        expected_list = ['yo', 'boyz', 'i', 'am', 'sing', 'song']
        s.set_suggestion_str(test_str)
        self.assertEqual(s.term_list,
                         expected_list)

    def test_set_suggestion_type(self):
        original_suggestion = suggestion.Suggestion(
            suggestion_str = 'yo boyz i am sing song')
        original_suggestion.set_suggestion_type('sentence')
        expected_suggestion = suggestion.Suggestion(
            suggestion_str =  'Yo boyz i am sing song.', 
            suggestion_type = 'sentence')
        self.assertEqual(original_suggestion,
                         expected_suggestion)

    def test__iter__(self):
        test_list = ['yo', 'boyz', 'i', 'am', 'sing', 'song']
        test_suggestion = suggestion.Suggestion(test_list)
        # iteration
        for i, term in enumerate(test_suggestion):
            self.assertEqual(term, test_list[i])
        
        # zip
        foo = zip(*enumerate(test_suggestion))
        self.assertEqual(list(foo[0]), range(len(test_list)))
        self.assertEqual(list(foo[1]), test_suggestion)

        self.assertEqual(test_suggestion[:-1],
                         test_list[:-1])

    def test__get_item__(self):
        test_list = ['yo', 'boyz', 'i', 'am', 'sing', 'song']
        test_suggestion = suggestion.Suggestion(test_list)
        self.assertEqual(test_suggestion[3],
                         test_list[3])

    def test__hash__(self):
        # This was a big bug. Because I didn't implement __hash__, the
        # default was probably something based on some hidden
        # properties and so I couldn't use a Suggestion instance A as
        # a key and then try to retrieve the value using an identical
        # Suggestion instance B.
        d = {}
        test_list = ['yo', 'boyz', 'i', 'am', 'sing', 'song']
        test_suggestion = suggestion.Suggestion(test_list)
        new_suggestion = suggestion.Suggestion(test_list)
        d[test_suggestion] = 3
        self.assertTrue(test_suggestion in d)
        self.assertTrue(new_suggestion in d)
        
def get_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(SuggestionTest)
    return suite

if __name__ == '__main__':
    suite = get_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
