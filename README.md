# Diviner
Given some test cases, this program automatically queries the oracle and tests your compiler!

More spefically this program:
    1) Runs your test inputs thru the oracle & collects its response
        to give a "true output"; writes "<\test>.oracle" to test dir.
        
    2) Runs all your test inputs through your compiled compiler & collects
        outputs to give an "actual output"; writes <test>.actual to test dir.
        
    3) For each (<test>.oracle, <test>.actual) pair, runs diff to check if
        your comiler is producing correct output; provides score and details.       

## Formal Usage:
    `python3 diviner.py <\path to cshantyc> <\path to dir containing *.cshantyc test cases> <-f, optional>`
    `python3 diviner.py --help`

## Example usage:
    `python3 diviner cshantyc my_tests/`
    `python3 diviner cshantyc my_tests/ --lazy-query`
    `python3 diviner cshantyc my_tests/ -l`
    `python3 diviner --help`
    
    ...where my_tests/ might contain test1.cshanty, test2.cshanty, etc.
    
## Dependencies:
    - python3 (https://www.python.org/downloads/)
    - bs4 (pip3 install bs4)
    
    ...the rest should be standard.
    
## Notes:
    - For a given "test.cshanty", if this program already detects a "test.oracle" it will still requery the oracle for that test. Setting lazy-query to 1 in cmd line will instead skip it to avoid excess time and requests.