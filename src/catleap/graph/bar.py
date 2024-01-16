import matplotlib.pyplot as plt
import japanize_matplotlib
import sys

sys.path.append("../")

from constants import path


def draw_bar(props):
    """props = {
          nested_list : List[list],
          xlabel : str,
          ylabel : str,
          title: str
          file_name: str
    }"""

    plt.bar(props.x, props.y, color="blue")

    plt.xlabel(props.xlabel)
    plt.ylabel(props.ylabel)
    plt.title(props.title)
    plt.grid(True)

    plt.savefig(path.BAR + props.file_name)
