import numpy as np

def is_straight_line(points, tolerance=1e-2):
    """
    Checks if the given points form a straight line within a given tolerance.
    
    Args:
    - points: numpy array of shape (n, 2).
    - tolerance: maximum deviation from straightness.
    
    Returns:
    - bool: True if the points form a straight line.
    """
    # Vector from the first to the last point
    vector = points[-1] - points[0]
    vector_norm = np.linalg.norm(vector)
    
    if vector_norm < tolerance:
        return True  # Treat very small segments as lines
    
    # Normalize the vector
    vector /= vector_norm
    
    # Check if all points are collinear
    for i in range(1, len(points) - 1):
        test_vector = points[i] - points[0]
        test_vector_norm = np.linalg.norm(test_vector)
        
        if test_vector_norm < tolerance:
            continue
        
        test_vector /= test_vector_norm
        
        # Check if vectors are parallel (cross product is zero)
        if np.abs(np.cross(vector, test_vector)) > tolerance:
            return False

    return True

def segment_curve(path, segment_length_threshold=10):
    """
    Segments the curve into sub-segments based on the length threshold.
    
    Args:
    - path: numpy array of shape (n, 2).
    - segment_length_threshold: minimum length of a segment.
    
    Returns:
    - list: A list of segmented paths.
    """
    # Example implementation (simple segmentation)
    segments = []
    current_segment = [path[0]]
    for point in path[1:]:
        current_segment.append(point)
        segment_length = np.linalg.norm(point - current_segment[0])
        if segment_length >= segment_length_threshold:
            segments.append(np.array(current_segment))
            current_segment = [point]
    
    if len(current_segment) > 1:
        segments.append(np.array(current_segment))
    
    return segments
