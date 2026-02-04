from testassist import TestAssist, Choice, Range
import os

def main():
    tg = TestAssist(seed=42)

    tg.begin_subtask()
    tg.make_batch(6, {
        'testgen': 'testgens/python_gen.py',
        'n': Choice([5, 10]),
        'm': Choice([2, 6, 12])
    })

    tg.begin_subtask()
    tg.make_batch(5, {
        'testgen' : 'testgens/cpp_gen',
        'n': Range(5, 10),
        'm': Range(6, 8)
    })

    tg.preview()

    tg.finalize(workers=4)

if __name__ == "__main__":
    main()