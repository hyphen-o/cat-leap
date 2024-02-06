import sys
import json
from tqdm import tqdm

sys.path.append("../")

from stats import MileStastics
from constants import path
from graph import draw_digraph

dupli_all = open(path.BAS_TO_DEV + "duplication-target.json", "r")
dupli_all2 = open(path.DEV_TO_MAS + "duplication-target.json", "r")
json_file = open(path.BAS_TO_DEV + "target.json", "r")
json_file2 = open(path.DEV_TO_MAS + "target.json", "r")
b_to_d = json.load(json_file)
d_to_m = json.load(json_file2)
dupli_all = json.load(dupli_all)
dupli_all2 = json.load(dupli_all2)

split_dict = {}
for i in range(2, 20):
    split_dict[str(i)] = []
    for USER_MILES in b_to_d:
        if USER_MILES["LENGTH"] == i:
            split_dict[str(i)].append(USER_MILES)

split_dict2 = {}
for i in range(2, 20):
    split_dict2[str(i)] = []
    for USER_MILES in d_to_m:
        if USER_MILES["LENGTH"] == i:
            split_dict2[str(i)].append(USER_MILES)

with open(path.BAS_TO_DEV + "splitted_target.json", "w") as f:
    json.dump(split_dict, f, indent=2)
with open(path.DEV_TO_MAS + "splitted_target.json", "w") as f:
    json.dump(split_dict2, f, indent=2)

Ms = MileStastics()
all_result = []
for key, value in split_dict.items():
    print(len(value))
    Ms.set_data(value)
    duplication_list = Ms.get_duplication()
    sorted_list = sorted(duplication_list, key=lambda x: x["Count"], reverse=True)
    with open(path.BAS_TO_DEV + f"/splitted/{key}.json", "w") as f:
        json.dump(sorted_list, f, indent=2)

    next_node = "NEXT_LEVEL"
    result = []
    for i in range(int(key) - 1):
        edges = [edge for edge in sorted_list if edge["Edge"]["EndP"] == next_node]
        if not edges:
            print("break")
            break

        # 最大値を取得
        max_edges = max(edges, key=lambda x: x["Count"])

        # 最大値と一致する要素を抽出
        max_nodes = [x for x in edges if x["Count"] == max_edges["Count"]]

        if not len(max_nodes) == 1:
            max_dupli = []
            for max_node in max_nodes:
                for dupli in dupli_all:
                    if (max_node["Edge"]["StartP"] == dupli["Edge"]["StartP"]) and (
                        max_node["Edge"]["EndP"] == dupli["Edge"]["EndP"]
                    ):
                        max_dupli.append({"all": dupli, "original": max_node})
                        break
            if not max_dupli:
                print(next_node)
            max_tmp = max(max_dupli, key=lambda x: x["all"]["Count"])
            max_nodes = [max_tmp["original"]].copy()

        max_nodes[0]["Num"] = i
        next_node = max_nodes.copy()[0]["Edge"]["StartP"]
        result.append(max_nodes[0].copy())  # グラフ出力の際はここ変える

    with open(path.BAS_TO_DEV + f"/splitted/{key}-max.json", "w") as f:
        json.dump(result, f, indent=2)
    all_result += result

with open(path.BAS_TO_DEV + f"/splitted/all-max.json", "w") as f:
    json.dump(all_result, f, indent=2)

# draw_digraph(all_result, "bas_to_dev_rq1", 0)

# Ms = MileStastics()
# all_result2 = []
# for key, value in split_dict2.items():
#   Ms.set_data(value)
#   duplication_list = Ms.get_duplication()
#   print(duplication_list)
#   sorted_list = sorted(duplication_list, key=lambda x: x["Count"], reverse=True)
#   with open(path.DEV_TO_MAS + f"/splitted/{key}.json", "w") as f:
#       json.dump(sorted_list, f, indent=2)

#   next_node = "NEXT_LEVEL"
#   result = []
#   for i in range(int(key) - 1):
#     edges = []
#     edges = [ edge for edge in sorted_list if edge["Edge"]["EndP"] == next_node]
#     # if next_node == "NEXT_LEVEL":
#     # else:
#     #   edges = [ edge for edge in sorted_list if edge["Edge"]["EndP"] != "NEXT_LEVEL" if edge["Edge"]["EndP"]["Feature"] == next_node["Feature"]]

#     # print(i)
#     # for edge in sorted_list:
#     #    if edge["Edge"]["EndP"] != "NEXT_LEVEL" and next_node != "NEXT_LEVEL":
#     #     if edge["Edge"]["EndP"]["Feature"] == next_node["Feature"]:
#     #       print("asdadas" + str(edge))
#     #       edges.append(edge)
#     #    else:
#     #       if edge["Edge"]["EndP"] == next_node:
#     #          edges.append(edge)


#     # 最大値を取得
#     max_edges = max(edges, key=lambda x: x["Count"])

#     # 最大値と一致する要素を抽出
#     max_nodes = [x for x in edges if x["Count"] == max_edges["Count"]]

#     if not len(max_nodes) == 1:
#       max_dupli = []
#       for max_node in max_nodes:
#         for dupli in dupli_all2:
#            if (max_node["Edge"]["StartP"] == dupli["Edge"]["StartP"]) and (max_node["Edge"]["EndP"] == dupli["Edge"]["EndP"]):
#               max_dupli.append({"all": dupli, "original": max_node})
#               break
#       if not max_dupli:
#          print("none")
#       max_tmp = max(max_dupli, key=lambda x: x["all"]["Count"])
#       max_nodes = [max_tmp["original"]]

#     result.append(max_nodes[0].copy()) #グラフ出力の際はここ変える
#     next_node = max_nodes.copy()[0]["Edge"]["StartP"]
#     print(i)
#     print("next : " + str(next_node))

#   with open(path.DEV_TO_MAS + f"/splitted/{key}-max.json", "w") as f:
#       json.dump(result, f, indent=2)
#   all_result2 += result

# with open(path.DEV_TO_MAS + f"/splitted/all-max.json", "w") as f:
#       json.dump(all_result2, f, indent=2)

# # draw_digraph(all_result2, "dev_to_mas_rq1", 0)
