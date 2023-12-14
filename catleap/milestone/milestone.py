import pandas as pd
import sys

sys.path.append("../")
from utils import ToCsv


class MileStoneEvaluater:
    def set_data(self, data: pd.DataFrame):
        self.__personal_data = data
        self.__milestone = []
        self.__mile_dir = {
            "Before": {
                "Abst": 0,
                "Para": 0,
                "Logi": 0,
                "Sync": 0,
                "Flow": 0,
                "User": 0,
                "Data": 0,
                "CTScore": 0,
            },
            "Reach": 0,
            "Distance": 0,
        }

    def get_milestone(self):
        user_score = -1
        before_index = 0
        for row in self.__personal_data.itertuples():
            if row.CTScore <= user_score or row.IsRemix == 1:
                continue

            self.__mile_dir["Reach"] = row.CTScore
            self.__mile_dir["Distance"] = row.Index - before_index
            new_mile_dir = self.__mile_dir.copy()

            self.__milestone.append(new_mile_dir)

            self.__mile_dir["Before"] = {
                "Abst": row.Abst,
                "Para": row.Para,
                "Logi": row.Logi,
                "Sync": row.Sync,
                "Flow": row.Flow,
                "User": row.User,
                "Data": row.Data,
                "CTScore": row.CTScore,
            }

            before_index = row.Index
            user_score = row.CTScore

        if self.__milestone:
            self.__milestone.pop(0)
        return self.__milestone

    def __categorize_level(score):
        if score < 8 and score >= 0:
            return "BASIC"
        elif score < 15 and score >= 8:
            return "DEVELOPING"
        elif score >= 15:
            return "MASTER"
