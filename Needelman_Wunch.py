import numpy as np
import json
import click


class InputError(ValueError):
    def __init__(self, exception):
        super().__init__('Wrong input:\n' + str(exception))


# Needelman-Wunch table
class NwTable:
    def __init__(self, seq1, seq2, config):
        #  Use first input sequence as a rows names
        #  First output sequence is alignment for first input
        pass
        # TODO

    def get_path(self):
        #  generates all paths.
        pass
        # TODO

    def __get_path__(self, x, y):
        #  generates paths starting in (x, y) position.
        pass
        # TODO


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


def read_fasta_file(file, max_len):
    lines = file.readlines()[1:]
    text = ''.join(lines)
    text = "".join(text.split())
    if len(text) > max_len:
        raise InputError('Fasta sequence too long.')
    text = text.upper()
    return text


@click.command()
@click.option('--seq1_file', '-a', help='First sequence file.', type=click.File('r'))
@click.option('--seq2_file', '-b', help='Second sequence file.', type=click.File('r'))
@click.option('--config_file', '-c', help='Config file.', type=click.File('r'))
@click.option('--output', '-o', help='Output file', type=click.File('w'))
def main(seq1_file, seq2_file, config_file, output):
    pass
    #  TODO: parse config
    #  TODO: read files into sentences
    #  TODO: Build NW table
    #  TODO: Print paths to file


if __name__ == "__main__":
    main()
