import numpy as np

csv_path = '/problems/problems'

def read_csv(csv_path):
    """Reads a CSV file and extracts path and XY data.

    Args:
        csv_path (str): Path to the CSV file.

    Returns:
        list: A list of lists, where each inner list contains XY data for a path.
    """

    np_path_xys = np.genfromtxt(csv_path, delimiter=',')
    path_xys = []

    for path_id in np.unique(np_path_xys[:, 0]):
        np_xys = np_path_xys[np_path_xys[:, 0] == path_id][:, 1:]
        xys = []

        for point_id in np.unique(np_xys[:, 0]):
            xy = np_xys[np_xys[:, 0] == point_id][:, 1:]
            xys.append(xy)

        path_xys.append(xys)

    return path_xys
