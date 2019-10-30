import numpy as np
import json
import click


# Needelman-Wunch table
class NwTable:
    def __init__(self, seq1, seq2, config):
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
        config_dict = json.dumps(config_json)
        self.gap_penalty = config_dict.GP
        self.same_reward = 0  # TODO
        self.diff_penalty = 0  # TODO
        self.max_seq_length = 10  # TODO
        self.max_paths = 3  # TODO


def read_fasta_file(file):
    pass
    #  return seq


@click.command()
@click.option('--seq1_file', '-a', help='First sequence.', type=click.File('r'))
@click.option('--seq2_file', '-b', help='Second sequence.', type=click.File('r'))
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
