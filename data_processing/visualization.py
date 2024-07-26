import matplotlib.pyplot as plt
import numpy as np

def plot(paths_xys, colors=None):
    """
    Plots the given paths with the specified colors.
    
    Args:
    - paths_xys: List of lists of numpy arrays. Each inner list corresponds to a shape, 
      and each numpy array corresponds to a path defining a polyline.
    - colors: List of RGBA colors to use for each shape.
    """
    if colors is None:
        # Default to a repeating set of colors
        colors = plt.cm.viridis(np.linspace(0, 1, len(paths_xys)))

    fig, ax = plt.subplots(figsize=(8, 8))
    for i, xy_paths in enumerate(paths_xys):
        c = colors[i % len(colors)]
        for xy in xy_paths:
            ax.plot(xy[0], xy[1], color=c, linewidth=2)

    ax.set_aspect('equal')
    plt.show()
