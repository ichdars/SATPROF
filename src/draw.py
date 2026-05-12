import graphviz
from .models import *

def tree_to_dot(tree: ProfilingNode, dot: graphviz.Digraph=None) -> graphviz.Digraph: # type: ignore
    if dot is None:
        dot = graphviz.Digraph()
    
    dot.node(tree.name, label=f"{tree.name}\n{tree.time:.2f}s")


    for child in tree.children:
        dot.edge(tree.name, child.name)
        tree_to_dot(child, dot)
    return dot