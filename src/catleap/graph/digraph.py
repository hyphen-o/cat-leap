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
    euclid: float
    is_remix_start: int
    is_remix_end: int
    feature_start: list
    feature_end: list


def draw_digraph(duplication_list: list, graph_name="graphs", min_duplication=2):
    dot = Digraph(format="png")
    G = nx.Graph()
    for duplication_dict in duplication_list:
        formatted_state = __format_state(duplication_dict)
        if int(formatted_state.count) > min_duplication:
            if formatted_state.euclid >= 0.0:
                dot.node(
                    formatted_state.start,
                    formatted_state.start,
                    color="orange" if formatted_state.is_remix_start else "black",
                )
                dot.node(
                    formatted_state.end,
                    formatted_state.end,
                    color="orange" if formatted_state.is_remix_end else "black",
                )
                dot.edge(
                    formatted_state.start,
                    formatted_state.end,
                    label=str(formatted_state.count),
                    color="red",
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
    euclid = duplication_dict["Euclid"]

    return FormattedState(
        start,
        end,
        count,
        is_remix_start,
        is_remix_end,
        euclid,
        feature_start,
        feature_end,
    )
