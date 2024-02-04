import sys
import json
from typing import NamedTuple

sys.path.append("../")

from stats import MileStastics
from constants import path
from graph import draw_line


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

bas_to_dev_count = [x['COUNT'] for x in dev_to_mas]
bas_to_dev_len = [x['LENGTH'] for x in dev_to_mas]

draw_line(BoxPlot(
                [bas_to_dev_count, bas_to_dev_len],
                "BASICからDEVELOPING以上",
                "DEVELOPINGからMASTER",
                "",
                "line2.png",
            ))
