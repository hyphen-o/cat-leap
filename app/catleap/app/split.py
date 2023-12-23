import pandas as pd
import sys

sys.path.append("../")
from constants import CT_CSV_PATH, CT_CSV_SPLITTED_PATH

df = pd.read_csv(CT_CSV_PATH + "ct_score_ando.csv")
grouped = df.groupby("UserName")

for name, group, index in grouped:
    group.to_csv(CT_CSV_SPLITTED_PATH + f"{name}.csv")
