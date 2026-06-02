import graphviz
from .models import *


def label_node(node: ProfilingNode) -> str:
    return f"{node.name}\n{node.time:.2f}s \n{node.percentage:.2f}%"

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


def draw_tree(dot, node, parent_id=None, counter=[0]):
    node_id = str(counter[0])
    counter[0] += 1

    if node is None:
        return

    label = f"{node.name}"
    dot.node(node_id, label=label)
 
    if parent_id is not None:
        dot.edge(parent_id, node_id)
 
    for child in node.children:
        draw_tree(dot, child, node_id, counter)
