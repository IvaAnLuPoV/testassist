import sys
import math
import os
import shutil
import random as rnd
import subprocess
import multiprocessing
from typing import Any, Dict, List, Union, Callable, Optional
from dataclasses import dataclass

@dataclass
class Choice:
    """
    Explicitly pick values in a cyclic manner from a list.
    """
    values: list
    def __len__(self):
        return len(self.values)

@dataclass
class Range:
    """
    Explicitly generate a random number in [low, high].
    """
    low: Union[int, float]
    high: Union[int, float]
    is_float: bool = False

@dataclass
class Task:
    """
    A structure representing a single test case unit in the RAM container.
    """
    test_id: int
    cmd_args: List[str]
    gen_file: str
    subtask_index: int
    test_name: Optional[str] = None
    final_cmd: Optional[List[str]] = None

def _worker_task(task: Task):
    """
    Static worker function for parallel execution.
    Writes output to the 'tests/' directory.
    """
    try:
        with open(f"tests/{task.test_name}", "w") as f:
            subprocess.run(task.final_cmd, stdout=f, stderr=sys.stdout, check=True)
        return f"Generated {task.test_name}: {' '.join(task.final_cmd)}"
    except subprocess.CalledProcessError as e:
        return f"ERROR: Generator failed on {task.test_name} (Exit code: {e.returncode})"
    except Exception as e:
        return f"ERROR: Unexpected error on {task.test_name}: {e}"

class TestAssist:
    """
    Core engine for test generation. Manages a task container, 
    cleans target directory, and executes tasks in parallel.
    """

    def __init__(self, seed: int = 0):
        self.current_test = 0
        self.subtasks_boundaries = []
        self.task_container: List[Task] = []
        rnd.seed(seed)

    @staticmethod
    def _get_lcm(lengths: List[int]) -> int:
        if not lengths: return 1
        res = lengths[0]
        for l in lengths[1:]:
            res = (res * l) // math.gcd(res, l)
        return res

    def process_arg(self, arg: Any, idx: int) -> str:
        if isinstance(arg, Choice):
            return str(arg.values[idx % len(arg.values)])
        if isinstance(arg, Range):
            if arg.is_float or isinstance(arg.low, float) or isinstance(arg.high, float):
                return f"{rnd.uniform(arg.low, arg.high):.6f}"
            else:
                return str(rnd.randrange(int(arg.low), int(arg.high) + 1))
        if callable(arg):
            return str(arg(idx))
        if isinstance(arg, float):
            return f"{arg:.6f}"
        return str(arg)

    def make_test(self, args: Dict[str, Any], idx: int = 0):
        self.current_test += 1
        gen_file = args['testgen']
        cmd_args = [f"--{k}={self.process_arg(v, idx)}" for k, v in args.items() if k != 'testgen']
        sub_idx = len(self.subtasks_boundaries) - 1
        self.task_container.append(Task(
            test_id=self.current_test, 
            cmd_args=cmd_args, 
            gen_file=gen_file, 
            subtask_index=sub_idx
        ))

    def make_batch(self, count: int, args: Dict[str, Any]):
        lengths = [len(v) for v in args.values() if isinstance(v, Choice)]
        required_lcm = self._get_lcm(lengths)
        if count % required_lcm != 0:
            raise ValueError(f"Batch size {count} must be multiple of LCM ({required_lcm})")
        for i in range(count):
            self.make_test(args, i)

    def begin_subtask(self):
        self.subtasks_boundaries.append(self.current_test + 1)

    def _prepare_directory(self):
        """
        Handles the creation and cleaning of the 'tests/' directory.
        Asking for user permission if the directory is not empty.
        """
        dir_name = "tests"
        if os.path.exists(dir_name):
            if os.listdir(dir_name):
                # Directory exists and is not empty
                choice = input(f"Directory '{dir_name}' is not empty. Clear it? [y/N]: ").lower()
                if choice == 'y':
                    shutil.rmtree(dir_name)
                    os.makedirs(dir_name)
                else:
                    print("Aborting to prevent overwriting existing data.")
                    sys.exit(0)
        else:
            os.makedirs(dir_name)

    def finalize(self, workers: Optional[int] = None):
        """
        Pads names, prepares directory, and executes tasks.
        """
        if not self.task_container:
            print("nothing to execute")
            return

        # Prepare naming and directory
        total_tests = len(self.task_container)
        padding = len(str(total_tests))
        self._prepare_directory()
        
        for task in self.task_container:
            task.test_name = f"test.{str(task.test_id).zfill(padding)}.in"
            interpreter = [sys.executable, task.gen_file] if task.gen_file.endswith('.py') else [f"./{task.gen_file}"]
            task.final_cmd = interpreter + task.cmd_args + [str(task.test_id)]

        print(f"start {total_tests} tests generation...")
        
        with multiprocessing.Pool(processes=workers) as pool:
            results = pool.map(_worker_task, self.task_container)

        for result in results:
            print(result)
            if result.startswith("ERROR"): sys.exit(1)

        self.subtasks_boundaries.append(self.current_test + 1)
        ranges = []
        for i in range(len(self.subtasks_boundaries) - 1):
            s, e = self.subtasks_boundaries[i], self.subtasks_boundaries[i+1] - 1
            if s <= e: ranges.append(f"{s}-{e}")
        
        print(f"\ndone; subtasks are: {','.join(ranges)}")
        
    def preview(self):
        """
        Prints the current state of the task container for debugging.
        Shows how tests are organized before final padding and execution.
        """
        if not self.task_container:
            print("\n[!] empty task container")
            return

        current_subtask = -1
        for task in self.task_container:
            if task.subtask_index != current_subtask:
                current_subtask = task.subtask_index
                print(f"subtask {current_subtask + 1}\n")
            
            args_str = " ".join(task.cmd_args)
            print(f"id: {task.test_id} | gen: {task.gen_file} | flags: {args_str}")