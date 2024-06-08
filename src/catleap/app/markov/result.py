import sys
import json
from tqdm import tqdm
from typing import NamedTuple
import numpy as np

sys.path.append("../../")

from constants import path
from graph import draw_acccumlate


class LineProps(NamedTuple):
    x: list
    y1: list
    y2: list
    file_name: str


json_file = open("markov-b-to-d-binary.json", "r")
bas_to_dev = json.load(json_file)
# json_file = open(path.MODEL + "btod_results5.json", "r")
# bas_to_dev = json.load(json_file)
new_list = np.array(bas_to_dev["all-count"]) - np.array(bas_to_dev["correct-count"]) - np.array(bas_to_dev["false-count"])

draw_acccumlate(
    {
        "x": bas_to_dev["num"],
        "precision": bas_to_dev["precision"],
        "recall": bas_to_dev["recall"],
        "f1": bas_to_dev["f1"],
        "y2": new_list,
        "y3": np.array(bas_to_dev["correct-count"]),
        "y4": np.array(bas_to_dev["false-count"]),
        "file_name": "markov-btod-binary.pdf"
    }
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
