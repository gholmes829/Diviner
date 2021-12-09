"""
Description:
    Given some test cases, this program automatically queries the oracle and tests your compiler!

See README.md for in depth details.
"""


__author__ = 'Grant Holmes'
__email__ = 'g.holmes429@gmail.com'


import sys
sys.path.append('..')
import os.path as osp, os
import argparse

from core.diviner import DivinerBase
from core import utils


class Diviner(DivinerBase):
    def __init__(self, compiler_path: str, test_dir_path: str) -> None:
        super().__init__(7, compiler_path, test_dir_path)

    def get_actual_output(self, test_i: int, test_name: str, test_path: str, s_path: str, o_path: str, e_path: str, out_path: str) -> str:
        """Compare true and actual output to determine if they match."""
        self.run_compiler(test_path, '-o', s_path)
        utils.execute_in_shell(f'as {s_path} -o {o_path}')
        res = utils.execute_in_shell(
            f'ld -dynamic-linker /lib64/ld-linux-x86-64.so.2 \
                /usr/lib/x86_64-linux-gnu/crt1.o \
                /usr/lib/x86_64-linux-gnu/crti.o \
                -lc \
                {o_path} \
                stdcshanty.o \
                /usr/lib/x86_64-linux-gnu/crtn.o \
                -o {e_path} > {out_path}'
            )
        if not osp.isfile(out_path) or 'Segmentation' in res:
            return None  # failed
        with open(e_path, 'r') as f:
            return f.read()

    def compare_outputs(self, true_output: str, actual_output: str) -> bool:
        """Determines if outputs should be considered equal."""
        return true_output == actual_output
            

    def get_test_cb_args(self) -> list:
        """Extra args passed to get_actual_output and get_true_output."""
        return [
            [test_path.replace('.cshanty', '.s') for test_path in self.test_file_paths],
            [test_path.replace('.cshanty', '.o') for test_path in self.test_file_paths],
            [test_path.replace('.cshanty', '.exe') for test_path in self.test_file_paths],
            [test_path.replace('.cshanty', '.out') for test_path in self.test_file_paths]
        ]
    

def make_subparser(subparsers) -> argparse.Namespace:
    """Defines and parses cmd line args."""
    parser = subparsers.add_parser('d7')
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