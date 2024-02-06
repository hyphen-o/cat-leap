import pandas as pd
import sys

sys.path.append("../")


class MileStoneEvaluater:
    def set_data(self, data: pd.DataFrame):
        self.__personal_data = data
        self.__milestones = {
            "BASIC_TO_DEVELOPING": {
                "CLASS": 0,
                "USER_NAME": "",
                "LENGTH": 0,
                "MILES": [],
            },
            "DEVELOPING_TO_MASTER": {
                "CLASS": 0,
                "USER_NAME": "",
                "LENGTH": 0,
                "MILES": [],
            },
        }

    def get_milestone(self, is_all=False):
        user_level = self.__get_user_level_init()

        if len(self.__personal_data):
            self.__milestones["BASIC_TO_DEVELOPING"]["USER_NAME"] = str(
                self.__personal_data.iloc[0]["UserName"]
            )
            self.__milestones["DEVELOPING_TO_MASTER"]["USER_NAME"] = str(
                self.__personal_data.iloc[0]["UserName"]
            )

        tmp_array = []
        index = 0
        for row in self.__personal_data.itertuples():
            CURRENT_LEVEL = self.__categorize_level(row.CTScore)

            # 現在の習熟度がMASTERなら処理終了
            if user_level == "MASTER":
                break

            tmp_array.append(
                {
                    "Before": {
                        "Abst": row.Abst,
                        "Para": row.Para,
                        "Logi": row.Logi,
                        "Sync": row.Sync,
                        "Flow": row.Flow,
                        "User": row.User,
                        "Data": row.Data,
                        "CTScore": row.CTScore,
                        "Feature": [
                            row.Abst,
                            row.Para,
                            row.Logi,
                            row.Sync,
                            row.Flow,
                            row.User,
                            row.Data,
                        ],
                    },
                    "IsRemix": row.IsRemix,
                    "Level": CURRENT_LEVEL
                    # "Num": index
                }
            )
            index += 1

            # オリジナル作品で習熟度が向上したら記録
            if self.__is_grown(user_level, CURRENT_LEVEL) and row.IsRemix == 0:
                if user_level == "BASIC":
                    self.__milestones["BASIC_TO_DEVELOPING"]["MILES"] = tmp_array.copy()
                    self.__milestones["BASIC_TO_DEVELOPING"]["CLASS"] = 1
                    self.__milestones["BASIC_TO_DEVELOPING"]["LENGTH"] = len(tmp_array)
                    index = 0
                elif user_level == "DEVELOPING":
                    self.__milestones["DEVELOPING_TO_MASTER"][
                        "MILES"
                    ] = tmp_array.copy()
                    self.__milestones["DEVELOPING_TO_MASTER"]["CLASS"] = 1
                    self.__milestones["DEVELOPING_TO_MASTER"]["LENGTH"] = len(tmp_array)
                tmp_array.clear()
                user_level = CURRENT_LEVEL


        if is_all and self.__milestones["BASIC_TO_DEVELOPING"]["CLASS"] == 0:
            self.__milestones["BASIC_TO_DEVELOPING"]["MILES"] = tmp_array.copy()
            self.__milestones["BASIC_TO_DEVELOPING"]["LENGTH"] = len(tmp_array)
        if is_all and self.__milestones["DEVELOPING_TO_MASTER"]["CLASS"] == 0:
            self.__milestones["DEVELOPING_TO_MASTER"]["MILES"] = tmp_array.copy()
            self.__milestones["DEVELOPING_TO_MASTER"]["LENGTH"] = len(tmp_array)

        return self.__milestones

    def __categorize_level(self, score: int):
        """CTスコアからCT習熟度を返す関数
        Args:
            score (int): カテゴリ分けしたいCTスコア
        Returns:
            str: 点数に沿ったCT習熟度の文字列を返す
        """

        if score >= 15:
            return "MASTER"
        elif score >= 8:
            return "DEVELOPING"
        elif score >= 0:
            return "BASIC"

    def __is_grown(self, user_level: str, current_level: str):
        """ユーザの習熟度が向上したかを返す関数

        Args:
            user_level (str): 現在のユーザの習熟度
            current_level (str): 最新の作品の習熟度

        Returns:
            boolean: ユーザの習熟度が向上したかどうかのフラグ
        """

        if (
            (user_level == "BASIC" and current_level == "DEVELOPING")
            or (user_level == "BASIC" and current_level == "MASTER")
            or (user_level == "DEVELOPING" and current_level == "MASTER")
        ):
            return True
        else:
            return False

    def __get_user_level_init(self):
        for row in self.__personal_data.itertuples():
            if row.IsRemix == 0:
                return self.__categorize_level(row.CTScore)
