import sys
import json
from tqdm import tqdm
from typing import NamedTuple

sys.path.append("../")

from stats import MileStastics
from constants import path
from graph import draw_lines


class LineProps(NamedTuple):
    x: list
    y1: list
    y2: list
    y3: list
    file_name: str


json_file = open(path.MODEL + "btod_results5.json", "r")
bas_to_dev = json.load(json_file)
# json_file = open(path.MODEL + "btod_results5.json", "r")
# bas_to_dev = json.load(json_file)

draw_lines(
    LineProps(
        bas_to_dev["num"],
        bas_to_dev["precision"],
        bas_to_dev["recall"],
        bas_to_dev["f1"],
        path.LINES + "btod-lines5.pdf",
    )
)

# json_file = open(path.MODEL + "dtom_results5.json", "r")
# bas_to_dev = json.load(json_file)

# draw_lines(LineProps(
#   bas_to_dev["num"],
#   bas_to_dev["precision"],
#   bas_to_dev["recall"],
#   bas_to_dev["f1"],
#   path.LINES + "dtom-lines5.pdf"
# ))
