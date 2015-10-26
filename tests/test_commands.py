import unittest
from datetime import datetime

from usage.management.commands.summarizeusage import _round_to_interval


class TestRoundToInterval(unittest.TestCase):

    input = datetime(2015, 10, 15, 10, 43, 21, 11)

    def test_simple_case(self):
        expected = datetime(2015, 10, 15, 10, 40)
        output = _round_to_interval(self.input, 5)
        self.assertEqual(expected, output)

    def test_60_case(self):
        expected = datetime(2015, 10, 15, 10, 00)
        output = _round_to_interval(self.input, 60)
        self.assertEqual(expected, output)

if __name__ == '__main__':
    unittest.main()
