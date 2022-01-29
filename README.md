# The Diviner
A complement to The Oracle for automatically testing and validating any compiler satisfying the 665 standard interface. Given some test cases, this program automatically queries The Oracle with test cases to ascertain the integrity of your compiler!

More spefically this program:
* Runs your *\*.lang* test inputs thru the oracle & collects its response to give a "true output"; writes *\*.truth* to test dir.
* Runs all your test inputs through your compiled compiler & collects outputs to give an "actual output"; writes *\*.actual* to test dir.
* For each *(\*.truth, \*.actual)* pair, essentially runs a more nuanced version of diff to check if your compiler is producing correct output; provides score and details.       

## Formal Usage:
* `python3 diviner.py <diviner version> <path to langc> <path to dir containing *.langc test cases>`
* `python3 diviner.py --help`
* `python3 diviner.py <diviner version> -h`

## Example usage:
* `python3 diviner d5 langc my_tests/`
* `python3 diviner d6 --help`
* `python3 diviner d6 -h`
    
...where `my_tests/` might contain test1.lang, test2.lang, etc.
    
## Dependencies:
* Python 3 (https://www.python.org/downloads/)
* several libraries, see below for installation
* ...the rest should be standard.

* You should run `make install` or `pip3 install -r requirements.txt` to grab Python dependencies
* While we are on the topic of make directives, `make clean` removes all compiled `*.pyc` files
    
    
## Notes:
* Results are cached by saving the *\*.truth* and *\*.actual* files in the test_dir. This has the added benefit of being able to see the differences and applying other tools like diff.
* Some diviner versions may be missing. However, feel free to fork, add new version `d[1-8]` in `core/versions.py`, and submit a PR. If you inherit from `core.diviner_base.DivinerBase` and take a look at the other versions, it shouldn't be too hard.
