import os
import json
import sys
from collections import defaultdict
sys.path.append("../")
from constants import CT_JSON_PATH


# with open(CT_JSON_PATH + 'out_unique_unit.json') as f:
#     di = json.load(f)


# def group_by_ct_score(data):
#     grouped_dict = defaultdict(list)

#     for d in data:
#         ct_score = d["Dictionary"]["Before"]["CTScore"]
#         grouped_dict[ct_score].append(d)

#     return grouped_dict


# grouped_by_ct_score = group_by_ct_score(di)

# with open(CT_JSON_PATH + 'out_unique_unit.json', 'w') as f:
#             json.dump(grouped_by_ct_score, f, indent=2)

# for i in range(21):
#     if di[str(i)]:
#       with open(CT_JSON_PATH + f'split_unitted/out_{i}.json', 'w') as f:
#             json.dump(di[str(i)], f, indent=2)
# 


for i in range(1, 21):
  dev = []
  mas = []  
  with open(f'{CT_JSON_PATH}milestones/out_{i}.json', "r") as f:
    di = json.load(f)
  
  for d in di:
     if d["Dictionary"]["Reach"] >= 15 and i < 15:
        mas.append(d)
     elif d["Dictionary"]["Reach"] >= 8 and i < 8:
        dev.append(d)
  
  with open(CT_JSON_PATH + f'milestones/{i}/developing/{i}_dev.json', 'w') as f:
    json.dump(dev, f, indent=2)
  with open(CT_JSON_PATH + f'milestones/{i}/master/{i}_mas.json', 'w') as f:
    json.dump(mas, f, indent=2)


