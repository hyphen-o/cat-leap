import sys
import json
from tqdm import tqdm

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

goal_dict = []
for USER_MILES in tqdm(dev_to_mas):
    GOAL_MILE = USER_MILES["MILES"][len(USER_MILES["MILES"]) - 1]
    flg = True
    for index, target in enumerate(goal_dict):
        if target["Feature"] == GOAL_MILE["Before"]["Feature"]:
            goal_dict[index]["COUNT"] += 1
            flg = False
            break

    if flg:
        goal_dict.append(
            {
                "COUNT": 1,
                "Feature": GOAL_MILE["Before"]["Feature"],
                "CTScore": GOAL_MILE["Before"]["CTScore"],
            }
        )

sorted_goal = sorted(goal_dict, key=lambda x: x["COUNT"], reverse=True)

with open(path.DEV_TO_MAS + "goals.json", "w") as f:
    json.dump(sorted_goal, f, indent=2)


Ms = MileStastics()

# Ms.set_data(bas_to_dev)
# duplication_list = Ms.get_all_duplication(bas_to_dev_dup)
# length = Ms.get_length()
# draw_digraph(duplication_list, "dev_to_mas", 2)
