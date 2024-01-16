import matplotlib.pyplot as plt
import japanize_matplotlib
import sys

sys.path.append("../")
from constants import path


def draw_boxplot(props):
    """props = {
          nested_list : List[list],
          xlabel : str,
          ylabel : str,
          title: str
          file_name: str
    }"""

    flg, ax = plt.subplots()

    bp = ax.boxplot(props.nested_list, showmeans=True)
    ax.set_xticklabels([props.xlabel, props.ylabel])
    plt.title(props.title)
    plt.grid()
    plt.savefig(path.BOXPLOT + props.file_name)