import sys
import json
from typing import NamedTuple
from tqdm import tqdm
from scipy.stats import mannwhitneyu
import statistics

sys.path.append("../")

from stats import MileStastics
from constants import path, skill
from graph import draw_digraph,draw_boxplot


json_file = open(path.BAS_TO_DEV + "out-all.json", "r")
json_file2 = open(path.DEV_TO_MAS + "out-all.json", "r")
bas_to_dev = json.load(json_file)
dev_to_mas = json.load(json_file2)

json_file = open(path.BAS_TO_DEV + "duplication-all2.json", "r")
json_file2 = open(path.DEV_TO_MAS + "duplication-all2.json", "r")
bas_to_dev_dupli = json.load(json_file)
dev_to_mas_dupli = json.load(json_file2)

btod_positive_array = []
btod_negative_array = []
dtom_positive_array = []
dtom_negative_array = []
for USER in tqdm(dev_to_mas):
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
  for dupli in dev_to_mas_dupli:
    if dupli["Edge"]["StartP"] == FLATTEN_MILE and dupli["Edge"]["EndP"] == FLATTEN_NEXT_MILE:
      if USER["CLASS"]:
        btod_positive_array.append(dupli["Count"])
      else:
        btod_negative_array.append(dupli["Count"])


"""props = {
          nested_list : List[list],
          xlabel : str,
          ylabel : str,
          title: str
          file_name: str
    }"""

statistic, p_value = mannwhitneyu(btod_positive_array, btod_negative_array)

print("Mann-Whitney U 検定統計量:", statistic)
print("p 値:", p_value)
print(f"中央値： {statistics.median(btod_positive_array)}")
print(f"中央値： {statistics.median(btod_negative_array)}")

class Props(NamedTuple):
  nested_list: list
  xlabel: str
  ylabel: str
  title: str
  file_name: str

draw_boxplot(
  Props(
    [btod_positive_array, btod_negative_array],
    "DtoMユーザ",
    "非DtoMユーザ",
    "",
    "add-dtom.pdf"
  )
)