from typing import NamedTuple
import numpy as np
import sys
from tqdm import tqdm

sys.path.append("../")
from constants import skill


class Length(NamedTuple):
    list: list
    mean: int


class MileStastics:
    def set_data(self, miles_data: list):
        self.__MILES_DATA = miles_data

    def get_length(self):
        list_len = []
        for USER_MILES in self.__MILES_DATA:
            list_len.append(len(USER_MILES) - 1)
        mean = np.mean(list_len)

        return Length(list_len, mean)

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
