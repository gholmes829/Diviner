"""
Contains base class for The Diviner.
"""

__author__ = 'Grant Holmes'
__email__ = 'g.holmes429@gmail.com'


from abc import ABCMeta, abstractmethod
import os.path as osp, os
import requests
from typing import BinaryIO
from bs4 import BeautifulSoup
from functools import reduce
from pipe import where, select
from tqdm.contrib.concurrent import thread_map

from core import utils

# TODO check for cached compiler output

class DivinerBase(metaclass = ABCMeta):
    version = None
    version_registry = {}

    def __init_subclass__(cls) -> None:
        if not hasattr(cls, 'version') or cls.version in DivinerBase.version_registry:
            utils.fatal_error(f'{cls} must have a unique hashable static version attribute')
        DivinerBase.version_registry[cls.__name__] = cls

    def __init__(self,
                language_ext: str,
                compiler_path: str,
                test_dir_path: str,
                write_to_file: bool = True,
            ) -> None:
        # path validation
        if not osp.isdir(osp.join(os.getcwd(), test_dir_path)):
            utils.fatal_error(f'<test_dir_path>, "{test_dir_path}", is not a directory')
        if not osp.isfile(osp.join(os.getcwd(), compiler_path)):
            utils.fatal_error(f'<compiler_path>, "{compiler_path}", is not a file')
        
        # store args
        self.oracle_url = f'https://compilers.cool/oracles/o{self.version}/'
        self.title_str = utils.make_title(f'THE DIVINER (P{self.version})')
        self.language_ext = language_ext

        self.compiler_path = compiler_path
        self.test_dir_path = test_dir_path

        self.write_to_file = write_to_file

        # collecting files
        self.test_file_names = list(os.listdir(test_dir_path) | where(lambda f: f.endswith(language_ext)))
        self.test_file_paths = list(self.test_file_names | select(lambda f_name: osp.join(test_dir_path, f_name)))
        self.test_data = [range(len(self.test_file_names)), self.test_file_names, self.test_file_paths]
        self.n_tests = len(self.test_file_names)

        # file validation
        duplicates = {name for name, c in utils.count(self.test_file_names).items() if c > 1}
        if duplicates:
            utils.fatal_error(f'test_dir_path, "{test_dir_path}" contains duplicates: {duplicates}')

        if not len(self.test_file_names):
            utils.fatal_error(f'no "*.{language_ext}" test cases found in "{test_dir_path}".')

        # evaluation
        self.oracle_requests_count = 0
        self.actual_outputs = None
        self.true_outputs = None


    @abstractmethod
    def compare_outputs(self, true_output: str, actual_output: str, *args) -> bool:
        """Compare true and actual output to determine if they match."""
        raise NotImplementedError
    

    @abstractmethod
    def get_actual_output(self, test_i: int, test_name: str, test_path: str, *args) -> str:
        """Get the real output that will be compared to the expected output."""
        raise NotImplementedError
    

    def get_true_output(self, test_i: int, test_name: str, test_path: str) -> str:
        self.oracle_requests_count += 1
        with open(test_path, 'rb') as f:
            return self.parse_oracle(self.scrape_oracle(f))


    def get_test_cb_args(self) -> list:
        """Extra args passed to get_actual_output and get_true_output."""
        return None

    def title(self):
        return self.title_str


    def run_compiler(self, *args) -> str:
        utils.execute_in_shell(f'./{self.compiler_path} ' + ' '.join(list(args)))

    @staticmethod
    def make_version(version: str, *args, **kwargs) -> 'DivinerBase':
        return DivinerBase.version_registry[version](*args, **kwargs)
    

    @utils.retryable(err_msg='could not connect to oracle', verbose = False)
    def scrape_oracle(self, test_file: BinaryIO) -> str:
        """Queries the oracle with a given test case and returns output."""
        res = requests.post(self.oracle_url, files={'input': test_file})
        if res.status_code == 200: return BeautifulSoup(res.text, 'html.parser')
        else: raise ConnectionError

    def parse_oracle(self, soup):
        return soup.find('pre').text


    def run_test(self, passed_map: dict, test_i: int, test_name: str, test_path: str, *args) -> int:
        """Gets the actual and true output, compares them, and writes to files."""
        base = test_name.split(".")[0]
        truth_path = osp.join(self.test_dir_path, f'{base}.truth')
        actual_path = osp.join(self.test_dir_path, f'{base}.actual')
        
        # if file does not exist or cached result outdated
        if not osp.isfile(truth_path) or osp.getmtime(test_path) > osp.getmtime(truth_path):
            true_output = self.get_true_output(test_i, test_name, test_path)
            if true_output and self.write_to_file:
                with open(truth_path, 'w') as f:
                    f.write(true_output)
        else:  # cached result is valid and up-to-date
            with open(truth_path, 'r') as f:
                true_output = f.read()

        # lets see what we are actually getting
        actual_output = self.get_actual_output(test_i, test_name, test_path, *args)
        if true_output is None or actual_output is None:  # failed to generate
            passed_map['null'].append(test_name)
            return 0
        else:  # successful evaluation
            if self.write_to_file:
                with open(actual_path, 'w') as f:
                    f.write(actual_output)
                
            passed = 'passed' * self.compare_outputs(true_output, actual_output) or 'failed'
            passed_map[passed].append(test_name)
            return 1


    def run_tests(self) -> None:
        """Use multithreading to run all tests then display results."""
        print(f'Consulting with The Oracle at "{self.oracle_url}" and evaluating on local compiler...')
        passed_map = {'failed': [], 'passed': [], 'null': []}
        params = list(zip(*reduce(lambda b, a: b + [a], self.get_test_cb_args() or [], self.test_data)))
        with utils.Timer() as t:
            try:
                exit_codes = list(thread_map(lambda params: self.run_test(passed_map, *params), params))
            except Exception as err:
                print(err)
                utils.fatal_error('exception occurred while evaluating tests.')
            else:
                self.print_test_results(passed_map['failed'], passed_map['passed'], passed_map['null'], t.elapsed)


    def print_test_results(self, failed_cases: list, passed_cases: list, null_cases: list, elapsed: float) -> None:
        percent_passed = 100 * len(passed_cases) / self.n_tests

        print()
        self.print_case_outcomes('passed', passed_cases)
        self.print_case_outcomes('failed', failed_cases)
        self.print_case_outcomes('null', null_cases)

        print(f'\n\nUsed {self.n_tests - self.oracle_requests_count} cached up-to-date truth queries.\n\n')
        if self.write_to_file: print(f'Wrote *.truth and *.actual files to "{self.test_dir_path}".\n\n')
        print(
            f'Completed {self.n_tests} test cases in {round(elapsed, 2)} secs.\n'
            f'Score: {len(passed_cases)}/{self.n_tests} ({round(percent_passed, 2)}%)\n'
        )


    def print_case_outcomes(self, outcome: str, cases: list) -> None:
        if cases:
            print(f'\nThe following tests {outcome.upper()}:')
            for test in sorted(cases): print(f'\t- {test}')
        else: print(f'\nNo test cases {outcome}.')