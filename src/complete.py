# src/complete.py
import numpy as np
from scipy.interpolate import splprep, splev

def complete_curve(points, tolerance=1e-2):
    """
    Complete an incomplete curve by interpolating gaps.
    
    Args:
        points (np.array): A numpy array of shape (N, 2) representing the points.
        tolerance (float): Tolerance for identifying gaps.
    
    Returns:
        np.array: Completed curve as a numpy array of shape (M, 2).
    """
    # Calculate the Euclidean distance between consecutive points
    distances = np.linalg.norm(np.diff(points, axis=0), axis=1)
    
    # Identify gaps where the distance between points is larger than the tolerance
    gap_indices = np.where(distances > tolerance)[0]
    
    # If no gaps are found, return the original points
    if len(gap_indices) == 0:
        return points
    
    # Split the points into segments at the gaps
    segments = np.split(points, gap_indices + 1)
    
    # Interpolate each segment separately
    completed_points = []
    for segment in segments:
        if len(segment) < 2:
            continue  # Skip segments with fewer than 2 points
        
        # Fit a spline to the segment
        tck, _ = splprep(segment.T, s=0)  # s=0 ensures interpolation (no smoothing)
        u_new = np.linspace(0, 1, 100)  # Generate 100 points for the completed segment
        x_new, y_new = splev(u_new, tck)
        completed_segment = np.column_stack((x_new, y_new))
        
        # Add the completed segment to the result
        completed_points.append(completed_segment)
    
    # If no segments were added, return the original points
    if len(completed_points) == 0:
        return points
    
    # Combine all completed segments into a single curve
    return np.vstack(completed_points)