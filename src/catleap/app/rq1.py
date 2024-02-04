import sys
import json

sys.path.append("../")

from stats import MileStastics
from constants import path
from graph import draw_digraph

json_file = open(path.BAS_TO_DEV + "out.json", "r")
dup_file = open(path.BAS_TO_DEV + "duplication.json", "r")
json_file2 = open(path.DEV_TO_MAS + "out.json", "r")
dup_file2 = open(path.DEV_TO_MAS + "duplication.json", "r")
bas_to_dev = json.load(json_file)
bas_to_dev_dup = json.load(dup_file)
dev_to_mas = json.load(json_file2)
dev_to_mas_dup = json.load(dup_file2)

Ms = MileStastics()
# Ms.set_data(bas_to_dev)
# duplication_list = Ms.get_all_duplication(bas_to_dev_dup)
# with open(path.BAS_TO_DEV + "duplication-all.json", "w") as f:
#     json.dump(duplication_list, f, indent=2)
# length = Ms.get_length()
# draw_digraph(duplication_list, "bas_to_dev", 2)

Ms.set_data(bas_to_dev)
duplication_list = Ms.get_all_duplication(bas_to_dev_dup)
with open(path.BAS_TO_DEV + "duplication-all.json", "w") as f:
    json.dump(duplication_list, f, indent=2)
# length = Ms.get_length()
# draw_digraph(duplication_list, "dev_to_mas", 2)
