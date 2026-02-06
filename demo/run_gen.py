from testassist import TestAssist, Choice, Range
import os

def main():
    ta = TestAssist(seed=42)

    ta.begin_subtask()
    ta.make_batch(6, {
        'testgen': 'demo/testgens/py_gen.py',
        'n': Choice([5, 10]),
        'm': Choice([2, 6, 12])
    })

    ta.begin_subtask()
    ta.make_batch(5, {
        'testgen' : 'demo/testgens/cpp_gen',
        'n': Range(5, 10),
        'm': Range(6, 8)
    })

    ta.preview()

    ta.finalize(workers=4)

if __name__ == "__main__":
    main()