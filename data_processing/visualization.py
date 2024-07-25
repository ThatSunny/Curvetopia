import numpy as np
import matplotlib.pyplot as plt

def plot(paths_xys, colors=None):
    """Visualizes the given paths.

    Args:
        paths_xys (list): A list of lists, where each inner list contains XY data for a path.
        colors (list, optional): A list of colors for the paths. Defaults to None, in which case a default color cycle is used.
    """

    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))

    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    for i, xys in enumerate(paths_xys):
        c = colors[i % len(colors)]
        for xy in xys:
            ax.plot(xy[:, 0], xy[:, 1], c=c, linewidth=2)

    ax.set_aspect('equal')
    plt.show()
