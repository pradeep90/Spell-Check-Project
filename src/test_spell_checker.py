#!/usr/bin/python

import spell_checker
import utils
import test_utils
import unittest

class SpellCheckerTest(unittest.TestCase):
    def setUp(self):
        self.spell_checker = spell_checker.SpellChecker()

    def tearDown(self):
        pass

    def test_foo(self):
        self.assertEqual(3 + 4,
                         7)

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

def get_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(SpellCheckerTest)
    return suite

if __name__ == '__main__':
    spell_checker_suite = get_suite()
    utils_suite = test_utils.get_suite()
    test_suites = [spell_checker_suite, utils_suite]

    all_tests = unittest.TestSuite(test_suites)
    unittest.TextTestRunner(verbosity=2).run(all_tests)
