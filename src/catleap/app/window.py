import sys
import json

sys.path.append("../")

from constants import path

json_file = open(path.BAS_TO_DEV + "out.json", "r")
json_file2 = open(path.DEV_TO_MAS + "out.json", "r")
bas_to_dev = json.load(json_file)
dev_to_mas = json.load(json_file2)
