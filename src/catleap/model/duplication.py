import sys
import json
import statistics
from scipy.stats import mannwhitneyu
from typing import NamedTuple

sys.path.append("../")

from stats import MileStastics
from constants import path
from graph import draw_boxplot
