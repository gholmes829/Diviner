"""

"""

__author__ = 'Grant Holmes'
__email__ = 'g.holmes429@gmail.com'


import argparse

from core import utils, versions


def make_argparser():
	argparser = argparse.ArgumentParser(description='Consult the oracle and run automated tests with ease and swagger.')
	argparser.add_argument('diviner_version', choices = versions.versions(), help='select which diviner version to use')
	argparser.add_argument('language_ext', help='file extension for source language')
	argparser.add_argument('compiler_path', help='relative path to compiler executable')
	argparser.add_argument('test_dir_path', help='relative path to dir containing input tests')
	argparser.add_argument('--no_file_gen', action='store_true', help='disable generating new files with results')
	return argparser


def main():
	args = make_argparser().parse_args()
	version: str = args.diviner_version
	language_ext: str = args.language_ext
	if language_ext.startswith('.'): language_ext = language_ext[1:]
	compiler_path: str = args.compiler_path
	test_dir_path: str = args.test_dir_path
	write_to_file: bool = not args.no_file_gen

	with utils.Timer() as t:
		diviner = versions.make_diviner(version, language_ext, compiler_path, test_dir_path, write_to_file = write_to_file)
		print(diviner.title() + '\n')
		diviner.run_tests()
    
	print(f'Testing and analysis took {round(t.elapsed, 2)} secs to complete.\n')


if __name__ == '__main__':
	main()
