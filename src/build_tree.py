from .models import *

def config_to_profling(config_node: dict, steps: dict[str, SolvingStep]) -> ProfilingNode:
    name: str = config_node["name"]
    children: list[ProfilingNode] = []
    ellapsed_time: float = 0.0
    percentage: float = 0.0

    if name in steps:
        ellapsed_time = steps[name].time
        percentage = steps[name].percentage

    for child in config_node["children"]:
        # if child["name"] in steps:  
        children.append(config_to_profling(child, steps))
    
    return ProfilingNode(name,lvl=config_node["profiling_lvl"], time=ellapsed_time, percentage=percentage, children=children)


def compare_log_to_config(steps: list[SolvingStep], config: dict):
    steps_dict = {step.name: step for step in steps}
    return  config_to_profling(config, steps_dict)