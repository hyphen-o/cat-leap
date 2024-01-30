import os
import json
import pandas as pd
from .milestone import MileStoneEvaluater
from constants import path
from tqdm import tqdm
from typing import NamedTuple


class MileStones(NamedTuple):
    bas_to_dev: dict
    dev_to_mas: dict


class MileStoneManager(MileStoneEvaluater):
    def __init__(self, dir_path):
        self.__DIR_PATH = dir_path
        self.__bas_to_dev = []
        self.__dev_to_mas = []

    def get_milestone(self, is_all=False):
        for file_name in tqdm(os.listdir(self.__DIR_PATH)):
            personal_data = pd.read_csv(path.CT_CSV_SPLITTED + file_name)
            super().set_data(personal_data)
            milestones = super().get_milestone(is_all)
            if (
                milestones["BASIC_TO_DEVELOPING"]["MILES"]
                and len(milestones["BASIC_TO_DEVELOPING"]["MILES"]) > 1
            ):
                self.__bas_to_dev.append(milestones["BASIC_TO_DEVELOPING"])
            if (
                milestones["DEVELOPING_TO_MASTER"]["MILES"]
                and len(milestones["DEVELOPING_TO_MASTER"]["MILES"]) > 1
            ):
                self.__dev_to_mas.append(milestones["DEVELOPING_TO_MASTER"])

        OUT_NAME = "out-all.json" if is_all else "out.json"

        sorted_bas_to_dev = sorted(self.__bas_to_dev, key=lambda x: x["LENGTH"])
        sorted_dev_to_mas = sorted(self.__dev_to_mas, key=lambda x: x["LENGTH"])

        with open(path.BAS_TO_DEV + OUT_NAME, "w") as f:
            json.dump(sorted_bas_to_dev, f, indent=2)
        with open(path.DEV_TO_MAS + OUT_NAME, "w") as f:
            json.dump(sorted_dev_to_mas, f, indent=2)

        return MileStones(self.__bas_to_dev, self.__dev_to_mas)
