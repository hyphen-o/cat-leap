from graphviz import Digraph
from typing import NamedTuple


class FormattedState(NamedTuple):
    start: str
    end: str
    count: str
    euclid: float
    is_remix_start: int
    is_remix_end: int
    feature_start: list
    feature_end: list


def draw_digraph(duplication_list: list, graph_name="graphs", min_duplication=2):
    G = Digraph(format="png")
    for duplication_dict in duplication_list:
        formatted_state = __format_state(duplication_dict)
        if int(formatted_state.count) > min_duplication:
            if formatted_state.euclid >= 0.0:
                G.node(
                    formatted_state.start,
                    formatted_state.start,
                    color="orange" if formatted_state.is_remix_start else "black",
                )
                G.node(
                    formatted_state.end,
                    formatted_state.end,
                    color="orange" if formatted_state.is_remix_end else "black",
                )
                G.edge(
                    formatted_state.start,
                    formatted_state.end,
                    label=formatted_state.count,
                    weight=formatted_state.count,
                    color="red",
                )

    G.render(graph_name)


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

    count = str(duplication_dict["Count"])
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
