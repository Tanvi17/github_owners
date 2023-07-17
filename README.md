# Github Owners

### Introduction

Implementing "suggested owners" feature for Github. Given a git repository, for every directory in the repository we want to figure out which git user is the “owner”.

The owner suggestions are made based on:

- active contributions to the directory
- when user is both author and committer
- whether the user made a first commit
- frequency of recent and old commits
- authored TODO comments
- files modified (via Github API)
- issues assigned to user (via Github API)

### Feature scoring

The features of Github data are collected by either cloned repo or accessing info via Github API. As we do not have sufficient label data to conduct supervised learning, the features are manually assigned weights, purely based on intuitions. Once data is collected, the score is calculated in linear regression fashion where values are applied againest weights of corresponding features. Followed by applying Softmax that normalizes it into probability distribution.

In simple words, it applies the standard exponential function to each element of the input vector and normalizes these values by dividing by the sum of all these exponentials; this normalization ensures that the sum of the components of the output vector is 1 [[wiki]](https://en.wikipedia.org/wiki/Softmax_function)

### Pre-requisites

- Generate a github authentication token and save it in .env file at root.
- Clone the public repository you wish to work with
- Install relevant packages by running `pip install -r requirements.txt`

### Sample input

- Four input arguments: path to cloned local, remote repo address, directory, number of top owners (default=3)

`python src/main.py --cloned_repo_path='path/to/local/cloned/repo' --remote_repo_link='https://github.com/golang/go' --dir='src/crypto' --number=3`
