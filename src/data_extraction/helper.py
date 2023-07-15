from dataclasses import dataclass
from typing import Dict
import pandas as pd


@dataclass
class UserInfo:
    authored_commits_count: int = 0
    commited_commits_count: int = 0
    author_is_committer_count: int = 0
    first_commit: int = 0
    oldest_commit_count: int = 0
    newest_commit_count: int = 0
    pr_files_touched_count: int = 0
    issue_assigned_count: int = 0
    todo_author_count: int = 0

@dataclass
class UserEmailData:
    user_email_data: Dict[str, UserInfo]

class CreateDataFrame():
    def __init__(self, class_object: UserEmailData):
        self.user_data = class_object.user_email_data

    def create_df(self) -> pd.DataFrame:
        df = pd.DataFrame({
            'email': [x for x in self.user_data.keys()],
            'authored_commits_count': [x.authored_commits_count for x in self.user_data.values()],
            'commited_commits_count': [x.commited_commits_count for x in self.user_data.values()],
            'author_is_committer_count': [x.author_is_committer_count for x in self.user_data.values()],
            'first_commit': [x.first_commit for x in self.user_data.values()],
            'oldest_commit_count': [x.oldest_commit_count for x in self.user_data.values()],
            'newest_commit_count': [x.newest_commit_count for x in self.user_data.values()],
            'pr_files_touched_count': [x.pr_files_touched_count for x in self.user_data.values()],
            'issue_assigned_count': [x.issue_assigned_count for x in self.user_data.values()],
            'todo_author_count': [x.todo_author_count for x in self.user_data.values()]
            })

        print(df.head())
        return df
