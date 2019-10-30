import json
import unittest
from io import StringIO
from unittest.mock import MagicMock

import Needelman_Wunch


class TestConfig(unittest.TestCase):
    def test_correct_json(self):
        file_mock = StringIO('{"GP": 1, "SAME": 2, "DIFF": 3, "MAX_SEQ_LENGTH": 4, "MAX_PATHS": 5}')
        config = Needelman_Wunch.Config(file_mock)
        self.assertEqual(config.gap_penalty, 1)
        self.assertEqual(config.same_reward, 2)
        self.assertEqual(config.diff_penalty, 3)
        self.assertEqual(config.max_seq_length, 4)
        self.assertEqual(config.max_paths, 5)

    def test_not_json(self):
        file_mock = StringIO('jnaiolfubsiao')
        with self.assertRaises(Needelman_Wunch.InputError):
            Needelman_Wunch.Config(file_mock)

    def test_lack_value(self):
        file_mock = StringIO('{"SAME": 2, "DIFF": 3, "MAX_SEQ_LENGTH": 4, "MAX_PATHS": 5}')
        with self.assertRaises(Needelman_Wunch.InputError):
            Needelman_Wunch.Config(file_mock)


class TestReadFastaFile(unittest.TestCase):
    def test_empty_fasta(self):
        file_mock = StringIO('')
        with self.assertRaises(Needelman_Wunch.InputError):
            Needelman_Wunch.read_fasta_file(file_mock, 100)

    def test_almost_empty_fasta(self):
        file_mock = StringIO('first line \n')
        with self.assertRaises(Needelman_Wunch.InputError):
            Needelman_Wunch.read_fasta_file(file_mock, 100)

    def test_file_too_long(self):
        file_mock = StringIO('first line \n TEITAAMVKELRESTGAGMMDCKNALSETNGDFDKAVQLLREKGLGKAAKKAD')
        with self.assertRaises(Needelman_Wunch.InputError):
            Needelman_Wunch.read_fasta_file(file_mock, 10)

    def test_valid_fasta(self):
        file_mock = StringIO('first line \n TEITAAMVKELREST GAGMMDCKN\nALSETNGDFDKAVQLLR EKGLGKAAKKAD')
        seq = Needelman_Wunch.read_fasta_file(file_mock, 100)
        self.assertEqual(seq, 'TEITAAMVKELRESTGAGMMDCKNALSETNGDFDKAVQLLREKGLGKAAKKAD')

    def test_small_case(self):
        file_mock = StringIO('first line \n teitAAMVKELreST')
        seq = Needelman_Wunch.read_fasta_file(file_mock, 100)
        self.assertEqual(seq, 'TEITAAMVKELREST')


class TestNwTable(unittest.TestCase):
    def test_same_length_seq(self):
        config_file_mock = StringIO('{"GP": -2, "SAME": 2, "DIFF": -3, "MAX_SEQ_LENGTH": 10, "MAX_PATHS": 5}')
        config = Needelman_Wunch.Config(config_file_mock)
        seq1 = 'ABC'
        seq2 = 'ADC'
        table = Needelman_Wunch.NwTable(seq1, seq2, config)
        paths_generator = table.path_generator()
        score, paths = next(paths_generator)
        self.assertEqual(score, 1)
        self.assertSequenceEqual(paths, ('A_C', 'A_C'))
        with self.assertRaises(StopIteration):
            next(paths_generator)

    def test_diff_length_seq(self):
        config_file_mock = StringIO('{"GP": -2, "SAME": 2, "DIFF": -3, "MAX_SEQ_LENGTH": 10, "MAX_PATHS": 5}')
        config = Needelman_Wunch.Config(config_file_mock)
        seq1 = 'ADB'
        seq2 = 'AB'
        table = Needelman_Wunch.NwTable(seq1, seq2, config)
        paths_generator = table.path_generator()
        score, paths = next(paths_generator)
        self.assertEqual(score, 2)
        self.assertSequenceEqual(paths, ('ADB', 'A_B'))
        with self.assertRaises(StopIteration):
            next(paths_generator)

    def test_multiple_output(self):
        config_file_mock = StringIO('{"GP": -2, "SAME": 2, "DIFF": -5, "MAX_SEQ_LENGTH": 10, "MAX_PATHS": 5}')
        expected_seqs = {('AB_', 'A_D'), ('A_B', 'AD_')}
        config = Needelman_Wunch.Config(config_file_mock)
        seq1 = 'AB'
        seq2 = 'AD'
        table = Needelman_Wunch.NwTable(seq1, seq2, config)
        paths_generator = table.path_generator()
        score1, out_seqs1 = next(paths_generator)
        score2, out_seqs2 = next(paths_generator)
        self.assertEqual(score1, -2)
        self.assertEqual(score2, -2)
        self.assertTrue({out_seqs1}.issubset(expected_seqs))
        self.assertTrue({out_seqs2}.issubset(expected_seqs))
        with self.assertRaises(StopIteration):
            next(paths_generator)

    def test_output_limit(self):
        config_file_mock = StringIO('{"GP": -2, "SAME": 2, "DIFF": -5, "MAX_SEQ_LENGTH": 10, "MAX_PATHS": 1}')
        expected_seqs = {('AB_', 'A_D'), ('A_B', 'AD_')}
        config = Needelman_Wunch.Config(config_file_mock)
        seq1 = 'AB'
        seq2 = 'AD'
        table = Needelman_Wunch.NwTable(seq1, seq2, config)
        paths_generator = table.path_generator()
        score1, out_seqs1 = next(paths_generator)
        self.assertEqual(score1, -2)
        self.assertTrue({out_seqs1}.issubset(expected_seqs))
        with self.assertRaises(StopIteration):
            next(paths_generator)


if __name__ == '__main__':
    unittest.main()
