### Introduction
testassist is designed to ease routine tasks involving test generation for competitive programming problems.
It relies on external test generators (Python scripts or C++ executables) for the actual structure of the problem tests.
It's usefulness is in quickly changing parameters and overall subtasks structure by delagating common functionality to the `testassist` module.

## Functionality
```
make_test()
```
`make_test()` creates a singular testcase with a chosen test generator and parameters chosen with `Range()` and `Choice()`
```
make_batch()
```
`make_batch()` creates multiple testcases following a similar structure -- it ensures all combination of the lists passed by `Choice()` are iterated.
```
begin_subtask() & finalize()
```
`begin_subtask()` signalizes the beginning of a new subtask in which all further defined testcases will be a part of, unless a new subtask is created.
`finalize()` initiates actual generation of the testcases and renames them such that an adequate ammount of zeroes are used for padding. 
