import pandas as pd

import sys
import json
from tqdm import tqdm

sys.path.append("../")

from stats import MileStastics
from constants import path
from graph import draw_digraph

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


# Select and display the relevant columns
# output_columns = ['UserName', 'Class_df1', 'PredClass_df1', 'Class_df2', 'PredClass_df2']
# result = filtered_df[output_columns]

# print(result)
