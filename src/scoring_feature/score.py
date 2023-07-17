import heapq
from dataclasses import dataclass, fields

import pandas as pd
from scipy.special import softmax

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
    issue_assigned_count: int = 2
    todo_author_count: int = 4


class WeightedAverage:
    def __init__(self, df: pd.DataFrame, number_of_contributors: int):
        self.df = df
        self.number_of_contributors = number_of_contributors
        self.contributor_score_dict = {}

    def apply_soft_max(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply softmax and return top n contributors
        """
        softmax_scores = softmax(df['score'])
        df['probs'] = softmax_scores
        df = df.sort_values(by='probs', ascending=False)

        return [(df.index[i], round((df['probs'][i])*100, 2)) for i in range(self.number_of_contributors)]

    def suggest_top_contributors(self):
        for _, row in self.df.iterrows():
            score = 0
            for field in fields(Weights):
                score += getattr(Weights, field.name) * row[field.name]

            self.contributor_score_dict[row['email']] = score

        suggested_owners_df = pd.DataFrame.from_dict(self.contributor_score_dict, orient='index', columns=['score'])

        return self.apply_soft_max(suggested_owners_df)