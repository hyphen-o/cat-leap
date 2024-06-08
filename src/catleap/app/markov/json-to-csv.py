import json
import pandas as pd
from tqdm import tqdm
import sys

sys.path.append("../../")
from utils import ToCsv

for i in range(1, 19):
  json_file = open(f"users/{i}-dtom.json", "r")
  bas_to_dev = json.load(json_file)
  csv = ToCsv(f"users/{i}-dtom.csv", ["UserName", "Class", "PredClass"])

  for row in bas_to_dev:
    csv.writeRow([row["USER_NAME"], row["TRUE_STATE"], row["PREDICT_STATE"]])