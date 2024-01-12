from typing import NamedTuple
import numpy as np


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
        for USER_MILES in self.__MILES_DATA:
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
                    list_duplication.append({"Count": 1, **edge})

        return list_duplication

    def __find_duplication(self, list: list, value: dict):
        if not list:
            return -1
        for index, dict in enumerate(list):
            if value["Edge"] == dict["Edge"]:
                return index
            else:
                return -1
