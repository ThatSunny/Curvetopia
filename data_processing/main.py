import read_csv
import numpy as np
import visualization
import matplotlib.colors as mcolors
from curve_processing import segment_curve
from symmetry_detection import has_reflection_symmetry, has_rotational_symmetry
from curve_completion import complete_curve_symmetry, complete_curve_interpolation, complete_curve_extrapolation, complete_curve

def main():
    csv_file_path = "./problems/problems/frag2.csv"
    paths_xys = read_csv.read_csv(csv_file_path)

    colors = [mcolors.to_rgba(c) for c in ['red', 'green', 'blue']]

    segmented_paths = []
    completed_paths = []

    for path in paths_xys:
        segments = segment_curve(path, segment_length_threshold=20)  # Adjust threshold as needed
        segmented_paths.extend(segments)
        completed_paths = complete_curve(path)

    # Detect refletion symmetry for each segment
    for segment in segments:
        symmetry_axes = has_reflection_symmetry(segment)
        print(f"Detected symmetry axes: {symmetry_axes}")

        # Complete the curve only if symmetry is detected
        if symmetry_axes:
            completed_segment = complete_curve_symmetry(segment, symmetry_axes)
            completed_segment = complete_curve_interpolation(completed_segment)
            completed_segment = complete_curve_extrapolation(completed_segment)
        else:
            completed_segment = segment.copy()  # Avoid modifying original
    
    visualization.plot(paths_xys, colors=colors)
    # visualization.plot(completed_paths, colors=['purple'] * len(completed_paths))


if __name__ == "__main__":
    main()