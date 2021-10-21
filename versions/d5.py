"""
Description:
    Given some test cases, this program automatically queries the oracle and tests your compiler!

More spefically this program:
    1) Runs your test inputs thru the oracle & collects its response
        to give a "true output"; writes "<test>.truth" to test dir.
        
    2) Runs all your test inputs through your compiled compiler & collects
        outputs to give an "actual output"; writes <test>.actual to test dir.
        
    3) For each (<test>.oracle, <test>.actual) pair, runs diff to check if
        your comiler is producing correct output; provides score and details.       

Formal Usage:
    python3 diviner.py <path to cshantyc> <path to dir containing *.cshantyc test cases> <-l, optional>
    python3 diviner.py --help

Example usage:
    python3 diviner cshantyc my_tests/
    python3 diviner cshantyc my_tests/ --lazy-query
    python3 diviner cshantyc my_tests/ -l
    python3 diviner --help
    
    ...where my_tests/ might contain test1.cshanty, test2.cshanty, etc.
    
Dependencies:
    - python3 (https://www.python.org/downloads/)
    - bs4 (pip3 install bs4)
    - tqdm (pip3 install tqdm)
    
    ...the rest should be standard.
    
    You can also run 'make install' or 'pip3 install -r requirements.txt' for convenience
    While we are on the topic of make directives, 'make clean' removes all compiled *.pyc
    
Notes:
    - For a given "test.cshanty", if this program already detects a "test.oracle" it
        will still requery the oracle for that test. Setting lazy-query to 1 in cmd
        line will instead skip it to avoid excess time and requests.
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