"""
Description:
    Given some test cases, this program automatically queries the oracle and tests your compiler!

See README.md for in depth details.
"""


__author__ = 'Grant Holmes'
__email__ = 'g.holmes429@gmail.com'
__created__ = '10/21/2021'
__modified__ = '11/3/2021'


import sys
sys.path.append('..')
import os.path as osp, os
import argparse

from core.diviner import DivinerBase
from core import utils


class Diviner(DivinerBase):
    truth_subs = [
        ('AND8', 'AND64'),
        ('OR8', 'OR64'),
        ('NOT8', 'NOT64'),
    ]

    actual_subs = [
        ('tmpVar', 'tmp'),
    ]

    def __init__(self, compiler_path: str, test_dir_path: str) -> None:
        super().__init__(6, compiler_path, test_dir_path)

    def get_actual_output(self, test_i: int, test_name: str, test_path: str, out_path: str) -> str:
        """Compare true and actual output to determine if they match."""
        res = self.run_compiler(test_path, '-a', out_path)
        if not osp.isfile(out_path) or 'Error' in res:
            return None  # failed
        with open(out_path, 'r') as f:
            return f.read()

    def compare_outputs(self, true_output: str, actual_output: str) -> bool:
        """Determines if outputs should be considered equal."""
        for true_ln, actual_ln in zip():
            for sub in Diviner.truth_subs:
                true_ln = true_ln.replace(*sub)
            for sub in Diviner.actual_subs:
                actual_ln = actual_ln.replace(*sub)
            if true_ln != actual_ln:
                return False
        return True
            

    def get_test_cb_args(self) -> list:
        """Extra args passed to get_actual_output and get_true_output."""
        return [[test_path.replace('.cshanty', '.out') for test_path in self.test_file_paths]]
    

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