from .models import *
import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
matplotlib.use("Agg")



def plot_distributions(matrix: ProfileMatrix, jitter=0.075, seed=0):
    names: list[str] = []
    data: list[list[float]] = []
    for node in matrix.node_order[1: ]:
        col: list[float] = matrix.filter_zeros(node)
        if not col:
            continue
        names.append(node)
        data.append(col)

        fig, axes = plt.subplots(figsize=(1.05 * len(names) + 2.5, 6.5),
                                    constrained_layout=True)
        
        pos: list[int] = list(range(len(names)))

        box = axes.boxplot(data,
                           positions=pos,
                           widths=0.55,
                           whis=(5, 95),
                           showfliers=False,
                           patch_artist=True
        )

        for patch in box["boxes"]:
            patch.set(facecolor="#EDE7DC", edgecolor="#7A7268", linewidth=1.0)

        for key in ("whiskers", "caps"):
            for element in box[key]:
                element.set(color="#7A7268", linewidth=1.0)
        
        for median in box["median"]:
            median.set(color="#C0642F", linewidth=3.0)
        

        rng = random.Random(seed)
        
        for position, column in zip(pos, data):
            x = [position + rng.gauss(0.0, jitter) for _ in column]
            axes.scatter(x, column, s=13, color="#3A6B8A", alpha=0.5, linewidths=0, zorder=3)
        
        axes.set_yscale("symlog", linthresh=1.0)
        axes.set_xticks(pos)
        axes.set_xticklabels([name for name in names], rotation=45, ha="right", fontsize=9)

        axes.grid(axis="y", color="#DDD8D0", linewidth=1.0)
        axes.set_axisbelow(True)

        for spine in ("top", "right"):
            axes.spines[spine].set_visible(False)
        
        return fig


