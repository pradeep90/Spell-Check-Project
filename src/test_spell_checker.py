import unittest

class SpellCheckerTest(unittest.TestCase):
    def setUp(self):
        self.foo = 'Yo, Boyz'

    def tearDown(self):
        pass

    def test_foo(self):
        self.assertEqual(self.foo, 'Yo, Boyz')

    def test_bar(self):
        self.assertEqual(3 + 4, 7)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SpellCheckerTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
