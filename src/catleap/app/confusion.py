from sklearn.metrics import confusion_matrix

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
print(df1)
print(df2)
# df2 = df2.drop(columns=["Class"])

# 'UserName'列をキーにして2つのDataFrameを結合
df1 = df2.merge(df1, on="UserName", how='inner')
len(df1.index)
len(df2.index)
print(df1)

y_true = df1['Class_x'].values
y_suggest = df1['PredClass_suggest'].values
y_before = df1['PredClass'].values

print(y_before)

# 提案モデルの混同行列
confusion_matrix_model1 = confusion_matrix(y_true, y_suggest)
print("モデル1の混同行列:")
print(confusion_matrix_model1)

# 従来モデルの混同行列
confusion_matrix_model2 = confusion_matrix(y_true, y_before)
print("モデル2の混同行列:")
print(confusion_matrix_model2)