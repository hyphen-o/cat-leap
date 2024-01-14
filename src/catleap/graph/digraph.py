from graphviz import Digraph
from typing import NamedTuple


class FormattedState(NamedTuple):
    start: str
    end: str
    count: str
    is_remix_start: int
    is_remix_end: int


def draw_digraph(duplication_list: list, graph_name="graphs", min_duplication=2):
    G = Digraph(format="png")
    for duplication_dict in duplication_list:
        formatted_state = __format_state(duplication_dict)
        if int(formatted_state.count) > min_duplication:
            G.attr(
                "node",
                shape="circle",
                style="filled",
                weight="200",
                color="orange" if formatted_state.is_remix_end else "gray",
            )
            G.edge(
                formatted_state.start,
                formatted_state.end,
                label=formatted_state.count,
                color="red",
            )

    G.render(graph_name)


def __format_state(duplication_dict: dict):
    start = str(list(duplication_dict["Edge"]["StartP"].values()))
    is_remix_start = duplication_dict["Edge"]["StartP"]["IsRemix"]
    is_remix_end = 0
    end = ""
    if type(duplication_dict["Edge"]["EndP"]) is str:
        end = duplication_dict["Edge"]["EndP"]
    else:
        end = str(list(duplication_dict["Edge"]["EndP"].values()))
        is_remix_end = duplication_dict["Edge"]["EndP"]["IsRemix"]

    count = str(duplication_dict["Count"])

    return FormattedState(start, end, count, is_remix_start, is_remix_end)
