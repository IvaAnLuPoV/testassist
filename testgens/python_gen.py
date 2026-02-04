import argparse
import random
import sys

def main():
    parser = argparse.ArgumentParser(description="Generate a table of single-digit numbers.")
    
    parser.add_argument("--n", type=int, default=3, help="Number of rows")
    parser.add_argument("--m", type=int, default=3, help="Number of columns")
    
    parser.add_argument("test_id", type=int, help="ID of the current test")

    args = parser.parse_args()

    random.seed(args.test_id)

    print(f"{args.n} {args.m}")

    for _ in range(args.n):
        row = [random.randint(0, 9) for _ in range(args.m)]
        print(*(row))

if __name__ == "__main__":
    main()