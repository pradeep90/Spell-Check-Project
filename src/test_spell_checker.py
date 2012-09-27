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

    def test_generate_suggestions_and_posteriors(self):
        query = 'foo'
        suggestions = self.spell_checker.generate_suggestions_and_posteriors(query)
        expected = [('believe', 0.11),
                    ('buoyant', 0.02),
                    ('committed', 0.14999999999999999),
                    ('distract', 0.040000000000000001),
                    ('ecstacy', 0.040000000000000001),
                    ('fairy', 0.050000000000000003),
                    ('hello', 0.02),
                    ('gracefully', 0.059999999999999998),
                    ('liaison', 0.070000000000000007),
                    ('occasion', 0.10000000000000001),
                    ('possible', 0.01),
                    ('throughout', 0.029999999999999999),
                    ('volley', 0.070000000000000007),
                    ('tattoos', 0.040000000000000001),
                    ('respect', 0.19)
                    ]
        self.assertEqual(suggestions,
                         expected)

    def test_run_spell_check(self):
        self.spell_checker.run_spell_check(['yo', 'boyz'])
        self.assertEqual(self.spell_checker.suggestion_dict['yo'],
                         self.spell_checker.generate_suggestions_and_posteriors('yo'))
        self.assertEqual(self.spell_checker.suggestion_dict['boyz'],
                         self.spell_checker.generate_suggestions_and_posteriors('boyz'))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SpellCheckerTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
