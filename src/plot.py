from .models import ProfileMatrix, SatProfError
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


def plot_distributions(matrix: ProfileMatrix, jitter=0.075, seed=0, title=None):
    names: list[str] = []
    data: list[list[float]] = []
    for node in matrix.node_order[1: ]:
        col: list[float] = matrix.filter_absents(node)
        if not col:
            continue
        names.append(node)
        data.append(col)

    if not data:
        raise SatProfError("no given data")

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
        
    for median in box["medians"]:
        median.set(color="#C0642F", linewidth=3.0)
        

    rng = random.Random(seed)
        
    for position, column in zip(pos, data):
        x = [position + rng.gauss(0.0, jitter) for _ in column]
        axes.scatter(x, column, s=13, marker="^" ,color="#3A6B8A", alpha=0.5, linewidths=0, zorder=3)
        
    axes.set_yscale("symlog", linthresh=1.0)
    axes.set_xticks(pos)
    axes.set_xticklabels([name for name in names], rotation=45, ha="right", fontsize=9)

    axes.grid(axis="y", color="#DDD8D0", linewidth=1.0)
    axes.set_axisbelow(True)

    for spine in ("top", "right"):
        axes.spines[spine].set_visible(False)

    trans = axes.get_xaxis_transform()
    for position, column in zip(pos, data):
        axes.text(position, 1.01, f"n={len(column)}", transform=trans, ha="center", va="bottom", fontsize=7, color="#7A7268")

    axes.set_ylabel("share of total runtime")
    axes.set_title(title or "Runtime share per profiling step", loc="left", pad=24)

    axes.legend(handles=[
        Patch(facecolor="#EDE7DC", edgecolor="#7A7268", label="IQR, whiskers 5-95%"),
        Line2D([0], [0], color="#C0642F", lw=3, label="median"),
        Line2D([0], [0], marker="^",  color="#3A6B8A", lw=0, alpha=0.5, label="single benchmark"),
        ], loc="upper right", frameon=False, fontsize=8)
        
    return fig


