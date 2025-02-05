# src/visualize.py
import numpy as np
import matplotlib.pyplot as plt

def plot_shapes(paths_XYs, title="Shapes", block=True):
    """
    Plot a list of polylines using Matplotlib.
    Args:
        paths_XYs (list): A list of polylines, where each polyline is a numpy array of points.
        title (str): Title of the plot.
        block (bool): If True, block execution until the plot window is closed.
    """
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    for i, XYs in enumerate(paths_XYs):
        c = colors[i % len(colors)]
        for XY in XYs:
            ax.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)
    ax.set_aspect('equal')
    ax.set_title(title)
    plt.show(block=block)


def plot_regularized_shapes(regularized_shapes, title="Regularized Shapes", block=True):
    """
    Plot regularized shapes (lines, circles, rectangles) using Matplotlib.
    Args:
        regularized_shapes (list): A list of regularized shapes.
        title (str): Title of the plot.
        block (bool): If True, block execution until the plot window is closed.
    """
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    for shape in regularized_shapes:
        if shape[0] == "line":
            # Plot a line
            slope, intercept = shape[1], shape[2]
            x = np.array([0, 300])  # Arbitrary x-range for the line
            y = slope * x + intercept
            ax.plot(x, y, 'r--', linewidth=2, label="Line")
        
        elif shape[0] == "circle":
            # Plot a circle
            center_x, center_y, radius = shape[1], shape[2], shape[3]
            circle = plt.Circle((center_x, center_y), radius, color='g', fill=False, linewidth=2, label="Circle")
            ax.add_artist(circle)
        
        elif shape[0] == "rectangle":
            # Plot a rectangle
            vertices = shape[1]
            rect = plt.Polygon(vertices, color='b', fill=False, linewidth=2, label="Rectangle")
            ax.add_artist(rect)
    
    ax.set_aspect('equal')
    ax.set_title(title)
    ax.legend()
    plt.show(block=block)


def plot_symmetry(shape, has_reflection, line_of_symmetry, has_rotation, angle_of_rotation):
    """Visualizes symmetry for a given shape."""
    shape_type = shape[0]
    plt.figure()

    if shape_type == "circle":
        center_x, center_y, radius = shape[1], shape[2], shape[3]
        angles = np.linspace(0, 2 * np.pi, 100)
        x = center_x + radius * np.cos(angles)
        y = center_y + radius * np.sin(angles)
        plt.plot(x, y, label="Circle")
        plt.plot(center_x, center_y, 'ro', label="Center")

        if has_reflection and line_of_symmetry:
            if "Horizontal" in line_of_symmetry:
                plt.axhline(y=center_y, color='g', linestyle='--', label="Horizontal Symmetry")
            if "Vertical" in line_of_symmetry:
                plt.axvline(x=center_x, color='b', linestyle='--', label="Vertical Symmetry")

        if has_rotation and angle_of_rotation == 360.0:
            plt.plot(center_x, center_y, 'go', markersize=8, label="360° Rotation Center")

    elif shape_type == "rectangle":
        points = np.array(shape[1])
        x = points[:, 0]
        y = points[:, 1]
        plt.plot(x, y, label="Rectangle")

        if has_reflection and line_of_symmetry:
            if "Horizontal" in line_of_symmetry:
                plt.axhline(y=np.mean(y), color='g', linestyle='--', label="Horizontal Symmetry")
            if "Vertical" in line_of_symmetry:
                plt.axvline(x=np.mean(x), color='b', linestyle='--', label="Vertical Symmetry")

        if has_rotation and angle_of_rotation:
            center_x = np.mean(x)
            center_y = np.mean(y)
            plt.plot(center_x, center_y, 'go', markersize=8, label=f"{angle_of_rotation}° Rotation Center")

    plt.title(f"Symmetry Visualization for {shape_type}")
    plt.legend()
    plt.axis('equal')
    plt.show(block=False)  # Important: Non-blocking to show multiple plots