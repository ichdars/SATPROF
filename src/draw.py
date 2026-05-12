import graphviz
from .models import *

def build_tree(dot, node, parent_id=None, counter=[0]):
    node_id = str(counter[0])
    counter[0] += 1
 
    label = f"{node['name']}\n(lvl {node['profiling_lvl']})"
    dot.node(node_id, label=label)
 
    if parent_id is not None:
        dot.edge(parent_id, node_id)
 
    for child in node["children"]:
        build_tree(dot, child, node_id, counter)
