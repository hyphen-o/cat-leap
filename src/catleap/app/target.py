import sys
import json
from tqdm import tqdm

sys.path.append("../")

from stats import MileStastics
from constants import path
from graph import draw_digraph

json_file = open(path.BAS_TO_DEV + "goals.json", "r")
json_file3 = open(path.BAS_TO_DEV + "out.json", "r")
json_file2 = open(path.DEV_TO_MAS + "goals.json", "r")
json_fil4 = open(path.DEV_TO_MAS + "out.json", "r")
b_to_d = json.load(json_file)
bas_to_dev_out = json.load(json_file3)
d_to_m = json.load(json_file2)
dev_to_mas_out = json.load(json_fil4)

target_b_to_d = []
for index, out in enumerate(bas_to_dev_out):
    if out["MILES"][len(out["MILES"]) - 1]["Before"]["Feature"] == b_to_d[0]["Feature"]:
        target_b_to_d.append(out)
        del bas_to_dev_out[index]
for index, out in enumerate(bas_to_dev_out):
    if out["MILES"][len(out["MILES"]) - 1]["Before"]["Feature"] == b_to_d[0]["Feature"]:
        target_b_to_d.append(out)
        del bas_to_dev_out[index]

target_d_to_m = []
for index, out in enumerate(dev_to_mas_out):
    if out["MILES"][len(out["MILES"]) - 1]["Before"]["Feature"] == d_to_m[0]["Feature"]:
        target_d_to_m.append(out)
        del dev_to_mas_out[index]
for index, out in enumerate(dev_to_mas_out):
    if out["MILES"][len(out["MILES"]) - 1]["Before"]["Feature"] == d_to_m[0]["Feature"]:
        target_d_to_m.append(out)
        del dev_to_mas_out[index]

with open(path.BAS_TO_DEV + "target.json", "w") as f:
    json.dump(target_b_to_d, f, indent=2)
with open(path.BAS_TO_DEV + "not-target.json", "w") as f:
    json.dump(bas_to_dev_out, f, indent=2)
