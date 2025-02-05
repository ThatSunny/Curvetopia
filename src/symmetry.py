# src/symmetry.py
import numpy as np

def detect_reflection_symmetry(points, tolerance=0.05):
    """
    Detect reflection symmetry in a set of points.
    """
    centroid = np.mean(points, axis=0)
    centered_points = points - centroid

    cov_matrix = np.cov(centered_points, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

    vertical_symmetry = False
    horizontal_symmetry = False

    # Check for vertical symmetry (reflection over y-axis)
    x_mirror = np.array([[-1, 0], [0, 1]])
    mirrored_x = centered_points @ x_mirror
    if np.allclose(np.sort(mirrored_x, axis=0), np.sort(centered_points, axis=0), atol=tolerance):
        vertical_symmetry = True

    # Check for horizontal symmetry (reflection over x-axis)
    y_mirror = np.array([[1, 0], [0, -1]])
    mirrored_y = centered_points @ y_mirror
    if np.allclose(np.sort(mirrored_y, axis=0), np.sort(centered_points, axis=0), atol=tolerance):
        horizontal_symmetry = True

    # Return results
    if vertical_symmetry and horizontal_symmetry:
        return True, "Both Vertical & Horizontal symmetry"
    elif vertical_symmetry:
        return True, "Vertical symmetry"
    elif horizontal_symmetry:
        return True, "Horizontal symmetry"

    return False, None


def detect_rotational_symmetry(points, tolerance=0.05):
    """Detect rotational symmetry."""
    centroid = np.mean(points, axis=0)
    centered_points = points - centroid

    # Calculate eigenvalues for rotational symmetry detection more robustly
    cov_matrix = np.cov(centered_points, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
    eigenvalues = np.sort(eigenvalues) # Sort eigenvalues for comparison

    # Improved check for near-equal eigenvalues, indicating circular symmetry
    if np.abs(eigenvalues[0] - eigenvalues[1]) < tolerance * np.mean(eigenvalues): # Relative tolerance
        return True, 360.0  # Full rotational symmetry for a circle

    # Check for other rotational symmetries (180°, 90°)
    rotated_180 = -centered_points
    if np.allclose(np.sort(rotated_180, axis=0), np.sort(centered_points, axis=0), atol=tolerance):
        return True, 180.0

    rotation_90 = np.array([0, -1, 1, 0]).reshape(2,2) @ centered_points.T # Use matrix multiplication directly
    if np.allclose(np.sort(rotation_90.T, axis=0), np.sort(centered_points, axis=0), atol=tolerance):
        return True, 90.0

    return False, None