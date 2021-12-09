import argparse

from versions import d5, d6, d7

exposed_versions = [d5, d6, d7]

argparser = argparse.ArgumentParser(description='Consult the oracle and run automated tests with ease.')
subparsers = argparser.add_subparsers(help='Select which diviner version to use', dest='version', required=True)
for version in exposed_versions: version.make_subparser(subparsers)