# The Diviner
A complement to The Oracle for the in-house Cshanty compiler. Given some test cases, this program automatically queries the oracle with test cases to ascertain the integrity of your compiler!

More spefically this program:
* Runs your *\*.cshanty* test inputs thru the oracle & collects its response to give a "true output"; writes *\*.truth* to test dir.
* Runs all your test inputs through your compiled compiler & collects outputs to give an "actual output"; writes *\*.actual* to test dir.
* For each *(\*.truth, \*.actual)* pair, essentially runs a more nuanced version of diff to check if your compiler is producing correct output; provides score and details.       

## Formal Usage:
* `python3 diviner.py <diviner version> <path to cshantyc> <path to dir containing *.cshantyc test cases>`
* `python3 diviner.py --help`
* `python3 diviner.py d5 -h`

## Example usage:
* `python3 diviner d5 cshantyc my_tests/`
* `python3 diviner d6 --help`
* `python3 diviner d6 -h`
    
...where `my_tests/` might contain test1.cshanty, test2.cshanty, etc.
    
## Dependencies:
* python3 (https://www.python.org/downloads/)
* bs4 `pip3 install bs4`
* tqdm `pip3 install tqdm`
* ...the rest should be standard.

* You can also (alternatively) run `make install` or `pip3 install -r requirements.txt` for convenience
* While we are on the topic of make directives, `make clean` removes all compiled `*.pyc` files
    
    
## Notes:
* Results are cached by saving the *\*.truth* and *\*.actual* files in the test_dir. This has the added benefit of being able to see the differences and applying other tools like diff.
* Currently, only type analysis version for P5 is developed (diviner version = d5). However, feel free to fork and add new version `d[1-8]` in `versions/`. If you inherit from `core/diviner.py/DivinerBase` it should be very trivial to do other versions. 
