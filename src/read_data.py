import numpy as np

def read_csv(csv_path):
    """
    Read a CSV file containing polylines and return a list of polylines.
    
    Args:
        csv_path (str): Path to the CSV file.
    
    Returns:
        list: A list of polylines, where each polyline is a numpy array of points.
    """
    # Read the CSV file into a numpy array
    np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
    
    # Initialize a list to store the polylines
    path_XYs = []
    
    # Loop through unique path IDs (first column in the CSV)
    for i in np.unique(np_path_XYs[:, 0]):
        # Extract points for the current path ID
        npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
        XYs = []
        
        # Loop through unique segment IDs (second column in the CSV)
        for j in np.unique(npXYs[:, 0]):
            # Extract points for the current segment ID
            XY = npXYs[npXYs[:, 0] == j][:, 1:]
            XYs.append(XY)
        
        # Add the polyline to the list
        path_XYs.append(XYs)
    
    return path_XYs