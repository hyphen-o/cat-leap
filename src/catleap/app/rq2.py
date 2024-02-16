import pandas as pd

import sys
import json
from tqdm import tqdm

sys.path.append("../")

from stats import MileStastics
from constants import path
from graph import draw_digraph
from scipy.stats import mannwhitneyu
import statistics

# Assuming you have two CSV files: 'file1.csv' and 'file2.csv'
# Load the CSV files into DataFrames
df1 = pd.read_csv(f"./results/dtom-before.csv")
df2 = pd.read_csv(f"./results/dtom.csv")

# Merge the DataFrames on the 'UserName' column
merged_df = pd.merge(df1, df2, on="UserName")

# Filter rows where Class or PredClass values differ between df1 and df2
before_positive = merged_df[
    (merged_df["Class_before"] == merged_df["PredClass_before"])
    & (merged_df["Class"] != merged_df["PredClass"])
]
positive = merged_df[
    (merged_df["Class_before"] != merged_df["PredClass_before"])
    & (merged_df["Class"] == merged_df["PredClass"])
]
dupli_positive = merged_df[
    (merged_df["Class_before"] == merged_df["PredClass_before"])
    & (merged_df["Class"] == merged_df["PredClass"])
]
negative = merged_df[
    (merged_df["Class_before"] != merged_df["PredClass_before"])
    & (merged_df["Class"] != merged_df["PredClass"])
]
# filtered_df = merged_df[(merged_df['Class_before'] == merged_df['Predclass_before']) | (merged_df['PredClass_df1'] != merged_df['PredClass_df2'])]
before_positive.to_csv("./results/dtom_before_positive.csv")
dupli_positive.to_csv("./results/dtom_dupli_positive.csv")
negative.to_csv("./results/dtom_negative.csv")
positive.to_csv("./results/dtom_positive.csv")

json_file = open(path.BAS_TO_DEV + "out-all.json", "r")
json_file2 = open(path.DEV_TO_MAS + "out-all.json", "r")
bas_to_dev = json.load(json_file)
dev_to_mas = json.load(json_file2)

array = []
for index, row in tqdm(before_positive.iterrows()):
    for USER in dev_to_mas:
        if USER["USER_NAME"] == row["UserName"]:
            array.append(len(USER["MILES"]) - 1)

array2 = []
for index, row in tqdm(positive.iterrows()):
    for USER in dev_to_mas:
        if USER["USER_NAME"] == row["UserName"]:
            array2.append(len(USER["MILES"]) - 1)

array3 = []
for index, row in tqdm(negative.iterrows()):
    for USER in dev_to_mas:
        if USER["USER_NAME"] == row["UserName"]:
            array3.append(len(USER["MILES"]) - 1)

array4 = []
for index, row in tqdm(dupli_positive.iterrows()):
    for USER in dev_to_mas:
        if USER["USER_NAME"] == row["UserName"]:
            array4.append(len(USER["MILES"]) - 1)

array5 = array + array2 + array4

statistic, p_value = mannwhitneyu(array3, array5)

print("Mann-Whitney U 検定統計量:", statistic)
print("p 値:", p_value)
print(f"中央値： {statistics.median(array3)}")
print(f"中央値： {statistics.median(array5)}")


# Select and display the relevant columns
# output_columns = ['UserName', 'Class_df1', 'PredClass_df1', 'Class_df2', 'PredClass_df2']
# result = filtered_df[output_columns]

# print(result)
