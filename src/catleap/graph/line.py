import matplotlib.pyplot as plt
import japanize_matplotlib
import sys

sys.path.append("../")

from constants import path


def draw_line(props):
    """props = {
          nested_list : List[list],
          xlabel : str,
          ylabel : str,
          title: str
          file_name: str
    }"""

    plt.plot(props.nested_list[0])
    plt.plot(props.nested_list[1])

    plt.ylabel(props.ylabel)
    plt.title(props.title)
    plt.grid(True)

    plt.savefig(path.LINE + props.file_name)
