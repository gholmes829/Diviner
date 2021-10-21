import argparse

from versions.d5 import make_D5_subparser
from versions.d6 import make_D6_subparser
make_subparsers = [make_D5_subparser, make_D6_subparser]

argparser = argparse.ArgumentParser(description='Consult the oracle and run automated tests with ease.')
subparsers = argparser.add_subparsers(help='Select which diviner version to use', dest='version', required=True)
for make_subparser in make_subparsers: make_subparser(subparsers)