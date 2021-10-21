import argparse

from versions.d5 import main as D5, make_D5_subparser
from versions.d6 import main as D6, make_D6_subparser

argparser = argparse.ArgumentParser(description='Consult the oracle and run automated tests with ease.')
subparsers = argparser.add_subparsers(help='Select which diviner version to use', dest='version', required=True)
make_D5_subparser(subparsers)
make_D6_subparser(subparsers)
