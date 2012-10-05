#!/usr/bin/python

import phrase
import unittest

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
        query = ['foo']
        suggestion = ['bar']
        expected = -(phrase.get_edits(suggestion[0], query[0])[0] / len(query[0]))
        self.assertAlmostEqual(phrase.get_likelihood(query, suggestion),
                               expected, 2)

        # query = [
        #     'the', 'departments', 'of', 'the', 'institute', 
        #     'offer', 'corses', 'conducted', 'by', 'highly', 'qualified', 'staff']
        # suggestion = [
        #     'the', 'departments', 'of', 'the', 'institute', 
        #     'offer', 'coarsest', 'conducted', 'by', 'highly', 'qualified', 'staff']
        # expected = -0.00070509367744390789

        # self.assertAlmostEqual(phrase.get_likelihood(query, suggestion),
        #                        expected, 2)

def get_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(PhraseTest)
    return suite

if __name__ == '__main__':
    suite = get_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
