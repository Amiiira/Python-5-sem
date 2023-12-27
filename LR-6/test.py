from main import CurrencyTracker

if __name__ == '__main__':

    import unittest

    class TestPrecisionFunc(unittest.TestCase):
        def test_result_type(self):
            self.assertIsInstance(CurrencyTracker(), CurrencyTracker)

        def test_is_singleton(self):
            my_cur_list = CurrencyTracker()
            my_cur_list2 = CurrencyTracker()
            my_cur_list2.get_currencies(['AED', 'QAR', 'EGP'])

            self.assertEqual(id(my_cur_list), id(my_cur_list2))

    unittest.main(
        verbosity=1)  # закомментировать эту строчку, если тестируете в PyCharm