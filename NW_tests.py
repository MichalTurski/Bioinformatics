import json
import unittest
from io import StringIO
from unittest.mock import MagicMock

import Needelman_Wunch


class TestConfig(unittest.TestCase):
    def test_correct_json(self):
        file_mock = StringIO('{"GP": 1, "SAME": 2, "DIFF": 3, "MAX_SEQ_LENGTH": 4, "MAX_PATHS": 5,}')
        config = Needelman_Wunch.Config(file_mock)
        self.assertEqual(config.gap_penalty, 1)
        self.assertEqual(config.same_reward, 2)
        self.assertEqual(config.diff_penalty, 3)
        self.assertEqual(config.max_seq_length, 4)
        self.assertEqual(config.max_paths, 5)

    def test_not_json(self):
        file_mock = StringIO('jnaiolfubsiao')
        self.assertRaises(Needelman_Wunch.InputError, Needelman_Wunch.Config(file_mock))

    def test_lack_value(self):
        file_mock = StringIO('{"SAME": 2, "DIFF": 3, "MAX_SEQ_LENGTH": 4, "MAX_PATHS": 5,}')
        self.assertRaises(Needelman_Wunch.InputError, Needelman_Wunch.Config(file_mock))


class TestReadFastaFile(unittest.TestCase):
    def


class TestNwTable(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
