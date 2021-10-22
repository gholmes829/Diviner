"""
Description:
    Given some test cases, this program automatically queries the oracle and tests your compiler!

See README.md for in depth details.
"""


__author__ = 'Grant Holmes'
__email__ = 'g.holmes429@gmail.com'
__created__ = '10/21/2021'
__modified__ = '10/21/2021'


import sys
sys.path.append('..')
import os.path as osp, os
import argparse

from core.diviner import DivinerBase
from core import utils


class Diviner(DivinerBase):
    def __init__(self, compiler_path: str, test_dir_path: str) -> None:
        super().__init__(6, compiler_path, test_dir_path)
        raise NotImplementedError
    

def make_subparser(subparsers) -> argparse.Namespace:
    """Defines and parses cmd line args."""
    parser = subparsers.add_parser('d6')
    parser.add_argument('compiler_path', help='relative path to "cshantyc" executable')
    parser.add_argument('test_dir_path', help='relative path to dir containing "*.cshanty" tests')
    parser.set_defaults(func = main)
    
    return parser  


def main(args) -> None:
    """Validates inputs then runs main functions."""
    with utils.Timer() as t:
        compiler_path = osp.join(os.getcwd(), args.compiler_path)
        if not osp.isfile(compiler_path):
            utils.fatal_error(f'Provided path is not a valid compiler: "{compiler_path}"')
        
        test_dir_path = osp.join(os.getcwd(), args.test_dir_path)
        if not osp.isdir(test_dir_path):
            utils.fatal_error(f'Provided path is not a valid test dir: "{test_dir_path}"')

        diviner = Diviner(compiler_path, test_dir_path)
        print(diviner.title() + '\n')
        diviner.run_tests()
    
    print(f'Program took {round(t.elapsed, 2)} secs to complete.\n')


if __name__ == '__main__':
    main()