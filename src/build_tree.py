import json

from .models import *
import pathlib

def config_to_profling(config_node: dict, steps: dict[str, SolvingStep]) -> ProfilingNode:
    name: str = config_node["name"]
    children: list[ProfilingNode] = []
    ellapsed_time: float = 0.0
    percentage: float = 0.0

    if name in steps:
        ellapsed_time = steps[name].time
        percentage = steps[name].percentage

    for child in config_node["children"]:
        if child["name"] in steps:  
            children.append(config_to_profling(child, steps))
    
    color = config_node.get("color", "blue")
    
    return ProfilingNode(name,lvl=config_node["profiling_lvl"], time=ellapsed_time, percentage=percentage, color=color ,children=children)


def compare_log_to_config(steps: list[SolvingStep], config: dict):
    steps_dict = {step.name: step for step in steps}
    return  config_to_profling(config, steps_dict)


def load_configs(configs: pathlib.Path) -> dict[str, dict]:
    res: dict[str, dict] = {}
    p: pathlib.Path = pathlib.Path(configs)
    for config_path in p.glob("*.json"):
        with config_path.open(encoding="utf-8") as file:
            config = json.load(file)
            name = config.get("solver")        
            if name is None:
                raise ValueError()
            if name in res:
                raise ValueError("Solver is already configurated")
            res[name] = config
    return res
