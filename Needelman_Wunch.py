import numpy as np
import json
import click


@click.command()
@click.option('--seq1', "-a", help='First sequence.', type=click.File('r'))
@click.option('--seq2', '-b', help='Second sequence.', type=click.File('r'))
@click.option('--config_file', '-c', help='Config file.', type=click.File('r'))
@click.option('--output', '-o', help='Output file', type=click.File('w'))
def main(seq1, seq2, config_file, output):
    config_json = config_file.read()
    config = json.dumps(config_json)


if __name__ == "__main__":
    main()
