#!/usr/bin/python

import spell_checker
import test_utils
import lexicon
import test_lexicon
from suggestion import Suggestion
import test_phrase
import test_suggestion
import test_edit_distance_calculator
import test_spell_checker
import unittest

if __name__ == '__main__':
    test_suites = [test_spell_checker.get_suite(),
                   test_utils.get_suite(),
                   test_lexicon.get_suite(),
                   test_edit_distance_calculator.get_suite(),
                   test_phrase.get_suite(),
                   test_suggestion.get_suite(),
                   ]

    all_tests = unittest.TestSuite(test_suites)
    unittest.TextTestRunner(verbosity=2).run(all_tests)
