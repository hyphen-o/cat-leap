import sys
import json
from tqdm import tqdm

sys.path.append("../")

from constants import path

json_file = open(path.MODEL + "btod_results5.json", "r")
bas_to_dev = json.load(json_file)