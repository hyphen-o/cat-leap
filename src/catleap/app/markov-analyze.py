import sys
import json
from tqdm import tqdm
import matplotlib.pyplot as plt
from collections import Counter

sys.path.append("../")

from constants import path

json_file = open(path.BAS_TO_DEV + "predictions/1-b-to-d-either.json", "r")
bas_to_dev = json.load(json_file)


predict_right = []
for result in tqdm(bas_to_dev):
  if not result["PREDICT"]:
    user_name = result["USER_NAME"]
    out_json = open(path.BAS_TO_DEV + "out.json", "r")
    miles = json.load(out_json)

    for mile in miles:
      if mile["USER_NAME"] == user_name:
        predict_right.append(len(mile["MILES"]))


# 重複数をカウント
counter = Counter(predict_right)

# カウント結果を棒グラフとして描画
labels, counts = zip(*counter.items())
plt.bar(labels, counts)
plt.xlabel('Number')
plt.ylabel('Frequency')
plt.title('Number Frequency')
plt.show()
