import pandas as pd
import json
from collections import defaultdict
import sys

sys.path.append("../")
from milestone import MileStoneManager
from constants import path

# df = pd.read_csv(path.CT_CSV_ + "ct_sample.csv")
msm = MileStoneManager(path.CT_CSV_SPLITTED)
dir = msm.get_milestone(True)
