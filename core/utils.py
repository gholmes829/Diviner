"""
Contains the TestManager base class and other useful utility based class/ fns.
"""

import sys
import os.path as osp, os
from typing import Callable, Iterable, Iterator
import time
import abc
from tqdm import tqdm
from functools import wraps, reduce
from concurrent.futures import ThreadPoolExecutor


__author__ = 'Grant Holmes'
__email__ = 'g.holmes429@gmail.com'
__created__ = '10/19/2021'
__modified__ = '10/21/2021'


class TestManager(metaclass=abc.ABCMeta):
    """
    Abstracted test manager. Must implement required abstract methods for particular use case.
    """
    def __init__(self, test_dir_path, test_ext) -> None:
        self.test_dir_path = test_dir_path
        self.test_ext = test_ext
        
        self.test_file_names = [f for f in os.listdir(test_dir_path) if f.split('.')[-1] == test_ext]
        self.n_tests = len(self.test_file_names)
        
        if not self.n_tests:
            fatal_error(f'no "*.{test_ext}" test cases found in "{test_dir_path}".')
            
        self.test_file_paths = [osp.join(test_dir_path, f_name) for f_name in self.test_file_names]

        self.test_data = [range(self.n_tests), self.test_file_names, self.test_file_paths]
        
        self.actual_outputs = None
        self.true_outputs = None
        
        self.pbar = None

    @abc.abstractmethod
    def compare_outputs(self, true_output: str, actual_output: str, *args) -> bool:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_actual_output(self, test_i: int, test_name: str, test_path: str, *args) -> str:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_true_output(self, test_i: int, test_name: str, test_path: str, *args) -> str:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_test_cb_args(self) -> list:
        raise NotImplementedError
    
    def run_test(self, passed_map, test_i, test_name, test_path):
        true_ouput = self.get_true_output(test_i, test_name, test_path)
        actual_output = self.get_actual_output(test_i, test_name, test_path)
        
        if true_ouput is None or actual_output is None:
            return 0  # failed
        else:
            base = test_name.split(".")[0]
            truth_path = osp.join(self.test_dir_path, f'{base}.truth')
            actual_path = osp.join(self.test_dir_path, f'{base}.actual')
            
            with open(actual_path, 'w') as f1, open(truth_path, 'w') as f2:
                f1.write(actual_output)
                f2.write(true_ouput)
                
            passed = self.compare_outputs(true_ouput, actual_output)
            passed_map[passed].append(test_name)
            self.pbar.update(1)
            return 1  # success

    def run_tests(self) -> None:
        self.print_pre_info()
        passed_map = {False: [], True: []}
        params = list(zip(*reduce(lambda b, a: b + [a], self.get_test_cb_args(), self.test_data)))
        with Timer() as t, tqdm(total=self.n_tests, ascii=True) as self.pbar:
            exit_codes = threaded_map(lambda params: self.run_test(passed_map, *params), params)

        try:
            _ = list(exit_codes)
        except Exception:
            self.pbar.close()
            fatal_error('exception occurred while evaluating tests.')
        else:
            self.print_test_results(passed_map[0], passed_map[1], t.elapsed)
        
    def print_test_results(self, failed_cases: list, passed_cases: list, elapsed: float) -> None:
        percent_passed = 100 * len(passed_cases) / self.n_tests
        self.print_cases('passed', passed_cases)
        self.print_cases('failed', failed_cases)
        self.print_post_info()
        print(f'\n\nWrote *.truth and *.actual files to "{self.test_dir_path}".\n')
        self.print_final(passed_cases, elapsed, percent_passed)
        
    def print_pre_info(self):
        print('Running tests...')
    
    def print_post_info(self): pass
        
    def print_cases(self, descr: str, cases: list) -> None:
        if cases:
            print(f'\nThe following tests {descr.upper()}:')
            for test in sorted(cases): print(f'\t- {test}')
        else: print(f'\nNo test cases {descr}.')
        
    def print_final(self, passed_cases: list, elapsed: float, percent_passed: float) -> None:
        print(
            f'\nCompleted {self.n_tests} test cases in {round(elapsed, 2)} secs.\n'
            f'Score: {len(passed_cases)}/{self.n_tests} ({round(percent_passed, 2)}%)\n'
        )
        

class Timer:
    """This context manager allows timing blocks of code."""
    def __enter__(self):
        self._timer = time.time()
        return self

    def __exit__(self, *args):
        self.elapsed = time.time() - self._timer
        
        
class ConnError(Exception): pass


def threaded_map(fn: Callable, data: Iterable, max_workers: int = None) -> Iterator:
    with ThreadPoolExecutor(max_workers = max_workers) as executor:
        return executor.map(fn, data)


def retryable(
            f: Callable = None,
            *,
            max_tries: int = 1,
            wait_time: Callable = (lambda t: 0.1),
            err_msg: str = None,
            verbose: bool = True
        ) -> Callable:
    def decorator(g):
        @wraps(g)
        def wrapper(*args,**kwargs):
            err = None
            for try_i in range(max_tries + 1):
                try:
                    return g(*args, **kwargs)
                except Exception as e:
                    err = e
                    if verbose: warning(err_msg or f'exhausted retries when attempting to run "{f.__name__}"' + ' -- trying again')
                    time.sleep(wait_time(try_i))
            if verbose: warning(err_msg or f'exhausted retries when attempting to run "{f.__name__}"')
            raise err
        return wrapper

    if f:
        return decorator(f)
    else:
        return decorator
    
    
def warning(msg: str) -> None:
    """Prints warning."""
    print(f'WARNING: {msg}')


def fatal_error(msg: str) -> None:
    """Prints error and exits program."""
    print(f'ERROR: {msg}')
    print('Exiting...')
    sys.exit()


def make_title(msg: str) -> str:
    """Returns basic title string."""
    return (
        f'+{(len(msg) + 2)*"="}+\n'
        f'| {msg} |\n'
        f'+{(len(msg) + 2)*"="}+'
    )