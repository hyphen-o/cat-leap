import json
import pandas as pd
from tqdm import tqdm
import sys

sys.path.append("../")
from constants import path

json_file = open(path.BAS_TO_DEV + "out.json", "r")
bas_to_dev = json.load(json_file)

jsons = []

for user in tqdm(bas_to_dev):
    miles = []
    for mile in user:
        miles.append(mile["Before"])

    miles.pop()

    jsons.append({"Miles": miles, "UserName": user[0]["UserName"]})

users = []

for mile1 in jsons:
    for mile2 in jsons:
        if mile1["UserName"] != mile2["UserName"]:
            if mile1["Miles"] == mile2["Miles"]:
                users.append([mile1["UserName"], mile2["UserName"]])

with open(path.BAS_TO_DEV + "comparator.json", "w") as f:
    json.dump(users, f, indent=2)

df = pd.read_csv(path.CSV + "ando/result_pre/[RESULT]class_CTScore-8.csv")
count = 0
array = []
print(users)
print(len(users))
for taple in users:
    row1 = df.loc[df["UserName"] == str(taple[0])]
    row2 = df.loc[df["UserName"] == str(taple[1])]
    if not row1[["Class", "PredClass"]].values.tolist():
        continue
    if not row2[["Class", "PredClass"]].values.tolist():
        continue
    # if (row1[['Class', 'PredClass']].values.tolist() != row2[['Class', 'PredClass']].values.tolist()):
    #   print(taple[0], taple[1])

    if (row1["Class"].values[0] == 1 and row1["PredClass"].values[0] == 0) and (
        row2["Class"].values[0] == 1 and row2["PredClass"].values[0] == 0
    ):
        array.append(taple)

with open(path.BAS_TO_DEV + "result-none-none.json", "w") as f:
    json.dump(array, f, indent=2)
