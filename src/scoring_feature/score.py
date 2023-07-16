import heapq
from dataclasses import dataclass, fields

import pandas as pd


@dataclass
class Weights: 
    # manually set weights for each feature on scale of 1 to 5
    # 1 being least important and 5 being most important
    
    authored_commits_count: int = 3
    commited_commits_count: int = 1
    author_is_committer_count: int = 4
    first_commit: int = 5
    oldest_commit_count: int = 4
    newest_commit_count: int = 3
    pr_files_touched_count: int = 2
    issue_assigned_count: int = 3
    todo_author_count: int = 4


class WeightedAverage:
    def __init__(self, df: pd.DataFrame, number_of_contributors: int):
        self.df = df
        self.number_of_contributors = number_of_contributors
        self.top_contributors = [] 

    def suggest_top_contributors(self):
        for _, row in self.df.iterrows():
            contributor_score = 0
            for field in fields(Weights):
                contributor_score += getattr(Weights, field.name) * row[field.name]

            # Add the github user score to the heap
            if len(self.top_contributors) < self.number_of_contributors:
                heapq.heappush(self.top_contributors, (contributor_score, row['email']))
            else:
                heapq.heappushpop(self.top_contributors, (contributor_score, row['email']))

            top_n_contributors = heapq.nlargest(self.number_of_contributors, self.top_contributors)

        return [user_email for _, user_email in top_n_contributors]