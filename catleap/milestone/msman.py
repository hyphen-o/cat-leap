import os
import json
import pandas as pd
from .milestone import MileStoneEvaluater
from utils import group_by_colname
from constants import CT_CSV_SPLITTED_PATH, CT_JSON_PATH


class MileStoneManager(MileStoneEvaluater):
    def __init__(self, dir_path):
        self.__DIR_PATH = dir_path
        self.__milestone = []

    def get_milestone(self):
        for file_name in os.listdir(self.__DIR_PATH):
            personal_data = pd.read_csv(CT_CSV_SPLITTED_PATH + file_name)
            super().set_data(personal_data)
            milestone = super().get_milestone()
            if milestone:
                self.__milestone += milestone

        with open(CT_JSON_PATH + "out.json", "w") as f:
            json.dump(self.__milestone, f, indent=2)
