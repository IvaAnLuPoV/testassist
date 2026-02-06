import argparse
import random

parser = argparse.ArgumentParser(description="Python test generator")

parser.add_argument("--n", type=int, help="Rows in the table")
parser.add_argument("--m", type=int, help="Columns in the table")
parser.add_argument("seed", type=int, help="Seed for the randomization")

args = parser.parse_args()

n = args.n
m = args.m

print(f"{n} {m}")
print("\n".join(
        [" ".join(
            str(random.randint(0, 9)) 
                for _ in range(0, m))
            for _ in range(0, n)]
        ))