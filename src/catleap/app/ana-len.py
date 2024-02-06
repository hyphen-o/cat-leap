import sys
import json
import statistics
from scipy.stats import mannwhitneyu
from typing import NamedTuple

sys.path.append("../")

from stats import MileStastics
from constants import path
from graph import draw_boxplot


class BoxPlot(NamedTuple):
    nested_list: list
    xlabel: str
    ylabel: str
    title: str
    file_name: str


json_file = open(path.BAS_TO_DEV + "not-target.json", "r")
json_file2 = open(path.DEV_TO_MAS + "duplication-all.json", "r")
bas_to_dev = json.load(json_file)
dev_to_mas = json.load(json_file2)

length = 0
for user_miles in bas_to_dev:
    length += len(user_miles["MILES"])

print(length)