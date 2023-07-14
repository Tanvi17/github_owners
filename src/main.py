import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--cloned_repo_path', type=str, help='path to the cloned repo')
parser.add_argument('--dir', type=str, help='directory path')

def main():
    args = parser.parse_args()
    print(args.cloned_repo_path, args.dir)

if __name__ == "__main__":
    main()