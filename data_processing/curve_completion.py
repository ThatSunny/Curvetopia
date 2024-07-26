import numpy as np
from scipy.interpolate import interp1d
from symmetry_detection import has_reflection_symmetry, has_rotational_symmetry
from curve_processing import segment_curve
from visualization import plot

def complete_curve_symmetry(points, symmetry_axes):
    """
    Complete the curve using detected symmetry axes.

    Args:
    - points: numpy array of shape (n, 2), original points of the curve.
    - symmetry_axes: list of tuples, each containing two points defining an axis of symmetry.

    Returns:
    - numpy array: Completed curve points.
    """
    completed_curve = points.copy()

    for axis in symmetry_axes:
        # Reflect existing points across the symmetry axis to generate missing parts
        line_point1, line_point2 = axis
        for point in points:
            reflected_point = reflect_point_across_line(point, line_point1, line_point2)
            # Add the reflected point to the curve if it doesn't already exist
            if not any(np.allclose(reflected_point, p) for p in completed_curve):
                completed_curve = np.vstack([completed_curve, reflected_point])
    
    return completed_curve

def complete_curve_interpolation(points, gap_tolerance=5):
    """
    Complete the curve using interpolation for small gaps.

    Args:
    - points: numpy array of shape (n, 2).
    - gap_tolerance: Maximum number of consecutive missing points to interpolate.

    Returns:
    - numpy array: Completed curve points with interpolated gaps.
    """
    # Sort points by x-coordinate
    points = points[np.argsort(points[:, 0])]
    
    completed_curve = points.copy()
    x_coords, y_coords = points[:, 0], points[:, 1]

    # Check for gaps in x-coordinates and interpolate
    for i in range(len(x_coords) - 1):
        if x_coords[i+1] - x_coords[i] > gap_tolerance:
            # Linear interpolation
            interp_x = np.linspace(x_coords[i], x_coords[i+1], num=int((x_coords[i+1] - x_coords[i])))
            interp_y = interp1d(x_coords[i:i+2], y_coords[i:i+2], kind='linear')(interp_x)
            interp_points = np.column_stack((interp_x, interp_y))

            completed_curve = np.vstack([completed_curve, interp_points])

    # Sort and return the completed curve
    completed_curve = completed_curve[np.argsort(completed_curve[:, 0])]
    return completed_curve

def complete_curve_extrapolation(points, extend_factor=1.5):
    """
    Complete the curve by extrapolating its endpoints.

    Args:
    - points: numpy array of shape (n, 2).
    - extend_factor: Factor by which to extend the curve's endpoints.

    Returns:
    - numpy array: Completed curve with extrapolated endpoints.
    """
    # Sort points by x-coordinate
    points = points[np.argsort(points[:, 0])]
    start_point, end_point = points[0], points[-1]
    curve_vector = end_point - start_point

    # Extend start and end points
    extended_start = start_point - extend_factor * curve_vector
    extended_end = end_point + extend_factor * curve_vector

    completed_curve = np.vstack([extended_start, points, extended_end])
    return completed_curve

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
    line_vec /= np.linalg.norm(line_vec)  # Normalize the line vector

    # Vector from line_point1 to the point
    point_vec = point - line_point1

    # Project the point vector onto the line vector
    proj_length = np.dot(point_vec, line_vec)
    proj_point = line_point1 + proj_length * line_vec

    # Calculate the reflected point
    reflected_point = 2 * proj_point - point
    return reflected_point

def complete_curve(curve):
  """
  Completes a curve based on detected symmetry.

  Args:
      curve: A numpy array representing the curve data points (x, y).

  Returns:
      A numpy array representing the completed curve.
  """
  segments = segment_curve(curve)
  completed_paths = []
  
  for segment in segments:
    symmetry_axes = has_reflection_symmetry(segment)
    
    if symmetry_axes:
      completed_segment = complete_curve_symmetry(segment, symmetry_axes)
      completed_segment = complete_curve_interpolation(completed_segment)
      completed_segment = complete_curve_extrapolation(completed_segment)
    else:
      completed_segment = segment.copy()
    
    completed_paths.append(completed_segment)
  
  return completed_paths