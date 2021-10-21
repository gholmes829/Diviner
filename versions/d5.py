"""
Description:
    Given some test cases, this program automatically queries the oracle and tests your compiler!

See README.md for in depth details.
"""


__author__ = 'Grant Holmes'
__email__ = 'g.holmes429@gmail.com'
__created__ = '10/19/2021'
__modified__ = '10/21/2021'

import sys
sys.path.append('..')
import os.path as osp, os
import argparse
import re

from core import diviner, utils


class DivinerD5(diviner.DivinerBase):
    def __init__(self, compiler_path: str, test_dir_path: str, force_query: bool = False) -> None:
        super().__init__(5, compiler_path, test_dir_path, force_query = force_query)
        self.rm_ptn = re.compile(r' \[[0-9]+,[0-9]+\]\-\[[0-9]+,[0-9]+\]: ')

    def get_actual_output(self, test_i: int, test_name: str, test_path: str) -> str:
        return self.run_compiler(test_path, '-c')
    
    def compare_outputs(self, true_output: str, actual_output: str) -> bool:
        """Determines if outputs should be considered equal. Note, that we
        are no longer required to match pos or order -- just error type."""
        actual_count = utils.count(map(lambda ln: re.sub(self.rm_ptn, ' ', ln), actual_output.split('\n')))
        truth_count = utils.count(map(lambda ln: re.sub(self.rm_ptn, ' ', ln), true_output.split('\n')))
        return actual_count == truth_count


def make_subparser(subparsers) -> argparse.Namespace:
    """Defines and parses cmd line args."""
    parser = subparsers.add_parser('d5')

    parser.add_argument('compiler_path', help='relative path to "cshantyc" executable')
    parser.add_argument('test_dir_path', help='relative path to dir containing "*.cshanty" tests')
    parser.add_argument(
        '-l',
        '--lazy-query',
        default=0,
        nargs='?',
        const=1,
        type=int,
        choices={1, 0},
        help='if 1 (not default), will skip test.cshanty if test.oracle file already present; setting to 0 \
                will query the oracle regardless and overwrite existing test.truth files'
    )
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

        diviner = DivinerD5(compiler_path, test_dir_path, force_query = not args.lazy_query)
        print(diviner.title() + '\n')
        diviner.run_tests()
    
    print(f'Program took {round(t.elapsed, 2)} secs to complete.\n')
    

if __name__ == '__main__':
    main()