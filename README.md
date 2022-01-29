# The Diviner
A complement to The Oracle for automatically testing and validating any compiler satisfying the 665 standard interface. Given some test cases, this program automatically queries The Oracle with test cases to ascertain the integrity of your compiler!

More spefically this program:
* Runs your *\*.lang* test inputs through the oracle & collects its response to give a "true output"; writes *\*.truth* to test dir.
* Runs all your test inputs through your compiled compiler & collects outputs to give an "actual output"; writes *\*.actual* to test dir.
* For each *(\*.truth, \*.actual)* pair, essentially runs a more nuanced version of diff to check if your compiler is producing correct output; provides scores and details.

## Formal Usage:
* `Diviner [-h] [--no_file_gen] {D1, D2, D3, D4, D5, D6, D7, D8} language_ext compiler_path test_dir_path`

## Example usage:
* `python3 Diviner D5 cshanty p5_files/cshantyc p5_files/tests`
* `python3 Diviner D3 cmm p3_files/cmmc p3_files/tests --no_file_gen`
* `python3 Diviner D6 -h`
    
...where `tests/` might contain `test1.lang`, `test2.lang`, etc. `--no_file_gen` flag disables the Diviner from saving *(\*.truth, \*.actual)* as files.
    
## Dependencies:
* Python 3 (https://www.python.org/downloads/)
* several libraries, see below for installation
* ...the rest should be standard.

* You should run `make install` or `pip3 install -r requirements.txt` to grab Python dependencies
* While we are on the topic of make directives, `make clean` removes all compiled `*.pyc` files
    
    
## Notes:
* Results are cached by default by saving the *\*.truth* and *\*.actual* files in the test_dir. This has the added benefit of being able to see the differences and applying other tools like diff.
* Several diviner versions may be missing. However, feel free to fork, add new version `d[1-8]` in `core/versions.py`, and submit a PR. If you inherit from `core.diviner_base.DivinerBase` and take a look at the other versions, it shouldn't be too hard.
