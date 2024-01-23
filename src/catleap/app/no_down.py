import sys
import pandas as pd
import os
from tqdm import tqdm

sys.path.append("../")

from constants import path


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


def __get_user_level_init(data):
    for row in data.itertuples():
        if row.IsRemix == 0:
            return __categorize_level(row.CTScore)


for file_name in tqdm(os.listdir(path.CT_CSV_SPLITTED)):
    personal_data = pd.read_csv(path.CT_CSV_SPLITTED + file_name)
    user_level = __get_user_level_init(personal_data)
    tmp_array = []
    for row in personal_data.itertuples():
        # オリジナル作品で習熟度が向上したら記録
        if self.__is_grown(user_level, CURRENT_LEVEL) and row.IsRemix == 0:
            if user_level == "BASIC":
                self.__milestones["BASIC_TO_DEVELOPING"] = tmp_array.copy()
            elif user_level == "DEVELOPING":
                self.__milestones["DEVELOPING_TO_MASTER"] = tmp_array.copy()
            tmp_array.clear()
            user_level = CURRENT_LEVEL
