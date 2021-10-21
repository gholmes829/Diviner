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
import subprocess
import argparse
import re

from core import diviner, utils


class DivinerD5(diviner.DivinerBase):
    def __init__(self, compiler_path: str, test_dir_path: str, force_query: bool = False) -> None:
        super().__init__(5, compiler_path, test_dir_path, force_query = force_query)
        self.disregard_pattern = re.compile(r' \[[0-9]+,[0-9]+\]\-\[[0-9]+,[0-9]+\]: ')

    def get_test_cb_args(self) -> list:
        return []

    def get_actual_output(self, test_i: int, test_name: str, test_path: str) -> str:
        try:
            return subprocess.run(
                [f'./{osp.basename(self.compiler_path)}', test_path, '-c'],
                cwd = osp.dirname(self.compiler_path),
                stdout = subprocess.PIPE,
                stderr = subprocess.STDOUT,
            ).stdout.decode(encoding='utf-8')
        except Exception as err:
            utils.fatal_error(f'unable to run compiler "{err.strerror}: {err.filename}".')
    
    def compare_outputs(self, true_output: str, actual_output: str) -> bool:
        """Determines if outputs should be considered equal. Note, that we
        are no longer required to match pos or order -- just error type."""
        actuals = [re.sub(self.disregard_pattern, ' ', ln) for ln in actual_output.split('\n')]
        truths = [re.sub(self.disregard_pattern, ' ', ln) for ln in true_output.split('\n')]
        actual_count = {ln: actuals.count(ln) for ln in set(actuals)}
        truth_count = {ln: truths.count(ln) for ln in set(truths)}
        return actual_count == truth_count


def parse_args() -> argparse.Namespace:
    """Defines and parses cmd line args."""
    parser = argparse.ArgumentParser(description='Consult the oracle and run automated tests with ease.')
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
    return parser.parse_args()    


def main() -> None:
    """Validates inputs then runs main functions."""
    with utils.Timer() as t:
        args = parse_args()
        
        compiler_path = osp.join(os.getcwd(), args.compiler_path)
        if not osp.isfile(compiler_path):
            utils.fatal_error(f'Provided path is not a valid compiler: "{compiler_path}"')
        
        test_dir_path = osp.join(os.getcwd(), args.test_dir_path)
        if not osp.isdir(test_dir_path):
            utils.fatal_error(f'Provided path is not a valid test dir: "{test_dir_path}"')

        diviner = DivinerD5(compiler_path, test_dir_path, force_query = not args.lazy_query)
        print(diviner.title() + '\n')
        diviner.run_tests()
    

if __name__ == '__main__':
    main()