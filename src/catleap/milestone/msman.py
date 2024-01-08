import os
import json
import pandas as pd
from .milestone import MileStoneEvaluater
from constants import path
from tqdm import tqdm


class MileStoneManager(MileStoneEvaluater):
    def __init__(self, dir_path):
        self.__DIR_PATH = dir_path
        self.__bas_to_dev = []
        self.__dev_to_mas = []

    def get_milestone(self):
        for file_name in tqdm(os.listdir(self.__DIR_PATH)):
            personal_data = pd.read_csv(path.CT_CSV_SPLITTED + file_name)
            super().set_data(personal_data)
            milestones = super().get_milestone()
            if milestones["BASIC_TO_DEVELOPING"]:
                self.__bas_to_dev.append(milestones["BASIC_TO_DEVELOPING"])
            if milestones["DEVELOPING_TO_MASTER"]:
                self.__dev_to_mas.append(milestones["DEVELOPING_TO_MASTER"])

        with open(path.BAS_TO_DEV + "out.json", "w") as f:
            json.dump(self.__bas_to_dev, f, indent=2)
        with open(path.DEV_TO_MAS + "out.json", "w") as f:
            json.dump(self.__dev_to_mas, f, indent=2)
