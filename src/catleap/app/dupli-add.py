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

json_file = open(path.BAS_TO_DEV + "duplication-all3.json", "r")
json_file2 = open(path.DEV_TO_MAS + "duplication-all3.json", "r")
bas_to_dev_dupli = json.load(json_file)
dev_to_mas_dupli = json.load(json_file2)

btod_positive_array = []
btod_negative_array = []
dtom_positive_array = []
dtom_negative_array = []
for USER in bas_to_dev:
  FLATTEN_MILE = {
      **USER["MILES"][len(USER["MILES"]) -3]["Before"],
      "IsRemix": USER["MILES"][len(USER["MILES"]) -3]["IsRemix"],
      "Level": USER["MILES"][len(USER["MILES"]) -3]["Level"],
  }
  FLATTEN_NEXT_MILE = {
      **USER["MILES"][len(USER["MILES"]) -2]["Before"],
      "IsRemix": USER["MILES"][len(USER["MILES"]) -2]["IsRemix"],
      "Level": USER["MILES"][len(USER["MILES"]) -2]["Level"],
  }
  for dupli in bas_to_dev_dupli:
    if dupli["Edge"]
    
