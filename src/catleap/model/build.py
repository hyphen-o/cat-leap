import sys
import json
from tqdm import tqdm

sys.path.append("../")

from constants import path
from feature import FeatureBuilder

fB = FeatureBuilder("TRANS")
fB.extract_features()