from typing import NamedTuple
import numpy as np
import sys
from tqdm import tqdm

sys.path.append("../")
from constants import skill
from graph import draw_boxplot


class Length(NamedTuple):
    array: list
    array2: list
    mean: int
    mean2: int


class BoxPlot(NamedTuple):
    nested_list: list
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
        for USER_MILES in self.__MILES_DATA:
            list_len.append(len(USER_MILES) - 1)
        if self.__MILES_SECOND_DATA:
            for USER_MILES in self.__MILES_SECOND_DATA:
                list_len2.append(len(USER_MILES) - 1)
        mean = np.mean(list_len)
        mean2 = np.mean(list_len2)

        return Length(list_len, list_len2, mean, mean2)

    def get_duplication(self):
        list_duplication = []
        for USER_MILES in tqdm(self.__MILES_DATA):
            for index, MILE in enumerate(USER_MILES):
                if index == len(USER_MILES) - 1:
                    break

                edge = {
                    "Edge": {
                        "StartP": {
                            **MILE["Before"],
                            "IsRemix": MILE["IsRemix"],
                            "Level": MILE["Level"],
                        },
                        "EndP": {
                            **USER_MILES[index + 1]["Before"],
                            "IsRemix": USER_MILES[index + 1]["IsRemix"],
                            "Level": USER_MILES[index + 1]["Level"],
                        }
                        if index != len(USER_MILES) - 2
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

    def draw_boxplot(self):
        mile_lengths = self.get_length()
        draw_boxplot(
            BoxPlot(
                [mile_lengths.array, mile_lengths.array2],
                "BASICからDEVELOPING以上",
                "DEVELOPINGからMASTER",
                "",
                "tests",
            )
        )

    def __find_duplication(self, list: list, value: dict):
        if not list:
            return -1
        for index, dict in enumerate(list):
            if value["Edge"] == dict["Edge"]:
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
