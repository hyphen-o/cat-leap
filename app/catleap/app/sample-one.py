import pandas as pd
import sys

sys.path.append("../")
from milestone import MileStoneEvaluater
from constants import CT_CSV_SAMPLE_PATH, CT_CSV_SPLITTED_PATH

df = pd.read_csv(CT_CSV_SAMPLE_PATH + "ct_sample.csv")
mse = MileStoneEvaluater()
mse.set_data(df)
print(mse.get_milestone())
