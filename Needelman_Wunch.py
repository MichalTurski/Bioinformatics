import numpy as np
import json
import click
import sys
import time


class InputError(ValueError):
    def __init__(self, exception):
        super().__init__('Wrong input:\n' + str(exception))


# Needelman-Wunch table
class NwTable:
    def __init__(self, seq1, seq2, config):
        #  Use first input sequence as a rows names
        self.seq1 = '_' + seq1
        self.seq2 = '_' + seq2
        self.config = config
        self.table = np.zeros((len(self.seq1), len(self.seq2)))
        for i in range(len(self.seq1)):
            for j in range(len(self.seq2)):
                if i == 0:
                    self.table[i, j] = j * config.gap_penalty
                elif j == 0:
                    self.table[i, j] = i * config.gap_penalty
                else:
                    self.__update_field__(i, j)

        #  First output sequence is alignment for first input

    def __calculate_possibilities__(self, i, j):
        if i > 0:
            val_if_up = self.table[i - 1, j] + self.config.gap_penalty
        else:
            val_if_up = np.nan

        if j > 0:
            val_if_left = self.table[i, j - 1] + self.config.gap_penalty
        else:
            val_if_left = np.nan

        if i == 0 and j == 0:
            val_if_corner = np.nan
        else:
            if self.seq1[i] == self.seq2[j]:
                val_if_corner = self.table[i - 1, j - 1] + self.config.same_reward
            else:
                val_if_corner = self.table[i - 1, j - 1] + self.config.diff_penalty

        return val_if_left, val_if_corner, val_if_up

    def __update_field__(self, i, j):
        (val_if_left, val_if_corner, val_if_up) = self.__calculate_possibilities__(i, j)
        self.table[i, j] = max(val_if_left, val_if_corner, val_if_up)

    def path_generator(self):
        i = len(self.seq1) - 1
        j = len(self.seq2) - 1
        for num, path in enumerate(self.__get_path__(i, j)):
            if num == self.config.max_paths:
                break
            yield int(self.table[i, j]), path

    def __get_path__(self, i, j):
        #  generates paths starting in (x, y) position.
        if i == j == 0:
            yield ('', '')
        else:
            val_if_left, val_if_corner, val_if_up = self.__calculate_possibilities__(i, j)
            if val_if_up == self.table[i, j]:
                for prefixes in self.__get_path__(i - 1, j):
                    yield (prefixes[0] + self.seq1[i], prefixes[1] + '_')

            if val_if_left == self.table[i, j]:
                for prefixes in self.__get_path__(i, j - 1):
                    yield (prefixes[0] + '_', prefixes[1] + self.seq2[j])

            if val_if_corner == self.table[i, j]:
                if self.seq1[i] == self.seq2[j]:
                    char_to_prepend = self.seq2[j]
                else:
                    char_to_prepend = '_'
                for prefixes in self.__get_path__(i - 1, j - 1):
                    yield (prefixes[0] + char_to_prepend, prefixes[1] + char_to_prepend)


class Config:
    def __init__(self, config_file):
        #  TODO: handle errors, throw exceptions and so on.
        config_json = config_file.read()
        try:
            config_dict = json.loads(config_json)
        except json.JSONDecodeError as e:
            raise InputError('Unable to parse configuration.')
        try:
            self.gap_penalty = config_dict['GP']
            self.same_reward = config_dict['SAME']
            self.diff_penalty = config_dict['DIFF']
            self.max_seq_length = config_dict['MAX_SEQ_LENGTH']
            self.max_paths = config_dict['MAX_PATHS']
        except KeyError as e:
            raise InputError('Parameter ' + str(e) + ' not specified.')
        sys.setrecursionlimit(max(2 * self.max_seq_length, sys.getrecursionlimit()))


def read_fasta_file(file, max_len):
    lines = file.readlines()[1:]
    text = ''.join(lines)
    if not text:
        raise InputError('There is no fasta sequence.')
    text = "".join(text.split())
    if len(text) > max_len:
        raise InputError('Fasta sequence too long.')
    text = text.upper()
    return text


@click.command()
@click.option('--seq1_file', '-a', help='First sequence file.', type=click.File('r'), required=True)
@click.option('--seq2_file', '-b', help='Second sequence file.', type=click.File('r'), required=True)
@click.option('--config_file', '-c', help='Config file.', type=click.File('r'), required=True)
@click.option('--output', '-o', help='Output file', type=click.File('w'), required=True)
def main(seq1_file, seq2_file, config_file, output):
    try:
        config = Config(config_file)
        in_seq1 = read_fasta_file(seq1_file, config.max_seq_length)
        in_seq2 = read_fasta_file(seq2_file, config.max_seq_length)
    except InputError as e:
        print(str(e))
    else:
        start_time = time.time()
        nw_table = NwTable(in_seq1, in_seq2, config)
        print("Table creation: %s seconds" % (time.time() - start_time))
        start_time = time.time()
        for score, alignments in nw_table.path_generator():
            output.write(str(score))
            output.write('\n')
            output.write(alignments[0])
            output.write('\n')
            output.write(alignments[1])
            output.write('\n')
        print("Paths generation and printing: %s seconds" % (time.time() - start_time))


if __name__ == "__main__":
    main()
