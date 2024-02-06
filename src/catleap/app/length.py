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


json_file = open(path.BAS_TO_DEV + "duplication-all.json", "r")
json_file2 = open(path.DEV_TO_MAS + "duplication-all.json", "r")
bas_to_dev = json.load(json_file)
dev_to_mas = json.load(json_file2)

for i in range(2, 21):
    bas_to_dev_len = []
    dev_to_mas_len = []
    for x in bas_to_dev:
        if int(x["LENGTH"]) == int(i):
            bas_to_dev_len.append(x)
    for x in dev_to_mas:
        if int(x["LENGTH"]) == int(i):
            dev_to_mas_len.append(x)

    sorted_bas_to_dev = sorted(bas_to_dev_len, key=lambda x: x["COUNT"], reverse=True)
    sorted_dev_to_mas = sorted(dev_to_mas_len, key=lambda x: x["COUNT"], reverse=True)

    sorted_bas_to_dev[0]["MILES"]
    sorted_dev_to_mas[0]["MILES"]

    print(str(i - 1) + ":" + str(statistics.median(bas_to_dev_len)))
    print(str(i - 1) + ":" + str(statistics.median(dev_to_mas_len)))
