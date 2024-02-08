import sys
import json

sys.path.append("../")

from stats import MileStastics
from constants import path, skill
from graph import draw_digraph

json_file = open(path.BAS_TO_DEV + "out-all.json", "r")
json_file2 = open(path.DEV_TO_MAS + "out-all.json", "r")
bas_to_dev = json.load(json_file)
dev_to_mas = json.load(json_file2)


# def get_duplication(MILES):
#     list_duplication = []
#     for index, MILE in enumerate(MILES):
#         if index == len(MILES) - 1:
#             break
#         if MILE == "NEXT_LEVEL":
#             continue

#         edge = {
#             "Edge": {
#                 "StartP": {**MILE},
#                 "EndP": MILES[index + 1]
#                 if MILES[index + 1] == "NEXT_LEVEL"
#                 else MILES[index + 1]
#                 if index != len(MILES) - 2
#                 else "NEXT_LEVEL",
#             }
#         }

#         # dupli_index = __find_duplication(list_duplication, edge)

#         # if not dupli_index == -1:
#         #     list_duplication[dupli_index]["Count"] += 1
#         # else:
#         list_duplication.append(
#             {
#                 "Count": 1,
#                 # "Euclid": __calculate_euclid(
#                 #     edge["Edge"]["StartP"], edge["Edge"]["EndP"]
#                 # )
#                 # if not __is_next_level(edge["Edge"]["EndP"])
#                 # else None,
#                 **edge,
#             }
#         )
#     return list_duplication


def __find_duplication(list: list, value: dict):
    if not list:
        return -1
    for index, dict in enumerate(list):
        if value["Edge"] == dict["Edge"]:
            return index
    return -1


def __is_next_level(end: str or dict):
    if type(end) is str:
        return True
    else:
        return False


def __calculate_euclid(x: dict, y: dict):
    sum = 0
    for concept in skill.CT_SKILL:
        sum += (int(x[concept]) - int(y[concept])) ** 2
    return round(sum**0.5, 3)


ms = MileStastics()
ms.set_data(bas_to_dev)
dupli = ms.get_duplication()
# duplication_list = get_duplication(bas_to_dev)
# print(duplication_list)
with open(path.BAS_TO_DEV + "duplication-all3.json", "w") as f:
    json.dump(dupli, f, indent=2)
ms.set_data(dev_to_mas)
dupli = ms.get_duplication()
# duplication_list = get_duplication(bas_to_dev)
# print(duplication_list)
with open(path.DEV_TO_MAS + "duplication-all3.json", "w") as f:
    json.dump(dupli, f, indent=2)
# draw_digraph(duplication_list, "bas_to_dev_marked", 0)

# duplication_list = get_duplication(dev_to_mas)
# with open(path.DEV_TO_MAS + "duplication-target.json", "w") as f:
#     json.dump(duplication_list, f, indent=2)
# draw_digraph(duplication_list, "dev_to_mas_marked", 0)
