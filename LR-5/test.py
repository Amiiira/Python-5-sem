from main import CurrencyTracker
import unittest

class TestCurrencyTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = CurrencyTracker()

    def test_get_currencies(self):
        currencies = self.tracker.get_currencies()
        self.assertIsInstance(currencies, dict)

    def test_get_currency_value(self):
        aed_value = self.tracker.get_currency_value('AED')
        self.assertIsInstance(aed_value, (float, str))

    def test_add_tracked_currency(self):
        initial_tracked_currencies = self.tracker.get_tracked_currencies()

        self.tracker.add_tracked_currency('JPY')
        updated_tracked_currencies = self.tracker.get_tracked_currencies()
        self.assertIn('JPY', updated_tracked_currencies)

        self.assertCountEqual(initial_tracked_currencies, updated_tracked_currencies)

    def test_set_tracked_currencies(self):
        new_tracked_currencies = ['USD', 'EUR', 'JPY']
        self.tracker.set_tracked_currencies(new_tracked_currencies)
        updated_tracked_currencies = self.tracker.get_tracked_currencies()
        self.assertCountEqual(new_tracked_currencies, updated_tracked_currencies)

    def test_repr(self):
        representation = repr(self.tracker)
        self.assertIn("CurrencyTracker", representation)
        self.assertIn("tracked_currencies", representation)
        self.assertIn("last_update_time", representation)



if __name__ == '__main__':
    unittest.main()
