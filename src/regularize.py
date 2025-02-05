# src/regularize.py
import numpy as np
from scipy.optimize import least_squares
from sklearn.linear_model import RANSACRegressor
from scipy.spatial import ConvexHull

def fit_line(points):
    """
    Fit a straight line to a set of points using linear regression.
    
    Args:
        points (np.array): A numpy array of shape (N, 2) representing the points.
    
    Returns:
        tuple: (slope, intercept) of the fitted line.
    """
    x = points[:, 0]
    y = points[:, 1]
    A = np.vstack([x, np.ones(len(x))]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    return slope, intercept

def fit_circle(points):
    """
    Fit a circle to a set of points using RANSAC and least squares.
    
    Args:
        points (np.array): A numpy array of shape (N, 2) representing the points.
    
    Returns:
        tuple: (center_x, center_y, radius) of the fitted circle.
    """
    def residuals(c, points):
        return np.sqrt((points[:, 0] - c[0])**2 + (points[:, 1] - c[1])**2) - c[2]
    
    # Use RANSAC to remove outliers
    ransac = RANSACRegressor()
    X = points[:, 0].reshape(-1, 1)
    y = points[:, 1]
    ransac.fit(X, y)
    inlier_mask = ransac.inlier_mask_
    inliers = points[inlier_mask]
    
    # Initial guess for the center and radius
    center = np.mean(inliers, axis=0)
    radius = np.mean(np.sqrt((inliers[:, 0] - center[0])**2 + (inliers[:, 1] - center[1])**2))
    
    # Optimize using least squares
    result = least_squares(residuals, [center[0], center[1], radius], args=(inliers,))
    return result.x[0], result.x[1], result.x[2]

def fit_rectangle(points):
    """
    Fit a minimum area bounding rectangle to a set of points.
    
    Args:
        points (np.array): A numpy array of shape (N, 2) representing the points.
    
    Returns:
        tuple: (vertices) representing the vertices of the minimum area bounding rectangle.
    """
    # Compute the convex hull of the points
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]
    
    # Compute the minimum area bounding rectangle
    min_area = float('inf')
    min_rect = None
    
    for i in range(len(hull_points)):
        # Get two adjacent points on the convex hull
        p1 = hull_points[i]
        p2 = hull_points[(i + 1) % len(hull_points)]
        
        # Compute the direction vector of the edge
        edge_dir = p2 - p1
        edge_dir = edge_dir / np.linalg.norm(edge_dir)
        
        # Compute the normal vector (perpendicular to the edge)
        normal_dir = np.array([-edge_dir[1], edge_dir[0]])
        
        # Project all points onto the edge and normal directions
        edge_proj = np.dot(hull_points, edge_dir)
        normal_proj = np.dot(hull_points, normal_dir)
        
        # Find the min and max projections
        min_edge, max_edge = np.min(edge_proj), np.max(edge_proj)
        min_normal, max_normal = np.min(normal_proj), np.max(normal_proj)
        
        # Compute the area of the rectangle
        area = (max_edge - min_edge) * (max_normal - min_normal)
        
        # Update the minimum area rectangle
        if area < min_area:
            min_area = area
            min_rect = [
                p1 + (min_edge - np.dot(p1, edge_dir)) * edge_dir + (min_normal - np.dot(p1, normal_dir)) * normal_dir,
                p1 + (max_edge - np.dot(p1, edge_dir)) * edge_dir + (min_normal - np.dot(p1, normal_dir)) * normal_dir,
                p1 + (max_edge - np.dot(p1, edge_dir)) * edge_dir + (max_normal - np.dot(p1, normal_dir)) * normal_dir,
                p1 + (min_edge - np.dot(p1, edge_dir)) * edge_dir + (max_normal - np.dot(p1, normal_dir)) * normal_dir
            ]
    
    return np.array(min_rect)

def regularize_shapes(paths_XYs):
    """
    Regularize a list of polylines into basic geometric shapes.
    
    Args:
        paths_XYs (list): A list of polylines, where each polyline is a numpy array of points.
    
    Returns:
        list: A list of regularized shapes (lines, circles, rectangles, etc.).
    """
    regularized_shapes = []
    
    for XYs in paths_XYs:
        for XY in XYs:
            # Fit a line
            slope, intercept = fit_line(XY)
            regularized_shapes.append(("line", slope, intercept))
            
            # Fit a circle
            center_x, center_y, radius = fit_circle(XY)
            regularized_shapes.append(("circle", center_x, center_y, radius))
            
            # Fit a rectangle
            rectangle_vertices = fit_rectangle(XY)
            regularized_shapes.append(("rectangle", rectangle_vertices))
    
    return regularized_shapes