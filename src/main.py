import argparse
import logging

from data_extraction import github_data
from data_extraction.helper import create_df, normalize_df
from scoring_feature.score import WeightedAverage
from utils import CSV_PATH

parser = argparse.ArgumentParser(description='Suggest owners for the given repo directory')
parser.add_argument('--cloned_repo_path', type=str, help='path to the cloned repo')
parser.add_argument('--remote_repo_link', type=str, help='path to the remote repo')
parser.add_argument('--dir', type=str, help='directory path')
parser.add_argument('--number', type=int, default=3, help='number of top owners to suggest')

def main():
    args = parser.parse_args()
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='app.log', level=logging.INFO)

    # Collect Github data
    gd = github_data.GithubData(args.remote_repo_path, args.cloned_repo_local_path, args.dir)
    collected_data_dict = gd.gather_github_data()

    # create dataframe and normalize it
    logging.info("Creating dataframe...")
    normalized_github_data_df = normalize_df(create_df(collected_data_dict))

    # save the dataframe to csv
    normalized_github_data_df.to_csv(CSV_PATH, index=False)

    # scoring system
    top_contributors = WeightedAverage(normalized_github_data_df, args.number_of_owners).suggest_top_contributors()
    print(f"The top {args.number_of_owners} contributors of directory {args.dir} are (with contri %) : \n {top_contributors}")

    

if __name__ == "__main__":
    main()