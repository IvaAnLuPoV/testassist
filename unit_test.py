import unittest
import os
from testassist import TestAssist, Choice, Range, Task

class TestTestGenerator(unittest.TestCase):

    def setUp(self):
        """Initializes a fresh generator before each test."""
        self.tg = TestAssist(seed=42)

    def test_choice_logic(self):
        """Check if Choice cycles through values correctly."""
        choice = Choice([10, 20])
        val0 = self.tg.process_arg(choice, 0)
        val1 = self.tg.process_arg(choice, 1)
        val2 = self.tg.process_arg(choice, 2)
        
        self.assertEqual(val0, "10")
        self.assertEqual(val1, "20")
        self.assertEqual(val2, "10") # Should cycle back

    def test_range_logic(self):
        """Check if Range produces values within bounds."""
        rng = Range(5, 10)
        for _ in range(100):
            val = int(self.tg.process_arg(rng, 0))
            self.assertTrue(5 <= val <= 10)

    def test_lcm_validation(self):
        """Ensure make_batch raises ValueError if count is not a multiple of LCM."""
        args = {
            'testgen': 'gen.py',
            'param': Choice([1, 2, 3]) # Length 3
        }
        # 10 is not a multiple of 3, should fail
        with self.assertRaises(ValueError):
            self.tg.make_batch(10, args)
        
        # 9 is a multiple of 3, should succeed
        self.tg.make_batch(9, args)
        self.assertEqual(len(self.tg.task_container), 9)

    def test_task_container_storage(self):
        """Check if tasks are correctly stored in the RAM container."""
        self.tg.begin_subtask()
        self.tg.make_test({'testgen': 'gen.py', 'n': 10})
        
        self.assertEqual(len(self.tg.task_container), 1)
        task = self.tg.task_container[0]
        self.assertIsInstance(task, Task)
        self.assertEqual(task.gen_file, 'gen.py')
        self.assertIn('--n=10', task.cmd_args)

    def test_subtask_boundaries(self):
        """Ensure subtask indexing is correct."""
        self.tg.begin_subtask()
        self.tg.make_test({'testgen': 'g1'}, 0)
        self.tg.begin_subtask()
        self.tg.make_test({'testgen': 'g2'}, 0)
        
        self.assertEqual(self.tg.task_container[0].subtask_index, 0)
        self.assertEqual(self.tg.task_container[1].subtask_index, 1)

if __name__ == '__main__':
    unittest.main()