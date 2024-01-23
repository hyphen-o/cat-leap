import pandas as pd
import json
import sys

sys.path.append("../")

from constants import path


df = pd.DataFrame(
    {
        "UserName": [],
        "Abst-0": [],
        "Abst-1": [],
        "Abst-2": [],
        "Abst-3": [],
        "Para-0": [],
        "Para-1": [],
        "Para-2": [],
        "Para-3": [],
        "Logi-0": [],
        "Logi-1": [],
        "Logi-2": [],
        "Logi-3": [],
        "Sync-0": [],
        "Sync-1": [],
        "Sync-2": [],
        "Sync-3": [],
        "Flow-0": [],
        "Flow-1": [],
        "Flow-2": [],
        "Flow-3": [],
        "User-0": [],
        "User-1": [],
        "User-2": [],
        "User-3": [],
        "Data-0": [],
        "Data-1": [],
        "Data-2": [],
        "Data-3": [],
        "Class": [],
    }
)


def __is_grow_up(scores_start, scores_end):
    for score_start, score_end in zip(scores_start, scores_end):
        if score_start > score_end:
            return False
    return True


json_file = open(path.BAS_TO_DEV + "out-all.json", "r")
json_file2 = open(path.DEV_TO_MAS + "out-all.json", "r")
bas_to_dev = json.load(json_file)
dev_to_mas = json.load(json_file2)

dict = {
    "UserName": 0,
    "Abst-0": 0,
    "Abst-1": 0,
    "Abst-2": 0,
    "Abst-3": 0,
    "Para-0": 0,
    "Para-1": 0,
    "Para-2": 0,
    "Para-3": 0,
    "Logi-0": 0,
    "Logi-1": 0,
    "Logi-2": 0,
    "Logi-3": 0,
    "Sync-0": 0,
    "Sync-1": 0,
    "Sync-2": 0,
    "Sync-3": 0,
    "Flow-0": 0,
    "Flow-1": 0,
    "Flow-2": 0,
    "Flow-3": 0,
    "User-0": 0,
    "User-1": 0,
    "User-2": 0,
    "User-3": 0,
    "Data-0": 0,
    "Data-1": 0,
    "Data-2": 0,
    "Data-3": 0,
    "Class": 0,
}

for index, data in enumerate(dev_to_mas):
    dict["UserName"] = data["USER_NAME"]
    dict["Class"] = data["CLASS"]

    my_feature = []
    for index2, miles in enumerate(data["MILES"]):
        if data["CLASS"] and index2 == len(data["MILES"]) - 1:
            break
        if miles["IsRemix"]:
            break
        if not __is_grow_up(my_feature, miles["Before"]["Feature"]):
            break

        dict[f"Abst-{miles['Before']['Feature'][0]}"] += 1
        dict[f"Para-{miles['Before']['Feature'][1]}"] += 1
        dict[f"Logi-{miles['Before']['Feature'][2]}"] += 1
        dict[f"Sync-{miles['Before']['Feature'][3]}"] += 1
        dict[f"Flow-{miles['Before']['Feature'][4]}"] += 1
        dict[f"User-{miles['Before']['Feature'][5]}"] += 1
        dict[f"Data-{miles['Before']['Feature'][6]}"] += 1

    df.loc[index] = [dict[col] if col in dict else df[col][1] for col in df.columns]
    dict = {
        "UserName": 0,
        "Abst-0": 0,
        "Abst-1": 0,
        "Abst-2": 0,
        "Abst-3": 0,
        "Para-0": 0,
        "Para-1": 0,
        "Para-2": 0,
        "Para-3": 0,
        "Logi-0": 0,
        "Logi-1": 0,
        "Logi-2": 0,
        "Logi-3": 0,
        "Sync-0": 0,
        "Sync-1": 0,
        "Sync-2": 0,
        "Sync-3": 0,
        "Flow-0": 0,
        "Flow-1": 0,
        "Flow-2": 0,
        "Flow-3": 0,
        "User-0": 0,
        "User-1": 0,
        "User-2": 0,
        "User-3": 0,
        "Data-0": 0,
        "Data-1": 0,
        "Data-2": 0,
        "Data-3": 0,
        "Class": 0,
    }

df.to_csv("CTScore15.csv")


print(df)
