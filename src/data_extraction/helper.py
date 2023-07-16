from dataclasses import dataclass

import pandas as pd
from sklearn.preprocessing import MinMaxScaler


@dataclass
class UserInfo:
    email: str
    authored_commits_count: int = 0
    commited_commits_count: int = 0
    author_is_committer_count: int = 0
    first_commit: int = 0
    oldest_commit_count: int = 0
    newest_commit_count: int = 0
    pr_files_touched_count: int = 0
    issue_assigned_count: int = 0
    todo_author_count: int = 0


def create_df(user_data) -> pd.DataFrame:
    return pd.DataFrame([r.__dict__ for r in user_data.values()])

def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    # normalizing or standardizing the data
    scaling_data = df.drop(['email'], axis=1)
    scaler = MinMaxScaler().fit(scaling_data)
    scaled_data = scaler.transform(scaling_data)

    df_shaped = df.copy()
    df_shaped[df_shaped.columns[1:]] = scaled_data
    return df_shaped