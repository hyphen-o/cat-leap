from typing import NamedTuple
import numpy as np
import sys
from tqdm import tqdm
from collections import Counter

sys.path.append("../")
from constants import skill, path
from graph import draw_boxplot, draw_bar


class Length(NamedTuple):
    array: list
    array2: list
    mean: float
    mean2: float
    median: float
    median2: float


class BoxPlot(NamedTuple):
    nested_list: list
    xlabel: str
    ylabel: str
    title: str
    file_name: str


class Bar(NamedTuple):
    x: list
    y: list
    xlabel: str
    ylabel: str
    title: str
    file_name: str


class MileStastics:
    def __init__(self):
        self.__MILES_DATA = []
        self.__MILES_SECOND_DATA = []

    def set_data(self, miles_data: list):
        self.__MILES_DATA = miles_data

    def set_second_data(self, miles_data: list):
        self.__MILES_SECOND_DATA = miles_data

    def get_length(self):
        list_len = []
        list_len2 = []
        mean2 = 0
        median2 = 0

        for USER_MILES in self.__MILES_DATA:
            list_len.append(len(USER_MILES) - 1)
        if self.__MILES_SECOND_DATA:
            for USER_MILES in self.__MILES_SECOND_DATA:
                list_len2.append(len(USER_MILES) - 1)
            mean2 = np.mean(list_len2)
            median2 = np.median(list_len2)
        mean = np.mean(list_len)
        median = np.median(list_len)

        return Length(list_len, list_len2, mean, mean2, median, median2)

    def get_duplication(self):
        list_duplication = []
        for USER_MILES in tqdm(self.__MILES_DATA):
            for index, MILE in enumerate(USER_MILES["MILES"]):
                if index == len(USER_MILES["MILES"]) - 1:
                    break
                # if not self.__is_grow_up(
                #     MILE["Before"]["Feature"],
                #     USER_MILES[index + 1]["Before"]["Feature"],
                # ):
                # break
                # if MILE["IsRemix"] or USER_MILES[index + 1]["IsRemix"]:
                #     break

                edge = {
                    "Edge": {
                        "StartP": {
                            **MILE["Before"],
                            "IsRemix": MILE["IsRemix"],
                            "Level": MILE["Level"],
                            # "Num": MILE["Num"]
                        },
                        "EndP": {
                            **USER_MILES["MILES"][index + 1]["Before"],
                            "IsRemix": USER_MILES["MILES"][index + 1]["IsRemix"],
                            "Level": USER_MILES["MILES"][index + 1]["Level"],
                            # "Num": USER_MILES["MILES"][index + 1]["Num"]
                        }
                        if index != len(USER_MILES["MILES"]) - 2 or not USER_MILES["CLASS"]
                        else "NEXT_LEVEL",
                    }
                }

                dupli_index = self.__find_duplication(list_duplication, edge)

                if not dupli_index == -1:
                    list_duplication[dupli_index]["Count"] += 1
                else:
                    list_duplication.append(
                        {
                            "Count": 1,
                            "Euclid": self.__calculate_euclid(
                                edge["Edge"]["StartP"], edge["Edge"]["EndP"]
                            )
                            if not self.__is_next_level(edge["Edge"]["EndP"])
                            else None,
                            **edge,
                        }
                    )
        return list_duplication

    def get_all_duplication(self, duplications):
        dict = self.__MILES_DATA.copy()
        for user_num, USER_MILES in enumerate(tqdm(self.__MILES_DATA)):
            for index, MILE in enumerate(USER_MILES["MILES"]):
                if index == len(USER_MILES["MILES"]) - 1:
                    break
                dict[user_num]["COUNT"] = 0

                for DUPLICATION in duplications:
                    if (
                        MILE["Before"]["Feature"]
                        == DUPLICATION["Edge"]["StartP"]["Feature"]
                    ):
                        if index == len(USER_MILES["MILES"]) - 2:
                            if DUPLICATION["Edge"]["EndP"] == "NEXT_LEVEL":
                                dict[user_num]["COUNT"] += DUPLICATION["Count"]
                        else:
                            if DUPLICATION["Edge"]["EndP"] == "NEXT_LEVEL":
                                continue
                            if (
                                USER_MILES["MILES"][index + 1]["Before"]["Feature"]
                                == DUPLICATION["Edge"]["EndP"]["Feature"]
                            ):
                                dict[user_num]["COUNT"] += DUPLICATION["Count"]

                dict[user_num]["COUNT"] = dict[user_num]["COUNT"] / (
                    len(USER_MILES["MILES"]) - 1
                )
                dict[user_num]["LENGTH"] = USER_MILES["LENGTH"]

        dict = sorted(dict, key=lambda x: x["COUNT"])

        return dict

    def draw_duplication(self, file_name="bar.png"):
        list_duplication = []
        DUPLICATIONS = self.get_duplication()
        for DUPLICATION in DUPLICATIONS:
            list_duplication.append(DUPLICATION["Count"])
        sorted_duplication = sorted(list_duplication)
        unique_values, counts = zip(
            *[
                (value, sorted_duplication.count(value))
                for value in set(sorted_duplication)
            ]
        )
        draw_bar(Bar(unique_values, counts, "重複数", "出現回数", "", file_name))

    def draw_boxplot(self, file_name="box.png"):
        mile_lengths = self.get_length()
        draw_boxplot(
            BoxPlot(
                [mile_lengths.array, mile_lengths.array2],
                "BASICからDEVELOPING以上",
                "DEVELOPINGからMASTER",
                "",
                file_name,
            )
        )

    def __is_grow_up(self, scores_start, scores_end):
        for score_start, score_end in zip(scores_start, scores_end):
            if score_start < score_end:
                return True
        return False

    def __find_duplication(self, list: list, value: dict):
        if not list:
            return -1
        for index, dict in enumerate(list):
            if Counter(value["Edge"]) == Counter(dict["Edge"]):
                return index
        return -1

    def __is_next_level(self, end: str or dict):
        if type(end) is str:
            return True
        else:
            return False

    def __calculate_euclid(self, x: dict, y: dict):
        sum = 0
        for concept in skill.CT_SKILL:
            sum += (int(x[concept]) - int(y[concept])) ** 2
        return round(sum**0.5, 3)
