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
df1 = pd.read_csv(f'file1.csv')
df2 = pd.read_csv(f'file2.csv')

# Merge the DataFrames on the 'UserName' column
merged_df = pd.merge(df1, df2, on='UserName', suffixes=('_df1', '_df2'))

# Filter rows where Class or PredClass values differ between df1 and df2
filtered_df = merged_df[(merged_df['Class_df1'] != merged_df['Class_df2']) | (merged_df['PredClass_df1'] != merged_df['PredClass_df2'])]

# Select and display the relevant columns
output_columns = ['UserName', 'Class_df1', 'PredClass_df1', 'Class_df2', 'PredClass_df2']
result = filtered_df[output_columns]

print(result)