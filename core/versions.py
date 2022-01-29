"""
Description:
    Given some test cases, this program automatically queries the oracle and tests your compiler!

See README.md for in depth details.
"""

__author__ = 'Grant Holmes'
__email__ = 'g.holmes429@gmail.com'


import os.path as osp, os
from pipe import select
import re

from core.base import DivinerBase
from core import utils


def versions():
    return list(sorted(DivinerBase.version_registry.values(), key = lambda cls: cls.version) | select(lambda cls: cls.__name__))


def make_diviner(version, *args, **kwargs):
    return DivinerBase.make_version(version, *args, **kwargs)


class D1(DivinerBase):
    version = 1

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_actual_output(self, test_i: int, test_name: str, test_path: str, token_path: str, error_path: str) -> str:
        """Compare true and actual output to determine if they match."""
        res = self.run_compiler(test_path, '-t', token_path, '2>', error_path)
        if not osp.isfile(token_path) or not osp.isfile(error_path) or res and 'Error' in res:
            return None  # failed
        with open(token_path, 'r') as token_f, open(error_path, 'r') as error_f:
            return token_f.read() + error_f.read()

    def compare_outputs(self, true_output: str, actual_output: str) -> bool:
        return true_output == actual_output

    def parse_oracle(self, soup):
        if '(no error output)' in soup.text:
            tokens, errors = soup.find('pre').text, ''
        else:
            tokens, errors = tuple(soup.find_all('pre') | select(lambda match: match.text))
        return tokens + errors

    def get_test_cb_args(self) -> list:
        """Extra args passed to get_actual_output and get_true_output."""
        return [
            [test_path.replace(f'.{self.language_ext}', '_tokens.txt') for test_path in self.test_file_paths],
            [test_path.replace(f'.{self.language_ext}', '_errors.txt') for test_path in self.test_file_paths]
        ]


class D2(DivinerBase):
    version = 2

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_actual_output(self, test_i: int, test_name: str, test_path: str) -> str:
        """Compare true and actual output to determine if they match."""
        res = self.run_compiler(test_path, '-u')

    def compare_outputs(self, true_output: str, actual_output: str) -> bool:
        raise NotImplementedError

    def get_test_cb_args(self) -> list:
        """Extra args passed to get_actual_output and get_true_output."""
        raise NotImplementedError


class D3(DivinerBase):
    version = 3

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_actual_output(self, test_i: int, test_name: str, test_path: str, unparse_path: str) -> str:
        """Compare true and actual output to determine if they match."""
        res = self.run_compiler(test_path, '-u', unparse_path)
        if not osp.isfile(unparse_path) or res and 'Error' in res:
            return None  # failed
        with open(unparse_path, 'r') as unparse_f:
            return unparse_f.read()

    def compare_outputs(self, true_output: str, actual_output: str) -> bool:
        return true_output == actual_output

    def get_test_cb_args(self) -> list:
        """Extra args passed to get_actual_output and get_true_output."""
        return [
            [test_path.replace(f'.{self.language_ext}', 'unparsed.out') for test_path in self.test_file_paths],
        ]


class D4(DivinerBase):
    version = 4

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_actual_output(self, test_i: int, test_name: str, test_path: str) -> str:
        """Compare true and actual output to determine if they match."""
        raise NotImplementedError

    def compare_outputs(self, true_output: str, actual_output: str) -> bool:
        raise NotImplementedError

    def get_test_cb_args(self) -> list:
        """Extra args passed to get_actual_output and get_true_output."""
        raise NotImplementedError


class D5(DivinerBase):
    version = 5

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.rm_ptn = re.compile(r' \[[0-9]+,[0-9]+\]\-\[[0-9]+,[0-9]+\]: ')

    def get_actual_output(self, test_i: int, test_name: str, test_path: str) -> str:
        """Compare true and actual output to determine if they match."""
        return self.run_compiler(test_path, '-c')
    
    def compare_outputs(self, true_output: str, actual_output: str) -> bool:
        """Determines if outputs should be considered equal. Note, that we
        are no longer required to match pos or order -- just error type."""
        actual_count = utils.count(map(lambda ln: re.sub(self.rm_ptn, ' ', ln), actual_output.split('\n')))
        truth_count = utils.count(map(lambda ln: re.sub(self.rm_ptn, ' ', ln), true_output.split('\n')))
        return actual_count == truth_count


class D6(DivinerBase):
    version = 6

    truth_subs = [
        ('AND8', 'AND64'),
        ('OR8', 'OR64'),
        ('NOT8', 'NOT64'),
    ]

    actual_subs = [
        ('tmpVar', 'tmp'),
    ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_actual_output(self, test_i: int, test_name: str, test_path: str, out_path: str) -> str:
        """Compare true and actual output to determine if they match."""
        res = self.run_compiler(test_path, '-a', out_path)
        if not osp.isfile(out_path) or 'Error' in res:
            return None  # failed
        with open(out_path, 'r') as f:
            return f.read()

    def compare_outputs(self, true_output: str, actual_output: str) -> bool:
        """Determines if outputs should be considered equal."""
        true_lns, actual_lns = true_output.split('\n'), actual_output.split('\n')
        if len(true_lns) != len(actual_lns):
            return False
        for true_ln, actual_ln in zip(true_lns, actual_lns):
            for sub in D6.truth_subs:
                true_ln = true_ln.replace(*sub)
            for sub in D6.actual_subs:
                actual_ln = actual_ln.replace(*sub)
            if true_ln != actual_ln:
                return False
        return True
            

    def get_test_cb_args(self) -> list:
        """Extra args passed to get_actual_output and get_true_output."""
        return [[test_path.replace(f'.{self.language_ext}', '.out') for test_path in self.test_file_paths]]


class D7(DivinerBase):
    version = 7

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_actual_output(self, test_i: int, test_name: str, test_path: str) -> str:
        """Compare true and actual output to determine if they match."""
        raise NotImplementedError

    def compare_outputs(self, true_output: str, actual_output: str) -> bool:
        raise NotImplementedError

    def get_test_cb_args(self) -> list:
        """Extra args passed to get_actual_output and get_true_output."""
        raise NotImplementedError


class D8(DivinerBase):
    version = 8

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_actual_output(self, test_i: int, test_name: str, test_path: str) -> str:
        """Compare true and actual output to determine if they match."""
        raise NotImplementedError

    def compare_outputs(self, true_output: str, actual_output: str) -> bool:
        raise NotImplementedError

    def get_test_cb_args(self) -> list:
        """Extra args passed to get_actual_output and get_true_output."""
        raise NotImplementedError