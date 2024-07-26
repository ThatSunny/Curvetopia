import numpy as np
from scipy.spatial import KDTree

def reflect_point_across_line(point, line_point1, line_point2):
    """
    Reflect a point across a line defined by two points.

    Args:
    - point: The point to reflect as a numpy array (x, y).
    - line_point1: First point on the line as a numpy array (x, y).
    - line_point2: Second point on the line as a numpy array (x, y).

    Returns:
    - numpy array: The reflected point.
    """
    # Vector of the line
    line_vec = line_point2 - line_point1
    line_vec = line_vec.astype(np.float64)  # Ensure line_vec is a float type
    line_vec /= np.linalg.norm(line_vec)  # Normalize the line vector

    # Vector from line_point1 to the point
    point_vec = point - line_point1
    point_vec = point_vec.astype(np.float64)  # Ensure point_vec is a float type

    # Project the point vector onto the line vector
    proj_length = np.dot(point_vec, line_vec)
    proj_point = line_point1 + proj_length * line_vec

    # Calculate the reflected point
    reflected_point = 2 * proj_point - point
    return reflected_point

def has_reflection_symmetry(points, tolerance=1e-6):
    """
    Check if a given set of points has reflection symmetry.

    Args:
    - points: numpy array of shape (n, 2).
    - tolerance: float, maximum deviation for point matching.

    Returns:
    - list of tuples: Each tuple contains two points defining an axis of symmetry.
    """
    symmetry_axes = []

    n_points = len(points)
    kd_tree = KDTree(points)

    for i in range(n_points):
        for j in range(i + 1, n_points):
            # Check symmetry across the line through points[i] and points[j]
            midpoint = (points[i] + points[j]) / 2
            line_vec = points[j] - points[i]

            perpendicular_vec = np.array([-line_vec[1], line_vec[0]], dtype=np.float64)  # Perpendicular vector
            perpendicular_vec /= np.linalg.norm(perpendicular_vec)  # Normalize

            # Check symmetry for each point
            symmetric = True
            for point in points:
                reflected_point = reflect_point_across_line(point, midpoint, midpoint + perpendicular_vec)
                if not any(kd_tree.query_ball_point(reflected_point, tolerance)):
                    symmetric = False
                    break

            if symmetric:
                symmetry_axes.append((points[i], points[j]))

    return symmetry_axes

def has_rotational_symmetry(points, n_fold=2, tolerance=1e-2):
    """
    Check if a given set of points has rotational symmetry.

    Args:
    - points: numpy array of shape (n, 2).
    - n_fold: integer, the number of folds in the rotational symmetry (e.g., 2 for 180-degree symmetry).
    - tolerance: float, maximum deviation for point matching.

    Returns:
    - bool: True if the points have n-fold rotational symmetry.
    """
    centroid = np.mean(points, axis=0)
    angle = 2 * np.pi / n_fold

    # Rotation matrix for the given angle
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                [np.sin(angle), np.cos(angle)]])

    kd_tree = KDTree(points)

    for fold in range(1, n_fold):
        rotated_points = (points - centroid) @ np.linalg.matrix_power(rotation_matrix, fold) + centroid

        for point in rotated_points:
            if not any(kd_tree.query_ball_point(point, tolerance)):
                return False

    return True
