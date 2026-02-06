import unittest
import os
import shutil
from unittest.mock import patch
from testassist import TestAssist

class TestIntegration(unittest.TestCase):

    def setUp(self):
        """Clean up environment before each integration test."""
        if os.path.exists("tests"):
            shutil.rmtree("tests")
        self.tg = TestAssist(seed=1)

    def tearDown(self):
        """Clean up environment after each integration test."""
        if os.path.exists("tests"):
            shutil.rmtree("tests")

    @patch('builtins.input', return_value='y')
    def test_finalize_creates_files_and_folder(self, mock_input):
        """
        Integration test to check if finalize() properly creates 
        the directory and the expected number of files.
        """
        # We use a simple command like 'echo' or a dummy python call 
        # that we know will succeed on any system.
        dummy_args = {
            'testgen': 'test_script.py', # We'll create this on the fly
            'n': 10
        }
        
        # Create a temporary dummy generator script
        with open("test_script.py", "w") as f:
            f.write("import sys; print('test data')")

        try:
            self.tg.make_batch(3, dummy_args)
            self.tg.finalize(workers=1)

            # Check if directory exists
            self.assertTrue(os.path.exists("tests"))

            # Check if exactly 3 files were created
            files = os.listdir("tests")
            self.assertEqual(len(files), 3)

            # Check naming pattern (padding for 3 tests should be 1, e.g., test.1.in)
            self.assertIn("test.1.in", files)
            self.assertIn("test.3.in", files)
            
        finally:
            # Clean up the dummy script
            if os.path.exists("test_script.py"):
                os.remove("test_script.py")

    @patch('builtins.input', return_value='n')
    def test_finalize_abort_on_no_permission(self, mock_input):
        """Check if the program exits when user refuses to clear the directory."""
        os.makedirs("tests")
        with open("tests/old_test.in", "w") as f:
            f.write("old data")

        self.tg.make_test({'testgen': 'dummy'}, 0)
        
        # sys.exit(0) should be called
        with self.assertRaises(SystemExit) as cm:
            self.tg.finalize()
        
        self.assertEqual(cm.exception.code, 0)