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

bas_to_dev = [x["COUNT"] for x in bas_to_dev]
dev_to_mas = [x["COUNT"] for x in dev_to_mas]

# Mann-Whitney U検定
statistic, p_value = mannwhitneyu(bas_to_dev, dev_to_mas)

print("Mann-Whitney U 検定統計量:", statistic)
print("p 値:", p_value)

print(
    "BAS_TO_DEV mean: "
    + str(statistics.mean(bas_to_dev))
    + " median: "
    + str(statistics.median(bas_to_dev))
)
print(
    "DEV_TO_MAS mean: "
    + str(statistics.mean(dev_to_mas))
    + " median: "
    + str(statistics.median(dev_to_mas))
)

draw_boxplot(
    BoxPlot(
        [bas_to_dev, dev_to_mas],
        "BASICからDEVELOPING以上",
        "DEVELOPINGからMASTER",
        "",
        "dupli-all.pdf",
    )
)
