"""
Contains useful utility based class/ fns.
"""

__author__ = 'Grant Holmes'
__email__ = 'g.holmes429@gmail.com'


import sys
from typing import Callable, Iterable
import time
import subprocess
from functools import wraps
        

class Timer:
    """This context manager allows timing blocks of code."""
    def __enter__(self):
        self.start = time.time()
        self.finish = None
        return self

    @property
    def elapsed(self):
        return self.finish or time.time() - self.start

    def __exit__(self, *_):
        self.finish = time.time() - self.start


def execute_in_shell(cmd: str, cwd = None) -> str:
    try:
        return subprocess.run(
            cmd,
            cwd = cwd,
            shell=True,
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
        ).stdout.decode(encoding='utf-8')
    except Exception as err:
        fatal_error(f'shell command crashed with "{err}".')


def retryable(
            f: Callable = None,
            *,
            max_tries: int = 1,
            wait_time: Callable = (lambda _: 0.1),
            err_msg: str = None,
            verbose: bool = True
        ) -> Callable:
    def decorator(g):
        @wraps(g)
        def wrapper(*args,**kwargs):
            err = None
            for try_i in range(max_tries + 1):
                try: return g(*args, **kwargs)
                except Exception as err:
                    if verbose: warning(err_msg or f'exhausted retries when attempting to run {f}' + ' -- trying again')
                    time.sleep(wait_time(try_i))
            if verbose: warning(err_msg or f'exhausted retries when attempting to run {f}')
            raise err
        return wrapper

    return decorator(f) if f else decorator
    
    
def count(data: Iterable) -> dict:
    """Counts number of occurrences for each item in list."""
    return {el: list(data).count(el) for el in set(data)}
    
    
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