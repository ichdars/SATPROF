from typing import TypeAlias, Optional
from .models import *
from .aggregate import write_outliers
from .parse import create_benchmark
import math


node: TypeAlias = ProfilingNode | AggregationNode


def label_node(node: node, min: float = 0, max: float = 0) -> str:
    if isinstance(node, ProfilingNode):
        return f"{node.name}\n{node.time:.2f}s \n{node.percentage:.2f}%"
    if isinstance(node, AggregationNode):
        return f"{node.name}\n{node.percentage:.2f}%\n ({min};{max}) \n{(node.present_count)} / {node.total_count}"


def calc_node_size(node: node, root: node) -> tuple[float, float]:
    """
    function to calculate each nodes size relative to the solving percentage
    """

    frac: float = node.percentage / root.percentage if root.percentage > 0 else 0.0
    size: float = math.sqrt(3 * frac)
    node_size: float = max(0.5, min(size, 3.5))
    font_size: float = max(10.0, min(25.0, 45.0 * frac))
    return node_size, font_size


def calc_edge_width(child: node, root: node) -> float:
    """
    function to calculate each edges width relative to the solving percentage
    """

    frac: float = child.percentage / root.percentage if root.percentage > 0.0 else 0.0
    width: float = math.sqrt(3 * frac)
    return max(0.5, min(width, 5.0))


def shared_nodes(root: node) -> set[str]:
    """
    function to evaluate which nodes have more then one parent node
    """

    inner_degrees: dict[str, int] = {}
    visited_edges: set[tuple[str, str]] = set()
    seen: set[str] = set()
    stack = [root]
    res: set[str] = set()

    # perform a depth first search to find the nodes with multiple parents
    while stack:
        current_node = stack.pop()
        if current_node.name in seen:
            continue
        seen.add(current_node.name)
        for child in current_node.children:
            current_edge = (current_node.name, child.name)
            if current_edge not in visited_edges:
                visited_edges.add(current_edge)
                inner_degrees[child.name] = inner_degrees.get(child.name, 0) + 1
            stack.append(child)

    for name, degree in inner_degrees.items():
        if degree > 1:
            res.add(name)
    return res


def draw_tree(dot, node, outliers: dict[str, Outlier] = {}, parent_id=None, drawn=None, shared=None, root: node | None = None):
    """
    function to draw the actual DAG, by identifieng which
    node has a single parent and which one has multiple
    drawn = set of strings of already drawn nodes
    """

    if node is None:
        return

    if drawn is None:
        drawn = set()
        shared = shared_nodes(node)

    node_id = node.name

    root_node = node if root is None else root

    if node_id not in drawn:
        drawn.add(node_id)

        node_size, font_size = calc_node_size(node, root_node)

        if isinstance(node, AggregationNode):
            outlier_data = outliers[node.name]

            dot.node(node_id,
                     label=label_node(node, outlier_data.min_val, outlier_data.max_val),
                     color=node.color,
                     fontcolor="black",
                     shape="rectangle",
                     fixedsize="shape",
                     height=f"{node_size:.2f}",
                     width=f"{node_size * 1.75:.2f}",
                     fontsize=f"{font_size:.0f}"
                     )
        else:
            dot.node(node_id,
                     label=label_node(node),
                     color=node.color,
                     fontcolor="black",
                     shape="rectangle",
                     fixedsize="shape",
                     height=f"{node_size:.2f}",
                     width=f"{node_size * 1.75:.2f}",
                     fontsize=f"{font_size:.0f}"
                     )

        for child in node.children:

            draw_tree(
                dot,
                child,
                outliers=outliers,
                parent_id=node_id,
                drawn=drawn,
                shared=shared,
                root=root_node,
            )
    
    write_outliers(outliers)

    if parent_id is not None:
        edge_width = calc_edge_width(node, root_node)
        dot.edge(parent_id, node_id, penwidth=f"{edge_width:.2f}")
