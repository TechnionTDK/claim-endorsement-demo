import pandas as pd
import os
import argparse
import sys
def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0
if __name__ == '__main__':
     parser = argparse.ArgumentParser(description='Process some parameters for claim_endorse.')
     parser.add_argument('--pathname', type=str, required=True, help='database identifier')
     args = parser.parse_args()
     filepath=f'data/{args.pathname}/results/demo_test.csv'
     if not os.path.exists(filepath):
        sys.exit(0)
     os.remove(filepath)
