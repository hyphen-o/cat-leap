import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns
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

    if len(props.nested_list) == 1:
      bp = ax.boxplot(props.nested_list[0], showmeans=True)
    else:
      bp = ax.boxplot(props.nested_list, showmeans=True, sym="",patch_artist=True)
      ax.set_xticklabels([props.xlabel, props.ylabel])

    bp['boxes'][0].set_color('lightblue')
    bp['boxes'][1].set_color('lightsalmon')

    for whisker in bp['whiskers']:
        whisker.set_color('#282828')

    for cap in bp['caps']:
        cap.set_color('#282828')

    for median in bp['medians']:
        median.set_color('#282828')

    for flier in bp['fliers']:
        flier.set(marker='o', color='red', alpha=0.5)

    ax.set_ylabel("ユーザのCTパス重複数")
    plt.title(props.title)
    plt.grid()
    plt.savefig(path.BOXPLOT + props.file_name)
