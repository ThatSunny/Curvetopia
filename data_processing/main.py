import read_csv
import visualization
import matplotlib.colors as mcolors
from curve_processing import segment_curve

def main():
    csv_file_path = "./problems/problems/frag0.csv"
    paths_xys = read_csv.read_csv(csv_file_path)

    colors = [mcolors.to_rgba(c) for c in ['red', 'green', 'blue']]

    segmented_paths = []
    for path in paths_xys:
        segments = segment_curve(path, segment_length_threshold=10)  # Adjust threshold as needed
        segmented_paths.extend(segments)

    visualization.plot(paths_xys, colors=colors)


if __name__ == "__main__":
    main()