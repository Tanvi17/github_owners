import argparse
from data_extraction import github_data
from data_extraction.helper import CreateDataFrame, UserEmailData
import os
from utils import CSV_PATH

parser = argparse.ArgumentParser(description='Suggest owners for the given repo directory')
parser.add_argument('--cloned_repo_local_path', type=str, help='path to the cloned repo')
parser.add_argument('--remote_repo_path', type=str, help='path to the remote repo')
parser.add_argument('--dir', type=str, help='directory path')

def main():
    args = parser.parse_args()

    # Collect Github data and create dataframe
    gd = github_data.GithubData(args.remote_repo_path, args.cloned_repo_local_path, args.dir)
    collected_data_obj = gd.gather_github_data()
    CreateDataFrame(collected_data_obj).create_df().to_csv(CSV_PATH, index=False)

    # scoring system

    

if __name__ == "__main__":
    main()