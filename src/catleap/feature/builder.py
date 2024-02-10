import sys
import json
import pandas as pd
from tqdm import tqdm

sys.path.append("../")

from constants import path


class FeatureBuilder:
    def __init__(self, type: str):
        self.__TYPE = type
        self.__read_data()

    def extract_features(self, bottom=True, cached=True):
        self.IS_BOTTOM = bottom
        match (self.__TYPE):
            case "TRANS":
                self.__extract_trans_features("BAS_TO_DEV", cached)
                self.__extract_trans_features("DEV_TO_MAS", cached)
                pass  # TODO
            case _:
                print("タイプを入力してください．")
                return

    def __read_data(self):
        match (self.__TYPE):
            case "TRANS":
                self.__DATA = {
                    "BAS_TO_DEV": {
                        "USERS": json.load(open(path.BAS_TO_DEV + "out-all.json", "r")),
                        "DUPLICATIONS": json.load(
                            open(path.BAS_TO_DEV + "duplication-all2.json", "r")
                        ),
                    },
                    "DEV_TO_MAS": {
                        "USERS": json.load(open(path.DEV_TO_MAS + "out-all.json", "r")),
                        "DUPLICATIONS": json.load(
                            open(path.DEV_TO_MAS + "duplication-all2.json", "r")
                        ),
                    },
                }
                return
            case _:
                print("正しいタイプを入力してください．")
                return

    def __extract_trans_features(self, target, cached):
        USERS = self.__DATA[target]["USERS"]
        probablities_dict = {}

        if not cached:
            for USER in tqdm(USERS):
                USER_NAME = USER["USER_NAME"]
                is_positive = USER["CLASS"]

                probablities = self.__calculate_probablity(
                    USER["MILES"], target, is_positive
                )
                probablities_dict[USER_NAME] = {}
                probablities_dict[USER_NAME]["PROBABILITY"] = probablities
                probablities_dict[USER_NAME]["ORIGIN_CLASS"] = USER["CLASS"]
            self.__save_dict(probablities_dict, target, "probablities")
        else:
            if target == "BAS_TO_DEV":
                probablities_dict = json.load(
                    open(path.BAS_TO_DEV + "probablities.json", "r")
                )
            elif target == "DEV_TO_MAS":
                probablities_dict = json.load(
                    open(path.DEV_TO_MAS + "probablities.json", "r")
                )

        for length in tqdm(range(1, 20)):
            labels = ["UserName"] + [f"Trans{i}" for i in range(length)] + ["Class"]
            df = pd.DataFrame(columns=labels)
            for user_name, dict in tqdm(probablities_dict.items(), leave=False):
                if len(dict["PROBABILITY"]) <= length:
                    continue
                
                user_class = 0
                if self.IS_BOTTOM:
                    user_class = dict["ORIGIN_CLASS"]
                else:         
                  if len(dict["PROBABILITY"]) == length:
                      if length == 19 and not dict["ORIGIN_CLASS"]:
                          user_class = 0
                      else:
                          user_class = 1

                trans = 1.0
                trans_array = []
                tmp = dict["PROBABILITY"].pop(-1)
                for index, probablity in enumerate(dict["PROBABILITY"][len(dict["PROBABILITY"]) - length: ]):
                    trans *= probablity
                    trans_array.append(trans)
                    if index + 1 == length:
                        break
                dict["PROBABILITY"].append(tmp)

                df.loc[len(df)] = [user_name] + trans_array + [user_class]
            if target == "BAS_TO_DEV":
                df.to_csv(path.MODEL + f"feature/CT8-{str(length) + '-reversed3' if self.IS_BOTTOM else str(length) + '-reversed'}.csv", index=False)
            elif target == "DEV_TO_MAS":
                df.to_csv(path.MODEL + f"feature/CT15-{str(length) + '-reversed3' if self.IS_BOTTOM else length}.csv", index=False)

    def __calculate_probablity(self, MILES, target, is_positive):
        DUPLICATIONS = self.__DATA[target]["DUPLICATIONS"]
        probablities = []

        for index, MILE in enumerate(MILES):
            if index == len(MILES) - 1:
                break

            FLATTEN_MILE = {
                **MILE["Before"],
                "IsRemix": MILE["IsRemix"],
                "Level": MILE["Level"],
            }

            FLATTEN_NEXT_MILE = {
                **MILES[index + 1]["Before"],
                "IsRemix": MILES[index + 1]["IsRemix"],
                "Level": MILES[index + 1]["Level"],
            }

            target = 0
            all = 0
            for DUPLICATION in DUPLICATIONS:
                if FLATTEN_MILE == DUPLICATION["Edge"]["StartP"]:
                    all += DUPLICATION["Count"]

                    # if index == len(MILES) - 2 and is_positive:
                    #     if DUPLICATION["Edge"]["EndP"] == "NEXT_LEVEL":
                    #         target = DUPLICATION["Count"]
                    # else:
                    if FLATTEN_NEXT_MILE == DUPLICATION["Edge"]["EndP"]:
                        target = DUPLICATION["Count"]

            probablity = 0.0
            if target:
                probablity = target / all

            probablities.append(probablity)

        return probablities

    def __save_dict(self, data, target, file_name):
        match (target):
            case "BAS_TO_DEV":
                with open(path.BAS_TO_DEV + f"{file_name}.json", "w") as f:
                    json.dump(data, f, indent=2)
            case "DEV_TO_MAS":
                with open(path.DEV_TO_MAS + f"{file_name}.json", "w") as f:
                    json.dump(data, f, indent=2)
