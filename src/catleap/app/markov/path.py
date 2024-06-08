from scipy.stats import mannwhitneyu

import matplotlib.pyplot as plt
import statistics
import japanize_matplotlib
import csv
import json
import sys

sys.path.append("../../")

from constants import path

# Read file A and store correct predictions
json_file = open("/catleap/catleap/out/json/milestones/bas_to_dev/out-all.json", "r")
bas_to_dev = json.load(json_file)

pathA = []
pathB = []

with open(f'extracted/{1}_only_correct_in_A.csv', mode='r') as file_A:
    reader_A = csv.DictReader(file_A)
    for row in reader_A: 
      for user in bas_to_dev:
          if user["USER_NAME"] == row["UserName"]:
            print(len(user["MILES"]))
            if not len(user["MILES"]) == 20:
              pathA.append(len(user["MILES"]))

with open(f'extracted/{1}_only_correct_in_B.csv', mode='r') as file_A:
    reader_A = csv.DictReader(file_A)
    for row in reader_A: 
      for user in bas_to_dev:
          if user["USER_NAME"] == row["UserName"]:
             if not len(user["MILES"]) == 20:
              pathB.append(len(user["MILES"]))


flg, ax = plt.subplots(figsize=(10, 5))

# bp = ax.boxplot(props.nested_list, showmeans=True, sym="", patch_artist=True)
bp = ax.boxplot([pathB, pathA], sym="", patch_artist=True, showmeans=True)
ax.set_xticklabels(["従来モデル", "提案マルコフ連鎖モデル"], fontsize=16)

bp["boxes"][0].set_color("lightblue")
bp["boxes"][1].set_color("lightsalmon")

for whisker in bp["whiskers"]:
    whisker.set_color("#282828")

for cap in bp["caps"]:
    cap.set_color("#282828")

for median in bp["medians"]:
    median.set_color("#282828")

for flier in bp["fliers"]:
    flier.set(marker="o", color="red", alpha=0.5)

ax.set_ylabel("作品制作数", fontsize=16)
plt.tight_layout()
plt.grid()
plt.savefig("btod-path.pdf")


# マン・ホイットニーのU検定を実施
stat, p_value = mannwhitneyu(pathA, pathB)
print(p_value)

print(str(statistics.median(pathA)))
print(str(statistics.median(pathB)))