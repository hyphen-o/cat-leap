import sys
import json
from tqdm import tqdm

sys.path.append("../")

from stats import MileStastics
from constants import path
from graph import draw_digraph

dupli_array = []
all_result = []
for i in range(2, 20):
  ct_array = open(path.DEV_TO_MAS + f"/splitted/{i}-max.json", "r")
  ct_array = json.load(ct_array)

  flat_array = []
  for ct_index, ct in enumerate(ct_array):
    if ct_index == 0:
      flat_array.insert(0, ct["Edge"]["EndP"])
    flat_array.insert(0, ct["Edge"]["StartP"])
  
  with open(path.DEV_TO_MAS + f"/splitted/flatten-{i}.json", "w") as f:
      json.dump(flat_array, f, indent=2)
    
  for index, node in enumerate(flat_array):
    if index == (len(flat_array) - 1):
       break
    flg = True
    for mark, dupli in enumerate(dupli_array):
        print(dupli)
        if dupli["Feature"] == node["Feature"]:
          print(mark)
          flat_array[index]["Mark"] = mark
          flg = False
          break
    if flg:
        dupli_array.append(node)
        flat_array[index]["Mark"] = int(len(dupli_array)) - 1
  
  all_result += flat_array
  
  with open(path.DEV_TO_MAS + f"/splitted/marked-{i}.json", "w") as f:
      json.dump(flat_array, f, indent=2)

with open(path.DEV_TO_MAS + f"/splitted/marked-all.json", "w") as f:
    json.dump(all_result, f, indent=2)



      
           
    








  # for ct_index, ct in enumerate(ct_array):
  #   flg = True
  #   for index, dupli in enumerate(dupli_array):
  #     if dupli == ct:
  #       ct_array[ct_index]["Mark"] = index
  #       flg = False
  #       break
  #   if flg:
  #     dupli_array.append(ct)
  #     ct_array[ct_index]["Mark"] = len(dupli_array) + 1
  
  # with open(path.DEV_TO_MAS + f"/splitted/{i}-max-new.json", "w") as f:
  #     json.dump(ct_array, f, indent=2)
    