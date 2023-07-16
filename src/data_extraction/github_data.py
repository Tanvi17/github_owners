import logging
import re
import time
from os import PathLike, path
from typing import Any, Union

import git
from data_extraction.helper import UserInfo
from github import Github

from . import github_auth as AUTH


class GithubData:
    def __init__(self, remote_repo: Union[str, PathLike], local_repo: Union[str, PathLike], dir_path: Union[str, PathLike]) -> None:
        self.remote_repo = remote_repo
        self.local_repo = local_repo
        self.dir_path = dir_path
        
        # remote repo object
        self.g = Github(auth=AUTH)
        repo_parts = self.remote_repo.split('/')[-2:]
        self.remote_repo = self.g.get_repo(path.join(repo_parts[0], repo_parts[1]))

        # local repo object
        self.repo = git.Repo(self.local_repo)
        self.commits = self.repo.iter_commits(paths=self.dir_path)
        
        self.u_data = {}


    def find_files(self, subdir):
        """
        Finds all files and subdirectories in a given directory
        """
        files, dirs = set(), set()
        contents = self.remote_repo.get_contents(subdir)

        for content in contents:
            if content.type == 'file' and content.path not in files:
                files.add(content.path)
                self.get_todo_comment_data(content.path)
            elif content.type == 'dir' and content.path not in dirs:
                dirs.add(content.path)
                subfiles, subdirs = self.find_files(content.path)
                files.update(subfiles)
                dirs.update(subdirs)

        return files, dirs

    def get_todo_comment_data(self, file_path) -> None:
        """
        Extracts author of the TODO comments in a file 
        """
        blame = self.repo.blame('HEAD', file=file_path)
        TODO_REGEX = r' TODO[^\n]*'
        for commit, lines in blame:
            for line in lines:
                try:
                    comments = re.findall(TODO_REGEX, line)
                except:
                    comments = None
                if comments and commit.author.email:
                    if commit.author.email not in self.u_data:
                        self.u_data[commit.author.email] = UserInfo(email=commit.author.email)
                    self.u_data[commit.author.email].todo_author_count += len(comments)

    def get_pr_data(self) -> None:
        """
        Gets the author from all the resolved PRs relevant to the directory
        """
        pulls = self.remote_repo.get_pulls(state='closed')

        # putting limit of 300 PRs to avoid rate limit
        for pr in pulls[:300]:
            for commit, file_ in zip(pr.get_commits(), pr.get_files()):
                if commit.author and commit.author.email and file_.filename.startswith(self.dir_path):
                    if commit.author.email not in self.u_data:
                        self.u_data[commit.author.email] = UserInfo(email=commit.author.email)
                    self.u_data[commit.author.email].pr_files_touched_count += 1

    def get_issue_data(self) -> None:
        """
        Finds the assignee of all the issues relevant to the directory
        """
        issues = self.remote_repo.get_issues(state='closed', assignee='*')

        # putting limit of 500 issues to avoid rate limit
        for issue in issues[:500]: 
            if issue.body:
                # get dump of files in issue
                mentioned_files = re.findall(r'[\w./-]+\.[\w]+', issue.body) 

                if any(f.startswith(self.dir_path) for f in mentioned_files) and issue.assignee:
                    # get the email of the user assigned to the issue
                    assigned_user_email = self.g.get_user(issue.assignee.login).email

                    if assigned_user_email not in self.u_data:
                        self.u_data[assigned_user_email] = UserInfo(email=assigned_user_email)
                    self.u_data[assigned_user_email].issue_assigned_count += 1

    def get_fresh_and_old_commit(self) -> Union[int, int, Any]:
        """
        Get the first and last commit in the repo
        """
        self.commits = list(self.commits)
        fresh, old = self.commits[0].authored_datetime.year, self.commits[-1].authored_datetime.year
        first = self.commits[-1].authored_datetime

        if fresh == old or fresh - old < 3:
            return fresh, old, first
        else:
            return fresh - 2, old + 2, first


    def get_authors_and_committers_data(self) -> None:
        """
        self.author_is_commiter_counter: Dict[str, int] = {email: count}
        """

        fresh_commit_threshold_year, old_commit_threshold_year, first_commit_datetime = self.get_fresh_and_old_commit()
        
        for commit in self.commits:
            author_email = commit.author.email
            committer_email = commit.committer.email

            # add author email to dict and increment authored commits count
            if author_email not in self.u_data:
                self.u_data[author_email] = UserInfo(email=author_email)
            self.u_data[author_email].authored_commits_count += 1

            # add commiter email to dict and increment commiter commits count
            if committer_email not in self.u_data:
                self.u_data[committer_email] = UserInfo(email=committer_email)
            self.u_data[committer_email].commited_commits_count += 1

            # increment authored and commited commits count
            if author_email == committer_email:
                self.u_data[author_email].author_is_committer_count += 1

            # fresh or old commit contributor
            if commit.authored_datetime.year >= fresh_commit_threshold_year:
                self.u_data[author_email].newest_commit_count += 1
            if commit.authored_datetime.year <= old_commit_threshold_year:
                self.u_data[author_email].oldest_commit_count += 1
            
            # first year and month commit contributor
            if commit.authored_datetime.year == first_commit_datetime.year and commit.authored_datetime.month == first_commit_datetime.month:
                self.u_data[author_email].first_commit += 1

    def gather_github_data(self):
        total_time_start = time.time()

        # author and committer data
        logging.info('Adding commit author and committer data..')
        self.get_authors_and_committers_data()

        # data from Github issues
        logging.info('Adding data from raised issues..')
        self.get_issue_data()

        # data from Github pull requests
        logging.info('Adding data from pull requests..')
        self.get_pr_data()

        # data from todo comments
        logging.info('Adding todo contributors...')
        _, _ = self.find_files(self.dir_path)

        logging.info('Total time taken to collect github data: ', time.time() - total_time_start)

        return self.u_data

