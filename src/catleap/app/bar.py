import sys
import json

sys.path.append("../")

from stats import MileStastics
from constants import path
from graph import draw_digraph

json_file = open(path.BAS_TO_DEV + "out.json", "r")
json_file2 = open(path.DEV_TO_MAS + "out.json", "r")
bas_to_dev = json.load(json_file)
dev_to_mas = json.load(json_file2)

Msm = MileStastics()
Msm.set_data(bas_to_dev)
Msm.draw_duplication("bas_to_dev.png")


Msm = MileStastics()
Msm.set_data(dev_to_mas)
Msm.draw_duplication("dev_to_mas.png")