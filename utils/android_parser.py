import argparse


class AndroidParser:
    def __init__(self):
        return

    def get_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--output", help="Location to output data being saved.", required=True
        )

        return parser

    def parse_args(self):
        parser = self.get_parser()
        return parser.parse_args()
