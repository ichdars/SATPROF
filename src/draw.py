import graphviz
from .models import *
from .parse import create_benchmark
import math


def label_node(node: ProfilingNode) -> str:
    return f"{node.name}\n{node.time:.2f}s \n{node.percentage:.2f}%"


def calc_node_size(node: ProfilingNode, root: ProfilingNode) -> float:
    """
    function to calculate each nodes size relative to the solving time
    """

    frac: float = node.time / root.time
    size: float = 3 * math.sqrt(frac)
    return max(0.5, min(size, 4))


def shared_nodes(root: ProfilingNode) -> set[str]:
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


def draw_tree(dot, node, parent_id=None, drawn=None, shared=None, filled = False):
    """ function to draw the actual DAG, by identifieng which
    node has a single parent and which one has multiple
    drawn = set of strings of already drawn nodes
    """

    if node is None:
        return
    
    if drawn is None:
        drawn = set()
        shared = shared_nodes(node)
    
    node_id = node.name

    if node_id not in drawn:
        drawn.add(node_id)

        root       

        # size = calc_node_size(node, )
        
        if filled:
            dot.node(node_id,
                    label=label_node(node),
                    style="filled",
                    fillcolor=node.color,
                    fontcolor="black",
                    )
        else:
            dot.node(node_id,
                    label=label_node(node),
                    color=node.color,
                    fontcolor="black",
                    )
            

         
        for child in node.children:
            draw_tree(dot, child, node_id, drawn, shared, filled)


    if parent_id is not None:
        dot.edge(parent_id, node_id) 
