from graphviz import Digraph
import networkx as nx
import json
import community
from typing import NamedTuple
import sys

sys.path.append("../")
from constants import path


class FormattedState(NamedTuple):
    start: str
    end: str
    count: int
    is_remix_start: int
    is_remix_end: int
    feature_start: list
    feature_end: list


def draw_digraph(duplication_list: list, graph_name="graphs", min_duplication=2):
    dot = Digraph(format="png")
    G = nx.Graph()
    dot.attr("node", shape="circle")
    for duplication_dict in duplication_list:
        formatted_state = __format_state(duplication_dict)
        if int(formatted_state.count) > min_duplication:
            # if formatted_state.euclid >= 0.0:
            dot.node(
                formatted_state.start,
                get_mark(duplication_dict["Edge"]["StartP"]["Mark"]),
                color="#282828",
            )
            dot.node(
                formatted_state.end,
                get_mark(
                    duplication_dict["Edge"]["EndP"]["Mark"]
                    if duplication_dict["Edge"]["EndP"] != "NEXT_LEVEL"
                    else "END"
                ),
                color="#282828",
            )
            dot.edge(
                formatted_state.start,
                formatted_state.end,
                color="darkblue",
            )
            G.add_node(
                formatted_state.start,
                features=formatted_state.feature_start,
            )
            G.add_node(
                formatted_state.end,
                features=formatted_state.feature_end,
            )
            G.add_edge(
                formatted_state.start,
                formatted_state.end,
                label=formatted_state.count,
                weight=formatted_state.count,
            )

    dot.render(path.DIGRAPH + graph_name)
    # Louvain法によるコミュニティ抽出
    communities = community.best_partition(G, weight="weight")

    # 結果の表示
    with open(f"{graph_name}.json", "w") as f:
        json.dump(communities, f, indent=2)


def get_mark(num: int):
    # dict = {
    #     "0": "A",
    #     "1": "B",
    #     "2": "C",
    #     "3": "D",
    #     "4": "E",
    #     "5": "F",
    #     "6": "G",
    #     "7": "H",
    #     "8": "I",
    #     "9": "J",
    #     "10": "K",
    #     "11": "L",
    #     "12": "M",
    #     "13": "N",
    #     "14": "O",
    #     "15": "P",
    #     "16": "Q",
    #     "17": "R",
    #     "18": "S",
    #     "19": "T",
    #     "20": "U",
    #     "21": "V",
    #     "22": "W",
    #     "23": "X",
    #     "24": "Y",
    #     "25": "Z",
    #     "26": "a",
    #     "27": "b",
    #     "28": "c",
    #     "29": "d",
    #     "30": "e",
    #     "31": "f",
    #     "32": "g",
    #     "33": "h",
    #     "34": "i",
    #     "35": "j",
    #     "36": "k",
    #     "37": "l",
    #     "38": "m",
    #     "END": ""
    # }

    dict = {
        "0": "A",
        "1": "B",
        "2": "C",
        "3": "D",
        "4": "E",
        "5": "F",
        "6": "G",
        "7": "H",
        "8": "I",
        "9": "J",
        "10": "K",
        "11": "L",
        "12": "M",
        "13": "N",
        "14": "O",
        "15": "P",
        "16": "Q",
        "17": "R",
        "18": "S",
        "19": "T",
        "20": "U",
        "21": "V",
        "22": "W",
        "23": "X",
        "24": "Y",
        "25": "Z",
        "26": "a",
        "33": "b",
        "36": "c",
        "37": "d",
        "38": "e",
        "39": "f",
        "40": "g",
        "42": "h",
        "43": "i",
        "44": "j",
        "45": "k",
        # "37": "l",
        # "38": "m",
        "END": "",
    }
    if str(num) not in dict.keys():
        return "-"

    return dict[str(num)]


def __format_state(duplication_dict: dict):
    start = str(list(duplication_dict["Edge"]["StartP"].values()))
    is_remix_start = int(duplication_dict["Edge"]["StartP"]["IsRemix"])
    is_remix_end = 0
    feature_start = duplication_dict["Edge"]["StartP"]["Feature"]
    feature_end = []

    end = ""
    if type(duplication_dict["Edge"]["EndP"]) is str:
        end = duplication_dict["Edge"]["EndP"]
    else:
        end = str(list(duplication_dict["Edge"]["EndP"].values()))
        is_remix_end = int(duplication_dict["Edge"]["EndP"]["IsRemix"])
        feature_end = duplication_dict["Edge"]["EndP"]["Feature"]

    count = duplication_dict["Count"]
    # euclid = duplication_dict["Euclid"]

    return FormattedState(
        start,
        end,
        count,
        is_remix_start,
        is_remix_end,
        feature_start,
        feature_end,
    )
