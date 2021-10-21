# The Diviner
A complement to The Oracle for compilers class. Given some test cases, this program automatically queries the oracle and tests your compiler!

More spefically this program:
* Runs your *\*.cshanty* test inputs thru the oracle & collects its response to give a "true output"; writes *\*.truth* to test dir.
* Runs all your test inputs through your compiled compiler & collects outputs to give an "actual output"; writes *\*.actual* to test dir.
* For each *(\*.truth, \*.actual)* pair, essentially runs a more nuanced version of diff to check if your comiler is producing correct output; provides score and details.       

## Formal Usage:
* `python3 diviner.py <path to cshantyc> <path to dir containing *.cshantyc test cases> <-l, optional>`
* `python3 diviner.py --help`

## Example usage:
* `python3 diviner cshantyc my_tests/`
* `python3 diviner cshantyc my_tests/ --lazy-query`
* `python3 diviner cshantyc my_tests/ -l`
* `python3 diviner --help`
    
...where `my_tests/` might contain test1.cshanty, test2.cshanty, etc.
    
## Dependencies:
* python3 (https://www.python.org/downloads/)
* bs4 `pip3 install bs4`
* tqdm `pip3 install tqdm`
* ...the rest should be standard.

* You can also run `make install` or `pip3 install -r requirements.txt` for convenience
* While we are on the topic of make directives, `make clean` removes all compiled `*.pyc` files
    
    
## Notes:
* For a given *.cshanty, if this program already detects a *.truth it will still requery the oracle for that test. Setting `--lazy-query=1` in cmd line args will instead skip it to avoid excess time and requests.
* Currently, only type analysis version for P5 is developed. However, feel free to fork and add new version `d[1-8]` in `versions/`. If you inherit from `core/diviner.py/DivinerBase` it should be very trivial to do other versions. 
