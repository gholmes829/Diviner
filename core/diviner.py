"""
Contains base class for The Diviner.
"""

__author__ = 'Grant Holmes'
__email__ = 'g.holmes429@gmail.com'
__created__ = '10/19/2021'
__modified__ = '10/21/2021'

import os.path as osp
import requests
import typing

from bs4 import BeautifulSoup

from core import utils


# constants and settings
ORACLE_URL_BASE = 'https://compilers.cool/oracles/o{version}/'
LANGUAGE = 'cshanty'
MULTI_THREADED = True


class DivinerBase(utils.TestManager):
    def __init__(self,
                oracle_version: int,
                compiler_path: str,
                test_dir_path: str,
                force_query: bool = False,
            ) -> None:
        super().__init__(test_dir_path, LANGUAGE)
        self.oracle_version = oracle_version
        self.oracle_url = ORACLE_URL_BASE.format(version=oracle_version)
        self.compiler_path = compiler_path
        self.force_query = force_query
        self.requests_made = 0
    
    def get_true_output(self, test_i: int, test_name: str, test_path: str) -> str:
        if not osp.isfile(test_path) or self.force_query:
            self.requests_made += 1
            return self.scrape_oracle(open(test_path, 'rb'))
    
    @utils.retryable(err_msg='could not connect to oracle', verbose = False)
    def scrape_oracle(self, test_file: typing.BinaryIO) -> str:
        """Queries the oracle with a given test case and returns output."""
        res = requests.post(self.oracle_url, files={'input': test_file})
        if res.status_code == 200:
            return BeautifulSoup(res.text, 'html.parser').find('pre').text
        else:
            raise utils.ConnError()
        
    def print_pre_info(self):
        print(f'Consulting with The Oracle at "{self.oracle_url}" and evaluating on local compiler...')
        
    def print_post_info(self):
        print(f'\nSkipping {self.n_tests - self.requests_made} previously evaluated queries.')

    def title(self) -> str:
        return utils.make_title(f'THE DIVINER (P{self.oracle_version})')